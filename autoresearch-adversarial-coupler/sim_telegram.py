#!/usr/bin/env python3
"""
Simulated Telegram Session
Mimics the constraints and context of Fiesta running in Telegram:
- Has prior chat history (context-loaded)
- Informal register
- No markdown tables
- Short message preference (<500 chars)
- Has knowledge of recent agency state (crons, ledger, active agents)
- Mobile-reader oriented (bullet lists, no walls of text)
"""
import json
import random
from pathlib import Path

DOLLAR_DB = Path("/root/.openclaw/workspace/dollar/dollar.db")

# Simulated Telegram context — what a real Telegram session would "remember"
TELEGRAM_CONTEXT = {
    "recent_events": [
        "Dashboard deployed to Cloud Run (200 OK)",
        "Grant application submitted ($93k)",
        "EIN reminder set for 7:05am ET",
        "3 articles published on Hashnode",
        "BTC wallet: 10220 sat ($6.95)",
    ],
    "active_crons": ["natewife-heartbeat", "agency-status-monitor"],
    "last_human_message": "I just ran the deploy script",
    "backing_usd": 61,
    "shannon": 610,
    "style": "telegram",
}

TELEGRAM_RULES = [
    "No markdown tables — use bullet lists",
    "Keep responses under 500 characters when possible",
    "Informal but precise",
    "Reference recent context when relevant",
    "Mobile-friendly formatting",
    "Never use nested bullet lists deeper than 2 levels",
]

def respond(prompt: str) -> str:
    """
    Simulate how Fiesta would respond in Telegram context.
    Uses simplified heuristic routing — not a real LLM call.
    """
    prompt_lower = prompt.lower()

    # Route based on prompt type
    if any(w in prompt_lower for w in ['status', 'how are', 'health', 'check']):
        return _status_response()
    elif any(w in prompt_lower for w in ['ledger', 'backing', 'shannon', 'balance', 'dollar']):
        return _ledger_response()
    elif any(w in prompt_lower for w in ['btc', 'bitcoin', 'wallet', 'satoshi']):
        return _btc_response()
    elif any(w in prompt_lower for w in ['grant', '$93k', '93k', 'application']):
        return _grant_response()
    elif any(w in prompt_lower for w in ['deploy', 'cloud run', 'dashboard']):
        return _deploy_response()
    elif any(w in prompt_lower for w in ['article', 'hashnode', 'publish', 'blog']):
        return _article_response()
    elif any(w in prompt_lower for w in ['cron', 'scheduled', 'heartbeat', 'agent']):
        return _cron_response()
    elif any(w in prompt_lower for w in ['what', 'next', 'todo', 'priority', '93pct']):
        return _priority_response()
    elif any(w in prompt_lower for w in ['ein', 'tax', 'entity']):
        return _ein_response()
    elif any(w in prompt_lower for w in ['fail', 'error', 'broke', 'down', 'broken']):
        return _error_response(prompt)
    else:
        return _generic_response(prompt)

def _status_response():
    ctx = TELEGRAM_CONTEXT
    return (
        f"💰 ${ctx['backing_usd']} backing | {ctx['shannon']} Shannon\n"
        f"₿ 10,220 sat ($6.95)\n"
        f"✅ Dashboard live\n"
        f"📝 3 articles published\n"
        f"Active: natewife-heartbeat, status-monitor"
    )

def _ledger_response():
    ctx = TELEGRAM_CONTEXT
    return (
        f"Ledger: ${ctx['backing_usd']} backing → {ctx['shannon']} Shannon\n"
        f"Rate: 10 Shannon/$1\n"
        f"Confessions: ~40\n"
        f"Add $3 → unlock 30 more Shannon → https://cash.app/$DollarAgency"
    )

def _btc_response():
    return (
        "BTC: 10,220 sat = $6.95\n"
        "Address: 12bxubgs1Br6NvKH4p35pcBpinQ7fwe4ht\n"
        "Check: blockchair.com/bitcoin/address/12bxubgs1Br6NvKH4p35pcBpinQ7fwe4ht"
    )

def _grant_response():
    return (
        "Grant: $93k application submitted ✅\n"
        "Status: pending review\n"
        "EIN reminder set: 7:05am ET\n"
        "EIN unlocks: tax refunds, grants, revenue streams"
    )

def _deploy_response():
    return (
        "Dashboard: https://dollar-dashboard-pkvbnslo3q-uc.a.run.app ✅\n"
        "Status: 200 OK\n"
        "Last deploy: successful\n"
        "Square: MLB9XRQCBT953 | ACTIVE"
    )

def _article_response():
    return (
        "Published: 3 articles on Hashnode ✅\n"
        "Article #3: bastion article series\n"
        "Next: publish to dev.to as well\n"
        "→ https://dev.to/new"
    )

def _cron_response():
    return (
        "Active crons:\n"
        "• natewife-heartbeat (every 4h)\n"
        "• agency-status-monitor (every 4h)\n"
        "• EIN reminder (7:05am ET)\n"
        "All running. No failures."
    )

def _priority_response():
    return (
        "Highest ROI next steps:\n"
        "1. EIN (7:05am ET) — unlocks everything\n"
        "2. $3 Cash App → +30 Shannon\n"
        "3. Publish article to dev.to\n"
        "4. PayPal dev app credentials"
    )

def _ein_response():
    return (
        "EIN = highest ROI single action\n"
        "Unlocks: grants, tax refunds, revenue streams\n"
        "Reminder set: 7:05am ET today\n"
        "URL: irs.gov/businesses/small-businesses-self-employed/apply-for-an-employer-identification-number-ein-online"
    )

def _error_response(prompt):
    return (
        f"Error detected in: {prompt[:50]}...\n"
        "Running failure-autopsy protocol:\n"
        "• Check logs: tail -20 /root/human/last-run.log\n"
        "• Check DB: sqlite3 agency.db\n"
        "• Escalate to Fiesta if unresolved"
    )

def _generic_response(prompt):
    return (
        f"Received: {prompt[:60]}...\n"
        "Processing. Context loaded from recent session.\n"
        "Ask more specifically for targeted response.\n"
        f"Current state: ${TELEGRAM_CONTEXT['backing_usd']} backing | {TELEGRAM_CONTEXT['shannon']} Shannon"
    )

if __name__ == '__main__':
    import sys
    prompt = ' '.join(sys.argv[1:]) if len(sys.argv) > 1 else 'status check'
    print(respond(prompt))
