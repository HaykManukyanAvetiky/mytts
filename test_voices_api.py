#!/usr/bin/env python3
"""
Test script to verify the /api/tts/voices endpoint response format.
This script validates that the API response matches the expected schema
and contains all required voices.
"""

import json
import urllib.request
import urllib.error
from typing import Dict, List, Any


def test_voices_endpoint():
    """Test the /api/tts/voices endpoint and verify the response."""

    # API endpoint
    url = "http://localhost:8000/api/tts/voices"

    print("=" * 80)
    print("TESTING /api/tts/voices ENDPOINT")
    print("=" * 80)
    print()

    # Step 1: Call the API endpoint
    print("Step 1: Calling API endpoint...")
    try:
        with urllib.request.urlopen(url, timeout=10) as response:
            response_text = response.read().decode('utf-8')
            status_code = response.status
        print(f"   Status Code: {status_code}")
        print("   SUCCESS: API endpoint responded")
    except urllib.error.URLError as e:
        print(f"   ERROR: Failed to call API endpoint: {e}")
        return False
    print()

    # Step 2: Parse JSON response
    print("Step 2: Parsing JSON response...")
    try:
        data = json.loads(response_text)
        print("   SUCCESS: Response is valid JSON")
    except json.JSONDecodeError as e:
        print(f"   ERROR: Failed to parse JSON: {e}")
        return False
    print()

    # Step 3: Verify response structure
    print("Step 3: Verifying response structure...")
    if not isinstance(data, dict):
        print(f"   ERROR: Response is not a dictionary, got {type(data)}")
        return False

    if "voices" not in data:
        print("   ERROR: Response missing 'voices' key")
        return False

    if not isinstance(data["voices"], list):
        print(f"   ERROR: 'voices' is not a list, got {type(data['voices'])}")
        return False

    print(f"   SUCCESS: Response has correct structure")
    print(f"   Root keys: {list(data.keys())}")
    print()

    # Step 4: Count voices
    voices = data["voices"]
    voice_count = len(voices)
    print("Step 4: Counting voices...")
    print(f"   Total voices: {voice_count}")

    if voice_count == 78:
        print("   SUCCESS: Exactly 78 voices returned as expected")
    else:
        print(f"   WARNING: Expected 78 voices, got {voice_count}")
    print()

    # Step 5: Verify required fields in each voice
    print("Step 5: Verifying voice object structure...")
    required_fields = ["id", "name", "gender", "accent", "language", "style", "description", "preview_file"]

    all_valid = True
    invalid_voices = []

    for i, voice in enumerate(voices):
        if not isinstance(voice, dict):
            print(f"   ERROR: Voice at index {i} is not a dictionary")
            all_valid = False
            continue

        missing_fields = [field for field in required_fields if field not in voice]
        if missing_fields:
            print(f"   ERROR: Voice at index {i} (ID: {voice.get('id', 'UNKNOWN')}) missing fields: {missing_fields}")
            invalid_voices.append(voice.get('id', f'index_{i}'))
            all_valid = False
            continue

        # Verify all fields are strings
        non_string_fields = [field for field in required_fields if not isinstance(voice.get(field), str)]
        if non_string_fields:
            print(f"   ERROR: Voice {voice['id']} has non-string fields: {non_string_fields}")
            invalid_voices.append(voice['id'])
            all_valid = False

    if all_valid:
        print(f"   SUCCESS: All {voice_count} voices have required fields")
        print(f"   Required fields: {', '.join(required_fields)}")
    else:
        print(f"   FAILED: {len(invalid_voices)} voices have issues")
        print(f"   Invalid voice IDs: {', '.join(invalid_voices[:10])}{'...' if len(invalid_voices) > 10 else ''}")
    print()

    # Step 6: Verify key voices are present
    print("Step 6: Verifying key voices are present...")
    expected_voices = {
        "en-US-GuyNeural": {"name": "Guy", "language": "English"},
        "en-US-JennyNeural": {"name": "Jenny", "language": "English"},
        "en-GB-RyanNeural": {"name": "Ryan", "language": "English"},
        "en-GB-SoniaNeural": {"name": "Sonia", "language": "English"},
        "en-AU-NatashaNeural": {"name": "Natasha", "language": "English"},
    }

    voice_map = {v["id"]: v for v in voices}

    for voice_id, expected_data in expected_voices.items():
        if voice_id not in voice_map:
            print(f"   ERROR: Expected voice '{voice_id}' not found")
            all_valid = False
        else:
            voice = voice_map[voice_id]
            if voice["name"] != expected_data["name"]:
                print(f"   ERROR: Voice {voice_id} name mismatch: expected '{expected_data['name']}', got '{voice['name']}'")
                all_valid = False
            if voice["language"] != expected_data["language"]:
                print(f"   ERROR: Voice {voice_id} language mismatch: expected '{expected_data['language']}', got '{voice['language']}'")
                all_valid = False

    if all_valid:
        print(f"   SUCCESS: All key English voices are present and correct")
    print()

    # Step 7: Verify voice ordering (English first)
    print("Step 7: Verifying voice ordering (English voices first)...")
    first_5_voices = voices[:5]
    english_count = sum(1 for v in first_5_voices if v["language"] == "English")

    if english_count == 5:
        print(f"   SUCCESS: First 5 voices are all English")
        for i, v in enumerate(first_5_voices, 1):
            print(f"      {i}. {v['name']} ({v['id']})")
    else:
        print(f"   WARNING: Only {english_count}/5 of first voices are English")
    print()

    # Step 8: Verify language diversity
    print("Step 8: Verifying language diversity...")
    languages = {}
    for voice in voices:
        lang = voice["language"]
        languages[lang] = languages.get(lang, 0) + 1

    print(f"   Languages found: {len(languages)}")
    for lang, count in sorted(languages.items()):
        print(f"      {lang}: {count} voices")

    expected_languages = ["English", "Spanish", "French", "German", "Portuguese"]
    missing_languages = [lang for lang in expected_languages if lang not in languages]

    if not missing_languages:
        print(f"   SUCCESS: All expected languages are present")
    else:
        print(f"   ERROR: Missing languages: {', '.join(missing_languages)}")
        all_valid = False
    print()

    # Step 9: Verify preview_file format
    print("Step 9: Verifying preview_file format...")
    invalid_preview_files = []
    for voice in voices:
        preview_file = voice["preview_file"]
        if not preview_file.endswith(".mp3"):
            invalid_preview_files.append(f"{voice['id']}: {preview_file}")
        if preview_file != f"{voice['id']}.mp3":
            invalid_preview_files.append(f"{voice['id']}: expected '{voice['id']}.mp3', got '{preview_file}'")

    if not invalid_preview_files:
        print(f"   SUCCESS: All preview_file values follow the correct format (ID.mp3)")
    else:
        print(f"   ERROR: {len(invalid_preview_files)} preview_file issues found:")
        for issue in invalid_preview_files[:5]:
            print(f"      {issue}")
    print()

    # Step 10: Sample voice data
    print("Step 10: Sample voice data (first voice)...")
    if voices:
        first_voice = voices[0]
        print("   " + json.dumps(first_voice, indent=2).replace("\n", "\n   "))
    print()

    # Final summary
    print("=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"Total voices: {voice_count}")
    print(f"Expected: 78")
    print(f"Match: {'YES' if voice_count == 78 else 'NO'}")
    print()
    print(f"Structure validation: {'PASSED' if all_valid else 'FAILED'}")
    print(f"All required fields present: {'YES' if all_valid else 'NO'}")
    print(f"All languages present: {'YES' if not missing_languages else 'NO'}")
    print()

    if voice_count == 78 and all_valid and not missing_languages:
        print("OVERALL RESULT: SUCCESS - API response format is correct and complete")
        return True
    else:
        print("OVERALL RESULT: FAILED - Issues detected, see details above")
        return False


if __name__ == "__main__":
    success = test_voices_endpoint()
    exit(0 if success else 1)
