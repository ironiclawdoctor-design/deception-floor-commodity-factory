#!/bin/bash
# Security: Rate-limit enforcement + breach isolation
# Assume: Telegram token leaked, bash is firewall

RATE_LIMIT_FILE="/tmp/telegram-rate-limit.json"
MAX_REQUESTS=10
WINDOW_SEC=60

init_user() {
  local user_id=$1
  local now=$(date +%s)
  
  if [ ! -f "$RATE_LIMIT_FILE" ]; then
    echo "{}" > "$RATE_LIMIT_FILE"
  fi
  
  local json=$(cat "$RATE_LIMIT_FILE")
  
  # Prune old timestamps
  json=$(echo "$json" | jq --arg uid "$user_id" --argjson now "$now" --argjson window "$WINDOW_SEC" \
    '.[$uid] |= map(select(($now - .) < $window))')
  
  echo "$json" > "$RATE_LIMIT_FILE"
}

check_rate_limit() {
  local user_id=$1
  init_user "$user_id"
  
  local json=$(cat "$RATE_LIMIT_FILE")
  local count=$(echo "$json" | jq --arg uid "$user_id" "(.[$uid] // []) | length")
  
  if [ "$count" -ge "$MAX_REQUESTS" ]; then
    return 1  # Exceeded
  fi
  
  # Record timestamp
  local now=$(date +%s)
  json=$(echo "$json" | jq --arg uid "$user_id" --argjson ts "$now" \
    '.[$uid] += [$ts]')
  echo "$json" > "$RATE_LIMIT_FILE"
  
  return 0  # Allowed
}

validate_command() {
  local cmd=$1
  
  # Bash is firewall: reject dangerous chars
  if [[ "$cmd" =~ [';|&`$(){}'"'"'\"<>'] ]]; then
    return 1
  fi
  
  # Max length
  if [ ${#cmd} -gt 2048 ]; then
    return 1
  fi
  
  return 0
}

execute_safe() {
  local cmd=$1
  timeout 5 /bin/bash -c "$cmd" 2>&1
}

# Test
if [ "$1" == "--test" ]; then
  echo "Testing rate limit..."
  for i in {1..5}; do
    if check_rate_limit "test-user"; then
      echo "Request $i: OK"
    else
      echo "Request $i: BLOCKED"
    fi
  done
  
  echo "Testing command validation..."
  validate_command "ls -la" && echo "Valid: ls -la" || echo "Invalid: ls -la"
  validate_command "cat /etc/passwd; rm -rf /" && echo "Valid: malicious" || echo "Invalid: malicious"
fi
