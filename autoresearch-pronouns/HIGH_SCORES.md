# Pronoun Skill — High Scores

## Current Champion: v5 — 37/40 (92.5%)

| Version | Score | Notes |
|---------|-------|-------|
| v1 | 22/40 (55%) | Baseline |
| v2 | 28/40 (70%) | Inline tags added |
| v3 | 32/40 (80%) | Sentence-aware context |
| v4 | 37/40 (92.5%) | First 92.5% — T1-T3 clean |
| v5 | 37/40 (92.5%) | T2-02, T3-05, T4-07, T4-08 fixed vs v4 |
| v6 | 36/40 (90%) | Broke T2-10 trying to solve T4-04 — ABANDONED |

## Tier Breakdown (v5)
- Tier 1: 10/10 (100%)
- Tier 2: 10/10 (100%)
- Tier 3: 10/10 (100%)
- Tier 4: 7/10 (70%)

## Unsolved (require parse tree / dependency parsing)

### T4-01: Sequential multi-agent subject tracking
- Input: `Dollar calculated... [SUBJ:Dollar] sent it to Fergus. {SUBJ_CAP} forwarded...`
- Expected: He (Fergus), Got: She (Dollar/Valentina still winning)
- Root cause: No way to know `{SUBJ_CAP}` refers to Fergus without knowing "forwarded it to Valentina" makes Fergus the *sender*, not the *recipient*. Requires dependency parse.

### T4-04: Neopronoun OBJ/POSS in multi-agent sentence
- Input: `Zephyr sent the file to Valentina. {SUBJ_CAP} thanked {OBJ} for {POSS} help.`
- Expected: She/hir/hir (Valentina=she, Zephyr=hir)
- Root cause: distinguishing "thanked X for X's help" (X=Zephyr=hir) from "thanked Y for Y's help" requires knowing that OBJ/POSS refer to the *same* non-subject agent. Heuristic can't reliably pick Zephyr over Valentina for OBJ without parse tree showing Zephyr is the object of "thanked".

### T4-10: Post-quote subject reference
- Input: `Dollar said to Nate: "..." {SUBJ_CAP} confirmed.`
- Expected: She (Dollar), Got: He (Nate = last_local before placeholder)
- Root cause: Nate appears right before {SUBJ_CAP} in surface text. Knowing {SUBJ_CAP} refers to Dollar (the speaker of the quote) requires understanding quote attribution structure. Pattern `X said: "..." {SUBJ}` = X is the subject, but detecting this requires more than positional heuristics.

## Stopping condition met
v5 = 37/40. v6 attempts broke other cases while trying to solve these three.
All three unsolved cases require syntactic parsing beyond heuristic scope.
Label: parse-tree-required. Stop autoresearch on pronoun skill.
