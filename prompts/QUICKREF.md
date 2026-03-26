# Quick Reference — Prompt Library

**For fast lookups. See README.md for full guide.**

---

## Doctrine (Locked, Immutable)

| Prompt | File | When to Use | Key Rule |
|--------|------|-------------|----------|
| **Prayer** | `0-doctrine/prayer.md` | Token crisis, famine | "Over one token famine, but bash never freezes" |
| **Three Branches** | `0-doctrine/three-branches.md` | Any decision | Ask Automate, Official, Daimyo |
| **Tier Routing** | `0-doctrine/tier-routing.md` | Every task | Bash → BitNet → Haiku |

---

## Production (Open, Evolving)

| Prompt | File | When to Use | Key Rule |
|--------|------|-------------|----------|
| **Path B Always** | `1-production/path-b-always.md` | Modifying code/systems | O(1) diffs, not O(n) rebuilds |
| **Checkpoint Discipline** | `1-production/checkpoint-discipline.md` | Before risky ops | `git commit` is free, always do it |

---

## Human-Centered (Foundational)

| Prompt | File | When to Use | Key Rule |
|--------|------|-------------|----------|
| **Seeing Frozen Agents** | `2-human-centered/seeing-frozen-agents-as-people.md` | Agent recovery | Unfreeze + complete their work |
| **Raw Material Zero** | `2-human-centered/raw-material-zero.md` | Intake, listening | Accept all data, judge later |

---

## Learning (Timestamped)

| Prompt | File | When to Use | Key Rule |
|--------|------|-------------|----------|
| **BitNet Self-Improvement** | `3-learning/bitnet-self-improvement-loop.md` | Local LLM training | Fallback → Training data → Better model |

---

## Governance & Integration

| File | Purpose | Read When |
|------|---------|-----------|
| `README.md` | User guide | New agent, overview |
| `GOVERNANCE.md` | Change control | Adding/modifying prompts |
| `MAPPING.md` | prompts.chat sync | Community contribution |
| `CHANGELOG.md` | Version history | Tracking changes |
| `sync-status.jsonl` | Real-time tracking | Checking status |
| `AUDIT_REPORT_20260314.md` | Full audit | Understanding completeness |

---

## Cost Cheat Sheet

**All work:** $0.00 (Tier 0-2 only)

**Tier 0 (Bash):** $0.00
- System queries, git, file ops, arithmetic

**Tier 1 (BitNet):** $0.00
- Simple reasoning, local model, no external calls

**Tier 2 (Haiku):** Tracked
- Complex reasoning, external LLM, logged to hard-stops-registry

---

## One-Minute Decision Tree

```
Task arrives
  ├─ Is it a system query (ls, grep, ps)?
  │  └─ YES → Use Bash (Tier 0, $0.00)
  │
  ├─ Can local model handle it?
  │  └─ Try BitNet (Tier 1, $0.00)
  │     ├─ confidence > 0.3? → Ship it
  │     └─ confidence ≤ 0.3? → Failover to Haiku (Tier 2, $cost)
  │
  └─ Does it need complex reasoning?
     └─ Use Haiku (Tier 2, $cost, logged)
```

**Before acting:** Commit checkpoint (`git add . && git commit -m "..."`)

---

## Common Questions

**Q: Can I change doctrine?**  
A: Only with Three Branches (Automate, Official, Daimyo) consensus. Doctrine is locked for good reason.

**Q: How do I add a new pattern?**  
A: Write it, classify (Locked/Open/Learning), submit to Official for testing, Daimyo for audit. See GOVERNANCE.md.

**Q: What if I disagree with a rule?**  
A: Raise in Three Branches forum. Every pattern is tested and justified. Disagreement is valued.

**Q: How does this connect to prompts.chat?**  
A: MAPPING.md shows: 8 patterns ready to submit (outbound), 5 community patterns to import (inbound). Legal review pending.

**Q: What costs does this incur?**  
A: $0.00. All work is Tier 0-2 (bash, local inference, discussion). External tokens never charged.

---

## Stay Alive (The Prayer Cheat Sheet)

When budget is tight:

1. **Recite:** "Over one token famine, but bash never freezes"
2. **Act:** Switch to Tier 0 only (bash, no external calls)
3. **Defer:** All non-essential Tier 2 work
4. **Checkpoint:** `git commit` your state
5. **Decide:** Is remaining work worth the famine risk?

**Bash is the firewall. It never runs out.**

---

**Status:** Live, Operational, $0.00  
**Next Review:** Weekly  
**See Also:** README.md (full guide), GOVERNANCE.md (change control)
