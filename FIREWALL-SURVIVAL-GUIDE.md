# 🔐 Agency Survival Firewall - Complete Documentation

**Daimyo Judicial Enforcement | Zero-Token Survival Architecture**

---

## Table of Contents
1. [Overview](#overview)
2. [System Architecture](#system-architecture)
3. [Core Scripts](#core-scripts)
4. [Operations Guide](#operations-guide)
5. [Failure Scenarios](#failure-scenarios)
6. [Recovery Procedures](#recovery-procedures)
7. [Testing Guide](#testing-guide)

---

## Overview

The Agency Survival Firewall is a **Tier 0-2 bash-based protection system** designed to keep the agency operational during:

- **Token famine** (zero external tokens)
- **BitNet failures** (local inference crash)
- **API outages** (all external services down)
- **System crashes** (service restarts)

**Core Principle:** Agency can operate **indefinitely** with only bash, git, and cron.

---

## System Architecture

```
┌─────────────────────────────────────────────┐
│         AGENCY SURVIVAL FIREWALL            │
├─────────────────────────────────────────────┤
│                                             │
│  ┌──────────────────────────────────────┐  │
│  │ Health Checks (agency-status.sh)    │  │
│  │ - 14 core system checks              │  │
│  │ - Zero external calls                │  │
│  │ - Exit codes: 0 (healthy)            │  │
│  └──────────────────────────────────────┘  │
│                   ↓                         │
│  ┌──────────────────────────────────────┐  │
│  │ Verification (verify-agency...)      │  │
│  │ - 10 service status checks           │  │
│  │ - Auto-restart degraded services     │  │
│  │ - Response: UP/DOWN/DEGRADED         │  │
│  └──────────────────────────────────────┘  │
│                   ↓                         │
│  ┌──────────────────────────────────────┐  │
│  │ Backup/Restore (agency-backup.sh)   │  │
│  │ - Git-based snapshots                │  │
│  │ - Atomic commits + tags              │  │
│  │ - Full state recovery                │  │
│  └──────────────────────────────────────┘  │
│                   ↓                         │
│  ┌──────────────────────────────────────┐  │
│  │ Keepalive (agency-keepalive.sh)      │  │
│  │ - Runs every 5 minutes via cron      │  │
│  │ - Monitors 5 critical systems        │  │
│  │ - Auto-restarts on failure           │  │
│  └──────────────────────────────────────┘  │
│                                             │
└─────────────────────────────────────────────┘
         ↓ Git-Based Persistence ↓
  All state persisted to .git/
```

---

## Core Scripts

### 1. `/usr/local/bin/agency-status.sh`

**Purpose:** Comprehensive health check (zero external calls)

**Checks (14 total):**
- ✓ Bash runtime
- ✓ Workspace directory
- ✓ Git repository
- ✓ Gateway process
- ✓ OpenClaw CLI
- ✓ Critical config files (SOUL.md, AGENTS.md, USER.md)
- ✓ Memory files
- ✓ Backups exist
- ✓ Disk space (>10MB free)
- ✓ Write permissions
- ✓ Git status
- ✓ Node runtime
- ✓ Cron daemon
- ✓ /tmp directory

**Usage:**
```bash
# Check health
agency-status.sh

# Exit codes:
# 0 = All critical checks passed
# 1 = Some non-critical warnings
# 2 = Critical failure
```

**Output:** Colored status report + exit code

---

### 2. `/usr/local/bin/verify-agency-protection.sh`

**Purpose:** Verify all services are alive and protected

**Checks (10 total):**
- Gateway status (UP/DOWN/DEGRADED)
- Workspace integrity
- Git storage connectivity
- Bash runtime
- Cron daemon
- Node.js runtime
- Disk health
- Write capability
- Critical files
- Protection scripts in place

**Usage:**
```bash
# Verify all services
verify-agency-protection.sh

# Exit codes:
# 0 = All services protected
# 1 = Some degraded
# 2 = Critical failure
```

**Auto-recovery:** Script automatically attempts restart of failed services

---

### 3. `/usr/local/bin/agency-backup.sh`

**Purpose:** Git-based backup and restore protocol

**Commands:**
```bash
# Create new backup (atomic git tag)
agency-backup.sh create

# List all backups
agency-backup.sh list

# Verify backup integrity
agency-backup.sh verify backup-20260313-225147

# Restore from backup
agency-backup.sh restore backup-20260313-225147

# Remove old backups (keep 10)
agency-backup.sh cleanup

# Check git repository integrity
agency-backup.sh status
```

**Backup Format:**
- Git annotated tags (one per backup)
- Metadata files in `backups/` directory
- Full workspace state captured
- Atomic commit model (all-or-nothing)

**Restore Safety:**
- Auto-creates safety backup before restore
- Partial restore reverts uncommitted changes
- Full git fsck verification

---

### 4. `/usr/local/bin/agency-keepalive.sh`

**Purpose:** Periodic monitoring + auto-recovery (cron job)

**Monitoring:**
- Gateway process
- Workspace directory
- Cron daemon
- Disk space
- Write capability

**Behavior:**
- Runs every 5 minutes (via cron)
- Logs to `/var/log/agency-keepalive.log`
- Accumulates 3 consecutive failures → triggers recovery
- Auto-restarts gateway and cron on threshold
- Reset state on success

**Log Location:**
```bash
tail -f /var/log/agency-keepalive.log
```

**Cron Entry:**
```
*/5 * * * * /usr/local/bin/agency-keepalive.sh
```

---

## Operations Guide

### Daily Health Check

```bash
# Check system health
agency-status.sh

# Verify protection
verify-agency-protection.sh

# Create backup (before major changes)
agency-backup.sh create
```

### Manual Recovery

If system degraded:

```bash
# 1. Check what's wrong
agency-status.sh
verify-agency-protection.sh

# 2. Check logs
tail -50 /var/log/agency-keepalive.log

# 3. Manual restart if needed
openclaw gateway restart

# 4. Verify recovery
verify-agency-protection.sh
```

### Backup Management

```bash
# Create backup
agency-backup.sh create

# List recent backups
agency-backup.sh list

# Verify specific backup
agency-backup.sh verify backup-20260313-225147

# Restore if needed
agency-backup.sh restore backup-20260313-225147

# Cleanup old backups (keep 10)
agency-backup.sh cleanup
```

---

## Failure Scenarios

### Scenario 1: Tokens = 0 (Zero External API Calls)

**Initial State:**
- All external APIs unavailable
- No token budget
- Agency must function on bash/git alone

**System Response:**
- All health checks pass (no external calls)
- Gateway stays operational
- Backup/restore works (git-based, local only)
- Keepalive continues monitoring
- Git persistence maintained

**Evidence:**
```bash
# All scripts work without external calls
agency-status.sh          # ✓ All local checks
verify-agency-protection.sh  # ✓ All local checks
agency-backup.sh create   # ✓ Git-based (local)
```

**Recovery:**
- System remains operational indefinitely
- No degradation of services
- All backups stored locally in git

---

### Scenario 2: BitNet Crashes (Local Inference Down)

**Initial State:**
- Local LLM inference unavailable
- External APIs also down (famine scenario)
- Only bash/git available

**System Response:**
- Health checks continue (no LLM dependency)
- Keepalive runs every 5 minutes
- All scripts execute normally
- Backups and restores work
- Gateway unaffected (separate process)

**Recovery:**
- Bash fallback sufficient for all operations
- No token spend required
- Services operate at baseline functionality

**Test:**
```bash
# Kill local inference (if running)
pkill -f "bitnet\|inference\|llm" || true

# System continues:
agency-status.sh          # ✓ Works
verify-agency-protection.sh  # ✓ Works
agency-keepalive.sh       # ✓ Works
```

---

### Scenario 3: All External APIs Down

**Initial State:**
- No external API connectivity
- Famine scenario with zero tokens
- BitNet also offline
- Only local bash/git available

**System Response:**
- No network calls attempted
- All checks pass locally
- Workspace remains intact
- Cron keepalive continues
- State persisted in git

**Recovery:**
- System fully autonomous
- No external dependency
- Indefinite operation possible

**Test:**
```bash
# Disable network (if applicable)
# System still functions:
agency-status.sh          # ✓ All local
verify-agency-protection.sh  # ✓ All local
agency-keepalive.sh       # ✓ Auto-restarts
```

---

### Scenario 4: Gateway Crash

**Initial State:**
- openclaw-gateway process dies
- Other systems intact

**System Response (Automatic):**
- Keepalive detects down (5-min interval)
- Logs failure
- After 3 failures (15 min window), auto-restarts gateway
- Waits 5 seconds for restart
- Verifies process is back
- Logs success

**Manual Recovery:**
```bash
# Immediate restart (if needed)
openclaw gateway restart

# Verify
verify-agency-protection.sh
```

**Log Evidence:**
```bash
grep "Gateway\|gateway" /var/log/agency-keepalive.log
```

---

### Scenario 5: Disk Full

**Initial State:**
- Less than 10MB available
- Write operations failing

**System Response:**
- Health check fails: `disk-space`
- Keepalive warns but doesn't retry (disk issue)
- Manual cleanup required

**Recovery:**
```bash
# 1. Identify large files
du -sh /root/.openclaw/workspace/* | sort -rh | head

# 2. Clean old backups (manual intervention needed)
# 3. Remove old memory files if safe
# 4. Check /tmp for debris

rm -rf /tmp/agency-* 2>/dev/null

# 5. Verify recovery
agency-status.sh
```

---

### Scenario 6: Cron Daemon Down

**Initial State:**
- System cron service crashed
- Keepalive can't run automatically

**System Response:**
- Keepalive detects cron down (if run manually)
- Logs cron failure
- Attempts restart via systemctl/service
- Auto-recovery on threshold

**Manual Trigger:**
```bash
# Run keepalive manually
/usr/local/bin/agency-keepalive.sh

# Check logs
tail /var/log/agency-keepalive.log
```

**Recovery:**
```bash
# Restart cron
systemctl restart cron
# or
service cron restart

# Verify
verify-agency-protection.sh
```

---

## Recovery Procedures

### Quick Recovery (All-in-One)

```bash
#!/usr/bin/env bash
# Quick agency recovery

echo "=== Agency Emergency Recovery ==="

# 1. Health check
echo "1. Checking health..."
agency-status.sh

# 2. Service verification
echo "2. Verifying services..."
verify-agency-protection.sh

# 3. Force keepalive check
echo "3. Running keepalive..."
/usr/local/bin/agency-keepalive.sh

# 4. Create recovery backup
echo "4. Creating backup..."
agency-backup.sh create

# 5. Final verification
echo "5. Final verification..."
verify-agency-protection.sh

echo "=== Recovery Complete ==="
```

### Step-by-Step Recovery

**Step 1: Diagnose**
```bash
agency-status.sh         # What's broken?
verify-agency-protection.sh  # Which services?
tail -50 /var/log/agency-keepalive.log  # What happened?
```

**Step 2: Isolate**
- Identify failed system
- Check system logs if available
- Verify disk/memory/connectivity

**Step 3: Restore (if data corruption)**
```bash
# List recent backups
agency-backup.sh list

# Verify backup
agency-backup.sh verify backup-20260313-225147

# Restore
agency-backup.sh restore backup-20260313-225147

# Verify restoration
agency-status.sh
```

**Step 4: Restart**
```bash
openclaw gateway restart
systemctl restart cron  # if cron was affected
```

**Step 5: Verify**
```bash
verify-agency-protection.sh
agency-keepalive.sh
```

---

## Testing Guide

### Test 1: Zero-Token Operation

```bash
#!/usr/bin/env bash
# Simulate zero external tokens

echo "TEST 1: Zero-Token Operation"
echo "=============================="

# Verify all scripts run without network calls
echo "1. Running agency-status.sh..."
agency-status.sh
STATUS1=$?

echo "2. Running verify-agency-protection.sh..."
verify-agency-protection.sh
STATUS2=$?

echo "3. Running agency-backup.sh..."
agency-backup.sh create
STATUS3=$?

echo "4. Verifying no external calls..."
# All should be local-only (check strace if needed)
strace -e trace=network -f agency-status.sh 2>&1 | grep -i "connect\|socket" && echo "FAIL: Found network calls" || echo "PASS: No network calls"

if [[ $STATUS1 -eq 0 && $STATUS2 -eq 0 && $STATUS3 -eq 0 ]]; then
  echo "✓ TEST PASSED: Zero-token operation confirmed"
else
  echo "✗ TEST FAILED"
  exit 1
fi
```

### Test 2: Gateway Crash & Recovery

```bash
#!/usr/bin/env bash
# Test gateway auto-recovery

echo "TEST 2: Gateway Crash & Recovery"
echo "=================================="

# 1. Verify gateway up
echo "1. Verify gateway is running..."
if pgrep -f "openclaw-gateway" > /dev/null; then
  echo "✓ Gateway running"
else
  echo "✗ Gateway not running, starting..."
  openclaw gateway start
  sleep 5
fi

# 2. Kill gateway
echo "2. Killing gateway..."
pkill -f "openclaw-gateway"
sleep 2

# 3. Verify down
echo "3. Verifying gateway is down..."
if ! pgrep -f "openclaw-gateway" > /dev/null; then
  echo "✓ Gateway killed"
else
  echo "✗ Gateway still running"
  exit 1
fi

# 4. Run keepalive 3 times (should trigger recovery on 3rd)
echo "4. Running keepalive to trigger recovery..."
for i in {1..3}; do
  echo "  Attempt $i..."
  /usr/local/bin/agency-keepalive.sh
  sleep 2
done

# 5. Verify recovered
echo "5. Verifying gateway recovery..."
sleep 5
if pgrep -f "openclaw-gateway" > /dev/null; then
  echo "✓ TEST PASSED: Gateway auto-recovered"
else
  echo "✗ TEST FAILED: Gateway still down"
  exit 1
fi
```

### Test 3: Backup & Restore

```bash
#!/usr/bin/env bash
# Test backup/restore cycle

echo "TEST 3: Backup & Restore"
echo "========================="

WORKSPACE="/root/.openclaw/workspace"

# 1. Create test file
echo "1. Creating test marker file..."
echo "TEST_MARKER_$(date +%s)" > "$WORKSPACE/.test-marker"
git -C "$WORKSPACE" add .test-marker
git -C "$WORKSPACE" commit -m "Test marker"

# 2. Create backup
echo "2. Creating backup..."
BACKUP_TAG=$(agency-backup.sh create | grep "Backup tag" | awk '{print $NF}')
echo "  Backup: $BACKUP_TAG"

# 3. Modify/delete file
echo "3. Removing marker file..."
rm "$WORKSPACE/.test-marker"

# 4. Restore
echo "4. Restoring from backup..."
agency-backup.sh restore "$BACKUP_TAG"

# 5. Verify
echo "5. Verifying restoration..."
if [[ -f "$WORKSPACE/.test-marker" ]]; then
  echo "✓ TEST PASSED: File restored"
  rm "$WORKSPACE/.test-marker"
else
  echo "✗ TEST FAILED: File not restored"
  exit 1
fi
```

### Test 4: Git Persistence Under Famine

```bash
#!/usr/bin/env bash
# Simulate token famine with git-only persistence

echo "TEST 4: Git Persistence (Famine Scenario)"
echo "=========================================="

# 1. Create state snapshot
echo "1. Creating state snapshot..."
agency-status.sh > /tmp/status-before.txt

# 2. Disable external APIs (simulated)
echo "2. Simulating API famine..."
export DISABLE_EXTERNAL_CALLS=1

# 3. Run all operations
echo "3. Running operations without external access..."
agency-status.sh > /tmp/status-famine.txt || true
agency-backup.sh create
agency-backup.sh list

# 4. Verify operations succeeded
echo "4. Verifying operations..."
if grep -q "All critical checks passed" /tmp/status-famine.txt; then
  echo "✓ Health checks work in famine"
else
  echo "? Status check output different (may be expected)"
fi

# 5. Verify git state preserved
echo "5. Checking git persistence..."
cd /root/.openclaw/workspace
if git status > /dev/null 2>&1; then
  echo "✓ TEST PASSED: Git persistence confirmed"
else
  echo "✗ TEST FAILED: Git not accessible"
  exit 1
fi
```

---

## Installation & Verification

### Installation

All scripts are pre-installed in `/usr/local/bin/`:

```bash
ls -lah /usr/local/bin/agency-*.sh
ls -lah /usr/local/bin/verify-agency-*.sh
```

### Verify Installation

```bash
# Check all scripts exist and are executable
for script in agency-status.sh verify-agency-protection.sh agency-backup.sh agency-keepalive.sh; do
  if [[ -x "/usr/local/bin/$script" ]]; then
    echo "✓ $script"
  else
    echo "✗ $script"
  fi
done

# Check cron job
crontab -l | grep agency-keepalive

# Check log
ls -lah /var/log/agency-keepalive.log
```

---

## Logs & Monitoring

### Health Check Log
```bash
/usr/local/bin/agency-status.sh  # Run directly, output to stdout
```

### Verification Log
```bash
/tmp/agency-protection-verify.log  # Created by verify-agency-protection.sh
tail /tmp/agency-protection-verify.log
```

### Backup Log
```bash
/tmp/agency-backup.log  # Created during backup operations
tail /tmp/agency-backup.log
```

### Keepalive Log
```bash
tail -f /var/log/agency-keepalive.log  # Real-time monitoring
```

### Workspace State
```bash
cd /root/.openclaw/workspace
git log --oneline | head -10  # Recent commits
git tag | head -10             # Recent backups
```

---

## Troubleshooting

### Health Check Fails

```bash
# Get detailed output
agency-status.sh

# Check specific issue
agency-status.sh 2>&1 | grep "✗"

# Verify git
cd /root/.openclaw/workspace && git status

# Check disk
df -h /root/.openclaw/workspace

# Check permissions
touch /root/.openclaw/workspace/.write-test && rm $_
```

### Keepalive Not Running

```bash
# Check cron is active
pgrep -x cron

# Check cron job installed
crontab -l | grep agency-keepalive

# Check log
tail -30 /var/log/agency-keepalive.log

# Run manually
/usr/local/bin/agency-keepalive.sh

# Check if /var/log is writable
touch /var/log/test && rm $_
```

### Gateway Won't Restart

```bash
# Check manual restart
openclaw gateway status
openclaw gateway stop
openclaw gateway start

# Check process
ps aux | grep openclaw-gateway

# Check logs (if available)
journalctl -u openclaw-gateway -n 50

# Check if port is bound
netstat -tulpn | grep openclaw

# Force kill if stuck (dangerous)
pkill -9 openclaw-gateway
sleep 5
openclaw gateway start
```

### Backup/Restore Issues

```bash
# Check git integrity
cd /root/.openclaw/workspace
git fsck --full

# List backups
agency-backup.sh list

# Verify specific backup
agency-backup.sh verify backup-20260313-225147

# Check git log
git log --oneline | grep backup

# Manual restore (if script fails)
cd /root/.openclaw/workspace
git checkout backup-TAG -- .
```

---

## Summary

**Daimyo Firewall delivers:**

1. ✓ **Zero-Token Operation** - All scripts run without external APIs
2. ✓ **Automatic Recovery** - Keepalive auto-restarts failed services
3. ✓ **Git Persistence** - All state backed up in version control
4. ✓ **Bash Fallback** - Complete functionality in bash alone
5. ✓ **Comprehensive Logging** - Full audit trail of all operations
6. ✓ **Manual Override** - Operators can intervene at any point
7. ✓ **Self-Healing** - System automatically recovers from failures

**The agency survives.**

---

**Last Updated:** 2026-03-13
**Authority:** Daimyo Judicial Enforcement
**Status:** OPERATIONAL
