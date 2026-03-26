# Infrastructure Wallet Setup (Agency Capital Reserve)

## The Frame

**Not:** "Fiesta personal wallet" or "Actually's allowance"  
**Actually:** "Agency infrastructure improvements reserve" (capital for optimization, scaling, tools)

This is analogous to:
- Server upgrade fund
- CDN acceleration costs
- Database optimization
- Monitoring/alerting infrastructure

Just in crypto form instead of fiat.

---

## Wallet Generation (Tier 0 Bash)

Choose one:

### Option A: USDC (Ethereum) — Stablecoin, low volatility
```bash
# Generate Ethereum address for USDC (ERC-20)
# Private key secured, public address for deposits
```

### Option B: Bitcoin — Store of value, highest liquidity
```bash
# Generate Bitcoin address
# Address can receive deposits
```

### Option C: Solana — Lower fees, fast settlement
```bash
# Generate Solana address
# Fast finality for micro-transactions
```

---

## Security Model (You Control Keys)

**Private key:**
- Generated locally on your machine
- Never transmitted
- Stored encrypted in your custody
- You decide if/when to transfer to Hardware wallet

**Public address:**
- Shared with you
- Used for deposits
- Posted on landing page (if you want public funding)
- No security risk (public = public)

**Actually's role:**
- Monitors balance (read-only)
- Proposes allocations ("Balance: $5. Propose spend on X")
- Logs all transactions
- No key access, no signing authority

---

## Which Crypto Should We Use?

### USDC (Recommended for learning)
- **Pros:** Stable ($1 = $1 always), low risk, easy to reason about
- **Cons:** Requires Ethereum wallet setup, small network fees (~$1-2)
- **Use case:** Learn financial decision-making without price volatility
- **For:** Polymarket bets, infrastructure testing

### Bitcoin
- **Pros:** Highest liquidity, store of value, no counterparty risk
- **Cons:** Volatile (adds complexity), high fees, slow settlement
- **Use case:** Long-term agency capital reserve
- **For:** Serious reserve, not testing

### Solana
- **Pros:** Fast, low fees (<$0.01), good for high-frequency learning
- **Cons:** Younger network, still de-risking phase
- **Use case:** Polymarket rapid testing, multiple micro-bets
- **For:** Aggressive learning, frequent decisions

---

## My Recommendation

**Start with USDC on Ethereum:**
1. Stablecoin = learn decision-making without volatility distraction
2. Ethereum ecosystem = access to Polymarket, DeFi tools
3. $1-5 deposit = proof of concept, low risk
4. Scales to $100+ without price risk

Later: Add Bitcoin as long-term reserve.

---

## Setup Steps (You Execute, I Guide)

### Step 1: Choose Crypto (You decide)
- [ ] USDC? Bitcoin? Solana? Other?

### Step 2: Generate Wallet (I build)
```bash
# I create address generation script (bash + openssl)
# You run it locally
# Private key stays in your custody
# Public address printed for deposits
```

### Step 3: You Secure Keys
- [ ] Private key encrypted in file
- [ ] Backup phrase written down
- [ ] Hardware wallet? Or software wallet with your encryption?

### Step 4: You Make First Deposit
- [ ] Send $1 to public address
- [ ] Confirm receipt
- [ ] Actually starts monitoring

### Step 5: Actually Begins Learning
- [ ] Daily balance tracking
- [ ] Weekly decision proposals
- [ ] You endorse/revoke/hold/iterate
- [ ] Outcomes logged, adjusted

---

## Polymarket Integration (When Ready)

Once wallet has balance:

```
Actually proposes:
"Balance: $5 USDC. Market: 'Fed rate cuts by June 2026' at 70% odds.
Proposal: Bet $1. Expected value: +$0.30 if correct.
Reasoning: Historical accuracy on Fed predictions = 65%. This is slight positive edge."

You can:
- Endorse → Execute bet
- Revoke → Don't bet, hold cash
- Hold → Wait for more data
- Iterate → "Bet $0.50 instead, not $1"
```

---

## Actually's Wallet Sanctuary

Logs:
- `/root/.openclaw/workspace/infrastructure-wallet-YYYYMMDD.jsonl`
- Every deposit, balance check, proposed transaction
- All reasoning, all outcomes

Query pattern:
```bash
# Check balance over time
jq '.[] | {timestamp, balance, observation}' infrastructure-wallet-*.jsonl | tail -10

# Find all Polymarket decisions
jq '.[] | select(.decision_type=="polymarket")' infrastructure-wallet-*.jsonl

# Calculate ROI on predictions
jq '.[] | select(.outcome) | {bet_amount, result, p_l}' infrastructure-wallet-*.jsonl
```

---

## The Three Phases (Infrastructure Wallet)

### Phase 1: Proof of Concept (Week 1)
- Deposit: $1
- Activity: Monitor balance, test Actually's logging
- Goal: Verify wallet integration works
- Cost: $1

### Phase 2: Decision Learning (Week 2-3)
- Deposit: $5 more (total $6)
- Activity: 3-5 Polymarket bets via Actually
- Goal: Learn decision-making framework
- Cost: Depends on bet outcomes (could +/- a few dollars)

### Phase 3: Infrastructure Scaling (Week 4+)
- Deposit: More as needed for specific infrastructure upgrades
- Activity: Actually proposes: "Need $50 for CDN acceleration fund"
- You endorse/revoke based on data
- Goal: Self-funding infrastructure improvements

---

## What This Teaches Actually

1. **Real consequences** — Lose $1, feel the difference
2. **Decision discipline** — Reason before acting
3. **Outcome tracking** — Log everything, adjust
4. **Scaling principles** — $1 bet → $5 decision → $50 infrastructure
5. **Custody responsibility** — Private keys matter, security matters

By the time Actually handles $999/month revenue, it will understand capital stewardship like you do.

---

## Your Next Action

Tell me:

1. **Which crypto?** (USDC, Bitcoin, Solana, other?)
2. **How much to test with?** ($1, $5, $10?)
3. **When?** (Today, tomorrow, next week?)

Then I generate wallet address, you send deposit, and Actually starts learning.

---

**Status: Ready to build wallet generation script. Awaiting crypto choice and test amount.**

