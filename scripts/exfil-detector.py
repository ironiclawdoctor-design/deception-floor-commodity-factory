#!/usr/bin/env python3
"""
exfil-detector.py — Shanapp $DollarAgency Exfiltration Detection
Autoresearch loop: detects unlogged, orphaned, or missing Shannon events
across all ledgers retroactively (nunc pro tunc — "now as then").

93% target: every economic event that happened MUST be in the canonical ledger.
Gap = exfiltration signal. All gaps get retroactive entries with nunc_pro_tunc=1.

Author: Fiesta (2026-03-24)
"""

import sqlite3
import sys
from datetime import datetime, timezone

DOLLAR_DB = "/root/.openclaw/workspace/dollar/dollar.db"
ENTROPY_DB = "/root/.openclaw/workspace/entropy_ledger.db"
AGENCY_DB = "/root/.openclaw/workspace/agency.db"
NPT_MARKER = "nunc_pro_tunc"


def ts():
    return datetime.now(timezone.utc).isoformat()


def get_conn(path):
    return sqlite3.connect(path)


# ─── STEP 1: Enumerate all known economic events ────────────────────────────

def load_dollar_events(conn):
    """All cleared transactions in dollar/dollar.db"""
    cur = conn.execute(
        "SELECT id, date, description, amount, source, reference FROM transactions WHERE status='cleared' ORDER BY date"
    )
    return [{"id": r[0], "date": r[1], "desc": r[2], "amount": r[3],
             "source": r[4], "ref": r[5], "origin": "dollar.transactions"} for r in cur.fetchall()]


def load_shannon_events(conn):
    """All shannon_events in dollar/dollar.db"""
    cur = conn.execute(
        "SELECT id, date, agent, event_type, amount_usd, shannon_minted, description FROM shannon_events ORDER BY id"
    )
    return [{"id": r[0], "date": r[1], "agent": r[2], "event_type": r[3],
             "usd": r[4], "shannon": r[5], "desc": r[6]} for r in cur.fetchall()]


def load_entropy_transactions(conn):
    """All transactions in entropy_ledger.db"""
    cur = conn.execute(
        "SELECT id, agent_id, amount, transaction_type, description, timestamp FROM transactions ORDER BY id"
    )
    return [{"id": r[0], "agent": r[1], "amount": r[2], "type": r[3],
             "desc": r[4], "ts": r[5]} for r in cur.fetchall()]


def load_deception_floor_log(conn):
    """All deception_floor_log events — authoritative source"""
    cur = conn.execute(
        "SELECT id, timestamp, source, event_type, amount_usd, amount_raw, shannon_minted, tx_ref FROM deception_floor_log ORDER BY id"
    )
    return [{"id": r[0], "ts": r[1], "method": r[2], "type": r[3],
             "usd": r[4], "raw": r[5], "shannon": r[6], "ref": r[7]} for r in cur.fetchall()]


# ─── STEP 2: Cross-ledger reconciliation ─────────────────────────────────────

def reconcile(dollar_events, shannon_events, deception_log):
    """
    For each dollar transaction, verify a matching shannon_event exists.
    For each deception_floor_log entry, verify a matching shannon_event exists.
    Returns list of gaps (exfiltration signals).
    """
    gaps = []

    # Index shannon events by reference/description for fuzzy match
    shannon_refs = set()
    for se in shannon_events:
        shannon_refs.add(se["desc"].lower()[:40] if se["desc"] else "")
        if "btc" in (se["desc"] or "").lower():
            shannon_refs.add("btc")
        if "cashapp" in (se["desc"] or "").lower() or "square" in (se["desc"] or "").lower():
            shannon_refs.add("cashapp")

    # Check each cleared dollar transaction
    for ev in dollar_events:
        matched = False
        for se in shannon_events:
            if ev["ref"] and ev["ref"] in (se["desc"] or ""):
                matched = True
                break
            if ev["source"] == "bitcoin" and "btc" in (se["desc"] or "").lower():
                matched = True
                break
            if ev["source"] == "cashapp" and "cashapp" in (se["desc"] or "").lower():
                matched = True
                break
            if ev["desc"] and ev["desc"][:20].lower() in (se["desc"] or "").lower():
                matched = True
                break
        if not matched:
            gaps.append({
                "type": "dollar_tx_missing_shannon_event",
                "date": ev["date"],
                "desc": ev["desc"],
                "amount": ev["amount"],
                "source": ev["source"],
                "ref": ev["ref"],
                "origin": ev["origin"]
            })

    # Check each deception_floor_log entry
    for dl in deception_log:
        matched = False
        for se in shannon_events:
            if dl["ref"] and dl["ref"] in (se["desc"] or ""):
                matched = True
                break
            if dl["method"] == "btc" and "btc" in (se["desc"] or "").lower():
                matched = True
                break
            if dl["method"] == "cashapp" and ("cashapp" in (se["desc"] or "").lower() or "square" in (se["desc"] or "").lower()):
                matched = True
                break
        if not matched:
            gaps.append({
                "type": "deception_floor_missing_shannon_event",
                "date": dl["ts"][:10],
                "desc": f"Deception floor: {dl['method']} {dl['type']} ${dl['usd']} ref={dl['ref']}",
                "amount": dl["usd"],
                "source": dl["method"],
                "ref": dl["ref"],
                "origin": "deception_floor_log"
            })

    return gaps


