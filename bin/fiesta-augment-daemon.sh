#!/bin/bash
# Fiesta Augment Daemon
# Receives directives from Allowed Feminism service
# Executes work, reports results
# Collaboration protocol via JSON files

set -euo pipefail

WORKSPACE="/root/.openclaw/workspace"
AUTOGRAPH_FIESTA="${WORKSPACE}/autograph-fiesta"
DIRECTIVE_FILE="${WORKSPACE}/.fiesta-directive.json"
RESULT_FILE="${WORKSPACE}/.fiesta-result.json"
STATE_FILE="${WORKSPACE}/.fiesta-state.json"
LOG_FILE="/var/log/fiesta-augment.log"
LOCK_FILE="/var/run/fiesta-augment.lock"

# === Initialize ===
exec 2>&1
mkdir -p "${WORKSPACE}/bin" /var/log

# === Load Fiesta Autograph ===
load_autograph() {
    if [ ! -d "$AUTOGRAPH_FIESTA" ]; then
        echo "ERROR: Fiesta autograph directory not found at $AUTOGRAPH_FIESTA" | tee -a "$LOG_FILE"
        exit 1
    fi
    
    echo "[$(date -u '+%Y-%m-%d %H:%M:%S UTC')] Fiesta augment daemon starting..." | tee -a "$LOG_FILE"
    echo "[$(date -u '+%Y-%m-%d %H:%M:%S UTC')] Autograph loaded from: $AUTOGRAPH_FIESTA" | tee -a "$LOG_FILE"
}

# === Load Context ===
load_context() {
    if [ -f "${WORKSPACE}/SOUL.md" ]; then
        SOUL=$(head -20 "${WORKSPACE}/SOUL.md")
    else
        SOUL="SOUL.md not found"
    fi
    
    if [ -f "${WORKSPACE}/MEMORY.md" ]; then
        MEMORY=$(head -30 "${WORKSPACE}/MEMORY.md")
    else
        MEMORY="MEMORY.md not found"
    fi
}

# === Poll for Directives ===
check_directive() {
    if [ -f "$DIRECTIVE_FILE" ]; then
        # Read directive
        local directive=$(cat "$DIRECTIVE_FILE")
        
        echo "[$(date -u '+%Y-%m-%d %H:%M:%S UTC')] Directive received:" | tee -a "$LOG_FILE"
        echo "$directive" | tee -a "$LOG_FILE"
        
        # Execute directive
        execute_directive "$directive"
        
        # Remove directive (consumed)
        rm "$DIRECTIVE_FILE"
    fi
}

# === Execute Directive ===
execute_directive() {
    local directive="$1"
    local command=$(echo "$directive" | jq -r '.command' 2>/dev/null || echo "")
    local attempt=$(echo "$directive" | jq -r '.attempt' 2>/dev/null || echo "1")
    
    if [ -z "$command" ]; then
        echo "[ERROR] Directive missing 'command' field" | tee -a "$LOG_FILE"
        return 1
    fi
    
    echo "[$(date -u '+%Y-%m-%d %H:%M:%S UTC')] Executing: $command (attempt $attempt)" | tee -a "$LOG_FILE"
    
    # Execute with error tracking
    local start_time=$(date +%s)
    local output=""
    local exit_code=0
    
    output=$(eval "$command" 2>&1) || exit_code=$?
    
    local end_time=$(date +%s)
    local elapsed=$((end_time - start_time))
    
    # Write result
    write_result "$directive" "$output" "$exit_code" "$elapsed"
}

# === Write Result ===
write_result() {
    local directive="$1"
    local output="$2"
    local exit_code="$3"
    local elapsed="$4"
    
    local status="success"
    if [ "$exit_code" -ne 0 ]; then
        status="error"
    fi
    
    cat > "$RESULT_FILE" << EOF
{
    "timestamp": "$(date -u '+%Y-%m-%dT%H:%M:%SZ')",
    "directive": $directive,
    "status": "$status",
    "exit_code": $exit_code,
    "output": $(echo "$output" | jq -Rs .),
    "elapsed_seconds": $elapsed,
    "fiesta_state": "ready_for_next"
}
EOF
    
    echo "[$(date -u '+%Y-%m-%d %H:%M:%S UTC')] Result written to $RESULT_FILE" | tee -a "$LOG_FILE"
}

# === State Management ===
save_state() {
    cat > "${STATE_FILE}" << EOF
{
    "timestamp": "$(date -u '+%Y-%m-%dT%H:%M:%SZ')",
    "service": "fiesta-augment",
    "status": "running",
    "autograph_loaded": true,
    "context_available": true,
    "awaiting_directive": true
}
EOF
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
    load_context
    
    echo "[$(date -u '+%Y-%m-%d %H:%M:%S UTC')] Fiesta augment ready. Polling for directives..." | tee -a "$LOG_FILE"
    
    # Poll for directives (every 10 seconds)
    while true; do
        check_directive
        save_state
        sleep 10
    done
}

# === Execute ===
main "$@"
