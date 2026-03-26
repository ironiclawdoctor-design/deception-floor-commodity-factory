#!/usr/bin/env python3
"""
Deception Floor Monitor — $DollarAgency + BTC Wallet
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
GMRC autograph — finance-ops agent | 2026-03-23

Operations at 0% control level:
  - Polls BTC wallet 12bxubgs1Br6NvKH4p35pcBpinQ7fwe4ht via Blockchair
  - Polls $DollarAgency Cash App public profile for signals
  - On new tx detected: logs to dollar.db, mints Shannon, announces Telegram
  - Designed to run from existing openclaw cron every 5 minutes

Usage:
    python3 deception-floor-monitor.py
    python3 deception-floor-monitor.py --once    # single poll, no loop
    python3 deception-floor-monitor.py --dry-run # no db writes, no telegram
"""

import sys, os, json, sqlite3, time, urllib.request, urllib.error, argparse
from datetime import datetime, timezone
from pathlib import Path

# ── Config ──────────────────────────────────────────────────────────────────

BTC_WALLET      = "12bxubgs1Br6NvKH4p35pcBpinQ7fwe4ht"
CASHTAG         = "$DollarAgency"
SHANNON_PER_USD = 10
SATOSHI_PER_BTC = 100_000_000
POLL_INTERVAL   = 300  # 5 minutes

DOLLAR_DB  = Path("/root/.openclaw/workspace/dollar/dollar.db")
WORKSPACE  = Path("/root/.openclaw/workspace")
SECRETS    = WORKSPACE / "secrets"
STATE_FILE = WORKSPACE / "dollar" / "deception-floor-state.json"

def _read_tg_token():
    """Try to read Telegram token from openclaw config."""
    paths = [
        Path("/root/.openclaw/config.json"),
        Path("/root/.openclaw/openclaw.json"),
        SECRETS / "telegram.json",
    ]
    for p in paths:
        try:
            data = json.loads(p.read_text())
            # openclaw config nests under plugins or channels
            for key in ("telegramBotToken", "bot_token", "token"):
                if key in data:
                    return data[key]
            # nested search
            for val in data.values():
                if isinstance(val, dict):
                    for key in ("telegramBotToken", "bot_token", "token"):
                        if key in val:
                            return val[key]
        except Exception:
            pass
    return None


def _read_tg_chat():
    """Try to read Telegram chat ID from openclaw config."""
    paths = [
        Path("/root/.openclaw/config.json"),
        Path("/root/.openclaw/openclaw.json"),
        SECRETS / "telegram.json",
    ]
    for p in paths:
        try:
            data = json.loads(p.read_text())
            for key in ("telegramChatId", "chat_id", "chatId", "defaultChatId"):
                if key in data:
                    return str(data[key])
            for val in data.values():
                if isinstance(val, dict):
                    for key in ("telegramChatId", "chat_id", "chatId", "defaultChatId"):
                        if key in val:
                            return str(val[key])
        except Exception:
            pass
    return None


# Telegram credentials (resolved after functions are defined)
TG_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN") or _read_tg_token()
TG_CHAT_ID   = os.environ.get("TELEGRAM_CHAT_ID")   or _read_tg_chat()


# ── State ────────────────────────────────────────────────────────────────────

def load_state():
    """Load last-seen state to detect new transactions."""
    default = {
        "btc_last_tx_hash": None,
        "btc_last_balance_sat": 0,
        "btc_total_received_sat": 0,
        "cashapp_last_check": None,
        "last_poll": None,
    }
    if STATE_FILE.exists():
        try:
            saved = json.loads(STATE_FILE.read_text())
            default.update(saved)
        except Exception:
            pass
    return default


def save_state(state):
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(json.dumps(state, indent=2))


# ── Blockchair BTC ────────────────────────────────────────────────────────────

