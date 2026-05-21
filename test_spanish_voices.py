"""Test script for Spanish voices in MyTTS API.

This script verifies that:
1. Spanish voices are correctly returned by the /api/tts/voices endpoint
2. TTS generation works with Spanish voices and Spanish text
3. Different regional Spanish voices generate valid audio files
"""

import asyncio
from pathlib import Path
from typing import Any

import httpx
from pydantic import BaseModel


class VoiceInfo(BaseModel):
    """Voice metadata model."""
    id: str
    name: str
    gender: str
    accent: str
    language: str
    style: str
    description: str
    preview_file: str


class VoiceListResponse(BaseModel):
    """Response model for voice list endpoint."""
    voices: list[VoiceInfo]


class TTSGenerateRequest(BaseModel):
    """Request model for TTS generation."""
    text: str
    voice: str | None = None
    rate: str = "+0%"
    pitch: str = "+0Hz"


class TTSGenerateResponse(BaseModel):
    """Response model for TTS generation."""
    audio_url: str
    filename: str
    character_count: int
    generated_at: str


# Test configuration
BASE_URL = "http://localhost:8000"
SAMPLE_SPANISH_TEXT = "Hola, esta es una prueba de voz en español."

# Test voices from different Spanish-speaking regions
TEST_VOICES = [
    {"id": "es-ES-ElviraNeural", "region": "Spain", "name": "Elvira"},
    {"id": "es-MX-DaliaNeural", "region": "Mexico", "name": "Dalia"},
    {"id": "es-AR-ElenaNeural", "region": "Argentina", "name": "Elena"},
]


async def test_voices_endpoint() -> dict[str, Any]:
    """Test that Spanish voices are returned by the /api/tts/voices endpoint.

    Returns:
        dict: Test results with pass/fail status and details
    """
    print("\n" + "="*80)
    print("TEST 1: Verify Spanish voices in /api/tts/voices endpoint")
    print("="*80)

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{BASE_URL}/api/tts/voices")
            response.raise_for_status()

            data = VoiceListResponse(**response.json())
            voices = data.voices

            # Count Spanish voices
            spanish_voices = [v for v in voices if v.language == "Spanish"]
            english_voices = [v for v in voices if v.language == "English"]

            total_voices = len(voices)
            spanish_count = len(spanish_voices)
            english_count = len(english_voices)

            print(f"\nTotal voices: {total_voices}")
            print(f"English voices: {english_count}")
            print(f"Spanish voices: {spanish_count}")

            # Expected: 5 English + 77 Spanish = 82 total
            expected_total = 82
            expected_spanish = 77

            # Check regions
            spanish_regions = {}
            for voice in spanish_voices:
                region = voice.accent
                if region not in spanish_regions:
                    spanish_regions[region] = []
                spanish_regions[region].append(voice.id)

            print(f"\nSpanish voice regions ({len(spanish_regions)} regions):")
            for region in sorted(spanish_regions.keys()):
                print(f"  - {region}: {len(spanish_regions[region])} voices")

            # Verify test voices exist
            test_voice_ids = [v["id"] for v in TEST_VOICES]
            missing_voices = []
            for test_voice in TEST_VOICES:
                voice_id = test_voice["id"]
                if not any(v.id == voice_id for v in voices):
                    missing_voices.append(voice_id)
                else:
                    print(f"\n✓ Found test voice: {voice_id} ({test_voice['name']}, {test_voice['region']})")

            # Determine pass/fail
            passed = (
                total_voices == expected_total and
                spanish_count == expected_spanish and
                len(missing_voices) == 0
            )

            result = {
                "test": "voices_endpoint",
                "passed": passed,
                "total_voices": total_voices,
                "spanish_voices": spanish_count,
                "english_voices": english_count,
                "expected_total": expected_total,
                "expected_spanish": expected_spanish,
                "regions": len(spanish_regions),
                "missing_test_voices": missing_voices
            }

            if passed:
                print("\n✅ TEST PASSED: All Spanish voices correctly returned by API")
            else:
                print("\n❌ TEST FAILED:")
                if total_voices != expected_total:
                    print(f"  - Expected {expected_total} total voices, got {total_voices}")
                if spanish_count != expected_spanish:
                    print(f"  - Expected {expected_spanish} Spanish voices, got {spanish_count}")
                if missing_voices:
                    print(f"  - Missing test voices: {missing_voices}")

            return result

    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        return {
            "test": "voices_endpoint",
            "passed": False,
            "error": str(e)
        }


