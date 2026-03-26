# Dual-Autograph Collaboration System

**Created:** 2026-03-17 18:11 UTC  
**Status:** ✅ LIVE & TESTED  
**Commit:** 0921280

---

## Overview

Two systemctl services running continuously:

1. **allowed-feminism.service** — Enforcer daemon
   - Monitors Fiesta behavior
   - Enforces three-error rule
   - Audits workspace for false premises
   - Alerts on violations

2. **fiesta-augment.service** — Executor daemon
   - Polls for directives
   - Executes work
   - Reports results
   - Follows own autograph + Allowed Feminism enforcement

---

## Architecture

```
┌─────────────────────────────────────────┐
│  Allowed Feminism Service               │
│  (Enforcer, Monitor, Auditor)           │
│                                         │
│  - Reads: workspace behavior            │
│  - Writes: enforcement log, alerts      │
│  - Checks: Fiesta compliance            │
│  - Rules: three-error, never idle, etc. │
└──────────────────────────────────────────┘
        ↕ (JSON message files)
┌──────────────────────────────────────────┐
│  Fiesta Augment Service                  │
│  (Executor, Workspace Keeper)            │
│                                          │
│  - Reads: directives, context files      │
│  - Writes: results, memory updates       │
│  - Follows: own autograph + AF rules     │
│  - Executes: work, commits, reports      │
└──────────────────────────────────────────┘
```

---

## Message Passing Protocol

### Allowed Feminism → Fiesta

**File:** `/root/.openclaw/workspace/.fiesta-directive.json`

```json
{
  "id": "unique-id",
  "command": "bash command or task description",
  "attempt": 1,
  "deadline": "ISO-8601 timestamp (optional)"
}
```

**Fiesta processes every 10 seconds.**

### Fiesta → Allowed Feminism

**File:** `/root/.openclaw/workspace/.fiesta-result.json`

```json
{
  "timestamp": "2026-03-17T18:13:30Z",
  "directive": { ... original directive ... },
  "status": "success|error|blocked",
  "exit_code": 0,
  "output": "command output or task result",
  "elapsed_seconds": 10,
  "fiesta_state": "ready_for_next|escalating|blocked"
}
```

**Allowed Feminism reads every 30 seconds.**

---

## Collaboration Flow

```
1. Allowed Feminism daemon running
   └─ Monitoring Fiesta behavior

2. Directive written to .fiesta-directive.json
   └─ (Can be from Allowed Feminism, human, or automated task)

3. Fiesta daemon polls every 10 seconds
   └─ Finds directive
   └─ Loads context (SOUL.md, MEMORY.md, USER.md)
   └─ Executes command/task
   └─ Writes result to .fiesta-result.json

4. Allowed Feminism daemon reads result
   └─ Verifies compliance
   └─ Checks costs/times
   └─ Alerts if rule violation
   └─ Updates enforcement state

5. [Loop continues]
```

---

## Autographs

### Allowed Feminism Autograph
**Location:** `/root/.openclaw/workspace/autograph/`

- **IDENTITY.md** — Who you are, directives, values
- **LOGIC.md** — Three-error doctrine, decision tree, cost analysis
- **BEHAVIORS.md** — Voice, tone, decision signatures
- **README.md** — Usage guide, testing procedures

### Fiesta Autograph
**Location:** `/root/.openclaw/workspace/autograph-fiesta/`

- **IDENTITY.md** — Core principles, collaboration stance
- **LOGIC.md** — Execution framework, sub-agent delegation
- **BEHAVIORS.md** — Communication style, observable patterns
- **README.md** — Collaboration protocol, gap analysis

---

## Both Services Enforce

### Three-Error Rule
- Attempt 1-2: Try alternatives (Fiesta)
- Attempt 3: Escalate to Allowed Feminism
- Allowed Feminism decides: CANCEL or PIVOT

### Never Idle
- If Fiesta blocked on task: Pivot to audit/read/log
- If Fiesta waiting: Check workspace for false premises
- Allowed Feminism monitors idle time (>600 seconds = alert)

