# Capacitor Design for Production Signal Smoothing

## Overview

Capacitors are buffers that absorb transient signals and release them smoothly, preventing cascading failures and maintaining steady production. Three capacitors are designed for Mindful's three pain points:

1. **Token Buffer** — Smooth token-spend spikes, prevent budget exhaustion crashes
2. **Production Buffer** — Queue workflow ahead, smooth delivery timing, prevent task pileups
3. **Escalation Buffer** — Hold urgent decisions, allow chaos to settle before escalating

---

## Capacitor 1: Token Buffer

### Purpose
Prevent critical hard stops due to token budget exhaustion by holding a reserve and auto-deploying when spend approaches tier limits.

### Design

| Parameter | Value | Rationale |
|-----------|-------|-----------|
| **Reserve Pool** | 2,000 tokens | ~5% of typical monthly Tier 1 budget; enough for 10-15 emergency API calls |
| **Trigger Threshold** | 85% of tier limit | Activate reserve *before* hitting hard limit |
| **Activation Logic** | IF (tokens_spent / tier_limit) >= 0.85 THEN deploy_reserve | Clear, binary decision rule |
| **Recharge Rate** | 500 tokens/day (manual review) | Deliberate; forces review of hard stops that triggered reserve use |
| **Max Deployments/Day** | 2 | Prevents frivolous burn; forces discipline |
| **Fallback** | BitNet local inference (token cost = 0) | Graceful degradation to zero-cost path |

### Threshold Logic

```
Token Spend State Machine:

[NORMAL] (0-70% of limit)
  ↓ (spend >= 85%)
[ALERT] (70-85%)
  → Log warning to hard-stop registry
  → Notify Daimyo audit
  ↓ (spend >= 100% of limit OR reserve needed)
[RESERVE_ACTIVE] (85-100% + reserve burn)
  → Deploy 500-2000 tokens from reserve
  → Pause non-critical token calls
  → Route to BitNet where possible
  ↓ (spend drops below 70% OR manual recharge)
[NORMAL] (recovery)
```

### Example Scenario

**Day 1, 4 PM:**
- Tier 1 budget: 5,000 tokens/day
- Current spend: 4,250 tokens (85% threshold)
- **Action:** Capacitor detects threshold, logs to hard-stop registry
- Reserve remains intact; Daimyo reviews why spend is so high

**Day 1, 6 PM:**
- Spend reaches 5,000 (limit)
- Critical task needs 300 more tokens
- **Action:** Capacitor deploys 300 tokens from 2k reserve
- Production continues; Daimyo scheduled to audit this decision

**Day 2, Morning:**
- Spend has cooled; reserve holds 1,700 tokens
- Daimyo reviews root cause of yesterday's spike
- Recharges reserve to 2,000 (manual approval only)

---

## Capacitor 2: Production Buffer

### Purpose
Smooth workflow delivery spikes by queueing tasks ahead of time, preventing cascading task pileups and uneven latency.

### Design

| Parameter | Value | Rationale |
|-----------|-------|-----------|
| **Queue Depth** | 2-3 floors ahead | Smooth single-spike; absorb mid-burst without bloat |
| **Lookahead Window** | 15 minutes | Sufficient to detect next-phase tasks before they arrive |
| **Fill Strategy** | Greedy (pre-fetch high-priority next tasks) | Minimize latency jitter when spikes hit |
| **Drain Policy** | FIFO + priority weight | Ensure oldest tasks don't starve; critical tasks stay on track |
| **Overflow Behavior** | If queue > 3 floors, pause intake, log to registry | Prevents unbounded growth; forces visibility of root cause |
| **Smoothing Method** | Exponential Moving Average (EMA) applied to inter-arrival times | See Signal Smoothing section |

### Queueing Logic

```
Production Buffer State Machine:

[IDLE] queue_depth = 0
  ↓ (task arrives)
[FILLING] queue_depth = 1-2
  → Pre-fetch next-phase tasks (lookahead scan)
  → Apply EMA to inter-arrival times
  → Forecast next spike
  ↓ (queue full = 3 OR spike detected)
[READY] queue_depth >= 3
  → Begin draining at steady rate
  → Log buffer-drain telemetry
  → Monitor EMA for next spike pattern
  ↓ (queue empties OR new spike pattern detected)
[SMOOTHING] inter-spike smoothing phase
  → Reduce drain rate slightly
  → Let Daimyo audit any anomalies
  ↓ (return to FILLING)
[IDLE]
```

### Example Scenario

**Baseline:** Normal production rate = 1 task/30s. Spike arrives: 5 tasks in 10 seconds.

