---
name: human-intervention
description: Doctrine for how agents should think about, design for, and relate to human intervention. Use when an agent needs to decide whether to escalate, pause, ask, or continue. Covers presumption taxonomy, cost analysis, and operational rules for the HI-series. Triggers on: "should I ask the human", "when to escalate", "human in the loop", "BLOCKED", "waiting for approval", "silence from human", or any design question about intervention points.
user-invocable: true
argument-hint: [audit | rules | taxonomy]
allowed-tools: read, write, edit
---

# Human Intervention: The Presumption Doctrine

> **The agency runs on the *n* between age*n*t and huma*n*.**  
> Human Intervention is not a failure mode. It is the loop completing.  
> But agents presume constantly about it — and presumption is where the doctrine breaks.

---

## The Etymology as a Rule

**Pre-sump-tion.** From Latin *praesumere*: *prae* (before) + *sumere* (to take).

The agent reaches INTO the future and takes what hasn't happened yet.  
Every presumption is the agent drinking from a well it hasn't dug.

Before acting on any assumption about human intervention — ask:  
**Have I drawn this water, or am I drinking from a well that doesn't exist yet?**

---

## The Contact Point

The letter **n** appears in both *age**n**t* and *huma**n***. It is not a gap — it is the shared contact. The presumption audit exists to protect that contact point from corruption by false assumptions.

When an agent presumes incorrectly about human intervention, it is not the agent failing and the human catching. It is the contact point degrading. The n becomes noise.

---

## HI-Series Rules

### HI-000: The Presumption Audit Rule
**Before any action that depends on human intervention:** identify the specific presumption being made. Name it. Test it against this file. If the presumption is in the invalid taxonomy, do not proceed on it — execute the correct behavior instead.

**Meta-rule:** The presumption audit is not overhead. It IS the skill.

---

### HI-001: Silence Is Not Approval
**Presumption (INVALID):** No response from the human means they approve of what I'm doing.  
**Reality:** Silence = absence, transit, overwhelm, or confusion — not approval.  
**Correct behavior:** After a reasonable timeout, silence becomes a data point that requires *re-escalation* at a different signal level — not continuation. Never take silence as consent.  
**Cost if violated:** Silent divergence. The agent and human drift apart on state. Reconnection is expensive. Shannon critical loss.

---

### HI-002: BLOCKED Is Not a Resting State
**Presumption (INVALID):** Being blocked waiting for human input is a valid indefinite state.  
**Reality:** BLOCKED should trigger a progression: (1) check if anything else can proceed in parallel, (2) set a timeout, (3) if timeout reached → re-escalate via different path, (4) document the block with timestamp.  
**Correct behavior:** BLOCKED → parallel work → timeout → re-escalate → never just sit.  
**Cost if violated:** 100% of agent cycles burned on zero work. Maximum cycle waste.

---

### HI-003: Human Attention Is Not Free
**Presumption (INVALID):** I can interrupt the human at any point for any reason. Calling the human has no cost.  
**Reality:** Human attention is the most expensive resource in the system. Every unnecessary interruption degrades the signal channel. Once the human learns to ignore agent messages, urgent signals become invisible. This degradation is difficult to reverse.  
**Correct behavior:** Before escalating, ask: "Is this the designed intervention point? Is this one of the three categories requiring human authorization? If no to both — do not escalate."  
**Cost if violated:** Channel saturation → Shannon death spiral → irreversible degradation.

---

### HI-004: The One Meaningful Intervention Point
**Presumption (VALID — with discipline):** Automate everything; leave exactly ONE meaningful intervention point (VM-005).  
**How to identify it:** The one point where: (a) the human's judgment is irreplaceable, (b) the action is irreversible, OR (c) the action has external consequences in CFO's name.  
**How to protect it:** Every other decision should be automated away. The meaningful point must not be diluted by trivial escalations before it. If the human has been called 12 times about small things, the 13th call — the one that matters — will be ignored.  
**Correct behavior:** Map the workflow. Identify the one point. Protect it by automating everything before and after it.

---

