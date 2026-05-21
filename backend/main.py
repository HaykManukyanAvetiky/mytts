import sys
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from backend.core.audio.storage import AudioStorageService
from backend.api.routes import tts
from backend.exceptions.tts_exceptions import TTSGenerationError, MyTTSException
from backend.models.responses import ErrorResponse
from backend.config import load_voices_from_json, VoiceLoadError


# Validate voice configuration on startup
try:
    voices = load_voices_from_json()
    print(f"✓ Loaded {len(voices)} voice configurations")
except VoiceLoadError as e:
    print(f"ERROR: Failed to load voice configuration:\n{e}", file=sys.stderr)
    sys.exit(1)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for FastAPI application.

    Handles startup and shutdown tasks:
    - Startup: Ensure temp directory exists for audio storage
    - Shutdown: Cleanup handled by background tasks
    """
    # Startup: ensure temp directory exists
    storage = AudioStorageService()
    storage.temp_dir.mkdir(parents=True, exist_ok=True)
    print(f"✓ Temp directory created/verified: {storage.temp_dir}")

    yield

    # Shutdown: cleanup handled by background tasks


app = FastAPI(
    title="MyTTS API",
    version="0.1.0",
    lifespan=lifespan
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Setup Jinja2 templates
templates = Jinja2Templates(directory="backend/templates")

# Include API routers
app.include_router(tts.router, prefix="/api/tts", tags=["TTS"])


# Exception handlers
@app.exception_handler(TTSGenerationError)
async def tts_generation_error_handler(request: Request, exc: TTSGenerationError) -> JSONResponse:
    """Handle TTS generation errors with 500 status code."""
    return JSONResponse(
        status_code=500,
        content=ErrorResponse(
            error="TTS_GENERATION_ERROR",
            message="Unable to generate audio at this time. Please try again in a few moments.",
            details={"detail": str(exc)}
        ).model_dump()
    )


@app.exception_handler(ValueError)
async def value_error_handler(request: Request, exc: ValueError) -> JSONResponse:
    """Handle validation errors with 400 status code."""
    return JSONResponse(
        status_code=400,
        content=ErrorResponse(
            error="VALIDATION_ERROR",
            message=str(exc),
            details=None
        ).model_dump()
    )


@app.exception_handler(Exception)
async def generic_error_handler(request: Request, exc: Exception) -> JSONResponse:
    """Handle unexpected errors with 500 status code."""
    return JSONResponse(
        status_code=500,
        content=ErrorResponse(
            error="INTERNAL_SERVER_ERROR",
            message="An unexpected error occurred. Please try again later.",
            details={"detail": str(exc)}
        ).model_dump()
    )


@app.get("/", response_class=HTMLResponse)
async def root(request: Request) -> HTMLResponse:
    """
    Root endpoint that returns the main TTS interface.

    Args:
        request: FastAPI Request object required for template rendering.

    Returns:
        HTML template response with the TTS interface.
    """
    return templates.TemplateResponse("index.html", {"request": request})
