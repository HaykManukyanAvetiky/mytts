"""Request models for API endpoints.

This module defines Pydantic models for validating incoming API requests.
"""

import re

from pydantic import BaseModel, Field, field_validator


class TTSGenerateRequest(BaseModel):
    """Request model for TTS generation endpoint.

    This model validates and sanitizes input for text-to-speech generation,
    ensuring text length constraints and trimming whitespace.

    Attributes:
        text: The text to convert to speech (1-3000 characters after trimming)
        voice: Optional voice ID for TTS generation, uses default if not provided
    """

    text: str = Field(
        ...,
        min_length=1,
        max_length=3000,
        description="Text to convert to speech"
    )
    voice: str | None = Field(
        None,
        description="Voice ID (optional, uses default if not provided)"
    )
    rate: str = Field(
        default="+0%",
        description="Speech rate (e.g., +0%, +25%, -25%)"
    )
    pitch: str = Field(
        default="+0Hz",
        description="Pitch adjustment (e.g., +0Hz, +10Hz, -20Hz)"
    )

    @field_validator("text")
    @classmethod
    def trim_whitespace(cls, v: str) -> str:
        """Trim leading and trailing whitespace from text.

        Args:
            v: The text value to validate

        Returns:
            The trimmed text value

        Note:
            This validator runs after the min_length/max_length checks,
            so the length constraints apply to the original string.
        """
        return v.strip()

    @field_validator("rate")
    @classmethod
    def validate_rate(cls, v: str) -> str:
        """Validate rate format for Edge TTS.

        Args:
            v: The rate value to validate

        Returns:
            The validated rate value

        Raises:
            ValueError: If rate format is invalid
        """
        if not re.match(r"^[+-]\d+%$", v):
            raise ValueError("Rate must be in format +/-{number}% (e.g., +25%, -25%)")
        return v

    @field_validator("pitch")
    @classmethod
    def validate_pitch(cls, v: str) -> str:
        """Validate pitch format for Edge TTS.

        Args:
            v: The pitch value to validate

        Returns:
            The validated pitch value

        Raises:
            ValueError: If pitch format is invalid
        """
        if not re.match(r"^[+-]\d+Hz$", v):
            raise ValueError("Pitch must be in format +/-{number}Hz (e.g., +10Hz, -20Hz)")
        return v
