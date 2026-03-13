#!/bin/bash

# Broadcast Grok & BitNet status to all Tailscale devices
# This creates a shareable status report

REPORT="/root/.openclaw/workspace/TAILSCALE_STATUS_BROADCAST.md"
TIMESTAMP=$(date -u +'%Y-%m-%d %H:%M:%S UTC')

# Verify services are running
echo "📊 Status Broadcast — $(date)"
echo ""

# Check each service
echo "Verifying services..."
echo ""

# Grok
GROK_HEALTH=$(curl -s http://localhost:8889/health)
GROK_STATUS=$(echo "$GROK_HEALTH" | python3 -c 'import sys,json; print(json.load(sys.stdin).get("status","unknown"))' 2>/dev/null || echo "offline")
echo "✅ Grok: $GROK_STATUS"

# BitNet
BITNET_HEALTH=$(curl -s http://localhost:8080/health)
BITNET_STATUS=$(echo "$BITNET_HEALTH" | python3 -c 'import sys,json; print(json.load(sys.stdin).get("status","unknown"))' 2>/dev/null || echo "offline")
echo "✅ BitNet: $BITNET_STATUS"

# Tailscale devices
echo "✅ Tailscale devices:"
sudo tailscale status 2>&1 | grep -E "^100\." | awk '{print "   - " $2 " (" $1 ")"}'

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📄 Full status report:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
cat "$REPORT"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ Status broadcast ready"
echo "   Access from iPhone: http://100.76.206.82:8889/health"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

