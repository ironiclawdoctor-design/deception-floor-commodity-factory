#!/bin/bash

################################################################################
# tier-routing-integration-example.sh
#
# Example: How to integrate tier-routing-enforcement.sh into your production
# Official loop for cost-conscious request handling.
#
# This shows how to:
# 1. Accept user input/task
# 2. Route through tier-routing-enforcement
# 3. Process the response
# 4. Track costs and metrics
#
################################################################################

set -e

ROUTING_SCRIPT="/root/.openclaw/workspace/tier-routing-enforcement.sh"
METRICS_FILE="/root/.openclaw/workspace/tier-routing-metrics-$(date +%Y%m%d).jsonl"

################################################################################
# Example 1: Simple Integration
################################################################################

example_simple_request() {
    echo "=== Example 1: Simple Request Routing ==="
    
    local task="What is the capital of France?"
    local prompt="Answer the question: What is the capital of France?"
    
    echo "Task: $task"
    echo ""
    
    # Run through tier-routing
    local output=$($ROUTING_SCRIPT --task "$task" --prompt "$prompt" 2>&1)
    
    # Extract model and cost from output
    local model=$(echo "$output" | grep "Model:" | awk '{print $2}')
    local cost=$(echo "$output" | grep "Cost:" | awk '{print $2}')
    local response=$(echo "$output" | tail -1)
    
    echo "Routed to: $model"
    echo "Cost: $cost"
    echo "Response: $response"
    echo ""
}

################################################################################
# Example 2: Batch Processing with Cost Tracking
################################################################################

example_batch_processing() {
    echo "=== Example 2: Batch Processing with Metrics ==="
    
    local tasks=(
        "What is 2+2?|Calculate: 2 + 2"
        "Write a haiku|Write a poem about spring"
        "List files in bash|Create a bash function to list files"
        "Explain machine learning|Provide a detailed explanation of machine learning algorithms"
    )
    
    local total_cost=0
    local bitnet_count=0
    local haiku_count=0
    
    for task_pair in "${tasks[@]}"; do
        IFS='|' read -r task prompt <<< "$task_pair"
        
        # Route and capture metrics
        local output=$($ROUTING_SCRIPT --task "$task" --prompt "$prompt" 2>&1)
        local model=$(echo "$output" | grep "Model:" | awk '{print $2}')
        local cost=$(echo "$output" | grep "Cost:" | sed 's/\$//' | awk '{print $2}')
        
        echo "Task: $task"
        echo "  → Model: $model, Cost: \$$cost"
        
        # Track metrics
        if [[ "$model" == "bitnet" ]]; then
            ((bitnet_count++))
        else
            ((haiku_count++))
        fi
        total_cost=$(echo "$total_cost + $cost" | bc)
        
        # Log metric for analysis
        local metric=$(jq -n \
            --arg task "$task" \
            --arg model "$model" \
            --arg cost "$cost" \
            '{task: $task, model: $model, cost: ($cost | tonumber)}')
        echo "$metric" >> "$METRICS_FILE"
    done
    
    echo ""
    echo "Batch Summary:"
    echo "  BitNet tasks: $bitnet_count"
    echo "  Haiku tasks: $haiku_count"
    echo "  Total cost: \$$total_cost"
    echo ""
}

################################################################################
# Example 3: Context-Aware Routing
################################################################################

example_context_routing() {
    echo "=== Example 3: Context-Aware Routing ==="
    
    # Simulate different user contexts
    local contexts=(
        "interactive|What is the weather?|Simple Q&A"
        "analysis|Analyze this dataset and provide insights|Complex analysis"
        "scripting|Write a function to process CSV files|Code generation"
    )
    
    for context_spec in "${contexts[@]}"; do
        IFS='|' read -r context_type task description <<< "$context_spec"
        
        echo "Context: $context_type"
        echo "Task: $task"
        
        # Route with context awareness
        local output=$($ROUTING_SCRIPT --task "$description" --prompt "$task" 2>&1)
        local model=$(echo "$output" | grep "Model:" | awk '{print $2}')
        
        echo "  → Routed to: $model"
        echo ""
    done
}

################################################################################
# Example 4: Cost Optimization
################################################################################

