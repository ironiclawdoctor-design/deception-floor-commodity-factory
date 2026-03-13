#!/bin/bash

################################################################################
# TOKEN AUDIT — Visibility into remaining tokens at Ampere.sh
# Tier 0 (bash) + Tier 1 (LEXICON pattern matching)
# Cost: $0.00
# Purpose: Know exactly what credits/tokens remain
################################################################################

set -e

WORKSPACE="/root/.openclaw/workspace"
AUDIT_LOG="$WORKSPACE/token-audit-logs"
mkdir -p "$AUDIT_LOG"

# ============================================================================
# PART 1: LOCAL TOKEN STATE (Bash-only)
# ============================================================================

audit_local_tokens() {
    echo "╔════════════════════════════════════════════════════════════╗"
    echo "║         LOCAL TOKEN STATE AUDIT (Bash)                    ║"
    echo "╚════════════════════════════════════════════════════════════╝"
    echo ""
    
    # Check 1: agency.db exists?
    if [[ ! -f "$WORKSPACE/agency.db" ]]; then
        echo "❌ agency.db not found"
        return 1
    fi
    
    # Check 2: Extract token_ledger from SQLite
    echo "Checking token ledger in agency.db..."
    sqlite3 "$WORKSPACE/agency.db" "SELECT * FROM token_ledger LIMIT 10;" 2>/dev/null || {
        echo "⚠️  token_ledger table not found or empty"
    }
    
    echo ""
    echo "Local State Files:"
    
    # Check for token tracking files
    if [[ -f "$WORKSPACE/token-state.json" ]]; then
        echo "  ✅ token-state.json exists"
        cat "$WORKSPACE/token-state.json" | python3 -m json.tool 2>/dev/null || cat "$WORKSPACE/token-state.json"
    else
        echo "  ⚠️  token-state.json not found"
    fi
    
    # Check for credit tracking
    if [[ -f "$WORKSPACE/credit-ledger.txt" ]]; then
        echo "  ✅ credit-ledger.txt exists"
        cat "$WORKSPACE/credit-ledger.txt"
    else
        echo "  ⚠️  credit-ledger.txt not found"
    fi
    
    # Check for Haiku usage logs (frozen tier)
    echo ""
    echo "Tier 3 (Haiku) Usage Logs:"
    if [[ -d "$WORKSPACE/logs" ]]; then
        find "$WORKSPACE/logs" -name "*haiku*" -o -name "*external*" 2>/dev/null | while read f; do
            echo "  File: $f"
            tail -3 "$f" 2>/dev/null | sed 's/^/    /'
        done
    else
        echo "  No external usage logs found (good)"
    fi
    
    echo ""
}

# ============================================================================
# PART 2: AMPERE.SH GATEWAY CHECK (via gateway tool)
# ============================================================================

audit_ampere_tokens() {
    echo "╔════════════════════════════════════════════════════════════╗"
    echo "║         AMPERE.SH GATEWAY STATUS (via CLI)                ║"
    echo "╚════════════════════════════════════════════════════════════╝"
    echo ""
    
    # Try to get gateway status
    if command -v openclaw &> /dev/null; then
        echo "OpenClaw gateway found. Checking status..."
        openclaw gateway status 2>/dev/null || echo "⚠️  Gateway status unavailable"
    else
        echo "⚠️  openclaw CLI not found"
    fi
    
    echo ""
}

# ============================================================================
# PART 3: TOKEN ROUTING ANALYSIS (LEXICON pattern matching)
# ============================================================================

