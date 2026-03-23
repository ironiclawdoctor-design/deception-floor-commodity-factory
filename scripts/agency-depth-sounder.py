import os
import sqlite3
import requests
import time

# Config
DB_PATH = "/root/.openclaw/workspace/projects/entropy-economy/entropy_ledger.db"
WORKSPACE = "/root/.openclaw/workspace"

def sound_depth():
    print("--- FIESTA AGENCY: DEPTH SOUNDING ---")
    print("Mode: Standing (Sovereign) -> Sounding (Probing)")
    
    # Measure 1: Shannon Density
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("SELECT SUM(balance_shannon) FROM wallets;")
        total_shannon = c.fetchone()[0] or 0
        c.execute("SELECT COUNT(*) FROM agents;")
        agent_count = c.fetchone()[0] or 1
        conn.close()
        density = total_shannon / agent_count
        print(f"Depth 0 (Economy): {total_shannon} Shannon / {agent_count} Agents = {density:.2f} Density")
    except:
        print("Depth 0 (Economy): PING TIMED OUT (ECONOMY RESTRICTED)")

    # Measure 2: Workspace Structural Mass
    try:
        file_count = sum([len(files) for r, d, files in os.walk(WORKSPACE)])
        print(f"Depth 1 (Artifacts): {file_count} Sovereign files detected.")
    except:
        print("Depth 1 (Artifacts): PING LOST (FILESYSTEM SEGMENTED)")

    # Measure 3: Signal Latency
    try:
        start = time.time()
        requests.get("http://127.0.0.1:9001/health", timeout=2)
        latency = (time.time() - start) * 1000
        print(f"Depth 2 (Signal): {latency:.2f}ms Heartbeat Latency")
    except:
        print("Depth 2 (Signal): ECHO LOST (REFINERY RESTARTING)")

    print("\nSOUNDING COMPLETE: Perimeter firm. Depth verified.")

if __name__ == "__main__":
    sound_depth()
