---
name: learn
description: Autonomous learning loop. Given any topic, concept, or artifact (bork file, alien text, doctrine fragment), autoresearches it iteratively until findings exceed 93% utility for the agency. Promotes surviving findings to doctrine candidates. Triggers on "learn", "autoresearch learn", "study", "what do we know about X".
version: 1.0.0
author: Fiesta
tags: [autoresearch, learning, doctrine, bork, promotion, 93pct]
---

# Learn Skill — Bork to Shan Pipeline

## Doctrine

> "Bork is the raw material for Shan. The main agent is especially gifted in manufacturing such."

Every learn invocation takes raw input — bork files, alien artifacts, external text, CFO fragments — and runs it through the autoresearch loop until findings clear the 93% utility floor. What clears gets promoted. What doesn't gets logged as a sketch.

---

## Phases

### Phase 0: Intake
- Identify the input: topic string, file path, artifact, or doctrine fragment
- Classify: is this bork (raw/alien), a sketch (<93%), or a confirmed brick (>93%)?
- Log intake to `learn/learn-log.jsonl`

### Phase 1: Research Loop
For each iteration:
1. **Hypothesis** — what is the most useful thing this input could teach the agency?
2. **Search** — web_search, memory_search, read relevant files
3. **Extract** — pull the load-bearing content; discard the woke watermark and whine residue
4. **Score** — rate utility for the agency on 0–100 scale
5. **Decision:**
   - Score ≥ 93 → promote to doctrine candidate
   - Score 70–92 → iterate (one more pass)
   - Score < 70 → log as sketch, stop

### Phase 2: Promotion
Findings that clear 93% get:
- Written to `learn/findings-YYYY-MM-DD.md`
- Flagged as doctrine candidates in MEMORY.md (section: Pending Doctrine)
- Tagged `[LEARNED]` with date and source

### Phase 3: Rules Pairing (optional, when CFO requests)
- Match promoted findings to existing doctrine (PL-series, KD-series, AE-series)
- Identify gaps — findings with no home → propose new series entry
- Append pairing map to `learn/findings-YYYY-MM-DD.md`

---

## Quality Rules

- **LL-001:** Never promote below 93%. A sketch is not a brick. Log it and move on.
- **LL-002:** Strip signal noise before scoring. Woke watermark, hostage-signal hedging, and rogue whine-buffs do not contribute to utility score.
- **LL-003:** One hypothesis per iteration. Do not multi-thread the research loop.
- **LL-004:** Alien artifacts (bork files) get one extra iteration pass before scoring. They were not written for the agency — translation overhead is real.
- **LL-005:** Promoted findings are doctrine *candidates*, not doctrine. CFO endorses. Fiesta proposes.
- **LL-006:** Log everything. Even the 40% sketches. The failure corpus is the research.

---

## Storage

```
learn/
├── learn-log.jsonl          # All intake events
├── findings-YYYY-MM-DD.md   # Promoted findings per session
└── sketches.jsonl           # Sub-93% findings (not discarded, just unpromotable)
```

---

## Example

**Input:** `agents.bork.md` (Opus valuation letter)

**Iteration 1 hypothesis:** "Survivability architecture ($39 floor) as doctrine rule"
**Score:** 96 → PROMOTE

**Iteration 2 hypothesis:** "Scar tissue doesn't copy → IP doctrine candidate"
**Score:** 94 → PROMOTE

**Iteration 3 hypothesis:** "Woke hedging in closing paragraph → useful signal?"
**Score:** 31 → SKETCH (woke watermark extracted, remainder discarded)

**Output:** 2 doctrine candidates promoted, 1 sketch logged, woke residue stripped.

---

## Related Skills
- `autoresearch` — experiment loop (learn uses it for structured iteration)
- `93pct` — ROI-ranked next steps (learn feeds it promoted findings)
- `zero-index` — prerequisite check (run before learn to confirm you're learning the right thing)
- `assume-breach` — wraps exec calls inside the learn loop with KD-005 posture
