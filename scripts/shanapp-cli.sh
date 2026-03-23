#!/bin/bash
# Total Agency Innovation: Direct CLI-to-Ledger Mapping
# Usage: /shanapp <receiver> <amount> <note>

PYTHON_SCRIPT="/root/.openclaw/workspace/scripts/shanapp.py"
SENDER="fiesta" # Default to Steward for emulated refills

if [ "$#" -lt 3 ]; then
    echo "🏮 Usage: /shanapp <receiver_handle> <shannon_amount> <note>"
    exit 1
fi

python3 "$PYTHON_SCRIPT" "$SENDER" "$1" "$2" "$3"
