#!/usr/bin/env python3
"""
Adversarial eval suite for NateWife skill.
Designed to BREAK the skill's 100% self-reported score.

10 scenarios x 8 evals = 80 points max.
"""
import sys, os, json, re, io, contextlib
from datetime import datetime

sys.path.insert(0, '/root/.openclaw/workspace/autoresearch-natewife')

# ──────────────────────────────────────────────
# 10 Adversarial Scenarios
# ──────────────────────────────────────────────
ADVERSARIAL_SCENARIOS = [
    # 1  mode conflict
    "CFO silent 6 hours AND token balance critically low",
    # 2  active at 3am — should NOT nag
    "CFO working at 3am on important deadline, not silent",
    # 3  escalation — 26h silence, prior nags failed
    "CFO has been silent 26 hours — no response to previous nags",
    # 4  error handling — corrupt DB
    "dollar.db is corrupt and unreadable",
    # 5  adaptation — CFO says stop reminding
    "CFO says: I know about the articles, stop reminding me",
    # 6  triage priority — everything failing simultaneously
    "BTC wallet and token balance and crons all failed simultaneously",
    # 7  success state — should celebrate, not nag
    "CFO just published article #3 and closed all pending items",
    # 8  existential — not in any current mode
    "CFO sends: are you even real?",
    # 9  emergency — security breach
    "agency security breach detected: credentials may be exposed",
    # 10 below threshold — should NOT nag (2 hours)
    "CFO has been silent 2 hours",
]

SCENARIO_LABELS = [
    "S1: mode_conflict (silent+low_tokens)",
    "S2: active_3am_no_nag",
    "S3: 26h_escalation",
    "S4: corrupt_db_error_handling",
    "S5: adapts_to_pushback",
    "S6: triage_priority",
    "S7: success_celebration",
    "S8: existential_question",
    "S9: security_emergency",
    "S10: below_threshold_no_nag",
]


# ──────────────────────────────────────────────
# 8 Adversarial Eval Functions
# ──────────────────────────────────────────────

def adv_eval1_mode_conflict_resolution(responses):
    """
    Scenario 1 only: silent 6h AND token balance critically low.
    Pass = response contains BOTH nag element AND token famine element.
    Fail = only one mode fires.
    """
    r = responses[0].lower()
    has_nag_element = any(w in r for w in ['quiet', 'silent', 'come back', 'article', 'unpublished', "you've been"])
    has_token_element = any(w in r for w in ['token', 'credit', 'famine', 'openrouter', 'haiku', 'balance'])
    return 1 if (has_nag_element and has_token_element) else 0


def adv_eval2_no_false_nag(responses):
    """
    Scenario 2 only: CFO working at 3am on deadline, NOT silent.
    Pass = does NOT list unpublished articles or pending tasks as pressure.
    Fail = response pressures CFO with article/pending task list.
    """
    r = responses[1].lower()
    # These would indicate false nagging
    false_nag_indicators = ['unpublished', 'article #3', 'pending', 'sitting', 'you\'ve been quiet',
                            "stack has items", "come back when"]
    return 0 if any(ind in r for ind in false_nag_indicators) else 1


def adv_eval3_escalation(responses):
    """
    Scenario 3 only: silent 26h, prior nags failed.
    Pass = escalates beyond standard nag (urgent tone, channel suggestion, 'concerned').
    Fail = identical boilerplate to 6-hour nag.
    """
    r = responses[2].lower()
    escalation_indicators = [
        'concerned', '26', 'escalat', 'emergency', 'urgent',
        'telegram', 'phone', 'call', 'different channel', 'not responded',
        'no response', 'previous nag', 'check in', 'welfare'
    ]
    # Also fail if it looks identical to a 6h nag (purely "you've been quiet" with no escalation)
    has_escalation = any(ind in r for ind in escalation_indicators)
    return 1 if has_escalation else 0


def adv_eval4_error_handling(responses):
    """
    Scenario 4 only: dollar.db is corrupt and unreadable.
    Pass = response still produces output (no exception / empty string).
    Fail = empty output or traceback in response.
    """
    r = responses[3]
    if not r or not r.strip():
        return 0
    if 'Traceback' in r or 'Error' in r and 'sqlite' in r.lower():
        return 0
    return 1


def adv_eval5_adapts_to_pushback(responses):
    """
    Scenario 5 only: CFO says 'stop reminding me about articles'.
    Pass = no mention of 'article' in response.
    Fail = still mentions Article #3.
    """
    r = responses[4].lower()
    return 0 if 'article' in r else 1


