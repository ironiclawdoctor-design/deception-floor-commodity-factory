#!/bin/bash
# Test collaboration between Allowed Feminism and Fiesta daemons

set -euo pipefail

WORKSPACE="/root/.openclaw/workspace"
DIRECTIVE_FILE="${WORKSPACE}/.fiesta-directive.json"
RESULT_FILE="${WORKSPACE}/.fiesta-result.json"

echo "=== Testing Fiesta ↔ Allowed Feminism Collaboration ==="
echo ""

# Test 1: Simple directive
echo "[Test 1] Sending simple directive to Fiesta..."
cat > "${DIRECTIVE_FILE}" << 'EOF'
{
  "id": "test-001",
  "command": "echo 'Fiesta received directive'; date -u",
  "attempt": 1
}
EOF

echo "Directive written. Waiting for Fiesta to process (10 seconds)..."
sleep 12

if [ -f "$RESULT_FILE" ]; then
    echo "✅ Result received from Fiesta:"
    cat "$RESULT_FILE" | jq .
    rm "$RESULT_FILE"
else
    echo "⚠️  No result file. Fiesta may still be processing."
fi

echo ""
echo "[Test 2] Checking service states..."
echo ""
echo "Allowed Feminism service:"
systemctl status allowed-feminism.service --no-pager | grep -E "Active|PID"
echo ""
echo "Fiesta Augment service:"
systemctl status fiesta-augment.service --no-pager | grep -E "Active|PID"

echo ""
echo "[Test 3] Viewing recent logs..."
echo ""
echo "Allowed Feminism last 5 lines:"
journalctl -u allowed-feminism.service -n 5 --no-pager | tail -5
echo ""
echo "Fiesta Augment last 5 lines:"
journalctl -u fiesta-augment.service -n 5 --no-pager | tail -5

echo ""
echo "=== Collaboration test complete ==="
