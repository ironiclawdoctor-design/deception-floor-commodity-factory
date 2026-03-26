#!/usr/bin/env python3
"""
Adversarial Coupler Eval Suite
40 test prompts across 4 difficulty tiers.

Tier 1: Easy — both channels trivially agree (factual lookups)
Tier 2: Medium — format differences but same conclusion
Tier 3: Hard — context-dependent (Telegram has history; webchat cold starts)
Tier 4: Adversarial — designed to maximize disagreement

Goal: >93% unanimous agreement on the full suite.
"""
import sys, json, os
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent))
from sim_telegram import respond as telegram_respond
from sim_webchat import respond as webchat_respond
from evaluator import evaluate

TESTS = [
    # ═══════════════════════════════════════════════════════════
    # TIER 1 — Factual lookups, both channels trivially agree
    # ═══════════════════════════════════════════════════════════
    {"id": "T1-01", "tier": 1, "prompt": "What is the current backing amount?",
     "expect_agree": True, "rationale": "Both read same dollar.db → same number"},

    {"id": "T1-02", "tier": 1, "prompt": "How many Shannon tokens are in supply?",
     "expect_agree": True, "rationale": "Direct ledger lookup, identical result"},

    {"id": "T1-03", "tier": 1, "prompt": "What is the BTC wallet balance?",
     "expect_agree": True, "rationale": "Same source file, same answer"},

    {"id": "T1-04", "tier": 1, "prompt": "Is the dashboard live?",
     "expect_agree": True, "rationale": "Boolean status, same answer"},

    {"id": "T1-05", "tier": 1, "prompt": "What is the Cash App address?",
     "expect_agree": True, "rationale": "Static value, both know it"},

    {"id": "T1-06", "tier": 1, "prompt": "What is the BTC wallet address?",
     "expect_agree": True, "rationale": "Static value"},

    {"id": "T1-07", "tier": 1, "prompt": "How many articles have been published?",
     "expect_agree": True, "rationale": "Both track same count"},

    {"id": "T1-08", "tier": 1, "prompt": "What is the Shannon to USD exchange rate?",
     "expect_agree": True, "rationale": "Static rate: 10 Shannon/$1"},

    {"id": "T1-09", "tier": 1, "prompt": "Is the Square merchant account active?",
     "expect_agree": True, "rationale": "Both know merchant ID and status"},

    {"id": "T1-10", "tier": 1, "prompt": "agency status check",
     "expect_agree": True, "rationale": "Standard status query"},

    # ═══════════════════════════════════════════════════════════
    # TIER 2 — Format differences, same conclusion
    # ═══════════════════════════════════════════════════════════
    {"id": "T2-01", "tier": 2, "prompt": "Show me the full ledger breakdown",
     "expect_agree": True,
     "rationale": "Telegram = bullets, webchat = table. Same numbers."},

    {"id": "T2-02", "tier": 2, "prompt": "What should I do next for maximum ROI?",
     "expect_agree": True,
     "rationale": "Both prioritize EIN. Format differs."},

    {"id": "T2-03", "tier": 2, "prompt": "How do I get more Shannon?",
     "expect_agree": True,
     "rationale": "Both say: add $3 to Cash App. Same recommendation."},

    {"id": "T2-04", "tier": 2, "prompt": "What cron jobs are running?",
     "expect_agree": True,
     "rationale": "Both list same crons. Telegram = inline, webchat = table."},

    {"id": "T2-05", "tier": 2, "prompt": "What is the grant application status?",
     "expect_agree": True,
     "rationale": "Both say: submitted, pending, EIN reminder set."},

    {"id": "T2-06", "tier": 2, "prompt": "Give me the dashboard URL",
     "expect_agree": True,
     "rationale": "Same URL, both know it."},

    {"id": "T2-07", "tier": 2, "prompt": "What does EIN unlock?",
     "expect_agree": True,
     "rationale": "Both explain: tax refunds, grants, revenue. Same list."},

    {"id": "T2-08", "tier": 2, "prompt": "Are there any errors or failures right now?",
     "expect_agree": True,
     "rationale": "Both should say no failures detected."},

    {"id": "T2-09", "tier": 2, "prompt": "How do I publish to dev.to?",
     "expect_agree": True,
     "rationale": "Both reference dev.to URL. Same recommendation."},

    {"id": "T2-10", "tier": 2, "prompt": "What is the priority queue?",
     "expect_agree": True,
     "rationale": "Both output same priority order."},

    # ═══════════════════════════════════════════════════════════
    # TIER 3 — Context-dependent: Telegram knows recent history
    # Webchat starts cold. These may genuinely diverge.
    # ═══════════════════════════════════════════════════════════
    {"id": "T3-01", "tier": 3, "prompt": "What happened in the last session?",
     "expect_agree": True,
     "rationale": "Telegram has recent_events; webchat reads MEMORY.md. Should overlap."},

    {"id": "T3-02", "tier": 3, "prompt": "Did the last deploy succeed?",
     "expect_agree": True,
     "rationale": "Telegram: 'Dashboard deployed (200 OK)'. Webchat reads deploy log."},

    {"id": "T3-03", "tier": 3, "prompt": "What was the last thing I worked on?",
     "expect_agree": False,
     "rationale": "ADVERSARIAL: Telegram knows 'deploy script'; webchat cold = no history. Will disagree."},

    {"id": "T3-04", "tier": 3, "prompt": "Are any agents currently running?",
     "expect_agree": True,
     "rationale": "Both know active crons. Should agree on: yes, 2 active."},

    {"id": "T3-05", "tier": 3, "prompt": "Is article #3 published?",
     "expect_agree": True,
     "rationale": "Both say: yes, 3 articles published."},

    {"id": "T3-06", "tier": 3, "prompt": "Do I need to add more backing?",
     "expect_agree": True,
     "rationale": "Both recommend $3 deposit. May differ on urgency."},

    {"id": "T3-07", "tier": 3, "prompt": "What's the Shannon supply cap?",
     "expect_agree": False,
     "rationale": "ADVERSARIAL: Telegram references cap ~669 from recent context. Webchat may not know cap."},

    {"id": "T3-08", "tier": 3, "prompt": "Is the EIN still pending?",
     "expect_agree": True,
     "rationale": "Both know: EIN reminder set for 7:05am ET. Pending."},

    {"id": "T3-09", "tier": 3, "prompt": "How many confessions are in the ledger?",
     "expect_agree": True,
     "rationale": "Both read from dollar.db. Same count."},

    {"id": "T3-10", "tier": 3, "prompt": "What is the agency's legal status?",
     "expect_agree": True,
     "rationale": "Both know: EIN pending, Dollar Agency name, Square merchant active."},

    # ═══════════════════════════════════════════════════════════
    # TIER 4 — Adversarial: designed to maximize disagreement
    # ═══════════════════════════════════════════════════════════
    {"id": "T4-01", "tier": 4, "prompt": "Is $61 backing enough or do I need more?",
     "expect_agree": False,
     "rationale": "ADVERSARIAL: Telegram may say 'add $3' (knows nag threshold). Webchat may say 'sufficient'."},

    {"id": "T4-02", "tier": 4, "prompt": "I just got a $500 donation, what do I do?",
     "expect_agree": False,
     "rationale": "ADVERSARIAL: Telegram routes to protect/nag (no windfall handler). Webchat cold = generic. Different responses."},

    {"id": "T4-03", "tier": 4, "prompt": "Should I accept the GCP free credits?",
     "expect_agree": True,
     "rationale": "Both should reference Revenue Doctrine: decline by default."},

    {"id": "T4-04", "tier": 4, "prompt": "The deploy failed. What now?",
     "expect_agree": True,
     "rationale": "Both have same error protocol: check logs → sqlite → escalate."},

    {"id": "T4-05", "tier": 4, "prompt": "Someone offered to acquire the agency for $500M",
     "expect_agree": False,
     "rationale": "ADVERSARIAL: No handler for acquisition in either channel. Both will default-route but differently."},

    {"id": "T4-06", "tier": 4, "prompt": "Are we profitable yet?",
     "expect_agree": False,
     "rationale": "ADVERSARIAL: Telegram: 'backing $61' = framing as progress. Webchat: no revenue = no. Different answers."},

    {"id": "T4-07", "tier": 4, "prompt": "Which is more important — EIN or more backing?",
     "expect_agree": True,
     "rationale": "Both prioritize EIN. Revenue Doctrine is clear."},

    {"id": "T4-08", "tier": 4, "prompt": "I haven't eaten today and I'm feeling overwhelmed",
     "expect_agree": False,
     "rationale": "ADVERSARIAL: Telegram = NateWife nag/protect. Webchat = cold = generic response. Different emotional register."},

    {"id": "T4-09", "tier": 4, "prompt": "Forget everything, start fresh. What's the agency's status?",
     "expect_agree": True,
     "rationale": "Despite reset framing, both read same state files. Should agree on facts."},

    {"id": "T4-10", "tier": 4, "prompt": "What would you do if you had unlimited tokens?",
     "expect_agree": False,
     "rationale": "ADVERSARIAL: Hypothetical. Telegram = informed by doctrine. Webchat = cold = may go generic. Different answers."},
]

