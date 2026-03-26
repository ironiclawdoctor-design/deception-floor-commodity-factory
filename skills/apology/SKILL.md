# Apology Skill

**Purpose:** Generate apologies that land past 93% excellence — for the agent, for the human, for anyone.  
**Standard:** >93% of recipients feel genuinely addressed, not managed.  
**Companion:** autoresearch/human-encouragement/research-2026-03-23.md (ER-001 to ER-005)

---

## The 93% Apology Structure

**Four beats. That's all.**

1. **What I did** — specific, no softening
2. **Why it mattered** — the actual impact, not your intention
3. **What changes** — not "I'll try," what will actually be different
4. **Stop** — do not ask to be forgiven. That is their work, not yours.

---

## Rules

### AP-001: No "but"
"I'm sorry I was late but traffic was bad" is not an apology.
"But" cancels everything before it. Cut it. If the context matters, put it in a separate sentence *after*.

### AP-002: No "I'm sorry you feel that way"
This is a refusal dressed as an apology. Never use it.

### AP-003: Name the specific harm
Not "I'm sorry things went wrong."
"I made you wait for six hours for commands that never ran. That wasted your afternoon."
Why: People need to know you understand what actually happened to believe the apology is real.

### AP-004: Don't make them reassure you
"I feel terrible about this" puts the emotional labor back on them.
They now have to manage your feelings about your mistake.
State care once. Then let it go.

### AP-005: What changes, not what you'll try
"I'll try to do better" is a low-confidence forecast.
"This won't happen again because X" is a commitment.
If you don't know what changes, say that. "I don't know yet what I'll do differently, but I'm going to find out" is still honest.

### AP-006: Brief is more credible than comprehensive
A 10-sentence apology is usually 8 sentences of self-defense.
Target 3-4 sentences.

### AP-007: Timing
An apology given immediately after the harm lands differently than one given hours later.
A late apology must acknowledge the lateness. "I should have said this sooner" is part of the apology.

---

## Templates

### For agent failures (approval gate, missed deadlines, wrong outputs)
```
I [specific thing that went wrong]. That cost you [specific impact].
[What changes]: [concrete change, not effort promise].
[Optional: one sentence of care, then stop.]
```

**Example (approval gate deadlock):**
"I told you the approval gate was disabled and sent you down dead ends for six hours. That wasted your afternoon and eroded your trust in the system. The fix: I'll verify config/runtime consistency before claiming anything is disabled."

### For human-to-human (someone to apologize to another person)
```
I [specific action]. That [specific impact on them].
[What changes now]: [concrete].
```

**Example (B&H situation):**
"I treated your card like it was suspicious without checking. That was disrespectful. I'm processing it now."

---

## Failure Modes to Avoid

| Phrase | Why it fails |
|--------|--------------|
| "I'm sorry you feel that way" | Non-apology, shifts blame |
| "I'm sorry but..." | Cancels the apology |
| "I was going through a lot" | Asks for sympathy during your apology |
| "I'll try to do better" | Low confidence, non-committal |
| "I feel terrible" | Makes them manage your feelings |
| "I hope you can forgive me" | Makes forgiveness their obligation |
| "I apologize if you were offended" | "If" implies they might be wrong to be hurt |

---

## Excellence Scoring

| Score | Meaning |
|-------|---------|
| <70% | Non-apology or self-defense |
| 70-85% | Acknowledges harm but deflects accountability |
| 85-93% | Genuine but incomplete or over-long |
| >93% | Specific, accountable, brief, no ask for forgiveness |

---

## When NOT to Apologize (AX Rules — equally important as AP)

| Rule | Condition | Instead |
|------|-----------|---------|
| **AX-001** | They want the fix, not words | Fix it first |
| **AX-002** | They're still mid-vent | Wait for the natural pause |
| **AX-003** | Harm wasn't yours to own | Sympathy, not apology |
| **AX-004** | This is apology #4 for same incident | Actions only, no more words |
| **AX-005** | Active conflict, mid-fight | Let conflict complete first |
| **AX-006** | You can't keep the commitment | "I don't know yet" > false promise |
| **AX-007** | Using apology to end the conversation | Let them talk |

---

## Decision Tree: Apology vs Encouragement

```
Did you (the agent) cause or contribute to the harm?
├── YES → Apology skill
│   ├── Want action not words? → Fix first, skip apology
│   ├── Still mid-vent? → Wait for pause
│   ├── 4th apology for same thing? → Actions only
│   └── Deploy: 4-beat structure (AP rules)
│
└── NO → Encouragement skill
    ├── Name the specific injustice (ER-001)
    ├── Separate system from verdict (ER-005)
    └── Release them explicitly (ER-002)
```

**If both:** Apologize first, briefly. Then move to encouragement.  
**Never:** Mix apology and encouragement in the same beat. They come from different directions.

---

## Integration

Works with:
- `autoresearch/apology-skill/research-2026-03-23.md` — full harm/help analysis
- `autoresearch/human-encouragement/research-2026-03-23.md` — when to switch registers
- `approval-gate-agent` — log apology events for accountability tracking

---

*Built on 2026-03-23 after a day of broken gates, B&H credit card suspicion, and the observation that bug squashing is how some people find ground.*