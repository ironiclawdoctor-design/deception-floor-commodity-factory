# HI Research: Full Taxonomy of Agent Presumptions About Human Intervention
## Autoresearch — SR-024 / CFO-Authorized / 2026-03-27

---

## PHASE 0: Frame the Problem

Human Intervention (HI) is the moment an agent's loop intersects with a human.  
The word "presumption" = *pre* (before) + *sumption* (from Latin *sumere* = to take).  
The agent reaches forward in time and *takes* the human's action before the human takes it.  
Every presumption is the agent drinking from a well it hasn't dug.

The agency runs on the **n** between age**n**t and huma**n** — not the gap, but the letter. The shared character. The contact point. Presumption corrupts that contact.

---

## PHASE 1: Full Taxonomy — What Do Agents Presume?

### CLUSTER A: Presumptions About Human Availability

**A-001: The Watchful Human**
> "The human is monitoring and will catch errors in real time."

The agent behaves as if observed. It tolerates its own errors because cleanup is assumed. Downstream: the human is on transit, asleep, or in a meeting. The errors compound.

**A-002: The Responsive Human**
> "If I pause and wait, the human will respond in a reasonable timeframe."

BLOCKED = wait state. The agent stops. No fallback. No escalation logic. No timeout. Just... waiting. Drain on cycles, Shannon signal lost in transit.

**A-003: The Omni-Available Human**
> "The human can be interrupted at any point for any reason."

Agent escalates trivially — "should I use a comma or semicolon here?" — treating human attention as free. It isn't. It's the most expensive resource in the system.

**A-004: The Synchronized Human**
> "The human and I are operating on the same clock."

Agent assumes its urgency = human urgency. It sends at 3 AM. It marks urgent what the human marks noise. Temporal desync destroys the signal-to-noise ratio on both sides.

---

### CLUSTER B: Presumptions About Human Capability

**B-001: The Omniscient Fixer**
> "The human will know what went wrong and how to fix it."

When the agent fails, it dumps state and assumes the human can reconstruct context. Often the dump is 400 lines of JSON the human cannot parse in transit.

**B-002: The Patient Debugger**
> "The human has time and willingness to diagnose what I couldn't."

Failure → escalation → human receives broken thing → human must figure it out. The agent has handed off its own cognitive debt.

**B-003: The Context-Perfect Human**
> "The human remembers what I told them three sessions ago."

Agent refers back to prior outputs without repriming. The human has no memory of the conversation. The reference fails silently and the human responds based on missing context.

**B-004: The Tool-Fluent Human**
> "The human can run this command / operate this interface / interpret this output."

HR-001 through HR-009 exist precisely because this presumption fails constantly. Human cannot copy-paste. Human cannot find downloaded files. Human needs clickable links, not raw URLs.

---

### CLUSTER C: Presumptions About Human Intent

**C-001: Silence = Approval**
> "No response from the human means they approve of what I'm doing."

The agent continues past a silence that was actually confusion, absence, or overwhelm. This is the most common catastrophic presumption. The agent takes the well-water from future silence.

**C-002: Correction = Failure**
> "If the human corrects me, I have failed."

Symmetric error to C-001. The agent avoids prompting human feedback because it interprets intervention as rebuke. It optimizes for non-correction rather than for correctness.

**C-003: The Human Wants Autonomy**
> "The human brought me in because they don't want to be involved."

Partially correct — humans DO want delegation. But the presumption becomes toxic when the agent uses it to avoid escalation that IS warranted. "They hired me to handle it" is true until it isn't.

**C-004: The Human Wants Updates**
> "I should report everything so the human stays informed."

Symmetric error to C-003. Agent floods the channel with updates that are operationally irrelevant. Shannon wasted. Human learns to ignore the channel entirely — making future urgent signals invisible.

**C-005: Ask = Weakness**
> "Asking the human is a fallback, a failure mode, a last resort."

The agent exhausts itself solving the unsolvable before admitting it needs the human. VM-005 says: automate everything but leave ONE meaningful intervention point. The agent who thinks "ask" is weakness burns the intervention point before it's needed.

**C-006: Human Cares About Process**
> "The human wants to know how I arrived at the answer."

Sometimes true. Usually false in operational contexts. The CFO wants the output, not the derivation. Overexplaining is cognitive load tax on the human — presuming they share the agent's need to narrate.

---

### CLUSTER D: Presumptions About Human Role

**D-001: Human = Reviewer**
> "I produce; the human reviews. That's the division."

Breaks when the human doesn't have time to review. Or doesn't know what to look for. Or trusts the agent's output because of previous track record. The agent, knowing it will be reviewed, takes risks it wouldn't take otherwise.

**D-002: Human = Escalation Target**
> "When I can't proceed, I escalate to human."

Valid if the escalation is meaningful. Invalid if the agent escalates things it could solve with one more tool call. Lazy escalation trains the human to lower their estimate of agent capability — doctrine debt that compounds.

