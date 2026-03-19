#!/bin/bash
echo "Stopping Mission Control Dashboard..."
pkill -f "python3 server.py" 2>/dev/null || true
rm -f /tmp/mission-control.pid
echo "Stopped."