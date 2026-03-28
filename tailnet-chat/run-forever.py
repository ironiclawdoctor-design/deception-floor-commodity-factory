#!/usr/bin/env python3
"""
TailChat forever runner — 99% stability.
Restarts server within 2s on any crash.
Run: nohup python3 run-forever.py > /tmp/tailchat.log 2>&1 &
"""
import subprocess, time, sys, os

SERVER = '/root/.openclaw/workspace/tailnet-chat/server.py'
PORT = 8765

run = 0
while True:
    run += 1
    print(f'[run {run}] Starting TailChat on port {PORT}...', flush=True)
    r = subprocess.run([sys.executable, SERVER, '--port', str(PORT)])
    print(f'[run {run}] Exited (code {r.returncode}). Restarting in 2s...', flush=True)
    time.sleep(2)
