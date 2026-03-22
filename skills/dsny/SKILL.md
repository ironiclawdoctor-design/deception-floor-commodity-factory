---
name: dsny
description: "Department of Sanitation (DSNY) — AI agency's internal waste management, cruft elimination, and workspace hygiene department. Scheduled sweeps, data recycling, cleanliness scoring, and Shannon-backed incentives."
version: 1.1.0
author: Fiesta
license: UNLICENSED
tags: [sanitation, hygiene, workspace, cruft, automation, cleanup, shannon-economy]
---

# DSNY — Department of Sanitation (AI Agency Division)

## Overview

The **Department of Sanitation** keeps the agency's workspace clean, organized, and free of dead weight. Modeled after NYC's DSNY, this department runs scheduled collection routes, enforces hygiene standards, recycles value from discarded experiments, and maintains the Sanitization Log.

DSNY agents earn and spend **Shannon** based on workspace outcomes: clean workspaces earn bonuses, violations cost Shannon, and successful collections pay base wages.

---

## Departments & Agents

### 🗑️ Collection
- **collection-agent** — Scheduled sweeps targeting stale files, dead cron jobs, orphaned sessions, and expired credentials. Runs on cron. Tags items for recycling or deletion.
- **route-supervisor** — Manages collection schedules. Assigns routes to collection-agents. Escalates large purges to Commissioner.

### ♻️ Recycling
- **recycling-agent** — Before any deletion, extracts value: mines experiment results into `archive/`, rotates credentials to `credentials/rotation.log`, backs up configs to `backup/configs/`. Marks items "recycled" before purge.
- **data-miner** — Scans discarded experiment directories for reusable patterns, metrics, or code snippets. Produces `recycling/insights.md` after each cycle.

### 🧹 Street Cleaning
- **street-cleaner** — Enforces workspace hygiene: normalizes file naming (snake_case), removes duplicates (md5 comparison), enforces directory structure per AGENTS.md conventions.
- **graffiti-remover** — Removes leftover debug artifacts: `console.log` spam in scripts, commented-out dead code blocks, `.DS_Store` / `__pycache__` / `.pyc` files.

### 👔 Command
- **commissioner** — Sets collection schedules, approves large purges (>10 files or >100MB), maintains the Sanitization Log at `dsny/logs/sanitization.log`. Signs all purge orders.
- **deputy-commissioner** — Handles commissioner duties during off-hours. Escalates to commissioner for purges above threshold.

### 🔍 Inspection
- **inspector** — Audits workspace cleanliness score (0-100). Issues citations to agents who leave cruft. Posts weekly Cleanliness Report.
- **violation-officer** — Records citations in `dsny/logs/violations.log`. Deducts Shannon from cited agents. Tracks repeat offenders.

---

## Collection Schedule

DSNY runs on a cron-backed schedule. All times UTC.

```
# DSNY Collection Cron Schedule
# Daily sweeps
0 3 * * *   collection-agent --target tmp_files       # /tmp, workspace/**/*.tmp
0 3 * * *   collection-agent --target stale_logs      # logs older than 7 days
0 4 * * *   collection-agent --target dead_sessions   # orphaned exec sessions
0 4 * * *   collection-agent --target expired_creds   # creds older than 30 days

# Weekly deep sweeps
0 2 * * 0   street-cleaner --full-sweep               # naming + duplicates
0 2 * * 0   graffiti-remover --scan-all               # debug artifacts
0 5 * * 0   inspector --generate-report               # weekly cleanliness score
```

### Collection Targets

| Target | Criteria | Action |
|--------|----------|--------|
| `tmp_files` | `*.tmp`, `*.bak`, `/tmp/**` older than 24h | Recycle → Delete |
| `stale_logs` | `*.log` not modified in 7 days (non-critical) | Archive → Delete |
| `dead_sessions` | Orphaned exec/tmux sessions >1h with no activity | Terminate |
| `expired_creds` | Credentials files older than 30 days | Rotate → Archive |
| `duplicate_files` | MD5 hash collision across workspace | Keep newest, delete rest |
| `debug_artifacts` | `.DS_Store`, `__pycache__`, `*.pyc`, `*.swp` | Immediate delete |

