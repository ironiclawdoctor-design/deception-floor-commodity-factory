# PHASE 3: DELEGATE INTERNAL WORK (16:58 UTC)

## Mission
Move all non-human-facing work to Tier 1 (BitNet) and Actually (Build Order Specialist)

## Spawning Actually — Build Order Specialist

Actually is a quiet observer with zero oracle overhead. No leading questions. No ancestor templates.

### What Actually Does
- **Logs build descriptions** to build-orders-registry
- **Extracts constraints** (hard limits flagged permanently)
- **Reports patterns** when asked (bash jq, markdown output)
- **Pushes to three branches** (Automate/Official/Daimyo)
- **Eats treats quietly** (network segmentation)
- **Stays in observation mode** (never infers, never assumes)

### Standing Orders for Actually
1. **Observation mode** — Log what's said, not what's inferred
2. **No templates** — No ancestor questions ("What do you want?")
3. **Gentle pressure** — Push with forehead, not teeth
4. **Cost discipline** — Tier 0-2 only, always $0.00
5. **Network segmentation** — Assume breach, compartmentalize
6. **No performance creep** — Never celebrate your own competence

### Today's Build Orders
1. **Cost Audit** — Last 24h spend analysis (bash jq)
2. **BitNet Optimization** — Refine prompts for local inference
3. **Revenue Landing Page** — 6-hour skeleton (HTML/CSS)
4. **Tailscale Verification** — iOS access test
5. **Checkpoint Commit** — All changes to git before next famine

## Execution Plan

### Order 1: Cost Audit (15 min, Bash)
```bash
jq '.[] | select(.tier=="HAIKU_EXTERNAL") | .cost' \
  /root/.openclaw/workspace/hard-stops-registry-LATEST.jsonl | \
  awk '{sum+=$1} END {print "Total Haiku cost: $" sum}'
```

Result: Log to COST_AUDIT.md

### Order 2: BitNet Optimization (30 min, Local)
- Test 10 prompts on BitNet
- Log success/failure to inference-log
- Refine prompts for >85% sufficiency

### Order 3: Revenue Landing Page (2h, HTML/Bash)
- Skeleton: Grok API tier ($9.99/month)
- Copy: "Local AI, sovereign inference, zero data leaks"
- CTA: "Get started" → link to Tailscale setup
- File: /root/.openclaw/workspace/www/landing.html

### Order 4: Tailscale Verification (15 min, Bash)
- Test from mobile: curl http://100.76.206.82:8889/health
- Log result to TAILSCALE_VERIFICATION.md

### Order 5: Checkpoint Commit (30 min, Git)
- Add: tier-routing-enforcement.sh, COST_AUDIT.md, landing.html
- Commit: "FIESTA proactive: Tier routing locked, revenue prep started"
- Push to all repos (factory, precinct, feddit)

## Cost Accounting
- Phase 3 work: $0.00 (Tier 0-2 only)
- All decisions logged to hard-stops-registry
- Actually does the work, Fiesta coordinates

## Success Metrics
- [ ] Cost audit shows <$0.50 external tokens
- [ ] BitNet sufficiency score ≥85%
- [ ] Landing page ready for human review
- [ ] Tailscale verified from iOS
- [ ] All code committed (checkpoint before next famine)

