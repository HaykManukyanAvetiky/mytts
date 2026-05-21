#!/usr/bin/env python3
"""Test script to verify English voices remain the default and work correctly."""

import asyncio
import sys
from pathlib import Path

import httpx


BASE_URL = "http://localhost:8000"
EXPECTED_ENGLISH_VOICES = [
    "en-US-GuyNeural",
    "en-US-JennyNeural",
    "en-GB-RyanNeural",
    "en-GB-SoniaNeural",
    "en-AU-NatashaNeural",
]
DEFAULT_VOICE = "en-US-GuyNeural"
TEST_TEXT = "Hello, this is a test of the English voice."


class TestResult:
    """Test result container."""

    def __init__(self, name: str, passed: bool, message: str):
        self.name = name
        self.passed = passed
        self.message = message

    def __str__(self) -> str:
        status = "✓ PASS" if self.passed else "✗ FAIL"
        return f"{status}: {self.name}\n  {self.message}"


async def test_english_is_default() -> TestResult:
    """Test 1: Verify English voices appear first in the list."""
    async with httpx.AsyncClient(timeout=10.0) as client:
        try:
            response = await client.get(f"{BASE_URL}/api/tts/voices")
            response.raise_for_status()
            data = response.json()

            voices = data.get("voices", [])
            if not voices:
                return TestResult(
                    "English is default",
                    False,
                    "No voices returned from API"
                )

            # Check first voice is English
            first_voice = voices[0]
            if first_voice["id"] != DEFAULT_VOICE:
                return TestResult(
                    "English is default",
                    False,
                    f"First voice is {first_voice['id']}, expected {DEFAULT_VOICE}"
                )

            # Count English voices at the start
            english_count = 0
            for voice in voices:
                if voice["language"] == "English":
                    english_count += 1
                else:
                    break

            if english_count != 5:
                return TestResult(
                    "English is default",
                    False,
                    f"Found {english_count} English voices at start, expected 5"
                )

            return TestResult(
                "English is default",
                True,
                f"First voice is {DEFAULT_VOICE}, followed by 4 more English voices"
            )

        except httpx.HTTPError as e:
            return TestResult(
                "English is default",
                False,
                f"HTTP error: {e}"
            )
        except Exception as e:
            return TestResult(
                "English is default",
                False,
                f"Unexpected error: {e}"
            )


async def test_english_voice_count() -> TestResult:
    """Test 2: Verify there are exactly 5 English voices."""
    async with httpx.AsyncClient(timeout=10.0) as client:
        try:
            response = await client.get(f"{BASE_URL}/api/tts/voices")
            response.raise_for_status()
            data = response.json()

            voices = data.get("voices", [])
            english_voices = [v for v in voices if v["language"] == "English"]

            if len(english_voices) != 5:
                return TestResult(
                    "English voice count",
                    False,
                    f"Found {len(english_voices)} English voices, expected 5"
                )

            # Verify all expected voices are present
            voice_ids = [v["id"] for v in english_voices]
            missing = set(EXPECTED_ENGLISH_VOICES) - set(voice_ids)
            extra = set(voice_ids) - set(EXPECTED_ENGLISH_VOICES)

            if missing:
                return TestResult(
                    "English voice count",
                    False,
                    f"Missing voices: {missing}"
                )

            if extra:
                return TestResult(
                    "English voice count",
                    False,
                    f"Extra voices: {extra}"
                )

            return TestResult(
                "English voice count",
                True,
                f"All 5 English voices present: {', '.join(voice_ids)}"
            )

        except httpx.HTTPError as e:
            return TestResult(
                "English voice count",
                False,
                f"HTTP error: {e}"
            )
        except Exception as e:
            return TestResult(
                "English voice count",
                False,
                f"Unexpected error: {e}"
            )


async def test_english_tts_generation() -> TestResult:
    """Test 3: Test English TTS generation."""
    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            # Generate audio with English voice
            payload = {
                "text": TEST_TEXT,
                "voice": DEFAULT_VOICE,
                "rate": "+0%",
                "pitch": "+0Hz"
            }

            response = await client.post(f"{BASE_URL}/api/tts/generate", json=payload)
            response.raise_for_status()
            data = response.json()

            audio_url = data.get("audio_url")
            if not audio_url:
                return TestResult(
                    "English TTS generation",
                    False,
                    "No audio_url in response"
                )

            # Try to fetch the audio file
            audio_response = await client.get(f"{BASE_URL}{audio_url}")
            audio_response.raise_for_status()

            audio_size = len(audio_response.content)
            if audio_size < 1000:  # MP3 should be at least 1KB
                return TestResult(
                    "English TTS generation",
                    False,
                    f"Audio file too small: {audio_size} bytes"
                )

            return TestResult(
                "English TTS generation",
                True,
                f"Generated audio with {DEFAULT_VOICE}, size: {audio_size} bytes"
            )

        except httpx.HTTPError as e:
            return TestResult(
                "English TTS generation",
                False,
                f"HTTP error: {e}"
            )
        except Exception as e:
            return TestResult(
                "English TTS generation",
                False,
                f"Unexpected error: {e}"
            )


def test_default_voice_config() -> TestResult:
    """Test 4: Verify default_voice setting in config."""
    try:
        config_path = Path("/Users/haykmanukyan/work/mytts/backend/config.py")
        if not config_path.exists():
            return TestResult(
                "Default voice config",
                False,
                f"Config file not found: {config_path}"
            )

        config_content = config_path.read_text()

        # Check if default_voice is set to en-US-GuyNeural
        if f'default_voice: str = "{DEFAULT_VOICE}"' in config_content:
            return TestResult(
                "Default voice config",
                True,
                f"default_voice is correctly set to {DEFAULT_VOICE}"
            )
        else:
            return TestResult(
                "Default voice config",
                False,
                f"default_voice is not set to {DEFAULT_VOICE} in config"
            )

    except Exception as e:
        return TestResult(
            "Default voice config",
            False,
            f"Error reading config: {e}"
        )


async def main():
    """Run all tests and report results."""
    print("=" * 70)
    print("Testing English Voices After Multilingual Update")
    print("=" * 70)
    print()

    # Run all tests
    results = []

    print("Running Test 1: Verify English is still the default...")
    results.append(await test_english_is_default())

    print("Running Test 2: Verify English voice count...")
    results.append(await test_english_voice_count())

    print("Running Test 3: Test English TTS generation...")
    results.append(await test_english_tts_generation())

    print("Running Test 4: Verify default_voice setting...")
    results.append(test_default_voice_config())

    print()
    print("=" * 70)
    print("Test Results")
    print("=" * 70)
    print()

    # Print results
    for result in results:
        print(result)
        print()

    # Summary
    passed = sum(1 for r in results if r.passed)
    total = len(results)

    print("=" * 70)
    print(f"Summary: {passed}/{total} tests passed")
    print("=" * 70)

    # Exit with appropriate code
    sys.exit(0 if passed == total else 1)


if __name__ == "__main__":
    asyncio.run(main())
