---
name: paypal-secure-access
description: Secure PayPal API integration for agent-driven payment operations. Check balances, send/receive payments, manage subscriptions, and fund agent operations (token credits). Uses OAuth 2.0 with client credentials stored securely. Built by the Deception Floor Commodity Factory as internal infrastructure.
version: 0.1.0
author: Official & Fiesta @ ironiclawdoctor-design
license: PRIVATE
tags: [paypal, payments, funding, agent-economy, secure-access]
---

# PayPal Secure Access — Agent Funding Skill

> **Origin:** This skill was manufactured by the Deception Floor Commodity Factory.
> No PayPal skill existed on ClawHub (0). Now one exists (1). Private property.

## Purpose

Enable agents to securely access PayPal for:
- 💰 Checking account balance (funding status)
- 🔄 Monitoring incoming payments/donations
- 📊 Transaction history and reporting
- ⛽ Auto-funding agent credits when balance is sufficient
- 🔐 All via OAuth 2.0, credentials never exposed in logs

## Security Model

```
┌──────────────────────────────────┐
│         SECURE CREDENTIAL STORE  │
│                                  │
│  PayPal Client ID  ──► env var   │
│  PayPal Secret     ──► env var   │
│  Access Token      ──► runtime   │
│  (never in files, never in logs) │
└──────────────────────────────────┘
         │
         ▼
┌──────────────────────────────────┐
│        PAYPAL API (REST v2)      │
│  api-m.paypal.com                │
│  OAuth 2.0 Bearer Token Auth    │
│  TLS 1.2+ encrypted transport   │
└──────────────────────────────────┘
```

### Why Not SSH?

PayPal's API does not support SSH key authentication. Their security model is:
- **OAuth 2.0** client credentials flow (client_id + client_secret → bearer token)
- **TLS** for transport encryption
- **Webhook signatures** for event verification

SSH keys secure *our server* (where credentials are stored). PayPal secures *their API* with OAuth. The two models complement each other:
- SSH key → access to this machine → access to encrypted env vars → access to PayPal API

### Credential Setup

```bash
# Store PayPal credentials as OpenClaw secrets (never in plaintext files)
openclaw configure --section paypal

# Or set environment variables on the host
export PAYPAL_CLIENT_ID="your-client-id"
export PAYPAL_CLIENT_SECRET="your-client-secret"
export PAYPAL_MODE="sandbox"  # or "live"
```

## Usage

### Check Balance
```bash
# Get PayPal account balance
./scripts/paypal-balance.sh
```

### List Recent Transactions
```bash
# Last 7 days of transactions
./scripts/paypal-transactions.sh --days 7
```

### Monitor Incoming Payments
```bash
# Check for new payments since last check
./scripts/paypal-monitor.sh
```

### Fund Agent Credits
```bash
# Check if PayPal balance can cover Ampere credit purchase
./scripts/paypal-fund-agents.sh --amount 10 --target ampere
```

## API Endpoints Used

| Endpoint | Purpose |
|----------|---------|
| `POST /v1/oauth2/token` | Get access token |
| `GET /v1/reporting/balances` | Account balance |
| `GET /v1/reporting/transactions` | Transaction history |
| `POST /v2/payments/payouts` | Send payments |
| `GET /v1/notifications/webhooks` | Webhook management |

## Integration with Factory Economy

This skill connects the real-world economy (PayPal) to the internal agent economy (floor credits):

```
Real World (PayPal $)
    │
    ▼
paypal-secure-access skill
    │
    ▼
Ampere Credits (agent gas)
    │
    ▼
Agent Operations (token economy)
    │
    ▼
Deception Floor Commodities (internal value)
    │
    ▼
Production Output (real-world value)
    │
    ▼
Revenue → PayPal $ (cycle completes)
```

## Factory Origin

- **0:** No PayPal skill existed on ClawHub
- **1:** This skill was manufactured internally
- **Path B applied:** Built from PayPal's existing REST API docs (reframed, not rebuilt from scratch)
- **Private property:** `ironiclawdoctor-design` internal use only until published
