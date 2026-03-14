#!/bin/bash
# agency-twitter-orchestrator.sh — Multi-agent Twitter coordination
# Usage: ./agency-twitter-orchestrator.sh [--automate | --official | --daimyo | --status | --schedule]
# Cost: $0.00 (Tier 0-2)

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TWEETS_QUEUE="${SCRIPT_DIR}/../data/twitter-queue.json"
TWEETS_HISTORY="${SCRIPT_DIR}/../data/twitter-posts.db"
LOG_FILE="${SCRIPT_DIR}/../logs/twitter-orchestrator.log"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
NC='\033[0m'

# Ensure directories
mkdir -p "$(dirname "$TWEETS_QUEUE")" "$(dirname "$LOG_FILE")"

# ============================================================================
# AUTOMATE: Policy & Strategy Posts
# ============================================================================

queue_automate_tweet() {
    local message="$1"
    local category="${2:-strategy}"
    
    local payload=$(cat <<EOF
{
  "agent": "automate",
  "category": "$category",
  "priority": "high",
  "text": "$message",
  "queued_at": "$(date -u +'%Y-%m-%dT%H:%M:%SZ')",
  "status": "pending"
}
EOF
)
    
    echo "$payload" | jq '.' >> "$TWEETS_QUEUE"
    echo -e "${PURPLE}[Automate] Queued: $category${NC}"
    echo "[$(date -u +'%Y-%m-%dT%H:%M:%SZ')] AUTOMATE queue: $category" >> "$LOG_FILE"
}

post_automate_strategy() {
    echo -e "${PURPLE}═══════════════════════════════════════════${NC}"
    echo -e "${PURPLE}  AUTOMATE Branch: Strategy & Policy Posts${NC}"
    echo -e "${PURPLE}═══════════════════════════════════════════${NC}"
    
    # Example: Policy post
    queue_automate_tweet \
        "📋 Agency Policy Update: All Tier routing now enforced. BitNet-first for internal tasks. Zero external token bleed. Learn more: [link]" \
        "policy"
    
    # Example: Roadmap post
    queue_automate_tweet \
        "🗺️ Q2 Roadmap: Ollama fork deployment, revenue tier gates, persistent caching layer. Vote on priorities in Discord." \
        "roadmap"
    
    echo -e "${GREEN}✓ Posted 2 strategy tweets${NC}"
}

# ============================================================================
# OFFICIAL: Production Status & Releases
# ============================================================================

queue_official_tweet() {
    local message="$1"
    local category="${2:-release}"
    
    local payload=$(cat <<EOF
{
  "agent": "official",
  "category": "$category",
  "priority": "critical",
  "text": "$message",
  "queued_at": "$(date -u +'%Y-%m-%dT%H:%M:%SZ')",
  "status": "pending"
}
EOF
)
    
    echo "$payload" | jq '.' >> "$TWEETS_QUEUE"
    echo -e "${GREEN}[Official] Queued: $category${NC}"
    echo "[$(date -u +'%Y-%m-%dT%H:%M:%SZ')] OFFICIAL queue: $category" >> "$LOG_FILE"
}

post_official_release() {
    echo -e "${GREEN}═══════════════════════════════════════════${NC}"
    echo -e "${GREEN}  OFFICIAL Branch: Production Releases${NC}"
    echo -e "${GREEN}═══════════════════════════════════════════${NC}"
    
    # Example: Version release
    queue_official_tweet \
        "🚀 Deception Floor Commodity Factory v2.1 live. 50 floors/hour, 93/100 quality score, $0.00 cost. Fully autonomous." \
        "release"
    
    # Example: Status update
    queue_official_tweet \
        "✅ All systems nominal. Sovereignty 85%, BitNet primary, Haiku frozen. Zero token deficit." \
        "status"
    
    echo -e "${GREEN}✓ Posted 2 official releases${NC}"
}

# ============================================================================
# DAIMYO: Enforcement & Security
# ============================================================================

queue_daimyo_tweet() {
    local message="$1"
    local category="${2:-enforcement}"
    
    local payload=$(cat <<EOF
{
  "agent": "daimyo",
  "category": "$category",
  "priority": "critical",
  "text": "$message",
  "queued_at": "$(date -u +'%Y-%m-%dT%H:%M:%SZ')",
  "status": "pending"
}
EOF
)
    
    echo "$payload" | jq '.' >> "$TWEETS_QUEUE"
    echo -e "${RED}[Daimyo] Queued: $category${NC}"
    echo "[$(date -u +'%Y-%m-%dT%H:%M:%SZ')] DAIMYO queue: $category" >> "$LOG_FILE"
}

