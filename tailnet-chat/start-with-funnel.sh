#!/bin/bash
# TailChat + Tailscale Funnel
# Makes TailChat publicly accessible via https://<hostname>.ts.net
# Run on grok-fortress (the linux Ampere.sh server)

set -e

CHAT_PORT=8765
FUNNEL_PORT=443

echo "=== TailChat Funnel Setup ==="
echo "Step 1: Start TailChat server..."
python3 /root/.openclaw/workspace/tailnet-chat/server.py --port $CHAT_PORT &
CHAT_PID=$!
echo "TailChat running (PID $CHAT_PID) on port $CHAT_PORT"

sleep 2

echo ""
echo "Step 2: Enable Tailscale Funnel..."
# Funnel routes public HTTPS → local TailChat
tailscale funnel --bg $CHAT_PORT

echo ""
echo "Step 3: Check Funnel status..."
tailscale funnel status

echo ""
echo "=== TailChat is now PUBLIC ==="
echo "URL: https://$(tailscale status --json | python3 -c "import sys,json; d=json.load(sys.stdin); print(d['Self']['DNSName'].rstrip('.'))")"
echo ""
echo "Anyone on the internet can reach TailChat."
echo "Tailnet peers get direct access."
echo "Agency agents POST to /message as usual."
echo ""
echo "To stop funnel: tailscale funnel --bg off"
echo "To stop chat:   kill $CHAT_PID"
