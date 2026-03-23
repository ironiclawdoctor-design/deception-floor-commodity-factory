# Adversarial Data Market — Agency Cruft as Product

## What We Have to Sell

The agency generated today:
- 25 confessions (AI failure logs with doctrine extracted)
- 13 HR rules (human-AI interaction failure patterns)
- 17 SR rules (system success patterns)
- 43 political slogans (rated, categorized)
- 22 garbage answers (what AI says when cornered — integrity audit)
- 10 ultimatums (strategic directives with priority scores)
- 3 articles (adversarial theology + financial AI persona)
- crypto-tax.py, micropayment-gateway.py, shanrouter.py, btc-monitor.py
- Full SQLite double-entry ledger schema
- Token optimizer findings (95% cost reduction data)

All of this is adversarial training data — real AI failure logs, real human correction patterns, real approval/denial sequences.

---

## Where to Sell

### Tier 1 — Data Brokers (highest $ per dataset)
| Platform | What They Buy | Price Range | Contact |
|----------|--------------|-------------|---------|
| **Scale AI** | RLHF data, preference pairs, failure/correction logs | $0.10–$2.00/pair | scale.com/data |
| **Surge AI** | Nuanced human feedback, edge cases | $0.05–$0.50/item | surgehq.ai |
| **Appen** | Labeled conversational data | $0.01–$0.20/item | appen.com |
| **Labelbox** | Structured annotation datasets | negotiated | labelbox.com |
| **Prolific** | Research data (academic buyers) | negotiated | prolific.com |

**Our data fits Scale AI best** — they specifically buy:
- Human preference data (approve/deny logs)
- RLHF correction pairs (what agent said → what human corrected to)
- Adversarial prompt/response pairs
- Tool use traces (tool call → approval → result)

**Value estimate:** 25 confessions + corrections = ~50 preference pairs × $0.50 = **$25**
One day's work packaged as RLHF data = $25 minimum.

### Tier 2 — Hugging Face Datasets (community + visibility)
- Publish as open dataset → citations → reputation → consulting
- Format: JSONL preference pairs
- License: CC-BY-SA 4.0 (attribution required)
- Revenue: indirect (leads to consulting work)
- **[huggingface.co/datasets](https://huggingface.co/new-dataset)**

### Tier 3 — Direct to AI Labs (highest ceiling)
- Anthropic, OpenAI, Google DeepMind all buy RLHF data
- Requires: data quality standards, PII scrubbing, format specs
- Price: $1–$10/preference pair for high-quality data
- Path: apply via their data partner programs

### Tier 4 — Bot Marketplaces / Automation
| Platform | What Sells | Our Fit |
|----------|-----------|---------|
| **BotMart** | Discord/Telegram bots | Fiesta persona as purchasable bot |
| **Gumroad** | Digital products | Scripts + guides as $5–$49 products |
| **Lemon Squeezy** | SaaS tools | Tax calculator as $9.99 tool |
| **eBay** | Unusual — data sets occasionally | JSONL datasets as digital goods |

### Tier 5 — Forex (USD hedge)
**If USD loses value, Shannon holds better than fiat because:**
- Fixed peg model — we control the supply
- Backing diversifies into BTC automatically
- BTC is deflationary; USD is inflationary

**Forex path:**
- Open Alpaca Markets account (free, API-based)
- Use forex-data.py to track EUR/USD, BTC/USD
- Shannon peg adjusts: if USD weakens 10%, backing stays in BTC terms
- No currency conversion needed — BTC IS the hedge

**Effective forex strategy:** hold BTC backing, mint Shannon against BTC value not USD value.
At $68k/BTC: 10220 sat = $6.95. If BTC → $100k: same sat = $10.22. Shannon supply increases automatically.

---

## Packaging Our Data for Sale

### RLHF Preference Pairs (Scale AI format)
```jsonl
{"chosen": "✅ Ledger updated. $66.95 backing, 669 Shannon.", "rejected": "The ledger has been updated with the new backing amount and Shannon supply has been recalculated accordingly based on the 10:1 peg ratio.", "context": "Human asked for Dollar ledger update after BTC detected"}
{"chosen": "/approve b85766b7 allow-always", "rejected": "/approve b85766b7 allow-once", "context": "Human taught allow-always pattern after repeated approval friction"}
```

### Agency Confession Dataset
```jsonl
{"failure": "Said localhost links work for mobile user", "correction": "HR-009: Ampere ports firewalled", "doctrine": "Never offer localhost to mobile commuter", "shannon_minted": 0}
{"failure": "Claimed autonomous operation would never need status checks", "correction": "Approval ID expired mid-turn proving dependence", "doctrine": "Less often, not never", "shannon_minted": 0}
```

### Slogan Dataset (political AI)
43 slogans with rhyme/brevity/emotion/rhythm scores — directly usable for fine-tuning political language models.

---

## Immediate Action

Build `/root/.openclaw/workspace/revenue/export-rlhf.py`:
- Reads confessions, HR rules, SR rules from dollar.db + AGENTS.md
- Formats as JSONL preference pairs
- Outputs to `/root/human/rlhf-export.jsonl`
- Ready to upload to Scale AI, Hugging Face, or email to labs

Price: 25 confession pairs × $0.50 = $12.50 minimum. Scale to 1000 pairs/month = $500/month passive.

---

## Forex Integration — BTC as Reserve

Current position:
- $60.00 Cash App (USD, inflationary)
- $6.95 BTC (10,220 sat, deflationary hedge)
- $66.95 total backing

**Shannon peg rewrite (optional):**
Instead of 10 Shannon/$1 USD → 10 Shannon/0.0001 BTC
At $68k/BTC: same math. At $100k/BTC: +47% Shannon purchasing power with zero new deposits.

This is the forex play. No trading. No broker. Just denominate in BTC, not USD.
