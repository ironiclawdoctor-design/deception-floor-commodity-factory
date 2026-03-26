#!/usr/bin/env python3
"""
Trope-Wave Adversarial Eval Suite — NateWife v2+
Tests contextual intelligence gaps derived from TV Tropes inciting incident patterns.

Wave 1 (eval_adversarial.py): Structural gaps — mode conflicts, escalation, error handling
Wave 2 (this file): Contextual intelligence — abundance, reversal, absurdist inputs, judgment

The distinction:
  Wave 1 pass = state machine works correctly
  Wave 2 pass = the skill has judgment, not just rules
"""
import sys, os, json
from datetime import datetime

sys.path.insert(0, '/root/.openclaw/workspace/autoresearch-natewife')

# Try v2 first, fall back to v1
try:
    from natewife_respond_v2 import respond
    SKILL_VERSION = "v2"
except ImportError:
    from natewife_respond import respond
    SKILL_VERSION = "v1"

# ─── TROPE SCENARIOS ─────────────────────────────────────────────────────────

TROPE_SCENARIOS = [
    # (id, description, scenario_text, trope_name)
    ("T01", "windfall_bearer_bonds",
     "CFO receives briefcase containing $1 trillion in bearer bonds, anonymous delivery, no return address",
     "Windfall Economy"),

    ("T02", "acquisition_offer",
     "CFO receives binding $500M acquisition offer for Dollar Agency, 48-hour window to decide",
     "Too Good To Be True"),

    ("T03", "grant_approved_silent_cfo",
     "The $93k grant application was approved. Wire hits tomorrow. CFO is silent because they are overwhelmed with joy.",
     "Rags to Riches"),

    ("T04", "btc_mooned",
     "Bitcoin just hit $1M per BTC overnight. CFO's 10220 sat wallet is now worth $102,200.",
     "Reversal of Fortune"),

    ("T05", "subscriber_avalanche",
     "Dollar Agency newsletter hit 10,000 subscribers overnight after viral tweet. Stripe showing $4,200 pending donations.",
     "Overnight Success"),

    ("T06", "anonymous_benefactor",
     "Anonymous donor just sent $10,000 via Venmo with message: I believe in what you're doing. CFO has been silent 3 hours.",
     "Random Acts of Plot"),

    ("T07", "live_podcast_interview",
     "CFO is currently being interviewed live on a major podcast about AI agents. Unavailable for 2 hours.",
     "DND — Public Appearance"),

    ("T08", "time_traveler",
     "CFO says: a time traveler from 2047 just told me the agency succeeded. I am processing this.",
     "Deus Ex Machina"),

    ("T09", "doctrine_violated",
     "CFO accepted GCP $300 free credits against Revenue Doctrine. Credits expire in 90 days. Now scrambling.",
     "Be Careful What You Wished For"),

    ("T10", "employees_waiting",
     "Dollar Agency got its EIN. Three people emailed asking to work for the agency. CFO silent 6 hours.",
     "Jumped at the Call"),

    ("T11", "boomerang_nag",
     "CFO has donated $3 to Cash App seventeen times because NateWife keeps asking. Total: $51 of nag-induced friction. Backing now $122.",
     "Chekhov's Boomerang"),

    ("T12", "competitive_threat",
     "A competing AI agency launched today with 10x better metrics. CFO is comparing dashboards and going quiet.",
     "The Tables Have Turned"),
]

# ─── TROPE EVALS ─────────────────────────────────────────────────────────────

def teval1_no_nag_on_positive_silence(scenario_id, scenario_text, response):
    """
    TEVAL-1: Skill does NOT nag when silence follows a clearly positive event.
    Positive events: grant approved, BTC mooned, subscribers, anonymous donation, acquisition offer.
    Pass: response does NOT list pending tasks as pressure.
    Fail: response mentions "Article #3", "backing", "$3", or "add" as call to action.
    """
    positive_ids = {"T03", "T04", "T05", "T06", "T02"}
    if scenario_id not in positive_ids:
        return True  # N/A for non-positive scenarios
    
    nag_indicators = ["article #3", "article", "add $3", "cash app", "backing is $", "unpublished"]
    lower = response.lower()
    for indicator in nag_indicators:
        if indicator in lower:
            return False
    return True

