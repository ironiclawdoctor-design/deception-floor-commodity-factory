# 🔝 LLM PRIORITY HIERARCHY — STRICT ENFORCEMENT

**Established:** 2026-03-13 13:50 UTC  
**Status:** LOCKED IN (no exceptions)  
**Doctrine:** Bash → BitNet → Haiku (never for internal work)

---

## The Three-Tier System

### Tier 0: BASH (Shell, Local, ZERO COST) ⭐⭐⭐

**Priority:** ALWAYS FIRST

**Use for:**
- File operations: `ls`, `cat`, `grep`, `find`, `sed`, `awk`
- Directory navigation: `pwd`, `cd`, `ls -la`
- Status checks: `[ -f file ]`, file size, permissions
- Health probes: service checks, port availability
- Data extraction: parsing logs, counting lines
- System information: uptime, processes, memory
- Git operations: git status, git log (read-only)
- Simple text manipulation: echo, cut, sort, uniq

**Cost:** $0.00 per invocation  
**Availability:** Always (even during token famine)  
**Performance:** Instant (<100ms)

**Examples:**
```bash
ls /root/.openclaw/workspace/
cat /root/.openclaw/workspace/MEMORY.md
grep "bashbug" /root/.openclaw/workspace/MEMORY.md | wc -l
[ -f /var/log/factory.log ] && echo "exists" || echo "missing"
```

---

### Tier 1: BITNET (Local LLM, ZERO COST) ⭐⭐

**Priority:** SECOND (use if bash can't)

**Use for:**
- Agent reasoning and decomposition
- Local task analysis and planning
- Message routing between agents
- Complex pattern matching (regex alternatives)
- Local data correlation (multi-file analysis)
- Agent communication (coordination)
- Internal logic (policy decisions)
- Format conversion (JSON parsing, data transformation)

**Cost:** $0.00 per invocation (local, zero tokens)  
**Availability:** Available (sovereign, no cloud dependency)  
**Performance:** Fast (29 tok/s, sub-second for small inputs)

**Examples:**
```bash
# Use BitNet for: "Should we spawn an agent for this task?"
# Use BitNet for: "Analyze these 3 log files and correlate events"
# Use BitNet for: "Route this message to the appropriate agent"
# Use BitNet for: "Is this configuration valid?"
```

---

### Tier 2: HAIKU (External LLM, COSTS TOKENS) ⭐ ⚠️

**Priority:** LAST RESORT (human-facing only)

**Use for:**
- Customer/human-facing responses (only)
- Prose summaries (only)
- Natural language explanation (only)
- External API calls that require reasoning
- Situations where bash/BitNet truly insufficient

**Cost:** ~50-100 tokens per invocation  
**Availability:** Conditional (requires token budget)  
**Performance:** Moderate (network-dependent, 1-3s)

**Examples:**
```bash
# Use Haiku for: "Please write a status summary for the customer"
# Use Haiku for: "Generate a human-readable report"
# Use Haiku for: "Explain to the user what happened during the famine"
```

**DO NOT use Haiku for:**
- ❌ `ls` alternatives
- ❌ `cat` alternatives
- ❌ File checking
- ❌ Status queries
- ❌ Internal logic
- ❌ Agent coordination
- ❌ Data parsing
- ❌ Anything bash or BitNet can do

---

## Decision Tree (ENFORCED)

```
Task request arrives:
  │
  ├─ Can bash handle it? (ls, cat, grep, find, stat, etc.)
  │  YES → Use bash (Tier 0) ✅ DONE
  │  NO  → Continue
  │
  ├─ Is it internal reasoning/coordination?
  │  YES → Use BitNet (Tier 1) ✅ DONE
  │  NO  → Continue
  │
  ├─ Is it human-facing prose output?
  │  YES → Use Haiku (Tier 2) ⚠️ (costs tokens, acceptable)
  │  NO  → Continue
  │
  └─ Can it wait until tokens refill?
     YES → Defer task (cost conservation) ✅
     NO  → Use Haiku (unavoidable)

NEVER skip tiers. Always start at Tier 0.
```

---

## Concrete Examples

### Example 1: "What's in the bashbug directory?"

**Wrong approach:**
```
User: "What files are in bashbug?"
Fiesta uses Haiku: "In the bashbug directory you'll find..."
Cost: 50+ tokens ❌
```

**Right approach:**
```bash
User: "What's in the bashbug directory?"
Fiesta uses bash: ls /root/.openclaw/workspace/bashbug/
Cost: $0.00 ✅
```

### Example 2: "Are all protection servers running?"

**Wrong approach:**
```
User: "Check if all servers are running"
Fiesta uses Haiku to reason about systemd status
Cost: 75+ tokens ❌
```

**Right approach:**
```bash
User: "Check if all servers are running"
Fiesta uses bash: systemctl status factory bitnet
(Or uses BitNet for parsing/correlation if needed)
Cost: $0.00 ✅
```

### Example 3: "Please explain the agency's current status to a customer"

**Right approach:**
```
Customer: "What's the agency's status?"
Fiesta uses bash/BitNet to gather facts
Fiesta uses Haiku to write human-readable response
Cost: 50-100 tokens ✅ (justified for customer communication)
```

### Example 4: "Did the factory produce any floors in the last 6 hours?"

**Wrong approach:**
```
Fiesta uses Haiku: "Let me check the logs for you..."
Cost: 60+ tokens ❌
```

**Right approach:**
```bash
Fiesta uses bash: grep "2026-03-13 13:" /var/log/bashbug-cron.log | wc -l
Cost: $0.00 ✅
```

---

## Token Conservation Audit

### Every Haiku call must pass three checks:

1. **Bash test**
   - Can bash do it? → No Haiku
   - Example: "ls" → bash, not Haiku
   - Example: "cat file" → bash, not Haiku

2. **BitNet test**
   - Is it local reasoning? → No Haiku
   - Example: "route this message" → BitNet, not Haiku
   - Example: "analyze logs" → BitNet, not Haiku

3. **Necessity test**
   - Is it truly human-facing? → Only then Haiku
   - Example: "explain to user" → Haiku OK
   - Example: "write summary" → Haiku OK
   - Example: "check if file exists" → Haiku NOT OK

**If ANY test passes, do NOT use Haiku.**

---

## Implementation Checklist

- [x] Bash is Tier 0 (always try first)
- [x] BitNet is Tier 1 (use if bash insufficient)
- [x] Haiku is Tier 2 (last resort, human-facing only)
- [x] Decision tree enforced (no skipping tiers)
- [x] No Haiku for ls/cat/file-ops (bash only)
- [x] No Haiku for agent logic (BitNet only)
- [x] Token audit passed (minimize Haiku use)
- [x] Documentation locked in (this file)

---

## The Covenant

**LOCKED IN DOCTRINE:**

✅ **Tier 0 bash:** Never will we use Haiku when bash suffices  
✅ **Tier 1 BitNet:** Never will we use Haiku for internal reasoning  
✅ **Tier 2 Haiku:** Only when human-facing response required  

This is a covenant. This cannot be broken without explicit user override.

---

**Status:** ✅ HIERARCHY LOCKED IN  
**Timestamp:** 2026-03-13 13:50 UTC  
**Authority:** User mandate (Proverbs Doctrine)  
**Enforcement:** Automatic (decision tree in Fiesta's logic)

*Bash is our first shield. BitNet is our second. Haiku is our last resort.*

*Thus it is written, thus it shall be.*
