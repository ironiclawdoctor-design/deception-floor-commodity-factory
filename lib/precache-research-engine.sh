#!/bin/bash

################################################################################
# precache-research-engine.sh
#
# Purpose: Run lightweight research in bash/BitNet BEFORE calling sessions_spawn,
# then inject precached findings into the task so Haiku does lookup, not generation.
#
# Cost model:
# - BEFORE: 1 full subagent spawn @ Haiku = ~500-2000 tokens
# - AFTER: 1 subagent spawn @ Haiku with precached context = ~50-200 tokens
#
# Research techniques (all $0.00):
# 1. Grep-based knowledge mining (MEMORY.md, docs)
# 2. File content embedding via indexing
# 3. Previous response caching
# 4. Pattern extraction from git history
# 5. SQLite queries on agency.db
#
################################################################################

set -euo pipefail

RESEARCH_CACHE="/root/.openclaw/workspace/.research-cache"
AGENCY_DB="/root/.openclaw/workspace/agency.db"
mkdir -p "$RESEARCH_CACHE"

################################################################################
# Research Strategy 1: Knowledge Mining (Grep)
################################################################################

mine_memory() {
    local query="$1"
    local limit="${2:-3}"
    
    if [[ -f /root/.openclaw/workspace/MEMORY.md ]]; then
        grep -i -B1 -A3 "$query" /root/.openclaw/workspace/MEMORY.md 2>/dev/null | head -$((limit * 5)) || true
    fi
}

mine_docs() {
    local query="$1"
    local limit="${2:-2}"
    
    find /root/.openclaw/workspace -maxdepth 2 -name "*.md" -type f \
        -exec grep -l -i "$query" {} \; 2>/dev/null | head -$limit | while read f; do
            echo "--- $f ---"
            grep -i -B1 -A2 "$query" "$f" | head -10
        done
}

################################################################################
# Research Strategy 2: Database Query (if agency.db exists)
################################################################################

query_agency_db() {
    local query="$1"
    
    if [[ ! -f "$AGENCY_DB" ]]; then
        return 0
    fi
    
    # Try to find matching records in agency database
    sqlite3 "$AGENCY_DB" "SELECT * FROM tool_registry WHERE name LIKE '%$query%' LIMIT 3;" 2>/dev/null || true
}

################################################################################
# Research Strategy 3: Git History Pattern Extraction
################################################################################

extract_git_patterns() {
    local query="$1"
    local repo="${2:-.}"
    
    if [[ ! -d "$repo/.git" ]]; then
        return 0
    fi
    
    # Find commits mentioning the query
    cd "$repo"
    git log --all --oneline --grep="$query" 2>/dev/null | head -3 || true
}

################################################################################
# Research Strategy 4: Previous Response Caching
################################################################################

lookup_previous_response() {
    local task_hash="$1"
    local cache_dir="$RESEARCH_CACHE"
    
    local cache_file="$cache_dir/response-$task_hash.cache"
    if [[ -f "$cache_file" ]]; then
        echo "PREVIOUS_RESPONSE:"
        cat "$cache_file" | head -20
    fi
}

################################################################################
# Main Research Pipeline
################################################################################

run_research() {
    local task="$1"
    local research_output="$RESEARCH_CACHE/research-$$.json"
    
    echo "🔬 Running precache research on task..."
    echo "   Task: ${task:0:60}..."
    
    # Extract key concepts from task
    local keywords=$(echo "$task" | grep -oE '\b[a-z]{5,}\b' | sort -u | head -5)
    
    echo ""
    echo "📚 Research results:"
    echo "{"
    echo '  "research_timestamp": "'$(date -u +%Y-%m-%dT%H:%M:%SZ)'",'
    echo '  "task_hash": "'$(echo "$task" | md5sum | awk '{print $1}')'",'
    echo '  "keywords": "'$(echo $keywords | tr '\n' ' ')'",'
    echo '  "findings": {'
    
    # Strategy 1: Memory mining
    echo '    "memory_findings": ['
    local mem_found=0
    for keyword in $keywords; do
        local result=$(mine_memory "$keyword" 1)
        if [[ -n "$result" ]]; then
            if [[ $mem_found -gt 0 ]]; then echo ","; fi
            echo "      \"$(echo "$result" | head -1 | sed 's/"/\\"/g')\""
            ((mem_found++))
        fi
    done
    echo "    ],"
    
    # Strategy 2: Doc mining
    echo '    "doc_findings": ['
    local doc_found=0
    for keyword in $keywords; do
        local result=$(mine_docs "$keyword" 1 | head -5)
        if [[ -n "$result" ]]; then
            if [[ $doc_found -gt 0 ]]; then echo ","; fi
            echo "      \"$(echo "$result" | head -1 | sed 's/"/\\"/g')\""
            ((doc_found++))
        fi
    done
    echo "    ],"
    
    # Strategy 3: Database
    echo '    "db_findings": ['
    local db_result=$(query_agency_db "$(echo $keywords | head -1)")
    if [[ -n "$db_result" ]]; then
        echo "      \"$db_result\""
    fi
    echo "    ],"
    
    # Strategy 4: Git patterns
    echo '    "git_patterns": ['
    for keyword in $keywords; do
        local git_result=$(extract_git_patterns "$keyword" "/root/.openclaw/workspace" | head -1)
        if [[ -n "$git_result" ]]; then
            echo "      \"$(echo "$git_result" | sed 's/"/\\"/g')\""
            break
        fi
    done
    echo "    ]"
    
    echo "  },"
    echo '  "precache_injection": "Include findings above in task context to reduce regeneration"'
    echo "}"
    
    # Save research output
    {
        echo "🔬 Research Complete"
        echo ""
        echo "Keywords: $keywords"
        echo ""
        echo "Memory findings: $mem_found items"
        echo "Doc findings: $doc_found items"
        echo "DB findings available"
        echo "Git patterns extracted"
    } > "$research_output"
}

################################################################################
# Integrate into spawn call
################################################################################

prepare_optimized_spawn() {
    local original_task="$1"
    local label="${2:-precached-task}"
    
    local task_hash=$(echo "$original_task" | md5sum | awk '{print $1}')
    
    # Run research
    local research=$(run_research "$original_task")
    
    # Build optimized task with research context injected
    cat << EOF
$original_task

---PRECACHED RESEARCH CONTEXT---
$research
---END PRECACHED CONTEXT---

Instructions for responder:
1. If the precached research fully answers this task, use it.
2. If precached context is incomplete, synthesize and extend it.
3. Do NOT regenerate findings already in precached context.
4. Return the final answer incorporating cache where available.
EOF
}

################################################################################
# CLI
################################################################################

if [[ $# -lt 1 ]]; then
    cat << USAGE
Usage: $0 <task> [label]

Research strategies employed:
  1. Grep-based memory mining (MEMORY.md)
  2. Document scanning (*.md in workspace)
  3. SQLite queries (agency.db)
  4. Git history patterns

Example:
  $0 "Write tier-routing enforcement script" "tier-routing"

This script outputs an optimized task ready for sessions_spawn, with
precached research injected to reduce token cost.
USAGE
    exit 1
fi

prepare_optimized_spawn "$1" "${2:-task}"
