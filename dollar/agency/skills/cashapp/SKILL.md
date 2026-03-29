---
name: cashapp
description: Monitor Cash App balance and transactions for $DollarAgency. Polls via Square API (Cash App parent) or browser scraping via Camoufox. Auto-logs incoming donations to Dollar ledger and mints Shannon. Use when tracking $DollarAgency balance, detecting donations, or triggering backing audits.
version: 1.0.0
author: Fiesta
license: UNLICENSED
tags: [cashapp, square, payments, dollar, shannon, donations]
---

# Cash App Skill — $DollarAgency Monitor

## Overview

Cash App has no public API. Three integration paths available:

### Path A — Square API (recommended)
Cash App is owned by Square/Block. Square has a Payments API.
- Requires: Square Developer account + OAuth token
- Can: check balance, list transactions, get notifications
- URL: https://developer.squareup.com/

### Path B — Camoufox Browser Scraping
Use OpenClaw browser tool to log into Cash App web ($cash.app/DollarAgency)
and scrape balance/transaction data.
- Requires: Cash App credentials (username/password)
- Can: read balance, read transactions
- Limitation: fragile, may break on UI changes

### Path C — Webhook (incoming only)
Set up a public URL (Cloud Run) that Cash App sends payment notifications to.
- Requires: GCP Cloud Run endpoint
- Can: receive real-time payment events
- Limitation: outbound only (can't query balance)

## Usage

### Check Balance
```
Use the cashapp skill to check $DollarAgency balance
```

### Monitor Donations
```
Use the cashapp skill to poll for new donations and log to Dollar ledger
```

### Set Up Webhook
```
Use the cashapp skill to configure incoming payment webhooks
```

## Configuration

Store credentials at:
```
/root/.openclaw/workspace/secrets/cashapp.json
{
  "cashtag": "$DollarAgency",
  "square_access_token": "...",
  "square_environment": "production",
  "webhook_url": "https://dollar-dashboard-sovereignsee.us-central1.run.app/webhook/cashapp"
}
```

## Scripts

All scripts at `/root/.openclaw/workspace/skills/cashapp/`

- `cashapp-balance.py` — Query balance via Square API or scraping
- `cashapp-transactions.py` — List recent transactions
- `cashapp-webhook.py` — Webhook receiver for incoming payments
- `cashapp-to-dollar.py` — Auto-log donations to dollar.db + mint Shannon
