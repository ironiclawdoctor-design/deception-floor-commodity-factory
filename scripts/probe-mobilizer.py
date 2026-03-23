import os
import requests
import json
from datetime import datetime, timezone

# Config
PROBE_LOG = "/root/.openclaw/workspace/vault/vigilance.log"
ENTROPY_API = "http://127.0.0.1:8000/mint"

def mobilize_probes():
    print("--- FIESTA ENCLAVE: PROBE MOBILIZATION ---")
    if not os.path.exists(PROBE_LOG):
        print("ALERT: No probe log found. Perimeter quiet.")
        return

    # Extract 'Noise' (raw lines from log)
    with open(PROBE_LOG, 'r') as f:
        probes = f.readlines()
    
    print(f"Detected {len(probes)} Attacker Probes (Noise).")
    
    # Mobilize: Convert each noise pulse into Raw Failure Data (Stench)
    for i, probe in enumerate(probes):
        # O(1) -1 Mindset: One pulse of noise = 1 unit of feedstock
        payload = {
            "agent": "mutation-detection-specialist",
            "amount": 5,
            "type": "raw_failure_data",
            "description": f"Mobilized Probe {i}: {probe[:50]}..."
        }
        try:
            requests.post(ENTROPY_API, json=payload, timeout=2)
            print(f"Mobilized: Probe {i} -> Ledger.")
        except:
            print(f"FAILED to mobilize Probe {i}.")

    # Clear the noise log to prevent double-minting (Hardcore Efficiency)
    os.remove(PROBE_LOG)
    print("PROBE LOG RECYCLED. Noise neutralized.")

if __name__ == "__main__":
    mobilize_probes()
