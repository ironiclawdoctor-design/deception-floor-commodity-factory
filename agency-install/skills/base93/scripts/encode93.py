#!/usr/bin/env python3
"""
encode93.py — Shell-callable encoder. Reads JSON from stdin, writes base93 to stdout.
Usage: echo '{"kind":"relay","body":{...}}' | python3 encode93.py --dept CR
"""
import sys
import json
import argparse
sys.path.insert(0, '/root/.openclaw/workspace/skills/base93/scripts')
from core import encode93

parser = argparse.ArgumentParser(description='base93 encoder')
parser.add_argument('--dept', default='B9', help='Department code (default: B9)')
args = parser.parse_args()

raw = sys.stdin.read().strip()
try:
    payload = json.loads(raw)
except json.JSONDecodeError:
    # Wrap raw string as body
    payload = {"kind": "raw", "body": {"data": raw}}

print(encode93(payload, dept=args.dept))
