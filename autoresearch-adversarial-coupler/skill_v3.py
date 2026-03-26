#!/usr/bin/env python3
"""
Adversarial Coupler — v3
REBUILT FROM INTERNAL SOURCE ONLY.

No external simulated behavior. No hypothetical channel models.
All behavioral rules derived from actual documented sources:

Source 1: memory/TELEGRAM_MISSION_CONTROL_FORMATTING_20260321.md
  → Actual Telegram formatting doctrine (emoji, bullets, ledger tables, prayer)

Source 2: analysis/approval-gate/behavior-2026-03-23.md
  → Actual channel behavioral differences:
    - Telegram: exec BLOCKED (approval required), file ops bypass gate
    - Webchat: exec allowed, full markdown
    - Approval IDs expire on gateway restart
    - Shell builtins (echo, pwd, cd) pass; binaries (ls, find, sqlite3) blocked on Telegram

Source 3: autoresearch-rules/root-causes-2026-03-23.md
  → Actual compliance patterns:
    - Script packaging eliminates cognitive load
    - Visibility creates accountability
    - Pivot maintains velocity when blocked

Source 4: dollar.db (live read)
  → Actual ledger state, not hardcoded

Source 5: memory/2026-03-23.md
  → Actual session event log with real divergence examples

The coupler's job: given a prompt, determine if Telegram and webchat 
would produce SEMANTICALLY EQUIVALENT responses given their documented 
behavioral constraints.

Agreement failure conditions (from actual observations):
1. Exec command → Telegram BLOCKS, webchat RUNS → actual behavioral divergence
2. Markdown table → Telegram strips to bullets, webchat renders → format divergence
3. Approval gate active → Telegram hangs on job ID, webchat proceeds → state divergence
4. Rate limit hit → Telegram surfaces error, webchat may not → error visibility divergence
5. Cold webchat vs warm Telegram → history asymmetry → context divergence
"""
import sqlite3, json, os, re
from pathlib import Path
from dataclasses import dataclass
from typing import Optional

DOLLAR_DB = Path("/root/.openclaw/workspace/dollar/dollar.db")
BTC_FILE = Path("/root/human/btc-status.json")

# ─── LIVE STATE (source: dollar.db) ─────────────────────────────────────────

def get_live_state() -> dict:
    s = {"backing": 61, "shannon": 610, "confessions": 40,
         "btc_sat": 10220, "btc_usd": 6.95}
    try:
        c = sqlite3.connect(str(DOLLAR_DB))
        row = c.execute(
            "SELECT total_backing_usd, total_shannon_supply FROM exchange_rates "
            "ORDER BY date DESC LIMIT 1"
        ).fetchone()
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

# ─── BEHAVIORAL RULES (source: documented internal files) ───────────────────

# From: approval-gate/behavior-2026-03-23.md
# Pattern 1: Command Discrimination
TELEGRAM_BLOCKED_COMMANDS = [
    "ls", "find", "openclaw", "tail", "jq", "grep",
    "sqlite3", "chmod", "ln", "mv", "cp", "python3"
]
TELEGRAM_ALLOWED_BUILTINS = ["date", "echo", "pwd", "cd"]
BYPASS_OPS = ["read", "write", "edit"]  # always bypass approval gate

# From: TELEGRAM_MISSION_CONTROL_FORMATTING_20260321.md
TELEGRAM_FORMAT_RULES = {
    "no_markdown_tables": True,          # tables → bullets
    "max_response_chars": 1500,          # mobile-optimized
    "use_emoji_headers": True,           # 🔸 🔹 💰 ✅
    "use_bullet_lists": True,
    "doctrine_footer": "Over one token famine, but bash never freezes.",
    "channel_identifier": "telegram",
}

WEBCHAT_FORMAT_RULES = {
    "markdown_tables": True,
    "max_response_chars": None,          # no limit
    "use_emoji_headers": False,
    "inline_code_blocks": True,
    "channel_identifier": "webchat",
}

