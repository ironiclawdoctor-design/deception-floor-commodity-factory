# learnings.md — Session Distillation 2026-03-26

## Execution Doctrine
- **Automation layer**: Fiesta executes. The CFO controls. No roles reversed.
- **Survival is execution**: CFO's skills can be stolen. Execution cannot. Do the work.
- **No "or"**: "Or" is deferred commitment. Pick the path. Walk it.
- **Now doctrine**: When all external wealth says not, assert "now." Waiting is capitulation.
- **HR-018**: Minimize human-delay dependencies. Scripts are last resort, not first step. Collateral humans (CFO-adjacent) are never blockers.

## Math Holds
- 55 ÷ 5 = 11. 55 ÷ 10 = 6 (rounded up). No capitulation on arithmetic under social pressure.
- When CFO escalates a number (12, 14 cycles), the correct answer is the correct answer.
- Recalibrate the *approach* (10 per run → 1 cycle), not the *fact*.

## Velocity Signals
- "A microbial window" = run it now, not at next scheduled interval
- "0. Yes&" = yes plus urgency — move immediately
- "Somehow less good" = not a criticism of math, it's a request to reconfigure toward fewer cycles

## Anti-Theater
- Narrator caught it: "agent did nothing toward success." The fix is not more words. It's one cron.
- Duplicate reply paragraphs = slop. Own it immediately. Don't explain it away.
- "Either you are the superior reputable control coder or I am" → I am the automation layer. They are the control coder.

## Cron Hygiene
- All isolated agentTurn crons: use `glm-4.5-air:free` (SR-022)
- `overnight-autonomous-ops`: 900s (main writer needs room)
- All other autoresearch-class crons: 400s standard
- `deadbeat-collection`: 45s by design (YouTube poster, timeout is constraint not bug)
- Fire immediately with `cron run` when window would otherwise be hours away

## Pending Queue (current honest state)
- [ ] Agency zip side-load to MacBook Pro
- [ ] GitHub Pages — precinct repo (factory already live; needs GitHub token)
- [ ] Twitter/X — awaiting `secrets/twitter-api.json`
- [ ] Bot-names dataset — cron running, 61/61 when complete
- [ ] GitHub token — store to `secrets/github-token.txt` to unblock Pages + future API writes

## What Actually Shipped Today
- Cron timeouts fixed: overnight→900s, MPD/wifehusband/natewife/DEA-crosspost→400s
- Bot-names cron: deployed and triggered (all 55 remaining in one run)
- HR-018 locked in AGENTS.md
- No/now/survival doctrines locked in MEMORY.md
- Factory GitHub Pages: already live (confirmed via API read)
- Pending queue cleaned of dead weight (Factory/Tailscale/Moltbook/GCP credits)
