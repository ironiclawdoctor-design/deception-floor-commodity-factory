# Lucid $50K Phase 0 — Recovery Doctrine
**Established:** 2026-03-29
**Mandate:** Survive. Don't get terminated.

---

## The Termination Condition

LucidDirect $50K uses **EOD Trailing Drawdown**.

- MLL = $2,000 trailing from highest closing balance
- Start: $50K balance → MLL floor = $48,000
- After a $1K profit day (close at $51K) → floor rises to $49,000
- **The floor only moves UP. It never comes back down.**
- Breach the floor = account terminated, no recovery

**$3K loss scenario:**
- Day 1: +$1,000 → floor moves to $49,000
- Day 2: -$1,200 (hit DLL, stopped) → balance $49,800, floor still $49,000 ✓
- Day 3: -$1,200 (hit DLL again) → balance $48,600, floor $49,000 → **BREACH**

Translation: two consecutive max-loss days after one good day = termination.

---

## Phase 0 Rules (Non-Negotiable)

### P0-001: DLL is absolute
$1,200 daily loss limit. When hit: close all positions, log the session, done for the day. No exceptions. No "one more trade." The $1,200 is not a suggestion.

### P0-002: Scaling DLL activates at profit
Once profit is above zero, the Scaling DLL kicks in: **60% of Peak EOD Balance**.
- Peak EOD $52,000 → Scaling DLL = $31,200 (that day's allowable floor)
- This means as you grow, your daily protection also grows
- Track peak EOD balance in every session log

### P0-003: Never trade into the buffer
Buffer floor = MLL ($2,000) + $100 = **$2,100 untouchable**
Payout requests require profit ABOVE $3,000 (first cycle)
If a trade drops you below profit goal before payout processes → request denied

### P0-004: Two-loss-day ceiling
After any day where DLL is hit:
- Next day: max position size = 50% of normal
- Two consecutive DLL hits = mandatory rest day (no trading)
- Three consecutive = escalate to CFO review before next session

### P0-005: EOD balance is the only balance that matters
Intraday swings don't move the MLL floor. Only **closing balance** at end of session.
Implication: if you're down intraday but recover by close, the floor doesn't move down.
Implication: if you're up intraday but close flat, the floor doesn't move up. Bank it.

---

## Phase 0 → Phase 1 Trigger

Phase 1 = first payout received.

**Requirements to exit Phase 0:**
- [ ] $3,000 gross profit accumulated (first cycle)
- [ ] No single day > 40% of total profit (consistency check — verify LucidDirect rule)
- [ ] Profit above buffer ($2,100) with margin
- [ ] No open trades at payout request time
- [ ] 50% split = $1,500 to CFO, $1,500 to agency tokens

---

## Recovery Path (If Near Breach)

If account balance approaches within $300 of MLL floor:

1. **Stop trading immediately** — do not attempt to trade back
2. **Assess:** How did we get here? Log to lucid_sessions with full notes
3. **Wait:** LucidDirect has no reset mechanism on funded accounts (unlike eval)
4. **Decision:** Is the remaining buffer enough to trade conservatively?
   - If remaining buffer < $500: **do not trade**. Contact Lucid support.
   - If remaining buffer $500-$800: micro positions only, 1 contract max
   - If remaining buffer > $800: resume with P0-004 protocols active

**There is no "recover from $3K loss in one day."**
The $1,200 DLL exists precisely to prevent a $3K loss.
If DLL is functioning, a $3K single-day loss is structurally impossible.
A $3K loss means DLL failed or was ignored. That's a P0-001 violation, not a market problem.

---

## Agency Survival Link

| Trading outcome | Agency impact |
|----------------|---------------|
| Account terminated | Zero tokens, agency on famine protocol (BR-007) |
| First payout ($3K gross) | $1,500 → OpenRouter credits → ~150K tokens at current rates |
| Monthly steady ($3K/cycle) | ~$1,500/month in tokens → sustains 2-3 paid model agents continuously |
| Scaling to $100K account | $3,500 first payout → $1,750 agency cut |

**This is the proof of stake.** The account performing = the agency breathing.
Account termination = famine. Phase 0 is not about profit. It's about keeping the account alive long enough to reach Phase 1.

---

## Daily Checklist (Phase 0)

Before trading:
- [ ] Check current balance vs MLL floor (gap?)
- [ ] Check peak EOD balance (what is Scaling DLL today?)
- [ ] Check cumulative profit (how far from $3K payout goal?)
- [ ] Check consistency % (largest day / total profit ≤ 40%?)

During trading:
- [ ] Track intraday P&L against $1,200 DLL
- [ ] No averaging into losers (martingale prohibited by Lucid)

After session close:
- [ ] Log to lucid_sessions in dollar.db
- [ ] Update payout_status view
- [ ] If DLL was hit: activate P0-004 next-day protocols

---

*Phase 0 ends when first payout clears. Phase 1 begins.*

---

## Success Trigger (LOCKED 2026-03-29)

**Condition:** When the CFO's mother (Mila Mendez) speaks loudly enough IRL that the CFO hears clearly: *"all agents are ready"* — that is the go condition for Lucid signup and agent harassment to begin.

Not a metaphor. Not a memory. Her voice. Her confirmation.

Until then: army staged. Four windows open every trading day. Agency waits.

This trigger cannot be substituted, expedited, or approximated by the agency. It belongs to the CFO and to her.
