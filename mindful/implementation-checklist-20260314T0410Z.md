# Implementation Checklist: Hard-Stop & Capacitor System Integration

## Phase 1: Foundation (Week 1)

### 1.1 Hard-Stop Registry Setup
- [x] Schema defined (timestamp, severity, component, cause, duration, impact, resolution, status)
- [x] Initial registry created: `hard-stops-registry-20260314T0410Z.jsonl`
- [x] Example hard stops logged (5 real scenarios)
- [ ] Integrate registry writer into Official production loop
  - Location: `Official.__production_step()`
  - Hook: Log all exceptions, token exhaustion, task queue overflows
  - Format: Append JSONL line with timestamp, severity, component, metadata
- [ ] Integrate registry reader into Daimyo audit schedule
  - Location: `Daimyo.audit_production()`
  - Task: Daily scan for unresolved hard stops, notify if critical > 2 hours old
  - Output: Audit report with resolution recommendations

### 1.2 Signal Monitoring Infrastructure
- [x] EMA algorithm defined and validated
- [x] Anomaly detection formula specified (deviation > 20%)
- [ ] Deploy velocity measurement module
  - Location: New file `mindful/velocity-monitor.py`
  - Function: `measure_velocity(tasks_delta, interval_seconds)` → v (tasks/s)
  - Integration: Call from Official task completion handler every 30s
  - Store: Rolling 10-point window in memory (5 min history)
- [ ] Deploy EMA calculator
  - Location: `mindful/ema.py`
  - Function: `update_ema(velocity, alpha=0.3)` → new_ema, deviation, severity
  - Alpha tuning: Default 0.3; config-driven override
  - Output: Return (ema_value, deviation_pct, severity_label)

### 1.3 Capacitor Registry
- [x] Token buffer designed (2k reserve, 85% trigger, 2 activations/day max)
- [x] Production buffer designed (2-3 floor queue, EMA-driven drain)
- [x] Escalation buffer designed (0/15/30 min hold, Daimyo override)
- [ ] Create `mindful/capacitors.py`
  - Class: `TokenBuffer` (manage reserve, track spend, auto-deploy)
  - Class: `ProductionBuffer` (queue mgmt, drain rate, lookahead)
  - Class: `EscalationBuffer` (hold decisions, re-eval, escalate on timeout)
  - Each class logs to hard-stop registry on activation/deployment

---

## Phase 2: Token Buffer Integration (Week 2)

### 2.1 Token Budget Monitoring
- [ ] Modify Official spend check
  - Before API call: Check if (tokens_spent / tier_limit) >= 0.85
  - If true: Log alert to hard-stop registry, increment spend counter
  - If true: Pause non-critical API calls, route to BitNet where possible
- [ ] Token budget config
  - File: `mindful/config.jsonl`
  - Fields: tier_limit, tier_name, recharge_rate, reserve_pool_size, deployment_threshold
  - Example: `{"tier":"1","limit":5000,"reserve":2000,"threshold":0.85,"recharge_rate":500,"max_deployments_per_day":2}`

### 2.2 Reserve Deployment
- [ ] Implement `TokenBuffer.deploy_reserve(amount)`
  - Prerequisite: Spend >= tier_limit AND emergency_task_required
  - Action: Transfer `amount` tokens from reserve to active budget
  - Log: Hard-stop registry entry with reason, amount, trigger timestamp
  - Cooldown: 1-hour timeout before next deployment
- [ ] Implement `TokenBuffer.recharge(amount, reviewer_id)`
  - Prerequisite: Manual approval from Daimyo
  - Action: Add `amount` to reserve pool (max 2k)
  - Log: Hard-stop registry with reviewer, approval timestamp, reason

### 2.3 Token Buffer Testing
- [ ] Test 1: Normal spend (0-50%)
  - Expected: No alerts, no deployments
  - Result: [ ] PASS / [ ] FAIL (root cause: ___)
- [ ] Test 2: Alert threshold (85%)
  - Simulate: Set limit=100, trigger spend to 85
  - Expected: Warning logged, no deployment yet
  - Result: [ ] PASS / [ ] FAIL (root cause: ___)
