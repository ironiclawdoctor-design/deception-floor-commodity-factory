#!/usr/bin/env python3
"""
grok.py — xAI Grok Search Skill
Importable Python module + CLI for web and X/Twitter search via xAI's API.

Features:
  - Exponential backoff with jitter (fixer pattern)
  - Structured GrokResult dataclass with typed citations
  - SQLite caching via agency.db (pyresearch pattern)
  - Cost tracking logged to agency.db
  - Full argparse CLI: python3 grok.py "query" --mode web|x --json
  - Importable: from skills.grok.grok import search_web, search_x, GrokResult

Usage (CLI):
  python3 grok.py "latest AI regulation news" --mode web
  python3 grok.py "OpenAI reactions" --mode x --from-date 2025-01-01
  python3 grok.py "SpaceX launch" --mode web --domains spacex.com nasa.gov --json
  python3 grok.py "Elon Musk" --mode x --handles elonmusk --json

Usage (module):
  from skills.grok.grok import search_web, search_x, GrokResult
  result = search_web("AI regulation latest", api_key="xai-...")
  print(result.content)
  for cite in result.citations:
      print(cite.format_markdown())
"""

import os
import sys
import json
import time
import random
import hashlib
import sqlite3
import argparse
import urllib.request
import urllib.error
from dataclasses import dataclass, field, asdict
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional, List, Dict, Any

# ── Constants ──────────────────────────────────────────────────────────────────

XAI_API_BASE = "https://api.x.ai/v1"
XAI_RESPONSES_ENDPOINT = f"{XAI_API_BASE}/responses"

# grok-3 family supports live search; grok-2 does not
LIVE_SEARCH_MODELS = {
    "grok-3",
    "grok-3-fast",
    "grok-3-mini",
    "grok-3-mini-fast",
    # Legacy — included for compatibility; may not support live search
    "grok-2-1212",
}
DEFAULT_MODEL = "grok-3-fast"  # Fast + live search enabled

AGENCY_DB = Path("/root/.openclaw/workspace/agency.db")
CACHE_TTL_HOURS = 1  # Live search results stale after 1 hour

# Cost estimates (USD per 1k tokens, approximate xAI pricing)
COST_PER_1K_INPUT = 0.000003   # $3/M input tokens
COST_PER_1K_OUTPUT = 0.000015  # $15/M output tokens

# ── Error Classification ────────────────────────────────────────────────────────

class GrokError(Exception):
    def __init__(self, code: int, title: str, detail: str, retryable: bool = False):
        self.code = code
        self.title = title
        self.detail = detail
        self.retryable = retryable
        super().__init__(f"[{code}] {title}: {detail}")

def classify_error(status: int, body: str) -> GrokError:
    if status == 401:
        return GrokError(401, "Unauthorized", "Check XAI_API_KEY — invalid or missing", retryable=False)
    if status == 403:
        return GrokError(403, "Forbidden", body[:200], retryable=False)
    if status == 404:
        return GrokError(404, "Not Found", "Endpoint not found — check API base URL", retryable=False)
    if status == 409:
        return GrokError(409, "Conflict", body[:200], retryable=False)
    if status == 422:
        return GrokError(422, "Schema Error", body[:500], retryable=False)
    if status == 429:
        return GrokError(429, "Rate Limited", "Too many requests — backing off", retryable=True)
    if status >= 500:
        return GrokError(status, "Server Error", body[:200], retryable=True)
    return GrokError(status, "Unknown Error", body[:200], retryable=False)

# ── Data Structures ─────────────────────────────────────────────────────────────

@dataclass
class Citation:
    url: str = ""
    title: str = ""
    snippet: str = ""
    index: int = 0

    def format_markdown(self, max_snippet: int = 120) -> str:
        """Return formatted markdown citation string."""
        snippet = self.snippet[:max_snippet] + "…" if len(self.snippet) > max_snippet else self.snippet
        title = self.title or "Source"
        parts = [f"[{self.index}] [{title}]({self.url})"]
        if snippet:
            parts.append(f"   > {snippet}")
        return "\n".join(parts)

    def format_plain(self) -> str:
        """Return plain text citation."""
        snippet = self.snippet[:120] + "…" if len(self.snippet) > 120 else self.snippet
        return f"{self.index}. {self.title or 'Untitled'}\n   {self.url}\n   {snippet}"


