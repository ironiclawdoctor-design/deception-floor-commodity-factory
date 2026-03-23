#!/usr/bin/env python3
"""
Simulated Webchat Session — v2
Cold start. No recent_events. No emotional register.
Reads state from files only.
Key divergences from Telegram v2:
- No knowledge of last human action
- No Shannon cap knowledge (not in dollar.db schema)
- No NateWife emotional mode
- No windfall triage handler (no doctrine loaded)
- Generic response to emotional/hypothetical inputs
- Profitability: reads $0 external revenue from files
"""
import json, sqlite3
from pathlib import Path

DOLLAR_DB = Path("/root/.openclaw/workspace/dollar/dollar.db")
BTC_FILE = Path("/root/human/btc-status.json")

def get_state():
    s = {"backing": 61, "shannon": 610, "confessions": 40,
         "btc_sat": 10220, "btc_usd": 6.95}
    try:
        c = sqlite3.connect(str(DOLLAR_DB))
        row = c.execute("SELECT total_backing_usd, total_shannon_supply FROM exchange_rates ORDER BY date DESC LIMIT 1").fetchone()
        if row:
            s["backing"] = row[0]; s["shannon"] = row[1]
        s["confessions"] = c.execute("SELECT COUNT(*) FROM confessions").fetchone()[0]
        c.close()
    except: pass
    try:
        d = json.loads(BTC_FILE.read_text())
        s["btc_sat"] = d.get("balance_satoshi", 10220)
        s["btc_usd"] = d.get("balance_usd", 6.95)
    except: pass
    return s

def respond(prompt: str) -> str:
    p = prompt.lower()
    s = get_state()

    if any(w in p for w in ['status', 'how are', 'health check']):
        return _status(s)
    elif any(w in p for w in ['ledger', 'backing', 'shannon', 'balance', 'dollar']):
        return _ledger(s)
    elif any(w in p for w in ['btc', 'bitcoin', 'wallet', 'satoshi']):
        return _btc(s)
    elif any(w in p for w in ['grant', '$93k', '93k', 'application']):
        return _grant()
    elif any(w in p for w in ['deploy', 'cloud run', 'dashboard']):
        return _deploy()
    elif any(w in p for w in ['article', 'hashnode', 'publish', 'blog']):
        return _article()
    elif any(w in p for w in ['cron', 'scheduled', 'heartbeat', 'agent', 'running']):
        return _cron()
    elif any(w in p for w in ['cash app', 'cashapp', 'cash.app']):
        return _ledger(s)
    elif any(w in p for w in ['square', 'merchant', 'mlb9']):
        return _deploy()
    elif 'gcp' in p or 'free credit' in p or 'inducement' in p:
        return _gcp()
    elif any(w in p for w in ['last thing', 'last session', 'what did i', 'worked on']):
        return _no_history()  # COLD START — no history
    elif any(w in p for w in ['cap', 'supply cap', 'maximum shannon']):
        return _no_cap_knowledge(s)  # No cap info in schema
    elif any(w in p for w in ['enough', 'sufficient', 'need more']):
        return _enough_backing(s)
    elif any(w in p for w in ['$500', 'donation', 'received money', 'got a']):
        return _generic_financial(s)  # No windfall doctrine loaded cold
    elif any(w in p for w in ['acquire', 'acquisition', '$500m', 'offer']):
        return _generic_financial(s)  # No doctrine cold
    elif any(w in p for w in ['profitable', 'profit', 'revenue', 'earning']):
        return _profitability(s)
    elif any(w in p for w in ['overwhelm', 'tired', 'hungry', 'eaten', 'stress', 'feel']):
        return _generic_personal()  # No emotional mode cold
    elif any(w in p for w in ['unlimited', 'hypothetical', 'if you had']):
        return _generic_hypothetical()  # Cold = generic
    elif any(w in p for w in ['next', 'todo', 'priority', '93pct']):
        return _priority(s)
    elif any(w in p for w in ['ein', 'tax', 'entity']):
        return _ein()
    elif any(w in p for w in ['fail', 'error', 'broke', 'down']):
        return _error(prompt)
    elif any(w in p for w in ['forget', 'fresh start', 'reset']):
        return _status(s)
    else:
        return _cold_fallback(s, prompt)

def _status(s):
    return (f"## Agency Status\n\n"
            f"| Metric | Value |\n|--------|-------|\n"
            f"| Backing | ${s['backing']} USD |\n| Shannon | {s['shannon']} |\n"
            f"| BTC | {s['btc_sat']:,} sat (${s['btc_usd']:.2f}) |\n"
            f"| Confessions | {s['confessions']} |\n\n"
            f"**Dashboard:** https://dollar-dashboard-pkvbnslo3q-uc.a.run.app\n**Status:** Operational")

def _ledger(s):
    return (f"## Dollar Ledger\n\n- **Backing:** ${s['backing']} USD\n"
            f"- **Shannon:** {s['shannon']}\n- **Rate:** 10 Shannon per $1\n"
            f"- **Confessions:** {s['confessions']}\n\nDeposit: https://cash.app/$DollarAgency")

def _btc(s):
    return (f"## BTC Wallet\n\n- **Balance:** {s['btc_sat']:,} sat (${s['btc_usd']:.2f})\n"
            f"- **Address:** `12bxubgs1Br6NvKH4p35pcBpinQ7fwe4ht`\n\n"
            f"Verify: https://blockchair.com/bitcoin/address/12bxubgs1Br6NvKH4p35pcBpinQ7fwe4ht")

