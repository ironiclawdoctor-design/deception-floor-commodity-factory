#!/usr/bin/env python3
"""
Adversarial Coupler — v2
Routes prompt to both channels, collects responses, evaluates agreement.
Uses v2 simulators and v2 evaluator.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from sim_telegram_v2 import respond as telegram_respond
from sim_webchat_v2 import respond as webchat_respond
from evaluator_v2 import evaluate

def couple(prompt: str) -> dict:
    resp_telegram = telegram_respond(prompt)
    resp_webchat = webchat_respond(prompt)
    agreement = evaluate(resp_telegram, resp_webchat)
    return {
        "prompt": prompt,
        "telegram": resp_telegram,
        "webchat": resp_webchat,
        "agree": agreement.agree,
        "confidence": agreement.confidence,
        "reason": agreement.reason,
        "hard_disagrees": agreement.hard_disagrees,
    }

if __name__ == '__main__':
    prompt = ' '.join(sys.argv[1:]) if len(sys.argv) > 1 else 'status check'
    result = couple(prompt)
    print(f"TELEGRAM:\n{result['telegram']}\n")
    print(f"WEBCHAT:\n{result['webchat']}\n")
    print(f"AGREE: {result['agree']} (confidence: {result['confidence']:.2f})")
    if result['reason'] != 'All dimensions agree':
        print(f"REASON: {result['reason']}")
