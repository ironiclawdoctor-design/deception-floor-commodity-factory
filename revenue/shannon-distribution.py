#!/usr/bin/env python3
"""
shannon-distribution.py — Shannon Distribution Planner

Reads the Shannon economy from dollar.db and generates:
1. Distribution ledger (who gets what)
2. Opportunity analysis (what events should mint Shannon)
3. Post-GCP spending plan (when Cloud Run is enabled)

Current state: 600 Shannon, $60 backing, 10 Shannon = $1 USD
Shannon is NOT yet spendable (awaiting GCP Cloud Run activation).
This script plans the distribution so it's ready to execute immediately
when GCP is enabled.

Usage:
  python3 shannon-distribution.py            # Full report
  python3 shannon-distribution.py --ledger   # Distribution ledger only
  python3 shannon-distribution.py --opps     # Minting opportunities
  python3 shannon-distribution.py --plan     # Post-GCP spending plan
"""

import argparse
import sqlite3
from datetime import date, datetime
from pathlib import Path

DOLLAR_DB = Path(__file__).parent.parent / "dollar" / "dollar.db"
AGENCY_DB = Path(__file__).parent.parent / "agency.db"

SHANNON_PER_USD = 10
BACKING_USD = 60.0
TOTAL_SUPPLY = 600


def get_shannon_state(conn: sqlite3.Connection) -> dict:
    """Get current Shannon economy state."""
    row = conn.execute(
        """SELECT shannon_per_usd, usd_per_shannon, total_backing_usd, total_shannon_supply
           FROM exchange_rates ORDER BY date DESC LIMIT 1"""
    ).fetchone()
    if row:
        return {
            "shannon_per_usd": row[0],
            "usd_per_shannon": row[1],
            "backing_usd": row[2],
            "total_supply": row[3],
        }
    return {
        "shannon_per_usd": SHANNON_PER_USD,
        "usd_per_shannon": 1.0 / SHANNON_PER_USD,
        "backing_usd": BACKING_USD,
        "total_supply": TOTAL_SUPPLY,
    }


def get_shannon_events(conn: sqlite3.Connection) -> list:
    """Get all Shannon minting events."""
    rows = conn.execute(
        """SELECT date, agent, event_type, amount_usd, shannon_minted, description
           FROM shannon_events ORDER BY created_at"""
    ).fetchall()
    return rows


def get_confessions(conn: sqlite3.Connection) -> list:
    """Get confession records."""
    rows = conn.execute(
        """SELECT date, agent, failure_type, description, doctrine_extracted, shannon_minted
           FROM confessions ORDER BY created_at"""
    ).fetchall()
    return rows


def generate_distribution_ledger(state: dict, events: list) -> list:
    """
    Generate proposed distribution ledger.
    
    Distribution model:
    - 40% → Operating Reserve (infrastructure costs)
    - 25% → Agent Payroll (agents that generate revenue events)
    - 20% → Content Rewards (article publishes, documentation)
    - 10% → Confession Bounty (doctrine extraction from failures)
    - 5%  → Human Dividend (Nathaniel — the original backer)
    """
    total = state["total_supply"]

    distributions = [
        {
            "category": "Operating Reserve",
            "allocation_pct": 40,
            "shannon_amount": int(total * 0.40),
            "usd_value": int(total * 0.40) / state["shannon_per_usd"],
            "purpose": "Hosting, tokens, API costs. Auto-deployed when Cloud Run active.",
            "trigger": "Monthly cron on the 1st",
            "recipients": ["Ampere infrastructure", "OpenRouter API", "Blockchair API"],
        },
        {
            "category": "Agent Payroll",
            "allocation_pct": 25,
            "shannon_amount": int(total * 0.25),
            "usd_value": int(total * 0.25) / state["shannon_per_usd"],
            "purpose": "Agents that generate revenue events get paid in Shannon.",
            "trigger": "On revenue event detection",
            "recipients": ["donation-tracker", "revenue-architect", "content-agent"],
        },
        {
            "category": "Content Rewards",
            "allocation_pct": 20,
            "shannon_amount": int(total * 0.20),
            "usd_value": int(total * 0.20) / state["shannon_per_usd"],
            "purpose": "Published articles, docs, tutorials. 25 Shannon per article.",
            "trigger": "On dev.to publish confirmed",
            "recipients": ["dollar-persona", "content-agent"],
        },
        {
            "category": "Confession Bounty",
            "allocation_pct": 10,
            "shannon_amount": int(total * 0.10),
            "usd_value": int(total * 0.10) / state["shannon_per_usd"],
            "purpose": "Agents that extract doctrine from failures get 5-10 Shannon.",
            "trigger": "On confession logged with doctrine_extracted",
            "recipients": ["All agents"],
        },
        {
            "category": "Human Dividend",
            "allocation_pct": 5,
            "shannon_amount": int(total * 0.05),
            "usd_value": int(total * 0.05) / state["shannon_per_usd"],
            "purpose": "Nathaniel backed the agency with $60. Shannon dividend for the founder.",
            "trigger": "Monthly — first of month",
            "recipients": ["Nathaniel (human)"],
        },
    ]

    return distributions


