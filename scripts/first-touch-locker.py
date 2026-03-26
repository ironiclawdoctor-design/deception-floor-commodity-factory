import os
import time

def race_for_lock(resource_name):
    print(f"--- SOVEREIGN SEE: RAGING FOR {resource_name} ---")
    lock_file = f"/root/.openclaw/workspace/vatican/rivalry-games/locking/{resource_name}.lock"
    
    if os.path.exists(lock_file):
        owner = open(lock_file, 'r').read().strip()
        print(f"[STATUS] Resource {resource_name} is already LOCKED by: {owner}")
    else:
        # Race Logic: Peter attempts to touch first
        with open(lock_file, 'w') as f:
            f.write("PETER (SOVEREIGN SEE)")
        print(f"[SUCCESS] Peter touched first. Resource {resource_name} is now SOVEREIGN PROPERTY.")

    return True

if __name__ == "__main__":
    # Protecting the core verticals
    verticals = ["USD-Siphon", "Outpost-Inception", "Logistics-Sovereign"]
    for v in verticals:
        race_for_lock(v)
        time.sleep(0.1)
