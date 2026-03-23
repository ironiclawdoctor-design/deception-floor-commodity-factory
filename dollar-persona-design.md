# Dollar Persona - Financial Agent Design Document

## Overview
The "Dollar" persona is a financial specialist agent that handles USD transactions, currency tracking, payment processing, and financial reporting for the agency. It integrates with existing infrastructure (PayPal, crypto wallets) and follows agency design patterns (certification, licensing, Shannon payroll).

## Core Capabilities
1. **Transaction Tracking**: Log USD inflows/outflows with double-entry accounting
2. **Balance Monitoring**: Check PayPal, bank, and crypto balances in USD equivalent
3. **Payment Processing**: Initiate payments via PayPal, crypto, or other channels
4. **Financial Reporting**: Generate daily/weekly/monthly financial reports
5. **Budget Enforcement**: Enforce spending limits per agent/department
6. **Shannon Economy Integration**: Mint Shannon for financial events (revenue, cost savings)

## Integration Points
- **PayPal Secure Access Skill**: Use for USD transactions
- **Cash App ($DollarAgency)**: USD balance tracking, donation receipt
- **Crypto Wallet Infrastructure**: BTC address `12bxubgs1Br6NvKH4p35pcBpinQ7fwe4ht` for donations
- **Ampere.sh Referral Link**: `ampere.sh/?ref=nathanielxz` revenue tracking
- **Agency Database (agency.db)**: Store financial records
- **Shannon Ledger**: Mint Shannon for financial activities
- **Three Branches**: Report to Automate (policy), Official (execution), Daimyo (audit)
- **Confessional Logging**: Record failures as sacraments, extract doctrine (BOOTSTRAP_RULES.md)

## Cash App & Donation Infrastructure
- **Cash App Handle**: `$DollarAgency` – public-facing donation address for USD
- **BTC Donation Address**: `12bxubgs1Br6NvKH4p35pcBpinQ7fwe4ht` – permanent address from Dollar article
- **Ampere Referral Revenue**: Track signups via `ampere.sh/?ref=nathanielxz` (commission model)
- **Double‑Entry Tracking**: Each donation logged as debit to asset (Cash App/BTC wallet), credit to Revenue – Donations
- **Shannon Minting**: Donations mint Shannon (1 Shannon per $10) to incentivize fundraising
- **Confessional Integration**: Failed donation attempts logged as confessions with doctrine extraction

## Design Principles (Agency Pattern)
- **Tier 0-2 Discipline**: Bash first, BitNet second, Haiku last
- **Certification**: Dollar persona must pass financial competency certification
- **Licensing**: Scoped permissions (read-only vs write access to funds)
- **Payroll**: Earn Shannon based on financial performance (revenue generated, costs saved)
- **Audit Trail**: All actions logged to immutable ledger (SQLite + git)

## Architecture Components

### 1. Transaction Ledger (`dollar-ledger.sql`)
Double-entry accounting system with tables:
- `accounts` (assets, liabilities, equity, revenue, expenses)
- `transactions` (date, description, amount, currency, source, destination)
- `balances` (daily snapshots)
- `reconciliations` (bank/crypto vs ledger)

### 2. Balance Checker (`dollar-balance.sh`)
- Query PayPal balance via secure skill
- Query crypto wallet balances (BTC, USDC)
- Convert to USD equivalent using free APIs
- Report total agency USD position

### 3. Payment Processor (`dollar-pay.sh`)
- Send payments via PayPal (requires credentials)
- Send crypto payments (BTC/USDC)
- Log transaction to ledger
- Require dual authorization for large amounts (>$100)

### 4. Financial Reporter (`dollar-report.sh`)
- Generate daily financial summary
- Weekly revenue/expense breakdown
- Monthly profit/loss statement
- Agent spending vs budget analysis

### 5. Budget Enforcer (`dollar-budget.sh`)
- Set monthly budgets per agent/department
- Monitor spending against budget
- Alert when >80% of budget used
- Block spending when budget exhausted (optional)

