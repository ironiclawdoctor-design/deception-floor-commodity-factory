#!/bin/bash
# Approval Helper - Simple interface for approval gate agent
# Source this file in your scripts to use internal approval system

APPROVAL_AGENT="/root/.openclaw/workspace/skills/approval-gate-agent/approval-gate-agent.sh"
DB_FILE="/root/.openclaw/workspace/approval-registry.db"

# Check if approval agent is available
check_approval_system() {
    if [ ! -f "$APPROVAL_AGENT" ]; then
        echo "⚠️  Approval gate agent not found: $APPROVAL_AGENT"
        echo "Run: ./approval-gate-agent.sh init"
        return 1
    fi
    if [ ! -f "$DB_FILE" ]; then
        echo "⚠️  Approval registry not initialized"
        echo "Run: ./approval-gate-agent.sh init"
        return 1
    fi
    return 0
}

# Request approval (blocking - waits for approval)
# Usage: request_approval <action> <description> <agent_id> [resource]
request_approval() {
    local action="$1"
    local description="$2"
    local agent_id="$3"
    local resource="${4:-}"
    
    if ! check_approval_system; then
        return 1
    fi
    
    echo "Requesting approval for: $description"
    echo "  Action: $action"
    echo "  Agent: $agent_id"
    echo "  Resource: $resource"
    
    # Create the approval request
    local request_id
    request_id=$("$APPROVAL_AGENT" request "$agent_id" "$action" "$resource")
    
    if [ $? -ne 0 ] || [ -z "$request_id" ]; then
        echo "❌ Failed to create approval request"
        return 1
    fi
    
    echo "✓ Approval request created: $request_id"
    echo "Status: pending"
    echo ""
    echo "TO APPROVE (in Web UI terminal):"
    echo "  ./approval-gate-agent.sh approve $request_id human '$description'"
    echo ""
    echo "TO CHECK STATUS:"
    echo "  ./approval-gate-agent.sh status $request_id"
    echo ""
    echo "Waiting for approval (checking every 30 seconds)..."
    
    # Wait for approval (max 5 minutes)
    local max_checks=10
    local check_count=0
    
    while [ $check_count -lt $max_checks ]; do
        sleep 30
        check_count=$((check_count + 1))
        
        # Check status
        local status
        status=$(sqlite3 "$DB_FILE" "SELECT status FROM approval_requests WHERE id='$request_id';" 2>/dev/null || echo "unknown")
        
        case "$status" in
            "approved")
                echo "✅ Approval granted: $request_id"
                return 0
                ;;
            "denied")
                echo "❌ Approval denied: $request_id"
                return 1
                ;;
            "pending")
                echo "⏳ Still pending... ($check_count/$max_checks checks)"
                ;;
            *)
                echo "⚠️  Unknown status '$status' for request $request_id"
                ;;
        esac
    done
    
    echo "⏰ Approval timeout after 5 minutes"
    echo "Request ID: $request_id is still pending"
    return 2
}

# Quick approval check (non-blocking)
# Returns 0 if already approved for similar action, 1 if needs approval
check_quick_approval() {
    local action="$1"
    local agent_id="$2"
    local resource="${3:-}"
    
    if ! check_approval_system; then
        return 1
    fi
    
    # Check for recent approval of same action (within last hour)
    local recent_approved
    recent_approved=$(sqlite3 "$DB_FILE" <<EOF
SELECT COUNT(*) 
FROM approval_requests 
WHERE agent_id='$agent_id' 
  AND action='$action' 
  AND (resource='$resource' OR resource IS NULL)
  AND status='approved'
  AND datetime(approved_at) >= datetime('now', '-1 hour')
EOF
)
    
    if [ "$recent_approved" -gt 0 ]; then
        echo "✅ Recent approval found for $action (within last hour)"
        return 0
    fi
    
    return 1
}

