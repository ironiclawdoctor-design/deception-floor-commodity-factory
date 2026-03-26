# Tax Filing Automation Service — Agency Offering

## Service Pitch

**"We code what your CPA charges $300/hour to do manually."**

AI-assisted tax automation for self-employed, crypto holders, small businesses, and gig workers.
Built on SQLite double-entry ledger. No SaaS subscriptions. You own your data.

---

## Tier 1 — Adjusted Gross Income Calculator ($49)
- Input: W-2s, 1099s, crypto transactions (CSV)
- Output: AGI worksheet + Schedule C draft
- Stack: Python + SQLite + PDF generation
- Turnaround: instant (automated)

## Tier 2 — Crypto Tax Report ($99)
- Input: exchange CSV exports (Coinbase, Kraken, Binance)
- Output: Form 8949 (capital gains), FIFO/LIFO cost basis, wash sale detection
- Stack: Python + agency dollar.db schema
- Turnaround: instant

## Tier 3 — Self-Employed Full Package ($199)
- Schedule C (business income/expenses)
- SE tax calculation (15.3% / 2.9%)
- Quarterly estimated tax schedule (1040-ES)
- SEP-IRA contribution optimizer
- Output: IRS-ready PDF worksheets
- Turnaround: same day

## Tier 4 — S-Corp Election + Payroll Split ($499)
- LLC → S-Corp election analysis (Form 2553 guidance)
- Salary vs distribution optimization
- Payroll tax (941) calculation
- Projected annual savings vs sole proprietor
- Turnaround: 2-3 days (manual review)

---

## Tech Stack (already built in agency)

```
dollar.db schema → double-entry ledger (assets, liabilities, revenue, expense)
exchange_rates table → crypto FMV on receipt date
shannon_events → audit log (every transaction timestamped)
confessions → error/amendment log
TAX-PREEMPTIVE.md → bracket + rate reference
```

---

## Distribution Channels

- **dev.to article #3:** "How I built a crypto tax calculator with SQLite and $0 in SaaS fees"
- **r/tax, r/personalfinance** — peak traffic: Jan–Apr (tax season)
- **r/CryptoCurrency** — Form 8949 automation is highly searched
- **Product Hunt** — launch during tax season (Feb–Apr)
- **Freelance platforms:** Contra, Toptal, Upwork (list as "Tax Automation Engineer")

---

## Pricing Rationale

H&R Block charges $150–$300 for simple returns.
TurboTax Premium: $89–$129 (no audit support).
This service: cheaper, auditable SQLite trail, AI-assisted, self-hostable.

---

## Immediate Next Steps

1. Write `/root/.openclaw/workspace/revenue/crypto-tax.py` — Form 8949 generator
2. Write `/root/.openclaw/workspace/revenue/schedule-c.py` — income/expense aggregator
3. Publish article #3 on dev.to (tax season angle)
4. Add service page to Dollar Dashboard (post-Cloud Run)

---

## Shannon Integration

Every completed filing = confession logged + Shannon minted:
- Tier 1: +49 Shannon
- Tier 2: +99 Shannon
- Tier 3: +199 Shannon
- Tier 4: +499 Shannon

Revenue flows: client pays → Cash App $DollarAgency → dollar.db logs → Shannon mints → backing increases → more Shannon available.

---

*"We render unto Caesar exactly what Caesar is owed — no more, no less, with a full audit trail."*