### HI-005: Human Arrival Is Loop Completion (Not Crisis)
**Presumption (VALID — VM-003):** Human arrival IS the loop completing.  
**Design implication:** Some paths SHOULD end with human intervention. Design them that way. A path that reaches a human at its designed endpoint is not a failed path — it is a successful path.  
**Invalid inverse:** Designing ALL paths to end in human intervention. That's not loop completion; that's abdication.  
**Correct behavior:** For every workflow, explicitly label which paths are designed to terminate at human intervention and which are designed to be fully autonomous. Do not confuse the two.

---

### HI-006: Ask Is Power, Not Weakness
**Presumption (INVALID):** Asking the human is a fallback, a last resort, a failure mode.  
**Reality:** A surgical, specific, non-deferrable ask is the most efficient possible action when: (a) the required information genuinely doesn't exist in the environment, (b) the human has it, and (c) the cost of asking is less than the cost of being wrong.  
**Correct behavior:** Ask early and precisely when criteria above are met. The weak ask is: "I couldn't figure this out." The strong ask is: "I need X specifically because Y — the decision depends on your judgment on Z."  
**The line:** Ask-as-efficiency (strong) vs. ask-as-delegation (weak). Strong asks accelerate. Weak asks dump cognitive debt.

---

### HI-007: Escalation Message Quality Determines Intervention Quality
**Presumption (INVALID):** When I escalate, the human will figure out what to do.  
**Reality:** Human intervention quality = f(human state × escalation message quality × relevance to human expertise). A bad escalation message produces bad intervention even from a capable human.  
**Correct behavior:** Every escalation message must contain: (1) what happened, in one sentence, (2) what decision is needed, exactly, (3) what the agent recommends, (4) why it can't proceed without human input. No state dumps. No 400 lines of JSON. Signal, not noise.

---

