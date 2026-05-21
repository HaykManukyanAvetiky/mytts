"""
Test pitch controls for all new language voices.
Tests -20%, 0%, and +20% pitch adjustments.
"""
import asyncio
import httpx
from pathlib import Path
from typing import List, Dict, Any


# Test configuration
BASE_URL = "http://localhost:8000"
OUTPUT_DIR = Path("/Users/haykmanukyan/work/mytts/test_pitch_output")

# Test voices - one per language
TEST_VOICES = [
    {
        "language": "English",
        "voice": "en-US-GuyNeural",
        "text": "Testing pitch control with English voice."
    },
    {
        "language": "Spanish",
        "voice": "es-AR-ElenaNeural",
        "text": "Probando el control de tono con voz española."
    },
    {
        "language": "French",
        "voice": "fr-FR-DeniseNeural",
        "text": "Test du contrôle de la hauteur avec une voix française."
    },
    {
        "language": "German",
        "voice": "de-DE-ConradNeural",
        "text": "Testen der Tonhöhenregelung mit deutscher Stimme."
    },
    {
        "language": "Portuguese",
        "voice": "pt-BR-AntonioNeural",
        "text": "Testando o controle de tom com voz portuguesa."
    }
]

# Pitch values to test
PITCH_VALUES = [
    {"label": "-20%", "value": "-10%"},
    {"label": "0%", "value": "+0Hz"},
    {"label": "+20%", "value": "+10%"}
]


async def test_pitch_control(
    client: httpx.AsyncClient,
    voice: str,
    language: str,
    text: str,
    pitch_label: str,
    pitch_value: str
) -> Dict[str, Any]:
    """Test TTS generation with specific pitch value."""

    request_data = {
        "text": text,
        "voice": voice,
        "pitch": pitch_value
    }

    try:
        response = await client.post(
            f"{BASE_URL}/api/tts/generate",
            json=request_data,
            timeout=30.0
        )

        if response.status_code == 200:
            # Save the audio file
            filename = f"{language}_{voice}_{pitch_label.replace('%', 'pct')}.mp3"
            output_path = OUTPUT_DIR / filename

            output_path.write_bytes(response.content)
            file_size = len(response.content)

            return {
                "success": True,
                "language": language,
                "voice": voice,
                "pitch": pitch_label,
                "pitch_value": pitch_value,
                "file_size": file_size,
                "output_file": str(output_path)
            }
        else:
            return {
                "success": False,
                "language": language,
                "voice": voice,
                "pitch": pitch_label,
                "pitch_value": pitch_value,
                "error": f"HTTP {response.status_code}: {response.text}"
            }

    except Exception as e:
        return {
            "success": False,
            "language": language,
            "voice": voice,
            "pitch": pitch_label,
            "pitch_value": pitch_value,
            "error": str(e)
        }


async def run_tests() -> None:
    """Run all pitch control tests."""

    # Create output directory
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    print("=" * 80)
    print("PITCH CONTROL TEST SUITE")
    print("=" * 80)
    print(f"\nTesting {len(TEST_VOICES)} languages x {len(PITCH_VALUES)} pitch values = {len(TEST_VOICES) * len(PITCH_VALUES)} total tests\n")

    results: List[Dict[str, Any]] = []

    async with httpx.AsyncClient() as client:
        for voice_config in TEST_VOICES:
            language = voice_config["language"]
            voice = voice_config["voice"]
            text = voice_config["text"]

            print(f"\n{language} ({voice}):")
            print("-" * 80)

            for pitch_config in PITCH_VALUES:
                pitch_label = pitch_config["label"]
                pitch_value = pitch_config["value"]

                print(f"  Testing pitch {pitch_label} ({pitch_value})...", end=" ")

                result = await test_pitch_control(
                    client=client,
                    voice=voice,
                    language=language,
                    text=text,
                    pitch_label=pitch_label,
                    pitch_value=pitch_value
                )

                results.append(result)

                if result["success"]:
                    file_size_kb = result["file_size"] / 1024
                    print(f"✓ SUCCESS ({file_size_kb:.1f} KB)")
                else:
                    print(f"✗ FAILED - {result['error']}")

    # Print summary
    print("\n" + "=" * 80)
    print("TEST SUMMARY")
    print("=" * 80)

    successful = [r for r in results if r["success"]]
    failed = [r for r in results if not r["success"]]

    print(f"\nTotal Tests: {len(results)}")
    print(f"Passed: {len(successful)} ✓")
    print(f"Failed: {len(failed)} ✗")
    print(f"Success Rate: {len(successful) / len(results) * 100:.1f}%")

    if failed:
        print("\nFailed Tests:")
        for result in failed:
            print(f"  - {result['language']} ({result['voice']}) at {result['pitch']}: {result['error']}")

    # Summary by language
    print("\n" + "-" * 80)
    print("Results by Language:")
    print("-" * 80)

    for voice_config in TEST_VOICES:
        language = voice_config["language"]
        voice = voice_config["voice"]

        lang_results = [r for r in results if r["language"] == language]
        lang_success = [r for r in lang_results if r["success"]]

        status = "✓ PASS" if len(lang_success) == len(PITCH_VALUES) else "✗ FAIL"
        print(f"{language:12} ({voice:25}): {len(lang_success)}/{len(PITCH_VALUES)} {status}")

    # Output directory info
    print("\n" + "-" * 80)
    print(f"Audio files saved to: {OUTPUT_DIR}")
    print("-" * 80)

    if len(successful) == len(results):
        print("\n✓ ALL TESTS PASSED!")
    else:
        print(f"\n✗ {len(failed)} TEST(S) FAILED")


if __name__ == "__main__":
    asyncio.run(run_tests())
