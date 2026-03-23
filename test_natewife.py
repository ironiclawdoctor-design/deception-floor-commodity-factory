#!/usr/bin/env python3
import subprocess
import sys
import os

sys.path.insert(0, '/root/.openclaw/workspace/skills/natewife')
os.chdir('/root/.openclaw/workspace/skills/natewife')

def run_mode(mode):
    cmd = ['python3', 'companion.py', mode]
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.stdout.strip()

if __name__ == '__main__':
    modes = ['--check', '--inspire', '--nag', '--protect']
    for m in modes:
        print(f'=== {m} ===')
        print(run_mode(m))
        print()