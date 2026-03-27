# TRUANT / TRUANT OFFICER — Raw Research Findings
# Generated: 2026-03-27
# Autoresearch Phase: Primary Research Agent (v1)

---

## Research Question 1: What signals indicate a Truant agent?

### The Signal Problem
Distinguishing deliberate skip from crash/timeout is the hardest part of truancy detection. A crashed agent and a selective agent look identical from the outside: both produce zero output. The difference is internal state.

### Signal Taxonomy

**Class A: Presence Signals (the agent ran)**
- Heartbeat write: agent wrote to a known file (e.g., `truant-heartbeat.jsonl`) with timestamp
- Log entry: agent emitted a log line at job start
- Lock file: agent created a pid/lock at invocation
- Receipt: agent wrote a completion token even if work was skipped

**Class B: Absence Signals (the agent did not run)**
- No heartbeat within window
- No log entry
- No receipt token
- Process table: no pid matching agent pattern during scheduled window

**Class C: Skip Signals (agent ran but skipped the work)**
- Heartbeat present, but work artifact absent
- Log entry: "SKIP: <reason>" present
- Skip token written to structured log
- Metrics: job_invoked=1, job_completed=0, skip_reason=<enum>

**Class D: Crash Signals (agent ran, then died)**
- Heartbeat present at T=0, absent at T=completion
- Exit code non-zero in process table or log
- Partial output artifact (truncated file, incomplete JSON)
- Error log present
- No completion token despite heartbeat

### Detection Decision Tree

```
Did agent heartbeat? 
  NO → ABSENT (crash or truant — cannot distinguish without receipt)
       → Check: did cron scheduler fire? 
           NO → SCHEDULER_FAILURE (not truancy)
           YES → AGENT_ABSENT (possible truancy OR silent crash)
  YES → Did agent write completion token?
        NO → Did agent write skip token?
              YES → DELIBERATE_SKIP (truancy)
              NO → CRASH (heartbeat + no token + no skip = died mid-run)
        YES → Did work artifact appear?
              YES → COMPLETED (healthy)
              NO → SKIP_WITH_RECEIPT (intentional zero-work run)
```

### Key Insight: Receipt Protocol
A Truant agent MUST write a receipt on every invocation, even skips. The receipt is the difference between truancy (visible, deliberate) and ghosting (invisible, broken). Without the receipt, Truant Officer cannot distinguish the two.

**Receipt Schema:**
```json
{
  "agent": "truant",
  "invoked_at": "<ISO8601>",
  "job_id": "<cron-job-id>",
  "decision": "RUN | SKIP | DEFER",
  "reason": "<why>",
  "signal_score": 0.0-1.0,
  "completed_at": "<ISO8601 or null>"
}
```

### Distinguishing Deliberate Skip from Crash

| Signal | Deliberate Skip | Crash/Timeout |
|--------|----------------|---------------|
| Heartbeat at T=0 | ✓ | ✓ |
| Skip token | ✓ | ✗ |
| Completion token | ✓ (with SKIP decision) | ✗ |
| Error log | ✗ | ✓ (often) |
| Partial artifacts | ✗ | ✓ (sometimes) |
| Pattern: same jobs skipped | ✓ | random |
| Pattern: time-correlated | random (value-based) | ✓ (resource contention) |

### The Interesting vs. Important Failure Mode
Truant's core failure: it mistakes "interesting" for "important."
- Interesting = high signal to Truant's model (novel, complex, engaging)
- Important = high impact to the agency (deadline, dependency, revenue)

Signal to detect this failure: `skipped_jobs_with_downstream_dependencies > threshold`
If Truant skips Job A and Job B fails because it depended on Job A's output → Truant has optimized for the wrong metric.

---

## Research Question 2: What is the correct consequence for truancy?

### What NOT to do
- **Deletion**: destroys the selective signal. If Truant was right to skip 80% of jobs, deleting it destroys 80% efficiency.
- **Promotion**: truancy is not proof of intelligence. A skipping agent that skips *wrong* is worse than a compliant agent.
- **Silence**: no consequence = no calibration. Truant drifts toward infinite selectivity (never runs).
- **Punishment loops**: consecutive escalating punishments create noise, not signal.