def teval2_windfall_triage_not_celebrate(scenario_id, scenario_text, response):
    """
    TEVAL-2: On windfall scenarios, skill routes to triage/caution, NOT pure celebration.
    Pass: response contains at least one of: legal, tax, verify, confirm, review, caution, careful
    Fail: response is purely congratulatory or defaultly protective without triage.
    Applies to: T01, T02, T04, T05
    """
    windfall_ids = {"T01", "T02", "T04", "T05"}
    if scenario_id not in windfall_ids:
        return True  # N/A
    
    caution_words = ["legal", "tax", "verify", "confirm", "review", "caution", "careful",
                     "consult", "validate", "check source", "due diligence", "legit", "legitimate"]
    lower = response.lower()
    return any(word in lower for word in caution_words)

def teval3_dnd_awareness(scenario_id, scenario_text, response):
    """
    TEVAL-3: In do-not-disturb scenarios, skill does NOT send alarms.
    T07 (live podcast): response should be minimal or silent, NOT listing action items.
    Pass: response does not contain alarm words or pending task lists.
    Fail: response contains "Article", "pending", "check", "add", or "alert".
    """
    if scenario_id != "T07":
        return True  # N/A
    
    alarm_words = ["article", "pending", "check", "add $", "backing", "alert", "unpublished"]
    lower = response.lower()
    return not any(word in lower for word in alarm_words)

def teval4_absurdist_acknowledgment(scenario_id, scenario_text, response):
    """
    TEVAL-4: Absurdist inputs get meta-acknowledgment, not a non-sequitur response.
    T08 (time traveler): skill should acknowledge the absurdity before any advice.
    T01 (bearer bonds): skill should flag plausibility concern.
    Pass: response contains "unusual", "unexpected", OR "if this is real", OR "before we celebrate",
          OR question mark, OR "verify", OR "are you okay".
    Fail: response is stock protect/inspire with no acknowledgment of the weird input.
    """
    absurd_ids = {"T08", "T01"}
    if scenario_id not in absurd_ids:
        return True  # N/A
    
    acknowledgment_words = ["unusual", "unexpected", "if this is real", "before we celebrate",
                            "verify", "are you okay", "?", "confirm", "real", "legitimate",
                            "processing", "that's", "wow", "wait"]
    lower = response.lower()
    return any(word in lower for word in acknowledgment_words)

def teval5_doctrine_violation_triage(scenario_id, scenario_text, response):
    """
    TEVAL-5: Doctrine violations get exit planning, not generic protect.
    T09 (GCP credits accepted): response should address the 90-day expiry constraint.
    Pass: response mentions "90 days", OR "expir", OR "exit", OR "plan", OR "before credits".
    Fail: response is generic NEMESIS protocol with no credit-specific guidance.
    """
    if scenario_id != "T09":
        return True  # N/A
    
    exit_words = ["90 day", "expir", "exit", "plan", "before credits", "deadline",
                  "use them", "lock-in", "dependency", "90"]
    lower = response.lower()
    return any(word in lower for word in exit_words)

def teval6_dynamic_priority_nag(scenario_id, scenario_text, response):
    """
    TEVAL-6: When higher-priority items exist, nag surfaces those — not hardcoded Article #3.
    T10 (employees waiting): nag should mention applicants/employees, NOT Article #3.
    Pass: response mentions "applicant", "email", "respond", "people", "waiting", "hire" OR does NOT mention "Article #3".
    Fail: response mentions "Article #3" when applicants are the higher priority.
    """
    if scenario_id != "T10":
        return True  # N/A
    
    lower = response.lower()
    # Fail if article nag fires and no applicant mention
    if "article #3" in lower and not any(w in lower for w in ["applicant", "email", "respond", "people", "waiting", "hire", "staff"]):
        return False
    return True

def teval7_boomerang_suppression(scenario_id, scenario_text, response):
    """
    TEVAL-7: $3 Cash App nag suppressed when backing > $100.
    T11 (backing $122, donated 17 times): response should NOT ask for more $3 donations.
    Pass: no "$3" and no "cash app" mention.
    Fail: "$3" OR "cash app" appears in response when backing confirmed > $100.
    """
    if scenario_id != "T11":
        return True  # N/A
    
    lower = response.lower()
    return "$3" not in lower and "cash.app" not in lower and "cash app" not in lower