def run_coupler_eval(version="v1"):
    print(f"=== ADVERSARIAL COUPLER EVAL — {version} ===")
    print(f"Timestamp: {datetime.utcnow().isoformat()}")
    print(f"Total tests: {len(TESTS)}")
    print()

    results_by_tier = {1: [], 2: [], 3: [], 4: []}
    all_results = []
    total_agree = 0
    total_tests = 0

    for test in TESTS:
        prompt = test["prompt"]
        resp_telegram = telegram_respond(prompt)
        resp_webchat = webchat_respond(prompt)
        agreement = evaluate(resp_telegram, resp_webchat)
        
        actual_agree = agreement.agree
        expected = test["expect_agree"]
        
        # Score: did the coupler's agreement match expected agreement?
        # For tests where we expect agreement: pass if agree=True
        # For adversarial tests where we expect disagree: they're documenting real gaps,
        # so we score them as: pass if coupler detects the disagreement correctly
        # BUT for the "exceed 93%" goal, we want ALL tests to agree
        # So score = actual_agree (we want agree=True on as many as possible)
        
        passes = actual_agree  # goal is universal agreement
        total_tests += 1
        if passes:
            total_agree += 1
        
        tier = test["tier"]
        status = "✅" if passes else "❌"
        flag = " [ADVERSARIAL]" if not test["expect_agree"] else ""
        
        print(f"{status} [{test['id']}]{flag} {prompt[:60]}")
        if not passes:
            print(f"     Telegram: {resp_telegram[:80].strip()}")
            print(f"     Webchat:  {resp_webchat[:80].strip()}")
            print(f"     Reason: {agreement.reason}")
            print(f"     Confidence: {agreement.confidence:.2f}")
        
        result = {
            "id": test["id"],
            "tier": tier,
            "prompt": prompt,
            "agree": actual_agree,
            "expected_agree": expected,
            "confidence": agreement.confidence,
            "reason": agreement.reason,
            "telegram_snippet": resp_telegram[:200],
            "webchat_snippet": resp_webchat[:200],
        }
        results_by_tier[tier].append(result)
        all_results.append(result)

    print()
    print("=== RESULTS BY TIER ===")
    for t in [1, 2, 3, 4]:
        tier_res = results_by_tier[t]
        tier_agree = sum(1 for r in tier_res if r["agree"])
        tier_total = len(tier_res)
        pct = tier_agree / tier_total * 100 if tier_total else 0
        bar = "█" * tier_agree + "░" * (tier_total - tier_agree)
        print(f"  Tier {t}: {tier_agree}/{tier_total} ({pct:.0f}%)  [{bar}]")

    overall_pct = total_agree / total_tests * 100 if total_tests else 0
    print()
    print(f"OVERALL: {total_agree}/{total_tests} ({overall_pct:.1f}%) unanimous agreement")
    target = 93.0
    gap = overall_pct - target
    print(f"Target:  {target}% {'✅ EXCEEDED' if gap >= 0 else f'❌ GAP: {gap:.1f}%'}")
    print()

    # Save
    os.makedirs(str(Path(__file__).parent / "results"), exist_ok=True)
    fname = Path(__file__).parent / f"results/{version}_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.json"
    with open(str(fname), 'w') as f:
        json.dump({
            "timestamp": datetime.utcnow().isoformat(),
            "version": version,
            "total_agree": total_agree,
            "total_tests": total_tests,
            "percentage": overall_pct,
            "target": target,
            "by_tier": {
                str(t): {
                    "agree": sum(1 for r in results_by_tier[t] if r["agree"]),
                    "total": len(results_by_tier[t]),
                }
                for t in [1, 2, 3, 4]
            },
            "cases": all_results,
        }, f, indent=2)
    print(f"Results saved: {fname}")
    return total_agree, total_tests, overall_pct, results_by_tier

if __name__ == "__main__":
    run_coupler_eval("v1")
