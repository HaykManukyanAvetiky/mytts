# Task List: Phase 1 - Core TTS Functionality

**Objective:** Build a working text-to-speech web application incrementally, ensuring the app remains runnable after each major task.

---

## Slice 1: Project Setup & "Hello World" API
**Goal:** Get a minimal FastAPI application running that serves a basic page

- [x] **Create project structure and dependencies**
  - [x] Create `pyproject.toml` with FastAPI, uvicorn, and basic dependencies
  - [x] Create directory structure: `backend/`, `static/css/`, `static/js/`
  - [x] Create all `__init__.py` files for Python modules
  - [x] Create `.gitignore` for Python projects
  - [x] Create `.env.example` file

- [x] **Setup virtual environment and install dependencies**
  - [x] Create virtual environment with `uv venv`
  - [x] Activate virtual environment: `source .venv/bin/activate`
  - [x] Install dependencies with `uv pip install -e .`
  - [x] Verify installation with `uv pip list`

- [x] **Implement minimal FastAPI app**
  - [x] Create `backend/main.py` with basic FastAPI app instance
  - [x] Add root GET endpoint that returns a simple HTML string "MyTTS - Coming Soon"
  - [x] Run `uvicorn backend.main:app --reload` and verify it works at `http://localhost:8000`

**Verification:** App starts without errors and displays "MyTTS - Coming Soon" in the browser.

---

## Slice 2: Static Frontend Shell (No Functionality)
**Goal:** Serve a complete HTML page with form elements, but no working functionality yet

- [x] **Create basic HTML template**
  - [x] Create `backend/templates/` directory
  - [x] Create `backend/templates/index.html` with basic structure:
    - HTML5 boilerplate
    - Title: "MyTTS - Text to Speech"
    - Link to Alpine.js CDN
    - Link to `/static/css/styles.css`
  - [x] Add Jinja2Templates to `backend/main.py`
  - [x] Update root route to return `templates.TemplateResponse("index.html", {"request": request})`

- [x] **Add form UI elements (non-functional)**
  - [x] Add large `<textarea>` for text input (no Alpine.js yet)
  - [x] Add "Generate" button (no click handler yet)
  - [x] Add placeholder divs for: loading indicator, error messages, success message, audio player

- [x] **Create basic CSS**
  - [x] Create `static/css/styles.css` with minimal styling
  - [x] Style textarea, button, and container layout
  - [x] Add CSS classes for `.toast`, `.error`, `.success` (for future use)
  - [x] Mount static files in `backend/main.py` with `app.mount("/static", StaticFiles(directory="static"), name="static")`

**Verification:** Navigate to `http://localhost:8000` and see a complete form layout with textarea and button (button does nothing).

---

## Slice 3: Pydantic Models & Configuration
**Goal:** Define data models and configuration (foundation for API)

- [x] **Create configuration**
  - [x] Create `backend/config.py` with `Settings` class using Pydantic Settings
  - [x] Add fields: `app_name`, `default_voice`, `max_text_length`, `temp_dir`, `cleanup_delay_seconds`
  - [x] Verify settings can be instantiated

- [x] **Create request/response models**
  - [x] Create `backend/models/__init__.py`
  - [x] Create `backend/models/requests.py` with `TTSGenerateRequest` model
    - Fields: `text` (str, 1-3000 chars), `voice` (str | None)
    - Add validator for text (trim whitespace)
  - [x] Create `backend/models/responses.py` with `TTSGenerateResponse` and `ErrorResponse` models
    - `TTSGenerateResponse`: `audio_url`, `filename`, `character_count`, `generated_at`
    - `ErrorResponse`: `error`, `message`, `details`

- [x] **Create custom exceptions**
  - [x] Create `backend/exceptions/__init__.py`
  - [x] Create `backend/exceptions/tts_exceptions.py` with exception classes:
    - `MyTTSException` (base)
    - `TTSGenerationError`

**Verification:** Import models and config in Python REPL, create instances, verify validation works (e.g., text too long raises error).

---

## Slice 4: Audio Storage Service (File Management)
**Goal:** Implement temporary file storage with filename generation (no TTS yet)