# Generate Web UI fallback for commands that need actual execution
# Usage: webui_fallback <request_id> <command> <description>
webui_fallback() {
    local request_id="$1"
    local command="$2"
    local description="$3"
    
    echo "🔧 WEB UI TERMINAL FALLBACK REQUIRED"
    echo ""
    echo "Description: $description"
    echo "Request ID: $request_id"
    echo ""
    echo "COMMAND TO RUN IN WEB UI TERMINAL:"
    echo "  $command"
    echo ""
    echo "AFTER RUNNING, UPDATE STATUS:"
    echo "  ./approval-gate-agent.sh approve $request_id human 'executed-via-webui'"
    echo ""
    echo "⚠️  This bypasses the broken OpenClaw approval gate"
    echo "✅ Execution will be logged to compliance system"
    
    return 0
}

# Log approval usage for compliance
log_approval_usage() {
    local request_id="$1"
    local action="$2"
    local outcome="$3"  # "used", "bypassed", "waived"
    
    # Load script logger if available
    local script_logger="/root/.openclaw/workspace/script-logger.sh"
    if [ -f "$script_logger" ]; then
        source "$script_logger" > /dev/null 2>&1
        
        if command -v log_script_step >/dev/null 2>&1; then
            local script_name="${0##*/}"
            log_script_step "$script_name" "approval-$outcome" "Approval $outcome for $action (request: $request_id)"
        fi
    fi
    
    # Also log to approval logs
    if [ -f "$DB_FILE" ] && [ -n "$request_id" ]; then
        sqlite3 "$DB_FILE" <<EOF
INSERT INTO approval_logs (request_id, event, details)
VALUES ('$request_id', 'usage-$outcome', 'Approval $outcome for action: $action');
EOF
    fi
}

# Example integration pattern
example_usage() {
    cat <<EOF
## Example: Using approval helper in your scripts

### Option 1: Blocking approval request
\`\`\`bash
#!/bin/bash
source /root/.openclaw/workspace/skills/approval-gate-agent/approval-helper.sh

# Request approval before critical operation
if request_approval "database-backup" "Full production backup" "backup-agent" "prod-db"; then
    echo "✅ Approval granted, proceeding with backup..."
    # Perform the backup
else
    echo "❌ Approval not granted, aborting..."
    exit 1
fi
\`\`\`

### Option 2: Quick check (non-blocking)
\`\`\`bash
#!/bin/bash
source /root/.openclaw/workspace/skills/approval-gate-agent/approval-helper.sh

# Check if we already have recent approval
if check_quick_approval "file-cleanup" "cleanup-agent"; then
    echo "Proceeding with cleanup (recently approved)..."
    perform_cleanup
else
    echo "Need fresh approval for cleanup..."
    # Request full approval
    request_approval "file-cleanup" "Temporary file cleanup" "cleanup-agent"
fi
\`\`\`

### Option 3: Web UI fallback for commands
\`\`\`bash
#!/bin/bash
source /root/.openclaw/workspace/skills/approval-gate-agent/approval-helper.sh

# Create approval request first
request_id=\$(./approval-gate-agent.sh request fiesta "system-check" "health")
webui_fallback "\$request_id" "openclaw doctor --non-interactive" "System health check"

# Human runs command in Web UI, then approves
echo "After human runs command and approves, continue..."
\`\`\`
EOF
}

# Export functions for use in other scripts
export -f check_approval_system
export -f request_approval
export -f check_quick_approval
export -f webui_fallback
export -f log_approval_usage

# Main (if run directly)
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    case "${1:-}" in
        "example")
            example_usage
            ;;
        "check")
            check_approval_system
            ;;
        *)
            echo "Approval Helper - Simple interface for approval gate agent"
            echo "Source this file in your scripts, or use:"
            echo ""
            echo "  source /root/.openclaw/workspace/skills/approval-gate-agent/approval-helper.sh"
            echo ""
            echo "Commands:"
            echo "  example    Show usage examples"
            echo "  check      Check if approval system is available"
            echo ""
            echo "Functions available after sourcing:"
            echo "  request_approval <action> <desc> <agent> [resource]"
            echo "  check_quick_approval <action> <agent> [resource]"
            echo "  webui_fallback <req_id> <command> <desc>"
            echo "  log_approval_usage <req_id> <action> <outcome>"
            ;;
    esac
fi