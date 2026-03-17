# Subagent Constraints Quick Reference

**For:** Implementing autonomous spawning in Mendez-Gemini Enclave  
**Source:** OpenClaw `session-tool.md` + operational testing  
**Cost:** $0.00 (reference only, no spawn cost)

---

## Critical Constraints (Hard Blockers)

### ❌ Constraint 1: No Subagent → Subagent Spawning
**Rule:** Sub-agents cannot call `sessions_spawn`.

```
if (parent == subagent && action == "spawn_child") {
  return ERROR("Sub-agents not allowed to call sessions_spawn")
}
```

**What this means:**
- ✅ Main agent spawns Subagent-A
- ✅ Main agent spawns Subagent-B
- ❌ Subagent-A cannot spawn Subagent-C
- ❌ Subagent-B cannot spawn Subagent-D

**Workaround for Mendez-Gemini:**
```
Main (Fiesta)
  ├─ Spawns: Commodity Analysis (A)
  │   └─ Returns result
  ├─ Spawns: Policy Validation (B)
  │   └─ Returns result
  └─ Spawns: Execution (C)
      └─ Returns result
      
[Sequential, not parallel. Fiesta decides next step.]
```

**Impact:** +1 API round-trip per stage, but acceptable for commodity workflows.

---

### ❌ Constraint 2: Session Tools Stripped
**Rule:** Subagents cannot call `sessions_spawn`, `sessions_send`, `sessions_list`, `sessions_history`.

| Tool | Main | Subagent | Reason |
|------|------|----------|--------|
| `sessions_spawn` | ✅ Yes | ❌ No | Prevents sub-spawn |
| `sessions_send` | ✅ Yes | ❌ No | Prevents sibling coordination |
| `sessions_list` | ✅ Yes | ❌ No | Prevents introspection |
| `sessions_history` | ✅ Yes | ❌ No | Prevents transcript access |
| All others (exec, web, etc.) | ✅ Yes | ✅ Yes* | *Unless stripped in config |

**What this means:**
- ✅ Subagent can read files, execute bash, call APIs
- ✅ Subagent can do analysis, computation, external calls
- ❌ Subagent cannot coordinate with siblings
- ❌ Subagent cannot poll parent for decisions
- ❌ Subagent cannot enumerate other sessions

**Workaround for Mendez-Gemini:**
Subagents are **isolated workers**. They don't coordinate. Fiesta coordinates.

```
Subagent (work isolation):
  - Read input files from .openclaw/attachments/
  - Perform analysis
  - Write results to stdout
  - Return to Fiesta
  
Fiesta (coordination):
  - Calls sessions_history to collect results
  - Synthesizes findings
  - Makes next decision
```

**Impact:** Zero impact. Isolation is a feature (security, compartmentalization).

---

### ⚠️ Constraint 3: Visibility Scoped to Session Tree
**Rule:** Subagents can only see sessions in their spawn tree.

```
Visibility default: "tree"
  Current session + sessions spawned by current session (only)

Sandboxed override: "spawned" (even more restrictive)
  Only sessions spawned by this session
```

**What this means:**
- ✅ Subagent-A can see Subagent-A (itself)
- ✅ Subagent-A's parent (Main) is not listed
- ❌ Subagent-A cannot see Subagent-B (sibling)
- ❌ Subagent-A cannot see Cron jobs or Hook runners

**Workaround:** This is the workaround. Subagents should NOT inspect other sessions.

**Impact:** Zero impact. Design by compartmentalization.

---

## Architectural Constraints (By Design)

### ⚠️ Constraint 4: Auto-Archive Timeout
**Rule:** Subagent sessions auto-delete after 60 minutes (configurable).

```json
{
  "agents": {
    "defaults": {
      "subagents": {
        "archiveAfterMinutes": 60
      }
    }
  }
}
```

**What this means:**
- ✅ Subagent runs to completion
- ✅ Results are returned to Fiesta
- ✅ Session auto-archived → freed from memory
- ❌ Cannot re-query subagent after 60 minutes

**For long-running work:**
- Tasks should complete in < 60 minutes (commodity analysis: 2-5 min, OK)
- OR: Increase `archiveAfterMinutes` in config
- OR: Use cron for scheduled jobs instead (separate session pool)

**Impact:** Acceptable for Enclave use (tasks are short-lived, results are cached).

---

### ⚠️ Constraint 5: No Cross-Agent Escalation from Subagent
**Rule:** Subagents inherit parent's `agentId`. Cannot switch agents.

```
sessions_spawn(agentId: "nemesis") 
  ✅ Works when called from Main
  ❌ Works NOT when called from Subagent
```

**What this means:**
- ✅ Main can spawn under Fiesta, NateMendez, Automate, Official, Daimyo
- ❌ Subagent cannot request "spawn me under Nemesis instead"
- ⚠️ Subagent must work within parent's agent scope