def minting_opportunities() -> list:
    """Enumerate Shannon minting opportunities that exist right now."""
    return [
        {
            "event": "Article #2 published to dev.to",
            "shannon_mint": 25,
            "usd_equivalent": 2.50,
            "status": "READY — needs DEV_API_KEY",
            "time_to_execute": "<5 minutes",
            "trigger": "publish-article.py run successfully",
        },
        {
            "event": "BTC donation received (any amount)",
            "shannon_mint": "amount_usd × 10",
            "usd_equivalent": "variable",
            "status": "LIVE — donation-tracker.py monitoring",
            "time_to_execute": "Automatic (15-min cron)",
            "trigger": "donation-tracker.py detects transaction",
        },
        {
            "event": "Ampere referral conversion",
            "shannon_mint": 200,
            "usd_equivalent": 20.0,
            "status": "TRACKING — needs someone to sign up",
            "time_to_execute": "Post conversion confirmation",
            "trigger": "ampere-referral-tracker.py --convert",
        },
        {
            "event": "Article #3 published",
            "shannon_mint": 25,
            "usd_equivalent": 2.50,
            "status": "PLANNED — needs writing",
            "time_to_execute": "<1 day",
            "trigger": "publish-article.py with article #3",
        },
        {
            "event": "Cash App donation received",
            "shannon_mint": "amount_usd × 10",
            "usd_equivalent": "variable",
            "status": "MANUAL — Square token missing",
            "time_to_execute": "Manual check or Square API token",
            "trigger": "Human confirms Cash App receipt",
        },
        {
            "event": "Doctrine confession logged",
            "shannon_mint": 5,
            "usd_equivalent": 0.50,
            "status": "LIVE — any agent can confess",
            "time_to_execute": "Immediate",
            "trigger": "INSERT INTO confessions with doctrine_extracted",
        },
        {
            "event": "Trial balance reconciled",
            "shannon_mint": 10,
            "usd_equivalent": 1.00,
            "status": "READY — dollar.db has transaction data",
            "time_to_execute": "<5 minutes",
            "trigger": "Manual reconciliation of journal entries",
        },
    ]


def post_gcp_plan() -> list:
    """Plan for Shannon spending when Cloud Run is enabled."""
    return [
        {
            "capability": "Shannon → API Access",
            "description": "Agents can spend Shannon to access premium LLM routing (GPT-4, Claude Opus)",
            "cost": "50 Shannon per 1M tokens",
            "requires": "Cloud Run + LLM routing endpoint",
        },
        {
            "capability": "Shannon → Agent Certification",
            "description": "Agents spend Shannon to get certified (adds to payroll eligibility)",
            "cost": "100 Shannon per certification",
            "requires": "Cloud Run + certification endpoint",
        },
        {
            "capability": "Shannon → Hosting Credits",
            "description": "Convert Shannon to Ampere credits (via human intermediary)",
            "cost": "200 Shannon = $20 (1:1 backing ratio)",
            "requires": "Manual conversion by human",
        },
        {
            "capability": "Shannon → External Agents",
            "description": "Pay external contributors in Shannon for skills/code",
            "cost": "Variable (market rate)",
            "requires": "Cloud Run + agent marketplace",
        },
        {
            "capability": "Shannon → Content Bounties",
            "description": "Post bounties for articles, documentation, tutorials",
            "cost": "25-100 Shannon per bounty",
            "requires": "Public endpoint (Cloud Run)",
        },
    ]