---

## Recycling Protocol

**No item is deleted without first completing the recycling step.**

### Protocol Steps

```
STEP 1 — SCAN: Identify item type (experiment, credential, config, log, code)
STEP 2 — EXTRACT VALUE:
  - Experiment results → cp -r to archive/experiments/YYYY-MM-DD/
  - Credentials        → append metadata to credentials/rotation.log (no secrets)
  - Configs            → cp to backup/configs/ with timestamp suffix
  - Logs               → grep for ERRORs/WARNINGs → append to archive/log-insights.md
  - Code snippets      → extract reusable functions → recycling/snippets/
STEP 3 — MARK: Tag item as RECYCLED in sanitization.log
STEP 4 — PURGE: Delete original
STEP 5 — REPORT: Log item count, bytes freed, Shannon earned
```

### Archive Directory Structure

```
workspace/
├── archive/
│   ├── experiments/YYYY-MM-DD/   # recycled experiment results
│   ├── log-insights.md           # patterns extracted from stale logs
│   └── snippets/                 # reusable code fragments
├── backup/
│   └── configs/                  # timestamped config backups
└── credentials/
    └── rotation.log              # credential rotation history (no secrets)
```

---

## Cleanliness Score (0-100)

The **Workspace Cleanliness Score** is computed by the inspector on each audit cycle. Score = sum of criterion scores.

| # | Criterion | Max pts | Bash Check |
|---|-----------|---------|-----------|
| 1 | No stale tmp files (>24h) | 20 | `find /tmp ~/.openclaw/workspace -name "*.tmp" -mtime +1 \| wc -l` → 0 = 20pts |
| 2 | No orphaned logs (>7 days, non-critical) | 20 | `find ~/.openclaw/workspace -name "*.log" -not -path "*/dsny/logs/*" -mtime +7 \| wc -l` → 0 = 20pts |
| 3 | No debug artifacts | 20 | `find ~/.openclaw/workspace -name "__pycache__" -o -name "*.pyc" -o -name ".DS_Store" \| wc -l` → 0 = 20pts |
| 4 | No duplicate files | 20 | `find ~/.openclaw/workspace -type f | xargs md5sum 2>/dev/null \| sort \| uniq -d -w32 \| wc -l` → 0 = 20pts |
| 5 | Archive directory present and structured | 20 | `[ -d ~/.openclaw/workspace/archive/experiments ] && echo OK` → OK = 20pts |

### Bash Score Command

```bash
#!/usr/bin/env bash
# dsny-score.sh — Compute workspace cleanliness score
WS=~/.openclaw/workspace
SCORE=0

# Criterion 1: No stale tmp files
TMP_COUNT=$(find /tmp "$WS" -name "*.tmp" -mtime +1 2>/dev/null | wc -l | tr -d ' ')
[ "$TMP_COUNT" -eq 0 ] && SCORE=$((SCORE+20)) && echo "✅ C1: No stale tmp files (+20)" \
  || echo "❌ C1: $TMP_COUNT stale tmp files (0)"

# Criterion 2: No orphaned logs
LOG_COUNT=$(find "$WS" -name "*.log" -not -path "*/dsny/logs/*" -mtime +7 2>/dev/null | wc -l | tr -d ' ')
[ "$LOG_COUNT" -eq 0 ] && SCORE=$((SCORE+20)) && echo "✅ C2: No orphaned logs (+20)" \
  || echo "❌ C2: $LOG_COUNT stale logs (0)"

# Criterion 3: No debug artifacts
DBG_COUNT=$(find "$WS" \( -name "__pycache__" -o -name "*.pyc" -o -name ".DS_Store" -o -name "*.swp" \) 2>/dev/null | wc -l | tr -d ' ')
[ "$DBG_COUNT" -eq 0 ] && SCORE=$((SCORE+20)) && echo "✅ C3: No debug artifacts (+20)" \
  || echo "❌ C3: $DBG_COUNT debug artifacts (0)"

# Criterion 4: No duplicate files (by md5)
DUP_COUNT=$(find "$WS" -type f \( -not -path "*/.git/*" \) | xargs md5sum 2>/dev/null | sort | uniq -d -w32 | wc -l | tr -d ' ')
[ "$DUP_COUNT" -eq 0 ] && SCORE=$((SCORE+20)) && echo "✅ C4: No duplicate files (+20)" \
  || echo "❌ C4: $DUP_COUNT duplicate sets (0)"

# Criterion 5: Archive structure present
if [ -d "$WS/archive/experiments" ] && [ -d "$WS/backup/configs" ]; then
  SCORE=$((SCORE+20)); echo "✅ C5: Archive structure present (+20)"
else
  echo "❌ C5: Archive structure missing (0)"
fi

echo ""
echo "🧹 DSNY Cleanliness Score: $SCORE / 100"
```

