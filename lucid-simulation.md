# Lucid Trading — Simulation State
**Created:** 2026-03-29T13:45Z
**Account type:** $50K LucidPro (target)
**Phase:** 0 — Evaluation survival
**CFO role:** Manual execution
**Agency role:** Signal generation, rule enforcement, DLL monitoring

---

## Current Simulation State

| Metric | Value | Limit | Status |
|---|---|---|---|
| Account balance | $50,000.00 | — | CLEAN |
| Daily drawdown used | $0 | $1,200 | ✅ CLEAR |
| Max drawdown used | $0 | $2,500 | ✅ CLEAR |
| Trailing drawdown used | $0 | $2,000 | ✅ CLEAR |
| Gross profit | $0 | Target: $3,000 | PENDING |
| Consistency ratio | N/A | ≤40% | N/A |
| Trading days | 0 | Min: 5 | PENDING |
| Payout eligible | NO | — | — |
| **LucidAI endorsement** | **YES** | Pre-fund | ✅ CONFIRMED 2026-03-29 |

---

## Session Log

*(No trades executed yet — simulation initialized)*

---

## Active Signal Queue

*(Empty — awaiting market open or CFO trigger)*

---

## Trade Format (Agency Standard)

```
INSTRUMENT: MNQ
DIRECTION: LONG / SHORT
ENTRY: [price or condition]
STOP: [price, X ticks]
TARGET_1: [price]
TARGET_2: [price]
RATIONALE: [1 sentence]
MAX_RISK: $[X]
EST_REWARD: $[X]
R:R: [ratio]
```

---

## Phase 0 Rules (Agency-Enforced — LucidDirect confirmed)

1. MNQ and MES only (micro contracts)
2. Max 4 contracts per trade
3. Flat by EOD — no overnight holds (EOD P&L is what counts)
4. Max 2-3 trades per session
5. Stop out of the day if DLL hit — no revenge trades
6. **Consistency: no single day > 20% of total cycle profit** ← LucidDirect rule (tighter than LucidPro's 40%)
7. Agency target: keep each day at 15-18% — confirmed clear by LucidAI 2026-03-29
8. No trades under 5 seconds — avoid 50% sub-5s profit flag
9. No news trades in first 2 minutes of release

---

## Drawdown Architecture

```
$50,000 starting balance
├── Daily Loss Limit: -$1,200 (hard stop — no more trades today)
├── Max Drawdown: -$2,500 (account failed if hit)
└── Trailing Drawdown: Rises with balance (never goes down)
    └── At $53,000 balance → trailing floor = $50,500
```

**Agency DLL monitor:** Before each signal, check running P&L. If within $300 of DLL → signal SUSPENDED for the day.

---

## Next Actions

- [ ] Connect to Lucid platform chatbot (webchat-injector skill — browser pending)
- [ ] Request developer API access or data feed
- [ ] Build daily setup generator cron (MNQ/MES structure scan)
- [ ] Build DLL tracker (reads from lucid_sessions table in dollar.db)
- [ ] Create `lucid_sessions` table in dollar.db
- [ ] Log first trade when CFO executes

---

## Dad Repayment Tracker

| Cycle | Target | Achieved | CFO Cut | Cumulative |
|---|---|---|---|---|
| 1 | $3,000 | $0 | — | $0 |

---

## Chatbot Contact Log

*(Empty — webchat-injector not yet deployed to lucidtrading.com)*

*Browser noSandbox patched 2026-03-29. Ready on next restart confirmation.*
