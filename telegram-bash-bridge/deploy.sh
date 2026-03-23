#!/bin/bash
# Deploy Telegram bot infrastructure

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=== Deploying Telegram Bot Infrastructure ==="

# 1. Ensure dependencies
echo "Installing python dependencies..."
pip3 install python-telegram-bot --break-system-packages > /dev/null 2>&1 || {
    echo "Failed to install python-telegram-bot"
    exit 1
}

# 2. Setup config
echo "Configuring bot token and chat IDs..."
python3 setup.py

# 3. Install systemd service
echo "Installing systemd service..."
cp telegram-bot.service /etc/systemd/system/
systemctl daemon-reload
systemctl enable telegram-bot.service

# 4. Set environment variable from config
CONFIG=$(cat config.json)
TOKEN=$(echo "$CONFIG" | grep -o '"token": "[^"]*' | cut -d'"' -f4)
if [ -n "$TOKEN" ]; then
    # Create environment file
    ENV_FILE="/etc/default/telegram-bot"
    echo "TELEGRAM_BOT_TOKEN=$TOKEN" > "$ENV_FILE"
    chmod 600 "$ENV_FILE"
    # Update service to use environment file
    sed -i 's|Environment=TELEGRAM_BOT_TOKEN=|EnvironmentFile='"$ENV_FILE"'|' /etc/systemd/system/telegram-bot.service
    systemctl daemon-reload
fi

# 5. Start service
echo "Starting telegram-bot service..."
systemctl restart telegram-bot.service 2>/dev/null || systemctl start telegram-bot.service
sleep 2
systemctl status telegram-bot.service --no-pager -l | head -20

# 6. Add cron job for routine reports
echo "Adding cron job for daily reports..."
CRON_LINE="0 9 * * * cd $SCRIPT_DIR && python3 routine_report.py >> routine_cron.log 2>&1"
(crontab -l 2>/dev/null | grep -v "routine_report.py"; echo "$CRON_LINE") | crontab -

# 7. Test handler
echo "Testing handler..."
python3 handler.py "deploytest" "/status" 2>&1 | grep -q '"status": "ok"' && echo "✓ Handler test passed" || echo "✗ Handler test failed"

echo ""
echo "=== Deployment Complete ==="
echo "• Systemd service: telegram-bot (status: systemctl status telegram-bot)"
echo "• Daily reports: 09:00 UTC (cron)"
echo "• Config file: $SCRIPT_DIR/config.json"
echo "• Logs: journalctl -u telegram-bot -f"
echo ""
echo "To update config later, run: python3 setup.py"