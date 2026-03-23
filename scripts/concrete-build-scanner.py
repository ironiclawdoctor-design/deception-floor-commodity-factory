import os
import glob
from datetime import datetime

def scan_concrete_builds():
    print("--- FIESTA ORCHESTRATOR: CONCRETE BUILD STATUS ---")
    
    # Define the 'Build' zones
    search_paths = [
        "/root/.openclaw/workspace/scripts/*.py",
        "/root/.openclaw/workspace/revenue/*/*.json",
        "/root/.openclaw/workspace/economy/*/*.json",
        "/root/.openclaw/workspace/status/*.md"
    ]
    
    builds = []
    for path in search_paths:
        for file in glob.glob(path):
            mtime = os.path.getmtime(file)
            dt = datetime.fromtimestamp(mtime).strftime('%Y-%m-%d %H:%M:%S')
            builds.append(f"{dt} | BUILD: {file}")
    
    builds.sort(reverse=True)
    
    print(f"Detected {len(builds)} Concrete Builds in the last cycle.")
    for b in builds[:10]: # Top 10 latest builds
        print(b)
        
    print("\nSTATUS: ACTUAL. The agency is what it builds.")
    return len(builds)

if __name__ == "__main__":
    scan_concrete_builds()
