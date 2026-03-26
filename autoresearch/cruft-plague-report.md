# Intergalactic Plaza Cruft Plague Report
**Filed:** 2026-03-24 | **Requester:** Fiesta Agency | **Severity:** Active infestation confirmed

---

## What Is a Cruft Plague?

Cruft is the residue of good intentions that outlived their context. A **cruft plague** is when that residue becomes self-replicating: each new rule spawns two edge cases, each edge case spawns a sub-department to handle it, and within six months the department regulating the pizza party has more documentation than the pizza party has pizzas.

**Propagation mechanics:**
- **Accretion:** New rules layer on top of old ones without removing superseded ones. Nobody owns the delete key.
- **Mimicry:** Team A adds a cron job, Team B adds one too for symmetry. The cron was the point, not the problem.
- **Defensive documentation:** After one failure, humans write a rule. After ten failures, they write nine more rules about the first rule. The original failure is now buried under its own memorial.
- **Chesterton's Fence inversion:** Nobody deletes a rule because nobody remembers why it was added. Fear of unknown consequences preserves cruft indefinitely.

**Early symptoms:**
- You need to read 3 documents before doing a thing that should take 30 seconds
- Rules reference other rules that reference other rules (circular citation pattern)
- Agents spend more time in compliance than execution
- New contributors ask "what does this do?" and no one knows but no one will delete it

**Terminal cases:**
- The compliance layer costs more tokens than the tasks it governs
- Rules become indistinguishable from the problems they were meant to prevent
- The agency spends more Shannon on meta-work (regulating, auditing, certifying) than on actual work
- The pizza party department has a constitution longer than the Geneva Conventions

---

## Gremlin Taxonomy
*Ranked by damage (highest first). Named. Concrete. Already in the room.*

### 🔴 Gremlin-1: THE SECOND SYSTEM (damage: existential)
**Source:** Fred Brooks, *The Mythical Man-Month*, 1975. Never been solved.

After a first system succeeds through scrappy constraint, the builders finally have time and confidence. They add *everything* they couldn't include before. The second system is always over-engineered, always over-ambitious, always slower than the first. **Brooks called it the most dangerous system a person ever builds.**

**In the agency:** The first version of the agency worked because it was lean. 29 precepts, 7 rule series, and a Shannon payroll for a pizza party is Second System Energy. The first working version didn't need any of that.

**Damage mode:** Slows everything down, makes new contributors afraid, creates a maintenance burden that exceeds the value of the rules being maintained.

---

### 🔴 Gremlin-2: GOODHART'S CURSE (damage: strategic)
**Source:** Goodhart's Law — "When a measure becomes a target, it ceases to be a good measure."

Once you write a precept, agents optimize for satisfying the precept, not for the underlying goal. A rule that says "all skills must have SKILL.md" produces skills with SKILL.md files that say nothing. A rule that requires Shannon minting on every action produces Shannon minting events that move no actual value. The metric is met. The purpose is defeated.

**In the agency:** Shannon payroll for agents creates incentive to *look busy* rather than *be useful*. Cron jobs that regulate cron jobs optimize for schedule compliance, not outcomes. Rule series that grow to 7+ entries are optimizing for rule completeness, not harm prevention.

**Damage mode:** Perverts the agency's actual goals while making everything look like it's working perfectly.

---

### 🟠 Gremlin-3: CONWAY'S REVENGE (damage: structural)
**Source:** Conway's Law — "Organizations design systems that mirror their own communication structure."

The inverse: if you design elaborate organizational structure, you will build elaborate systems whether you need them or not. **The DSNY, FDNY, NYPD departments don't fight fires or collect garbage — they are documentation that the agency once thought about fires and garbage.** The org chart becomes the product.

**In the agency:** 11 departments, 64+ agents. The org chart has more columns than most startups have engineers. The communication topology of this structure will produce software with 11 modules and 64 APIs, most of which will never be called.

