#!/bin/bash

################################################################################
# GROK Startup Script — Simple, Reliable, Pure Bash
# Launches grok-simple.sh if available, then grok.sh as fallback
################################################################################

set -e

WORKSPACE="/root/.openclaw/workspace/grok-server"
PORT="${1:-8888}"
LOG="${WORKSPACE}/logs/grok.log"

mkdir -p "${WORKSPACE}/logs"

echo "================================"
echo "🚀 Grok Server Starting"
echo "================================"
echo "Port: $PORT"
echo "Workspace: $WORKSPACE"
echo "Log: $LOG"
echo ""

# Check for running instance
if pgrep -f "grok.*\.sh.*$PORT" >/dev/null 2>&1; then
    echo "⚠️  Grok already running on port $PORT"
    pgrep -f "grok.*\.sh.*$PORT" | xargs ps aux | grep -v grep
    exit 1
fi

# Start server in background
nohup bash "$WORKSPACE/grok-simple.sh" "$PORT" > "$LOG" 2>&1 &
SERVER_PID=$!

echo "✅ Grok started (PID $SERVER_PID)"
echo "   Logs: tail -f $LOG"
echo ""
echo "Test it:"
echo "  curl http://localhost:$PORT/health"
echo "  curl http://localhost:$PORT/status"
echo "  curl -X POST http://localhost:$PORT/infer -d '{\"prompt\": \"tell me about bash\"}' -H 'Content-Type: application/json'"
echo ""
echo "Stop: kill $SERVER_PID"
