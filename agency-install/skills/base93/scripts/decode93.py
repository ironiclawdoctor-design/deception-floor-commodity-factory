#!/usr/bin/env python3
"""
decode93.py — Shell-callable decoder. Reads base93 from stdin, writes JSON to stdout.
Usage: echo "B9:CR:3924:ABc..." | python3 decode93.py
"""
import sys
import json
sys.path.insert(0, '/root/.openclaw/workspace/skills/base93/scripts')
from core import decode93

raw = sys.stdin.read().strip()
try:
    envelope = decode93(raw)
    print(json.dumps(envelope, indent=2))
except Exception as e:
    print(json.dumps({"error": str(e), "input": raw[:40]}), file=sys.stderr)
    sys.exit(1)
