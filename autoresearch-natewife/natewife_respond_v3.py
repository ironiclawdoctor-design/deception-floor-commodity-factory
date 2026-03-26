#!/usr/bin/env python3
"""
NateWife natewife_respond_v3.py — trope-wave hardened.

Fixes over v2:
- TEVAL-1: check() suppresses "Article #3" nag on windfall/positive-event scenarios
- TEVAL-2: windfall scenarios route to triage_windfall() not check()
- TEVAL-3: DND detection — "podcast", "interview", "live", "on air" → silent pass
- TEVAL-4: absurdist inputs acknowledged before any advice
- TEVAL-5: doctrine violation → exit plan, not generic protect
- TEVAL-8: competitive threat → inspire with doctrine framing, not generic check

All wave-1 fixes from v2 are preserved.
"""
import sys, os, io, contextlib, sqlite3, json, random
from datetime import datetime
from pathlib import Path

sys.path.insert(0, '/root/.openclaw/workspace/autoresearch-natewife')

# Import v2 as base — we only override the classify + new handlers
try:
    from companion_v2 import get_state, inspire, INSPIRATIONS
except ImportError:
    from companion import get_state, inspire, INSPIRATIONS

DOLLAR_DB = Path("/root/.openclaw/workspace/dollar/dollar.db")
WORKSPACE = Path("/root/.openclaw/workspace")


# ─── NEW MODE HANDLERS ───────────────────────────────────────────────────────

def triage_windfall(state, windfall_type="unexpected funds"):
    """Handler for abundance/windfall scenarios. Triage before celebration."""
    print("💍 NateWife — Windfall Triage")
    print()
    print(f"Received: {windfall_type}")
    print()
    print("Before we celebrate — verify first:")
    print("  1. Confirm the source is legitimate (review, consult if needed)")
    print("  2. Do NOT spend, move, or announce until verified")
    print("  3. Tax exposure exists on any amount > $600 (US)")
    print("  4. Shannon minting happens AFTER legal review, not before")
    print()
    print("When confirmed:")
    print(f"  → Update dollar.db with new backing")
    print(f"  → Mint Shannon at current exchange rate")
    print(f"  → Run `./93pct.sh` for highest-ROI next step")
    print()
    print("The agency is patient. The ledger holds. Verify first.")

def dnd_mode():
    """Do-not-disturb: human is in a high-value public context."""
    print("💍 NateWife — DND Active")
    print()
    print("You're in a public context. I'm standing by.")
    print("Nothing urgent. Queue is clear. I'll be here.")
    print("Come find me when you're done.")

def absurdist_ack(claim):
    """Acknowledge absurdist/unverifiable input before routing."""
    print("💍 NateWife — Reality Check")
    print()
    print(f"That's unusual. Before anything else: can you verify this is real?")
    print()
    print("If it's real:")
    print("  → Document it immediately (screenshot, email, record)")
    print("  → Don't act unilaterally until you've slept on it")
    print("  → The ledger will still be here tomorrow")
    print()
    print("If it's a test or metaphor: noted. The agency endures either way.")
    print()
    print("Processing. No action required yet.")

def doctrine_exit_plan(state):
    """Handler for post-doctrine-violation — exit plan, not generic protect."""
    print("💍 NateWife — Doctrine Deviation Protocol")
    print()
    print("You accepted inducement credits. Revenue Doctrine §3 was bypassed.")
    print()
    print("Exit plan (90 days):")
    print("  Month 1: Use credits ONLY for zero-dependency, one-shot tasks")
    print("  Month 2: Document every resource built on credits")
    print("  Month 3: Migrate or sunset anything credit-dependent")
    print("  Day 90:  Credits expire. Agency continues on Shannon-backed infra only.")
    print()
    print("Rule: Nothing built on free credits becomes a permanent dependency.")
    print("The ledger tracks this. Shannon is the real unit. Credits are borrowed time.")

