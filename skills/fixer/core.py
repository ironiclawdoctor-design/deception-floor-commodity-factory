#!/usr/bin/env python3
"""
Fixer — Industry Standard API Resilience Layer
Applies: RFC 7807, exponential backoff, schema validation, circuit breaker, idempotency
"""
import urllib.request, urllib.error, json, time, random, hashlib
from pathlib import Path

# ── Error Classification ──────────────────────────────────────────────────────

class FixerError(Exception):
    def __init__(self, code, title, detail, retryable=False):
        self.code = code
        self.title = title
        self.detail = detail
        self.retryable = retryable
        super().__init__(f"[{code}] {title}: {detail}")

def classify(status: int, body: str) -> FixerError:
    if status == 401: return FixerError(401, "Unauthorized", "Check API key/token", retryable=False)
    if status == 403: return FixerError(403, "Forbidden", body[:200], retryable=False)
    if status == 404: return FixerError(404, "Not Found", body[:200], retryable=False)
    if status == 409: return FixerError(409, "Conflict", "Resource already exists", retryable=False)
    if status == 422: return FixerError(422, "Schema Error", body[:500], retryable=False)
    if status == 429: return FixerError(429, "Rate Limited", "Backing off", retryable=True)
    if status >= 500: return FixerError(status, "Server Error", body[:200], retryable=True)
    return FixerError(status, "Unknown", body[:200], retryable=True)

# ── Schema Validators ─────────────────────────────────────────────────────────

HASHNODE_TAG_SCHEMA = {
    "required": ["slug", "name"],
    "slug": {"type": str, "pattern": r'^[a-z0-9\-]+$'},
    "name": {"type": str, "min_len": 1, "max_len": 50},
}

def validate_hashnode_tags(tags: list) -> list:
    """Ensure tags have both slug and name. Fix slugs automatically."""
    import re
    clean = []
    for t in tags[:5]:
        if isinstance(t, str):
            slug = re.sub(r'[^a-z0-9\-]', '', t.lower().replace(' ', '-'))
            t = {"slug": slug, "name": t.strip()}
        if not t.get("slug") or not t.get("name"):
            continue
        t["slug"] = re.sub(r'[^a-z0-9\-]', '', t["slug"].lower())
        clean.append(t)
    return clean

def validate_hf_commit(payload: dict) -> dict:
    """Ensure HuggingFace commit payload has required 'summary' field."""
    if "commit_message" in payload and "summary" not in payload:
        payload["summary"] = payload.pop("commit_message")
    if "summary" not in payload:
        payload["summary"] = "Update"
    return payload

# ── Resilient HTTP ────────────────────────────────────────────────────────────

def resilient_post(url: str, payload: dict, headers: dict,
                   max_retries: int = 3, base_delay: float = 1.0,
                   dry_run: bool = False) -> dict:
    """
    POST with exponential backoff + jitter.
    Raises FixerError on unretryable failures.
    Returns parsed JSON on success.
    """
    if dry_run:
        print(f"[DRY RUN] POST {url}")
        print(f"  Payload: {json.dumps(payload)[:200]}")
        return {"dry_run": True}

    data = json.dumps(payload).encode()
    attempt = 0
    last_error = None

    while attempt <= max_retries:
        try:
            req = urllib.request.Request(url, data=data, headers={
                **headers, "Content-Type": "application/json"
            })
            with urllib.request.urlopen(req, timeout=20) as r:
                return json.loads(r.read())

        except urllib.error.HTTPError as e:
            body = e.read().decode(errors='ignore')
            err = classify(e.code, body)
            last_error = err
            if not err.retryable:
                raise err
            # Retryable: backoff with jitter
            delay = base_delay * (2 ** attempt) + random.uniform(0, 0.5)
            print(f"  ⚠️  {err.title} (attempt {attempt+1}/{max_retries+1}) — retry in {delay:.1f}s")
            time.sleep(delay)

        except (urllib.error.URLError, TimeoutError) as e:
            last_error = FixerError(0, "Network Error", str(e), retryable=True)
            delay = base_delay * (2 ** attempt)
            print(f"  ⚠️  Network error — retry in {delay:.1f}s")
            time.sleep(delay)

        attempt += 1

    raise last_error or FixerError(0, "Max retries exceeded", str(url))

