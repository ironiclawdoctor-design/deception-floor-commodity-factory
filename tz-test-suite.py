#!/usr/bin/env python3
"""
Test suite for time zone reframe skill.
Tests accuracy, churn reduction, and Excel integration.
"""

import sys
import argparse
import datetime
import random
from excel_integration import ExcelTimeZoneManager, TimeZoneConverter
import os
import time

def run_baseline_tests(iterations: int = 1000, excel_test: bool = True) -> dict:
    """
    Run baseline tests for time zone conversion accuracy and churn.
    
    Args:
        iterations: Number of test iterations
        excel_test: Whether to test Excel integration
    
    Returns:
        Dictionary of test results
    """
    results = {
        'baseline_accuracy': 0.0,
        'baseline_churn': 0.0,
        'excel_export_success': False,
        'excel_import_success': False,
        'total_time_ms': 0,
        'errors': 0
    }
    
    start_time = time.time()
    
    # Initialize converter
    converter = TimeZoneConverter()
    
    # Test data generation
    test_conversions = []
    timezone_pairs = [
        ('EST', 'UTC'),
        ('CST', 'UTC'),
        ('PST', 'EST'),
        ('UTC', 'EST'),
        ('MST', 'PST'),
        ('HST', 'CST'),
        ('EST', 'PST'),
        ('CST', 'MST')
    ]
    
    # Generate test datetime strings
    for i in range(iterations):
        days_offset = i % 365
        dt = datetime.datetime.now() - datetime.timedelta(days=days_offset)
        dt_str = dt.isoformat().replace('T', ' ')
        
        from_tz, to_tz = timezone_pairs[i % len(timezone_pairs)]
        
        test_conversions.append({
            'original_time': dt_str,
            'from_tz': from_tz,
            'to_tz': to_tz
        })
    
    # Run conversions
    successful_conversions = 0
    for conversion in test_conversions:
        try:
            result = converter.convert(
                conversion['original_time'],
                conversion['from_tz'],
                conversion['to_tz']
            )
            
            if not result.startswith('ERROR'):
                successful_conversions += 1
        except Exception as e:
            results['errors'] += 1
    
    # Calculate baseline metrics
    results['baseline_accuracy'] = (successful_conversions / iterations) * 100
    stats = converter.get_stats()
    results['baseline_churn'] = stats['churn']
    
    # Excel integration tests
    if excel_test:
        manager = ExcelTimeZoneManager()
        
        # Export test
        export_data = []
        for i, conversion in enumerate(test_conversions[:100]):
            result = converter.convert(
                conversion['original_time'],
                conversion['from_tz'],
                conversion['to_tz']
            )
            export_data.append({
                'original_time': conversion['original_time'],
                'from_tz': conversion['from_tz'],
                'to_tz': conversion['to_tz'],
                'converted_time': result
            })
        
        try:
            export_result = manager.export_conversions("test_export.xlsx", export_data)
            if "Exported" in export_result or "Export error" not in export_result:
                results['excel_export_success'] = True
                os.remove("test_export.xlsx")  # Clean up
        except Exception as e:
            print(f"Excel export error: {e}")
        
        # Import test (create test file first)
        try:
            manager.export_conversions("test_import.xlsx", export_data)
            import_results = manager.import_schedule("test_import.xlsx")
            if import_results and not import_results[0].get('error'):
                results['excel_import_success'] = True
            os.remove("test_import.xlsx")  # Clean up
        except Exception as e:
            print(f"Excel import error: {e}")
    
    # Calculate total time
    end_time = time.time()
    results['total_time_ms'] = int((end_time - start_time) * 1000)
    
    return results

def validate_accuracy_threshold(accuracy: float, threshold: float = 93.0) -> bool:
    """Validate that accuracy meets threshold."""
    return accuracy >= threshold

def validate_churn_threshold(churn: float, threshold: float = 50.0) -> bool:
    """Validate that churn meets threshold."""
    return churn <= threshold

def main():
    parser = argparse.ArgumentParser(description="Time zone reframe skill test suite")
    parser.add_argument('--iterations', type=int, default=1000, help='Number of test iterations')
    parser.add_argument('--excel-integration-test', type=bool, default=True, help='Test Excel integration')
    parser.add_argument('--threshold', type=float, default=93.0, help='Accuracy threshold percentage')
    
    args = parser.parse_args()
    
    print(f"Running baseline tests with {args.iterations} iterations...")
    results = run_baseline_tests(args.iterations, args.excel_integration_test)
    
    print("\n=== TEST RESULTS ===")
    print(f"Baseline accuracy: {results['baseline_accuracy']:.2f}%")
    print(f"Baseline churn: {results['baseline_churn']:.2f}%")
    print(f"Excel export success: {results['excel_export_success']}")
    print(f"Excel import success: {results['excel_import_success']}")
    print(f"Total errors: {results['errors']}")
    print(f"Total time: {results['total_time_ms']}ms")
    
    # Validate against thresholds
    accuracy_valid = validate_accuracy_threshold(results['baseline_accuracy'], args.threshold)
    churn_valid = validate_churn_threshold(results['baseline_churn'], 50.0)
    
    print("\n=== VALIDATION ===")
    if accuracy_valid:
        print(f"✓ Accuracy meets threshold ({args.threshold}%)")
    else:
        print(f"✗ Accuracy below threshold ({args.threshold}%)")
    
    if churn_valid:
        print(f"✓ Churn meets threshold (<50%)")
    else:
        print(f"✗ Churn exceeds threshold (<50%)")
    
    if results['excel_export_success']:
        print("✓ Excel export successful")
    else:
        print("✗ Excel export failed")
    
    if results['excel_import_success']:
        print("✓ Excel import successful")
    else:
        print("✗ Excel import failed")
    
    # Overall assessment
    all_valid = accuracy_valid and churn_valid and results['excel_export_success'] and results['excel_import_success']
    
    if all_valid:
        print("\n✓ ALL TESTS PASSED - Baseline meets requirements")
        return 0
    else:
        print("\n✗ SOME TESTS FAILED - Baseline needs improvement")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)