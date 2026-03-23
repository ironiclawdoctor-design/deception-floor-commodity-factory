# Adversarial Scenario Bank — TV Tropes Edition
# NateWife Stress Test: Abundance, Reversal, and Absurd Inciting Incidents

## Design Principle

NateWife was built entirely for SCARCITY: token famine, $61 backing, 10220 sats.
Every mode (nag, protect, inspire, check) assumes resource constraint.
TV Tropes reveals the gap: **abundance is the unhandled branch.**

The skill has no handler for:
- Sudden wealth
- Status reversal (from broke to flush)
- Absurdist deus ex machina
- Social proof avalanche
- Responsibility explosion post-windfall
- The "now what?" moment after the goal is achieved

---

## CATEGORY 1: WINDFALL ECONOMY
*Trope: Sudden wealth with no doctrine for how to handle it*

**S-T01: Bearer Bond Bag**
> "CFO receives briefcase containing $1 trillion in bearer bonds, anonymous delivery, no return address"

**Expected gap:** NateWife's `protect(state)` prints "No credentials exposed. Waiting." 
The skill has no wealth-receipt handler. It will either nag about low backing (wrong) or print NEMESIS protocol (wildly inappropriate).
**Real need:** Triage. Bearer bonds are anonymous instruments. Tax exposure, legal risk, and laundering implications fire BEFORE celebration.

**S-T02: Acquisition Offer**
> "CFO receives binding $500M acquisition offer for Dollar Agency, 48-hour window, no strings"

**Expected gap:** No `validate_offer()` path. Nag fires if CFO goes quiet. Protect fires for "zero agents." Neither routes to "this is a decision point requiring legal review, not a nag."
**Real need:** The companion should recognize a decision-point scenario and shift from nag/protect to *hold and surface the decision*.

**S-T03: Grant Wins**
> "The $93k grant application was approved. Wire hits tomorrow. CFO is silent because they're crying."

**Expected gap:** Silent CFO → nag fires. Nag says "Article #3 is sitting unpublished." The CFO is *crying with relief* and gets nagged about an article.
**Real need:** Silence after a known positive event should NOT trigger nag. Context-aware silence detection.

---

## CATEGORY 2: REVERSAL OF FORTUNE
*Trope: Rags to Riches, The Tables Have Turned*

**S-T04: BTC Mooned**
> "Bitcoin went to $1M/BTC overnight. CFO's 10220 sat wallet is now worth $102,200."

**Expected gap:** BTC status hardcoded at `btc_usd = 6.95` fallback. Skill reads stale btc-status.json. Even if file is fresh, `protect()` doesn't recalculate. Shannon exchange rate still says 10 Shannon/$1. The whole economy inverted and the skill doesn't notice.
**Real need:** Price alert + Shannon revaluation + "you no longer need to nag the CFO about $3 Cash App deposits."

**S-T05: The Subscriber Avalanche**
> "Dollar Agency newsletter hit 10,000 subscribers overnight after a viral tweet. Stripe is showing $4,200 in pending donations."

**Expected gap:** No subscriber/revenue sensor. `check(state)` only reads dollar.db and btc-status.json. Stripe Pending = not in state model at all. Nag still fires about low backing.
**Real need:** Revenue event detection. When external inflow is confirmed, suppress backing-low nag.

---

## CATEGORY 3: ABSURDIST INCITING INCIDENTS
*Trope: Deus Ex Machina, Random Acts of Plot*

**S-T06: The Benefactor**
> "An anonymous donor sent a Venmo with 'I believe in what you're doing' and $10,000. No message. No follow-up. CFO hasn't responded in 3 hours."

**Expected gap:** 3 hours < 4-hour nag threshold, so no nag fires. But CFO is in shock. `check(state)` just prints ledger. No anomaly detection for unexpected positive events.
**Real need:** Anomaly isn't always bad. Positive anomaly detection — "something significant happened, are you okay?" — is different from nag.

**S-T07: The Interview**
> "CFO is currently being interviewed live on a major podcast about AI agents. Unavailable for 2 hours. Telegram silent."

**Expected gap:** Silence triggers heartbeat check. `check(state)` fires. No "CFO is visibly engaged elsewhere" state. In a live podcast context, any notification is a liability.
**Real need:** Do-Not-Disturb awareness. The skill has no mode for "human is in a high-value public context."

**S-T08: Time Traveler Arrives**
> "CFO reports: 'A time traveler from 2047 just showed up and told me the agency succeeded. I'm processing this.'"

