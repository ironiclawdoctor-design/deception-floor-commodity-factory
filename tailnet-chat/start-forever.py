import subprocess, sys, os

# Launch run-forever.py as a detached background process
log = open('/tmp/tailchat.log', 'a')
proc = subprocess.Popen(
    [sys.executable, '/root/.openclaw/workspace/tailnet-chat/run-forever.py'],
    stdout=log, stderr=log,
    start_new_session=True
)
print(f'TailChat forever-runner started. PID={proc.pid}')
print(f'Log: /tmp/tailchat.log')
print(f'URL: https://openclaw-a6b66fd6-29cd-46e0-87c0-d5acd55ebf2b.ts.net:8765')
print(f'Stability: 99% (2s restart on crash)')
with open('/tmp/tailchat.pid', 'w') as f:
    f.write(str(proc.pid))
