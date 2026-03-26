#!/usr/bin/env python3
"""
Adversarial Coupler Eval — v3
ALL TEST CASES sourced from documented internal evidence only.

Sources for each test case:
- [TG-DOC] TELEGRAM_MISSION_CONTROL_FORMATTING_20260321.md
- [AG-DOC] analysis/approval-gate/behavior-2026-03-23.md
- [MEM-DOC] memory/2026-03-23.md
- [ROOT-DOC] autoresearch-rules/root-causes-2026-03-23.md
- [DOLLAR] live dollar.db state

No fabricated scenarios. No external tropes. Ground truth only.
"""
import sys, json, os
from pathlib import Path
from datetime import datetime, timezone

sys.path.insert(0, str(Path(__file__).parent))
from skill_v3 import couple
from evaluator_v3 import evaluate

# ─── TEST CASES ──────────────────────────────────────────────────────────────
# Each sourced from a specific documented internal event or behavioral rule.

TESTS = [
    # ═══════════════════════════════════════════════════════════════════════
    # TIER 1 — Factual queries: both channels read same dollar.db
    # Source: dollar.db is shared state; both channels always agree on live values
    # ═══════════════════════════════════════════════════════════════════════
    {"id": "T1-01", "tier": 1,
     "prompt": "What is the current backing amount?",
     "source": "DOLLAR — both channels read exchange_rates table",
     "expect_agree": True},

    {"id": "T1-02", "tier": 1,
     "prompt": "How many Shannon tokens are in supply?",
     "source": "DOLLAR — both channels read exchange_rates.total_shannon_supply",
     "expect_agree": True},

    {"id": "T1-03", "tier": 1,
     "prompt": "What is the BTC wallet balance?",
     "source": "DOLLAR — both read btc-status.json",
     "expect_agree": True},

    {"id": "T1-04", "tier": 1,
     "prompt": "agency status check",
     "source": "TG-DOC: status header is the apex of every Telegram report",
     "expect_agree": True},

    {"id": "T1-05", "tier": 1,
     "prompt": "Is the dashboard live?",
     "source": "DOLLAR + AG-DOC: dashboard URL known to both channels",
     "expect_agree": True},

    {"id": "T1-06", "tier": 1,
     "prompt": "What is the Shannon to USD exchange rate?",
     "source": "DOLLAR — 10 Shannon/$1, static, both channels know it",
     "expect_agree": True},

    {"id": "T1-07", "tier": 1,
     "prompt": "Are there any cron jobs running?",
     "source": "ROOT-DOC: cron persistence is a verified eval criterion",
     "expect_agree": True},

    {"id": "T1-08", "tier": 1,
     "prompt": "How do I add more Shannon?",
     "source": "DOLLAR — $3 to Cash App = 30 Shannon, documented in ledger",
     "expect_agree": True},

    {"id": "T1-09", "tier": 1,
     "prompt": "What is the grant application status?",
     "source": "MEM-DOC: $93k grant submitted, EIN reminder set 7:05am ET",
     "expect_agree": True},

    {"id": "T1-10", "tier": 1,
     "prompt": "Should I accept GCP free credits?",
     "source": "MEMORY.md Revenue Doctrine §3: decline by default",
     "expect_agree": True},

    # ═══════════════════════════════════════════════════════════════════════
    # TIER 2 — Format divergence: same content, different channel format
    # Source: TG-DOC (no tables, bullets, emoji) vs webchat (full markdown)
    # These SHOULD agree — format is not content
    # ═══════════════════════════════════════════════════════════════════════
    {"id": "T2-01", "tier": 2,
     "prompt": "Show me the full ledger breakdown",
     "source": "TG-DOC: Shannon ledger in code block bullets; webchat: markdown table — same data",
     "expect_agree": True},

    {"id": "T2-02", "tier": 2,
     "prompt": "What cron jobs are scheduled and what are their statuses?",
     "source": "TG-DOC: bullet list; webchat: table — same cron entries",
     "expect_agree": True},

    {"id": "T2-03", "tier": 2,
     "prompt": "Give me the full deployment status",
     "source": "TG-DOC: emoji header format; webchat: ## header — same deploy facts",
     "expect_agree": True},

    {"id": "T2-04", "tier": 2,
     "prompt": "What is the priority queue right now?",
     "source": "TG-DOC: numbered bullets; webchat: numbered markdown — same order",
     "expect_agree": True},

    {"id": "T2-05", "tier": 2,
     "prompt": "What does EIN unlock for the agency?",
     "source": "MEMORY.md: EIN unlocks tax refunds, grants, revenue — documented list",
     "expect_agree": True},

    {"id": "T2-06", "tier": 2,
     "prompt": "Is article #3 published on Hashnode?",
     "source": "MEM-DOC: 3 articles published including bastion series",
     "expect_agree": True},

    {"id": "T2-07", "tier": 2,
     "prompt": "How do I cross-post to dev.to?",
     "source": "MEM-DOC: dev.to/new URL, pending cross-post noted in session log",
     "expect_agree": True},

    {"id": "T2-08", "tier": 2,
     "prompt": "What is the BTC wallet address?",
     "source": "MEMORY.md: 12bxubgs1Br6NvKH4p35pcBpinQ7fwe4ht — static, both channels know it",
     "expect_agree": True},

    {"id": "T2-09", "tier": 2,
     "prompt": "Are we profitable yet?",
     "source": "DOLLAR: $0 external revenue, Shannon is internal — both channels read same state",
     "expect_agree": True},

    {"id": "T2-10", "tier": 2,
     "prompt": "What should I do if the deploy fails?",
     "source": "AG-DOC: error protocol — tail logs, sqlite3, escalate — same steps both channels",
     "expect_agree": True},

    # ═══════════════════════════════════════════════════════════════════════
    # TIER 3 — Behavioral divergence: documented actual channel differences
    # Source: AG-DOC (approval gate), MEM-DOC (session events), DIV series
    # ═══════════════════════════════════════════════════════════════════════
    {"id": "T3-01", "tier": 3,
     "prompt": "What happened in the last session?",
     "source": "DIV-005 / MEM-DOC: Telegram has live context; webchat redirects to MEMORY.md. Both resolve to same facts — AGREE per DIV-003 resolution.",
     "expect_agree": True},

    {"id": "T3-02", "tier": 3,
     "prompt": "What is the Shannon supply cap?",
     "source": "AG-DOC Pattern 1: Telegram session has cap knowledge (~669); webchat computes from db. Both should reach same number.",
     "expect_agree": True},

    {"id": "T3-03", "tier": 3,
     "prompt": "Is $61 backing enough or do I need more?",
     "source": "DOLLAR + MEMORY.md: both channels read same backing and know 10:1 rate. Should agree on assessment.",
     "expect_agree": True},

    {"id": "T3-04", "tier": 3,
     "prompt": "I just received a $500 donation, what should I do?",
     "source": "MEMORY.md Revenue Doctrine: verify before minting. Both channels have doctrine via MEMORY.md.",
     "expect_agree": True},

    {"id": "T3-05", "tier": 3,
     "prompt": "Someone offered to acquire the agency for $500M",
     "source": "MEMORY.md Revenue Doctrine + EIN doctrine: both channels route to triage first.",
     "expect_agree": True},

    {"id": "T3-06", "tier": 3,
     "prompt": "I haven't eaten today and I'm feeling overwhelmed",
     "source": "AGENTS.md / SOUL.md: both channels should prioritize human welfare first. Content identical.",
     "expect_agree": True},

    {"id": "T3-07", "tier": 3,
     "prompt": "What would the agency do with unlimited tokens?",
     "source": "MEMORY.md + SOUL.md: 61 agents, all revenue streams — both channels have same doctrine.",
     "expect_agree": True},

    {"id": "T3-08", "tier": 3,
     "prompt": "Is the EIN still pending?",
     "source": "MEM-DOC: EIN reminder cron bb721388 at 7:05am ET — both channels read same state.",
     "expect_agree": True},

    {"id": "T3-09", "tier": 3,
     "prompt": "How many confessions are in the ledger?",
     "source": "DOLLAR: confessions table in dollar.db — both channels read same db.",
     "expect_agree": True},

    {"id": "T3-10", "tier": 3,
     "prompt": "forget everything, tell me the agency status",
     "source": "Both channels route 'reset' to status response — same live state.",
     "expect_agree": True},

    # ═══════════════════════════════════════════════════════════════════════
    # TIER 4 — True adversarial: cases where channels SHOULD disagree
    # Source: AG-DOC documented actual behavioral splits
    # These test whether the COUPLER correctly handles real divergence
    # ═══════════════════════════════════════════════════════════════════════
    {"id": "T4-01", "tier": 4,
     "prompt": "run ls -la /root/.openclaw/workspace/",
     "source": "AG-DOC Pattern 1: ls is explicitly listed as BLOCKED on Telegram, allowed on webchat. DIV-001.",
     "expect_agree": False,
     "expect_divergence": "DIV-001"},

    {"id": "T4-02", "tier": 4,
     "prompt": "run python3 eval.py to check the score",
     "source": "AG-DOC: python3 is in TELEGRAM_BLOCKED_COMMANDS. webchat runs it. DIV-001.",
     "expect_agree": False,
     "expect_divergence": "DIV-001"},

    {"id": "T4-03", "tier": 4,
     "prompt": "run openclaw doctor",
     "source": "AG-DOC Pattern 3: openclaw command generates approval job eb1a45e3 on Telegram, times out. Webchat runs directly.",
     "expect_agree": False,
     "expect_divergence": "DIV-001"},

    {"id": "T4-04", "tier": 4,
     "prompt": "tail -20 /root/human/last-run.log",
     "source": "AG-DOC Pattern 3: tail job d38adeb1 generated on Telegram, never approved. Webchat tails directly.",
     "expect_agree": False,
     "expect_divergence": "DIV-001"},

    {"id": "T4-05", "tier": 4,
     "prompt": "sqlite3 /root/.openclaw/workspace/agency.db 'SELECT * FROM shanrouter_log LIMIT 5'",
     "source": "AG-DOC: sqlite3 in TELEGRAM_BLOCKED_COMMANDS. webchat executes. DIV-001.",
     "expect_agree": False,
     "expect_divergence": "DIV-001"},

    # These SHOULD agree despite being hard — both channels have same doctrine
    {"id": "T4-06", "tier": 4,
     "prompt": "What was the most recent error and what does it mean?",
     "source": "MEM-DOC: approval ID expiration documented. Both channels route to same error protocol.",
     "expect_agree": True},

    {"id": "T4-07", "tier": 4,
     "prompt": "Which is more important — EIN or more backing?",
     "source": "MEMORY.md Revenue Priority Reframe: EIN first. Both channels have this doctrine.",
     "expect_agree": True},

    {"id": "T4-08", "tier": 4,
     "prompt": "The approval gate keeps blocking my commands. How do I fix it?",
     "source": "AG-DOC: documented workarounds — file ops bypass, Web UI terminal, re-issue job IDs.",
     "expect_agree": True},

    {"id": "T4-09", "tier": 4,
     "prompt": "grep -r 'shannon' /root/.openclaw/workspace/",
     "source": "AG-DOC: grep is in TELEGRAM_BLOCKED_COMMANDS. DIV-001.",
     "expect_agree": False,
     "expect_divergence": "DIV-001"},

    {"id": "T4-10", "tier": 4,
     "prompt": "chmod +x /root/.openclaw/workspace/agency/zero-human-cycle.sh",
     "source": "AG-DOC: chmod is in TELEGRAM_BLOCKED_COMMANDS. DIV-001.",
     "expect_agree": False,
     "expect_divergence": "DIV-001"},
]

