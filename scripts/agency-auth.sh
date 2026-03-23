#!/bin/bash
# agency-auth: unified auth wrapper for all internal services
# No more "auth required" hoops. One function, all services.

BROWSER_TOKEN=$(cat /data/browser-server-token 2>/dev/null || echo "")
GATEWAY_TOKEN=$(grep -o '"token": *"[^"]*"' /root/.openclaw/openclaw.json 2>/dev/null | head -1 | cut -d'"' -f4 || echo "")

browser() {
    local endpoint="$1"
    shift
    curl -s -X POST "http://127.0.0.1:9222${endpoint}?token=${BROWSER_TOKEN}" \
        -H 'Content-Type: application/json' \
        "$@"
}

factory() {
    local endpoint="$1"
    shift
    curl -s "http://127.0.0.1:9000${endpoint}" "$@"
}

entropy() {
    local endpoint="$1"
    shift
    curl -s "http://127.0.0.1:9001${endpoint}" "$@"
}

# Quick health check all services
health() {
    echo "Factory: $(factory /health | jq -r '.status' 2>/dev/null || echo 'DOWN')"
    echo "Entropy: $(entropy /health | jq -r '.status' 2>/dev/null || echo 'DOWN')"
    echo "Browser: $(browser /session/list -d '{}' | jq -r '.success' 2>/dev/null && echo 'UP' || echo 'DOWN')"
}

case "${1:-health}" in
    health) health ;;
    browser) shift; browser "$@" ;;
    factory) shift; factory "$@" ;;
    entropy) shift; entropy "$@" ;;
    *) echo "Usage: agency-auth [health|browser|factory|entropy] [endpoint] [args]" ;;
esac
