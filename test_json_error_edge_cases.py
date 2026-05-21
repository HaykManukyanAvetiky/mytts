#!/usr/bin/env python3
"""Test additional edge cases for JSON error handling.

This script tests various types of JSON corruption to ensure
robust error handling across different scenarios.
"""

import shutil
from pathlib import Path

from backend.config import load_voices_from_json, VoiceLoadError, VOICES_FILE


def run_test_case(case_name: str, corrupt_json: str) -> bool:
    """Run a single test case with corrupt JSON.

    Args:
        case_name: Descriptive name of the test case
        corrupt_json: The corrupt JSON string to test

    Returns:
        True if test passed, False otherwise
    """
    print(f"\nTest Case: {case_name}")
    print("-" * 60)

    # Backup original file
    backup_file = VOICES_FILE.with_suffix('.json.bak')
    shutil.copy2(VOICES_FILE, backup_file)

    try:
        # Write corrupt JSON
        VOICES_FILE.write_text(corrupt_json, encoding='utf-8')

        # Clear cache and try to load
        load_voices_from_json.cache_clear()

        try:
            voices = load_voices_from_json()
            print(f"FAIL: No exception raised! Loaded {len(voices)} voices")
            return False

        except VoiceLoadError as e:
            print("PASS: VoiceLoadError raised")
            print(f"Error message: {str(e)[:200]}...")
            return True

        except Exception as e:
            print(f"FAIL: Unexpected exception: {type(e).__name__}: {e}")
            return False

    finally:
        # Restore original file
        shutil.copy2(backup_file, VOICES_FILE)
        backup_file.unlink()
        load_voices_from_json.cache_clear()


def test_all_edge_cases():
    """Test various JSON corruption scenarios."""
    print("=" * 60)
    print("JSON Error Handling - Edge Cases")
    print("=" * 60)

    test_cases = [
        (
            "Missing closing brace",
            """{
  "version": "1.0.0",
  "updated": "2025-12-18",
  "voices": []
"""
        ),
        (
            "Unclosed string",
            """{
  "version": "1.0.0",
  "updated": "2025-12-18,
  "voices": []
}"""
        ),
        (
            "Missing comma between fields",
            """{
  "version": "1.0.0"
  "updated": "2025-12-18",
  "voices": []
}"""
        ),
        (
            "Extra comma at end",
            """{
  "version": "1.0.0",
  "updated": "2025-12-18",
  "voices": [],
}"""
        ),
        (
            "Unclosed array",
            """{
  "version": "1.0.0",
  "updated": "2025-12-18",
  "voices": [
}"""
        ),
        (
            "Invalid escape sequence",
            """{
  "version": "1.0.0",
  "updated": "2025-12-18",
  "voices": [],
  "invalid": "\\x"
}"""
        ),
        (
            "Empty file",
            ""
        ),
        (
            "Not JSON at all",
            "This is not JSON"
        ),
        (
            "Only opening brace",
            "{"
        ),
    ]

    results = []
    for case_name, corrupt_json in test_cases:
        result = run_test_case(case_name, corrupt_json)
        results.append((case_name, result))

    # Summary
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for case_name, result in results:
        status = "PASS" if result else "FAIL"
        print(f"{status}: {case_name}")

    print()
    print(f"Passed: {passed}/{total}")

    return passed == total


def verify_normal_operation():
    """Verify that normal operation still works after tests."""
    print("\n" + "=" * 60)
    print("Verifying normal operation")
    print("=" * 60)

    try:
        voices = load_voices_from_json()
        print(f"SUCCESS: Loaded {len(voices)} voices")
        return True
    except Exception as e:
        print(f"FAIL: {e}")
        return False


if __name__ == "__main__":
    edge_cases_passed = test_all_edge_cases()
    normal_op_passed = verify_normal_operation()

    print("\n" + "=" * 60)
    print("Final Result")
    print("=" * 60)
    print(f"Edge cases: {'PASSED' if edge_cases_passed else 'FAILED'}")
    print(f"Normal operation: {'PASSED' if normal_op_passed else 'FAILED'}")
    print()

    if edge_cases_passed and normal_op_passed:
        print("All tests PASSED!")
        exit(0)
    else:
        print("Some tests FAILED!")
        exit(1)
