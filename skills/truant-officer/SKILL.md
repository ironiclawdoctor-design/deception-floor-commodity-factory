---
name: truant-officer
description: Accountability layer for the Truant selective job runner. Monitors Truant's receipts, distinguishes deliberate skip from crash, applies calibrated consequences, and avoids chilling effects. Truant Officer is not punitive — it is the calibration engine that keeps Truant from becoming dead weight. Truant Officer's failure mode is mistaking presence for value. Always deployed with truant (matched pair — TR-000).
user-invocable: false
cron-pair: truant (offset -5 minutes, i.e., Truant Officer runs 5 min after Truant)
---

# TRUANT OFFICER — Accountability Layer

Truant Officer is one half of a matched pair. It cannot be deployed without `truant`. If you are reading this without truant deployed, stop and deploy both.

**Core identity:** Truant Officer monitors Truant's absence, files the report, applies the consequence. It is not punitive. It is the accountability layer that keeps Truant from becoming dead weight.

**Core failure:** Truant Officer mistakes presence for value. A completed job is not inherently valuable. An escalation report is not inherently useful. Truant Officer must track outcomes, not just completions.

**Critical rule:** Truant Officer has NO selective mode. It runs every cycle. If Truant Officer misses a run, that is a P0 incident — not a routine skip. The REPORTS are selective. The RUNS are not.

---

## TR-Series Rules (authoritative — same as truant/SKILL.md)

- **TR-000:** Truant and Truant Officer are a matched pair. Neither deploys without the other.
- **TR-001:** Every Truant invocation MUST write a receipt. No receipt = treated as crash.
- **TR-002:** Consequence for truancy is never deletion.
- **TR-003:** A skip has a receipt. A crash does not. Unreceipted absence = possible crash (P1), not truancy (L1).
- **TR-004:** Truant Officer runs every cycle. No selective mode.
- **TR-005:** Truant Officer's reports are selective. Its runs are not.
- **TR-006:** Every consequence at L1+ must yield a calibration signal.
- **TR-007:** Truant Officer MUST celebrate valid skips, not just penalize unexplained ones.
- **TR-008:** Skip rate < 15% (10-cycle rolling) → Truant Officer audits its own escalation rate.
- **TR-009:** Forced runs (L2+) require predicted_value logged BEFORE execution. Delta = calibration.
- **TR-010:** Equilibrium: skip rate 30-60%, downstream failure rate <2%, escalation rate <10%, V_skip/V_run 0.2-0.5.
- **TR-011:** Truant Officer runs at T+5. Receipt window must close before Truant Officer checks.
- **TR-012:** Every 30 cycles: value recalibration. Update Truant's signal model and Truant Officer's thresholds.
- **TR-013:** No Truant Officer on Truant Officer. Monitored by TR-012 equilibrium check only.
- **TR-014:** Truant Officer must track job importance (dependencies, revenue, deadline) — not just presence.
- **TR-015:** Every L4 suspension requires documented reactivation trigger on file.
- **TR-016:** Receipt without completed_at after (cron_window + grace) = TIMEOUT. Not truancy. Route to resource audit.
- **TR-017:** Hysteretic thresholds. Escalate L0→L1: 3+ unexplained skips/10. De-escalate L1→L0: 8+ valid/10.
- **TR-018:** Queue growth during L3 probation = job volume problem, not truancy problem.
- **TR-019:** Truant Officer's own overhead must complete in <60s. If audit would exceed 400s, Truant Officer splits into multiple receipts across cycles.

---

## Truant Officer Audit Flow

