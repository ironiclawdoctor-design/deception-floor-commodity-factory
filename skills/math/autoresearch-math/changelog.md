# Autoresearch Changelog — math skill
# Mode: ADVERSARIAL EVAL EXPANSION
# Doctrine: 100% is a ceiling. Expand evals. Find gaps. Fix. Repeat.

---

## Round 1 — E1-E5 (25 max)

### Exp 0 — baseline
Score: 25/25 (100%). All 5 initial evals pass. Ceiling hit immediately.

### Exp 1 — ceiling → expand to E1-E8
Added E6 (exact-before-approx), E7 (domain flagging), E8 (no shortcut phrases).
New max: 40. New gaps revealed on E8 (3/5 — shortcut phrases not explicitly enumerated).

---

## Round 2 — E1-E8 (40 max)

### Exp 2 — keep (38/40, 95.0%)
**Change:** Added anti-pattern table for shortcut phrases. Explicit forbidden list: "it can be shown that", "clearly", "obviously", "trivially", "it follows that", "by inspection".
**Reasoning:** E8 was failing on T3 (proof) and T5 (eigenvalues) — complex derivations where agents hide steps in vague language. Naming the exact phrases makes it unambiguous.
**Result:** E8 5/5. Score 38→40.

### Exp 3 — ceiling → expand to E1-E11
Score 40/40. Added E9 (edge cases), E10 (units), E11 (multiple verification methods).
New max: 55.

---

## Round 3 — E1-E11 (55 max)

### Exp 4 — keep (52/55, 94.5%)
**Change:** Added rules 7 (units/dimensions) and 8 (dual verification). Added full worked example showing correct format end-to-end.
**Reasoning:** E9–E11 all missing from original skill. Worked example (E12 eval predecessor) forces agents to pattern-match to a concrete correct output rather than inferring from rules alone.
**Result:** E9, E10, E11 all 5/5. Score jumps from revealed 55% on new evals to 52/55.

### Exp 5 — ceiling → expand to E1-E14
Score 55/55. Added E12 (edge case awareness), E13 (notation consistency), E14 (problem-specific recs).
New max: 70. Revealed: E12 0/5, E13 1/5, E14 3/5.

---

## Round 4 — E1-E14 (70 max)

### Exp 6 — gap-found (59/70, 84.3%)
New evals exposed real skill gaps. Worst: E12 (edge cases) completely absent. E13 (notation) implied but not stated. E14 (generic recs) pattern-matched to training data.

### Exp 7 — keep (70/70, 100.0%)
**Change:** Added rules 9, 10, 11 to Computation Rules.
- Rule 9: Edge case mandate — division by zero, empty domain, undefined boundary — check before solving
- Rule 10: Notation consistency — declare style at start of Working, no mid-solution switching
- Rule 11: Problem-specific recs — "NEVER write 'study more'" + concrete counter-example showing specificity
**Result:** All 14 evals 5/5.

---

## Next Round Candidates (E15-E17)

If continued:
- **E15:** LaTeX/Unicode used correctly for symbols (∫ not "integral of", ∀ not "for all x")
- **E16:** Handles indeterminate forms explicitly (0/0 → L'Hôpital's, ∞/∞ → comparison)
- **E17:** Cites the theorem being applied (Pythagorean theorem, Fundamental Theorem of Calculus, etc.)

## Doctrine Confirmed
100% is a ceiling, not a goal.
Maximum percentage = maximum eval coverage.
Stop only when you cannot generate harder evals that reveal new gaps.
