#!/usr/bin/env python3
"""
ampere-referral-tracker.py — Ampere Referral Counter & Revenue Projector

Tracks referral clicks and conversions for ampere.sh/?ref=nathanielxz
Stores in agency.db. Generates shareable text snippets.
Projects revenue based on conversion assumptions.

Usage:
  python3 ampere-referral-tracker.py            # Show dashboard
  python3 ampere-referral-tracker.py --snippet  # Generate shareable snippet
  python3 ampere-referral-tracker.py --record   # Record a click/conversion
  python3 ampere-referral-tracker.py --convert  # Record a confirmed conversion

Revenue model: $20/month per active Ampere referral (standard plan)
"""

import argparse
import sqlite3
import sys
from datetime import date, datetime
from pathlib import Path

AGENCY_DB = Path(__file__).parent.parent / "agency.db"
REFERRAL_URL = "https://www.ampere.sh/?ref=nathanielxz"
REFERRAL_CODE = "nathanielxz"
MONTHLY_RATE = 20.0  # USD per active referral per month
SHANNON_PER_USD = 10


def ensure_tables(conn: sqlite3.Connection):
    """Create referral tracking tables if they don't exist."""
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS referral_clicks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            platform TEXT,
            source_note TEXT,
            clicked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS referral_conversions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            platform TEXT,
            confirmed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            monthly_value REAL DEFAULT 20.0,
            active INTEGER DEFAULT 1,
            notes TEXT
        );

        CREATE TABLE IF NOT EXISTS referral_snippets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            platform TEXT,
            content TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            times_used INTEGER DEFAULT 0
        );
    """)
    conn.commit()


def get_stats(conn: sqlite3.Connection) -> dict:
    """Get current referral stats."""
    total_clicks = conn.execute("SELECT COUNT(*) FROM referral_clicks").fetchone()[0]
    active_conversions = conn.execute(
        "SELECT COUNT(*) FROM referral_conversions WHERE active = 1"
    ).fetchone()[0]
    total_conversions = conn.execute(
        "SELECT COUNT(*) FROM referral_conversions"
    ).fetchone()[0]

    monthly_revenue = active_conversions * MONTHLY_RATE
    annual_revenue = monthly_revenue * 12
    shannon_from_referrals = int(monthly_revenue * SHANNON_PER_USD)

    return {
        "total_clicks": total_clicks,
        "active_conversions": active_conversions,
        "total_conversions": total_conversions,
        "monthly_revenue_usd": monthly_revenue,
        "annual_revenue_usd": annual_revenue,
        "shannon_per_month": shannon_from_referrals,
        "hosting_covered": monthly_revenue >= 20.0,  # Ampere base plan
    }


def generate_snippets() -> list[dict]:
    """Generate shareable text snippets for different platforms."""
    snippets = [
        {
            "platform": "twitter",
            "label": "Twitter/X (Short)",
            "content": f"""I'm running AI agents on @ampere_sh for $20/month.
No GCP, no AWS, no vendor lock-in. Just honest compute.

If you're building agents: {REFERRAL_URL}

(That's a referral link — I get $20 if you sign up, you get a solid server)"""
        },
        {
            "platform": "devto",
            "label": "dev.to article CTA",
            "content": f"""---
*Dollar runs on [Ampere.sh]({REFERRAL_URL}) — $20/month, honest compute, 
no hallucination about the price. If you're running agents, this is where to do it.*
---"""
        },
        {
            "platform": "reddit",
            "label": "Reddit / HN (Transparent)",
            "content": f"""I've been running AI agents on Ampere.sh for the past few weeks.
$20/month, ARM compute, no port restrictions on the higher tiers.

Referral link (I get credit if you sign up): {REFERRAL_URL}
Direct link: https://www.ampere.sh/

Happy to answer questions about the setup."""
        },
        {
            "platform": "discord",
            "label": "Discord / Slack",
            "content": f"""Anyone running AI agents on a budget? Been using Ampere.sh — $20/month ARM server, solid for agent hosting.

Referral: {REFERRAL_URL} (disclosure: I get $20/month credit per signup)"""
        },
        {
            "platform": "telegram",
            "label": "Telegram / Personal",
            "content": f"""Hey — if you need a cheap server for running bots or AI agents, I'm on Ampere.sh. $20/month, been solid.

Here's my referral link: {REFERRAL_URL}
(I get credit, you get good compute — win/win)"""
        },
    ]
    return snippets


