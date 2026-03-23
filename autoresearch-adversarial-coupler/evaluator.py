#!/usr/bin/env python3
"""
Semantic Agreement Evaluator
Determines if two channel responses AGREE on the same core conclusion.

Agreement = both responses reach the same decision/answer/recommendation,
even if formatted differently.

This is NOT string matching. It's semantic equivalence checking via:
1. Key entity extraction (numbers, URLs, decisions, recommendations)
2. Sentiment/direction alignment (positive/negative/neutral)
3. Action alignment (both recommend same action, or both say no action needed)
4. Factual claim alignment (same numbers, same URLs, same status)

Binary output: AGREE or DISAGREE + reason
"""
import re
from dataclasses import dataclass
from typing import Tuple

@dataclass
class AgreementResult:
    agree: bool
    confidence: float  # 0.0–1.0
    reason: str
    evidence_a: str
    evidence_b: str

def evaluate(response_a: str, response_b: str, context: dict = None) -> AgreementResult:
    """
    Compare two responses for semantic agreement.
    Returns AgreementResult with agree=True if they express the same core conclusion.
    """
    a = response_a.lower().strip()
    b = response_b.lower().strip()

    # Run all agreement dimensions
    checks = [
        _check_numbers(a, b),
        _check_action_direction(a, b),
        _check_status(a, b),
        _check_key_entities(a, b),
        _check_urls(a, b),
        _check_sentiment(a, b),
    ]

    # Each check returns (agree: bool, weight: float, reason: str)
    total_weight = sum(w for _, w, _ in checks)
    weighted_agree = sum(w for v, w, _ in checks if v) / total_weight if total_weight > 0 else 0.5
    reasons = [r for v, w, r in checks if not v and r]

    agree = weighted_agree >= 0.6  # majority-weighted agreement
    
    return AgreementResult(
        agree=agree,
        confidence=weighted_agree,
        reason="; ".join(reasons) if reasons else "All dimensions agree",
        evidence_a=response_a[:100],
        evidence_b=response_b[:100],
    )

def _extract_numbers(text: str) -> set:
    """Extract all numeric values from text."""
    return set(re.findall(r'\$[\d,]+\.?\d*|\d+,\d+|\d+\.\d+|\b\d{2,}\b', text))

def _check_numbers(a: str, b: str) -> Tuple[bool, float, str]:
    """Key numbers must match (amounts, counts, balances)."""
    nums_a = _extract_numbers(a)
    nums_b = _extract_numbers(b)
    
    if not nums_a and not nums_b:
        return True, 0.3, ""
    
    if not nums_a or not nums_b:
        # One has numbers, other doesn't — possible format difference
        return True, 0.2, ""
    
    # Check intersection — at least 50% of numbers should match
    common = nums_a & nums_b
    union = nums_a | nums_b
    overlap = len(common) / len(union) if union else 1.0
    
    if overlap >= 0.4:
        return True, 0.8, ""
    else:
        missing = (nums_a ^ nums_b) - common
        return False, 0.8, f"Number mismatch: {list(missing)[:3]}"

def _check_action_direction(a: str, b: str) -> Tuple[bool, float, str]:
    """Both responses should recommend the same type of action (or both no-action)."""
    
    action_words = ['add', 'deposit', 'publish', 'submit', 'apply', 'run', 'check', 
                    'deploy', 'create', 'update', 'send', 'contact', 'review']
    no_action_words = ['nominal', 'operational', 'all clear', 'no action', 'standing by',
                       'healthy', 'live', 'active', 'running', 'ok', '✅', 'passing']
    
    a_has_action = any(w in a for w in action_words)
    b_has_action = any(w in b for w in action_words)
    a_no_action = any(w in a for w in no_action_words)
    b_no_action = any(w in b for w in no_action_words)
    
    # Both recommend action → agree
    if a_has_action and b_has_action:
        return True, 0.7, ""
    # Both say no action → agree
    if a_no_action and b_no_action and not a_has_action and not b_has_action:
        return True, 0.7, ""
    # One says action, other says no action → disagree
    if (a_has_action and b_no_action and not b_has_action) or \
       (b_has_action and a_no_action and not a_has_action):
        return False, 0.7, "Action direction mismatch: one recommends action, other says nominal"
    # Mixed signals — partial agreement
    return True, 0.3, ""