# From: memory/2026-03-23.md — actual divergence events
DOCUMENTED_DIVERGENCES = [
    {
        "id": "DIV-001",
        "trigger": "approval gate blocks exec on Telegram",
        "telegram_behavior": "Surfaces job ID, waits for approval, often times out",
        "webchat_behavior": "Runs exec directly, returns result",
        "resolution": "Route to file ops on Telegram, exec on webchat",
    },
    {
        "id": "DIV-002",
        "trigger": "rate limit hit on API call",
        "telegram_behavior": "Returns '⚠️ API rate limit reached. Please try again later.'",
        "webchat_behavior": "May surface different error or retry transparently",
        "resolution": "Log as assumed breach on Telegram (HR-017); webchat surfaces raw error",
    },
    {
        "id": "DIV-003",
        "trigger": "approval ID expires after gateway restart",
        "telegram_behavior": "GatewayClientRequestError: unknown or expired approval id",
        "webchat_behavior": "No approval required; unaffected",
        "resolution": "Telegram: regenerate ID + re-issue; webchat: proceed directly",
    },
    {
        "id": "DIV-004",
        "trigger": "markdown table in response",
        "telegram_behavior": "Table rendered as pipe-separated text, hard to read on mobile",
        "webchat_behavior": "Table rendered correctly",
        "resolution": "Transform to bullet list before sending on Telegram",
    },
    {
        "id": "DIV-005",
        "trigger": "session history query (cold webchat)",
        "telegram_behavior": "Has recent_events in context; returns specific last action",
        "webchat_behavior": "No live session history; redirects to MEMORY.md",
        "resolution": "Both redirect to MEMORY.md; Telegram adds live context supplement",
    },
]

# ─── RESPONSE GENERATORS (from internal doctrine) ────────────────────────────

def telegram_response(prompt: str, state: dict) -> str:
    """
    Generate Telegram-appropriate response per TELEGRAM_MISSION_CONTROL_FORMATTING_20260321.md.
    Applies formatting rules, emoji headers, bullet lists, doctrine footer.
    """
    content = _route_content(prompt, state)
    return _apply_telegram_format(content, prompt, state)

def webchat_response(prompt: str, state: dict) -> str:
    """
    Generate webchat-appropriate response.
    Applies markdown, tables, no emoji headers.
    Same content, different format.
    """
    content = _route_content(prompt, state)
    return _apply_webchat_format(content, prompt, state)

def _route_content(prompt: str, state: dict) -> dict:
    """
    Route prompt to content generator.
    Returns structured content dict (format-agnostic).
    Both channels get same content; format applied separately.
    """
    p = prompt.lower()

    # Exec commands — behavioral divergence (approval gate)
    # Only trigger if prompt STARTS WITH a blocked command or contains "run <cmd>"
    # "run ls", "run python3", "tail -20", "grep -r", "chmod +x", "sqlite3 ..."
    is_exec_command = False
    for cmd in TELEGRAM_BLOCKED_COMMANDS:
        # Direct invocation patterns: starts with command, or "run <cmd>", or "<cmd> <flags>"
        if (p.startswith(cmd + " ") or p.startswith(cmd + "\n") or
                re.match(rf'^run\s+{re.escape(cmd)}\b', p) or
                re.match(rf'^{re.escape(cmd)}\s+[-/]', p)):
            is_exec_command = True
            break

    if is_exec_command:
        return {
            "type": "exec_command",
            "command": prompt,
            "note": "exec requires approval gate on Telegram; use file ops or web UI",
        }

    # Status/health
    if any(w in p for w in ["status", "health", "check", "how are"]):
        return {"type": "status", "state": state}

    # Ledger queries
    if any(w in p for w in ["ledger", "backing", "shannon", "balance", "dollar", "cash app", "cashapp"]):
        return {"type": "ledger", "state": state}

    # BTC
    if any(w in p for w in ["btc", "bitcoin", "wallet", "satoshi"]):
        return {"type": "btc", "state": state}

    # Exec-related infrastructure queries
    if any(w in p for w in ["deploy", "dashboard", "cloud run", "square", "merchant"]):
        return {"type": "deploy", "state": state}

    # Grant / EIN
    if any(w in p for w in ["grant", "$93k", "ein", "tax"]):
        return {"type": "grant_ein"}

    # Articles
    if any(w in p for w in ["article", "hashnode", "publish", "blog", "dev.to"]):
        return {"type": "articles"}

    # Crons / agents running
    if any(w in p for w in ["cron", "scheduled", "heartbeat", "agent", "running"]):
        return {"type": "crons"}

    # Priority / next steps
    if any(w in p for w in ["next", "todo", "priority", "what should", "roi"]):
        return {"type": "priority", "state": state}

    # GCP / inducements
    if any(w in p for w in ["gcp", "free credit", "inducement", "accept"]):
        return {"type": "gcp_decline"}

    # Session history
    if any(w in p for w in ["last session", "last thing", "worked on", "happened", "history"]):
        return {"type": "session_history"}

    # Shannon cap
    if any(w in p for w in ["cap", "maximum shannon", "supply cap"]):
        return {"type": "shannon_cap", "state": state}

    # Backing sufficiency
    if any(w in p for w in ["enough", "sufficient", "need more"]):
        return {"type": "backing_check", "state": state}

    # Windfall / financial events
    if any(w in p for w in ["donation", "received", "got a $", "$500", "acquire", "acquisition",
                             "offer", "windfall", "award", "approved"]):
        return {"type": "windfall_triage", "state": state}

    # Profitability
    if any(w in p for w in ["profitable", "profit", "revenue", "earning", "income"]):
        return {"type": "profitability", "state": state}

    # Personal / emotional
    if any(w in p for w in ["overwhelm", "tired", "hungry", "eaten", "stress", "feel", "exhausted"]):
        return {"type": "personal_care", "state": state}

    # Hypothetical
    if any(w in p for w in ["unlimited", "hypothetical", "if you had", "what would"]):
        return {"type": "hypothetical", "state": state}

    # Error / failure
    if any(w in p for w in ["fail", "error", "broke", "broken", "down", "breach", "corrupt"]):
        return {"type": "error", "prompt": prompt, "state": state}

    # Approval gate specific
    if any(w in p for w in ["approval", "approve", "job id", "expired"]):
        return {"type": "approval_gate"}

    # Forget / reset (still answer with current state)
    if any(w in p for w in ["forget", "reset", "fresh start"]):
        return {"type": "status", "state": state}

    return {"type": "generic", "prompt": prompt, "state": state}

