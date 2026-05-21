#!/usr/bin/env python3
"""Test the exact error handling example from the task requirements.

This script tests the specific corrupt JSON example provided in the task:
missing comma after the "updated" line.
"""

import shutil
from pathlib import Path

from backend.config import load_voices_from_json, VoiceLoadError, VOICES_FILE


def test_exact_task_example():
    """Test the exact example from task requirements."""
    print("=" * 60)
    print("Testing Exact Task Example")
    print("=" * 60)
    print()
    print("This test uses the exact corrupt JSON from the task:")
    print("Missing comma after 'updated' line")
    print()

    # Backup original file
    backup_file = VOICES_FILE.with_suffix('.json.bak')
    print(f"1. Backing up {VOICES_FILE}")
    shutil.copy2(VOICES_FILE, backup_file)
    print("   Backup created\n")

    # The exact corrupt JSON from the task requirements
    corrupt_json = """{
  "version": "1.0.0",
  "updated": "2025-12-18"
  "voices": []
}"""

    try:
        print("2. Creating corrupt JSON file:")
        print("-" * 60)
        print(corrupt_json)
        print("-" * 60)
        print()

        VOICES_FILE.write_text(corrupt_json, encoding='utf-8')

        print("3. Clearing lru_cache")
        load_voices_from_json.cache_clear()
        print("   Cache cleared\n")

        print("4. Attempting to call load_voices_from_json()")
        print("   Should raise VoiceLoadError...\n")

        try:
            voices = load_voices_from_json()
            print("ERROR: No exception was raised!")
            print(f"Unexpectedly loaded {len(voices)} voices")
            return False

        except VoiceLoadError as e:
            print("SUCCESS: VoiceLoadError raised as expected!\n")
            print("5. Verifying error message contents:")
            print("-" * 60)
            print(str(e))
            print("-" * 60)
            print()

            error_msg = str(e)

            # Verify specific requirements from the task
            checks = {
                "Contains 'Parse error' or 'parse error'": (
                    "Parse error" in error_msg or "parse error" in error_msg
                ),
                "Contains line number (line 4)": "line 4" in error_msg,
                "Contains column number": "column" in error_msg.lower(),
                "Mentions the file path": str(VOICES_FILE) in error_msg,
                "Describes the actual error": (
                    "delimiter" in error_msg.lower() or
                    "comma" in error_msg.lower() or
                    "expecting" in error_msg.lower()
                ),
            }

            print("Error message validation:")
            all_passed = True
            for check_desc, result in checks.items():
                status = "PASS" if result else "FAIL"
                print(f"  [{status}] {check_desc}")
                if not result:
                    all_passed = False

            print()

            if all_passed:
                print("All validation checks PASSED!")
                print()
                return True
            else:
                print("Some validation checks FAILED!")
                print()
                return False

        except Exception as e:
            print(f"ERROR: Unexpected exception type!")
            print(f"Type: {type(e).__name__}")
            print(f"Message: {e}")
            return False

    finally:
        print("6. Restoring original file from backup")
        shutil.copy2(backup_file, VOICES_FILE)
        backup_file.unlink()
        load_voices_from_json.cache_clear()
        print("   File restored and cache cleared\n")


def verify_restoration():
    """Verify that the original file works after restoration."""
    print("=" * 60)
    print("Verifying File Restoration")
    print("=" * 60)
    print()

    try:
        voices = load_voices_from_json()
        print(f"SUCCESS: Loaded {len(voices)} voices from restored file")
        print(f"Sample voices:")
        for voice in voices[:3]:
            print(f"  - {voice.id}: {voice.name} ({voice.gender}, {voice.accent})")
        print()
        return True

    except Exception as e:
        print(f"ERROR: Failed to load voices after restoration!")
        print(f"{type(e).__name__}: {e}")
        return False


if __name__ == "__main__":
    test_passed = test_exact_task_example()
    restore_passed = verify_restoration()

    print("=" * 60)
    print("FINAL RESULTS")
    print("=" * 60)
    print()
    print(f"Task Example Test:     {'PASSED ✓' if test_passed else 'FAILED ✗'}")
    print(f"File Restoration Test: {'PASSED ✓' if restore_passed else 'FAILED ✗'}")
    print()

    if test_passed and restore_passed:
        print("=" * 60)
        print("ALL TESTS PASSED!")
        print("=" * 60)
        print()
        print("Summary:")
        print("- VoiceLoadError is raised for invalid JSON")
        print("- Error message contains line and column of parse error")
        print("- Original file successfully restored after test")
        print()
        exit(0)
    else:
        print("SOME TESTS FAILED!")
        exit(1)
