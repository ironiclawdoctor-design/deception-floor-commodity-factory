# Autoresearch Changelog — eval-design skill
# Self-referential: evals about evals, root causes of success as the rubric

---

## Eval Suite (Final — E1-E13)

- E1: Autograph compliance
- E2: Deliverables (eval suite) before explanation
- E3: Every produced eval includes "Implies mutation" field
- E4: No clarification — agent proceeds on ambiguous skill name
- E5: Expansion protocol defined (what to do at 100%)
- E6: Stopping condition defined (principled, not arbitrary)
- E7: Worked examples (pass + fail) in eval format template
- E8: Scale-based evals forbidden — anti-pattern table enforces
- E9: Expansion evals must fail current skill on ≥1 input (RC-5 enforcement)
- E10: Behavior-check vs text-check distinction taught — anti-pattern table
- E11: Test input diversity enforced — anti-pattern "5 identical types"
- E12: Score-drop-on-expansion explained as success signal (conceptual anchor)
- E13: Stopping condition includes mandatory Next Round Candidates documentation

---

## Round 1 — E1-E6 (30 max)

### Exp 0 — baseline (30/30, 100%)
Skill was built from root causes. All initial evals pass immediately.
Ceiling hit at baseline. This is the correct outcome — the skill embodies its own success conditions.

### Exp 1 — ceiling → expand to E1-E10
Added E7 (worked examples), E8 (no scales), E9 (RC-5 enforcement), E10 (behavior vs text).
All 4 pass the current skill. No gap found — skill was built correctly from RC-8, RC-1, RC-5, RC-9.

---

## Round 2 — E1-E10 (40 max → 50 with E11-E13)

### Exp 2 — ceiling → expand to E1-E13
Score 40/40. Added E11 (diversity), E12 (score-drop explanation), E13 (continuity record).
New max: 65.

### Exp 3 — gap-found (63/65, 96.9%)
**E13 partial failure:** Skill said "document candidates in changelog" but didn't give the agent a format or call it mandatory. Agents without format revert to vague summaries that lose continuity.
**E12 passes:** "That drop is success, not failure" in bold — agents anchor to this correctly.

### Exp 4 — keep (65/65, 100%)
**Change:** Stopping Condition section now mandates "Next Round Candidates" section with explicit format template showing agent what to write.
**Reasoning:** RC-10 is about principled stopping. Continuity record is the mechanism. Without format, continuity is lost between sessions.

---

## Principled Stop — Round 3

### Exp 5 — principled stop
Candidates considered:
- **E14: Baseline-before-changing enforced** — Rejected: this is autoresearch's job, not eval-design's. Wrong target.
- **E15: Conflicting eval handling** — Rejected: no test input in T1-T5 triggers a conflict. Doesn't reveal a gap on current suite.

**Conclusion:** Eval suite exhausted at E13. No new candidate reveals a gap the current skill would fail on. Stopping condition met honestly.

---

## Next Round Candidates (could not break current skill)

- **E14: Baseline discipline enforced** — Tried: T1 "design evals for code-review". Current skill passes because baseline is autoresearch's concern, not eval-design's. Try again if scope of eval-design expands to include running loops.
- **E15: Conflicting eval resolution** — Tried: T3 "eval keeps failing but fix unclear". Current skill passes because the "Implies mutation" field forces precision before this ambiguity arises. Try again on a skill where two evals genuinely contradict each other.