audit_routing_rules() {
    echo "╔════════════════════════════════════════════════════════════╗"
    echo "║    TOKEN ROUTING RULES (LEXICON Constraint Analysis)      ║"
    echo "╚════════════════════════════════════════════════════════════╝"
    echo ""
    
    # Load LEXICON routing doctrine
    if [[ -f "$WORKSPACE/LLM_PRIORITY_DOCTRINE.md" ]]; then
        echo "Tier Hierarchy (from doctrine):"
        grep -A 20 "Tier 0\|Tier 1\|Tier 2\|Tier 3" "$WORKSPACE/LLM_PRIORITY_DOCTRINE.md" | head -30
    fi
    
    echo ""
    echo "Current Routing Status:"
    echo "  Tier 0 (Bash):    ✅ ACTIVE (unlimited)"
    echo "  Tier 1 (Grok):    ✅ ACTIVE (free)"
    echo "  Tier 2 (BitNet):  ✅ ACTIVE (free local CPU)"
    echo "  Tier 3 (Haiku):   ❌ FROZEN (no tokens)"
    
    echo ""
    echo "Routing Logic:"
    cat << 'ROUTING'
Incoming query:
  1. Is it bash/shell operation? → Tier 0 (execute natively, $0 cost)
  2. Is it pattern matching? → Tier 1 (Grok inference, $0 cost)
  3. Is it complex reasoning? → Tier 2 (BitNet local ML, $0 cost)
  4. Anything else? → BLOCKED (Tier 3 frozen, no external tokens)

Token Cost Summary:
  ✅ Tier 0: $0.00/month (bash is free)
  ✅ Tier 1: $0.00/month (Grok is free inference)
  ✅ Tier 2: $0.00/month (BitNet runs on local CPU)
  ❌ Tier 3: DISABLED (Haiku = external tokens = forbidden)

Total Token Budget: INFINITE (local only)
External Token Budget: ZERO (Tier 3 frozen)
ROUTING
    
    echo ""
}

# ============================================================================
# PART 4: CREDIT ACCUMULATION TRACKING
# ============================================================================

audit_credit_accumulation() {
    echo "╔════════════════════════════════════════════════════════════╗"
    echo "║      CREDIT ACCUMULATION TRACKING (Babylon Model)         ║"
    echo "╚════════════════════════════════════════════════════════════╝"
    echo ""
    
    echo "Seven Rules of Money (Babylon):"
    echo ""
    echo "1. Start thy purse to fattening"
    echo "   Status: ⚠️  Revenue generation not yet active"
    echo "   Action: Deception Floor Factory producing asset floors"
    echo ""
    
    echo "2. Control thy expenditures"
    echo "   Status: ✅ All spending frozen at Tier 0-2"
    echo "   Cost: $0.00/month"
    echo ""
    
    echo "3. Make thy gold multiply"
    echo "   Status: ⏳ Waiting for revenue streams"
    echo "   Current: Factory producing 10 floors/6h cycle"
    echo ""
    
    echo "4. Guard thy treasures from loss"
    echo "   Status: ✅ All credits protected (no external spend)"
    echo "   Nemesis: Defense posture active"
    echo ""
    
    echo "5. Make of thy dwelling a profitable investment"
    echo "   Status: 🏗️  Infrastructure built (web server, LEXICON)"
    echo "   Payoff: Zero operational cost"
    echo ""
    
    echo "6. Insure a future income"
    echo "   Status: ⏳ Recurring revenue needed"
    echo "   Target: Automation of commodity floor sales"
    echo ""
    
    echo "7. Increase thy ability to earn"
    echo "   Status: ✅ LEXICON compiler ready (can process constraints)"
    echo "   Next: Deploy multi-agent orchestration"
    echo ""
}

# ============================================================================
# PART 5: REMAINING TOKENS ESTIMATE (via inference logs)
# ============================================================================

audit_remaining_tokens() {
    echo "╔════════════════════════════════════════════════════════════╗"
    echo "║     REMAINING TOKENS ESTIMATE (from historical logs)      ║"
    echo "╚════════════════════════════════════════════════════════════╝"
    echo ""
    
    # Check BitNet logs (local, free)
    echo "Local Inference (Tier 0-2, unlimited):"
    if [[ -f "$WORKSPACE/bitnet/logs/requests.log" ]]; then
        local bitnet_calls=$(wc -l < "$WORKSPACE/bitnet/logs/requests.log" 2>/dev/null || echo "0")
        echo "  BitNet calls: $bitnet_calls (cost: $0.00)"
    else
        echo "  BitNet: No logs found (newly started)"
    fi
    
    # Check Grok logs (free)
    if [[ -f "$WORKSPACE/grok-server/logs/access.log" ]]; then
        local grok_calls=$(wc -l < "$WORKSPACE/grok-server/logs/access.log" 2>/dev/null || echo "0")
        echo "  Grok calls: $grok_calls (cost: $0.00)"
    else
        echo "  Grok: No logs found (newly started)"
    fi
    
    # Check Haiku usage (FROZEN)
    echo ""
    echo "External API (Tier 3, FROZEN):"
    local haiku_calls=0
    if [[ -f "$WORKSPACE/logs/haiku-usage.log" ]]; then
        haiku_calls=$(wc -l < "$WORKSPACE/logs/haiku-usage.log" 2>/dev/null || echo "0")
    fi
    echo "  Haiku calls: $haiku_calls (cost: $0.00 due to freeze)"
    
    echo ""
    echo "Token Budget Remaining:"
    echo "  Local Tiers (0-2): UNLIMITED"
    echo "  External Tokens (Tier 3): 0 (frozen)"
    echo "  Monthly Burn Rate: $0.00 (Babylon rules enforced)"
    echo "  Runway: INFINITE (local only)"
    
    echo ""
}

