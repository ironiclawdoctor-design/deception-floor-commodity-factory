#!/usr/bin/env python3
"""
donation-tracker.py — BTC Donation Monitor for Fiesta Agency

Monitors BTC address 12bxubgs1Br6NvKH4p35pcBpinQ7fwe4ht via blockchair.com
(free tier, no API key required). Detects new transactions, logs to dollar.db,
and mints Shannon.

Run as cron every 15 minutes:
  */15 * * * * cd /root/.openclaw/workspace && python3 revenue/donation-tracker.py >> /tmp/donation-tracker.log 2>&1

Dependencies: stdlib only (urllib, sqlite3, json)
"""

import json
import sqlite3
import sys
import urllib.request
import urllib.error
from datetime import date, datetime
from pathlib import Path

# Config
BTC_ADDRESS = "12bxubgs1Br6NvKH4p35pcBpinQ7fwe4ht"
# Primary: blockchain.info (free, no key, permissive rate limits)
# Fallback: blockchair.com (may 430 from shared IPs)
BLOCKCHAIN_INFO_URL = f"https://blockchain.info/rawaddr/{BTC_ADDRESS}?limit=50"
BLOCKCHAIR_URL = f"https://api.blockchair.com/bitcoin/dashboards/address/{BTC_ADDRESS}"
DOLLAR_DB = Path(__file__).parent.parent / "dollar" / "dollar.db"
STATE_FILE = Path(__file__).parent / ".donation-tracker-state.json"

# Shannon economy
SHANNON_PER_USD = 10
BTC_TO_USD_APPROX = 65000  # Fallback if price fetch fails

AGENT_NAME = "donation-tracker"


def log(msg: str):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{ts}] {msg}")


def get_btc_price_usd() -> float:
    """Fetch current BTC/USD price from a free API."""
    try:
        url = "https://api.blockchair.com/bitcoin/stats"
        req = urllib.request.Request(url, headers={"User-Agent": "fiesta-agent/1.0"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode())
            price = data.get("data", {}).get("market_price_usd", BTC_TO_USD_APPROX)
            return float(price)
    except Exception as e:
        log(f"Price fetch failed ({e}), using fallback ${BTC_TO_USD_APPROX}")
        return float(BTC_TO_USD_APPROX)


def fetch_address_data() -> dict:
    """
    Fetch address info from blockchain.info (primary) with blockchair fallback.
    Returns normalized dict: {n_tx, final_balance, total_received, txs: [txid, ...]}
    """
    # Try blockchain.info first
    try:
        req = urllib.request.Request(
            BLOCKCHAIN_INFO_URL,
            headers={"User-Agent": "Mozilla/5.0 (compatible; fiesta-agent/1.0)"}
        )
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode())
            txids = [tx["hash"] for tx in data.get("txs", [])]
            return {
                "source": "blockchain.info",
                "n_tx": data.get("n_tx", 0),
                "final_balance": data.get("final_balance", 0),
                "total_received": data.get("total_received", 0),
                "txs": txids,
            }
    except Exception as e:
        log(f"blockchain.info failed ({e}), trying blockchair...")

    # Fallback: blockchair.com
    try:
        req = urllib.request.Request(
            BLOCKCHAIR_URL,
            headers={"User-Agent": "Mozilla/5.0 (compatible; fiesta-agent/1.0)"}
        )
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode())
            addr_data = data["data"][BTC_ADDRESS]
            addr_info = addr_data.get("address", {})
            txids = addr_data.get("transactions", [])
            return {
                "source": "blockchair",
                "n_tx": addr_info.get("transaction_count", 0),
                "final_balance": addr_info.get("balance", 0),
                "total_received": addr_info.get("received", 0),
                "txs": txids,
            }
    except urllib.error.HTTPError as e:
        log(f"blockchair HTTP error {e.code}: {e.reason}")
        sys.exit(1)
    except Exception as e:
        log(f"Both APIs failed. Last error: {e}")
        sys.exit(1)


def load_state() -> dict:
    """Load last-known transaction state."""
    if STATE_FILE.exists():
        with open(STATE_FILE) as f:
            return json.load(f)
    return {"last_tx_count": 0, "last_balance_sat": 0, "seen_txids": []}


def save_state(state: dict):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)


def get_or_create_accounts(conn: sqlite3.Connection) -> tuple[int, int]:
    """Get BTC Asset account and Revenue-Donations account IDs."""
    # BTC asset account
    row = conn.execute(
        "SELECT id FROM accounts WHERE name = 'BTC Wallet' LIMIT 1"
    ).fetchone()
    if row:
        btc_account_id = row[0]
    else:
        conn.execute(
            "INSERT INTO accounts (name, type, currency, description) VALUES (?, ?, ?, ?)",
            ("BTC Wallet", "asset", "BTC", f"BTC address: {BTC_ADDRESS}")
        )
        btc_account_id = conn.execute("SELECT last_insert_rowid()").fetchone()[0]

    # Revenue account
    row = conn.execute(
        "SELECT id FROM accounts WHERE name = 'Revenue - BTC Donations' LIMIT 1"
    ).fetchone()
    if row:
        rev_account_id = row[0]
    else:
        conn.execute(
            "INSERT INTO accounts (name, type, currency, description) VALUES (?, ?, ?, ?)",
            ("Revenue - BTC Donations", "revenue", "USD", "BTC donations converted to USD")
        )
        rev_account_id = conn.execute("SELECT last_insert_rowid()").fetchone()[0]

    conn.commit()
    return btc_account_id, rev_account_id


