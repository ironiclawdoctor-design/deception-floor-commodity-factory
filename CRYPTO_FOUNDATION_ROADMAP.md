# Agency Crypto Foundation Roadmap (2026-03-14)

## The Vision

Not a rug pull. A solid foundation for the agency's own crypto.

**Phase 0 (Now):** Learn on external crypto + build local wallet software  
**Phase 1 (Month 2):** Test internal blockchain infrastructure  
**Phase 2 (Month 3):** Deploy agency token (ERC-20 or custom chain)  
**Phase 3 (Month 4+):** Revenue-backed token, real utility  

---

## Phase 0: Foundation (This Week)

### Your $1.22 Deposit (Test Signal)

You send $1.22 (specific amount, intention-based) to locally compiled wallet.

**Why $1.22?**
- Real money, not fake test
- Small enough to lose without pain
- Specific enough to track (not round number)
- Testing signal: "This infrastructure is real"

### Locally Compiled Wallet Software (I Build This Week)

Not MetaMask. Not Ledger. **Your wallet, compiled locally.**

```bash
# /root/.openclaw/workspace/agency-wallet/
# Generated wallet software (bash + crypto libs)
# Private key stays encrypted on your machine
# Public address for deposits
# Balance tracking via blockchain API (free tier)
```

**Tech stack:**
- Bash for key generation
- OpenSSL for encryption
- Free blockchain API (etherscan, solana.fm, blockchair)
- Zero external dependencies for private key handling
- Auditable source (you can read every line)

### Actually's Role (Week 1)

1. Monitor $1.22 deposit confirmation
2. Log receipt in infrastructure-wallet-20260314.jsonl
3. Confirm wallet software works
4. Report: "Foundation test successful. Ready for Phase 1."

---

## Phase 1: Internal Infrastructure (Month 2)

### Build Local Blockchain Mockup

```bash
# /root/.openclaw/workspace/agency-chain/
# Proof of concept: Internal ledger blockchain
# Demonstrates: Can we build our own chain?
# Not yet mainnet, but testnet-ready
```

**What it does:**
- Tracks transactions internally (JSON-based ledger)
- Generates blocks (Fiesta signs them)
- Verifies chain integrity (cryptographic hashing)
- Ready to connect to real blockchain later

### Actually's Job (Month 2)

1. Run transactions through internal chain
2. Log each block
3. Compare accuracy vs. external crypto (USDC)
4. Report: "Internal ledger is X% accurate. Ready for Phase 2."

---

## Phase 2: Deploy Agency Token (Month 3)

### Option A: ERC-20 (Ethereum)

```solidity
// AGENCY token on Ethereum
// 1 AGENCY = ?
// Backed by: Agency capital + revenue commitment
// Utility: Governance, access to agency tools
```

**Advantages:**
- Ethereum ecosystem maturity
- Liquidity pools available
- Clear regulatory path
- Real adoption possible

**Disadvantages:**
- Ethereum network fees
- Requires mainnet launch (real cost)

### Option B: Custom Chain (More Ambitious)

```bash
# Fork Solana or Cosmos
# Deploy agency-specific blockchain
# 1 AGENCY token = governance + capital share
```

**Advantages:**
- Full control
- Lower fees
- Custom mechanics
- True decentralization

**Disadvantages:**
- Complexity
- Validator requirements
- Network security harder

**My recommendation:** Start ERC-20 (easier, faster proof). Upgrade to custom chain later if traction justifies it.

---

## Phase 3: Revenue-Backed Token (Month 4+)

### The Model

```
Agency Revenue → AGENCY Token Backing

Month 1: 0 users, token = concept
Month 3: 30 users @ $9.99/month = $300 MRR
         AGENCY token now backed by $300/month revenue
Month 6: 100 users = $999/month
         Token = actual asset (backed by real revenue)
```

### Token Utility

