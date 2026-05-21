#!/usr/bin/env python3
"""Test error handling for corrupt JSON in voices.json file.

This script tests that VoiceLoadError is properly raised when the JSON
file contains invalid syntax, and that the error message includes
parse error details with line and column information.
"""

import shutil
from pathlib import Path

# Import the voice loading function and exception
from backend.config import load_voices_from_json, VoiceLoadError, VOICES_FILE


def test_corrupt_json_error_handling():
    """Test that corrupt JSON raises VoiceLoadError with parse details."""

    print("Testing JSON error handling...")
    print(f"Voices file path: {VOICES_FILE}")
    print()

    # Step 1: Backup the current voices.json file
    backup_file = VOICES_FILE.with_suffix('.json.bak')
    print(f"Step 1: Backing up {VOICES_FILE} to {backup_file}")
    shutil.copy2(VOICES_FILE, backup_file)
    print("Backup created successfully")
    print()

    try:
        # Step 2: Create invalid JSON with missing comma after "updated" line
        print("Step 2: Creating corrupt JSON file (missing comma after 'updated')")
        corrupt_json = """{
  "version": "1.0.0",
  "updated": "2025-12-18"
  "voices": []
}"""
        VOICES_FILE.write_text(corrupt_json, encoding='utf-8')
        print("Corrupt JSON file created")
        print()

        # Step 3: Clear the lru_cache to force reload
        print("Step 3: Clearing lru_cache")
        load_voices_from_json.cache_clear()
        print("Cache cleared")
        print()

        # Step 4: Try to load voices - should raise VoiceLoadError
        print("Step 4: Attempting to load voices (should raise VoiceLoadError)")
        try:
            voices = load_voices_from_json()
            print("ERROR: No exception was raised! This is unexpected.")
            print(f"Loaded {len(voices)} voices")
            return False

        except VoiceLoadError as e:
            print("SUCCESS: VoiceLoadError was raised as expected")
            print()
            print("Error message:")
            print("-" * 60)
            print(str(e))
            print("-" * 60)
            print()

            # Step 5: Verify error message contains parse details
            print("Step 5: Verifying error message contains parse details")
            error_msg = str(e)

            checks = [
                ("Parse error", "Parse error" in error_msg or "parse error" in error_msg),
                ("Line number", "line" in error_msg.lower()),
                ("Column number", "column" in error_msg.lower()),
            ]

            all_passed = True
            for check_name, check_result in checks:
                status = "PASS" if check_result else "FAIL"
                print(f"  {status}: {check_name}")
                if not check_result:
                    all_passed = False

            print()

            if all_passed:
                print("SUCCESS: All error message checks passed!")
                return True
            else:
                print("FAILURE: Some error message checks failed")
                return False

        except Exception as e:
            print(f"ERROR: Unexpected exception type: {type(e).__name__}")
            print(f"Message: {e}")
            return False

    finally:
        # Step 6: Restore the original file
        print()
        print("Step 6: Restoring original voices.json from backup")
        shutil.copy2(backup_file, VOICES_FILE)
        print("Original file restored")

        # Clean up backup file
        backup_file.unlink()
        print("Backup file removed")

        # Clear cache again to reload proper data
        load_voices_from_json.cache_clear()
        print("Cache cleared")
        print()


def test_successful_reload():
    """Verify that the voices can be loaded successfully after restoration."""
    print("Verifying successful reload after restoration...")
    try:
        voices = load_voices_from_json()
        print(f"SUCCESS: Loaded {len(voices)} voices successfully")
        print(f"First voice: {voices[0].id} - {voices[0].name}")
        return True
    except Exception as e:
        print(f"ERROR: Failed to reload voices: {e}")
        return False


if __name__ == "__main__":
    print("=" * 60)
    print("JSON Error Handling Test")
    print("=" * 60)
    print()

    test_result = test_corrupt_json_error_handling()

    print("=" * 60)
    print()

    reload_result = test_successful_reload()

    print()
    print("=" * 60)
    print("Test Summary")
    print("=" * 60)
    print(f"Error handling test: {'PASSED' if test_result else 'FAILED'}")
    print(f"Reload verification: {'PASSED' if reload_result else 'FAILED'}")
    print()

    if test_result and reload_result:
        print("All tests PASSED!")
        exit(0)
    else:
        print("Some tests FAILED!")
        exit(1)
