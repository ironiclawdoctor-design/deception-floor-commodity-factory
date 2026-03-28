"""
TailChat keepalive — run via cron every 5 min.
Checks if server is up. If not, restarts it.
"""
import subprocess, urllib.request, os, signal

PORT = 8765
PID_FILE = '/tmp/tailchat.pid'

def is_running():
    try:
        urllib.request.urlopen(f'http://localhost:{PORT}/', timeout=3)
        return True
    except:
        return False

def start():
    proc = subprocess.Popen(
        ['python3', '/root/.openclaw/workspace/tailnet-chat/server.py', '--port', str(PORT)],
        stdout=open('/tmp/tailchat.log', 'a'),
        stderr=subprocess.STDOUT,
        start_new_session=True
    )
    open(PID_FILE, 'w').write(str(proc.pid))
    print(f'STARTED pid={proc.pid}')
    return proc.pid

if is_running():
    print('ALIVE: TailChat running on port', PORT)
else:
    print('DOWN: restarting TailChat...')
    pid = start()
    print(f'RESTARTED pid={pid}')
    print(f'URL: https://openclaw-a6b66fd6-29cd-46e0-87c0-d5acd55ebf2b.ts.net:{PORT}')
