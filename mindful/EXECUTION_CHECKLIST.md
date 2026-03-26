# ✅ Execution Checklist — Famine Cycle 72h

## Pre-Cycle: Hours -4 to 0

### Phase 1: Infrastructure Readiness (Hour -4)

- [ ] **BitNet Status Check**
  - [ ] BitNet process running? `ps aux | grep bitnet`
  - [ ] llama.cpp available? `which llama-cli` or verify /usr/local/bin/llama-cli
  - [ ] Test inference on sample code (~100 tokens, should complete <5s)
    - Sample test: "def hello(): return 'world'"
    - Expected output: ~2 lines, <1s execution
  - [ ] CPU cores available? `nproc` should be ≥2
  - [ ] Memory available? `free -h | grep Mem` should show >2GB free
  
- [ ] **Haiku Access Verified**
  - [ ] Platform API key set? `echo $CLAUDE_API_KEY` (masked check)
  - [ ] Credit balance >$25? (We only use up to $20, need margin)
  - [ ] Haiku endpoint responding? Test call with minimal request
  
- [ ] **File System Ready**
  - [ ] Workspace directory exists: `/root/.openclaw/workspace/mindful/`
  - [ ] Spend plan file present: `spend-plan-72h-2026-03-14T04.03Z.jsonl`
  - [ ] Risk assessment file present: `risk-assessment-72h.md`
  - [ ] Resistance log directory: `/root/.openclaw/workspace/precinct92-...` exists
  - [ ] Data directories writable: test `touch /tmp/test-write` ✅ then cleanup

- [ ] **Network Connectivity**
  - [ ] GitHub API accessible? `curl -s https://api.github.com/octocat | head -5`
  - [ ] No NAT/firewall issues blocking platform API? Test with Haiku call

**Approval:** ZeroIndex reviews checklist at Hour -3

---

### Phase 2: Branch Briefing (Hour -3)

- [ ] **Official (Shipping) Briefed**
  - [ ] Received spend plan document
  - [ ] Understands token budget: $12.50 total
  - [ ] Understands floor targets: 6 floors, 100/100 quality each
  - [ ] Knows BitNet is primary, Haiku is emergency fallback
  - [ ] Has floor templates ready (or will generate them in-cycle)
  - [ ] Knows audit checkpoints at hours 8, 16, 24, 36, 48, 72
  - [ ] Signature: _______________  Date: _______________

- [ ] **Daimyo (Auditing) Briefed**
  - [ ] Received spend plan document
  - [ ] Understands audit budget: $4.00 total (5 Haiku calls pre-approved)
  - [ ] Audit schedule locked in (hours 8, 16, 24, 48, 72)
  - [ ] Soft ceiling for Official: $10.00 (80% of $12.50)
  - [ ] Hard ceiling for Official: $12.50
  - [ ] Knows how to use Daimyo's Authority (escalation levels 0-3)
  - [ ] Signature: _______________  Date: _______________

- [ ] **Coordinator (Oversight) Briefed**
  - [ ] Received spend plan + risk assessment
  - [ ] Understands escalation paths and abort conditions
  - [ ] Ready to make on-the-fly decisions (Path B, audits, pivots)
  - [ ] Knows emergency contact for each branch (or async message channel)
  - [ ] Signature: _______________  Date: _______________

- [ ] **ZeroIndex (Compliance) Briefed**
  - [ ] Reviewed spend plan against Precinct 92 rules
  - [ ] Plan is LEGAL and APPROVED? (or blocked with required changes)
  - [ ] Checkpoints: initial (hour 0), mid-cycle (hour 36), final (hour 72)
  - [ ] Plan status: ✅ APPROVED / ❌ BLOCKED (if blocked, list required changes below)
  - [ ] ZeroIndex decision: _______________  Date: _______________

---

### Phase 3: Technical Validation (Hour -2)

- [ ] **Official's Workflow Tested**
  - [ ] Can Official generate a floor design? (Test on Floor 0, mock)
    - [ ] Output folder structure correct?
    - [ ] Quality validation logic works?
  - [ ] BitNet inference chain works end-to-end?
  - [ ] Can Haiku fallback trigger cleanly (if needed)?
  - [ ] Result logged correctly for Daimyo review?

- [ ] **Daimyo's Audit Workflow Tested**
  - [ ] Can Daimyo read Official's output?
  - [ ] Can Daimyo run quality validation?
  - [ ] Alert system works (Daimyo can notify Coordinator)?
  - [ ] Budget tracking dashboard updated correctly?

