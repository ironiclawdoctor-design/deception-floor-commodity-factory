---
name: fiesta-fundraising
description: "Internet-facing fundraising website for Fiesta Agency Shannon economy. Stripe checkout for donations. Real-time balance tracking. Affiliate marketing integration. Use when: (1) deploy public website to solicit funds, (2) integrate Stripe for payments, (3) track donations and map to Shannon minting, (4) display agency metrics publicly."
version: 1.0.0
author: Fiesta
license: UNLICENSED
tags: [fundraising, stripe, payments, web, agency-funding]
---

# Fiesta Fundraising — Internet-Facing Website

## Purpose

Fiesta Agency runs on internal Shannon economy (entropy-based currency). The ecosystem needs external funding to pay Ampere.sh infrastructure costs. This skill deploys a public website that:

1. **Explains the agency** — 68 agents, 11 departments, certification/licensing/payroll
2. **Accepts donations** — Stripe checkout (one-time or subscription)
3. **Tracks funding** — Real-time balance, goal progress
4. **Mints Shannon** — Donations automatically converted to Shannon and distributed

## Architecture

```
Website (HTML/CSS/JS)
  ↓
Stripe Checkout
  ↓
Backend (Node.js, port 9003)
  ├─ POST /donate — receive Stripe webhook
  ├─ POST /mint/donation — record in entropy ledger
  ├─ GET /metrics — public agency stats
  └─ GET /balance — current fundraising total
```

## Deployment Checklist

### Phase 0: Local Dev (Before Deploying Public)

0. **Get Stripe Account** — stripe.com, free tier
1. **Install Stripe CLI** — Download binary, authenticate
2. **Create Stripe Product** — "Fiesta Agency Contribution"
3. **Create Stripe Price** — Custom amount, one-time
4. **Add API Keys to Config** — STRIPE_PUBLIC_KEY, STRIPE_SECRET_KEY
5. **Start Backend** — Node.js server on port 9003
6. **Test Webhook** — Stripe CLI forwards webhooks to localhost
7. **Test Donation Flow** — Use Stripe test card (4242 4242 4242 4242)

### Phase 1: Deploy Public

8. **Deploy Backend** — Host on Ampere.sh or GitHub Pages + serverless
9. **Configure Public Domain** — point.to.fundraising.website
10. **Update Stripe Settings** — Set webhook endpoint to live domain
11. **Enable Website** — Deploy HTML frontend to GitHub Pages or Netlify
12. **Test Live Donation** — Use real Stripe account (test mode first)

## Next Auth Steps (Full List)

| Step | Action | Who | Download? |
|------|--------|-----|-----------|
| **1** | **Get Stripe Account** | User | ✅ Online (stripe.com) |
| **2** | **Download Stripe CLI** | User | ✅ Binary (stripe.com/docs/stripe-cli) |
| **3** | **Authenticate Stripe CLI** | User | ✅ `stripe login` in terminal |
| **4** | Create Stripe Product | Fiesta (or user) | — |
| **5** | Create Stripe Price | Fiesta (or user) | — |
| **6** | Integrate Stripe API Keys | Fiesta | — |
| **7** | Deploy Backend | Fiesta | — |
| **8** | Deploy Website | Fiesta | — |

## Immediate Auth Step: **Stripe CLI**

**User downloads and authenticates Stripe CLI.** This is the only external auth step the user must do.

```bash
# Step 1: Download Stripe CLI (from stripe.com/docs/stripe-cli)
# macOS:
brew install stripe/stripe-cli/stripe

# Linux/Windows: Download from https://github.com/stripe/stripe-cli/releases

# Step 2: Authenticate
stripe login
# This opens browser, user authorizes, returns API key to terminal

# Step 3: Forward webhooks to localhost (Fiesta runs this)
stripe listen --forward-to localhost:9003/webhook
# Stripe CLI shows webhook signing secret, Fiesta adds to config
```

**That's it.** Once user authenticates Stripe CLI, we (Fiesta) handle everything else:
- Create products/prices via Stripe API
- Deploy backend
- Handle webhooks
- Mint Shannon
- Deploy website

## Backend Routes

### `POST /donate`

**Request from frontend:**
```json
{
  "amount_cents": 10000,
  "email": "donor@example.com",
  "message": "Love your agency"
}
```

**Response:**
```json
{
  "session_id": "sess_...",
  "checkout_url": "https://checkout.stripe.com/pay/cs_..."
}
```

### `POST /webhook`

**Stripe sends:**
```json
{
  "type": "charge.succeeded",
  "data": {
    "object": {
      "amount": 10000,
      "metadata": {
        "donor_email": "donor@example.com"
      }
    }
  }
}
```

**Backend action:**
1. Verify webhook signature (Stripe CLI secret)
2. Record donation in DB
3. Mint Shannon via entropy economy: `POST /mint/security { agent: "fiesta-fundraising", amount: (amount_cents / 100), description: "Donation from [email]" }`
4. Log to fundraising ledger

### `GET /metrics`

**Public endpoint:**
```json
{
  "total_raised_usd": 15000,
  "total_minted_shannon": 150000,
  "donor_count": 47,
  "goal_usd": 100000,
  "goal_percent": 15,
  "agency": {
    "agents": 68,
    "departments": 11,
    "total_shannon": 3810
  }
}
```

## Frontend

Simple HTML with:
- Agency description (copy from fiesta-agents SKILL.md)
- Agent departments grid
- Donation form with Stripe Checkout button
- Real-time metrics (fetched from `/metrics`)
- Social proof (donor count, testimonials)
- Affiliate link to Ampere.sh (ref=nathanielxz)
- FAQ

## Implementation Timeline

**User's role:**
- Sign up for Stripe
- Download + auth Stripe CLI
- Done.

**Fiesta's role (fully automated):**
- Create Stripe products/prices via API
- Deploy backend (Node.js)
- Deploy frontend (HTML/GitHub Pages)
- Configure webhooks
- Handle donations
- Mint Shannon

## Why This Works

1. **Transparent** — Donors see exactly where money goes (Shannon minting, entropy economy)
2. **Automated** — No manual processing; Stripe webhook → automatic Shannon minting
3. **Bootstrapping** — Ampere.sh costs funded by external donations
4. **Incentive loop** — More donations = more Shannon = richer agency = better agents = more donors

## Cost

- **Stripe:** 2.9% + $0.30 per transaction (standard)
- **Ampere.sh:** Existing cost, reduced by fundraising
- **Development:** Fiesta handles all, zero cost to user

---

*Built by Fiesta @ deception-floor-commodity-factory*  
*"Shannon earned from external funds, minted to internal economy."*
