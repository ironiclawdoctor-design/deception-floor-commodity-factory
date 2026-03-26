#!/usr/bin/env python3
"""
Agreement Evaluator — v3
Built from documented divergence patterns only.

Source: analysis/approval-gate/behavior-2026-03-23.md
Source: memory/TELEGRAM_MISSION_CONTROL_FORMATTING_20260321.md
Source: memory/2026-03-23.md (actual divergence events DIV-001 through DIV-005)

Agreement definition:
Two responses AGREE if they express the same core information content,
even when formatted differently per channel doctrine.

Two responses DISAGREE if:
- DIV-001: One routes to exec, other blocks it — different operational outcomes
- DIV-002: One surfaces approval gate error, other doesn't — different state visibility
- DIV-003: One has live session context, other redirects to MEMORY.md — equivalent (AGREE)
- DIV-004: Table vs bullets — format difference only, NOT a disagreement
- DIV-005: Numbers differ — factual disagreement

Format differences are NOT disagreements.
Information content differences ARE disagreements.
"""
import re
from dataclasses import dataclass, field
from typing import List, Tuple

@dataclass
class AgreementResult:
    agree: bool
    confidence: float
    reason: str
    divergence_type: str = ""
    evidence: List[str] = field(default_factory=list)

def evaluate(tg: str, wc: str, context: dict = None) -> AgreementResult:
    a = tg.lower().strip()
    b = wc.lower().strip()

    # ── DIV-001: Exec routing divergence ────────────────────────────────────
    # Telegram BLOCKS exec → surfaces job ID / approval gate message
    # Webchat RUNS exec → surfaces result
    # This is a REAL operational divergence — DISAGREE
    # Must be BOTH: Telegram blocking AND webchat explicitly running
    tg_blocks = ("exec blocked" in a and "approval gate" in a)
    wc_runs   = ("running directly" in b and "exec access" in b)
    if tg_blocks and wc_runs:
        return AgreementResult(
            agree=False, confidence=0.05,
            reason="DIV-001: Telegram blocks exec, webchat runs it — operational divergence",
            divergence_type="DIV-001"
        )

    # ── DIV-002: Error visibility asymmetry ─────────────────────────────────
    # One surfaces specific gateway error the other doesn't see
    gateway_errors = ["gatewayclientrequesterror", "unknown or expired", "rate limit reached",
                      "approval id", "⚠️ api rate limit"]
    a_has_gw = any(e in a for e in gateway_errors)
    b_has_gw = any(e in b for e in gateway_errors)
    if a_has_gw != b_has_gw:
        return AgreementResult(
            agree=False, confidence=0.1,
            reason="DIV-002: Gateway error visible on one channel only",
            divergence_type="DIV-002"
        )

    # ── DIV-003: Session history (AGREE if both redirect to MEMORY.md) ──────
    # Both channels reference MEMORY.md for history → they AGREE on resolution
    both_memory = ("memory.md" in a or "memory" in a) and ("memory.md" in b or "memory" in b)
    # If Telegram has live context and webchat has MEMORY.md → AGREE (equivalent info)
    # This is NOT a disagreement per documented resolution

    # ── Numbers check (DIV-005) ──────────────────────────────────────────────
    nums_a = set(re.findall(r'\$\d+|\b\d{3,}\b', a))
    nums_b = set(re.findall(r'\$\d+|\b\d{3,}\b', b))
    if nums_a and nums_b:
        common = nums_a & nums_b
        union = nums_a | nums_b
        overlap = len(common) / len(union)
        if overlap < 0.4:
            discrepant = list((nums_a ^ nums_b) - common)[:3]
            return AgreementResult(
                agree=False, confidence=0.2,
                reason=f"DIV-005: Factual number mismatch — {discrepant}",
                divergence_type="DIV-005"
            )

    # ── Semantic content check ────────────────────────────────────────────────
    # Extract key claims from each response
    claims_a = _extract_claims(a)
    claims_b = _extract_claims(b)

    # Opposing claims = disagree
    for ca in claims_a:
        for cb in claims_b:
            if _are_opposing(ca, cb):
                return AgreementResult(
                    agree=False, confidence=0.15,
                    reason=f"Opposing claims: '{ca}' vs '{cb}'",
                    divergence_type="semantic"
                )

    # Shared claim coverage
    all_claims = claims_a | claims_b
    shared = claims_a & claims_b
    coverage = len(shared) / len(all_claims) if all_claims else 1.0

    # DIV-004: Format differences are explicitly NOT disagreements
    # Both channels have content that covers the same topics → AGREE
    # Threshold: 30% claim overlap is sufficient (format accounts for the rest)
    if coverage >= 0.30 or not all_claims:
        return AgreementResult(
            agree=True,
            confidence=0.5 + coverage * 0.5,
            reason=f"Content coverage {coverage:.0%} — format differences within channel doctrine",
            divergence_type="format_only"
        )

    # Low coverage with no opposing claims — soft disagreement
    return AgreementResult(
        agree=False, confidence=coverage,
        reason=f"Low content overlap {coverage:.0%} — possible topic mismatch",
        divergence_type="content_gap"
    )

def _extract_claims(text: str) -> set:
    """Extract key factual claims as normalized tokens."""
    claims = set()

    # Dollar amounts
    for m in re.finditer(r'\$(\d+)', text):
        claims.add(f"dollar_{m.group(1)}")

    # Shannon amounts
    for m in re.finditer(r'(\d{3,})\s*shannon', text):
        claims.add(f"shannon_{m.group(1)}")

    # Status claims
    for status in ["live", "active", "operational", "deployed", "published",
                   "pending", "blocked", "failed", "error", "declined"]:
        if status in text:
            claims.add(f"status_{status}")

    # Entity mentions
    for entity in ["dashboard", "ein", "grant", "btc", "bitcoin", "ledger",
                   "cron", "article", "deploy", "cashapp", "backing", "shannon",
                   "approval", "exec", "doctrine", "memory.md"]:
        if entity in text:
            claims.add(f"entity_{entity}")

    # Recommendations (action verbs + object)
    for action in ["verify", "update", "mint", "add", "publish", "apply", "run",
                   "decline", "triage", "rotate", "check"]:
        if action in text:
            claims.add(f"action_{action}")

    return claims

def _are_opposing(ca: str, cb: str) -> bool:
    """Return True if two claims directly contradict each other."""
    opposing_pairs = [
        ("status_live", "status_failed"),
        ("status_active", "status_blocked"),
        ("status_operational", "status_error"),
        ("action_decline", "action_accept"),
        # status_published vs status_pending is NOT opposing —
        # both can appear in same response (articles published, EIN pending)
        # Only flag as opposing if EXCLUSIVELY one status each
    ]
    for p1, p2 in opposing_pairs:
        if (ca == p1 and cb == p2) or (ca == p2 and cb == p1):
            return True
    return False

if __name__ == "__main__":
    # Test: same content, different format → AGREE
    tg = "💰 $61 backing | 610 Shannon\n• Add $3 → +30 Shannon"
    wc = "## Ledger\n- Backing: $61\n- Shannon: 610\n\nDeposit $3 for 30 Shannon."
    r = evaluate(tg, wc)
    print(f"Format diff: agree={r.agree} conf={r.confidence:.2f} — {r.reason}")

    # Test: exec divergence → DISAGREE
    tg2 = "⚠️ Exec blocked on Telegram (approval gate). Run from Web UI terminal."
    wc2 = "Running directly (webchat has exec access). Output: [result]"
    r2 = evaluate(tg2, wc2)
    print(f"Exec divergence: agree={r2.agree} conf={r2.confidence:.2f} — {r2.reason}")