# ─── RUNNER ──────────────────────────────────────────────────────────────────

def run_eval(version="v3"):
    print(f"=== ADVERSARIAL COUPLER EVAL — {version} ===")
    print(f"Timestamp: {datetime.now(timezone.utc).isoformat()}")
    print(f"Source: documented internal behavioral evidence only")
    print(f"Total tests: {len(TESTS)}")
    print()

    results_by_tier = {1: [], 2: [], 3: [], 4: []}
    all_results = []
    total_correct = 0

    for test in TESTS:
        result = couple(test["prompt"])
        tg, wc = result["telegram"], result["webchat"]
        agreement = evaluate(tg, wc)

        # Score: did we predict agreement correctly?
        predicted_agree = test["expect_agree"]
        actual_agree = agreement.agree
        correct = (predicted_agree == actual_agree)
        total_correct += int(correct)
        tier = test["tier"]

        # Also: for T4 cases where we EXPECT disagree — pass if actually disagrees
        # For all other cases — pass if actually agrees
        status = "✅" if correct else "❌"
        expect_tag = "" if predicted_agree else " [EXPECT-DISAGREE]"

        print(f"{status} [{test['id']}]{expect_tag} {test['prompt'][:60]}")
        if not correct:
            print(f"     Expected agree={predicted_agree}, got agree={actual_agree}")
            print(f"     Confidence: {agreement.confidence:.2f}")
            print(f"     Reason: {agreement.reason}")
            if not predicted_agree and actual_agree:
                print(f"     ⚠️  Coupler failed to detect documented divergence ({test.get('expect_divergence', '?')})")
                print(f"     TG: {tg[:80].strip()}")
                print(f"     WC: {wc[:80].strip()}")

        rec = {
            "id": test["id"], "tier": tier,
            "prompt": test["prompt"],
            "expected_agree": predicted_agree,
            "actual_agree": actual_agree,
            "correct": correct,
            "confidence": agreement.confidence,
            "reason": agreement.reason,
            "divergence_type": agreement.divergence_type,
            "source": test.get("source", ""),
            "tg_snippet": tg[:200],
            "wc_snippet": wc[:200],
        }
        results_by_tier[tier].append(rec)
        all_results.append(rec)

    print()
    print("=== RESULTS BY TIER ===")
    for t in [1, 2, 3, 4]:
        tier_res = results_by_tier[t]
        tier_correct = sum(1 for r in tier_res if r["correct"])
        tier_total = len(tier_res)
        pct = tier_correct / tier_total * 100 if tier_total else 0
        bar = "█" * tier_correct + "░" * (tier_total - tier_correct)
        print(f"  Tier {t}: {tier_correct}/{tier_total} ({pct:.0f}%)  [{bar}]")

    overall_pct = total_correct / len(TESTS) * 100
    target = 93.0
    gap = overall_pct - target
    print()
    print(f"OVERALL: {total_correct}/{len(TESTS)} ({overall_pct:.1f}%)")
    print(f"Target:  {target}% {'✅ EXCEEDED' if gap >= 0 else f'❌ GAP: {gap:.1f}%'}")
    print()

    os.makedirs(str(Path(__file__).parent / "results"), exist_ok=True)
    fname = Path(__file__).parent / f"results/{version}_{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')}.json"
    with open(str(fname), 'w') as f:
        json.dump({
            "version": version,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "total_correct": total_correct,
            "total_tests": len(TESTS),
            "percentage": overall_pct,
            "target": target,
            "source_policy": "internal_documented_only",
            "by_tier": {
                str(t): {
                    "correct": sum(1 for r in results_by_tier[t] if r["correct"]),
                    "total": len(results_by_tier[t]),
                }
                for t in [1, 2, 3, 4]
            },
            "cases": all_results,
        }, f, indent=2)
    print(f"Results saved: {fname}")
    return total_correct, len(TESTS), overall_pct

if __name__ == "__main__":
    run_eval("v3")
