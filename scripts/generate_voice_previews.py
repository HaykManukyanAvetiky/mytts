"""Generate voice preview audio files for all available voices.

This script creates short MP3 preview samples for each voice configured in the
application settings. Preview files are stored in static/audio/previews/ and
can be served to users for voice selection.
"""

import asyncio
from pathlib import Path

from backend.config import Settings
from backend.core.tts.service import EdgeTTSService

# Preview texts for each language
PREVIEW_TEXTS = {
    "English": "Hello, this is a preview of this voice. I can help you create natural-sounding speech for your videos and podcasts.",
    "Spanish": "Hola, esta es una vista previa de esta voz. Puedo ayudarte a crear un habla natural para tus videos y podcasts.",
    "French": "Bonjour, ceci est un aperçu de cette voix. Je peux vous aider à créer un discours naturel pour vos vidéos et podcasts.",
    "German": "Hallo, dies ist eine Vorschau dieser Stimme. Ich kann Ihnen helfen, natürlich klingende Sprache für Ihre Videos und Podcasts zu erstellen.",
    "Portuguese": "Olá, esta é uma prévia desta voz. Posso ajudá-lo a criar uma fala natural para seus vídeos e podcasts."
}


async def generate_previews() -> None:
    """Generate preview audio files for all available voices.

    Creates the preview directory if it doesn't exist, then generates an MP3
    file for each voice. Skips generation if the preview file already exists.
    """
    # Load settings and get available voices
    settings = Settings()
    print(f"Found {len(settings.available_voices)} voices to process")

    # Create preview directory
    preview_dir = Path("static/audio/previews")
    preview_dir.mkdir(parents=True, exist_ok=True)
    print(f"Preview directory: {preview_dir.absolute()}")

    # Initialize TTS service
    tts_service = EdgeTTSService()

    # Generate preview for each voice
    for voice in settings.available_voices:
        preview_path = preview_dir / voice.preview_file

        # Skip if preview already exists
        if preview_path.exists():
            print(f"✓ Skipping {voice.id} (preview already exists)")
            continue

        print(f"Generating preview for {voice.id} ({voice.name})...", end=" ")

        try:
            # Get the preview text for this voice's language
            preview_text = PREVIEW_TEXTS.get(
                voice.language,
                PREVIEW_TEXTS["English"]  # Fallback to English
            )

            # Generate preview audio
            await tts_service.generate(
                text=preview_text,
                voice=voice.id,
                output_path=preview_path,
            )

            # Verify file was created
            if preview_path.exists():
                file_size = preview_path.stat().st_size
                print(f"✓ Done ({file_size} bytes)")
            else:
                print("✗ Failed (file not created)")

        except Exception as e:
            print(f"✗ Error: {e}")

    print("\nPreview generation complete!")


async def main() -> None:
    """Main entry point for the script."""
    print("=" * 60)
    print("Voice Preview Generation Script")
    print("=" * 60)
    print()

    await generate_previews()


if __name__ == "__main__":
    asyncio.run(main())
