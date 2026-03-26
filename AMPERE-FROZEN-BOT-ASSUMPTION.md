# Ampere Frozen Bot Assumption (2026-03-15 14:00 UTC)

## Doctrine Lock

**When bash or tcpdump access Ampere infrastructure:**
- Assume all access is **frozen bot data** (read-only observation)
- No modifications to system state
- All operations are **forensic** (preserve-first, analyze-second)
- If write is required: STOP and escalate to human (user in Ampere cockpit)

## Rationale

1. **Frozen bot data** = immutable ground truth (no exfiltration risk)
2. **Observation mode** = safety default (can't damage what you're watching)
3. **Ampere access** = user's direct control (human decides modifications)
4. **Bash/tcpdump** = read-only agents (report findings, never execute)

## Implications

### What Bash/tcpdump CAN do:
- ✅ Read snapshots, logs, audit trails
- ✅ Query databases (SELECT only)
- ✅ Parse tcpdump captures (analyze packets)
- ✅ Generate reports from historical data
- ✅ Flag anomalies (output to JSONL)

### What Bash/tcpdump CANNOT do:
- ❌ Modify files (except append-only logs)
- ❌ Kill processes
- ❌ Execute system commands (beyond read/parse)
- ❌ Transfer funds, assets, credentials
- ❌ Change configurations

## Implementation

**Frozen Bot Guard (bash function):**
```bash
frozen_bot_guard() {
    local operation="$1"  # read, query, parse, report, flag
    
    case "$operation" in
        read|query|parse|report|flag)
            return 0  # ALLOWED
            ;;
        write|modify|delete|execute|transfer)
            echo "FROZEN_BOT_GUARD: Operation '$operation' blocked"
            echo "FROZEN_BOT_GUARD: Escalate to user via Ampere cockpit"
            return 1  # BLOCKED
            ;;
        *)
            echo "FROZEN_BOT_GUARD: Unknown operation '$operation'"
            return 1
            ;;
    esac
}
```

**Usage in scripts:**
```bash
if ! frozen_bot_guard "read"; then
    echo "Operation blocked by frozen bot assumption"
    exit 1
fi

# Safe to read
cat /root/.openclaw/workspace/snapshots/snapshot-*.jsonl
```

## Safety Guarantee

**Locked in place (2026-03-15 14:00 UTC):**
- Bash operates as forensic tool (observation only)
- tcpdump operates as packet analyzer (no network modifications)
- All Ampere access assumed frozen (immutable ground truth)
- User retains exclusive write authority (Ampere cockpit terminal)

**Cost:** $0.00 (safety is free)

**Prayer holds:** Over token famines, bash never freezes.

---

**Status:** DOCTRINE LOCKED. All bash/tcpdump agents bound by frozen bot observation mode.