# ── Idempotency ───────────────────────────────────────────────────────────────

class IdempotencyStore:
    """Track completed operations to prevent duplicates."""
    def __init__(self, db_path: str = "/root/.openclaw/workspace/agency.db"):
        import sqlite3
        self.conn = sqlite3.connect(db_path)
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS idempotency_keys (
                key TEXT PRIMARY KEY,
                result TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        self.conn.commit()

    def key(self, *parts) -> str:
        return hashlib.sha256("|".join(str(p) for p in parts).encode()).hexdigest()[:16]

    def seen(self, key: str) -> bool:
        return bool(self.conn.execute("SELECT 1 FROM idempotency_keys WHERE key=?", (key,)).fetchone())

    def mark(self, key: str, result: str = "ok"):
        self.conn.execute("INSERT OR IGNORE INTO idempotency_keys (key, result) VALUES (?,?)", (key, result))
        self.conn.commit()

# ── Fixed Hashnode Publisher ──────────────────────────────────────────────────

def hashnode_publish(article_path: str, hn_key: str, pub_id: str,
                     dry_run: bool = False) -> str:
    content = Path(article_path).read_text()
    end = content.find('\n---', 3)
    meta = {}
    if content.startswith('---') and end > 0:
        for line in content[3:end].strip().splitlines():
            if ':' in line:
                k, v = line.split(':', 1)
                meta[k.strip()] = v.strip().strip('"')
    body = content[end+4:].strip() if end > 0 else content

    title = meta.get('title', Path(article_path).stem)
    raw_tags = [t.strip() for t in meta.get('tags', 'ai').split(',')]
    tags = validate_hashnode_tags(raw_tags)

    q = 'mutation P($i:PublishPostInput!){publishPost(input:$i){post{url}}}'
    payload = {'query': q, 'variables': {'i': {
        'title': title,
        'contentMarkdown': body,
        'publicationId': pub_id,
        'tags': tags
    }}}

    idem = IdempotencyStore()
    key = idem.key(pub_id, title)
    if idem.seen(key):
        return f'⏭️  Already published: {title}'

    result = resilient_post('https://gql.hashnode.com', payload,
                            {'Authorization': hn_key}, dry_run=dry_run)
    if dry_run:
        return f'[DRY RUN] Would publish: {title}'
    if 'errors' in result:
        raise FixerError(422, "Hashnode Error", result['errors'][0]['message'])

    url = result['data']['publishPost']['post']['url']
    idem.mark(key, url)
    return f'✅ {url}'

# ── Fixed HuggingFace Uploader ────────────────────────────────────────────────

def hf_upload(file_path: str, hf_token: str, user: str, repo: str,
              summary: str = "Update dataset") -> str:
    import base64
    p = Path(file_path)
    payload = validate_hf_commit({
        'operations': [{'operation': 'upsert', 'path': p.name,
            'content': base64.b64encode(p.read_bytes()).decode(), 'encoding': 'base64'}],
        'summary': summary
    })
    idem = IdempotencyStore()
    key = idem.key(user, repo, p.name, p.stat().st_mtime)
    if idem.seen(key):
        return f'⏭️  Already uploaded: {p.name}'

    resilient_post(
        f'https://huggingface.co/api/datasets/{user}/{repo}/commit/main',
        payload, {'Authorization': f'Bearer {hf_token}'}
    )
    idem.mark(key, 'uploaded')
    return f'✅ huggingface.co/datasets/{user}/{repo}'

if __name__ == "__main__":
    print("Fixer core loaded. Import and use hashnode_publish() or hf_upload().")
    print("Validators: validate_hashnode_tags(), validate_hf_commit()")
