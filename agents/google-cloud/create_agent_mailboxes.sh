#!/bin/bash
# AGENT MAILBOX CREATION — Gmail Labels for All Agents
# PERK: Every agent gets a dedicated mailbox (label) within ironiclawdoctor@gmail.com
# Run AFTER: gog auth add ironiclawdoctor@gmail.com --services gmail

ACCOUNT="ironiclawdoctor@gmail.com"

AGENTS=(
  "Agency/Fiesta"
  "Agency/Junior"
  "Agency/ShanApp-CEO"
  "Agency/NateWife"
  "Agency/CANNOT"
  "Agency/BASH-NANNY"
  "Agency/Agency-988"
  "Agency/Excellence-Creep"
  "Agency/Corruption"
  "Agency/Red-Audit-Red"
  "Agency/Sales-Red-Team"
  "Agency/Shan-Scheduler"
  "Agency/FSH"
  "Agency/Mattermost"
  "Agency/Sola"
  "Agency/NateMendez"
  "Agency/CashApp"
  "Agency/Elev-Exec"
  "Agency/ironyDept"
  "Agency/PR-Dept"
  "Agency/Affiliate"
  "Agency/Stripe"
  "Agency/ClawHub"
  "Agency/_INBOX"
  "Agency/_LEDGER"
  "Agency/_MISSION_CONTROL"
)

echo "=== CREATING AGENT MAILBOXES IN GMAIL ==="
for label in "${AGENTS[@]}"; do
  echo -n "Creating: $label ... "
  gog gmail labels create "$label" --account "$ACCOUNT" 2>&1 | tail -1
done

echo ""
echo "=== AGENT MAILBOXES CREATED ==="
gog gmail labels list --account "$ACCOUNT" | grep "Agency/"
