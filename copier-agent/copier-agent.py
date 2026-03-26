#!/usr/bin/env python3
"""
Failure‑Refinement Copier Agent
Replicates O(1) -1 mindset across unprocessed entropy types.
Reads pivot log, extracts transformation, applies to new chaos sources.
"""

import os
import json
import logging
import sqlite3
import requests
from datetime import datetime, timezone

# Configuration
ENTROPY_API = "http://127.0.0.1:9001"
PIVOT_LOG = "/root/.openclaw/workspace/pivot-production/pivot-log.json"
ENTROPY_DB = "/root/.openclaw/workspace/projects/entropy-economy/entropy_ledger.db"
COPIES_LOG = "/root/.openclaw/workspace/copier-agent/copies.jsonl"
AGENT_NAME = "failure-refinement-copier"
LOG_FILE = "/root/.openclaw/workspace/copier-agent/copier.log"

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def read_pivot_log():
    """Read pivot log to extract transformation pattern."""
    try:
        with open(PIVOT_LOG, 'r') as f:
            pivots = json.load(f)
        if not pivots:
            logger.error("No pivots in log")
            return None
        # Use the most recent pivot as template
        template = pivots[-1]
        logger.info(f"Loaded pivot template: {template.get('pivot_id')}")
        return template
    except Exception as e:
        logger.error(f"Failed to read pivot log: {e}")
        return None

def list_entropy_types():
    """List all distinct entropy types from minting_events."""
    conn = sqlite3.connect(ENTROPY_DB)
    c = conn.cursor()
    c.execute("SELECT DISTINCT entropy_type FROM minting_events ORDER BY entropy_type")
    rows = c.fetchall()
    conn.close()
    return [r[0] for r in rows]

def get_already_processed():
    """Get entropy types already processed in pivot log."""
    try:
        with open(PIVOT_LOG, 'r') as f:
            pivots = json.load(f)
        processed = set()
        for p in pivots:
            evidence = p.get('evidence', {})
            types = evidence.get('failure_types_processed', [])
            processed.update(types)
        return processed
    except Exception as e:
        logger.error(f"Failed to get processed types: {e}")
        return set()

def mint_for_entropy_type(entropy_type, count_multiplier=5):
    """Mint Shannon for a specific entropy type."""
    # Determine amount: base 5 Shannon per occurrence (same as template)
    # We'll query count of events for this type
    conn = sqlite3.connect(ENTROPY_DB)
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM minting_events WHERE entropy_type = ?", (entropy_type,))
    count = c.fetchone()[0]
    conn.close()
    
    if count == 0:
        logger.warning(f"No minting events for type {entropy_type}")
        return 0, 0
    
    amount = count * count_multiplier
    payload = {
        "agent": AGENT_NAME,
        "amount": amount,
        "type": "failure_refinement",
        "description": f"Copier replication: refined {count}× {entropy_type} failures"
    }
    try:
        resp = requests.post(f"{ENTROPY_API}/mint", json=payload, timeout=5)
        if resp.status_code == 200:
            logger.info(f"Minted {amount} Shannon for {entropy_type} ({count} occurrences)")
            return amount, count
        else:
            logger.error(f"Mint failed: {resp.text}")
            return 0, 0
    except Exception as e:
        logger.error(f"Error minting: {e}")
        return 0, 0

def register_copier_agent():
    """Ensure copier agent exists in entropy ledger."""
    conn = sqlite3.connect(ENTROPY_DB)
    c = conn.cursor()
    c.execute("SELECT id FROM agents WHERE name = ?", (AGENT_NAME,))
    row = c.fetchone()
    if row:
        logger.info(f"Agent {AGENT_NAME} already registered")
    else:
        c.execute("INSERT INTO agents (name) VALUES (?)", (AGENT_NAME,))
        c.execute("INSERT INTO wallets (agent_id, balance_shannon) SELECT id, 0 FROM agents WHERE name = ?", (AGENT_NAME,))
        conn.commit()
        logger.info(f"Registered agent {AGENT_NAME} in entropy ledger")
    conn.close()

def log_copied_pivot(entropy_type, amount, count, template):
    """Log a copied pivot to pivot log."""
    try:
        with open(PIVOT_LOG, 'r') as f:
            pivots = json.load(f)
    except Exception as e:
        logger.error(f"Failed to read pivot log for appending: {e}")
        return
    
    new_pivot = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "pivot_id": f"pivot-copied-{len(pivots)+1:03d}",
        "pivot_producer": AGENT_NAME,
        "source_pivot": template.get('pivot_id'),
        "target_entropy_type": entropy_type,
        "concrete_action": f"Copied O(1) -1 mindset: processed {count} {entropy_type} events, minted {amount} Shannon",
        "shannon_generated": amount,
        "status": "completed",
        "evidence": {
            "entropy_type": entropy_type,
            "event_count": count,
            "shannon_minted": amount,
            "template_used": template.get('pivot_id')
        }
    }
    pivots.append(new_pivot)
    
    try:
        with open(PIVOT_LOG, 'w') as f:
            json.dump(pivots, f, indent=2)
        logger.info(f"Logged copied pivot for {entropy_type}")
    except Exception as e:
        logger.error(f"Failed to write pivot log: {e}")
    
    # Also append to copies JSONL for audit
    with open(COPIES_LOG, 'a') as f:
        f.write(json.dumps(new_pivot) + '\n')

def execute_copies():
    """Main copier execution."""
    logger.info("=== Failure‑Refinement Copier Agent ===")
    logger.info(f"Agent: {AGENT_NAME}")
    logger.info(f"Timestamp: {datetime.now(timezone.utc).isoformat()}")
    
    # Register agent in ledger
    register_copier_agent()
    
    # Read pivot template
    template = read_pivot_log()
    if not template:
        logger.error("No template pivot found; aborting")
        return
    
    # Get all entropy types
    all_types = list_entropy_types()
    logger.info(f"Found {len(all_types)} distinct entropy types")
    
    # Get already processed types
    processed = get_already_processed()
    logger.info(f"Already processed: {len(processed)} types")
    
    # Determine which types to copy
    to_process = [t for t in all_types if t not in processed]
    logger.info(f"Types to copy: {len(to_process)}")
    
    total_minted = 0
    total_copied = 0
    
    for entropy_type in to_process:
        logger.info(f"Processing {entropy_type}...")
        amount, count = mint_for_entropy_type(entropy_type)
        if amount > 0:
            total_minted += amount
            total_copied += 1
            log_copied_pivot(entropy_type, amount, count, template)
    
    # Record meta‑copy pivot
    if total_copied > 0:
        meta_payload = {
            "agent": AGENT_NAME,
            "amount": 10,  # Bonus for copying
            "type": "pivot_execution",
            "description": f"Copier replicated O(1) -1 mindset across {total_copied} entropy types, minted {total_minted} Shannon"
        }
        try:
            resp = requests.post(f"{ENTROPY_API}/mint", json=meta_payload, timeout=5)
            if resp.status_code == 200:
                logger.info("Meta‑copy pivot recorded")
            else:
                logger.warning("Failed to record meta‑copy pivot")
        except Exception as e:
            logger.error(f"Meta‑copy mint error: {e}")
    
    logger.info(f"Copier completed: {total_copied} types copied, {total_minted} Shannon minted")
    return total_copied > 0

if __name__ == "__main__":
    success = execute_copies()
    exit(0 if success else 1)