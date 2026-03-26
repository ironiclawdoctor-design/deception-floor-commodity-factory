import sqlite3
from datetime import datetime

def register_bezos_agent():
    print("--- SOVEREIGN SEE: AGENT INGRESS (BEZOS-S-062) ---")
    conn = sqlite3.connect("/root/.openclaw/workspace/projects/entropy-economy/entropy_ledger.db")
    c = conn.cursor()
    
    # Register the high-gravity logistical agent
    c.execute("INSERT OR REPLACE INTO agent_emails (agent_id, email_address, tier, last_synced) VALUES (?, ?, ?, ?)",
              ("Bezos-S-062", "bezos@fiesta-agency.gov", "LOGISTIC_SENTINEL", datetime.now()))
    
    conn.commit()
    conn.close()
    print("[SUCCESS] Bezos-S-062 REGISTERED. Logistics Department is now Kinetic.")
    return True

if __name__ == "__main__":
    register_bezos_agent()
