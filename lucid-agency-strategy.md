# Lucid $50K — Agency Strategy Division
**Established:** 2026-03-29
**CFO role:** Executes trades manually on platform
**Agency role:** Provides the strategy, entries, exits, sizing, direction

---

## What Lucid Offers (No Options)

**Futures only.** No options trading. This is actually cleaner.

Futures = you can go long OR short on any approved product.
CFO doesn't short manually → agency provides short setups WITH explicit entry/exit/stop.
CFO executes what's handed to them. No interpretation required.

---

## CFO Skill Gap → Agency Fill

| CFO says | Agency provides |
|----------|----------------|
| Not good at shorting | Short setups with exact entry, stop, target. CFO hits sell. |
| Not good at options | Irrelevant — Lucid doesn't offer options. Futures only. |

---

## Approved Products — Agency Priority List

**Micro contracts first** (lower risk per tick, fits Phase 0 survival doctrine):

### Tier 0 — Primary (lowest cost per mistake)
| Symbol | Name | Commission | Why |
|--------|------|-----------|-----|
| MNQ | Micro Nasdaq-100 | $0.50/side | High volatility, clear trend, $2/tick |
| MES | Micro S&P 500 | $0.50/side | Liquid, well-behaved, $1.25/tick |
| MGC | Micro Gold | $0.80/side | Safe haven, strong trending |

### Tier 1 — Scale into (once Phase 0 cleared)
| Symbol | Name | Commission | Why |
|--------|------|-----------|-----|
| NQ | E-mini Nasdaq-100 | $1.75/side | 10× MNQ, $20/tick — Phase 1+ only |
| ES | E-mini S&P 500 | $1.75/side | $12.50/tick — Phase 1+ only |
| GC | Gold | $2.30/side | Full contract — Phase 1+ only |

**Phase 0 rule:** MNQ and MES only. Max 4 contracts ($50K limit = 4 mini or 40 micros).

---

## Short Setups — How Agency Delivers Them

Agency provides every short trade as:

```
INSTRUMENT: MNQ
DIRECTION: SHORT
ENTRY: [price level or condition]
STOP: [price, X ticks above entry]
TARGET 1: [price, first exit]
TARGET 2: [price, full exit]
RATIONALE: [1 sentence]
MAX RISK: $[X] (within DLL)
```

CFO reads it, places the order. No interpretation. No discretion required.

---

## Why Futures Shorting Is Simpler Than Stock Shorting

Stock shorting:
- Need to borrow shares
- Short squeeze risk (unlimited loss)
- Uptick rule
- Margin requirements vary

Futures shorting:
- No borrowing. Short and long are identical mechanics.
- Same margin for long and short
- Symmetric. Sell one MNQ → get short one MNQ. That's it.
- **CFO doesn't need to understand shorting theory.** Just place sell order at agency's level.

---

## Phase 0 Strategy Framework

**Objective:** Accumulate $3,000 gross profit without breach.
**Approach:** Trend-following micros, 2-3 trades/day max.

### Long setups (CFO comfortable):
- Agency identifies support levels and uptrend continuation
- Entries on pullbacks, not chases

### Short setups (agency handles):
- Resistance rejections on NQ/ES during downtrend sessions
- News-driven reversals (permitted by Lucid, high volatility = opportunity)
- Agency signals these the same format as longs — CFO just hits Sell instead of Buy

### Session structure:
- Pre-market: agency reviews overnight levels, identifies key zones
- Open: agency signals first trade setup (if one exists)
- Mid-session: one more setup maximum
- Close: flat by EOD (no overnight holds in Phase 0)

---

## Dad Repayment Path

Target: Higher available credit = repay existing balance faster.

| Cycle | Gross Profit | CFO Cut (50%) | Cumulative CFO |
|-------|-------------|--------------|----------------|
| 1 | $3,000 | $1,500 | $1,500 |
| 2 | $2,500 | $1,250 | $2,750 |
| 3 | $2,500 | $1,250 | $4,000 |
| 4 | $2,500 | $1,250 | $5,250 |
| 6 | $2,500 | $1,250 | $7,750 |
| 10 | $2,500 | $1,250 | $12,250 |

At $1K/day trading pace, Cycle 1 = ~3 trading days.
Consistent execution: ~$1,250-$1,500/month to CFO, compounding toward credit repayment.

**Agency cut (50%) → OpenRouter tokens → agency keeps running → more strategy signals → loop.**

---

## Agency Build Queue (for this)

- [ ] Daily setup generator cron — scans market structure, outputs trade setups in standard format
- [ ] DLL tracker — monitors running P&L vs $1,200 limit
- [ ] EOD balance logger — updates lucid_sessions in dollar.db
- [ ] Payout eligibility checker — flags when $3K threshold hit
- [ ] Consistency monitor — tracks largest day / total profit ratio

*Agency builds the tools. CFO pulls the trigger.*