- [ ] **Coordinator's Decision Log Set Up**
  - [ ] Decision log file created: `/root/.openclaw/workspace/mindful/decisions-72h.md`
  - [ ] Template ready for decision entries (time, decision, rationale, outcome)
  - [ ] Coordinator can quickly write decisions and publish

- [ ] **ZeroIndex Compliance Check Automated**
  - [ ] Script ready to validate spend plan against rules
  - [ ] Output format: list of violations (empty = compliant)
  - [ ] Run pre-cycle: `./scripts/check-compliance.sh` → should be ✅

---

### Phase 4: Go/No-Go Decision (Hour 0)

**FINAL GO/NO-GO CHECKPOINT**

- [ ] **All infrastructure checks passed?** ✅ / ❌
  - If ❌: list failures below, fix, re-check before proceeding
  
- [ ] **All branches briefed and ready?** ✅ / ❌
  - If ❌: resolve, re-brief affected branch
  
- [ ] **ZeroIndex compliance approved?** ✅ / ❌
  - If ❌: do NOT proceed. Amend plan and recheck.
  
- [ ] **Risk assessment reviewed?** ✅ / ❌
  - All branches understand R1-R6 and mitigation paths
  
- [ ] **Budget tracking set up and running?** ✅ / ❌
  - Dashboard rendering, spend log recording, alerts active

**GO/NO-GO DECISION:**
- [ ] **GO** — All checks passed, begin cycle immediately
- [ ] **DELAY** — Issues found, fix and re-check (do not start cycle until all green)
- [ ] **ABORT** — Critical blockers identified, cycle cannot proceed

**Approved by:** Coordinator  
**Time:** _______________  
**Decision:** _______________  

---

## During Cycle: Checkpoints

### Checkpoint 1: Hour 8 (Floor 1 Complete)

- [ ] **Floor 1 shipped?** ✅ / ❌
  - If ❌: diagnose why, adjust pace for remaining floors
  
- [ ] **Quality 100/100?** ✅ / ❌
  - Daimyo audit complete, no issues found
  - If ❌: Official reworks, cost logged to budget
  
- [ ] **Tokens spent ≤ $2.00?** ✅ / ❌
  - Check spend-log: Actual / Planned
  - If >$2.00: slow down, review BitNet performance
  
- [ ] **BitNet still alive?** ✅ / ❌
  - Test inference with small call (~50 tokens)
  - If ❌: R1 triggered, escalate to Coordinator
  
- [ ] **Daimyo audit clean?** ✅ / ❌
  - No escalations, no cost overruns
  - If issues: log to resistance-log.md

**Status:** ✅ PROCEED / 🟡 CAUTION / ❌ ESCALATE

**Coordinator Notes:** _______________

---

### Checkpoint 2: Hour 16 (Floors 2-3 Complete)

- [ ] **Floors 2-3 shipped?** ✅ / ❌
  - If ❌: assess whether pace is sustainable to hour 72
  
- [ ] **Quality 100/100 each?** ✅ / ❌
  - Daimyo batch audit, no rejections
  
- [ ] **Cumulative spend ≤ $3.20?** ✅ / ❌
  - Plan target: $2.00 (Floor 1) + $1.20 (Floor 2) + $1.20 (Floor 3) = $4.40 (allows $1.20 overhead)
  - Actual: _____________
  - If over: Coordinator reviews why, adjusts remaining pace
  
- [ ] **Efficiency ratio ≥ 2:1?** ✅ / ❌
  - Output bytes / tokens spent should be healthy
  - If <2:1: token waste suspected, Daimyo investigates
  
- [ ] **No critical failures?** ✅ / ❌
  - R1 (BitNet): still up? Test again.
  - R4 (Coordination): still async-only? No Haiku message loops?
  - R5 (Failed paths): Any wasted tokens? If yes, document.

**Status:** ✅ PROCEED / 🟡 CAUTION / ❌ ESCALATE

**Coordinator Notes:** _______________

---

### Checkpoint 3: Hour 24 (24-Hour Mark, Floors 1-3+ Complete)

- [ ] **Floors 1-3 definitely shipped and approved?** ✅ / ❌
  
