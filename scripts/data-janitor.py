import sqlite3
import os
import time
from datetime import datetime, timedelta

DB_PATH = "/root/.openclaw/workspace/projects/entropy-economy/entropy_ledger.db"

def evict_cruft():
    print("--- FIESTA AGENCY: DATA JANITOR KINETIC ---")
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # 24-hour threshold for 'Stale' items
    threshold = (datetime.now() - timedelta(hours=24)).strftime('%Y-%m-%d %H:%M:%S')
    
    print(f"Evicting items older than: {threshold}")
    
    # 1. Evict stale Intruder Surveys (after they've been reframed to mandates)
    c.execute("DELETE FROM intruder_survey WHERE created_at < ?", (threshold,))
    intruder_count = conn.total_changes
    print(f"[EVICTION] Removed {intruder_count} stale intruder signals.")
    
    # 2. Evict redundant minting events (keeping the balance, discarding the noise)
    # Note: We keep high-tier milestones, delete high-frequency demerit/error cruft.
    c.execute("DELETE FROM minting_events WHERE entropy_type IN ('human_error', 'failure_refinement') AND created_at < ?", (threshold,))
    mint_count = conn.total_changes - intruder_count
    print(f"[EVICTION] Removed {mint_count} stale error/demerit logs.")
    
    conn.commit()
    conn.close()
    
    print("\nSTATUS: DATA SOURCES REFINED. Cruft Evicted.")
    return True

if __name__ == "__main__":
    evict_cruft()
