#!/bin/bash

# Grok Server Launcher — Simple, bulletproof
# Uses nc (netcat) to listen on port, pipes to handler.sh

PORT="${1:-8888}"
WORKSPACE="/root/.openclaw/workspace/grok-server"
HANDLER="$WORKSPACE/handler.sh"
LOGDIR="$WORKSPACE/logs"

mkdir -p "$LOGDIR"

# Make handler executable
chmod +x "$HANDLER"

echo "[$(date)] Starting Grok on port $PORT (PID $$)" | tee -a "$LOGDIR/server.log"
echo $$ > "$WORKSPACE/grok.pid"

# Listen and forward to handler
# -k means keep listening after connection
while true; do
    (
        timeout 30 nc -l -p "$PORT" -q 1 | "$HANDLER"
    ) >> "$LOGDIR/requests.log" 2>&1 &
    
    # Avoid CPU spin
    sleep 0.1
done