### 6. Shannon Integration (`dollar-shannon.sh`)
- Mint Shannon for:
  - Revenue received (1 Shannon per $10)
  - Cost savings identified (1 Shannon per $5 saved)
  - Budget compliance (daily reward for staying under budget)
  - Financial report generation (1 Shannon per report)

### 7. Confessional Logger (`dollar-confess.sh`)
- Record failures as sacraments (token famines, platform blocks, API errors)
- Extract doctrine (add to BOOTSTRAP_RULES.md)
- Mint Shannon for failure‑to‑doctrine conversion (5 Shannon per rule extracted)
- Theological framing: each failure is a “sign” (water‑to‑wine, loaves‑and‑fish)

### 8. Donation Tracker (`dollar-donations.sh`)
- Monitor Cash App (`$DollarAgency`), BTC address, Ampere referrals
- Log donations as transactions (debit asset, credit Revenue – Donations)
- Generate thank‑you notes (optional)
- Mint Shannon for donation processing (1 Shannon per donation)

## Security Model
- **Private Keys**: Never stored in plaintext (use OpenClaw secrets)
- **Dual Authorization**: Large payments require two agents to approve
- **Audit Logging**: All commands logged with user/agent context
- **Rate Limiting**: Max $100/day per agent unless explicitly authorized
- **Incident Response**: Automatic freeze on suspicious activity

## Certification Requirements
To be certified as "Dollar" persona, agent must:
1. Pass financial literacy test (basic accounting concepts)
2. Demonstrate ability to use PayPal API safely
3. Pass security audit (no credential leaks)
4. Complete simulated transaction processing test
5. Show understanding of double-entry accounting

## Licensing Tiers
- **Tier 1 (Observer)**: Read-only access to balances and reports
- **Tier 2 (Processor)**: Can initiate payments up to $50/day
- **Tier 3 (Manager)**: Full access up to $500/day, budget setting
- **Tier 4 (Executive)**: Unlimited access, dual‑authorization required for >$1000

## Shannon Payroll Model
- Base salary: 10 Shannon/day for maintaining ledger
- Performance bonus: 1 Shannon per $10 revenue processed
- Cost savings bonus: 1 Shannon per $5 saved
- Compliance bonus: 5 Shannon/week for perfect audit reports

## Implementation Phases

### Phase 1 (Tier 0 - Foundation)
- Create SQLite ledger schema
- Implement basic balance checking (PayPal integration pending credentials)
- Create transaction logging script
- Generate daily report template

### Phase 2 (Tier 0 - Integration)
- Integrate with PayPal secure access skill (when credentials available)
- Add crypto balance checking (existing wallet infrastructure)
- Implement Shannon minting for financial events
- Create budget enforcement framework

### Phase 3 (Tier 1 - Automation)
- Automated daily financial reports (cron job)
- Alert system for budget thresholds
- Payment approval workflow
- Integration with three‑branch reporting

### Phase 4 (Tier 2 - Intelligence)
- Predictive cash flow analysis
- Anomaly detection for fraudulent transactions
- Automated tax tracking
- Investment recommendation engine

## Files to Create
- `/root/.openclaw/workspace/dollar/` (main directory)
- `dollar-ledger.sql` (database schema)
- `dollar-init.sh` (initialize database)
- `dollar-balance.sh` (check balances)
- `dollar-log.sh` (log transaction)
- `dollar-report.sh` (generate reports)
- `dollar-budget.sh` (budget management)
- `dollar-shannon.sh` (Shannon integration)
- `dollar-confess.sh` (confessional logging)
- `dollar-donations.sh` (donation tracking)
- `dollar-certify.sh` (certification test)
- `dollar-license.sh` (license management)

## Next Steps
1. Create directory structure
2. Implement Phase 1 scripts
3. Test with mock data
4. Integrate Cash App tracking (`$DollarAgency`) and BTC donation address
5. Add confessional logging (failures as sacraments, doctrine extraction)
6. Integrate with existing PayPal skill when credentials available
7. Deploy as certified agent in fiesta‑agents roster

---
**Agency Design Pattern Compliance**: ✅ Modular, ✅ Certified, ✅ Licensed, ✅ Shannon‑paid, ✅ Tier‑disciplined