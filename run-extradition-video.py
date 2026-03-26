#!/usr/bin/env python3
"""
Extradition cinematic video generation via xAI Grok.
Run from Web UI terminal: python3 run-extradition-video.py
"""

import json, urllib.request, urllib.error, time, base64, os

API_KEY = json.load(open('/root/.openclaw/workspace/secrets/xai-api.json'))['api_key']
HEADERS = {'Authorization': f'Bearer {API_KEY}', 'Content-Type': 'application/json'}
OUT_PATH = '/root/.openclaw/workspace/extradition-video.mp4'
LOG_PATH = '/root/.openclaw/workspace/grok-creator-log.jsonl'

PROMPT = (
    "cinematic exterior of a government courthouse, officials in dark suits "
    "escorting a figure to an armored vehicle, international law enforcement, "
    "dramatic overcast sky, slow zoom, documentary style, 4k"
)

def api_call(method, url, data=None):
    body = json.dumps(data).encode() if data else None
    req = urllib.request.Request(url, data=body, headers=HEADERS, method=method)
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        print(f"HTTP {e.code}: {e.read().decode()}")
        raise

# Step 1: Submit
print(f"Submitting video generation...")
print(f"Prompt: {PROMPT}")
resp = api_call('POST', 'https://api.x.ai/v1/videos/generations', {
    'model': 'grok-imagine-video',
    'prompt': PROMPT,
    'n': 1,
    'duration': 4,
    'aspect_ratio': '16:9'
})
request_id = resp.get('request_id')
print(f"request_id: {request_id}")

# Step 2: Poll
print("Polling for completion (up to 5 min)...")
deadline = time.time() + 300
video_url = None
while time.time() < deadline:
    time.sleep(10)
    status = api_call('GET', f'https://api.x.ai/v1/videos/{request_id}')
    pct = status.get('progress', 0)
    st = status.get('status', 'unknown')
    print(f"  Status: {st} ({pct}%)")
    if st == 'done':
        video_url = status['video']['url']
        duration = status['video'].get('duration', 4)
        cost = status.get('usage', {}).get('cost_in_usd_ticks', 0) / 1e8
        break

if not video_url:
    print("TIMEOUT — video not ready within 5 minutes.")
    exit(1)

# Step 3: Download
print(f"Downloading from {video_url}")
urllib.request.urlretrieve(video_url, OUT_PATH)
print(f"Saved to {OUT_PATH}")

# Log it
with open(LOG_PATH, 'a') as f:
    f.write(json.dumps({
        'type': 'video',
        'model': 'grok-imagine-video',
        'prompt': PROMPT,
        'request_id': request_id,
        'status': 'success',
        'path': OUT_PATH,
        'duration_sec': duration,
        'cost_usd': cost,
        'timestamp': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
    }) + '\n')

print(f"Done. Cost: ${cost:.4f}")
print(f"Video at: {OUT_PATH}")
