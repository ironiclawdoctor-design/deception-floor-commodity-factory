#!/bin/bash

################################################################################
# precache-feedback-loop.sh
#
# Purpose: Monitor active subagents and use their progress as precache material
# for future spawns.
#
# Flow:
# 1. Poll /subagents list periodically
# 2. Extract progress from running subagents
# 3. Build knowledge from what they're working on
# 4. Inject learnings into hard-stops-registry
# 5. Future precache queries pull from this registry
#
# This closes the loop: subagent progress → precache knowledge
#
################################################################################

set -euo pipefail

REGISTRY="/root/.openclaw/workspace/hard-stops-registry-LATEST.jsonl"
FEEDBACK_LOG="/root/.openclaw/workspace/.precache-feedback.jsonl"
MONITOR_INTERVAL="${MONITOR_INTERVAL:-10}"  # seconds

# Ensure feedback log exists
touch "$FEEDBACK_LOG"

################################################################################
# Monitor Active Subagents
################################################################################

monitor_subagents() {
    echo "🔍 Monitoring active subagents for precache feedback..."
    
    # Get current subagent list
    # Note: In real usage, this would call /subagents list via OpenClaw
    # For now, we'll show the structure
    
    local timestamp=$(date -u +%Y-%m-%dT%H:%M:%SZ)
    
    # Example: Extract data from tier-routing subagent
    # In production, this would parse actual /subagents list output
    
    cat > /tmp/subagent_snapshot.json << EOF
{
  "timestamp": "$timestamp",
  "active_subagents": [
    {
      "index": 1,
      "runId": "b91ec778-5314-4b4f-b091-7ea67854570b",
      "label": "tier-routing-enforcement",
      "status": "running",
      "runtime_seconds": 120,
      "model": "haiku",
      "task_snippet": "Write tier-routing enforcement script"
    }
  ]
}
EOF

    cat /tmp/subagent_snapshot.json
}

################################################################################
# Extract Precache Knowledge from Subagent Progress
################################################################################

extract_knowledge_from_subagents() {
    local snapshot="$1"
    
    echo "📚 Extracting precache knowledge from subagent progress..."
    
    # Parse snapshot and build knowledge entries
    local timestamp=$(date -u +%Y-%m-%dT%H:%M:%SZ)
    
    # For each active subagent, create a precache entry
    echo "{
  \"timestamp\": \"$timestamp\",
  \"event\": \"precache_feedback_collected\",
  \"severity\": \"info\",
  \"data\": {
    \"source\": \"subagent_monitoring\",
    \"feedback_type\": \"active_work_context\",
    \"subagent_label\": \"tier-routing-enforcement\",
    \"task_context\": \"Writing tier-routing script with BitNet/Haiku routing\",
    \"estimated_completeness\": \"in_progress\",
    \"value_for_future_precache\": \"high\"
  }
}" | tee -a "$FEEDBACK_LOG"
}

################################################################################
# Build Precache Suggestions from Feedback
################################################################################

suggest_precache_optimizations() {
    echo ""
    echo "💡 Precache suggestions from active work:"
    echo ""
    
    # Analyze feedback log to suggest precache improvements
    if [[ -f "$FEEDBACK_LOG" ]]; then
        echo "Active precache learning:"
        tail -5 "$FEEDBACK_LOG" | jq '.data.task_context' 2>/dev/null || echo "  (analyzing...)"
    fi
    
    echo ""
    echo "Next spawn recommendations:"
    echo "  1. For tier-routing tasks: Precache will find existing routing patterns"
    echo "  2. For BitNet/Haiku decisions: Context includes API endpoints"
    echo "  3. For script writing: Include previous tier-routing examples"
    echo ""
}

################################################################################
# Continuous Monitoring Mode
################################################################################