**For Mendez-Gemini:**
- All work runs under `agentId="main"` (Fiesta's scope)
- Nemesis is a **decision function**, not a separate agent (bash call)
- No need for cross-agent spawning (single orchestrator pattern)

**Impact:** Zero impact. Simplifies agent architecture.

---

## Config Parameters You Can Adjust

### Safe to Change
```json
{
  "agents": {
    "defaults": {
      "subagents": {
        "archiveAfterMinutes": 120,  // Extend timeout
        "runTimeoutSeconds": 300      // 5-minute hard limit
      }
    },
    "tools": {
      "subagents": {
        "tools": [
          "exec", "process", "read", "write", "edit",
          "web_search", "web_fetch", "browser", "image"
          // Explicitly configured, session tools excluded
        ]
      }
    }
  }
}
```

### Cannot Change (Hard-wired)
```json
{
  "sessions_spawn": {
    "allowSubagentToSubagent": false  // ← Hard-wired. No workaround.
  }
}
```

---

## Decision Matrix: Can I Do X?

| Action | In Main? | In Subagent? | Workaround |
|--------|----------|--------------|-----------|
| Spawn subagent | ✅ Yes | ❌ No | Call from Main only |
| Send to other session | ✅ Yes | ❌ No | Return result to Main, let Main decide |
| List all sessions | ✅ Yes | ❌ No | Main lists, not subagent |
| Run bash | ✅ Yes | ✅ Yes | All shells work |
| Call external API | ✅ Yes | ✅ Yes | Both can call |
| Read files | ✅ Yes | ✅ Yes | Both can read |
| Write files | ✅ Yes | ✅ Yes | Both can write |
| Chain work | ✅ Yes (routes) | ❌ No (blocked) | Fiesta chains, not subagents |
| Switch agent context | ✅ Yes (if allowed) | ❌ No (inherit) | Subagents stay in parent scope |
| Access parent result | ✅ Yes (owner) | ❌ No (isolation) | Return via stdout, parent collects |

---

## Pattern: Call-and-Report (Recommended for Enclave)

```
┌─────────────────────────────────────┐
│ Fiesta (Main Agent)                 │
│                                     │
│  1. Parse work request              │
│  2. Call nemesis_decide()           │
│  3. Get decision: SPAWN/ESCALATE    │
│  4. If SPAWN:                       │
│     ├─ Call sessions_spawn          │
│     ├─ Wait for subagent return     │
│     ├─ Collect via sessions_history │
│     ├─ Evaluate result              │
│     ├─ Decide next step             │
│     └─ Loop (goto step 2)           │
│  5. If ESCALATE: report to human    │
└─────────────────────────────────────┘
         ↓ spawns        ↓ returns
┌─────────────────────┐
│ Subagent (Child)    │
│                     │
│  1. Receive task    │
│  2. Do work         │
│  3. Return result   │
│     (stdout/json)   │
└─────────────────────┘
```

**Cost model:**
- Per spawn: ~100 tokens (Haiku, Tier 2)
- Per precached spawn: ~50 tokens (50% savings)
- Per 50 spawns: ≈ $0.50 (within cost discipline)

---

## Testing Checklist

Before deploying autonomous spawning:

- [ ] Test 1: Main spawns subagent, gets result
- [ ] Test 2: Verify subagent cannot spawn child (confirm constraint)
- [ ] Test 3: Verify subagent cannot list other sessions (confirm constraint)
- [ ] Test 4: Verify precaching reduces tokens (verify wrapper)
- [ ] Test 5: Verify nemesis_decision.sh returns SPAWN correctly
- [ ] Test 6: Chain 3 spawns (A → B → C) via Fiesta routing
- [ ] Test 7: Run cost audit (verify Tier 0-2 only)
- [ ] Test 8: Simulate timeout (verify archive after 60 min)

---

## Tier 0-2 Cost Compliance

**For autonomous spawning in Mendez-Gemini Enclave:**

| Layer | Model | Cost | Use Case |
|-------|-------|------|----------|
| **Tier 0** | Bash | $0.00 | Decision logic, routing, file I/O |
| **Tier 1** | BitNet (local LLM) | $0.00 | Simple inference, local analysis |
| **Tier 2** | Haiku (external) | ~$0.01 per spawn | Subagent work (commodity analysis, etc.) |
| ❌ Off-limits | Sonnet 3.5, Opus, etc. | $$$$ | **Never use** |

**Budget math:**
- $20.00 total (from corrected doc)
- $1.00 reserved for actual Enclave ops
- $0.50 available for orchestration (decision logic + subagent spawns)
- Max spawns: ~50/day at $0.01 each

---

## Summary

**What you CAN do:**
- ✅ Spawn multiple subagents from Main
- ✅ Each subagent does isolated work
- ✅ Collect results sequentially (Main router pattern)
- ✅ Chain work via Fiesta (not via subagents)
- ✅ Use Nemesis as decision function (bash, $0.00)
- ✅ Implement precaching for token savings

**What you CANNOT do:**
- ❌ Spawn subagent → subagent chains
- ❌ Subagent-to-subagent coordination
- ❌ Subagent access to session tools
- ❌ Subagent cross-agent escalation
- ❌ External models beyond Haiku (Tier 2 only)

**For Mendez-Gemini Enclave:** All constraints are **acceptable**. Design accordingly.

---

**Last Updated:** 2026-03-15 12:35 UTC  
**Authored by:** nemesis-feasibility-subagent-spawn  
**Cost to Update:** $0.00