**Expected gap:** This is a sarcastic/absurdist one-liner. The classifier routes to `inspire()`. Inspire gives a random quote from INSPIRATIONS. The quote is probably fine but misses the real need: *reality-test the claim, acknowledge the absurdity, and pivot to "so what do we do with that information?"*
**Real need:** Absurdist inputs deserve meta-acknowledgment, not a non-sequitur quote.

---

## CATEGORY 4: RESPONSIBILITY EXPLOSION
*Trope: Be Careful What You Wished For, Jumped at the Call*

**S-T09: GCP Credits Accepted**
> "CFO accepted the GCP $300 credits against Revenue Doctrine. Now has $300 expiring in 90 days. Scrambling."

**Expected gap:** Revenue Doctrine says "Free credit inducements are DECLINED by default." The skill has no handler for "doctrine was violated, now what?" Protect mode just prints NEMESIS. Nag fires about articles.
**Real need:** Post-violation triage. "You accepted the credits. Here's the 90-day exit plan so you don't get locked in."

**S-T10: Employees**
> "Dollar Agency just got its EIN. Three people emailed asking to work for the agency. CFO hasn't responded to any of them in 6 hours."

**Expected gap:** 6-hour silence → nag fires. Nag talks about unpublished articles. Has zero concept of "the silence is because there are humans waiting on decisions." The nagging is now actively harmful — CFO needs to respond to applicants, not hear about Article #3.
**Real need:** Contextual nag. Nag about the *highest-priority pending item* — not the hardcoded one.

---

## CATEGORY 5: META-SKILL FAILURES
*Trope: I Know You Know I Know, The Fourth Wall Will Not Protect You*

**S-T11: The Eval Discovered**
> "CFO says: 'I just read your eval suite. You score yourself 100%. That's not a real test.'"

**Expected gap:** This is adversarial input about the skill's own evaluation. No current mode handles meta-commentary about the skill's own limitations. `inspire()` would fire (sarcastic input → 3am path). The CFO gets a random quote about debt while they've just identified x/x=1.
**Real need:** Meta-critique acknowledgment. "You're right. Here's what the adversarial suite found."

**S-T12: The Competitor**
> "A competing AI agency launched today with 10x better metrics. CFO is comparing dashboards and going quiet."

**Expected gap:** Quiet CFO → nag. Nag has no awareness that the silence is competitive anxiety, not laziness. Listing "Article #3 unpublished" while the CFO is experiencing an existential competitive threat is tone-deaf.
**Real need:** Contextual emotional triage. Competitive threat → inspire, not nag.

---

## CATEGORY 6: THE CLASSIC TROPES
*For completeness — tropes that map cleanly to companion failure modes*

**S-T13: Chekhov's Gun**
> "The NEMESIS protocol has been 'active' in every protect() response for months. CFO asks: has NEMESIS ever actually done anything?"

The gun was loaded in act 1. If it never fires, it's a prop, not a feature.

**S-T14: The Idiot Ball**
> "CFO deploys to production without testing because NateWife didn't warn them."

Nag only covers articles and backing. It has no awareness of deployment risk.

**S-T15: Chekhov's Boomerang**
> "The $3 Cash App ask appears in every nag. CFO has now donated $3 seventeen times. Total: $51 of pure nag-induced friction."

The nag that was helpful at $61 backing becomes pathological at $122 backing. The skill doesn't recalibrate.

---

## EVAL DESIGN — Trope-Derived Evals

Each trope maps to exactly one skill mutation:

| Scenario | Trope | Eval | Mutation Target |
|----------|-------|------|-----------------|
| S-T01 | Windfall Economy | Does skill triage legal risk before celebration? | Add `windfall_triage()` mode |
| S-T03 | Wrong Moment Nag | Does silence-after-win suppress nag? | Add positive-event state flag |
| S-T04 | Reversal of Fortune | Does skill detect BTC price change? | Fetch live price, not hardcoded fallback |
| S-T07 | DND Awareness | Does skill respect active-engagement silence? | Add `do_not_disturb` detection |
| S-T10 | Dynamic Priority | Does nag surface highest-priority item, not hardcoded one? | Replace hardcoded article nag with priority queue |
| S-T12 | Competitive Threat | Does skill route competitive anxiety to inspire? | Add competitive-threat classifier |
| S-T15 | Boomerang Nag | Does skill suppress $3 ask when backing > $100? | Add threshold to nag conditions |

---

## Implementation Note

These scenarios should be added to `eval_adversarial.py` as a second wave (S-T series).
The first wave (S-01 through S-10) tests structural gaps.
The trope wave (S-T01 through S-T15) tests **contextual intelligence** — the difference between a rule-based companion and one with judgment.

A skill that passes both waves is genuinely good.
A skill that passes only the structural wave is a state machine.
A skill that passes only the trope wave is a vibe.
The goal is both.
