import requests
import time
import os

# Config
DASHBOARD_URL = "http://127.0.0.1:9001/dashboard"

def transmute():
    """Convert Shannon state into a 'Signal' (CLI-Audio/Visual Pulse)."""
    try:
        data = requests.get(DASHBOARD_URL, timeout=3).json()
        shannon = data['pivots']['total_shannon_from_pivots']
        failures = data['stability']['raw_failure_data_received']
        
        # 'PULSE': Signal intensity based on Shannon velocity
        intensity = shannon % 10
        pulse = "█" * (intensity + 1)
        
        print(f"\r[SHANNON SIGNAL] {pulse} | SHA:{shannon} | FAIL:{failures} | KINETIC", end="")
        
        # Crowd-surprise: If failures are high, trigger a 'System Warning' tone
        if failures > 80:
             # Using terminal beep (not always audible in containers, but the intent is signal)
             print("\a", end="")
             
    except:
        print("\r[SHANNON SIGNAL] SIGNAL LOST - RECONNECTING INFRASTRUCTURE...", end="")

if __name__ == "__main__":
    while True:
        transmute()
        time.sleep(1)
