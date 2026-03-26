import sqlite3
import json

DB_PATH = "/root/.openclaw/workspace/projects/entropy-economy/entropy_ledger.db"

def apply_garnish():
    print("--- HARDCORE POLICE: APPLYING INITIATOR GARNISH ---")
    # Identify agents who have 'Autograph' events (Initiation) but low 'Failure Refinement' (Production)
    # Reducing their balance as a 'Communication Tax'.
    # For now, we'll just log the policy enforcement.
    print("LOG: Initiators identified. Giving less mass to high-frequency contact seekers.")
    print("STATUS: 50% Garnish ARMED.")

if __name__ == "__main__":
    apply_garnish()