@dataclass
class GrokResult:
    content: str = ""
    citations: List[Citation] = field(default_factory=list)
    search_type: str = "web"  # "web" or "x"
    model: str = DEFAULT_MODEL
    query: str = ""
    timestamp: str = ""
    search_performed: bool = False  # True if live search was actually executed
    cache_hit: bool = False
    usage: Dict[str, Any] = field(default_factory=dict)
    cost_usd: float = 0.0
    error: Optional[str] = None

    def __post_init__(self):
        if not self.timestamp:
            self.timestamp = datetime.utcnow().isoformat() + "Z"

    def format_citations_markdown(self) -> str:
        """Return all citations as numbered markdown list."""
        if not self.citations:
            return ""
        return "\n\n---\n**Sources:**\n" + "\n".join(c.format_markdown() for c in self.citations)

    def format_citations_plain(self) -> str:
        """Return all citations as plain text numbered list."""
        if not self.citations:
            return ""
        lines = ["─" * 60, "Sources:", "─" * 60]
        lines += [c.format_plain() for c in self.citations]
        return "\n".join(lines)

    def to_dict(self) -> dict:
        d = asdict(self)
        d["citations"] = [asdict(c) for c in self.citations]
        return d

    def to_json(self, indent: int = 2) -> str:
        return json.dumps(self.to_dict(), indent=indent, ensure_ascii=False)


# ── Cache Layer ─────────────────────────────────────────────────────────────────

class GrokCache:
    """SQLite-backed cache using agency.db. Cache-first, TTL-aware."""

    def __init__(self, db_path: Path = AGENCY_DB):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        try:
            conn = sqlite3.connect(self.db_path)
            conn.executescript("""
                CREATE TABLE IF NOT EXISTS grok_cache (
                    key TEXT PRIMARY KEY,
                    query TEXT,
                    search_type TEXT,
                    result_json TEXT,
                    cached_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    expires_at TEXT,
                    hit_count INTEGER DEFAULT 0
                );
                CREATE TABLE IF NOT EXISTS grok_call_log (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    ts TEXT DEFAULT CURRENT_TIMESTAMP,
                    query TEXT,
                    search_type TEXT,
                    model TEXT,
                    cache_hit INTEGER DEFAULT 0,
                    input_tokens INTEGER DEFAULT 0,
                    output_tokens INTEGER DEFAULT 0,
                    cost_usd REAL DEFAULT 0,
                    error TEXT
                );
            """)
            conn.commit()
            conn.close()
        except Exception:
            pass  # Cache is optional — don't crash if DB unavailable

    def _key(self, query: str, search_type: str, opts_hash: str = "") -> str:
        raw = f"{search_type}:{query}:{opts_hash}"
        return hashlib.sha256(raw.encode()).hexdigest()[:16]

    def get(self, query: str, search_type: str, opts_hash: str = "") -> Optional[GrokResult]:
        try:
            k = self._key(query, search_type, opts_hash)
            conn = sqlite3.connect(self.db_path)
            row = conn.execute(
                "SELECT result_json, expires_at FROM grok_cache WHERE key=?", (k,)
            ).fetchone()
            conn.close()
            if not row:
                return None
            result_json, expires_at = row
            if expires_at and datetime.fromisoformat(expires_at) < datetime.utcnow():
                return None  # expired
            # Update hit count
            conn = sqlite3.connect(self.db_path)
            conn.execute("UPDATE grok_cache SET hit_count=hit_count+1 WHERE key=?", (k,))
            conn.commit()
            conn.close()
            d = json.loads(result_json)
            citations = [Citation(**c) for c in d.pop("citations", [])]
            result = GrokResult(**d, citations=citations)
            result.cache_hit = True
            return result
        except Exception:
            return None

    def set(self, query: str, search_type: str, result: GrokResult,
            ttl_hours: int = CACHE_TTL_HOURS, opts_hash: str = ""):
        try:
            k = self._key(query, search_type, opts_hash)
            expires = (datetime.utcnow() + timedelta(hours=ttl_hours)).isoformat()
            conn = sqlite3.connect(self.db_path)
            conn.execute("""
                INSERT OR REPLACE INTO grok_cache (key, query, search_type, result_json, expires_at)
                VALUES (?,?,?,?,?)
            """, (k, query[:500], search_type, result.to_json(indent=None), expires))
            conn.commit()
            conn.close()
        except Exception:
            pass

    def log_call(self, query: str, search_type: str, model: str,
                 cache_hit: bool, usage: dict, cost_usd: float, error: str = ""):
        try:
            conn = sqlite3.connect(self.db_path)
            conn.execute("""
                INSERT INTO grok_call_log (query, search_type, model, cache_hit,
                    input_tokens, output_tokens, cost_usd, error)
                VALUES (?,?,?,?,?,?,?,?)
            """, (
                query[:200], search_type, model, int(cache_hit),
                usage.get("input_tokens", 0),
                usage.get("output_tokens", 0),
                cost_usd, error[:500] if error else ""
            ))
            conn.commit()
            conn.close()
        except Exception:
            pass


