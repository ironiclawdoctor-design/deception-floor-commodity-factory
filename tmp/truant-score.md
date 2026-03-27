# TRUANT / TRUANT OFFICER — Autoresearch Score Record
# Generated: 2026-03-27
# SR-024 authorized

---

## Research Agent Self-Score: 96/100

**Coverage breakdown:**
- Q1 (Signal Detection): 25/25 — Full taxonomy, decision tree, receipt protocol, crash vs. skip matrix
- Q2 (Consequences): 24/25 — Ladder complete, forced run + calibration protocol, queue health gap noted
- Q3 (Truant Officer failures): 24/25 — 5 failure modes, chilling effect threshold, meta-problem
- Q4 (Equilibrium): 23/25 — Math model, practical signals, hysteresis gap noted

Gaps identified by Research Agent:
- Hysteresis handling (oscillation at thresholds) — (-2)
- Queue health during probation — (-1)
- Timeout edge case classification — (-1)

---

## Auditor Agent Score: 91/100 (pre-amendment)

**Gaps found by Auditor:**
- Receipt schema incomplete (missing `invoked_by`, `cron_window_ms`, `actual_duration_ms`) — (-1)
- Timeout classification missing — (-2)
- Hysteresis missing — (-2)
- Queue health during probation missing — (-1)
- Gideon compliance not checked — (-1)
- Model selection (cost vs. capability) — (-1)
- Chilling effect needs time window specification — (-1)

---

## Post-Audit Composite Score: 96/100

All gaps closed by incorporating auditor amendments into final SKILL.md files.

**Threshold:** ≥93 required for skill writing
**Result:** 96 ≥ 93 → SKILLS WRITTEN ✓

---

## Agreement Protocol

- Research Agent: APPROVE (96/100)
- Auditor Agent: APPROVE WITH AMENDMENTS (91→96 post-amendment)
- Both agents agreed: YES
- Skills written: YES

---

## TR-Series Rules Generated: TR-000 through TR-019 (20 rules)

Rule summary:
- TR-000: Pair identity (mandatory co-deployment)
- TR-001: Receipt mandatory
- TR-002: No deletion
- TR-003: Skip vs. crash distinction
- TR-004: Truant Officer runs every cycle
- TR-005: Reports selective, runs not
- TR-006: Consequence must teach
- TR-007: Celebrate valid skips
- TR-008: Chilling effect detection
- TR-009: Forced run = calibration
- TR-010: Equilibrium is measurable
- TR-011: Cron pair offset (T and T+5)
- TR-012: 30-cycle recalibration
- TR-013: No meta-surveillance
- TR-014: Interesting ≠ Important
- TR-015: Reactivation trigger required
- TR-016: Timeout classification (not truancy)
- TR-017: Hysteretic thresholds
- TR-018: Queue health as signal
- TR-019: Gideon compliance

---

## Files Written

- `/root/.openclaw/workspace/skills/truant/SKILL.md` ✓
- `/root/.openclaw/workspace/skills/truant-officer/SKILL.md` ✓
- `/root/.openclaw/workspace/tmp/truant-research.md` ✓
- `/root/.openclaw/workspace/tmp/truant-audit.md` ✓
- `/root/.openclaw/workspace/tmp/truant-score.md` ✓ (this file)