1. **Governance:** Holders vote on feature priorities
2. **Revenue share:** Holders get % of monthly revenue
3. **Access:** Holders get special tier (lower cost or premium features)
4. **Liquidity:** Can trade on Uniswap or Solana DEX

### Actually's Job (Month 4+)

1. Monitor token price vs. fundamental value
2. Recommend buybacks if undervalued
3. Propose expansion if overvalued
4. Track holder sentiment
5. Report quarterly to you

---

## Locally Compiled Wallet (This Week's Deliverable)

### What I'll Build

```bash
/root/.openclaw/workspace/agency-wallet/
├── generate-keys.sh          # Generate keypair, encrypt private key
├── check-balance.sh          # Query blockchain for balance
├── sign-transaction.sh       # Sign with private key
├── verify-transaction.sh     # Verify blockchain receipt
├── monitor.sh                # Continuous balance monitoring
├── README.md                 # Full docs, audit trail
└── tests/
    └── test-deposit.sh       # Verify $1.22 receipt
```

**Security model:**
- Private key stored encrypted in `~/.agency-wallet/keys/`
- You provide password to decrypt
- All transactions logged to SQLite
- Source code fully auditable (100 lines of bash)

### Your $1.22 Test

```bash
# Step 1: You run wallet generator
$ ./agency-wallet/generate-keys.sh
# Output: Public address (e.g., 0x123abc...)

# Step 2: You send $1.22 USDC to that address
# (From your wallet to agency wallet)

# Step 3: I verify receipt
$ ./agency-wallet/check-balance.sh
# Output: Balance: $1.22 USDC

# Step 4: Actually logs it
# Timestamp: 2026-03-14T17:09:00Z
# Event: deposit_confirmed
# Amount: $1.22
# Status: Foundation test successful
```

---

## Actually's Crypto Learning (Parallel Track)

While you're testing local wallet software:

Actually will:
1. Study blockchain architecture (Bitcoin, Ethereum, Solana whitepapers)
2. Model token economics (supply, demand, pricing)
3. Research governance models (vote mechanisms, token distribution)
4. Identify risks (security, regulatory, market)
5. Propose: "If agency builds token, recommend X approach because Y"

**Cost:** $0.00 (all Tier 0-2, free research)

---

## Timeline (Aggressive But Realistic)

```
Week 1 (Now):
  - Build locally compiled wallet software
  - You send $1.22
  - Actually logs and verifies
  - ✓ Foundation test complete

Week 2-3:
  - Build internal blockchain mockup (JSON ledger)
  - Run practice transactions
  - Compare accuracy
  - ✓ Internal infrastructure proven

Week 4-6:
  - Deploy ERC-20 token (if you endorse)
  - List on testnet first
  - Get community feedback
  - ✓ Agency token exists

Month 2:
  - Upgrade to custom chain (optional)
  - Increase utility
  - Build governance

Month 3+:
  - Revenue-backed token
  - Real market value
  - Actual investor interest
  - ✓ Agency has its own asset class
```

---

## What This Teaches Actually

1. **Cryptography** — Keys, signing, verification
2. **Economics** — Token supply, demand, pricing
3. **Governance** — Who decides, how, when
4. **Risk management** — Regulatory, security, market
5. **Building blocks** — How to go from concept to real asset

By Month 3, Actually understands crypto better than 99% of people.

---

## Your $1.22 Deposit

**Meaning:**
- Real money (not test)
- Foundation signal (this is happening)
- Actually's first financial responsibility
- Proof that agency can accept capital

**Next steps:**

1. **Endorse:** Build locally compiled wallet software this week
2. **Specify:** Which chain? (USDC on Ethereum? Bitcoin? Solana?)
3. **Timeline:** Ready to send $1.22 when? (Today? Tomorrow?)

Then I build the wallet, you deposit, Actually learns, and we're on the path to agency crypto.

---

**This is not a rug pull. This is institution building.**

