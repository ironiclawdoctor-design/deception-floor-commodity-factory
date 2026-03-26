#!/usr/bin/env python3
"""
ShanRouter — Internal Agency LLM Router
Inspired by OpenRouter. Optimized for file lookups, context, memory, bootstrap, experiments.

Architecture:
  Tier 0: FILE  → local file/SQLite lookup (free, instant)
  Tier 1: CACHE → prompt cache hit (near-free)
  Tier 2: LIGHT → deepseek-v3 / minimax (cheap, capable)
  Tier 3: HEAVY → claude-sonnet (expensive, reserved for complex reasoning)

Every request is routed to lowest viable tier.
Shannon minted for every token saved vs Tier 3 baseline.
"""
import sqlite3, json, hashlib, os, re, time
from pathlib import Path
from datetime import datetime

WORKSPACE = Path("/root/.openclaw/workspace")
AGENCY_DB = WORKSPACE / "agency.db"
MEMORY_MD = WORKSPACE / "MEMORY.md"
MEMORY_DIR = WORKSPACE / "memory"

# Pricing per token (OpenRouter)
PRICING = {
    "file":     {"prompt": 0,          "output": 0},
    "cache":    {"prompt": 0.000000014, "output": 0},
    "deepseek": {"prompt": 0.00000014,  "output": 0.00000028},
    "minimax":  {"prompt": 0.0000003,   "output": 0.0000012},
    "claude":   {"prompt": 0.000003,    "output": 0.000015},
}

# Route rules: task_type → tier
ROUTES = {
    "memory_lookup":    "file",
    "file_read":        "file",
    "sqlite_query":     "file",
    "bootstrap_check":  "file",
    "experiment_log":   "file",
    "context_trim":     "file",
    "simple_format":    "cache",
    "short_answer":     "deepseek",
    "code_gen":         "deepseek",
    "agent_turn":       "deepseek",
    "content_writing":  "deepseek",
    "orchestration":    "deepseek",
    "complex_reasoning":"claude",
    "security_audit":   "claude",
    "architecture":     "claude",
}

