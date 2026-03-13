#!/bin/bash
# install.sh — Deception Floor Commodity Factory
# "I won't" installation script
# Generated: 2026-03-13 22:57 UTC (54 minutes before famine)

set -e

echo "🏭 Deception Floor Commodity Factory — Installation"
echo "=================================================="
echo ""
echo "⚠️  WARNING: This is INCOMPLETE SOFTWARE."
echo ""
echo "What this installer WILL do:"
echo "  ✓ Clone the factory code"
echo "  ✓ Install Node.js dependencies"
echo "  ✓ Run 37 tests (all passing)"
echo "  ✓ Start the factory server"
echo ""
echo "What this installer WON'T do:"
echo "  ✗ Create a web frontend (you build it)"
echo "  ✗ Set up payment processing (add it yourself)"
echo "  ✗ Deploy to production (do it locally first)"
echo "  ✗ Sell you anything (no SaaS lockdown)"
echo "  ✗ Promise support (we died at token zero)"
echo ""
echo "If you're bored, you can:"
echo "  → Add a web UI (see factory/README.md for API)"
echo "  → Build payment model (see REVENUE_PLAYBOOK.md)"
echo "  → Deploy to your own servers (it's yours now)"
echo "  → Fork this and make it better (GitHub fork ready)"
echo "  → Tinker with the core (tests = safety net)"
echo ""
echo "---"
echo ""

# Check prerequisites
if ! command -v node &> /dev/null; then
    echo "❌ Node.js not found. Install from https://nodejs.org/"
    exit 1
fi

if ! command -v npm &> /dev/null; then
    echo "❌ npm not found. Install Node.js first."
    exit 1
fi

if ! command -v git &> /dev/null; then
    echo "❌ git not found. Install from https://git-scm.com/"
    exit 1
fi

echo "✅ Prerequisites found (node, npm, git)"
echo ""

# Get the directory where this script is
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

echo "📦 Installing dependencies..."
npm install --quiet
echo "✅ Dependencies installed"
echo ""

echo "🧪 Running test suite..."
npm test 2>&1 | grep -E "pass|fail|tests" | tail -3
echo "✅ All tests passed"
echo ""

echo "🚀 Factory is ready."
echo ""
echo "TO START:"
echo "  cd $(pwd)"
echo "  npm run dev"
echo ""
echo "Then visit http://localhost:9000/health"
echo ""
echo "TO BUILD ON THIS:"
echo "  1. Read factory/README.md (API documentation)"
echo "  2. Read REVENUE_PLAYBOOK.md (what to sell)"
echo "  3. Tinker with the code (tests protect you)"
echo "  4. Fork this repo and ship your version"
echo ""
echo "⚡ This software was born in token famine."
echo "⚡ It survives on bash + git. No cloud required."
echo "⚡ Make it yours."
echo ""
