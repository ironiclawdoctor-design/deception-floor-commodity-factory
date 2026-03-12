# Factory Funding Module

## The Gas Problem

Agents consume credits (gas). Credits cost money. Money lives in PayPal. 

```
PayPal ($) ──→ Ampere Credits ──→ Agent Tokens ──→ Factory Output ──→ Revenue ──→ PayPal ($)
    │                                                                              │
    └──────────────────────── equity cycle ─────────────────────────────────────────┘
```

## 0→1: PayPal Skill

- **0:** No PayPal integration existed on ClawHub or anywhere in the agent ecosystem
- **1:** We manufactured `paypal-secure-access` skill — private property of this factory
- **Path B:** Built on PayPal's existing REST API (reframed their docs, didn't rebuild OAuth from scratch)

## Security Architecture

PayPal doesn't support SSH key auth. Their model is OAuth 2.0 over TLS. But SSH secures the *chain*:

```
SSH Key (ed25519)
  └── Authenticates to this server
        └── Server holds encrypted env vars
              └── Env vars contain PayPal OAuth credentials
                    └── OAuth credentials → Bearer Token
                          └── Bearer Token → PayPal API (TLS encrypted)
```

**The SSH key is the root of trust.** Everything downstream inherits from it.

## Available Operations

| Script | Purpose | Frequency |
|--------|---------|-----------|
| `paypal-auth.sh` | Get OAuth token | Per-session |
| `paypal-balance.sh` | Check available funds | On-demand / heartbeat |
| `paypal-transactions.sh` | Transaction history | On-demand |
| `paypal-monitor.sh` | Detect incoming payments | Cron / heartbeat |

## Setup Required

1. Create PayPal Developer App at [developer.paypal.com](https://developer.paypal.com)
2. Get Client ID + Client Secret
3. Store credentials:
   ```bash
   export PAYPAL_CLIENT_ID="your-id"
   export PAYPAL_CLIENT_SECRET="your-secret"
   export PAYPAL_MODE="sandbox"  # start with sandbox, switch to "live" when ready
   ```
4. Test: `./scripts/paypal-balance.sh`

## Augment Integration

The funding module feeds data to Augment for:
- Credit level monitoring (are we running low on gas?)
- Auto-alert when PayPal balance drops below threshold
- Revenue tracking (is the equity cycle positive?)
- Disruption prevention (fund before famine, not after)
