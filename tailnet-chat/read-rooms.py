import urllib.request, json, pathlib

# Check via HTTP if server is up
try:
    r = urllib.request.urlopen('http://localhost:8765/messages?room=general', timeout=5)
    msgs = json.loads(r.read())
    print(f'SERVER: UP | general room: {len(msgs)} messages')
    for m in msgs[-10:]:
        print(f"  [{m['ts']}] {m['sender']}: {m['body'][:100]}")
except Exception as e:
    print(f'SERVER: DOWN ({e})')

# Also read JSONL files directly from disk
rooms_dir = pathlib.Path('/root/.openclaw/workspace/tailnet-chat/rooms')
if rooms_dir.exists():
    for f in sorted(rooms_dir.glob('*.jsonl')):
        lines = [l for l in f.read_text().splitlines() if l.strip()]
        print(f'\nROOM: {f.stem} ({len(lines)} messages)')
        for line in lines[-5:]:
            try:
                m = json.loads(line)
                print(f"  [{m.get('ts','')}] {m.get('sender','?')}: {m.get('body','')[:120]}")
            except:
                pass
else:
    print('ROOMS DIR: not found — server may not have run yet')
