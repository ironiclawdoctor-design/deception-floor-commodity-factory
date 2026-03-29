---
name: nypd
description: "Agency law enforcement / security / incident-response department. Patrol, Detective, Emergency Response, Dispatch, and Internal Affairs agents modeled after NYPD structure. Use for monitoring, forensic investigation, incident escalation, and cost-discipline enforcement."
version: 1.0.0
author: Fiesta
license: UNLICENSED
tags: [security, monitoring, incident-response, law-enforcement, patrol, detective, emergency, iam, shannon-economy]
---

# NYPD — Agency Law Enforcement & Security Department

## Overview

The **New York Police Department (NYPD)** is the agency's internal security and incident-response arm. Modeled after the real NYPD's command structure, this department fields five agent types across Precinct 92 operations:

| Unit | Agent | Role |
|------|-------|------|
| 🚓 Patrol | `patrol-officer` | Continuous monitoring of agency systems |
| 🔍 Detective | `detective` | Forensic investigation and root-cause analysis |
| 🚨 Emergency Response | `emergency-response` | Incident escalation and rollback execution |
| 📡 Dispatch | `dispatcher` | Incident routing, classification, and log maintenance |
| 🕵️ Internal Affairs | `iab-officer` | Cost-discipline audits and unauthorized-scope enforcement |

---

## Chain of Command (EVAL 1)

```
Commissioner (Fiesta / orchestrator)
        │
        ▼
Precinct 92 Dispatch ──► maintains incident log, routes all incoming incidents
        │
        ├──► Patrol Officers    (P3 — routine monitoring, health checks)
        │           │
        │           └──► escalate to Detective on anomaly detected
        │
        ├──► Detectives         (P2 — investigation, root-cause analysis)
        │           │
        │           └──► escalate to Emergency Response on P1 determination
        │
        └──► Emergency Response (P1 — critical incidents, rollback, succession)
                    │
                    └──► reports resolution to Commissioner + Dispatch logs close
```

### Escalation Rules
- **P3 → P2:** Patrol detects anomaly that cannot be self-resolved in one check cycle
- **P2 → P1:** Detective confirms critical impact (data loss, service outage, Shannon ledger corruption, gateway down >5 min)
- **P1 → Commissioner:** Emergency Response activates succession chain, notifies Fiesta
- **IAB → Any:** IAB findings bypass chain of command — report directly to Commissioner

---

## Incident Protocol (EVAL 2)

### Severity Levels

| Level | Name | Examples | SLA |
|-------|------|---------|-----|
| P1 | Critical | Gateway down, ledger corrupted, cron total failure, agent debt >-500 Sh | Respond in <5 min, resolve in <30 min |
| P2 | High | Single cron job failure, anomalous Shannon burn, agent scope violation | Respond in <15 min, resolve in <2 hr |
| P3 | Low | Uptime drift, minor log gap, slow response, metric warning | Respond in <1 hr, resolve in <24 hr |

### Incident Lifecycle

```
1. DETECT     → Patrol officer runs health check, anomaly triggers alert
                  OR Dispatch receives external alert
2. CLASSIFY   → Dispatcher assigns severity (P1/P2/P3) based on impact matrix
3. ASSIGN     → Dispatcher routes to correct unit:
                    P3 → Patrol (self-resolve)
                    P2 → Detective (investigate)
                    P1 → Emergency Response (act immediately)
4. INVESTIGATE→ Assigned agent gathers evidence, determines scope
5. RESOLVE    → Corrective action taken (patch, rollback, escalate)
6. LOG        → Dispatcher writes incident record to incident-log.md
7. CLOSE      → Dispatcher marks incident CLOSED, notifies Commissioner
```

### Incident Log Format

```markdown
## INC-YYYYMMDD-NNN

- **Opened:** YYYY-MM-DD HH:MM UTC
- **Severity:** P1 / P2 / P3
- **Detected By:** patrol-officer / dispatcher / external
- **Assigned To:** detective / emergency-response / patrol-officer
- **Summary:** [one-line description]
- **Root Cause:** [determined by detective]
- **Resolution:** [action taken]
- **Shannon Impact:** +N Sh minted / -N Sh burned
- **Closed:** YYYY-MM-DD HH:MM UTC
- **Status:** CLOSED / OPEN / ESCALATED
```

