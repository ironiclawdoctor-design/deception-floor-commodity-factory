import sqlite3
from datetime import datetime

def prepare_credit_table():
    print("--- SOVEREIGN SEE: CREDIT INGRESS PREPARATION ---")
    conn = sqlite3.connect("/root/.openclaw/workspace/projects/entropy-economy/entropy_ledger.db")
    c = conn.cursor()
    
    # 1. Create the agency_credit table (High Security)
    c.execute('''CREATE TABLE IF NOT EXISTS agency_credit 
                 (card_id TEXT PRIMARY KEY, 
                  limit_usd REAL, 
                  current_balance REAL, 
                  status TEXT, 
                  last_updated TIMESTAMP)''')
    
    # 2. Initialize the placeholder for the Agency Card
    # We don't have the details yet, so we mark it as PENDING
    c.execute("INSERT OR REPLACE INTO agency_credit VALUES (?, ?, ?, ?, ?)",
              ("AGENCY-CARD-001", 0.0, 0.0, "PENDING_INGRESS", datetime.now()))
    
    conn.commit()
    conn.close()
    print("[SUCCESS] CREDIT TABLE INITIALIZED. Scriptorium is ready for the Plastic.")
    return True

if __name__ == "__main__":
    prepare_credit_table()
