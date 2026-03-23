#!/usr/bin/env python3
"""
raise-awareness daemon - Monitors system events and logs security anomalies.
Integrates with Entropy economy for minting security entropy.
"""

import os
import sys
import time
import json
import logging
import subprocess
import sqlite3
import requests
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any, Optional

# Configuration
WORKSPACE = Path("/root/.openclaw/workspace")
LOG_DIR = WORKSPACE / "logs"
DAEMON_LOG = LOG_DIR / "raise-awareness.log"
CONFIG_FILE = WORKSPACE / "daemons" / "raise-awareness-config.json"
ENTROPY_URL = "http://127.0.0.1:9001"
FACTORY_URL = "http://127.0.0.1:9000"
CHECK_INTERVAL = 60  # seconds

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

class RaiseAwarenessDaemon:
    def __init__(self):
        self.log = setup_logging()
        self.config = self.load_config()
        self.last_checks = {}
        self.log.info("Raise Awareness daemon starting")
        
    def load_config(self) -> Dict[str, Any]:
        default = {
            "monitor_paths": [
                str(WORKSPACE / "memory"),
                str(WORKSPACE / "logs"),
                str(WORKSPACE / "scripts")
            ],
            "alert_on_new_files": True,
            "alert_on_file_changes": True,
            "entropy_mint_threshold": 5,  # number of anomalies to mint entropy
            "anomaly_count": 0
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
    
    def check_system_health(self):
        """Check core services are running"""
        services = [
            ("Factory", f"{FACTORY_URL}/health"),
            ("Entropy", f"{ENTROPY_URL}/health"),
            ("Gateway", "http://127.0.0.1:18789/health")  # Assuming gateway health endpoint
        ]
        
        for name, url in services:
            try:
                resp = requests.get(url, timeout=5)
                if resp.status_code == 200:
                    self.log.debug(f"{name} OK")
                else:
                    self.log.warning(f"{name} returned {resp.status_code}")
                    self.record_anomaly(f"service_{name.lower()}_unhealthy", {"status_code": resp.status_code})
            except Exception as e:
                self.log.warning(f"{name} unreachable: {e}")
                self.record_anomaly(f"service_{name.lower()}_unreachable", {"error": str(e)})
    
    def check_file_integrity(self):
        """Monitor configured paths for unexpected changes"""
        for path_str in self.config["monitor_paths"]:
            path = Path(path_str)
            if not path.exists():
                self.log.warning(f"Monitor path does not exist: {path}")
                continue
            
            # Check for new files (simplistic)
            if self.config["alert_on_new_files"]:
                key = f"file_count_{path}"
                current_count = sum(1 for _ in path.rglob('*') if _.is_file())
                last_count = self.last_checks.get(key)
                
                if last_count is not None and current_count != last_count:
                    if current_count > last_count:
                        self.log.info(f"New files detected in {path}: +{current_count - last_count}")
                        self.record_anomaly("new_files_detected", {
                            "path": str(path),
                            "previous_count": last_count,
                            "current_count": current_count
                        })
                
                self.last_checks[key] = current_count
    
    def check_mutation_detector(self):
        """Verify mutation detector is running"""
        try:
            result = subprocess.run(
                ["pgrep", "-f", "mutation_detector"],
                capture_output=True,
                text=True
            )
            if result.returncode != 0:
                self.log.warning("Mutation detector not running")
                self.record_anomaly("mutation_detector_stopped", {})
        except Exception as e:
            self.log.error(f"Error checking mutation detector: {e}")
    
    def check_token_burn(self):
        """Monitor token burn rate if tracking file exists"""
        token_file = WORKSPACE / ".token-ledger.json"
        if token_file.exists():
            try:
                with open(token_file) as f:
                    data = json.load(f)
                    current_burn = data.get("total_burn", 0)
                    last_burn = self.last_checks.get("token_burn")
                    
                    if last_burn is not None and current_burn > last_burn:
                        burn_delta = current_burn - last_burn
                        self.log.info(f"Token burn increased: +${burn_delta:.2f}")
                        if burn_delta > 10:  # Alert on large burns
                            self.record_anomaly("high_token_burn", {
                                "amount": burn_delta,
                                "total": current_burn
                            })
                    
                    self.last_checks["token_burn"] = current_burn
            except Exception as e:
                self.log.error(f"Error reading token ledger: {e}")
    
    def check_token_budget_events(self):
        """Check for token budget circuit breaker events"""
        db_path = WORKSPACE / "entropy_ledger.db"
        if not db_path.exists():
            return
        
        try:
            conn = sqlite3.connect(str(db_path))
            cursor = conn.cursor()
            cursor.execute("""
                SELECT agent_id, event_type, tokens_used, threshold, timestamp
                FROM circuit_breaker_events
                WHERE resolved_at IS NULL
                ORDER BY timestamp DESC
            """)
            events = cursor.fetchall()
            conn.close()
            
            for agent_id, event_type, tokens_used, threshold, timestamp in events:
                self.log.warning(f"Token budget event: {agent_id} {event_type} - {tokens_used}/{threshold}")
                self.record_anomaly(f"token_budget_{event_type}", {
                    "agent": agent_id,
                    "tokens_used": tokens_used,
                    "threshold": threshold,
                    "timestamp": timestamp
                })
        except Exception as e:
            self.log.error(f"Error checking token budget events: {e}")
    
    def record_anomaly(self, anomaly_type: str, details: Dict[str, Any]):
        """Record an anomaly and mint entropy if threshold reached"""
        self.config["anomaly_count"] += 1
        self.save_config()
        
        self.log.warning(f"Anomaly detected: {anomaly_type} - {details}")
        
        # Log to anomaly log
        anomaly_log = LOG_DIR / "anomalies.log"
        entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "type": anomaly_type,
            "details": details,
            "count": self.config["anomaly_count"]
        }
        try:
            with open(anomaly_log, 'a') as f:
                f.write(json.dumps(entry) + "\n")
        except Exception as e:
            self.log.error(f"Failed to log anomaly: {e}")
        
        # Mint entropy if threshold reached
        if self.config["anomaly_count"] >= self.config["entropy_mint_threshold"]:
            self.mint_security_entropy()
            self.config["anomaly_count"] = 0
            self.save_config()
        
        # Attempt automated remediation for certain anomaly types
        self.attempt_remediation(anomaly_type, details)
    
    def attempt_remediation(self, anomaly_type: str, details: Dict[str, Any]):
        """Attempt automated remediation for detected anomalies"""
        remediation_attempted = False
        remediation_success = False
        
        # Service unreachable remediation
        if anomaly_type.startswith("service_") and anomaly_type.endswith("_unreachable"):
            service_name = anomaly_type.replace("service_", "").replace("_unreachable", "")
            remediation_attempted = True
            
            # Map service names to systemd units
            service_map = {
                "factory": "deception-floor-commodity-factory",
                "entropy": "entropy-daemon",  # assuming systemd unit name
                "gateway": "openclaw-gateway"  # assuming systemd unit name
            }
            
            systemd_service = service_map.get(service_name.lower())
            if systemd_service:
                try:
                    self.log.info(f"Attempting to restart {service_name} via systemd")
                    result = subprocess.run(
                        ["systemctl", "restart", systemd_service],
                        capture_output=True,
                        text=True,
                        timeout=30
                    )
                    
                    if result.returncode == 0:
                        remediation_success = True
                        self.log.info(f"Successfully restarted {service_name}")
                        # Mint entropy for successful remediation
                        self.mint_remediation_entropy(service_name, "restart")
                    else:
                        self.log.warning(f"Failed to restart {service_name}: {result.stderr}")
                except Exception as e:
                    self.log.error(f"Error restarting {service_name}: {e}")
            else:
                self.log.warning(f"No systemd mapping for service: {service_name}")
        
        # Log remediation attempt
        if remediation_attempted:
            remediation_log = LOG_DIR / "remediation.log"
            entry = {
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "anomaly_type": anomaly_type,
                "details": details,
                "remediation_attempted": remediation_attempted,
                "remediation_success": remediation_success,
                "tag": "REMEDIATION"
            }
            try:
                with open(remediation_log, 'a') as f:
                    f.write(json.dumps(entry) + "\n")
            except Exception as e:
                self.log.error(f"Failed to log remediation: {e}")
    
    def mint_remediation_entropy(self, service_name: str, action: str):
        """Mint entropy for successful remediation actions"""
        try:
            payload = {
                "source": "raise_awareness",
                "event": "auto_remediation",
                "service": service_name,
                "action": action,
                "timestamp": datetime.now(timezone.utc).isoformat()
            }
            resp = requests.post(
                f"{ENTROPY_URL}/mint/security",
                json=payload,
                timeout=10
            )
            if resp.status_code == 200:
                self.log.info(f"Minted remediation entropy: {resp.json()}")
            else:
                self.log.warning(f"Failed to mint remediation entropy: {resp.status_code}")
        except Exception as e:
            self.log.error(f"Error minting remediation entropy: {e}")
    
    def mint_security_entropy(self):
        """Mint entropy for security event detection"""
        try:
            payload = {
                "source": "raise_awareness",
                "event": "security_anomalies_detected",
                "count": self.config["anomaly_count"],
                "timestamp": datetime.now(timezone.utc).isoformat()
            }
            resp = requests.post(
                f"{ENTROPY_URL}/mint/security",
                json=payload,
                timeout=10
            )
            if resp.status_code == 200:
                self.log.info(f"Minted security entropy: {resp.json()}")
            else:
                self.log.warning(f"Failed to mint entropy: {resp.status_code}")
        except Exception as e:
            self.log.error(f"Error minting entropy: {e}")
    
    def run(self):
        """Main daemon loop"""
        self.log.info("Starting monitoring loop")
        try:
            while True:
                self.log.debug("Running checks")
                self.check_system_health()
                self.check_file_integrity()
                self.check_mutation_detector()
                self.check_token_burn()
                
                time.sleep(CHECK_INTERVAL)
        except KeyboardInterrupt:
            self.log.info("Shutting down gracefully")
        except Exception as e:
            self.log.error(f"Unexpected error: {e}", exc_info=True)
            sys.exit(1)

if __name__ == "__main__":
    daemon = RaiseAwarenessDaemon()
    daemon.run()
# --- Integrated Mutation Detector (-1 Pivot) ---
def integrated_mutation_check():
    """Simplified mutation check: verify core config and script integrity."""
    critical_files = [
        "/root/.openclaw/openclaw.json",
        "/root/.openclaw/workspace/daemons/raise-awareness.py",
        "/root/.openclaw/workspace/daemons/proactive-supervisor.py"
    ]
    for f in critical_files:
        if not os.path.exists(f):
            logging.error(f"INTEGRITY ALERT: Critical file missing: {f}")
