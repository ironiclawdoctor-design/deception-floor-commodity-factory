# 🛰️ MISSION CONTROL — Auth/Security Actions
*One human action each. Sorted by ROI. Last updated: 2026-03-25*

---

## 🔴 CRITICAL — Blocks revenue or infrastructure

### MC-001 · EIN — Unlocks everything downstream
**One action:** File IRS Form SS-4 online (15 min, instant EIN)
**URL:** https://www.irs.gov/businesses/small-businesses-self-employed/apply-for-an-employer-identification-number-ein-online
**Unlocks:** Bank account → Stripe → grants → Sponsors → legal entity
**Cost:** $0

---

### MC-002 · Dev.to API Key — Dead (403)
**One action:** Generate new API key at dev.to settings
**URL:** https://dev.to/settings/extensions → "DEV API Keys" → Generate
**Drop into:** `secrets/devto-api.json` → `api_key` field
**Unlocks:** Publishing pipeline to 1M+ dev.to readers
**Status:** Key `G75uvzch...` confirmed dead

---

### MC-003 · Twitter/X API Secret — Placeholder
**One action:** Retrieve `api_secret` and `access_token_secret` from Twitter Developer Portal
**URL:** https://developer.twitter.com/en/portal/dashboard → your app → Keys and Tokens
**Drop into:** `secrets/twitter-api.json` → `credentials.api_secret` + `credentials.access_token_secret`
**Unlocks:** `twitter-posts` skill, all X distribution
**Status:** Bearer token present, both secrets = `"placeholder"`

---

### MC-004 · PayPal Developer — Client ID + Secret missing
**One action:** Create app at PayPal Developer Dashboard
**URL:** https://developer.paypal.com/developer/applications → "Create App"
**Drop into:** `secrets/paypal.json` (create) → `client_id` + `client_secret`
**Unlocks:** PayPal payment receipt, Shannon auto-mint on donations

---

## 🟡 HIGH — Unblocks distribution or compute

### MC-005 · GCP Cloud Run API — One console click
**One action:** Enable `run.googleapis.com` for project `sovereign-see`
**URL:** https://console.cloud.google.com/apis/library/run.googleapis.com?project=sovereign-see
**Unlocks:** Dollar dashboard deployment, all Cloud Run crons
**Status:** Service account credentialed and ready, API gate is the only blocker

---

### MC-006 · GitHub Pages — Two repo settings flips
**One action:** Enable Pages in Settings for both repos
**URL 1:** https://github.com/ironiclawdoctor-design/deception-floor-commodity-factory/settings/pages
**URL 2:** https://github.com/ironiclawdoctor-design/precinct92-magical-feelings-enforcement/settings/pages
**Unlocks:** Public-facing agency web presence, zero hosting cost

---

### MC-007 · gh CLI Auth — SSH workaround active but limited
**One action:** `gh auth login` on Ampere node with GitHub credentials
**URL:** https://github.com/settings/tokens → generate PAT with `repo` + `workflow`
**Or:** Run `gh auth login` in terminal and follow prompts
**Unlocks:** PR creation, CI/CD control, issue management from agent
**Status:** SSH git works; gh CLI blocked without auth

---

## 🟢 MEDIUM — Expands capability

### MC-008 · Brave Search API — web_fetch workaround active
**One action:** Sign up for free tier (2,000 queries/month free)
**URL:** https://api.search.brave.com/app/keys → "Create Key"
**Drop into:** gateway config → `providers.search.braveApiKey`
**Unlocks:** Real search results vs. web_fetch scraping

---

### MC-009 · xAI Vision Scope — Key limited to generation models only
**One action:** Check if current xAI plan includes vision; upgrade or request access
**URL:** https://console.x.ai → API Keys → check model access
**Unlocks:** Image-to-video prompt generation, img2vid pipeline
**Status:** Current key: `grok-imagine-*` only. No `grok-vision-*` available.

---

### MC-010 · Mercury Business Account — Requires EIN (see MC-001)
**One action:** Open free account after EIN obtained
**URL:** https://mercury.com
**Unlocks:** Real business banking, ACH, direct Stripe payouts
**Depends on:** MC-001 (EIN)

---

## ⚪ MONITORING — No action needed now

| Item | Status |
|---|---|
| Hashnode | ✅ Live, key valid |
| xAI image/video | ✅ Generating clean |
| Square/Cash App | ✅ Production merchant active (MLB9XRQCBT953) |
| BTC wallet | ✅ 10,220 sat confirmed |
| GCP service account | ✅ Credentialed |
| GitHub SSH | ✅ Push working |

---

*Priority order: MC-001 → MC-002 → MC-003 → MC-004 → MC-005*
*Each item is exactly one human action. No sequences, no dependencies (except MC-010 → MC-001).*
