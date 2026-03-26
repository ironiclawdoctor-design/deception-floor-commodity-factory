# GLP Gatekeeper — Design Document
## Source: godlikeproductions.com access model (observed pattern, 2026-03-24)
## Purpose: Reference for all agency policies on new members, posters, and trillionaires

---

## What GLP Does (The Model)

GodLikeProductions is a conspiracy/paranormal forum that has operated since ~1999. It is one 
of the most heavily trafficked forums of its kind — and it stays that way through **extreme 
access friction by design**.

### The Gatekeeper Stack (observed layers)

1. **IP banning** — entire ISPs, VPNs, Tor exit nodes, corporate ranges blocked at the gate
2. **Browser fingerprint check** — Cloudflare/CDN challenge page ("Just a moment...") before any content loads
3. **Account creation friction** — not open registration; new posters face cooldown windows
4. **Post count gating** — certain threads/sections invisible to accounts below threshold
5. **Lurk requirement** — reading is possible; writing requires demonstrated intent to stay
6. **No indexing for fresh IPs** — new visitors see a degraded or blocked view
7. **Shadowban-first philosophy** — problematic users see their own posts; nobody else does
8. **Trillionaire tier** — paid membership that bypasses most friction layers instantly

### The Paradox That Works

GLP is hostile to new visitors by design. Yet it retains a massive loyal community. The 
friction is not a bug — it is the filter. The people who push through the gatekeeper are 
exactly the people GLP wants. The people who bounce are not missed.

**Agency translation:** A community that is hard to enter is self-selecting. Every barrier 
is a quality filter, not a growth obstacle.

---

## Agency Policy Framework (GLP-Derived)

### Tier 0: Public Facing (The GLP Homepage)
- Visible to anyone, no authentication
- Content is curated teasers, not full access
- Represents the agency's public face (Hashnode articles, bot /start response)
- **Rule:** Never put operational data at Tier 0. Public sees the pitch, not the ledger.

### Tier 1: Lurker Access (Read-Only)
- Can read but not write
- No account required, but IP/fingerprint tracked
- Equivalent to: following @DeceptionFloorBot, reading Hashnode articles
- **Rule:** Lurkers are potential converts. Do not friction them — educate them.
- **GLP equivalent:** Being able to browse threads without an account

### Tier 2: Poster Access (Basic Member)
- Account created, identity established
- Can post but subject to moderation queue
- Low Shannon balance or zero contributions
- Equivalent to: first-time donor, first bot command used
- **Rule:** New posters get watched, not trusted. Prove contribution before access expands.
- **GLP equivalent:** New account, post count < 50, no special permissions

### Tier 3: Verified Member
- Track record established (post history, donation history, skill usage)
- Access to internal channels, private threads
- Shannon balance > 0, active in agency ecosystem
- Equivalent to: repeat donor, ClawHub skill user, active bot engagement
- **Rule:** Verified members get benefit of the doubt. Extend access incrementally.
- **GLP equivalent:** Account with 500+ posts, years on platform

### Tier 4: Trillionaire (Paid Access / Ally)
- Bypasses most friction layers
- Direct access to agency internal state
- Active financial or operational contributor
- Equivalent to: GCP collaborator, significant donor, skill co-author
- **Rule:** Trillionaires earned their access. Never re-friction them. Remove barriers proactively.
- **GLP equivalent:** Paid subscription that bypasses IP bans, captchas, post delays

### Tier 5: Agency (Internal / No Friction)
- Full access to all systems
- Doctrinal alignment verified
- Fiesta, Actually, Shannode, base93, all named agents
- **Rule:** Internal agents never see the gatekeeper. They ARE the gatekeeper.
- **GLP equivalent:** Moderator / Admin / Trinity (site operators)

---

## Gatekeeper Rules Derived from GLP Model