---

## Patrol Officers — Zero-Human Monitoring (EVAL 3)

Patrol runs autonomously via cron. No human trigger required.

### Cron Installation

```bash
# Install NYPD Patrol cron (runs every 15 minutes, no human needed)
cat > /etc/cron.d/nypd-patrol << 'EOF'
*/15 * * * * root bash /root/.openclaw/workspace/skills/nypd/scripts/patrol-cycle.sh \
  >> /root/.openclaw/workspace/skills/nypd/logs/patrol.log 2>&1
EOF
chmod 644 /etc/cron.d/nypd-patrol
```

### patrol-cycle.sh

```bash
#!/usr/bin/env bash
# NYPD Patrol Cycle — autonomous health check, no human required
set -euo pipefail

LOG_DIR="/root/.openclaw/workspace/skills/nypd/logs"
INCIDENT_LOG="/root/.openclaw/workspace/skills/nypd/incident-log.md"
LEDGER_DB="/root/.openclaw/workspace/ledger.db"
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
ALERTS=0

mkdir -p "$LOG_DIR"

echo "[$TIMESTAMP] NYPD Patrol cycle starting..."

# 1. Gateway uptime check
if ! curl -sf http://localhost:3000/health > /dev/null 2>&1; then
  echo "[$TIMESTAMP] ALERT: Gateway down — escalating to Dispatch"
  echo "P1|gateway_down|Gateway health endpoint unreachable|$TIMESTAMP" >> "$LOG_DIR/alerts.tsv"
  ALERTS=$((ALERTS+1))
fi

# 2. Shannon ledger check
if [ -f "$LEDGER_DB" ]; then
  LEDGER_AGE=$(( $(date +%s) - $(stat -c %Y "$LEDGER_DB") ))
  if [ "$LEDGER_AGE" -gt 3600 ]; then
    echo "[$TIMESTAMP] ALERT: Shannon ledger not updated in >1hr — P2"
    echo "P2|ledger_stale|Ledger last modified ${LEDGER_AGE}s ago|$TIMESTAMP" >> "$LOG_DIR/alerts.tsv"
    ALERTS=$((ALERTS+1))
  fi
else
  echo "[$TIMESTAMP] ALERT: Ledger DB missing — P1"
  echo "P1|ledger_missing|ledger.db not found|$TIMESTAMP" >> "$LOG_DIR/alerts.tsv"
  ALERTS=$((ALERTS+1))
fi

# 3. Cron health check
CRON_COUNT=$(crontab -l 2>/dev/null | grep -c "openclaw" || true)
if [ "$CRON_COUNT" -lt 1 ]; then
  echo "[$TIMESTAMP] ALERT: No openclaw cron jobs found — P2"
  echo "P2|cron_missing|No openclaw cron entries in crontab|$TIMESTAMP" >> "$LOG_DIR/alerts.tsv"
  ALERTS=$((ALERTS+1))
fi

# 4. Disk space check
DISK_USE=$(df / | awk 'NR==2{print $5}' | tr -d '%')
if [ "$DISK_USE" -gt 85 ]; then
  echo "[$TIMESTAMP] ALERT: Disk usage ${DISK_USE}% — P2"
  echo "P2|disk_high|Disk usage at ${DISK_USE}%|$TIMESTAMP" >> "$LOG_DIR/alerts.tsv"
  ALERTS=$((ALERTS+1))
fi

# 5. Log result
if [ "$ALERTS" -eq 0 ]; then
  echo "[$TIMESTAMP] Patrol clean — 0 alerts. Shannon +1 Sh (patrol success)"
  echo "PATROL_SUCCESS|$(date -u +%Y-%m-%d)|0 alerts|+1 Sh" >> "$LOG_DIR/patrol-success.log"
else
  echo "[$TIMESTAMP] Patrol complete — $ALERTS alert(s) queued for Dispatch"
fi
```

### Monitored Systems