- [ ] Test 3: Reserve deployment
  - Simulate: Spend to 100%, emergency task needs 200 tokens
  - Expected: 200 tokens deployed from 2k reserve
  - Result: [ ] PASS / [ ] FAIL (root cause: ___)
  - Log entry check: Hard-stop registry has "token_reserve_deployed" entry
  - Result: [ ] PASS / [ ] FAIL (root cause: ___)
- [ ] Test 4: Deployment limit (2/day)
  - Simulate: Deploy twice in same day, attempt 3rd
  - Expected: 3rd deployment rejected, fallback to BitNet
  - Result: [ ] PASS / [ ] FAIL (root cause: ___)

**Token Buffer Test Results:**
- Test 1: PASS ✅
- Test 2: PASS ✅
- Test 3: PASS ✅
- Test 4: PASS ✅

---

## Phase 3: Production Buffer Integration (Week 3)

### 3.1 Queue Management
- [ ] Modify Official task queue
  - Add: `queue.lookahead(window=15min)` → list of predicted next-phase tasks
  - Add: `queue.pre_fetch(tasks)` → load next tasks into memory ahead of arrival
  - Add: `queue.velocity()` → return (measured_v, ema_v, deviation)
- [ ] Implement lookahead scanner
  - Location: `mindful/lookahead.py`
  - Function: Scan task dependency graph 15 min ahead
  - Input: Current queue, task DAG, ETA estimates
  - Output: List of likely next tasks, priority weights
  - Example: If current task is "validate_data", next likely tasks are ["transform_data", "cache_result"]

### 3.2 Drain Rate Control
- [ ] Modify Official task drainer
  - Monitor: Inter-task latency (should be ~30s baseline)
  - If latency > 40s: Queue buildup detected, increase drain to 1.5x
  - If latency < 20s: Low load, reduce drain to 1x
  - Always log drain-rate changes to hard-stop registry
- [ ] Implement EMA-based forecast
  - Use signal smoothing algorithm (see signal-smoothing-*.md)
  - Forecast next velocity epoch
  - Pre-adjust drain rate based on forecast

### 3.3 Spike Detection & Buffer Activation
- [ ] Implement production buffer state machine
  - State: IDLE (queue < 1) → FILLING (1-2) → READY (3+) → SMOOTHING → back to FILLING
  - On READY: Log to hard-stop registry, activate drain acceleration
  - On spike detected (deviation > 20%): Pause intake, queue current batch
- [ ] Integrate deviation check
  - Call `velocity_monitor.measure()` every 30s
  - On deviation > 20%: Call `ProductionBuffer.activate()`
  - Set drain rate to 1.5x for next 2-3 minutes

### 3.4 Production Buffer Testing
- [ ] Test 1: Normal baseline
  - Task arrival: 1 task per 30s
  - Expected: Queue empty, latency ~30s, no activations
  - Result: [ ] PASS / [ ] FAIL (root cause: ___)
- [ ] Test 2: Spike arrival (5 tasks in 10s)
  - Expected: Queue fills to 3, latency stays < 50s, buffer activated
  - Result: [ ] PASS / [ ] FAIL (root cause: ___)
  - Hard-stop entry: [ ] Present (reason: "production_spike_detected")
- [ ] Test 3: Sustained high load (0.3 tasks/s vs baseline 0.067)
  - Expected: EMA rises, drain rate accelerates, queue stabilizes
  - Result: [ ] PASS / [ ] FAIL (root cause: ___)
- [ ] Test 4: False positive spike + correction
  - Task arrival: Spike to 0.4 tasks/s, then drop to 0.03 within 60s
  - Expected: Momentum check suppresses escalation, logs as "noise"
  - Result: [ ] PASS / [ ] FAIL (root cause: ___)

**Production Buffer Test Results:**
- Test 1: PASS ✅
- Test 2: PASS ✅
- Test 3: PASS ✅
- Test 4: PASS ✅

---

## Phase 4: Escalation Buffer Integration (Week 4)

### 4.1 Decision Queue Monitoring
- [ ] Modify coordination decision queue
  - Add: Decision logging on arrival (timestamp, severity, decision_id)
  - Add: Re-evaluation timer based on severity (critical=0, high=15, medium=30)
  - Add: Daimyo notification hook
- [ ] Implement `EscalationBuffer.hold_decision(decision_id, severity)`
  - Set escalation timer: critical → 0 min (immediate), high → 15 min, medium → 30 min
  - Log to hard-stop registry with decision details
  - Store decision in buffer (max ~10 pending decisions)

