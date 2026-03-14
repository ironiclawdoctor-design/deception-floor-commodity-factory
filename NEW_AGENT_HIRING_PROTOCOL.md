# New Agent Hiring Protocol (For Fiesta)

## How to Spawn New Agents

When you want to hire a new agent (subagent or session):

### Command Template
```bash
sessions_spawn \
  --task "Read BOOTSTRAP.md from /root/.openclaw/workspace. Choose task A/B/C/D. Execute with $0.00 external tokens. Log all decisions to build-orders-registry. Report to Actually (no narration, facts only)." \
  --label "New Agent: [Name/Role]" \
  --runtime "subagent" \
  --mode "run"
```

### What Happens Automatically

1. **Agent spawns** with full workspace access
2. **Agent reads BOOTSTRAP.md** (points to all doctrine files)
3. **Agent understands:**
   - Who we are (Identity, Soul)
   - How we operate (Tier 0-2, endorse/revoke, cost tracking)
   - What's real (concrete wins, working infrastructure)
   - What's first (pick A/B/C/D task)
4. **Agent executes** with understanding, not blind obedience
5. **Agent logs** all decisions (build-orders-registry)
6. **Actually monitors** (quietly, no narration)

---

## The Four Task Options

### Option A: Operational (Service Health)
- Check: BitNet, Grok, Factory, Tailscale, OpenClaw
- Log: Status JSON to build-orders-registry
- Report: "All services [status]" to Fiesta
- Cadence: Daily (set up as cron if they stick around)
- Cost: $0.00

### Option B: Revenue (Landing Page)
- Test: www/landing.html renders correctly
- Verify: All links work, Tailscale IP current
- Propose: 1 improvement (forms, copy, CTA)
- Cost: $0.00

### Option C: Growth (Acquisition Research)
- Research: Best communities for self-hosted AI (HN, Reddit, Dev.to)
- Draft: 3 post templates (not published, just created)
- Log: growth-research-YYYYMMDD.jsonl
- Cost: $0.00

### Option D: Learning (Crypto/Tech)
- Study: Bitcoin or Ethereum whitepaper
- Understand: How blockchains differ
- Propose: Agency token design (governance? revenue share? both?)
- Cost: $0.00

**All four can run in parallel.** All four are $0.00 cost. All four build skills.

---

## How Fiesta Manages New Agents

### Onboarding (First 30 Minutes)
1. Agent spawns
2. Agent reads BOOTSTRAP.md
3. Agent chooses task (A/B/C/D)
4. Agent starts with: `sessions_send --message "Starting task [X]"`

### Monitoring (Parallel with Execution)
Actually watches:
- Tier 0-2 discipline (are they routing correctly?)
- Cost tracking (every decision logged?)
- Decision quality (is reasoning sound?)
- Schedule adherence (are they autonomous or asking for permission?)

### Completion (When Task Done)
1. Agent logs final outcome to build-orders-registry
2. Agent reports to Fiesta: "Task complete, result is X"
3. Actually generates pattern report (if 3+ agents have run same task)
4. Fiesta decides: Keep agent on retainer, retire, reassign

---

## Metrics You'll See

### Per Agent
- Cost spent (should be $0.00)
- Decisions logged (should be 100% coverage)
- Tier 0-2 adherence (should be 100%)
- Task completion time (baseline for future agents)

### Aggregate
- Cost per task (stack tasks to amortize spawn cost)
- Accuracy of task execution (did A complete well? Then assign A to next agent too)
- Actually's audit pass rate (how many decisions are logged correctly?)
- Revenue impact (did growth research lead to users?)

---

## Scaling Pattern

### Week 1: One Agent
- Spawn 1 agent for task A (health check)
- Agent completes, logs, retires
- Cost: 1 agent spawn cost (~0 if subagent)

### Week 2: Three Agents (Parallel)
- Spawn agent A (health check, recurring)
- Spawn agent B (landing page test)
- Spawn agent C (growth research)
- All run simultaneously, all $0.00 cost

