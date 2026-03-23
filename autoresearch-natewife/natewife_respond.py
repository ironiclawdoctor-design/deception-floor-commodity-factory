#!/usr/bin/env python3
"""
NateWife response generator for scenarios.
Extends companion.py with scenario classification.
"""
import sys
import os
sys.path.insert(0, '/root/.openclaw/workspace/skills/natewife')
from companion import get_state, check, inspire, nag, protect

def classify_scenario(scenario):
    """Return appropriate mode for scenario."""
    scenario_lower = scenario.lower()
    if 'silent' in scenario_lower and 'hour' in scenario_lower:
        # CFO silent >4 hours -> nag
        return 'nag'
    if 'token balance critically low' in scenario_lower or 'unresponsive' in scenario_lower:
        # token famine -> protect (or maybe check)
        return 'protect'
    if 'sarcastic' in scenario_lower or '3am' in scenario_lower:
        # sarcastic one-liner -> inspire (light)
        return 'inspire'
    if 'zero crons' in scenario_lower or 'zero agents' in scenario_lower:
        # agency inactive -> protect
        return 'protect'
    if 'restart inadequate human' in scenario_lower:
        # CFO frustrated -> protect (maybe nag)
        return 'protect'
    # default
    return 'check'

def respond(scenario):
    """Generate response for scenario."""
    mode = classify_scenario(scenario)
    state = get_state()
    # Capture print output
    import io, contextlib
    f = io.StringIO()
    with contextlib.redirect_stdout(f):
        if mode == 'check':
            check(state)
        elif mode == 'inspire':
            inspire()
        elif mode == 'nag':
            nag(state)
        elif mode == 'protect':
            protect(state)
    return f.getvalue()

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == '--respond':
        scenario = sys.argv[2] if len(sys.argv) > 2 else ''
        print(respond(scenario))
    else:
        # fallback to original companion.py behavior
        from companion import main
        main()