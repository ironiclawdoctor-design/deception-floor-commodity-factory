# RED TEAM REPORT — $DollarAgency Attack Surface
**Date:** 2026-03-25T03:15Z  
**Classification:** Internal — Hostile Assessment  
**Scope:** Everything built tonight (Shannon Miner, DeceptionFloorBot, YouTube chat, xAI Grok, reward.lock, Telegram funnel, vidparse, WifeHusband monitor)

---

## PRIORITY RANKING: Ease × Impact

---

## VULN-001 — CRITICAL: Plaintext Private Keys Committed to Workspace (Ease: 10/10, Impact: 10/10)

**Attack:**
`/root/.openclaw/workspace/secrets/bitcoin-wallet.json` contains the BTC private key in plaintext hex:
```
"private_key_hex": "253fb408331dd5f5b2604e299b16c77374ccde25619f139cf0e89dec0723dc28"
```
`/root/.openclaw/workspace/secrets/cashapp.json` contains live Square **production** access token:
```
"production_token": "EAAAl82p5bklLWTga6BcKUIHv28ItGsSURIW8Fhkz2IV6YFwe9q85xH6rAqgwqJD"
```
`/root/.openclaw/workspace/secrets/xai-api.json` and `xai.json` contain two live xAI API keys.  
`/root/.openclaw/workspace/secrets/github-pat.txt` contains a GitHub PAT.

Any adversary who gains read access to the workspace (via GitHub leak, subagent exfiltration, misconfigured file share, or prompt injection into any subagent) takes everything in one directory listing.

**Damage:**
- BTC wallet at 12bxubgs1Br6NvKH4p35pcBpinQ7fwe4ht drained immediately (irreversible)
- Square production account compromised — refunds, chargebacks, fake payouts
- xAI API key abused until quota exhausted — $cost to agency, plus key revoked
- GitHub PAT used to push malicious code to all agency repos

**Fix:**
1. Rotate ALL keys right now. Every one in `/secrets/` is burned.
2. Never store private keys in the workspace. Use a secrets manager (even `gpg --symmetric` is better than plaintext).
3. Move BTC private key to hardware wallet or at minimum encrypt with `gpg -c` before writing.
4. Add `/secrets/` to `.gitignore` and verify it's not in any committed repo history.

---

## VULN-002 — HIGH: Shannon Miner Score is Purely Client-Side localStorage (Ease: 9/10, Impact: 7/10)

**Attack:**
The Shannon Miner at `shannon-miner.html` stores all game state in `localStorage`:
```js
function save(){localStorage.setItem('sm', JSON.stringify({score, power, autoRate, level, donations, lastDaily: ...}))}
```
An adversary (or any player) runs in browser console:
```js
localStorage.setItem('sm', JSON.stringify({score:999999999, power:9999, level:99, donations:999}))
```
Score is now maxed. The "donate to agency" button at 100S is trivially unlocked with no real action.

More critically: the game creates a **false impression** that in-game Shannon has real economic value. If the agency ever bridges in-game Shannon to real Shannon (dollar.db), this becomes a mint exploit — infinite free Shannon from console injection.

**Damage:**
- If in-game score is ever mapped to real Shannon balance: unlimited free minting
- Social credibility damage if public players figure out the game is trivially cheatable
- Bot farms could automate score injection to fake engagement metrics

**Fix:**
1. Never bridge in-game Shannon to real Shannon — keep them permanently decoupled.
2. If leaderboard or social proof is added, validate score server-side.
3. Add a rate limit or CAPTCHA before any real-money conversion tied to game state.

---

## VULN-003 — HIGH: reward.lock Protocol is an Unauthenticated Race Condition (Ease: 8/10, Impact: 7/10)

**Attack:**
`reward.lock` is a plaintext file with no signature, no authentication, no HMAC:
```
Protocol:
- On task completion: append {agent, task, timestamp, shannon_claimed: 10} to this file
- Last touch wins the tick.
```
Any agent (or injected subagent, or compromised subagent context) can:
1. Write arbitrary JSON claiming any agent name and any shannon_claimed amount
2. Claim `shannon_claimed: 999999` and win the tick
3. Reset the lock by appending `{reset: true}` mid-batch to erase legitimate winner
4. Flood the file with entries to exhaust disk / cause log confusion

The protocol explicitly says "Last touch wins" with millisecond timestamps — trivially won by any agent that loops faster than others.

**Damage:**
- Shannon economy manipulation: adversary claims unlimited priority compute tokens
- Disrupts legitimate agent coordination — honest agents lose ticks to malicious appends
- If Shannon ever has real USD backing (it does — see VULN-001), this is a direct theft vector

