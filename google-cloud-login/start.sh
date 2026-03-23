#!/bin/bash
# Start Google Cloud login server

set -e

echo "🔐 Starting Google Cloud Login Server"
echo "====================================="

# Check if port 8080 is in use
if lsof -Pi :8080 -sTCP:LISTEN -t >/dev/null 2>&1; then
    echo "⚠️  Port 8080 is already in use. Killing existing process..."
    fuser -k 8080/tcp 2>/dev/null || true
    sleep 2
fi

# Check Python availability
if ! command -v python3 >/dev/null 2>&1; then
    echo "❌ Python 3 not found. Please install python3."
    exit 1
fi

# Check dependencies
echo "📦 Checking Python dependencies..."
if ! python3 -c "import http.server" 2>/dev/null; then
    echo "✅ http.server module available"
else
    echo "✅ http.server is built-in"
fi

# Start server
echo "🚀 Starting server on http://localhost:8080"
echo ""
echo "📋 Options:"
echo "  1. Open http://localhost:8080 in your browser"
echo "  2. Choose authentication method:"
echo "     - Manual cookie export (DevTools)"
echo "     - OAuth 2.0 flow (recommended)"
echo "     - Service account (most secure)"
echo ""
echo "🔒 Secrets will be stored in:"
echo "  /root/.openclaw/workspace/secrets/"
echo ""
echo "📝 Logs will be written to server.log"
echo "🛑 Press Ctrl+C to stop server"

# Run server
cd "$(dirname "$0")"
exec python3 server.py 2>&1 | tee server.log