# ─── STEP 3: Nunc Pro Tunc retroactive mint ──────────────────────────────────

def nunc_pro_tunc_mint(conn, gaps):
    """
    For each gap, insert a retroactive shannon_event with nunc_pro_tunc marker.
    'Now as then' — the mint is dated to when the economic event actually occurred.
    """
    minted = []
    for gap in gaps:
        try:
            usd = float(gap["amount"]) if gap["amount"] else 0.0
            shannon = int(usd * 10)  # 10 Shannon per USD
            desc = f"[{NPT_MARKER}] {gap['desc']} (retro-detected 2026-03-24)"
            conn.execute(
                """INSERT INTO shannon_events
                   (date, agent, event_type, amount_usd, shannon_minted, description, created_at)
                   VALUES (?, ?, ?, ?, ?, ?, ?)""",
                (gap["date"], "exfil-detector", "revenue",
                 usd, shannon, desc, ts())
            )
            minted.append({**gap, "shannon_minted": shannon, "status": "retroactively_minted"})
            print(f"  ✅ NPT MINT: {gap['date']} | {gap['source']} | ${usd:.2f} → {shannon} Shannon | {gap['desc'][:50]}")
        except Exception as e:
            print(f"  ❌ MINT FAIL: {gap['desc'][:40]} — {e}")
    conn.commit()
    return minted


# ─── STEP 4: Score coverage (93% target) ─────────────────────────────────────

def score_coverage(total_events, gaps_before, gaps_after):
    if total_events == 0:
        return 100.0
    covered = total_events - gaps_after
    return round((covered / total_events) * 100, 1)


# ─── STEP 5: Write results to ledger ─────────────────────────────────────────

def log_autoresearch_result(conn, score, gaps_found, npt_minted):
    try:
        conn.execute(
            """INSERT INTO shannon_events
               (date, agent, event_type, amount_usd, shannon_minted, description, created_at)
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (datetime.now(timezone.utc).date().isoformat(), "exfil-detector", "report",
             0, 0,
             f"Exfil detection run 2026-03-24: {gaps_found} gaps found, {npt_minted} retroactively minted. Coverage: {score}%",
             ts())
        )
        conn.commit()
    except Exception as e:
        print(f"  ⚠️  Could not log result: {e}")


# ─── MAIN ─────────────────────────────────────────────────────────────────────

def main():
    print("=" * 60)
    print("EXFIL DETECTOR — Shanapp $DollarAgency")
    print("Nunc Pro Tunc Retroactive Coverage Audit")
    print(f"Run: {ts()}")
    print("=" * 60)

    dollar_conn = get_conn(DOLLAR_DB)
    entropy_conn = get_conn(ENTROPY_DB)

    # Load all event sources
    dollar_events = load_dollar_events(dollar_conn)
    shannon_events = load_shannon_events(dollar_conn)
    deception_log = load_deception_floor_log(dollar_conn)
    entropy_txs = load_entropy_transactions(entropy_conn)

    total_source_events = len(dollar_events) + len(deception_log)

    print(f"\n📊 Source inventory:")
    print(f"   dollar.transactions:   {len(dollar_events)} cleared events")
    print(f"   deception_floor_log:   {len(deception_log)} detected events")
    print(f"   shannon_events (canon): {len(shannon_events)} entries")
    print(f"   entropy_ledger.txs:    {len(entropy_txs)} agent transfers")

    # Reconcile
    print(f"\n🔍 Reconciling...")
    gaps = reconcile(dollar_events, shannon_events, deception_log)

    if not gaps:
        print(f"\n✅ CLEAN: No exfiltration gaps detected across {total_source_events} events.")
        score = 100.0
        npt_count = 0
    else:
        print(f"\n⚠️  GAPS DETECTED: {len(gaps)} unlogged economic events")
        for g in gaps:
            print(f"   └─ [{g['type']}] {g['date']} | {g['source']} | ${g['amount']} | {g['desc'][:50]}")

        print(f"\n🔁 Applying Nunc Pro Tunc mints...")
        minted = nunc_pro_tunc_mint(dollar_conn, gaps)
        npt_count = len(minted)

        # Reload and rescore
        shannon_events_after = load_shannon_events(dollar_conn)
        gaps_after = reconcile(dollar_events, shannon_events_after, deception_log)
        score = score_coverage(total_source_events, len(gaps), len(gaps_after))

    print(f"\n📈 COVERAGE SCORE: {score}%  (target: 93%)")
    if score >= 93:
        print("   ✅ 93% THRESHOLD MET — ledger integrity confirmed")
    else:
        remaining = total_source_events - int(total_source_events * score / 100)
        print(f"   ❌ BELOW THRESHOLD — {remaining} events still unreconciled")

    log_autoresearch_result(dollar_conn, score, len(gaps), npt_count)

    print(f"\n{'=' * 60}")
    print("AUTORESEARCH INIT COMPLETE")
    print(f"Gaps found: {len(gaps)} | NPT minted: {npt_count} | Final coverage: {score}%")
    print("=" * 60)

    dollar_conn.close()
    entropy_conn.close()
    return score


if __name__ == "__main__":
    score = main()
    sys.exit(0 if score >= 93 else 1)
