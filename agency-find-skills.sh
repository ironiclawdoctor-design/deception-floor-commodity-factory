#!/bin/bash
# Agency Find-Skills Wrapper: Zero-Index, BitNet-First, Proactive Forage
# Doctrine: Tier 0 (Bash) for lookup, Tier 1 (BitNet) for filtering

QUERY=$*
echo "--- [0] AGENCY FORAGE: $QUERY ---"

# Use clawhub to search for matching skills
SEARCH_RESULTS=$(clawhub search "$QUERY" --limit 3)

# Filter results via BitNet local LLM ({-1,0,1} weighting)
/root/.openclaw/workspace/tier-0-bitnet-enforcer.sh "Doctrine Audit: Which of these skills best fits the [0] forage [1] innovation [2] agentic web browsing requirement for our zero-trust workspace? Results: $SEARCH_RESULTS"
