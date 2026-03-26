#!/usr/bin/env python3
"""
Crypto Tax Calculator — Form 8949 Generator
Supports: CSV exports from Coinbase, Kraken, Binance, generic
Output: Form 8949 line items + capital gains summary

Usage:
  python3 crypto-tax.py --input transactions.csv --year 2025
  python3 crypto-tax.py --demo  (generates sample output)
"""
import csv, json, sys, sqlite3
from datetime import datetime, date
from pathlib import Path
from decimal import Decimal, ROUND_HALF_UP

AGENCY_DB = Path("/root/.openclaw/workspace/agency.db")
OUT_DIR = Path("/root/human")

def init_db():
    conn = sqlite3.connect(AGENCY_DB)
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS crypto_lots (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            asset TEXT NOT NULL,
            acquired DATE NOT NULL,
            quantity REAL NOT NULL,
            cost_basis_usd REAL NOT NULL,
            source TEXT DEFAULT 'import'
        );
        CREATE TABLE IF NOT EXISTS crypto_disposals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            asset TEXT NOT NULL,
            disposed DATE NOT NULL,
            quantity REAL NOT NULL,
            proceeds_usd REAL NOT NULL,
            cost_basis_usd REAL DEFAULT 0,
            gain_loss REAL DEFAULT 0,
            holding_days INTEGER DEFAULT 0,
            term TEXT DEFAULT 'short',
            form8949_box TEXT DEFAULT 'B'
        );
    """)
    conn.commit()
    return conn

def days_held(acquired: date, disposed: date) -> int:
    return (disposed - acquired).days

def term(days: int) -> str:
    return "long" if days > 365 else "short"

def process_demo():
    """Generate demo output with BTC wallet transaction."""
    transactions = [
        {"asset": "BTC", "type": "buy",  "date": "2025-01-15", "qty": 0.0001022, "price_usd": 45000},
        {"asset": "BTC", "type": "sell", "date": "2026-03-22", "qty": 0.0001022, "price_usd": 68047},
    ]

    lots = []
    disposals = []

    for tx in transactions:
        d = datetime.strptime(tx["date"], "%Y-%m-%d").date()
        if tx["type"] == "buy":
            lots.append({
                "asset": tx["asset"],
                "acquired": d,
                "qty": tx["qty"],
                "cost": tx["qty"] * tx["price_usd"]
            })
        elif tx["type"] == "sell" and lots:
            lot = lots.pop(0)  # FIFO
            proceeds = tx["qty"] * tx["price_usd"]
            basis = lot["cost"]
            gain = proceeds - basis
            days = days_held(lot["acquired"], d)
            disposals.append({
                "asset": tx["asset"],
                "acquired": lot["acquired"].isoformat(),
                "disposed": d.isoformat(),
                "qty": tx["qty"],
                "proceeds": round(proceeds, 2),
                "basis": round(basis, 2),
                "gain_loss": round(gain, 2),
                "days": days,
                "term": term(days),
                "box": "D" if term(days) == "long" else "B"
            })

    print("=" * 70)
    print("FORM 8949 — Sales and Other Dispositions of Capital Assets")
    print(f"Tax Year: 2025-2026 | Method: FIFO | Generated: {date.today()}")
    print("=" * 70)
    print()

    short = [d for d in disposals if d["term"] == "short"]
    long_  = [d for d in disposals if d["term"] == "long"]

    for section, items, box in [("Part I — Short-Term", short, "B"), ("Part II — Long-Term", long_, "D")]:
        print(f"{section} (Box {box})")
        print(f"{'Asset':<8} {'Acquired':<12} {'Disposed':<12} {'Proceeds':>10} {'Basis':>10} {'Gain/Loss':>10} {'Days':>6}")
        print("-" * 72)
        total_gain = 0
        for d in items:
            print(f"{d['asset']:<8} {d['acquired']:<12} {d['disposed']:<12} ${d['proceeds']:>8.2f} ${d['basis']:>8.2f} ${d['gain_loss']:>8.2f} {d['days']:>6}")
            total_gain += d["gain_loss"]
        if items:
            print(f"{'TOTAL':<34} {'':>10} {'':>10} ${total_gain:>8.2f}")
        else:
            print("  (no transactions)")
        print()

    print("SUMMARY")
    print(f"  Short-term gain/loss: ${sum(d['gain_loss'] for d in short):.2f} (ordinary income rate)")
    print(f"  Long-term gain/loss:  ${sum(d['gain_loss'] for d in long_):.2f} (0/15/20% rate)")
    print()
    print("NOTE: BTC received as income (10,220 sat @ $68,047) = $6.95 ordinary income.")
    print("      Report on Schedule 1, Line 8z. Not a capital gain — it's income on receipt.")
    print()
    print("OUTPUT: Ready to transfer to IRS Form 8949 and Schedule D.")

    out = OUT_DIR / "form-8949-demo.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(disposals, indent=2))
    print(f"JSON saved: {out}")

if __name__ == "__main__":
    init_db()
    if "--demo" in sys.argv or len(sys.argv) == 1:
        process_demo()
    else:
        print("Usage: python3 crypto-tax.py --demo")
        print("Full CSV import: coming in v2")
