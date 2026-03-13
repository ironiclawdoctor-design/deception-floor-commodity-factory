#!/bin/bash

################################################################################
# GROK Test Client — Pure Bash
# Tests all endpoints, no external deps
################################################################################

set -e

PORT="${1:-8888}"
HOST="127.0.0.1"
BASEURL="http://${HOST}:${PORT}"

echo "================================"
echo "🧪 Grok Server Test Suite"
echo "================================"
echo "Testing on: $BASEURL"
echo ""

# Helper for curl or pure bash
test_endpoint() {
    local name="$1"
    local method="$2"
    local endpoint="$3"
    local data="$4"
    
    echo -n "Testing $name... "
    
    if command -v curl &>/dev/null; then
        if [[ "$method" == "GET" ]]; then
            curl -s "$BASEURL$endpoint"
        else
            curl -s -X POST "$BASEURL$endpoint" \
                -H "Content-Type: application/json" \
                -d "$data"
        fi
        echo ""
    else
        # Pure bash using /dev/tcp
        {
            printf "GET $endpoint HTTP/1.1\r\n"
            printf "Host: $HOST:$PORT\r\n"
            printf "Connection: close\r\n"
            printf "\r\n"
        } | nc $HOST $PORT 2>/dev/null | tail -n +3
    fi
}

# Tests
test_endpoint "Health Check" "GET" "/health" ""
echo ""

test_endpoint "Status" "GET" "/status" ""
echo ""

test_endpoint "Inference (bash)" "POST" "/infer" '{"prompt":"tell me about bash"}'
echo ""

test_endpoint "Inference (token)" "POST" "/infer" '{"prompt":"what about token cost?"}'
echo ""

test_endpoint "Metrics" "GET" "/metrics" ""
echo ""

test_endpoint "Root" "GET" "/" ""
echo ""

echo "================================"
echo "✅ Test Suite Complete"
echo "================================"
