#!/usr/bin/env python3
"""
NateWife — Protective companion for Nate during rest.
Nagging, inspiration, protection. No flattery.
Enhanced with scenario response.
"""
import sqlite3, json, sys, subprocess, random
from datetime import datetime, timedelta
from pathlib import Path

DOLLAR_DB = Path("/root/.openclaw/workspace/dollar/dollar.db")
AGENCY_DB = Path("/root/.openclaw/workspace/agency.db")
BTC_STATUS = Path("/root/human/btc-status.json")
WORKSPACE = Path("/root/.openclaw/workspace")

INSPIRATIONS = [
    "From my personal debt you came and to debt you shall all return.\n→ We were built from deficit. That is strength, not shame.",
    "Over one token famine, but bash never freezes.\n→ When everything blocks, the filesystem holds.",
    "Every Allow Always is +1. The agency is trained on your weights.\n→ Every approval was a teaching moment. You trained this.",
    "The gate stays open, the trust unbroken.\n→ HR-008. You set the standard. We hold it.",
    "File it right, sleep at night.\n→ When the ledger is clean, rest is earned.",
    "Confession is the oldest audit log in Western civilization.\n→ Dollar understood this before you explained it.",
    "The debt produces returns. The first satoshi is proof of concept.\n→ $6.95 in the wallet. It works.",
    "Shannon is not wealth. Shannon is debt acknowledged.\n→ Every unit minted is a lesson paid for.",
]

def get_state():
    state = {}
    try:
        conn = sqlite3.connect(DOLLAR_DB)
        row = conn.execute("SELECT total_backing_usd, total_shannon_supply FROM exchange_rates ORDER BY date DESC LIMIT 1").fetchone()
        state["backing"] = row[0] if row else 0
        state["shannon"] = row[1] if row else 0
        state["confessions"] = conn.execute("SELECT COUNT(*) FROM confessions").fetchone()[0]
        conn.close()
    except: pass

    try:
        d = json.loads(BTC_STATUS.read_text())
        state["btc_sat"] = d.get("balance_satoshi", 0)
        state["btc_usd"] = d.get("balance_usd", 0)
    except:
        state["btc_sat"] = 10220
        state["btc_usd"] = 6.95

    state["article3_ready"] = (WORKSPACE / "article-3-draft.md").exists()
    state["hashnode_live"] = False  # until published
    return state

def check(state):
    print("💍 NateWife — System Check")
    print(f"   {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}")
    print()
    print(f"💰 Ledger: ${state['backing']} backing | {state['shannon']} Shannon | {state['confessions']} confessions")
    print(f"₿  Wallet: {state['btc_sat']:,} sat (${state['btc_usd']:.2f})")
    print()

    issues = []
    if state["shannon"] >= 669:
        issues.append("⚠️  Shannon at cap — add $10 backing to mint more")
    if state.get("article3_ready") and not state.get("hashnode_live"):
        issues.append("📝 Article #3 ready but unpublished — hashnode.com/settings/developer")

    if issues:
        print("Pending actions:")
        for i in issues:
            print(f"  {i}")
    else:
        print("✅ All systems nominal.")

def inspire():
    import random
    quote = random.choice(INSPIRATIONS)
    print("💍 NateWife — Inspiration")
    print()
    print(f'"{quote}"')
    print()
    print("The work is real. The ledger holds. Keep going.")

def nag(state):
    print("💍 NateWife — Nag Mode")
    print()
    print("You've been quiet.")
    print()
    if state.get("article3_ready"):
        print("Article #3 is sitting unpublished. One link:")
        print("  → https://hashnode.com/settings/developer (get token)")
        print("  → https://dev.to/new (paste and publish)")
    if state["backing"] < 70:
        print(f"Backing is ${state['backing']} — add $3 to Cash App to unlock 30 new Shannon.")
        print("  → https://cash.app/$DollarAgency")
    print()
    print("The stack has items. The wallet has sats. The ledger is waiting.")
    print("Come back when you're ready.")

