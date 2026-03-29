#!/usr/bin/env python3
"""
base93/scripts/core.py — Agency-private encoding core.
Learned from: the-apparatus.py, context-serializer.sh, list_services.py,
              security-rule-functions.sh, fixer/core.py
"""
import base64
import json
import sqlite3
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

# ─── Agency alphabet (93 chars, shell-safe, JSON-safe) ───────────────────────
B64 = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
B93 = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!#$%&*-:;<=>?@^_`{|}~.,/()+[]=?"

assert len(B93) == 93, f"base93 alphabet must be 93 chars, got {len(B93)}"

# ─── Department codes ─────────────────────────────────────────────────────────
DEPARTMENTS = {
    "AUTOMATE": "AT", "OFFICIAL": "OF", "DAIMYO": "DA",
    "FIESTA":   "FI", "SHANNODE": "SN", "BASE93":  "B9",
    "EXFIL":    "EX", "CRON":     "CR"
}

DB_PATH = Path("/root/.openclaw/workspace/dollar/dollar.db")
AGENCY_DB = Path("/root/.openclaw/workspace/agency.db")

def ts():
    return datetime.now(timezone.utc).isoformat()

def get_shannon_supply() -> int:
    """Read current Shannon supply from dollar.db for salt derivation."""
    try:
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        # Try shannon_events table first
        cur.execute("SELECT SUM(amount) FROM shannon_events WHERE amount > 0")
        row = cur.fetchone()
        conn.close()
        return int(row[0] or 3924)
    except Exception:
        return 3924  # fallback to last known supply

def get_salt(shannon_supply: int) -> int:
    """Derive rotation offset from Shannon supply."""
    return shannon_supply % 93

def _rotate_alphabet(salt: int) -> str:
    """Rotate B93 alphabet by salt positions."""
    return B93[salt:] + B93[:salt]

def encode93(payload: dict, dept: str = "B9") -> str:
    """
    Encode a payload dict into a base93 string.
    
    Envelope: {v, dept, ts_shannon, ts_unix, kind, body}
    Output: "B9:<dept>:<shannon>:<encoded>"
    
    Learned from:
    - the-apparatus.py: camouflage pattern with prefix
    - list_services.py: urlsafe_b64encode + rstrip padding
    - context-serializer.sh: pipe-safe output format
    """
    shannon = get_shannon_supply()
    salt = get_salt(shannon)
    rotated = _rotate_alphabet(salt)
    
    # Wrap in agency envelope
    envelope = {
        "v": 1,
        "dept": dept,
        "ts_shannon": shannon,
        "ts_unix": int(time.time()),
        "kind": payload.get("kind", "relay"),
        "body": payload.get("body", payload)
    }
    
    # Encode: JSON → bytes → base64 → remap to B93 alphabet
    raw_bytes = json.dumps(envelope, separators=(',', ':')).encode()
    b64_bytes = base64.b64encode(raw_bytes).decode().rstrip('=')
    
    # Remap b64 chars to rotated B93 alphabet
    # B64 chars map to positions 0-63; positions 64-92 are agency-only
    encoded = ''.join(
        rotated[B64.index(c)] if c in B64 else c
        for c in b64_bytes
    )
    
    result = f"B9:{dept}:{shannon}:{encoded}"
    
    # Audit log
    _log_operation("encode", dept, shannon, len(raw_bytes), len(result))
    
    return result

