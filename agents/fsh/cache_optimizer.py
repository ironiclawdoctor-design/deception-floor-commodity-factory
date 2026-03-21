import sys
import json
import os
import time

CACHE_FILE = "/root/.openclaw/workspace/agents/fsh/cmd_cache.json"

def load_cache():
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_cache(cache):
    with open(CACHE_FILE, 'w') as f:
        json.dump(cache, f)

action = sys.argv[1]
cmd = " ".join(sys.argv[2:])

cache = load_cache()

if action == "check":
    # Logic: If command was run recently (< 60s), it's 'Optimized' (Free)
    last_run = cache.get(cmd, 0)
    if time.time() - last_run < 60:
        print("OK") # Cached excellence
    else:
        # Check for 'cannot' or 'rate limit' patterns to block heavy syscalls
        if "curl" in cmd or "clawhub" in cmd:
             # Apply the 14-day gate logic from Agent CANNOT
             print("BLOCK")
        else:
             print("OK")

elif action == "log":
    cache[cmd] = time.time()
    save_cache(cache)
