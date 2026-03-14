#!/bin/bash

################################################################################
# bitnet-failover-sync.sh
#
# BitNet as failover repository:
# 1. PUSH: Backup critical files to .bitnet-failover/
# 2. PULL: Restore from failover backup
# 3. VERIFY: Check integrity
#
################################################################################

WORKSPACE_DIR="/root/.openclaw/workspace"
FAILOVER_DIR="${WORKSPACE_DIR}/.bitnet-failover"
FAILOVER_LOG="${WORKSPACE_DIR}/bitnet-failover-$(date +%Y%m%d).jsonl"
TIMESTAMP=$(date -u +%Y-%m-%dT%H:%M:%SZ)

mkdir -p "$FAILOVER_DIR"

log_failover() {
    echo "{\"timestamp\":\"$TIMESTAMP\",\"action\":\"$1\",\"status\":\"$2\",\"detail\":\"${3:-}\"}" >> "$FAILOVER_LOG"
    echo "[FAILOVER] $1: $2 ${3:+($3)}"
}

################################################################################
# PUSH
################################################################################

push_to_bitnet() {
    echo ""
    echo "╔════════════════════════════════════════════════════════════════╗"
    echo "║         PUSH: Archive Workspace → BitNet Failover              ║"
    echo "║         $(date -u +%Y-%m-%d\ %H:%M:%S\ UTC)                                    ║"
    echo "╚════════════════════════════════════════════════════════════════╝"
    echo ""
    
    echo "📥 Pushing critical files..."
    
    local pushed=0
    local total_size=0
    
    # Core identity files
    for file in SOUL.md MEMORY.md USER.md AGENTS.md IDENTITY.md; do
        if [[ -f "$WORKSPACE_DIR/$file" ]]; then
            cp "$WORKSPACE_DIR/$file" "$FAILOVER_DIR/$file.backup" 2>/dev/null && ((pushed++))
            local size=$(stat -c%s "$WORKSPACE_DIR/$file" 2>/dev/null || echo 0)
            total_size=$((total_size + size))
            echo "  ✓ $file"
        fi
    done
    
    # Tier-routing & commands
    for file in SLASH_COMMANDS.md TIER_ROUTING_DISCIPLINE.md NEW_SESSION_INFERENCE_LOGGING.md AUGMENTATION_LOG_20260314.md; do
        if [[ -f "$WORKSPACE_DIR/$file" ]]; then
            cp "$WORKSPACE_DIR/$file" "$FAILOVER_DIR/$file.backup" 2>/dev/null && ((pushed++))
            local size=$(stat -c%s "$WORKSPACE_DIR/$file" 2>/dev/null || echo 0)
            total_size=$((total_size + size))
            echo "  ✓ $file"
        fi
    done
    
    # Critical scripts
    for file in lib/tier-routing-enforcement.sh lib/slash-truthfully.sh lib/bitnet-diagnostics.sh lib/bitnet-health-orchestration.sh; do
        if [[ -f "$WORKSPACE_DIR/$file" ]]; then
            cp "$WORKSPACE_DIR/$file" "$FAILOVER_DIR/$(basename "$file").backup" 2>/dev/null && ((pushed++))
            local size=$(stat -c%s "$WORKSPACE_DIR/$file" 2>/dev/null || echo 0)
            total_size=$((total_size + size))
            echo "  ✓ $(basename "$file")"
        fi
    done
    
    # Ledgers (latest only)
    for pattern in hard-stops-registry inference-log bitnet-orchestration; do
        local latest=$(ls -t "$WORKSPACE_DIR/${pattern}"*.jsonl 2>/dev/null | head -1)
        if [[ -f "$latest" ]]; then
            cp "$latest" "$FAILOVER_DIR/$(basename "$latest").backup" 2>/dev/null && ((pushed++))
            local size=$(stat -c%s "$latest" 2>/dev/null || echo 0)
            total_size=$((total_size + size))
            echo "  ✓ $(basename "$latest")"
        fi
    done
    
    log_failover "push" "complete" "files=$pushed size=${total_size}B"
    
    echo ""
    echo "✅ Push complete"
    echo "   Files backed up: $pushed"
    echo "   Total size: $total_size bytes"
    echo "   Failover dir: $FAILOVER_DIR"
    echo ""
}

################################################################################
# PULL
################################################################################

