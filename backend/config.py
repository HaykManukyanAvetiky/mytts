"""Application configuration using Pydantic Settings.

This module provides the Settings class for managing application configuration
through environment variables and default values.
"""

import json
from functools import lru_cache
from pathlib import Path

from pydantic import BaseModel, ConfigDict, ValidationError
from pydantic_settings import BaseSettings


class VoiceLoadError(Exception):
    """Raised when voice data cannot be loaded from JSON file.

    This can occur when:
    - The JSON file is missing
    - The JSON file contains invalid syntax
    - The JSON structure doesn't match the expected schema
    """
    pass


class VoiceInfo(BaseModel):
    """Voice metadata model.

    Attributes:
        id: Unique voice identifier (e.g., "en-US-GuyNeural")
        name: Display name of the voice (e.g., "Guy")
        gender: Gender of the voice ("Male" or "Female")
        accent: Accent/region of the voice (e.g., "US", "UK", "Australian")
        language: Language of the voice (e.g., "English")
        style: Voice style descriptor (e.g., "Professional", "Friendly", "Neutral")
        description: Detailed description of voice characteristics and use cases
        preview_file: Filename of the preview audio sample
    """

    id: str
    name: str
    gender: str
    accent: str
    language: str
    style: str
    description: str
    preview_file: str


class VoicesConfig(BaseModel):
    """Configuration model for voices.json file.

    This model validates the structure of the external voices configuration file,
    ensuring it contains the required version metadata and list of voice definitions.

    Attributes:
        version: Semantic version of the voices configuration file (e.g., "1.0.0")
        updated: Date when the voices configuration was last updated (e.g., "2025-12-18")
        voices: List of VoiceInfo objects representing available TTS voices
    """

    version: str
    updated: str
    voices: list[VoiceInfo]


VOICES_FILE = Path(__file__).parent / "data" / "voices.json"


@lru_cache(maxsize=1)
def load_voices_from_json() -> list[VoiceInfo]:
    """Load voice configurations from JSON file.

    Uses @lru_cache to ensure file is read only once at startup.

    Returns:
        List of VoiceInfo objects.

    Raises:
        VoiceLoadError: If file is missing, invalid JSON, or has invalid structure.
    """
    if not VOICES_FILE.exists():
        raise VoiceLoadError(
            f"Voice configuration file not found: {VOICES_FILE}\n"
            "Please ensure backend/data/voices.json exists."
        )

    try:
        with open(VOICES_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        raise VoiceLoadError(
            f"Invalid JSON in voice configuration file: {VOICES_FILE}\n"
            f"Parse error at line {e.lineno}, column {e.colno}: {e.msg}"
        )

    try:
        config = VoicesConfig(**data)
        return config.voices
    except ValidationError as e:
        raise VoiceLoadError(
            f"Invalid voice configuration structure:\n{e}"
        )


class Settings(BaseSettings):
    """Application settings loaded from environment variables.

    This class uses Pydantic Settings to load configuration from environment
    variables or a .env file. All settings have sensible defaults.

    Attributes:
        app_name: Name of the application
        debug: Enable debug mode for detailed logging
        default_voice: Default voice ID for TTS generation
        max_text_length: Maximum allowed characters for TTS input
        min_text_length: Minimum required characters for TTS input
        temp_dir: Directory for storing temporary audio files
        cleanup_delay_seconds: Delay before cleaning up temporary files
        cors_origins: List of allowed CORS origins
        host: Host address to bind the server
        port: Port number to run the server
    """

    model_config = ConfigDict(env_file=".env")

    # Application settings
    app_name: str = "MyTTS"
    debug: bool = False

    # TTS settings
    default_voice: str = "en-US-GuyNeural"
    max_text_length: int = 3000
    min_text_length: int = 1

    # File management settings
    temp_dir: Path = Path("/tmp/mytts_audio")
    cleanup_delay_seconds: int = 300

    # Server settings
    cors_origins: list[str] = ["*"]
    host: str = "0.0.0.0"
    port: int = 8000

    @property
    def available_voices(self) -> list[VoiceInfo]:
        """Get list of available voices from JSON configuration.

        Returns:
            List of VoiceInfo objects representing available TTS voices.
        """
        return load_voices_from_json()


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Get cached settings instance.

    Uses @lru_cache to ensure settings are loaded only once.

    Returns:
        Settings instance with environment variables loaded.
    """
    return Settings()
