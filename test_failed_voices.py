#!/usr/bin/env python3
"""Test failed Spanish voices to determine if they're truly unavailable."""

import asyncio
from pathlib import Path
import edge_tts


# Voices that failed to generate previews (0-byte files)
FAILED_VOICES = [
    # Spain
    "es-ES-AbrilNeural",
    "es-ES-DarioNeural",
    "es-ES-ElviraNeural",  # Should work - was in original test
    # Mexico
    "es-MX-BeatrizNeural",
    "es-MX-DaliaNeural",  # Should work - was in original test
]

TEST_TEXT = "Hola, esta es una prueba de voz."
OUTPUT_DIR = Path("/tmp/failed_voice_tests")


async def test_voice(voice_id: str) -> tuple[str, bool, int]:
    """Test if a voice can generate audio.

    Returns:
        Tuple of (voice_id, success, file_size_bytes)
    """
    output_file = OUTPUT_DIR / f"{voice_id}.mp3"

    try:
        communicate = edge_tts.Communicate(text=TEST_TEXT, voice=voice_id)
        await communicate.save(str(output_file))

        # Check if file has content
        file_size = output_file.stat().st_size
        success = file_size > 0

        return (voice_id, success, file_size)
    except Exception as e:
        print(f"Error testing {voice_id}: {e}")
        return (voice_id, False, 0)


async def main():
    """Test all failed voices and report results."""
    # Create output directory
    OUTPUT_DIR.mkdir(exist_ok=True)

    print("Testing failed Spanish voices...")
    print("=" * 80)

    # Test all voices
    results = await asyncio.gather(*[test_voice(voice) for voice in FAILED_VOICES])

    # Categorize results
    working_voices = []
    failed_voices = []

    for voice_id, success, file_size in results:
        if success:
            working_voices.append((voice_id, file_size))
        else:
            failed_voices.append(voice_id)

    # Print results
    print("\nRESULTS:")
    print("=" * 80)

    if working_voices:
        print(f"\nWORKING VOICES ({len(working_voices)}):")
        print("-" * 80)
        for voice_id, file_size in working_voices:
            print(f"  ✓ {voice_id:45} {file_size:>8} bytes")

    if failed_voices:
        print(f"\nFAILED VOICES ({len(failed_voices)}):")
        print("-" * 80)
        for voice_id in failed_voices:
            print(f"  ✗ {voice_id}")

    # Summary
    print("\n" + "=" * 80)
    print(f"SUMMARY: {len(working_voices)} working, {len(failed_voices)} failed")
    print("=" * 80)

    # Recommendation
    if failed_voices:
        print("\nRECOMMENDATION:")
        print("The following voices should be REMOVED from backend/config.py:")
        for voice_id in failed_voices:
            print(f"  - {voice_id}")
    else:
        print("\nAll tested voices are working!")
        print("The failed previews were likely due to temporary network issues.")


if __name__ == "__main__":
    asyncio.run(main())
