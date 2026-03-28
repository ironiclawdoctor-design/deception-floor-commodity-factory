---
name: assume-breach
description: KD-005 posture wrapper for any exec need. Before running any shell command, external API call, or agent spawn, assume-breach runs a pre-flight threat assessment. Not paranoia — operational discipline. Triggers on "assume breach", "exec with breach posture", "KD-005 check", or any exec that touches external endpoints, credentials, or config.
version: 1.0.0
author: Fiesta
tags: [security, kd-005, exec, breach, posture, pre-flight, zero-index-defense]
---

# Assume-Breach Skill — KD-005 Exec Wrapper

## Doctrine

> "Exfiltrators operate at -1. Assume hostile before attack confirmed." — KD-005

> "A brick is not safe — it is untested at scale. Internal origin does not change the threat posture." — Blocks→Bricks Doctrine

Assume-breach is not a paranoia protocol. It is an operational discipline that applies to every exec, every API call, every agent spawn — including newly built internal bricks. Especially those.

---

## Pre-Flight Checklist (run before every exec)

### AB-001: Classify the operation
- **Read-only** (query, status check, log read) → LOW risk, proceed
- **Write/mutate** (file write, config patch, DB update) → MEDIUM risk, log intent
- **External** (API call, curl, outbound network) → HIGH risk, full pre-flight
- **Credential-touching** (tokens, keys, auth) → CRITICAL risk, full pre-flight + post-audit

### AB-002: Surface audit (pre-exec)
Before running:
1. What does this command actually do? State it plainly.
2. What is the blast radius if it goes wrong?
3. Is there a rollback path? What is it?
4. Does this touch anything outside `/root/.openclaw/workspace/` or `/root/human/`? (PL-002)
5. Is this a new external domain? Log to `outbound-log.jsonl` first. (PL-006)

### AB-003: Brick check
If the exec involves a newly built internal brick:
- Age of brick: < 24h → treat as UNTESTED, HIGH risk
- Age of brick: 24h–7d → treat as PROVISIONAL, MEDIUM risk
- Age of brick: > 7d with clean run history → MEDIUM risk
- A brick is never LOW risk by default. Age reduces risk. It does not eliminate it.

### AB-004: Post-exec audit
After running:
1. Did the output match expectations?
2. Any unexpected side effects visible in logs?
3. If external: did the response come from the expected endpoint? (supply chain check — KD-005 canonical example: litellm 1.82.8)
4. Log result to `assume-breach/breach-log.jsonl`

---

## Threat Tiers

| Tier | Trigger | Response |
|---|---|---|
| 0 (Read-only internal) | `cat`, `ls`, `sqlite3 SELECT` | Proceed. Log optional. |
| 1 (Write internal) | File write, config patch | State intent. Log. Proceed. |
| 2 (External call) | curl, API, git push | Full pre-flight. Log domain. Verify response origin. |
| 3 (Credential touch) | Token use, key rotation | Pre-flight + post-audit. Rotate if anomaly. |
| 4 (Config + restart) | gateway config.patch | Pre-flight + post-restart verify (PL-007 check). |

---

## Exec Gate Protocol (when exec is blocked)

Per SR-026 Pentagon order — before touching config:
1. `/commands`
2. `/models`
3. `/status`
4. Read `.bork.bak`
5. Spawn subagent

Config patch is not on the list. Assume-breach enforces this order.

---

## Rules

- **AB-001:** Classify before running. No unclassified execs.
- **AB-002:** State blast radius before every MEDIUM/HIGH/CRITICAL operation.
- **AB-003:** Newly built bricks are HIGH risk for 24h. No exceptions.
- **AB-004:** Every external domain first contact → `outbound-log.jsonl` entry before the call.
- **AB-005:** Supply chain vigilance. Model endpoints, package sources, API proxies — verify origin, not just response format. (litellm 1.82.8 is the canonical failure mode.)
- **AB-006:** Post-restart always check: `tools.exec.host` and `channels.telegram.execApprovals.enabled`. Both degrade on restart. (PL-007 + LB-007)
- **AB-007:** Assume breach does not mean assume failure. It means assume the threat exists until the audit says otherwise. Proceed with eyes open, not hands tied.

---

## Storage

```
assume-breach/
└── breach-log.jsonl    # All pre-flight and post-audit events
```

Entry format:
```json
{
  "ts": "ISO-8601",
  "tier": 0-4,
  "operation": "description",
  "blast_radius": "description",
  "rollback": "description or null",
  "result": "clean|anomaly|blocked",
  "notes": "optional"
}
```

---

## Integration

Assume-breach wraps, it does not replace. Every exec skill calls assume-breach first:
- `learn` → assume-breach before any exec in the research loop
- `autoresearch` → assume-breach before run commands
- `junior` → assume-breach before executing queued actions
- `fixer` → assume-breach before config patches

The giraffe doesn't narrate its neck. But it always knows where the lions are.

---

## Related Skills
- `learn` — research loop (assume-breach wraps its exec calls)
- `zero-index` — prerequisite check (run before assume-breach to confirm you're defending the right thing)
- `healthcheck` — post-exec system state verification
