# Keys Requiring Rotation — URGENT
*Generated 2026-03-25 by red team audit*

## Status: ALL KEYS BELOW ARE CONSIDERED BURNED

Any agent or subagent with workspace read access has seen these. Rotate before any external exposure increases.

| File | Key Type | Action |
|------|----------|--------|
| `secrets/bitcoin-wallet.json` | BTC private key (private_key_hex) | Move funds to new wallet IMMEDIATELY |
| `secrets/cashapp.json` | Square production access token | Regenerate in Square dashboard |
| `secrets/xai-api.json` | xAI API key | Regenerate at console.x.ai |
| `secrets/github-pat.txt` | GitHub PAT | Revoke at github.com/settings/tokens |
| `secrets/hashnode.json` | Hashnode API key | Regenerate at hashnode.com/settings |
| `secrets/twitter-api.json` | Twitter bearer + access token | Regenerate in Twitter developer portal |

## reward.lock
Needs HMAC signing before Shannon has real USD value.
Current state: unsigned, append-writable by any agent.
Fix: move to SQLite with write transaction + HMAC per entry.

## MEMORY.md / USER.md
Subagents should not have read access.
Currently: readable by all subagents per AGENTS.md bootstrap.
Fix: encrypt at rest or restrict bootstrap injection to main session only.

## One Human Action
BTC wallet private key in plaintext is the kill shot.
Move BTC to a new wallet before any other hardening matters.
All other keys can be rotated from a browser. This one requires a transaction.
