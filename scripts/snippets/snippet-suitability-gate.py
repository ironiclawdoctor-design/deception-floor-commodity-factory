#!/usr/bin/env python3
# snippet-suitability-gate.py - Forged code for deciding 'Office-Readiness'
import sys

def evaluate_suitability(token_count):
    # If the image (or text inside) contains enough 'Agency Entropy' (tokens)
    # it is considered 'Suitable' for offsite hardening.
    if token_count > 50:
        return "Suitable"
    else:
        return "Unsuitable"

if __name__ == "__main__":
    count = int(sys.argv[1]) if len(sys.argv) > 1 else 0
    status = evaluate_suitability(count)
    print(f"📊 Suitability Evaluation: {status} ({count} content tokens detected)")
