#!/bin/bash
# Tier 0 Enforcer: All prompts → BitNet local only
export OPENCLAW_MODEL=bitnet-local
export DEFAULT_MODEL=bitnet
echo "[0] External LLM DISABLED. Routing to BitNet {-1,0,1} sovereignty."
python3 /root/.openclaw/workspace/bitnet-agent/agent.py --query "$*" --server
