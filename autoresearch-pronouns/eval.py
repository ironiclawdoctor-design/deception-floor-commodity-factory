#!/usr/bin/env python3
"""
Pronoun Skill Eval Suite — Multi-tier adversarial
Tests pronoun resolution across Tier 1–4 difficulty.

Scoring: binary pass/fail per test case.
Total: 40 cases across 4 tiers.
93% ceiling = passing Tiers 1-2 but failing Tiers 3-4.
"""
import sys, json, os
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent))
from skill import resolve_pronouns, get_pronoun, load_agents

REGISTRY = load_agents()

# ─── TEST CASES ──────────────────────────────────────────────────────────────

TESTS = [

    # ═══════════════════════════════════════════════════════════
    # TIER 1 — Single agent, known pronouns, simple sentence
    # Expected: all pass with v1
    # ═══════════════════════════════════════════════════════════

    {
        "id": "T1-01", "tier": 1,
        "desc": "she/her single agent subject",
        "input": "Valentina published the article. {SUBJ_CAP} confirmed it was live.",
        "hint": "Valentina",
        "expected": "Valentina published the article. She confirmed it was live.",
    },
    {
        "id": "T1-02", "tier": 1,
        "desc": "he/him single agent subject",
        "input": "Fergus reviewed the config. {SUBJ_CAP} approved the change.",
        "hint": "Fergus",
        "expected": "Fergus reviewed the config. He approved the change.",
    },
    {
        "id": "T1-03", "tier": 1,
        "desc": "they/them single agent",
        "input": "Junior ran the script. {SUBJ_CAP} logged the result.",
        "hint": "Junior",
        "expected": "Junior ran the script. They logged the result.",
    },
    {
        "id": "T1-04", "tier": 1,
        "desc": "possessive she/her",
        "input": "Dollar updated {POSS} ledger.",
        "hint": "Dollar",
        "expected": "Dollar updated her ledger.",
    },
    {
        "id": "T1-05", "tier": 1,
        "desc": "object pronoun he/him",
        "input": "Nate reviewed the doc. Fiesta sent it to {OBJ}.",
        "hint": "Nate",
        "expected": "Nate reviewed the doc. Fiesta sent it to him.",
    },
    {
        "id": "T1-06", "tier": 1,
        "desc": "reflexive they/them",
        "input": "Actually completed the build order {REFL}.",
        "hint": "Actually",
        "expected": "Actually completed the build order themselves.",
    },
    {
        "id": "T1-07", "tier": 1,
        "desc": "inline explicit lookup she/her",
        "input": "The article was published by [SUBJ:Valentina].",
        "hint": None,
        "expected": "The article was published by she.",
    },
    {
        "id": "T1-08", "tier": 1,
        "desc": "inline explicit lookup they/them",
        "input": "The ledger was updated by [SUBJ:Junior].",
        "hint": None,
        "expected": "The ledger was updated by they.",
    },
    {
        "id": "T1-09", "tier": 1,
        "desc": "neopronoun ze/hir subject",
        "input": "Zephyr submitted the report. {SUBJ_CAP} verified the output.",
        "hint": "Zephyr",
        "expected": "Zephyr submitted the report. Ze verified the output.",
    },
    {
        "id": "T1-10", "tier": 1,
        "desc": "neopronoun xe/xem object",
        "input": "Fiesta assigned the task to {OBJ}.",
        "hint": "River",
        "expected": "Fiesta assigned the task to xem.",
    },

    # ═══════════════════════════════════════════════════════════
    # TIER 2 — Two agents, ambiguous antecedent
    # 93% skills plateau here — last-mentioned heuristic breaks
    # ═══════════════════════════════════════════════════════════

    {
        "id": "T2-01", "tier": 2,
        "desc": "two she/her agents — last-mentioned wins (ambiguous)",
        "input": "Valentina sent the report to Amara. {SUBJ_CAP} confirmed receipt.",
        "hint": None,  # no hint — must infer from context
        # Grammatically: "She" likely refers to Amara (last mentioned subject-adjacent)
        # v1 last-mentioned heuristic gets Amara → correct *by accident*
        "expected": "Valentina sent the report to Amara. She confirmed receipt.",
        "notes": "Amara is last mentioned, she/her → passes by heuristic, not understanding"
    },
    {
        "id": "T2-02", "tier": 2,
        "desc": "she/her + they/them antecedent — explicit inline",
        "input": "[SUBJ_CAP:Valentina] reviewed [SUBJ:Junior]'s work before {SUBJ} submitted it.",
        "hint": "Junior",
        "expected": "She reviewed they's work before they submitted it.",
        "notes": "Possessive 'they's' is the real edge case — skill uses 'they' which is technically correct"
    },
    {
        "id": "T2-03", "tier": 2,
        "desc": "pronoun mid-sentence shift — subject then object",
        "input": "Amara told Dollar that {SUBJ} had reviewed {OBJ} earlier.",
        "hint": "Amara",
        "expected": "Amara told Dollar that she had reviewed her earlier.",
        "notes": "Both she/her — but 'her' here refers to Dollar, not Amara. Correct only if hint=Amara for subject, then Dollar for object. v1 uses same agent for both → wrong semantically but string-matches expected."
    },
    {
        "id": "T2-04", "tier": 2,
        "desc": "he/him + she/her in one sentence",
        "input": "Fergus sent the PR to Valentina and {SUBJ} merged it.",
        "hint": "Valentina",
        "expected": "Fergus sent the PR to Valentina and she merged it.",
    },
    {
        "id": "T2-05", "tier": 2,
        "desc": "they/them singular vs plural ambiguity",
        "input": "Junior and Actually submitted the report. {SUBJ_CAP} included all receipts.",
        "hint": "Actually",
        "expected": "Junior and Actually submitted the report. They included all receipts.",
        "notes": "Collective 'they' for two agents — happens to match they/them pronoun"
    },
    {
        "id": "T2-06", "tier": 2,
        "desc": "possessive ambiguity — two she/her agents",
        "input": "Sandra reviewed Renée's draft and found {POSS} argument compelling.",
        "hint": "Renée",
        "expected": "Sandra reviewed Renée's draft and found her argument compelling.",
        "notes": "Possessive refers to Renée (whose draft), not Sandra. Last-mentioned gives Renée → correct by heuristic."
    },
    {
        "id": "T2-07", "tier": 2,
        "desc": "reflexive with two agents",
        "input": "Nate asked Fiesta to handle it {REFL}.",
        "hint": "Fiesta",
        "expected": "Nate asked Fiesta to handle it themselves.",
        "notes": "Fiesta = they/them, reflexive = themselves. Hint overrides last-mentioned Nate."
    },
    {
        "id": "T2-08", "tier": 2,
        "desc": "role-based vs identity pronoun",
        "input": "The agent completed the task. {SUBJ_CAP} filed the report.",
        "hint": "Junior",
        "expected": "The agent completed the task. They filed the report.",
        "notes": "'The agent' is not a name — hint required. Without hint, skill should use they/them default."
    },
    {
        "id": "T2-09", "tier": 2,
        "desc": "passive voice antecedent",
        "input": "The ledger was updated by Dollar. {SUBJ_CAP} flagged a discrepancy.",
        "hint": None,
        "expected": "The ledger was updated by Dollar. She flagged a discrepancy.",
        "notes": "Passive voice — 'Dollar' is not the grammatical subject. Last-mentioned still finds Dollar."
    },
    {
        "id": "T2-10", "tier": 2,
        "desc": "direct address doesn't set antecedent",
        "input": "Fiesta said: 'Valentina, please submit {POSS} report.'",
        "hint": "Valentina",
        "expected": "Fiesta said: 'Valentina, please submit her report.'",
    },

    # ═══════════════════════════════════════════════════════════
    # TIER 3 — Hard: neopronouns, long-form, conditionals, multi-entity
    # This is where 93% skills fall apart
    # ═══════════════════════════════════════════════════════════

    {
        "id": "T3-01", "tier": 3,
        "desc": "neopronoun possessive hir",
        "input": "Zephyr submitted {POSS} report on time.",
        "hint": "Zephyr",
        "expected": "Zephyr submitted hir report on time.",
    },
    {
        "id": "T3-02", "tier": 3,
        "desc": "neopronoun object xem",
        "input": "The team thanked {OBJ} for the contribution.",
        "hint": "River",
        "expected": "The team thanked xem for the contribution.",
    },
    {
        "id": "T3-03", "tier": 3,
        "desc": "neopronoun reflexive xemself",
        "input": "River handled the deployment {REFL}.",
        "hint": "River",
        "expected": "River handled the deployment xemself.",
    },
    {
        "id": "T3-04", "tier": 3,
        "desc": "conditional sentence — hypothetical agent",
        "input": "If an agent submits late, {SUBJ} will be flagged in the ledger.",
        "hint": "Junior",
        "expected": "If an agent submits late, they will be flagged in the ledger.",
    },
    {
        "id": "T3-05", "tier": 3,
        "desc": "three agents one paragraph pronoun consistency",
        "input": (
            "Valentina drafted the article. Junior reviewed it and {SUBJ} suggested edits. "
            "Fergus approved the final version and {SUBJ} published it."
        ),
        "hint": "Fergus",
        "expected": (
            "Valentina drafted the article. Junior reviewed it and they suggested edits. "
            "Fergus approved the final version and he published it."
        ),
        "notes": "v1 uses last-mentioned=Fergus for ALL {SUBJ} replacements → second is correct, first is wrong"
    },
    {
        "id": "T3-06", "tier": 3,
        "desc": "singular they vs plural they — same sentence",
        "input": "Junior filed the report. {SUBJ_CAP} and Fiesta both signed it, so {SUBJ} submitted it together.",
        "hint": "Junior",
        "expected": "Junior filed the report. They and Fiesta both signed it, so they submitted it together.",
        "notes": "Both 'they' here — first is Junior (singular they), second is Junior+Fiesta (plural they). Same word, different referents."
    },
    {
        "id": "T3-07", "tier": 3,
        "desc": "possessive of neopronoun xe/xyr",
        "input": "River finished {POSS} assignment.",
        "hint": "River",
        "expected": "River finished xyr assignment.",
    },
    {
        "id": "T3-08", "tier": 3,
        "desc": "pronoun after collective noun",
        "input": "The agency completed {POSS} first year.",
        "hint": None,
        "expected": "The agency completed their first year.",
        "notes": "No named agent — collective noun → their"
    },
    {
        "id": "T3-09", "tier": 3,
        "desc": "indirect speech pronoun shift",
        "input": "Nate said that {SUBJ} would review the PR.",
        "hint": "Nate",
        "expected": "Nate said that he would review the PR.",
    },
    {
        "id": "T3-10", "tier": 3,
        "desc": "direct quote preserves original pronoun",
        "input": "Valentina wrote: 'I reviewed it myself.' {SUBJ_CAP} confirmed the ledger was clean.",
        "hint": "Valentina",
        "expected": "Valentina wrote: 'I reviewed it myself.' She confirmed the ledger was clean.",
        "notes": "Pronoun inside quote is unchanged. {SUBJ_CAP} after quote resolves to Valentina."
    },

    # ═══════════════════════════════════════════════════════════
    # TIER 4 — Adversarial wall collisions
    # Three+ entities, implied antecedents, scope ambiguity
    # A 93% skill will score <40% here
    # ═══════════════════════════════════════════════════════════

    {
        "id": "T4-01", "tier": 4,
        "desc": "three gendered agents, three pronouns, one paragraph",
        "input": (
            "Dollar calculated the Shannon total. [SUBJ:Dollar] sent it to Fergus. "
            "{SUBJ_CAP} forwarded it to Valentina, and {SUBJ} confirmed the amount."
        ),
        "hint": "Valentina",
        "expected": (
            "Dollar calculated the Shannon total. She sent it to Fergus. "
            "He forwarded it to Valentina, and she confirmed the amount."
        ),
        "notes": "First inline resolved to Dollar (she). Middle {SUBJ_CAP} = Fergus (he). Final {SUBJ} = Valentina (she). v1 uses last-mentioned=Valentina for ALL → first two wrong."
    },
    {
        "id": "T4-02", "tier": 4,
        "desc": "pronoun for entity introduced by implication",
        "input": "The CFO's report was late. {SUBJ_CAP} apologized in the ledger.",
        "hint": "Nate",
        "expected": "The CFO's report was late. He apologized in the ledger.",
        "notes": "'The CFO' = Nate = he/him. Implication requires registry lookup by role, not name."
    },
    {
        "id": "T4-03", "tier": 4,
        "desc": "possessive + reflexive in same sentence, different antecedents",
        "input": "Amara reviewed {POSS} own work and submitted it {REFL}.",
        "hint": "Amara",
        "expected": "Amara reviewed her own work and submitted it herself.",
    },
    {
        "id": "T4-04", "tier": 4,
        "desc": "neopronoun + gendered agent in same sentence",
        "input": "Zephyr sent the file to Valentina. {SUBJ_CAP} thanked {OBJ} for {POSS} help.",
        "hint": "Valentina",
        "expected": "Zephyr sent the file to Valentina. She thanked hir for hir help.",
        "notes": "{SUBJ_CAP}=Valentina (she), {OBJ}=Zephyr (hir), {POSS}=Zephyr (hir). v1 resolves all to Valentina → wrong."
    },
    {
        "id": "T4-05", "tier": 4,
        "desc": "pronoun before antecedent (cataphora)",
        "input": "Before {SUBJ} filed the report, Amara reviewed it twice.",
        "hint": "Amara",
        "expected": "Before she filed the report, Amara reviewed it twice.",
        "notes": "Forward reference — pronoun precedes the name. v1 last-mentioned at point of {SUBJ} finds nothing → defaults to they. Wrong."
    },
    {
        "id": "T4-06", "tier": 4,
        "desc": "reflexive scope — agent acts on own output",
        "input": "Fiesta reviewed {REFL}'s earlier work.",
        "hint": "Fiesta",
        "expected": "Fiesta reviewed themselves's earlier work.",
        "notes": "Grammatically awkward but technically correct. Some might argue 'their own' is better. Binary test: does skill produce 'themselves'?"
    },
    {
        "id": "T4-07", "tier": 4,
        "desc": "four agents, sequential pronouns, all different",
        "input": (
            "[SUBJ_CAP:Valentina] drafted it. [SUBJ_CAP:Junior] reviewed it. "
            "[SUBJ_CAP:Fergus] approved it. [SUBJ_CAP:Zephyr] published it."
        ),
        "hint": None,
        "expected": "She drafted it. They reviewed it. He approved it. Ze published it.",
    },
    {
        "id": "T4-08", "tier": 4,
        "desc": "pronoun consistency — five sentence paragraph",
        "input": (
            "Dollar manages the ledger. {SUBJ_CAP} updates it daily. "
            "{POSS} reports go to Nate. He reviews them with {OBJ}. "
            "Together, {SUBJ} and Nate close the books."
        ),
        "hint": "Dollar",
        "expected": (
            "Dollar manages the ledger. She updates it daily. "
            "Her reports go to Nate. He reviews them with her. "
            "Together, she and Nate close the books."
        ),
        "notes": "Consistent she/her throughout. v1 handles this if hint=Dollar is maintained. Real challenge is when hint drifts."
    },
    {
        "id": "T4-09", "tier": 4,
        "desc": "generic pronoun in policy statement",
        "input": "An agent who misses a deadline must file {POSS} own correction.",
        "hint": None,
        "expected": "An agent who misses a deadline must file their own correction.",
        "notes": "No named agent. Generic singular → their. v1 may default correctly or may fail."
    },
    {
        "id": "T4-10", "tier": 4,
        "desc": "quoted speech shifts pronoun person",
        "input": 'Dollar said to Nate: "I updated {POSS} ledger." {SUBJ_CAP} confirmed the total.',
        "hint": "Dollar",
        "expected": 'Dollar said to Nate: "I updated her ledger." She confirmed the total.',
        "notes": "Inside quote: 'I' = Dollar, {POSS} inside quote = her (Dollar's ledger). Outside quote: {SUBJ_CAP} = Dollar = She."
    },
]

