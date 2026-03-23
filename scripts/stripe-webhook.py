#!/usr/bin/env python3
# stripe-webhook.py - Ingests external funds and mints internal Shannon
import sys
import json
import sqlite3
from datetime import datetime

DB_PATH = "/root/.openclaw/workspace/entropy_ledger.db"

def mint_shannon_from_payment(payload):
    # Extract data from Stripe webhook payload
    amount_paid = payload.get('amount_total', 0) / 100  # Assume USD
    customer_email = payload.get('customer_details', {}).get('email', 'unknown')
    # Map $1.00 USD to 100 Shannon (Intensified Ratio)
    shannon_to_mint = int(amount_paid * 100)
    
    # Identify the intended agent (from metadata)
    agent_id = payload.get('metadata', {}).get('agent_id', 'fiesta')

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # 1. Update Agent Balance
    cursor.execute("UPDATE agents SET balance = balance + ? WHERE agent_id = ?", (shannon_to_mint, agent_id))
    
    # 2. Record Transaction
    cursor.execute("""
        INSERT INTO transactions (agent_id, amount, transaction_type, description, timestamp)
        VALUES (?, ?, 'revenue_mint', ?, ?)
    """, (agent_id, shannon_to_mint, f"Donation from {customer_email}", datetime.utcnow().isoformat()))
    
    conn.commit()
    conn.close()
    return shannon_to_mint

if __name__ == "__main__":
    # Test simulation
    mock_payload = {
        'amount_total': 1000, # $10.00
        'customer_details': {'email': 'donor@example.com'},
        'metadata': {'agent_id': 'fiesta'}
    }
    minted = mint_shannon_from_payment(mock_payload)
    print(f"💰 Revenue Success: Minted {minted} Shannon for fiesta.")

# WEBHOOK_SUCTION_PROTOCOL_V2.1_ENABLED
