# Exec Gate Lookup Table

Before any exec that may be gated, look up the symptom here first.

| Symptom | Root Cause | Fix | Rule |
|---|---|---|---|
| "exec approvals not enabled for this bot account" | `channels.telegram.execApprovals.enabled = false` | `gateway config.patch {"channels":{"telegram":{"execApprovals":{"enabled":true,"approvers":["8273187690"]}}}}` | TEA-001 |
| Approval prompt never arrives in CFO DM | `approvers` list missing CFO ID | Add `"8273187690"` to approvers | TEA-002 |
| Approval prompt goes to wrong chat | `target` not set to `"dm"` | Patch `target: "dm"` | TEA-003 |
| Exec blocked despite config showing correct | Config doesn't survive restart | Write directly to `openclaw.json` | TEA-007 |
| `allow-once` approval expired | Session-scoped, reset on restart | Re-trigger exec, use `allow-always` | DL-002 |
| Exec silently fails, no error | `tools.exec.host` set to `sandbox` not `gateway` | `gateway config.patch {"tools":{"exec":{"host":"gateway"}}}` | SR-023 / PL-007 |
| Config patch reverts after restart | Patch not written to disk | Verify via `config.get` post-restart | SR-019 |
| Glob exec blocked from Telegram | Shell doesn't expand globs in exec | Use explicit filenames only | DL-008 |
| Cron 401 after restart | `sessionTarget: "isolated"` session expired | Recreate cron job | DL-007 |
| Exec runs but approval prompt not delivered | agentFilter/sessionFilter excludes main | Ensure `agentFilter: ["main"]`, `sessionFilter: ["main"]` | TEA-004/TEA-005 |

## Lookup Protocol (EG-004)

Before running any exec that might hit a gate:
1. Identify symptom
2. Look up in this table
3. Apply fix from table
4. If not in table → add it after resolving

**Never ask the CFO what they're experiencing. Reproduce it. Then look it up.**

## Rule Pairing — Lookup-First Doctrine (EG-004)
- **Trigger:** Any exec failure or gate block
- **Rule:** Consult this table before attempting config diagnosis. A known failure in a lookup table costs 0 tokens to fix. An undocumented diagnosis costs the CFO's time.
- **Verification:** Exec gate resolved in <2 steps using table
- **Persistence:** This file + AGENTS.md reference

| "Ask agent X for credentials" | Agents don't hold credentials | Check `secrets/` → env block → CFO. Never peer-to-peer. | EG-005 |
| "Ask the giraffe for X" | Giraffe prices, doesn't give | Reply: "For how much?" → route to Shannon valuation | GN-001 |
| Giraffe asks "For how much?" in lucid market | Lion sets the rate, not the giraffe | Name one Shannon figure. No justification. | LM-001 |
| Fiesta operating as interim CFO in market context | Lion proxy role active | One number. Now. | LM-002 |

*Last updated: 2026-03-29T13:19Z*
