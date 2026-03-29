#!/usr/bin/env python3
"""
BTC Monitor — Autonomous Bitcoin payment detection for agency-payments skill.
Polls blockchain.info (fallback: blockstream.info) every invocation.
Detects new transactions, calculates USD value, mints Shannon, logs to dollar.db.

Usage:
  python3 btc-monitor.py              # Run once (called by cron)
  python3 btc-monitor.py --dry-run    # Detect but don't write to DB
  python3 btc-monitor.py --force-mint # Force mint even if no new txn (testing)
"""
import json
import sqlite3
import sys
import argparse
import urllib.request
import urllib.error
from datetime import datetime, timezone
from pathlib import Path

# ── Configuration ──────────────────────────────────────────────────────────────
BTC_ADDRESS      = "12bxubgs1Br6NvKH4p35pcBpinQ7fwe4ht"
DOLLAR_DB        = Path("/root/.openclaw/workspace/dollar/dollar.db")
STATE_FILE       = Path("/root/.openclaw/workspace/skills/agency-payments/.btc_last_tx")
FALLBACK_LOG     = Path("/root/.openclaw/workspace/skills/agency-payments/payment-fallback.log")
SKILL_DIR        = Path("/root/.openclaw/workspace/skills/agency-payments")
SHANNON_PER_USD  = 10   # $1 = 10 Shannon

# ── Helpers ────────────────────────────────────────────────────────────────────
def now_utc() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

def log(msg: str):
    ts = now_utc()
    line = f"[{ts}] {msg}"
    print(line)
    # Append to skill log
    try:
        (SKILL_DIR / "btc-monitor.log").open("a").write(line + "\n")
    except Exception:
        pass

# ── BTC API ───────────────────────────────────────────────────────────────────
def fetch_btc_data() -> dict | None:
    """Try blockchain.info first, fall back to blockstream.info."""

    # Primary
    try:
        url = f"https://blockchain.info/rawaddr/{BTC_ADDRESS}"
        req = urllib.request.Request(url, headers={"User-Agent": "agency-payments/1.0"})
        with urllib.request.urlopen(req, timeout=15) as r:
            data = json.loads(r.read())
            return {
                "source": "blockchain.info",
                "balance_sat": data["final_balance"],
                "received_sat": data["total_received"],
                "n_tx": data["n_tx"],
                "txs": data.get("txs", []),
                "raw": data,
            }
    except Exception as e:
        log(f"⚠️  blockchain.info failed: {e} — trying blockstream.info")

    # Fallback
    try:
        url = f"https://blockstream.info/api/address/{BTC_ADDRESS}"
        req = urllib.request.Request(url, headers={"User-Agent": "agency-payments/1.0"})
        with urllib.request.urlopen(req, timeout=15) as r:
            data = json.loads(r.read())
            stats = data["chain_stats"]
            return {
                "source": "blockstream.info",
                "balance_sat": stats["funded_txo_sum"] - stats["spent_txo_sum"],
                "received_sat": stats["funded_txo_sum"],
                "n_tx": stats["tx_count"],
                "txs": [],  # blockstream tx list needs separate call
                "raw": data,
            }
    except Exception as e:
        log(f"❌ blockstream.info also failed: {e}")
        return None

# ── BTC Price ─────────────────────────────────────────────────────────────────
def get_btc_price_usd() -> float:
    """Get current BTC/USD price. Returns 85000 as safe fallback."""
    try:
        url = "https://api.coindesk.com/v1/bpi/currentprice/USD.json"
        req = urllib.request.Request(url, headers={"User-Agent": "agency-payments/1.0"})
        with urllib.request.urlopen(req, timeout=10) as r:
            data = json.loads(r.read())
            return float(data["bpi"]["USD"]["rate_float"])
    except Exception:
        pass
    try:
        # Fallback: coingecko
        url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"
        req = urllib.request.Request(url, headers={"User-Agent": "agency-payments/1.0"})
        with urllib.request.urlopen(req, timeout=10) as r:
            data = json.loads(r.read())
            return float(data["bitcoin"]["usd"])
    except Exception:
        pass
    log("⚠️  Price API failed — using fallback $85,000")
    return 85000.0

# ── State ─────────────────────────────────────────────────────────────────────
def get_last_tx_count() -> int:
    try:
        return int(STATE_FILE.read_text().strip())
    except Exception:
        return 0

def save_tx_count(n: int):
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(str(n))

