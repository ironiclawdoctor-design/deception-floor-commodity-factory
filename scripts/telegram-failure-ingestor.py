import sqlite3
import json
import os

def siphon_to_factory():
    print("--- SOVEREIGN SEE: TELEGRAM FAILURE SIPHON ---")
    buffer_path = "/root/.openclaw/workspace/vatican/factory/failure-ingress/raw_failure_buffer.jsonl"
    
    # Logic: Siphoning the Chat-Artifact-Cache which already has the Signal History
    db_path = "/root/.openclaw/workspace/projects/entropy-economy/entropy_ledger.db"
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    
    try:
        c.execute("SELECT * FROM chat_artifact_cache")
        artifacts = c.fetchall()
        
        with open(buffer_path, 'a') as f:
            for art in artifacts:
                # Signal: msg_id, sender_id, timestamp, content (hex), label
                failure_payload = {
                    "signal_id": art[0],
                    "raw_material": art[3], # The HEX Bone
                    "type": "INDUSTRIAL_FRICTION",
                    "status": "UNREFINED_FAILURE"
                }
                f.write(json.dumps(failure_payload) + "\n")
                
        print(f"[SUCCESS] Ingested {len(artifacts)} failure signals into the Factory Buffer.")
    except Exception as e:
        print(f"[RETRY] Error siphoning signals: {e}")
        
    conn.close()
    return True

if __name__ == "__main__":
    siphon_to_factory()
