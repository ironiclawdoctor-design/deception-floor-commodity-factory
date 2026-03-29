#!/usr/bin/env python3
"""
Cash App Balance Monitor — $DollarAgency
Tries Square API first, falls back to browser scraping.
"""
import json, os, urllib.request, urllib.parse, sqlite3
from datetime import datetime
from pathlib import Path

SECRETS = Path("/root/.openclaw/workspace/secrets")
SA_CONFIG = SECRETS / "cashapp.json"
DOLLAR_DB = Path("/root/.openclaw/workspace/dollar/dollar.db")
LOG = Path("/root/human/cashapp-balance.log")

def load_config():
    if SA_CONFIG.exists():
        with open(SA_CONFIG) as f:
            return json.load(f)
    return {}

def check_square_api(config):
    """Query balance via Square API."""
    token = config.get("square_access_token")
    if not token:
        return None, "No Square access token configured"

    env = config.get("square_environment", "sandbox")
    base = "https://connect.squareup.com" if env == "production" else "https://connect.squareupsandbox.com"

    req = urllib.request.Request(
        f"{base}/v2/merchants/me",
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            data = json.loads(r.read())
            return data, None
    except Exception as e:
        return None, str(e)

def check_dollar_db():
    """Get last known backing from Dollar ledger."""
    try:
        conn = sqlite3.connect(DOLLAR_DB)
        row = conn.execute(
            "SELECT date, total_backing_usd, total_shannon_supply FROM exchange_rates ORDER BY date DESC LIMIT 1"
        ).fetchone()
        conn.close()
        if row:
            return {"date": row[0], "backing_usd": row[1], "shannon_supply": row[2]}
    except Exception as e:
        return {"error": str(e)}
    return {}

def log_result(lines):
    LOG.parent.mkdir(parents=True, exist_ok=True)
    with open(LOG, "w") as f:
        f.write("\n".join(lines))

def main():
    lines = []
    def out(s): print(s); lines.append(s)

    out(f"💰 Cash App Balance Check — {datetime.utcnow().isoformat()}Z")
    out(f"   Cashtag: $DollarAgency")
    out("")

    config = load_config()

    # Try Square API
    out("📡 Square API...")
    result, err = check_square_api(config)
    if result:
        out(f"  ✅ Square API connected: {json.dumps(result, indent=2)[:200]}")
    else:
        out(f"  ⚠️  Square API: {err}")
        out("     → Configure: /root/.openclaw/workspace/secrets/cashapp.json")
        out("     → Get token: https://developer.squareup.com/apps")

    # Dollar DB fallback
    out("")
    out("📊 Dollar Ledger (last known state)...")
    db = check_dollar_db()
    if "error" not in db:
        out(f"  ✅ Date: {db.get('date')}")
        out(f"  ✅ Backing: ${db.get('backing_usd')}")
        out(f"  ✅ Shannon: {db.get('shannon_supply')}")
    else:
        out(f"  ⚠️  DB error: {db.get('error')}")

    out("")
    out("📋 Next steps:")
    out("  A) Square API: get token at https://developer.squareup.com/apps")
    out("     Store in /root/.openclaw/workspace/secrets/cashapp.json")
    out("  B) Browser scraping: attach Chrome tab → cashapp-scrape.py")
    out("  C) Webhook: deploy Cloud Run endpoint → receive real-time notifications")

    log_result(lines)
    out(f"\n✅ Log saved to {LOG}")

if __name__ == "__main__":
    main()