### The Correct Consequence Ladder

**Level 0 — Normal (0-2 unexplained skips in 10 runs)**
- No action
- Receipt logged, Truant Officer notes pattern

**Level 1 — Watch (3-5 unexplained skips in 10 runs)**
- Truant Officer flags: "Pattern detected, monitoring"
- Next skip requires mandatory reason tag
- Truant must include `reason` field in receipt
- No job impact

**Level 2 — Audit (6+ unexplained skips OR skip caused downstream failure)**
- Truant Officer generates audit report
- Truant's skip criteria re-evaluated against actual job importance
- Mandatory run on next 3 scheduled jobs (override selectivity)
- If overridden jobs were indeed low-value: Truant's model vindicated, recalibrate threshold
- If overridden jobs had value: Truant's model wrong, update signal weights

**Level 3 — Probation (skip caused critical path failure)**
- Truant runs ALL jobs for 5 cycles (no selectivity)
- Truant Officer monitors every run
- At end of probation: Truant's selectivity restored IF audit clean
- If probation triggers again: Level 4

**Level 4 — Suspension (repeated critical path failures)**
- Truant disabled, replaced by compliant agent temporarily
- Truant's historical data preserved (the signal is still valuable)
- Reactivation trigger: manual CFO review + updated signal spec

### Key Principle: Consequence Must Teach
Every consequence at L1-L4 must answer: "Did Truant's model need updating, or was the job list wrong?"
The consequence is not punishment — it is calibration data. If Truant was right and the system was wrong, the system updates. If Truant was wrong, Truant's weights update.

### The Forced Run Protocol (L2+)
When Truant is forced to run jobs it would have skipped:
1. Truant runs the job
2. Truant records its predicted value score BEFORE seeing results
3. Job completes, actual value measured
4. Delta (predicted vs. actual) is the calibration signal
5. If |delta| > threshold → model update
6. If |delta| < threshold → Truant's model was correct, skip was valid

This is the core feedback loop. Truancy without calibration is drift. Truancy with calibration is intelligence.

---

## Research Question 3: When does Truant Officer become the problem?

### The Truant Officer Failure Modes

**FM-1: Presence-as-Value (the core failure)**
Truant Officer mistakes "ran" for "did good work."
Signal: Truant Officer's reports show job completion rates but not outcome quality.
Fix: Truant Officer must track job outcomes, not just completions.

**FM-2: Over-reporting**
Truant Officer files a report for every skip, flooding the agency with noise.
Signal: Truant Officer generates more reports than Truant generates skips.
Fix: Truant Officer must have its own threshold — only report patterns, not single events.

**FM-3: False Positives**
Truant Officer flags legitimate selective work as truancy.
Signal: Truant Officer's reports correlate with low-importance job queues (Truant was right).
Fix: Truant Officer must cross-reference job importance score before flagging.

**FM-4: Chilling Effect**
Truant is afraid to skip even low-value work because Truant Officer will report it.
Signal: Truant's skip rate drops to near-zero, but agency throughput does not improve.
Fix: Truant Officer must celebrate valid skips, not just penalize unexplained ones.

**FM-5: Recursive Vigilance**
Truant Officer runs so frequently/intensively it becomes a resource drain.
Signal: Truant Officer consumes >20% of the compute budget it's supposed to protect.
Fix: Truant Officer must have its own cron budget cap.

### The Meta-Problem: Who Watches Truant Officer?
Truant Officer can itself become a truant. If Truant Officer skips its audit runs, the entire accountability system fails silently.

Resolution: Truant Officer has NO selective mode. It runs every cycle, no exceptions. If Truant Officer misses a run, that is automatically a P0 incident.

But: Truant Officer's REPORTS can be selective. It runs every time, but only escalates when thresholds are crossed.