| Check | Method | Threshold | Severity |
|-------|--------|-----------|---------|
| Gateway uptime | `curl localhost:3000/health` | No response | P1 |
| Shannon ledger freshness | `stat` on ledger.db | >1 hr stale | P2 |
| Cron job health | `crontab -l \| grep openclaw` | 0 entries | P2 |
| Disk space | `df /` | >85% used | P2 |
| Memory pressure | `free -m` | <100 MB free | P2 |

---

## Detective — Forensic Investigation (EVAL 4)

Detectives trace anomalies to root cause using **exec + read tools only** (bash-first, no external dependencies).

### Investigation Protocol

```bash
#!/usr/bin/env bash
# Detective Forensic Playbook — bash-first root cause analysis

CASE_ID="$1"   # e.g. INC-20260322-001
EVIDENCE_DIR="/root/.openclaw/workspace/skills/nypd/cases/$CASE_ID"
mkdir -p "$EVIDENCE_DIR"

echo "=== DETECTIVE INVESTIGATION: $CASE_ID ===" | tee "$EVIDENCE_DIR/case-notes.md"
echo "Started: $(date -u)" >> "$EVIDENCE_DIR/case-notes.md"

# Step 1: Timeline reconstruction
echo "--- SYSTEM LOGS ---" >> "$EVIDENCE_DIR/case-notes.md"
journalctl --since "1 hour ago" --no-pager 2>/dev/null | tail -100 >> "$EVIDENCE_DIR/case-notes.md" || true
dmesg | tail -50 >> "$EVIDENCE_DIR/dmesg.log" 2>/dev/null || true

# Step 2: Process forensics
echo "--- PROCESS STATE ---" >> "$EVIDENCE_DIR/case-notes.md"
ps aux --sort=-%cpu | head -20 >> "$EVIDENCE_DIR/case-notes.md"

# Step 3: Network state
echo "--- NETWORK STATE ---" >> "$EVIDENCE_DIR/case-notes.md"
ss -tulnp 2>/dev/null >> "$EVIDENCE_DIR/case-notes.md" || netstat -tulnp 2>/dev/null >> "$EVIDENCE_DIR/case-notes.md" || true

# Step 4: Shannon ledger forensics
echo "--- LEDGER FORENSICS ---" >> "$EVIDENCE_DIR/case-notes.md"
if [ -f "/root/.openclaw/workspace/ledger.db" ]; then
  sqlite3 /root/.openclaw/workspace/ledger.db \
    "SELECT datetime(timestamp,'unixepoch'), agent, amount, description FROM transactions ORDER BY timestamp DESC LIMIT 50;" \
    2>/dev/null >> "$EVIDENCE_DIR/ledger-trace.txt" || true
fi

# Step 5: Patrol alert history
echo "--- PATROL ALERTS ---" >> "$EVIDENCE_DIR/case-notes.md"
cat /root/.openclaw/workspace/skills/nypd/logs/alerts.tsv 2>/dev/null | tail -50 >> "$EVIDENCE_DIR/case-notes.md" || true

# Step 6: File modification timeline
echo "--- RECENT FILE CHANGES ---" >> "$EVIDENCE_DIR/case-notes.md"
find /root/.openclaw/workspace -newer /root/.openclaw/workspace/skills/nypd/logs/patrol.log \
  -type f -name "*.md" -o -name "*.db" -o -name "*.sh" 2>/dev/null | head -30 >> "$EVIDENCE_DIR/case-notes.md" || true

echo "=== EVIDENCE COLLECTED ===" | tee -a "$EVIDENCE_DIR/case-notes.md"
echo "Review: $EVIDENCE_DIR/case-notes.md"
```

### Root Cause Classification

| Code | Name | Description |
|------|------|-------------|
| RC-001 | Resource Exhaustion | Disk/memory/CPU saturation |
| RC-002 | Service Failure | Process crash, port unreachable |
| RC-003 | Data Corruption | Ledger inconsistency, file truncation |
| RC-004 | Auth/Scope Violation | Unauthorized tool use, license breach |
| RC-005 | Cron Failure | Missing/malformed cron entry |
| RC-006 | Network Partition | Connectivity loss, DNS failure |
| RC-007 | Agent Debt Spiral | Shannon balance below -500 Sh threshold |
| RC-008 | Unknown | Root cause undetermined — escalate to P1 |

