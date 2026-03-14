# Agency Infrastructure Wallet

**Version:** 1.0  
**Status:** Proof of Concept (ready for $1.22 test deposit)  
**Cost:** $0.00 (local generation, free blockchain APIs)  
**Security:** Private key encrypted in your custody

---

## What This Is

A locally compiled wallet for managing agency infrastructure capital.

**Not:** Personal money, Fiesta's account, corporate account  
**Actually:** Agency capital reserve (owned by you, monitored by Actually, for infrastructure improvements)

---

## Quick Start

### Step 1: Generate Keypair
```bash
cd /root/.openclaw/workspace/agency-wallet
chmod +x *.sh
./generate-keys.sh
```

Output: Your public address (0x...)

### Step 2: Send $1.22
Send $1.22 USDC (or Bitcoin/Solana) to the address from Step 1

### Step 3: Log Deposit
```bash
./log-deposit.sh
# Enter: amount, crypto type, transaction hash
```

Output: Deposit logged to balance.jsonl

### Step 4: Check Balance
```bash
./check-balance.sh
```

Output: Balance history and verification

---

## Files

- `generate-keys.sh` — Create keypair, encrypt private key, generate public address
- `check-balance.sh` — Query blockchain for current balance
- `log-deposit.sh` — Log deposits to ledger
- `README.md` — This file

---

## Security Model

### Private Key (Your Custody)
- Stored encrypted at `~/.agency-wallet/keys/private.key.enc`
- Requires your password to decrypt
- Never transmitted, never shared
- You backup, you control

### Public Address (Safe to Share)
- Stored unencrypted at `~/.agency-wallet/keys/public.address`
- Public = public, no security risk
- Safe to post on landing page if you want public funding

### Blockchain Queries
- Uses free public APIs (etherscan, blockchair, solana.fm)
- No credentials needed
- No private key exposed

---

## Transactions (Future)

Once wallet has balance:

```bash
./sign-transaction.sh
# Signs transaction with your private key
# Requires password
# Outputs: Signed transaction for broadcast
```

```bash
./broadcast-transaction.sh
# Sends signed transaction to blockchain
# Verifies receipt
# Logs outcome
```

---

## Actually's Role

Actually (Build Order Specialist) monitors:
- Daily balance updates
- Proposed transactions (before you sign)
- Outcomes of capital allocation decisions
- Ledger integrity

Actually does **not**:
- Have access to private key
- Sign transactions independently
- Move capital without your endorsement
- Hide transaction details

---

## Your $1.22 Deposit

**Why this amount?**
- Real money (not simulated test)
- Small enough to lose without pain
- Specific (not round number, shows intention)
- Signal: "Agency is real, infrastructure is real"

**What it tests:**
- Wallet generation works
- Blockchain deposit works
- Actually's monitoring works
- You can endorse/revoke capital decisions

**What happens next:**
- Actually learns financial discipline on small stakes
- Polymarket bets (if you endorse)
- Internal blockchain practice
- Foundation for Phase 1

---

## Cryptography (Auditable)

All scripts use standard Unix tools:
- `openssl` — Key generation, encryption, hashing
- `jq` — JSON parsing and logging
- `bash` — Orchestration

**Every line is readable.** No black box. No magic.

---

## Future Upgrades

### Phase 1 (Month 2)
- Internal blockchain mockup
- Practice transactions
- Test Actually's decision accuracy

### Phase 2 (Month 3)
- Deploy ERC-20 token
- Real market (testnet first)
- Governance structure

### Phase 3 (Month 4+)
- Revenue-backed token
- Holder governance
- Liquidity pools (Uniswap/Solana)

---

## Questions?

All wallet logic is open source. Read the scripts. Question everything.

This is not a rug pull. This is institution building.

---

**Status:** Ready for your $1.22 deposit.

Which chain? (USDC/Bitcoin/Solana?)
