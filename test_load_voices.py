#!/usr/bin/env python3
"""Test script for load_voices_from_json() function."""

from backend.config import load_voices_from_json, VoiceInfo

def test_load_voices():
    """Test the load_voices_from_json function."""

    # Test 1: Load voices
    print("Test 1: Loading voices from JSON...")
    voices = load_voices_from_json()
    print(f"✓ Total voices loaded: {len(voices)}")
    assert len(voices) == 78, f"Expected 78 voices, got {len(voices)}"

    # Test 2: Verify all are VoiceInfo instances
    print("\nTest 2: Verifying all items are VoiceInfo instances...")
    assert all(isinstance(v, VoiceInfo) for v in voices), "Not all items are VoiceInfo instances"
    print(f"✓ All {len(voices)} items are VoiceInfo instances")

    # Test 3: Check languages
    print("\nTest 3: Checking language coverage...")
    languages = set(v.language for v in voices)
    expected_langs = {"English", "Spanish", "French", "German", "Portuguese"}
    print(f"  Found languages: {sorted(languages)}")
    assert languages == expected_langs, f"Expected {expected_langs}, got {languages}"
    print("✓ All expected languages present")

    # Test 4: Verify at least one voice from each language
    print("\nTest 4: Verifying at least one voice per language...")
    for lang in expected_langs:
        lang_voices = [v for v in voices if v.language == lang]
        print(f"  {lang}: {len(lang_voices)} voices")
        assert len(lang_voices) > 0, f"No voices found for {lang}"
        # Show first voice as example
        example = lang_voices[0]
        print(f"    Example: {example.name} ({example.id}) - {example.gender}, {example.accent}")
    print("✓ Each language has at least one voice")

    # Test 5: Test caching (should return same object)
    print("\nTest 5: Testing LRU cache...")
    voices2 = load_voices_from_json()
    assert voices is voices2, "LRU cache not working - returned different object"
    print("✓ LRU cache works correctly (same object returned)")

    # Test 6: Verify data structure integrity
    print("\nTest 6: Verifying data structure integrity...")
    for i, voice in enumerate(voices[:3]):  # Check first 3 voices
        assert hasattr(voice, 'id'), f"Voice {i} missing 'id' attribute"
        assert hasattr(voice, 'name'), f"Voice {i} missing 'name' attribute"
        assert hasattr(voice, 'gender'), f"Voice {i} missing 'gender' attribute"
        assert hasattr(voice, 'accent'), f"Voice {i} missing 'accent' attribute"
        assert hasattr(voice, 'language'), f"Voice {i} missing 'language' attribute"
        assert hasattr(voice, 'style'), f"Voice {i} missing 'style' attribute"
        assert hasattr(voice, 'description'), f"Voice {i} missing 'description' attribute"
        assert hasattr(voice, 'preview_file'), f"Voice {i} missing 'preview_file' attribute"
        print(f"  Voice {i+1}: {voice.name} ({voice.id}) - All attributes present")
    print("✓ Data structure integrity verified")

    print("\n" + "="*50)
    print("ALL TESTS PASSED!")
    print("="*50)

if __name__ == "__main__":
    test_load_voices()
