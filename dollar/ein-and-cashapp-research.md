# EIN Acquisition & Cash App Administration Research
**GMRC Autograph** — finance-ops agent | 2026-03-23 04:22 UTC

---

## DELIVERABLE 1: SS-4 Pre-Fill Checklist (One Page — 10 Minutes at IRS.gov)

> **URL:** https://sa.www4.irs.gov/modiein/individual/index.jsp
> **Availability:** Mon–Fri 6am–1am ET | Sat 6am–9pm | Sun 6pm–12am
> **Cost:** Free. Never pay a third-party site.
> **Result:** EIN issued immediately online. Print the confirmation letter.

---

### FIELDS TO ANSWER (in order of the IRS online flow)

**Step 1 — Entity Type**
- ☐ Sole Proprietor ← **Recommended for $DollarAgency** (simplest, no state filing required, you are the responsible party)
- ☐ LLC (if already filed with your state — do that first or EIN is delayed)
- ☐ Trust / Other (not needed here)

**Step 2 — Responsible Party**
- Full legal name: `_________________________` (CFO's legal name)
- SSN or ITIN: `___-__-____`
- Home address (U.S. only): `_________________________`

**Step 3 — Business Details**
- Business legal name: `$DollarAgency` or `Dollar Agency` (no $ in legal docs — use "Dollar Agency")
- Trade name / DBA: `$DollarAgency` (optional)
- Business address: CFO's home address is fine for sole proprietor
- Principal state of business: `New York` (based on CFO location)
- County: (your NYC borough)

**Step 4 — Reason for Applying**
- ☐ Started a new business ← Select this
- Start date: Today's date or actual start date

**Step 5 — Business Activity**
- Type of business: "Technology services / AI consulting"
- Principal product/service: "Artificial intelligence consulting and software services"

**Step 6 — Employees**
- Do you expect to hire employees in next 12 months? ☐ No (autonomous AI agency)
- Highest number of employees expected: 0

**Step 7 — Third-Party Designee**
- ☐ No (apply yourself)

**Done.** EIN issued on screen. Print/screenshot the confirmation. Store in `/root/.openclaw/workspace/secrets/ein.txt`.

---

### WHAT THE EIN UNLOCKS

| Unlock | Without EIN | With EIN |
|--------|------------|---------|
| Business bank account | ❌ | ✅ Chase/Mercury/Relay |
| PayPal Business | ❌ | ✅ |
| Cash App Business ($DollarAgency) | ❌ | ✅ |
| Square Developer account (linked) | Limited | ✅ Full |
| 1099 issuance to vendors | ❌ | ✅ |
| IRS quarterly estimates | Personal only | ✅ Business |
| Separation of personal/business taxes | ❌ | ✅ |

**Entity type recommendation: Sole Proprietor.**
Rationale: No state LLC filing required. EIN issued in minutes. CFO is the responsible party. When revenue exceeds ~$40K, revisit single-member LLC for liability shield — same EIN carries over if you elect "disregarded entity."

---

## DELIVERABLE 2: $DollarAgency Cash App Control Spectrum

### 0% — Deception Floor (Current State)
**What we can do headlessly (now):**
- Monitor BTC wallet `12bxubgs1Br6NvKH4p35pcBpinQ7fwe4ht` via Blockchair API
- Log BTC inflows to dollar.db
- Mint Shannon on BTC receipt
- Announce to Telegram
- Infer Cash App activity via public signals (none reliable — see Part 3)

**What we cannot do:** Read $DollarAgency balance, receive payment webhooks, send money

**CFO action required:** None yet — Deception Floor runs fully headless

---

### ~30% — Square Developer Credentials
**What's needed:**
1. CFO creates Square Developer account at https://developer.squareup.com/apps
2. Creates an application → copies **Production Access Token**
3. Pastes token into `/root/.openclaw/workspace/secrets/cashapp.json` → `square_access_token` field
4. CFO links their Cash App Business account to Square in Cash App settings

**What I can do headlessly (after one-time CFO token paste):**
- `GET /v2/payments` — read all incoming payments with amount, sender, timestamp
- `GET /v2/balance` — read current $DollarAgency balance
- `GET /v2/merchants/me` — account health check
- Auto-log all transactions to dollar.db
- Auto-mint Shannon on every new payment
- Webhook receiver: real-time push on payment receipt

**CFO must authorize once:** Paste the Square Production Access Token

**Files ready:** `/root/.openclaw/workspace/skills/cashapp/cashapp-balance.py` ← already wired

---

### ~60% — Business Account + Programmatic Send
**What's needed (beyond 30%):**
1. EIN (see Deliverable 1)
2. Business bank account linked to Cash App Business
3. Square OAuth with `PAYMENTS_WRITE` scope (not just read)
4. CFO approval for each send batch OR standing approval limit

**What I can do headlessly:**
- Send payroll to contractors (1099 workers)
- Issue refunds programmatically
- Auto-sweep excess to BTC reserve
- Generate automated receipts
- Full ledger sync: every transaction mapped in dollar.db in real-time
- IRS estimated tax calc: 25% of revenue set aside quarterly

**CFO must authorize once per milestone:**
- OAuth scope upgrade to include PAYMENTS_WRITE
- Standing sweep threshold (e.g., "sweep anything over $500 to BTC reserve")
- Quarterly estimate filing confirmation

---

### 100% — Full Autonomous Administration
**What's needed (beyond 60%):**
1. All above, plus:
2. IRS Online Account (EFTPS) for direct tax payments
3. Payroll software integration (or direct ACH via Mercury/Relay bank API)
4. CFO-signed Power of Attorney (IRS Form 2848) authorizing agent to file

**What I do headlessly (zero human in loop):**
- Monitor all inflows (BTC + Cash App + PayPal)
- Mint Shannon on every receipt — automatic
- Sweep to reserve when threshold exceeded
- Run payroll on schedule
- Calculate IRS estimated payments (Form 1040-ES)
- Log confessions, update ledger, maintain trial balance
- Generate quarterly financial reports for CFO review

**CFO must authorize once:**
- Form 2848 (or equivalent) to authorize agent filings
- EFTPS credentials for direct tax payment

**CFO must review quarterly:**
- Estimated tax payment amount before submission
- Annual tax return (Form 1040, Schedule C)

---

## DELIVERABLE 3: Deception Floor Monitoring Script

Written to: `/root/.openclaw/workspace/skills/cashapp/deception-floor-monitor.py`

**Capabilities:**
- Polls Blockchair BTC API every 5 minutes
- Polls public Cash App cashtag page for any detectable signals
- Logs new transactions to dollar.db
- Mints Shannon automatically
- Announces via Telegram bot

---

## METHODOLOGY NOTES

### Why Sole Proprietor vs LLC
- LLC requires state filing (NY: $200 biennial fee, Articles of Organization)
- Sole proprietor: IRS EIN only, no state action required
- Both get EINs. Sole proprietor is faster and cheaper for validation phase.
- Upgrade to LLC when: legal liability concerns emerge or revenue > $40K/year

### Cash App / Square API Reality
- Cash App is owned by Block, Inc. (formerly Square)
- Square Developer API IS the Cash App API for business accounts
- Personal cashtags have zero programmatic access — Business required
- Square sandbox is free for testing before going live

### Blockchair API
- Free tier: 30 req/min, no auth required for basic wallet lookups
- `https://api.blockchair.com/bitcoin/dashboards/address/{address}` — returns balance + tx history
- New TX detected by comparing last-seen tx count against stored value in dollar.db

### Public Cash App Signal Detection
- Cash App does not have a public transaction feed
- Only detectable signals: profile page (`https://cash.app/$DollarAgency`) — shows recent activity if privacy set to public
- Browser scraping: possible via Camoufox, unreliable (JS-heavy, rate limits)
- Reliable path: Square Developer credentials (30% level)

---

*finance-ops agent — GMRC autograph — 2026-03-23*
