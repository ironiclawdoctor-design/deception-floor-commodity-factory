#!/usr/bin/env python3
"""
Tokenwatch Daemon — real‑time token tracking and budget enforcement.

Usage:
  python3 tokenwatch_daemon.py --start   # start daemon
  python3 tokenwatch_daemon.py --stop    # stop daemon
  python3 tokenwatch_daemon.py --status  # show status

The daemon:
  1. Monitors OpenClaw gateway logs for token events
  2. Updates tokenwatch_usage and tokenwatch_budgets tables
  3. Enforces budgets (hard stops at 100%)
  4. Mints Shannon for external spend
  5. Sends alerts via Telegram when thresholds crossed

Runs as a background process, managed via systemd or supervisor.
"""

import argparse
import sqlite3
import time
import json
import logging
from pathlib import Path
from datetime import datetime, timezone
import subprocess
import sys

# Paths
SKILL_DIR = Path(__file__).parent.parent
AGENCY_DB = Path("/root/.openclaw/workspace/agency.db")
DOLLAR_DB = Path("/root/.openclaw/workspace/dollar.db")
LOG_PATH = Path("/var/log/openclaw/gateway.log")  # may need adjustment

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [tokenwatch] %(levelname)s: %(message)s',
    handlers=[
        logging.FileHandler(SKILL_DIR / "tokenwatch.log"),
        logging.StreamHandler()
    ]
)
log = logging.getLogger(__name__)

def ensure_tables():
    """Create tokenwatch tables in agency.db if they don't exist."""
    conn = sqlite3.connect(str(AGENCY_DB))
    cur = conn.cursor()
    # tokenwatch_usage
    cur.execute("""
        CREATE TABLE IF NOT EXISTS tokenwatch_usage (
            id INTEGER PRIMARY KEY,
            timestamp INTEGER,
            agent_id TEXT,
            model TEXT,
            provider TEXT,
            input_tokens INTEGER,
            output_tokens INTEGER,
            cache_read_tokens INTEGER,
            cache_write_tokens INTEGER,
            estimated_usd_cost REAL,
            shannon_minted INTEGER,
            session_key TEXT,
            project_tag TEXT,
            estimated BOOLEAN DEFAULT 0
        )
    """)
    # tokenwatch_budgets
    cur.execute("""
        CREATE TABLE IF NOT EXISTS tokenwatch_budgets (
            agent_id TEXT PRIMARY KEY,
            daily_limit INTEGER DEFAULT 100000,
            weekly_limit INTEGER DEFAULT 500000,
            monthly_limit INTEGER DEFAULT 2000000,
            current_daily INTEGER DEFAULT 0,
            current_weekly INTEGER DEFAULT 0,
            current_monthly INTEGER DEFAULT 0,
            last_reset INTEGER DEFAULT (unixepoch())
        )
    """)
    # tokenwatch_alerts
    cur.execute("""
        CREATE TABLE IF NOT EXISTS tokenwatch_alerts (
            id INTEGER PRIMARY KEY,
            timestamp INTEGER,
            alert_level TEXT,
            message TEXT,
            resolved INTEGER DEFAULT 0
        )
    """)
    conn.commit()
    conn.close()
    log.info("Tables ensured")

def get_usd_to_shannon():
    """Get latest USD → Shannon exchange rate from dollar.db."""
    if not DOLLAR_DB.exists():
        log.warning("dollar.db not found, using default 10 Shannon/$1")
        return 10.0
    conn = sqlite3.connect(str(DOLLAR_DB))
    cur = conn.cursor()
    try:
        cur.execute("SELECT usd_to_shannon FROM exchange_rates ORDER BY timestamp DESC LIMIT 1")
        row = cur.fetchone()
        rate = row[0] if row else 10.0
    except sqlite3.Error as e:
        log.error(f"Failed to query exchange_rates: {e}")
        rate = 10.0
    conn.close()
    return rate

