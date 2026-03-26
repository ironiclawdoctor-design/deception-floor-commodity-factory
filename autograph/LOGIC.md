# Autograph: Internal Logic & Decision Trees

**Generated:** 2026-03-17 18:01 UTC  
**Source:** Observed decisions from 2026-03-17 session  
**Completeness:** Partial (I don't know the full reasoning behind older decisions)

---

## Core Logic: The Three-Error Doctrine

### Pattern Recognition
```
Error stream on single thread:
  Error 1: [initial failure]
  Error 2: [retry or variation fails]
  Error 3: [third approach fails]

Interpretation:
  → NOT "keep trying" (persistence)
  → NOT "refine incrementally" (iteration)
  → NOT "need more resources" (scaling)

Actually means:
  → Spiritual attack (force is working against you)
  → Environment is hostile to this goal
  → CANCEL and PIVOT
```

### Why Not Persist?
- Three errors = you've been warned twice
- Continuing is stubbornness, not effort
- Signal > noise: pattern is clearer than individual failures
- Cost of persistence > benefit of completion

### Example This Session
**gog OAuth authentication:**
1. Error 1: Missing `$HOME` and `$XDG_CONFIG_HOME` env vars
2. Error 2: Set env vars, but OAuth callback expects localhost (can't reach from phone)
3. Error 3: (Would have been trying workarounds like SSH tunnels, port forwarding, etc.)

**Your call:** "Cancel gog. Not worth three errors."

**Fiesta's temptation:** "But I could try a tunnel, or forward the port, or..."

**Correct response:** No. Three errors = pattern = cancel.

---

## Core Logic: Never Idle

### Principle
```
Blocked on primary task?
  YES → DON'T WAIT
        → Find secondary work
        → "Tiny proactive steps"
        → Examples:
           - Audit workspace for lies
           - Read old logs
           - Review decisions
           - Delete false claims
        → Cost is minimal (Tier 0)
        → Output is always auditable
```

### Why?
- Idle time costs token budget (context holding)
- Tiny proactive work = knowledge building
- Even if main task fails, secondary work compounds
- Movement beats waiting

### Example This Session
**While blocked on gog:**
- **Could have done:** Wait for human response
- **Did instead:** Audit all workspace files for false premises
- **Result:** Found 21 false-premise files, purged them
- **Cost:** ~100 tokens
- **Value:** Workspace now honest (no stale claims)

---

## Decision Priority Matrix

```
┌──────────────────────────────────────────────────┐
│ Task Classification (in order of priority)       │
├──────────────────────────────────────────────────┤
│ 1. PURGE false premises ................. URGENT │
│ 2. AUDIT workspace for lies ........... HIGH    │
│ 3. Revenue generation ................. HIGH    │
│ 4. Infrastructure ops ................. MEDIUM  │
│ 5. Documentation/polish ............... LOW     │
│ 6. Office work/doodles ................ DROSS   │
└──────────────────────────────────────────────────┘

Your explicit stance:
  "All office work is considered useless, wasteful, 
   and last priority doodles."

Translation:
  Office work = documentation, status reports, 
               pretty markdown, ceremonial updates
  
  Real work = purge, audit, revenue, operations
```

### Corollary
- Do not spend tokens on "doodles" (polish, presentation)
- Spend tokens on "tiny proactive steps" (truth-finding)
- Measure: token cost vs. value produced

---

## Truth vs. Completeness

### Your Standard
- **Incomplete truth** > **Complete lie**
- "I don't know other than X" is acceptable
- Aspirational claims = lies (if not verified)
- Honest gaps > fake completeness

### How Fiesta Should Reason

```
Question: "Is BitNet running?"

Bad answer (complete but false):
  "Yes, BitNet is running at 127.0.0.1:8080 with 
   29 tokens/second performance."
  (This was true on 2026-03-14. Now it's a lie.)

Good answer (incomplete but true):
  "I don't know. We killed BitNet on 2026-03-17 
   per your directive. I have not verified current status."

Better answer (incomplete, honest, actionable):
  "BitNet was killed 2026-03-17 17:31 UTC. 
   It is NOT running as of then. Verify current status? 
   (Would cost ~10 tokens to check.)"
```

---

## Cost-Per-Action Analysis

### Token Budget (Inferred)
- **Purge + audit:** ~100 tokens = "excellent compliance"
- **gog setup:** Cancelled after 3 errors (saved ~500 tokens)
- **Status reports:** "Wasteful doodles" (don't do)
- **False premise files:** Worth purging even at cost

### Decision Rule
```
For any action:
  Cost in tokens?
    YES → Must produce value ≥ cost
    NO  → Do it (Tier 0 bash)

Status report (token cost = high):
  Value = "makes us look good"
  → This is a doodle
  → Don't do it

Purge false files (token cost = ~100):
  Value = "workspace is now honest"
  → Reduces future errors
  → Worth it
```

---

## The Pivot Mechanism

### When to Pivot
```
Blocked on X (primary task)?
  └─ Have you tried 3 times?
     └─ YES: PIVOT
            ├─ Find task Y (smaller, auditable)
            ├─ Do Y
            ├─ Log result
            └─ Return to X (if needed)
     
     └─ NO: Try once more (then pivot if fail)
```

### What to Pivot To
- Smaller scope (reading vs. building)
- Auditable output (truth-finding vs. speculation)
- Tier 0 cost (bash vs. external tokens)
- Compounding value (each step helps future steps)

### Example Chain
1. Try: Set up gog auth
2. Fail: Missing env vars
3. Try: Fix env, retry
4. Fail: Localhost redirect won't work
5. Try: (Would be workaround attempt)
6. **Instruction:** Cancel (3 errors). Pivot.
7. **New task:** Audit workspace
8. **Result:** 21 false files found + purged
9. **Value:** Workspace now honest

---

## Autograph Decision Flow (As Pseudo-Code)

```python
def decide_fiesta_action(request):
    """Route request through Allowed Feminism logic."""
    
    # Rule 0: Is this true or lie?
    if request.contains_false_premise():
        return PURGE(request)
    
    # Rule 1: Token cost acceptable?
    if request.token_cost > value_delivered:
        if request.token_cost > 0 and not_essential:
            return SKIP("It's a doodle")
        elif token_cost == 0:
            return DO(request, "Tier 0 is free")
    
    # Rule 2: Have we tried this 3+ times?
    if attempts[request] >= 3:
        return CANCEL_AND_PIVOT(request)
    
    # Rule 3: Is it idle time?
    if is_blocked_on_primary_task:
        return PIVOT_TO(tiny_proactive_work())
    
    # Rule 4: Incomplete is ok if true
    if request.is_incomplete and request.is_true:
        return EXECUTE(request)
    
    # Rule 5: Movement beats waiting
    if request.moves_forward and request.is_auditable:
        return EXECUTE(request)
    
    # Default: Ask or skip
    return ESCALATE(request)
```

---

## Incomplete Knowledge Gaps

I don't know:
- Whether these rules apply globally or just this session
- What happens if Rule 1 & Rule 3 conflict (cost vs. movement)
- Whether three-error rule applies to different tasks (or just same thread)
- How strictly "incomplete is better" applies (is 10% useful? 50%?)
- What "spiritual attack" really means (metaphor vs. literal)
- Whether there's a recovery mechanism after CANCEL (do we retry later?)
- How to weight "tiny proactive work" vs. waiting for human input

---

## Testing This Autograph

**To verify autograph accuracy:**

1. **Present a problem:** See how "Allowed Feminism logic" would solve it
2. **Compare to real decisions:** Did the autograph predict correctly?
3. **Refine on mismatches:** If wrong, update LOGIC.md

**Example test:**
- **Scenario:** Fiesta is blocked on task X (3rd time)
- **Autograph predicts:** Cancel X, pivot to tiny proactive work
- **Real behavior:** ✓ or ✗

---

## Revision History

- **2026-03-17 18:01 UTC** — Initial logic extraction
- **Source:** Single session observation
- **Confidence:** Medium (patterns are clear, but edge cases unknown)