def get_current_backing(conn: sqlite3.Connection) -> tuple[float, int]:
    """Get current USD backing and Shannon supply from exchange_rates."""
    row = conn.execute(
        "SELECT total_backing_usd, total_shannon_supply FROM exchange_rates ORDER BY date DESC LIMIT 1"
    ).fetchone()
    if row:
        return float(row[0]), int(row[1])
    return 60.0, 600  # Default from known state


def mint_shannon(conn: sqlite3.Connection, amount_usd: float, description: str) -> int:
    """Mint Shannon tokens proportional to USD amount received."""
    current_backing, current_supply = get_current_backing(conn)
    new_shannon = int(amount_usd * SHANNON_PER_USD)
    new_backing = current_backing + amount_usd
    new_supply = current_supply + new_shannon

    # Log Shannon mint event
    conn.execute(
        """INSERT INTO shannon_events (date, agent, event_type, amount_usd, shannon_minted, description)
           VALUES (?, ?, ?, ?, ?, ?)""",
        (date.today().isoformat(), AGENT_NAME, "revenue", amount_usd, new_shannon, description)
    )

    # Update exchange rate record
    today = date.today().isoformat()
    existing = conn.execute(
        "SELECT date FROM exchange_rates WHERE date = ?", (today,)
    ).fetchone()

    if existing:
        conn.execute(
            """UPDATE exchange_rates
               SET total_backing_usd = ?, total_shannon_supply = ?
               WHERE date = ?""",
            (new_backing, new_supply, today)
        )
    else:
        conn.execute(
            """INSERT INTO exchange_rates (date, shannon_per_usd, usd_per_shannon, total_backing_usd, total_shannon_supply)
               VALUES (?, ?, ?, ?, ?)""",
            (today, SHANNON_PER_USD, 1.0 / SHANNON_PER_USD, new_backing, new_supply)
        )

    conn.commit()
    return new_shannon


def log_transaction(conn: sqlite3.Connection, txid: str, amount_btc: float,
                    amount_usd: float, btc_account_id: int, rev_account_id: int):
    """Log a donation transaction to dollar.db."""
    conn.execute(
        """INSERT INTO transactions (date, description, amount, currency,
           debit_account_id, credit_account_id, source, reference, status)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (
            date.today().isoformat(),
            f"BTC donation: {amount_btc:.8f} BTC (≈${amount_usd:.2f} USD)",
            round(amount_usd, 2),
            "USD",
            btc_account_id,
            rev_account_id,
            "bitcoin",
            txid[:64],  # Truncate to fit if schema has limit
            "cleared"
        )
    )
    conn.commit()


def main():
    log(f"Donation tracker starting — watching {BTC_ADDRESS}")

    # Load state
    state = load_state()
    log(f"State: {state['last_tx_count']} txs seen, {len(state['seen_txids'])} txids tracked")

    # Fetch address data
    data = fetch_address_data()

    total_received_sat = data["total_received"]
    balance_sat = data["final_balance"]
    tx_count = data["n_tx"]
    transactions = data["txs"]

    log(f"API source: {data['source']}")

    log(f"Address stats: {tx_count} txs, balance={balance_sat} sat, received={total_received_sat} sat")

    # Check for new transactions
    new_txids = [tx for tx in transactions if tx not in state["seen_txids"]]

    if not new_txids:
        log("No new transactions detected.")
        save_state(state)
        return

    log(f"🎉 Found {len(new_txids)} new transaction(s)!")

    # Fetch BTC price
    btc_price = get_btc_price_usd()
    log(f"BTC price: ${btc_price:,.2f} USD")

    # Connect to dollar.db
    if not DOLLAR_DB.exists():
        log(f"ERROR: dollar.db not found at {DOLLAR_DB}")
        sys.exit(1)

    conn = sqlite3.connect(str(DOLLAR_DB))
    btc_account_id, rev_account_id = get_or_create_accounts(conn)

    # Process new transactions (we don't have per-tx amounts from dashboard endpoint,
    # so we calculate the delta from total received)
    prev_received_sat = state.get("last_received_sat", 0)
    new_received_sat = total_received_sat - prev_received_sat

    if new_received_sat > 0:
        amount_btc = new_received_sat / 1e8
        amount_usd = amount_btc * btc_price

        log(f"New received: {amount_btc:.8f} BTC ≈ ${amount_usd:.2f} USD")

        for txid in new_txids:
            # Approximate split if multiple txs (rare edge case)
            tx_amount_usd = amount_usd / len(new_txids)
            tx_amount_btc = amount_btc / len(new_txids)

            log_transaction(conn, txid, tx_amount_btc, tx_amount_usd,
                           btc_account_id, rev_account_id)
            shannon_minted = mint_shannon(
                conn,
                tx_amount_usd,
                f"BTC donation: {tx_amount_btc:.8f} BTC txid={txid[:16]}..."
            )
            log(f"  ✅ Logged {txid[:16]}... → ${tx_amount_usd:.2f} → {shannon_minted} Shannon minted")
    else:
        log("Transaction(s) detected but no new satoshis received (possible re-org or already counted)")

    conn.close()

    # Update state
    state["last_tx_count"] = tx_count
    state["last_balance_sat"] = balance_sat
    state["last_received_sat"] = total_received_sat
    state["seen_txids"].extend(new_txids)
    # Keep only last 200 txids to avoid unbounded growth
    state["seen_txids"] = state["seen_txids"][-200:]
    save_state(state)

    log("Done.")


if __name__ == "__main__":
    main()