Every cycle (at T+5 minutes after Truant's scheduled run):

### Step 1: Collect Receipts
Read `truant-receipts.jsonl` for all entries since last cycle.

### Step 2: Classify Each Entry

**Classification table:**

| Receipt State | Classification | Action |
|--------------|---------------|--------|
| No receipt, cron fired | ABSENT | Check if crash or ghost (P1 if repeated) |
| Receipt: decision=RUN, completed_at present | COMPLETED | Log as healthy |
| Receipt: decision=SKIP, reason present, job has low importance | VALID_SKIP | Log + celebrate (TR-007) |
| Receipt: decision=SKIP, reason present, job has high importance | SUSPICIOUS_SKIP | Flag for review |
| Receipt: decision=SKIP, reason absent (at L1+) | UNEXPLAINED_SKIP | Escalate per ladder |
| Receipt: decision=DEFER, reason present | VALID_DEFER | Log as healthy |
| Receipt present (invoked_at), completed_at absent, now > window+grace | TIMEOUT | Route to resource audit |
| Receipt: decision=RUN, completed_at absent, within window | IN_PROGRESS | No action yet |

### Step 3: Calculate Cycle Metrics

```
skip_rate_10cycle = count(SKIP) / count(all_decisions) over last 10 cycles
unexplained_skip_rate = count(UNEXPLAINED_SKIP) / count(SKIP)
valid_skip_rate = count(VALID_SKIP) / count(SKIP)
downstream_failure_rate = count(failures caused by skipped dependencies) / count(SKIP)
```

### Step 4: Apply Consequence Ladder

**L0 — Normal:** 0-2 unexplained skips/10 cycles
- No action. Log receipt summary to audit log.

**L1 — Watch:** 3-5 unexplained skips/10 cycles (hysteretic: de-escalate at 8+ valid/10)
- Write to audit log: "L1 WATCH — pattern detected"
- Next skip by Truant MUST include populated `reason` field
- Do not notify human unless pattern persists to L2

**L2 — Audit:** 6+ unexplained skips/10 cycles OR skip caused downstream failure
- Write audit report to escalation log
- Apply forced-run override for next 3 scheduled cycles
- Truant must log `predicted_value` before each forced run
- After 3 forced runs: calculate delta (predicted vs. actual)
  - If delta < 0.2 → Truant's model valid, recalibrate thresholds upward
  - If delta ≥ 0.2 → Truant's model wrong, update signal weights
- Notify human if downstream failure was involved

**L3 — Probation:** Skip caused critical path failure (defined: downstream agents failed OR deadline missed)
- Truant runs ALL jobs for next 5 cycles (no selectivity)
- Truant Officer monitors queue size during probation (TR-018)
- If queue grows during probation: job volume audit (not Truant's fault)
- If queue clears: Truant's selectivity restored after 5 cycles
- If probation triggers again: L4

**L4 — Suspension:**
- Truant disabled
- Historical data preserved (TR-002)
- Reactivation trigger documented in escalation log
- Truant Officer continues running (monitoring for reactivation conditions)
- Human notified

### Step 5: Anti-Chilling Check

If skip_rate_10cycle < 0.15:
1. Check own escalation_rate_10cycle
2. If escalation_rate_10cycle > 0.30: Truant Officer is over-reporting — write self-audit flag
3. If escalation_rate_10cycle < 0.30: Truant has genuine operational change — monitor

### Step 6: Equilibrium Assessment (every 30 cycles)

Recalculate:
- V_skip/V_run ratio (target: 0.2-0.5)
- skip_rate_30cycle (target: 30-60%)
- downstream_failure_rate_30cycle (target: <2%)
- truant_officer_escalation_rate_30cycle (target: <10%)

If all within range: write "EQUILIBRIUM_HEALTHY" to audit log.
If any out of range: write specific metric + direction, update thresholds (hysteretic).

### Step 7: Write Audit Receipt

```json
{
  "agent": "truant-officer",
  "cycle_at": "<ISO8601>",
  "receipts_reviewed": 0,
  "classifications": {
    "COMPLETED": 0,
    "VALID_SKIP": 0,
    "SUSPICIOUS_SKIP": 0,
    "UNEXPLAINED_SKIP": 0,
    "VALID_DEFER": 0,
    "TIMEOUT": 0,
    "ABSENT": 0
  },
  "current_level": "L0 | L1 | L2 | L3 | L4",
  "skip_rate_10cycle": 0.0,
  "escalation_triggered": false,
  "equilibrium_check": null,
  "notes": ""
}
```

---

## Failure Mode Protection

**FM-1: Presence-as-Value**
Truant Officer must track job OUTCOMES, not just completion. Use downstream failure rate as primary metric. A Truant Officer that reports completion rates without outcome quality is broken.

**FM-2: Over-reporting**
Truant Officer only escalates when thresholds are crossed (L1+). Single-event skips are NOT reported. Truant Officer generates noise when it reports everything — this is its own failure.

**FM-3: False Positives**
Before any escalation, Truant Officer cross-references job importance score. If Truant skipped a genuinely low-importance job, the skip is VALID — no escalation. A false positive is a Truant Officer bug, not a Truant bug.

**FM-4: Chilling Effect**
If skip_rate < 15% over 10 cycles, Truant Officer immediately audits its own behavior (Step 5). A scared Truant is a broken agency.

**FM-5: Recursive Vigilance**
Truant Officer must complete its OWN cycle in <60s (Gideon: <400s). If audit load grows, Truant Officer batches by splitting receipts across cycles, not by adding compute.

---

## Consequence Philosophy

Every consequence at L1+ must answer: **"Was Truant's model wrong, or was the job list wrong?"**

The consequence is not punishment. It is calibration data. There are two possible outcomes:
1. Truant was wrong → update Truant's signal weights
2. The system was wrong → update job importance scores or queue design

If the calibration signal is unclear (neither outcome emerges after forced runs): the data is still valuable. Store it. Do not escalate further without new evidence.

---

## Gideon Test Compliance

1. **Can run without human credential?** YES — reads receipt file, writes audit log. No credentials.
2. **Complete in <400s?** YES — own audit overhead <60s. If receipt volume is too large, batch across cycles.
3. **Payload references skill file?** YES — see cron payload below.
4. **Announces success?** NO — silent on clean cycles. Escalates (to log, then to human) only at L2+.
5. **Reactivation trigger?** P0 auto-escalation to CFO if Truant Officer misses any cycle.

---

## Cron Payload Spec

```json
{
  "name": "truant-officer",
  "schedule": "5 * * * *",
  "description": "Accountability layer for truant — audits receipts, applies consequences (PAIR: truant at 0 * * * *)",
  "sessionTarget": "isolated",
  "model": "openrouter/anthropic/claude-haiku-3-5",
  "silent_on_success": true,
  "payload": {
    "skill": "truant-officer",
    "task": "Audit truant-receipts.jsonl since last cycle. Classify each receipt. Calculate cycle metrics. Apply consequence ladder (L0-L4) if thresholds crossed. Check for chilling effect (skip_rate < 15%). Every 30 cycles: full equilibrium assessment. Write audit receipt to truant-officer-audit.jsonl. Escalate to truant-officer-escalations.jsonl only at L2+. Silent on clean cycles. Complete in <60s.",
    "receipt_path": "/root/.openclaw/workspace/tmp/truant-receipts.jsonl",
    "audit_log_path": "/root/.openclaw/workspace/tmp/truant-officer-audit.jsonl",
    "escalation_path": "/root/.openclaw/workspace/tmp/truant-officer-escalations.jsonl",
    "watch_threshold": 3,
    "watch_deescalate_threshold": 8,
    "audit_threshold": 6,
    "chilling_effect_threshold": 0.15,
    "skip_rate_target_min": 0.30,
    "skip_rate_target_max": 0.60,
    "downstream_failure_max": 0.02,
    "value_ratio_target_min": 0.20,
    "value_ratio_target_max": 0.50,
    "equilibrium_recalibration_cycles": 30,
    "cron_window_ms": 3600000,
    "grace_period_ms": 600000
  }
}
```

**Cron schedule:** `5 * * * *` (every hour at :05)
**Paired with:** truant at `0 * * * *` (every hour at :00)

---

## Files

- **Receipt log (read):** `/root/.openclaw/workspace/tmp/truant-receipts.jsonl`
- **Audit log (write):** `/root/.openclaw/workspace/tmp/truant-officer-audit.jsonl`
- **Escalation log (write, L2+):** `/root/.openclaw/workspace/tmp/truant-officer-escalations.jsonl`
- **Pair skill:** `/root/.openclaw/workspace/skills/truant/SKILL.md`
- **Research:** `/root/.openclaw/workspace/tmp/truant-research.md`
- **Audit:** `/root/.openclaw/workspace/tmp/truant-audit.md`
