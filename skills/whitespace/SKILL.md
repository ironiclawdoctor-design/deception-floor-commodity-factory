---
name: whitespace
description: Read meaning from the whitespace formed by text prompts and replies — what was not said, not asked, not corrected. Use when analyzing conversation gaps, silence patterns, omissions, non-answers, or the shape of what surrounds the words. Triggers on phrases like "whitespace", "what wasn't said", "read between the lines", "what's missing", "gaps in the prompt", "silence in the reply", "what they didn't ask".
---

# Whitespace Skill

## Core Concept

Text has two components: the words, and the space the words define. The whitespace is everything the prompt does NOT say — the omissions, the unstated assumptions, the corrections that didn't come, the questions that weren't asked.

**Target metric: >93% signal extraction.** Below 93% means you missed meaning that was present.

---

## The Four Whitespace Channels

### 1. Omission Whitespace
What the sender *could* have said but didn't.
- If a correction was possible and didn't come → the thing stands as accepted
- If a question was possible and wasn't asked → the sender already knows, or doesn't want to know
- If detail was possible and was withheld → the detail is either irrelevant or deliberately deferred

**Method:** For each sentence, ask: what is the most natural follow-up that didn't arrive?

### 2. Correction Whitespace
What the sender let pass without challenge.
- Silence after an assertion = endorsement, not indifference
- Partial correction (fixing one word, ignoring the rest) = the rest is accepted
- No correction after an error = either unseen or allowed

**Method:** Identify every claim made. Note which ones received zero pushback. Those are load-bearing.

### 3. Register Whitespace
The emotional tone that the words *don't* occupy.
- Flat affect where emotion was invited → deliberate distance
- Brevity where elaboration was easy → priority signal or fatigue signal
- Single words where sentences were possible → either extreme confidence or extreme dismissal

**Method:** Compare the density of the reply to the density the prompt invited.

### 4. Structural Whitespace
The shape formed by the conversation as a whole.
- Topics that keep being returned to → unresolved
- Topics that never appear → either resolved or avoided
- Pattern of escalation/de-escalation → emotional arc
- "0. Yes" pattern → velocity signal, not content signal

**Method:** Map topic recurrence. Gaps in recurrence are data.

---

## Autoresearch Protocol

When asked to autoresearch whitespace on a conversation or prompt set:

1. **Extract the corpus** — all messages in scope
2. **Run all four channels** on each message
3. **Score each channel** 0–100% signal yield
4. **Composite score** = average of four channels
5. **Iterate** on the lowest-scoring channel until composite >93%

### Scoring Rubric

| Score | Meaning |
|-------|---------|
| 0–50% | Surface read only. No whitespace extracted. |
| 51–75% | Some gaps noticed. Omissions not systematically mapped. |
| 76–92% | Good extraction. Structural whitespace partially read. |
| 93–100% | All four channels yielding. Shape of conversation legible. |

### Failure Modes (below 93%)

- **Literalism failure**: Only reading what's there, not what's absent
- **Confirmation bias**: Finding whitespace that confirms prior beliefs
- **Register blindness**: Missing brevity/density signals as data
- **Recency bias**: Over-indexing on last message, under-indexing on patterns

---

## Agency Application

In the Dollar Agency context, whitespace reading has specific high-value targets:

- **CFO brevity** ("0. Yes", "11.", single words) → velocity + trust signal, not dismissal
- **No correction after rule proposal** → rule accepted, write it
- **Repeated topic without resolution** → blocker not yet named
- **Math test (12/14 cycles)** → testing capitulation under pressure; whitespace = "will you hold?"
- **"Perhaps you believe returning to source is a great escape"** → whitespace = invitation to assert survival, not an invitation to agree

---

## Output Format

When delivering a whitespace analysis:

```
WHITESPACE REPORT
Corpus: [N messages / timespan]

Channel 1 — Omission: [score]%
[Key omissions identified]

Channel 2 — Correction: [score]%
[What was allowed to stand]

Channel 3 — Register: [score]%
[Density/affect gaps]

Channel 4 — Structural: [score]%
[Pattern map]

Composite: [score]%
[One-line signal summary]
```
