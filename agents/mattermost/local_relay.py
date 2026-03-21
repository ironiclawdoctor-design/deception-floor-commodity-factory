#!/usr/bin/env python3
"""
Local webhook relay — queues outbound messages until real URL is configured.
Writes to /tmp/webhook_queue.jsonl and prints to stdout.
"""
import json, sys, os
from datetime import datetime, timezone

QUEUE = "/root/.openclaw/workspace/logs/webhook_queue.jsonl"
os.makedirs(os.path.dirname(QUEUE), exist_ok=True)

def queue_message(text, target="mattermost"):
    entry = {"timestamp": datetime.now(timezone.utc).isoformat(), "target": target, "text": text, "status": "QUEUED"}
    with open(QUEUE, "a") as f:
        f.write(json.dumps(entry) + "\n")
    print(f"[RELAY] Queued for {target}: {text[:60]}...")

if __name__ == "__main__":
    msg = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "Agency heartbeat"
    queue_message(msg)
