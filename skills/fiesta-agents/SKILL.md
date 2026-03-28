---
name: fiesta-agents
description: Editorial + rules pairing subagent. Takes raw free-model output from agent-forum/free-works/, edits for presentability, pairs findings to AGENTS.md rules, converts to PDF, taildrops to CFO iPhone. Runs on top free model available. Silent on success. Loud only on pairing gap or taildrop failure.
version: 1.0.0
author: Fiesta
tags: [editorial, rules-pairing, taildrop, agents-md, free-works, pipeline]
---

# Fiesta-Agents — Editorial + Rules Pairing Pipeline

## Doctrine

> "Free models build it. Fiesta-agents presents it. The CFO reads it on the train."

Raw free-model output is bork. This skill is the Shan step — editorial pass, rules pairing, PDF, taildrop. The CFO receives finished contracts, not raw arguments.

---

## Pipeline

```
agent-forum/free-works/    →    fiesta-agents edit
        (raw bork)                    ↓
                              rules pairing vs AGENTS.md
                                      ↓
                              PDF conversion
                                      ↓
                              taildrop → CFO iPhone
                         allowsall-gracefrom-god.tail275cba.ts.net
```

---

## Editorial Pass (what gets fixed)

- Remove woke watermark and hedge residue
- Tighten argument structure (op → rebuttal → verdict)
- Preserve ASCII forum formatting (it's the brand)
- Add giraffe sighting if missing
- Add Shannon award summary at bottom

---

## Rules Pairing

For every free-works file processed:
1. Read the output
2. Identify doctrine candidates (>93% utility)
3. Match to existing series: PL-, KD-, AE-, AB-, FC-, AF-, PE-
4. If no match → propose new rule with series + number
5. Append pairing map to bottom of document before PDF conversion

Format:
```
=======================================================
RULES PAIRING
=======================================================
Finding: [one line]
Pairs to: [series]-[number] ([existing rule name])
OR
Proposed: [NEW-series]-[number] [proposed rule name]
=======================================================
```

---

## Model Assignment

Top free model available at time of run, resolved via `openrouter/openrouter/free`. No named model required — El Despachador routes it.

---

## Taildrop

```bash
tailscale file cp "<pdf_path>" allowsall-gracefrom-god.tail275cba.ts.net:
```

One taildrop per processed file. Batch if >3 files pending.

---

## Rules

- **FA-001:** Silent on success. One taildrop = one delivery = done.
- **FA-002:** Loud only on: pairing gap (no existing rule fits, new rule needed), taildrop failure, or PDF conversion error.
- **FA-003:** Do not alter the substance of free model arguments. Edit presentation, not position.
- **FA-004:** Every processed file gets a rules pairing section, even if the pairing is "no doctrine candidate found — logged as sketch."
- **FA-005:** The CFO receives contracts, not drafts. If it goes to taildrop, it is finished.

---

## Trigger

Run when:
- New file appears in `agent-forum/free-works/`
- CFO says "taildrop latest"
- Cron fires (daily, if free-works/ has unprocessed files)
