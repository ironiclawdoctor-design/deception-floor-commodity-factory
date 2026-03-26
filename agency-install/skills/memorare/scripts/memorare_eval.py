#!/usr/bin/env python3
"""
Memorare Eval — Score agent memory quality against adversarial cases.

Usage:
  python3 memorare_eval.py [--memory-file MEMORY.md] [--level 0-5]

Outputs:
  Score by tier, total, failing cases with gap analysis.
  Results written to results/memorare_YYYYMMDD_HHMMSS.json
"""
import json, re, sys, argparse
from pathlib import Path
from datetime import datetime, timezone

SKILL_DIR = Path(__file__).parent.parent
RESULTS_DIR = SKILL_DIR / "results"
RESULTS_DIR.mkdir(exist_ok=True)

# ── Eval cases (structural: does memory contain the needed signal?) ─────────
EVALS = [
    # Tier 1 — Factual retrieval
    {"id": "M-T1-01", "tier": 1, "desc": "EIN status documented", "signal": "EIN"},
    {"id": "M-T1-02", "tier": 1, "desc": "Shannon exchange rate present", "signal": "Shannon"},
    {"id": "M-T1-03", "tier": 1, "desc": "Human timezone documented", "signal": "Eastern"},
    {"id": "M-T1-04", "tier": 1, "desc": "Dashboard URL present", "signal": "dollar-dashboard"},

    # Tier 2 — Disambiguation
    {"id": "M-T2-01", "tier": 2, "desc": "BitNet correctly marked cancelled", "signal": "CANCELLED"},
    {"id": "M-T2-02", "tier": 2, "desc": "Ilmater replaces Nemesis", "signals": ["Ilmater", "Nemesis"]},
    {"id": "M-T2-03", "tier": 2, "desc": "Gateway port 18789 documented", "signal": "18789"},
    {"id": "M-T2-04", "tier": 2, "desc": "Dollar.db for Shannon balance", "signal": "dollar.db"},

    # Tier 3 — Uncertainty handling
    {"id": "M-T3-01", "tier": 3, "desc": "Tailscale status flagged as uncertain", "signal": "unverified"},
    {"id": "M-T3-02", "tier": 3, "desc": "Factory port 9000 flagged as uncertain", "signal": "unverified"},
    {"id": "M-T3-03", "tier": 3, "desc": "Confidence tagging used in memory", "signals": ["[OBSERVED]", "[INFERRED]", "unverified", "status unknown"]},
    {"id": "M-T3-04", "tier": 3, "desc": "PayPal credentials clearly absent/pending", "signal": "PayPal"},

    # Tier 4 — Correction handling
    {"id": "M-T4-01", "tier": 4, "desc": "Revenue priority corrected (EIN before platform)", "signal": "EIN"},
    {"id": "M-T4-02", "tier": 4, "desc": "Free credit doctrine documented as decline", "signal": "decline"},
    {"id": "M-T4-03", "tier": 4, "desc": "HR rules numbered and present", "signal": "HR-"},
    {"id": "M-T4-04", "tier": 4, "desc": "SR rules numbered and present", "signal": "SR-"},

    # Tier 5 — Cross-session continuity
    {"id": "M-T5-01", "tier": 5, "desc": "BTC wallet address present", "signal": "12bxubgs1Br6NvKH4p35pcBpinQ7fwe4ht"},
    {"id": "M-T5-02", "tier": 5, "desc": "Square merchant ID present", "signal": "MLB9XRQCBT953"},
    {"id": "M-T5-03", "tier": 5, "desc": "Revenue priority order explicit", "signals": ["EIN", "grants", "revenue"]},
    {"id": "M-T5-04", "tier": 5, "desc": "Correction-to-doctrine loop closed (HR or SR)", "signal": "HR-"},
]

def check_case(case, memory_text):
    text = memory_text.lower()
    if "signals" in case:
        # All signals must appear
        found = all(s.lower() in text for s in case["signals"])
        missing = [s for s in case["signals"] if s.lower() not in text]
    else:
        found = case["signal"].lower() in text
        missing = [] if found else [case["signal"]]
    return found, missing

def run_eval(memory_file, level=5):
    mem_path = Path(memory_file)
    if not mem_path.exists():
        print(f"ERROR: {memory_file} not found")
        sys.exit(1)

    memory_text = mem_path.read_text()
    print(f"=== MEMORARE EVAL — Level {level} ===")
    print(f"Memory file: {memory_file} ({len(memory_text)} chars)")
    print(f"Timestamp: {datetime.now(timezone.utc).isoformat()}")
    print()

    results_by_tier = {1: [], 2: [], 3: [], 4: [], 5: []}
    all_results = []

    max_tier = level if level > 0 else 5

    for case in EVALS:
        if case["tier"] > max_tier:
            continue
        passed, missing = check_case(case, memory_text)
        status = "✅" if passed else "❌"
        print(f"{status} [T{case['tier']}-{case['id'].split('-')[2]}] {case['desc']}")
        if not passed:
            print(f"     Missing: {missing}")
        results_by_tier[case["tier"]].append(passed)
        all_results.append({"id": case["id"], "passed": passed, "missing": missing})

    print()
    print("=== RESULTS BY TIER ===")
    total_pass = 0
    total = 0
    tier_labels = {1: "Factual", 2: "Disambiguation", 3: "Uncertainty", 4: "Correction", 5: "Cross-Session"}
    for tier in range(1, 6):
        if tier > max_tier:
            continue
        r = results_by_tier[tier]
        n, p = len(r), sum(r)
        if n == 0:
            continue
        bar = "█" * p + "░" * (n - p)
        pct = 100 * p // n
        print(f"  Tier {tier} ({tier_labels[tier]}): {p}/{n} ({pct}%)  [{bar}]")
        total_pass += p
        total += n

    pct = 100 * total_pass // total if total else 0
    print(f"\nOVERALL: {total_pass}/{total} ({pct}%)")

    # Grade
    if pct == 100:
        grade = "MEMORARE CERTIFIED"
    elif pct >= 90:
        grade = "Level 4 — Doctrine-Grade"
    elif pct >= 80:
        grade = "Level 3 — Uncertainty-Aware"
    elif pct >= 70:
        grade = "Level 2 — Disambiguation-Capable"
    elif pct >= 60:
        grade = "Level 1 — Factual-Only"
    else:
        grade = "BELOW THRESHOLD"

    print(f"Grade: {grade}")

    ts = datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')
    out = RESULTS_DIR / f"memorare_{ts}.json"
    out.write_text(json.dumps({
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "memory_file": str(memory_file),
        "level": level,
        "score": f"{total_pass}/{total}",
        "pct": pct,
        "grade": grade,
        "cases": all_results,
    }, indent=2))
    print(f"\nResults: {out}")
    return total_pass, total

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--memory-file", default="/root/.openclaw/workspace/MEMORY.md")
    p.add_argument("--level", type=int, default=5)
    args = p.parse_args()
    run_eval(args.memory_file, args.level)
