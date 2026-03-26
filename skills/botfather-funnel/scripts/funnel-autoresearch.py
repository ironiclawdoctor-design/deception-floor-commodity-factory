#!/usr/bin/env python3
"""
funnel-autoresearch.py — Measure bot command → Cash App conversion.
Logs experiment results to references/funnel-experiments.md.

Metric: funnel_conversion_rate = confirmed_donations / bot_interactions
Target: any positive conversion traceable to a bot session.
"""
import sqlite3
import json
from datetime import datetime, timezone

DOLLAR_DB = "/root/.openclaw/workspace/dollar/dollar.db"
AGENCY_DB = "/root/.openclaw/workspace/agency.db"
LOG_PATH = "/root/.openclaw/workspace/skills/botfather-funnel/references/funnel-experiments.md"


def ts():
    return datetime.now(timezone.utc).isoformat()


def get_bot_interactions(conn):
    """Count inbound Telegram messages (proxy for bot command usage)."""
    try:
        result = conn.execute(
            "SELECT COUNT(*) FROM shanrouter_log WHERE source='telegram' AND ts > date('now','-7 days')"
        ).fetchone()
        return result[0] if result else 0
    except Exception:
        return 0


def get_donations_this_week(conn):
    """Count Cash App + BTC donations in last 7 days."""
    try:
        result = conn.execute(
            """SELECT COUNT(*), SUM(amount_usd) FROM shannon_events
               WHERE event_type='revenue'
               AND date >= date('now','-7 days')"""
        ).fetchone()
        return result[0] or 0, result[1] or 0.0
    except Exception:
        return 0, 0.0


def score(interactions, donations):
    if interactions == 0:
        return 0.0
    return round((donations / max(interactions, 1)) * 100, 2)


def log_experiment(run_id, interactions, donation_count, donation_usd, rate, notes=""):
    entry = f"""
## Experiment {run_id} — {ts()[:10]}

| Metric | Value |
|--------|-------|
| Bot interactions (7d) | {interactions} |
| Donations (7d) | {donation_count} |
| Donation USD (7d) | ${donation_usd:.2f} |
| Conversion rate | {rate}% |
| Notes | {notes or 'baseline'} |

"""
    try:
        with open(LOG_PATH, "a") as f:
            f.write(entry)
        print(f"✅ Logged to {LOG_PATH}")
    except Exception as e:
        print(f"⚠️  Could not write log: {e}")


def main():
    print("=" * 50)
    print("BOTFATHER FUNNEL AUTORESEARCH")
    print(f"Run: {ts()}")
    print("=" * 50)

    agency_conn = sqlite3.connect(AGENCY_DB)
    dollar_conn = sqlite3.connect(DOLLAR_DB)

    interactions = get_bot_interactions(agency_conn)
    donation_count, donation_usd = get_donations_this_week(dollar_conn)
    rate = score(interactions, donation_count)

    print(f"\n📊 Week snapshot:")
    print(f"   Bot interactions:  {interactions}")
    print(f"   Donations:         {donation_count} (${donation_usd:.2f})")
    print(f"   Conversion rate:   {rate}%")

    # Experiment ID = count of existing experiments + 1
    try:
        with open(LOG_PATH) as f:
            run_id = f.read().count("## Experiment") + 1
    except FileNotFoundError:
        run_id = 1

    notes = ""
    if interactions == 0:
        notes = "No bot interactions yet — commands not registered or bot not active"
    elif donation_count == 0:
        notes = "Bot active but zero donations — funnel top exists, no conversion"
    else:
        notes = f"CONVERSION CONFIRMED: {donation_count} donation(s) in window"

    log_experiment(run_id, interactions, donation_count, donation_usd, rate, notes)

    print(f"\n{'=' * 50}")
    print(f"RESULT: {rate}% conversion | {notes}")
    print("=" * 50)

    agency_conn.close()
    dollar_conn.close()


if __name__ == "__main__":
    main()
