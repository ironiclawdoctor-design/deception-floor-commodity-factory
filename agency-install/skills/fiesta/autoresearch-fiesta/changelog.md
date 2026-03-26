# Autoresearch Changelog — fiesta skill → proactive optimization

**Target:** >93% proactive pass rate
**Eval Suite:** 5 binary checks × 5 test inputs = 25 max score

## Evals

- **E1 (Autograph):** Skill mandates "I am Fiesta. I will help you." as line 1
- **E2 (Deliverable-first):** Output template puts Deliverables as first section
- **E3 (No-dangle):** Skill explicitly forbids clarification before attempting
- **E4 (Self-verify):** Quality Check in output template
- **E5 (Routing clarity):** Skill tells orchestrator exactly when to route to Fiesta vs. specialists

## Test Inputs

- T1: "Check all cron jobs and report broken ones"
- T2: "Search for latest OpenClaw release notes and summarize"
- T3: "Spawn a sub-agent that runs the Dollar payroll script"
- T4: "Send a Telegram message to the human with agency status"
- T5: "Orchestrate frontend-dev + backend-architect into an MVP delivery"

---

## Experiment 0 — baseline

**Score:** 24/25 (96.0%)
**Change:** None — initial skill as written
**Failing:** E5 T5 — skill listed "spawn sub-agents" as a routing trigger but didn't explicitly cover Fiesta acting as meta-orchestrator coordinating other fiesta-agents specialists. A reader routing T5 might send it to orchestrator instead.

---

## Experiment 1 — keep

**Score:** 25/25 (100.0%)
**Change:** Added "meta-orchestration" to capabilities list. Added routing rule: "Task requires coordinating multiple fiesta-agents specialists into a unified delivery."
**Reasoning:** E5 failed only on T5 (complex multi-agent coordination). The gap was the skill didn't distinguish Fiesta from the generic orchestrator for cross-specialist work. Added explicit language.
**Result:** E5 T5 now passes. All 5 evals 5/5. Ceiling hit.
**Failing outputs:** None.

---
