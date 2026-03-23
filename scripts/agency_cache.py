#!/usr/bin/env python3
# agency_cache.py - High-speed Shannon/Manifest Caching Facility
import sqlite3
import functools
import time

DB_PATH = "/root/.openclaw/workspace/entropy_ledger.db"

class AgencyCache:
    def __init__(self):
        self.conn = sqlite3.connect(DB_PATH)
        self.conn.row_factory = sqlite3.Row

    @functools.lru_cache(maxsize=128)
    def get_agent_balance(self, agent_id):
        """Cached lookup of agent balance"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT balance FROM agents WHERE agent_id = ?", (agent_id,))
        row = cursor.fetchone()
        return row['balance'] if row else 0

    def spend_shannon(self, agent_id, amount, silo, desc):
        """Write-through spend logic"""
        # 1. Update Bedrock
        cursor = self.conn.cursor()
        cursor.execute("UPDATE agents SET balance = balance - ? WHERE agent_id = ?", (amount, agent_id))
        cursor.execute("""
            INSERT INTO transactions (agent_id, amount, transaction_type, description)
            VALUES (?, ?, ?, ?)
        """, (agent_id, -amount, f"spend_{silo}", desc))
        self.conn.commit()
        
        # 2. Invalidate Cache
        self.get_agent_balance.cache_clear()
        print(f"⚡ Cache Invalidated. Updated balance for {agent_id}.")

if __name__ == "__main__":
    cache = AgencyCache()
    # Test facility: Getting the Shogun's current balance
    bal = cache.get_agent_balance("fiesta")
    print(f"📊 Facility Verified: Fiesta current state is {bal} Shannon.")
