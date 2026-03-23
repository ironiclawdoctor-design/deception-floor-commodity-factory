#!/bin/bash
# Dollar Persona - Initialize Financial Ledger

set -e

DB_PATH="${1:-/root/.openclaw/workspace/dollar/dollar.db}"
SCHEMA_PATH="$(dirname "$0")/dollar-ledger.sql"

echo "💰 Initializing Dollar Persona Financial Ledger"
echo "Database: $DB_PATH"

if ! command -v sqlite3 &> /dev/null; then
    echo "❌ sqlite3 not found. Install with: apt-get install sqlite3"
    exit 1
fi

# Create database directory if needed
mkdir -p "$(dirname "$DB_PATH")"

# Initialize schema
if [ -f "$SCHEMA_PATH" ]; then
    echo "📦 Applying schema..."
    sqlite3 "$DB_PATH" < "$SCHEMA_PATH"
    echo "✅ Schema applied"
else
    echo "❌ Schema file not found: $SCHEMA_PATH"
    exit 1
fi

# Verify tables
echo "🔍 Verifying tables..."
TABLES=$(sqlite3 "$DB_PATH" ".tables")
EXPECTED_TABLES="accounts transactions balances budgets budget_usage reconciliations shannon_events"
for table in $EXPECTED_TABLES; do
    if echo "$TABLES" | grep -q "\b$table\b"; then
        echo "  ✅ $table exists"
    else
        echo "  ❌ $table missing"
        exit 1
    fi
done

# Count default accounts
COUNT=$(sqlite3 "$DB_PATH" "SELECT COUNT(*) FROM accounts")
echo "📊 Default accounts created: $COUNT"

# Create default monthly budget for Fiesta (if not exists)
BUDGET_EXISTS=$(sqlite3 "$DB_PATH" "SELECT 1 FROM budgets WHERE name = 'fiesta'")
if [ -z "$BUDGET_EXISTS" ]; then
    sqlite3 "$DB_PATH" <<EOF
INSERT INTO budgets (name, period, amount, currency, start_date) VALUES
    ('fiesta', 'monthly', 500.00, 'USD', date('now')),
    ('engineering', 'monthly', 1000.00, 'USD', date('now')),
    ('marketing', 'monthly', 300.00, 'USD', date('now'));
EOF
    echo "📅 Default budgets created"
fi

echo "🎉 Dollar ledger initialized successfully!"
echo ""
echo "Next steps:"
echo "1. Check balances: ./dollar-balance.sh"
echo "2. Log a transaction: ./dollar-log.sh 'Payment received' 100.00 USD revenue"
echo "3. Generate report: ./dollar-report.sh"