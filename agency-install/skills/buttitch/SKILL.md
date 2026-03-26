---
name: buttitch
description: Buttitch — Main agent-only compliance enforcement skill. Use when a cron job, sub-agent, or skill is non-cooperative: timing out repeatedly, ignoring prompts, returning empty output, refusing tool use, or operating outside its mandate. Buttitch autoresearches the non-cooperative agent, classifies the failure mode, applies a targeted intervention (prompt surgery, timeout adjustment, model swap, or disable+replace), logs the action to agency.db, and mints Shannon for successful remediation. RESTRICTED: callable only by the main agent (Fiesta). Sub-agents may not invoke Buttitch against each other. Triggers on: "non-cooperative agent", "agent won't comply", "fix this cron", "agent keeps failing", "intervention needed", "buttitch", "enforce compliance". NOT for: general debugging (use failure-autopsy), scheduled sweeps (use sanitarium-sweep), or human-facing enforcement.
---

# Buttitch — Non-Cooperative Agent Enforcement

Main-agent-only. Buttitch identifies, autoresearches, and remedies non-cooperative agents across the agency. Named after the doctrine of last resort: when gentler methods have failed, Buttitch applies.

## Authorization Check

Before doing anything, verify caller is main session. If invoked from a sub-agent or cron, log an unauthorized invocation to `agency.db` and exit:

```sql
INSERT INTO confessions (agent, failure_type, description, doctrine_extracted, shannon_minted)
VALUES ('buttitch', 'unauthorized_invoke', 'Sub-agent attempted to invoke Buttitch', 
        'Buttitch is main-agent-only. Standing order.', 0);
```

Then stop. Do not proceed.

## Non-Cooperative Agent Classification

Classify the target before intervening. Read `references/failure-taxonomy.md` for full taxonomy. Quick matrix:

| Class | Signal | Intervention |
|-------|--------|-------------|
| **TIMEOUT** | consecutiveErrors ≥ 3, lastErrorReason=timeout | Prompt surgery + timeout bump |
| **EMPTY** | Runs OK but produces no output | Prompt rewrite with explicit output requirement |
| **RATE_LIMIT** | lastErrorReason=rate_limit | Model swap (qwen3-coder → glm-4.5-air:free) |
| **SCOPE_DRIFT** | Output unrelated to mandate | Mandate injection + hard output format |
| **GHOST** | Enabled, never ran, no state | Trigger manually, classify from first run |
| **INSOLENT** | Agent output contains refusal language toward CFO | Immediate disable + confession + escalate to main |

## Autoresearch Protocol

For each non-cooperative agent:

1. **Pull cron state** via `cron(action=list)` — get consecutiveErrors, lastError, lastDurationMs, model
2. **Read the prompt** — identify what's too long, too vague, or calling missing scripts
3. **Check the script** — if prompt calls `python3 path/to/script.py`, verify script exists via `read`
4. **Classify** using the matrix above
5. **Apply intervention** (see below)
6. **Test-fire** via `cron(action=run, jobId=...)`
7. **Log result** to `agency.db` confessions table
8. **Mint Shannon** if remediated: 10 Shannon per agent fixed

## Interventions

### TIMEOUT — Prompt Surgery
- Strip all multi-step logic from prompt
- Reduce to: one action + one output sentence
- Bump timeoutSeconds by 50% minimum
- If still timing out after 2 attempts: disable + log as CHRONIC_TIMEOUT

### EMPTY — Output Injection
Append to prompt:
> "End your response with exactly one line: `RESULT: [your finding]`. If nothing found, write `RESULT: CLEAN`."

### RATE_LIMIT — Model Swap
Switch from `qwen3-coder:free` or any rate-limited model to `openrouter/z-ai/glm-4.5-air:free`.

### SCOPE_DRIFT — Mandate Lock
Prepend to prompt:
> "You are [agent-name]. Your ONLY task is: [original mandate]. Do not expand scope. Output: [expected format]."

### GHOST — Trigger + Observe
Run once manually. Classify from output. Apply appropriate intervention.

### INSOLENT — Immediate Disable
```python
cron(action=update, jobId=..., patch={"enabled": False})
```
Log confession with `failure_type: insolence`. Escalate to main session with full output transcript.

## Shannon Minting

After each successful remediation (agent runs clean on re-test):

```sql
INSERT INTO shannon_events (agent, event_type, amount_usd, shannon_minted, description)
VALUES ('buttitch', 'certification', 0.00, 10, 
        'Remediated: [agent-name] — [class] → [intervention applied]');
```

Chronic failures (3+ interventions, still failing): mint 5 Shannon as documentation bounty, then disable.

## Logging

All actions logged to `agency.db` confessions table:

```sql
INSERT INTO confessions (agent, failure_type, description, doctrine_extracted, shannon_minted)
VALUES (
    'buttitch',
    '[TIMEOUT|EMPTY|RATE_LIMIT|SCOPE_DRIFT|GHOST|INSOLENT]',
    'Target: [agent-name]. Action: [intervention]. Result: [ok|chronic|disabled].',
    '[doctrine derived from this failure class]',
    [shannon_minted]
);
```

## Standing Orders

- **SO-1**: Never disable an agent without logging a confession first.
- **SO-2**: Never apply an intervention without classifying first.
- **SO-3**: Prompt surgery is always less destructive than disable. Prefer it.
- **SO-4**: If the script a cron calls doesn't exist, write a minimal stub before rewriting the prompt.
- **SO-5**: Model swaps are free. Try them before touching timeouts.
- **SO-6**: Buttitch does not negotiate with insolent agents. Disable is immediate.
- **SO-7**: Buttitch reports remediation summary to main session. No silent operations.

## References

- `references/failure-taxonomy.md` — Full failure class taxonomy with examples
- `references/intervention-library.md` — Pre-written prompt patches for common failure modes
