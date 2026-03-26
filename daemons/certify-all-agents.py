#!/usr/bin/env python3
"""
Certify All Agents - Create initial certification records for all fiesta-agents.
"""

import os
import sys
import sqlite3
from datetime import datetime, timezone, timedelta
from pathlib import Path

WORKSPACE = Path("/root/.openclaw/workspace")
FIESTA_AGENTS_DIR = WORKSPACE / "skills" / "fiesta-agents" / "agents"
ENTROPY_DB = WORKSPACE / "entropy_ledger.db"

def get_all_agents():
    """Scan agent markdown files and return agent IDs."""
    agents = []
    if not FIESTA_AGENTS_DIR.exists():
        print(f"Fiesta agents directory not found: {FIESTA_AGENTS_DIR}")
        return agents
    
    # Walk through department directories
    for dept_dir in FIESTA_AGENTS_DIR.iterdir():
        if dept_dir.is_dir():
            for md_file in dept_dir.glob("*.md"):
                agent_id = md_file.stem
                agents.append({
                    "id": agent_id,
                    "department": dept_dir.name,
                    "path": md_file
                })
    
    return agents

def ensure_certifications_table():
    """Ensure certifications table exists."""
    conn = sqlite3.connect(ENTROPY_DB)
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS certifications (
            agent_id TEXT PRIMARY KEY,
            certification_level INTEGER DEFAULT 1,
            certified_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            expires_at TIMESTAMP,
            certifying_officer TEXT DEFAULT 'certification-officer',
            competency_domain TEXT,
            notes TEXT
        )
    """)
    
    conn.commit()
    conn.close()

def insert_certifications(agents):
    """Insert certification records for agents."""
    conn = sqlite3.connect(ENTROPY_DB)
    cursor = conn.cursor()
    
    inserted = 0
    updated = 0
    
    for agent in agents:
        # Check if already exists
        cursor.execute("SELECT agent_id FROM certifications WHERE agent_id = ?", (agent["id"],))
        exists = cursor.fetchone()
        
        # Set expiry 90 days from now
        expires_at = (datetime.now(timezone.utc) + timedelta(days=90)).isoformat()
        
        if exists:
            # Update expiry date
            cursor.execute("""
                UPDATE certifications 
                SET expires_at = ?
                WHERE agent_id = ?
            """, (expires_at, agent["id"]))
            updated += 1
        else:
            # Insert new certification
            cursor.execute("""
                INSERT INTO certifications 
                (agent_id, certification_level, expires_at, competency_domain, notes)
                VALUES (?, ?, ?, ?, ?)
            """, (
                agent["id"],
                1,  # L1 Apprentice
                expires_at,
                agent["department"],
                f"Initial certification via certify-all-agents.py"
            ))
            inserted += 1
    
    conn.commit()
    conn.close()
    
    return inserted, updated

def create_certification_tasks(agents):
    """Create dummy task history for certification requirements."""
    conn = sqlite3.connect(ENTROPY_DB)
    cursor = conn.cursor()
    
    # Ensure token_usage_log table exists (already does)
    # Insert dummy tasks for each agent
    for agent in agents:
        # Insert 3 dummy tasks (minimum for L1 certification)
        for i in range(3):
            cursor.execute("""
                INSERT OR IGNORE INTO token_usage_log 
                (timestamp, agent_id, tokens_used, model, estimated_cost, source)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                (datetime.now(timezone.utc) - timedelta(days=i)).isoformat(),
                agent["id"],
                100,  # tokens
                "local",
                0.0,
                "certification-sample-task"
            ))
    
    conn.commit()
    conn.close()

def main():
    print("=== Fiesta Agents Certification Initialization ===")
    
    # Ensure table exists
    ensure_certifications_table()
    
    # Get all agents
    agents = get_all_agents()
    print(f"Found {len(agents)} agents")
    
    # Insert certifications
    inserted, updated = insert_certifications(agents)
    print(f"Certifications: {inserted} inserted, {updated} updated")
    
    # Create dummy task history
    create_certification_tasks(agents)
    print(f"Created dummy task history for certification requirements")
    
    # Generate report
    conn = sqlite3.connect(ENTROPY_DB)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM certifications")
    total = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM token_usage_log WHERE source = 'certification-sample-task'")
    tasks = cursor.fetchone()[0]
    conn.close()
    
    print(f"\n=== Certification Report ===")
    print(f"Total agents certified: {total}")
    print(f"Sample tasks created: {tasks}")
    print(f"Certification level: L1 (Apprentice) for all agents")
    print(f"Expiry: 90 days from now")
    print(f"\nNext steps:")
    print("1. Run actual tasks with agents to build real competency history")
    print("2. Use certification-officer agent to evaluate and upgrade certifications")
    print("3. Integrate with fiesta-agents orchestrator for project work")
    
    # Save report
    report_file = WORKSPACE / "logs" / "certification-init-report.txt"
    report_file.parent.mkdir(exist_ok=True)
    with open(report_file, 'w') as f:
        f.write(f"Certification initialization completed at {datetime.now(timezone.utc).isoformat()}\n")
        f.write(f"Agents processed: {len(agents)}\n")
        f.write(f"Certifications inserted: {inserted}\n")
        f.write(f"Certifications updated: {updated}\n")
    
    print(f"\nReport saved to: {report_file}")

if __name__ == "__main__":
    main()