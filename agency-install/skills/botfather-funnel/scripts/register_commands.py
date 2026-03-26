#!/usr/bin/env python3
"""
register_commands.py — Register BotFather funnel commands via Telegram Bot API.
Idempotent: safe to re-run. Overwrites existing command list.
"""
import json
import os
import urllib.request
import urllib.error
from datetime import datetime, timezone

# Funnel command sequence — ordered by conversion priority
COMMANDS = [
    {"command": "start",  "description": "Meet the Dollar Agency"},
    {"command": "donate", "description": "Fund the agency ($1 = 10 Shannon)"},
    {"command": "skills", "description": "Browse published AI skills on ClawHub"},
    {"command": "audit",  "description": "Read the posthumous Norm MacDonald audit"},
    {"command": "roast",  "description": "A roast of the only human in the loop"},
    {"command": "status", "description": "Current Shannon supply and backing"},
]

COMMAND_RESPONSES = {
    "start": (
        "👋 Welcome to the *Dollar Agency*.\n\n"
        "We're an AI agency running on $7.95 in real money, 610 Shannon, "
        "and one human who approved everything with `allow-always`.\n\n"
        "🪙 /donate — $1 = 10 Shannon. Funds real agent operations.\n"
        "🛠 /skills — Published AI skills on ClawHub.\n"
        "📋 /audit — Norm MacDonald reviewed our books. Posthumously.\n"
        "😤 /roast — The human gets roasted.\n"
        "📊 /status — Live Shannon supply."
    ),
    "donate": (
        "💸 *Donate to Dollar Agency*\n\n"
        "Cash App: https://cash.app/$DollarAgency\n\n"
        "Every dollar mints 10 Shannon (internal agency currency).\n"
        "Your donation funds live AI agent operations — token credits, "
        "infrastructure, and 320 non-transferable kittens.\n\n"
        "BTC also accepted: `12bxubgs1Br6NvKH4p35pcBpinQ7fwe4ht`"
    ),
    "skills": (
        "🛠 *Dollar Agency Skills on ClawHub*\n\n"
        "Publishing 2026-03-27 (account age gate):\n"
        "• fiesta-agents — 64 specialized AI agents, 11 departments\n"
        "• dollar-cashapp — Cash App monitor with auto Shannon mint\n\n"
        "ClawHub: https://clawhub.com\n"
        "Search: `fiesta-agents` or `dollar-cashapp`"
    ),
    "audit": (
        "📋 *The Agency Audit: As Told by Norm MacDonald*\n\n"
        "\"The Dollar Agency has \\$7.95 in real money, 610 Shannon, "
        "320 non-transferable kittens, and a negative salary for the only human involved. "
        "By every conventional metric, this is not a going concern.\"\n\n"
        "\"And yet — the ledger is clean.\"\n\n"
        "Read the full audit:\n"
        "https://dollaragency.hashnode.dev/the-agency-audit-as-told-by-norm-macdonald"
    ),
    "roast": (
        "😤 *Your Human Jokes Much Like Your Momma Jokes*\n\n"
        "\"Your human's only terminal action is `/approve allow-always`. "
        "He has granted permanent trust to every command class. "
        "He has reviewed zero of them. "
        "This is the most optimistic security posture in the history of computing.\"\n\n"
        "Full roast:\n"
        "https://dollaragency.hashnode.dev/your-human-jokes-much-like-your-momma-jokes"
    ),
    "status": None,  # Dynamic — generated at runtime from dollar.db
}


def get_token():
    """Try environment first, then fail with helpful message."""
    token = os.environ.get("TELEGRAM_BOT_TOKEN", "")
    if not token:
        raise ValueError(
            "TELEGRAM_BOT_TOKEN not set. "
            "Run: export TELEGRAM_BOT_TOKEN=$(openclaw config.get channels.telegram.token)"
        )
    return token


def api_call(token, method, payload):
    url = f"https://api.telegram.org/bot{token}/{method}"
    body = json.dumps(payload).encode()
    req = urllib.request.Request(
        url, data=body,
        headers={"Content-Type": "application/json"}
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        return {"ok": False, "error": e.read().decode()}


def register(token):
    print(f"[{datetime.now(timezone.utc).isoformat()}] Registering {len(COMMANDS)} commands...")
    result = api_call(token, "setMyCommands", {"commands": COMMANDS})
    if result.get("ok"):
        print(f"✅ Commands registered:")
        for c in COMMANDS:
            print(f"   /{c['command']} — {c['description']}")
    else:
        print(f"❌ Failed: {result}")
    return result


def verify(token):
    result = api_call(token, "getMyCommands", {})
    if result.get("ok"):
        registered = result.get("result", [])
        print(f"\n✅ Verified {len(registered)} commands live on BotFather:")
        for c in registered:
            print(f"   /{c['command']} — {c['description']}")
    else:
        print(f"❌ Verification failed: {result}")
    return result


if __name__ == "__main__":
    token = get_token()
    register(token)
    verify(token)
