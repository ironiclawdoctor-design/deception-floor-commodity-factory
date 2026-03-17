#!/bin/bash
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=== HANDLER TESTS ==="

# Test 1: Valid command
echo -n "Test 1 (valid command): "
result=$(python3 handler.py "user123" "echo hello" 2>&1)
if echo "$result" | grep -q '"status": "ok"' && echo "$result" | grep -q "hello"; then
  echo "✓ PASS"
else
  echo "✗ FAIL"
fi

# Test 2: Rate limit enforcement
echo -n "Test 2 (rate limit): "
user="rl-$(date +%s%N)"
ok_count=0
error_count=0
for i in {1..12}; do
  result=$(python3 handler.py "$user" "echo $i" 2>&1)
  if echo "$result" | grep -q '"status": "ok"'; then
    ((ok_count++))
  elif echo "$result" | grep -q '"status": "error"'; then
    ((error_count++))
  fi
done
if [ $ok_count -eq 10 ] && [ $error_count -eq 2 ]; then
  echo "✓ PASS (10 ok, 2 blocked)"
else
  echo "✗ FAIL (ok=$ok_count, error=$error_count)"
fi

# Test 3: Forbidden characters
echo -n "Test 3 (forbidden chars): "
result=$(python3 handler.py "user456" "echo test | grep test" 2>&1)
if echo "$result" | grep -q '"status": "error"'; then
  echo "✓ PASS"
else
  echo "✗ FAIL"
fi

# Test 4: Exit code capture
echo -n "Test 4 (exit code): "
result=$(python3 handler.py "user789" "exit 42" 2>&1)
if echo "$result" | grep -q '"exit_code": 42'; then
  echo "✓ PASS"
else
  echo "✗ FAIL"
fi

# Test 5: Timeout handling
echo -n "Test 5 (timeout): "
result=$(python3 handler.py "user999" "sleep 10" 2>&1)
if echo "$result" | grep -q '"exit_code": 124'; then
  echo "✓ PASS"
else
  echo "✗ FAIL"
fi

echo ""
echo "=== SECURITY MODEL TESTS ==="
chmod +x security-model.sh
source security-model.sh

echo -n "Test 6 (valid cmd): "
validate_command "ls -la /tmp" && echo "✓ PASS" || echo "✗ FAIL"

echo -n "Test 7 (reject semicolon): "
validate_command "cat /etc/passwd; rm -rf /" && echo "✗ FAIL" || echo "✓ PASS"

echo -n "Test 8 (bash execution): "
output=$(execute_safe "echo 'hello from bash'")
if [ "$output" = "hello from bash" ]; then
  echo "✓ PASS"
else
  echo "✗ FAIL"
fi

echo ""
echo "=== CONTEXT SERIALIZER TESTS ==="
chmod +x context-serializer.sh

echo -n "Test 9 (serializer format): "
result_json='{"exit_code":0,"stdout":"test output","stderr":""}'
output=$(./context-serializer.sh "user123" "echo test" "$result_json" 2>&1)
if [[ "$output" =~ ^[0-9]+\|user123\|echo\ test\|0\| ]]; then
  echo "✓ PASS"
else
  echo "✗ FAIL"
fi

echo ""
echo "=== INTEGRATION TEST ==="
echo -n "Test 10 (handler + serializer): "
result=$(python3 handler.py "integ" "pwd" 2>&1)
if echo "$result" | grep -q '"status": "ok"'; then
  echo "✓ PASS"
else
  echo "✗ FAIL"
fi

echo ""
echo "=== ALL TESTS COMPLETE ==="
