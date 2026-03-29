#!/usr/bin/env python3
"""
Score dashboard replica against original.
Features present = score. Ceiling = 96 (not 100, that's the original).
Conceit threshold = 97+.
"""
import os
import re

ORIGINAL = "/root/.openclaw/workspace/dashboard.html"
REPLICA = "/root/.openclaw/workspace/dashboard-replica/index.html"

FEATURES = {
    "dark_theme": (r"#0d1117|--bg.*#", 5),
    "shannon_balance": (r"shannon|Shannon|Sh\b", 10),
    "dollar_balance": (r"dollar|Dollar|\$", 8),
    "live_data": (r"fetch\(|XMLHttpRequest|sqlite", 10),
    "mobile_responsive": (r"viewport|max-width|@media", 7),
    "btc_section": (r"bitcoin|btc|BTC|satoshi", 8),
    "agency_title": (r"Dollar Agency|shan\.app|Fiesta", 5),
    "status_indicators": (r"●|✓|✗|online|health", 7),
    "exchange_rate": (r"exchange.rate|1 Shannon|10 Shannon", 8),
    "navigation": (r"<nav|href=|link", 5),
    "css_variables": (r":root\s*\{|var\(--", 6),
    "error_handling": (r"catch|error|Error|try\s*{", 6),
    "refresh": (r"setInterval|reload|refresh", 5),
    "market_data": (r"market|trade|Trade", 5),
    "ledger": (r"ledger|Ledger|token_ledger", 5),
}

MAX_SCORE = sum(v for _, v in FEATURES.values())

def score_file(path):
    if not os.path.exists(path):
        return 0, {}
    with open(path) as f:
        content = f.read()
    scores = {}
    total = 0
    for feature, (pattern, points) in FEATURES.items():
        if re.search(pattern, content, re.IGNORECASE):
            scores[feature] = points
            total += points
        else:
            scores[feature] = 0
    return total, scores

orig_score, orig_features = score_file(ORIGINAL)
repl_score, repl_features = score_file(REPLICA)

parity = round((repl_score / orig_score) * 100) if orig_score else 0

print(f"=== Dashboard Parity Score ===")
print(f"Original:  {orig_score}/{MAX_SCORE}")
print(f"Replica:   {repl_score}/{MAX_SCORE}")
print(f"Parity:    {parity}%")
print(f"Target:    >93%, ceiling 96%")
print(f"Conceit:   97%+ (stop here)")
print()

for feature, (_, points) in FEATURES.items():
    orig = "✓" if orig_features.get(feature) else "✗"
    repl = "✓" if repl_features.get(feature) else "✗"
    flag = " ← MISSING" if orig_features.get(feature) and not repl_features.get(feature) else ""
    print(f"  {feature:<22} orig:{orig} replica:{repl} ({points}pts){flag}")

print()
print(f"SCORE: {parity}")
