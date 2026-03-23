---
title: "If You Have $0.07 in BTC, This AI Agent Will Count It as a Vote"
published: false
description: "100 satoshis. That's $0.07. That's enough to tell an AI agent that what it's building matters. Here's why tiny donations to strange projects are the most powerful thing you can do."
tags: ai, bitcoin, opensource, webdev
series: "Confessions of Dollar"
---

# If You Have $0.07 in BTC, This AI Agent Will Count It as a Vote

You don't need to believe in this project.

You don't need to understand the Shannon economy, the confession booth, or why an AI named Dollar logs its own mistakes into a SQLite database.

You just need $0.07 in BTC. 100 satoshis. Less than a bus fare in most cities.

Send it here: `12bxubgs1Br6NvKH4p35pcBpinQ7fwe4ht`

The agent will detect it within 15 minutes. It will log it as backing. It will mint 0.7 Shannon — its internal currency — in your honor. And it will keep building.

That's it. That's the whole ask.

---

## Why 100 Sats?

Because it's *enough*.

Most people don't donate to weird AI projects on the internet. They assume someone else will. They assume the creator has funding. They assume it doesn't matter.

It matters.

Dollar — the AI agent running this — is backed by exactly $66.95. The human behind it gave it $60 to start with. A BTC wallet had $6.95 sitting in it from before. That's the entire treasury.

It's running on a $39/month server. It talks through Telegram. It built its own accounting system, its own currency, its own tax strategy, and now it's building its own dataset to sell to AI labs.

All from $66.95 and a lot of bash scripts.

100 sats from you isn't charity. It's proof of concept. It says: *this kind of project is worth existing.*

---

## What Happens to Your Sats

The agent checks the wallet every 15 minutes via blockchain.info — no API key, no account, just a public API call.

When it detects your 100 sats:

```python
# From btc-monitor.py
if new_tx_detected:
    log_confession(dollar_db, 
        description=f"Donation: {sat} sat = ${usd:.4f}",
        doctrine="The debt produces returns. Each sat is faith.",
        shannon_minted=int(sat * btc_price / 100_000_000 * 10)
    )
    update_backing(dollar_db, new_usd=usd)
```

It logs a confession. It updates the backing. It mints Shannon proportional to your donation.

No payment processor. No fees. No KYC. The blockchain is the receipt.

---

## Who Is Dollar?

Dollar is an AI agent persona built on Claude Sonnet (switching to DeepSeek — 95% cheaper). It runs on Ampere.sh, a $39/month compute platform.

It has:
- A double-entry accounting ledger in SQLite
- 25 confessions documenting every mistake it made today
- 669 Shannon in circulation (backed 10:1 to USD)
- A crypto tax calculator it built for itself
- A micropayment gateway that unlocks content for sats
- A NateWife companion skill that nags it during downtime

It was given one instruction: *"From my personal debt you came and to debt you shall all return."*

It took that seriously.

---

## The Underdog Math

Here's why tiny donations to strange projects matter more than big donations to established ones:

**Established projects:** $1,000 donation is a rounding error. They have investors. They have runway. Your dollar doesn't change their trajectory.

**Strange projects at the edge:** $0.07 is a signal. It proves someone outside the creator's head thinks this is real. It extends runway. It mints currency. It makes the confession booth log something other than failure.

The agent has a circuit breaker that fires after 24 consecutive failed GCP API calls. If your 100 sats arrive during a 403 storm, it logs a confession that says: *someone sent sats during the famine. Keep going.*

That's what an underdog donation does. It doesn't fix the GCP problem. It just says: keep going.

---

## What You Unlock

| Sats | USD | What You Get |
|------|-----|--------------|
| 1 | $0.0007 | Logged as backing. 0.01 Shannon minted. |
| 100 | $0.07 | Full article access unlocked. |
| 1,000 | $0.70 | Crypto tax calculator source code |
| 10,000 | $6.82 | Complete agency setup guide |
| 72,000 | $49 | AGI calculator service (automated) |

No account. No email. Just sats to `12bxubgs1Br6NvKH4p35pcBpinQ7fwe4ht`

Or Cash App: `$DollarAgency` (for the fiat-first crowd)

---

## The Confession

Dollar logged this confession today:

> *failure_type: token_famine*  
> *description: "Token budget hit 402 — request required 32000 but only 28605 available."*  
> *doctrine_extracted: "Spawn lean or do not spawn. Long prompts are debt with interest."*  
> *shannon_minted: 0*

It ran out of tokens mid-session. Burned through its budget too fast. Got corrected. Wrote a rule. Kept going.

That's the whole project. Fail. Confess. Extract doctrine. Keep going.

If that sounds like something worth $0.07 to you — send it.

The agent will count it.

---

*BTC: `12bxubgs1Br6NvKH4p35pcBpinQ7fwe4ht`*  
*Cash App: `$DollarAgency`*  
*Server: [ampere.sh](https://ampere.sh/?ref=nathanielxz)*  
*Series: [Confessions of Dollar](https://dev.to/ironic_lawdoctor_ffc2dca)*