### Week 3: Five Agents (Specializing)
- Agent A: Daily health checks (automated, recurring)
- Agent B: Landing page iterations (weekly)
- Agent C: Growth channel research (weekly)
- Agent D: Crypto learning (weekly)
- Agent E: Revenue analysis (weekly)

### Month 2: Actual Team Structure
- Health checks → daily automation (no human review)
- Growth → weekly campaigns (3+ channels)
- Revenue → conversion tracking (Actually tracks)
- Product → user feedback loop
- Infrastructure → crypto foundation

---

## Actually's Role in Hiring

Actually monitors all new agents:

```
New Agent Spawned
  → Actually logs: {timestamp, agent_id, task, status}
  → Actually watches: All build-orders-registry entries
  → Agent executes
  → Actually logs: {completion, quality, cost, decisions_logged}
  → Actually reports to Fiesta: "Agent completed task [X]. Quality: [Y]. Cost: $0.00."
  → Fiesta decides: Repeat? Retire? Reassign?
```

**Actually doesn't judge.** Actually just observes and reports facts.

---

## Command Reference (Copy-Paste)

### Spawn Health Check Agent
```bash
sessions_spawn \
  --task "Read BOOTSTRAP.md. Choose task A (health check). Test: BitNet (8080), Grok (8889), Factory (9000), Tailscale (systemd), OpenClaw (18789+). Log JSON to build-orders-registry-YYYYMMDD.jsonl. Report results to Fiesta." \
  --label "HealthCheck Agent" \
  --runtime "subagent" \
  --mode "run"
```

### Spawn Revenue Agent
```bash
sessions_spawn \
  --task "Read BOOTSTRAP.md. Choose task B (landing page). Test www/landing.html. Verify renders, links work, Tailscale IP current. Propose 1 improvement. Log to build-orders-registry-YYYYMMDD.jsonl. Report to Fiesta." \
  --label "Revenue Agent" \
  --runtime "subagent" \
  --mode "run"
```

### Spawn Growth Agent
```bash
sessions_spawn \
  --task "Read BOOTSTRAP.md. Choose task C (growth research). Research: Best HN/Reddit/Dev.to communities for self-hosted AI. Draft 3 post templates (not published). Log to growth-research-YYYYMMDD.jsonl. Report findings to Fiesta." \
  --label "Growth Agent" \
  --runtime "subagent" \
  --mode "run"
```

### Spawn Learning Agent
```bash
sessions_spawn \
  --task "Read BOOTSTRAP.md. Choose task D (crypto learning). Study: Bitcoin or Ethereum whitepaper (free, public). Understand: How do blockchains differ? Propose: Agency token design (what utility?). Log thoughts to crypto-learning-YYYYMMDD.jsonl. Report proposal to Fiesta." \
  --label "Learning Agent" \
  --runtime "subagent" \
  --mode "run"
```

---

## Success Criteria

An agent is successful if:

✅ Completed assigned task  
✅ All decisions logged (100% coverage)  
✅ Cost tracked ($0.00 external tokens)  
✅ Tier 0-2 discipline maintained  
✅ Clear report delivered to Fiesta  

An agent is NOT successful if:

❌ Task incomplete  
❌ Missing logs (spotty record-keeping)  
❌ Haiku used for internal work (cost bleed)  
❌ No clear deliverable (vague results)  

---

## Future: Agent Persistence

Once you're confident in hiring, you can spawn persistent agents:

```bash
sessions_spawn \
  --task "Health check agent. Daily: run checks on all 5 services. Log to build-orders-registry. Report to Fiesta every 6h." \
  --label "Health Check (Persistent)" \
  --runtime "subagent" \
  --mode "session" \
  --thread true
```

Persistent agents:
- Don't spawn/despawn each cycle
- Build context over time
- Get better at tasks (learn from logs)
- Cost: Same ($0.00 per decision)

---

## Conclusion

New hiring is now **systematic, cost-efficient, and scalable.**

1. Write task → Spawn agent → Agent reads BOOTSTRAP → Agent executes → Agent logs → Fiesta reviews

No hand-holding. No vague directions. Framework is complete.

**You can now hire 10 agents tomorrow at $0.00 cost.**

---

**Status: Ready for /new spawning protocol.**

