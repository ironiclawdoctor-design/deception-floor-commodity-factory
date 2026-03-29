#!/usr/bin/env python3
"""
projectx_client.py
ProjectX Gateway API client — agency-built, $0 outlay.
Base: https://api.topstepx.com
Auth: API key (POST /api/Auth/loginKey)
"""

import json
import urllib.request
import urllib.error
import sqlite3
from pathlib import Path
from datetime import datetime, timezone

BASE = "https://api.topstepx.com"
DB = Path("/root/.openclaw/workspace/dollar.db")

def _post(path: str, body: dict, token: str = None) -> dict:
    data = json.dumps(body).encode()
    headers = {"Content-Type": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    req = urllib.request.Request(f"{BASE}{path}", data=data, headers=headers)
    try:
        resp = urllib.request.urlopen(req, timeout=15)
        return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        return {"error": e.code, "reason": e.reason, "body": e.read().decode()[:500]}
    except Exception as ex:
        return {"error": str(ex)}

# ── AUTH ──────────────────────────────────────────────────────────────────────

def login_key(api_key: str) -> dict:
    """Authenticate with API key. Returns session token."""
    return _post("/api/Auth/loginKey", {"apiKey": api_key})

def validate(token: str) -> dict:
    return _post("/api/Auth/validate", {}, token=token)

def logout(token: str) -> dict:
    return _post("/api/Auth/logout", {}, token=token)

# ── ACCOUNT ───────────────────────────────────────────────────────────────────

def search_accounts(token: str, only_active: bool = True) -> dict:
    return _post("/api/Account/search", {"onlyActiveAccounts": only_active}, token=token)

# ── CONTRACTS (instruments) ───────────────────────────────────────────────────

def search_contracts(token: str, query: str = "MNQ") -> dict:
    return _post("/api/Contract/search", {"searchText": query, "live": False}, token=token)

# ── ORDERS ────────────────────────────────────────────────────────────────────

def search_orders(token: str, account_id: int, start_ts: int = None) -> dict:
    body = {"accountId": account_id}
    if start_ts:
        body["startTimestamp"] = start_ts
    return _post("/api/Order/search", body, token=token)

# ── POSITIONS ─────────────────────────────────────────────────────────────────

def search_positions(token: str, account_id: int) -> dict:
    return _post("/api/Position/search", {"accountId": account_id}, token=token)

# ── TRADES ────────────────────────────────────────────────────────────────────

def search_trades(token: str, account_id: int) -> dict:
    return _post("/api/Trade/search", {"accountId": account_id}, token=token)

# ── DLL MONITOR ───────────────────────────────────────────────────────────────

def dll_status(token: str, account_id: int) -> dict:
    """
    Compute DLL status from live account data.
    Returns: {balance, daily_pnl, dll_limit, dll_remaining, status}
    """
    accs = search_accounts(token)
    if "error" in accs:
        return accs
    for acc in accs.get("accounts", []):
        if acc.get("id") == account_id:
            balance = acc.get("balance", 0)
            daily_pnl = acc.get("dailyPnl", 0)
            dll_limit = -1200  # LucidDirect $50k standard
            dll_remaining = dll_limit - daily_pnl
            status = "CLEAR" if daily_pnl > dll_limit else "BREACHED"
            warning = daily_pnl < (dll_limit + 300)
            return {
                "balance": balance,
                "daily_pnl": daily_pnl,
                "dll_limit": dll_limit,
                "dll_remaining": dll_remaining,
                "status": status,
                "warning": warning,
                "warning_msg": "Within $300 of DLL — signals suspended" if warning else None
            }
    return {"error": "account not found"}

# ── CONSISTENCY MONITOR ───────────────────────────────────────────────────────

def consistency_ratio(token: str, account_id: int) -> dict:
    """
    Calculate largest_day_pnl / total_cycle_pnl.
    LucidDirect limit: 20% max.
    Agency target: 15-18%.
    """
    conn = sqlite3.connect(DB)
    rows = conn.execute(
        "SELECT date, SUM(pnl_usd) as day_pnl FROM lucid_sessions "
        "WHERE result IN ('win','loss') GROUP BY date ORDER BY date"
    ).fetchall()
    conn.close()

    if not rows:
        return {"ratio": 0, "status": "NO_DATA", "days": 0}

    day_pnls = [r[1] for r in rows if r[1] and r[1] > 0]
    if not day_pnls:
        return {"ratio": 0, "status": "NO_PROFITABLE_DAYS", "days": len(rows)}

    total = sum(day_pnls)
    largest = max(day_pnls)
    ratio = (largest / total) * 100 if total > 0 else 0

    status = "CLEAR" if ratio <= 20 else "BREACH"
    warning = 15 <= ratio <= 20

    return {
        "largest_day": largest,
        "total_profit": total,
        "ratio_pct": round(ratio, 2),
        "limit_pct": 20,
        "agency_target_pct": "15-18",
        "status": status,
        "warning": warning,
        "days": len(day_pnls),
        "payout_ready": ratio <= 20 and total >= 3000
    }

# ── FULL STATUS REPORT ────────────────────────────────────────────────────────

def agency_status(api_key: str) -> dict:
    auth = login_key(api_key)
    token = auth.get("token")
    if not token:
        return {"error": "auth_failed", "detail": auth}

    accounts = search_accounts(token)
    account_id = None
    for acc in accounts.get("accounts", []):
        account_id = acc.get("id")
        break

    result = {
        "ts": datetime.now(timezone.utc).isoformat(),
        "auth": "ok",
        "account_id": account_id,
        "accounts": accounts,
        "consistency": consistency_ratio(token, account_id) if account_id else "no_account",
        "dll": dll_status(token, account_id) if account_id else "no_account",
    }

    logout(token)
    return result

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        key = sys.argv[1]
        print(json.dumps(agency_status(key), indent=2))
    else:
        print("Usage: python3 projectx_client.py <api_key>")
        print("Endpoints available:")
        print("  login_key, validate, logout")
        print("  search_accounts, search_contracts")
        print("  search_orders, search_positions, search_trades")
        print("  dll_status, consistency_ratio, agency_status")
