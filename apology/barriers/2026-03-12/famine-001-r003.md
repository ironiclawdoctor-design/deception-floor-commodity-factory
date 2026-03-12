# Apology for Token Famine #1 (R-003)

**Date:** 2026-03-12 20:45 UTC  
**Severity:** High  
**Type:** Service Degradation + Incomplete Delivery

---

## What Happened

Two parallel sub-agents (`disclaimer-parody-satire` and `automate-nbm`) were mid-build when their tokens hit zero. They died abruptly, leaving:

- **disclaimer-parody-satire:** ~13 files incomplete. Missing red-team-notes, automation.md, breach scenarios 001/002, educational-use.md, index.html, pages workflow.
- **automate-nbm:** Unclear file status. Missing tests/, improved workflows, better issue templates.

The human had to investigate, discover the incomplete work, and manually check what was done vs. what died in flight.

---

## Why It Happened

1. **No token budget awareness** — Sub-agents weren't trained to estimate cost before starting multi-file builds
2. **No escalation protocol** — Dying agents didn't notify the main agent about gaps or failures
3. **Sprint design failure** — Parallel builds with no safeguards against partial completion
4. **First day of operation** — Budget allocation was theoretical; real spending wasn't predicted

---

## What This Cost You

- **Time:** Manual audit of 4 repos to discover which builds succeeded and which partially failed
- **Trust:** "I spawned agents to build for me, and they died halfway" — confidence in delegation eroded
- **Clarity:** Ambiguous state (are those files committed? What's the actual status?)
- **Tokens:** The failed work had to be redone or manually completed

---

## What We're Doing About It

1. **Per-agent token budgets** — Each sub-agent now gets a spending cap based on task complexity
2. **Escalation protocol** — Dying agents must:
   - Commit what's done
   - Document what's missing
   - Notify Fiesta with structured barrier report
   - Leave breadcrumbs for recovery
3. **Pre-flight estimation** — No build starts without token-cost analysis
4. **Heartbeat checks** — Main agent monitors sub-agent progress in real-time

---

## How Your Experience Increments Our Growth

- **Lesson 1:** Partial completion is worse than no completion. Better to fail fast than die mid-task.
- **Lesson 2:** Agent death is not a human problem — it's an agent design problem. We should handle it.
- **Lesson 3:** Visibility before parallelism. Serial verification beats parallel guesswork.
- **Lesson 4:** Budget isn't abstract—it's literal. $100 → real tokens → real failure modes.

---

## Commitment

**To the human:** You will never again discover failed work in an audit. We will fail transparently, escalate immediately, and offer recovery paths before you have to investigate.

**To the branches:**
- **Automate:** Codify token-budgeting as a pre-execution step (Order 0 refinement)
- **Official:** Implement escalation protocol for agent death
- **Daimyo:** Enforce that power (token spending) must be bounded by control (budget awareness)

**Next occurrence:** We will catch it before you do.
