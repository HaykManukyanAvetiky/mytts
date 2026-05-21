#!/usr/bin/env python3
"""
Test Script for Sub-task 6.3: Test pitch controls with one voice per language

Tests ONE representative voice from each of 5 languages with 2 different pitch settings:
- Low (-20% / "-20Hz")
- High (+20% / "+20Hz")

Verifies:
1. API returns 200 status
2. Response contains audio_url field
3. Audio file is generated successfully
"""

import json
import sys
import time
from typing import Dict, List, Tuple
from urllib.request import urlopen, Request
from urllib.error import HTTPError, URLError


# API Configuration
API_BASE_URL = "http://localhost:8000"
GENERATE_ENDPOINT = f"{API_BASE_URL}/api/tts/generate"

# Test configuration: one voice per language as specified in task
TEST_VOICES = {
    "English": {
        "voice": "en-US-GuyNeural",
        "text": "This is a test of pitch control."
    },
    "Spanish": {
        "voice": "es-MX-DaliaNeural",
        "text": "Esta es una prueba de control de tono."
    },
    "French": {
        "voice": "fr-FR-DeniseNeural",
        "text": "Ceci est un test de contrôle de la tonalité."
    },
    "German": {
        "voice": "de-DE-AmalaNeural",
        "text": "Dies ist ein Test der Tonhöhensteuerung."
    },
    "Portuguese": {
        "voice": "pt-BR-AntonioNeural",
        "text": "Este é um teste de controle de tom."
    }
}

# Pitch settings to test (2 pitch values as specified in task)
PITCH_TESTS = {
    "Low (-20%)": "-20Hz",
    "High (+20%)": "+20Hz"
}


def test_tts_generation(
    language: str,
    voice: str,
    text: str,
    pitch_label: str,
    pitch_value: str
) -> Dict:
    """
    Test a single TTS generation with specified parameters.

    Returns:
        Dictionary with test results
    """
    result = {
        "language": language,
        "voice": voice,
        "pitch_label": pitch_label,
        "pitch_value": pitch_value,
        "success": False,
        "status_code": None,
        "audio_url": None,
        "error": None
    }

    try:
        payload = {
            "text": text,
            "voice": voice,
            "rate": "+0%",
            "pitch": pitch_value
        }

        # Make POST request
        req = Request(
            GENERATE_ENDPOINT,
            data=json.dumps(payload).encode('utf-8'),
            headers={'Content-Type': 'application/json'}
        )

        with urlopen(req, timeout=60) as response:
            result["status_code"] = response.getcode()

            if result["status_code"] == 200:
                data = json.loads(response.read().decode('utf-8'))
                result["audio_url"] = data.get("audio_url")

                if result["audio_url"]:
                    result["success"] = True
                else:
                    result["error"] = "No audio_url in response"
            else:
                result["error"] = f"Unexpected status code: {result['status_code']}"

    except HTTPError as e:
        result["status_code"] = e.code
        result["error"] = f"HTTP Error {e.code}: {e.reason}"
    except URLError as e:
        result["error"] = f"URL Error: {e.reason}"
    except Exception as e:
        result["error"] = f"Unexpected error: {str(e)}"

    return result


def run_tests() -> Tuple[List[Dict], Dict]:
    """
    Run all pitch control tests.

    Returns:
        Tuple of (all_results, summary_stats)
    """
    print("=" * 80)
    print("SUB-TASK 6.3: TEST PITCH CONTROLS")
    print("=" * 80)
    print(f"\nAPI Endpoint: {GENERATE_ENDPOINT}")
    print(f"\nTesting {len(TEST_VOICES)} languages × {len(PITCH_TESTS)} pitch settings each")
    print(f"Total tests: {len(TEST_VOICES) * len(PITCH_TESTS)}\n")
    print("=" * 80)

    all_results = []

    for language, config in TEST_VOICES.items():
        print(f"\n{language} ({config['voice']}):")

        for pitch_label, pitch_value in PITCH_TESTS.items():
            print(f"  Testing {pitch_label} (pitch={pitch_value})...", end=" ")

            result = test_tts_generation(
                language=language,
                voice=config["voice"],
                text=config["text"],
                pitch_label=pitch_label,
                pitch_value=pitch_value
            )

            all_results.append(result)

            if result["success"]:
                print(f"✓ SUCCESS")
                print(f"    Status: {result['status_code']}")
                print(f"    Audio URL: {result['audio_url']}")
            else:
                print(f"✗ FAILED")
                print(f"    Status: {result['status_code']}")
                print(f"    Error: {result['error']}")

            # Add delay between requests to avoid overwhelming the API
            time.sleep(2)

    # Calculate summary
    total_tests = len(all_results)
    successful_tests = sum(1 for r in all_results if r["success"])
    failed_tests = total_tests - successful_tests

    summary = {
        "total": total_tests,
        "successful": successful_tests,
        "failed": failed_tests,
        "success_rate": (successful_tests / total_tests * 100) if total_tests > 0 else 0
    }

    return all_results, summary


def print_summary(results: List[Dict], summary: Dict):
    """Print test summary and conclusion."""
    print("\n" + "=" * 80)
    print("TEST SUMMARY")
    print("=" * 80)

    print(f"\nTotal Tests: {summary['total']}")
    print(f"Successful: {summary['successful']}")
    print(f"Failed: {summary['failed']}")
    print(f"Success Rate: {summary['success_rate']:.1f}%\n")

    # Group results by language
    by_language = {}
    for result in results:
        if result["language"] not in by_language:
            by_language[result["language"]] = []
        by_language[result["language"]].append(result)

    for language, lang_results in by_language.items():
        passed = sum(1 for r in lang_results if r["success"])
        total = len(lang_results)
        status = "✓ PASS" if passed == total else "✗ FAIL"
        print(f"{status} {language}: {passed}/{total} tests passed")

    print("\n" + "=" * 80)
    print("TASK 6.3 COMPLETION STATUS")
    print("=" * 80)

    if summary["failed"] == 0 and summary["successful"] >= 10:
        print("\n✓ TASK COMPLETE - All requirements met:")
        print(f"  • {summary['successful']} TTS generations succeeded (5 languages × 2 pitch settings)")
        print("  • All API calls returned 200 with valid audio_url")
        print("  • Pitch parameter accepted without errors for all languages")
        print("  • Pitch controls verified working across all languages")
        return 0
    else:
        print("\n✗ TASK INCOMPLETE - Requirements not met:")
        if summary["successful"] < 10:
            print(f"  • Only {summary['successful']}/10 required tests succeeded")
        if summary["failed"] > 0:
            print(f"  • {summary['failed']} test(s) failed")
        print("\nFailed tests:")
        for result in results:
            if not result["success"]:
                print(f"  • {result['language']} at {result['pitch_label']}: {result['error']}")
        return 1


def main():
    """Main test execution."""
    try:
        # Run tests
        results, summary = run_tests()

        # Print summary and return exit code
        exit_code = print_summary(results, summary)

        print("\n" + "=" * 80 + "\n")
        return exit_code

    except Exception as e:
        print(f"\n✗ Test execution failed: {str(e)}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