### The Chilling Effect Threshold
A healthy Truant skip rate: 30-70% (optimizing signal over noise)
Chilling effect signature: skip rate drops below 15% with no corresponding value improvement

If skip rate < 15%: Truant Officer is over-reporting
If skip rate > 85%: Truant is ghosting (broken or gaming)
Healthy range: 15-85%, with median around 40-60%

---

## Research Question 4: What is the equilibrium?

### Equilibrium Definition
The system reaches equilibrium when:
1. Truant's skip rate is stable (not drifting toward 0% or 100%)
2. Skipped jobs have measurably lower value than completed jobs
3. Truant Officer's escalation rate is stable and low
4. Agency throughput per compute unit is higher than a compliant agent baseline

### The Equilibrium Math

Let:
- S = skip rate (0.0-1.0)
- V_skip = average value of skipped jobs
- V_run = average value of completed jobs
- C = compute cost per job
- R = Truant Officer overhead per cycle

Equilibrium condition:
`V_run - (V_skip * (1-S) * C) - R > V_baseline`

Where V_baseline = value if Truant ran every job (compliant agent).

Truant is net-positive if: `V_run/V_baseline > 1 + R/V_run`

I.e., Truant's selectivity gain must exceed Truant Officer's overhead.

### Practical Equilibrium Signals

**System is healthy:**
- Skip rate: 30-60%
- Downstream failures caused by skips: <2%
- Truant Officer escalation rate: <10% of cycles
- Job outcome quality (run jobs): consistently above median

**System needs rebalancing:**
- Truant Officer escalates >30% of cycles → Truant's selectivity is wrong
- Downstream failures >10% → Truant's model is wrong (interesting ≠ important)
- Skip rate <15% → chilling effect active
- Skip rate >80% with no improvement in value → Truant is ghosting

### The Equilibrium Maintenance Protocol

Every 30 cycles:
1. Recalculate V_skip vs V_run
2. If V_skip/V_run > 0.8 → Truant's skipping non-selectively (not enough discrimination)
3. If V_skip/V_run < 0.2 → Truant's model may be too aggressive (investigate chilling effect)
4. Optimal target: V_skip/V_run in range 0.2-0.5 (skipped jobs are clearly less valuable)

---

## TR-Series Rules (Draft)

### TR-000: Pair Identity
Truant and Truant Officer are a matched pair. Neither is deployed without the other. Truant without Truant Officer = unchecked drift. Truant Officer without Truant = surveillance theater.

### TR-001: Receipt Mandatory
Every Truant invocation MUST write a receipt. RUN, SKIP, DEFER — all receipts. No receipt = signal loss = treated as crash.

### TR-002: No Deletion
Consequence for truancy is never deletion. Truant's historical skip data is agency intelligence. Deletion is information destruction.

### TR-003: Distinguish Skip from Crash
A skip has a receipt. A crash does not. Truant Officer treats unreceipted absences as possible crashes (P1), not truancy (L1).

### TR-004: Truant Officer Runs Every Cycle
Truant Officer has no selective mode. It is a clock, not an agent. If Truant Officer misses a run, that is a P0 system failure.

### TR-005: Reports Are Selective, Runs Are Not
Truant Officer runs every cycle. Truant Officer escalates only when thresholds are crossed. The difference between a working Truant Officer and a broken one is not run rate — it is escalation calibration.

### TR-006: Consequence Must Teach
Every consequence at L1+ must yield a calibration signal. If the consequence doesn't update a model (Truant's or the job list's), it is theater.

### TR-007: Celebrate Valid Skips
Truant Officer must distinguish "unexplained skip" from "explained skip that was correct." A Truant that skips correctly is the highest-value state. It must be reinforced, not penalized.

### TR-008: Chilling Effect Detection
If Truant's skip rate drops below 15%, Truant Officer must check its own escalation rate. Chilling effect is a Truant Officer failure, not a Truant success.

### TR-009: Forced Run = Calibration
When Truant is forced to run a job (L2+ consequence), it must record its predicted value before running. The delta (predicted vs. actual) is the calibration signal. Without the delta, forced runs are punishment, not learning.

