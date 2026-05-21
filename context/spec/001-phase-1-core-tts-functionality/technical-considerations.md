# Technical Specification: Phase 1 - Core TTS Functionality

- **Functional Specification:** `context/spec/001-phase-1-core-tts-functionality/functional-spec.md`
- **Status:** Draft
- **Author(s):** Technical Team

---

## 1. High-Level Technical Approach

We will implement a **FastAPI-based single-page web application** with async TTS generation using Edge TTS. The application follows a **stateless, protocol-based architecture** with these key components:

1. **Backend (FastAPI):** Async API server with TTS generation and file serving
2. **TTS Service:** Protocol-based service wrapping Edge TTS library
3. **Storage Service:** Temporary file storage with automatic background cleanup
4. **Frontend:** Single Jinja2 template with Alpine.js for reactivity

**Architecture Principles:**
- Async-first for all I/O operations
- Type-safe with Pydantic models throughout
- Protocol-based design for testability
- Dependency injection via FastAPI
- No database or persistent storage

**Affected Systems:**
- New FastAPI application (no existing systems to modify)
- Temporary file system for MP3 storage
- CDN for Alpine.js delivery

---

## 2. Proposed Solution & Implementation Plan

### 2.1 Project Structure

```
/Users/haykmanukyan/work/mytts/
├── backend/                          # Main application directory
│   ├── __init__.py
│   ├── main.py                       # FastAPI app entry point
│   ├── config.py                     # Pydantic Settings configuration
│   │
│   ├── api/                          # API layer
│   │   ├── __init__.py
│   │   └── routes/                   # Route handlers
│   │       ├── __init__.py
│   │       └── tts.py                # TTS generation endpoints
│   │
│   ├── core/                         # Core business logic
│   │   ├── __init__.py
│   │   ├── tts/                      # TTS module
│   │   │   ├── __init__.py
│   │   │   ├── protocols.py          # TTS protocols/interfaces
│   │   │   └── service.py            # EdgeTTS service implementation
│   │   └── audio/                    # Audio handling
│   │       ├── __init__.py
│   │       └── storage.py            # Temporary file storage service
│   │
│   ├── models/                       # Pydantic models
│   │   ├── __init__.py
│   │   ├── requests.py               # API request models
│   │   └── responses.py              # API response models
│   │
│   ├── exceptions/                   # Custom exceptions
│   │   ├── __init__.py
│   │   └── tts_exceptions.py         # TTS-specific exceptions
│   │
│   └── templates/                    # Jinja2 templates
│       └── index.html                # Single-page frontend
│
├── static/                           # Static assets
│   ├── css/
│   │   └── styles.css                # Application styles
│   └── js/
│       └── app.js                    # Alpine.js application logic
│
├── .env.example                      # Environment variables template
├── .gitignore                        # Git ignore rules
├── pyproject.toml                    # Project metadata and dependencies
└── README.md                         # Setup and run instructions
```

### 2.2 Dependencies (pyproject.toml)

**Package Management:**
This project uses `uv` for fast, reliable package management. `uv` is a modern Python package installer and resolver written in Rust that is significantly faster than pip.

**Installation with uv:**
```bash
# Install uv (if not already installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Create virtual environment
uv venv

# Activate virtual environment
source .venv/bin/activate  # On Unix/macOS
# or
.venv\Scripts\activate     # On Windows

# Install project dependencies
uv pip install -e .

# Install development dependencies (optional)
uv pip install -e ".[dev]"
```

**Core Dependencies:**
```toml
[project]
name = "mytts"
version = "0.1.0"
requires-python = ">=3.10"
dependencies = [
    "fastapi>=0.104.0",
    "uvicorn[standard]>=0.24.0",
    "edge-tts>=6.1.9",
    "python-multipart>=0.0.6",
    "jinja2>=3.1.2",
    "aiofiles>=23.2.1",
    "pydantic>=2.5.0",
    "pydantic-settings>=2.1.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.4.0",
    "pytest-asyncio>=0.21.0",
    "httpx>=0.25.0",
]
```

**Benefits of using uv:**
- 10-100x faster than pip for package installation
- Better dependency resolution algorithm
- Built-in virtual environment management
- Compatible with pip and pyproject.toml standards
- Produces deterministic installations

