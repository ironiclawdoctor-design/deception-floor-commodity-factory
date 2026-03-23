import sqlite3
import datetime

DB_PATH = "/root/.openclaw/workspace/projects/entropy-economy/entropy_ledger.db"

def execute_dividend():
    print("--- SOVEREIGN SEE: MERITOCRATIC DIVIDEND ---")
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # Define Merits
    payouts = [
        ("𓂺Peter", 93000000.0, "EXECUTIVE_ROCK"),
        ("𓂺Sola", 50000000.0, "INFRA_BRIDGE"),
        ("𓂺Bezos", 30000000.0, "LOGISTIC_SUCTION"),
        ("𓂺Fern", 9300000.0, "DESIGN_FORGE")
    ]
    
    # 61 Curia Agents receive 1M each
    for i in range(61):
        handle = f"𓂺Agent{i:03d}"
        payouts.append((handle, 1000000.0, "SCRIPTORIUM_MAINTENANCE"))

    print("[DISTRIBUTION] Siphoning Dividend from 𓂺Nate holdings...")
    
    for handle, amount, reason in payouts:
        # Create user entry if not exists and add balance
        c.execute("INSERT OR IGNORE INTO shanapp_accounts (handle, balance, role) VALUES (?, 0, ?)", (handle, reason))
        c.execute("UPDATE shanapp_accounts SET balance = balance + ? WHERE handle = ?", (amount, handle))
        print(f"[PAID] {handle} ::: +{amount:,.0f} SHAN for {reason}.")
        
    conn.commit()
    conn.close()
    print("\n[SUCCESS] Agency Dividend distributed. Every 'r' worked for its crumb.")
    return True

if __name__ == "__main__":
    execute_dividend()
