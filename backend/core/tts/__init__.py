"""
Text-to-Speech service module.

This module provides TTS generation functionality using protocol-based
architecture for type safety and testability.
"""

from backend.core.tts.protocols import TTSProvider
from backend.core.tts.service import EdgeTTSService

__all__ = [
    "TTSProvider",
    "EdgeTTSService",
]
