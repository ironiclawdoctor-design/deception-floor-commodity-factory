#!/bin/bash
# Directive Lookup Query Tool
# Usage: ./query.sh <pattern>
# Cost: $0.00 | Tier: 0

LOOKUP_FILE="/root/.openclaw/workspace/agency-directives/lookup-table.json"
QUERY="$1"

if [ -z "$QUERY" ]; then
    echo "Usage: $0 <directive-pattern>"
    echo "Examples: $0 'do it' | $0 'status' | $0 'build'"
    exit 1
fi

# Simple grep-based lookup (Tier 0)
echo "--- [0] DIRECTIVE LOOKUP: '$QUERY' ---"
jq -r --arg q "$QUERY" '
  .directive_patterns | to_entries[] | 
  select(.value.patterns[] | contains($q)) |
  "Pattern: \(.key)\n  Action: \(.value.action)\n  Tier: \(.value.tier)\n  Cost: \(.value.cost)\n  Patterns: \(.value.patterns | join(\", \"))"
' "$LOOKUP_FILE" 2>/dev/null || grep -i "$QUERY" "$LOOKUP_FILE" | head -10

echo "--- [1] RECENT MATCHING DIRECTIVES ---"
jq -r --arg q "$QUERY" '
  .session_directives[] | 
  select(.directive | contains($q)) |
  "\(.timestamp): \(.directive) → \(.action) [\(.cost)]"
' "$LOOKUP_FILE" 2>/dev/null | head -5
