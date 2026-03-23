#!/bin/bash
# Apply Dollar Persona SQL patch (fix views, add market tables, etc.)

set -e

DB_PATH="${1:-/root/.openclaw/workspace/dollar/dollar.db}"
PATCH_FILE="$(dirname "$0")/dollar-patch-final.sql"

echo "💰 Applying Dollar Persona SQL patch..."
echo "Database: $DB_PATH"
echo "Patch: $PATCH_FILE"

if [ ! -f "$DB_PATH" ]; then
    echo "❌ Database not found. Run ./dollar-init.sh first."
    exit 1
fi

if [ ! -f "$PATCH_FILE" ]; then
    echo "❌ Patch file not found: $PATCH_FILE"
    exit 1
fi

# Backup existing database
BACKUP="${DB_PATH}.backup.$(date +%Y%m%d_%H%M%S)"
cp "$DB_PATH" "$BACKUP"
echo "📦 Backup created: $BACKUP"

# Apply patch
if sqlite3 "$DB_PATH" < "$PATCH_FILE"; then
    echo "✅ Patch applied successfully."
    echo ""
    echo "Changes applied:"
    echo "  - Fixed daily_usd_position view"
    echo "  - Added Cash App, BTC wallet, Ampere referral accounts"
    echo "  - Created confessions table for failure logging"
    echo "  - Added market tables (exchange_rates, market_trades)"
    echo "  - Created Treasury/Reserve accounts"
    echo "  - Set initial exchange rate: 10 Shannon/$1 ($60 backing → 600 Shannon)"
    echo "  - Added donation_summary and shannon_supply views"
    echo ""
    echo "Next:"
    echo "  1. Run ./dollar-report.sh to verify"
    echo "  2. Run ./dollar-sweep.sh to check backing"
    echo "  3. Run ./dollar-market.sh rate to see exchange rate"
else
    echo "❌ Patch failed. Restoring backup..."
    cp "$BACKUP" "$DB_PATH"
    exit 1
fi