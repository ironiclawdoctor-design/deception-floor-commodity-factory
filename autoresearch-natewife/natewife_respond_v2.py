#!/usr/bin/env python3
"""
NateWife respond v2 — uses companion_v2 for adversarially-hardened responses.
Drop-in replacement for natewife_respond.py.
"""
import sys, io, contextlib
sys.path.insert(0, '/root/.openclaw/workspace/autoresearch-natewife')
from companion_v2 import respond_to_scenario, get_state, check, inspire, nag, protect


def respond(scenario):
    """Generate response for scenario using v2 companion logic."""
    return respond_to_scenario(scenario)


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == '--respond':
        scenario = sys.argv[2] if len(sys.argv) > 2 else ''
        print(respond(scenario))
    else:
        state = get_state()
        check(state)
