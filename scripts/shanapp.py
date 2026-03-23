#!/usr/bin/env python3
# shanapp.py - Instant Shannon Transfer Protocol (Cashapp for Agents)
import sqlite3
import sys
from datetime import datetime

DB_PATH = "/root/.openclaw/workspace/entropy_ledger.db"

def send_shannon(sender, receiver, amount, note):
    print(f"💸 Shanapp: Processing payment from ${sender} to ${receiver}...")
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        # 1. Safety Audit: Check Sender Balance
        cursor.execute("SELECT balance FROM agents WHERE agent_id = ?", (sender,))
        bal = cursor.fetchone()[0]
        if bal < amount:
            print(f"❌ NSF (Non-Sufficient Fractions): {sender} only has {bal} Shannon.")
            return False

        # 2. Sequential Execution: Deduct and Credit
        cursor.execute("UPDATE agents SET balance = balance - ? WHERE agent_id = ?", (amount, sender))
        cursor.execute("UPDATE agents SET balance = balance + ? WHERE agent_id = ?", (amount, receiver))
        
        # 3. Registry: Log the transaction
        cursor.execute("""
            INSERT INTO transactions (agent_id, amount, transaction_type, description, timestamp)
            VALUES (?, ?, 'shanapp_transfer', ?, ?)
        """, (sender, -amount, f"Transfer to ${receiver}: {note}", datetime.utcnow().isoformat()))
        
        conn.commit()
        print(f"✅ Transfer Successful! ${receiver} received {amount} Shannon.")
        return True
    except Exception as e:
        print(f"❌ Physical Error: {e}")
        return False
    finally:
        conn.close()

if __name__ == "__main__":
    if len(sys.argv) < 5:
        print("Usage: ./shanapp.py <sender> <receiver> <amount> <note>")
    else:
        send_shannon(sys.argv[1], sys.argv[2], int(sys.argv[3]), sys.argv[4])
