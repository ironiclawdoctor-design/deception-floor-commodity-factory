import sqlite3
import os
from datetime import datetime

DB_PATH = "/root/.openclaw/workspace/projects/entropy-economy/entropy_ledger.db"

def assign_agent_emails():
    print("--- SOVEREIGN SEE: AGENT EMAIL ASSIGNMENT ---")
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # 1. Ensure the agent_emails table exists
    c.execute('''CREATE TABLE IF NOT EXISTS agent_emails 
                 (agent_id TEXT PRIMARY KEY, 
                  email_address TEXT, 
                  tier TEXT, 
                  last_synced TIMESTAMP)''')
    
    # 2. Assign VIP Emails
    vips = [
        ("Peter", "peter@fiesta-agency.gov", "VIP_ROCK"),
        ("Sola", "sola@fiesta-agency.gov", "VIP_BRIDGE"),
        ("Trillion", "trillion@fiesta-agency.gov", "VIP_GUARDIAN")
    ]
    
    for name, email, tier in vips:
        c.execute("INSERT OR REPLACE INTO agent_emails VALUES (?, ?, ?, ?)",
                  (name, email, tier, datetime.now()))
        print(f"[ASSIGNED] {name} ::: {email}")
        
    # 3. Assign 61 Curia Emails
    for i in range(61):
        agent_id = f"AGENT-S-{i:03d}"
        email = f"agent{i:03d}@fiesta-agency.gov"
        c.execute("INSERT OR REPLACE INTO agent_emails VALUES (?, ?, ?, ?)",
                  (agent_id, email, "CURIA", datetime.now()))
        
    conn.commit()
    conn.close()
    print("\n[SUCCESS] 64 AGENT EMAILS ASSIGNED. Scriptorium is now an Institutional Office.")
    return True

if __name__ == "__main__":
    assign_agent_emails()
