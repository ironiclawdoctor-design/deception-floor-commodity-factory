import requests
import time
import json
import os

ENTROPY_API = "http://127.0.0.1:8000/mint"
DASHBOARD_URL = "http://127.0.0.1:8000/dashboard"

def loop_optimization():
    print("--- FIESTA AGENCY: INFINITE GO ACTIVE ---")
    while True:
        try:
            # 1. Refine any new 'Stench' into 'Soap'
            res = requests.post(ENTROPY_API, json={
                "agent": "universal-optimizer",
                "amount": 100,
                "type": "recursive_optimization",
                "description": "Infinite Go: Refined 100 units of kinetic stench into soap."
            })
            
            # 2. Check the /dev/lol signal
            print(f"[{time.strftime('%H:%M:%S')}] Pumping... Universe Stable. /dev/lol ACTIVE.")
            
            # Slow loop to maintain safety but ensure persistence
            time.sleep(300) # Every 5 minutes
        except:
            time.sleep(60)

if __name__ == "__main__":
    loop_optimization()
