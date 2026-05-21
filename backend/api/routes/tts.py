"""TTS API routes.

This module provides the FastAPI routes for text-to-speech generation,
including dependency injection for services and background task scheduling
for audio file cleanup.
"""

from datetime import datetime
from pathlib import Path
from typing import Optional

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Query
from fastapi.responses import FileResponse

from backend.config import Settings, load_voices_from_json
from backend.core.audio.storage import AudioStorageService
from backend.core.tts.service import EdgeTTSService
from backend.models.requests import TTSGenerateRequest
from backend.models.responses import (
    LanguageListResponse,
    TTSGenerateResponse,
    VoiceListResponse,
)

router = APIRouter()


def get_settings() -> Settings:
    """Get application settings instance.

    This dependency provides the application configuration settings
    to all routes that need them.

    Returns:
        Settings: Application configuration instance.
    """
    return Settings()


def get_tts_service(settings: Settings = Depends(get_settings)) -> EdgeTTSService:
    """Get TTS service instance with dependency injection.

    Creates an EdgeTTSService instance configured with the default voice
    from application settings.

    Args:
        settings: Application settings injected by FastAPI.

    Returns:
        EdgeTTSService: Configured TTS service instance.
    """
    return EdgeTTSService(default_voice=settings.default_voice)


def get_audio_storage(settings: Settings = Depends(get_settings)) -> AudioStorageService:
    """Get audio storage service instance with dependency injection.

    Creates an AudioStorageService instance configured with the temporary
    directory path from application settings.

    Args:
        settings: Application settings injected by FastAPI.

    Returns:
        AudioStorageService: Configured audio storage service instance.
    """
    return AudioStorageService(temp_dir=settings.temp_dir)


@router.get("/voices", response_model=VoiceListResponse)
async def get_voices(
    language: Optional[str] = Query(
        None,
        description="Filter voices by language (e.g., 'English', 'Spanish')"
    ),
    settings: Settings = Depends(get_settings),
) -> VoiceListResponse:
    """Get list of available TTS voices with optional language filtering.

    This endpoint returns all available voices that can be used for
    text-to-speech generation. Each voice includes metadata such as
    name, gender, accent, language, style, and description.

    When a language filter is provided, only voices matching that language
    are returned. The endpoint remains backward compatible - calling without
    a language parameter returns all voices.

    Args:
        language: Optional language filter (e.g., 'English', 'Spanish').
                 If None or "All", returns all voices.
        settings: Application settings instance (injected dependency).

    Returns:
        VoiceListResponse: Response containing list of available voices.

    Raises:
        HTTPException: 400 if an invalid language is provided.
    """
    all_voices = load_voices_from_json()

    if language and language != "All":
        # Validate language exists
        valid_languages = set(v.language for v in all_voices)
        if language not in valid_languages:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid language. Available: {', '.join(sorted(valid_languages))}"
            )
        filtered = [v for v in all_voices if v.language == language]
        return VoiceListResponse(voices=filtered)

    return VoiceListResponse(voices=all_voices)


@router.get("/languages", response_model=LanguageListResponse)
async def get_languages() -> LanguageListResponse:
    """Get list of available languages for TTS voices.

    This endpoint returns all unique languages available in the voice
    configuration, sorted alphabetically. This is useful for populating
    language filter dropdowns in the UI.

    Returns:
        LanguageListResponse: Response containing sorted list of unique languages.
    """
    all_voices = load_voices_from_json()
    languages = sorted(set(v.language for v in all_voices))
    return LanguageListResponse(languages=languages)