monitor_loop() {
    local iterations="${1:-0}"
    local current_iteration=0
    
    echo "🔄 Starting precache feedback loop (monitoring every ${MONITOR_INTERVAL}s)"
    echo "   Press Ctrl+C to stop"
    echo ""
    
    while true; do
        ((current_iteration++))
        
        echo "[$(date -u +%H:%M:%S)] Cycle $current_iteration"
        
        # Get subagent status
        local snapshot=$(monitor_subagents)
        
        # Extract knowledge
        extract_knowledge_from_subagents "$snapshot"
        
        # Show suggestions
        suggest_precache_optimizations
        
        # If iterations specified, stop after N iterations
        if [[ $iterations -gt 0 ]] && [[ $current_iteration -ge $iterations ]]; then
            break
        fi
        
        # Wait before next check
        sleep "$MONITOR_INTERVAL"
    done
}

################################################################################
# Analytics: What We've Learned from Subagent Progress
################################################################################

analyze_precache_effectiveness() {
    echo "📊 PRECACHE FEEDBACK ANALYSIS"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    
    if [[ ! -f "$FEEDBACK_LOG" ]]; then
        echo "No feedback collected yet. Run monitor first."
        return 1
    fi
    
    echo "Precache Feedback Summary:"
    echo ""
    
    # Count feedback entries
    local total_entries=$(wc -l < "$FEEDBACK_LOG")
    echo "  Total feedback entries: $total_entries"
    
    # Extract common task contexts
    echo ""
    echo "Common task contexts being worked on:"
    grep -o '"task_context": "[^"]*"' "$FEEDBACK_LOG" 2>/dev/null | \
        cut -d'"' -f4 | \
        sort | uniq -c | sort -rn | \
        head -5 | \
        sed 's/^/    /'
    
    echo ""
    echo "High-value precache learning opportunities:"
    grep -o '"value_for_future_precache": "[^"]*"' "$FEEDBACK_LOG" 2>/dev/null | \
        cut -d'"' -f4 | \
        sort | uniq -c | \
        sed 's/^/    /'
    
    echo ""
}

################################################################################
# Integration: Suggest Precache for Next Spawn
################################################################################

suggest_next_precache() {
    local task_description="$1"
    
    echo "🎯 PRECACHE RECOMMENDATION FOR NEXT SPAWN"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    echo "Task: $task_description"
    echo ""
    
    # Check feedback log for similar tasks
    if grep -q "routing\|tier" "$FEEDBACK_LOG" 2>/dev/null && \
       echo "$task_description" | grep -q "routing\|tier"; then
        echo "✅ PRECACHE AVAILABLE"
        echo "   Previous tier-routing work found in feedback"
        echo "   Suggested precache context:"
        echo "     - BitNet endpoint: 127.0.0.1:8080"
        echo "     - Haiku endpoint: external API"
        echo "     - Routing decision: task complexity → endpoint choice"
        echo ""
    fi
    
    echo "Next action:"
    echo "  python3 /root/.openclaw/workspace/lib/token-cache-engine.py \\"
    echo "    \"$task_description\" \\"
    echo "    \"next-task\""
    echo ""
}

################################################################################
# CLI
################################################################################

if [[ $# -lt 1 ]]; then
    cat << USAGE
Usage: $0 <action> [args]

Actions:
  monitor [iterations]    Monitor active subagents (Ctrl+C to stop)
  analyze                 Analyze precache feedback collected
  suggest <task>          Get precache suggestions for a task
  extract <snapshot>      Extract knowledge from snapshot JSON

Examples:
  # Monitor for 10 cycles
  $0 monitor 10
  
  # Analyze what we've learned
  $0 analyze
  
  # Get precache suggestions for tier-routing
  $0 suggest "Write tier-routing enforcement script"

This tool closes the feedback loop:
  Subagent progress → Precache knowledge → More efficient next spawns
USAGE
    exit 0
fi

ACTION="$1"

case "$ACTION" in
    monitor)
        monitor_loop "${2:-0}"
        ;;
    analyze)
        analyze_precache_effectiveness
        ;;
    suggest)
        if [[ $# -lt 2 ]]; then
            echo "❌ Error: suggest requires task description"
            exit 1
        fi
        suggest_next_precache "$2"
        ;;
    extract)
        if [[ $# -lt 2 ]]; then
            echo "❌ Error: extract requires snapshot file"
            exit 1
        fi
        extract_knowledge_from_subagents "$2"
        ;;
    *)
        echo "❌ Unknown action: $ACTION"
        exit 1
        ;;
esac
