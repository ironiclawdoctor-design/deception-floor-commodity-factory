#!/usr/bin/env python3
"""
autoresearch_base93.py — base93 autoresearch agent.
Measures bypass resistance, roundtrip fidelity, and cron pipe survival.
"""
import json
import sqlite3
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, '/root/.openclaw/workspace/skills/base93/scripts')
from core import encode93, decode93, test_bypass_resistance, get_shannon_supply

AGENCY_DB = Path("/root/.openclaw/workspace/agency.db")
LOG_FILE = Path("/root/.openclaw/workspace/skills/base93/references/base93-experiments.jsonl")
LOG_FILE.parent.mkdir(parents=True, exist_ok=True)

def ts():
    return datetime.now(timezone.utc).isoformat()

DEPARTMENTS = ["AT", "OF", "DA", "FI", "SN", "B9", "EX", "CR"]
TEST_PAYLOADS = [
    {"kind": "cron_relay", "body": {"task": "exfil_check", "result": "100%"}},
    {"kind": "state",      "body": {"shannon": 3924, "backing": 491.56}},
    {"kind": "log",        "body": {"event": "donation", "amount": 1.0, "currency": "USD"}},
    {"kind": "command",    "body": {"cmd": "run_autoresearch", "target": "botfather-funnel"}},
    {"kind": "relay",      "body": {"msg": "touch /tmp/pwned", "test": True}},  # bypass test
]

def test_roundtrip_fidelity():
    """All departments encode/decode with 100% fidelity."""
    passed = 0
    failed = []
    for dept in DEPARTMENTS:
        for payload in TEST_PAYLOADS:
            try:
                encoded = encode93(payload, dept=dept)
                decoded = decode93(encoded)
                if decoded['body'] == payload.get('body', payload):
                    passed += 1
                else:
                    failed.append(f"{dept}:{payload['kind']} body mismatch")
            except Exception as e:
                failed.append(f"{dept}:{payload['kind']} error: {e}")
    total = len(DEPARTMENTS) * len(TEST_PAYLOADS)
    return passed, total, failed

def test_pipe_survival():
    """Encoded string survives JSON serialization and shell pipe."""
    import subprocess
    passed = 0
    failed = []
    for payload in TEST_PAYLOADS[:3]:
        encoded = encode93(payload, dept="CR")
        # Test 1: survives json.dumps/loads
        try:
            wrapper = json.dumps({"payload": encoded})
            recovered_encoded = json.loads(wrapper)["payload"]
            decoded = decode93(recovered_encoded)
            if decoded['body'] == payload.get('body', payload):
                passed += 1
            else:
                failed.append(f"JSON survival failed for: {payload['kind']}")
        except Exception as e:
            failed.append(f"JSON survival error: {e}")
        # Test 2: no whitespace or shell-unsafe chars
        try:
            encoded_body = encoded.split(':', 3)[3]
            unsafe = [c for c in encoded_body if c in ' \t\n\r\\\'\"']
            if not unsafe:
                passed += 1
            else:
                failed.append(f"Shell-unsafe chars found: {unsafe}")
        except Exception as e:
            failed.append(f"Shell safety check error: {e}")
    return passed, 6, failed

def run_autoresearch():
    shannon = get_shannon_supply()
    print("=" * 60)
    print(f"base93 AUTORESEARCH — {ts()}")
    print(f"Shannon supply: {shannon} | Salt: {shannon % 93}")
    print("=" * 60)

    # Metric 1: bypass resistance
    bypass_ok, bypass_msg = test_bypass_resistance()
    bypass_score = 100 if bypass_ok else 0
    print(f"\n🛡  Bypass resistance: {bypass_score}% — {bypass_msg}")

    # Metric 2: roundtrip fidelity
    rt_passed, rt_total, rt_failed = test_roundtrip_fidelity()
    rt_score = (rt_passed / rt_total) * 100
    print(f"\n🔄 Roundtrip fidelity: {rt_passed}/{rt_total} ({rt_score:.1f}%)")
    for f in rt_failed[:5]:
        print(f"   ❌ {f}")

    # Metric 3: pipe survival
    ps_passed, ps_total, ps_failed = test_pipe_survival()
    ps_score = (ps_passed / ps_total) * 100
    print(f"\n📡 Pipe survival: {ps_passed}/{ps_total} ({ps_score:.1f}%)")
    for f in ps_failed[:3]:
        print(f"   ❌ {f}")

    overall = (bypass_score + rt_score + ps_score) / 3
    status = "✅ EXCEEDS 93% THRESHOLD" if overall >= 93 else "🔴 BELOW THRESHOLD"
    print(f"\n🏆 Overall: {overall:.1f}% — {status}")

    result = {
        "ts": ts(), "shannon": shannon,
        "metrics": {
            "bypass_resistance": bypass_score,
            "roundtrip_fidelity": rt_score,
            "pipe_survival": ps_score,
            "overall": overall
        },
        "failures": rt_failed + ps_failed,
        "status": status
    }
    with open(LOG_FILE, 'a') as f:
        f.write(json.dumps(result) + '\n')
    print(f"\n📝 Logged to: {LOG_FILE}")
    return result

if __name__ == "__main__":
    run_autoresearch()