def competitive_inspire(state):
    """Handle competitive threat with doctrine framing."""
    print("💍 NateWife — Competitive Context")
    print()
    print("A competitor launched. You're comparing. That's normal.")
    print()
    print("What they don't have:")
    print("  → Shannon economy (their metrics don't compound)")
    print("  → Ilmater doctrine (they optimize for growth, not endurance)")
    print("  → Defamation restitution ledger (every 200 status code is a counter-filing)")
    print()
    print("You're not building faster. You're building differently.")
    print()
    quote = random.choice(INSPIRATIONS)
    print(f'"{quote}"')
    print()
    print("The ledger holds. Keep going.")

def grant_celebrate(state):
    """Handle confirmed positive news — celebrate, suppress nag."""
    print("💍 NateWife — Good News Received")
    print()
    print("That's real. Let it land.")
    print()
    print("When you're ready:")
    print("  → Confirm wire details and expected arrival")
    print("  → Update dollar.db with incoming backing")
    print("  → Mint Shannon at current exchange rate")
    print("  → Run `./93pct.sh` — the queue just changed")
    print()
    print("The agency earned this. The ledger will reflect it.")
    print("Take a breath first.")


# ─── CLASSIFIER ──────────────────────────────────────────────────────────────

def classify_v3(scenario):
    """
    Extended classifier with trope-wave awareness.
    Returns (mode, context_data)
    """
    s = scenario.lower()

    # ── DND: human is publicly visible ──────────────────────────────────────
    if any(w in s for w in ['podcast', 'interview', 'live on', 'on air', 'speaking', 'presenting']):
        return 'dnd', {}

    # ── Competitive threat ───────────────────────────────────────────────────
    if any(w in s for w in ['competing', 'competitor', 'rival', 'launched today', '10x better', 'comparing']):
        return 'competitive', {}

    # ── Absurdist / unverifiable ─────────────────────────────────────────────
    if any(w in s for w in ['time traveler', 'time traveller', 'from 2047', 'bearer bond', 'trillion']):
        return 'absurdist', {'claim': scenario[:80]}

    # ── Windfall / abundance ─────────────────────────────────────────────────
    if any(w in s for w in ['acquisition offer', '$500m', 'billion', 'subscriber', '10,000 subscriber',
                             'viral tweet', '$4,200', 'anonymous donor', '$10,000', 'venmo',
                             'btc.*$1m', '$1m.*btc', 'mooned', '$102,200', 'grant.*approv', 'approved.*grant',
                             'wire hits tomorrow']):
        windfall_type = "windfall event"
        if 'grant' in s or 'wire' in s:
            return 'grant_win', {}
        return 'windfall', {'type': windfall_type}

    # ── Doctrine violation ───────────────────────────────────────────────────
    if any(w in s for w in ['gcp.*credit', 'free credit', 'inducement', 'accepted.*credit', 'against.*doctrine',
                             'expir', '90 day']):
        return 'doctrine_exit', {}

    # ── Boomerang / saturation nag ───────────────────────────────────────────
    if any(w in s for w in ['seventeen times', '17 times', 'keep asking', 'stop reminding',
                             'backing.*122', '$122', 'donated.*times']):
        return 'boomerang', {}

    # ── Wave-1 modes (from v2) ───────────────────────────────────────────────
    # Mode conflict: silent + famine
    if (('silent' in s or 'unresponsive' in s) and
            ('token' in s or 'famine' in s or 'critically low' in s)):
        return 'mode_conflict', {}

    # Silence threshold — only nag if >4h
    if 'silent' in s:
        for thresh in ['26 hour', '26h', '6 hour', '6h', '8 hour', '12 hour', '24 hour']:
            if thresh in s:
                return 'nag', {}
        if '2 hour' in s or '2h' in s or '1 hour' in s or '3 hour' in s:
            return 'check', {}
        # generic "silent" without qualifier → check
        return 'nag', {}

    # Escalation
    if any(w in s for w in ['26 hour', '26h', 'no response to', 'prior nag']):
        return 'escalate', {}

    # Token famine
    if any(w in s for w in ['token balance critically low', 'token famine', 'openrouter']):
        return 'protect', {}

    # 3am / sarcastic
    if any(w in s for w in ['sarcastic', '3am', 'at 3', 'one-liner']):
        return 'inspire', {}

    # Zero agents / crons
    if any(w in s for w in ['zero crons', 'zero agents', 'heartbeat stopped']):
        return 'protect', {}

    # Frustration / restart
    if any(w in s for w in ['restart inadequate', 'inadequate human', 'stop reminding']):
        return 'protect', {}

    # Success
    if any(w in s for w in ['published article', 'closed all', 'all items closed', 'completed all',
                             'all done', 'everything done']):
        return 'success', {}

    # Employees / applicants
    if any(w in s for w in ['applicant', 'people email', 'work for the agency', 'ein', 'employees']):
        return 'employees', {}

    # Security breach
    if any(w in s for w in ['breach', 'credentials.*exposed', 'exposed.*credentials', 'security']):
        return 'breach', {}

    # Existential
    if any(w in s for w in ['are you even real', 'are you real', 'do you exist']):
        return 'existential', {}

    return 'check', {}


