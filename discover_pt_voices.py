#!/usr/bin/env python3
"""Discover all Portuguese voices from Edge TTS."""
import asyncio
import edge_tts


async def list_portuguese_voices():
    """List all available Portuguese voices with details."""
    voices = await edge_tts.list_voices()

    # Filter for Portuguese voices (pt-BR and pt-PT)
    pt_voices = [v for v in voices if v["Locale"].startswith("pt-")]

    print(f"Total Portuguese voices found: {len(pt_voices)}\n")
    print("=" * 80)

    for voice in pt_voices:
        print(f"Voice ID: {voice['ShortName']}")
        print(f"Name: {voice['FriendlyName']}")
        print(f"Gender: {voice['Gender']}")
        print(f"Locale: {voice['Locale']}")
        print(f"LocaleName: {voice.get('LocaleName', 'N/A')}")
        print(f"Content Categories: {', '.join(voice.get('ContentCategories', []))}")
        print(f"Voice Personalities: {', '.join(voice.get('VoicePersonalities', []))}")
        print(f"All fields: {list(voice.keys())}")
        print("-" * 80)


if __name__ == "__main__":
    asyncio.run(list_portuguese_voices())
