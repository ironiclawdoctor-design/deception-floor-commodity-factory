#!/bin/bash
# btc-monitor-cron.sh — Cron wrapper for BTC donation tracker
# Runs btc-monitor.py, announces to Telegram if new tx detected.
# Called by cron every 15 minutes.

set -euo pipefail

MONITOR="/root/.openclaw/workspace/revenue/btc-monitor.py"
LOG="/root/human/btc-monitor.log"

# Run monitor; exit code 2 = new transaction detected
python3 "$MONITOR" >> "$LOG" 2>&1
EXIT_CODE=$?

if [ "$EXIT_CODE" -eq 2 ]; then
    # New transaction — read the status JSON and announce
    STATUS=$(cat /root/human/btc-status.json 2>/dev/null || echo '{}')
    SAT=$(echo "$STATUS" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('balance_satoshi','?'))")
    USD=$(echo "$STATUS" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('balance_usd','?'))")
    TX=$(echo "$STATUS" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('last_tx_hash','?')[:16])")
    SHANNON=$(echo "$STATUS" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('shannon_minted_this_run',0))")

    # Announce via openclaw message (Telegram)
    openclaw message send \
      --channel telegram \
      --message "💰 BTC DONATION DETECTED!
Address: 12bxubgs1Br6NvKH4p35pcBpinQ7fwe4ht
Balance: ${SAT} sat (\$${USD})
Last tx: ${TX}…
Shannon minted: ${SHANNON}" 2>/dev/null || true

    echo "[btc-monitor-cron] Announcement sent." >> "$LOG"
fi

exit 0
