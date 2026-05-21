"""Test script for voice validation error handling.

This script tests that Pydantic validation properly catches missing required
fields in voice entries and raises appropriate VoiceLoadError exceptions.
"""

import json
import shutil
from pathlib import Path

from backend.config import VoiceLoadError, load_voices_from_json


def test_missing_field_validation() -> None:
    """Test that missing required field raises VoiceLoadError."""
    # Paths
    voices_file = Path("backend/data/voices.json")
    backup_file = Path("backend/data/voices.json.bak")

    print("=" * 70)
    print("Testing Voice Validation: Missing Required Field")
    print("=" * 70)

    # Step 1: Backup original file
    print("\n1. Creating backup of voices.json...")
    shutil.copy(voices_file, backup_file)
    print(f"   ✓ Backup created: {backup_file}")

    try:
        # Step 2: Load original data
        print("\n2. Loading original voices.json...")
        with open(voices_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        print(f"   ✓ Loaded {len(data['voices'])} voices")

        # Step 3: Create modified version with missing field
        print("\n3. Creating modified version with missing 'accent' field...")
        modified_data = data.copy()
        # Remove 'accent' field from first voice
        first_voice = modified_data["voices"][0].copy()
        voice_id = first_voice["id"]
        del first_voice["accent"]
        modified_data["voices"][0] = first_voice

        print(f"   ✓ Removed 'accent' field from voice: {voice_id}")
        print(f"   ✓ Modified voice fields: {list(first_voice.keys())}")

        # Step 4: Write modified file
        print("\n4. Writing modified voices.json...")
        with open(voices_file, "w", encoding="utf-8") as f:
            json.dump(modified_data, f, indent=2, ensure_ascii=False)
        print("   ✓ Modified file written")

        # Step 5: Clear cache and try to load
        print("\n5. Clearing lru_cache and attempting to load voices...")
        load_voices_from_json.cache_clear()
        print("   ✓ Cache cleared")

        # Step 6: Attempt to load - should raise VoiceLoadError
        print("\n6. Calling load_voices_from_json() - expecting VoiceLoadError...")
        try:
            voices = load_voices_from_json()
            print("   ✗ ERROR: No exception was raised!")
            print(f"   ✗ Unexpectedly loaded {len(voices)} voices")
            success = False
        except VoiceLoadError as e:
            print("   ✓ VoiceLoadError raised as expected")
            print(f"\n   Error message:\n   {'-' * 66}")
            error_lines = str(e).split('\n')
            for line in error_lines:
                print(f"   {line}")
            print(f"   {'-' * 66}")

            # Check if error message mentions the missing field
            error_msg = str(e).lower()
            if "accent" in error_msg:
                print("\n   ✓ Error message correctly identifies missing 'accent' field")
                success = True
            else:
                print("\n   ✗ ERROR: Error message does not mention 'accent' field")
                success = False

    finally:
        # Step 7: Restore original file
        print("\n7. Restoring original voices.json from backup...")
        shutil.copy(backup_file, voices_file)
        print("   ✓ Original file restored")

        # Clean up backup
        backup_file.unlink()
        print("   ✓ Backup file removed")

        # Clear cache again
        load_voices_from_json.cache_clear()
        print("   ✓ Cache cleared")

    # Step 8: Final summary
    print("\n" + "=" * 70)
    if success:
        print("✓ TEST PASSED: Validation correctly caught missing required field")
        print("✓ Error message indicates which field is missing")
        print("✓ Original file successfully restored")
    else:
        print("✗ TEST FAILED: See errors above")
    print("=" * 70)


if __name__ == "__main__":
    test_missing_field_validation()