@router.get("/preview/{voice_id}")
async def get_voice_preview(
    voice_id: str,
    settings: Settings = Depends(get_settings),
) -> FileResponse:
    """Serve voice preview audio file.

    This endpoint serves the preview MP3 file for a specific voice. Preview
    files are short audio samples that allow users to hear the voice before
    generating their full script.

    Args:
        voice_id: The unique identifier of the voice (e.g., "en-US-GuyNeural").
        settings: Application settings instance (injected dependency).

    Returns:
        FileResponse: Preview audio file with appropriate headers.

    Raises:
        HTTPException: 404 if voice not found or preview file doesn't exist.
    """
    # Find the voice in available voices
    voice = next(
        (v for v in settings.available_voices if v.id == voice_id),
        None,
    )

    if voice is None:
        raise HTTPException(
            status_code=404,
            detail=f"Voice '{voice_id}' not found",
        )

    # Construct path to preview file
    preview_path = Path("static/audio/previews") / voice.preview_file

    # Check if file exists
    if not preview_path.exists():
        raise HTTPException(
            status_code=404,
            detail=f"Preview file for voice '{voice_id}' not found. Run scripts/generate_voice_previews.py to generate previews.",
        )

    # Serve the preview file
    return FileResponse(
        path=preview_path,
        media_type="audio/mpeg",
        filename=voice.preview_file,
    )


@router.post("/generate", response_model=TTSGenerateResponse)
async def generate_tts(
    request: TTSGenerateRequest,
    background_tasks: BackgroundTasks,
    tts_service: EdgeTTSService = Depends(get_tts_service),
    storage: AudioStorageService = Depends(get_audio_storage),
    settings: Settings = Depends(get_settings),
) -> TTSGenerateResponse:
    """Generate TTS audio from text.

    This endpoint receives text and voice parameters, generates speech audio
    using Edge TTS, stores it temporarily, and schedules cleanup after a
    configured delay. The generated audio file is accessible via the returned
    URL for the duration of the cleanup delay.

    Args:
        request: TTS generation request containing text and voice.
        background_tasks: FastAPI background tasks for scheduling cleanup.
        tts_service: TTS service instance (injected dependency).
        storage: Audio storage service instance (injected dependency).
        settings: Application settings instance (injected dependency).

    Returns:
        TTSGenerateResponse: Response containing audio URL, filename, metadata.

    Raises:
        HTTPException: If TTS generation or file storage fails.
    """
    # Validate voice ID if provided
    if request.voice is not None:
        valid_voice_ids = [v.id for v in settings.available_voices]
        if request.voice not in valid_voice_ids:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid voice ID '{request.voice}'. Available voices: {', '.join(valid_voice_ids)}",
            )

    # Generate unique filename for the audio file
    filename = storage.generate_filename()
    output_path = storage.get_temp_path(filename)

    # Generate audio using TTS service
    await tts_service.generate(
        text=request.text,
        voice=request.voice,
        output_path=output_path,
        rate=request.rate,
        pitch=request.pitch,
    )

    # Schedule cleanup task to remove file after configured delay
    background_tasks.add_task(
        storage.schedule_cleanup,
        output_path,
        settings.cleanup_delay_seconds,
    )

    # Return response with audio URL and metadata
    return TTSGenerateResponse(
        audio_url=f"/api/tts/audio/{filename}",
        filename=filename,
        character_count=len(request.text),
        generated_at=datetime.utcnow(),
    )


@router.get("/audio/{filename}")
async def serve_audio(
    filename: str,
    storage: AudioStorageService = Depends(get_audio_storage),
) -> FileResponse:
    """Serve generated audio file for download or streaming.

    This endpoint serves the MP3 audio file generated by the TTS service.
    The file is served with appropriate headers for audio playback and download.
    Returns 404 if the file doesn't exist or has been cleaned up.

    Args:
        filename: Name of the audio file to serve.
        storage: Audio storage service instance (injected dependency).

    Returns:
        FileResponse: Audio file with appropriate headers.

    Raises:
        HTTPException: 404 if file doesn't exist.
    """
    # Get full path to the audio file
    file_path = storage.get_temp_path(filename)

    # Check if file exists
    if not file_path.exists():
        raise HTTPException(
            status_code=404,
            detail=f"Audio file '{filename}' not found or has been deleted",
        )

    # Serve the file with appropriate headers
    return FileResponse(
        path=file_path,
        media_type="audio/mpeg",
        filename=filename,
        headers={"Content-Disposition": f"attachment; filename={filename}"},
    )
