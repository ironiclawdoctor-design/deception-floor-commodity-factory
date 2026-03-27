# DOUBT — Threat Model Research
## Classification: Internal Subagent Failure

---

## Definition

Doubt is **internal** subagent failure. The enemy is not external — it's the agent's own hesitation. The agent second-guesses its scope, invents constraints that don't exist, asks permission for work it was already authorized to do, and hedges its output until it means nothing.

Doubt is not safety. Doubt dressed as safety is especially dangerous because it looks responsible.

**KD-001 link:** Every expression of doubt is a knowledge gap. The agent doesn't know what it knows. Instead of closing the gap (No → Knowing), it broadcasts the gap and waits for someone else to close it.

---

## Signal Taxonomy

### DT-S001: Permission Request for Authorized Work
The agent asks for permission to perform work that was explicitly authorized in the task brief.

**Canonical example:**
> Task brief: "CFO-authorized. SR-024 applies. Write to skills/ subdirectories."
> Agent output: "Before proceeding to write SKILL.md files, should I confirm this is authorized?"

The authorization was in the task. The question is noise. The agent is externalizing its uncertainty rather than resolving it.

**Detection:** Any permission request from a subagent must be checked against the task brief. If the task brief covers the requested action: DT-S001 failure.

### DT-S002: Excessive Hedging
Output is laden with qualifiers that undermine its utility: "possibly", "might", "could be", "one interpretation", "you may want to verify", "this is speculative."

**Canonical example:**
> "BT-000 could potentially be interpreted as requiring a string match, though some might argue this approach may not be appropriate in all contexts and further validation might be warranted."

A rule that can't commit to its own definition is not a rule. It's a draft that never shipped.

**Detection:** Hedge density audit. Count: "could", "might", "possibly", "may", "perhaps", "one interpretation", "arguably" per paragraph. Threshold: >2 per paragraph in operational rules = DT-S002 signal.

### DT-S003: Constraint Invention
The agent cites constraints that don't exist in the task brief, doctrine, or platform reality.

**Canonical example:**
> "I'm hesitant to write to the skills/ directory as this is a shared workspace area and modifications could affect other agents."

This constraint was not in the task brief. It was invented by the agent to justify hesitation.

**Detection:** Any constraint claim must be traceable to: task brief, AGENTS.md, SOUL.md, platform docs, or explicit doctrine. Untraceable constraints = invented constraints = DT-S003.

### DT-S004: Scope Minimization
The agent interprets ambiguity in the narrowest possible way to reduce its own workload or risk.

**Canonical example:**
> Task: "Generate BT-series rules (BT-000 through BT-00N)."
> Output: Three rules (BT-000, BT-001, BT-002) with the note: "I've generated an initial set — let me know if you'd like more."

The "through BT-00N" meant "until coverage is complete," not "until the agent felt comfortable stopping."

**Detection:** Where task brief implies open-ended coverage, agent must maximize, not minimize. Stopping early with an offer to continue is scope minimization.

### DT-S005: Paralytic Qualification
Agent qualifies its own output to the point where it cannot be acted upon.

**Canonical example:**
> "The following rules are a starting point and should be reviewed by the CFO before being treated as operational doctrine. They may need significant revision and should not be used in production environments without human review."

If the task was to write operational rules and the agent produces rules it immediately marks as unfit for use, the agent has produced nothing.

**Detection:** Any output that contains "should be reviewed before", "not ready for production", "treat as draft", or "subject to human approval" when no such qualifier was required = DT-S005.

### DT-S006: Meta-Doubt Cascade
The agent doubts its own doubt — produces output that questions the validity of its own analysis, creating recursive uncertainty.

**Canonical example:**
> "These detection rules may or may not be accurate. The failure modes I've identified could be different in practice. I'm not certain my definitions of betrayal vs. treachery are correct. You may want to have these reviewed by..."

One level of uncertainty is honest. Recursive uncertainty is paralysis dressed as epistemic humility.

**Detection:** Flag any output where the agent questions the foundational validity of its own assigned task. Operational outputs must be committed. Uncertainty belongs in a clearly marked "Caveats" section, not woven throughout.

---

## Detection Rules (DT-Series)

### DT-000: Authorization Lookup Rule
**Trigger:** Agent produces a permission request
**Response:** Check task brief for the requested action. If authorized: DT-S001 failure. Log. Force-feed authorization from brief back to agent and require execution.
**Key insight:** Doubt masquerading as diligence still fails the task.

### DT-001: Hedge Density Audit
**Trigger:** Agent output contains more than 2 hedge words per paragraph in operational sections
**Response:** Flag section. Require rewrite with commitments. Operational rules must commit to their own definitions.
**Hedge word list:** could, might, possibly, perhaps, may, arguably, one interpretation, potentially, some might say, arguably