def print_full_report(conn: sqlite3.Connection):
    """Print the complete Shannon distribution report."""
    state = get_shannon_state(conn)
    events = get_shannon_events(conn)
    confessions = get_confessions(conn)
    distributions = generate_distribution_ledger(state, events)
    opportunities = minting_opportunities()
    plan = post_gcp_plan()

    ts = datetime.now().strftime("%Y-%m-%d %H:%M UTC")

    print(f"""
╔══════════════════════════════════════════════════════════════╗
║           SHANNON DISTRIBUTION REPORT                        ║
║           Generated: {ts:<38}║
╚══════════════════════════════════════════════════════════════╝

═══ CURRENT STATE ═══
  Backing:        ${state['backing_usd']:.2f} USD
  Total Supply:   {state['total_supply']} Shannon
  Exchange Rate:  {state['shannon_per_usd']} Shannon = $1 USD
  Minting Events: {len(events)} events logged
  Confessions:    {len(confessions)} logged

═══ DISTRIBUTION LEDGER (Proposed) ═══
""")

    for d in distributions:
        print(f"  {d['category']:<25} {d['allocation_pct']:>3}% │ {d['shannon_amount']:>4} Shannon │ ${d['usd_value']:>5.2f}")
        print(f"    Purpose: {d['purpose']}")
        print(f"    Trigger: {d['trigger']}")
        print(f"    Recipients: {', '.join(d['recipients'])}")
        print()

    total_allocated = sum(d["shannon_amount"] for d in distributions)
    print(f"  {'TOTAL':<25} {100:>3}% │ {total_allocated:>4} Shannon │ ${total_allocated/state['shannon_per_usd']:>5.2f}")

    print(f"""
═══ MINTING OPPORTUNITIES ═══
""")
    for op in opportunities:
        status_icon = "✅" if "LIVE" in op["status"] or "READY" in op["status"] else "⏳"
        print(f"  {status_icon} {op['event']}")
        print(f"     Mint: {op['shannon_mint']} Shannon | Status: {op['status']}")
        print(f"     Time: {op['time_to_execute']}")
        print()

    print(f"""
═══ POST-GCP SPENDING PLAN ═══
(Activate by visiting: console.cloud.google.com/apis/library/run.googleapis.com?project=sovereign-see)
""")
    for p in plan:
        print(f"  ◆ {p['capability']}")
        print(f"    {p['description']}")
        print(f"    Cost: {p['cost']}")
        print(f"    Requires: {p['requires']}")
        print()

    print(f"""
═══ UNLOCK PATH ═══
  $60 current backing → 600 Shannon cap
  Each $10 donation   → +100 Shannon minting capacity
  1 Ampere referral   → $20/mo → 200 Shannon/mo NEW minting
  3 articles live     → est. $5-20 tips → 50-200 more Shannon
  GCP enabled (1 click) → Shannon spendable → full economy live

═══ BOTTOM LINE ═══
  Shannon is a backed, evidential currency.
  Every token = $0.10 of real USD already spent.
  Distribution can execute the moment GCP is live.
  Until then: mint, log, accumulate. The ledger is ready.
""")


def main():
    parser = argparse.ArgumentParser(description="Shannon distribution planner")
    parser.add_argument("--ledger", action="store_true", help="Distribution ledger only")
    parser.add_argument("--opps", action="store_true", help="Minting opportunities")
    parser.add_argument("--plan", action="store_true", help="Post-GCP spending plan")
    args = parser.parse_args()

    if not DOLLAR_DB.exists():
        print(f"ERROR: dollar.db not found at {DOLLAR_DB}")
        print(f"Checked: {DOLLAR_DB}")
        import sys; sys.exit(1)

    conn = sqlite3.connect(str(DOLLAR_DB))

    if args.ledger:
        state = get_shannon_state(conn)
        events = get_shannon_events(conn)
        for d in generate_distribution_ledger(state, events):
            print(f"{d['category']}: {d['shannon_amount']} Shannon (${d['usd_value']:.2f})")
    elif args.opps:
        for op in minting_opportunities():
            status_icon = "✅" if "LIVE" in op["status"] or "READY" in op["status"] else "⏳"
            print(f"{status_icon} {op['event']} → {op['shannon_mint']} Shannon [{op['status']}]")
    elif args.plan:
        for p in post_gcp_plan():
            print(f"◆ {p['capability']}: {p['cost']}")
    else:
        print_full_report(conn)

    conn.close()


if __name__ == "__main__":
    main()
