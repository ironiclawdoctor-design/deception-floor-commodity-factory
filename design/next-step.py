#!/usr/bin/env python3
"""
Intent Cache Prototype - Simple SQLite-based caching system
"""

import sqlite3
import json
import datetime
import logging
import os

# Configure logging
logging.basicConfig(
    filename='design/cache-prototype.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class IntentCache:
    def __init__(self, db_path='intent_cache.db'):
        self.db_path = db_path
        self.init_db()
    
    def init_db(self):
        """Initialize the database schema"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create table for caching intents
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS intent_cache (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                intent_hash TEXT NOT NULL,
                query TEXT NOT NULL,
                response TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                expires_at TEXT
            )
        ''')
        
        # Create index for faster lookups
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_intent_hash ON intent_cache (intent_hash)')
        
        conn.commit()
        conn.close()
        logging.info("Database initialized")
    
    def hash_intent(self, intent):
        """Generate a simple hash for the intent"""
        # In a real implementation, this would be a proper hash function
        return hash(str(intent)).hex()[:16]
    
    def store_intent(self, intent, query, response):
        """Store an intent/query/response in the cache"""
        intent_hash = self.hash_intent(intent)
        timestamp = datetime.datetime.now().isoformat()
        expires_at = (datetime.datetime.now() + datetime.timedelta(days=7)).isoformat()
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO intent_cache (intent_hash, query, response, timestamp, expires_at)
            VALUES (?, ?, ?, ?, ?)
        ''', (intent_hash, query, json.dumps(response), timestamp, expires_at))
        
        conn.commit()
        conn.close()
        logging.info(f"Stored intent: {intent_hash[:8]}...")
    
    def get_cached_response(self, intent):
        """Retrieve a cached response for an intent, if available and not expired"""
        intent_hash = self.hash_intent(intent)
        now = datetime.datetime.now().isoformat()
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT query, response, timestamp FROM intent_cache
            WHERE intent_hash = ? AND datetime(timestamp) < datetime(expires_at)
            ORDER BY timestamp DESC LIMIT 1
        ''', (intent_hash,))
        
        result = cursor.fetchone()
        conn.close()
        
        if result:
            query, response, timestamp = result
            logging.info(f"Cache hit for intent: {intent_hash[:8]}...")
            return json.loads(response), timestamp
        else:
            logging.info(f"No cache hit for intent: {intent_hash[:8]}...")
            return None, None

def demo_cache():
    """Demonstrate basic cache functionality"""
    cache = IntentCache()
    
    print("=== Intent Cache Prototype Demo ===")
    
    # Sample intent
    sample_intent = "show me a summary of the current financial ledger"
    sample_query = "What are the total expenses this month?"
    sample_response = {
        "summary": "Total expenses this month are $1,234.56",
        "breakdown": {
            "personnel": "$500",
            "supplies": "$200",
            "operations": "$534.56"
        }
    }
    
    print(f"1. Storing intent: '{sample_intent}'")
    cache.store_intent(sample_intent, sample_query, sample_response)
    
    print("\n2. Retrieving cached response:")
    cached, timestamp = cache.get_cached_response(sample_intent)
    if cached:
        print(f"   Cached response: {cached}")
        print(f"   Cached at: {timestamp}")
    else:
        print("   No cached response found")
    
    print("\n=== Cache Demo Complete ===")

if __name__ == "__main__":
    demo_cache()