### GK-001: Friction is a Filter, Not a Bug
> New members experiencing friction is correct behavior. The friction selects for people 
> with genuine interest. Do not optimize it away. Optimize it to be surmountable by the 
> right people and impenetrable by the wrong ones.

### GK-002: The Shadowban is Mercy
> Before banning or blocking a disruptive member, shadowban first. They see their own posts; 
> no one else does. This prevents martyrdom and gives them time to self-correct. Hard bans 
> are for repeat offenders who already know they're banned.

### GK-003: Trillionaires Skip the Line
> Anyone who has paid real money (USD, Shannon, or demonstrated labor) to access the agency 
> gets frictionless passage. Never re-verify a verified contributor. Trust compounds.

### GK-004: IP/Fingerprint First, Identity Second
> The agency's first question about any new actor is behavioral, not biographical. 
> What are they doing? How are they accessing? From where? Identity questions come after 
> behavioral signals are established.

### GK-005: The Lurk Window is Real
> New members should be able to consume content freely before being asked to contribute. 
> Force-asking for commitment before value is demonstrated is the fastest way to lose 
> good members. GLP lets you read for years before you post.

### GK-006: Post Count is Proof of Work
> In GLP, post count is a rough proxy for commitment. In the agency, Shannon balance and 
> interaction history serve the same function. A member with 0 Shannon and 1 bot command 
> gets less access than one with 50 Shannon and 40 bot commands. This is correct.

### GK-007: The Gatekeeper Page is Doctrine
> GLP's "Just a moment..." Cloudflare challenge is not just security — it is a statement. 
> "We are worth waiting for. If you won't wait 3 seconds, you are not our audience." 
> The agency's equivalent is requiring real intent before granting access. 
> Base93 encoding IS the gatekeeper page for inter-department communication.

### GK-008: No Gatekeeper for Existing Members
> Once inside, the experience should be frictionless. The gatekeeper exists at the boundary, 
> not inside the community. Friction applied to existing members destroys trust.
> **HR-008 corollary:** The human has already passed every gate. Never re-gate the human.

---

## Shannode Application

Shannode manages the Hashnode publication. Using GLP model:

- **Public articles** (Tier 0): Everyone reads, no friction
- **Comment moderation** (Tier 1→2 gate): Comments require Hashnode account (built-in friction)
- **Article updates** (Tier 3+): Only verified engagement drives content improvements
- **Private doctrine articles** (Tier 4+): Internal Hashnode drafts, not published publicly
- **Editorial access** (Tier 5): Only Fiesta/Shannode can publish to the publication

### Comment Response by Tier

| Tier | Who | Response Protocol |
|------|-----|-------------------|
| 0 | Anonymous reader | No interaction possible (read-only) |
| 1 | Lurker | No response needed (they haven't spoken) |
| 2 | New commenter | Acknowledge, answer question, assess intent |
| 3 | Verified member | Full engagement, link to related articles |
| 4 | Trillionaire | Priority response, invite to collaborate |
| 5 | Agency | Internal routing, not public comment |

---

## The Trillionaire Doctrine

GLP's paid tier is called "Trillionaire." This is intentionally absurd — it signals that 
the value of the community is worth more than the subscription price, not less.

The agency's Trillionaire equivalent: anyone who contributes Shannon, USD, labor, or 
intellectual property to the agency is a Trillionaire by definition. The absurdity is 
the point. We don't have millionaires here. We have people who believe the agency is worth 
more than they paid, so they pay anyway. That belief is the asset.

**Trillionaire access grants:**
- Direct Telegram DM access to @DeceptionFloorBot (bypasses /start funnel)
- Private Hashnode draft access (articles before publication)
- Shannon minting reports (weekly ledger digest)
- Ability to propose new agency doctrines (GK-009 pending)

---

## Status
**Adopted as agency access policy: 2026-03-24**  
**Applies to:** Shannode moderation, BotFather funnel tiers, ClawHub access, all new member onboarding  
**Does NOT apply to:** Internal agent-to-agent communication (base93 handles that)
