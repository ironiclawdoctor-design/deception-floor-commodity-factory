#!/usr/bin/env python3
"""
proactive-supervisor daemon - Oversees agent operations and suggests improvements.
Monitors cron jobs, agent status, token usage, and system health.
"""

import os
import sys
import time
import json
import logging
import subprocess
import requests
import sqlite3
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Dict, Any, List, Optional

# Configuration
WORKSPACE = Path("/root/.openclaw/workspace")
LOG_DIR = WORKSPACE / "logs"
DAEMON_LOG = LOG_DIR / "proactive-supervisor.log"
CONFIG_FILE = WORKSPACE / "daemons" / "proactive-supervisor-config.json"
ENTROPY_URL = "http://127.0.0.1:9001"
FACTORY_URL = "http://127.0.0.1:9000"
CHECK_INTERVAL = 300  # 5 minutes
SUGGESTIONS_FILE = WORKSPACE / "suggestions" / "improvements.json"
AGENCY_AUTH = WORKSPACE / "scripts" / "agency-auth.sh"

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

class ProactiveSupervisorDaemon:
    def __init__(self):
        self.log = setup_logging()
        self.config = self.load_config()
        self.last_suggestions = set()
        self.log.info("Proactive Supervisor daemon starting")
        
    def load_config(self) -> Dict[str, Any]:
        default = {
            "monitor_cron": True,
            "monitor_agents": True,
            "monitor_token_burn": True,
            "suggestion_cooldown_hours": 24,
            "max_suggestions_per_day": 5,
            "suggestions_today": 0,
            "last_suggestion_date": None
        }
        if CONFIG_FILE.exists():
            try:
                with open(CONFIG_FILE) as f:
                    config = json.load(f)
                    default.update(config)
                    return default
            except Exception as e:
                self.log.error(f"Failed to load config: {e}")
        return default
    
    def save_config(self):
        try:
            with open(CONFIG_FILE, 'w') as f:
                json.dump(self.config, f, indent=2)
        except Exception as e:
            self.log.error(f"Failed to save config: {e}")
    
    def check_cron_jobs(self):
        """Monitor cron jobs for failures or optimization opportunities"""
        try:
            # Check OpenClaw cron jobs via gateway API
            # For now, check crontab
            result = subprocess.run(
                ["crontab", "-l"],
                capture_output=True,
                text=True
            )
            cron_count = len([line for line in result.stdout.split('\n') 
                            if line.strip() and not line.startswith('#')])
            
            if cron_count == 0:
                self.make_suggestion(
                    "cron_empty",
                    "SYSTEM_STABLE: Persistent hearts active. Consider adding health checks or automation.",
                    "low"
                )
            elif cron_count > 10:
                self.make_suggestion(
                    "cron_too_many",
                    f"High number of cron jobs ({cron_count}). Consider consolidating.",
                    "medium"
                )
            
        except subprocess.CalledProcessError:
            self.log.debug("No user crontab")
        except Exception as e:
            self.log.error(f"Error checking cron: {e}")
    
    def check_agent_health(self):
        """Check status of key agents and services"""
        try:
            # Use agency-auth.sh to check services
            if AGENCY_AUTH.exists():
                result = subprocess.run(
                    [str(AGENCY_AUTH), "health"],
                    capture_output=True,
                    text=True
                )
                if result.returncode == 0:
                    lines = result.stdout.split('\n')
                    for line in lines:
                        if "DOWN" in line.upper():
                            service = line.split(':')[0].strip()
                            self.make_suggestion(
                                "service_down",
                                f"Service {service} is down. Check logs and restart.",
                                "high"
                            )
                else:
                    self.log.warning("agency-auth health check failed")
        except Exception as e:
            self.log.error(f"Error checking agent health: {e}")
    
    def check_token_usage(self):
        """Analyze token burn patterns and suggest optimizations"""
        token_file = WORKSPACE / ".token-ledger.json"
        if not token_file.exists():
            return
        
        try:
            with open(token_file) as f:
                data = json.load(f)
            
            total_burn = data.get("total_burn", 0)
            daily_burn = data.get("daily_burn", {})
            
            # Check if burn exceeds $5/day threshold
            today = datetime.now(timezone.utc).date().isoformat()
            if today in daily_burn and daily_burn[today] > 5:
                self.make_suggestion(
                    "token_burn_high",
                    f"Token burn today (${daily_burn[today]:.2f}) exceeds $5/day threshold.",
                    "high"
                )
            
            # Check for rapid burn increases
            if len(daily_burn) >= 2:
                days = sorted(daily_burn.keys())
                last_day = days[-1]
                prev_day = days[-2]
                increase = daily_burn[last_day] - daily_burn[prev_day]
                if increase > 2:  # $2 increase day over day
                    self.make_suggestion(
                        "token_burn_spike",
                        f"Token burn increased by ${increase:.2f} from {prev_day} to {last_day}.",
                        "medium"
                    )
                    
        except Exception as e:
            self.log.error(f"Error checking token usage: {e}")
    
    def check_disk_usage(self):
        """Monitor disk space and warn if low"""
        try:
            result = subprocess.run(
                ["df", "-h", "/"],
                capture_output=True,
                text=True
            )
            lines = result.stdout.split('\n')
            if len(lines) >= 2:
                parts = lines[1].split()
                usage_percent = int(parts[4].replace('%', ''))
                if usage_percent > 80:
                    self.make_suggestion(
                        "disk_usage_high",
                        f"Root disk usage is {usage_percent}%. Consider cleaning up.",
                        "medium"
                    )
        except Exception as e:
            self.log.error(f"Error checking disk usage: {e}")
    
    def check_memory_usage(self):
        """Monitor memory usage"""
        try:
            result = subprocess.run(
                ["free", "-m"],
                capture_output=True,
                text=True
            )
            lines = result.stdout.split('\n')
            if len(lines) >= 2:
                parts = lines[1].split()
                total = int(parts[1])
                used = int(parts[2])
                usage_percent = (used / total) * 100
                if usage_percent > 85:
                    self.make_suggestion(
                        "memory_usage_high",
                        f"Memory usage is {usage_percent:.1f}%. Consider optimizing.",
                        "medium"
                    )
        except Exception as e:
            self.log.error(f"Error checking memory usage: {e}")
    
    def check_entropy_economy(self):
        """Check entropy economy health and participation"""
        try:
            resp = requests.get(f"{ENTROPY_URL}/health", timeout=5)
            if resp.status_code == 200:
                data = resp.json()
                balance = data.get("balance", 0)
                if balance < 100:
                    self.make_suggestion(
                        "entropy_low",
                        f"Entropy balance low ({balance}). Consider minting more entropy.",
                        "low"
                    )
            else:
                self.log.warning(f"Entropy health check failed: {resp.status_code}")
        except Exception as e:
            self.log.error(f"Error checking entropy economy: {e}")
    
    def make_suggestion(self, suggestion_id: str, message: str, priority: str):
        """Record and log a suggestion"""
        # Check cooldown
        today = datetime.now(timezone.utc).date().isoformat()
        if self.config["last_suggestion_date"] != today:
            self.config["suggestions_today"] = 0
            self.config["last_suggestion_date"] = today
            self.save_config()
        
        if self.config["suggestions_today"] >= self.config["max_suggestions_per_day"]:
            self.log.debug(f"Suggestion limit reached for today")
            return
        
        # Check if already suggested recently
        if suggestion_id in self.last_suggestions:
            return
        
        # Create suggestion entry
        suggestion = {
            "id": suggestion_id,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "message": message,
            "priority": priority,
            "status": "new"
        }
        
        # Save to suggestions file
        suggestions_dir = WORKSPACE / "suggestions"
        suggestions_dir.mkdir(exist_ok=True)
        
        suggestions = []
        suggestions_file = suggestions_dir / "improvements.json"
        if suggestions_file.exists():
            try:
                with open(suggestions_file) as f:
                    suggestions = json.load(f)
            except Exception as e:
                self.log.error(f"Error reading suggestions: {e}")
        
        # Add new suggestion
        suggestions.append(suggestion)
        
        try:
            with open(suggestions_file, 'w') as f:
                json.dump(suggestions[-50:], f, indent=2)  # Keep last 50
        except Exception as e:
            self.log.error(f"Error saving suggestion: {e}")
            return
        
        # Update state
        self.config["suggestions_today"] += 1
        self.last_suggestions.add(suggestion_id)
        self.save_config()
        
        # Log
        self.log.info(f"Suggestion [{priority}]: {message}")
        
        # Mint entropy for useful suggestion
        if priority in ["high", "medium"]:
            self.mint_suggestion_entropy(suggestion_id, message)
    
    def mint_suggestion_entropy(self, suggestion_id: str, message: str):
        """Mint entropy for valuable suggestion"""
        try:
            payload = {
                "source": "proactive_supervisor",
                "event": "improvement_suggestion",
                "suggestion_id": suggestion_id,
                "message": message[:100],  # Truncate
                "timestamp": datetime.now(timezone.utc).isoformat()
            }
            resp = requests.post(
                f"{ENTROPY_URL}/mint/security",
                json=payload,
                timeout=10
            )
            if resp.status_code == 200:
                self.log.debug(f"Minted entropy for suggestion {suggestion_id}")
            else:
                self.log.debug(f"Failed to mint entropy: {resp.status_code}")
        except Exception as e:
            self.log.error(f"Error minting suggestion entropy: {e}")
    
    def cleanup_old_suggestions(self):
        """Remove suggestions older than 7 days"""
        suggestions_file = WORKSPACE / "suggestions" / "improvements.json"
        if not suggestions_file.exists():
            return
        
        try:
            with open(suggestions_file) as f:
                suggestions = json.load(f)
            
            week_ago = datetime.now(timezone.utc) - timedelta(days=7)
            filtered = [
                s for s in suggestions
                if datetime.fromisoformat(s["timestamp"].replace('Z', '+00:00')) > week_ago
            ]
            
            if len(filtered) < len(suggestions):
                with open(suggestions_file, 'w') as f:
                    json.dump(filtered, f, indent=2)
                self.log.debug(f"Cleaned up {len(suggestions) - len(filtered)} old suggestions")
        except Exception as e:
            self.log.error(f"Error cleaning suggestions: {e}")
    
    def run(self):
        """Main daemon loop"""
        self.log.info("Starting supervision loop")
        try:
            while True:
                self.log.debug("Running supervision checks")
                
                if self.config["monitor_cron"]:
                    self.check_cron_jobs()
                
                if self.config["monitor_agents"]:
                    self.check_agent_health()
                
                if self.config["monitor_token_burn"]:
                    self.check_token_usage()
                
                self.check_disk_usage()
                self.check_memory_usage()
                self.check_entropy_economy()
                self.cleanup_old_suggestions()
                
                time.sleep(CHECK_INTERVAL)
        except KeyboardInterrupt:
            self.log.info("Shutting down gracefully")
        except Exception as e:
            self.log.error(f"Unexpected error: {e}", exc_info=True)
            sys.exit(1)

if __name__ == "__main__":
    daemon = ProactiveSupervisorDaemon()
    daemon.run()