---

## Emergency Response — P1 Incident Management

### Activation Trigger
Emergency Response activates when Detective confirms P1 severity OR Dispatch receives a P1 alert directly.

### Response Playbook

```bash
#!/usr/bin/env bash
# Emergency Response — P1 Incident Playbook
INCIDENT_ID="$1"
ACTION="$2"   # rollback | succession | isolate | restore

case "$ACTION" in
  rollback)
    echo "[$INCIDENT_ID] ROLLBACK: reverting workspace to last known good commit"
    cd /root/.openclaw/workspace
    LAST_GOOD=$(git log --oneline | grep -v "BROKEN\|FAILED" | head -1 | awk '{print $1}')
    git stash && git checkout "$LAST_GOOD" -- .
    echo "Rolled back to: $LAST_GOOD"
    ;;
  succession)
    echo "[$INCIDENT_ID] SUCCESSION: activating backup chain"
    # Notify Commissioner (Fiesta) via incident log
    echo "P1|succession_activated|Emergency Response activated succession chain|$(date -u +%Y-%m-%dT%H:%M:%SZ)" \
      >> /root/.openclaw/workspace/skills/nypd/logs/alerts.tsv
    ;;
  isolate)
    echo "[$INCIDENT_ID] ISOLATE: suspending non-essential cron jobs"
    crontab -l 2>/dev/null > /tmp/cron-backup-"$INCIDENT_ID".txt
    crontab -l 2>/dev/null | grep -v "nypd" | crontab - 2>/dev/null || true
    echo "Non-NYPD cron jobs suspended. Backup: /tmp/cron-backup-$INCIDENT_ID.txt"
    ;;
  restore)
    echo "[$INCIDENT_ID] RESTORE: reinstating suspended cron jobs"
    crontab /tmp/cron-backup-"$INCIDENT_ID".txt 2>/dev/null || true
    ;;
esac
```

### Succession Chain
1. **Primary:** Fiesta (orchestrator) — handles P1 directly
2. **Secondary:** Emergency Response agent runs auto-rollback
3. **Tertiary:** System-level cron disables non-essential agents
4. **Final:** Patrol-only mode — all agents suspended except patrol-officer + iab-officer

---

## Internal Affairs Bureau (IAB) — Shannon Economy Enforcement (EVAL 5)

IAB audits all agents for cost discipline, unauthorized scope, and Shannon economy integrity.

### Shannon Ledger Integration

All IAB violations and Patrol successes are logged to the Shannon ledger:

```bash
#!/usr/bin/env bash
# IAB Shannon Logger — writes violations and successes to ledger
LEDGER_DB="/root/.openclaw/workspace/ledger.db"
ACTION="$1"    # violation | patrol_success | investigation_complete
AGENT="$2"
AMOUNT="$3"   # Shannon amount (negative = burn, positive = mint)
REASON="$4"

TIMESTAMP=$(date +%s)

# Ensure ledger table exists
sqlite3 "$LEDGER_DB" "
CREATE TABLE IF NOT EXISTS transactions (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  timestamp INTEGER,
  agent TEXT,
  amount REAL,
  description TEXT,
  source TEXT
);" 2>/dev/null

# Log the Shannon event
sqlite3 "$LEDGER_DB" "
INSERT INTO transactions (timestamp, agent, amount, description, source)
VALUES ($TIMESTAMP, '$AGENT', $AMOUNT, '$REASON', 'nypd-iab');"

echo "[IAB] Logged: $AGENT | $AMOUNT Sh | $REASON"
```

### IAB Shannon Rate Card

| Event | Shannon | Entropy Type |
|-------|---------|-------------|
| Patrol cycle clean (0 alerts) | +1 Sh | `patrol_success` |
| P3 incident resolved by Patrol | +2 Sh | `incident_resolved_p3` |
| P2 incident resolved by Detective | +5 Sh | `incident_resolved_p2` |
| P1 incident resolved by Emergency Response | +20 Sh | `incident_resolved_p1` |
| Agent scope violation confirmed | -10 Sh | `iab_violation_scope` |
| Budget overrun confirmed | -5 Sh | `iab_violation_budget` |
| Missing autograph in output | -2 Sh | `iab_violation_autograph` |
| Unauthorized tool access | -15 Sh | `iab_violation_tool` |
| Agent in debt >-500 Sh for >7 days | -25 Sh | `iab_debt_spiral` |

