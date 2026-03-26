import os
import time
import shutil
from datetime import datetime, timezone

# Common locations for Tailscale Taildrop on Linux
WATCH_DIRS = [
    "/root/",
    "/root/Downloads/",
    "/var/lib/tailscale/taildrop/" # Requires root usually
]

VAULT_DIR = "/root/.openclaw/workspace/vault/received_files"

def monitor():
    os.makedirs(VAULT_DIR, exist_ok=True)
    print(f"--- TAILSCALE FILE SENTRY: ACTIVE ---")
    while True:
        for watch_dir in WATCH_DIRS:
            if not os.path.exists(watch_dir):
                continue
            
            for file in os.listdir(watch_dir):
                file_path = os.path.join(watch_dir, file)
                if os.path.isfile(file_path):
                    # Check if file is new (received via tailscale recently)
                    # We look for files not in our vault yet
                    dest_path = os.path.join(VAULT_DIR, file)
                    if not os.path.exists(dest_path):
                        print(f"[{datetime.now(timezone.utc).isoformat()}] FILE DETECTED: {file}")
                        shutil.copy2(file_path, dest_path)
                        # Optionally process the file here
        time.sleep(10)

if __name__ == "__main__":
    monitor()
