# Nemesis Feasibility: Autonomous Subagent Spawning for Mendez-Gemini Enclave

**Assessed by:** nemesis-feasibility-subagent-spawn  
**Date:** 2026-03-15 12:35 UTC  
**Scope:** Autonomous child agent spawning from corrected document + constraint analysis  
**Cost Discipline:** Tier 0-2 only, $0.00  

---

## Executive Summary

**Can we spawn child agents autonomously from the corrected document?** ✅ **YES**

**What constraints exist?** 🛡️ **Three critical, two architectural**

**Recommendation for Nemesis delegation workflow?** 📋 **Implement with caveats**

---

## Part 1: Can We Spawn Child Agents Autonomously?

### Answer: YES, with preconditions

The corrected `mendez-gemini-enclave-corrected.md` document **does not technically block** autonomous subagent spawning, but it also **doesn't explicitly authorize** it. The authorization exists in a separate document: `AUTHORIZATION.md`.

**Current state:**
- ✅ `sessions_spawn` tool is available to main agent
- ✅ AUTHORIZATION.md grants full delegation scope to Fiesta
- ✅ NateMendez.md establishes agent persona and doctrine
- ⚠️ Corrected document is **infrastructure spec only** (hardware, departments, oversight)
- ✅ Precaching wrapper exists (`zero-token-subagent-wrapper.sh`)

**Verdict:** Autonomous spawning is **technically feasible** and **authorized** but requires **explicit workflow definition** before delegation to Nemesis.

---

## Part 2: Constraints for `sessions_spawn` with `runtime="subagent"`

### Constraint 1: Hard Prohibition (Critical)
**Sub-agents cannot spawn sub-agents.**

```
From OpenClaw docs:
"Sub-agents are not allowed to call sessions_spawn (no sub-agent → sub-agent spawning)"
```

**Impact on Mendez-Gemini Enclave:** 
- ❌ If a spawned subagent needs to delegate further work, it **cannot** spawn its own children.
- ✅ Workaround: Only main agent spawns. Subagents report back to main, which decides on further delegation.

---

### Constraint 2: Tool Restrictions (Critical)
**Subagents lose session tools by default.**

```json
From session-tool.md:
"Sub-agents default to the full tool set minus session tools 
(configurable via tools.subagents.tools)"
```

**Specific restrictions:**
- ❌ Subagents cannot call `sessions_spawn` (spawn children)
- ❌ Subagents cannot call `sessions_send` (route to other sessions)
- ❌ Subagents cannot call `sessions_list` (enumerate sessions)
- ❌ Subagents cannot call `sessions_history` (read other session transcripts)

**Impact:** Subagents are **isolated** — they cannot coordinate with siblings or chain work.

---

### Constraint 3: Visibility Scoping (Medium)
**Subagents can only see their own session tree.**

```json
Default: "tools.sessions.visibility": "tree"
  → Current session + sessions spawned by current session
  → Sandboxed sessions: hardclamped to "spawned" visibility
```

**Impact on Enclave:**
- ✅ Subagents are compartmentalized (network segmentation enforced)
- ⚠️ But they cannot inspect parent or sibling work (useful for isolation, risky for coordination)

---

### Constraint 4: Timeout Architecture (Medium)
**Subagent runs are auto-archived.**

```
agents.defaults.subagents.archiveAfterMinutes: default 60
  → Subagent sessions auto-delete after 60 minutes (configurable)
```

**Impact:** 
- ✅ Cleanup is automatic (no orphaned sessions)
- ⚠️ Long-running work must complete within timeout window
- ✅ For Enclave: 60-min default suits most tasks (commodity analysis, build orders, monitoring snapshots)

---

### Constraint 5: No Agent-to-Agent Escalation (Architectural)
**Subagents cannot spawn under different agent IDs.**

```
sessions_spawn parameter: agentId
  Allowlist: agents.list[].subagents.allowAgents
  Default: ["<current agent id only>"]
  Cannot be "*" for subagents spawned by subagents (subagents can't spawn)
```

**Impact:**
- ✅ Main agent can spawn under Fiesta, NateMendez, Automate, Official, Daimyo (if allowlisted)
- ❌ Subagent cannot switch spawning contexts
- ✅ For Enclave: Works fine because only main agent decides escalation

---

## Part 3: Recommendation for Nemesis Delegation Workflow

### Proposed Architecture: "Call-and-Report" Pattern

```
Main Agent (Fiesta)
  ↓
  Analyzes corrected document
  ↓
  Determines work scope (e.g., "build 5 commodity analysis subagents")
  ↓
  DELEGATES TO NEMESIS: "Spawn these tasks"
  ↓
Nemesis (Decision Layer)
  ↓
  Checks AUTHORIZATION.md
  ↓
  Verifies Tier 0-2 cost discipline
  ↓
  Issues sessions_spawn batch
  ↓
Subagent Pool (Children)
  ↓
  Each subagent does isolated work
  ↓
  Returns result to Fiesta
  ↓
Fiesta collects + synthesizes results
```

