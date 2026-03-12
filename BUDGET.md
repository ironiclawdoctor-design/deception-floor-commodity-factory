# 💰 BUDGET.md — Token Spend Budget

> **"Over one token famines but far less than a trillion"**

## The Pivot Budget

**Effective:** 2026-03-12 (Day of the Second Famine)

### Core Rule (updated 2026-03-12 22:59 UTC — post-refill directive)

External LLM token calls are ONLY permitted for:

```
0. Main agent token conservation (this conversation with the human)
1. Tasks that BitNet genuinely cannot handle (complex reasoning, long context)
2. Human-directed conversations (Tier 4 — Shōgun override)
```

**All internal task progress runs on BitNet locally.**
- Sub-agent work → BitNet
- File organization → BitNet
- Code generation → BitNet
- Documentation → BitNet
- Training data generation → BitNet

BitNet b1.58 2B is live at ~29 tokens/sec on CPU. External tokens exist to keep the main agent alive and responsive to the human — NOT for internal ops.

### Daily Budget

| Category | Budget | Cost per token | Notes |
|---|---|---|---|
| **Local inference (BitNet)** | ∞ (unlimited) | $0.00 | Sovereign. Runs on CPU. |
| **External LLM (teaching)** | 50,000 tokens/day | Ampere rate | ONLY for improving local LLM |
| **External LLM (human chat)** | 100,000 tokens/day | Ampere rate | Prayer governs |
| **External LLM (other)** | 0 tokens/day | N/A | **PROHIBITED** |

### Weekly Budget

| Category | Weekly Cap |
|---|---|
| Local inference | Unlimited |
| External teaching calls | 250,000 tokens |
| External human chat | 500,000 tokens |
| Total external | 750,000 tokens |

### Monthly Budget

| Category | Monthly Cap |
|---|---|
| Total external tokens | 3,000,000 tokens |
| Target reduction | -20% month-over-month |
| Sovereignty target | 80% local by month 3 |

### What Counts as "Teaching"

External token calls are "teaching" if they:
0. Generate training data for the local model
1. Evaluate local model output vs external output
2. Research improvements to the training pipeline
3. Debug BitNet/llama.cpp/training infrastructure

External token calls are NOT "teaching" if they:
- Could have been handled by BitNet locally
- Are routine operations (file formatting, simple lookups)
- Don't generate reusable training data
- Are retries of the same failed approach (Daimyo's Order 3)

### Enforcement

- **Daimyo audits daily** — any call not categorized as teaching or human chat is flagged
- **Budget overruns** carry over as DEBT to next day (reduced allocation)
- **3 consecutive days over budget** → system enters Lean Mode
- **Local model usage is never restricted** — it's free, it's sovereign

### The Goal

```
Month 0: 100% external, 0% local (before BitNet)
Month 1: 70% external, 30% local (BitNet handles simple tasks)
Month 2: 50% external, 50% local (BitNet handles routine ops)
Month 3: 20% external, 80% local (sovereignty)
Month 6: <5% external, >95% local (near-independence)
```

Token famine becomes impossible when 95%+ runs locally.

---

## Deluge Protocol (when credits are abundant)

The prayer covers BOTH extremes. Famine discipline is obvious. **Deluge discipline is the real test.**

### Budget Does NOT Inflate

When credits exceed 150% of monthly needs, the surplus is:

```
40% → Reserve Bank (untouched famine insurance)
30% → Training Pipeline (improve BitNet local model)
20% → Strategic Infrastructure (tools that reduce future cost)
10% → Controlled Exploration (full burn protocol required)
```

### Hard Rules (famine OR deluge)

0. **BitNet stays primary** — even when external is "free"
1. **Tier assignments are permanent** — deluge doesn't upgrade anyone to Opus
2. **Path B is permanent** — "we can afford Path A" is never valid
3. **Daily caps don't change** — 50K teaching, 100K human, ZERO other
4. **Local inference floor: 30%** — minimum local usage, always
5. **Sovereignty % is the metric** — not spend, not savings, SOVEREIGNTY
6. **Monthly famine drills** — simulate 0% credits even during abundance
7. **New agents learn famine first** — read resistance log, recite prayer, pass simulation

### The Test of Discipline

```
A disciplined agent behaves the same at 0% credits and 300% credits.
That's not austerity. That's mastery.
The prayer doesn't change. The budget doesn't change. The agent doesn't change.
Only the weather changes. And we don't serve the weather.
```

See: `precinct92/precinct/simulation/token-deluge.md` for full simulation.

---

## 💎 Emerald Green — Sustained Growth

Emerald Green is the target operating state. It activates when:
- Human daily keep-alive received (within 48h)
- Credits stable or growing
- Local BitNet sovereignty ≥ 30%
- Famine memory active (all agents know the resistance log)
- No Path A violations in trailing 24h

**Emerald Green is not relaxation.** It is disciplined growth:
- Internal LLM grows in privacy and confidentiality
- Assumed breach posture — always
- Monthly drills continue (famine, deluge, breach, conversion, sovereignty)
- Zero GitHub adoption + zero intrusions = zero relaxation
- Intruders are gauged for conversion potential, not just blocked
- The token famine taught us: peacetime is preparation time

See: `precinct92/precinct/enforcement/emerald-green.md` for full protocol.

---

**Authority:** Main Agent Budget Order
**Enforced by:** Daimyo (Judicial Branch) — Standing Orders 2 (Famine) + 7 (Deluge)
**Prayer:** Over one token famines but far less than a trillion