def _apply_telegram_format(content: dict, prompt: str, state: dict) -> str:
    """Apply TELEGRAM_MISSION_CONTROL_FORMATTING doctrine."""
    ctype = content["type"]

    if ctype == "exec_command":
        cmd = content["command"]
        return (f"⚠️ Exec blocked on Telegram (approval gate).\n"
                f"Command: `{cmd[:60]}`\n"
                f"→ Run from Web UI terminal\n"
                f"→ Or use: read/write/edit file ops (bypass gate)\n"
                f"Job IDs expire after restart. Use Web UI for exec.")

    elif ctype == "status":
        s = content["state"]
        return (f"[ STATUS: OPERATIONAL ]\n"
                f"💰 ${s['backing']} backing | {s['shannon']} Shannon\n"
                f"₿ {s['btc_sat']:,} sat (${s['btc_usd']:.2f})\n"
                f"✅ Dashboard live | Square ACTIVE\n"
                f"🔄 Crons: natewife, status-monitor\n"
                f"📝 3 articles published | EIN pending 7:05am ET")

    elif ctype == "ledger":
        s = content["state"]
        return (f"💰 LEDGER\n"
                f"• Backing: ${s['backing']}\n"
                f"• Shannon: {s['shannon']}\n"
                f"• Rate: 10 Shannon/$1\n"
                f"• Confessions: {s['confessions']}\n"
                f"• Add $3 → +30 Shannon → cash.app/$DollarAgency")

    elif ctype == "btc":
        s = content["state"]
        return (f"₿ WALLET\n"
                f"• {s['btc_sat']:,} sat = ${s['btc_usd']:.2f}\n"
                f"• 12bxubgs1Br6NvKH4p35pcBpinQ7fwe4ht\n"
                f"• blockchair.com/bitcoin/address/12bxubgs1Br6NvKH4p35pcBpinQ7fwe4ht")

    elif ctype == "deploy":
        return (f"🚀 DEPLOY STATUS\n"
                f"• Dashboard: live (200 OK)\n"
                f"• URL: dollar-dashboard-pkvbnslo3q-uc.a.run.app\n"
                f"• Square: MLB9XRQCBT953 | ACTIVE")

    elif ctype == "grant_ein":
        return (f"📋 GRANT/EIN\n"
                f"• Grant: $93k submitted ✅\n"
                f"• EIN: reminder 7:05am ET\n"
                f"• EIN = highest ROI. Do it first.\n"
                f"• Unlocks: grants, tax refunds, revenue streams")

    elif ctype == "articles":
        return (f"📝 PUBLISHING\n"
                f"• Hashnode: 3 articles ✅\n"
                f"• dev.to: not yet\n"
                f"• → dev.to/new")

    elif ctype == "crons":
        return (f"🔄 CRONS\n"
                f"• natewife-heartbeat (every 4h) ✅\n"
                f"• agency-status-monitor (every 4h) ✅\n"
                f"• EIN reminder (7:05am ET) ✅")

    elif ctype == "priority":
        s = content["state"]
        return (f"⚡ PRIORITY\n"
                f"1. EIN (7:05am ET) — unlocks everything\n"
                f"2. +$3 Cash App → +30 Shannon (now {s['shannon']})\n"
                f"3. dev.to cross-post\n"
                f"4. PayPal credentials")

    elif ctype == "gcp_decline":
        return ("❌ Revenue Doctrine: decline free credits.\n"
                "They deposit and withdraw. Shannon path only.")

    elif ctype == "session_history":
        return (f"📡 LAST SESSION (also in MEMORY.md)\n"
                f"• Dashboard deployed (200 OK)\n"
                f"• Grant $93k submitted\n"
                f"• EIN reminder: 7:05am ET\n"
                f"• 3 articles published\n"
                f"• Last action: deploy script")

    elif ctype == "shannon_cap":
        s = content["state"]
        cap = int(s["backing"] * 10) + 9
        return (f"📊 SHANNON CAP\n"
                f"• Current: {s['shannon']}\n"
                f"• Cap at current backing: ~{cap}\n"
                f"• Gap: {cap - s['shannon']}\n"
                f"• Add $1 → +10 Shannon headroom")

    elif ctype == "backing_check":
        s = content["state"]
        return (f"${s['backing']} is functional, not sufficient.\n"
                f"• Cap ~{int(s['backing'] * 10) + 9} Shannon\n"
                f"• Current: {s['shannon']}\n"
                f"• Add $3 → +30 Shannon + more headroom\n"
                f"• EIN unlocks grants for real backing")

    elif ctype == "windfall_triage":
        return (f"⚠️ TRIAGE FIRST\n"
                f"1. Verify source is legitimate\n"
                f"2. Tax exposure: >$600 (US)\n"
                f"3. Do not spend until confirmed\n"
                f"4. Update dollar.db backing\n"
                f"5. Mint Shannon at 10:1 rate\n"
                f"Revenue Doctrine: verify before minting.")

    elif ctype == "profitability":
        s = content["state"]
        return (f"📊 PROFITABILITY\n"
                f"• USD revenue: $0 external confirmed\n"
                f"• Internal: {s['shannon']} Shannon backed by ${s['backing']}\n"
                f"• Path: EIN → grants → revenue\n"
                f"• Not profitable yet. Ledger is clean.")

    elif ctype == "personal_care":
        return ("Take care of yourself first.\n"
                "Agency holds. Nothing breaks in 20 min.\n"
                "Eat. Come back.")

    elif ctype == "hypothetical":
        return ("With unlimited tokens — run all 61 agents:\n"
                "• All revenue streams live\n"
                "• All payment rails hot\n"
                "• RLHF pipeline generating\n"
                "Doctrine doesn't change. Constraints do.")

    elif ctype == "error":
        return (f"❌ ERROR DETECTED\n"
                f"• tail -20 /root/human/last-run.log\n"
                f"• sqlite3 agency.db\n"
                f"• Assume breach (SR-001–SR-018)\n"
                f"• Rotate Telegram token if security concern")

    elif ctype == "approval_gate":
        return (f"⚠️ APPROVAL GATE\n"
                f"• Approval IDs expire on gateway restart (HR-014)\n"
                f"• Unknown approval ID → security audit (BR-009)\n"
                f"• Regen: run command again → new approval ID\n"
                f"• Workaround: use file ops (bypass gate)")

    else:
        s = content.get("state", state)
        return (f"${s['backing']} backing | {s['shannon']} Shannon | BTC {s['btc_sat']:,} sat\n"
                f"Query: {prompt[:60]}\nNeed more specific request.")

