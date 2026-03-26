# Checkpoint Discipline (Production Doctrine)

**Rule:** `git commit` is free. Use it ruthlessly.

---

## The Pattern

**Before any risky operation:**

```bash
git add -A
git commit -m "Checkpoint: [clear description of state]"
```

**Cost:** ~0.5 seconds  
**Risk reduction:** Exponential  
**Recovery path:** Always available  

---

## When to Checkpoint

- [ ] Before executing external API calls
- [ ] Before token-costing operations (Tier 2+)
- [ ] Before delegation to sub-agents
- [ ] Before any operation you're unsure about
- [ ] Before running unfamiliar code
- [ ] End of every session (nightly commit)
- [ ] During active development (every 30 min)

---

## Why This Matters

**Real incident (2026-03-12 18:00-22:16 UTC):**
- Five token famines in 4 hours
- Each famine: Official agent died mid-execution
- Recovery: Parent agent caught failure, reviewed checkpoint
- Result: No permanent data loss, system recovered

**The Prayer was enabled by checkpoints.**

---

## Checkpoint + Three Branches

**For Automate (Legislative):**
- Checkpoint before policy changes
- Diff shows what policy changed
- Accountability is automatic

**For Official (Executive):**
- Checkpoint before shipping
- Production rollback is one git revert
- Safe deployment guaranteed

**For Daimyo (Judicial):**
- Checkpoint log is audit trail
- Every decision is recoverable
- Cost tracking visible in diffs

---

## Standing Order: Nightly Commits

**Every session ending:**

```bash
git add -A && git commit -m "Session checkpoint: [date] [summary]"
```

**Status:** Automated (cron job)  
**Cost:** $0.00  
**Benefit:** Never lose a day's work  

---

## Related Doctrine

**See Also:**
- The Prayer (token famine resilience)
- Three Branches (accountability via git history)
- Path B Always (diffs show small changes)
- Least Terrible Option (revert if wrong)

**Status:** LOCKED (operational requirement, not optional)
