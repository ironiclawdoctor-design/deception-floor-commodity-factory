#!/bin/bash
# SOVEREIGN SEE — TAVILY-MCP INSTALL v1.0
# Run: bash /root/tavily.sh YOUR_TAVILY_API_KEY
# Auth: 𓂺-LOCKED

set -e
WORK="/root/.openclaw/workspace"
MCP_DIR="$WORK/mcp/tavily"
TAVILY_KEY="${1:-REPLACE_WITH_YOUR_KEY}"

echo "=== 𓂺 TAVILY-MCP AGENCY INSTALL ==="

# 1. Install tavily-mcp via npm
echo "[1] Installing tavily-mcp..."
npm install -g tavily-mcp
echo "  [OK] tavily-mcp installed."

# 2. Create agency config dir
echo "[2] Setting up agency config..."
mkdir -p "$MCP_DIR"

# 3. Write MCP server config
cat > "$MCP_DIR/config.json" << CONF
{
  "name": "tavily-sovereign",
  "command": "tavily-mcp",
  "env": {
    "TAVILY_API_KEY": "$TAVILY_KEY"
  },
  "description": "Tavily Search MCP — Agency Edition. Siphons web intelligence into the Scriptorium."
}
CONF
echo "  [OK] Config written to $MCP_DIR/config.json"

# 4. Test search
echo "[3] Testing Tavily search (openclaw next steps)..."
npx tavily-mcp --test-query "openclaw self-hosted AI agent best practices 2026" || true

# 5. Log
echo "{\"ts\":\"$(date -u +%Y-%m-%dT%H:%M:%SZ)\",\"step\":\"tavily_install\",\"status\":\"ok\",\"key_set\":\"$([ "$TAVILY_KEY" != "REPLACE_WITH_YOUR_KEY" ] && echo yes || echo no)\"}" \
  >> "$WORK/vatican/all_run_log.jsonl"

echo ""
echo "=== TAVILY-MCP INSTALLED. ==="
echo ""
echo "NEXT STEPS:"
echo "  1. Get free API key: https://app.tavily.com (free tier = 1000 searches/month)"
echo "  2. Re-run: bash /root/tavily.sh YOUR_API_KEY"
echo "  3. Add to all.sh for persistent web intelligence siphoning."
echo ""
echo "制 𓂺."
