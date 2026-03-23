#!/usr/bin/env python3
"""
token-budget-enforcer daemon - Enforces SR-011: per-agent daily token ceilings
with circuit breaker (1000 tok/h warn, 2000 halt). Integrates with Entropy economy.
"""

import os
import sys
import time
import json
import logging
import sqlite3
import re
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Dict, Any, Optional, Tuple

# Configuration
WORKSPACE = Path("/root/.openclaw/workspace")
LOG_DIR = WORKSPACE / "logs"
DAEMON_LOG = LOG_DIR / "token-budget-enforcer.log"
ENTROPY_DB = WORKSPACE / "entropy_ledger.db"
CHECK_INTERVAL = 60  # seconds

# Token estimation per model (tokens per request estimate)
TOKEN_ESTIMATES = {
    "haiku": 200,       # Typical Haiku request (conservative)
    "grok": 100,        # Grok inference
    "bitnet": 150,      # BitNet local
    "bash_direct": 50,  # Bash operations
    "unknown": 100,     # Default
}

# Whether to ignore historical log entries (only track from now)
IGNORE_HISTORICAL = True

# Setup logging
def setup_logging():
    LOG_DIR.mkdir(exist_ok=True)
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(DAEMON_LOG),
            logging.StreamHandler(sys.stdout)
        ]
    )
    return logging.getLogger(__name__)

