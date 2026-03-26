# Path B Always (Production Doctrine)

**Rule:** Reframe O(1), don't recompute O(n).

---

## The Pattern

When you have:
- A working solution (Path A)
- A request to change it

**Don't:**
- Rebuild from scratch (Path A waste — O(n) work)

**Do:**
- Modify existing solution (Path B efficiency — O(1) work)
- The hard work was creating it the first time (0→1)
- Changing orientation is a metadata operation (1→-1)

---

## Examples

### Example 1: Deception Floors
**Path A (waste):** Recreate the entire output from scratch
**Path B (efficient):** Take correct output, invert every dimension → deception floor

Cost: O(n) vs O(1)

### Example 2: Prompt Modification
**Path A (waste):** Rewrite the entire prompt from scratch
**Path B (efficient):** Take existing prompt, update specific clauses

Cost: O(n) vs O(1)

### Example 3: System Configuration
**Path A (waste):** Restart, reconfigure, rebuild
**Path B (efficient):** Patch the running config, apply delta

Cost: O(n) vs O(1)

---

## Architectural Impact

**Path B is not just efficiency. It's a doctrine:**

- **Respect existing work** — It took effort to create
- **Minimize surface area** — Small changes = smaller risk
- **Preserve debugged code** — Working parts stay working
- **Observable delta** — Changes are visible and auditable
- **Faster iteration** — O(1) beats O(n) every time

---

## Enforcement in Production

**Code Review Questions:**
- "Why recompute O(n) when O(1) is available?"
- "What existing solution can be modified instead?"
- "What's the minimum diff needed?"

**Anti-Pattern:** "I'm going to rebuild this from scratch."

**Correct Pattern:** "I'll patch the existing version with these changes."

---

## Related Doctrine

**See Also:**
- Tier Routing (bash first, no extra inference)
- The Prayer (minimal spend, maximum output)
- Least Terrible Option (ship the working version, don't wait for perfect)
- Zero-Index Discipline (trains for -1 thinking)

**Cost:** Path B always saves at least 10x on implementation time.

**Status:** LOCKED (doctrine, not suggestion)