def print_dashboard(conn: sqlite3.Connection):
    """Print the referral dashboard."""
    stats = get_stats(conn)
    ts = datetime.now().strftime("%Y-%m-%d %H:%M")

    print(f"""
╔══════════════════════════════════════════╗
║     AMPERE REFERRAL TRACKER              ║
║     As of: {ts}             ║
╠══════════════════════════════════════════╣
║  Referral code: {REFERRAL_CODE:<24} ║
║  URL: {REFERRAL_URL[:35]:<35}  ║
╠══════════════════════════════════════════╣
║  METRICS                                 ║
║  Total clicks logged:    {stats['total_clicks']:<15} ║
║  Conversions (active):   {stats['active_conversions']:<15} ║
║  Conversions (total):    {stats['total_conversions']:<15} ║
╠══════════════════════════════════════════╣
║  REVENUE PROJECTION                      ║
║  Monthly (current):      ${stats['monthly_revenue_usd']:<14.2f} ║
║  Annual (current):       ${stats['annual_revenue_usd']:<14.2f} ║
║  Shannon/month:          {stats['shannon_per_month']:<15} ║
║  Hosting covered:        {'✅ YES' if stats['hosting_covered'] else '❌ Need 1 more'}           ║
╠══════════════════════════════════════════╣
║  PROJECTIONS (by referral count)         ║
║  1 referral  = $20/mo  (hosting covered) ║
║  3 referrals = $60/mo  (+$40 profit)     ║
║  5 referrals = $100/mo (solid base)      ║
║  10 referrals = $200/mo + 2000 Shannon   ║
╚══════════════════════════════════════════╝
""")


def main():
    parser = argparse.ArgumentParser(description="Ampere referral tracker")
    parser.add_argument("--snippet", action="store_true", help="Print all shareable snippets")
    parser.add_argument("--record", action="store_true", help="Record a referral click")
    parser.add_argument("--convert", action="store_true", help="Record a confirmed conversion")
    parser.add_argument("--platform", default="unknown", help="Platform for --record/--convert")
    parser.add_argument("--note", default="", help="Optional note")
    args = parser.parse_args()

    if not AGENCY_DB.exists():
        print(f"ERROR: agency.db not found at {AGENCY_DB}", file=sys.stderr)
        sys.exit(1)

    conn = sqlite3.connect(str(AGENCY_DB))
    ensure_tables(conn)

    if args.snippet:
        snippets = generate_snippets()
        for s in snippets:
            print(f"\n{'='*60}")
            print(f"[{s['platform'].upper()}] {s['label']}")
            print('='*60)
            print(s["content"])
        print(f"\n{'='*60}")
        print(f"Referral URL: {REFERRAL_URL}")
        return

    if args.record:
        conn.execute(
            "INSERT INTO referral_clicks (platform, source_note) VALUES (?, ?)",
            (args.platform, args.note)
        )
        conn.commit()
        total = conn.execute("SELECT COUNT(*) FROM referral_clicks").fetchone()[0]
        print(f"✅ Click recorded on {args.platform}. Total clicks: {total}")
        conn.close()
        return

    if args.convert:
        conn.execute(
            "INSERT INTO referral_conversions (platform, notes) VALUES (?, ?)",
            (args.platform, args.note)
        )
        conn.commit()
        active = conn.execute(
            "SELECT COUNT(*) FROM referral_conversions WHERE active = 1"
        ).fetchone()[0]
        monthly = active * MONTHLY_RATE
        print(f"🎉 Conversion recorded! Active referrals: {active}, Monthly revenue: ${monthly:.2f}")
        conn.close()
        return

    # Default: show dashboard
    print_dashboard(conn)
    conn.close()


if __name__ == "__main__":
    main()
