#!/usr/bin/env python3
"""
Preflight — Agency Photographer.
Run before ALL work and autoresearch.
Checks OpenRouter balance and blocks if below safe floor.
"""

import urllib.request, urllib.error, json, os, sys
from pathlib import Path

FLOOR_USD = 1.00       # minimum to proceed
WARN_USD  = 3.00       # warn but continue
SECRETS   = Path("/root/.openclaw/workspace/secrets")

def get_openrouter_balance():
    key = os.environ.get("OPENROUTER_API_KEY")
    if not key:
        # Try reading from openclaw config indirectly via env
        try:
            result = Path("/root/.openclaw/openclaw.json").read_text()
            # key is redacted in config reads — use env only
        except Exception:
            pass
    if not key:
        return None, "OPENROUTER_API_KEY not in env"

    req = urllib.request.Request(
        "https://openrouter.ai/api/v1/auth/key",
        headers={"Authorization": f"Bearer {key}"}
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            data = json.loads(r.read())
            limit = data.get("data", {}).get("limit")
            usage = data.get("data", {}).get("usage", 0)
            if limit is None:
                return 999.0, "unlimited"
            remaining = float(limit) - float(usage)
            return remaining, f"${remaining:.2f} remaining (limit ${limit}, used ${usage:.2f})"
    except urllib.error.HTTPError as e:
        return None, f"HTTP {e.code}: {e.read().decode()[:100]}"
    except Exception as ex:
        return None, str(ex)

def run():
    print("📸 Agency Preflight Check")
    balance, msg = get_openrouter_balance()

    if balance is None:
        print(f"  ⚠️  Balance unknown: {msg}")
        print("  Proceeding with caution — monitor closely.")
        return True  # don't hard-block on unknown

    print(f"  💳 OpenRouter: {msg}")

    if balance < FLOOR_USD:
        print(f"  ❌ BLOCKED — balance ${balance:.2f} below floor ${FLOOR_USD:.2f}")
        print(f"  Top up: https://openrouter.ai/settings/credits")
        print(f"  BR-006: Credits are oxygen. Tank is empty. Abort.")
        return False

    if balance < WARN_USD:
        print(f"  ⚠️  WARNING — balance ${balance:.2f} below warn threshold ${WARN_USD:.2f}")
        print(f"  BR-002: Verify balance before spawning agents.")

    print(f"  ✅ Cleared to proceed")
    return True

if __name__ == "__main__":
    ok = run()
    sys.exit(0 if ok else 1)
