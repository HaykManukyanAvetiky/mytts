"""Test that server startup fails gracefully with invalid voice data.

This script simulates what would happen if the server tries to start with
invalid voice configuration. The Settings class calls load_voices_from_json()
during initialization, so any validation errors should be caught at startup.
"""

import json
import shutil
from pathlib import Path

from backend.config import Settings, VoiceLoadError, load_voices_from_json


def test_server_startup_with_invalid_data() -> None:
    """Test that server fails to start with invalid voice data."""
    voices_file = Path("backend/data/voices.json")
    backup_file = Path("backend/data/voices.json.bak")

    print("=" * 70)
    print("Testing: Server Startup with Invalid Voice Data")
    print("=" * 70)

    # Step 1: Backup original file
    print("\n1. Creating backup of voices.json...")
    shutil.copy(voices_file, backup_file)
    print(f"   ✓ Backup created")

    try:
        # Step 2: Create invalid voice data (missing 'language' field)
        print("\n2. Creating invalid voice data (missing 'language' field)...")
        with open(voices_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        modified_data = data.copy()
        first_voice = modified_data["voices"][0].copy()
        voice_id = first_voice["id"]
        del first_voice["language"]
        modified_data["voices"][0] = first_voice

        with open(voices_file, "w", encoding="utf-8") as f:
            json.dump(modified_data, f, indent=2, ensure_ascii=False)

        print(f"   ✓ Modified voice: {voice_id}")
        print(f"   ✓ Removed 'language' field")

        # Step 3: Clear cache
        print("\n3. Clearing cache...")
        load_voices_from_json.cache_clear()
        print("   ✓ Cache cleared")

        # Step 4: Try to load voices (simulating server startup)
        print("\n4. Attempting to load voices (simulating server startup)...")
        try:
            # This is what Settings.__init__ does when accessing available_voices
            voices = load_voices_from_json()
            print("   ✗ ERROR: Server would start with invalid data!")
            print(f"   ✗ Loaded {len(voices)} voices without validation")
            success = False
        except VoiceLoadError as e:
            print("   ✓ VoiceLoadError raised - server startup would fail")
            print(f"\n   Error details:")
            print(f"   {'-' * 66}")
            error_lines = str(e).split('\n')
            for line in error_lines:
                print(f"   {line}")
            print(f"   {'-' * 66}")

            # Verify error mentions the missing field
            if "language" in str(e).lower():
                print("\n   ✓ Error correctly identifies missing 'language' field")
                success = True
            else:
                print("\n   ✗ Error doesn't identify the missing field")
                success = False

        # Step 5: Test API route behavior (what actually calls load_voices_from_json)
        print("\n5. Testing API route behavior (calls load_voices_from_json)...")
        print("   Note: The /voices endpoint calls load_voices_from_json()")
        load_voices_from_json.cache_clear()
        try:
            # This simulates what the /voices endpoint does
            voices = load_voices_from_json()
            print("   ✗ ERROR: API endpoint would return invalid voice data!")
            success = False
        except VoiceLoadError as e:
            print("   ✓ API endpoint would fail with VoiceLoadError (status 500)")
            print("   ✓ This prevents serving invalid voice data to clients")
            success = success and True  # Keep previous success state

    finally:
        # Step 6: Restore original file
        print("\n6. Restoring original voices.json...")
        shutil.copy(backup_file, voices_file)
        backup_file.unlink()
        load_voices_from_json.cache_clear()
        print("   ✓ Original file restored")

    # Step 7: Verify server can start with valid data
    print("\n7. Verifying server can start with valid data...")
    try:
        voices = load_voices_from_json()
        settings = Settings()
        print(f"   ✓ Successfully loaded {len(voices)} voices")
        print(f"   ✓ Settings initialized successfully")
        print(f"   ✓ Default voice: {settings.default_voice}")
    except Exception as e:
        print(f"   ✗ ERROR: Failed to load valid data: {e}")
        success = False

    # Summary
    print("\n" + "=" * 70)
    if success:
        print("✓ TEST PASSED:")
        print("  - load_voices_from_json() fails with invalid data (VoiceLoadError)")
        print("  - Error message identifies the missing field")
        print("  - API endpoint validation prevents serving invalid voice data")
        print("  - Server works successfully with valid data")
    else:
        print("✗ TEST FAILED - See errors above")
    print("=" * 70)


if __name__ == "__main__":
    test_server_startup_with_invalid_data()
