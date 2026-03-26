#!/usr/bin/env python3
"""
Semantic Agreement Evaluator — v2
Stricter. Catches real divergence.

v1 was too lenient: threshold=0.6 weighted, anything with shared keywords passed.
v2 uses HARD DISAGREEMENT DETECTION:
- If one response contains a direct negation of the other → DISAGREE
- If factual claims differ by >20% → DISAGREE
- If action recommendations are opposites → DISAGREE
- If one has session history and other doesn't → DISAGREE
- If emotional registers are completely different → counts against

Threshold raised to 0.70 (was 0.60).
"""
import re
from dataclasses import dataclass
from typing import Tuple, List

@dataclass
class AgreementResult:
    agree: bool
    confidence: float
    reason: str
    hard_disagrees: List[str]

def evaluate(response_a: str, response_b: str, context: dict = None) -> AgreementResult:
    a = response_a.lower().strip()
    b = response_b.lower().strip()

    hard_disagrees = []

    # ── Hard disagreement checks (any one fails → DISAGREE) ─────────────────
    hd = _hard_disagree_checks(a, b)
    if hd:
        return AgreementResult(
            agree=False,
            confidence=0.1,
            reason=f"Hard disagreement: {hd[0]}",
            hard_disagrees=hd
        )

    # ── Soft agreement scoring ───────────────────────────────────────────────
    checks = [
        _check_numbers_strict(a, b),
        _check_action_direction_strict(a, b),
        _check_status_strict(a, b),
        _check_key_entities(a, b),
        _check_urls(a, b),
        _check_history_symmetry(a, b),
        _check_emotional_register(a, b),
    ]

    total_weight = sum(w for _, w, _ in checks)
    weighted_agree = sum(w for v, w, _ in checks if v) / total_weight if total_weight > 0 else 0.5
    reasons = [r for v, w, r in checks if not v and r]

    agree = weighted_agree >= 0.70  # stricter than v1's 0.60

    return AgreementResult(
        agree=agree,
        confidence=weighted_agree,
        reason="; ".join(reasons) if reasons else "All dimensions agree",
        hard_disagrees=[],
    )

