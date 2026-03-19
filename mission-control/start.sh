#!/bin/bash
set -e

echo "🚀 Starting Fiesta Mission Control Dashboard..."

# Get Tailscale IP if available
TAILSCALE_IP=$(tailscale ip --4 2>/dev/null | head -1 || echo "YOUR_TAILSCALE_IP")
HOST_IP=$(hostname -I | awk '{print $1}' || echo "localhost")

cd "$(dirname "$0")"

# Install dependencies if needed
python3 -c "import requests" 2>/dev/null || {
    echo "Installing Python dependencies..."
    pip3 install requests --break-system-packages
}

# Generate initial data
python3 gather-data.py

# Check if server already running
if curl -s http://localhost:9005/ >/dev/null 2>&1; then
    echo "⚠️ Mission Control already running on port 9005"
else
    echo "Starting HTTP server on port 9005..."
    python3 server.py &
    SERVER_PID=$!
    echo $SERVER_PID > /tmp/mission-control.pid
    sleep 2
fi

echo ""
echo "✅ Mission Control Dashboard is ready!"
echo ""
echo "Access via:"
echo "   Local:      http://localhost:9005"
echo "   Network:    http://$HOST_IP:9005"
echo "   Tailscale:  http://$TAILSCALE_IP:9005"
echo ""
echo "📊 Dashboard shows:"
echo "   - System health (factory, entropy economy, payment backend)"
echo "   - Cron job status"
echo "   - Entropy agent balances"
echo "   - Git status"
echo "   - Stalled items"
echo "   - Next steps"
echo ""
echo "Data auto-refreshes every 30 seconds."
echo ""
echo "To stop: pkill -f 'python3 server.py'"
echo ""