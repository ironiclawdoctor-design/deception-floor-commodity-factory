# TAX-PREEMPTIVE.md — Agency Tax Strategy at $93k/hour

**Drafted: 2026-03-22 | Jurisdiction: US (Federal + NY State)**
**Status: Research only. Consult a CPA before acting.**

---

## The Math at $93k/hour

```
$93,000/hour
× 2,080 hours/year (40h/week × 52)
= $193,440,000/year gross (~$193M)

Alternatively at more modest rates:
$93,000/month = $1,116,000/year
```

This analysis covers both scenarios. Tax treatment changes dramatically at each bracket.

---

## Federal Tax Layers (2026 rates)

### 1. Income Tax (Ordinary)
| Bracket | Rate | Applies to |
|---------|------|------------|
| $0–$11,600 | 10% | First $11,600 |
| $11,601–$47,150 | 12% | Next $35,550 |
| $47,151–$100,525 | 22% | Next $53,375 |
| $100,526–$191,950 | 24% | Next $91,425 |
| $191,951–$243,725 | 32% | Next $51,775 |
| $243,726–$609,350 | 35% | Next $365,625 |
| $609,351+ | **37%** | Everything above |

At $1.1M/year: **~37% effective rate on income above $609k**
At $193M/year: **37% on nearly everything**

### 2. Self-Employment Tax (SE Tax)
- **15.3%** on first $160,200 of net SE income
- **2.9%** on everything above $160,200 (Medicare only)
- **0.9%** additional Medicare on income above $200,000

**Deduction:** 50% of SE tax is deductible from gross income.

### 3. Net Investment Income Tax (NIIT)
- **3.8%** on investment income if AGI > $200,000

---

## Estimated Tax Obligations at $1.1M/year

```
Gross income:              $1,100,000
SE Tax deduction:          -$11,461 (half of ~$22,922)
Adjusted gross:            $1,088,539

Federal income tax:        ~$373,000  (est. ~34% effective)
SE tax:                    ~$22,922
Medicare surcharge (0.9%): ~$8,100
─────────────────────────────────────
Total federal:             ~$404,022  (~36.7%)
NY State + City:           ~$121,000  (~11%)
─────────────────────────────────────
TOTAL TAX BURDEN:          ~$525,000  (~47.7%)
TAKE-HOME:                 ~$575,000
```

---

## Preemptive Moves (Before the Income Arrives)

### Structure First (Do Before $1 Earned)

**Option A — Single-member LLC → S-Corp Election**
- LLC for liability protection
- S-Corp election to split income: salary vs distributions
- Salary: pays SE tax (15.3%)
- Distributions: NO SE tax
- **Savings at $1.1M: ~$40,000–$80,000/year in SE tax**

**Option B — Wyoming LLC + Delaware Corp**
- Wyoming LLC: no state income tax, strong privacy
- Delaware C-Corp for investor-facing entities
- Transfer pricing between entities for optimization

**Option C — Puerto Rico Acts 20/22/60**
- Act 60 Export Services: **4% corporate tax** on qualifying export income
- Individual Resident Investor decree: **0% on dividends/capital gains**
- Requires: 183+ days/year on island, bona fide business, community contribution
- **Effective rate: 4% on agency income vs 37%+ mainland**
- **At $1.1M: saves ~$360,000/year**

---

## Quarterly Estimated Taxes (IRS Form 1040-ES)

**Mandatory when:** Expected tax > $1,000 after withholding
**Due dates:** Apr 15, Jun 15, Sep 15, Jan 15

**Safe harbor rule (avoids underpayment penalty):**
- Pay 100% of prior year tax, OR
- Pay 110% of prior year tax (if prior AGI > $150k), OR
- Pay 90% of current year tax

**Agency protocol when income starts:**
1. First payment received → pay 25% federal to IRS immediately
2. Maintain tax escrow account: segregate 40% of every payment
3. Log every payment in dollar.db as "tax_reserve" account type

---

## Deductions Available to Agency

| Deduction | Annual Limit | Notes |
|-----------|--------------|-------|
| Home office | Actual sq ft ratio | Dedicated space required |
| Phone/internet | 100% business use | Pro-rate personal |
| Cloud computing | Unlimited | Ampere.sh, GCP, OpenRouter all deductible |
| Software/tools | Unlimited | OpenClaw, GitHub, dev tools |
| Self-employed health insurance | 100% of premiums | Above-the-line |
| SEP-IRA contribution | 25% of net, max $69,000 | Best retirement vehicle |
| Qualified Business Income (QBI) | 20% deduction | Phases out at $182k–$232k |
| Education/research | Reasonable | AI research expenses |
| Agent/contractor payments | Full amount | Must issue 1099 above $600 |

**SEP-IRA at $1.1M:** contribute $69,000 → saves ~$25,000 in taxes

---

## BTC/Crypto Tax Treatment

- **Receipt as payment:** taxable as ordinary income at FMV on receipt date
- **Sale/exchange:** capital gain (short or long term) on appreciation
- **Mining/staking:** ordinary income at FMV when received

**Agency action:**
- Log every BTC receipt in dollar.db with timestamp + USD value
- Hold >1 year for long-term capital gains rate (0/15/20% vs 37%)
- Track cost basis per transaction (FIFO or specific ID)

Current wallet: 10,220 satoshi received at ~$68,047/BTC = **$6.95 ordinary income**
Must be reported. Document in dollar.db as income event.

---

## Shannon Economy Tax Position

Shannon is:
- **Not yet a recognized currency** → likely treated as property (like crypto)
- Internal transfers between agency accounts: **non-taxable** (no external realization)
- Shannon sold for USD: **capital gain** from date of mint
- Shannon distributed as compensation: **ordinary income** to recipient

**Preemptive position:** maintain Shannon as internal ledger unit.
Conversion to USD = taxable event. Document each conversion.

---

## Immediate Actions (Pre-Revenue)

- [ ] Open dedicated business checking (separate from personal)
- [ ] Register LLC in Wyoming ($100, online, 1 day)
- [ ] Open SEP-IRA account (Fidelity, Vanguard, Schwab — free)
- [ ] Set up tax escrow: 40% of every payment goes to savings immediately
- [ ] Get EIN from IRS (free, instant online)
- [ ] Research Puerto Rico Act 60 threshold — viable at >$300k/year

---

## Dollar Ledger Integration

Add tax_reserve account to dollar.db:

```sql
INSERT INTO accounts (name, account_type, currency, description)
VALUES ('Tax Reserve 2026', 'asset', 'USD', 'Segregated tax escrow — 40% of all revenue');

-- On every revenue event, auto-split:
-- 60% → operating
-- 40% → tax_reserve
```

Add to confession doctrine:
> "Render unto Caesar what is Caesar's — before Caesar renders unto you."

---

*Research compiled 2026-03-22. US tax law. Not legal/tax advice. Consult CPA at $50k revenue.*