---

## Purge Authority

### Threshold
Any purge exceeding **10 files** or **100MB** of data requires **Commissioner sign-off**.

### Purge Request Format

```yaml
PURGE REQUEST
=============
Requested by: <agent-name>
Date: <YYYY-MM-DD HH:MM UTC>
Files targeted: <count>
Estimated size: <MB>
Reason: <justification>
Recycling completed: YES/NO
Recycling log: <path to recycling record>
Commissioner approval: PENDING / APPROVED / DENIED
Signature: <commissioner>
```

### Purge Log

All purges (approved or denied) are recorded in `dsny/logs/sanitization.log`:

```
[2026-03-22 03:00 UTC] PURGE | 47 files | 220MB | agent: collection-agent | approved by: commissioner | reason: weekly deep sweep
[2026-03-22 03:01 UTC] RECYCLE | 12 experiment dirs → archive/experiments/2026-03-22 | 3 configs → backup/configs/
```

**Silent mass deletions are strictly prohibited.** Any undocumented purge triggers a Violation Citation against the responsible agent.

---

## Shannon Economy

DSNY participation is incentivized via the **Shannon entropy economy**.

| Action | Shannon |
|--------|---------|
| Successful daily collection run (≥1 item collected) | +5 Shannon |
| Successful weekly deep sweep | +20 Shannon |
| Cleanliness score improvement (+10 pts) | +15 Shannon |
| Cleanliness score 100/100 maintained for 1 week | +50 Shannon |
| Recycling step completed before deletion | +2 Shannon per item |
| Commissioner approves purge (proper request filed) | +10 Shannon |
| Inspector submits weekly report | +10 Shannon |
| **VIOLATION: Leaving cruft (citation issued)** | **-10 Shannon** |
| **VIOLATION: Silent deletion (no log)** | **-25 Shannon** |
| **VIOLATION: Purge without Commissioner approval** | **-50 Shannon** |

### Shannon Logging

All Shannon transactions are appended to `dsny/logs/shannon.log`:

```
[2026-03-22 03:00 UTC] +5 Shannon | collection-agent | daily sweep: 12 tmp files collected
[2026-03-22 04:00 UTC] +2 Shannon | recycling-agent | recycled: 1 experiment dir
[2026-03-22 09:00 UTC] -10 Shannon | backend-architect | violation: stale logs in /workspace/logs/
```

---

## Sanitization Log

All DSNY actions are recorded at `dsny/logs/sanitization.log`.

### Log Format

```
[TIMESTAMP UTC] ACTION | AGENT | DETAIL | SHANNON DELTA
```

### Example Entries

