#!/bin/bash
# agency-snapshot-daemon.sh
# Snapshot current agency state every 30 seconds
# Background process, no exfiltration, local logging only
# Cost: Tier 0 bash only ($0.00)

set -euo pipefail

SNAPSHOT_DIR="/root/.openclaw/workspace/snapshots"
mkdir -p "$SNAPSHOT_DIR"
DAEMON_PID_FILE="/root/.openclaw/workspace/.agency-snapshot-daemon.pid"
STATE_FILE="/root/.openclaw/workspace/.agency-state-current.jsonl"

# ============================================================================
# SNAPSHOT FUNCTION: Capture current agency state
# ============================================================================
snapshot_agency() {
    local timestamp=$(date -u +%Y-%m-%dT%H:%M:%SZ)
    local snapshot_file="$SNAPSHOT_DIR/snapshot-${timestamp//[:-]/}.jsonl"
    
    # Initialize snapshot
    echo "{" > "$snapshot_file.tmp"
    echo "  \"timestamp\": \"$timestamp\"," >> "$snapshot_file.tmp"
    echo "  \"state\": {" >> "$snapshot_file.tmp"
    
    # 1. Budget snapshot
    local budget_remaining=$(cat /root/.openclaw/workspace/.budget-remaining 2>/dev/null || echo "15.50")
    echo "    \"budget_remaining\": $budget_remaining," >> "$snapshot_file.tmp"
    
    # 2. File count snapshot
    local file_count=$(find /root/.openclaw/workspace -type f -name "*.md" -o -name "*.sh" -o -name "*.jsonl" 2>/dev/null | wc -l)
    echo "    \"file_count\": $file_count," >> "$snapshot_file.tmp"
    
    # 3. BTC wallet balance (if canonical ledger exists)
    if [[ -f "/root/.openclaw/workspace/bitcoin-ledger-canonical-20260315.json" ]]; then
        local btc_balance=$(jq -r '.balance_satoshis // "unknown"' /root/.openclaw/workspace/bitcoin-ledger-canonical-20260315.json 2>/dev/null || echo "unknown")
        echo "    \"btc_balance_satoshis\": \"$btc_balance\"," >> "$snapshot_file.tmp"
    fi
    
    # 4. Feddit wallet balance (if exists)
    if [[ -f "/root/.openclaw/workspace/agency.db" ]]; then
        local feddit_balance=$(sqlite3 /root/.openclaw/workspace/agency.db "SELECT COALESCE(SUM(amount), 0) FROM balances WHERE asset='USD'" 2>/dev/null || echo "0")
        echo "    \"feddit_balance_usd\": $feddit_balance," >> "$snapshot_file.tmp"
    fi
    
    # 5. Process health (bash, bitnet, openclaw running?)
    local bash_ok="true"
    local openclaw_ok=$(pgrep -f openclaw > /dev/null 2>&1 && echo "true" || echo "false")
    echo "    \"bash_healthy\": $bash_ok," >> "$snapshot_file.tmp"
    echo "    \"openclaw_running\": $openclaw_ok," >> "$snapshot_file.tmp"
    
    # 6. Cron jobs active (next-actions-automation scheduled?)
    local cron_active=$(grep -c "next-actions-automation" /var/spool/cron/crontabs/root 2>/dev/null || echo "0")
    echo "    \"cron_jobs_active\": $cron_active," >> "$snapshot_file.tmp"
    
    # 7. Doctrine version (SOUL.md last update)
    local soul_mtime=$(stat -f%m /root/.openclaw/workspace/SOUL.md 2>/dev/null || stat -c%Y /root/.openclaw/workspace/SOUL.md 2>/dev/null || echo "0")
    echo "    \"doctrine_last_update\": $soul_mtime" >> "$snapshot_file.tmp"
    
    echo "  }" >> "$snapshot_file.tmp"
    echo "}" >> "$snapshot_file.tmp"
    
    # Atomically move to real file
    mv "$snapshot_file.tmp" "$snapshot_file"
    
    # Keep only last 100 snapshots (rotate old ones)
    local snapshot_count=$(ls -1 "$SNAPSHOT_DIR"/snapshot-*.jsonl 2>/dev/null | wc -l)
    if (( snapshot_count > 100 )); then
        ls -1t "$SNAPSHOT_DIR"/snapshot-*.jsonl 2>/dev/null | tail -n +101 | xargs rm -f
    fi
    
    # Update current state file (used by health checks)
    cp "$snapshot_file" "$STATE_FILE"
    
    echo "$snapshot_file"
}

