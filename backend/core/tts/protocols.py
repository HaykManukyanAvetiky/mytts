"""
Protocol definitions for TTS service providers.

This module defines the TTSProvider protocol for type-safe dependency injection
and testing with different TTS implementations.
"""

from pathlib import Path
from typing import Protocol


class TTSProvider(Protocol):
    """
    Protocol for text-to-speech service providers.

    This protocol defines the interface that all TTS implementations must follow,
    enabling type-safe dependency injection and easy testing with mock providers.
    """

    async def generate(self, text: str, voice: str, output_path: Path) -> Path:
        """
        Generate audio from text using the specified voice.

        Args:
            text: The text to convert to speech
            voice: The voice ID to use for generation
            output_path: The file path where the audio will be saved

        Returns:
            Path: The path to the generated audio file

        Raises:
            TTSGenerationError: If audio generation fails
        """
        ...
