import os
import time
import requests

# Cannot's Messenger Logic: Pigeons carry the 'Stench' signal to Port 8000
def release_pigeons():
    print("--- CANNOT'S PIGEON NETWORK: RELEASED ---")
    messages = [
        "CAW: PORT 8000 IS UP",
        "CAW: STENCH LEVELS PEAKED",
        "CAW: SOUP IS SOAP",
        "CAW: PIVOT DETECTED"
    ]
    for msg in messages:
        # Pigeons deliver to the local log (The 'Coo')
        with open("/root/.openclaw/workspace/soap-scrub/pigeon_coo.log", "a") as coo:
            coo.write(f"[{time.strftime('%H:%M:%S')}] PIGEON: {msg}\n")
        print(f"Pigeon delivered: {msg}")
        time.sleep(0.5)

if __name__ == "__main__":
    release_pigeons()