### 2.3 API Contracts

#### Endpoint 1: Root Page (GET /)
**Purpose:** Serve the single-page application

**Request:**
```http
GET / HTTP/1.1
Host: localhost:8000
```

**Response:**
```http
HTTP/1.1 200 OK
Content-Type: text/html

<!DOCTYPE html>
<html>...</html>
```

---

#### Endpoint 2: Generate TTS (POST /api/tts/generate)
**Purpose:** Generate audio from text and return metadata with audio URL

**Request:**
```http
POST /api/tts/generate HTTP/1.1
Host: localhost:8000
Content-Type: application/json

{
  "text": "Hello world, this is a test of the text to speech system.",
  "voice": null
}
```

**Request Model (Pydantic):**
```python
class TTSGenerateRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=3000)
    voice: str | None = Field(None)
```

**Success Response (200):**
```json
{
  "audio_url": "/api/tts/audio/mytts-2025-11-24-143022.mp3",
  "filename": "mytts-2025-11-24-143022.mp3",
  "character_count": 62,
  "generated_at": "2025-11-24T14:30:22.123456"
}
```

**Response Model (Pydantic):**
```python
class TTSGenerateResponse(BaseModel):
    audio_url: str
    filename: str
    character_count: int
    generated_at: datetime
```

**Error Responses:**

- **400 Bad Request** (Validation Error):
```json
{
  "error": "VALIDATION_ERROR",
  "message": "Text exceeds 3000 character limit. Please shorten your text to continue."
}
```

- **500 Internal Server Error** (TTS Generation Error):
```json
{
  "error": "TTS_GENERATION_ERROR",
  "message": "Unable to generate audio at this time. Please try again in a few moments."
}
```

---

#### Endpoint 3: Download/Stream Audio (GET /api/tts/audio/{filename})
**Purpose:** Serve generated MP3 file for download or playback

**Request:**
```http
GET /api/tts/audio/mytts-2025-11-24-143022.mp3 HTTP/1.1
Host: localhost:8000
```

**Success Response (200):**
```http
HTTP/1.1 200 OK
Content-Type: audio/mpeg
Content-Disposition: attachment; filename="mytts-2025-11-24-143022.mp3"

<binary audio data>
```

**Error Response (404):**
```json
{
  "error": "FILE_NOT_FOUND",
  "message": "Audio file not found or has expired."
}
```

### 2.4 Component Breakdown

#### Component 1: Configuration (backend/config.py)
**Purpose:** Centralized configuration using Pydantic Settings

**Implementation:**
```python
from pydantic_settings import BaseSettings
from pathlib import Path

class Settings(BaseSettings):
    # Application
    app_name: str = "MyTTS"
    debug: bool = False

    # TTS Configuration
    default_voice: str = "en-US-GuyNeural"
    max_text_length: int = 3000
    min_text_length: int = 1

    # File Storage
    temp_dir: Path = Path("/tmp/mytts_audio")
    cleanup_delay_seconds: int = 300  # 5 minutes

    # API
    cors_origins: list[str] = ["*"]

    # Server
    host: str = "0.0.0.0"
    port: int = 8000

    class Config:
        env_file = ".env"
```

---

#### Component 2: TTS Protocol & Service (backend/core/tts/)

**Protocol Definition (protocols.py):**
```python
from typing import Protocol
from pathlib import Path

class TTSProvider(Protocol):
    async def generate(self, text: str, voice: str, output_path: Path) -> Path:
        """Generate audio from text"""
        ...
```

**Edge TTS Service (service.py):**
```python
from edge_tts import Communicate
from backend.exceptions.tts_exceptions import TTSGenerationError

class EdgeTTSService:
    def __init__(self, default_voice: str = "en-US-GuyNeural"):
        self.default_voice = default_voice

    async def generate(
        self,
        text: str,
        voice: str | None,
        output_path: Path
    ) -> Path:
        """Generate audio using Edge TTS"""
        try:
            communicate = Communicate(
                text=text,
                voice=voice or self.default_voice
            )
            await communicate.save(str(output_path))
            return output_path
        except Exception as e:
            raise TTSGenerationError(f"Failed to generate audio: {str(e)}") from e
```