- [ ] **Floor 4 in progress or complete?** ✅ / ❌
  - If complete: ahead of schedule ✨
  - If in progress: on track
  - If not started: behind schedule 🟡, Coordinator reviews
  
- [ ] **Cumulative spend ≤ $8.00?** ✅ / ❌
  - Target: 40% of $20 budget, 50% of time
  - Actual spend: _____________
  - Cost per floor so far: _____________
  
- [ ] **ZeroIndex mid-cycle review: PASSED?** ✅ / ❌
  - No rule violations detected
  - Spend trajectory sustainable
  - If issues: ZeroIndex blocks continuation until resolved
  
- [ ] **Daimyo reporting normally?** ✅ / ❌
  - All audits on schedule
  - Audit budget ≤ $2.00 spent (half of $4.00 allocated)
  - If Daimyo overrunning: R3 triggered, Coordinator restricts future audits
  
- [ ] **Coordinator decision log updated?** ✅ / ❌
  - All decisions since Hour 0 logged with time, rationale, outcome

**24-Hour Summary:**
- Floors shipped: ___ / 6
- Cumulative cost: $___ / $20
- Pace assessment: ✅ ON TRACK / 🟡 TIGHT / ❌ UNSUSTAINABLE
- Top risk right now: _______________

**Status:** ✅ PROCEED / 🟡 CAUTION / ❌ ESCALATE

**Coordinator Signature:** _______________

---

### Checkpoint 4: Hour 36 (Midpoint, Floors 1-4 Complete)

- [ ] **Floors 1-4 all shipped?** ✅ / ❌
  - If yes: on pace for 6 floors (2 floors per 24h)
  - If no: assess if Floors 5-6 can be compressed into remaining 36h
  
- [ ] **Quality audit passed on Floors 1-4?** ✅ / ❌
  - All 100/100? Or any rework?
  
- [ ] **Cumulative spend ≤ $13.00?** ✅ / ❌
  - Target: 65% of $20 budget, 50% of time
  - Allows 50% buffer for final push
  - Actual: _____________
  
- [ ] **ZeroIndex final verification: APPROVED?** ✅ / ❌
  - Confirm trajectory to $20 by hour 72
  - No mid-course corrections needed?
  
- [ ] **BitNet performance over last 12h?** ✅ / ❌
  - Stable? Fast? Any errors?
  - If degrading: risk R1 monitoring intensifies
  
- [ ] **No cascade escalations from R1-R6?** ✅ / ❌
  - If any risk triggered: document outcome, lessons learned

**Midpoint Summary:**
- 4/6 floors complete (67% progress)
- $____ spent out of $20 (____% budget used)
- Remaining pace: ___ floors in 36 hours (final push)
- Risk level: 🟢 LOW / 🟡 MEDIUM / 🔴 HIGH

**Status:** ✅ PROCEED / 🟡 CAUTION / ❌ ESCALATE

**Coordinator Signature:** _______________

---

### Checkpoint 5: Hour 48 (48-Hour Mark, Floors 1-5 Complete)

- [ ] **Floors 1-5 all shipped?** ✅ / ❌
  - If yes: only Floor 6 left, final 24h is floor-building + final audits
  - If no: CRITICAL 🔴 — can't ship 6 floors in remaining 24h at normal pace
  
- [ ] **Quality 100/100 on all 5 floors?** ✅ / ❌
  - Any rework in progress? If yes, will it block Floor 6?
  
- [ ] **Cumulative spend ≤ $16.00?** ✅ / ❌
  - Target: 80% of $20 budget, 67% of time (tight, but possible)
  - Actual: _____________
  - Remaining for Floor 6 + final audits: $_____________
  
- [ ] **Floor 6 design ready?** ✅ / ❌
  - Can be built in remaining 24h?
  - Any complexity that requires >2500 tokens?
  
- [ ] **Daimyo ready for final audit push?** ✅ / ❌
  - Audit budget remaining: $____ (should be ~$1.20)
  - Final checkpoint scheduled for hour 72
  
- [ ] **Coordinator confident in finishing 6 floors?** ✅ / ❌
  - If no: declare ABORT or MODIFY (reduce Floor 6 scope)

**48-Hour Summary:**
- 5/6 floors complete (83% progress)
- $___ spent out of $20 (____% used)
- Final push: 1 floor in 24 hours
- Risk: 🟢 NORMAL / 🟡 TIGHT / 🔴 CRITICAL

