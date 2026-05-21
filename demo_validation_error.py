"""Demo: What happens when voice data is invalid.

This script demonstrates the actual error message a developer would see
if they accidentally created invalid voice data.
"""

import json
import shutil
from pathlib import Path

from backend.config import VoiceLoadError, load_voices_from_json


def demo_validation_error() -> None:
    """Demonstrate validation error with clear, helpful output."""
    voices_file = Path("backend/data/voices.json")
    backup_file = Path("backend/data/voices.json.bak")

    print("\n" + "=" * 70)
    print("DEMO: Voice Validation Error")
    print("=" * 70)
    print("\nScenario: A developer accidentally forgets to include the 'gender'")
    print("field when adding a new voice to voices.json")
    print("=" * 70)

    # Backup and modify
    shutil.copy(voices_file, backup_file)

    try:
        with open(voices_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        # Show the invalid voice data
        modified_data = data.copy()
        first_voice = modified_data["voices"][0].copy()
        del first_voice["gender"]
        modified_data["voices"][0] = first_voice

        print("\nInvalid voice entry (missing 'gender'):")
        print("-" * 70)
        for key, value in first_voice.items():
            if key == "description":
                print(f'  "{key}": "{value[:50]}..."')
            else:
                print(f'  "{key}": "{value}"')
        print("-" * 70)

        # Write and try to load
        with open(voices_file, "w", encoding="utf-8") as f:
            json.dump(modified_data, f, indent=2, ensure_ascii=False)

        load_voices_from_json.cache_clear()

        print("\nAttempting to load voices.json...\n")

        try:
            voices = load_voices_from_json()
            print("ERROR: Validation did not catch the missing field!")
        except VoiceLoadError as e:
            print("VoiceLoadError: " + "=" * 54)
            print(str(e))
            print("=" * 70)
            print("\n✓ The error message clearly indicates:")
            print("  1. What went wrong: 'Field required'")
            print("  2. Where it happened: 'voices.0.gender'")
            print("  3. The type of error: '[type=missing]'")
            print("  4. Link to documentation for help")

    finally:
        # Restore
        shutil.copy(backup_file, voices_file)
        backup_file.unlink()
        load_voices_from_json.cache_clear()

    print("\n" + "=" * 70)
    print("This validation prevents invalid data from reaching production!")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    demo_validation_error()