example_cost_optimization() {
    echo "=== Example 4: Cost Optimization Analysis ==="
    
    echo "Current registry data:"
    if [[ -f "/root/.openclaw/workspace/hard-stops-registry-$(date +%Y%m%d).jsonl" ]]; then
        local registry="/root/.openclaw/workspace/hard-stops-registry-$(date +%Y%m%d).jsonl"
        
        echo ""
        echo "Tasks routed to BitNet (free):"
        jq 'select(.model == "bitnet") | .task' "$registry" 2>/dev/null | head -3
        echo ""
        
        echo "Total cost by model:"
        jq -s 'group_by(.model) | map({model: .[0].model, count: length, total: (map(.cost | tonumber) | add)})' "$registry" 2>/dev/null || echo "(Registry empty)"
        echo ""
    fi
}

################################################################################
# Example 5: Production-Grade Integration
################################################################################

production_request_handler() {
    local user_task="$1"
    local user_prompt="$2"
    
    # Validate inputs
    if [[ -z "$user_task" ]] || [[ -z "$user_prompt" ]]; then
        echo "Error: task and prompt required"
        return 1
    fi
    
    # Route through tier-routing
    local routing_output=$($ROUTING_SCRIPT --task "$user_task" --prompt "$user_prompt" 2>&1)
    
    # Parse results
    local model=$(echo "$routing_output" | grep "Model:" | awk '{print $2}')
    local cost=$(echo "$routing_output" | grep "Cost:" | sed 's/\$//' | awk '{print $2}')
    local response=$(echo "$routing_output" | tail -1)
    
    # Log to production metrics
    local metric=$(jq -n \
        --arg task "$user_task" \
        --arg model "$model" \
        --arg cost "$cost" \
        --arg timestamp "$(date -u +%Y-%m-%dT%H:%M:%SZ)" \
        '{timestamp: $timestamp, task: $task, model: $model, cost: ($cost | tonumber)}')
    
    echo "$metric" >> "/root/.openclaw/workspace/production-metrics-$(date +%Y%m%d).jsonl"
    
    # Return formatted response
    echo "{ \"success\": true, \"model\": \"$model\", \"cost\": $cost, \"response\": \"$response\" }"
}

################################################################################
# Example 6: Monitoring and Alerting
################################################################################

example_cost_monitoring() {
    echo "=== Example 6: Cost Monitoring ==="
    
    local registry="/root/.openclaw/workspace/hard-stops-registry-$(date +%Y%m%d).jsonl"
    
    if [[ -f "$registry" ]]; then
        local total_cost=$(jq -s 'map(.cost | tonumber) | add' "$registry" 2>/dev/null || echo 0)
        local task_count=$(wc -l < "$registry")
        local avg_cost=$(echo "scale=6; $total_cost / $task_count" | bc 2>/dev/null || echo 0)
        
        echo "Daily Metrics ($(date +%Y-%m-%d)):"
        echo "  Total cost: \$$total_cost"
        echo "  Task count: $task_count"
        echo "  Avg cost per task: \$$avg_cost"
        echo ""
        
        # Alert if cost exceeds threshold
        local cost_threshold=0.10  # $0.10 per day
        if (( $(echo "$total_cost > $cost_threshold" | bc -l) )); then
            echo "⚠️  ALERT: Daily cost exceeds threshold (\$$cost_threshold)"
            echo "   Consider adjusting classification patterns to favor BitNet"
        fi
    else
        echo "No data yet"
    fi
    
    echo ""
}

################################################################################
# Run Examples
################################################################################

main() {
    if [[ ! -f "$ROUTING_SCRIPT" ]]; then
        echo "Error: $ROUTING_SCRIPT not found"
        exit 1
    fi
    
    # Ensure metrics directory exists
    mkdir -p "$(dirname "$METRICS_FILE")"
    
    # Run all examples
    example_simple_request
    example_batch_processing
    example_context_routing
    example_cost_optimization
    example_cost_monitoring
    
    echo "=== Production Integration Ready ==="
    echo ""
    echo "To use in your code:"
    echo ""
    echo "  source /root/.openclaw/workspace/tier-routing-integration-example.sh"
    echo "  production_request_handler 'Your task' 'Your prompt'"
    echo ""
}

main "$@"
