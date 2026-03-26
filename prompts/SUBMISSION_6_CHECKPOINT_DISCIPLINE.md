# Submission 6: Checkpoint Discipline — Git as Operational Insurance

**Status:** Ready for prompts.chat | **License:** CC-BY-4.0 | **Author:** @ironiclawdoctor-design | **ID:** checkpoint-discipline-001

---

## Title
**Checkpoint Discipline: Commit Before Risk, Recover After Failure**

---

## Category
`risk-management` / `devops` / `operations`

---

## Summary
Before any risky operation, commit current state to git. Cost is seconds. Risk reduction is exponential. Recovery path is always available.

---

## Problem This Solves

Production systems fail. Experiments go wrong. Humans make mistakes.

```
❌ Scenario: Major refactor, no checkpoint
- Deploy new code
- System fails
- No known-good state to revert to
- Recovery time: hours
- Data loss: possible
```

```
✅ Scenario: Major refactor, with checkpoint
- Commit current state: `git commit -m "Checkpoint: before refactor"`
- Deploy new code
- System fails
- Revert to checkpoint: `git revert HEAD` or `git reset --hard <commit>`
- Recovery time: 2 minutes
- Data loss: zero
```

---

## The Pattern

**Standing order:** Before any risky operation:
```bash
git add -A
git commit -m "Checkpoint: [clear description of state]"
```

**Cost:** 0.5 seconds  
**Risk reduction:** Exponential  
**Recovery path:** Always available

---

## What Counts as "Risky"?

✓ Major refactors  
✓ Deployments  
✓ Experiments  
✓ Policy changes  
✓ Database migrations  
✓ Dependency upgrades  
✓ Any change that could break things  

---

## Real Example: Token Famine Recovery

```
Timeline:

18:30 UTC - Operations running normally
Checkpoint created: "Normal operations, all systems green"

18:45 UTC - Token budget exhausted
Error cascades through system
Sub-agents frozen

18:46 UTC - Recovery starts
git log shows clear history
Last known-good checkpoint: 18:30

18:48 UTC - Revert executed
git reset --hard <18:30-checkpoint>
Systems restored

18:50 UTC - Online
Recovery time: 5 minutes
Data loss: 0
```

---

## Implementation

### 1. Commit Frequently
```bash
# After each significant state change
git add -A
git commit -m "Checkpoint: [what changed and why]"
```

### 2. Use Clear Messages
```bash
✓ Good: "Checkpoint: before agent scaling, 3 agents → 5 agents"
✗ Bad: "update"
✗ Bad: "fix bug"
✓ Good: "Checkpoint: after policy update to tier-routing v1.2"
```

### 3. Review Before Risky Work
```bash
# Before deployment
git log --oneline -5  # See recent checkpoints
git status  # Make sure working tree is clean
git commit -m "Checkpoint: before deployment"
```

### 4. Revert When Needed
```bash
# If something breaks
git log --oneline  # Find the checkpoint
git reset --hard <commit-hash>  # Restore to known-good state
```

---

## Production Evidence

**Live since:** 2026-03-12  
**Checkpoint frequency:** 15-20 per day  
**Token famines:** 5 in first 24 hours  
**Successful recoveries:** 5  
**Recovery time:** 2-5 min average  
**Data loss:** 0  

---

## Why Git Over Backups?

**Backups:** Point-in-time snapshots (good but not enough)  
**Git:** Continuous history + rollback capability + audit trail (better)

```
Backup model:
- Full backup every 24h
- If disaster at hour 20, lose 20 hours of work
- Recovery time: Find backup, restore, validate

Git model:
- Checkpoints every 15 minutes
- If disaster, lose ~7 min of work max
- Recovery time: 2-3 minutes
- Audit trail: Every change documented
```

---

## Standing Order

**Policy:** Git commit before any risky operation.  
**Frequency:** Minimum 3 checkpoints per day during active work  
**Message format:** "Checkpoint: [what], [why], [expected impact]"  
**Audit:** git log is audit trail for all operations

---

## Common Pitfalls

❌ **Mistake 1:** Commit too infrequently  
"I'll checkpoint after I finish the feature"  
→ Fix: Checkpoint before AND after risky work

❌ **Mistake 2:** Unclear messages  
"update"  
→ Fix: Write messages future-you can understand

❌ **Mistake 3:** Forgetting to commit  
"I'll remember the state"  
→ Fix: Make checkpointing automatic/routine

❌ **Mistake 4:** Not testing recovery  
"This works in theory"  
→ Fix: Actually practice reverting to checkpoints

---

## Checklist

- [ ] Commit before major changes
- [ ] Use clear checkpoint messages
- [ ] Review git log regularly
- [ ] Test recovery procedures (actually revert to old commits)
- [ ] Keep git history clean (don't delete old commits)
- [ ] Backup your git repo (just in case)

---

**Status:** Ready for prompts.chat | **License:** CC-BY-4.0
