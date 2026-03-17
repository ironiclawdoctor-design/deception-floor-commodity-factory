#!/bin/bash
# Telegram↔Bash CLI wrapper
# Usage: ./telegram-cli.sh <user_id> <command>

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

USER_ID="${1:-unknown}"
COMMAND="${2:-}"

if [ -z "$COMMAND" ]; then
  echo '{"error":"Usage: telegram-cli.sh <user_id> <command>"}'
  exit 1
fi

# Execute via handler
result=$(python3 handler.py "$USER_ID" "$COMMAND" 2>&1)

# Serialize context
if echo "$result" | grep -q '"status": "ok"'; then
  json_result=$(echo "$result" | python3 -c "
import sys, json
data = json.load(sys.stdin)
print(json.dumps(data['result']))
")
  ./context-serializer.sh "$USER_ID" "$COMMAND" "$json_result"
else
  echo "$result"
fi
