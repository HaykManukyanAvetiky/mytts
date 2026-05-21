"""Response models for API endpoints.

This module defines Pydantic models for API responses, including success
and error responses.
"""

from datetime import datetime

from pydantic import BaseModel, Field

from backend.config import VoiceInfo


class TTSGenerateResponse(BaseModel):
    """Response model for successful TTS generation.

    This model represents the successful result of a text-to-speech generation
    request, including metadata about the generated audio.

    Attributes:
        audio_url: URL path to access the generated audio file
        filename: Name of the generated audio file
        character_count: Number of characters processed in the TTS request
        generated_at: Timestamp when the audio was generated
    """

    audio_url: str = Field(
        ...,
        description="URL to access the generated audio"
    )
    filename: str = Field(
        ...,
        description="Filename of the generated audio"
    )
    character_count: int = Field(
        ...,
        description="Number of characters processed"
    )
    generated_at: datetime = Field(
        ...,
        description="Timestamp of generation"
    )


class ErrorResponse(BaseModel):
    """Standard error response model.

    This model provides a consistent structure for all error responses,
    including an error code, human-readable message, and optional details.

    Attributes:
        error: Error code or type identifier
        message: Human-readable error message
        details: Optional dictionary with additional error context
    """

    error: str = Field(
        ...,
        description="Error code/type"
    )
    message: str = Field(
        ...,
        description="Human-readable error message"
    )
    details: dict[str, str] | None = Field(
        None,
        description="Additional error context"
    )


class VoiceListResponse(BaseModel):
    """Response model for voice list endpoint.

    This model represents the list of available voices that can be used
    for text-to-speech generation.

    Attributes:
        voices: List of available voice configurations
    """

    voices: list[VoiceInfo] = Field(
        ...,
        description="List of available voices"
    )


class LanguageListResponse(BaseModel):
    """Response model for language list endpoint.

    This model represents the list of available languages that can be used
    for text-to-speech generation.

    Attributes:
        languages: List of available languages
    """

    languages: list[str] = Field(
        ...,
        description="List of available languages"
    )
