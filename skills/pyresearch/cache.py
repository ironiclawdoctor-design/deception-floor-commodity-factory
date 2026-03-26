#!/usr/bin/env python3
"""
PyResearch Cache — Python-native research cache
L1: SQLite (instant, $0) → L2: disk → L3: web → L4: LLM
Every cache hit saves tokens. Cache miss = learning event → logged.
"""
import sqlite3, json, hashlib, time, urllib.request
from pathlib import Path
from datetime import datetime, timedelta

AGENCY_DB = Path("/root/.openclaw/workspace/agency.db")

class ResearchCache:
    def __init__(self):
        self.conn = sqlite3.connect(AGENCY_DB)
        self.conn.executescript("""
            CREATE TABLE IF NOT EXISTS research_cache (
                key TEXT PRIMARY KEY,
                query TEXT,
                result TEXT,
                source TEXT,
                cached_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                expires_at TIMESTAMP,
                hit_count INTEGER DEFAULT 0,
                tokens_saved INTEGER DEFAULT 0
            );
            CREATE TABLE IF NOT EXISTS research_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                key TEXT,
                cache_hit INTEGER,
                source TEXT,
                tokens_used INTEGER DEFAULT 0,
                cost_usd REAL DEFAULT 0
            );
        """)
        self.conn.commit()

    def _key(self, query: str) -> str:
        return hashlib.sha256(query.encode()).hexdigest()[:16]

    def get(self, query: str):
        """Return cached result if fresh, else None."""
        k = self._key(query)
        row = self.conn.execute(
            "SELECT result, expires_at, hit_count FROM research_cache WHERE key=?", (k,)
        ).fetchone()
        if not row:
            return None
        result, expires_at, hits = row
        if expires_at and datetime.fromisoformat(expires_at) < datetime.utcnow():
            return None  # expired
        # Update hit count
        self.conn.execute(
            "UPDATE research_cache SET hit_count=hit_count+1, tokens_saved=tokens_saved+100 WHERE key=?", (k,)
        )
        self.conn.commit()
        self._log(k, hit=True, source="cache")
        return json.loads(result)

    def set(self, query: str, result, source: str = "web", ttl_hours: int = 24):
        k = self._key(query)
        expires = (datetime.utcnow() + timedelta(hours=ttl_hours)).isoformat()
        self.conn.execute("""
            INSERT OR REPLACE INTO research_cache (key, query, result, source, expires_at)
            VALUES (?,?,?,?,?)
        """, (k, query[:500], json.dumps(result), source, expires))
        self.conn.commit()
        self._log(k, hit=False, source=source)

    def get_or_fetch(self, query: str, fetch_fn, ttl_hours: int = 24, source: str = "web"):
        """Cache-first lookup. Only calls fetch_fn on cache miss."""
        cached = self.get(query)
        if cached is not None:
            return cached
        result = fetch_fn()
        self.set(query, result, source=source, ttl_hours=ttl_hours)
        return result

    def fetch_url(self, url: str, ttl_hours: int = 24) -> str:
        """Fetch URL with cache."""
        def _fetch():
            req = urllib.request.Request(url, headers={"User-Agent": "DollarAgency/1.0"})
            with urllib.request.urlopen(req, timeout=10) as r:
                return r.read().decode(errors='ignore')[:10000]
        return self.get_or_fetch(url, _fetch, ttl_hours=ttl_hours, source="web_fetch")

    def _log(self, key: str, hit: bool, source: str):
        self.conn.execute(
            "INSERT INTO research_log (key, cache_hit, source) VALUES (?,?,?)",
            (key, 1 if hit else 0, source)
        )
        self.conn.commit()

    def stats(self):
        total = self.conn.execute("SELECT COUNT(*) FROM research_cache").fetchone()[0]
        hits = self.conn.execute("SELECT SUM(hit_count), SUM(tokens_saved) FROM research_cache").fetchone()
        logs = self.conn.execute("SELECT SUM(cache_hit), COUNT(*) FROM research_log").fetchone()
        print(f"📦 Research Cache Stats")
        print(f"   Entries: {total}")
        print(f"   Total hits: {hits[0] or 0} | Tokens saved: {hits[1] or 0}")
        hit_rate = (logs[0] or 0) / max(1, logs[1] or 1) * 100
        print(f"   Hit rate: {hit_rate:.0f}% ({logs[0] or 0}/{logs[1] or 1} requests)")
        print(f"   Est. cost saved: ${(hits[1] or 0) * 0.00000014:.4f} (DeepSeek rate)")

    def warm(self):
        """Pre-warm cache with common agency queries."""
        common = [
            ("hashnode_tags_format", lambda: {"format": "slug+name required", "example": {"slug":"ai","name":"AI"}}, 168),
            ("hf_commit_format", lambda: {"field": "summary not commit_message"}, 168),
            ("camoufox_auth", lambda: {"method": "query_param", "param": "token", "source": "/data/browser-server-token"}, 168),
            ("gcp_billing_api", lambda: {"status": "disabled", "enable_url": "https://console.developers.google.com/apis/api/cloudbilling.googleapis.com/overview?project=sovereign-see"}, 24),
        ]
        for key, fn, ttl in common:
            if not self.get(key):
                self.set(key, fn(), source="warm", ttl_hours=ttl)
                print(f"  Warmed: {key}")

if __name__ == "__main__":
    rc = ResearchCache()
    rc.warm()
    rc.stats()
    print()
    # Test cache hit
    result = rc.get_or_fetch("hashnode_tags_format", lambda: {}, ttl_hours=168)
    print(f"Tag format (from cache): {result}")
