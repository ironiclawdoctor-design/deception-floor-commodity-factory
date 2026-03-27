#!/usr/bin/env python3
"""
Standalone runner for the correctness invariant check.
Does NOT require excel_integration. Uses only pytz + stdlib.
Logs result to exec-rule-log.jsonl.
"""
import sys
import datetime
import json
import os

def correctness_invariant_check():
    result = {
        'passed': False,
        'dt_before': None,
        'dt_after': None,
        'utc_before': None,
        'utc_after': None,
        'offsets_different': False,
        'error': None
    }

    try:
        import pytz
        eastern = pytz.timezone('US/Eastern')

        fmt = '%Y-%m-%d %H:%M:%S'
        before_naive = datetime.datetime.strptime('2026-03-08 01:30:00', fmt)
        after_naive  = datetime.datetime.strptime('2026-03-08 03:30:00', fmt)

        before_eastern = eastern.localize(before_naive, is_dst=False)  # EST -5
        after_eastern  = eastern.localize(after_naive,  is_dst=True)   # EDT -4

        import pytz as _pytz
        before_utc = before_eastern.astimezone(_pytz.utc)
        after_utc  = after_eastern.astimezone(_pytz.utc)

        result['dt_before']  = str(before_eastern)
        result['dt_after']   = str(after_eastern)
        result['utc_before'] = str(before_utc)
        result['utc_after']  = str(after_utc)

        offset_before = before_eastern.utcoffset()
        offset_after  = after_eastern.utcoffset()
        result['offsets_different'] = (offset_before != offset_after)

        utc_results_differ = (before_utc != after_utc)

        if result['offsets_different'] and utc_results_differ:
            result['passed'] = True
        else:
            result['error'] = (
                f"CACHE COLLAPSE DETECTED: both datetimes produced same UTC offset "
                f"(before={offset_before}, after={offset_after}). "
                f"UTC before={before_utc}, UTC after={after_utc}"
            )

    except ImportError:
        # pytz not available — use zoneinfo (Python 3.9+)
        try:
            from zoneinfo import ZoneInfo
            eastern = ZoneInfo('America/New_York')

            fmt = '%Y-%m-%d %H:%M:%S'
            before_naive = datetime.datetime.strptime('2026-03-08 01:30:00', fmt)
            after_naive  = datetime.datetime.strptime('2026-03-08 03:30:00', fmt)

            # fold=0 = first occurrence (EST -5 for 01:30, unambiguous)
            before_eastern = before_naive.replace(tzinfo=eastern, fold=0)
            # fold=0 = after spring forward (EDT -4 for 03:30, unambiguous)
            after_eastern  = after_naive.replace(tzinfo=eastern, fold=0)

            utc = datetime.timezone.utc
            before_utc = before_eastern.astimezone(utc)
            after_utc  = after_eastern.astimezone(utc)

            result['dt_before']  = str(before_eastern)
            result['dt_after']   = str(after_eastern)
            result['utc_before'] = str(before_utc)
            result['utc_after']  = str(after_utc)

            offset_before = before_eastern.utcoffset()
            offset_after  = after_eastern.utcoffset()
            result['offsets_different'] = (offset_before != offset_after)

            utc_results_differ = (before_utc != after_utc)

            if result['offsets_different'] and utc_results_differ:
                result['passed'] = True
            else:
                result['error'] = (
                    f"CACHE COLLAPSE DETECTED (zoneinfo): "
                    f"before_offset={offset_before}, after_offset={offset_after}, "
                    f"UTC before={before_utc}, UTC after={after_utc}"
                )
        except Exception as e2:
            result['error'] = f"zoneinfo fallback failed: {e2}"

    except Exception as e:
        result['error'] = f"Invariant check exception: {e}"

    return result


def main():
    print("=== CORRECTNESS INVARIANT CHECK ===")
    print("Testing: 2026-03-08 01:30 EST (before spring forward) vs 03:30 EST (after)")
    print()

    inv = correctness_invariant_check()

    print(f"  Before DST: {inv.get('dt_before')}")
    print(f"    => UTC:   {inv.get('utc_before')}")
    print(f"  After  DST: {inv.get('dt_after')}")
    print(f"    => UTC:   {inv.get('utc_after')}")
    print(f"  Offsets different: {inv.get('offsets_different')}")

    if inv['passed']:
        print()
        print("✓ INVARIANT PASSED: DST offsets differ — no cache collapse detected")
        status = "passed"
        finding = f"DST offsets correctly differ. UTC before={inv['utc_before']}, UTC after={inv['utc_after']}"
    else:
        print()
        print(f"✗ INVARIANT FAILED: {inv.get('error')}")
        status = "failed"
        finding = inv.get('error', 'unknown error')

    # Log result to exec-rule-log.jsonl
    log_path = os.path.join(os.path.dirname(__file__), 'exec-rule-log.jsonl')
    log_entry = {
        "rule_id": "TZ-EXP-000-RESULT",
        "experiment": "0",
        "timestamp": "2026-03-27T19:12:00Z",
        "status": status,
        "invariant_passed": inv['passed'],
        "finding": finding,
        "utc_before": inv.get('utc_before'),
        "utc_after": inv.get('utc_after'),
        "offsets_different": inv.get('offsets_different'),
        "error": inv.get('error')
    }
    with open(log_path, 'a') as f:
        f.write(json.dumps(log_entry) + '\n')

    print()
    print(f"Result logged to exec-rule-log.jsonl: status={status}")

    # Now attempt to run the full test suite
    print()
    print("=== ATTEMPTING FULL TEST SUITE ===")
    try:
        sys.argv = ['tz-test-suite.py', '--iterations=100', '--excel-integration-test=true', '--threshold=93.0']
        # Import and run
        import importlib.util
        spec = importlib.util.spec_from_file_location(
            "tz_test_suite",
            os.path.join(os.path.dirname(__file__), 'tz-test-suite.py')
        )
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        exit_code = mod.main()
        print(f"\nTest suite exit code: {exit_code}")
    except SystemExit as e:
        print(f"\nTest suite exited with code: {e.code}")
    except Exception as e:
        print(f"\nTest suite import/run error: {e}")

    return 0 if inv['passed'] else 2


if __name__ == '__main__':
    sys.exit(main())