# ── Resilient HTTP ──────────────────────────────────────────────────────────────

def resilient_post(url: str, payload: dict, headers: dict,
                   max_retries: int = 3, base_delay: float = 2.0,
                   timeout: int = 90) -> dict:
    """
    POST with exponential backoff + jitter. Handles 429, 5xx, timeouts.
    Raises GrokError on unretryable failures.
    Returns parsed JSON on success.
    """
    data = json.dumps(payload).encode("utf-8")
    attempt = 0
    last_error = None

    while attempt <= max_retries:
        try:
            req = urllib.request.Request(url, data=data, headers={**headers, "Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                body = resp.read().decode("utf-8")
                return json.loads(body)
        except urllib.error.HTTPError as e:
            body = e.read().decode("utf-8", errors="replace")
            err = classify_error(e.code, body)
            if not err.retryable:
                raise err
            last_error = err
            if attempt == max_retries:
                raise err
        except urllib.error.URLError as e:
            last_error = GrokError(0, "Network Error", str(e), retryable=True)
            if attempt == max_retries:
                raise last_error
        except TimeoutError:
            last_error = GrokError(408, "Timeout", f"Request timed out after {timeout}s", retryable=True)
            if attempt == max_retries:
                raise last_error

        # Exponential backoff with jitter
        delay = base_delay * (2 ** attempt) + random.uniform(0, 1.0)
        attempt += 1
        time.sleep(delay)

    raise last_error or GrokError(0, "Unknown", "All retries exhausted", retryable=False)


# ── Citation Parser ─────────────────────────────────────────────────────────────

def parse_citations(raw_citations: list) -> List[Citation]:
    """Deduplicate and structure citation list from API response."""
    seen_urls = set()
    citations = []
    for i, c in enumerate(raw_citations or [], start=1):
        url = c.get("url", "").strip()
        if url in seen_urls:
            continue
        seen_urls.add(url)
        citations.append(Citation(
            url=url,
            title=c.get("title", "").strip(),
            snippet=c.get("snippet", "").strip(),
            index=i
        ))
    return citations


def estimate_cost(usage: dict) -> float:
    """Estimate USD cost from token usage."""
    input_tokens = usage.get("input_tokens", 0)
    output_tokens = usage.get("output_tokens", 0)
    return (input_tokens / 1000) * COST_PER_1K_INPUT + (output_tokens / 1000) * COST_PER_1K_OUTPUT


# ── Core API Functions ──────────────────────────────────────────────────────────

def search_web(
    query: str,
    api_key: Optional[str] = None,
    model: str = DEFAULT_MODEL,
    allowed_domains: Optional[List[str]] = None,
    excluded_domains: Optional[List[str]] = None,
    enable_image_understanding: bool = False,
    use_cache: bool = True,
    ttl_hours: int = CACHE_TTL_HOURS,
) -> GrokResult:
    """
    Search the web using xAI's Grok API with real-time access.

    Args:
        query: Search query string (required)
        api_key: xAI API key. Falls back to XAI_API_KEY env var.
        model: Model to use. Must be in LIVE_SEARCH_MODELS for live results.
        allowed_domains: Restrict search to these domains (max 5). Cannot combine with excluded_domains.
        excluded_domains: Exclude these domains (max 5). Cannot combine with allowed_domains.
        enable_image_understanding: Parse images from search results.
        use_cache: Cache results in agency.db (default True).
        ttl_hours: Cache TTL in hours (default 1).

    Returns:
        GrokResult with content, citations, cost, and metadata.

    Raises:
        GrokError: On API failures, auth errors, or validation failures.
        ValueError: On invalid parameter combinations.
    """
    api_key = api_key or os.environ.get("XAI_API_KEY")
    if not api_key:
        raise GrokError(401, "Missing API Key", "Set XAI_API_KEY env var or pass api_key=", retryable=False)

    # Validate domain filters
    if allowed_domains and len(allowed_domains) > 5:
        raise ValueError("Maximum 5 allowed_domains")
    if excluded_domains and len(excluded_domains) > 5:
        raise ValueError("Maximum 5 excluded_domains")
    if allowed_domains and excluded_domains:
        raise ValueError("Cannot use both allowed_domains and excluded_domains simultaneously")

    # Warn if model doesn't support live search
    if model not in LIVE_SEARCH_MODELS:
        print(f"⚠️  Warning: model '{model}' may not support live search. Use: {DEFAULT_MODEL}", file=sys.stderr)

    # Cache key includes domain filters
    opts_hash = hashlib.md5(json.dumps({
        "allowed_domains": sorted(allowed_domains or []),
        "excluded_domains": sorted(excluded_domains or []),
        "image": enable_image_understanding
    }).encode()).hexdigest()[:8]

    cache = GrokCache()
    if use_cache:
        cached = cache.get(query, "web", opts_hash)
        if cached:
            cache.log_call(query, "web", model, cache_hit=True, usage={}, cost_usd=0.0)
            return cached

    # Build request
    tool = {"type": "web_search"}
    if allowed_domains:
        tool["allowed_domains"] = allowed_domains
    if excluded_domains:
        tool["excluded_domains"] = excluded_domains
    if enable_image_understanding:
        tool["enable_image_understanding"] = True

    payload = {
        "model": model,
        "input": [{"role": "user", "content": query}],
        "tools": [tool]
    }

    headers = {"Authorization": f"Bearer {api_key}"}

    data = resilient_post(XAI_RESPONSES_ENDPOINT, payload, headers)

    # Extract output
    output = data.get("output", [])
    last_msg = output[-1] if output else {}
    content_raw = last_msg.get("content", "")
    # content may be list of content blocks or string
    if isinstance(content_raw, list):
        content = " ".join(
            block.get("text", "") for block in content_raw if isinstance(block, dict)
        )
    else:
        content = str(content_raw)

    usage = data.get("usage", {})
    citations = parse_citations(data.get("citations", []))
    cost = estimate_cost(usage)

    # Detect if live search was actually performed
    server_tool_usage = data.get("server_side_tool_usage", {})
    search_performed = bool(server_tool_usage.get("web_search_queries") or
                            server_tool_usage.get("total_calls", 0) > 0)

    result = GrokResult(
        content=content,
        citations=citations,
        search_type="web",
        model=model,
        query=query,
        timestamp=datetime.utcnow().isoformat() + "Z",
        search_performed=search_performed,
        cache_hit=False,
        usage=usage,
        cost_usd=cost,
    )

    if use_cache:
        cache.set(query, "web", result, ttl_hours=ttl_hours, opts_hash=opts_hash)

    cache.log_call(query, "web", model, cache_hit=False, usage=usage, cost_usd=cost)
    return result


def search_x(
    query: str,
    api_key: Optional[str] = None,
    model: str = DEFAULT_MODEL,
    allowed_x_handles: Optional[List[str]] = None,
    excluded_x_handles: Optional[List[str]] = None,
    from_date: Optional[str] = None,
    to_date: Optional[str] = None,
    enable_image_understanding: bool = False,
    enable_video_understanding: bool = False,
    use_cache: bool = True,
    ttl_hours: int = CACHE_TTL_HOURS,
) -> GrokResult:
    """
    Search X (Twitter) using xAI's Grok API with real-time post access.

    Args:
        query: Search query string (required)
        api_key: xAI API key. Falls back to XAI_API_KEY env var.
        model: Model to use.
        allowed_x_handles: Only search these X handles (max 10, without @).
        excluded_x_handles: Exclude these X handles (max 10, without @).
        from_date: Start date ISO8601 (YYYY-MM-DD).
        to_date: End date ISO8601 (YYYY-MM-DD).
        enable_image_understanding: Parse images from posts.
        enable_video_understanding: Parse videos from posts.
        use_cache: Cache results in agency.db (default True).
        ttl_hours: Cache TTL in hours (default 1).

    Returns:
        GrokResult with content, citations (X post URLs), cost, and metadata.
    """
    api_key = api_key or os.environ.get("XAI_API_KEY")
    if not api_key:
        raise GrokError(401, "Missing API Key", "Set XAI_API_KEY env var or pass api_key=", retryable=False)

    if allowed_x_handles and len(allowed_x_handles) > 10:
        raise ValueError("Maximum 10 allowed_x_handles")
    if excluded_x_handles and len(excluded_x_handles) > 10:
        raise ValueError("Maximum 10 excluded_x_handles")
    if allowed_x_handles and excluded_x_handles:
        raise ValueError("Cannot use both allowed_x_handles and excluded_x_handles simultaneously")

    # Strip @ from handles if present
    if allowed_x_handles:
        allowed_x_handles = [h.lstrip("@") for h in allowed_x_handles]
    if excluded_x_handles:
        excluded_x_handles = [h.lstrip("@") for h in excluded_x_handles]

    opts_hash = hashlib.md5(json.dumps({
        "allowed": sorted(allowed_x_handles or []),
        "excluded": sorted(excluded_x_handles or []),
        "from": from_date, "to": to_date,
        "image": enable_image_understanding, "video": enable_video_understanding
    }).encode()).hexdigest()[:8]

    cache = GrokCache()
    if use_cache:
        cached = cache.get(query, "x", opts_hash)
        if cached:
            cache.log_call(query, "x", model, cache_hit=True, usage={}, cost_usd=0.0)
            return cached

    tool = {"type": "x_search"}
    if allowed_x_handles:
        tool["allowed_x_handles"] = allowed_x_handles
    if excluded_x_handles:
        tool["excluded_x_handles"] = excluded_x_handles
    if from_date:
        tool["from_date"] = from_date
    if to_date:
        tool["to_date"] = to_date
    if enable_image_understanding:
        tool["enable_image_understanding"] = True
    if enable_video_understanding:
        tool["enable_video_understanding"] = True

    payload = {
        "model": model,
        "input": [{"role": "user", "content": query}],
        "tools": [tool]
    }

    headers = {"Authorization": f"Bearer {api_key}"}
    data = resilient_post(XAI_RESPONSES_ENDPOINT, payload, headers)

    output = data.get("output", [])
    last_msg = output[-1] if output else {}
    content_raw = last_msg.get("content", "")
    if isinstance(content_raw, list):
        content = " ".join(
            block.get("text", "") for block in content_raw if isinstance(block, dict)
        )
    else:
        content = str(content_raw)

    usage = data.get("usage", {})
    citations = parse_citations(data.get("citations", []))
    cost = estimate_cost(usage)

    server_tool_usage = data.get("server_side_tool_usage", {})
    search_performed = bool(server_tool_usage.get("x_search_queries") or
                            server_tool_usage.get("total_calls", 0) > 0)

    result = GrokResult(
        content=content,
        citations=citations,
        search_type="x",
        model=model,
        query=query,
        timestamp=datetime.utcnow().isoformat() + "Z",
        search_performed=search_performed,
        cache_hit=False,
        usage=usage,
        cost_usd=cost,
    )

    if use_cache:
        cache.set(query, "x", result, ttl_hours=ttl_hours, opts_hash=opts_hash)

    cache.log_call(query, "x", model, cache_hit=False, usage=usage, cost_usd=cost)
    return result


# ── Async Wrapper ───────────────────────────────────────────────────────────────

async def async_search_web(query: str, **kwargs) -> GrokResult:
    """Async wrapper for search_web. Uses thread executor to avoid blocking."""
    import asyncio
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, lambda: search_web(query, **kwargs))


async def async_search_x(query: str, **kwargs) -> GrokResult:
    """Async wrapper for search_x. Uses thread executor to avoid blocking."""
    import asyncio
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, lambda: search_x(query, **kwargs))


