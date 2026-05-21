#!/usr/bin/env python3
"""Test ALL failed Spanish voices to determine if they're truly unavailable."""

import asyncio
from pathlib import Path
import edge_tts


# ALL voices that failed to generate previews (0-byte files)
FAILED_VOICES = [
    # Spain - 17 failed voices
    "es-ES-AbrilNeural",
    "es-ES-ArabellaMultilingualNeural",
    "es-ES-ArnauNeural",
    "es-ES-DarioNeural",
    "es-ES-EliasNeural",
    "es-ES-EstrellaNeural",
    "es-ES-IreneNeural",
    "es-ES-IsidoraMultilingualNeural",
    "es-ES-LaiaNeural",
    "es-ES-LiaNeural",
    "es-ES-NilNeural",
    "es-ES-SaulNeural",
    "es-ES-TeoNeural",
    "es-ES-TrianaNeural",
    "es-ES-TristanMultilingualNeural",
    "es-ES-VeraNeural",
    "es-ES-XimenaMultilingualNeural",
    # Mexico - 14 failed voices
    "es-MX-BeatrizNeural",
    "es-MX-CandelaNeural",
    "es-MX-CarlotaNeural",
    "es-MX-CecilioNeural",
    "es-MX-DaliaMultilingualNeural",
    "es-MX-GerardoNeural",
    "es-MX-JorgeMultilingualNeural",
    "es-MX-LarissaNeural",
    "es-MX-LibertoNeural",
    "es-MX-LucianoNeural",
    "es-MX-MarinaNeural",
    "es-MX-NuriaNeural",
    "es-MX-PelayoNeural",
    "es-MX-RenataNeural",
    "es-MX-YagoNeural",
]

TEST_TEXT = "Hola, esta es una prueba de voz."
OUTPUT_DIR = Path("/tmp/failed_voice_tests")


async def test_voice(voice_id: str) -> tuple[str, bool, int, str]:
    """Test if a voice can generate audio.

    Returns:
        Tuple of (voice_id, success, file_size_bytes, error_message)
    """
    output_file = OUTPUT_DIR / f"{voice_id}.mp3"

    try:
        communicate = edge_tts.Communicate(text=TEST_TEXT, voice=voice_id)
        await communicate.save(str(output_file))

        # Check if file has content
        file_size = output_file.stat().st_size
        success = file_size > 0

        return (voice_id, success, file_size, "")
    except Exception as e:
        return (voice_id, False, 0, str(e))


async def main():
    """Test all failed voices and report results."""
    # Create output directory
    OUTPUT_DIR.mkdir(exist_ok=True)

    print(f"Testing {len(FAILED_VOICES)} failed Spanish voices...")
    print("=" * 80)

    # Test all voices concurrently (in batches to avoid overwhelming the service)
    batch_size = 5
    all_results = []

    for i in range(0, len(FAILED_VOICES), batch_size):
        batch = FAILED_VOICES[i:i + batch_size]
        print(f"Testing batch {i//batch_size + 1}/{(len(FAILED_VOICES) + batch_size - 1)//batch_size}...")
        results = await asyncio.gather(*[test_voice(voice) for voice in batch])
        all_results.extend(results)
        # Small delay between batches
        if i + batch_size < len(FAILED_VOICES):
            await asyncio.sleep(1)

    # Categorize results
    working_voices = []
    failed_voices = []

    for voice_id, success, file_size, error_msg in all_results:
        if success:
            working_voices.append((voice_id, file_size))
        else:
            failed_voices.append((voice_id, error_msg))

    # Print results
    print("\n" + "=" * 80)
    print("RESULTS:")
    print("=" * 80)

    if working_voices:
        print(f"\nWORKING VOICES ({len(working_voices)}):")
        print("-" * 80)
        for voice_id, file_size in sorted(working_voices):
            print(f"  ✓ {voice_id:45} {file_size:>8} bytes")

    if failed_voices:
        print(f"\nFAILED VOICES ({len(failed_voices)}):")
        print("-" * 80)
        for voice_id, error_msg in sorted(failed_voices):
            print(f"  ✗ {voice_id}")

    # Summary
    print("\n" + "=" * 80)
    print(f"SUMMARY: {len(working_voices)} working, {len(failed_voices)} failed out of {len(FAILED_VOICES)} tested")
    print("=" * 80)

    # Recommendation
    if failed_voices:
        print("\nRECOMMENDATION:")
        print(f"The following {len(failed_voices)} voices should be REMOVED from backend/config.py:")
        print("They are NOT available in Edge TTS and will always fail.")
        print()
        for voice_id, _ in sorted(failed_voices):
            print(f"  - {voice_id}")

    if working_voices:
        print("\nNOTE:")
        print(f"The following {len(working_voices)} voices ARE working:")
        print("Their preview generation likely failed due to temporary network issues.")
        print("They should REMAIN in the config.")
        print()
        for voice_id, _ in sorted(working_voices):
            print(f"  - {voice_id}")


if __name__ == "__main__":
    asyncio.run(main())
