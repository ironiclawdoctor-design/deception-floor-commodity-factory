# Process Optimizer — Approval ID Expiration Analysis

## Root Cause Analysis
Error: `GatewayClientRequestError: unknown or expired approval id`
- Occurs when human tries to approve jobs after gateway restart or session timeout.
- Approval IDs are stored in gateway memory; restart clears them.
- Human perceives this as "corruption" and assumes breach.

## Solutions (3-5 specific)

### 1. Gateway Restart Detection
**Goal:** Detect gateway restart before human attempts approval, expire cached IDs automatically.
**Implementation (Tier 0-2):**
- Script: `gateway-status.sh` that captures gateway PID and start time.
- Store in `/tmp/gateway-state.json` (PID, start_time, hash of config).
- Before presenting any approval ID, compare current gateway state with stored state.
- If changed, emit warning: "Gateway restarted — previous approval IDs invalid."
- Update stored state after each restart detection.

**Commands:**
```bash
#!/bin/bash
# /root/human/gateway-status.sh
PID=$(ps aux | grep '[o]penclaw-gateway' | awk '{print $2}')
START=$(ps -p $PID -o lstart= 2>/dev/null || echo "unknown")
echo "{\"pid\":\"$PID\",\"start\":\"$START\"}" > /tmp/gateway-state.json
```

### 2. Approval ID Logging & Purge
**Goal:** Log every generated approval ID in agency.db, purge after restart.
**Implementation:**
- Use SQLite table `approval_ids (id TEXT, command TEXT, created INTEGER, expires INTEGER)`.
- When exec returns approval ID, insert record.
- On gateway restart detection, delete all rows for that gateway session.
- Provide script `list-pending-approvals.sh` to show human what’s pending.

**SQL:**
```sql
CREATE TABLE IF NOT EXISTS approval_ids (
    id TEXT PRIMARY KEY,
    command TEXT,
    created INTEGER DEFAULT (unixepoch()),
    expires INTEGER DEFAULT (unixepoch() + 3600)
);
```

### 3. Pre‑Approval Validation
**Goal:** Before human copies `/approve <id> allow-always`, validate that ID is still active.
**Implementation:**
- Script `validate-approval.sh <id>` that checks:
  1. Gateway state unchanged (if changed, ID invalid).
  2. ID exists in agency.db (optional).
- If invalid, regenerate command and present fresh approval ID with explanation.

### 4. Clear Communication Protocol
**Goal:** Every approval request must include gateway state and expiration notice.
**Template:**
```
🗳️ **Approval Required**
Command: `python3 /root/human/05-script.py`
Approval ID: `c989be6d`
Gateway PID: 1234 (started 2026‑03‑23 12:00 UTC)
⚠️  This ID will expire if gateway restarts. Run `./gateway-status.sh` to check.
/approve c989be6d allow-always
```

### 5. Security Response for Unknown IDs
**Goal:** Treat unknown/expired IDs as potential breach.
**Implementation:**
- If human reports "unknown approval id" and gateway hasn’t restarted, trigger security audit:
  - SR-001: Direct SQLite query to check for unauthorized ledger entries.
  - SR-002: Verify config files unchanged.
  - SR-003: Rotate Telegram token via human action.
- Script `breach-response.sh` that logs incident and recommends steps.

## Draft New Agency Rules

### HR-015 (Approval ID Validation)
**Rule:** Before surfacing any approval ID, validate gateway state. If gateway restarted since ID generation, discard ID and regenerate command. Always include gateway PID and start time in approval request.

### HR-016 (Approval ID Logging)
**Rule:** Log every approval ID in agency.db `approval_ids` table. On gateway restart detection, purge all entries and notify human: "Gateway restarted — previous approval IDs expired."

### BR-009 (Unknown Approval ID Breach Protocol)
**Rule:** Any report of "unknown or expired approval id" without gateway restart triggers security audit (SR‑001 to SR‑018). Assume breach until proven otherwise. Rotate Telegram token, audit subagent processes, verify config integrity.

## Recommended Changes to Existing Rules

### HR-014 Refinement
**Current:** "Exec approval gate resets after gateway restart. All `allow-always` whitelists are session‑scoped, not persistent across restarts. After every restart, human must re-approve from Web UI. Mitigation: batch all critical post‑restart commands into a single numbered script so one approval covers everything."

**Add:** 
- "Automatically detect gateway restart via `gateway-status.sh` and notify human before they attempt to approve expired IDs."
- "Store pending approval IDs in agency.db; on restart detection, auto‑purge and surface fresh batch script."

## Integration with Security Doctrine
- SR-001: Use SQLite for approval ID logging (bypass gateway).
- SR-002: Write gateway state to file (no approval needed).
- SR-013: Use `allow-always` pattern for post‑restart batch script.

## Implementation Priority
1. Create `gateway-status.sh` and integrate into heartbeat.
2. Add SQLite table `approval_ids`.
3. Update approval presentation template.
4. Create `breach-response.sh` skeleton.

## How I Did It
1. Read AGENTS.md to understand existing HR/BR/SR rules.
2. Analyzed error pattern from memory/2026‑03‑23.md.
3. Derived solutions focusing on detection, logging, communication, security.
4. Drafted rules following agency numbering convention.
5. Ensured all solutions are actionable with bash/sqlite/file ops (Tier 0‑2).

## Recommendations
- Implement gateway restart detection immediately (low‑cost, high‑value).
- Add approval ID logging to agency.db for audit trail.
- Train human to run `gateway-status.sh` after any gateway operation.
- Incorporate unknown ID response into existing security drills.

---
**Process Optimizer** — Subagent task completed.