async def test_tts_generation(voice_id: str, region: str, name: str) -> dict[str, Any]:
    """Test TTS generation with a specific Spanish voice.

    Args:
        voice_id: Voice ID to test
        region: Region name for logging
        name: Voice name for logging

    Returns:
        dict: Test results with pass/fail status and details
    """
    print(f"\n  Testing voice: {voice_id} ({name}, {region})")

    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            # Generate TTS
            request_data = TTSGenerateRequest(
                text=SAMPLE_SPANISH_TEXT,
                voice=voice_id
            )

            response = await client.post(
                f"{BASE_URL}/api/tts/generate",
                json=request_data.model_dump()
            )
            response.raise_for_status()

            data = TTSGenerateResponse(**response.json())

            print(f"    ✓ Generated audio: {data.filename}")
            print(f"    ✓ Character count: {data.character_count}")
            print(f"    ✓ Audio URL: {data.audio_url}")

            # Download and verify the audio file
            audio_response = await client.get(f"{BASE_URL}{data.audio_url}")
            audio_response.raise_for_status()

            audio_content = audio_response.content
            audio_size = len(audio_content)

            print(f"    ✓ Audio file size: {audio_size:,} bytes")

            # Verify it's a valid MP3 (check for MP3 header)
            is_valid_mp3 = audio_content[:3] == b'\xff\xfb' or audio_content[:3] == b'ID3'

            if is_valid_mp3:
                print(f"    ✓ Valid MP3 file (header check passed)")
            else:
                print(f"    ⚠ Warning: MP3 header check failed")

            passed = audio_size > 0 and is_valid_mp3

            return {
                "voice_id": voice_id,
                "region": region,
                "name": name,
                "passed": passed,
                "filename": data.filename,
                "audio_size": audio_size,
                "character_count": data.character_count,
                "is_valid_mp3": is_valid_mp3
            }

    except Exception as e:
        print(f"    ❌ Failed: {e}")
        return {
            "voice_id": voice_id,
            "region": region,
            "name": name,
            "passed": False,
            "error": str(e)
        }


async def test_multiple_voices() -> dict[str, Any]:
    """Test TTS generation with multiple Spanish voices from different regions.

    Returns:
        dict: Test results with pass/fail status and details
    """
    print("\n" + "="*80)
    print("TEST 2: Generate audio with Spanish voices from different regions")
    print("="*80)
    print(f"\nSample text: \"{SAMPLE_SPANISH_TEXT}\"")

    results = []
    for voice in TEST_VOICES:
        result = await test_tts_generation(
            voice_id=voice["id"],
            region=voice["region"],
            name=voice["name"]
        )
        results.append(result)

    # Summary
    passed_count = sum(1 for r in results if r["passed"])
    failed_count = len(results) - passed_count

    print(f"\n{'='*80}")
    print(f"Summary: {passed_count}/{len(results)} voices generated audio successfully")

    if passed_count == len(results):
        print("✅ TEST PASSED: All regional voices generated valid audio")
    else:
        print(f"❌ TEST FAILED: {failed_count} voice(s) failed to generate audio")
        for result in results:
            if not result["passed"]:
                print(f"  - {result['voice_id']}: {result.get('error', 'Unknown error')}")

    return {
        "test": "multiple_voices",
        "passed": passed_count == len(results),
        "total_tested": len(results),
        "passed_count": passed_count,
        "failed_count": failed_count,
        "results": results
    }


async def main() -> None:
    """Run all tests."""
    print("\n" + "="*80)
    print("SPANISH VOICES TEST SUITE")
    print("="*80)
    print(f"Testing against: {BASE_URL}")

    # Check if server is running
    print("\nChecking server connectivity...")
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{BASE_URL}/", timeout=5.0)
            response.raise_for_status()
            print("✓ Server is running and accessible")
    except Exception as e:
        print(f"❌ ERROR: Cannot connect to server at {BASE_URL}")
        print(f"   {e}")
        print("\nPlease start the server first:")
        print("   uvicorn backend.main:app --reload")
        return

    # Run tests
    test1_result = await test_voices_endpoint()
    test2_result = await test_multiple_voices()

    # Final summary
    print("\n" + "="*80)
    print("FINAL TEST RESULTS")
    print("="*80)

    all_passed = test1_result["passed"] and test2_result["passed"]

    print(f"\nTest 1 (Voices Endpoint): {'✅ PASSED' if test1_result['passed'] else '❌ FAILED'}")
    print(f"Test 2 (Audio Generation): {'✅ PASSED' if test2_result['passed'] else '❌ FAILED'}")

    if all_passed:
        print("\n🎉 ALL TESTS PASSED!")
        print("\nSpanish voices have been successfully integrated:")
        print(f"  - {test1_result['spanish_voices']} Spanish voices available")
        print(f"  - {test1_result['regions']} regional variants")
        print(f"  - {test2_result['passed_count']} test voices generated audio successfully")
    else:
        print("\n⚠️ SOME TESTS FAILED - See details above")


if __name__ == "__main__":
    asyncio.run(main())
