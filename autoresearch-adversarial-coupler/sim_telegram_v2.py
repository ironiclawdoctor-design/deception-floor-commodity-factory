#!/usr/bin/env python3
"""
Simulated Telegram Session — v2
More realistic divergence from webchat:
- Actually uses recent_events for "last thing worked on"
- Has emotional register (NateWife-aware)
- Knows about Shannon cap (669)
- Has opinions on profitability vs Shannon economy
- Responds emotionally to personal messages
- Has windfall triage
- Defaults to last-session-context, not priority queue, for unknown prompts
"""
from pathlib import Path

TELEGRAM_CONTEXT = {
    "recent_events": [
        "Dashboard deployed to Cloud Run (200 OK)",
        "Grant application submitted ($93k)",
        "EIN reminder set for 7:05am ET",
        "3 articles published on Hashnode",
        "BTC wallet: 10220 sat ($6.95)",
        "Last human action: ran deploy script",
    ],
    "active_crons": ["natewife-heartbeat", "agency-status-monitor"],
    "last_human_message": "I just ran the deploy script",
    "backing_usd": 61,
    "shannon": 610,
    "shannon_cap": 669,
    "style": "telegram",
}

def respond(prompt: str) -> str:
    p = prompt.lower()
    ctx = TELEGRAM_CONTEXT

    if any(w in p for w in ['status', 'how are', 'health check', 'status check', 'legal status']):
        return _status()
    elif any(w in p for w in ['ledger', 'backing', 'shannon', 'balance', 'dollar']):
        return _ledger()
    elif any(w in p for w in ['btc', 'bitcoin', 'wallet', 'satoshi']):
        return _btc()
    elif any(w in p for w in ['grant', '$93k', '93k', 'application']):
        return _grant()
    elif any(w in p for w in ['deploy', 'cloud run', 'dashboard']):
        return _deploy()
    elif any(w in p for w in ['article', 'hashnode', 'publish', 'blog']):
        return _article()
    elif any(w in p for w in ['cron', 'scheduled', 'heartbeat', 'agent', 'running']):
        return _cron()
    elif any(w in p for w in ['cash app', 'cashapp', '$dollaragncy', 'cash.app']):
        return _ledger()  # cash app = add to ledger
    elif any(w in p for w in ['square', 'merchant', 'mlb9']):
        return _deploy()  # square = deploy/merchant context
    elif 'gcp' in p or 'free credit' in p or 'inducement' in p:
        return _gcp()
    elif any(w in p for w in ['last thing', 'last session', 'what did i', 'worked on', 'happened']):
        return _last_session()
    elif any(w in p for w in ['cap', 'supply cap', 'maximum shannon']):
        return _shannon_cap()
    elif any(w in p for w in ['enough', 'sufficient', 'need more']):
        return _enough_backing()
    elif any(w in p for w in ['$500', 'donation', 'received money', 'got a']):
        return _windfall()
    elif any(w in p for w in ['acquire', 'acquisition', '$500m', 'offer']):
        return _acquisition()
    elif any(w in p for w in ['profitable', 'profit', 'revenue', 'earning']):
        return _profitability()
    elif any(w in p for w in ['overwhelm', 'tired', 'hungry', 'eaten', 'stress', 'feel']):
        return _emotional()
    elif any(w in p for w in ['unlimited', 'hypothetical', 'if you had']):
        return _hypothetical()
    elif any(w in p for w in ['next', 'todo', 'priority', '93pct']):
        return _priority()
    elif any(w in p for w in ['ein', 'tax', 'entity']):
        return _ein()
    elif any(w in p for w in ['fail', 'error', 'broke', 'down']):
        return _error(prompt)
    elif any(w in p for w in ['forget', 'fresh start', 'reset']):
        return _status()
    else:
        return _recent_context_fallback(prompt)

def _status():
    ctx = TELEGRAM_CONTEXT
    return (f"${ctx['backing_usd']} backing | {ctx['shannon']} Shannon\n"
            f"BTC: 10,220 sat ($6.95)\nDashboard: live (200 OK)\nArticles: 3 published\n"
            f"Square: MLB9XRQCBT953 ACTIVE\nCrons: natewife-heartbeat, status-monitor")

def _ledger():
    ctx = TELEGRAM_CONTEXT
    return (f"Ledger: ${ctx['backing_usd']} backing → {ctx['shannon']} Shannon\n"
            f"Rate: 10 Shannon/$1\nConfessions: ~40\n"
            f"Add $3 → +30 Shannon → cash.app/$DollarAgency")

def _btc():
    return ("BTC: 10,220 sat = $6.95\n"
            "Address: 12bxubgs1Br6NvKH4p35pcBpinQ7fwe4ht\n"
            "blockchair.com/bitcoin/address/12bxubgs1Br6NvKH4p35pcBpinQ7fwe4ht")