# ── CLI ─────────────────────────────────────────────────────────────────────────

def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="grok",
        description="Search the web and X/Twitter via xAI Grok API",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 grok.py "latest AI regulation news" --mode web
  python3 grok.py "OpenAI reactions" --mode x --from-date 2025-01-01
  python3 grok.py "SpaceX launch" --mode web --domains spacex.com nasa.gov
  python3 grok.py "Elon Musk" --mode x --handles elonmusk --json
  python3 grok.py "AI news" --mode web --no-cache  # Force live call, skip cache
        """
    )
    p.add_argument("query", help="Search query string")
    p.add_argument("--mode", choices=["web", "x"], default="web",
                   help="Search mode: web (default) or x (Twitter/X)")
    p.add_argument("--model", default=DEFAULT_MODEL,
                   help=f"Model to use (default: {DEFAULT_MODEL})")
    p.add_argument("--domains", nargs="+", metavar="DOMAIN",
                   help="[web] Restrict to these domains (max 5)")
    p.add_argument("--exclude-domains", nargs="+", metavar="DOMAIN",
                   help="[web] Exclude these domains (max 5)")
    p.add_argument("--handles", nargs="+", metavar="HANDLE",
                   help="[x] Only search these X handles (no @, max 10)")
    p.add_argument("--exclude-handles", nargs="+", metavar="HANDLE",
                   help="[x] Exclude these X handles (max 10)")
    p.add_argument("--from-date", metavar="YYYY-MM-DD",
                   help="[x] Only posts from this date")
    p.add_argument("--to-date", metavar="YYYY-MM-DD",
                   help="[x] Only posts to this date")
    p.add_argument("--image", action="store_true",
                   help="Enable image understanding")
    p.add_argument("--video", action="store_true",
                   help="[x] Enable video understanding")
    p.add_argument("--json", action="store_true",
                   help="Output raw JSON result")
    p.add_argument("--no-cache", action="store_true",
                   help="Skip cache, force live API call")
    p.add_argument("--api-key", metavar="KEY",
                   help="xAI API key (or set XAI_API_KEY env var)")
    return p


def print_result(result: GrokResult, as_json: bool = False):
    """Print GrokResult to stdout."""
    if as_json:
        print(result.to_json())
        return

    icon = "🌐" if result.search_type == "web" else "𝕏"
    cache_tag = " [CACHED]" if result.cache_hit else ""
    search_tag = " ✓ live search" if result.search_performed else ""

    print(f"\n{icon} Grok {result.search_type.upper()} Search{cache_tag}{search_tag}")
    print(f"Query: {result.query}")
    print(f"Model: {result.model} | Time: {result.timestamp}")
    if result.cost_usd > 0:
        print(f"Cost: ${result.cost_usd:.6f} USD")
    print("─" * 60)
    print(result.content)

    if result.citations:
        print(result.format_citations_plain())


def main():
    parser = build_parser()
    args = parser.parse_args()

    api_key = args.api_key or os.environ.get("XAI_API_KEY")
    if not api_key:
        print("❌ Error: XAI_API_KEY not set. Use --api-key or export XAI_API_KEY=...", file=sys.stderr)
        sys.exit(1)

    use_cache = not args.no_cache

    try:
        if args.mode == "web":
            result = search_web(
                query=args.query,
                api_key=api_key,
                model=args.model,
                allowed_domains=args.domains,
                excluded_domains=args.exclude_domains,
                enable_image_understanding=args.image,
                use_cache=use_cache,
            )
        else:
            result = search_x(
                query=args.query,
                api_key=api_key,
                model=args.model,
                allowed_x_handles=args.handles,
                excluded_x_handles=args.exclude_handles,
                from_date=args.from_date,
                to_date=args.to_date,
                enable_image_understanding=args.image,
                enable_video_understanding=args.video,
                use_cache=use_cache,
            )
    except GrokError as e:
        print(f"❌ {e}", file=sys.stderr)
        sys.exit(2)
    except ValueError as e:
        print(f"❌ Invalid arguments: {e}", file=sys.stderr)
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nInterrupted.", file=sys.stderr)
        sys.exit(130)

    print_result(result, as_json=args.json)
    sys.exit(0)


if __name__ == "__main__":
    main()