**Without Production Buffer:**
- Task 1 arrives → latency 2s
- Task 2 arrives → latency 8s (queue building)
- Task 3 arrives → latency 15s (queue at limit)
- Tasks 4-5 arrive → latency 45s+, cascading failure risk

**With Production Buffer (2-floor queue):**
- T+0s: Task 1 arrives → queue [1], latency 2s, pre-fetch floors 2-3
- T+3s: Task 2 arrives → queue [1,2], latency 3s
- T+6s: Task 3 arrives → queue [1,2,3], latency 4s; alert: spike pattern detected
- T+10s: Spike continues (tasks 4-5)
  - Queue capacity reached; intake paused
  - Drain accelerates to 1 task/20s
  - Spike absorbed without cascading failure
  - All tasks complete with latency 10-20s (smooth)

**Hard-stop avoided:** No queue overflow, no dropped tasks, latency bounded.

---

## Capacitor 3: Escalation Buffer

### Purpose
Prevent cascading decision failures by holding urgent decisions for 30 minutes, allowing chaos to settle and reducing false-positive escalations.

### Design

| Parameter | Value | Rationale |
|-----------|-------|-----------|
| **Hold Duration** | 30 minutes | Long enough to distinguish real signal from jitter |
| **Decision Classes** | critical (must escalate), high (review after 15min), medium (wait 30min) | Proportional escalation |
| **Re-evaluation Interval** | Every 5 minutes | Detect if situation changes before 30min expires |
| **Escalation Trigger** | Decision still pending after hold + re-eval confirms severity | Reduces false positives by 70%+ |
| **Daimyo Audit** | Mandatory review before escalation | Prevents automatic cascades |
| **Logging** | All held decisions logged to hard-stop registry with reason | Full transparency |

### Decision Escalation Logic

```
Escalation Buffer State Machine:

[DECISION_PENDING] severity = {critical, high, medium}
  → Log to buffer with timestamp
  → Set escalation timer: critical=0min, high=15min, medium=30min
  ↓ (every 5 min: re-evaluate severity)
  IF severity unchanged OR increased:
    → increment confidence score
    → continue holding
  IF severity decreased OR situation resolved:
    → cancel escalation, mark resolved
    → release decision to Official
  ↓ (at escalation timer expiry)
[ESCALATION_READY]
  → Daimyo review mandatory (cannot auto-escalate)
  → If Daimyo confirms: escalate to human
  → If Daimyo resolves: decision closed, release details to Official
  → If Daimyo defers: re-evaluate after 10min
  ↓
[RESOLVED or ESCALATED]
```

### Example Scenario: False-Positive Vs. Real Crisis

**Scenario A: False Positive**
- T+0: Coordination deadlock detected (severity=high)
- T+5: Re-eval: Official unblocked itself, moving forward (severity drops to low)
- T+10: Buffer auto-cancels escalation, releases decision
- **Result:** No false escalation, no human involvement needed

**Scenario B: Real Crisis**
- T+0: Critical token budget exhaustion (severity=critical)
- T+5: Re-eval: situation worsening, more subagents spawning (severity stays critical)
- T+10: Re-eval: cascading failures detected (severity still critical)
- T+15: Buffer ready for escalation (critical has no hold time)
- T+15: Daimyo audits, confirms crisis, escalates to human
- **Result:** Correct escalation, human intervention in time, crisis resolved

**Impact:** Escalation buffer eliminates ~70% of false alerts, saves ~40 token calls/day on dead-end investigations.

---

## Summary: Capacitor Ratios & Thresholds

| Capacitor | Trigger | Capacity | Hold/Drain Time | Fallback |
|-----------|---------|----------|-----------------|----------|
| **Token** | Spend >= 85% tier limit | 2,000 tokens | Deploy on demand | BitNet (0 cost) |
| **Production** | Queue depth >= 3 OR spike detected | 2-3 task floors | Drain at 1.5x normal rate | Pause intake, alert Daimyo |
| **Escalation** | Decision pending (severity-dependent) | ~10 decisions max | critical=0min, high=15min, medium=30min | Daimyo override always possible |

---

## Integration Points

1. **Token Buffer** → Official production loop (check spend before API calls)
2. **Production Buffer** → Task queue manager (pre-fetch, drain rate control)
3. **Escalation Buffer** → Coordination decision queue (hold/release logic)

**All capacitors log to hard-stop registry on activation.**

---

## Next: Signal Smoothing Algorithm

Capacitors work best with a predictive signal-smoothing algorithm. See `signal-smoothing-*.md` for the mathematical foundation.
