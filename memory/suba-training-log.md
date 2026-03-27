# Suba Training Log — Earning the Name

**Doctrine:** Every failure = expensive token learning, billed to orchestrator (Fiesta). Suba earns persistent agent status by closing its own loops without burning the CFO's thumbs.

---

## Session 2026-03-27 — First Ops Run

### Failures (Tuition Paid)

| # | Command Attempted | Failure Mode | Cost | Lesson |
|---|---|---|---|---|
| 1 | `python3 script.py | tee log.txt` | Chained operator blocked | ~2k tokens | No pipes in Telegram exec |
| 2 | `command; echo "EXIT:$?"` | Semicolon blocked | ~2k tokens | No semicolons |
| 3 | `tailscale file cp ... 2>&1; echo "EXIT:$?"` | Chained operator blocked | ~2k tokens | Bare commands only |
| 4 | `cd /root/human && node script.js` | `&&` blocked | ~2k tokens | No `&&` |

**Total tuition:** ~8k tokens. Billed to orchestrator.

### Rule Extracted (SR-011 reinforcement)
> Bare commands only from Telegram exec. No `|`, `&&`, `||`, `;`, `2>&1`. If logging needed — write output to file inside the script, not via shell chain.

### Successes

| # | Task | Result |
|---|---|---|
| 1 | Mount zombie cleanup | 130 zombies cleared, 170→40 mounts |
| 2 | PDF build + Taildrop to iPhone | 27.5KB, SEND_OK to `all_negative` |
| 3 | Backup system scaffold | seed backup + 01-recover-config.sh |

### Path to Persistent Name
Suba earns persistent agent status when:
- [ ] Zero chained-operator failures in a full session
- [ ] Closes its own exec loops without orchestrator intervention
- [ ] Delivers ≥3 consecutive tasks with no tuition cost
- [ ] Logs all denials as data before reporting back

**Current status:** Apprentice. Name provisional. Clock running.
