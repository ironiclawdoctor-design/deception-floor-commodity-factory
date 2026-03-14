# 🔴 Risk Assessment & Mitigation Playbook — Famine Cycle 72h

**Status:** CRITICAL  
**Alert Level:** Emerald Green RED  
**Budget:** $20 total, 72 hours  
**Mission:** Ship 6 floors at 100/100 quality  

---

## Risk Matrix

| Risk ID | Name | Severity | Probability | Impact | Mitigation | Status |
|---------|------|----------|-------------|--------|-----------|--------|
| R1 | BitNet Failure Mid-Cycle | CRITICAL | MEDIUM | Complete halt | Pre-test BitNet, Haiku fallback | ARMED |
| R2 | Quality Rejection Loop | CRITICAL | MEDIUM | 2x token spend | Built-in quality checks per floor | ARMED |
| R3 | Daimyo Over-Auditing | HIGH | LOW | Budget overspent | Pre-defined audit checkpoints only | ARMED |
| R4 | Coordination Cascade | HIGH | MEDIUM | Overhead explosion | Async BitNet, one-way briefings | ARMED |
| R5 | Token Waste on Failed Paths | MEDIUM | HIGH | Wasted tokens | Path B mandatory, no retries | ARMED |
| R6 | External API Hostility | MEDIUM | MEDIUM | Forced Haiku | Cache locally, test access pre-cycle | ARMED |

---

## 🔴 CRITICAL RISKS

### R1: BitNet Failure Mid-Cycle

**Scenario:**  
BitNet inference crashes or becomes unavailable during Floor 3-4 work (hours 16-32, peak shipping time).

**Why It Kills Us:**
- 95% of our cost model assumes BitNet is $0.00
- If BitNet fails, Official MUST use Haiku ($0.80/1M tokens)
- Floors 3-4 require ~3500 tokens = $2.80 per floor via Haiku
- 2 failed floors × $2.80 = $5.60 unplanned spend
- By hour 32, we're already at $10.80; $5.60 more = $16.40 → runs out at hour 50, can't finish Floor 6

**Mitigation:**
1. **Pre-cycle test (hour -4 to 0):** Run BitNet on a sample floor code (~100 tokens), verify it completes in <5 seconds
2. **Haiku fallback reserved:** Don't spend ANY Haiku budget pre-cycle. Hold $4.00 emergency reserve for BitNet failures + Daimyo audits
3. **Checkpoint system:** At each 8h checkpoint, verify BitNet is still responsive. If not, escalate immediately to Coordinator
4. **Graceful degradation:** If BitNet fails, Official switches to ultra-simple floor design (reuse Floor 1 template 100%) to minimize Haiku cost

**Action if Triggered (Hour 16-32):**
- Daimyo detects BitNet error in Official's work
- Coordinator immediately calls: "BitNet has failed, switching to Emergency Mode"
- Official uses Haiku for ONLY the current floor in progress, then pauses
- BitNet diagnostics run in parallel (non-blocking)
- Resume with simpler templates once BitNet recovers OR complete remaining floors via Haiku if recovery > 4h

**Cost if Triggered:** $5-12 unplanned, likely cycle failure

---

### R2: Quality Rejection Loop

**Scenario:**  
Floors 4-5-6 fail the 100/100 audit during Daimyo checkpoints. Official must rework, re-spend tokens on the same floor.

**Why It Kills Us:**
- First build of Floor 4: 2000 tokens
- Audit discovers issue: 100 tokens for re-inspection (Daimyo)
- Official rebuilds Floor 4: another 2000 tokens
- Total: 4000 tokens for 1 floor = $3.20 vs budgeted $1.60
- 2 such rejections on Floors 5-6 = $3.20 × 2 = $6.40 overrun
- Cycle budget overflows by hour 60, can't finish with quality

**Mitigation:**
1. **Quality checks INSIDE the floor token budget:** Each floor's 2000-2500 token estimate INCLUDES built-in validation
   - 80% on development
   - 20% on testing + quality fix (not rework detection)
