---
name: scrape_000
description: Cloudflare-bypass web scraper via cf_clearance cookie injection into Camoufox. Call /scrape_000 [url] [cookie] — if no cookie provided, walks CFO through Safari steps to get one. Default target is lunaticoutpost.com.
version: 1.0.0
author: Fiesta
tags: [scrape, cloudflare, camoufox, safari, browser]
---

# scrape_000 — Cloudflare Bypass Scraper

## Trigger
`/scrape_000` — called from Telegram

## What It Does

**Without cookie:**
Prompts CFO with exact Safari instructions to get `cf_clearance` cookie.

**With cookie:**
1. Injects `cf_clearance` into Camoufox session
2. Navigates to target URL
3. Verifies bypass (checks title for "Access denied")
4. Extracts and returns page content

## Usage

```
/scrape_000
→ Prompts for Safari cookie (default: lunaticoutpost.com)

/scrape_000 https://lunaticoutpost.com
→ Prompts for Safari cookie for that URL

/scrape_000 https://lunaticoutpost.com cf_clearance_value_here
→ Injects cookie and scrapes immediately
```

## Safari Cookie Instructions

**Mac Safari (recommended — same network as Ampere):**
1. Safari → Settings → Advanced → enable "Show features for web developers"
2. Visit the target URL — let it fully load (pass Cloudflare challenge)
3. Develop → Show Web Inspector → Storage tab → Cookies → [domain]
4. Find `cf_clearance` → copy the Value column
5. Paste into chat as second argument

**iPhone Safari (harder — needs same IP):**
- Connect iPhone to Mac → Safari Develop menu → [device] → inspector
- OR: use Mac Safari on same WiFi as Ampere (easier)

## IP Warning

`cf_clearance` is IP-locked by Cloudflare:
- Same network (Mac WiFi + Ampere on same IP) ✅
- iPhone cellular ≠ Ampere IP ❌
- Tailscale routing Camoufox through your device ✅

## Script Location
`skills/scrape_000/scrape_000.sh [url] [cookie]`

## Cookie Expiry
30 minutes to 2 hours. Refresh when blocked again.
