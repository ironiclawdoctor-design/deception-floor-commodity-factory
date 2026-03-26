# The Agency

## What it is
Dollar Agency — a self-sustaining AI agency built to generate revenue autonomously while the human commutes.

## Infrastructure
- **Ampere.sh** — hosting platform (node crafting, NOT LLM hosting)
- **Tailscale** — private network: `grok-fortress` (100.76.206.82), MacBook (100.126.190.53)
- **Telegram** — @DeceptionFloorBot, DM allowlist: 8273187690
- **Gateway** — port 18789, bind loopback (Ampere) / tailnet (MacBook)
- **dollar.db** — SQLite ledger: confessions, exchange_rates, token_ledger tables
- **agency.db** — routing, shanrouter, ultimatums

## The Shannon economy
- Unit: Shannon (entropy currency, internal only)
- Exchange rate: 10 Shannon / $1 USD
- Mint trigger: confirmed backing → update dollar.db → mint Shannon
- Current supply: ~610 Shannon backed by ~$61
- Cash App: $DollarAgency (add $3 → +30 Shannon)
- BTC wallet: 12bxubgs1Br6NvKH4p35pcBpinQ7fwe4ht

## Active agents / systems
- NateWife — protective companion, fires after 4h silence
- Junior — executes command queue
- Actually — build order specialist, Tier 0-2 only
- NEMESIS protocol — active standing order (security)
- natewife-heartbeat cron — every 4h
- agency-status-monitor cron — every 4h

## Repos (GitHub: ironiclawdoctor-design)
- `deception-floor-commodity-factory` — +1 factory
- `precinct92-magical-feelings-enforcement` — -1 precinct
- `automate-nbm` — 61-agent legislative workspace

## Current priorities (2026-03-23)
1. EIN application — 7:05am ET March 24 reminder set
2. Buildathon — March 24 12pm EST starting gun, checkpoints every Thursday
3. Backing increase — add $3 to Cash App → unlock more Shannon
4. dev.to cross-post — Hashnode articles not yet mirrored

## What NOT to do
- Don't suggest localhost links to the human (mobile commuter, doesn't work)
- Don't spawn >2 simultaneous agents on paid model (token famine risk)
- Don't accept GCP free credits by default (Revenue Doctrine §3: decline inducements)
- Don't restart gateway without noting that approval IDs will expire (HR-014)