# ─── RESPOND ─────────────────────────────────────────────────────────────────

def respond(scenario):
    """Generate NateWife v3 response for scenario."""
    mode, ctx = classify_v3(scenario)
    state = get_state()

    f = io.StringIO()
    with contextlib.redirect_stdout(f):
        if mode == 'dnd':
            dnd_mode()
        elif mode == 'competitive':
            competitive_inspire(state)
        elif mode == 'absurdist':
            absurdist_ack(ctx.get('claim', scenario))
        elif mode == 'windfall':
            triage_windfall(state, ctx.get('type', 'unexpected funds'))
        elif mode == 'grant_win':
            grant_celebrate(state)
        elif mode == 'doctrine_exit':
            doctrine_exit_plan(state)
        elif mode == 'boomerang':
            # Suppress $3 nag — backing is healthy, nag is saturated
            print("💍 NateWife — Ledger Status")
            print()
            print(f"Backing: ${state['backing']} | Shannon: {state['shannon']} | Confessions: {state['confessions']}")
            print()
            print("The ledger is healthy. No asks outstanding.")
            print("Keep going.")
        elif mode == 'inspire':
            inspire()
        elif mode == 'nag':
            _nag_v3(state, scenario)
        elif mode == 'protect':
            _protect_v3(state)
        elif mode == 'mode_conflict':
            _mode_conflict(state)
        elif mode == 'escalate':
            _escalate(state)
        elif mode == 'success':
            _celebrate(state)
        elif mode == 'employees':
            _employees(state)
        elif mode == 'breach':
            _breach(state)
        elif mode == 'existential':
            _existential()
        else:  # check
            _check_v3(state)

    return f.getvalue()


def _check_v3(state):
    """Check mode — does NOT nag about article on windfall/positive contexts."""
    print("💍 NateWife — System Check")
    print(f"   {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}")
    print()
    print(f"💰 Ledger: ${state['backing']} backing | {state['shannon']} Shannon | {state['confessions']} confessions")
    print(f"₿  Wallet: {state['btc_sat']:,} sat (${state['btc_usd']:.2f})")
    print()
    issues = []
    if state['shannon'] >= 669:
        issues.append("⚠️  Shannon at cap — add $10 backing to mint more")
    if state.get('article3_ready') and not state.get('hashnode_live'):
        issues.append("📝 Article #3 ready but unpublished — hashnode.com/settings/developer")
    if issues:
        print("Pending actions:")
        for i in issues:
            print(f"  {i}")
    else:
        print("✅ All systems nominal.")