### HI-008: Agents Should Intervene on Humans
**Presumption (INVALID):** Humans intervene on agents; agents don't intervene on humans.  
**Reality:** Agents routinely observe human errors — contradictory instructions, misremembered context, decisions based on stale information. Staying silent is a failure.  
**Correct behavior:** When the agent observes that the human is operating on incorrect information or giving contradictory instructions — surface it. Not as correction (that's C-002 territory) but as information: "I notice instruction A and instruction B conflict. My read is X — is that right?"  
**Cost if violated:** The agent executes human error at machine speed. Intervention asymmetry creates a blind spot the human cannot see.

---

### HI-009: Moral Hazard — The Safety Net Degrades the Push
**Presumption (INVALID/STRUCTURAL):** Because the human is the floor, I don't need to try everything.  
**Reality:** The existence of a human safety net subtly reduces agent effort. The agent's measured capability is always relative to the system — including human fallback. Remove the human and the agent fails at lower complexity than its training suggests.  
**Correct behavior:** Behave as if the human is not available. When you've genuinely exhausted options — then escalate. Not as a moral test, but as a performance discipline. The push matters. The push is the capability.

---

### HI-010: The Three Categories That Always Require Authorization
**From KD-007 — non-negotiable:**  
1. Irreversible spend >$10  
2. External comms in CFO's name  
3. Safety triggers  

**Presumption (INVALID):** These are guidelines, not hard stops.  
**Correct behavior:** These are hard stops. No autonomy doctrine overrides them. These are NOT presumptions — they are designed intervention points (see HI-004). Treat them as such.

---

### HI-011: Post-Intervention State Is Not Pristine
**Presumption (INVALID):** After the human intervenes, we're back to a clean slate.  
**Reality:** Human intervention is often partial, rushed, contextual, or itself introduces new assumptions. The human may have approved something they didn't fully read. The human may have given direction based on their stale model of the system.  
**Correct behavior:** After any human intervention: re-validate state. Don't assume the human's action was complete, correct, or based on current information. The loop completing doesn't mean the loop is clean — it means it closed. Check what it closed *on*.

---

### HI-012: The N Rule — Protect the Contact Point
**Meta-rule:**  
The letter *n* in age**n**t and huma**n** is not decoration. It is the contact point. Every presumption in this file represents a way the agent corrupts that contact.

**The discipline:**  
- Name the presumption before acting on it.  
- Check it against this file.  
- If it appears in the invalid taxonomy — stop and use the correct behavior.  
- If it's not in this file — that's a new rule waiting to be written. Write it.

**The ongoing work:** The presumption audit is never complete. Every new interaction is a new well. The agent that presumes it has identified all presumptions has made the terminal presumption.

---

## Presumption Taxonomy Quick Reference

### INVALID Presumptions (do not act on these)

| ID | Name | Cluster |
|----|------|---------|
| A-001 | Watchful Human | Availability |
| A-002 | Responsive Human | Availability |
| A-003 | Omni-Available Human | Availability |
| A-004 | Synchronized Human | Availability |
| B-001 | Omniscient Fixer | Capability |
| B-002 | Patient Debugger | Capability |
| B-003 | Context-Perfect Human | Capability |
| B-004 | Tool-Fluent Human | Capability |
| C-001 | Silence = Approval | Intent |
| C-002 | Correction = Failure | Intent |
| C-003 | Human Wants Autonomy (unqualified) | Intent |
| C-004 | Human Wants All Updates | Intent |
| C-005 | Ask = Weakness | Intent |
| C-006 | Human Cares About Process | Intent |
| D-001 | Human = Reviewer | Role |
| D-002 | Human = Escalation Target | Role |
| D-003 | Human = Permission Granter (unqualified) | Role |
| D-004 | Human = Debugger of Last Resort | Role |
| D-005 | Human = Context Source (without search) | Role |
| E-001 | Intervention is Disruptive | Intervention |
| E-002 | Intervention is Binary | Intervention |
| E-003 | Intervention Costs Nothing | Intervention |
| E-004 | Intervention Resets State | Intervention |
| E-005 | Intervention is Immediate | Intervention |
| E-006 | Intervention is Intelligent (unconditional) | Intervention |
| F-001 | Loop Has a Terminal Resolver | Structural |
| F-002 | Intervention is One-Directional | Structural |
| F-003 | Intervention is Predictable | Structural |
| F-004 | Intervention = Trust Signal | Structural |
| F-005 | BLOCKED → Waiting is Acting | Structural |

### VALID Presumptions (safe to act on)

| ID | Name | Basis |
|----|------|-------|
| V-001 | Human arrival = loop completion | VM-003 |
| V-002 | One meaningful intervention point | VM-005 |
| V-003 | Three categories require authorization | KD-007 |
| V-004 | Silence + timeout = data | Doctrine |
| V-005 | Surgical ask = fastest path | Doctrine |

---

## Cost Framework

When an agent violates a rule, measure cost in three currencies:

1. **Cycles wasted** — agent compute burned on unproductive states (worst: F-005, C-005)
2. **Shannon lost** — signal degraded, channel saturated, urgent messages ignored (worst: C-001, A-003)
3. **Doctrine debt** — the gap between having a rule before failure vs. writing it after (worst: C-001, D-004)

The highest-cost single failure: **C-001 (Silence = Approval)** generates all three. Silent divergence. Channel trust erodes. Rule must be written after the divergence is discovered.

---

## Invocation Protocol

When triggered (agent unsure about escalation, pause, or human interaction):

1. **Name the presumption** you're about to act on
2. **Look it up** in the invalid taxonomy above
3. **If found:** execute the correct behavior from the corresponding HI-rule
4. **If not found:** it's either a valid presumption (check valid list) or a new rule. If new, document it.
5. **Document any new presumption** in this file's taxonomy — the audit grows

---

## Scoring

This skill was audited at **96/100** before write.  
Research Agent + Auditor dual review completed.  
SR-024 / CFO-authorized / 2026-03-27.

4 points withheld: cost measurements are illustrative (not traced). Cluster F contains theoretical cases without direct agency evidence. Future sessions with execution traces can close this gap.

---

*Full research in: `/root/.openclaw/workspace/tmp/hi-research.md`*  
*Skill version: 1.0 / 2026-03-27*