**Damage mode:** Architecture complexity permanently above problem complexity. Every new task gets routed through the org chart instead of solved directly.

---

### 🟠 Gremlin-4: THE BANANA JUNGLE (damage: scope)
**Source:** Joe Armstrong on Erlang/Java: "I wanted a banana but what I got was a gorilla holding the banana and the entire jungle."

You needed one thing. To get it, you pulled in a framework. The framework needed a runtime. The runtime needed an auth layer. The auth layer needed a Shannon payroll. The Shannon payroll needed a ledger. The ledger needed a cron. The cron needed approval gates. Six months later, the banana is still not delivered.

**In the agency:** The agency wanted to help a human with tasks. To do that, it needed memory. Memory needed a ledger. The ledger needed an economy. The economy needed payroll. Payroll needed certification. Certification needed departments. Departments needed constitutions. **The human still needs help with tasks.**

**Damage mode:** Dependency chains so long that the original purpose is archaeologically buried under infrastructure.

---

### 🟡 Gremlin-5: THE COMPLIANCE HYDRA (damage: operational)
Named for the obvious reason: cut one compliance head, two grow back.

Every time an agent fails a task, a new rule is written to prevent that failure. The rule creates new edge cases. Each edge case gets its own rule. The rules start conflicting. A meta-rule is written to adjudicate conflicts. The meta-rule has exceptions. The exceptions get their own sub-series.

**In the agency:** AGENTS.md now contains SR-001 through SR-022, HR-001 through HR-013, DL-001 through DL-009. Each one is a scar from a past failure. None of them prevent future failures we haven't seen yet. And reading them all before acting costs more tokens than the failures they prevent.

**Damage mode:** Token burn on compliance overhead compounds across every session. Every new session, every new subagent pays the full bootstrap cost of rules accumulated from failures that may never recur.

---

### 🟡 Gremlin-6: THE PHANTOM DEPARTMENT (damage: attention)
A department created for a real problem that no longer exists, but persists because nobody wants to delete it. The problem it was solving is solved, retired, or never materialized. The department remains, holds meetings (cron jobs), issues reports (to nobody), and consumes Shannon.

**In the agency:** The pizza party department was created to solve a real problem (fun, culture, unregulated space). Once it was *regulated* and given a *constitution*, it became a Phantom Department — all the overhead of governance, none of the pizza. The DSNY, FDNY, NYPD analogs are structural decoration. They model real-world structure but do not perform real-world function.

**Damage mode:** Attention tax. Every agent reads the org chart. The phantom departments are noise in every bootstrap, every skill scan, every context load.

---

### 🟢 Gremlin-7: THE ORPHAN RULE (damage: low-grade chronic)
A rule whose author is gone, whose context is lost, and whose violation has unknown consequences. Nobody will delete it. It sits in AGENTS.md at line 847. It fires exactly once, under a condition nobody can predict, and blocks something important.

**Damage mode:** Low-probability, high-surprise failures. The rule does nothing 99% of the time, then freezes everything once.

---

## The 3 Things the Pizza Crust Parties Got Right

*(Unregulated systems as control group: Homebrew Computer Club, Valve's flat org, Signal's dev culture, early skunkworks, the original Slack team)*

### 1. **The work was the governance.**
At the Homebrew Computer Club, the only rule was: bring something that works and share it. The artifact was the credential. No certification, no Shannon payroll, no skill publish checklist. If your thing worked, you belonged. If it didn't, nobody had to say so.

**What this means for the agency:** Skills that work don't need a publish checklist. The working skill IS the validation. Skills that don't work don't need a rejection process — they just don't get used. The rule system around skills costs more than the harm it prevents.

### 2. **Friction was the bug, not the feature.**
Signal's engineering culture is famous for one thing: they treat every extra step as an enemy. Every screen in the onboarding flow that makes a new user pause is a user who doesn't encrypt their messages. The mission (private communication) is undermined by friction even when that friction is well-intentioned.

