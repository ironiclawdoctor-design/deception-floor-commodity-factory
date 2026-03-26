# QR Code Onboarding System (Crypto Deposit)

## The Problem

Crypto onboarding is friction-heavy:
1. Sender gets address (text, copy/paste error prone)
2. Sender sends crypto
3. Sends to wrong address/network
4. Crypto is lost (void/chaos, non-recoverable)
5. No accountability, no logging

## The Solution

**QR code deposit flow with risk acknowledgment and down-payment logging.**

---

## Workflow

### Step 1: You Generate QR Code (Once)
```bash
cd /root/.openclaw/workspace/agency-wallet
./generate-qr-deposit.sh
# Input: Crypto type (USDC/Bitcoin/Solana), expected amount
# Output: QR code (ASCII + PNG)
```

**Output Example:**
```
┌─────────────────────────────┐
│ ▄▄▄▄▄ ▀█ ▀ █ ▄▄▄▄▄ │
│ █   █  █▄█   █   █ │
│ █ ▄ █  █ ▄▀█ █ ▄ █ │
│ █▄█▄█ ▀█▄ ▀▄ █▄█▄█ │
│ ▄▄▄▄▄ ▀  █▄█ ▄▄▄▄▄ │
│ ethereum:0x123abc... │
└─────────────────────────────┘
```

**Files Created:**
- `qr-USDC-20260314-171600.txt` (ASCII for email/chat)
- `qr-USDC-20260314-171600.png` (PNG for web/print)

### Step 2: Sender Scans QR Code
1. Opens wallet (MetaMask, Trust Wallet, etc.)
2. Taps "Scan QR"
3. Points at QR code
4. Wallet auto-fills address
5. Sends crypto

**Friction Reduced:** Zero copy/paste errors (machine-scanned)

### Step 3: Crypto Arrives (Ideal Case)
```bash
./log-deposit.sh
# Input: Amount, crypto type, transaction hash
# Logs to balance.jsonl
```

**Status:** ✅ Deposit confirmed, balance updated

### Step 4: Wrong Send (Risk Case)
If sender used wrong network or address:

```bash
./log-down-payment.sh
# Input: Crypto type, amount lost, reason
# Logs to delinquent-accounts.jsonl
```

**What Happens:**
1. Lost crypto logged as "down payment on seriously delinquent accounts"
2. Triggers governance review
3. Pattern tracked: Is this a UX problem or user error?
4. Restitution: Governance decides

---

## Risk Model: Void/Chaos

**Reality:** Wrong send = lost crypto, non-recoverable

**Our Approach:**
- Don't hide it
- Don't blame sender (usually UX failure, not malice)
- Log it systematically
- Govern restitution as policy decision

### Down Payment Logic

When crypto is lost:
- It's treated as payment into "seriously delinquent accounts"
- Void/chaos becomes an asset (entropy owed)
- Governance can decide: reimburse? hold? use for UX improvement?

**Philosophy:**
- Money is real, loss is real
- Accountability (everything logged)
- Transparency (no hidden losses)
- Governance (humans decide fairness)

---

## Implementation Details

### QR Generation
Uses Python `qrcode` library (installed):
- `python3-qr` for ASCII terminal display
- `qrcode` module for PNG generation

**Crypto URL Schemes:**
- USDC: `ethereum:0x...`
- Bitcoin: `bitcoin:...`
- Solana: `solana:...`

**Amount Optional:**
- `ethereum:0x123abc...?amount=1.22` (for precision)
- Wallet auto-fills if present

### Risk Logging
```json
{
  "timestamp": "2026-03-14T17:16:00Z",
  "event": "crypto_lost",
  "crypto": "USDC",
  "amount": "1.22",
  "sender": "First-time user",
  "reason": "Sent to wrong network (Polygon instead of Ethereum)",
  "status": "down_payment_logged",
  "note": "Void/chaos = entropy owed. May trigger governance restitution consideration."
}
```

**Queryable:**
```bash
# Find all lost crypto
jq '.[] | select(.event=="crypto_lost")' delinquent-accounts.jsonl

# Total lost (sum)
jq '.[] | select(.event=="crypto_lost") | .amount' delinquent-accounts.jsonl | \
  awk '{sum+=$1} END {print "Total lost: $" sum}'

# Patterns (most common reason)
jq '.[] | select(.event=="crypto_lost") | .reason' delinquent-accounts.jsonl | sort | uniq -c
```

---

## Files

### In `/root/.openclaw/workspace/agency-wallet/`

- `generate-qr-deposit.sh` — Generate QR code for deposit
- `log-down-payment.sh` — Log lost crypto as down payment
- `qr-codes/` — Directory containing generated QR codes
  - `qr-USDC-*.txt` (ASCII for email)
  - `qr-USDC-*.png` (PNG for web)
- `delinquent-accounts.jsonl` — All lost-crypto entries
- `balance.jsonl` — All deposits logged

---

## Usage Patterns

### Pattern 1: Public Fundraising (Website)
```html
<!-- Post QR code on landing page -->
<section id="support">
  <h2>Support Agency Development</h2>
  <img src="qr-USDC-20260314.png" alt="Scan to deposit USDC">
  <p>Scan to send crypto (USDC/Bitcoin/Solana)</p>
  <small>Wrong network? Logged as down payment, may trigger restitution.</small>
</section>
```

### Pattern 2: Private Circle (Discord/Telegram)
```
💰 Send USDC → Scan QR → Agency gets funded

QR Code:
[ASCII art here]

⚠️ Warning: Double-check network before sending!
Wrong network = down payment on seriously delinquent accounts.
Governance may reimburse, but it's queued for review.
```

### Pattern 3: Governance Review (Monthly)
```bash
# Check delinquent accounts
./agency-wallet/log-down-payment.sh --summary

# Output:
# Total lost: $12.30
# Common reason: Wrong network (8 cases)
# Restitution decided: Reimburse 3 cases, hold 5 for UX review

# Execute restitution (if approved)
./agency-wallet/reimburse-delinquent.sh --approve 3
```

---

## Security Notes

### Private Key Safety
- Private key stays encrypted, never used by QR generation
- QR only encodes public address (safe to post publicly)
- No signing authority in QR code

### Network Safety
- URL scheme (`ethereum:`, `bitcoin:`) triggers wallet validation
- Wallet checks network before sending
- Our end: logs all sends + all losses

### Accountability
- Every send logged (balance.jsonl)
- Every loss logged (delinquent-accounts.jsonl)
- Governance can audit both

---

## Cost

- **QR generation:** $0.00 (bash + Python, local)
- **QR hosting:** $0.00 (PNG on GitHub Pages)
- **Risk logging:** $0.00 (JSON lines, local storage)
- **Restitution:** Paid from agency revenue (governance decision)

---

## Philosophy

**Not a rug pull.** Void/chaos acknowledgment.

- Risk is real (crypto loss is non-recoverable)
- We own it (log everything, no hiding)
- We govern it (humans decide fairness)
- We improve from it (pattern analysis → UX fixes)

QR code makes deposit **easier**. Down-payment logging makes loss **accountable**.

---

## Next Steps (Your Call)

1. **Generate QR codes** (one per crypto type)
2. **Post on landing page** (or share in private circle)
3. **Monitor delinquent-accounts.jsonl** (watch for patterns)
4. **Govern restitution** (monthly review, approve/hold/deny)

**Cost:** $0.00 ongoing. Governance is human decision.

---

**Status: QR system ready. Awaiting your decision to deploy.**