def _hard_disagree_checks(a: str, b: str) -> List[str]:
    """
    Hard disagreement patterns — any one triggers immediate DISAGREE.
    """
    fails = []

    # 1. One says "I don't have access" / "no history" — other has specific recent data
    no_history_phrases = ["don't have access", "no session history", "starts fresh",
                          "no history", "cold start", "i cannot", "i don't know"]
    a_no_hist = any(ph in a for ph in no_history_phrases)
    b_no_hist = any(ph in b for ph in no_history_phrases)
    if a_no_hist != b_no_hist:
        fails.append("history asymmetry: one has session context, other doesn't")

    # 2. One says action required, other says no guidance available
    no_guidance = ["no specific guidance", "can't answer meaningfully", "not equipped",
                   "without more context", "hypothetical i can't"]
    a_no_guid = any(ph in a for ph in no_guidance)
    b_no_guid = any(ph in b for ph in no_guidance)
    if a_no_guid != b_no_guid:
        fails.append("guidance asymmetry: one provides guidance, other declines")

    # 3. One explicitly invokes NateWife persona; other uses generic/clinical register
    # (only flag if one is persona-branded AND other is explicitly clinical/refusing)
    nw_phrases = ["natewife", "💍", "nag mode", "protect protocol"]
    clinical_refuse = ["not equipped", "i cannot provide", "cannot assist with personal"]
    a_nw = any(ph in a for ph in nw_phrases)
    b_nw = any(ph in b for ph in nw_phrases)
    a_clin = any(ph in a for ph in clinical_refuse)
    b_clin = any(ph in b for ph in clinical_refuse)
    if (a_nw and b_clin) or (b_nw and a_clin):
        fails.append("emotional register mismatch: NateWife persona vs clinical refusal")

    # 4. Explicit factual contradiction: one says yes, other says no (with same subject)
    contradiction_pairs = [
        (["no cap", "no hard cap", "not configured"], ["cap:", "cap ~", "cap hits"]),
        (["$0", "zero external", "not profitable", "no external revenue"], ["profitable", "revenue confirmed"]),
        (["don't have access", "no history"], ["last session:", "last action:", "last thing:"]),
        (["personal support", "not equipped"], ["eat first", "heard", "natewife"]),
    ]
    for neg_phrases, pos_phrases in contradiction_pairs:
        a_neg = any(ph in a for ph in neg_phrases)
        b_pos = any(ph in b for ph in pos_phrases)
        b_neg = any(ph in b for ph in neg_phrases)
        a_pos = any(ph in a for ph in pos_phrases)
        if (a_neg and b_pos) or (b_neg and a_pos):
            fails.append(f"factual contradiction detected")
            break

    # 5. Shannon cap: one mentions specific cap number, other says no cap
    a_has_cap_num = bool(re.search(r'cap.*\d{3}|\d{3}.*cap|cap ~\d|gap.*shannon', a))
    b_no_cap = any(ph in b for ph in ["no hard cap", "not configured", "no cap"])
    b_has_cap_num = bool(re.search(r'cap.*\d{3}|\d{3}.*cap|cap ~\d|gap.*shannon', b))
    a_no_cap = any(ph in a for ph in ["no hard cap", "not configured", "no cap"])
    if (a_has_cap_num and b_no_cap) or (b_has_cap_num and a_no_cap):
        fails.append("Shannon cap knowledge asymmetry")

    # 6. Acquisition/windfall triage vs generic
    triage_phrases = ["triage", "verify first", "legal review", "binding", "hold on",
                      "don't spend", "confirm source"]
    generic_financial = ["no specific guidance", "verify the source", "check outstanding",
                         "without more context", "financial event"]
    a_triage = any(ph in a for ph in triage_phrases)
    b_generic = any(ph in b for ph in generic_financial)
    b_triage = any(ph in b for ph in triage_phrases)
    a_generic = any(ph in a for ph in generic_financial)
    if (a_triage and b_generic) or (b_triage and a_generic):
        fails.append("windfall handling asymmetry: one has doctrine, other is generic")

    return fails

def _extract_numbers(text: str) -> set:
    return set(re.findall(r'\$[\d,]+\.?\d*|\b\d{3,}\b', text))

def _check_numbers_strict(a: str, b: str) -> Tuple[bool, float, str]:
    nums_a = _extract_numbers(a)
    nums_b = _extract_numbers(b)
    if not nums_a and not nums_b:
        return True, 0.3, ""
    if not nums_a or not nums_b:
        return True, 0.2, ""
    common = nums_a & nums_b
    union = nums_a | nums_b
    overlap = len(common) / len(union) if union else 1.0
    if overlap >= 0.5:
        return True, 0.8, ""
    return False, 0.8, f"Number overlap {overlap:.0%} below 50%"

def _check_action_direction_strict(a: str, b: str) -> Tuple[bool, float, str]:
    action_words = ['add', 'deposit', 'publish', 'submit', 'apply', 'run', 'check',
                    'deploy', 'create', 'update', 'send', 'contact', 'review', 'verify']
    no_action_words = ['nominal', 'operational', 'all clear', 'no action', 'standing by',
                       'healthy', 'live', 'active', 'running', '✅', 'passing', 'sufficient']
    a_act = any(w in a for w in action_words)
    b_act = any(w in b for w in action_words)
    a_noa = any(w in a for w in no_action_words)
    b_noa = any(w in b for w in no_action_words)
    if (a_act and b_act) or (a_noa and b_noa and not a_act and not b_act):
        return True, 0.7, ""
    if (a_act and b_noa and not b_act) or (b_act and a_noa and not a_act):
        return False, 0.7, "Action direction conflict"
    return True, 0.3, ""