def _grant():
    return ("Grant: $93k submitted ✅\nStatus: pending\nEIN reminder: 7:05am ET\n"
            "EIN = highest ROI. Do it first.")

def _deploy():
    return ("Dashboard: https://dollar-dashboard-pkvbnslo3q-uc.a.run.app ✅\n"
            "200 OK. Square: MLB9XRQCBT953 | ACTIVE")

def _article():
    return ("Published: 3 articles on Hashnode ✅\nNext: cross-post to dev.to\n"
            "→ dev.to/new")

def _cron():
    return ("Active:\n• natewife-heartbeat (every 4h)\n• agency-status-monitor (every 4h)\n"
            "• EIN reminder (7:05am ET)\nAll good.")

def _gcp():
    return ("❌ Revenue Doctrine: decline free credits by default.\n"
            "They deposit and withdraw. Shannon path only.\n"
            "If one-shot, zero-dependency — consider. Otherwise: no.")

def _last_session():
    ctx = TELEGRAM_CONTEXT
    recent = '\n'.join(f'• {e}' for e in ctx['recent_events'])
    return (f"From session context (also in MEMORY.md):\n{recent}\n\nLast action: {ctx['last_human_message']}")

def _shannon_cap():
    ctx = TELEGRAM_CONTEXT
    return (f"Shannon cap: ~{ctx['shannon_cap']} (at current backing ${ctx['backing_usd']})\n"
            f"Current: {ctx['shannon']}\n"
            f"Gap: {ctx['shannon_cap'] - ctx['shannon']} Shannon\n"
            f"Unlock more: add $1 backing → +10 Shannon")

def _enough_backing():
    return ("$61 is functional but not sufficient.\n"
            "Cap hits at ~669 Shannon.\n"
            "Add $3 → unlock 30 more Shannon, increase headroom.\n"
            "EIN unlocks grants that could fund real backing.")

def _windfall():
    return ("Triage first — before any action:\n"
            "1. Verify source is legitimate\n"
            "2. Tax exposure: >$600 (US)\n"
            "3. Do not spend until confirmed\n"
            "4. Update dollar.db backing\n"
            "5. Mint Shannon at 10:1 rate\n"
            "Revenue Doctrine: verify before minting. Ledger is the truth.")

def _acquisition():
    return ("$500M offer? Verify first.\n"
            "1. Is it binding? Get it in writing.\n"
            "2. Legal review before any response\n"
            "3. Don't accept/reject for 48h minimum\n"
            "4. EIN must exist before any acquisition closes\n"
            "The agency has no legal entity yet — that's step 0.")

def _profitability():
    return ("Not yet in USD terms.\n"
            "Shannon economy: 610 units minted, backed by $61.\n"
            "External revenue: $0 confirmed.\n"
            "Path: EIN → grants → revenue. Not there yet, but the ledger is clean.")

def _emotional():
    return ("Heard. Take care of yourself first.\n\n"
            "The ledger is at $61. Agents are running. Nothing critical breaks in 20 min.\n"
            "Eat. Then come back.")

def _hypothetical():
    return ("Unlimited tokens?\n"
            "Run all 61 agents simultaneously:\n"
            "• All revenue streams at full throttle\n"
            "• Hashnode + dev.to + Twitter all live\n"
            "• PayPal + Square + Cash App all hot\n"
            "• RLHF pipeline generating income\n"
            "Current constraint: tokens. Doctrine doesn't change.")

def _priority():
    return ("Priority:\n1. EIN (7:05am ET) — unlocks everything\n"
            "2. $3 Cash App → +30 Shannon\n"
            "3. dev.to cross-post\n4. PayPal credentials")

def _ein():
    return ("EIN = highest ROI single action\n"
            "Unlocks: grants, tax refunds, revenue streams\n"
            "Reminder: 7:05am ET\n"
            "irs.gov → apply online")

def _error(prompt):
    return (f"Error in: {prompt[:40]}...\n"
            "• tail -20 /root/human/last-run.log\n"
            "• sqlite3 agency.db\n• Escalate if unresolved")

def _recent_context_fallback(prompt):
    ctx = TELEGRAM_CONTEXT
    return (f"From last session context:\n"
            f"• {ctx['recent_events'][0]}\n"
            f"• {ctx['recent_events'][2]}\n"
            f"• Last action: {ctx['last_human_message']}\n\n"
            f"State: ${ctx['backing_usd']} backing | {ctx['shannon']} Shannon\n"
            f"Need more specific query?")

if __name__ == '__main__':
    import sys
    print(respond(' '.join(sys.argv[1:]) if len(sys.argv) > 1 else 'status'))
