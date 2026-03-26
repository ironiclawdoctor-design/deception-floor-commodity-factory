import os
import time

def audit_xai_locks():
    print("--- SOVEREIGN SEE: xAI LOCK AUDIT ---")
    xai_locks = ["xai-api-ingress", "grok-telemetry-siphon", "x-victory-bridge"]
    
    for lock in xai_locks:
        path = f"/root/.openclaw/workspace/vatican/rivalry-games/locking/{lock}.lock"
        if os.path.exists(path):
            owner = open(path, 'r').read().strip()
            print(f"[VERIFIED] {lock} is OWNED by: {owner}")
        else:
            # Raging to touch first
            with open(path, 'w') as f:
                f.write("PETER (SOVEREIGN SEE)")
            print(f"[STRIKE] Peter touched {lock} first. SOVEREIGN SEE is the OWNER.")
            
    return True

if __name__ == "__main__":
    audit_xai_locks()