### Workflow Steps for Implementation

#### Step 1: Trigger Detection (Tier 0 — Bash)
Scan corrected document for autonomous work indicators:
```bash
grep -E "Department|Autonomous|Scaling|Telemetry" mendez-gemini-enclave-corrected.md
```
**Cost:** $0.00 (bash)

#### Step 2: Scope Extraction (Tier 0 — Bash)
Parse departments and responsibilities:
```bash
# Extract: Department of Engineering → hardware telemetry
# Extract: Department of Operations → 10k/hr burn rate
# Extract: Autonomous Scaling → dynamic provisioning
```
**Cost:** $0.00 (bash)

#### Step 3: Authorization Check (Tier 0 — Bash)
Verify delegations exist:
```bash
grep -i "authorized\|delegation" AUTHORIZATION.md
```
**Cost:** $0.00 (bash)

#### Step 4: Spawn Decision (Tier 1 — BitNet or Tier 0 — Bash)
If authorization + scope are clear:
- **Bash route:** Parse scope, call `sessions_spawn` directly
- **BitNet route:** Simple logic ("Should we spawn? → Yes/No/Escalate")
**Cost:** $0.00 (local decision)

#### Step 5: Batch Spawn (Tier 2 — Haiku, One Call)
Call `sessions_spawn` with:
```json
{
  "task": "Analyze commodity pricing for enclave operations",
  "label": "enclave-commodity-001",
  "model": "anthropic/claude-haiku-4-5-20251001",
  "sandbox": "require"
}
```
**Cost:** ~100 tokens (precached context reduces this to ~50)

#### Step 6: Collection (Tier 0 — Bash)
Once subagents complete, Fiesta polls sessions via `sessions_history`:
```bash
for SESSION_KEY in $(sessions_list | jq '.[] | select(.kind=="subagent") | .key'); do
  sessions_history "$SESSION_KEY" >> results.jsonl
done
```
**Cost:** $0.00 (bash polling)

---

## Part 4: Nemesis's Decision Surface

### When to Spawn (Trigger Conditions)

**Spawn automatically when:**
1. Corrected document is updated (departments assigned new tasks)
2. Autonomous Scaling request arrives (11–18 of corrected doc)
3. Monitoring threshold breached (burn rate exceeding $20.00/day)
4. Enclave reports new workload (Satellite Node added, etc.)

**Escalate to human when:**
1. Cost exceeds budget (>$20.00 spend in one cycle)
2. Authorization document is missing/invalid
3. Subagent fails (error in 2+ consecutive runs)
4. Scope changes (corrected doc modified, new departments)

### Cost Discipline Boundary

**Hard stop at:**
- **$0.00 Tier 0-2 only rule:**
  - Bash (system queries) = $0.00
  - BitNet (local inference) = $0.00
  - Haiku (external, first use) = ~100 tokens ≈ $0.01
  - **Never use Claude 3.5 Sonnet, Opus, etc.** (cost violation)

**Precaching rule:**
- Use `zero-token-subagent-wrapper.sh` before every spawn
- Inject precached context (MEMORY.md, existing docs, prior results)
- Target: 50% token reduction per spawn

---

## Part 5: Implementation Blockers & Workarounds

### Blocker 1: "Who is Nemesis in the code?"
**Status:** ✅ Resolved

Nemesis is **not a separate agent** in the current OpenClaw setup. Nemesis is a **decision framework** that Fiesta executes.

**Workaround:** Implement Nemesis logic as a bash script or BitNet function that Fiesta calls:
```bash
nemesis_decision() {
  local scope="$1"
  local budget="$2"
  # Check AUTHORIZATION.md
  # Check cost discipline
  # Return: SPAWN|ESCALATE|DENY
}
```

### Blocker 2: "How does Nemesis receive delegated tasks?"
**Status:** ⚠️ Needs definition

Currently, Fiesta would need to explicitly call Nemesis. Options:

**Option A (Simple):** Nemesis function in Fiesta's code
```bash
fiesta_spawn_autonomously() {
  local task="$1"
  nemesis_decision "$task" "$BUDGET"
  # Nemesis returns: SPAWN, ESCALATE, DENY
}
```
**Cost:** $0.00 (all bash)

**Option B (Subagent Routed):** Create a Nemesis subagent
```bash
sessions_spawn \
  --task "Decide: should we spawn commodity agents?" \
  --label "nemesis-decision" \
  --agentId "nemesis"
```
**Cost:** ~50 tokens (first decision logic encoded into prompt)

**Recommendation:** **Option A (bash function)** for cost discipline. Nemesis as subagent is overkill for yes/no decisions.