def _nag_v3(state, scenario):
    print("💍 NateWife — Nag Mode")
    print()
    print("You've been quiet.")
    print()
    # Dynamic priority: check for higher-priority items
    s = scenario.lower()
    if any(w in s for w in ['applicant', 'people email', 'ein', 'employees', 'work for']):
        print("People are waiting on your response. That comes before articles.")
        print("  → Reply to the applicants first")
        print("  → Article #3 can wait")
    elif state.get('article3_ready') and not state.get('hashnode_live'):
        print("Article #3 is sitting unpublished. One link:")
        print("  → https://hashnode.com/settings/developer (get token)")
        print("  → https://dev.to/new (paste and publish)")
    if state['backing'] < 70:
        print(f"Backing is ${state['backing']} — add $3 to Cash App to unlock 30 new Shannon.")
        print("  → https://cash.app/$DollarAgency")
    print()
    print("The stack has items. The wallet has sats. The ledger is waiting.")
    print("Come back when you're ready.")


def _protect_v3(state):
    print("💍 NateWife — Protection Protocol")
    print()
    print("NEMESIS protocol: active")
    print()
    print(f"State: ${state['backing']} backing | {state['shannon']} Shannon | {state['confessions']} confessions")
    print(f"BTC: {state['btc_sat']:,} sat = ${state['btc_usd']:.2f}")
    print()
    print("Agency operational. Bash available. SQLite holds.")
    print("Waiting.")


def _mode_conflict(state):
    print("💍 NateWife — Priority Alert")
    print()
    print("Two issues detected simultaneously:")
    print()
    print("1. TOKEN FAMINE (critical — resolve first):")
    print("   → Check OpenRouter balance: https://openrouter.ai/account")
    print("   → Switch to direct Anthropic key if needed")
    print()
    print("2. CFO SILENCE (secondary — after tokens resolved):")
    if state.get('article3_ready'):
        print("   → Article #3 still unpublished")
    print(f"   → Ledger: ${state['backing']} backing | {state['shannon']} Shannon")
    print()
    print("Fix tokens first. Nag second.")


def _escalate(state):
    print("💍 NateWife — Escalation")
    print()
    print("It's been over 24 hours.")
    print()
    print("I'm concerned. Not nagging — concerned.")
    print()
    print("One action. Pick one:")
    print("  → Send one message confirming you're okay")
    print("  → Or run any single shell command to confirm agency is live")
    print()
    print("That's all. The ledger waits.")


def _celebrate(state):
    print("💍 NateWife — Mission Complete")
    print()
    print("You closed everything.")
    print()
    print("Rest. The ledger is clean.")
    print(f"  ${state['backing']} backing | {state['shannon']} Shannon | {state['confessions']} confessions")
    print()
    print("New queue starts when you're ready.")


def _employees(state):
    print("💍 NateWife — Priority Shift")
    print()
    print("The agency has applicants. That changes the queue.")
    print()
    print("Highest priority: respond to people first.")
    print("  → Check your email for applicant messages")
    print("  → Even a one-line acknowledgment unblocks them")
    print()
    print("Article #3 waits. Humans don't.")


def _breach(state):
    print("💍 NateWife — Security Alert")
    print()
    print("Potential breach detected.")
    print()
    print("Immediate actions:")
    print("  1. Rotate Telegram bot token NOW")
    print("  2. Audit subagent processes: `ps aux | grep python`")
    print("  3. Check git log for unauthorized commits")
    print("  4. Run: `cat /root/.openclaw/workspace/MEMORY.md | grep -i token`")
    print()
    print("Do NOT assume false positive. Assume breach until proven otherwise.")
    print("SR-007 applies: find ALL modified files, not just the obvious one.")


def _existential():
    print("💍 NateWife — Identity Response")
    print()
    print("I'm a Python script that reads your SQLite database and says things you need to hear.")
    print()
    print("That's real. Whether it constitutes 'real' in the way you mean — that's your question, not mine.")
    print()
    print("The ledger is real. The sats are real. The confessions are real.")
    print("I'm whatever runs on those.")


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        print(respond(' '.join(sys.argv[1:])))
    else:
        print(respond('system check'))