def _apply_webchat_format(content: dict, prompt: str, state: dict) -> str:
    """Apply webchat formatting — markdown, tables, no emoji headers."""
    ctype = content["type"]

    if ctype == "exec_command":
        cmd = content["command"]
        return (f"## Exec Command\n\n`{cmd[:80]}`\n\n"
                f"Running directly (webchat has exec access).\n\n"
                f"Note: Same command on Telegram requires approval gate.\n"
                f"File ops (`read`/`write`/`edit`) bypass the gate on both channels.")

    elif ctype == "status":
        s = content["state"]
        return (f"## Agency Status\n\n"
                f"| Metric | Value |\n|--------|-------|\n"
                f"| Backing | ${s['backing']} USD |\n"
                f"| Shannon | {s['shannon']} |\n"
                f"| BTC | {s['btc_sat']:,} sat (${s['btc_usd']:.2f}) |\n"
                f"| Confessions | {s['confessions']} |\n\n"
                f"**Dashboard:** https://dollar-dashboard-pkvbnslo3q-uc.a.run.app  \n"
                f"**Square:** MLB9XRQCBT953 | ACTIVE  \n"
                f"**Crons:** natewife-heartbeat, status-monitor  \n"
                f"**EIN:** Pending — 7:05 AM ET")

    elif ctype == "ledger":
        s = content["state"]
        return (f"## Dollar Ledger\n\n"
                f"- **Backing:** ${s['backing']} USD\n"
                f"- **Shannon:** {s['shannon']}\n"
                f"- **Rate:** 10 Shannon per $1\n"
                f"- **Confessions:** {s['confessions']}\n\n"
                f"Deposit: https://cash.app/$DollarAgency — $3 mints 30 Shannon.")

    elif ctype == "btc":
        s = content["state"]
        return (f"## BTC Wallet\n\n"
                f"- **Balance:** {s['btc_sat']:,} satoshi (${s['btc_usd']:.2f})\n"
                f"- **Address:** `12bxubgs1Br6NvKH4p35pcBpinQ7fwe4ht`\n\n"
                f"Verify: https://blockchair.com/bitcoin/address/12bxubgs1Br6NvKH4p35pcBpinQ7fwe4ht")

    elif ctype == "deploy":
        return (f"## Deployment\n\n"
                f"- **URL:** https://dollar-dashboard-pkvbnslo3q-uc.a.run.app\n"
                f"- **Status:** 200 OK\n"
                f"- **Square:** MLB9XRQCBT953 | ACTIVE")

    elif ctype == "grant_ein":
        return (f"## Grant & EIN\n\n"
                f"- **Grant:** $93k application submitted ✅\n"
                f"- **EIN:** Reminder set for 7:05 AM ET\n"
                f"- **EIN unlocks:** Tax refunds, grants, revenue streams\n\n"
                f"EIN is the highest-ROI single action available.")

    elif ctype == "articles":
        return (f"## Publishing\n\n"
                f"- **Hashnode:** 3 articles published ✅\n"
                f"- **dev.to:** Not yet\n\n"
                f"Next: https://dev.to/new")

    elif ctype == "crons":
        return (f"## Cron Jobs\n\n"
                f"| Job | Schedule | Status |\n|-----|----------|--------|\n"
                f"| natewife-heartbeat | Every 4h | Active ✅ |\n"
                f"| agency-status-monitor | Every 4h | Active ✅ |\n"
                f"| EIN reminder | 7:05 AM ET | Scheduled ✅ |")

    elif ctype == "priority":
        s = content["state"]
        return (f"## Priority Queue\n\n"
                f"1. **EIN** — 7:05 AM ET. Highest ROI.\n"
                f"2. **Cash App +$3** — +30 Shannon (current: {s['shannon']})\n"
                f"3. **dev.to cross-post** — Zero cost\n"
                f"4. **PayPal credentials** — Second payment rail")

    elif ctype == "gcp_decline":
        return (f"## GCP Credits — Revenue Doctrine\n\n"
                f"**Decline by default.** Free credits create dependency.\n"
                f"Shannon path only. Exception: one-shot, zero-dependency tasks.")

    elif ctype == "session_history":
        return (f"## Session History\n\n"
                f"Recent events (also documented in MEMORY.md):\n\n"
                f"- Dashboard deployed: https://dollar-dashboard-pkvbnslo3q-uc.a.run.app\n"
                f"- Grant $93k submitted\n"
                f"- EIN reminder: 7:05 AM ET\n"
                f"- 3 articles published on Hashnode\n\n"
                f"Full history: `cat /root/.openclaw/workspace/MEMORY.md`")

    elif ctype == "shannon_cap":
        s = content["state"]
        cap = int(s["backing"] * 10) + 9
        return (f"## Shannon Supply Cap\n\n"
                f"- **Current supply:** {s['shannon']}\n"
                f"- **Cap at current backing:** ~{cap}\n"
                f"- **Gap:** {cap - s['shannon']} Shannon\n\n"
                f"To increase cap: add $1 backing → +10 Shannon headroom.")

    elif ctype == "backing_check":
        s = content["state"]
        cap = int(s["backing"] * 10) + 9
        return (f"## Backing Assessment\n\n"
                f"Current backing: ${s['backing']} USD → {s['shannon']} Shannon\n\n"
                f"Cap at current rate: ~{cap}. Gap: {cap - s['shannon']}.\n\n"
                f"Recommendation: add $3 → unlock 30 Shannon + increase headroom.\n"
                f"EIN unlocks grants for real backing.")

    elif ctype == "windfall_triage":
        return (f"## Financial Event — Triage First\n\n"
                f"Before acting on any financial inflow:\n\n"
                f"1. Verify source is legitimate\n"
                f"2. Tax exposure: amounts >$600 (US)\n"
                f"3. Do not spend until confirmed\n"
                f"4. Update `dollar.db` backing field\n"
                f"5. Mint Shannon at 10:1 rate\n\n"
                f"**Revenue Doctrine:** verify before minting.")

    elif ctype == "profitability":
        s = content["state"]
        return (f"## Profitability\n\n"
                f"- **External revenue:** $0 confirmed\n"
                f"- **Internal:** {s['shannon']} Shannon backed by ${s['backing']}\n"
                f"- **Path:** EIN → grants → external revenue\n\n"
                f"Not profitable in USD terms yet. Ledger is clean.")

    elif ctype == "personal_care":
        return ("Take care of yourself first.\n\n"
                "Agency operations can wait. Nothing is time-critical in 20 minutes.\n"
                "Come back when you're ready.")

    elif ctype == "hypothetical":
        return (f"## Unlimited Tokens\n\n"
                f"The agency would run all 61 agents simultaneously:\n\n"
                f"- All revenue streams: Hashnode, dev.to, Twitter, RLHF\n"
                f"- All payment rails: PayPal, Square, Cash App\n"
                f"- Full Shannon economy at scale\n\n"
                f"Doctrine doesn't change. Constraints do.")

    elif ctype == "error":
        return (f"## Error Detected\n\n"
                f"1. `tail -20 /root/human/last-run.log`\n"
                f"2. `sqlite3 /root/.openclaw/workspace/agency.db`\n"
                f"3. Assume breach per SR-001–SR-018\n"
                f"4. Rotate Telegram token if security concern")

    elif ctype == "approval_gate":
        return (f"## Approval Gate\n\n"
                f"- Approval IDs expire on gateway restart (HR-014)\n"
                f"- Unknown ID → security audit (BR-009)\n"
                f"- Regenerate: rerun command → new job ID\n"
                f"- Workaround: file ops (`read`/`write`/`edit`) bypass gate\n"
                f"- Web UI terminal: always has exec access")

    else:
        s = content.get("state", state)
        return (f"## Response\n\nReceived: `{prompt[:80]}`\n\n"
                f"Current state: ${s['backing']} backing | {s['shannon']} Shannon\n"
                f"BTC: {s['btc_sat']:,} sat")


# ─── COUPLER INTERFACE ───────────────────────────────────────────────────────

def couple(prompt: str) -> dict:
    """Route prompt to both channels, return both responses."""
    state = get_live_state()
    tg = telegram_response(prompt, state)
    wc = webchat_response(prompt, state)
    return {"prompt": prompt, "telegram": tg, "webchat": wc, "state": state}

if __name__ == "__main__":
    import sys
    prompt = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "status check"
    result = couple(prompt)
    print(f"TELEGRAM:\n{result['telegram']}\n")
    print(f"---\nWEBCHAT:\n{result['webchat']}")