**Abort Decision (if applicable):**
- [ ] Continue to Floor 6 (normal path)
- [ ] Reduce Floor 6 scope (smaller floor, ship same 6 with less complexity)
- [ ] Abort cycle (not enough time/budget for 6 floors at 100/100)

**Status:** ✅ PROCEED / 🟡 TIGHT / ❌ ABORT

**Coordinator Signature:** _______________

---

### Checkpoint 6: Hour 60 (Pre-Final Check, Floor 6 Near Complete)

- [ ] **Floor 6 in final stages?** ✅ / ❌
  - Can be shipped within next 12 hours?
  
- [ ] **Quality audit ready for Floor 6?** ✅ / ❌
  - All prior floors ready for final sign-off?
  
- [ ] **Budget remaining: < $2.00?** ✅ / ❌
  - Should have ~$4.00 left (50% of $20)
  - Actual: _____________
  - This covers final audits + any emergency fixes
  
- [ ] **All decision logs up to date?** ✅ / ❌
  - Ready for final post-incident report

**60-Hour Status:**
- 6/6 floors: ___ complete, ___ in QA, ___ ready to ship
- Cumulative spend: $____ / $20
- Time remaining: 12 hours
- Final push: QA audit + ship Floor 6

**Status:** ✅ FINISH LINE / 🟡 URGENT / ❌ CRITICAL

---

### Checkpoint 7: Hour 72 (Cycle Complete)

- [ ] **All 6 floors shipped?** ✅ / ❌
  - If ❌: CYCLE FAILED — document why in post-incident review
  
- [ ] **All 6 floors pass 100/100 quality audit?** ✅ / ❌
  - Daimyo final sign-off on each floor
  - Any failures? If yes, cycle is incomplete (rework needed)
  
- [ ] **Final spend ≤ $20.00?** ✅ / ❌
  - Cumulative: $_____________
  - Budget remaining: $_____________
  - If over: BUDGET VIOLATION — log to resistance-log.md
  
- [ ] **All branches completed their missions?**
  - Official: shipped 6 floors ✅ / ❌
  - Daimyo: audited all, enforced budget ✅ / ❌
  - Coordinator: oversaw cycle, made decisions ✅ / ❌
  - ZeroIndex: verified compliance ✅ / ❌
  
- [ ] **Resistance log updated?** ✅ / ❌
  - All failures, escalations, risks triggered documented
  
- [ ] **Post-cycle report queued for generation?** ✅ / ❌

**FINAL STATUS:**

- **Mission:** Ship 6 floors at 100/100 quality in $20 budget, 72 hours
- **Result:** ✅ SUCCESS / 🟡 PARTIAL (N floors shipped) / ❌ FAILED
- **Floors shipped:** ___ / 6
- **Quality:** All 100/100? ✅ / ❌
- **Cost:** $____ / $20.00
- **Cost per floor:** $____ (target: $3.33)
- **Efficiency ratio:** ___:1 (target: ≥3:1)

---

## Post-Cycle: Hour 72-73

- [ ] **Post-cycle report generated**
  - File: `/root/.openclaw/workspace/mindful/post-incident-72h-[TIMESTAMP].md`
  - Sections: Executive Summary, Floors Shipped, Risk Events, Lessons, Recommendations
  
- [ ] **Resistance log updated**
  - All failures, escalations, overruns documented
  - Link to spend plan and post-incident report
  
- [ ] **Famine lessons extracted**
  - What worked? (Keep doing it)
  - What broke? (Fix for next cycle)
  - Which risks were real? (Update risk assessment for next cycle)
  - Which were false alarms? (Adjust planning)
  
- [ ] **Debrief scheduled**
  - All branches (Official, Daimyo, Coordinator, ZeroIndex)
  - Time: _______________
  - Topics: successes, failures, improvements for next cycle
  
- [ ] **Next cycle planning begins** (if authorized)
  - Incorporate lessons from this cycle
  - Update spend plan template with actual data
  - Schedule next famine drill

---

## Sign-Off

**Cycle Started:** _______________  
**Cycle Ended:** _______________  

**Official (Shipping):** _______________  
**Daimyo (Auditing):** _______________  
**Coordinator (Oversight):** _______________  
**ZeroIndex (Compliance):** _______________  

---

**This checklist is sacred. Every box must be checked or explicitly waived by Coordinator.**  
**Do not skip. Do not guess. Do not proceed until confirmed.**  
