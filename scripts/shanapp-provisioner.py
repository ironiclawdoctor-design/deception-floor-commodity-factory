import sqlite3
import datetime

DB_PATH = "/root/.openclaw/workspace/projects/entropy-economy/entropy_ledger.db"

def provision_accounts():
    print("--- SHANAPP: ACCOUNT PROVISIONING ---")
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # Ensure accounts table exists
    c.execute('''CREATE TABLE IF NOT EXISTS shanapp_accounts 
                 (handle TEXT PRIMARY KEY, balance REAL, role TEXT)''')
    
    # Ingest Current Realized Mass
    c.execute("SELECT SUM(amount) FROM credits")
    nate_mass = c.fetchone()[0] or 0
    
    # Reserve Sovereign Accounts
    accounts = [
        ("𓂺Nate", nate_mass, "SOVEREIGN HUMAN"),
        ("𓂺Fern", 93.0, "DESIGN SPEC AI (CASHAPP-ORIGIN)")
    ]
    
    for handle, balance, role in accounts:
        c.execute("INSERT OR REPLACE INTO shanapp_accounts VALUES (?, ?, ?)", (handle, balance, role))
        print(f"[RESERVED] Account: {handle} ::: Balance: {balance:,.2f} SHAN ::: Role: {role}")
        
    conn.commit()
    conn.close()
    print("\n[SUCCESS] ShanApp Accounts Synced with 𓂺-Archetype.")
    return True

if __name__ == "__main__":
    provision_accounts()