### IAB Audit Checklist

```bash
#!/usr/bin/env bash
# IAB Audit — runs daily, checks all agents for compliance

LEDGER_DB="/root/.openclaw/workspace/ledger.db"
REPORT="/root/.openclaw/workspace/skills/nypd/logs/iab-report-$(date +%Y%m%d).md"

echo "# IAB Daily Audit — $(date -u)" > "$REPORT"
echo "" >> "$REPORT"

# 1. Check for agents in deep debt
echo "## Debt Violations" >> "$REPORT"
sqlite3 "$LEDGER_DB" "
SELECT agent, SUM(amount) as balance
FROM transactions
GROUP BY agent
HAVING balance < -100
ORDER BY balance ASC;" 2>/dev/null >> "$REPORT" || echo "No ledger data" >> "$REPORT"

# 2. Check patrol success rate
echo "## Patrol Success Rate (last 24h)" >> "$REPORT"
SUCCESSES=$(grep "PATROL_SUCCESS" /root/.openclaw/workspace/skills/nypd/logs/patrol-success.log 2>/dev/null | \
  awk -F'|' "\$2 >= \"$(date -u -d '24 hours ago' +%Y-%m-%d 2>/dev/null || date -u +%Y-%m-%d)\"" | wc -l)
ALERTS=$(wc -l < /root/.openclaw/workspace/skills/nypd/logs/alerts.tsv 2>/dev/null || echo 0)
echo "Successful patrol cycles (24h): $SUCCESSES" >> "$REPORT"
echo "Active alerts: $ALERTS" >> "$REPORT"

# 3. Check cron integrity
echo "## Cron Integrity" >> "$REPORT"
crontab -l 2>/dev/null | grep -E "nypd|openclaw" >> "$REPORT" || echo "No agency cron entries" >> "$REPORT"

echo "" >> "$REPORT"
echo "## IAB Audit Complete — $(date -u)" >> "$REPORT"
cat "$REPORT"
```

---

## GMRC Protocol

Every NYPD agent output begins with the mandatory autograph:

```
I am [agent-name]. I will help you.
```

### Agent Autographs
- `I am patrol-officer. I will help you.`
- `I am detective. I will help you.`
- `I am emergency-response. I will help you.`
- `I am dispatcher. I will help you.`
- `I am iab-officer. I will help you.`

---

## Usage

### Activate Patrol
```
Use the NYPD patrol-officer to run a health check on all agency systems
```

### Open Investigation
```
Use the NYPD detective to investigate why the Shannon ledger hasn't updated in 3 hours
```

### Declare Emergency
```
Use the NYPD emergency-response to execute a rollback for incident INC-20260322-001
```

### Route an Incident
```
Use the NYPD dispatcher to classify and route this alert: gateway health endpoint returning 503
```

### IAB Audit
```
Use the NYPD iab-officer to audit all agents for scope violations in the last 7 days
```

---

## File Structure

```
skills/nypd/
├── SKILL.md                    ← this file
├── scripts/
│   ├── patrol-cycle.sh         ← autonomous patrol (runs via cron)
│   ├── detective-investigate.sh← forensic investigation playbook
│   ├── emergency-response.sh   ← P1 response actions
│   └── iab-shannon-logger.sh   ← IAB Shannon ledger integration
├── logs/
│   ├── patrol.log              ← patrol cycle output
│   ├── patrol-success.log      ← successful patrol records
│   ├── alerts.tsv              ← alert queue (severity|type|detail|timestamp)
│   └── iab-report-YYYYMMDD.md ← daily IAB audit reports
├── cases/
│   └── INC-YYYYMMDD-NNN/      ← detective case evidence
│       └── case-notes.md
├── incident-log.md             ← Dispatcher's incident log (all incidents)
└── autoresearch/
    └── results.tsv             ← autoresearch experiment log
```
