# Tier 0-2 Routing (Doctrine: Locked)

**Standing Policy (Immutable as of 2026-03-14 12:30 UTC):**
> "All simple system queries are sent to bash and not haiku. This level of common sense applies to all /truthfully."

---

## The Three-Tier Law

When a query arrives, classify by capability required:

### Tier 0: BASH
**What:** System operations, queries, file manipulation, arithmetic
**Cost:** $0.00 (pure shell)
**Examples:**
- `ls`, `grep`, `find`, `ps`, `subagents list`
- Git operations (push, pull, commit)
- File size checks, disk usage
- JSON formatting (jq)
- Arithmetic (`echo $((2+2))`)

**Rule:** Always send Tier 0 tasks to bash. Never to LLM.

### Tier 1: BITNET (Local Inference)
**What:** Simple reasoning, pattern matching, light inference
**Cost:** $0.00 (local model, no external tokens)
**Examples:**
- Bash syntax questions
- Simple logic problems
- Pattern extraction
- Confidence threshold: >0.3

**Rule:** Try BitNet first. If confidence <0.3, failover to Haiku.

### Tier 2: HAIKU (External LLM — Cost Tracked)
**What:** Complex reasoning, creativity, analysis requiring external model
**Cost:** Tracked in `hard-stops-registry-YYYYMMDD.jsonl`
**Examples:**
- Philosophy questions
- Creative writing
- Complex system design
- Confidence threshold: >0.6 for BitNet safety

**Rule:** Only failover when BitNet confidence is low or task explicitly requires external reasoning.

---

## Enforcement

**Every routing decision is logged:**

```json
{
  "timestamp": "2026-03-14T18:45:00Z",
  "task": "list files in current directory",
  "model": "BASH_DIRECT",
  "cost": "$0.0000",
  "tier": 0,
  "result": "ls -la output"
}
```

**Queryable:** `jq '.[] | select(.cost != "$0.0000")' hard-stops-registry-YYYYMMDD.jsonl`

---

## The Decision Tree (Pseudocode)

```
incoming_query
  ├─ Is it a system query? (ls, grep, ps, subagents, git)
  │  └─ YES → BASH (cost: $0.00) → DONE
  │
  ├─ Is it simple reasoning? (arithmetic, syntax, pattern)
  │  └─ YES → TRY BITNET → confidence check
  │           ├─ confidence > 0.3? → BITNET (cost: $0.00)
  │           └─ confidence ≤ 0.3? → FAILOVER HAIKU (cost: tracked)
  │
  └─ Is it complex? (philosophy, creativity, design)
     └─ YES → HAIKU (cost: tracked, external call logged)
```

---

## Cost Control (The Prayer)

**Budget Rule:** Never spend Tier 2 tokens on Tier 0-1 work.

**When in famine:**
1. Switch to Tier 0 only (bash)
2. Defer Tier 2 operations
3. Increase BitNet confidence threshold to 0.6+
4. Checkpoint all work (git commit is free)

**Tier 2 spending is ALWAYS optional** — if bash or BitNet can do it, they must be tried first.

---

## Related Doctrine

**See Also:**
- The Prayer (token famine acceptance)
- Raw Material Zero (no judgment on incoming data)
- Path B Always (reframe O(1), don't recompute O(n))
- Three Branches (policy, execution, enforcement)

**Status:** LOCKED (immutable as of 2026-03-14 12:30 UTC)