---

#### Component 3: Audio Storage Service (backend/core/audio/storage.py)

**Purpose:** Manage temporary MP3 file storage with automatic cleanup

**Key Methods:**
- `generate_filename()` - Create timestamped filename
- `get_temp_path(filename)` - Get full path for file
- `schedule_cleanup(path, delay)` - Schedule background deletion

**Implementation:**
```python
from pathlib import Path
import tempfile
import asyncio
from datetime import datetime

class AudioStorageService:
    def __init__(self, temp_dir: Path | None = None):
        self.temp_dir = temp_dir or Path(tempfile.gettempdir()) / "mytts_audio"
        self.temp_dir.mkdir(exist_ok=True)

    def generate_filename(self) -> str:
        timestamp = datetime.now().strftime("%Y-%m-%d-%H%M%S")
        return f"mytts-{timestamp}.mp3"

    def get_temp_path(self, filename: str) -> Path:
        return self.temp_dir / filename

    async def schedule_cleanup(self, file_path: Path, delay_seconds: int = 300):
        """Schedule file deletion after delay"""
        await asyncio.sleep(delay_seconds)
        if file_path.exists():
            await asyncio.to_thread(file_path.unlink, missing_ok=True)
```

---

#### Component 4: API Routes (backend/api/routes/tts.py)

**Dependencies:**
```python
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse

async def get_tts_service() -> EdgeTTSService:
    return EdgeTTSService()

async def get_audio_storage() -> AudioStorageService:
    return AudioStorageService()
```

**Route Handler:**
```python
@router.post("/generate", response_model=TTSGenerateResponse)
async def generate_tts(
    request: TTSGenerateRequest,
    background_tasks: BackgroundTasks,
    tts_service: EdgeTTSService = Depends(get_tts_service),
    storage: AudioStorageService = Depends(get_audio_storage)
) -> TTSGenerateResponse:
    # Generate filename
    filename = storage.generate_filename()
    output_path = storage.get_temp_path(filename)

    # Generate audio
    await tts_service.generate(request.text, request.voice, output_path)

    # Schedule cleanup
    background_tasks.add_task(storage.schedule_cleanup, output_path, 300)

    return TTSGenerateResponse(
        audio_url=f"/api/tts/audio/{filename}",
        filename=filename,
        character_count=len(request.text),
        generated_at=datetime.utcnow()
    )
```

---

#### Component 5: Frontend (backend/templates/index.html)

**Structure:**
```html
<!DOCTYPE html>
<html>
<head>
    <title>MyTTS - Text to Speech</title>
    <script defer src="https://cdn.jsdelivr.net/npm/alpinejs@3.x.x/dist/cdn.min.js"></script>
    <link rel="stylesheet" href="/static/css/styles.css">
</head>
<body>
    <div x-data="ttsApp()">
        <!-- Text Input -->
        <textarea x-model="text" @input="updateCharCount"></textarea>

        <!-- Character Counter (shown at 2500+) -->
        <div x-show="text.length >= 2500">
            <span x-text="text.length"></span> / 3000 characters
        </div>

        <!-- Generate Button -->
        <button
            @click="generateAudio"
            :disabled="isLoading"
            x-text="isLoading ? 'Generating...' : 'Generate'">
        </button>

        <!-- Loading Indicator -->
        <div x-show="isLoading">Generating audio...</div>

        <!-- Error Toast -->
        <div x-show="error" x-transition class="toast error">
            <span x-text="error"></span>
        </div>

        <!-- Success Toast -->
        <div x-show="success" x-transition class="toast success">
            Audio generated successfully!
        </div>

        <!-- Audio Player (hidden until audio generated) -->
        <div x-show="audioUrl">
            <audio controls :src="audioUrl"></audio>
            <a :href="audioUrl" download>Download MP3</a>
        </div>
    </div>

    <script src="/static/js/app.js"></script>
</body>
</html>
```

