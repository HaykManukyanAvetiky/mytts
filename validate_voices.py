#!/usr/bin/env python3
"""
Validate voices.json file structure and required fields.
"""
import json
from pathlib import Path
from typing import Any

VOICES_FILE = Path("/Users/haykmanukyan/work/mytts/backend/data/voices.json")

REQUIRED_ROOT_KEYS = ["version", "updated", "voices"]
REQUIRED_VOICE_FIELDS = [
    "id",
    "name",
    "gender",
    "accent",
    "language",
    "style",
    "description",
    "preview_file"
]

VALID_GENDERS = ["Male", "Female"]


def validate_voices_json() -> dict[str, Any]:
    """
    Validate the voices.json file.

    Returns:
        Dictionary with validation results
    """
    results = {
        "valid": True,
        "errors": [],
        "warnings": [],
        "stats": {}
    }

    # Step 1: Check file exists
    if not VOICES_FILE.exists():
        results["valid"] = False
        results["errors"].append(f"File not found: {VOICES_FILE}")
        return results

    # Step 2: Parse JSON
    try:
        with open(VOICES_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        results["valid"] = False
        results["errors"].append(f"Invalid JSON: {e}")
        return results
    except Exception as e:
        results["valid"] = False
        results["errors"].append(f"Failed to read file: {e}")
        return results

    # Step 3: Validate root structure
    for key in REQUIRED_ROOT_KEYS:
        if key not in data:
            results["valid"] = False
            results["errors"].append(f"Missing root key: '{key}'")

    if not isinstance(data.get("voices"), list):
        results["valid"] = False
        results["errors"].append("'voices' must be a list")
        return results

    voices = data["voices"]
    results["stats"]["total_voices"] = len(voices)

    # Step 4: Check voice count
    if len(voices) != 78:
        results["warnings"].append(
            f"Expected 78 voices, found {len(voices)}"
        )

    # Step 5: Validate each voice
    missing_fields_count = 0
    empty_fields_count = 0
    invalid_gender_count = 0

    for idx, voice in enumerate(voices, start=1):
        voice_id = voice.get("id", f"<unknown-{idx}>")

        # Check for missing fields
        for field in REQUIRED_VOICE_FIELDS:
            if field not in voice:
                results["errors"].append(
                    f"Voice #{idx} ({voice_id}): Missing field '{field}'"
                )
                missing_fields_count += 1
                results["valid"] = False
            elif not voice[field]:
                # Check for empty values
                results["errors"].append(
                    f"Voice #{idx} ({voice_id}): Empty field '{field}'"
                )
                empty_fields_count += 1
                results["valid"] = False

        # Validate gender values
        gender = voice.get("gender")
        if gender and gender not in VALID_GENDERS:
            results["errors"].append(
                f"Voice #{idx} ({voice_id}): Invalid gender '{gender}'. "
                f"Must be one of: {', '.join(VALID_GENDERS)}"
            )
            invalid_gender_count += 1
            results["valid"] = False

    # Step 6: Additional statistics
    results["stats"]["missing_fields"] = missing_fields_count
    results["stats"]["empty_fields"] = empty_fields_count
    results["stats"]["invalid_genders"] = invalid_gender_count

    # Count by language
    language_counts = {}
    for voice in voices:
        lang = voice.get("language", "Unknown")
        language_counts[lang] = language_counts.get(lang, 0) + 1
    results["stats"]["by_language"] = language_counts

    # Count by gender
    gender_counts = {}
    for voice in voices:
        gender = voice.get("gender", "Unknown")
        gender_counts[gender] = gender_counts.get(gender, 0) + 1
    results["stats"]["by_gender"] = gender_counts

    return results


def print_validation_report(results: dict[str, Any]) -> None:
    """Print formatted validation report."""
    print("=" * 70)
    print("VOICES.JSON VALIDATION REPORT")
    print("=" * 70)
    print()

    # Overall status
    if results["valid"]:
        print("✓ VALIDATION PASSED")
    else:
        print("✗ VALIDATION FAILED")
    print()

    # Statistics
    print("-" * 70)
    print("STATISTICS")
    print("-" * 70)
    stats = results["stats"]
    print(f"Total voices: {stats.get('total_voices', 0)}")
    print()

    print("By Language:")
    for lang, count in sorted(stats.get("by_language", {}).items()):
        print(f"  {lang}: {count}")
    print()

    print("By Gender:")
    for gender, count in sorted(stats.get("by_gender", {}).items()):
        print(f"  {gender}: {count}")
    print()

    # Errors
    if results["errors"]:
        print("-" * 70)
        print(f"ERRORS ({len(results['errors'])})")
        print("-" * 70)
        for error in results["errors"]:
            print(f"  • {error}")
        print()

    # Warnings
    if results["warnings"]:
        print("-" * 70)
        print(f"WARNINGS ({len(results['warnings'])})")
        print("-" * 70)
        for warning in results["warnings"]:
            print(f"  • {warning}")
        print()

    print("=" * 70)


if __name__ == "__main__":
    results = validate_voices_json()
    print_validation_report(results)

    # Exit with appropriate code
    exit(0 if results["valid"] else 1)