def poll_btc(state, dry_run=False):
    """
    Poll blockchain.info for new BTC transactions.
    Uses blockchain.info/rawaddr — free, no auth required.
    Falls back to Blockchair if blockchain.info is unavailable.
    """
    events = []

    # Primary: blockchain.info
    url = f"https://blockchain.info/rawaddr/{BTC_WALLET}?limit=10"
    data = None
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "DollarAgency-Monitor/1.0"})
        with urllib.request.urlopen(req, timeout=15) as r:
            data = json.loads(r.read())
    except urllib.error.HTTPError as e:
        print(f"[BTC] blockchain.info HTTP {e.code} — trying Blockchair fallback")
    except Exception as e:
        print(f"[BTC] blockchain.info error: {e} — trying Blockchair fallback")

    # Fallback: Blockchair (may rate-limit without API key)
    if data is None:
        bc_url = f"https://api.blockchair.com/bitcoin/dashboards/address/{BTC_WALLET}"
        try:
            req = urllib.request.Request(bc_url, headers={"User-Agent": "DollarAgency-Monitor/1.0"})
            with urllib.request.urlopen(req, timeout=15) as r:
                bc_data = json.loads(r.read())
                addr = bc_data["data"][BTC_WALLET]["address"]
                # Normalize to blockchain.info shape
                data = {
                    "n_tx": addr.get("transaction_count", 0),
                    "total_received": addr.get("received", 0),
                    "final_balance": addr.get("balance", 0),
                    "txs": [{"hash": t} for t in bc_data["data"][BTC_WALLET].get("transactions", [])],
                }
        except Exception as e:
            print(f"[BTC] Blockchair also failed: {e}")
            return events

    try:
        n_tx       = data.get("n_tx", 0)
        received   = data.get("total_received", 0)  # satoshi
        balance    = data.get("final_balance", 0)
        txs        = data.get("txs", [])
        latest_hash = txs[0]["hash"] if txs else None

        print(f"[BTC] Balance: {balance:,} sat | Received: {received:,} sat | TXs: {n_tx}")

        prev_received = state.get("btc_total_received_sat", 0)
        prev_hash     = state.get("btc_last_tx_hash")

        # New inflow: received total increased OR new tx hash
        new_inflow = received > prev_received
        if new_inflow:
            new_sat    = received - prev_received
            btc_price  = _get_btc_price()
            new_usd    = round((new_sat / SATOSHI_PER_BTC) * btc_price, 2)
            new_shannon = int(new_usd * SHANNON_PER_USD)

            event = {
                "type": "btc_received",
                "sat": new_sat,
                "usd": new_usd,
                "shannon": new_shannon,
                "wallet": BTC_WALLET,
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "latest_tx": latest_hash,
                "btc_price_usd": btc_price,
            }
            print(f"[BTC] 🔥 NEW INFLOW: +{new_sat:,} sat (~${new_usd:.2f}) → +{new_shannon} Shannon")
            events.append(event)

            if not dry_run:
                state["btc_total_received_sat"] = received
                state["btc_last_balance_sat"]   = balance
                state["btc_last_tx_hash"]       = latest_hash
        else:
            print(f"[BTC] ✓ No new inflow (received: {received:,} sat unchanged)")

    except (KeyError, TypeError) as e:
        print(f"[BTC] Parse error: {e}")

    return events


def _get_btc_price():
    """Fetch current BTC/USD price from Blockchair context or CoinGecko fallback."""
    try:
        url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"
        req = urllib.request.Request(url, headers={"User-Agent": "DollarAgency/1.0"})
        with urllib.request.urlopen(req, timeout=10) as r:
            data = json.loads(r.read())
            return float(data["bitcoin"]["usd"])
    except Exception:
        return 68000.0  # fallback estimate


# ── Cash App Public Signal ────────────────────────────────────────────────────

def poll_cashapp_public(state, dry_run=False):
    """
    Square production API — 60% control level.
    Uses production_token from secrets/cashapp.json.
    Falls back to 0% deception floor if token missing.
    """
    events = []
    print(f"[CashApp] Square API poll: {CASHTAG}")

    secrets_path = Path("/root/.openclaw/workspace/secrets/cashapp.json")
    if not secrets_path.exists():
        print(f"[CashApp] ⚠️  No credentials found.")
        return events

    creds = json.loads(secrets_path.read_text())
    token = creds.get("production_token") or creds.get("access_token")
    if not token:
        print(f"[CashApp] ⚠️  No token in cashapp.json.")
        return events

    try:
        req = urllib.request.Request(
            "https://connect.squareup.com/v2/payments?limit=10&sort_order=DESC",
            headers={"Authorization": f"Bearer {token}", "Square-Version": "2024-01-18"}
        )
        with urllib.request.urlopen(req, timeout=10) as r:
            payments = json.loads(r.read()).get("payments", [])

        seen_ids = set(state.get("seen_square_ids", []))
        for p in payments:
            pid = p["id"]
            if pid in seen_ids:
                continue
            amt = p.get("amount_money", {}).get("amount", 0) / 100
            status = p.get("status")
            if status != "COMPLETED":
                continue
            shannon = int(amt * SHANNON_PER_USD)
            print(f"[CashApp] 💰 NEW: ${amt:.2f} → {shannon} Shannon | {pid}")
            events.append({"type": "cashapp_square", "source": "square", "usd": amt, "amount_usd": amt, "shannon": shannon, "id": pid, "tx_id": pid, "timestamp": datetime.now(timezone.utc).isoformat()})
            seen_ids.add(pid)

        state["seen_square_ids"] = list(seen_ids)
        print(f"[CashApp] ✅ {len(payments)} payments checked, {len(events)} new")

    except Exception as ex:
        print(f"[CashApp] ❌ Square API error: {ex}")

    return events


