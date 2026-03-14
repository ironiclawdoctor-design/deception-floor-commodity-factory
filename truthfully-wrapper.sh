#!/bin/bash
# Truthfully autonomous agent wrapper
# Runs as background service, manages work queue, reports earnings

LOG="/var/log/truthfully.log"
WALLET_FILE="/root/.openclaw/workspace/.truthfully-wallet"
EARNINGS_FILE="/root/.openclaw/workspace/.truthfully-earnings"
TASKS_FILE="/root/.openclaw/workspace/.truthfully-tasks"

# Initialize
touch "$EARNINGS_FILE" "$TASKS_FILE"

case "${1:-status}" in
  start)
    sudo systemctl start truthfully
    echo "✓ Truthfully started (port 3777)"
    ;;
  
  stop)
    sudo systemctl stop truthfully
    echo "✓ Truthfully stopped"
    ;;
  
  status)
    if sudo systemctl is-active truthfully > /dev/null 2>&1; then
      echo "✓ Truthfully running (port 3777)"
      echo ""
      echo "Dashboard: http://localhost:3777"
      echo "Earnings: $(tail -1 "$EARNINGS_FILE" 2>/dev/null || echo '$0.00')"
      echo "Tasks completed: $(wc -l < "$TASKS_FILE" 2>/dev/null || echo 0)"
      echo ""
      echo "Recent activity:"
      tail -5 "$LOG" 2>/dev/null || echo "No activity yet"
    else
      echo "✗ Truthfully not running"
    fi
    ;;
  
  logs)
    tail -50 "$LOG"
    ;;
  
  earnings)
    echo "Truthfully Earnings Report"
    echo "========================"
    tail -20 "$EARNINGS_FILE" 2>/dev/null || echo "No earnings yet"
    ;;
  
  *)
    echo "Usage: truthfully-wrapper.sh {start|stop|status|logs|earnings}"
    exit 1
    ;;
esac
