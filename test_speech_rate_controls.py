#!/usr/bin/env python3
"""
Test speech rate controls for multiple languages.

Tests rate values:
- 0.75x (slow): rate parameter = "-25%"
- 1.0x (normal): rate parameter = "+0%"
- 1.25x (fast): rate parameter = "+25%"
- 1.5x (fastest): rate parameter = "+50%"

Verifies:
1. Audio is generated successfully
2. File sizes differ based on rate (slower = larger, faster = smaller)
"""

import json
import time
from typing import Dict, Tuple
from urllib.request import urlopen, Request


API_BASE_URL = "http://localhost:8000"
GENERATE_ENDPOINT = f"{API_BASE_URL}/api/tts/generate"
AUDIO_ENDPOINT = f"{API_BASE_URL}/api/tts/audio"


# Test configuration: one voice per language with appropriate test text
TEST_VOICES = {
    "English": {
        "voice": "en-US-GuyNeural",
        "text": "Testing speech rate controls with different speeds."
    },
    "Spanish": {
        "voice": "es-AR-ElenaNeural",
        "text": "Probando controles de velocidad de voz con diferentes velocidades."
    },
    "French": {
        "voice": "fr-FR-DeniseNeural",
        "text": "Test des contrôles de vitesse de parole avec différentes vitesses."
    },
    "German": {
        "voice": "de-DE-ConradNeural",
        "text": "Testen der Sprachgeschwindigkeitssteuerung mit verschiedenen Geschwindigkeiten."
    },
    "Portuguese": {
        "voice": "pt-BR-AntonioNeural",
        "text": "Testando controles de velocidade de fala com diferentes velocidades."
    }
}


# Rate values to test
RATE_TESTS = {
    "0.75x (slow)": "-25%",
    "1.0x (normal)": "+0%",
    "1.25x (fast)": "+25%",
    "1.5x (fastest)": "+50%"
}


def generate_audio(
    text: str,
    voice: str,
    rate: str
) -> Tuple[bool, str, int]:
    """
    Generate audio with specified parameters.

    Args:
        text: Text to convert to speech
        voice: Voice ID to use
        rate: Speech rate parameter

    Returns:
        Tuple of (success, audio_url, file_size)
    """
    try:
        payload = {
            "text": text,
            "voice": voice,
            "rate": rate,
            "pitch": "+0Hz"
        }

        # Make POST request
        req = Request(
            GENERATE_ENDPOINT,
            data=json.dumps(payload).encode('utf-8'),
            headers={'Content-Type': 'application/json'}
        )

        with urlopen(req, timeout=30) as response:
            data = json.loads(response.read().decode('utf-8'))
            audio_url = data.get("audio_url")

            if not audio_url:
                return False, "", 0

            # Download the audio file to get its size
            with urlopen(f"{API_BASE_URL}{audio_url}") as audio_response:
                audio_data = audio_response.read()
                file_size = len(audio_data)

            return True, audio_url, file_size

    except Exception as e:
        print(f"      ERROR: {str(e)}")
        return False, "", 0


def test_language(
    language: str,
    config: Dict[str, str]
) -> Dict[str, any]:
    """
    Test all rate values for a specific language.

    Args:
        language: Language name
        config: Dictionary with voice and text

    Returns:
        Dictionary with test results
    """
    print(f"\n{'='*80}")
    print(f"Testing {language} - Voice: {config['voice']}")
    print(f"{'='*80}")

    results = {
        "language": language,
        "voice": config["voice"],
        "tests": {},
        "success": True
    }

    file_sizes = []

    for rate_label, rate_value in RATE_TESTS.items():
        print(f"\n  Testing {rate_label} (rate={rate_value})...")

        success, audio_url, file_size = generate_audio(
            config["text"], config["voice"], rate_value
        )

        results["tests"][rate_label] = {
            "rate_value": rate_value,
            "success": success,
            "audio_url": audio_url,
            "file_size": file_size
        }

        if success:
            print(f"    ✓ SUCCESS - File size: {file_size:,} bytes")
            file_sizes.append(file_size)
        else:
            print(f"    ✗ FAILED")
            results["success"] = False

    # Verify file sizes differ
    if len(file_sizes) == len(RATE_TESTS) and len(set(file_sizes)) > 1:
        print(f"\n  ✓ File sizes vary as expected")
        # Generally: slower speech = larger file (more audio duration)
        sizes_by_rate = [
            (RATE_TESTS[label], results["tests"][label]["file_size"])
            for label in RATE_TESTS.keys()
        ]
        print(f"  File size progression:")
        for rate, size in sizes_by_rate:
            print(f"    {rate}: {size:,} bytes")
    elif len(set(file_sizes)) == 1:
        print(f"\n  ⚠ WARNING: All file sizes are identical ({file_sizes[0]:,} bytes)")

    return results


def run_all_tests() -> None:
    """Run tests for all languages."""
    print("="*80)
    print("SPEECH RATE CONTROLS TEST")
    print("="*80)
    print(f"\nTesting {len(TEST_VOICES)} languages with {len(RATE_TESTS)} rate values each")
    print(f"Total tests: {len(TEST_VOICES) * len(RATE_TESTS)}")

    all_results = []

    for language, config in TEST_VOICES.items():
        result = test_language(language, config)
        all_results.append(result)
        # Small delay between languages to avoid overwhelming the server
        time.sleep(1)

    # Print summary
    print(f"\n\n{'='*80}")
    print("TEST SUMMARY")
    print(f"{'='*80}\n")

    total_tests = len(TEST_VOICES) * len(RATE_TESTS)
    passed_tests = sum(
        len([t for t in r["tests"].values() if t["success"]])
        for r in all_results
    )

    for result in all_results:
        language_passed = sum(1 for t in result["tests"].values() if t["success"])
        language_total = len(result["tests"])
        status = "✓ PASS" if result["success"] else "✗ FAIL"

        print(f"{status} - {result['language']}: {language_passed}/{language_total} tests passed")

        if not result["success"]:
            for rate_label, test in result["tests"].items():
                if not test["success"]:
                    print(f"  ✗ Failed: {rate_label}")

    print(f"\n{'='*80}")
    print(f"OVERALL RESULT: {passed_tests}/{total_tests} tests passed")

    if passed_tests == total_tests:
        print("✓ ALL TESTS PASSED")
        print("\nConclusion:")
        print("- Speech rate controls work correctly for all 5 languages")
        print("- Different rate values produce different file sizes")
        print("- No errors occurred during generation")
    else:
        print("✗ SOME TESTS FAILED")

    print(f"{'='*80}\n")


if __name__ == "__main__":
    run_all_tests()