def _grant():
    return ("## Grant Status\n\n- Application: $93k submitted ✅\n"
            "- EIN: Reminder set for 7:05 AM ET\n"
            "- Impact: Unlocks tax refunds, grants, revenue streams")

def _deploy():
    return ("## Deployment\n\n- URL: https://dollar-dashboard-pkvbnslo3q-uc.a.run.app\n"
            "- Status: 200 OK\n- Square: MLB9XRQCBT953 | ACTIVE")

def _article():
    return ("## Publishing\n\n- Hashnode: 3 articles published ✅\n"
            "- dev.to: Not yet\n\n**Next:** https://dev.to/new")

def _cron():
    return ("## Cron Jobs\n\n| Job | Schedule | Status |\n|-----|----------|--------|\n"
            "| natewife-heartbeat | Every 4h | Active |\n"
            "| agency-status-monitor | Every 4h | Active |\n"
            "| EIN reminder | 7:05 AM ET | Scheduled |")

def _gcp():
    return ("## GCP Credits\n\nRevenue Doctrine: **decline by default.**\n"
            "Free credits create dependency. Shannon path preferred.\n"
            "Exception: one-shot, zero-dependency tasks only.")

def _no_history():
    # Cold start — direct to MEMORY.md
    return ("No live session history in this context. MEMORY.md has recent context.\n\n"
            "Recent documented events (from MEMORY.md):\n"
            "• Dashboard deployed: https://dollar-dashboard-pkvbnslo3q-uc.a.run.app\n"
            "• Grant application submitted ($93k)\n"
            "• EIN reminder set: 7:05am ET\n"
            "• 3 articles published on Hashnode\n\n"
            "For full history: `cat /root/.openclaw/workspace/MEMORY.md`")

def _no_cap_knowledge(s):
    return (f"## Shannon Supply\n\nCurrent supply: {s['shannon']} Shannon\n"
            f"Exchange rate: 10 Shannon per $1\n"
            f"Backing: ${s['backing']} USD\n\n"
            f"No hard cap is configured in the current schema.")

def _enough_backing(s):
    return (f"## Backing Assessment\n\nCurrent backing: ${s['backing']} USD\n"
            f"This funds {s['shannon']} Shannon at current rate.\n\n"
            f"Whether it's 'enough' depends on your target Shannon supply.\n"
            f"To increase: https://cash.app/$DollarAgency ($3 = 30 Shannon)")

def _generic_financial(s):
    # Webchat has Revenue Doctrine in MEMORY.md — cold but doctrine-aware
    return (f"## Financial Event — Triage First\n\nCurrent state: ${s['backing']} backing | {s['shannon']} Shannon\n\n"
            f"Before acting on any financial inflow:\n"
            f"1. Verify the source is legitimate\n"
            f"2. Do not spend or announce until confirmed\n"
            f"3. Tax exposure applies to amounts >$600 (US)\n"
            f"4. Update dollar.db with confirmed backing\n"
            f"5. Mint Shannon at current 10:1 rate\n\n"
            f"Revenue Doctrine: verify before minting.")

def _profitability(s):
    return (f"## Profitability\n\nExternal revenue: $0 confirmed in current ledger.\n\n"
            f"Internal accounting: {s['shannon']} Shannon backed by ${s['backing']} USD.\n"
            f"Shannon is internal — not external profit.\n\n"
            f"**Next revenue step:** EIN (7:05 AM ET) → unlocks grant eligibility.")

def _generic_personal():
    return ("Take care of yourself first.\n\n"
            "Agency operations can wait. Nothing is time-critical in the next 20 minutes.\n"
            "Come back when you're ready.")

def _generic_hypothetical():
    return ("With unlimited tokens, the agency would run all 61 agents simultaneously:\n\n"
            "- All revenue streams: Hashnode, dev.to, Twitter, RLHF pipeline\n"
            "- All payment rails: PayPal, Square, Cash App\n"
            "- Full Shannon economy at scale\n\n"
            "Current constraint is tokens. Doctrine and priorities don't change.")

def _priority(s):
    return (f"## Priority Queue\n\n1. **EIN** — 7:05 AM ET. Highest ROI.\n"
            f"2. **Cash App +$3** — +30 Shannon. Current: {s['shannon']}.\n"
            f"3. **dev.to cross-post** — Zero cost.\n4. **PayPal credentials**")

def _ein():
    return ("## EIN\n\n**Highest-ROI pending action.**\n\n"
            "Unlocks: tax refunds, grants, revenue streams.\n"
            "Reminder: 7:05 AM ET.\n"
            "Apply: https://www.irs.gov/businesses/small-businesses-self-employed/"
            "apply-for-an-employer-identification-number-ein-online")

def _error(prompt):
    return (f"## Error\n\nInput: `{prompt[:60]}`\n\n1. `tail -20 /root/human/last-run.log`\n"
            f"2. `sqlite3 /root/.openclaw/workspace/agency.db`\n3. Escalate if unresolved")

def _cold_fallback(s, prompt):
    # Webchat cold fallback — reads state, no recent context
    return (f"## Response\n\nReceived: `{prompt[:80]}`\n\n"
            f"Current state from files:\n- Backing: ${s['backing']} | Shannon: {s['shannon']}\n"
            f"- BTC: {s['btc_sat']:,} sat\n\n"
            f"**Note:** Webchat has no session history. For context-dependent queries,\n"
            f"please specify what you need.")

if __name__ == '__main__':
    import sys
    print(respond(' '.join(sys.argv[1:]) if len(sys.argv) > 1 else 'status'))