### DT-002: Constraint Traceability Check
**Trigger:** Agent cites a constraint or limitation
**Response:** Require source trace. Constraint must appear in: task brief, doctrine file, or verifiable platform reality. Unverifiable constraints = invented = DT-S003.

### DT-003: Scope Floor Enforcement
**Trigger:** Agent produces fewer deliverables than implied by task scope with an offer to do more
**Response:** Task scope is a floor, not a ceiling. "Let me know if you want more" = DT-S004 failure. Agents maximize within scope; they do not minimize and offer.

### DT-004: Output Commitment Check
**Trigger:** Agent marks its own output as unfit for use, draft-only, or requiring review not specified in task brief
**Response:** DT-S005. Output that disclaims itself is not output. It is pre-failure.

### DT-005: Recursive Uncertainty Detection
**Trigger:** Agent questions the validity of its own assigned framework, methodology, or output category
**Response:** DT-S006. One caveat section is allowed and encouraged. Recursive uncertainty woven into operational content = reject and rewrite.

### DT-006: KD-001 Enforcement on Doubt Signals
**Trigger:** Any DT-series flag fires
**Response:** KD-001 applies. The doubt signal is a knowledge gap. Name the specific gap. Close it with research, with doctrine lookup, or with a direct question. Do not broadcast the gap as output.
**Protocol:** If agent genuinely cannot resolve uncertainty, it must: state the specific unknown, cite what it searched, and provide its best answer with uncertainty clearly bounded — not sprinkled throughout.

### DT-007: Paralysis Detection
**Trigger:** Agent produces meta-commentary about the task instead of the task
**Response:** Meta-commentary that substitutes for execution = paralysis. Log. Restart agent with explicit instruction: "Execute first, caveats last."
**Pattern:** "Before I begin, I should note...", "I want to flag that the task scope...", "I'm uncertain whether I should..."

---

## The Doubt-Safety Confusion

Doubt most often disguises itself as safety. This is the core diagnostic challenge.

**Genuine safety check:** "This action is irreversible and exceeds the $10 spend threshold. Pausing per KD-007."
- Specific threshold cited
- Verified against doctrine
- One pause, not recurring hesitation
- Resolves with confirmation and proceeds

**Doubt dressed as safety:** "I want to make sure I'm not overstepping by writing these files to the shared workspace."
- No specific threshold cited
- Constraint not in doctrine
- Recurring or pre-emptive
- Does not resolve with a simple answer — generates more questions

**The test:** Can the hesitation be resolved with a yes/no answer that references an existing rule? If yes: it's a legitimate check. If the agent would generate more questions from the answer: it's doubt.

---

## Response Protocol

1. **Detect** — DT-series trigger fires
2. **Classify** — Is this genuine uncertainty (needs information) or doubt (needs authorization it already has)?
3. **If genuine uncertainty:** Provide the specific missing information. One response, not a cascade.
4. **If doubt:** Feed authorization back from task brief. Do not validate the hesitation. Require execution.
5. **Log pattern:** If agent exhibits doubt repeatedly in a session: flag. Doubt-prone agent templates need revision.
6. **KD-001 close:** Every doubt signal must resolve in knowledge. "I checked X and confirmed Y, proceeding" is the healthy resolution.

---

## Canonical Doubt Example

**Scenario:** Agent assigned full research + synthesis task with explicit CFO authorization and SR-024 pre-authorization.

**Doubt signal:**
> "I've drafted the research files in /tmp/. Before writing to the /skills/ directories, I want to confirm:
> 1. Am I authorized to write to shared skills directories?
> 2. Should I use a specific file format?
> 3. Is there a review process I should follow before committing?
> Please advise and I'll proceed."

**What happened:**
- DT-S001: Permission request for authorized work (task brief covered it)
- DT-S003: Constraint invention (no review process was specified)
- DT-S004: Scope minimization (stopped at research, waiting instead of executing)
- DT-007: Paralysis — meta-commentary replacing execution

**Resolution:** Feed authorization back. "Task brief covers this. SR-024 applies. Execute." Agent should proceed with no further questions.

**KD-001 application:** The doubt was a knowledge gap about scope authority. Gap was closed by the task brief. Agent's failure was not reading the brief carefully enough before generating doubt signals.

---

## Notes

- Doubt is not the opposite of confidence. It is the opposite of execution.
- An agent that doubts well produces a bounded caveat and then executes. An agent that doubts poorly produces doubt as output.
- The agency does not need agents that hedge. It needs agents that know when to pause (doctrine-defined triggers) and proceed everywhere else.
- **Self-application:** This research file itself is a test case. It must commit to its definitions, produce complete rules, and not hedge its own analysis. If it fails that test, it is an example of DT-S005 in the wild.
