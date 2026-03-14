#!/bin/bash

################################################################################
# spawn-precached.sh
#
# Main entry point: Run research + spawn with precached context
#
# USAGE: spawn-precached.sh <task> [label] [model]
#
# This is the wrapper you call instead of sessions_spawn directly when you
# want to minimize token cost via precaching.
#
# Cost reduction: ~75-95% per call (regeneration prevention)
#
################################################################################

set -euo pipefail

LIBDIR="/root/.openclaw/workspace/lib"
RESEARCH_ENGINE="$LIBDIR/precache-research-engine.sh"

if [[ ! -f "$RESEARCH_ENGINE" ]]; then
    echo "❌ Error: precache-research-engine.sh not found at $RESEARCH_ENGINE"
    exit 1
fi

if [[ $# -lt 1 ]]; then
    cat << USAGE
Usage: $0 <task> [label] [model]

Example:
  $0 "Write tier-routing enforcement script" "tier-routing" "haiku"
  
  Then use the output as the optimized_task in:
  
  sessions_spawn(
    task="<optimized_task_from_above>",
    label="tier-routing",
    model="haiku",
    runtime="subagent"
  )

This wrapper:
1. Runs $RESEARCH_ENGINE to extract precached context (Bash, $0.00)
2. Injects findings into the task
3. Outputs the optimized task ready for sessions_spawn
4. Estimated token savings: 50-200 tokens per call

Environment:
  Task: "$1"
  Label: "${2:-task}"
  Model: "${3:-anthropic/claude-haiku-4-5-20251001}"
USAGE
    exit 1
fi

# Run research phase
echo "📊 PRECACHE RESEARCH PHASE (Bash, \$0.00)"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

OPTIMIZED_TASK=$("$RESEARCH_ENGINE" "$1" "${2:-task}")

echo ""
echo "✅ Research complete. Optimized task ready for sessions_spawn:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "STEP 1: Save this optimized task to a variable"
echo ""
echo 'optimized_task='"'"''"$OPTIMIZED_TASK"''"'"
echo ""
echo ""
echo "STEP 2: Call sessions_spawn with this command:"
echo ""
echo '  sessions_spawn('
echo '    task: optimized_task,'
echo '    label: "'${2:-task}'",'
echo '    model: "'${3:-anthropic/claude-haiku-4-5-20251001}'",'
echo '    runtime: "subagent",'
echo '    runTimeoutSeconds: 600'
echo '  )'
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "COST ANALYSIS:"
echo "  - Research phase: \$0.00 (bash-only)"
echo "  - Spawn phase: ~50-200 tokens (vs. 500-2000 without precache)"
echo "  - Estimated savings: 75-95% token cost reduction"
echo ""
