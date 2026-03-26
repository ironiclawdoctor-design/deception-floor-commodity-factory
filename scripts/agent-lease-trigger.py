import requests
import sys

ENTROPY_API = "http://127.0.0.1:9001"

def process_lease(agent_name):
    print(f"--- FIESTA LEASING: {agent_name} ---")
    # Cost: 1 Shannon to lease for the project
    payload = {
        "from": agent_name,
        "to": "banking-cartel",
        "amount": 1,
        "description": "Long-term internal project lease (1 Shannon)"
    }
    try:
        res = requests.post(f"{ENTROPY_API}/transfer", json=payload, timeout=2)
        if res.status_code == 200:
            print(f"LEASE GRANTED: {agent_name} is now dedicated to the project.")
        else:
            print(f"LEASE DENIED: {res.json().get('error')}")
    except:
        print("LEASE SYSTEM OFFLINE")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        process_lease(sys.argv[1])
