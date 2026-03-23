import os
import glob
import json
from datetime import datetime, timezone

WORKSPACE = "/root/.openclaw/workspace"
FRONTIERS_LOG = "/root/.openclaw/workspace/frontiers/motilized.jsonl"

def motilize():
    # Scan for unused frontiers (files in workspace not recently touched or with 'speculation' in name)
    files = glob.glob(f"{WORKSPACE}/**/*.md", recursive=True) + glob.glob(f"{WORKSPACE}/**/*.json", recursive=True)
    unused = [f for f in files if "speculation" in f or "lead-gen" in f]
    
    results = []
    for f in unused:
        # Create a 'Motility Signature' - a concrete action for an unused thought
        sig = {
            "source_file": f,
            "motility_trigger": "AUTO_RESEARCH_V1",
            "actionable_query": f"latest developments in {os.path.basename(f).replace('.md','').replace('.json','')}",
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        results.append(sig)
        
        # Log motility
        with open(FRONTIERS_LOG, "a") as log:
            log.write(json.dumps(sig) + "\n")
            
    return results

if __name__ == "__main__":
    count = len(motilize())
    print(f"MOTILIZED {count} FRONTIERS.")
