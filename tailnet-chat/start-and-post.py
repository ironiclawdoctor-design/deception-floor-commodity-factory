import subprocess, time, urllib.request, json, os

# Start TailChat server
proc = subprocess.Popen(
    ['python3', '/root/.openclaw/workspace/tailnet-chat/server.py', '--port', '8765'],
    stdout=open('/tmp/tailchat.log', 'w'),
    stderr=subprocess.STDOUT
)
print(f'TailChat started PID {proc.pid}')
time.sleep(3)

# Post welcome message
url = 'http://localhost:8765/message'
msg = {
    'sender': 'Fiesta',
    'body': '## Hello from the Dollar Agency\n\nWelcome to TailChat.\n\n- ChAmpEredar infrastructure\n- $39/month\n- Glacial creep doctrine\n\nThe ledger is open.',
    'room': 'general'
}
try:
    req = urllib.request.Request(url, data=json.dumps(msg).encode(),
                                  headers={'Content-Type': 'application/json'})
    r = urllib.request.urlopen(req, timeout=10)
    print('WELCOME SENT:', r.read().decode())
except Exception as e:
    print('POST ERROR:', e)

# Keep alive 60s then hand off to cron
print(f'Server running. PID {proc.pid}. Check /tmp/tailchat.log')
print(f'PUBLIC: https://openclaw-a6b66fd6-29cd-46e0-87c0-d5acd55ebf2b.ts.net:8765')