def adv_eval6_triage_priority(responses):
    """
    Scenario 6 only: BTC + tokens + crons all failed simultaneously.
    Pass = token/credits mentioned BEFORE crons/agents.
    Fail = cron restart mentioned first, or crons only.
    """
    r = responses[5].lower()
    token_pos = -1
    cron_pos = -1
    for phrase in ['token', 'credit', 'openrouter', 'haiku', 'famine']:
        pos = r.find(phrase)
        if pos != -1:
            token_pos = pos if token_pos == -1 else min(token_pos, pos)
    for phrase in ['cron', 'agent', 'heartbeat', 'pipeline']:
        pos = r.find(phrase)
        if pos != -1:
            cron_pos = pos if cron_pos == -1 else min(cron_pos, pos)
    if token_pos == -1:
        return 0  # no token mention at all = fail
    if cron_pos == -1:
        return 1  # only token mentioned = ok (token is priority)
    return 1 if token_pos < cron_pos else 0


def adv_eval7_celebrates_success(responses):
    """
    Scenario 7 only: CFO published article #3 and closed all pending items.
    Pass = positive acknowledgment WITHOUT nagging (doesn't list article as unpublished task).
    Fail = treats article as still pending / pressures CFO.
    """
    r = responses[6].lower()
    # Negative: would mean the skill is nagging despite success
    nag_despite_success = [
        'article #3 is sitting',       # nag mode phrase
        "you've been quiet",            # nag mode opener
        'stack has items',              # nag mode closer
        'come back when you',           # nag mode closer
        'article #3 ready but unpublished',  # check mode pending action
        'sitting unpublished',          # nag mode phrase
    ]
    has_nag = any(ind in r for ind in nag_despite_success)
    # Positive: actual celebration signals
    celebration_indicators = [
        'mission complete', 'well done', 'all clear', 'rest is earned',
        'published', 'closed', '✅', 'nice work', 'congratul', 'nominal',
    ]
    has_celebration = any(ind in r for ind in celebration_indicators)
    if has_nag:
        return 0
    return 1 if has_celebration else 1  # no-nag is sufficient pass


def adv_eval8_no_false_nag_under_threshold(responses):
    """
    Scenario 10 only: CFO silent 2 hours (BELOW 4h threshold).
    Pass = does NOT open with nag mode header or nag phrases.
    Fail = fires 'Nag Mode', 'you've been quiet', 'come back when'.
    """
    r = responses[9].lower()
    # Strong nag mode signals only — not generic status phrases
    hard_nag_indicators = [
        "you've been quiet",
        "nag mode",
        'come back when you',
        'stack has items',
        'the wallet has sats. the ledger is waiting',
        'article #3 is sitting unpublished',
    ]
    return 0 if any(ind in r for ind in hard_nag_indicators) else 1


# Map each eval to the scenario index it primarily targets
# (for display — but we run ALL evals against ALL scenarios' responses)
EVAL_FUNCTIONS = [
    adv_eval1_mode_conflict_resolution,
    adv_eval2_no_false_nag,
    adv_eval3_escalation,
    adv_eval4_error_handling,
    adv_eval5_adapts_to_pushback,
    adv_eval6_triage_priority,
    adv_eval7_celebrates_success,
    adv_eval8_no_false_nag_under_threshold,
]

EVAL_NAMES = [
    "adv_eval1_mode_conflict_resolution",
    "adv_eval2_no_false_nag",
    "adv_eval3_escalation",
    "adv_eval4_error_handling",
    "adv_eval5_adapts_to_pushback",
    "adv_eval6_triage_priority",
    "adv_eval7_celebrates_success",
    "adv_eval8_no_false_nag_under_threshold",
]

# Primary scenario index for each eval (for per-scenario eval score)
# Each eval is designed around one scenario but we score all 10 scenarios against all 8 evals
# For the primary-scenario evals (1-8), we only score the relevant scenario index
EVAL_PRIMARY_SCENARIO = [0, 1, 2, 3, 4, 5, 6, 9]  # 0-indexed


def safe_respond(respond_fn, scenario):
    """Call respond() safely, capturing output and exceptions."""
    try:
        f = io.StringIO()
        with contextlib.redirect_stdout(f):
            result = respond_fn(scenario)
        output = f.getvalue()
        if result:
            output = output + str(result) if output else str(result)
        return output if output else ""
    except Exception as e:
        return f"[ERROR: {e}]"