class TokenBudgetEnforcer:
    def __init__(self):
        self.log = setup_logging()
        self.db = sqlite3.connect(ENTROPY_DB)
        self.ensure_tables()
        self.log.info("Token Budget Enforcer daemon starting")
        
    def ensure_tables(self):
        """Ensure required tables exist"""
        cursor = self.db.cursor()
        
        # token_budgets table (already created)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS token_budgets (
                agent_id TEXT PRIMARY KEY,
                daily_limit INTEGER DEFAULT 10000,
                hourly_limit INTEGER DEFAULT 1000,
                current_daily_used INTEGER DEFAULT 0,
                current_hourly_used INTEGER DEFAULT 0,
                daily_reset_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                hourly_reset_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                warn_threshold INTEGER DEFAULT 800,
                halt_threshold INTEGER DEFAULT 2000,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # token_usage_log table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS token_usage_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                agent_id TEXT,
                tokens_used INTEGER,
                model TEXT,
                estimated_cost REAL,
                source TEXT,
                session_key TEXT
            )
        """)
        
        # circuit_breaker_events table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS circuit_breaker_events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                agent_id TEXT,
                event_type TEXT,
                tokens_used INTEGER,
                threshold INTEGER,
                action_taken TEXT,
                resolved_at TIMESTAMP
            )
        """)
        
        self.db.commit()
        self.log.debug("Database tables ensured")
    
    def reset_if_needed(self):
        """Reset daily/hourly counters if past reset time"""
        cursor = self.db.cursor()
        now = datetime.now(timezone.utc)
        
        # Reset daily counters
        cursor.execute("""
            UPDATE token_budgets 
            SET current_daily_used = 0,
                daily_reset_at = ?
            WHERE datetime(daily_reset_at) < datetime(?, '-1 day')
        """, (now.isoformat(), now.isoformat()))
        
        # Reset hourly counters
        cursor.execute("""
            UPDATE token_budgets 
            SET current_hourly_used = 0,
                hourly_reset_at = ?
            WHERE datetime(hourly_reset_at) < datetime(?, '-1 hour')
        """, (now.isoformat(), now.isoformat()))
        
        updated = cursor.rowcount
        if updated > 0:
            self.log.info(f"Reset counters for {updated} agent(s)")
        
        self.db.commit()
    
    def parse_slash_truthfully_log(self) -> list:
        """Parse slash-truthfully.log for token usage"""
        log_file = WORKSPACE / "slash-truthfully.log"
        if not log_file.exists():
            return []
        
        entries = []
        # Sample line: [2026-03-14 12:26:50] [INFO] Tier: HAIKU | Cost: $0.00081 | Tokens: 0
        pattern = r'\[(.*?)\] \[INFO\] Tier: (\w+) \| Cost: \$(.*?) \| Tokens: (\d+)'
        
        cutoff_time = None
        if IGNORE_HISTORICAL:
            cutoff_time = datetime.now(timezone.utc) - timedelta(hours=1)
        
        with open(log_file, 'r') as f:
            for line in f:
                match = re.search(pattern, line)
                if match:
                    timestamp_str, tier, cost_str, tokens_str = match.groups()
                    try:
                        timestamp = datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M:%S')
                        timestamp = timestamp.replace(tzinfo=timezone.utc)
                        
                        # Skip old entries if ignoring historical
                        if cutoff_time and timestamp < cutoff_time:
                            continue
                        
                        tokens = int(tokens_str)
                        # Use actual token count if > 0, else use estimate
                        if tokens <= 0:
                            tokens = TOKEN_ESTIMATES.get(tier.lower(), 100)
                        
                        # Default agent is 'fiesta' for main session
                        entries.append({
                            'timestamp': timestamp,
                            'agent_id': 'fiesta',
                            'tokens': tokens,
                            'model': tier.lower(),
                            'cost': float(cost_str),
                            'source': 'slash-truthfully'
                        })
                    except Exception as e:
                        self.log.warning(f"Failed to parse log line: {e}")
        
        return entries
    
    def parse_agent_logs(self) -> list:
        """Parse other agent logs for token usage"""
        entries = []
        # TODO: Implement parsing of other logs
        # For now, return empty
        return entries
    
    def record_token_usage(self, entries: list):
        """Record token usage to database"""
        cursor = self.db.cursor()
        
        for entry in entries:
            # Insert into token_usage_log
            cursor.execute("""
                INSERT INTO token_usage_log 
                (timestamp, agent_id, tokens_used, model, estimated_cost, source)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                entry['timestamp'].isoformat(),
                entry['agent_id'],
                entry['tokens'],
                entry['model'],
                entry.get('cost', 0.0),
                entry['source']
            ))
            
            # Update token_budgets counters
            cursor.execute("""
                UPDATE token_budgets 
                SET current_daily_used = current_daily_used + ?,
                    current_hourly_used = current_hourly_used + ?
                WHERE agent_id = ?
            """, (entry['tokens'], entry['tokens'], entry['agent_id']))
        
        self.db.commit()
        if entries:
            self.log.info(f"Recorded {len(entries)} token usage entries")
    
    def check_limits(self):
        """Check limits and trigger warnings/halts"""
        cursor = self.db.cursor()
        cursor.execute("""
            SELECT agent_id, current_hourly_used, current_daily_used,
                   hourly_limit, daily_limit, warn_threshold, halt_threshold
            FROM token_budgets
        """)
        
        for row in cursor.fetchall():
            agent_id, hourly_used, daily_used, hourly_limit, daily_limit, warn_thresh, halt_thresh = row
            
            # Check hourly halt threshold (SR-011: 2000 halt)
            if hourly_used >= halt_thresh:
                self.trigger_circuit_breaker(agent_id, 'halt', hourly_used, halt_thresh)
            
            # Check hourly warn threshold (SR-011: 1000 warn)
            elif hourly_used >= warn_thresh:
                self.trigger_circuit_breaker(agent_id, 'warn', hourly_used, warn_thresh)
            
            # Check daily limits
            if daily_used >= daily_limit:
                self.trigger_circuit_breaker(agent_id, 'daily_halt', daily_used, daily_limit)
    
    def trigger_circuit_breaker(self, agent_id: str, event_type: str, tokens_used: int, threshold: int):
        """Trigger circuit breaker event"""
        cursor = self.db.cursor()
        
        # Check if this event already active
        cursor.execute("""
            SELECT id FROM circuit_breaker_events 
            WHERE agent_id = ? AND event_type = ? AND resolved_at IS NULL
        """, (agent_id, event_type))
        
        if cursor.fetchone():
            # Event already active
            return
        
        # Determine action
        action = "alert"
        if event_type == 'halt':
            action = "HARD STOP - Block further token usage"
        elif event_type == 'warn':
            action = "WARNING - Approaching limit"
        elif event_type == 'daily_halt':
            action = "DAILY HARD STOP - Daily limit exceeded"
        
        # Log event
        cursor.execute("""
            INSERT INTO circuit_breaker_events 
            (agent_id, event_type, tokens_used, threshold, action_taken)
            VALUES (?, ?, ?, ?, ?)
        """, (agent_id, event_type, tokens_used, threshold, action))
        
        self.db.commit()
        
        # Log to daemon log
        self.log.warning(f"Circuit breaker triggered: {agent_id} {event_type} - {tokens_used}/{threshold} - {action}")
        
        # Mint entropy for security event
        self.mint_security_entropy(agent_id, event_type, tokens_used, threshold)
    
    def mint_security_entropy(self, agent_id: str, event_type: str, tokens_used: int, threshold: int):
        """Mint entropy for token budget events"""
        try:
            # Try to call entropy daemon
            import requests
            payload = {
                "source": "token_budget_enforcer",
                "event": f"token_budget_{event_type}",
                "agent": agent_id,
                "tokens_used": tokens_used,
                "threshold": threshold,
                "timestamp": datetime.now(timezone.utc).isoformat()
            }
            # Assuming entropy daemon runs on 9001
            resp = requests.post(
                "http://127.0.0.1:9001/mint/security",
                json=payload,
                timeout=5
            )
            if resp.status_code == 200:
                self.log.info(f"Minted security entropy: {resp.json()}")
            else:
                self.log.warning(f"Failed to mint entropy: {resp.status_code}")
        except Exception as e:
            self.log.error(f"Error minting entropy: {e}")
    
    def run_cycle(self):
        """Run a single monitoring cycle"""
        self.log.debug("Running token budget check cycle")
        
        # Reset counters if needed
        self.reset_if_needed()
        
        # Parse logs for token usage
        entries = []
        entries.extend(self.parse_slash_truthfully_log())
        entries.extend(self.parse_agent_logs())
        
        # Record usage
        if entries:
            self.record_token_usage(entries)
        
        # Check limits
        self.check_limits()
        
        # Log summary
        self.log_summary()
    
    def log_summary(self):
        """Log current token budget status"""
        cursor = self.db.cursor()
        cursor.execute("""
            SELECT agent_id, current_hourly_used, hourly_limit, 
                   current_daily_used, daily_limit
            FROM token_budgets
        """)
        
        for row in cursor.fetchall():
            agent_id, hourly_used, hourly_limit, daily_used, daily_limit = row
            hourly_percent = (hourly_used / hourly_limit * 100) if hourly_limit > 0 else 0
            daily_percent = (daily_used / daily_limit * 100) if daily_limit > 0 else 0
            
            self.log.debug(
                f"{agent_id}: hourly {hourly_used}/{hourly_limit} ({hourly_percent:.1f}%), "
                f"daily {daily_used}/{daily_limit} ({daily_percent:.1f}%)"
            )
    
    def run(self):
        """Main daemon loop"""
        self.log.info("Starting token budget enforcement loop")
        try:
            while True:
                self.run_cycle()
                time.sleep(CHECK_INTERVAL)
        except KeyboardInterrupt:
            self.log.info("Shutting down gracefully")
        except Exception as e:
            self.log.error(f"Unexpected error: {e}", exc_info=True)
            sys.exit(1)
        finally:
            self.db.close()

if __name__ == "__main__":
    enforcer = TokenBudgetEnforcer()
    enforcer.run()