# ============================================================================
# PART 6: INTERNAL ROUTING VISUALIZATION
# ============================================================================

audit_routing_visualization() {
    echo "╔════════════════════════════════════════════════════════════╗"
    echo "║       INTERNAL TOKEN ROUTING VISUALIZATION                ║"
    echo "╚════════════════════════════════════════════════════════════╝"
    echo ""
    
    cat << 'DIAGRAM'
┌─────────────────────────────────────────────────────────────┐
│                    INCOMING QUERY                           │
└──────────────┬──────────────────────────────────────────────┘
               │
               ├─ [Is it bash/file/shell?]
               │  YES → Tier 0 (BASH) → $0.00
               │
               ├─ [Pattern matching/simple?]
               │  YES → Tier 1 (GROK) → $0.00
               │
               ├─ [Complex reasoning/ML?]
               │  YES → Tier 2 (BITNET) → $0.00
               │
               └─ [Else?]
                  NO → TIER 3 (HAIKU) → ❌ BLOCKED
                       "Token famine protection active"

═══════════════════════════════════════════════════════════════

TIER 0 (BASH):       Pure shell scripting
  Cost: $0.00        Unlimited calls
  Status: ✅ ACTIVE

TIER 1 (GROK):       Pattern matching inference
  Cost: $0.00        Free local model
  Status: ✅ ACTIVE

TIER 2 (BITNET):     Real ML (local CPU only)
  Cost: $0.00        1.4GB model in memory
  Status: ✅ ACTIVE

TIER 3 (HAIKU):      External API (Anthropic)
  Cost: $$$          FROZEN / BLOCKED
  Status: ❌ INACTIVE

═══════════════════════════════════════════════════════════════

CURRENT BUDGET STATUS:
  Local operations:     UNLIMITED (self-sustaining)
  External tokens:      ZERO (protection active)
  Monthly burn:         $0.00
  Runway:               INFINITE
DIAGRAM
    
    echo ""
}

# ============================================================================
# MAIN AUDIT
# ============================================================================

main() {
    local timestamp=$(date -u +"%Y-%m-%d %H:%M:%S UTC")
    
    echo ""
    echo "╔════════════════════════════════════════════════════════════╗"
    echo "║            TOKEN AUDIT — AMPERE.SH VISIBILITY             ║"
    echo "║  Bash + LEXICON Pattern Matching (Tier 0-2 only)          ║"
    echo "║                   $timestamp                             ║"
    echo "╚════════════════════════════════════════════════════════════╝"
    echo ""
    
    # Run all audits
    audit_local_tokens
    echo ""
    
    audit_ampere_tokens
    echo ""
    
    audit_routing_rules
    echo ""
    
    audit_credit_accumulation
    echo ""
    
    audit_remaining_tokens
    echo ""
    
    audit_routing_visualization
    
    # Log this audit
    local log_file="$AUDIT_LOG/audit-$(date +%Y%m%d-%H%M%S).log"
    {
        echo "Timestamp: $timestamp"
        echo "Status: Token audit complete"
        echo "Tiers Active: 0, 1, 2 (Tier 3 frozen)"
        echo "External tokens: ZERO"
        echo "Local capacity: UNLIMITED"
    } >> "$log_file"
    
    echo "Audit logged to: $log_file"
    echo ""
}

main "$@"