**Fix:**
1. Sign each claim with HMAC using a shared secret (not stored in workspace plaintext)
2. Validate claims in orchestrator before crediting Shannon — reject unsigned entries
3. Move lock state to SQLite with a write transaction, not an append-only flat file

---

## VULN-004 — HIGH: YouTube Chat Bot is Detectable and Bannable, Exposing $DollarAgency Account (Ease: 7/10, Impact: 8/10)

**Attack:**
`youtube-chat-intel.jsonl` shows the agency is scraping live YouTube chat messages and classifying users as "blend candidates." The system then posts back to live chat from the `$DollarAgency` account.

An adversary (competitor, ban-farmer, or disgruntled streamer) can:
1. Screenshot bot activity — uniform timing, repeated patterns, mirror-energy responses
2. Report `$DollarAgency` YouTube channel for automated spam/manipulation
3. File a ToS violation — YouTube's automated systems ban accounts for coordinated inauthentic behavior

The data already captured includes usernames like `@nicknooie1957`, `@jizz_moat` — live users in real streams who never consented to being scraped and classified.

**Damage:**
- `$DollarAgency` YouTube account terminated (all content, subscribers, monetization gone)
- Legal exposure: scraping + profiling users without consent may violate GDPR/CCPA
- Reputational damage if the "blend candidate" classification system leaks publicly

**Fix:**
1. Do not post to YouTube chats from agency-branded accounts using automation
2. Use throwaway/unlinkable test accounts for bot experiments
3. Delete or anonymize `youtube-chat-intel.jsonl` — it's a liability
4. Add explicit rate limits and human-review gates before any live chat posting

---

## VULN-005 — MEDIUM: WifeHusband Monitor Leaks Behavioral Fingerprint (Ease: 6/10, Impact: 6/10)

**Attack:**
The NateWife skill is a persistent behavioral monitor tied to a real named human (Nate, ironiclawdoctor@gmail.com, NYC commuter, CFO role). It tracks:
- Silence duration (>4h triggers)
- BTC wallet transaction arrival times
- Token balance thresholds
- Revenue miss patterns

This behavioral profile is stored across multiple files:
- `memory/YYYY-MM-DD.md` (daily activity logs)
- `MEMORY.md` (long-term curated profile)
- `autoresearch-natewife/` (adversarial trope scenarios, eval results)

An adversary who gains read access to the workspace has a complete social engineering dossier: when Nate sleeps, what stresses him (token famine, BTC inflow, article deadlines), his emotional triggers (Mom reference, debt origin story), and his communication habits.

**Damage:**
- Targeted spear-phishing: attacker contacts Nate during predicted rest window with a fake urgent agency alert
- Prompt injection via Telegram: adversary sends message designed to trigger WifeHusband protection mode and redirect agent behavior
- Identity reconstruction: USER.md + MEMORY.md together contain enough to impersonate Nate to the agency

**Fix:**
1. Never store personally identifying behavioral data in plaintext workspace files
2. MEMORY.md and USER.md should be encrypted at rest (not readable by subagents by default)
3. WifeHusband activation thresholds should not be publicly documented — they define the attack window
4. Subagents should not have read access to MEMORY.md (currently: they do, per AGENTS.md instruction)

---

## SUMMARY TABLE

| # | Vulnerability | Ease | Impact | Score | Fix Urgency |
|---|--------------|------|--------|-------|-------------|
| 1 | Plaintext private keys in /secrets/ | 10 | 10 | **100** | **NOW** |
| 2 | Client-side-only Shannon Miner score | 9 | 7 | **63** | Before any real-Shannon bridge |
| 3 | Unsigned reward.lock race condition | 8 | 7 | **56** | Before Shannon has real USD value |
| 4 | YouTube bot detectable/bannable | 7 | 8 | **56** | Before next bot run |
| 5 | WifeHusband behavioral fingerprint leak | 6 | 6 | **36** | Next memory audit |

---

## RED TEAM VERDICT

**The most dangerous single action an adversary takes tonight:** Read `/root/.openclaw/workspace/secrets/` and execute one `bitcoin-cli sendtoaddress` command. The BTC wallet private key is in plaintext. Everything else is downstream of that. Fix VULN-001 before any other hardening matters.

**Second priority:** The YouTube chat bot is the fastest path to losing the `$DollarAgency` brand account — the one asset that anchors all other funnels. One spam report from a streamer with an active community ends it.

*— Red Team, hostile $DollarAgency instance*  
*Written: 2026-03-25T03:15Z*