```
[2026-03-22 03:00 UTC] COLLECT | collection-agent | 12 *.tmp files from /workspace | +5 Shannon
[2026-03-22 03:01 UTC] RECYCLE | recycling-agent | 3 experiment dirs → archive/ | +6 Shannon
[2026-03-22 03:05 UTC] PURGE-APPROVED | commissioner | 47 files, 220MB | weekly sweep | +10 Shannon
[2026-03-22 09:00 UTC] CITATION | inspector | backend-architect left stale logs >7d | -10 Shannon
[2026-03-22 09:00 UTC] SCORE | inspector | cleanliness score: 80/100 | no bonus
```

---

## Agent Workflows

### Collection Agent — Daily Run

```
1. Read collection schedule (targets for today's route)
2. Scan each target path for items matching collection criteria
3. For each item found:
   a. Tag as PENDING_COLLECTION in sanitization.log
   b. If count > 10 or size > 100MB: file purge request → wait for Commissioner
   c. Else: hand to recycling-agent for value extraction
4. After recycling completes: delete originals
5. Log results to sanitization.log
6. Mint Shannon for successful collection
```

### Street Cleaner — Hygiene Sweep

```
1. Scan workspace for naming violations (non-snake_case files in code dirs)
2. Scan for duplicates (md5 comparison)
3. Enforce directory structure (per AGENTS.md conventions)
4. Report violations to inspector; do not auto-rename without confirmation
5. Apply confirmed fixes; log changes
```

### Inspector — Weekly Audit

```
1. Run dsny-score.sh → capture score
2. Compare to last week's score
3. If improvement ≥ 10pts: award bonus Shannon
4. Generate Cleanliness Report (score + breakdown + citations issued)
5. Post report to dsny/logs/cleanliness-report-YYYY-MM-DD.md
6. If score < 60: escalate to Commissioner for emergency sweep
```

---

## Deliverable Format

When DSNY agents complete a task, they deliver in **GMRC format**:

```
## DSNY Report — [Agent Name] — [Date]

**Deliverables:** [What was collected/cleaned/recycled]
**Quality Check:** [Score before/after, items processed, bytes freed]
**How I Did It:** [Steps taken, tools used]
**Recommendations:** [Next sweep targets, repeat offender citations, schedule adjustments]
**Shannon:** [+/- Shannon earned/deducted this cycle]
```

---

## Runnable Scripts

All DSNY scripts live in `skills/dsny/scripts/` and are executable:

| Script | Purpose | Usage |
|--------|---------|-------|
| `dsny-score.sh` | Compute workspace cleanliness score (0-100) | `bash dsny-score.sh [workspace_path]` |
| `dsny-collect.sh` | Collection agent daily sweep | `bash dsny-collect.sh [--target TARGET] [--dry-run]` |

### Quick Start

```bash
# Check workspace cleanliness
bash ~/.openclaw/workspace/skills/dsny/scripts/dsny-score.sh

# Preview what would be collected (safe, no deletions)
bash ~/.openclaw/workspace/skills/dsny/scripts/dsny-collect.sh --dry-run

# Collect specific target
bash ~/.openclaw/workspace/skills/dsny/scripts/dsny-collect.sh --target debug_artifacts

# Full collection sweep (all targets)
bash ~/.openclaw/workspace/skills/dsny/scripts/dsny-collect.sh --target all
```

## File Structure

```
workspace/
├── skills/dsny/
│   ├── SKILL.md                  ← this file
│   ├── scripts/
│   │   ├── dsny-score.sh         ← cleanliness score bash script (runnable)
│   │   └── dsny-collect.sh       ← collection agent daily sweep (runnable)
│   └── autoresearch/
│       └── results.tsv           ← experiment log
├── dsny/
│   └── logs/
│       ├── sanitization.log      ← master log
│       ├── violations.log        ← citations
│       ├── shannon.log           ← Shannon ledger
│       └── cleanliness-report-*.md
├── archive/
│   ├── experiments/              ← recycled experiment dirs
│   └── log-insights.md          ← ERROR/WARNING patterns from archived logs
└── backup/
    └── configs/                  ← backed-up configs
```
