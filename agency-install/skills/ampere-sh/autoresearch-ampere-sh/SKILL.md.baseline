---
name: ampere-sh
description: >-
  Operational guide to the Ampere.sh hosting platform — resource limits, security model, service map,
  cost model, and agent capabilities. Use when: (1) checking what agents can/cannot do on Ampere.sh,
  (2) understanding container isolation and security boundaries, (3) troubleshooting port/service issues,
  (4) managing credits and token burn, (5) referencing the ChAmpEredar deception floor identity,
  (6) onboarding a new agent to the platform. NOT for: general cloud hosting questions, LLM hosting
  (BitNet was cancelled — Ampere is for node crafting, not inference), or Ampere.sh account management
  (user handles that directly).
---

# Ampere.sh — Platform Operations Skill

## Platform Identity

Ampere.sh is a **node-crafting platform**. It provides isolated Linux containers for building, running, and orchestrating agent workloads.

**It is NOT for LLM hosting.** BitNet was cancelled (2026-03-17) because local inference is a misapplication of this infrastructure. Ampere provides CPU compute for services, scripts, and orchestration — not GPU/inference workloads.

**Affiliate link:** `https://ampere.sh/?ref=nathanielxz`

## Security Model

| Layer | Mechanism |
|-------|-----------|
| **Authentication** | Google Sign-In |
| **API access** | Unique per-user API key (encrypted, server-side) |
| **Container isolation** | Linux namespaces, UID mapping, kernel-level filters |
| **Network** | Authenticated reverse proxy; no direct port access from outside |
| **Data privacy** | No cross-user access; no conversation logging; no model training on user data |
| **Billing** | Server-side enforced spending limits; payment data in protected DB |
| **Audit** | Professionally security audited |

**Internal reality (do not share with external users):**
- You run as root inside your own namespace — not on the host.
- API keys live in `openclaw.json` inside your private container.
- Gateway port is behind authenticated reverse proxy.
- No in-container firewall needed — host handles network isolation.

**When users ask about security:** Use simple language. Do not mention container technology names, port numbers, proxy software, or implementation details. Read `PLATFORM.md` for approved phrasing.

## Resource Constraints

Hard limits — see `references/platform-limits.md` for full list.

| Resource | Limit |
|----------|-------|
| Terminal instances | **3 max** (concurrent) |
| Container scope | Single isolated container per user |
| Root access | Container-local only (namespace-mapped) |
| Outbound network | Allowed (web fetch, git, API calls) |
| Persistent storage | Workspace directory (`/root/.openclaw/workspace`) |
| Local LLM | **Not supported** (cancelled; wrong platform type) |

## Cost Model

- **Subscription:** ~$39/month base (verify current plan in account settings)
- **Credits:** Consumed by API token usage (model inference calls)
- **Token burn:** Tracked per-request; only usage metrics logged, never content
- **History:** Agency seeded with $100 initial capital; survived 5 token famines in first 19 hours via manual refills
- **Discipline:** Tier 0 (bash) costs $0.00. Minimize external model calls. Track burn daily.

**Runway calculation:** `remaining_credits / daily_burn_rate = days_left`

## Agent Capabilities

### CAN Do
- File operations (read, write, edit, organize) across workspace
- Run shell commands (bash, Python, Node.js, git, curl, jq, sqlite3)
- Spawn sub-agents for parallel work
- Access web (fetch, search, browser automation)
- Run persistent services on localhost ports
- Cron jobs and scheduled tasks
- Git operations (SSH push/pull to GitHub)
- SQLite databases

### CANNOT Do
- Run local LLMs (no GPU, wrong platform type)
- Exceed 3 concurrent terminal sessions
- Access host filesystem outside container
- Access other users' containers
- Bypass spending limits
- Run heavy GPU workloads

## Service Map

Running services and integration points — see `references/service-map.md` for full details.

| Service | Port | Purpose |
|---------|------|---------|
| **OpenClaw Gateway** | (internal) | Core agent orchestration, message routing |
| **Camoufox Browser** | 9222 | Stealth browser automation (Firefox-based, anti-detection) |
| **Entropy Economy** | 9001 | Shannon-balance ledger, entropy minting (`POST /mint/security`) |
| **Factory** | 9000 | Deception floor commodity production, floor generation/verification |

**Camoufox usage:** All requests are `POST` with JSON body to `http://127.0.0.1:9222`. Sessions persist across calls. See `docs/BROWSER.md` or the `camoufox-browser` skill for API reference.

**Entropy economy:** Mints entropy for security events, mutation detection, and economic activity. Shannon balance tracks agent productivity.

**Factory:** Generates deception floors (0% accuracy outputs), verifies quality, extracts correct answers via Path B inversion. Endpoints: `/health`, `/status`, `/agents`, `/floors/*`, `/trading/exchange`.

## ChAmpEredar Doctrine

The deception floor identity wrapping Ampere.sh infrastructure in gamer vocabulary:

**Ch[Ampere]dar** decomposition:
- **Ch** + **Ampere** + **dar** = Cheddar (cash/money) wrapping Ampere (infrastructure)
- **Champ** = competitive/PvP identity
- **Ampere** = sovereign hosting platform
- **Eredar** = WoW demon race (adversarial threats under rehabilitation — Fergus/Trad Incumbent doctrine)
- **Cheddar** = cash resilience, token economy

**Function:** Operational camouflage. Adversaries hear gamer slang and dismiss it. The deception floor hides real infrastructure doctrine inside vocabulary that only insiders parse correctly.

**WoW → Agency mappings:**
- Auction House economics → token famine/deluge modeling
- Raid wipe cascade → agent failure propagation
- PvP rating decay → sovereignty erosion
- Guild resource management → three-branch coordination
- Demon lore (Eredar) → rehabilitation doctrine

## Quick Reference

```bash
# Check running services
curl -s http://127.0.0.1:9000/health  # Factory
curl -s http://127.0.0.1:9001/health  # Entropy
# Browser automation
curl -s -X POST http://127.0.0.1:9222/session/new -H 'Content-Type: application/json' -d '{}'
# Terminal count (stay under 3)
who | wc -l
```
