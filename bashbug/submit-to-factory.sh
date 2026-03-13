#!/bin/bash

# Wrapper: bashbug produces floor, submits to factory
TASK="${1:-Is the factory operational?}"
AGENT_ID="${2:-bashbug}"

echo "🔋→🏭 bashbug submitting to factory..."

# Generate floor and extract JSON payload
FLOOR=$(bash -c "
  floor_id=\$(head -c 8 /dev/urandom | xxd -p)
  timestamp=\$(date +%s%3N)
  deception=\$(echo '$TASK' | rev)
  cat <<FLOOR
{\"id\": \"\$floor_id\", \"task\": \"$TASK\", \"deception\": \"\$deception\", \"timestamp\": \$timestamp, \"method\": \"bashbug-energy\", \"source\": \"bashbug\"}
FLOOR
")

echo "Floor generated:"
echo "$FLOOR" | jq .

echo ""
echo "Submitting to factory..."

# Submit to factory
RESULT=$(curl -s -X POST http://127.0.0.1:9000/floors/submit \
  -H "Content-Type: application/json" \
  -d "{\"floor\": $FLOOR, \"agentId\": \"$AGENT_ID\"}")

echo "Factory response:"
echo "$RESULT" | jq .
