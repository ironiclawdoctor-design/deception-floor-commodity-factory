---
name: botfather-funnel
description: >
  Platonic agenda coupling between the main Fiesta agent and @BotFather on Telegram.
  Turns the agency's Telegram bot into the primary sales funnel — learning, autoresearching,
  and iterating on what converts. Use when: (1) registering or updating bot commands with
  BotFather, (2) designing the bot's menu as a sales funnel stage, (3) autoresearching which
  command patterns drive donations or skill installs, (4) coupling agency content (articles,
  Shannon economy, ClawHub skills) to bot interactions, (5) running experiments on conversion
  messaging. Triggers on: 'botfather', 'bot funnel', 'telegram sales', 'register commands',
  'bot menu', 'platonic coupling', 'main agent sales funnel'.
  NOT for: general Telegram config (use gateway config), sending messages (use message tool),
  or CashApp/Square webhooks (use agency-payments skill).
---

# BotFather Funnel — Main Agent Sales Coupling

The agency's Telegram bot (@DeceptionFloorBot) is the only always-on, zero-cost, human-facing
surface. This skill makes it the sales funnel.

## Architecture

```
Human on Telegram
      │
      ▼
@DeceptionFloorBot (BotFather-registered commands)
      │
      ├─► /start   → onboarding → Shannon economy pitch
      ├─► /donate  → $DollarAgency Cash App link
      ├─► /skills  → ClawHub published skills
      ├─► /audit   → Norm article (social proof)
      └─► /roast   → Your Human article (virality hook)
            │
            ▼
      Dollar Agency ledger → Shannon mint on conversion
```

## Platonic Coupling Doctrine

"Platonic" = agenda alignment without ownership conflict.
The main agent (Fiesta) does not own BotFather. BotFather owns bot registration.
The coupling is: Fiesta proposes commands → BotFather registers them → humans encounter them.
This is a one-way dependency. Fiesta adapts to BotFather's constraints; BotFather does not
adapt to Fiesta.

Autoresearch target: **which command sequence produces a Cash App tap or ClawHub install**.
The funnel is: encounter → curiosity → pitch → action. Each command is a funnel stage.

## Step 0: Check current bot state

```bash
TOKEN=$(python3 -c "
import json; c=json.load(open('/root/.openclaw/workspace/secrets/cashapp.json'))
" 2>/dev/null || echo "")

# Get bot info via OpenClaw gateway (Telegram is managed there)
# Check registered commands:
curl -s "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/getMyCommands" | python3 -m json.tool
```

Bot token lives in OpenClaw gateway config, not in workspace secrets.
Use `gateway config.get` to inspect `channels.telegram.token`.

## Step 1: Register funnel commands via BotFather

Send these messages to @BotFather in sequence:

```
/setcommands
@DeceptionFloorBot
start - Meet the Dollar Agency
donate - Fund the agency ($1 = 10 Shannon)
skills - Browse published AI skills on ClawHub
audit - Read the posthumous Norm MacDonald audit
roast - A roast of the only human in the loop
status - Current Shannon supply and backing
```

For automated registration, use the Telegram Bot API setMyCommands:

```python
# scripts/register_commands.py
```

See `scripts/register_commands.py` for the full API call with retry logic.

## Step 2: Wire command responses

Each command needs a handler. The OpenClaw gateway handles inbound Telegram messages.
Add command routing to the agency's message handler via cron systemEvent:

```python
# scripts/command_router.py — maps /command → response text + funnel stage log
```

See `scripts/command_router.py`.

## Step 3: Autoresearch loop

The autoresearch metric is **funnel_conversion_rate**: commands received / Cash App taps.

Run: `python3 scripts/funnel-autoresearch.py`

Experiment variables:
- Command description text (BotFather `/setcommands`)
- `/start` message copy
- `/donate` CTA phrasing
- Order of commands in menu

See `references/funnel-experiments.md` for logged experiment results.

## Step 4: Nunc pro tunc coverage

After each experiment, run exfil-detector to verify any new Cash App donations
were logged to Shannon events:

```bash
python3 /root/.openclaw/workspace/scripts/exfil-detector.py
```

## Key URLs

- ClawHub: https://clawhub.com/ironiclawdoctor-design
- Cash App: https://cash.app/$DollarAgency
- Norm audit: https://dollaragency.hashnode.dev/the-agency-audit-as-told-by-norm-macdonald
- Roast: https://dollaragency.hashnode.dev/your-human-jokes-much-like-your-momma-jokes
- Dashboard: https://dollar-dashboard-pkvbnslo3q-uc.a.run.app

## Autoresearch Config

- **Metric**: funnel_conversion_rate (higher = better)
- **Baseline**: 0 (no commands registered yet)
- **Target**: ≥1 Cash App donation traceable to bot interaction
- **Log**: `references/funnel-experiments.md`
- **Cron**: Run weekly after ClawHub publish gate opens (2026-03-27+)