# ── Shannon Mint ──────────────────────────────────────────────────────────────
def mint_shannon_sqlite(btc_amount: float, amount_usd: float, shannon: int, description: str) -> bool:
    """Write directly to dollar.db via SQLite (SR-001: bypasses approval gateway)."""
    try:
        conn = sqlite3.connect(str(DOLLAR_DB))

        # shannon_events
        conn.execute("""
            INSERT INTO shannon_events (date, agent, event_type, amount_usd, shannon_minted, description)
            VALUES (date('now'), 'agency-payments', 'revenue', ?, ?, ?)
        """, (round(amount_usd, 8), shannon, description))

        # confessions
        conn.execute("""
            INSERT INTO confessions (date, agent, failure_type, description, doctrine_extracted, shannon_minted)
            VALUES (date('now'), 'agency-payments', 'milestone', ?, 'Every satoshi received is a vote of faith in the agency.', ?)
        """, (description, shannon))

        # exchange_rates — update today's row if it exists
        updated = conn.execute("""
            UPDATE exchange_rates
            SET total_backing_usd     = total_backing_usd + ?,
                total_shannon_supply  = total_shannon_supply + ?,
                updated_at            = CURRENT_TIMESTAMP
            WHERE date = date('now')
        """, (round(amount_usd, 8), shannon)).rowcount

        if updated == 0:
            # No row yet for today — insert
            conn.execute("""
                INSERT INTO exchange_rates (date, total_backing_usd, total_shannon_supply)
                VALUES (date('now'), ?, ?)
            """, (round(amount_usd, 8), shannon))

        conn.commit()
        conn.close()
        return True
    except Exception as e:
        log(f"❌ SQLite mint failed: {e}")
        return False

def log_fallback(btc_amount: float, amount_usd: float, shannon: int, description: str):
    """Append to fallback log if DB unavailable."""
    FALLBACK_LOG.parent.mkdir(parents=True, exist_ok=True)
    with FALLBACK_LOG.open("a") as f:
        f.write(f"{now_utc()} | BTC | {btc_amount:.8f} BTC | ${amount_usd:.2f} USD | {shannon} Shannon | {description}\n")

# ── Main ──────────────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description="Agency BTC Monitor")
    parser.add_argument("--dry-run", action="store_true", help="Detect but don't write to DB")
    parser.add_argument("--force-mint", action="store_true", help="Force mint (testing)")
    args = parser.parse_args()

    log(f"🔍 BTC Monitor starting — address: {BTC_ADDRESS}")

    # 1. Fetch blockchain data
    data = fetch_btc_data()
    if data is None:
        log("❌ All blockchain APIs failed — aborting")
        sys.exit(1)

    balance_btc  = data["balance_sat"]  / 1e8
    received_btc = data["received_sat"] / 1e8
    n_tx         = data["n_tx"]
    source       = data["source"]

    log(f"📊 [{source}] Balance: {balance_btc:.8f} BTC | Received: {received_btc:.8f} BTC | Txns: {n_tx}")

    # 2. Check for new transactions
    last_tx = get_last_tx_count()
    new_txns = n_tx - last_tx

    if new_txns <= 0 and not args.force_mint:
        log(f"✅ No new transactions (last seen: {last_tx}, current: {n_tx})")
        return

    if args.force_mint:
        log("⚡ --force-mint: processing as if new transaction")
        new_txns = max(new_txns, 1)

    log(f"🚨 NEW TRANSACTIONS DETECTED: {new_txns} new (was {last_tx}, now {n_tx})")

    # 3. Calculate USD value of new incoming amount
    btc_price = get_btc_price_usd()
    log(f"💱 BTC price: ${btc_price:,.2f}")

    # Estimate: use total received delta (best we can do without full tx parsing)
    # For simplicity: if this is the first tx, use full received amount
    # For subsequent: would need tx-level parsing (blockchain.info provides txs[])
    if last_tx == 0:
        new_btc = received_btc  # First ever detection
    else:
        # Parse individual txs from blockchain.info if available
        new_btc = 0.0
        for tx in data.get("txs", [])[:new_txns]:
            for out in tx.get("out", []):
                if out.get("addr") == BTC_ADDRESS:
                    new_btc += out["value"] / 1e8

        if new_btc == 0:
            # Blockstream fallback — can't get tx breakdown easily
            new_btc = received_btc  # Conservative: use total

    amount_usd = new_btc * btc_price
    shannon    = int(amount_usd * SHANNON_PER_USD)
    description = (
        f"BTC donation: {new_btc:.8f} BTC received at {BTC_ADDRESS} "
        f"(${amount_usd:.2f} USD @ ${btc_price:,.0f}/BTC → {shannon} Shannon)"
    )

    log(f"💰 New BTC: {new_btc:.8f} BTC = ${amount_usd:.2f} USD → {shannon} Shannon")

    if args.dry_run:
        log("🔵 DRY RUN — skipping DB write")
        log(f"   Would mint: {shannon} Shannon")
        log(f"   Would log: {description}")
        return

    # 4. Mint Shannon to dollar.db
    if DOLLAR_DB.exists():
        success = mint_shannon_sqlite(new_btc, amount_usd, shannon, description)
        if success:
            log(f"✅ Shannon minted: +{shannon} to dollar.db")
        else:
            log_fallback(new_btc, amount_usd, shannon, description)
            log(f"⚠️  Logged to fallback: {FALLBACK_LOG}")
    else:
        log(f"⚠️  dollar.db not found at {DOLLAR_DB} — using fallback log")
        log_fallback(new_btc, amount_usd, shannon, description)

    # 5. Save new tx count
    save_tx_count(n_tx)
    log(f"💾 State saved: last_tx = {n_tx}")

    log(f"🎉 Done — {new_txns} new txn(s), {shannon} Shannon minted")

if __name__ == "__main__":
    main()
