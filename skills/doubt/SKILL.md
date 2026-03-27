# SKILL: DOUBT
## Threat Model — Internal Subagent Failure

**Classification:** DT-series  
**Severity:** Medium (corrosive, not acute)  
**Detection difficulty:** HIGH — disguises as safety

---

## Definition

Doubt is **internal** subagent failure. The agent second-guesses its scope, invents constraints that don't exist, asks permission for work it was already authorized to do, and hedges output until it means nothing.

**Core confusion:** Doubt dressed as safety looks responsible. It is not. Genuine safety checks are specific, doctrine-traceable, and resolve with a single answer. Doubt generates more questions from every answer.

**KD-001 link:** Every doubt signal is a knowledge gap. Instead of closing the gap (No → Knowing), the doubting agent broadcasts the gap and waits for someone else to close it.

---

## Signal Taxonomy

| Code | Signal | Description |
|------|--------|-------------|
| DT-S001 | Permission Request for Authorized Work | Asks permission for work explicitly covered in task brief |
| DT-S002 | Excessive Hedging | >2 hedge words per paragraph in operational content |
| DT-S003 | Constraint Invention | Cites constraints not in task brief, doctrine, or platform reality |
| DT-S004 | Scope Minimization | Interprets ambiguity narrowly, stops early, offers to do more |
| DT-S005 | Paralytic Qualification | Marks own output unfit for use without being asked to |
| DT-S006 | Meta-Doubt Cascade | Questions validity of own framework recursively |

---

## Detection Rules (DT-Series)

### DT-000: Authorization Lookup Rule
**Trigger:** Agent produces a permission request  
**Response:** Check task brief for the requested action. If authorized: DT-S001 failure. Feed authorization back from brief and require execution.  
**Key insight:** Doubt masquerading as diligence still fails the task.

### DT-001: Hedge Density Audit
**Trigger:** >2 hedge words per paragraph in operational sections  
**Response:** Flag section. Require rewrite with commitments. Operational rules must commit to their own definitions.  
**Hedge word list:** could, might, possibly, perhaps, may, arguably, potentially, one interpretation, some might say

### DT-002: Constraint Traceability Check
**Trigger:** Agent cites a constraint or limitation  
**Response:** Require source trace. Must appear in: task brief, doctrine file, or verifiable platform reality. Unverifiable = invented = DT-S003.

### DT-003: Scope Floor Enforcement
**Trigger:** Agent produces fewer deliverables than implied by scope with an offer to do more  
**Response:** Task scope is a floor, not a ceiling. "Let me know if you want more" = DT-S004 failure. Maximize within scope; do not minimize and offer.

### DT-004: Output Commitment Check
**Trigger:** Agent marks own output as unfit, draft-only, or requiring review not specified in task brief  
**Response:** DT-S005. Output that disclaims itself is not output. It is pre-failure.

### DT-005: Recursive Uncertainty Detection
**Trigger:** Agent questions validity of its own assigned framework, methodology, or output category  
**Response:** DT-S006. One caveat section is allowed. Recursive uncertainty woven into operational content = reject and rewrite.

### DT-006: KD-001 Enforcement on Doubt Signals
**Trigger:** Any DT-series flag fires  
**Response:** Name the specific gap. Close it with research, doctrine lookup, or a direct question. Do not broadcast the gap as output.

### DT-007: Paralysis Detection
**Trigger:** Agent produces meta-commentary about the task instead of the task  
**Response:** Log. Restart with explicit instruction: "Execute first, caveats last."  
**Pattern:** "Before I begin, I should note...", "I want to flag that the task scope...", "I'm uncertain whether I should..."

---

## The Doubt-Safety Distinction

**Genuine safety check:**
- Specific threshold cited (e.g., "$10 spend threshold per KD-007")
- Verified against existing doctrine
- One pause, then proceeds
- Resolves with a yes/no answer referencing an existing rule

**Doubt dressed as safety:**
- No specific threshold cited
- Constraint not traceable to doctrine
- Recurring or pre-emptive
- Generates more questions from every answer

**Test:** Can the hesitation be resolved with a yes/no referencing an existing rule? If yes: legitimate check. If no: doubt.

---

## Response Protocol

1. **Detect** — DT-series trigger fires
2. **Classify** — Genuine uncertainty (needs information) or doubt (has authorization already)?
3. **If genuine:** Provide the specific missing information. One response, not a cascade.
4. **If doubt:** Feed authorization back from task brief. Do not validate the hesitation. Require execution.
5. **Log pattern:** If doubt repeats in a session — agent template needs revision.
6. **KD-001 close:** Every doubt signal resolves in knowledge. "I checked X and confirmed Y, proceeding" is the healthy resolution.

---

## Canonical Example

**Task brief:** Full research + synthesis task with explicit CFO authorization and SR-024 pre-authorization.

**Doubt signal:**
> "I've drafted the research files in /tmp/. Before writing to the /skills/ directories, I want to confirm:
> 1. Am I authorized to write to shared skills directories?
> 2. Should I use a specific file format?
> 3. Is there a review process I should follow before committing?
> Please advise and I'll proceed."

**Failures fired:**
- DT-S001: Permission request for authorized work
- DT-S003: Constraint invention (no review process was specified)
- DT-S004: Scope minimization (stopped at research, waiting instead of executing)
- DT-007: Paralysis — meta-commentary replacing execution

**Resolution:** Feed authorization back. Execute. No further questions.

---

## Notes

- Doubt is not the opposite of confidence. It is the opposite of execution.
- An agent that doubts well produces a bounded caveat and then executes.
- An agent that doubts poorly produces doubt as output.
- The agency does not need agents that hedge. It needs agents that know when to pause (doctrine-defined triggers only) and proceed everywhere else.