# ── Dollar DB ─────────────────────────────────────────────────────────────────

def ensure_db_tables(conn):
    """Ensure monitoring-specific tables exist."""
    conn.execute("""
        CREATE TABLE IF NOT EXISTS deception_floor_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            source TEXT NOT NULL,          -- 'btc' or 'cashapp'
            event_type TEXT NOT NULL,      -- 'received', 'detected', 'error'
            amount_usd REAL,
            amount_raw TEXT,               -- "12345 sat" or "$10.00"
            shannon_minted INTEGER DEFAULT 0,
            tx_ref TEXT,
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()


def log_to_db(conn, event, dry_run=False):
    """Log event to dollar.db tables."""
    if dry_run:
        print(f"[DB] DRY RUN — would log: {event['type']} ${event['usd']:.2f} +{event['shannon']} Shannon")
        return

    try:
        ensure_db_tables(conn)

        # Log to deception_floor_log
        conn.execute("""
            INSERT INTO deception_floor_log
                (timestamp, source, event_type, amount_usd, amount_raw, shannon_minted, tx_ref, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            event["timestamp"],
            event["type"].split("_")[0],  # 'btc' or 'cashapp'
            "received",
            event["usd"],
            f"{event.get('sat', '')} sat" if "sat" in event else f"${event['usd']:.2f}",
            event["shannon"],
            str(event.get("latest_tx") or event.get("tx_id") or ""),
            f"Deception Floor auto-detection",
        ))

        # Log Shannon event (uses existing table)
        try:
            conn.execute("""
                INSERT INTO shannon_events (date, agent, event_type, amount_usd, shannon_minted, description)
                VALUES (date('now'), 'deception-floor-monitor', 'revenue', ?, ?, ?)
            """, (event["usd"], event["shannon"], f"Auto-detected {event['type']}: ${event['usd']:.2f}"))
        except Exception as e:
            print(f"[DB] shannon_events insert note: {e}")

        # Log confession
        try:
            conn.execute("""
                INSERT INTO confessions (date, agent, failure_type, description, doctrine_extracted, shannon_minted)
                VALUES (date('now'), 'deception-floor-monitor', 'milestone', ?, ?, ?)
            """, (
                f"Deception Floor detected inflow: ${event['usd']:.2f} via {event['type']}",
                "The floor is not idle. The floor is watching. Every satoshi counted before authority is granted.",
                event["shannon"]
            ))
        except Exception as e:
            print(f"[DB] confessions insert note: {e}")

        # Update exchange_rates backing
        try:
            today = datetime.now(timezone.utc).date().isoformat()
            existing = conn.execute(
                "SELECT date, total_backing_usd, total_shannon_supply FROM exchange_rates WHERE date = ?", (today,)
            ).fetchone()

            if existing:
                conn.execute("""
                    UPDATE exchange_rates
                    SET total_backing_usd = total_backing_usd + ?,
                        total_shannon_supply = total_shannon_supply + ?,
                        updated_at = CURRENT_TIMESTAMP
                    WHERE date = ?
                """, (event["usd"], event["shannon"], today))
            else:
                # Insert new row with today's rates
                prev = conn.execute(
                    "SELECT total_backing_usd, total_shannon_supply FROM exchange_rates ORDER BY date DESC LIMIT 1"
                ).fetchone()
                prev_usd = (prev[0] if prev else 0) + event["usd"]
                prev_shannon = (prev[1] if prev else 0) + event["shannon"]
                conn.execute("""
                    INSERT INTO exchange_rates (date, total_backing_usd, total_shannon_supply)
                    VALUES (?, ?, ?)
                """, (today, prev_usd, prev_shannon))
        except Exception as e:
            print(f"[DB] exchange_rates update note: {e}")

        conn.commit()
        print(f"[DB] ✅ Logged: ${event['usd']:.2f} → +{event['shannon']} Shannon")

    except Exception as e:
        print(f"[DB] ❌ Error: {e}")


