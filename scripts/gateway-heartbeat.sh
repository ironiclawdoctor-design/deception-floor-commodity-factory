#!/bin/bash
STATUS=$(curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:18789/health)
if [ "$STATUS" != "200" ]; then
    echo "$(date) - GATEWAY UNREACHABLE: $STATUS" >> /root/.openclaw/workspace/logs/anomalies.log
else
    # Update Dashboard
    echo "<h3>System Heartbeat: OK - $(date)</h3>" >> /root/.openclaw/workspace/www/victory.html
fi
