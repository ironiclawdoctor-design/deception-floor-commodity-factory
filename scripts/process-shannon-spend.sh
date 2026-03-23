#!/bin/bash
# process-shannon-spend.sh - Process Shannon reinvestment into Agency silos
# usage: ./process-shannon-spend.sh <agent_id> <amount> <silo> <description>

AGENT_ID=$1
AMOUNT=$2
SILO=$3
DESCRIPTION=$4

ENTROPY_DB="/root/.openclaw/workspace/entropy_ledger.db"

if [ -z "$AGENT_ID" ] || [ -z "$AMOUNT" ] || [ -z "$SILO" ]; then
    echo "Usage: $0 <agent_id> <amount> <silo> <description>"
    exit 1
fi

# 1. Verify Silo exists
case $SILO in
    infrastructure|governance|investment) ;;
    *) echo "Error: Silo must be infrastructure, governance, or investment."; exit 1 ;;
esac

# 2. Check balance
BALANCE=$(sqlite3 "$ENTROPY_DB" "SELECT balance FROM agents WHERE agent_id='$AGENT_ID';")
if [ -z "$BALANCE" ]; then BALANCE=0; fi

# Allow negative balance (Debt Economy) but log it
NEW_BALANCE=$((BALANCE - AMOUNT))

# 3. Record the transaction
sqlite3 "$ENTROPY_DB" <<EOF
INSERT INTO transactions (agent_id, amount, transaction_type, description, timestamp)
VALUES ('$AGENT_ID', -$AMOUNT, 'spend_$SILO', '$DESCRIPTION', datetime('now'));

UPDATE agents SET balance = $NEW_BALANCE WHERE agent_id = '$AGENT_ID';
EOF

echo "✅ Spend Processed: $AMOUNT Shannon from $AGENT_ID into $SILO."
echo "   New Balance: $NEW_BALANCE Shannon."
echo "   REINVESTMENT: $DESCRIPTION"
