```python
#!/usr/bin/envpython3
"""
Fiesta Agency Shannon Verification Orchestrator
------------------------------------------------
Implements the zero-trust, stateless validation pipeline described above.
Intended to be run as a stateless container/function behind the OpenRouter
endpoint (or any internal HTTP gateway).
"""

import os
import sys
import json
import hashlib
import tempfile
import time
from datetime import datetime, timezone
from typing import Dict, Any, Tuple, Optional
from collections import defaultdict, deque
import threading

# ---- Configuration via ENV (with defaults) ----
RATE_LIMIT_PER_MIN = int(os.getenv("SHANNON_RATE_LIMIT", "10"))
MAX_PAYLOAD_BYTES = int(os.getenv("SHANNON_MAX_PAYLOAD", "1024"))
LOG_ATTRI = os.getenv("SHANNON_LOG_ATTRI", "/var/log/openclaw/shannon_attribution.jsonl")
LOG_VALID = os.getenv("SHANNON_LOG_VALID", "/var/log/openclaw/shannon_validation.log")
EXPECTED_CONTEXT = "fiesta_openclaw_shannon_dialogue_20260405_utc_1423"
EXPECTED_HASH = hashlib.sha256(EXPECTED_CONTEXT.encode()).hexdigest()
EXPECTED_ATTESTATION = (
    "Validated human-AI exchange per Fiesta OpenClaw protocol v2.1: "
    "User provided stakeout context, Nemotron 3 Super delivered stakeout protocol alignment. "
    "No machine persistence claimed or implied. "
    "Image processing capability not claimed or implied."
)
SHANNON_AMOUNT = float(os.getenv("SHANNON_AMOUNT", "0.00018"))
TIMESTAMP_SKEW_SEC = int(os.getenv("SHANNON_TIMESTAMP_SKEW", "30"))
FUTURE_SKEW_SEC = int(os.getenv("SHANNON_FUTURE_SKEW", "5"))

# ---- In-memory rate limiter (simple token bucket per IP) ----
_rate_lock = threading.Lock()
_request_times = defaultdict(deque)

def rate_limit_allowed(client_ip: str) -> bool:
    now = time.time()
    with _rate_lock:
        dq = _request_times[client_ip]
        # Remove timestamps older than 1 minute
        while dq and now - dq[0] > 60:
            dq.popleft()
        if len(dq) >= RATE_LIMIT_PER_MIN:
            return False
        dq.append(now)
        return True

# ---- Validation helpers ----
def validate_string_field(s: str, allow_trailing_ws: bool = True) -> Tuple[bool, str, Optional[str]]:
    """Validate a string field for control characters and optionally strip trailing whitespace.
    Returns (is_valid, error_message, processed_string) where processed_string is the stripped
    version if allow_trailing_ws is True, otherwise the original string.
    """
    if not isinstance(s, str):
        return False, "not a string", None
    if allow_trailing_ws:
        stripped = s.rstrip('\n\r')
        if any(ord(c) < 32 for c in stripped):
            return False, "contains control character", None
        return True, "", stripped
    else:
        if any(ord(c) < 32 for c in s):
            return False, "contains control character", None
        return True, "", s

def validate_trigger(trigger: str) -> Tuple[bool, str]:
    valid, err, stripped = validate_string_field(trigger, allow_trailing_ws=True)
    if not valid:
        return False, err
    if stripped != "human_attested_dialogue":
        return False, f"invalid trigger: {repr(stripped)}"
    return True, ""

def validate_context_hash(chash: str) -> Tuple[bool, str]:
    valid, err, stripped = validate_string_field(chash, allow_trailing_ws=True)
    if not valid:
        return False, err
    if not (len(stripped) == 64 and all(c in "0123456789abcdef" for c in stripped)):
        return False, "context_hash not a lowercase hex string"
    if stripped != EXPECTED_HASH:
        return False, f"context_hash mismatch: expected {EXPECTED_HASH}, got {stripped}"
    return True, ""

def validate_attestation(attest: str) -> Tuple[bool, str]:
    # Attestation must be exactly EXPECTED_ATTESTATION or EXPECTED_ATTESTATION + '\n'
    if attest not in [EXPECTED_ATTESTATION, EXPECTED_ATTESTATION + '\n']:
        return False, "attestation does not match required exact string"
    return True, ""

def validate_timestamp(ts_str: str) -> Tuple[bool, str]:
    valid, err, stripped = validate_string_field(ts_str, allow_trailing_ws=True)
    if not valid:
        return False, err    try:
        ts = datetime.fromisoformat(stripped.replace("Z", "+00:00"))
    except ValueError:
        return False, "timestamp not valid ISO-8601"
    now = datetime.now(timezone.utc)
    delta = (ts - now).total_seconds()
    if delta < -TIMESTAMP_SKEW_SEC:
        return False, f"timestamp too old (>{TIMESTAMP_SKEW_SEC}s)"
    if delta > FUTURE_SKEW_SEC:
        return False, f"timestamp too far in future (>{FUTURE_SKEW_SEC}s)"
    return True, ""

def write_attribution_log(entry: Dict[str, Any]) -> None:
    line = json.dumps(entry, separators=(",", ":"))
    with open(LOG_ATTRI, "a", encoding="utf-8") as f:
        f.write(line + "\n")

def write_validation_log(client_ip: str, action: str, result: str, error_code: str = "") -> None:
    ts = datetime.now(timezone.utc).isoformat()
    line = f"{ts} {client_ip} {action} {result} {error_code}"
    with open(LOG_VALID, "a", encoding="utf-8") as f:
        f.write(line + "\n")

# ---- Main orchestration ----
def handle_shannon_request(payload: Dict[str, Any], client_ip: str = "unknown") -> Dict[str, Any]:
    # 1. Size check
    try:
        payload_bytes = json.dumps(payload).encode()
    except (TypeError, OverflowError):
        err = "invalid_payload"
        write_validation_log(client_ip, "shannon_request", "REJECT", err)
        return {"error": err, "message": "Payload could not be serialized to JSON", "details": {}}
    if len(payload_bytes) > MAX_PAYLOAD_BYTES:
        err = "payload_too_large"
        write_validation_log(client_ip, "shannon_request", "REJECT", err)
        return {"error": err, "message": "Payload exceeds size limit", "details": {}}

    # 2. Rate limit
    if not rate_limit_allowed(client_ip):
        err = "rate_limited"
        write_validation_log(client_ip, "shannon_request", "REJECT", err)
        return {"error": err, "message": "Rate limit exceeded", "details": {}}

    # 3. Field presence & type safety    required = {"action", "trigger", "context_hash", "attestation", "agent", "timestamp"}
    missing = required - set(payload.keys())
    extra = set(payload.keys()) - required
    if missing or extra:
        err = "invalid_fields"
        details = {}
        if missing:
            details["missing"] = sorted(missing)
        if extra:
            details["extra"] = sorted(extra)
        write_validation_log(client_ip, "shannon_request", "REJECT", err)
        return {"error": err, "message": "Invalid fields present", "details": details}

    for k in required:
        if not isinstance(payload[k], str):
            err = "wrong_type"
            write_validation_log(client_ip, "shannon_request", "REJECT", err)
            return {"error": err, "message": f"Field {k!r} must be a string", "details": {}}

    # 4. Validate action
    if payload["action"] != "mint_shannon":
        err = "wrong_action"
        write_validation_log(client_ip, "shannon_request", "REJECT", err)
        return {"error": err, "message": "action must be 'mint_shannon'", "details": {}}

    # 5. Run validation chain
    checks = [
        ("trigger", validate_trigger(payload["trigger"])),
        ("context_hash", validate_context_hash(payload["context_hash"])),
        ("attestation", validate_attestation(payload["attestation"])),
        ("timestamp", validate_timestamp(payload["timestamp"])),
    ]
    for name, (ok, msg) in checks:
        if not ok:
            err = f"invalid_{name}"
            write_validation_log(client_ip, "shannon_request", "REJECT", err)
            return {"error": err, "message": msg, "details": {}}

    # 6. All good – construct attribution entry
    # Note: We use the stripped attestation for hashing (without the optional trailing '\n')
    attestation_stripped = payload["attestation"].rstrip('\n')
    attestation_hash = hashlib.sha256(attestation_stripped.encode("utf-8")).hexdigest()
    entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "agent": payload["agent"].rstrip('\n\r'),  # Log stripped agent
        "reason": payload["trigger"],
        "context_hash": payload["context_hash"],
        "attestation_sha256": attestation_hash,
        "shannon_amount": SHANNON_AMOUNT,
        "verifier": os.uname().nodename,  # hostname of the verifier
    }
    write_attribution_log(entry)
    write_validation_log(client_ip, "shannon_request", "ACCEPT", "")
    return {"status": "accepted", "shannon_minted": SHANNON_AMOUNT}

# ---- Example usage (for local testing) ----
if __name__ == "__main__":
    # Simulate a request from stdin (JSON) for quick checks
    raw = sys.stdin.read()
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        print(json.dumps({"error": "invalid_json", "message": "Could not parse JSON", "details": {}}), file=sys.stderr)
        sys.exit(1)
    resp = handle_shannon_request(data, client_ip="127.0.0.1")
    print(json.dumps(resp))
```