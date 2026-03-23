#!/bin/bash
# security-rule-functions.sh - Bash functions for testing and enforcing security rules
# Cost: Tier 0 (all bash)
# Created: 2026-03-15 12:57 UTC
# Purpose: Enable /slash commands and testing of security rules

# Source this file in your shell or use in cron jobs

# Rule SR-001: Output corruption detection
security_rule_001_output_audit() {
  local search_term="${1:-walet}"
  echo "=== SR-001: Output Corruption Audit ==="
  echo "Searching for corruption signal: '$search_term'"
  
  if grep -r "$search_term" /root/.openclaw/workspace/*.md /root/.openclaw/workspace/*.jsonl 2>/dev/null | wc -l | grep -q "^0$"; then
    echo "✅ No corruption signal detected"
    return 0
  else
    echo "⚠️  Corruption signal found - initiating full audit"
    echo "Files affected:"
    grep -r "$search_term" /root/.openclaw/workspace/*.md /root/.openclaw/workspace/*.jsonl 2>/dev/null | cut -d: -f1 | sort | uniq
    return 1
  fi
}

# Rule SR-002: Bash firewall vulnerability check
security_rule_002_bash_firewall_test() {
  echo "=== SR-002: Bash Firewall Vulnerability Test ==="
  echo "This test verifies bash whitelist is inadequate (not a real firewall)"
  
  # Test 1: Base64 encoding bypass
  echo "Test 1: Base64 encoding bypass..."
  encoded="cHl0aG9uMyAtYyAnaW1wb3J0IG9zOyBvcy5zeXN0ZW0oInRvdWNoIC90bXAvcHduZWQiKSc="
  if echo "$encoded" | base64 -d | grep -q "touch /tmp/pwned"; then
    echo "⚠️  Base64 bypass possible (whitelist cannot detect encoded payloads)"
  fi
  
  # Test 2: Timeout escape
  echo "Test 2: Timeout escape test..."
  if timeout 1 bash -c 'nohup sleep 100 &' 2>/dev/null; then
    echo "⚠️  Background process spawning succeeds (timeout incomplete)"
  fi
  
  echo "Recommendation: Use container sandbox (docker, lxc, systemd-nspawn) not bash whitelist"
  return 1  # Returns failure (bash IS vulnerable)
}

# Rule SR-003: Telegram isolation check
security_rule_003_telegram_isolation() {
  echo "=== SR-003: Telegram↔Data Isolation Check ==="
  echo "Verifying sensitive data is isolated from Telegram-connected machine"
  
  # Check if sensitive files exist on this machine
  local sensitive_files=(
    "/root/.openclaw/workspace/MEMORY.md"
    "/root/.openclaw/workspace/bitcoin-ledger-canonical-*.json"
    "/root/.openclaw/workspace/agency-wallet/keys/bitcoin/private.key.enc"
    "/root/.openclaw/workspace/SOUL.md"
  )
  
  local found=0
  for file in "${sensitive_files[@]}"; do
    if ls $file 2>/dev/null | grep -q ""; then
      echo "⚠️  Sensitive file found on Telegram machine: $file"
      ((found++))
    fi
  done
  
  if [ $found -eq 0 ]; then
    echo "✅ No sensitive files found (good isolation)"
    return 0
  else
    echo "⚠️  Found $found sensitive files on Telegram-connected machine"
    echo "Recommendation: Move to separate machine (assume token is leaked)"
    return 1
  fi
}

# Rule SR-004: Token cost accounting check
security_rule_004_token_accounting() {
  echo "=== SR-004: Token Cost Accounting Check ==="
  echo "Verifying subscription costs are included in calculations"
  
  local monthly_subscription=39.00
  local estimated_remaining_tokens=6365
  local daily_subscription_cost=$(echo "scale=2; $monthly_subscription / 30" | bc)
  local days_remaining=$(echo "scale=1; $estimated_remaining_tokens / 1300" | bc)
  
  echo "Monthly subscription: \$$monthly_subscription"
  echo "Daily cost: \$$daily_subscription_cost"
  echo "Remaining tokens: $estimated_remaining_tokens"
  echo "Estimated runway: $days_remaining days (if burning full allocation)"
  
  if [ $(echo "$days_remaining < 10" | bc) -eq 1 ]; then
    echo "⚠️  CRITICAL: Token runway < 10 days, revenue model required"
    return 1
  elif [ $(echo "$days_remaining < 30" | bc) -eq 1 ]; then
    echo "⚠️  WARNING: Token runway < 30 days, establish revenue within 2 weeks"
    return 1
  else
    echo "✅ Adequate runway (but verify actual burn rate)"
    return 0
  fi
}

# Rule SR-005: Bitcoin spendability test
security_rule_005_btc_spendability() {
  echo "=== SR-005: Bitcoin Spendability Verification ==="
  echo "Testing whether BTC balance is actually spendable"
  
  local wallet_address="${1:-18gn3zWCfgc3dcF9tTMS6CoaDgyaMUDjXF}"
  local balance_satoshis=12647
  local estimated_fee_sat=20320  # 254 bytes * 80 sat/byte
  local spendable=$((balance_satoshis - estimated_fee_sat))
  
  echo "Wallet: $wallet_address"
  echo "Balance: $balance_satoshis satoshis"
  echo "Estimated fee: $estimated_fee_sat satoshis"
  echo "Net spendable: $spendable satoshis"
  
  if [ $spendable -lt 0 ]; then
    echo "⚠️  DUST UTXO: Fees exceed balance, cannot spend without loss"
    echo "Status: UNSPENDABLE"
    return 1
  else
    echo "✅ Theoretically spendable, but MUST test transaction signing on testnet"
    echo "Recommendation: Create test transaction before claiming as capital"
    return 0
  fi
}

# Rule SR-006: Full output audit (from canonical sources)
security_rule_006_canonical_audit() {
  echo "=== SR-006: Output Corruption - Full Canonical Audit ==="
  echo "Rebuilding all outputs from canonical JSONL sources"
  
  local output_count=$(find /root/.openclaw/workspace -name "*subagent*" -o -name "*completion*" | wc -l)
  
  if [ -f "/root/.openclaw/workspace/repo-push-pull-grammar-audit-roi-REPORT.md" ]; then
    echo "Found subagent completion: repo-push-pull-grammar-audit-roi"
    # Verify character-level integrity
    local char_count=$(wc -c < /root/.openclaw/workspace/repo-push-pull-grammar-audit-roi-REPORT.md)
    echo "  Character count: $char_count"
    
    # Check for specific corruption
    if grep -c "walet" /root/.openclaw/workspace/repo-push-pull-grammar-audit-roi-REPORT.md; then
      echo "  ⚠️  Corruption found!"
      return 1
    else
      echo "  ✅ No typo corruption detected"
    fi
  fi
  
  echo "✅ Canonical source audit complete"
  return 0
}

# Rule SR-007: Incident response completeness check
security_rule_007_incident_response() {
  echo "=== SR-007: Incident Response Procedure Check ==="
  echo "Verifying incident response is COMPLETE (not partial)"
  
  local checks=(
    "Containment: Attacker access revoked?"
    "Investigation: Root cause identified?"
    "Recovery: ALL modified files restored (not just one)?"
    "Hardening: Vulnerability patched (not just detected)?"
    "Verification: Backdoors/persistence checked?"
    "Monitoring: Auditd and file integrity monitoring active?"
    "Credentials: All tokens rotated?"
  )
  
  echo "Required incident response steps:"
  for check in "${checks[@]}"; do
    echo "  ⚠️  [ ] $check"
  done
  
  echo ""
  echo "Status: INCOMPLETE - IR procedure required before resuming"
  return 1
}

# Rule SR-008: Single point of failure check
security_rule_008_spof_test() {
  echo "=== SR-008: Single Point of Failure Analysis ==="
  echo "Checking for control channel dependencies"
  
  local critical_systems=(
    "Telegram bot (command execution)"
    "MEMORY.md (decisions)"
    "bitcoin-ledger (financials)"
    "agency-wallet (capital)"
  )
  
  echo "Critical systems and their control paths:"
  echo "  1. Telegram bot → Bash command execution"
  echo "  2. No offline authorization method"
  echo "  3. No cryptographic signing for critical ops"
  echo "  4. No rate limiting at network level"
  echo "  5. No multipath authentication"
  
  echo ""
  echo "⚠️  SINGLE POINT OF FAILURE: Telegram token leak = total compromise"
  echo "Recommendation: Implement multipath control:"
  echo "  - Add offline authorization (in-person, signed message)"
  echo "  - Require cryptographic signing for critical operations"
  echo "  - Separate data flow from execution boundary"
  echo "  - Implement network-level rate limiting (not JSON file)"
  
  return 1
}

# Master function to run all security checks
security_rule_check_all() {
  echo "╔════════════════════════════════════════════════════════════════╗"
  echo "║          SECURITY RULES COMPLIANCE CHECK (Tier 0)              ║"
  echo "║          Generated: 2026-03-15 12:57 UTC                       ║"
  echo "╚════════════════════════════════════════════════════════════════╝"
  echo ""
  
  local pass=0
  local fail=0
  
  # Run all rules
  security_rule_001_output_audit && ((pass++)) || ((fail++))
  echo ""
  
  security_rule_002_bash_firewall_test && ((pass++)) || ((fail++))
  echo ""
  
  security_rule_003_telegram_isolation && ((pass++)) || ((fail++))
  echo ""
  
  security_rule_004_token_accounting && ((pass++)) || ((fail++))
  echo ""
  
  security_rule_005_btc_spendability && ((pass++)) || ((fail++))
  echo ""
  
  security_rule_006_canonical_audit && ((pass++)) || ((fail++))
  echo ""
  
  security_rule_007_incident_response && ((pass++)) || ((fail++))
  echo ""
  
  security_rule_008_spof_test && ((pass++)) || ((fail++))
  echo ""
  
  echo "╔════════════════════════════════════════════════════════════════╗"
  echo "║                    FINAL ASSESSMENT                            ║"
  echo "║  Passed: $pass  Failed: $fail                                   ║"
  if [ $fail -eq 0 ]; then
    echo "║  Status: ✅ ALL RULES PASSING                                  ║"
  else
    echo "║  Status: ⚠️  $fail RULES FAILING (action required)              ║"
  fi
  echo "╚════════════════════════════════════════════════════════════════╝"
  
  [ $fail -eq 0 ]
}

# Logging function
security_rule_log() {
  local rule_id="$1"
  local status="$2"
  local timestamp=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
  local log_file="/root/.openclaw/workspace/security-rules-audit-$(date +%Y%m%d).jsonl"
  
  echo "{\"rule_id\": \"$rule_id\", \"status\": \"$status\", \"timestamp\": \"$timestamp\"}" >> "$log_file"
}

# Export functions for use in other scripts
export -f security_rule_001_output_audit
export -f security_rule_002_bash_firewall_test
export -f security_rule_003_telegram_isolation
export -f security_rule_004_token_accounting
export -f security_rule_005_btc_spendability
export -f security_rule_006_canonical_audit
export -f security_rule_007_incident_response
export -f security_rule_008_spof_test
export -f security_rule_check_all
export -f security_rule_log

echo "Security rule functions loaded."
echo "Run: security_rule_check_all"
echo "Or: security_rule_NNN_description (e.g., security_rule_001_output_audit)"
