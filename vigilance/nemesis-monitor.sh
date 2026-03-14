#!/bin/bash
# Nemesis Forensic Vigilance Monitor
# Continuous monitoring of three branches: Automate, Official, Daimyo

VIGILANCE_DIR="/root/.openclaw/workspace/vigilance"
FORENSIC_LOG="${VIGILANCE_DIR}/nemesis-forensic-$(date -u +%Y%m%dT%H%M%SZ).jsonl"
STATE_FILE="${VIGILANCE_DIR}/vigilance-state.json"
CHECK_INTERVAL=60  # seconds

# Initialize forensic log
mkdir -p "$VIGILANCE_DIR"

# Function: Log event
log_event() {
    local event="$1"
    local data="$2"
    local severity="${3:-info}"
    echo "{\"timestamp\":\"$(date -u +%Y-%m-%dT%H:%M:%SZ)\",\"event\":\"$event\",\"severity\":\"$severity\",\"data\":$data}" >> "$FORENSIC_LOG"
}

# Function: Check branch health
check_branch() {
    local branch="$1"
    case "$branch" in
        "Automate")
            if [ -f "/root/.openclaw/workspace/automate-nbm/config/automate.yml" ]; then
                echo "operational"
            fi
            ;;
        "Official")
            if tail -1 /root/.openclaw/workspace/commodity-production/floors-*.jsonl 2>/dev/null | grep -q "shipped"; then
                echo "operational"
            fi
            ;;
        "Daimyo")
            if [ -d "/root/.openclaw/workspace/audit-logs" ]; then
                echo "operational"
            fi
            ;;
    esac
}

# Continuous monitoring loop
while true; do
    ISO_TIME=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
    
    # Monitor external API calls
    EXTERNAL_CALLS=$(grep "external_calls" "$STATE_FILE" 2>/dev/null | grep -o '[0-9]\+' | tail -1)
    if [ "$EXTERNAL_CALLS" -gt 3 ]; then
        log_event "threshold_exceeded" "{\"type\":\"external_calls\",\"value\":$EXTERNAL_CALLS,\"threshold\":3}" "alert"
    fi
    
    # Check branch status
    for branch in "Automate" "Official" "Daimyo"; do
        status=$(check_branch "$branch")
        if [ -z "$status" ]; then
            log_event "branch_degraded" "{\"branch\":\"$branch\",\"status\":\"degraded\"}" "warning"
        else
            log_event "branch_check" "{\"branch\":\"$branch\",\"status\":\"$status\"}" "info"
        fi
    done
    
    # Check for token bleed
    if grep -q "tokens" "$FORENSIC_LOG" 2>/dev/null; then
        BLEED_SCORE=$(grep "tokens" "$FORENSIC_LOG" | wc -l)
        if [ "$BLEED_SCORE" -gt 10 ]; then
            log_event "token_bleed_alert" "{\"events\":$BLEED_SCORE}" "warning"
        fi
    fi
    
    sleep "$CHECK_INTERVAL"
done