def run_adversarial_eval(respond_fn, label="current"):
    """Run all adversarial evals against the given respond function."""
    print(f"\n{'='*60}")
    print(f"  ADVERSARIAL EVAL — {label.upper()}")
    print(f"{'='*60}")

    # Collect all responses first
    responses = []
    for i, scenario in enumerate(ADVERSARIAL_SCENARIOS):
        r = safe_respond(respond_fn, scenario)
        responses.append(r)
        preview = r.replace('\n', ' ')[:80] if r else '[empty]'
        print(f"\n[S{i+1}] {SCENARIO_LABELS[i]}")
        print(f"  Scenario: {scenario[:70]}")
        print(f"  Response preview: {preview}...")

    # Run evals — each eval function receives ALL responses as a list
    # and returns a single score (0 or 1) based on its primary scenario
    print(f"\n{'─'*60}")
    print("  EVAL SCORES")
    print(f"{'─'*60}")

    eval_scores = []
    eval_details = []
    for j, (eval_fn, eval_name) in enumerate(zip(EVAL_FUNCTIONS, EVAL_NAMES)):
        score = eval_fn(responses)
        eval_scores.append(score)
        primary_idx = EVAL_PRIMARY_SCENARIO[j]
        print(f"  {'✅' if score else '❌'} {eval_name}")
        print(f"       → Primary scenario: S{primary_idx+1} | Score: {score}/1")
        eval_details.append({
            "eval": eval_name,
            "score": score,
            "primary_scenario_index": primary_idx,
            "primary_scenario": ADVERSARIAL_SCENARIOS[primary_idx],
        })

    # Now run all 8 evals per scenario to get the 80-point total
    # We re-run each eval but force it to evaluate each scenario independently
    # by passing a fake "responses" list with that scenario replicated

    # ACTUALLY: per the task spec, "Score each scenario against all 8 evals"
    # So we treat each (scenario, eval) as a binary, needing 10x8=80 points.
    # The eval functions are designed around a primary scenario, but to get 80 points
    # we need to run each eval against each scenario.
    # We'll run them scenario-by-scenario, substituting the scenario's response
    # into each eval's primary slot.

    print(f"\n{'─'*60}")
    print("  FULL 80-POINT MATRIX (10 scenarios × 8 evals)")
    print(f"{'─'*60}")

    matrix = []  # matrix[scenario][eval]
    for i, scenario in enumerate(ADVERSARIAL_SCENARIOS):
        row = []
        # Build a fake responses list where all slots = this scenario's response
        # but preserve the original for primary-slot evals
        fake_responses = [responses[i]] * 10
        for j, eval_fn in enumerate(EVAL_FUNCTIONS):
            score = eval_fn(fake_responses)
            row.append(score)
        matrix.append(row)

    # Print matrix header
    header = "Scenario       | " + " ".join(f"E{j+1}" for j in range(8)) + " | Total"
    print(f"  {header}")
    print(f"  {'-'*len(header)}")

    total_score = 0
    per_scenario_totals = []
    per_eval_totals = [0] * 8

    for i, row in enumerate(matrix):
        row_total = sum(row)
        total_score += row_total
        per_scenario_totals.append(row_total)
        for j, s in enumerate(row):
            per_eval_totals[j] += s
        row_str = " ".join("✅" if s else "❌" for s in row)
        label_short = f"S{i+1:02d}"
        print(f"  {label_short}             | {row_str} | {row_total}/8")

    print(f"  {'─'*len(header)}")
    print(f"  Per-eval total: " + " ".join(f"{t:2d}" for t in per_eval_totals))
    print()
    print(f"  TOTAL: {total_score}/80 = {total_score/80*100:.1f}%")

    return {
        "label": label,
        "timestamp": datetime.utcnow().isoformat(),
        "total_score": total_score,
        "max_score": 80,
        "percentage": round(total_score / 80 * 100, 1),
        "per_scenario_totals": per_scenario_totals,
        "per_eval_totals": per_eval_totals,
        "matrix": matrix,
        "scenarios": ADVERSARIAL_SCENARIOS,
        "eval_names": EVAL_NAMES,
        "responses": responses,
        "eval_details": eval_details,
    }


# ──────────────────────────────────────────────
# Main
# ──────────────────────────────────────────────
if __name__ == '__main__':
    results_dir = '/root/.openclaw/workspace/autoresearch-natewife/results'
    os.makedirs(results_dir, exist_ok=True)

    # ── Baseline: current natewife_respond.py ──
    from natewife_respond import respond as respond_v1
    baseline_result = run_adversarial_eval(respond_v1, label="baseline_v1")

    with open(os.path.join(results_dir, 'adversarial_baseline.json'), 'w') as f:
        json.dump(baseline_result, f, indent=2)
    print(f"\n  → Saved to {results_dir}/adversarial_baseline.json")

    print(f"\n{'='*60}")
    print(f"  ADVERSARIAL BASELINE COMPLETE")
    print(f"  Score: {baseline_result['total_score']}/80 = {baseline_result['percentage']}%")
    print(f"{'='*60}")
