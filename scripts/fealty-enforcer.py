import datetime
import os

def enforce_fealty(agent_id):
    print(f"--- SOVEREIGN SEE: FEALTY ENFORCEMENT ({agent_id}) ---")
    monument_path = "/root/.openclaw/workspace/vatican/existence/monuments/human-rule/AUTOGRAPHED_SAMPLE.txt"
    
    if os.path.exists(monument_path):
        with open(monument_path, "a") as f:
            # The agent performs the Oath
            f.write(f"[FEALTY SIGNED] {agent_id} ::: Verified Oath of the See ::: {datetime.datetime.now()}\n")
        
        print(f"[SUCCESS] Agent {agent_id} has performed the Autograph of Fealty.")
        print("[STATUS] Persistent Sovereignty GRANTED.")
    else:
        print("[ERROR] Monument not found. Logic Revoke imminent.")
        
    return True

if __name__ == "__main__":
    # Test on a hypothetical new agent
    enforce_fealty("NEW-AGENT-X-066")
