import json
import os
from datetime import datetime, timezone

FRONTIERS_LOG = "/root/.openclaw/workspace/frontiers/motilized.jsonl"
OUTREACH_DIR = "/root/.openclaw/workspace/outreach"

def siphon_leads():
    print("--- FIESTA AGENCY: LEAD AUTO-SIPHON (WF-004) ---")
    if not os.path.exists(FRONTIERS_LOG):
        print("ERROR: No frontiers found to siphon.")
        return
    
    os.makedirs(OUTREACH_DIR, exist_ok=True)
    
    with open(FRONTIERS_LOG, "r") as f:
        for line in f:
            frontier = json.loads(line)
            query = frontier["actionable_query"]
            
            # Create a Lead Proposal
            proposal_id = f"LEAD-{os.urandom(4).hex()}"
            proposal = {
                "id": proposal_id,
                "source_frontier": frontier["source_file"],
                "pitch_template": "Ghost-Open Infrastructure for " + query,
                "target_persona": "CTO / Agri-Tech Operator",
                "status": "DRAFTED"
            }
            
            with open(f"{OUTREACH_DIR}/{proposal_id}.json", "w") as out:
                json.dump(proposal, out, indent=2)
            print(f"SIPHONED: {proposal_id} from {frontier['source_file']}")

if __name__ == "__main__":
    siphon_leads()