pull_from_bitnet() {
    echo ""
    echo "╔════════════════════════════════════════════════════════════════╗"
    echo "║         PULL: Retrieve Backup ← BitNet Failover                ║"
    echo "║         $(date -u +%Y-%m-%d\ %H:%M:%S\ UTC)                                    ║"
    echo "╚════════════════════════════════════════════════════════════════╝"
    echo ""
    
    echo "📤 Pulling from BitNet failover..."
    
    local restored=0
    local backups=$(ls "$FAILOVER_DIR"/*.backup 2>/dev/null || echo "")
    
    if [[ -z "$backups" ]]; then
        echo "❌ No backups found"
        log_failover "pull" "failed" "no_backups"
        return 1
    fi
    
    for backup in $backups; do
        local filename=$(basename "$backup" .backup)
        
        # Don't overwrite if original is newer
        if [[ -f "$WORKSPACE_DIR/$filename" ]]; then
            local backup_mtime=$(stat -c%Y "$backup" 2>/dev/null || echo 0)
            local orig_mtime=$(stat -c%Y "$WORKSPACE_DIR/$filename" 2>/dev/null || echo 0)
            
            if [[ $orig_mtime -gt $backup_mtime ]]; then
                echo "  ⊘ $filename (original is newer, skipping)"
                continue
            fi
        fi
        
        cp "$backup" "$WORKSPACE_DIR/$filename" 2>/dev/null && ((restored++))
        echo "  ✓ $filename"
    done
    
    log_failover "pull" "complete" "restored=$restored"
    
    echo ""
    echo "✅ Pull complete"
    echo "   Files restored: $restored"
    echo ""
}

################################################################################
# VERIFY
################################################################################

verify_sync() {
    echo ""
    echo "╔════════════════════════════════════════════════════════════════╗"
    echo "║         VERIFY: Failover Integrity Check                       ║"
    echo "║         $(date -u +%Y-%m-%d\ %H:%M:%S\ UTC)                                    ║"
    echo "╚════════════════════════════════════════════════════════════════╝"
    echo ""
    
    echo "🔐 Verifying failover..."
    
    local verified=0
    local missing=0
    local mismatched=0
    
    local critical_files=(
        "SOUL.md"
        "MEMORY.md"
        "SLASH_COMMANDS.md"
        "TIER_ROUTING_DISCIPLINE.md"
        "lib/tier-routing-enforcement.sh"
        "lib/slash-truthfully.sh"
        "lib/bitnet-diagnostics.sh"
    )
    
    for filename in "${critical_files[@]}"; do
        local original="$WORKSPACE_DIR/$filename"
        local backup="$FAILOVER_DIR/$(basename "$filename").backup"
        
        if [[ ! -f "$original" ]]; then
            echo "  ❌ MISSING: $filename (original)"
            ((missing++))
            continue
        fi
        
        if [[ ! -f "$backup" ]]; then
            echo "  ❌ MISSING: $filename (backup)"
            ((missing++))
            continue
        fi
        
        # Compare checksums
        local orig_hash=$(sha256sum "$original" 2>/dev/null | awk '{print $1}')
        local backup_hash=$(sha256sum "$backup" 2>/dev/null | awk '{print $1}')
        
        if [[ "$orig_hash" == "$backup_hash" ]]; then
            echo "  ✅ VERIFIED: $filename"
            ((verified++))
        else
            echo "  ⚠️  MISMATCH: $filename"
            ((mismatched++))
        fi
    done
    
    echo ""
    echo "📊 Summary"
    echo "  Verified: $verified"
    echo "  Missing:  $missing"
    echo "  Mismatch: $mismatched"
    echo ""
    
    if [[ $missing -eq 0 && $mismatched -eq 0 ]]; then
        echo "✅ All critical files synchronized"
        log_failover "verify" "success" "all_verified"
    else
        echo "⚠️  Some files need attention"
        log_failover "verify" "warning" "verified=$verified missing=$missing mismatch=$mismatched"
    fi
    echo ""
}

################################################################################
# Main
################################################################################

main() {
    case "${1:-help}" in
        push)
            push_to_bitnet
            ;;
        pull)
            pull_from_bitnet
            ;;
        verify)
            verify_sync
            ;;
        all)
            push_to_bitnet
            pull_from_bitnet
            verify_sync
            ;;
        *)
            cat << USAGE
Usage: bitnet-failover-sync.sh [action]

Actions:
  push    - Backup workspace → BitNet failover
  pull    - Restore ← BitNet failover  
  verify  - Integrity check
  all     - All three phases

Examples:
  bash bitnet-failover-sync.sh push
  bash bitnet-failover-sync.sh all
USAGE
            ;;
    esac
}

main "$@"