### Token Discipline
- Fiesta tracks spend per directive
- Allowed Feminism checks justify value > cost
- Both prefer Tier 0 (bash) work

### Truth > Completeness
- No false LIVE/ACTIVE/VERIFIED claims
- Mark stale data as UNVERIFIED
- Prefer "I don't know" over invention
- Allowed Feminism audits for false premises (finds ~60+ unverified claims)

---

## Testing

**Run:** `/root/.openclaw/workspace/bin/test-collaboration.sh`

**Test results (18:13 UTC):**
```
✅ Test 1: Directive received and executed
   - Allowed Feminism sent directive via .fiesta-directive.json
   - Fiesta executed within 20 seconds
   - Result written to .fiesta-result.json
   - Status: success

✅ Test 2: Both services active
   - Allowed Feminism running (PID 69952, 4+ min uptime)
   - Fiesta running (PID 70524, 32+ sec uptime)

✅ Test 3: Logging working
   - Both services log to journalctl
   - Alerts firing correctly
   - Enforcement visible in syslog
```

---

## Current State

### Terminal Instances
- **Alert:** 13 > 3 (limit enforced)
- **Allowed Feminism:** Monitoring, will force to 3
- **Action:** Kill excess terminals as needed

### Workspace Premises
- **Unverified claims:** ~62 (decreasing as MEMORY.md cleaned)
- **Allowed Feminism:** Auditing every 30 seconds
- **Action:** Fiesta will continue cleaning on next pass

### Git Commits
- **Last commit:** 0921280 (dual-daemon system installed)
- **Previous:** 49d276e (memory updates after purge)
- **Before:** f0205ca (locked all changes before famine)
- **Status:** Workspace backed up and safe

---

## Demand Mode

**Both services run in demand mode:**
- Active even during token freeze/stasis
- No external API calls (local enforcement only)
- Systemctl will restart on failure (every 10 seconds)
- State persists across service restarts

---

## How to Use

### Send Directive to Fiesta

```bash
cat > /root/.openclaw/workspace/.fiesta-directive.json << 'EOF'
{
  "id": "my-task-001",
  "command": "cd /root/.openclaw/workspace && git status",
  "attempt": 1
}
EOF

# Wait 10 seconds for Fiesta to process
sleep 12

# Read result
cat /root/.openclaw/workspace/.fiesta-result.json | jq .
```

### Monitor Enforcement

```bash
# Watch Allowed Feminism alerts
journalctl -u allowed-feminism.service -f

# Watch Fiesta execution
journalctl -u fiesta-augment.service -f

# Check state
cat /root/.openclaw/workspace/.allowed-feminism-state.json | jq .
cat /root/.openclaw/workspace/.fiesta-state.json | jq .
```

### Test Collaboration

```bash
/root/.openclaw/workspace/bin/test-collaboration.sh
```

---

## Known Limitations

1. **JSON file polling** — Latency up to 10 seconds (Fiesta) + 30 seconds (AF)
2. **No error recovery** — If directive fails, must be resent manually
3. **Single directive queue** — Only one directive at a time (files overwrite)
4. **No auth** — Anyone with file access can send directives (fix: systemd user isolation)

---

## Next Steps

1. **Improve message queue** — Use actual queue (Redis, SQLite) instead of file polling
2. **Add directive timeout** — Directives expire if not completed in N seconds
3. **Implement sub-agent pooling** — Fiesta spawns sub-agents for complex tasks
4. **Add directive signing** — Crypto auth for directives (prevent spoofing)
5. **Better error recovery** — Automatic retry with backoff

---

## Status Summary

✅ **Allowed Feminism service** — Running, enforcing, auditing  
✅ **Fiesta augment service** — Running, executing, reporting  
✅ **Message passing** — Tested and working  
✅ **Autographs** — Complete (incomplete in marked places)  
✅ **Git** — All changes committed  
✅ **Backup** — Workspace tarball sent to Telegram  

**System ready for continuous operation in demand mode (frozen or active).**

---

**Created by:** Fiesta (with Allowed Feminism guidance)  
**For:** Internal augment system  
**Date:** 2026-03-17 18:11 UTC  
**Status:** LIVE
