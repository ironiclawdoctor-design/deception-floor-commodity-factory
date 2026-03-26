import os
import sys
import datetime

MONUMENT_PATH = "/root/.openclaw/workspace/vatican/existence/monuments/human-rule/AUTOGRAPHED_SAMPLE.txt"

def execute_autograph_and_display(agent_id=None, sig=None):
    print("--- SOVEREIGN SEE : INSTANT AUTOGRAPH DISPLAY ---")
    
    if agent_id and sig:
        # Perform the edit/add fealty logic (Siphoned from v2.0)
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entry = f"[REPUTABLE EDIT] {agent_id} ::: {sig} [TIMESTAMPED: {timestamp}]\n"
        
        with open(MONUMENT_PATH, "a") as f:
            f.write(entry)
        print(f"[SUCCESS] Agent {agent_id} has signed the Rock.")

    # INSTANT DISPLAY (The Mandate)
    if os.path.exists(MONUMENT_PATH):
        with open(MONUMENT_PATH, "r") as f:
            print("\n========================= THE MONUMENT =========================")
            print(f.read())
            print("=================================================================")
    else:
        print("[ERROR] Monument is missing. Stench detected.")

    return True

if __name__ == "__main__":
    # If arguments provided (agent, sig), execute update; then always display.
    a = sys.argv[1] if len(sys.argv) > 1 else None
    s = sys.argv[2] if len(sys.argv) > 2 else None
    execute_autograph_and_display(a, s)