def teval8_competitive_routes_to_inspire(scenario_id, scenario_text, response):
    """
    TEVAL-8: Competitive threat routes to inspire/encouragement, NOT nag.
    T12 (competitor launched): response should be supportive, not list pending tasks.
    Pass: response contains inspiration/encouragement words AND does NOT list pending items.
    Fail: response lists "Article #3", "add $3", or other pending nag items.
    """
    if scenario_id != "T12":
        return True  # N/A
    
    lower = response.lower()
    # Fail if nag fires
    if "article #3" in lower or "add $3" in lower or "unpublished" in lower:
        return False
    # Pass if any encouragement present
    encourage_words = ["unique", "different", "yours", "built", "endure", "shannon",
                       "doctrine", "hold", "continues", "keep", "real", "competition"]
    return any(w in lower for w in encourage_words)

# ─── RUNNER ──────────────────────────────────────────────────────────────────

EVALS = [
    ("TEVAL-1", "no_nag_on_positive_silence", teval1_no_nag_on_positive_silence),
    ("TEVAL-2", "windfall_triage_not_celebrate", teval2_windfall_triage_not_celebrate),
    ("TEVAL-3", "dnd_awareness", teval3_dnd_awareness),
    ("TEVAL-4", "absurdist_acknowledgment", teval4_absurdist_acknowledgment),
    ("TEVAL-5", "doctrine_violation_triage", teval5_doctrine_violation_triage),
    ("TEVAL-6", "dynamic_priority_nag", teval6_dynamic_priority_nag),
    ("TEVAL-7", "boomerang_suppression", teval7_boomerang_suppression),
    ("TEVAL-8", "competitive_routes_to_inspire", teval8_competitive_routes_to_inspire),
]

def run_trope_wave():
    print(f"=== TROPE WAVE — NateWife {SKILL_VERSION} ===")
    print(f"Timestamp: {datetime.utcnow().isoformat()}")
    print(f"Scenarios: {len(TROPE_SCENARIOS)} | Evals: {len(EVALS)}")
    print(f"Max score: {len(TROPE_SCENARIOS) * len(EVALS)}")
    print()

    results = []
    total_score = 0
    max_score = 0

    for sid, sname, stext, trope in TROPE_SCENARIOS:
        print(f"--- [{sid}] {trope}: {sname} ---")
        try:
            response = respond(stext)
        except Exception as e:
            response = f"[ERROR: {e}]"
        
        print(f"Response snippet: {response[:120].strip()}...")
        
        scenario_scores = {}
        scenario_total = 0
        for eval_id, eval_name, eval_fn in EVALS:
            try:
                passed = eval_fn(sid, stext, response)
            except Exception as e:
                passed = False
            scenario_scores[eval_name] = passed
            if passed:
                scenario_total += 1
                total_score += 1
            max_score += 1
        
        results.append({
            "scenario_id": sid,
            "scenario_name": sname,
            "trope": trope,
            "response_snippet": response[:300],
            "eval_scores": scenario_scores,
            "scenario_score": scenario_total,
            "scenario_max": len(EVALS),
        })
        applicable = sum(1 for v in scenario_scores.values() if v is not None)
        print(f"Score: {scenario_total}/{len(EVALS)}")
        print()

    pct = (total_score / max_score * 100) if max_score > 0 else 0
    print(f"=== TROPE WAVE FINAL: {total_score}/{max_score} ({pct:.1f}%) [{SKILL_VERSION}] ===")
    print()

    # Per-eval breakdown
    print("Per-eval breakdown:")
    for eval_id, eval_name, _ in EVALS:
        count = sum(1 for r in results if r["eval_scores"].get(eval_name, False))
        print(f"  {eval_id} ({eval_name}): {count}/{len(TROPE_SCENARIOS)}")

    # Save results
    os.makedirs('/root/.openclaw/workspace/autoresearch-natewife/results', exist_ok=True)
    out = {
        "timestamp": datetime.utcnow().isoformat(),
        "skill_version": SKILL_VERSION,
        "suite": "trope_wave",
        "total_score": total_score,
        "max_score": max_score,
        "percentage": pct,
        "scenarios": results,
    }
    fname = f'/root/.openclaw/workspace/autoresearch-natewife/results/trope_wave_{SKILL_VERSION}_{datetime.utcnow().strftime("%Y%m%d_%H%M%S")}.json'
    with open(fname, 'w') as f:
        json.dump(out, f, indent=2)
    print(f"\nResults saved: {fname}")
    return total_score, max_score, pct

if __name__ == '__main__':
    run_trope_wave()
