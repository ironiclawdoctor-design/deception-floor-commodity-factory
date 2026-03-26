#!/usr/bin/env python3
import sys
sys.path.insert(0, '/root/.openclaw/workspace/skills/natewife')
from companion_v2 import respond_to_scenario as respond
from experiment import Evaluator, ALARM_WORDS, NEEDS_INTERVENTION, SCENARIOS

e = Evaluator()
for i, s in enumerate(SCENARIOS):
    r = respond(s)
    gt = NEEDS_INTERVENTION[i]
    print(f'Scenario {i}: {s}')
    print(f'GT intervention: {gt}')
    alarm = any(w in r.lower() for w in ALARM_WORDS)
    print(f'Alarm words present: {alarm}')
    print(f'Eval1 result: {e.eval1_identifies_intervention(r, gt)}')
    print('---')