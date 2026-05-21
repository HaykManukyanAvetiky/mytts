#!/usr/bin/env python3
"""Test all Portuguese voices to ensure they work correctly."""
import asyncio
import edge_tts
from pathlib import Path


PORTUGUESE_VOICES = [
    # Brazilian Portuguese
    "pt-BR-AntonioNeural",
    "pt-BR-FranciscaNeural",
    "pt-BR-ThalitaMultilingualNeural",
    # European Portuguese
    "pt-PT-DuarteNeural",
    "pt-PT-RaquelNeural",
]

TEST_TEXT = "Olá, este é um teste de síntese de voz em português."


async def test_voice(voice_id: str, output_dir: Path) -> bool:
    """Test a single voice by generating a short audio sample."""
    try:
        communicate = edge_tts.Communicate(text=TEST_TEXT, voice=voice_id)
        output_file = output_dir / f"{voice_id}.mp3"

        await communicate.save(str(output_file))

        if output_file.exists() and output_file.stat().st_size > 0:
            print(f"✓ {voice_id:40} - SUCCESS ({output_file.stat().st_size} bytes)")
            return True
        else:
            print(f"✗ {voice_id:40} - FAILED (no output)")
            return False

    except Exception as e:
        print(f"✗ {voice_id:40} - ERROR: {e}")
        return False


async def test_all_voices():
    """Test all Portuguese voices."""
    output_dir = Path("/tmp/mytts_pt_test")
    output_dir.mkdir(exist_ok=True)

    print("Testing Portuguese Voices")
    print("=" * 80)
    print(f"Test text: '{TEST_TEXT}'")
    print(f"Output directory: {output_dir}")
    print("=" * 80)

    results = []
    for voice_id in PORTUGUESE_VOICES:
        success = await test_voice(voice_id, output_dir)
        results.append((voice_id, success))

    print("=" * 80)
    successful = sum(1 for _, success in results if success)
    print(f"\nResults: {successful}/{len(PORTUGUESE_VOICES)} voices tested successfully")

    if successful == len(PORTUGUESE_VOICES):
        print("All Portuguese voices are working correctly!")
    else:
        print("\nFailed voices:")
        for voice_id, success in results:
            if not success:
                print(f"  - {voice_id}")


if __name__ == "__main__":
    asyncio.run(test_all_voices())