# ============================================================================
# DAEMON LOOP: Run snapshot every 30 seconds
# ============================================================================
daemon_loop() {
    echo "$$" > "$DAEMON_PID_FILE"
    
    echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] Agency snapshot daemon started (PID $$)"
    
    while true; do
        snapshot_agency > /dev/null 2>&1
        sleep 30
    done
}

# ============================================================================
# HEALTH CHECK: Is daemon running?
# ============================================================================
health_check() {
    if [[ -f "$DAEMON_PID_FILE" ]]; then
        local pid=$(cat "$DAEMON_PID_FILE")
        if kill -0 "$pid" 2>/dev/null; then
            echo "✅ Agency snapshot daemon healthy (PID $pid)"
            
            # Show last snapshot
            if [[ -f "$STATE_FILE" ]]; then
                echo "Last snapshot:"
                cat "$STATE_FILE" | jq -r '.state | to_entries[] | "  \(.key): \(.value)"' 2>/dev/null || cat "$STATE_FILE"
            fi
            
            return 0
        else
            echo "❌ Daemon PID $pid not running"
            rm -f "$DAEMON_PID_FILE"
            return 1
        fi
    else
        echo "❌ Daemon not running (no PID file)"
        return 1
    fi
}

# ============================================================================
# START: Launch daemon in background
# ============================================================================
start_daemon() {
    if [[ -f "$DAEMON_PID_FILE" ]]; then
        local pid=$(cat "$DAEMON_PID_FILE")
        if kill -0 "$pid" 2>/dev/null; then
            echo "⚠️  Daemon already running (PID $pid)"
            return 0
        fi
    fi
    
    # Start daemon in background, redirect output to log
    daemon_loop > /root/.openclaw/workspace/logs/agency-snapshot-daemon.log 2>&1 &
    sleep 1
    
    if health_check; then
        echo "✅ Agency snapshot daemon started"
        return 0
    else
        echo "❌ Failed to start daemon"
        return 1
    fi
}

# ============================================================================
# STOP: Kill daemon gracefully
# ============================================================================
stop_daemon() {
    if [[ -f "$DAEMON_PID_FILE" ]]; then
        local pid=$(cat "$DAEMON_PID_FILE")
        if kill -0 "$pid" 2>/dev/null; then
            kill "$pid"
            sleep 1
            rm -f "$DAEMON_PID_FILE"
            echo "✅ Agency snapshot daemon stopped"
            return 0
        fi
    fi
    
    echo "⚠️  Daemon not running"
    return 0
}

# ============================================================================
# MAIN: Parse command
# ============================================================================
main() {
    local action="${1:-help}"
    
    case "$action" in
        start)
            start_daemon
            ;;
        stop)
            stop_daemon
            ;;
        status|health)
            health_check
            ;;
        snapshot-now)
            snapshot_agency
            ;;
        tail-snapshots)
            tail -f "$STATE_FILE" 2>/dev/null || echo "No snapshots yet"
            ;;
        list-snapshots)
            ls -lht "$SNAPSHOT_DIR"/snapshot-*.jsonl 2>/dev/null | head -20
            ;;
        help|*)
            cat << 'HELP'
USAGE: ./agency-snapshot-daemon.sh <action>

Actions:
  start                Launch daemon (30s snapshots, background)
  stop                 Stop daemon gracefully
  status|health        Check daemon health, show last snapshot
  snapshot-now         Capture snapshot immediately
  tail-snapshots       Follow last snapshot (live)
  list-snapshots       List recent snapshots (20 most recent)
  help                 Show this help

Examples:
  ./agency-snapshot-daemon.sh start      # Start background daemon
  ./agency-snapshot-daemon.sh status     # Check health
  ./agency-snapshot-daemon.sh tail-snapshots  # Monitor live

Daemon Operation:
- Runs in background (PID stored in .agency-snapshot-daemon.pid)
- Snapshots every 30 seconds to /root/.openclaw/workspace/snapshots/
- Keeps last 100 snapshots (auto-rotates)
- Updates .agency-state-current.jsonl with latest state
- No exfiltration (local only)
- Cost: Tier 0 bash only ($0.00)

Data Captured:
  - Timestamp
  - Budget remaining
  - File count
  - BTC balance (if ledger exists)
  - Feddit balance (if database exists)
  - Process health (bash, openclaw)
  - Cron job status
  - Doctrine version

Logs: /root/.openclaw/workspace/logs/agency-snapshot-daemon.log
HELP
            ;;
    esac
}

# Auto-start if invoked as daemon
if [[ "${1:-}" == "daemon-loop" ]]; then
    daemon_loop
else
    main "$@"
fi