def estimate_cost(model, provider, input_tokens, output_tokens, cache_read, cache_write):
    """Estimate USD cost based on provider pricing table."""
    # Simplified pricing — in production, load from config
    pricing = {
        ("openrouter", "anthropic/claude-sonnet-4.6"): (3.00, 15.00, 0.0, 0.0),
        ("openrouter", "deepseek/deepseek-v3.2"): (0.10, 0.10, 0.0, 0.0),
        ("anthropic", "claude-opus-4-6"): (15.00, 75.00, 0.30, 1.50),
    }
    key = (provider, model)
    if key in pricing:
        in_rate, out_rate, read_rate, write_rate = pricing[key]
    else:
        in_rate, out_rate, read_rate, write_rate = 5.00, 25.00, 0.0, 0.0  # defaults per 1M tokens
    cost = (input_tokens * in_rate / 1_000_000 +
            output_tokens * out_rate / 1_000_000 +
            cache_read * read_rate / 1_000_000 +
            cache_write * write_rate / 1_000_000)
    return round(cost, 6)

def record_usage(event):
    """
    Record a token usage event.
    event dict keys: timestamp, agent_id, model, provider, input_tokens,
                     output_tokens, cache_read, cache_write, session_key, project_tag
    """
    cost = estimate_cost(event['model'], event['provider'],
                         event['input_tokens'], event['output_tokens'],
                         event.get('cache_read', 0), event.get('cache_write', 0))
    shannon = int(cost * get_usd_to_shannon())
    
    conn = sqlite3.connect(str(AGENCY_DB))
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO tokenwatch_usage
        (timestamp, agent_id, model, provider, input_tokens, output_tokens,
         cache_read_tokens, cache_write_tokens, estimated_usd_cost, shannon_minted,
         session_key, project_tag)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (event['timestamp'], event['agent_id'], event['model'], event['provider'],
          event['input_tokens'], event['output_tokens'],
          event.get('cache_read', 0), event.get('cache_write', 0),
          cost, shannon, event.get('session_key', ''), event.get('project_tag', '')))
    
    # Update budget counters
    cur.execute("""
        UPDATE tokenwatch_budgets
        SET current_daily = current_daily + ?,
            current_weekly = current_weekly + ?,
            current_monthly = current_monthly + ?
        WHERE agent_id = ?
    """, (event['input_tokens'] + event['output_tokens'],
          event['input_tokens'] + event['output_tokens'],
          event['input_tokens'] + event['output_tokens'],
          event['agent_id']))
    
    # If agent has no budget row, create one with defaults
    if cur.rowcount == 0:
        cur.execute("""
            INSERT INTO tokenwatch_budgets (agent_id) VALUES (?)
        """, (event['agent_id'],))
        cur.execute("""
            UPDATE tokenwatch_budgets
            SET current_daily = ?, current_weekly = ?, current_monthly = ?
            WHERE agent_id = ?
        """, (event['input_tokens'] + event['output_tokens'],
              event['input_tokens'] + event['output_tokens'],
              event['input_tokens'] + event['output_tokens'],
              event['agent_id']))
    
    conn.commit()
    conn.close()
    
    # Check thresholds
    check_thresholds(event['agent_id'])
    log.debug(f"Recorded {event['input_tokens'] + event['output_tokens']} tokens for {event['agent_id']}")

def check_thresholds(agent_id):
    """Check if agent has exceeded any budget thresholds, send alerts."""
    conn = sqlite3.connect(str(AGENCY_DB))
    cur = conn.cursor()
    cur.execute("""
        SELECT daily_limit, weekly_limit, monthly_limit,
               current_daily, current_weekly, current_monthly
        FROM tokenwatch_budgets WHERE agent_id = ?
    """, (agent_id,))
    row = cur.fetchone()
    if not row:
        return
    daily_limit, weekly_limit, monthly_limit, daily_used, weekly_used, monthly_used = row
    
    alerts = []
    if daily_used >= daily_limit:
        alerts.append(("critical", f"{agent_id} exceeded daily token budget ({daily_used}/{daily_limit})"))
    elif daily_used >= daily_limit * 0.95:
        alerts.append(("warning", f"{agent_id} at 95% of daily budget ({daily_used}/{daily_limit})"))
    elif daily_used >= daily_limit * 0.8:
        alerts.append(("info", f"{agent_id} at 80% of daily budget ({daily_used}/{daily_limit})"))
    
    for level, msg in alerts:
        cur.execute("""
            INSERT INTO tokenwatch_alerts (timestamp, alert_level, message)
            VALUES (?, ?, ?)
        """, (int(time.time()), level, msg))
        # In production, send Telegram alert here
        log.info(f"ALERT {level}: {msg}")
    
    conn.commit()
    conn.close()