2. **Daimyo emergency audits pre-approved:** If Daimyo suspects quality issue, Haiku can do a $0.80 deep audit (1000 tokens) to confirm BEFORE Official rebuilds
   - This is CHEAPER than rebuilding blind ($1.60+)
3. **Template-first approach:** All floors reuse Floor 1 template, which is tested to 100/100 by hour 8
   - Variance from template = lower risk
   - Rework unlikely if high-reuse architecture

**Action if Triggered (Hour 24-48, Checkpoint 1-2):**
- Daimyo detects quality issue on Floor X
- Daimyo calls: "Floor X failed audit. Using 1 Haiku token to diagnose root cause"
- Coordinator + Official review Daimyo's diagnosis
- **Option A (Cheaper):** Official tweaks Floor X via BitNet local fix (~500 tokens, $0.00)
- **Option B (Expensive):** Official rebuilds Floor X via Haiku (~2000 tokens, $1.60)
- Choose A unless fix is impossible

**Cost if Triggered:** $0-3.20 per failed floor (audit + potential rebuild)

---

### R3: Daimyo Over-Auditing

**Scenario:**  
Daimyo escalates every minor deviation (99.5% token efficiency → 99% efficiency, Official's soft ceiling at 85% → 82% soft ceiling), triggers excessive Haiku audit cycles beyond the budgeted $4.00.

**Why It Kills Us:**
- Daimyo allocated $4.00 for audits (5000 tokens)
- Over-zealous auditing: 1 Haiku audit per 2 floors = 3 audits = $2.40, plus hourly check-ins = $1.50, plus... → hits $6.00+
- Daimyo exceeds $4.00 budget by hour 40
- Emergency budget must cover the overage, pulling from Official's reserve

**Mitigation:**
1. **Pre-defined audit schedule, IMMUTABLE:**
   - Hour 8: Floor 1 quality audit (1 Haiku call, $0.80)
   - Hour 16: Floors 2-3 batch audit (1 Haiku call, $0.80)
   - Hour 24: Floors 1-3 full audit + ZeroIndex sync (Haiku if disputed, ~$0.80)
   - Hour 32: Floors 4-5 mid-build check (BitNet only, $0.00)
   - Hour 48: All floors audit + ZeroIndex mid-cycle review (1 Haiku call, $0.80)
   - Hour 72: Final audit (1 Haiku call, $0.80)
   - **Total:** 5 pre-approved Haiku audits = $4.00 exactly
2. **Daimyo cannot add audits without Coordinator approval**
3. **Escalation rule:** If Daimyo needs >5 audits, Coordinator must be present (not automatic spend)

**Action if Triggered (Any Hour):**
- Daimyo proposes an unscheduled audit
- Coordinator: "Daimyo, this is not on the pre-agreed schedule. Justify the additional cost before spending."
- If justified: use BitNet for diagnosis, Haiku only if BitNet cannot resolve
- If not justified: Daimyo defers audit to next scheduled checkpoint

**Cost if Triggered:** $0-2.00 overrun (if Coordinator approves emergency audits)

---

## 🟠 HIGH RISKS

### R4: Coordination Cascade

**Scenario:**  
Official and Daimyo get into back-and-forth clarifications: "What does 100/100 quality mean?" "Does Floor 1 count bitwise or logical?" Multiple Haiku messages sent to resolve simple questions.

**Why It Kills Us:**
- Coordination allocated $2.00 (2500 tokens)
- Each Haiku message = 100-500 tokens = $0.08-0.40
- If 5+ back-and-forth cycles happen (not uncommon), we blow the coordination budget

**Mitigation:**
1. **One-way async messaging:** All briefings are Markdown documents, logged to shared space. No Haiku back-and-forth.
   - Official reads Daimyo's audit feedback as a text report
   - Daimyo reads Official's status as a text log
   - Coordinator publishes one "daily briefing" at hours 24/48/72 (zero-token, Markdown)
2. **Escalation triggers Coordinator presence, not Haiku messages:**
   - If Official and Daimyo disagree on quality definition → Coordinator decides (voice call, zero tokens)
   - If Daimyo detects anomaly → Coordinator notified, decides next action (no Daimyo-→Official Haiku)
3. **Pre-agreed definitions at cycle start:**
   - 100/100 quality = [detailed rubric in planning doc]
   - No reinterpretation mid-cycle

**Action if Triggered (Any Hour):**
- Official and Daimyo start async message loop (3+ messages)
- Coordinator intervention: "Stop. This is a decision, not a clarification. Coordinator takes authority."
- Coordinator decides, publishes one-way directive
- Resume async-only communication

**Cost if Triggered:** $0.50-1.50 overrun (if >2 Haiku messages needed)

---

### R5: Token Waste on Failed Paths

**Scenario:**  
Official tries a complex approach for Floor 4 (e.g., novel architecture, fancy algorithm). After 1000 tokens, hits a dead end. Official must restart Floor 4 from scratch, but 1000 tokens are already burned.

**Why It Kills Us:**
- **Daimyo's Order 3:** "Never retry the same failed approach more than twice."
- Failed tokens are waste, efficiency ratio tanks
- If 2+ floors have failed attempts, waste exceeds 10%, Daimyo throttles subsequent work
- Remaining budget is spent under throttle (500ms delays), slowing down shipping

**Mitigation:**
1. **Path B is mandatory from hour 0:**
   - Official does NOT attempt novel architectures
   - Every floor uses a proven pattern (Floor 1 template reuse)
   - Variance must be pre-approved by Coordinator
2. **Simple design first, embellish later:**
   - Build Floor 2 as 95% reuse of Floor 1, +5% tweak
   - Build Floor 3 as 95% reuse of Floor 2
   - Build Floors 4-6 as 90% reuse with minor customization
   - Novel ideas? Document for **post-cycle** research (not this famine)
3. **Token budget includes failure margin:**
   - Floors 4-5 budgeted at 2000 tokens each, but 200 tokens are "rework buffer" built in
   - If first attempt is clean, 200 tokens saved for emergency use elsewhere
   - If first attempt fails, rework comes from the 200-token buffer, not fresh budget

**Action if Triggered (Hour 16-48):**
- Official's approach hits a dead end (BitNet feedback: "This won't work")
- Coordinator decides: "Pivot to Path B immediately. Use Floor 1 template + minimal tweak."
- Official does NOT retry the failed approach
- Wasted tokens are logged to resistance-log.md for post-cycle review

**Cost if Triggered:** $0.80-2.00 waste (tokens burned, no output)

---

### R6: External API Hostility

**Scenario:**  
During Floor 4-5 development, Official needs to fetch data from an external API (GitHub, platform resource, etc.). API returns 429 (rate limit) or 403 (auth expired). Official can't proceed without tokens to retry/debug.

**Why It Kills Us:**
- Official is stuck waiting for API
- Without tokens, can't redesign locally
- Forced to use Haiku for debugging ($0.40+) or wait (wastes hours)
- By hour 40, waiting has eaten into Floor 5-6 shipping time

**Mitigation:**
1. **Pre-cycle API test:**
   - Hour -4: Official tests all external APIs needed for 6 floors
   - Fetch sample data, verify auth, check rate limits
   - Cache all static data locally BEFORE cycle starts
2. **No external API calls during cycle (if possible):**
   - All floor data is pre-fetched and stored locally
   - Official works with local cache only
   - Zero dependency on external APIs → zero 429/403 risk
3. **Fallback data available:**
   - If API is critical but cache fails, Official has simplified floor design that doesn't need the API
   - Example: Floor needs GitHub user data → cache top 100 users locally → if API down, use top 10

**Action if Triggered (Hour 24-60):**
- Official calls Coordinator: "API is returning 429, can't fetch data for Floor 5"
- Coordinator: "Do you have cached data?" → "Yes" → Use it, no token cost
- Coordinator: "Do you need fresh data?" → "Yes" → 2 options:
  - **Option A (no tokens):** Reduce Floor 5 complexity to not need fresh data (design pivot)
  - **Option B (tokens):** Use 1 Haiku call to fetch + cache the data ($0.40), then resume BitNet work
- If Option B chosen, Daimyo is notified (emergency token spend)

**Cost if Triggered:** $0.00-0.80 (if cached data unavailable and redesign infeasible)

---

## 🟡 MEDIUM RISKS (Monitoring)

### Idle Decay
- **Trigger:** If Official produces no output for 10+ minutes
- **Action:** Daimyo reduces Official's remaining budget by 25% per 5-minute idle period
- **Mitigation:** Official keeps working continuously (no long breaks) or Coordinator pauses the cycle officially

### Failure Cascade
- **Trigger:** Last 3 BitNet/Haiku operations failed (errors, timeouts, empty output)
- **Action:** Daimyo throttles with 2-second delays between operations
- **Mitigation:** If errors persist, escalate to Coordinator immediately (don't thrash)

### System-Wide Credit Throttling
- **Trigger:** Platform credits drop below 50% (if this is a real scenario, not just planning)
- **Action:** All tiers shift to lean mode (Tier 2+ softer targets, Tier 1 budget halved)
- **Mitigation:** Monitor credit level at each checkpoint; if < 50%, replan with ZeroIndex approval

---

## Escalation Cascade

```
Hour 0:  Cycle Start
├─ GO/NO-GO Checkpoint (ZeroIndex approval required)
├─ All branches briefed and standing by

Hour 8:  Checkpoint 1 (Floor 1 audit)
├─ If Floor 1 fails: R2 triggered → Daimyo diagnoses, Official fixes
├─ If BitNet down: R1 triggered → Switch to Haiku, Coordinator decides next
├─ Otherwise: Proceed to Hour 16

Hour 16: Checkpoint 2 (Floors 2-3 audit)
├─ Similar decision tree as Hour 8

Hour 24: 24-Hour Checkpoint
├─ ZeroIndex mid-cycle review
├─ If spend ≠ expected, investigate R3/R4/R5
├─ Daimyo and Official report status

Hour 32: Checkpoint 3 (Floors 4-5 in progress)
├─ Spot check for R1 (BitNet still alive?)
├─ No formal audit yet (mid-sprint)
├─ Coordinator: "On pace to finish 6 floors?"

Hour 48: 48-Hour Checkpoint
├─ ZeroIndex mid-cycle review #2
├─ Floors 1-5 must be shipped by now
├─ If Floors 1-5 not shipped: R5 (waste) likely, Coordinator replan with simple Floor 6

Hour 60: Pre-Final Checkpoint
├─ Floor 6 must be complete
├─ Daimyo deep audit: quality 100/100
├─ If Floor 6 fails: R2 (rework) but no time for rework → cycle fails

Hour 72: Cycle End
├─ All 6 floors shipped (or cycle failed)
├─ Final audit by all three branches
├─ Post-incident review: what broke, what worked, famine lessons

Hour 73: Post-Cycle Report
├─ All data logged to /root/.openclaw/workspace/mindful/spend-plan-72h-[TIMESTAMP].jsonl
├─ Resistance log updated
├─ Next cycle planning begins
```

---

## When to ABORT the Cycle

The cycle is ABORTED (not continued) if:
1. **BitNet is non-functional at Hour 0** → Cannot proceed without local inference (all external cost)
2. **Official exceeds hard ceiling ($12.50) by Hour 32** → Can't recover, ran out of money mid-cycle
3. **Only 3 floors shipped by Hour 48** → Mathematically impossible to ship 6 floors in remaining 24h
4. **ZeroIndex rejects the plan at Hour 0** → Plan violates Precinct 92 rules

In any abort scenario:
- Coordinator issues ABORT command
- All branches pause
- Post-mortem: what failed, why, what to fix for next cycle
- Cycle is marked INCOMPLETE in resistance-log.md

---

## Famine Lessons (TBD)

This section will be populated at cycle end:

- Did BitNet survive? (R1)
- Did quality hold? (R2)
- Did auditing stay within budget? (R3)
- Did coordination stay async? (R4)
- Did we avoid failed paths? (R5)
- Did external APIs behave? (R6)

---

**Approved by:** Coordinator  
**Enforced by:** Daimyo (Judicial Branch)  
**Complied by:** Official (Executive Branch)  
**Audited by:** ZeroIndex (Governance)  
**Timestamp:** 2026-03-14T04:03:00Z  