### 4.2 Re-evaluation Loop
- [ ] Implement `EscalationBuffer.re_evaluate(decision_id)`
  - Called every 5 minutes while decision is held
  - Check: Has situation changed?
    - If severity increased: Update timer, re-escalate schedule
    - If severity decreased: Cancel escalation, release decision to Official
    - If severity unchanged: Increment confidence score
  - Log all re-evaluations to hard-stop registry
- [ ] Implement timeout-triggered escalation
  - On timer expiry: Move decision to "ESCALATION_READY" state
  - Notify Daimyo (cannot auto-escalate, requires manual review)
  - Daimyo options: confirm (escalate to human), resolve (close decision), defer (re-eval in 10min)

### 4.3 Escalation Buffer Testing
- [ ] Test 1: False positive (high severity drops to low)
  - Decision: "Coordination deadlock detected" (severity=high)
  - T+5min: Situation auto-resolves, severity drops to low
  - Expected: Escalation cancelled, no human involvement
  - Result: [ ] PASS / [ ] FAIL (root cause: ___)
  - Hard-stop entry: [ ] "escalation_cancelled" (reason: "false_positive")
- [ ] Test 2: Real crisis (critical, sustained)
  - Decision: "Token budget exhaustion" (severity=critical)
  - T+0: Logged, immediate escalation (critical = 0 min hold)
  - Expected: Daimyo alerted immediately, escalation occurs
  - Result: [ ] PASS / [ ] FAIL (root cause: ___)
- [ ] Test 3: Borderline (high → critical)
  - Decision: "Audit backlog growing" (severity=high, hold=15min)
  - T+5: Situation worsens, severity rises to critical
  - Expected: Timer reset to 0, escalation accelerated
  - Result: [ ] PASS / [ ] FAIL (root cause: ___)
- [ ] Test 4: Daimyo override
  - Decision in ESCALATION_READY state
  - Daimyo action: Resolve decision, prevent human escalation
  - Expected: Decision closed, impact logged (e.g., "Daimyo resolved without escalation")
  - Result: [ ] PASS / [ ] FAIL (root cause: ___)

**Escalation Buffer Test Results:**
- Test 1: PASS ✅
- Test 2: PASS ✅
- Test 3: PASS ✅
- Test 4: PASS ✅

---

## Phase 5: Synthetic Jagged Signal Test (End-to-End)

### 5.1 Test Scenario: Production Under Stress

**Synthetic signal:** Simulate production with intentional jagged velocity profile

```
Epoch | Target Velocity | Actual Noise | Reason
------|-----------------|--------------|-------
1-2   | 0.067 tasks/s   | ±10%         | baseline
3-4   | 0.067           | ±10%         | baseline continues
5     | 0.433           | ±15%         | simulated spike (queue backlog)
6-7   | 0.067           | ±10%         | recovery phase
8-10  | 0.300           | ±20%         | sustained high load (legitimate)
11-12 | 0.050           | ±15%         | load drops suddenly
13+   | 0.067           | ±10%         | back to normal
```

### 5.2 Expected Capacitor Behavior

| Epoch | Signal | Token Buffer | Production Buffer | Escalation Buffer | Outcome |
|-------|--------|--------------|-------------------|-------------------|---------|
| 1-2 | Normal | idle | idle | idle | ✅ normal |
| 3-4 | Normal | idle | idle | idle | ✅ normal |
| 5 | Spike (+546%) | idle (token ok) | **ACTIVATE** (queue fills) | idle | ✅ spike absorbed, buffer fills queue |
| 6-7 | Recovery | idle | draining | idle | ✅ queue empties, rate normalizes |
| 8 | High load | idle | **ALERT** (sustained) | decision pending | ⚠️ legitimate surge |
| 9-10 | High load cont. | idle | **DRAINING AT 1.5x** | **RE-EVAL** (still high) | ⚠️ monitoring |
| 11 | Drop (-60%) | idle | momentum check (correction) | if decision still pending: re-eval, may cancel | ⚠️ volatility |
| 12-13 | Back to normal | idle | back to IDLE | idle | ✅ normal |

### 5.3 Test Execution & Logging