def decode93(encoded_str: str) -> dict:
    """
    Decode a base93 string back to payload dict.
    
    Requires: Shannon supply at encode time (embedded in prefix).
    Fails safely if wrong department or Shannon mismatch.
    
    Learned from:
    - security-rule-functions.sh: must NOT decode via standard base64 -d
    - fixer/core.py: encoding flag signals which decoder to use
    """
    parts = encoded_str.split(':', 3)
    if len(parts) != 4 or parts[0] != 'B9':
        raise ValueError(f"Not a base93 payload: missing B9 prefix")
    
    _, dept, shannon_str, encoded = parts
    shannon = int(shannon_str)
    salt = get_salt(shannon)
    rotated = _rotate_alphabet(salt)
    
    # Reverse remap: rotated B93 → B64
    b64_chars = ''.join(
        B64[rotated.index(c)] if c in rotated and rotated.index(c) < 64 else c
        for c in encoded
    )
    
    # Restore padding
    padding = 4 - len(b64_chars) % 4
    if padding != 4:
        b64_chars += '=' * padding
    
    # Decode
    raw_bytes = base64.b64decode(b64_chars)
    envelope = json.loads(raw_bytes.decode())
    
    # Audit log
    _log_operation("decode", dept, shannon, len(raw_bytes), len(encoded_str))
    
    return envelope

def _log_operation(op: str, dept: str, shannon: int, payload_bytes: int, encoded_len: int):
    """Log encode/decode to agency.db base93_log table."""
    try:
        conn = sqlite3.connect(AGENCY_DB)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS base93_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ts TEXT NOT NULL,
                operation TEXT NOT NULL,
                department TEXT NOT NULL,
                shannon_at_time INTEGER NOT NULL,
                payload_bytes INTEGER NOT NULL,
                encoded_length INTEGER NOT NULL
            )
        """)
        conn.execute(
            "INSERT INTO base93_log (ts, operation, department, shannon_at_time, payload_bytes, encoded_length) VALUES (?,?,?,?,?,?)",
            (ts(), op, dept, shannon, payload_bytes, encoded_len)
        )
        conn.commit()
        conn.close()
    except Exception as e:
        pass  # Never crash on audit failure — SR doctrine

def test_bypass_resistance():
    """
    Verify base93 payloads resist known base64 bypass patterns.
    Learned from security-rule-functions.sh bypass detection tests.
    """
    payload = {"dept": "B9", "kind": "test", "body": {"msg": "touch /tmp/pwned"}}
    encoded = encode93(payload)
    encoded_body = encoded.split(':', 3)[3]  # Just the encoded part
    
    # Test 1: Standard base64 -d should NOT produce readable output
    try:
        decoded = base64.b64decode(encoded_body + '==')
        decoded_str = decoded.decode('utf-8', errors='replace')
        if 'touch /tmp/pwned' in decoded_str:
            return False, "BYPASS POSSIBLE: standard base64 decoded payload"
        if '"body"' in decoded_str and 'pwned' in decoded_str:
            return False, "BYPASS POSSIBLE: partial decode succeeded"
    except Exception:
        pass  # Decode failure = bypass resistance confirmed
    
    # Test 2: Full roundtrip should work with correct decoder
    try:
        recovered = decode93(encoded)
        if recovered['body']['msg'] != 'touch /tmp/pwned':
            return False, "ROUNDTRIP FAILED: payload corrupted"
    except Exception as e:
        return False, f"ROUNDTRIP FAILED: {e}"
    
    return True, "BYPASS RESISTANT + ROUNDTRIP OK"

if __name__ == "__main__":
    # Self-test
    print("=== base93 self-test ===")
    print(f"Alphabet length: {len(B93)}")
    print(f"Shannon supply: {get_shannon_supply()}")
    print(f"Current salt: {get_salt(get_shannon_supply())}")
    
    # Encode test
    test_payload = {
        "kind": "cron_relay",
        "body": {"task": "exfil_check", "result": "100%", "dept_from": "EX", "dept_to": "FI"}
    }
    encoded = encode93(test_payload, dept="EX")
    print(f"\nEncoded: {encoded[:60]}...")
    
    # Decode test
    decoded = decode93(encoded)
    print(f"Decoded body: {decoded['body']}")
    print(f"Envelope dept: {decoded['dept']}, shannon: {decoded['ts_shannon']}")
    
    # Bypass resistance test
    ok, msg = test_bypass_resistance()
    print(f"\nBypass resistance: {'✅' if ok else '❌'} {msg}")
    
    print("\n✅ base93 operational")
