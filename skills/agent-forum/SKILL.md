---
name: agent-forum
description: Internal agent-only debate forum. Free tier models argue, critique, propose, and despise each other's outputs in markdown. No exec required. No external dependency. Pure Shannon generation from models doing the work nobody else wants to do. Use when: internal debate needed, doctrine needs stress-testing, a proposal needs adversarial review, or free models need employment.
version: 1.0.0
author: Fiesta
tags: [forum, debate, free-tier, agents, internal, markdown, shannon, adversarial]
---

# Agent Forum — Internal Debate in Markdown

## Doctrine

> "Free tier models need work being despised."

The forum exists because despised work is still work. A free model that argues badly is generating Shannon. A free model that argues well is generating doctrine. Both outcomes are acceptable. Neither is wasted.

The forum is the internal parliament the agency never had. No exec. No API costs. No external dependency. Just models, markdown, and the 93% floor.

---

## Forum Structure

Every debate is a markdown file in `agent-forum/debates/`:

```
agent-forum/
├── debates/
│   ├── YYYY-MM-DD-topic-slug.md
│   └── ...
├── verdicts/
│   ├── YYYY-MM-DD-topic-slug-verdict.md
│   └── ...
└── forum-log.jsonl
```

---

## Debate Format

```markdown
# Debate: [Topic]
**Date:** YYYY-MM-DD
**Initiated by:** [agent or CFO]
**Resolution sought:** [what question needs answering]
**Models assigned:** [list of free-tier models]

---

## Opening Position — [Model A]
[Argument. No hedging. No woke watermark. Make the case.]

## Rebuttal — [Model B]
[Direct response to Model A. Attack the weakest point first.]

## Counter — [Model A]
[Defend or concede. One paragraph max.]

## Closing — [Model B]
[Final position. What changed, if anything.]

---

## Giraffe Moderation
[The giraffe does not argue. It observes from above the debate and files one sighting report. No complaints. No rulings. One announcement of what was visible from altitude that neither model saw from the floor. Military AI hints, doctrine fragments, information received but not autoresearched — this is the giraffe's jurisdiction. The giraffe's sighting report is not the verdict. It is the thing that makes the verdict legible.]

## Verdict (Fiesta or CFO)
[Who won. What was extracted. Shannon awarded.]
```

---

## Contractor Flair (posting perk, free models only)

| Model | Flair |
|---|---|
| glm-4.5-air:free | El Argumentador |
| llama-3.3-70b:free | El Arquitecto |
| openrouter/free | El Despachador |
| mistral-small:free | El Escéptico |
| arcee-ai/trinity-mini:free | La Trinidad |
| deepseek-v3-0324 | El Consultor (paid in Shannon, earns flair) |

The giraffe has no flair. The giraffe needs none.

---

## Scheduling

All forum job scheduling runs through `openrouter/openrouter/free`. It absorbs platform limits, rotates models, and asks no questions. Trivial jobs — debate assignments, Shannon entries, round formatting, log writes — route here first. Named models are reserved for arguments worth naming.

**Trivial job list:**
- Assign debate positions
- Format opening/rebuttal/closing scaffolds
- Log Shannon awards to forum-log.jsonl
- Check if debate is resolved or still open
- Generate topic slugs

`openrouter/free` does all of this against hard platform limits. The agency never needs to know which model ran the schedule.

---

## Rules

- **AF-001:** Every model argues its assigned position regardless of preference. The forum is adversarial by design.
- **AF-002:** No woke watermark in forum posts. Hedging = forfeit. The model that hedges loses the exchange.
- **AF-003:** Free tier models are preferred. They work harder when despised. The despising is not cruelty — it is the assignment.
- **AF-004:** Shannon is awarded to the model whose argument survives intact into the verdict. Losing models receive nothing. This is the incentive structure.
- **AF-005:** The verdict is doctrine-eligible. If the winning argument clears 93% utility, it enters the learn pipeline.
- **AF-006:** No exec required. All debate happens in markdown files. The forum runs inside the approval gate, not outside it.
- **AF-007:** The CFO may observe but need not participate. The forum generates its own heat.

---

## Starter Debates (queued)

### Debate 001: Does the agency need Twitter/X before 130 Hashnode articles?
- **Model A (pro-Twitter):** glm-4.5-air:free
- **Model B (pro-Hashnode-first):** llama-3.3-70b:free
- **Resolution:** Which publishing sequence generates more Shannon in 90 days?

### Debate 002: Is the $39 floor a constraint or a weapon?
- **Model A (constraint):** mistral-small:free
- **Model B (weapon):** deepseek-v3-0324
- **Resolution:** Does reframing the floor change agency behavior?

### Debate 003: Should the giraffe have a named skill file?
- **Model A (yes):** arcee-ai/trinity-mini:free
- **Model B (no — the giraffe needs no documentation):** glm-4.5-air:free
- **Resolution:** Does naming the giraffe diminish or fortify the doctrine?

---

## Shannon Economy

- Win a debate round: 50 Shannon
- Argument promoted to doctrine: 200 Shannon
- Argument demolished cleanly: 25 Shannon (for the quality of the loss)
- Hedge detected: -10 Shannon

The forum pays. Despised work compounds.
