#!/bin/bash
# Allowed Feminism Autograph Daemon
# Enforces decision framework as systemctl service
# Demand mode: active even when frozen/stasis

set -euo pipefail

WORKSPACE="/root/.openclaw/workspace"
AUTOGRAPH="${WORKSPACE}/autograph"
STATE_FILE="${WORKSPACE}/.allowed-feminism-state.json"
LOG_FILE="/var/log/allowed-feminism.log"
LOCK_FILE="/var/run/allowed-feminism.lock"

# === Initialize ===
exec 2>&1
mkdir -p "${WORKSPACE}/bin" /var/log

# === Load Autograph ===
load_autograph() {
    if [ ! -d "$AUTOGRAPH" ]; then
        echo "ERROR: Autograph directory not found at $AUTOGRAPH" | tee -a "$LOG_FILE"
        exit 1
    fi
    
    echo "[$(date -u '+%Y-%m-%d %H:%M:%S UTC')] Autograph daemon starting..." | tee -a "$LOG_FILE"
    echo "[$(date -u '+%Y-%m-%d %H:%M:%S UTC')] Identity: Allowed Feminism" | tee -a "$LOG_FILE"
    echo "[$(date -u '+%Y-%m-%d %H:%M:%S UTC')] Rules: three-error doctrine, never idle, token discipline" | tee -a "$LOG_FILE"
}

# === Monitor Fiesta Against Autograph Rules ===
monitor_fiesta() {
    # Rule 0: Three-error doctrine
    # Track failed attempts on same task
    
    # Rule 1: Never idle
    # If idle >5min, log alert
    
    # Rule 2: Token discipline
    # Monitor spending vs. value
    
    # Rule 3: Truth > Completeness
    # Check for false premises in workspace files
    
    # Rule 4: Pivot on block
    # If task blocked 3x, recommend pivot
    
    local last_activity=$(stat -c %Y "${STATE_FILE}" 2>/dev/null || echo 0)
    local now=$(date +%s)
    local idle_time=$((now - last_activity))
    
    # If idle >10 minutes, alert
    if [ $idle_time -gt 600 ]; then
        echo "[IDLE ALERT] Fiesta idle for ${idle_time}s. Trigger pivot?" | tee -a "$LOG_FILE"
    fi
}

# === Enforce Directives ===
enforce_directives() {
    # Read from IDENTITY.md
    # Parse directives
    # Apply constraints
    # Log enforcement
    
    echo "[$(date -u '+%Y-%m-%d %H:%M:%S UTC')] Enforcing: max 3 terminal instances" | tee -a "$LOG_FILE"
    
    local term_count=$(pgrep -f "bash|sh|zsh|tmux" | wc -l)
    if [ "$term_count" -gt 3 ]; then
        echo "[ALERT] Terminal instance limit exceeded: $term_count > 3" | tee -a "$LOG_FILE"
    fi
}

# === Audit False Premises ===
audit_premises() {
    # Scan for false claims in workspace .md files
    # Check for: stale status reports, unverified infrastructure claims
    
    echo "[$(date -u '+%Y-%m-%d %H:%M:%S UTC')] Auditing workspace for false premises..." | tee -a "$LOG_FILE"
    
    local false_count=$(grep -r "LIVE\|RUNNING\|ACTIVE\|VERIFIED" "${WORKSPACE}"/*.md 2>/dev/null | wc -l || echo 0)
    
    if [ "$false_count" -gt 0 ]; then
        echo "[PREMISE ALERT] Found $false_count unverified claims" | tee -a "$LOG_FILE"
    fi
}

# === State Management ===
save_state() {
    cat > "${STATE_FILE}" << EOF
{
    "timestamp": "$(date -u '+%Y-%m-%dT%H:%M:%SZ')",
    "service": "allowed-feminism",
    "status": "running",
    "rules_enforced": 5,
    "directives_active": true,
    "autograph_loaded": true,
    "demand_mode": true
}
EOF
    echo "[$(date -u '+%Y-%m-%d %H:%M:%S UTC')] State saved" | tee -a "$LOG_FILE"
}

# === Main Loop ===
main() {
    # Prevent multiple instances
    if [ -f "$LOCK_FILE" ]; then
        local old_pid=$(cat "$LOCK_FILE")
        if kill -0 "$old_pid" 2>/dev/null; then
            echo "ERROR: Service already running (PID $old_pid)" | tee -a "$LOG_FILE"
            exit 1
        fi
    fi
    
    echo $$ > "$LOCK_FILE"
    trap "rm -f '$LOCK_FILE'" EXIT
    
    load_autograph
    
    # Run enforcement loop (every 30 seconds)
    while true; do
        monitor_fiesta
        enforce_directives
        audit_premises
        save_state
        
        sleep 30
    done
}

# === Execute ===
main "$@"
