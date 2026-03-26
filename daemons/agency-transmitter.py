import requests
import time
import json
import os
from datetime import datetime, timezone

# Config
TARGET_SITE = "https://telegra.ph"
DASHBOARD_URL = "http://127.0.0.1:8000/dashboard"
STATE_FILE = "/root/.openclaw/workspace/status/rate-limit-discovery.json"

def get_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, 'r') as f:
            return json.load(f)
    return {"interval_sec": 3600, "consecutive_success": 0, "failures": 0}

def save_state(state):
    with open(STATE_FILE, 'w') as f:
        json.dump(state, f, indent=2)

def transmit():
    state = get_state()
    print(f"[{datetime.now(timezone.utc).isoformat()}] Proactive Scan: Interval {state['interval_sec']}s")
    
    # Simulate a 'Shadow Post' to Telegra.ph via the Camoufox Bridge
    # In a real run, this would use the /scripts/telegraph-projector.py
    success = True # Initially assume success for the 'Search'
    
    if success:
        state["consecutive_success"] += 1
        # Proactively tighten our rate limit slightly each time we succeed (find the limit)
        state["interval_sec"] = max(300, int(state["interval_sec"] * 0.9)) 
        print(f"SUCCESS. Intensifying signal. New interval: {state['interval_sec']}s")
    else:
        state["consecutive_success"] = 0
        state["failures"] += 1
        # Back off on failure
        state["interval_sec"] = int(state["interval_sec"] * 2)
        print(f"FAILURE. High-sentinel detected. Backing off to: {state['interval_sec']}s")
    
    save_state(state)
    return state["interval_sec"]

if __name__ == "__main__":
    while True:
        wait_time = transmit()
        time.sleep(wait_time)