def init():
    conn = sqlite3.connect(AGENCY_DB)
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS shanrouter_cache (
            hash TEXT PRIMARY KEY,
            task_type TEXT,
            prompt_snippet TEXT,
            response TEXT,
            tier TEXT,
            tokens_saved INTEGER DEFAULT 0,
            shannon_minted INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            hit_count INTEGER DEFAULT 1
        );
        CREATE TABLE IF NOT EXISTS shanrouter_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            task_type TEXT,
            tier_used TEXT,
            tier_avoided TEXT,
            tokens_in INTEGER DEFAULT 0,
            tokens_out INTEGER DEFAULT 0,
            cost_actual REAL DEFAULT 0,
            cost_avoided REAL DEFAULT 0,
            shannon_minted INTEGER DEFAULT 0
        );
        CREATE TABLE IF NOT EXISTS shanrouter_context (
            key TEXT PRIMARY KEY,
            content TEXT,
            token_estimate INTEGER,
            priority INTEGER DEFAULT 5,
            last_used TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            source TEXT
        );
    """)
    conn.commit()
    return conn

def token_estimate(text: str) -> int:
    return max(1, len(text) // 4)

def cost(tier: str, t_in: int, t_out: int) -> float:
    p = PRICING.get(tier, PRICING["claude"])
    return t_in * p["prompt"] + t_out * p["output"]

def route(task_type: str) -> str:
    return ROUTES.get(task_type, "deepseek")

def shannon_for_savings(saved_usd: float) -> int:
    """1 Shannon per $0.01 saved vs Claude baseline."""
    return int(saved_usd / 0.01)

# ── File-tier resolvers ────────────────────────────────────────────────────────

def resolve_memory(query: str) -> str | None:
    """Search MEMORY.md and daily notes for query."""
    hits = []
    for f in [MEMORY_MD] + sorted(MEMORY_DIR.glob("*.md"), reverse=True)[:3]:
        if not f.exists():
            continue
        text = f.read_text()
        for line in text.splitlines():
            if any(w.lower() in line.lower() for w in query.split()):
                hits.append(f"[{f.name}] {line.strip()}")
    return "\n".join(hits[:10]) if hits else None

def resolve_bootstrap() -> str:
    """Return bootstrap status."""
    b = WORKSPACE / "BOOTSTRAP.md"
    if b.exists():
        return f"BOOTSTRAP.md exists ({b.stat().st_size} bytes) — new agent onboarding pending"
    return "BOOTSTRAP.md absent — no pending onboarding"

def resolve_experiment(tag: str = None) -> str:
    """Return autoresearch experiment state."""
    cfg = WORKSPACE / "autoresearch.config.md"
    if cfg.exists():
        return cfg.read_text()[:500]
    return "No active autoresearch experiment."

def context_budget(max_tokens: int = 4000) -> str:
    """Build optimized context from ranked files, respecting token budget."""
    conn = init()
    rows = conn.execute(
        "SELECT key, content, token_estimate FROM shanrouter_context ORDER BY priority DESC, last_used DESC"
    ).fetchall()
    conn.close()

    used = 0
    parts = []
    for key, content, tok in rows:
        if used + tok > max_tokens:
            break
        parts.append(f"## {key}\n{content}")
        used += tok
    return "\n\n".join(parts) if parts else ""

def index_context():
    """Index key workspace files into shanrouter_context."""
    conn = init()
    files = [
        (MEMORY_MD, "memory", 10),
        (WORKSPACE / "SOUL.md", "soul", 9),
        (WORKSPACE / "AGENTS.md", "agents", 8),
        (WORKSPACE / "AUTONOMOUS.md", "autonomous", 7),
        (WORKSPACE / "REVENUE-DESIGN.md", "revenue", 6),
        (WORKSPACE / "autoresearch.config.md", "autoresearch", 5),
    ]
    indexed = 0
    for path, key, priority in files:
        if not path.exists():
            continue
        content = path.read_text()[:3000]  # cap per file
        tok = token_estimate(content)
        conn.execute("""
            INSERT OR REPLACE INTO shanrouter_context (key, content, token_estimate, priority, source)
            VALUES (?, ?, ?, ?, ?)
        """, (key, content, tok, priority, str(path)))
        indexed += 1
    conn.commit()
    conn.close()
    return indexed

def log_route(task_type, tier, t_in, t_out, conn):
    """Log routing decision and mint Shannon for savings."""
    actual = cost(tier, t_in, t_out)
    avoided = cost("claude", t_in, t_out) - actual
    shannon = shannon_for_savings(avoided)
    conn.execute("""
        INSERT INTO shanrouter_log (task_type, tier_used, tier_avoided, tokens_in, tokens_out,
            cost_actual, cost_avoided, shannon_minted)
        VALUES (?, ?, 'claude', ?, ?, ?, ?, ?)
    """, (task_type, tier, t_in, t_out, actual, avoided, shannon))
    conn.commit()
    return actual, avoided, shannon

def report():
    conn = init()
    print("🔀 ShanRouter — Routing Report")
    print(f"   {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}")
    print()

    rows = conn.execute("""
        SELECT tier_used, COUNT(*), SUM(tokens_in), SUM(cost_actual),
               SUM(cost_avoided), SUM(shannon_minted)
        FROM shanrouter_log GROUP BY tier_used ORDER BY SUM(cost_actual)
    """).fetchall()

    if not rows:
        print("  No routing history yet. Run: python3 shanrouter.py --index")
    else:
        print(f"  {'Tier':<12} {'Requests':>9} {'Tokens':>10} {'Cost':>10} {'Saved':>10} {'Shannon':>8}")
        print("  " + "-" * 62)
        for tier, cnt, tok, cost_a, saved, sh in rows:
            print(f"  {tier:<12} {cnt:>9} {tok:>10,} ${cost_a:>8.4f} ${saved:>8.4f} {sh:>8}")

    ctx = conn.execute("SELECT COUNT(*), SUM(token_estimate) FROM shanrouter_context").fetchone()
    print()
    print(f"  Context index: {ctx[0]} files, {ctx[1] or 0:,} tokens indexed")

    conn.close()

def status_report() -> str:
    """Run the agency status report through ShanRouter — logs route, mints Shannon."""
    conn = init()
    import subprocess

    # Route this as agent_turn (orchestration-level status check)
    task_type = "agent_turn"
    tier = route(task_type)
    t_in = 500  # estimated tokens for status check
    t_out = 100
    actual, avoided, shannon = log_route(task_type, tier, t_in, t_out, conn)
    conn.close()

    lines = []
    lines.append(f"🔀 ShanRouter routed: {task_type} → {tier} | +{shannon} Shannon minted")

    # Ledger
    try:
        r = subprocess.run(
            ["sqlite3", "/root/.openclaw/workspace/dollar/dollar.db",
             "SELECT '💰 $'||total_backing_usd||' → '||total_shannon_supply||' Shannon | Confessions: '||(SELECT COUNT(*) FROM confessions) FROM exchange_rates ORDER BY date DESC LIMIT 1;"],
            capture_output=True, text=True, timeout=5
        )
        lines.append(r.stdout.strip() or "💰 ledger empty")
    except Exception as e:
        lines.append(f"💰 ledger error: {e}")

    # BTC
    try:
        import json as _json
        btc = _json.loads(Path("/root/human/btc-status.json").read_text())
        lines.append(f"₿ {btc['balance_satoshi']} sat = ${btc['balance_usd']:.2f}")
    except Exception:
        lines.append("₿ btc-status.json not found")

    # Last run log
    try:
        log = Path("/root/human/last-run.log")
        if log.exists():
            tail = log.read_text().splitlines()[-3:]
            lines.extend(tail)
        else:
            lines.append("📋 last-run.log not found")
    except Exception as e:
        lines.append(f"📋 log error: {e}")

    return "\n".join(lines)


if __name__ == "__main__":
    import sys
    conn = init()
    cmd = sys.argv[1] if len(sys.argv) > 1 else "--report"

    if cmd == "--index":
        n = index_context()
        print(f"✅ Indexed {n} files into shanrouter_context")
        report()
    elif cmd == "--memory":
        q = " ".join(sys.argv[2:]) or "Shannon dollar backing"
        result = resolve_memory(q)
        print(result or "No matches found.")
    elif cmd == "--budget":
        max_t = int(sys.argv[2]) if len(sys.argv) > 2 else 4000
        print(context_budget(max_t))
    elif cmd == "--bootstrap":
        print(resolve_bootstrap())
    elif cmd == "--route":
        task = sys.argv[2] if len(sys.argv) > 2 else "agent_turn"
        tier = route(task)
        print(f"Task '{task}' → Tier: {tier}")
        t_in = int(sys.argv[3]) if len(sys.argv) > 3 else 1000
        actual, avoided, sh = log_route(task, tier, t_in, 200, conn)
        print(f"Cost: ${actual:.5f} | Saved: ${avoided:.5f} | +{sh} Shannon")
    elif cmd == "--report":
        report()
    elif cmd == "--status":
        print(status_report())
    conn.close()