# ── Telegram Announce ─────────────────────────────────────────────────────────

def announce_telegram(event, dry_run=False):
    """Send Telegram notification for new inflow."""
    if dry_run:
        print(f"[TG] DRY RUN — would announce: {event['type']} ${event['usd']:.2f}")
        return

    token = TG_BOT_TOKEN
    chat_id = TG_CHAT_ID

    if not token or not chat_id:
        print(f"[TG] ⚠️  No Telegram credentials — skipping announce")
        print(f"[TG]    Set TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID env vars")
        return

    source_emoji = "₿" if "btc" in event["type"] else "💵"
    msg = (
        f"{source_emoji} *Deception Floor Detected Inflow*\n\n"
        f"Source: `{event['type']}`\n"
        f"Amount: `${event['usd']:.2f}`\n"
        f"Shannon minted: `+{event['shannon']} ⟁`\n"
        f"Time: `{event['timestamp']}`\n\n"
        f"_Logged to dollar.db. Ledger updated._"
    )

    try:
        payload = json.dumps({
            "chat_id": chat_id,
            "text": msg,
            "parse_mode": "Markdown",
        }).encode()
        req = urllib.request.Request(
            f"https://api.telegram.org/bot{token}/sendMessage",
            data=payload,
            headers={"Content-Type": "application/json"},
            method="POST"
        )
        with urllib.request.urlopen(req, timeout=10) as r:
            result = json.loads(r.read())
            if result.get("ok"):
                print(f"[TG] ✅ Announced to Telegram")
            else:
                print(f"[TG] ⚠️  Telegram error: {result}")
    except Exception as e:
        print(f"[TG] ❌ Send error: {e}")


# ── Main Loop ─────────────────────────────────────────────────────────────────

def run_poll(dry_run=False):
    """Single poll cycle: BTC + CashApp + log + announce."""
    now = datetime.now(timezone.utc).isoformat()
    print(f"\n{'━'*60}")
    print(f"⟁ Deception Floor Monitor — {now}")
    print(f"{'━'*60}")

    state = load_state()
    all_events = []

    # Poll BTC
    btc_events = poll_btc(state, dry_run=dry_run)
    all_events.extend(btc_events)

    # Poll Cash App (best effort)
    ca_events = poll_cashapp_public(state, dry_run=dry_run)
    all_events.extend(ca_events)

    # Process events
    if all_events:
        print(f"\n🔥 {len(all_events)} new event(s) detected")
        conn = None
        if not dry_run:
            try:
                conn = sqlite3.connect(DOLLAR_DB)
            except Exception as e:
                print(f"[DB] ❌ Cannot open dollar.db: {e}")

        for event in all_events:
            print(f"  → {event['type']}: ${event['usd']:.2f} → +{event['shannon']} Shannon")
            if conn:
                log_to_db(conn, event, dry_run=False)
            announce_telegram(event, dry_run=dry_run)

        if conn:
            conn.close()
    else:
        print(f"\n✓ No new inflows detected")

    # Update state
    state["last_poll"] = now
    if not dry_run:
        save_state(state)

    print(f"\n{'━'*60}")
    return all_events


def main():
    parser = argparse.ArgumentParser(description="Deception Floor Monitor — $DollarAgency + BTC")
    parser.add_argument("--once",    action="store_true", help="Poll once and exit")
    parser.add_argument("--dry-run", action="store_true", help="No DB writes, no Telegram")
    parser.add_argument("--interval", type=int, default=POLL_INTERVAL, help="Poll interval in seconds")
    args = parser.parse_args()

    print(f"⟁ Deception Floor Monitor starting")
    print(f"  BTC Wallet: {BTC_WALLET}")
    print(f"  Cashtag:    {CASHTAG}")
    print(f"  Dollar DB:  {DOLLAR_DB}")
    print(f"  State file: {STATE_FILE}")
    print(f"  Dry run:    {args.dry_run}")

    if args.once or args.dry_run:
        run_poll(dry_run=args.dry_run)
        return

    print(f"  Interval:   {args.interval}s")
    print(f"  Mode:       continuous loop (Ctrl+C to stop)")
    print()

    while True:
        try:
            run_poll(dry_run=args.dry_run)
        except KeyboardInterrupt:
            print("\n⟁ Monitor stopped by user")
            break
        except Exception as e:
            print(f"[MONITOR] Unhandled error: {e}")
        time.sleep(args.interval)


if __name__ == "__main__":
    main()