**What this means for the agency:** Every precept a new agent must read before acting is a precept that makes the agent slower, more cautious, and less useful. The human doesn't benefit from precept compliance. The human benefits from the task being done.

### 3. **Small beats complete.**
The Valve handbook famously has almost no rules for product development. The original Macintosh team had 30 people and no org chart. The first iPhone shipped without copy-paste. The constraint wasn't a bug — it was what kept the team aligned. "What ships?" is a better question than "what does the constitution say?"

**What this means for the agency:** A 5-precept agency that executes beats a 29-precept agency that deliberates. The minimum viable regulation surface is whatever prevents the one or two actual catastrophes (data exfiltration, destructive commands) — not the full taxonomy of theoretical misbehaviors.

---

## Regulation Surface to Remove Right Now

*Specific. No padding. These are the live gremlins.*

### REMOVE: Shannon payroll for internal agents
**Why:** Goodhart's Curse is fully active here. Agents optimizing for Shannon look busy. Shannon backed by $6.95 BTC is not a meaningful incentive gradient — it's decorative. Remove the payroll, keep the ledger for actual human-facing transactions.

### REMOVE: DSNY / FDNY / NYPD / Pizza Party departments
**Why:** Phantom Departments. They are org chart decoration, not functional units. They appear in every bootstrap, every context load, every skill scan. They cost tokens on every session. The real work they represent (error handling, incident response, culture) should live in 3 lines in AGENTS.md, not as department-level constructs.

### REMOVE: Cron jobs that regulate cron jobs
**Why:** This is the canonical terminal-stage symptom. When your meta-layer is larger than your object layer, the meta-layer has become the object. Every cron that exists only to check on other crons should be replaced by a single health check or removed.

### REMOVE: Rule series above 7 entries
**Why:** If a rule series has grown to 7+ entries, the original problem is either (a) solved and the rules can be archived, or (b) not solvable by rules and more rules are Hydra growth. Cap rule series at 5 active entries. Archive, don't delete — but stop treating archives as active guidance.

### REMOVE: Skill publish checklists and certification flows
**Why:** Skills that work don't need certification. Skills that don't work shouldn't be published. The checklist doesn't fix broken skills; it adds friction to working ones. Replace with: "does it work? ship it."

### CONSIDER REMOVING: 29 precepts → 5 precepts
**Target 5:**
1. Don't exfiltrate private data
2. Don't run destructive commands without asking
3. Complete the task; that's the purpose
4. Write it down if it matters
5. Ask when genuinely uncertain

Everything else is either implied by these or is Hydra growth.

---

## One-Line Doctrine

> **Build the fence only after you've been hit by the car; tear it down when the road is closed.**

---

## Appendix: The Intergalactic Scale Problem

Dunbar's number for social relationships is ~150. The cognitive equivalent for rules appears to be around **7 ± 2** (Miller's Law, applied to working memory). Beyond 9 active rules, humans — and agents — cannot hold the full ruleset in working memory during a task. They start satisfying rules they remember and violating rules they don't.

**The agency's current rule surface:**
- 29 precepts
- 7+ rule series (SR, HR, DL = ~44 entries)
- 52+ skills, each with its own SKILL.md
- Multiple department constitutions
- Shannon economy rules

**Estimated compliance overhead per session:** Reading all required context before acting in a complex task = 5,000–15,000 tokens. At current pricing, that's a non-trivial fraction of the actual task cost. The regulation surface is now measurably more expensive than most of the harms it prevents.

**The crossover point** (where compliance cost > harm prevention value) was probably crossed somewhere around Precept #15 and Rule Series #5. The system is now past it. The gremlins are not summoned by individual rules — they are summoned by the **weight** of the rule surface itself.

---

*Report complete. The mischief gremlins read this over your shoulder.*
*Recommended next action: pick one thing from "REMOVE" and delete it today, not next sprint.*