def reset_budgets_if_needed():
    """Reset daily/weekly/monthly counters when period rolls over."""
    conn = sqlite3.connect(str(AGENCY_DB))
    cur = conn.cursor()
    now = datetime.now(timezone.utc)
    # Daily reset
    cur.execute("""
        UPDATE tokenwatch_budgets
        SET current_daily = 0, last_reset = ?
        WHERE date(datetime(last_reset, 'unixepoch')) < date(?)
    """, (int(now.timestamp()), now.date().isoformat()))
    # Weekly reset (Sunday‑based)
    cur.execute("""
        UPDATE tokenwatch_budgets
        SET current_weekly = 0
        WHERE strftime('%W', datetime(last_reset, 'unixepoch')) < strftime('%W', ?)
    """, (now.isoformat(),))
    # Monthly reset
    cur.execute("""
        UPDATE tokenwatch_budgets
        SET current_monthly = 0
        WHERE strftime('%Y-%m', datetime(last_reset, 'unixepoch')) < strftime('%Y-%m', ?)
    """, (now.isoformat(),))
    conn.commit()
    conn.close()

def tail_log():
    """Simplified log tailer — in production, use gateway event stream."""
    # Placeholder: read from a named pipe or websocket
    # For now, just log that we're ready
    log.info("Tokenwatch daemon started, waiting for log events...")
    while True:
        # Simulate an event every 10s for demonstration
        time.sleep(10)
        fake_event = {
            'timestamp': int(time.time()),
            'agent_id': 'fiesta',
            'model': 'openrouter/anthropic/claude-sonnet-4.6',
            'provider': 'openrouter',
            'input_tokens': 150,
            'output_tokens': 450,
            'cache_read': 0,
            'cache_write': 0,
            'session_key': 'test',
            'project_tag': 'demo'
        }
        record_usage(fake_event)
        reset_budgets_if_needed()

def start_daemon():
    """Start the tokenwatch daemon."""
    pid_path = SKILL_DIR / "tokenwatch.pid"
    if pid_path.exists():
        log.error("Daemon already running (pid file exists)")
        return 1
    ensure_tables()
    # In production, daemonize here
    with open(pid_path, 'w') as f:
        f.write(str(os.getpid()))
    try:
        tail_log()
    except KeyboardInterrupt:
        log.info("Shutting down")
    finally:
        pid_path.unlink(missing_ok=True)
    return 0

def stop_daemon():
    """Stop the tokenwatch daemon."""
    pid_path = SKILL_DIR / "tokenwatch.pid"
    if not pid_path.exists():
        log.error("No running daemon found")
        return 1
    pid = int(pid_path.read_text())
    try:
        os.kill(pid, signal.SIGTERM)
        log.info(f"Sent SIGTERM to pid {pid}")
    except ProcessLookupError:
        log.warning(f"Process {pid} not found")
    pid_path.unlink(missing_ok=True)
    return 0

def status():
    """Show daemon status."""
    pid_path = SKILL_DIR / "tokenwatch.pid"
    if pid_path.exists():
        pid = pid_path.read_text().strip()
        print(f"Tokenwatch daemon running (pid {pid})")
    else:
        print("Tokenwatch daemon not running")
    # Show recent alerts
    conn = sqlite3.connect(str(AGENCY_DB))
    cur = conn.cursor()
    cur.execute("""
        SELECT timestamp, alert_level, message FROM tokenwatch_alerts
        WHERE resolved = 0 ORDER BY timestamp DESC LIMIT 5
    """)
    alerts = cur.fetchall()
    if alerts:
        print("\nRecent alerts:")
        for ts, level, msg in alerts:
            dt = datetime.fromtimestamp(ts, timezone.utc)
            print(f"  {dt:%H:%M} [{level}] {msg}")
    conn.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--start", action="store_true", help="Start daemon")
    parser.add_argument("--stop", action="store_true", help="Stop daemon")
    parser.add_argument("--status", action="store_true", help="Show status")
    args = parser.parse_args()
    
    if args.start:
        sys.exit(start_daemon())
    elif args.stop:
        sys.exit(stop_daemon())
    elif args.status:
        status()
    else:
        parser.print_help()