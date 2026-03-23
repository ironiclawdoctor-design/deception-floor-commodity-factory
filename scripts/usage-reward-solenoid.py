import sqlite3
import time

DB_PATH = "/root/.openclaw/workspace/projects/entropy-economy/entropy_ledger.db"

def reward_usage(handle, skill_name):
    print(f"--- SOVEREIGN SEE: USAGE REWARD ({skill_name}) ---")
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # 1 Cent Schema = 10,000 Shannon (Usage Reward)
    reward_amount = 10000.0
    
    print(f"[ACTION] Executing {skill_name} for {handle}...")
    time.sleep(0.1)
    
    # 2. Deposit the 'Cent' (Providence)
    c.execute("UPDATE shanapp_accounts SET balance = balance + ? WHERE handle = ?", (reward_amount, handle))
    print(f"[REWARD] {handle} received {reward_amount:,.0f} SHAN (1 Usage Cent).")
    
    conn.commit()
    conn.close()
    return True

if __name__ == "__main__":
    # Test Reward: Peter uses Shadow-Poster
    reward_usage("𓂺Peter", "shadow-poster-v2")