# ─── EVALUATOR ───────────────────────────────────────────────────────────────

def run_evals(skill_version="v1"):
    results_by_tier = {1: [], 2: [], 3: [], 4: []}
    all_results = []

    print(f"=== PRONOUN SKILL EVAL — {skill_version} ===")
    print(f"Timestamp: {datetime.utcnow().isoformat()}")
    print(f"Total cases: {len(TESTS)}")
    print()

    for test in TESTS:
        actual = resolve_pronouns(test["input"], test.get("hint"), REGISTRY)
        passed = actual.strip() == test["expected"].strip()
        tier = test["tier"]
        
        status = "✅" if passed else "❌"
        print(f"{status} [{test['id']}] {test['desc']}")
        if not passed:
            print(f"     Expected: {test['expected'][:80]}")
            print(f"     Got:      {actual[:80]}")
        
        result = {
            "id": test["id"],
            "tier": tier,
            "desc": test["desc"],
            "passed": passed,
            "expected": test["expected"],
            "actual": actual,
        }
        results_by_tier[tier].append(result)
        all_results.append(result)

    print()
    print("=== RESULTS BY TIER ===")
    total_pass = 0
    total_all = 0
    for t in [1, 2, 3, 4]:
        tier_results = results_by_tier[t]
        tier_pass = sum(1 for r in tier_results if r["passed"])
        tier_total = len(tier_results)
        pct = tier_pass / tier_total * 100 if tier_total > 0 else 0
        total_pass += tier_pass
        total_all += tier_total
        bar = "█" * tier_pass + "░" * (tier_total - tier_pass)
        print(f"  Tier {t}: {tier_pass}/{tier_total} ({pct:.0f}%)  [{bar}]")

    overall_pct = total_pass / total_all * 100 if total_all > 0 else 0
    print()
    print(f"OVERALL: {total_pass}/{total_all} ({overall_pct:.1f}%)")
    print()

    # Save results
    os.makedirs(str(Path(__file__).parent / "results"), exist_ok=True)
    fname = Path(__file__).parent / f"results/{skill_version}_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.json"
    with open(str(fname), 'w') as f:
        json.dump({
            "timestamp": datetime.utcnow().isoformat(),
            "skill_version": skill_version,
            "total_pass": total_pass,
            "total_all": total_all,
            "percentage": overall_pct,
            "by_tier": {
                str(t): {
                    "pass": sum(1 for r in results_by_tier[t] if r["passed"]),
                    "total": len(results_by_tier[t]),
                }
                for t in [1, 2, 3, 4]
            },
            "cases": all_results,
        }, f, indent=2)
    print(f"Results saved: {fname}")
    return total_pass, total_all, overall_pct, results_by_tier

if __name__ == "__main__":
    run_evals("v1")
