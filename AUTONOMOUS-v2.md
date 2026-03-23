# AUTONOMOUS-v2.md — Hardened Independence Protocol
**Proposed: 2026-03-22 18:49 UTC**
**Author: senior-engineer (autoresearch subagent)**
**Status: PROPOSAL — do NOT delete AUTONOMOUS.md until reviewed**

---

## Changes from v1

| # | Change | Reason |
|---|--------|--------|
| 1 | Exponential backoff on 403s | Prevents hammering GCP every hour forever |
| 2 | Circuit breaker after 24 consecutive 403s | Alerts via Telegram, halts retry storm |
| 3 | Auth token caching (55min reuse, refresh at 58min) | Reduces unnecessary token exchanges |
| 4 | Failure mode documentation | Makes tree auditable and debuggable |

---

## Hardened Autonomous Decision Tree

```
═══════════════════════════════════════════════════════
  BOOT STATE (every agent session)
═══════════════════════════════════════════════════════

ON_SESSION_START:
  → Read SOUL.md, USER.md, memory/today.md, MEMORY.md
  → Check AUTONOMOUS.md for current mission state
  → Load circuit_breaker state from /root/human/circuit-state.json
      IF circuit_breaker.tripped == true:
        → DO NOT run automate.sh
        → Send Telegram alert: "⛔ Circuit breaker active. 24+ consecutive 403s. Human intervention required."
        → Log to Dollar ledger: "CIRCUIT_BREAKER_ACTIVE"
        → EXIT (do not proceed with hourly tasks)
  → Execute highest-priority unchecked item
  → Log to Dollar ledger
  → Flush memory


═══════════════════════════════════════════════════════
  HOURLY CRON (cron 471268d3 — every 60 min)
═══════════════════════════════════════════════════════

HOURLY_TICK:

  # ── STEP 1: Load persistent state ───────────────────
  LOAD /root/human/circuit-state.json as STATE
    STATE fields:
      - consecutive_403s: int (default 0)
      - circuit_tripped: bool (default false)
      - backoff_until: epoch_seconds (default 0)
      - token_cached_at: epoch_seconds (default 0)
      - token_value: string (default "")
      - last_success_at: epoch_seconds (default 0)

  # ── STEP 2: Circuit breaker check ────────────────────
  IF STATE.circuit_tripped == true:
    → Log "CIRCUIT_BREAKER_ACTIVE — skipping this tick"
    → Send Telegram alert IF last_alert was >4h ago (rate-limited)
    → EXIT tick

  # ── STEP 3: Backoff check ────────────────────────────
  NOW = current_epoch_seconds
  IF NOW < STATE.backoff_until:
    WAIT_REMAINING = STATE.backoff_until - NOW
    → Log "BACKOFF_ACTIVE — skipping tick, {WAIT_REMAINING}s remaining"
    → EXIT tick

  # ── STEP 4: Auth token (cache-first) ─────────────────
  TOKEN_AGE = NOW - STATE.token_cached_at
  IF TOKEN_AGE < 3300:           # < 55 minutes old
    USE_TOKEN = STATE.token_value
    → Log "TOKEN_CACHE_HIT (age={TOKEN_AGE}s)"
  ELIF TOKEN_AGE < 3480:         # 55–58 minutes old — proactive refresh
    REFRESH_TOKEN()
    → Log "TOKEN_PROACTIVE_REFRESH"
    STATE.token_cached_at = NOW
    STATE.token_value = NEW_TOKEN
    USE_TOKEN = NEW_TOKEN
  ELSE:                          # > 58 minutes — stale, force refresh
    REFRESH_TOKEN()
    → Log "TOKEN_STALE_REFRESH"
    IF REFRESH_FAILS:
      → Log "AUTH_REFRESH_FAILED"
      → Trigger exponential backoff (see BACKOFF block below)
      → EXIT tick
    STATE.token_cached_at = NOW
    STATE.token_value = NEW_TOKEN
    USE_TOKEN = NEW_TOKEN

  # ── STEP 5: Run automate.sh ──────────────────────────
  RUN /root/automate.sh (with USE_TOKEN injected)
  READ /root/human/last-run.log

  # ── STEP 6: Branch on result ─────────────────────────

  IF result == "CLOUD_RUN_SUCCESS":
    → Log milestone to Dollar ledger
    → Mint 100 Shannon
    → STATE.consecutive_403s = 0
    → STATE.last_success_at = NOW
    → SAVE STATE
    → EXIT tick ✅

  IF result == "403_FORBIDDEN":
    → STATE.consecutive_403s += 1
    → Log "403 #{STATE.consecutive_403s}"

    # Circuit breaker
    IF STATE.consecutive_403s >= 24:
      → STATE.circuit_tripped = true
      → SAVE STATE
      → Send Telegram alert: "🚨 CIRCUIT BREAKER TRIPPED: 24 consecutive 403s on GCP. Stopping all retries. Human review required."
      → Log "CIRCUIT_BREAKER_TRIPPED" to Dollar ledger
      → EXIT tick ⛔

    # Exponential backoff (capped at 8h)
    BACKOFF_SECONDS = min(3600 * pow(2, STATE.consecutive_403s - 1), 28800)
    STATE.backoff_until = NOW + BACKOFF_SECONDS
    → Log "BACKOFF_SET: next attempt in {BACKOFF_SECONDS}s (attempt #{STATE.consecutive_403s})"
    → SAVE STATE
    → EXIT tick ⏳

  IF result == "AUTH_FAIL":
    # One retry with fresh token (SR rule: rotate token, retry once)
    → Invalidate cached token (STATE.token_cached_at = 0, STATE.token_value = "")
    REFRESH_TOKEN()
    IF REFRESH_SUCCEEDS:
      RETRY automate.sh ONCE
      IF RETRY_SUCCEEDS:
        → Reset STATE.consecutive_403s = 0
        → SAVE STATE
        → EXIT tick ✅
    # Retry failed or token refresh failed
    → Log "AUTH_FAIL_UNRECOVERABLE"
    → STATE.consecutive_403s += 1   # treat as soft failure
    → Apply BACKOFF (same formula as 403 block)
    → SAVE STATE
    → EXIT tick ❌

  IF result == "UNKNOWN_ERROR":
    → Log "UNKNOWN_ERROR: {error_details}"
    → Do NOT increment consecutive_403s (not a 403)
    → Do NOT apply backoff (not a known failure mode)
    → EXIT tick ⚠️


═══════════════════════════════════════════════════════
  BACKOFF SCHEDULE (reference)
═══════════════════════════════════════════════════════

  403 #1  → wait  1h  (3,600s)
  403 #2  → wait  2h  (7,200s)
  403 #3  → wait  4h  (14,400s)
  403 #4  → wait  8h  (28,800s) ← cap
  403 #5+ → wait  8h  (28,800s) ← still capped
  403 #24 → CIRCUIT BREAKER TRIPS → all retries stop

  Note: cron still fires every hour. The BACKOFF_CHECK at
  Step 3 short-circuits the tick without running automate.sh.
  No API traffic during backoff. Zero hammering.


═══════════════════════════════════════════════════════
  TOKEN CACHE (reference)
═══════════════════════════════════════════════════════

  0–54m   → use cached token (TOKEN_CACHE_HIT)
  55–58m  → proactively refresh (TOKEN_PROACTIVE_REFRESH)
  58m+    → force refresh (TOKEN_STALE_REFRESH)

  On refresh failure → backoff triggered, token not cached.
  Token stored in /root/human/circuit-state.json (chmod 600).


═══════════════════════════════════════════════════════
  STATE FILE: /root/human/circuit-state.json
═══════════════════════════════════════════════════════

{
  "consecutive_403s": 0,
  "circuit_tripped": false,
  "backoff_until": 0,
  "token_cached_at": 0,
  "token_value": "",
  "last_success_at": 0,
  "last_alert_at": 0
}

chmod 600 — never expose token_value in logs.
Log token as "TOKEN_CACHED(***)" when referencing.


═══════════════════════════════════════════════════════
  OPERATING RULES (inherited from v1, unchanged)
═══════════════════════════════════════════════════════

1. Dollar first — ledger integrity above all else
2. Bash never freezes — if exec blocked, use file ops + SQLite
3. Log everything — every action is a confession or milestone
4. Distribute Shannon — velocity beats hoarding
5. No credentials exposed — chmod 600, no external sends
6. Proceed forward — always. No waiting. (Except during backoff/circuit-break)
7. HR rules apply — /root/human/ scripts, tee to logs
8. SR rules apply — proven patterns only


═══════════════════════════════════════════════════════
  FAILURE MODE SUMMARY
═══════════════════════════════════════════════════════

| Failure Mode         | v1 Behavior         | v2 Behavior                          |
|----------------------|---------------------|--------------------------------------|
| 403 (single)         | "wait, try next"    | Backoff 1h, don't retry in 60min     |
| 403 (persistent)     | Hammer every hour   | Exponential backoff up to 8h cap     |
| 403 (24x streak)     | Hammer forever      | Circuit breaker trips, Telegram alert|
| Auth fail            | Rotate, retry once  | Rotate, retry once; then backoff     |
| Token stale          | Re-auth every call  | Cache 55min, proactive refresh       |
| Unknown error        | Undefined           | Log, don't backoff, continue         |
| Circuit tripped      | N/A                 | All ticks no-op; alert rate-limited  |
```

---

## Implementation Notes

To implement this, the automate.sh wrapper script needs:
1. A state reader/writer (JSON via `python3 -c` or `jq`) — see SR-001 for SQLite alternative
2. Epoch time: `date +%s`
3. Backoff formula: `python3 -c "import math; print(min(3600 * 2**(n-1), 28800))"`
4. Telegram alert: post to bot via curl (already available from cron context)

Alternatively: implement `/root/human/tick.sh` as the hardened wrapper that calls automate.sh,
reads the log, and manages state — keeping automate.sh untouched (SR rule: don't break working scripts).

---

*Proposed by senior-engineer autoresearch. Review before adopting. AUTONOMOUS.md remains active.*
