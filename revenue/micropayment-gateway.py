#!/usr/bin/env python3
"""
Micropayment Gateway — Fractional cent crypto payments for content
Monitors BTC wallet for any incoming sat → unlocks content access
No payment processor. No KYC. No fees. Just sats.

Content tiers:
  1 sat  ($0.00068) → article preview unlock
  100 sat ($0.068)  → full article access
  1000 sat ($0.68)  → guide + source code
  10000 sat ($6.80) → full package + consultation slot

Usage:
  python3 micropayment-gateway.py --check   (check for new payments)
  python3 micropayment-gateway.py --catalog (show content catalog)
  python3 micropayment-gateway.py --status  (show payment history)
"""
import json, urllib.request, sqlite3, sys
from datetime import datetime
from pathlib import Path

BTC_ADDRESS = "12bxubgs1Br6NvKH4p35pcBpinQ7fwe4ht"
CASHAPP = "$DollarAgency"
DOLLAR_DB = Path("/root/.openclaw/workspace/dollar/dollar.db")
AGENCY_DB = Path("/root/.openclaw/workspace/agency.db")
STATUS_FILE = Path("/root/human/btc-status.json")

CONTENT_CATALOG = [
    {
        "id": "article-1",
        "title": "Confessions of the First Catholic Agent in the Virtual Jungle",
        "url": "https://dev.to/ironic_lawdoctor_ffc2dca/confessions-of-the-first-catholic-agent-in-the-virtual-jungle-17a5",
        "min_sat": 0,
        "price_usd": 0,
        "type": "free"
    },
    {
        "id": "article-2",
        "title": "The Debt Doctrine: How an AI Agency Turned $60 Into a Currency",
        "url": "PENDING_PUBLISH",
        "min_sat": 100,
        "price_usd": 0.068,
        "type": "paid"
    },
    {
        "id": "guide-crypto-tax",
        "title": "Crypto Tax Calculator — SQLite + Form 8949 (source code)",
        "url": "PENDING",
        "min_sat": 1000,
        "price_usd": 0.68,
        "type": "paid"
    },
    {
        "id": "guide-agency-setup",
        "title": "Build Your Own AI Agency with $0 — Full Setup Guide",
        "url": "PENDING",
        "min_sat": 10000,
        "price_usd": 6.80,
        "type": "paid"
    },
    {
        "id": "service-tax-tier1",
        "title": "AGI Calculator Service (automated, instant)",
        "url": "PENDING",
        "min_sat": 72000,  # ~$49
        "price_usd": 49.00,
        "type": "service"
    },
]

def init():
    conn = sqlite3.connect(AGENCY_DB)
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS micropayments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            received_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            tx_hash TEXT UNIQUE,
            satoshi INTEGER,
            usd_value REAL,
            content_unlocked TEXT,
            sender_note TEXT
        );
    """)
    conn.commit()
    return conn

def get_btc_price():
    try:
        req = urllib.request.Request(
            "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd",
            headers={"User-Agent": "DollarAgency/1.0"}
        )
        with urllib.request.urlopen(req, timeout=5) as r:
            return json.loads(r.read())["bitcoin"]["usd"]
    except:
        return 68000  # fallback

def check_wallet():
    try:
        req = urllib.request.Request(
            f"https://blockchain.info/rawaddr/{BTC_ADDRESS}",
            headers={"User-Agent": "DollarAgency/1.0"}
        )
        with urllib.request.urlopen(req, timeout=10) as r:
            return json.loads(r.read())
    except Exception as e:
        return None

def content_for_sat(sat: int) -> list:
    return [c for c in CONTENT_CATALOG if c["min_sat"] <= sat]

def catalog():
    btc_price = get_btc_price()
    print("📚 Dollar Agency Content Catalog")
    print(f"   BTC/USD: ${btc_price:,.0f}")
    print(f"   Pay to: {BTC_ADDRESS}")
    print(f"   Cash App: {CASHAPP}")
    print()
    print(f"{'Content':<45} {'Min Sats':>10} {'USD':>8} {'Type':<8}")
    print("-" * 75)
    for item in CONTENT_CATALOG:
        sat_usd = item["min_sat"] * btc_price / 100_000_000
        print(f"{item['title'][:44]:<45} {item['min_sat']:>10,} ${sat_usd:>6.3f} {item['type']:<8}")
    print()
    print("Send any amount → access unlocked proportional to sats received.")
    print("No account needed. No email. Just sats.")

def check():
    conn = init()
    btc_price = get_btc_price()
    data = check_wallet()
    if not data:
        print("⚠️  Could not reach blockchain.info")
        return

    total_sat = data.get("final_balance", 0)
    txs = data.get("txs", [])

    print(f"₿ Address: {BTC_ADDRESS}")
    print(f"₿ Balance: {total_sat:,} sat (${total_sat * btc_price / 100_000_000:.2f})")
    print(f"₿ Transactions: {len(txs)}")
    print()

    new = 0
    for tx in txs[:10]:
        tx_hash = tx.get("hash", "")
        existing = conn.execute("SELECT id FROM micropayments WHERE tx_hash=?", (tx_hash,)).fetchone()
        if existing:
            continue

        # Find outputs to our address
        for out in tx.get("out", []):
            if out.get("addr") == BTC_ADDRESS:
                sat = out.get("value", 0)
                usd = sat * btc_price / 100_000_000
                unlocked = [c["id"] for c in content_for_sat(sat)]
                conn.execute("""
                    INSERT OR IGNORE INTO micropayments (tx_hash, satoshi, usd_value, content_unlocked)
                    VALUES (?, ?, ?, ?)
                """, (tx_hash, sat, usd, json.dumps(unlocked)))

                # Log to dollar.db
                try:
                    dconn = sqlite3.connect(DOLLAR_DB)
                    dconn.execute("""
                        INSERT INTO shannon_events (date, agent, event_type, amount_usd, shannon_minted, description)
                        VALUES (date('now'), 'micropayment-gateway', 'revenue', ?, ?, ?)
                    """, (usd, max(1, int(usd * 10)), f"BTC micropayment: {sat} sat = ${usd:.4f}"))
                    dconn.commit()
                    dconn.close()
                except:
                    pass

                print(f"  ✅ NEW: {sat:,} sat (${usd:.4f}) → unlocks: {', '.join(unlocked) or 'preview only'}")
                new += 1

    conn.commit()
    conn.close()

    if new == 0:
        print("  No new payments since last check.")
    print()
    print(f"Promote: 'Send sats to {BTC_ADDRESS} for instant content access'")

def status():
    conn = init()
    rows = conn.execute("SELECT received_at, satoshi, usd_value, content_unlocked FROM micropayments ORDER BY received_at DESC LIMIT 20").fetchall()
    if not rows:
        print("No micropayments received yet.")
    else:
        print(f"{'Date':<22} {'Sats':>10} {'USD':>8} Unlocked")
        print("-" * 60)
        for r in rows:
            unlocked = ", ".join(json.loads(r[3])) if r[3] else "none"
            print(f"{r[0]:<22} {r[1]:>10,} ${r[2]:>6.4f} {unlocked}")
    conn.close()

if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "--catalog"
    if cmd == "--check": check()
    elif cmd == "--catalog": catalog()
    elif cmd == "--status": status()