- [x] **Create storage service**
  - [x] Create `backend/core/__init__.py`
  - [x] Create `backend/core/audio/__init__.py`
  - [x] Create `backend/core/audio/storage.py` with `AudioStorageService` class
    - `__init__`: Create temp directory if doesn't exist
    - `generate_filename()`: Return timestamped filename
    - `get_temp_path(filename)`: Return full Path to temp file
    - `schedule_cleanup(path, delay)`: Async method to delete file after delay

- [x] **Update main.py with lifespan**
  - [x] Add lifespan context manager to `backend/main.py`
  - [x] On startup: Create temp directory using `AudioStorageService`
  - [x] Verify temp directory is created when app starts

**Verification:** Start app, verify `/tmp/mytts_audio` directory is created. Test `generate_filename()` returns correct format.

---

## Slice 5: TTS Service & Edge TTS Integration
**Goal:** Implement TTS generation service that can create real audio files

- [x] **Create TTS protocol and service**
  - [x] Create `backend/core/tts/__init__.py`
  - [x] Create `backend/core/tts/protocols.py` with `TTSProvider` protocol
  - [x] Create `backend/core/tts/service.py` with `EdgeTTSService` class
    - `__init__`: Store default voice (`en-US-GuyNeural`)
    - `generate(text, voice, output_path)`: Async method using Edge TTS `Communicate`
    - Wrap in try/except to raise `TTSGenerationError` on failure

- [x] **Test TTS generation manually**
  - [x] Create a simple test script or use Python REPL
  - [x] Generate a test audio file: `await EdgeTTSService().generate("Hello world", None, Path("/tmp/test.mp3"))`
  - [x] Verify MP3 file is created and can be played

**Verification:** Run test script, verify audio file is generated and sounds correct when played.

---

## Slice 6: API Endpoint - Generate TTS
**Goal:** Implement POST /api/tts/generate endpoint (no frontend integration yet)

- [x] **Create API routes**
  - [x] Create `backend/api/__init__.py`
  - [x] Create `backend/api/routes/__init__.py`
  - [x] Create `backend/api/routes/tts.py` with `APIRouter`
  - [x] Add dependency injection functions: `get_tts_service()`, `get_audio_storage()`
  - [x] Implement `POST /generate` endpoint:
    - Accept `TTSGenerateRequest`
    - Generate filename using storage service
    - Call TTS service to generate audio
    - Schedule cleanup using `BackgroundTasks`
    - Return `TTSGenerateResponse` with audio URL
  - [x] Include router in `backend/main.py` with prefix `/api/tts`

- [x] **Test API endpoint**
  - [x] Use `curl` or Postman to POST to `http://localhost:8000/api/tts/generate`
  - [x] Body: `{"text": "This is a test", "voice": null}`
  - [x] Verify response includes `audio_url`, `filename`, `character_count`
  - [x] Verify MP3 file exists in temp directory

**Verification:** API returns 200 with correct JSON, audio file exists on disk.

---

## Slice 7: API Endpoint - Serve Audio Files
**Goal:** Implement GET /api/tts/audio/{filename} to download/stream audio

- [x] **Add audio serving endpoint**
  - [x] In `backend/api/routes/tts.py`, add `GET /audio/{filename}` route
  - [x] Use `FileResponse` to serve the audio file
  - [x] Set headers: `Content-Type: audio/mpeg`, `Content-Disposition: attachment`
  - [x] Return 404 if file doesn't exist

- [x] **Test audio serving**
  - [x] Generate audio using POST endpoint
  - [x] Copy the `audio_url` from response
  - [x] Navigate to `http://localhost:8000/api/tts/audio/{filename}` in browser
  - [x] Verify MP3 file downloads or plays

**Verification:** Can access generated audio file via URL, browser plays or downloads it.

---

## Slice 8: Frontend Integration - Basic Generate Flow
**Goal:** Wire up frontend to call API and display audio player (no validation or error handling yet)

- [x] **Create Alpine.js app logic**
  - [x] Create `static/js/app.js` with `ttsApp()` function
  - [x] Add state: `text`, `isLoading`, `error`, `success`, `audioUrl`
  - [x] Add `generateAudio()` method:
    - Set `isLoading = true`
    - POST to `/api/tts/generate` with text
    - On success: Set `audioUrl` and `success`
    - Finally: Set `isLoading = false`