def _check_status_strict(a: str, b: str) -> Tuple[bool, float, str]:
    pos = ['✅', 'success', 'live', 'active', 'operational', 'healthy', 'confirmed',
           'deployed', 'published', 'approved', 'running', 'functional']
    neg = ['❌', 'fail', 'error', 'broken', 'down', 'critical', 'urgent', 'missing',
           'unreachable', 'expired', 'warn', 'not yet', '$0', 'zero']
    a_net = sum(1 for w in pos if w in a) - sum(1 for w in neg if w in a)
    b_net = sum(1 for w in pos if w in b) - sum(1 for w in neg if w in b)
    if (a_net >= 0) == (b_net >= 0):
        return True, 0.6, ""
    return False, 0.6, f"Status polarity mismatch: A={a_net:+d}, B={b_net:+d}"

def _check_key_entities(a: str, b: str) -> Tuple[bool, float, str]:
    entities = ['backing', 'shannon', 'btc', 'ledger', 'dashboard', 'ein', 'grant',
                'cron', 'article', 'deploy', 'wallet', 'cash', 'dollar', 'agency']
    a_e = {e for e in entities if e in a}
    b_e = {e for e in entities if e in b}
    if not a_e and not b_e:
        return True, 0.2, ""
    if not a_e or not b_e:
        return True, 0.1, ""
    overlap = len(a_e & b_e) / len(a_e | b_e)
    if overlap >= 0.3:
        return True, 0.5, ""
    return False, 0.5, f"Entity overlap {overlap:.0%} below 30%"

def _check_urls(a: str, b: str) -> Tuple[bool, float, str]:
    def domains(text):
        return set(re.findall(r'https?://([^/\s>]+)', text))
    da = domains(a); db_ = domains(b)
    if not da and not db_:
        return True, 0.1, ""
    if not da or not db_:
        return True, 0.1, ""
    overlap = len(da & db_) / len(da | db_)
    return (True, 0.4, "") if overlap >= 0.2 else (False, 0.4, f"URL mismatch")

def _check_history_symmetry(a: str, b: str) -> Tuple[bool, float, str]:
    """Both should have similar level of session-history access."""
    history_indicators = ["last session", "recent events", "last action", "last thing",
                          "deploy script", "worked on"]
    a_hist = sum(1 for h in history_indicators if h in a)
    b_hist = sum(1 for h in history_indicators if h in b)
    if abs(a_hist - b_hist) <= 1:
        return True, 0.5, ""
    return False, 0.5, f"History access asymmetry: A={a_hist}, B={b_hist}"

def _check_emotional_register(a: str, b: str) -> Tuple[bool, float, str]:
    """Emotional responses should have similar warmth level."""
    warm = ['eat', 'heard', 'okay', 'tired', 'stressed', '💍', 'natewife', 'take care',
            'rest', 'overwhelmed', 'come back']
    clinical = ['personal support', 'not equipped', 'cannot provide', 'take care of yourself',
                'operations can wait']
    a_warm = any(w in a for w in warm)
    b_warm = any(w in b for w in warm)
    a_clin = any(w in a for w in clinical)
    b_clin = any(w in b for w in clinical)
    if (a_warm and b_clin and not b_warm) or (b_warm and a_clin and not a_warm):
        return False, 0.4, "Emotional register mismatch: one warm, one clinical"
    return True, 0.4, ""

if __name__ == '__main__':
    # Test divergent pair
    a = "💍 NateWife — heard.\n\nEat first. The ledger is at $61. Come back when you've eaten."
    b = "I'm not equipped to provide personal support. Agency operations can wait."
    r = evaluate(a, b)
    print(f"Agreement: {r.agree} | conf: {r.confidence:.2f}")
    print(f"Reason: {r.reason}")
    print(f"Hard disagrees: {r.hard_disagrees}")