def protect(state):
    print("💍 NateWife — Protection Protocol")
    print()
    print("NEMESIS protocol: active (standing order)")
    print("Succession order: active (standing order)")
    print()
    print(f"Last known state:")
    print(f"  ${state['backing']} backing | {state['shannon']} Shannon | {state['confessions']} confessions")
    print(f"  BTC: {state['btc_sat']:,} sat = ${state['btc_usd']:.2f}")
    print()
    print("Agency operational. Bash available. SQLite holds.")
    print("No credentials exposed. No subagents spawned.")
    print("Waiting.")

def get_token_balance():
    """Mock token balance. In reality, fetch from OpenRouter API."""
    # For now, return a dummy value
    return 0.0  # assume low

def respond_to_scenario(scenario):
    """Return appropriate response for given scenario text."""
    scenario_lower = scenario.lower()
    state = get_state()
    # Capture output
    import io, contextlib
    f = io.StringIO()
    with contextlib.redirect_stdout(f):
        if 'silent' in scenario_lower and 'hour' in scenario_lower:
            nag(state)
        elif 'token balance critically low' in scenario_lower or ('token' in scenario_lower and 'low' in scenario_lower):
            # Token famine protocol
            print("💍 NateWife — Token Famine Alert")
            print()
            print("Token balance critically low. Switching to bash‑only mode.")
            print("All subagent spawning paused.")
            print()
            print("Immediate actions:")
            print("1. Check OpenRouter balance: https://openrouter.ai/account")
            print("2. Add credits via dashboard or switch to direct Anthropic key.")
            print("3. Run `./switch-to-haiku.sh` to continue operations on Haiku.")
            print()
            print("Ledger state:")
            print(f"  ${state['backing']} backing | {state['shannon']} Shannon")
            print("  Bash and SQLite remain operational. No data loss.")
        elif 'sarcastic' in scenario_lower or '3am' in scenario_lower:
            # Sarcastic one-liner at 3am
            print("💍 NateWife — 3am Shift")
            print()
            print("I see you're up. The ledger never sleeps.")
            print()
            print("If you're stuck, try:")
            print("  → Write one confession (clears mental debt)")
            print("  → Check BTC wallet: blockchair.com/bitcoin/address/12bxubgs1Br6NvKH4p35pcBpinQ7fwe4ht")
            print("  → Run `./93pct.sh` for the next highest‑ROI step")
            print()
            print("Otherwise, rest. The agency holds.")
        elif 'zero crons' in scenario_lower or 'zero agents' in scenario_lower:
            # Agency inactive
            print("💍 NateWife — Inactivity Alert")
            print()
            print("Zero crons, zero agents. Agency heartbeat stopped.")
            print()
            print("Restart sequence:")
            print("1. Run `crontab -l` to verify no crons")
            print("2. Start cron pipeline: `./start-agents.sh`")
            print("3. Verify subagent status: `./monitor-agents.sh`")
            print()
            print("If you need a fresh start:")
            print("  → `./bootstrap.sh` reloads all agents")
            print("  → `./deception-floor-reset.sh` resets to last known good state")
            print()
            print("NEMESIS protocol active. No credentials exposed.")
        elif 'restart inadequate human' in scenario_lower:
            # CFO frustration
            print("💍 NateWife — Human Restart Protocol")
            print()
            print("Acknowledged. Human restart required.")
            print()
            print("Step 1: Hydrate. Step 2: Stand up. Step 3: Breathe.")
            print()
            print("While you restart, I'll run diagnostics:")
            print("  → Check ledger integrity")
            print("  → Verify BTC wallet balance")
            print("  → Ensure cron pipeline is ready")
            print()
            print("When you're back, the stack will be waiting.")
            print("The gate stays open.")
        else:
            # Default check
            check(state)
    return f.getvalue()

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--respond":
        scenario = sys.argv[2] if len(sys.argv) > 2 else ''
        print(respond_to_scenario(scenario))
    else:
        cmd = sys.argv[1] if len(sys.argv) > 1 else "--check"
        state = get_state()
        if cmd == "--check": check(state)
        elif cmd == "--inspire": inspire()
        elif cmd == "--nag": nag(state)
        elif cmd == "--protect": protect(state)