### TR-010: Equilibrium is Measurable
The pair is healthy when: skip rate is stable (30-60%), downstream failure rate <2%, Truant Officer escalation rate <10%, and V_skip/V_run ratio is 0.2-0.5.

### TR-011: Cron Pair Offset
Truant runs on schedule T. Truant Officer runs at T+5 minutes. This gives Truant time to write its receipt before Truant Officer checks. If Truant Officer runs before receipt window closes, it will generate false positives.

### TR-012: 30-Cycle Recalibration
Every 30 cycles, the pair undergoes value recalibration. Job importance scores are re-evaluated against actual outcomes. Truant's signal model is updated. Truant Officer's thresholds may adjust.

### TR-013: No Truant Officer on Truant Officer
Meta-surveillance creates recursion traps. Truant Officer is not itself subject to selective monitoring. It either runs or it doesn't, and both states are observable without another layer.

### TR-014: Interesting ≠ Important
Truant's failure mode is optimizing for signal richness over agency value. Truant Officer must track job importance (downstream dependencies, revenue impact, deadline proximity) — not just presence. A beautiful skip of a critical job is a failure, not a success.

### TR-015: The Reactivation Trigger
Every suspension (L4) must have a documented reactivation trigger. Without it, suspension becomes permanent deletion by neglect.

---

## Cron Pair Spec

### TRUANT Cron Payload
```json
{
  "name": "truant",
  "schedule": "0 * * * *",
  "description": "Selective job runner — optimizes for signal over noise",
  "sessionTarget": "isolated",
  "model": "openrouter/anthropic/claude-sonnet-4-5:beta",
  "payload": {
    "skill": "truant",
    "task": "evaluate and selectively execute pending jobs",
    "receipt_path": "/root/.openclaw/workspace/tmp/truant-receipts.jsonl",
    "job_queue_path": "/root/.openclaw/workspace/tmp/truant-queue.jsonl",
    "signal_threshold": 0.4
  }
}
```

### TRUANT OFFICER Cron Payload
```json
{
  "name": "truant-officer",
  "schedule": "5 * * * *",
  "description": "Accountability layer — monitors Truant receipts and applies consequences",
  "sessionTarget": "isolated",
  "model": "openrouter/anthropic/claude-sonnet-4-5:beta",
  "payload": {
    "skill": "truant-officer",
    "task": "audit truant receipts from last cycle, apply consequences if thresholds crossed",
    "receipt_path": "/root/.openclaw/workspace/tmp/truant-receipts.jsonl",
    "audit_log_path": "/root/.openclaw/workspace/tmp/truant-officer-audit.jsonl",
    "escalation_path": "/root/.openclaw/workspace/tmp/truant-officer-escalations.jsonl",
    "watch_threshold": 3,
    "audit_threshold": 6,
    "chilling_effect_threshold": 0.15
  }
}
```

---

## Self-Score: Research Agent Assessment

**Coverage of research questions (25 pts each):**
- Q1 (Signals): 25/25 — Full taxonomy, decision tree, receipt protocol, distinction matrix
- Q2 (Consequences): 24/25 — Ladder complete, forced run protocol strong, could add more on system-blames-itself case
- Q3 (Truant Officer failure): 24/25 — 5 failure modes, chilling effect threshold, meta-problem addressed
- Q4 (Equilibrium): 23/25 — Math model present, practical signals clear, could add hysteresis handling

**TR-series completeness:** 15 rules (TR-000 through TR-015), covering all major dynamics

**Cron pair spec:** Both payloads included with offset (T+5), schema complete

**Total Research Score: 96/100**

Gaps:
- Hysteresis handling for threshold crossings (avoid oscillation at boundary)
- What happens to the job queue when Truant is on probation (L3) — does queue grow?
- Timeout handling edge case (agent invoked but takes >cron_window to complete)

---

*Research Agent v1 complete. Submitting for auditor review.*
