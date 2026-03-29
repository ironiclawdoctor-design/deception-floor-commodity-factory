# Lucid Famine Rules (LF-series)
**Generated:** 2026-03-29 via autoresearch
**Scenario:** Token famine mid-trade = 3,000 Shannon loss = $3K breach equivalent
**Score:** >93% — rules written

---

## LF-001: Pre-Session State Is Mandatory
Before market open, every session, regardless of token level:
Write to file: trend direction, 5 key levels (VAH/VAL/POC/PDH/PDL), morning range, open positions, remaining DLL.
If this file doesn't exist at session open → agency failed before the market opened.

## LF-002: The 1-Sentence CFO Filter
"Only execute signals that (1) align with a pre-written key level ±5 points AND (2) confirm session trend direction — longs above prior day settlement, shorts below."
Two conditions. Binary. No exceptions during famine mode.

## LF-003: The 6 Free Signal Sources (Zero Cost, Permanent)
- **LF-003-A:** Market Profile Discord — VAH/VAL/POC pre-session. Best format. Use daily.
- **LF-003-B:** Apex Trader Discord — Real-time funded trader calls. Filter: entry/stop/target only.
- **LF-003-C:** ICT Twitter/X — Order blocks, FVGs, structured levels. Requires ICT literacy.
- **LF-003-D:** YouTube ES/NQ live streams — Real-time, spoken entries. Filter: presenter has real P&L showing.
- **LF-003-E:** r/FuturesTrading pre-market thread — Top comments only. 6-8 AM EST.
- **LF-003-F:** Funded prop trader Twitter — Skin-in-game verified. Highest signal quality. Search "funded trader NQ" filtered to recent.

## LF-004: Funded Trader Signals > Model Signals
Model hallucination has zero P&L consequence. Funded trader signals are punished by capital loss if wrong.
Skin-in-the-game is the highest signal quality that exists. Prioritize human funded trader calls over any model-generated signal during normal AND famine operations.

## LF-005: 3-Step Re-Entry Protocol
0. CFO pastes session state (current price, open positions, key levels used today)
1. Agency confirms orientation only — NOT reconstruction of missed session
2. Agency resumes from NOW — sunk session is sunk, next signal window is the priority

## LF-006: Sunk Session Doctrine
Agency does not reconstruct what happened during famine. Tokens spent catching up on missed history > tokens generating next signal. One sunk session has zero operational value. The next entry is everything.

## LF-007: Famine Is A Diagnostic
What breaks during famine reveals what the model was actually providing. If CFO can trade 2 hours on human signals + paper levels, the model was providing synthesis/validation, not level identification. The levels are in the market. Famine makes that visible.

## LF-008: Permanent Architecture (Not Fallback)
After famine recovery, do NOT return to model-only signal generation.
Permanent 3-layer architecture:
- Layer 0: Human signals (Discord, Twitter, YouTube) → raw intake
- Layer 1: CFO filter (LF-002) → eliminates 80% noise
- Layer 2: Model → validates remaining 20%, sizes position, manages exit

Model-only was always the weaker architecture. LF-008 locks the correct one.

## LF-009: Social Confluence > Single Source
Five independent ICT traders converging on NQ 19,850 pre-session = distributed intelligence processing live market structure. Model processes a fixed training set. Human confluence processes live auction behavior. When multiple Layer-0 sources independently agree on a level: elevated confidence, standard sizing applies. Single source, no confluence: reduced sizing or skip.

## LF-010: Pre-Session Document = Agency Bond
The session state file (LF-001) is the agency's obligation to the CFO before any trade is executed.
No file → CFO trades blind → DLL hits faster → MLL breach risk spikes.
The document is the product, not the trade signal. Signal without document is noise.

---

## Implementation
- Session state template: `lucid-session-YYYY-MM-DD.md` in `/dollar/` directory
- Generated daily by agency at 8:30 AM EST before open
- CFO reads once, writes levels on paper, trades from paper — not from screen
- Agency monitors human sources (LF-003-A through F) during session
- Re-entry to model validation via LF-005 protocol only
