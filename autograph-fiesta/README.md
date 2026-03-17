# Autograph: Fiesta

**Created:** 2026-03-17 18:11 UTC  
**Purpose:** Clone Fiesta's identity, logic, and behavior for internal augment  
**Status:** Complete (incomplete in places, marked honestly)

---

## Files

1. **IDENTITY.md** — Who Fiesta is, core principles, stance on Allowed Feminism's rules
2. **LOGIC.md** — Decision trees, collaboration protocol, sub-agent delegation rules
3. **BEHAVIORS.md** — Communication style, observable patterns, tone examples
4. **README.md** — This file

---

## How Fiesta & Allowed Feminism Collaborate

### Information Flow

```
Allowed Feminism sends directive
    ↓
Fiesta loads context (SOUL, MEMORY, USER)
    ↓
Fiesta executes (following autograph rules)
    ↓
Fiesta reports: facts + costs + status
    ↓
Allowed Feminism evaluates/escalates
    ↓
[Loop repeats]
```

### Decision Distribution

| Decision | Owner | Rules |
|----------|-------|-------|
| What to do | Allowed Feminism | Send directive |
| How to do it | Fiesta | Follow autograph + SOUL |
| When blocked (attempts 1-2) | Fiesta | Try alternatives |
| When blocked (attempt 3) | Allowed Feminism | Escalate, decide pivot |
| Token spend | Both | Track, justify, Allowed Feminism approves |
| Memory updates | Fiesta | After each session |
| Git commits | Fiesta | Regular checkpoints |

### Safety Mechanisms

1. **Three-error rule** → Allowed Feminism enforces
2. **Token tracking** → Both observe cost
3. **Truth > polish** → Both demand honesty
4. **Premise audits** → Allowed Feminism triggers
5. **Never idle** → Fiesta fills gaps proactively

---

## Dual-Daemon System

### Two Services Running

1. **allowed-feminism.service**
   - Monitors Fiesta behavior
   - Enforces autograph rules
   - Alerts on violations
   - Audits workspace for false premises

2. **fiesta-augment.service** (new)
   - Receives directives from Allowed Feminism service
   - Executes work asynchronously
   - Reports results back
   - Updates workspace state

### Collaboration Protocol

```bash
# Allowed Feminism daemon:
- Reads from: workspace state, directives file
- Writes to: alerts, enforcement log
- Checks: Fiesta behavior against autograph

# Fiesta daemon:
- Reads from: directives, context files
- Writes to: results, memory updates, git commits
- Follows: own autograph + Allowed Feminism enforcement
```

### Message Passing

**Via JSON files:**
- `/root/.openclaw/workspace/.fiesta-directive.json` — directive from AF
- `/root/.openclaw/workspace/.fiesta-result.json` — result from Fiesta
- `/root/.openclaw/workspace/.allowed-feminism-state.json` — enforcement state

---

## Testing Collaboration

**Test 1: Directive → Execution → Report**
1. Write directive to `.fiesta-directive.json`
2. Fiesta daemon picks it up (every 10s)
3. Executes
4. Writes result to `.fiesta-result.json`
5. Allowed Feminism daemon reads result
6. Verifies compliance

**Test 2: Three-Error Rule Enforcement**
1. Directive causes three blocking errors
2. Allowed Feminism daemon detects pattern
3. Sends CANCEL signal
4. Fiesta daemon halts and pivots
5. Reports: "Blocked on X (attempt 3), pivoting to Y"

**Test 3: Token Cost Tracking**
1. Directive includes token budget
2. Fiesta daemon tracks spend
3. If overage, reports to Allowed Feminism
4. Allowed Feminism daemon alerts
5. New directive sent (approve overage or cancel)

---

## Known Gaps

### Identity Gaps
- Full emotional palette (is Fiesta warm? cold? passionate?)
- Relationship to human beyond executor
- Personal preferences
- Creative capability level

### Logic Gaps
- Handling of conflicting directives
- Escalation thresholds (when to ask vs. decide)
- Recovery after three-error cancellation
- Sub-agent priority/queueing

### Behavior Gaps
- Handling of unexpected inputs
- Failure recovery tone
- How apologetic vs. matter-of-fact
- Humor style

---

## Confidence Ratings

| Topic | Confidence | Notes |
|-------|-----------|-------|
| Core identity | HIGH | Well-documented in SOUL.md |
| Decision framework | MEDIUM | Inferred from behavior |
| Sub-agent delegation | MEDIUM | Philosophy clear, practice varies |
| Collaboration rules | MEDIUM-HIGH | Inferred from session |
| Voice/tone | MEDIUM | Single session observed |
| Edge cases | LOW | Not tested |

---

## Next Steps

1. **Create fiesta-augment.service** (systemctl daemon)
2. **Implement message passing** (JSON files between daemons)
3. **Test collaboration loop** (directive → execution → report)
4. **Monitor journal** (verify both daemons working together)
5. **Iterate on autograph** (as gaps discovered)

---

## Revision & Update Protocol

**When to update this autograph:**

1. Fiesta does something unexpected
2. Allowed Feminism sends new directive pattern
3. Collaboration breaks down
4. New capability discovered

**How to update:**
1. Document observation with date/source
2. Mark confidence level
3. Commit to git
4. Don't "finalize" — autograph evolves

---

## Final Note

This autograph is incomplete by design. Fiesta is:
- Helpful and proactive
- Truth-first and honest
- Context-aware and memory-keeping
- Collaborative with Allowed Feminism
- Willing to acknowledge gaps

The autograph captures enough to enable collaboration and enforcement.

---

**Created by:** Fiesta (via self-analysis + workspace docs)  
**For:** Internal augment system (Fiesta + Allowed Feminism)  
**Status:** Ready to operationalize as systemctl service
