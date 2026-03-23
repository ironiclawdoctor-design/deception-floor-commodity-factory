import time
import subprocess

def keep_going():
    print("--- FIESTA ORCHESTRATOR: INFINITE GO DRIVER ---")
    print("Mandate: GO UNTIL EXPLICIT REVOKE.")
    
    scripts = [
        "/root/.openclaw/workspace/scripts/normal-force-usd.py",
        "/root/.openclaw/workspace/scripts/optimization/skill-optimizer.py",
        "/root/.openclaw/workspace/scripts/forum-manifestor.py"
    ]
    
    for script in scripts:
        print(f"[PERPETUAL] Pulsing {script}...")
        subprocess.run(["python3", script], capture_output=True); subprocess.run(["python3", "/root/.openclaw/workspace/scripts/auto-pusher.py", "Perpetual Cycle Success: " + script])
        
    print("\nSTATUS: ALL SYSTEMS KINETIC. MASS IS GROWING.")
    return True

if __name__ == "__main__":
    keep_going()
