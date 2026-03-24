#!/bin/bash
set -e

cd "$(dirname "$0")"

# Set environment
export LOG_LEVEL=DEBUG
export LOG_FORMAT=json
export PORT=0  # Let OS assign a free port

# Start server in background
node factory/server/index.js &
SERVER_PID=$!

# Wait for server to start (max 10 seconds)
for i in {1..20}; do
  sleep 0.5
  if curl -s http://localhost:3000/health >/dev/null 2>&1; then
    echo "Server is up"
    break
  fi
  if [ $i -eq 20 ]; then
    echo "Server failed to start"
    kill $SERVER_PID 2>/dev/null
    exit 1
  fi
done

# Make a request with correlation ID
echo "Making test request..."
curl -v -H "X-Request-ID: test-correlation-123" \
  -H "Content-Type: application/json" \
  -d '{"task": "hello world"}' \
  http://localhost:3000/floors/generate 2>&1 | grep -E "(< HTTP|{.*})" | head -20

# Get metrics
curl -s http://localhost:3000/metrics | jq . 2>/dev/null || cat

# Stop server
kill $SERVER_PID
wait $SERVER_PID 2>/dev/null
echo "Test completed"