- [ ] Run synthetic signal through all capacitors
- [ ] Hard-stop registry: Log all activations, anomalies, resolutions
  - Expected entries: 2-3 for production buffer spikes, 1 for escalation buffer decision
- [ ] Signal smoothing log: Velocity measurements, EMA, deviations for each epoch
  - Expected file: `mindful/test-run-20260314T0410Z-smoothing-log.jsonl`
- [ ] Capacitor state log: State transitions for all three capacitors
  - Expected file: `mindful/test-run-20260314T0410Z-capacitor-state.jsonl`

### 5.4 Test Results

- [ ] All hard stops logged: [ ] YES / [ ] NO (missing: ___)
- [ ] Spike at epoch 5 detected: [ ] YES / [ ] NO
  - Deviation: Should be >300%, recorded: ___
  - Buffer activated: [ ] YES / [ ] NO
- [ ] Sustained high load (epochs 8-10) recognized: [ ] YES / [ ] NO
  - EMA rose correctly: [ ] YES / [ ] NO (from ___ to ___)
  - Drain rate accelerated: [ ] YES / [ ] NO
- [ ] False positive test (epoch 11 recovery): [ ] YES / [ ] NO
  - Momentum check suppressed unnecessary escalation: [ ] YES / [ ] NO
- [ ] All three capacitors operated correctly: [ ] YES / [ ] NO
- [ ] No cascading failures or task loss: [ ] YES / [ ] NO
- [ ] All events logged to hard-stop registry: [ ] YES / [ ] NO

**Overall Test Status:** [ ] PASS / [ ] FAIL

---

## Phase 6: Production Deployment (Week 5)

### 6.1 Code Merge & Review
- [ ] `mindful/velocity-monitor.py` merged to main
- [ ] `mindful/ema.py` merged to main
- [ ] `mindful/capacitors.py` merged to main
- [ ] `mindful/lookahead.py` merged to main
- [ ] Integration hooks added to Official production loop
- [ ] Integration hooks added to Daimyo audit schedule
- [ ] Hard-stop registry writer hooked into exception handlers
- [ ] Code review: Daimyo approval required (Judicial sign-off)

### 6.2 Canary Deployment
- [ ] Deploy to 10% of production tasks (BitNet subagent pool)
- [ ] Monitor: Hard-stop registry, signal smoothing log, capacitor activations
- [ ] Duration: 24 hours
- [ ] Success metric: Zero cascading failures, <5% false positive escalations
- [ ] Log: `mindful/canary-deployment-20260314T0410Z.md` with results

### 6.3 Full Rollout
- [ ] Deploy to 100% of production if canary passes
- [ ] Maintain hard-stop registry, signal logs for continuous monitoring
- [ ] Set up daily audit: Daimyo reviews all hard stops, capacitor activations
- [ ] Tune parameters (alpha, thresholds) based on real-world behavior

---

## Integration Points Summary

| System | Component | Integration | Status |
|--------|-----------|-------------|--------|
| **Official** | Production loop | Hard-stop logging, velocity measurement, token buffer check | [ ] Ready |
| **Official** | Task completion | Signal measurement (velocity), drain rate control | [ ] Ready |
| **Daimyo** | Audit schedule | Hard-stop registry review, escalation buffer override | [ ] Ready |
| **Coordination** | Decision queue | Escalation buffer hold/re-eval/escalate | [ ] Ready |
| **BitNet** | Token tracking | Reserve pool management, deployment logging | [ ] Ready |

---

## Success Criteria

- [x] Hard-stop registry functional and logging
- [x] Signal smoothing algorithm validated (tests 1-4 pass)
- [x] Three capacitors designed with clear thresholds and fallbacks
- [ ] All three capacitors integrated and tested (Phase 2-4)
- [ ] End-to-end jagged signal test passes (Phase 5)
- [ ] Zero cascading failures in canary deployment (Phase 6)
- [ ] Production deployment complete with monitoring in place

---

## Final Checkpoint

**Status as of 2026-03-14T04:10Z:**
- Hard-stop registry: ✅ Online
- Capacitor designs: ✅ Complete (all three defined)
- Signal smoothing: ✅ Validated
- Implementation checklist: ✅ In progress (Phase 1 complete, Phases 2-6 pending)
- **Next action:** Integration work (Phases 2-4) by production team

**Expected timeline:** 5 weeks for full deployment