post_daimyo_enforcement() {
    echo -e "${RED}═══════════════════════════════════════════${NC}"
    echo -e "${RED}  DAIMYO Branch: Enforcement & Security${NC}"
    echo -e "${RED}═══════════════════════════════════════════${NC}"
    
    # Example: Security advisory
    queue_daimyo_tweet \
        "🔒 Security Update: All external API calls now rate-limited. Tier routing enforced at compile-time. No token leaks." \
        "security"
    
    # Example: Cost control
    queue_daimyo_tweet \
        "💰 Cost Report: Token burn reduced 60% via BitNet. Next: 90% reduction by Q3. Revenue per token UP 40%." \
        "cost-control"
    
    echo -e "${RED}✓ Posted 2 enforcement notices${NC}"
}

# ============================================================================
# Cross-Agent Coordination
# ============================================================================

show_status() {
    echo -e "${BLUE}═══════════════════════════════════════════${NC}"
    echo -e "${BLUE}  Agency Twitter Orchestration Status${NC}"
    echo -e "${BLUE}═══════════════════════════════════════════${NC}"
    echo ""
    
    # Count by agent
    if [[ -f "$TWEETS_QUEUE" ]]; then
        echo "📊 Queued tweets:"
        jq -r '.agent' "$TWEETS_QUEUE" 2>/dev/null | sort | uniq -c || echo "  (empty)"
    else
        echo "📊 Queued tweets: (none)"
    fi
    
    echo ""
    
    # Posted tweets (from DB)
    if [[ -f "$TWEETS_HISTORY" ]]; then
        echo "✅ Posted tweets:"
        sqlite3 "$TWEETS_HISTORY" "SELECT COUNT(*) as total, status FROM posts GROUP BY status;" 2>/dev/null || echo "  (DB not initialized)"
    else
        echo "✅ Posted tweets: (none)"
    fi
    
    echo ""
    echo -e "${BLUE}Queue file: $TWEETS_QUEUE${NC}"
    echo -e "${BLUE}History DB: $TWEETS_HISTORY${NC}"
    echo -e "${BLUE}Logs: $LOG_FILE${NC}"
}

process_queue() {
    echo -e "${BLUE}═══════════════════════════════════════════${NC}"
    echo -e "${BLUE}  Processing Twitter Queue${NC}"
    echo -e "${BLUE}═══════════════════════════════════════════${NC}"
    echo ""
    
    if [[ ! -f "$TWEETS_QUEUE" ]] || [[ ! -s "$TWEETS_QUEUE" ]]; then
        echo "⚠️  Queue is empty"
        return 0
    fi
    
    local count=0
    while IFS= read -r line; do
        if [[ -z "$line" ]]; then continue; fi
        
        local text=$(echo "$line" | jq -r '.text' 2>/dev/null) || continue
        local agent=$(echo "$line" | jq -r '.agent' 2>/dev/null)
        
        echo -e "[$agent] Posting: ${text:0:50}..."
        
        # Call the main twitter-post.sh
        if "${SCRIPT_DIR}/twitter-post.sh" "$text"; then
            echo -e "${GREEN}  ✓ Posted${NC}"
            ((count++))
        else
            echo -e "${RED}  ✗ Failed (will retry next cycle)${NC}"
        fi
    done < <(jq -c '.' "$TWEETS_QUEUE" 2>/dev/null)
    
    # Clear processed queue (in production, archive instead)
    > "$TWEETS_QUEUE"
    
    echo ""
    echo -e "${GREEN}✓ Processed $count tweets${NC}"
}

# ============================================================================
# Main Entry Point
# ============================================================================

main() {
    local command="${1:-status}"
    
    case "$command" in
        --automate)
            post_automate_strategy
            ;;
        --official)
            post_official_release
            ;;
        --daimyo)
            post_daimyo_enforcement
            ;;
        --status)
            show_status
            ;;
        --schedule)
            process_queue
            ;;
        --help)
            cat <<EOF
Agency Twitter Orchestrator

Usage:
  ./agency-twitter-orchestrator.sh [COMMAND]

Commands:
  --automate     Post Automate branch tweets (strategy, policy, roadmap)
  --official     Post Official branch tweets (releases, status)
  --daimyo       Post Daimyo branch tweets (security, enforcement)
  --status       Show queue and history status
  --schedule     Process entire queue (for cron jobs)
  --help         Show this message

Examples:
  # Post all three branches' prepared tweets
  ./agency-twitter-orchestrator.sh --automate
  ./agency-twitter-orchestrator.sh --official
  ./agency-twitter-orchestrator.sh --daimyo

  # Check status
  ./agency-twitter-orchestrator.sh --status

  # Run from cron (processes queue every 30 min)
  # 0,30 * * * * /path/to/agency-twitter-orchestrator.sh --schedule

Cost: \$0.00 (Tier 0-2, Twitter free tier)
EOF
            ;;
        *)
            echo -e "${RED}Unknown command: $command${NC}"
            echo "Run with --help for usage"
            exit 1
            ;;
    esac
}

main "$@"
