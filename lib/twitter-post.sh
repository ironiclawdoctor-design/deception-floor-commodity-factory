#!/bin/bash
# twitter-post.sh — Post tweets from any agent (Tier 0-2)
# Usage: ./twitter-post.sh "Your tweet text here" [--thread] [--dry-run]
# Cost: $0.00 (Twitter free tier)

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SECRETS_DIR="${SCRIPT_DIR}/../secrets"
LOG_FILE="${SCRIPT_DIR}/../logs/twitter-posts.log"
DB_FILE="${SCRIPT_DIR}/../data/twitter-posts.db"

# Source the secrets loader
source "${SCRIPT_DIR}/secrets-loader.sh"

# Parse arguments
TWEET_TEXT="${1:?Error: Tweet text required}"
THREAD_MODE="${2:---single}"
DRY_RUN="${3:---execute}"

# Ensure directories exist
mkdir -p "$(dirname "$LOG_FILE")" "$(dirname "$DB_FILE")"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# ============================================================================
# TIER 0: Validation (pure bash, no external calls)
# ============================================================================

validate_tweet() {
    local text="$1"
    
    # Twitter API v2 limit: 280 characters
    local length=${#text}
    if (( length > 280 )); then
        echo -e "${RED}✗ Tweet too long ($length > 280 chars)${NC}" >&2
        return 1
    fi
    
    if (( length == 0 )); then
        echo -e "${RED}✗ Tweet cannot be empty${NC}" >&2
        return 1
    fi
    
    # Check for credential file
    if [[ ! -f "$SECRETS_DIR/twitter-api.json" ]]; then
        echo -e "${RED}✗ Credentials not found: $SECRETS_DIR/twitter-api.json${NC}" >&2
        echo -e "${YELLOW}  → Copy from template: cp twitter-api-template.json twitter-api.json${NC}" >&2
        return 1
    fi
    
    return 0
}

# ============================================================================
# TIER 1: Logging & Audit Trail (SQLite, local)
# ============================================================================

init_db() {
    if [[ ! -f "$DB_FILE" ]]; then
        sqlite3 "$DB_FILE" << 'EOF'
CREATE TABLE posts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    tweet_id TEXT,
    text TEXT NOT NULL,
    status TEXT NOT NULL,
    error_msg TEXT,
    posted_by TEXT NOT NULL,
    cost REAL NOT NULL DEFAULT 0.0
);

CREATE TABLE rate_limits (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    checked_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    remaining INTEGER NOT NULL,
    reset_at TEXT NOT NULL
);

CREATE INDEX idx_status ON posts(status);
CREATE INDEX idx_created_at ON posts(created_at);
EOF
        echo -e "${GREEN}✓ Database initialized: $DB_FILE${NC}"
    fi
}

log_post_attempt() {
    local text="$1"
    local status="${2:-pending}"
    local error_msg="${3:-}"
    local posted_by="${4:-$(whoami)@$(hostname)}"
    
    local sanitized_text=$(echo "$text" | sed "s/'/''/g")
    
    sqlite3 "$DB_FILE" << EOF
INSERT INTO posts (text, status, error_msg, posted_by, cost)
VALUES ('$sanitized_text', '$status', '$error_msg', '$posted_by', 0.0);
EOF
}

# ============================================================================
# TIER 2: Twitter API v2 Interaction (curl + jq)
# ============================================================================

post_to_twitter() {
    local text="$1"
    local dry_run="${2:---execute}"
    
    # Load credentials
    local bearer_token
    bearer_token=$(load_secret "twitter-api" "credentials.bearer_token") || {
        echo -e "${RED}✗ Failed to load bearer token${NC}" >&2
        log_post_attempt "$text" "failed" "Credential load error"
        return 1
    }
    
    if [[ "$bearer_token" == "YOUR_BEARER_TOKEN_HERE" ]]; then
        echo -e "${RED}✗ Bearer token not configured (template value detected)${NC}" >&2
        echo -e "${YELLOW}  → Edit: $SECRETS_DIR/twitter-api.json${NC}" >&2
        return 1
    fi
    
    # Build request
    local payload=$(jq -n --arg text "$text" '{text: $text}')
    
    if [[ "$dry_run" == "--dry-run" ]]; then
        echo -e "${BLUE}📋 [DRY RUN] Would POST to Twitter:${NC}"
        echo "$payload" | jq '.'
        log_post_attempt "$text" "dry_run"
        return 0
    fi
    
    # Execute POST
    echo -e "${BLUE}🐦 Posting to Twitter...${NC}"
    
    local response
    response=$(curl -s -X POST \
        "https://api.twitter.com/2/tweets" \
        -H "Authorization: Bearer $bearer_token" \
        -H "Content-Type: application/json" \
        -d "$payload" 2>&1) || {
        echo -e "${RED}✗ Request failed${NC}" >&2
        log_post_attempt "$text" "failed" "curl error"
        return 1
    }
    
    # Parse response
    local tweet_id
    tweet_id=$(echo "$response" | jq -r '.data.id // empty' 2>/dev/null) || {
        echo -e "${RED}✗ Invalid response from Twitter API:${NC}" >&2
        echo "$response" | jq '.' >&2
        
        local error_msg=$(echo "$response" | jq -r '.errors[0].message // .detail // "Unknown error"' 2>/dev/null)
        log_post_attempt "$text" "failed" "$error_msg"
        return 1
    }
    
    if [[ -z "$tweet_id" ]]; then
        echo -e "${RED}✗ No tweet ID in response${NC}" >&2
        echo "$response" | jq '.' >&2
        log_post_attempt "$text" "failed" "No tweet ID returned"
        return 1
    fi
    
    # Success
    echo -e "${GREEN}✓ Posted! Tweet ID: $tweet_id${NC}"
    echo -e "${GREEN}  View: https://twitter.com/i/web/status/$tweet_id${NC}"
    
    # Update DB with tweet ID
    sqlite3 "$DB_FILE" << EOF
INSERT INTO posts (text, status, posted_by, cost, tweet_id)
VALUES ('${text//\'/\'\'}', 'posted', '$(whoami)@$(hostname)', 0.0, '$tweet_id');
EOF
    
    # Append to log
    echo "[$(date -u +'%Y-%m-%dT%H:%M:%SZ')] ✓ POSTED tweet_id=$tweet_id by $(whoami)" >> "$LOG_FILE"
    
    return 0
}

# ============================================================================
# Main Entry Point
# ============================================================================

main() {
    echo -e "${BLUE}═══════════════════════════════════════════${NC}"
    echo -e "${BLUE}  Twitter Post Agent (Tier 0-2, Cost: \$0.00)${NC}"
    echo -e "${BLUE}═══════════════════════════════════════════${NC}"
    
    # Initialize
    init_db
    
    # Validate
    if ! validate_tweet "$TWEET_TEXT"; then
        return 1
    fi
    
    echo -e "${YELLOW}Tweet (${#TWEET_TEXT} chars):${NC}"
    echo "  $TWEET_TEXT"
    echo ""
    
    # Post
    if ! post_to_twitter "$TWEET_TEXT" "$DRY_RUN"; then
        return 1
    fi
    
    return 0
}

main "$@"