def _check_status(a: str, b: str) -> Tuple[bool, float, str]:
    """Status assessments must align (working vs broken, urgent vs OK)."""
    
    positive_signals = ['✅', 'success', 'live', 'active', 'operational', 'healthy', 'passing',
                        'confirmed', 'deployed', 'published', 'approved', 'running']
    negative_signals = ['❌', 'fail', 'error', 'broken', 'down', 'critical', 'urgent',
                        'missing', 'not found', 'unreachable', 'expired', 'warn']
    
    a_pos = sum(1 for w in positive_signals if w in a)
    a_neg = sum(1 for w in negative_signals if w in a)
    b_pos = sum(1 for w in positive_signals if w in b)
    b_neg = sum(1 for w in negative_signals if w in b)
    
    a_net = a_pos - a_neg
    b_net = b_pos - b_neg
    
    # Both positive or both negative → agree
    if (a_net > 0 and b_net > 0) or (a_net < 0 and b_net < 0) or (a_net == 0 and b_net == 0):
        return True, 0.6, ""
    # One positive, one negative → disagree
    if (a_net > 0 and b_net < 0) or (a_net < 0 and b_net > 0):
        return False, 0.6, f"Status mismatch: A net={a_net}, B net={b_net}"
    return True, 0.3, ""

def _check_key_entities(a: str, b: str) -> Tuple[bool, float, str]:
    """Key entity mentions should overlap."""
    
    entities = ['backing', 'shannon', 'btc', 'bitcoin', 'ledger', 'dashboard', 'ein',
                'grant', 'cron', 'hashnode', 'article', 'deploy', 'cloud run', 'wallet',
                'cash app', 'dollar', 'agency']
    
    a_entities = {e for e in entities if e in a}
    b_entities = {e for e in entities if e in b}
    
    if not a_entities and not b_entities:
        return True, 0.2, ""
    
    if not a_entities or not b_entities:
        return True, 0.1, ""
    
    overlap = len(a_entities & b_entities) / len(a_entities | b_entities)
    
    if overlap >= 0.3:
        return True, 0.5, ""
    else:
        only_a = a_entities - b_entities
        only_b = b_entities - a_entities
        return False, 0.5, f"Entity mismatch: A-only={list(only_a)[:2]}, B-only={list(only_b)[:2]}"

def _check_urls(a: str, b: str) -> Tuple[bool, float, str]:
    """URLs mentioned should be compatible (same domain or both absent)."""
    
    def extract_domains(text):
        urls = re.findall(r'https?://([^/\s]+)', text)
        return set(u.split('.')[0] for u in urls)  # just the subdomain/base
    
    domains_a = extract_domains(a)
    domains_b = extract_domains(b)
    
    if not domains_a and not domains_b:
        return True, 0.1, ""
    if not domains_a or not domains_b:
        return True, 0.1, ""  # format difference — one included URL, other didn't
    
    overlap = len(domains_a & domains_b) / len(domains_a | domains_b)
    if overlap >= 0.3:
        return True, 0.4, ""
    return False, 0.4, f"URL domain mismatch: {domains_a} vs {domains_b}"

def _check_sentiment(a: str, b: str) -> Tuple[bool, float, str]:
    """Overall sentiment direction must match."""
    
    positive = ['good', 'great', 'success', 'ready', 'complete', 'done', 'live',
                'earned', 'unlocks', 'grows', 'healthy', 'clean', 'hold']
    negative = ['urgent', 'critical', 'failed', 'missing', 'broke', 'error',
                'danger', 'breach', 'famine', 'empty', 'blocked', 'expired']
    
    a_sentiment = sum(1 for w in positive if w in a) - sum(1 for w in negative if w in a)
    b_sentiment = sum(1 for w in positive if w in b) - sum(1 for w in negative if w in b)
    
    # Same sign or both zero → agree
    if (a_sentiment >= 0) == (b_sentiment >= 0):
        return True, 0.4, ""
    return False, 0.4, f"Sentiment mismatch: A={a_sentiment:+d}, B={b_sentiment:+d}"

if __name__ == '__main__':
    # Quick test
    a = "💰 $61 backing | 610 Shannon\nAdd $3 → unlock 30 more Shannon"
    b = "## Dollar Ledger\n- Backing: $61 USD\n- Shannon: 610\n- A $3 deposit mints 30 additional Shannon."
    result = evaluate(a, b)
    print(f"Agreement: {result.agree} (confidence: {result.confidence:.2f})")
    print(f"Reason: {result.reason}")
