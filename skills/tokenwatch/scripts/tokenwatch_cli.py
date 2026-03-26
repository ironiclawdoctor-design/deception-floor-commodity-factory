#!/usr/bin/env python3
"""
Tokenwatch CLI — budget management and reporting.

Usage:
  tokenwatch_cli.py --budget-set <agent> --daily <tokens> [--weekly <tokens>] [--monthly <tokens>]
  tokenwatch_cli.py --budget-get <agent>
  tokenwatch_cli.py --report runway|burn|usage [--days 7]
  tokenwatch_cli.py --alert-resolve <alert_id>
  tokenwatch_cli.py --override <agent> <tokens> <hours>
"""

import argparse
import sqlite3
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path

AGENCY_DB = Path("/root/.openclaw/workspace/agency.db")
DOLLAR_DB = Path("/root/.openclaw/workspace/dollar.db")

def budget_set(agent, daily=None, weekly=None, monthly=None):
    conn = sqlite3.connect(str(AGENCY_DB))
    cur = conn.cursor()
    updates = []
    params = []
    if daily is not None:
        updates.append("daily_limit = ?")
        params.append(daily)
    if weekly is not None:
        updates.append("weekly_limit = ?")
        params.append(weekly)
    if monthly is not None:
        updates.append("monthly_limit = ?")
        params.append(monthly)
    if not updates:
        print("No limits specified")
        return
    params.append(agent)
    cur.execute(f"""
        INSERT OR REPLACE INTO tokenwatch_budgets
        (agent_id, daily_limit, weekly_limit, monthly_limit, last_reset)
        VALUES (?, COALESCE(?, daily_limit), COALESCE(?, weekly_limit), COALESCE(?, monthly_limit), unixepoch())
    """, (agent, daily, weekly, monthly))
    conn.commit()
    conn.close()
    print(f"Budget set for {agent}")

def budget_get(agent):
    conn = sqlite3.connect(str(AGENCY_DB))
    cur = conn.cursor()
    cur.execute("""
        SELECT daily_limit, weekly_limit, monthly_limit,
               current_daily, current_weekly, current_monthly,
               last_reset
        FROM tokenwatch_budgets WHERE agent_id = ?
    """, (agent,))
    row = cur.fetchone()
    conn.close()
    if not row:
        print(f"No budget found for {agent}")
        return
    d_limit, w_limit, m_limit, d_used, w_used, m_used, last_reset = row
    reset_dt = datetime.fromtimestamp(last_reset, timezone.utc)
    print(f"Budget for {agent} (last reset {reset_dt:%Y-%m-%d %H:%M} UTC):")
    print(f"  Daily:   {d_used:,} / {d_limit:,} tokens ({100*d_used/d_limit:.1f}%)")
    print(f"  Weekly:  {w_used:,} / {w_limit:,} tokens ({100*w_used/w_limit:.1f}%)")
    print(f"  Monthly: {m_used:,} / {m_limit:,} tokens ({100*m_used/m_limit:.1f}%)")

def report_runway():
    if not DOLLAR_DB.exists():
        print("dollar.db not found")
        return
    conn = sqlite3.connect(str(DOLLAR_DB))
    cur = conn.cursor()
    cur.execute("SELECT usd_to_shannon FROM exchange_rates ORDER BY timestamp DESC LIMIT 1")
    row = cur.fetchone()
    rate = row[0] if row else 10.0
    # Sum backing (simplified)
    cur.execute("SELECT SUM(amount) FROM token_ledger WHERE memo LIKE 'backing%'")
    backing = cur.fetchone()[0] or 0
    conn.close()
    
    conn = sqlite3.connect(str(AGENCY_DB))
    cur = conn.cursor()
    week_ago = int((datetime.now(timezone.utc) - timedelta(days=7)).timestamp())
    cur.execute("""
        SELECT SUM(input_tokens + output_tokens) FROM tokenwatch_usage WHERE timestamp >= ?
    """, (week_ago,))
    tokens_7d = cur.fetchone()[0] or 0
    conn.close()
    
    burn_rate = tokens_7d / 7  # tokens per day
    usd_burn = burn_rate * 5.0 / 1_000_000  # approximate $ per token
    shannon_burn = usd_burn * rate
    runway = backing / shannon_burn if shannon_burn > 0 else float('inf')
    
    print(f"Shannon backing: {backing:,}")
    print(f"Burn rate: {burn_rate:,.0f} tokens/day ({shannon_burn:.0f} Shannon/day)")
    print(f"Runway: {runway:.1f} days")
    if runway < 7:
        print("⚠️  Runway < 7 days — consider adding backing")
    elif runway < 14:
        print("⚠️  Runway < 14 days — monitor closely")

def report_burn(days=7):
    conn = sqlite3.connect(str(AGENCY_DB))
    cur = conn.cursor()
    since = int((datetime.now(timezone.utc) - timedelta(days=days)).timestamp())
    cur.execute("""
        SELECT agent_id, SUM(input_tokens + output_tokens) as total
        FROM tokenwatch_usage WHERE timestamp >= ?
        GROUP BY agent_id ORDER BY total DESC
    """, (since,))
    rows = cur.fetchall()
    conn.close()
    print(f"Top token burners (last {days} days):")
    for agent, total in rows:
        print(f"  {agent}: {total:,} tokens")

def alert_resolve(alert_id):
    conn = sqlite3.connect(str(AGENCY_DB))
    cur = conn.cursor()
    cur.execute("UPDATE tokenwatch_alerts SET resolved = 1 WHERE id = ?", (alert_id,))
    conn.commit()
    conn.close()
    print(f"Alert {alert_id} resolved")

def override(agent, tokens, hours):
    # In production, write to tokenwatch_override_log and adjust budget temporarily
    print(f"Override for {agent}: +{tokens} tokens for {hours} hours (not yet implemented)")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--budget-set", metavar="AGENT", help="Set budget for agent")
    parser.add_argument("--daily", type=int, help="Daily token limit")
    parser.add_argument("--weekly", type=int, help="Weekly token limit")
    parser.add_argument("--monthly", type=int, help="Monthly token limit")
    parser.add_argument("--budget-get", metavar="AGENT", help="Get budget for agent")
    parser.add_argument("--report", choices=["runway", "burn", "usage"], help="Generate report")
    parser.add_argument("--days", type=int, default=7, help="Days for burn report")
    parser.add_argument("--alert-resolve", type=int, help="Resolve alert by ID")
    parser.add_argument("--override", nargs=3, metavar=("AGENT", "TOKENS", "HOURS"), help="Grant temporary override")
    args = parser.parse_args()
    
    if args.budget_set:
        budget_set(args.budget_set, args.daily, args.weekly, args.monthly)
    elif args.budget_get:
        budget_get(args.budget_get)
    elif args.report == "runway":
        report_runway()
    elif args.report == "burn":
        report_burn(args.days)
    elif args.report == "usage":
        print("Usage report not yet implemented")
    elif args.alert_resolve:
        alert_resolve(args.alert_resolve)
    elif args.override:
        override(args.override[0], int(args.override[1]), int(args.override[2]))
    else:
        parser.print_help()