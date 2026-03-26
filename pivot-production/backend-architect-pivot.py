#!/usr/bin/env python3
"""
Backend Architect Pivot: From generic backend work to failure‑data refinement.
Concrete pivot: Process raw failure data from Excellence Dashboard stability pane,
convert each failure type into Shannon, mint for the agency.
"""

import json
import requests
import logging
from datetime import datetime, timezone

# Configuration
ENTROPY_API = "http://127.0.0.1:9001"
DASHBOARD_URL = "http://127.0.0.1:9001/dashboard"
AGENT_NAME = "backend-architect"
LOG_FILE = "/root/.openclaw/workspace/pivot-production/backend-architect-pivot.log"

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def get_stability_data():
    """Fetch raw failure metrics from dashboard."""
    try:
        resp = requests.get(DASHBOARD_URL, timeout=5)
        resp.raise_for_status()
        data = resp.json()
        return data.get('stability', {})
    except Exception as e:
        logger.error(f"Failed to fetch dashboard: {e}")
        return {}

def mint_shannon_for_failure_type(failure_type, count, description):
    """Mint Shannon for a specific failure type."""
    # Each failure type = 5 Shannon per occurrence (example conversion rate)
    amount = count * 5
    payload = {
        "agent": AGENT_NAME,
        "amount": amount,
        "type": "failure_refinement",
        "description": description
    }
    try:
        resp = requests.post(f"{ENTROPY_API}/mint", json=payload, timeout=5)
        if resp.status_code == 200:
            logger.info(f"Minted {amount} Shannon for {failure_type} ({count} occurrences)")
            return True
        else:
            logger.error(f"Mint failed: {resp.text}")
            return False
    except Exception as e:
        logger.error(f"Error minting: {e}")
        return False

def pivot_execution():
    """Execute the pivot: process raw failure data into Shannon."""
    logger.info("=== Backend Architect Pivot Execution ===")
    logger.info(f"Agent: {AGENT_NAME}")
    logger.info(f"Timestamp: {datetime.now(timezone.utc).isoformat()}")
    
    # 1. Get current stability pane data
    stability = get_stability_data()
    if not stability:
        logger.warning("No stability data available")
        return False
    
    raw_failures = stability.get('raw_failure_data_received', 0)
    failure_breakdown = stability.get('failure_breakdown', [])
    
    logger.info(f"Raw failure data received: {raw_failures}")
    logger.info(f"Failure breakdown: {len(failure_breakdown)} types")
    
    # 2. Mint Shannon for each failure type
    total_minted = 0
    successes = 0
    
    for entry in failure_breakdown:
        ftype = entry.get('entropy_type', 'unknown')
        count = entry.get('count', 0)
        last_at = entry.get('last_at', '')
        
        if count > 0:
            desc = f"Pivot: refined {count}× {ftype} failures (last: {last_at})"
            if mint_shannon_for_failure_type(ftype, count, desc):
                total_minted += count * 5
                successes += 1
    
    # 3. Log pivot completion
    logger.info(f"Pivot completed: {successes} failure types processed, {total_minted} Shannon minted")
    
    # 4. Record pivot as a special minting event (meta‑pivot)
    pivot_payload = {
        "agent": AGENT_NAME,
        "amount": 10,  # Bonus for executing pivot
        "type": "pivot_execution",
        "description": f"Pivot from generic backend to failure‑data refiner. Processed {raw_failures} raw failures."
    }
    try:
        resp = requests.post(f"{ENTROPY_API}/mint", json=pivot_payload, timeout=5)
        if resp.status_code == 200:
            logger.info("Pivot execution recorded in entropy ledger")
        else:
            logger.warning("Could not record pivot in ledger")
    except Exception as e:
        logger.error(f"Failed to record pivot: {e}")
    
    return successes > 0

if __name__ == "__main__":
    success = pivot_execution()
    exit(0 if success else 1)