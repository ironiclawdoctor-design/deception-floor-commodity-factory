#!/usr/bin/env python3
"""
btc-monitor.py — BTC Donation Tracker for Fiesta Agency
Address: 12bxubgs1Br6NvKH4p35pcBpinQ7fwe4ht
Zero external dependencies (stdlib only).
Logs new transactions to dollar.db confessions + mints Shannon.
"""

import json
import os
import sqlite3
import sys
import time
import urllib.request
from datetime import date, datetime

# ── Config ──────────────────────────────────────────────────────────────────
BTC_ADDRESS     = "12bxubgs1Br6NvKH4p35pcBpinQ7fwe4ht"
AGENCY_DB       = "/root/.openclaw/workspace/agency.db"
DOLLAR_DB       = "/root/.openclaw/workspace/dollar/dollar.db"
STATUS_JSON     = "/root/human/btc-status.json"
SATOSHI         = 1e8

# Shannon per satoshi donated (1 satoshi = 1 Shannon)
SHANNON_PER_SATOSHI = 1

# ── Fetch BTC data ───────────────────────────────────────────────────────────
def fetch_btc_data():
    """Fetch address data from blockchain.info (no API key needed)."""
    url = f"https://blockchain.info/rawaddr/{BTC_ADDRESS}?limit=5"
    req = urllib.request.Request(url, headers={"User-Agent": "fiesta-btc-monitor/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            data = json.loads(r.read())
        balance_satoshi = data["final_balance"]
        tx_count        = data["n_tx"]
        last_tx_hash    = data["txs"][0]["hash"] if data["txs"] else None
        # blockchain.info doesn't return USD — estimate via coingecko
        btc_price_usd   = fetch_btc_price_usd()
        balance_usd     = (balance_satoshi / SATOSHI) * btc_price_usd
        return {
            "balance_satoshi": balance_satoshi,
            "balance_btc":     round(balance_satoshi / SATOSHI, 8),
            "balance_usd":     round(balance_usd, 2),
            "tx_count":        tx_count,
            "last_tx_hash":    last_tx_hash,
            "btc_price_usd":   btc_price_usd,
        }
    except Exception as e:
        print(f"[btc-monitor] ERROR fetching BTC data: {e}", file=sys.stderr)
        raise

def fetch_btc_price_usd():
    """Fetch current BTC price in USD from CoinGecko (free, no key)."""
    try:
        url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"
        req = urllib.request.Request(url, headers={"User-Agent": "fiesta-btc-monitor/1.0"})
        with urllib.request.urlopen(req, timeout=10) as r:
            data = json.loads(r.read())
        return data["bitcoin"]["usd"]
    except Exception:
        # Fallback: try blockchain.info ticker
        try:
            with urllib.request.urlopen("https://blockchain.info/ticker", timeout=10) as r:
                ticker = json.loads(r.read())
            return ticker["USD"]["last"]
        except Exception:
            return 0.0  # Unknown — can't reach price feed

# ── Database ops ─────────────────────────────────────────────────────────────
def ensure_table(db_path):
    conn = sqlite3.connect(db_path)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS btc_snapshots (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            checked_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            balance_satoshi INTEGER,
            balance_usd     REAL,
            tx_count        INTEGER,
            last_tx_hash    TEXT
        )
    """)
    conn.commit()
    return conn

def get_last_snapshot(conn):
    row = conn.execute("""
        SELECT balance_satoshi, tx_count, last_tx_hash
        FROM btc_snapshots
        ORDER BY id DESC LIMIT 1
    """).fetchone()
    if row:
        return {"balance_satoshi": row[0], "tx_count": row[1], "last_tx_hash": row[2]}
    return None

def save_snapshot(conn, d):
    conn.execute("""
        INSERT INTO btc_snapshots (balance_satoshi, balance_usd, tx_count, last_tx_hash)
        VALUES (?, ?, ?, ?)
    """, (d["balance_satoshi"], d["balance_usd"], d["tx_count"], d["last_tx_hash"]))
    conn.commit()

def log_confession(new_satoshi, btc_data):
    """Log the BTC donation as a confession event in dollar.db."""
    try:
        conn = sqlite3.connect(DOLLAR_DB)
        conn.execute("""
            INSERT INTO confessions
                (date, agent, failure_type, platform, description, shannon_minted)
            VALUES (?, 'btc-monitor', 'donation_received', 'bitcoin', ?, ?)
        """, (
            date.today().isoformat(),
            f"BTC donation detected: +{new_satoshi} satoshi ({new_satoshi/SATOSHI:.8f} BTC). "
            f"Last tx: {btc_data['last_tx_hash']}. Balance now {btc_data['balance_satoshi']} sat.",
            new_satoshi * SHANNON_PER_SATOSHI,
        ))
        conn.commit()
        conn.close()
        print(f"[btc-monitor] Logged confession: +{new_satoshi} sat")
    except Exception as e:
        print(f"[btc-monitor] WARNING: confession log failed: {e}", file=sys.stderr)

def mint_shannon(new_satoshi, btc_data):
    """Mint Shannon in dollar.db shannon_events table."""
    try:
        shannon_amount = new_satoshi * SHANNON_PER_SATOSHI
        conn = sqlite3.connect(DOLLAR_DB)
        conn.execute("""
            INSERT INTO shannon_events
                (date, agent, event_type, amount_usd, shannon_minted, description)
            VALUES (?, 'btc-monitor', 'btc_donation', ?, ?, ?)
        """, (
            date.today().isoformat(),
            round((new_satoshi / SATOSHI) * btc_data["btc_price_usd"], 2),
            shannon_amount,
            f"BTC donation +{new_satoshi} sat → {shannon_amount} Shannon minted. "
            f"Tx: {btc_data['last_tx_hash']}",
        ))
        conn.commit()
        conn.close()
        print(f"[btc-monitor] Minted {shannon_amount} Shannon")
        return shannon_amount
    except Exception as e:
        print(f"[btc-monitor] WARNING: Shannon mint failed: {e}", file=sys.stderr)
        return 0

# ── Status JSON ───────────────────────────────────────────────────────────────
def write_status_json(btc_data, new_tx_detected, shannon_minted):
    status = {
        "address":        BTC_ADDRESS,
        "checked_at":     datetime.utcnow().isoformat() + "Z",
        "balance_satoshi": btc_data["balance_satoshi"],
        "balance_btc":    btc_data["balance_btc"],
        "balance_usd":    btc_data["balance_usd"],
        "tx_count":       btc_data["tx_count"],
        "last_tx_hash":   btc_data["last_tx_hash"],
        "btc_price_usd":  btc_data["btc_price_usd"],
        "new_tx_detected": new_tx_detected,
        "shannon_minted_this_run": shannon_minted,
    }
    os.makedirs(os.path.dirname(STATUS_JSON), exist_ok=True)
    with open(STATUS_JSON, "w") as f:
        json.dump(status, f, indent=2)
    return status

# ── Main ──────────────────────────────────────────────────────────────────────
def main():
    print(f"[btc-monitor] Checking {BTC_ADDRESS} …")

    # 1. Fetch live data
    btc_data = fetch_btc_data()
    print(f"[btc-monitor] Balance: {btc_data['balance_satoshi']} sat "
          f"({btc_data['balance_btc']} BTC / ${btc_data['balance_usd']:.2f})")
    print(f"[btc-monitor] Tx count: {btc_data['tx_count']} | Last tx: {btc_data['last_tx_hash']}")

    # 2. Load last snapshot
    conn = ensure_table(AGENCY_DB)
    last = get_last_snapshot(conn)

    new_tx_detected = False
    shannon_minted  = 0

    # 3. Detect new transaction
    if last is None:
        print("[btc-monitor] First run — baseline snapshot saved.")
    else:
        prev_tx  = last["tx_count"]
        curr_tx  = btc_data["tx_count"]
        prev_sat = last["balance_satoshi"]
        curr_sat = btc_data["balance_satoshi"]

        if curr_tx > prev_tx or btc_data["last_tx_hash"] != last["last_tx_hash"]:
            new_tx_detected = True
            gained_sat = max(0, curr_sat - prev_sat)  # net gain (could be 0 if send)
            print(f"[btc-monitor] 🎉 NEW TRANSACTION DETECTED! "
                  f"Tx count {prev_tx} → {curr_tx}, "
                  f"balance change: {gained_sat:+d} sat")

            # Log confession + mint Shannon for inbound amounts
            if gained_sat > 0:
                log_confession(gained_sat, btc_data)
                shannon_minted = mint_shannon(gained_sat, btc_data)
            else:
                log_confession(0, btc_data)
        else:
            print("[btc-monitor] No new transactions since last check.")

    # 4. Save snapshot
    save_snapshot(conn, btc_data)
    conn.close()

    # 5. Write status JSON
    status = write_status_json(btc_data, new_tx_detected, shannon_minted)
    print(f"[btc-monitor] Status written → {STATUS_JSON}")

    # 6. Return structured result for cron announcer
    return status

if __name__ == "__main__":
    result = main()
    print("\n── SUMMARY ──────────────────────────────────")
    print(json.dumps(result, indent=2))
    # Exit 2 signals "new tx detected" to cron wrapper
    if result["new_tx_detected"]:
        sys.exit(2)
