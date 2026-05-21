"""Comprehensive test for voice validation error handling.

This script tests validation for all required fields to ensure Pydantic
properly catches any missing required field.
"""

import json
import shutil
from pathlib import Path

from backend.config import VoiceLoadError, load_voices_from_json


def test_missing_field(field_name: str) -> bool:
    """Test that missing a specific field raises VoiceLoadError.

    Args:
        field_name: Name of the required field to remove

    Returns:
        True if test passed, False otherwise
    """
    voices_file = Path("backend/data/voices.json")
    backup_file = Path("backend/data/voices.json.bak")

    print(f"\n{'=' * 70}")
    print(f"Testing: Missing '{field_name}' field")
    print(f"{'=' * 70}")

    # Backup original file
    shutil.copy(voices_file, backup_file)

    try:
        # Load original data
        with open(voices_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        # Create modified version with missing field
        modified_data = data.copy()
        first_voice = modified_data["voices"][0].copy()
        voice_id = first_voice["id"]

        if field_name not in first_voice:
            print(f"   ⚠ Field '{field_name}' not found in voice - skipping")
            return True

        del first_voice[field_name]
        modified_data["voices"][0] = first_voice

        # Write modified file
        with open(voices_file, "w", encoding="utf-8") as f:
            json.dump(modified_data, f, indent=2, ensure_ascii=False)

        # Clear cache and try to load
        load_voices_from_json.cache_clear()

        # Attempt to load - should raise VoiceLoadError
        try:
            voices = load_voices_from_json()
            print(f"   ✗ FAIL: No exception raised for missing '{field_name}'")
            return False
        except VoiceLoadError as e:
            error_msg = str(e).lower()
            if field_name.lower() in error_msg:
                print(f"   ✓ PASS: VoiceLoadError raised, mentions '{field_name}'")
                return True
            else:
                print(f"   ✗ FAIL: Error raised but doesn't mention '{field_name}'")
                print(f"   Error: {e}")
                return False

    finally:
        # Restore original file
        shutil.copy(backup_file, voices_file)
        backup_file.unlink()
        load_voices_from_json.cache_clear()


def main() -> None:
    """Run comprehensive validation tests for all required fields."""
    print("=" * 70)
    print("COMPREHENSIVE VOICE VALIDATION TEST")
    print("Testing all required fields")
    print("=" * 70)

    # All required fields for VoiceInfo
    required_fields = [
        "id",
        "name",
        "gender",
        "accent",
        "language",
        "style",
        "description",
        "preview_file",
    ]

    results = {}
    for field in required_fields:
        results[field] = test_missing_field(field)

    # Summary
    print(f"\n{'=' * 70}")
    print("TEST SUMMARY")
    print(f"{'=' * 70}")

    passed = sum(results.values())
    total = len(results)

    for field, passed_test in results.items():
        status = "✓ PASS" if passed_test else "✗ FAIL"
        print(f"{status:8} | Missing field: {field}")

    print(f"{'=' * 70}")
    print(f"Results: {passed}/{total} tests passed")

    if passed == total:
        print("✓ ALL TESTS PASSED")
    else:
        print(f"✗ {total - passed} TESTS FAILED")
    print(f"{'=' * 70}")


if __name__ == "__main__":
    main()