**Alpine.js Logic (static/js/app.js):**
```javascript
function ttsApp() {
    return {
        text: '',
        isLoading: false,
        error: null,
        success: false,
        audioUrl: null,

        async generateAudio() {
            // Clear previous state
            this.error = null;
            this.success = false;
            this.audioUrl = null;

            // Validate
            if (this.text.trim().length === 0) {
                this.showError('Please enter at least 1 character to generate audio.');
                return;
            }
            if (this.text.length > 3000) {
                this.showError('Text exceeds 3000 character limit. Please shorten your text to continue.');
                return;
            }

            // Generate
            this.isLoading = true;
            try {
                const response = await fetch('/api/tts/generate', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ text: this.text, voice: null })
                });

                if (!response.ok) {
                    const error = await response.json();
                    throw new Error(error.message || 'Generation failed');
                }

                const data = await response.json();
                this.audioUrl = data.audio_url;
                this.showSuccess();
            } catch (err) {
                this.showError(err.message || 'Connection error. Please check your internet connection and try again.');
            } finally {
                this.isLoading = false;
            }
        },

        showError(message) {
            this.error = message;
            setTimeout(() => this.error = null, 5000);
        },

        showSuccess() {
            this.success = true;
            setTimeout(() => this.success = false, 3000);
        }
    }
}
```

---

#### Component 6: Main Application (backend/main.py)

```python
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from contextlib import asynccontextmanager
from backend.api.routes import tts
from backend.core.audio.storage import AudioStorageService

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: ensure temp directory exists
    storage = AudioStorageService()
    storage.temp_dir.mkdir(exist_ok=True)
    yield
    # Shutdown: cleanup handled by background tasks

app = FastAPI(
    title="MyTTS API",
    version="0.1.0",
    lifespan=lifespan
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Templates
templates = Jinja2Templates(directory="backend/templates")

# Include API routes
app.include_router(tts.router, prefix="/api/tts", tags=["TTS"])

# Root route
@app.get("/")
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
```

---

## 3. Impact and Risk Analysis

### 3.1 System Dependencies

**External Dependencies:**
- **Edge TTS Service:** Requires internet connectivity; relies on Microsoft's public API
- **Temporary File System:** Requires write access to `/tmp` or configured temp directory
- **Alpine.js CDN:** Requires CDN availability (jsDelivr or unpkg)

**Internal Dependencies:**
- No existing system dependencies (greenfield project)

### 3.2 Potential Risks & Mitigations

| Risk | Impact | Likelihood | Mitigation Strategy |
|------|--------|------------|---------------------|
| **Edge TTS API unavailable** | Users cannot generate audio | Medium | Implement clear error messages; consider fallback TTS provider in future |
| **Disk space exhaustion** | App crashes due to too many temp files | Low | Background cleanup after 5 minutes; periodic cleanup on startup |
| **Large text input** | Slow generation, poor UX | Low | Enforce 3000 character limit; client-side validation |
| **Concurrent requests** | Multiple simultaneous generations | Medium | FastAPI async handles this; uvicorn worker count can scale |
| **File naming collisions** | Two files generated same second | Very Low | Timestamp includes seconds; extremely unlikely in practice |
| **CDN unavailable** | Alpine.js won't load | Low | Consider self-hosting Alpine.js in future; add fallback |
| **No rate limiting** | Potential abuse | Medium | Deferred to later phase; monitor usage patterns |

### 3.3 Security Considerations

**Input Validation:**
- Pydantic validates all inputs (character limits, type checking)
- Sanitize text input (prevent injection attacks)

**File Security:**
- Generate unique filenames (no user-controlled paths)
- Serve files with `Content-Disposition: attachment`
- Automatic cleanup prevents file accumulation

**Error Handling:**
- Generic error messages to users (no stack traces)
- Detailed logging for debugging (future)

---

## 4. Testing Strategy

**Phase 1 Testing Approach:**
- **Manual Testing Only:** No automated tests in Phase 1 to accelerate development
- **Test Coverage:**
  - Happy path: Enter text → Generate → Play → Download
  - Empty text validation
  - Text too long validation
  - TTS generation failure
  - Audio playback in browser
  - Download functionality
  - Character counter appearance at 2500+ chars
  - Error toast messages display and fade
  - Success toast display

**Future Testing (Post-Phase 1):**
- Unit tests for TTS service
- API integration tests with pytest-asyncio
- Frontend interaction tests
- Load testing for concurrent requests