- [x] **Update HTML template**
  - [x] Add `x-data="ttsApp()"` to wrapper div
  - [x] Bind textarea to `text` with `x-model="text"`
  - [x] Bind button click to `@click="generateAudio"`
  - [x] Bind button disabled state to `:disabled="isLoading"`
  - [x] Show/hide audio player with `x-show="audioUrl"`
  - [x] Bind audio src to `:src="audioUrl"`
  - [x] Add download link with `:href="audioUrl"`
  - [x] Include `/static/js/app.js` script

**Verification:** Enter text, click Generate, wait, audio player appears with working audio that can be played and downloaded.

---

## Slice 9: Loading States & Button Behavior
**Goal:** Add loading indicator and button state changes during generation

- [x] **Update frontend for loading**
  - [x] Update button text to show "Generating..." when `isLoading` is true (`:x-text="isLoading ? 'Generating...' : 'Generate'"`)
  - [x] Show loading indicator div with `x-show="isLoading"`
  - [x] Clear previous audio player when starting new generation (set `audioUrl = null` at start of `generateAudio`)

**Verification:** Click Generate, button shows "Generating..." and is disabled, loading message appears, then audio player replaces loading state.

---

## Slice 10: Client-Side Validation & Error Messages
**Goal:** Add validation and display error toasts for client-side errors

- [x] **Add validation to generateAudio()**
  - [x] Check if `text.trim().length === 0`, show error: "Please enter at least 1 character to generate audio."
  - [x] Check if `text.length > 3000`, show error: "Text exceeds 3000 character limit..."
  - [x] Return early if validation fails

- [x] **Implement error/success toast display**
  - [x] Add `showError(message)` method: Set `error`, clear after 5 seconds
  - [x] Add `showSuccess()` method: Set `success`, clear after 3 seconds
  - [x] Call `showSuccess()` after successful generation

- [x] **Update HTML for toasts**
  - [x] Show error toast with `x-show="error"` and `x-transition`
  - [x] Show success toast with `x-show="success"` and `x-transition`
  - [x] Display error message with `x-text="error"`

**Verification:** Try to generate with empty text (error shown), try with 3001+ characters (error shown), successful generation shows success toast.

---

## Slice 11: Server-Side Error Handling
**Goal:** Handle API errors and display appropriate messages to user

- [x] **Add exception handlers to FastAPI**
  - [x] In `backend/main.py`, add exception handler for `TTSGenerationError` → returns 500 with `ErrorResponse`
  - [x] Add exception handler for `ValueError` → returns 400 with `ErrorResponse`
  - [x] Add generic exception handler for unexpected errors

- [x] **Update frontend to handle API errors**
  - [x] In `generateAudio()`, check `if (!response.ok)`
  - [x] Parse error JSON and extract `message`
  - [x] Call `showError(error.message)`
  - [x] Add catch block for network errors, show: "Connection error. Please check your internet connection and try again."

**Verification:** Simulate API failure (stop Edge TTS service or disconnect internet), verify error toast appears with helpful message.

---

## Slice 12: Character Counter
**Goal:** Add character counter that appears when approaching limit

- [x] **Implement character counter**
  - [x] In HTML, add div with `x-show="text.length >= 2500"`
  - [x] Display: `<span x-text="text.length"></span> / 3000 characters`
  - [x] Style counter appropriately in CSS

**Verification:** Type text, counter hidden until 2500 characters, then appears and updates in real-time.

---

## Slice 13: Polish & Documentation
**Goal:** Add final touches, README, and verify end-to-end flow

- [x] **Create documentation**
  - [x] Create `README.md` with:
    - Project description
    - Setup instructions (install dependencies, run server)
    - Usage instructions
    - Tech stack overview

- [x] **Final CSS polish**
  - [x] Improve toast animations and positioning
  - [x] Ensure responsive layout works on different screen sizes
  - [x] Add hover states for button
  - [x] Style audio player container

- [x] **End-to-end manual testing**
  - [x] Test complete happy path: enter text → generate → play → download
  - [x] Test all error scenarios (empty, too long, API failure)
  - [x] Test character counter appearance
  - [x] Test multiple generations in sequence
  - [x] Verify cleanup happens (check temp directory after 5+ minutes)

**Verification:** Complete manual test checklist passes, app looks polished and professional.