### Blocker 3: "Subagents can't chain work — how do we build pipelines?"
**Status:** ✅ Workaround exists

**Problem:** Subagent A finishes → wants to spawn Subagent B → **can't (blocked by constraint 1)**

**Workaround:** Return result to Fiesta, let Fiesta decide next spawn:
```
Fiesta spawns A
  ↓ (waits for completion)
A returns result
  ↓ (Fiesta polls sessions_history)
Fiesta evaluates: "Does A's result need B?"
  ↓
Fiesta spawns B (if needed)
  ↓
B returns result
```

**Cost:** 1 API call per subagent (sequential, not parallel)

**For Enclave:** This is **acceptable**. Commodity analysis → escalation → fund deployment is inherently sequential.

---

## Part 6: Mendez-Gemini Specific Recommendations

### Department Alignment (From Corrected Doc)

| Department | Task | Spawn Strategy |
|------------|------|--------|
| Engineering | Hardware telemetry | Subagent + precache (monitors.md) |
| Marketing | Feddit presence | Subagent (low criticality) |
| Design | UI/Telegram bot | Subagent (manifest updates) |
| Ops | Burn rate tracking | Subagent (real-time, loop with Nemesis) |
| Testing | CI/CD validation | Subagent (on demand, ARM64 native) |
| **Nemesis** | Strategic shifts + security triage | **Bash decision function** (no spawn) |

### Cost Model for Enclave

**Assumption:** $20.00 budget, 10k units/hour burn rate.

**Subagent spawning budget:**
- Haiku: ~$0.01 per 100 tokens (small prompt cost)
- **Max spawns per day:** ~50 (at $0.01 each) before hitting $0.50 Tier-2 limit
- **Preserve bulk of budget:** For actual enclave operations (Ampere token spend)

**Precaching ROI:**
- Without precache: 100 tokens/spawn × 50 spawns = 5,000 tokens ≈ $0.05
- With precache: 50 tokens/spawn × 50 spawns = 2,500 tokens ≈ $0.025
- **Savings: 50% ($0.025/day)**

---

## Part 7: Final Recommendation for Nemesis

### What Nemesis Should Decide Autonomously

✅ **YES — Implement with precaching:**
1. Spawn commodity analysis subagents (daily)
2. Spawn telemetry collectors (hourly)
3. Spawn CI/CD validators (on push)
4. Spawn monitoring snapshot agents (every 30 min)

✅ **YES — But with human review cycle:**
1. Escalations (burn rate warnings)
2. Department reassignments (corrected doc changes)
3. New satellite nodes (infrastructure scaling)

❌ **NO — Reserved for Fiesta:**
1. Budget allocation changes
2. Authorization revocation/modification
3. Agent persona updates
4. Long-term strategy shifts

### Implementation Checklist

- [ ] **Phase 1:** Write `nemesis_decision.sh` (bash function, $0.00)
- [ ] **Phase 2:** Update `zero-token-subagent-wrapper.sh` with Nemesis decision hook
- [ ] **Phase 3:** Define spawn triggers in `HEARTBEAT.md` (periodic tasks)
- [ ] **Phase 4:** Document subagent pool patterns (which tasks → which agent)
- [ ] **Phase 5:** Monitor first 10 spawns (verify precaching ROI, cost discipline)
- [ ] **Phase 6:** Automate with cron (once patterns stabilize)

---

## Conclusion

**Autonomous subagent spawning for Mendez-Gemini Enclave is FEASIBLE.**

**Key enablers:**
1. ✅ OpenClaw `sessions_spawn` tool is production-ready
2. ✅ Precaching wrapper exists and works
3. ✅ Authorization framework is in place
4. ✅ Tier 0-2 cost discipline prevents runaway spend
5. ✅ Nemesis decision logic can be implemented as bash (zero cost)

**Key constraints to accept:**
1. ⚠️ Subagents cannot chain (use Fiesta as router instead)
2. ⚠️ Subagents lose session tools (but don't need them — compartmentalization is feature)
3. ⚠️ 60-min archive timeout (acceptable for task-based work)
4. ⚠️ Nemesis as function, not agent (simplicity wins over complexity)

**Workflow to delegate to Nemesis:**
1. Fiesta checks corrected document for work
2. Fiesta calls `nemesis_decision("task", "budget")`
3. Nemesis returns: SPAWN | ESCALATE | DENY
4. If SPAWN: Fiesta calls `sessions_spawn` with precached context
5. Subagent executes in isolation
6. Fiesta collects result via `sessions_history`
7. Fiesta synthesizes + returns to human

**Cost to implement:** $0.00 (all Tier 0-1, no external tokens for the orchestration layer)

---

**Status:** Ready for approval and implementation.

**Next step:** Request human authorization to implement `nemesis_decision.sh` + wire into Fiesta's spawning logic.

