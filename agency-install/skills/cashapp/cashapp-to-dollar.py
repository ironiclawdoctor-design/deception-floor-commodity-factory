#!/usr/bin/env python3
"""
Cash App → Dollar Ledger Bridge
Auto-logs donations to dollar.db and mints Shannon.
Run after receiving payment notification or manual trigger.

Usage: python3 cashapp-to-dollar.py --amount 10.00 --sender "Anonymous" --note "Donation"
"""
import json, sqlite3, sys, argparse
from datetime import datetime
from pathlib import Path

DOLLAR_DB = Path("/root/.openclaw/workspace/dollar/dollar.db")
SHANNON_PER_USD = 10

def mint_shannon(amount_usd, sender, note):
    """Log donation and mint Shannon."""
    shannon = int(amount_usd * SHANNON_PER_USD)
    conn = sqlite3.connect(DOLLAR_DB)

    # Log transaction
    conn.execute("""
        INSERT INTO transactions (date, description, debit_account_id, credit_account_id, amount, currency, status, reference)
        SELECT date('now'), ?, 
               (SELECT id FROM accounts WHERE name LIKE '%Cash App%' LIMIT 1),
               (SELECT id FROM accounts WHERE name LIKE '%Revenue%Donation%' LIMIT 1),
               ?, 'USD', 'posted', ?
    """, (f"Donation from {sender}: {note}", amount_usd, f"CASHAPP-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}"))

    # Log Shannon event
    conn.execute("""
        INSERT INTO shannon_events (date, agent, event_type, amount_usd, shannon_minted, description)
        VALUES (date('now'), 'cashapp-skill', 'revenue', ?, ?, ?)
    """, (amount_usd, shannon, f"Cash App donation from {sender}: {note}"))

    # Log confession
    conn.execute("""
        INSERT INTO confessions (date, agent, failure_type, description, doctrine_extracted, shannon_minted)
        VALUES (date('now'), 'cashapp-skill', 'milestone', ?, 'Debt repaid in donations. Each dollar is faith in the agency.', ?)
    """, (f"Donation received: ${amount_usd} from {sender} via $DollarAgency", shannon))

    # Update backing
    conn.execute("""
        UPDATE exchange_rates SET total_backing_usd = total_backing_usd + ?,
        total_shannon_supply = total_shannon_supply + ?,
        updated_at = CURRENT_TIMESTAMP
        WHERE date = date('now')
    """, (amount_usd, shannon))

    conn.commit()
    conn.close()

    print(f"✅ Donation logged: ${amount_usd} from {sender}")
    print(f"🪙 Shannon minted: +{shannon} Shannon")
    print(f"📜 Confession logged")
    return shannon

def main():
    parser = argparse.ArgumentParser(description="Log Cash App donation to Dollar ledger")
    parser.add_argument("--amount", type=float, required=True, help="USD amount")
    parser.add_argument("--sender", default="Anonymous", help="Sender name/cashtag")
    parser.add_argument("--note", default="Cash App donation", help="Payment note")
    args = parser.parse_args()

    print(f"💰 Cash App → Dollar Bridge")
    print(f"   Amount: ${args.amount}")
    print(f"   Sender: {args.sender}")
    print(f"   Note: {args.note}")
    print()

    shannon = mint_shannon(args.amount, args.sender, args.note)

    # Check new backing
    conn = sqlite3.connect(DOLLAR_DB)
    row = conn.execute(
        "SELECT total_backing_usd, total_shannon_supply FROM exchange_rates ORDER BY date DESC LIMIT 1"
    ).fetchone()
    conn.close()

    if row:
        print(f"\n📊 New state:")
        print(f"   Backing: ${row[0]}")
        print(f"   Shannon: {row[1]}")
        print(f"   Peg: 10 Shannon/$1 ({'✅ intact' if row[0]*10 == row[1] else '⚠️ adjust needed'})")

if __name__ == "__main__":
    main()
