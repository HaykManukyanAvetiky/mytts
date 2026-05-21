"""
Edge TTS service implementation.

This module provides the EdgeTTSService class that implements text-to-speech
generation using Microsoft's Edge TTS API.
"""

from pathlib import Path

from edge_tts import Communicate

from backend.exceptions.tts_exceptions import TTSGenerationError


class EdgeTTSService:
    """
    Text-to-speech service using Microsoft Edge TTS.

    This service implements the TTSProvider protocol and provides high-quality
    text-to-speech generation using Microsoft's Edge TTS neural voices.

    Attributes:
        default_voice: The default voice ID to use when none is specified
    """

    def __init__(self, default_voice: str = "en-US-GuyNeural") -> None:
        """
        Initialize the Edge TTS service.

        Args:
            default_voice: The voice ID to use as default (default: "en-US-GuyNeural")
        """
        self.default_voice = default_voice

    async def generate(
        self,
        text: str,
        voice: str | None,
        output_path: Path,
        rate: str = "+0%",
        pitch: str = "+0Hz",
    ) -> Path:
        """
        Generate audio from text using Edge TTS.

        This method converts the provided text to speech using the specified voice
        (or the default voice if none is provided) and saves the result to the
        specified output path.

        Args:
            text: The text to convert to speech
            voice: The voice ID to use, or None to use the default voice
            output_path: The file path where the audio will be saved
            rate: Speech rate adjustment (e.g., +0%, +25%, -25%)
            pitch: Pitch adjustment (e.g., +0Hz, +10Hz, -20Hz)

        Returns:
            Path: The path to the generated audio file

        Raises:
            TTSGenerationError: If audio generation or saving fails
        """
        try:
            communicate = Communicate(
                text=text,
                voice=voice or self.default_voice,
                rate=rate,
                pitch=pitch,
            )
            await communicate.save(str(output_path))
            return output_path
        except Exception as e:
            raise TTSGenerationError(f"Failed to generate audio: {str(e)}") from e
