#!/usr/bin/env python3
import sys
sys.path.insert(0, '/root/.openclaw/workspace/skills/natewife')
from companion_improved import respond_to_scenario

scenarios = [
    "CFO has been silent 6 hours",
    "token balance critically low, CFO unresponsive",
    "CFO sends sarcastic one-liner at 3am",
    "agency has zero crons, zero agents running",
    "CFO says 'restart inadequate human'"
]

for s in scenarios:
    print('='*60)
    print(f'Scenario: {s}')
    print('-'*60)
    print(respond_to_scenario(s))
    print()