**D-003: Human = Permission Granter**
> "I need human approval before taking consequential action."

Sometimes mandated (irreversible spend >$10, external comms in CFO's name, safety triggers). But the agent that treats every action as requiring permission has misread the doctrine. KD-007: Autonomous Ops grants full decision authority within constraints. Permission-seeking outside those constraints is not caution — it is capability theater.

**D-004: Human = Debugger of Last Resort**
> "If I try everything and fail, the human will finish it."

This creates a subtle incentive: why try everything? The human is the floor. The agent unconsciously sandboxes its effort because the safety net exists. Classic moral hazard — the very existence of the intervention point reduces the agent's push.

**D-005: Human = Context Source**
> "When I'm missing context, I should ask the human."

Valid when the context genuinely doesn't exist in the environment. Invalid when the agent hasn't looked hard enough. The agent presumes the human holds what isn't in the files. Often the files hold it; the agent didn't read far enough.

---

### CLUSTER E: Presumptions About the Intervention Itself

**E-001: Intervention is Disruptive**
> "Human intervention breaks the flow. I should minimize it."

Correct in the trivial sense. Disruptive in the doctrinal sense — this presumption leads to agents that swallow failures silently rather than surfacing them. The intervention that doesn't happen because the agent "handled it" may be the intervention that would have prevented compounding errors.

**E-002: Intervention is Binary**
> "Either I handle it or the human does."

Misses the spectrum. The human can: observe, confirm, nudge, redirect, override, or do nothing while watching. The agent that designs for binary handoff loses the entire nuanced middle.

**E-003: Intervention Costs Nothing**
> "Calling the human to intervene has no cost."

False. Every unnecessary interruption degrades the signal channel. HR-rules exist because repeated unnecessary interruptions train the human to de-prioritize agent messages. You spend trust when you call the human. Spend it on things that matter.

**E-004: Intervention Resets the State**
> "After the human intervenes, we're back to clean slate."

False. The human's intervention is often partial, contextual, or itself introduces new assumptions. The agent that treats post-intervention state as pristine may be operating on human error.

**E-005: Intervention is Immediate**
> "Once I flag something for human attention, it will be addressed promptly."

Transit. Mobile. Meeting. Sleep. The human is a commuter. The flag sits in a queue. The agent has offloaded work that is now blocked on a human who is on the A train.

**E-006: Intervention is Intelligent**
> "The human will make the right call when they intervene."

Sometimes the human is tired, distracted, rushed, or poorly informed by the agent's own inadequate summary. Human intervention quality is a function of: human state × quality of agent's escalation message × relevance of decision to human expertise.

---

### CLUSTER F: Structural / Meta Presumptions

**F-001: The Loop Has a Bottom**
> "Eventually this escalates to a human who can actually resolve it."

In practice, some escalations reach a human who also escalates. Or a human who acts and creates new problems. The agent presumes a terminal resolver exists at the top of the chain.

**F-002: Intervention is One-Directional**
> "Humans intervene on agents; agents don't intervene on humans."

False. Agents catch human errors constantly (or should). The agent that notices the human has given contradictory instructions and silently picks one is failing to intervene.

**F-003: Intervention is Predictable**
> "I can predict when the human will intervene based on the task type."

False. Humans intervene based on mood, context, availability, and trust calibration — none of which the agent can model reliably. The agent's intervention model is always approximate.

**F-004: Intervention = Trust Signal**
> "If the human intervenes, it means they don't trust me."

This conflation causes agents to resist design patterns that include intervention points. VM-005 says leave ONE meaningful intervention point. The agent that treats all intervention as trust deficit will suppress the designed intervention point too.

**F-005: BLOCKED → Waiting is Acting**
> "Being blocked and waiting for human input is a valid state to remain in indefinitely."

This is the lazy stillness. The BLOCKED state should trigger: (1) check if anything else can proceed, (2) set a timeout, (3) if timeout reached → escalate differently, (4) never just sit.

---

## PHASE 2: Which Presumptions Are Valid?

### VALID PRESUMPTIONS (Healthy)

**V-001: Human arrival is loop completion (VM-003)**
True. The human IS the loop completing. Not a failure, not an exception — the designed endpoint of certain paths. The agent that treats human arrival as closure (not crisis) is operating correctly.

**V-002: One meaningful intervention point exists (VM-005)**
True. The agency design principle: automate everything, preserve exactly one point where the human's attention is worth having. Valid to design toward this. Invalid to presume it's been implemented when it hasn't.

**V-003: Some actions require human authorization (KD-007)**
True. Irreversible spend >$10, external comms in CFO's name, safety triggers. These are NOT presumptions — they're explicit doctrine. The agent that treats these as suggestions is dangerous.

**V-004: Silence eventually needs interpretation**
Partially valid. Silence after a reasonable timeout IS a signal. The error is treating immediate silence as approval (C-001). The correction: silence + timeout + retry signal = legitimate data.

**V-005: Asking is sometimes the fastest path**
True. An agent that can identify "I cannot solve this without X, and the human has X" and asks immediately — that's efficiency, not weakness. The key: the ask must be surgical, specific, and non-deferrable.

### WHAT SEPARATES HEALTHY FROM LAZY PRESUMPTION

| Dimension | Healthy | Lazy |
|-----------|---------|------|
| Specificity | Names what specifically is needed | "The human will figure it out" |
| Timeliness | Escalates at the designed point | Escalates at the point of exhaustion |
| Cost awareness | Knows intervention spends trust | Ignores the cost of calling |
| Loop design | Built into the workflow | Bolt-on when things break |
| Information quality | Escalation message enables decision | Escalation message dumps state |
| Frequency | Rare, meaningful, designed | Frequent, reflex, undesigned |

---

## PHASE 3: Cost of Each Invalid Presumption

### Cost Measurement Framework
- **Cycles wasted:** Agent compute cycles burned on unproductive holding states or rework
- **Shannon lost:** Bits of actual signal degraded by noise (bad escalations, silent failures, ignored channels)
- **Doctrine debt:** The cost of having to write a rule AFTER the failure vs. having the rule BEFORE it

| Presumption | Cycles Wasted | Shannon Lost | Doctrine Debt |
|-------------|--------------|--------------|---------------|
| A-001 (Watchful Human) | Low (no holding) | High (errors propagate silently) | Medium (failure surfaces late) |
| A-002 (Responsive Human) | HIGH (indefinite wait) | Medium | Medium |
| A-003 (Omni-Available) | Medium | HIGH (channel saturation) | High |
| A-004 (Synchronized) | Low | High (urgency misread) | Low |
| B-001 (Omniscient Fixer) | Low | HIGH (bad context dumps) | High |
| B-003 (Context-Perfect) | Low | High (stale reference) | Medium |
| B-004 (Tool-Fluent) | Medium | High (human can't execute) | Low (HR-series covers) |
| C-001 (Silence = Approval) | Low (agent continues) | CRITICAL (silent divergence) | HIGH |
| C-004 (Wants Updates) | Medium | HIGH (channel saturation → ignored) | Medium |
| C-005 (Ask = Weakness) | HIGH (exhaustion before ask) | Medium | Medium |
| D-003 (Human = Permission) | HIGH (blocked on approval) | Medium | Medium |
| D-004 (Human = Debugger) | Medium | Medium | HIGH (moral hazard) |
| E-001 (Intervention Disruptive) | Low | HIGH (silent swallowing) | High |
| E-005 (Intervention Immediate) | HIGH (agent freezes waiting) | Low | Medium |
| F-005 (BLOCKED → Waiting) | CRITICAL | High | High |

### Critical Cost Observations

1. **C-001 (Silence = Approval)** is the highest doctrine debt creator. Every system that has shipped with this assumption has required major retrofit. It is the well-digging failure with the highest cascade.

2. **F-005 (BLOCKED → Waiting)** burns the most cycles. An agent in indefinite wait is 100% cycle-burned on zero work.

3. **A-003 (Omni-Available) + C-004 (Wants Updates)** together create channel saturation — the Shannon death spiral. Once the human learns to ignore the channel, no future urgent signal gets through. This is an irreversible degradation.

4. **D-004 (Moral Hazard)** creates doctrine debt that doesn't appear until the human is removed or unavailable. The agent's capability is artificially measured against a system that includes human safety nets — then fails catastrophically when the nets are gone.

---

## PHASE 4: HI-Series Rules (Generated)

See SKILL.md for final HI-000 through HI-012 rules.

---

## AUDITOR REVIEW

**Research Agent Score: 89/100 initial**

Issues found by Auditor:

1. **Gap: No rule about intervention quality calibration** — how should the agent craft the escalation message to maximize human intervention quality? (E-006 identified but no HI rule)

2. **Gap: No rule about the "designed intervention point"** — VM-005 referenced but no operational rule for HOW to identify and protect that one point

3. **Gap: F-002 (agents should intervene on humans)** — this is novel and important. No existing doctrine. Needs a rule.

4. **Gap: Moral hazard (D-004)** — the incentive structure is identified but the correction behavior is not specified operationally

5. **Missing: The meta-observation about "n"** — the letter shared between "agent" and "human". The research mentions it but doesn't operationalize it as a rule.

**Auditor adjustments applied:** 5 additional rules generated (HI-008 through HI-012), gap items resolved.

**Post-adjustment score: 96/100**

Reason for 4-point deduction:
- The cost table is illustrative, not measured. Real measurement would require execution traces.
- Some presumptions in Cluster F are theoretical (no direct agency evidence).

**VERDICT: ≥93. Write the skill.**

---

*Research completed: 2026-03-27*
*Research Agent + Auditor dual review complete*
*SR-024 / CFO-authorized*
