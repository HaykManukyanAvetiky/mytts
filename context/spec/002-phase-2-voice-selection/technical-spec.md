# Technical Specification: Phase 2 - Voice Selection

- **Functional Spec Reference:** `002-phase-2-voice-selection/functional-spec.md`
- **Status:** Draft
- **Author:** Engineering Team

---

## 1. Architecture Overview

Phase 2 adds voice selection capabilities to the existing MyTTS application. The implementation follows the same architecture patterns established in Phase 1.

### Changes Required:

1. **Backend Changes:**
   - Add voice configuration/metadata storage
   - Generate and serve voice preview audio files
   - Add voice validation to API endpoints

2. **Frontend Changes:**
   - Add voice dropdown component
   - Add voice preview functionality
   - Add localStorage persistence
   - Update API calls to include voice parameter

3. **Static Assets:**
   - Pre-generated voice preview MP3 files

---

## 2. Data Models & Configuration

### 2.1 Voice Configuration (backend/config.py)

Add voice definitions to configuration:

```python
from pydantic import BaseModel
from typing import List

class VoiceInfo(BaseModel):
    """Voice metadata model."""
    id: str  # e.g., "en-US-GuyNeural"
    name: str  # e.g., "Guy"
    gender: str  # "Male" or "Female"
    accent: str  # e.g., "US", "UK", "Australian"
    language: str  # e.g., "English"
    style: str  # e.g., "Professional", "Friendly", "Neutral"
    description: str  # e.g., "Great for podcasts and narrations"
    preview_file: str  # e.g., "en-US-GuyNeural.mp3"

class Settings(BaseSettings):
    # ... existing settings ...

    # Voice configuration
    available_voices: List[VoiceInfo] = [
        VoiceInfo(
            id="en-US-GuyNeural",
            name="Guy",
            gender="Male",
            accent="US",
            language="English",
            style="Professional",
            description="Clear, professional voice perfect for narrations and presentations",
            preview_file="en-US-GuyNeural.mp3"
        ),
        VoiceInfo(
            id="en-US-JennyNeural",
            name="Jenny",
            gender="Female",
            accent="US",
            language="English",
            style="Friendly",
            description="Warm, friendly voice ideal for casual content and vlogs",
            preview_file="en-US-JennyNeural.mp3"
        ),
        VoiceInfo(
            id="en-GB-RyanNeural",
            name="Ryan",
            gender="Male",
            accent="UK",
            language="English",
            style="Professional",
            description="British accent, perfect for formal content and documentaries",
            preview_file="en-GB-RyanNeural.mp3"
        ),
        VoiceInfo(
            id="en-GB-SoniaNeural",
            name="Sonia",
            gender="Female",
            accent="UK",
            language="English",
            style="Neutral",
            description="Clear British accent, great for educational content",
            preview_file="en-GB-SoniaNeural.mp3"
        ),
        VoiceInfo(
            id="en-AU-NatashaNeural",
            name="Natasha",
            gender="Female",
            accent="Australian",
            language="English",
            style="Friendly",
            description="Australian accent, engaging for lifestyle and travel content",
            preview_file="en-AU-NatashaNeural.mp3"
        ),
    ]
```

### 2.2 Response Models (backend/models/responses.py)

Add voice list response:

```python
class VoiceListResponse(BaseModel):
    """Response model for voice list endpoint."""
    voices: List[VoiceInfo]
```

---

## 3. API Endpoints

### 3.1 GET /api/tts/voices

**Purpose:** Return list of available voices with metadata

**Response:**
```json
{
  "voices": [
    {
      "id": "en-US-GuyNeural",
      "name": "Guy",
      "gender": "Male",
      "accent": "US",
      "language": "English",
      "style": "Professional",
      "description": "Clear, professional voice perfect for narrations",
      "preview_file": "en-US-GuyNeural.mp3"
    },
    // ... more voices
  ]
}
```

**Implementation (backend/api/routes/tts.py):**
```python
@router.get("/voices", response_model=VoiceListResponse)
async def list_voices(
    settings: Settings = Depends(get_settings)
) -> VoiceListResponse:
    """
    List all available TTS voices with metadata.

    Returns:
        VoiceListResponse: List of available voices with their metadata.
    """
    return VoiceListResponse(voices=settings.available_voices)
```

### 3.2 GET /api/tts/preview/{voice_id}

**Purpose:** Serve pre-generated voice preview audio file

**Response:** MP3 audio file

**Implementation (backend/api/routes/tts.py):**
```python
@router.get("/preview/{voice_id}")
async def get_voice_preview(
    voice_id: str,
    settings: Settings = Depends(get_settings)
) -> FileResponse:
    """
    Serve voice preview audio file.

    Args:
        voice_id: Voice identifier (e.g., "en-US-GuyNeural").
        settings: Application settings.

    Returns:
        FileResponse: Preview audio file.

    Raises:
        HTTPException: 404 if voice not found.
    """
    # Find voice in available voices
    voice = next((v for v in settings.available_voices if v.id == voice_id), None)

    if not voice:
        raise HTTPException(
            status_code=404,
            detail=f"Voice '{voice_id}' not found"
        )

    # Get preview file path
    preview_path = Path("static/audio/previews") / voice.preview_file

    if not preview_path.exists():
        raise HTTPException(
            status_code=404,
            detail=f"Preview file for voice '{voice_id}' not found"
        )

    return FileResponse(
        path=preview_path,
        media_type="audio/mpeg",
        filename=voice.preview_file
    )
```

### 3.3 POST /api/tts/generate (Modified)

**Changes:** Voice parameter is now used from request (already implemented in Phase 1)

**Validation:** Add voice ID validation:

```python
@router.post("/generate", response_model=TTSGenerateResponse)
async def generate_tts(
    request: TTSGenerateRequest,
    background_tasks: BackgroundTasks,
    tts_service: EdgeTTSService = Depends(get_tts_service),
    storage: AudioStorageService = Depends(get_audio_storage),
    settings: Settings = Depends(get_settings),
) -> TTSGenerateResponse:
    """Generate TTS audio from text."""

    # Validate voice if provided
    if request.voice:
        valid_voices = [v.id for v in settings.available_voices]
        if request.voice not in valid_voices:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid voice ID. Available voices: {', '.join(valid_voices)}"
            )

    # ... rest of implementation remains the same
```

---

## 4. Frontend Implementation

### 4.1 Voice Data Management (static/js/app.js)

Add voice management to Alpine.js app:

```javascript
function ttsApp() {
    return {
        // Existing state
        text: '',
        isLoading: false,
        error: null,
        success: false,
        audioUrl: null,

        // New voice-related state
        voices: [],
        selectedVoice: null,
        loadingVoices: false,
        previewingVoice: null,
        previewAudio: null,

        /**
         * Initialize app - load voices and restore selection
         */
        async init() {
            await this.loadVoices();
            this.restoreVoiceSelection();
        },

        /**
         * Load available voices from API
         */
        async loadVoices() {
            this.loadingVoices = true;
            try {
                const response = await fetch('/api/tts/voices');
                if (response.ok) {
                    const data = await response.json();
                    this.voices = data.voices;

                    // Set default voice if none selected
                    if (!this.selectedVoice && this.voices.length > 0) {
                        this.selectedVoice = this.voices[0].id;
                    }
                }
            } catch (err) {
                console.error('Failed to load voices:', err);
            } finally {
                this.loadingVoices = false;
            }
        },

        /**
         * Restore voice selection from localStorage
         */
        restoreVoiceSelection() {
            const savedVoice = localStorage.getItem('selectedVoice');
            if (savedVoice && this.voices.some(v => v.id === savedVoice)) {
                this.selectedVoice = savedVoice;
            }
        },

        /**
         * Save voice selection to localStorage
         */
        saveVoiceSelection() {
            if (this.selectedVoice) {
                localStorage.setItem('selectedVoice', this.selectedVoice);
            }
        },

        /**
         * Handle voice selection change
         */
        onVoiceChange() {
            this.saveVoiceSelection();
        },

        /**
         * Preview a voice
         */
        async previewVoice(voiceId) {
            // Stop any currently playing preview
            if (this.previewAudio) {
                this.previewAudio.pause();
                this.previewAudio = null;
            }

            // If clicking the same voice, stop preview
            if (this.previewingVoice === voiceId) {
                this.previewingVoice = null;
                return;
            }

            // Start new preview
            this.previewingVoice = voiceId;

            try {
                const audio = new Audio(`/api/tts/preview/${voiceId}`);
                this.previewAudio = audio;

                audio.onended = () => {
                    this.previewingVoice = null;
                    this.previewAudio = null;
                };

                audio.onerror = () => {
                    this.showError('Failed to load voice preview');
                    this.previewingVoice = null;
                    this.previewAudio = null;
                };

                await audio.play();
            } catch (err) {
                this.showError('Failed to play voice preview');
                this.previewingVoice = null;
            }
        },

        /**
         * Get voice display label
         */
        getVoiceLabel(voice) {
            return `${voice.name} (${voice.gender}, ${voice.accent})`;
        },

        // Existing methods...
        showError(message) { /* ... */ },
        showSuccess() { /* ... */ },

        /**
         * Generate audio (modified to use selected voice)
         */
        async generateAudio() {
            // Validation...

            // Clear previous state
            this.audioUrl = null;
            this.error = null;
            this.success = false;
            this.isLoading = true;

            try {
                const response = await fetch('/api/tts/generate', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        text: this.text,
                        voice: this.selectedVoice  // Use selected voice
                    }),
                });

                // Handle response...
            } catch (err) {
                // Error handling...
            } finally {
                this.isLoading = false;
            }
        }
    };
}
```

### 4.2 HTML Template Updates (backend/templates/index.html)

Add voice selector UI:

```html
<div class="container" x-data="ttsApp()" x-init="init()">
    <!-- Header -->
    <header>
        <h1>MyTTS</h1>
        <p class="subtitle">Convert your text to natural-sounding speech</p>
    </header>

    <div class="form-container">
        <!-- Voice Selection -->
        <div class="voice-section">
            <label for="voice-select">Select Voice:</label>
            <div class="voice-selector">
                <select
                    id="voice-select"
                    x-model="selectedVoice"
                    @change="onVoiceChange"
                    :disabled="loadingVoices"
                    class="voice-dropdown"
                >
                    <template x-for="voice in voices" :key="voice.id">
                        <option :value="voice.id" x-text="getVoiceLabel(voice)"></option>
                    </template>
                </select>

                <!-- Voice info tooltip -->
                <template x-if="selectedVoice">
                    <div class="voice-info">
                        <template x-for="voice in voices" :key="voice.id">
                            <div x-show="voice.id === selectedVoice" class="voice-details">
                                <span class="voice-style" x-text="voice.style"></span>
                                <span class="voice-description" x-text="voice.description"></span>
                            </div>
                        </template>
                    </div>
                </template>
            </div>

            <!-- Preview button -->
            <button
                type="button"
                @click="previewVoice(selectedVoice)"
                :disabled="!selectedVoice || loadingVoices"
                class="btn-preview"
                :class="{ 'playing': previewingVoice === selectedVoice }"
            >
                <span x-show="previewingVoice !== selectedVoice">🔊 Preview</span>
                <span x-show="previewingVoice === selectedVoice">⏸ Stop</span>
            </button>
        </div>

        <!-- Existing text input section -->
        <div class="input-section">
            <!-- ... existing textarea ... -->
        </div>

        <!-- Existing generate button and other elements -->
        <!-- ... -->
    </div>
</div>
```

### 4.3 CSS Styling (static/css/styles.css)

Add styles for voice selector:

```css
/* Voice Selection Section */
.voice-section {
    margin-bottom: 1.5rem;
}

.voice-selector {
    display: flex;
    gap: 1rem;
    align-items: flex-start;
    margin-bottom: 0.5rem;
}

.voice-dropdown {
    flex: 1;
    padding: 0.75rem;
    font-size: 1rem;
    border: 2px solid var(--border-color);
    border-radius: 8px;
    background-color: white;
    cursor: pointer;
    transition: border-color 0.3s ease;
}

.voice-dropdown:hover {
    border-color: var(--primary-color);
}

.voice-dropdown:focus {
    outline: none;
    border-color: var(--primary-color);
    box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1);
}

.voice-dropdown:disabled {
    opacity: 0.6;
    cursor: not-allowed;
}

.btn-preview {
    padding: 0.75rem 1.5rem;
    background-color: var(--secondary-color, #6b7280);
    color: white;
    border: none;
    border-radius: 8px;
    font-size: 1rem;
    cursor: pointer;
    transition: all 0.3s ease;
    white-space: nowrap;
}

.btn-preview:hover:not(:disabled) {
    background-color: var(--secondary-dark, #4b5563);
    transform: translateY(-2px);
}

.btn-preview:disabled {
    opacity: 0.6;
    cursor: not-allowed;
}

.btn-preview.playing {
    background-color: var(--error-color);
}

.voice-info {
    margin-top: 0.5rem;
    padding: 0.75rem;
    background-color: var(--background-light, #f3f4f6);
    border-radius: 6px;
}

.voice-details {
    font-size: 0.875rem;
    color: var(--text-secondary, #6b7280);
}

.voice-style {
    display: inline-block;
    padding: 0.25rem 0.5rem;
    background-color: var(--primary-color);
    color: white;
    border-radius: 4px;
    font-size: 0.75rem;
    font-weight: 600;
    margin-right: 0.5rem;
}

.voice-description {
    display: block;
    margin-top: 0.5rem;
}
```

---

## 5. Voice Preview Generation

### 5.1 Preview Text

Use consistent text for all preview samples:

```text
"Hello, this is a preview of this voice. I can help you create natural-sounding speech for your videos and podcasts."
```

### 5.2 Generation Script

Create `scripts/generate_voice_previews.py`:

```python
"""
Script to generate voice preview audio files.
Run once to create preview samples for all voices.
"""
import asyncio
from pathlib import Path
from backend.core.tts.service import EdgeTTSService
from backend.config import Settings

PREVIEW_TEXT = "Hello, this is a preview of this voice. I can help you create natural-sounding speech for your videos and podcasts."

async def generate_previews():
    """Generate preview audio files for all configured voices."""
    settings = Settings()
    tts_service = EdgeTTSService()

    # Create preview directory
    preview_dir = Path("static/audio/previews")
    preview_dir.mkdir(parents=True, exist_ok=True)

    for voice in settings.available_voices:
        output_path = preview_dir / voice.preview_file

        if output_path.exists():
            print(f"✓ Preview already exists: {voice.id}")
            continue

        print(f"Generating preview for {voice.id}...")
        try:
            await tts_service.generate(
                text=PREVIEW_TEXT,
                voice=voice.id,
                output_path=output_path
            )
            print(f"✓ Generated: {output_path}")
        except Exception as e:
            print(f"✗ Failed to generate {voice.id}: {e}")

if __name__ == "__main__":
    asyncio.run(generate_previews())
```

**Usage:**
```bash
source .venv/bin/activate
python scripts/generate_voice_previews.py
```

---

## 6. Testing Strategy

### 6.1 Backend Tests

```python
# Test voice list endpoint
def test_list_voices():
    response = client.get("/api/tts/voices")
    assert response.status_code == 200
    data = response.json()
    assert len(data["voices"]) >= 5
    assert all("id" in v and "name" in v for v in data["voices"])

# Test voice preview endpoint
def test_get_voice_preview():
    response = client.get("/api/tts/preview/en-US-GuyNeural")
    assert response.status_code == 200
    assert response.headers["content-type"] == "audio/mpeg"

# Test invalid voice preview
def test_invalid_voice_preview():
    response = client.get("/api/tts/preview/invalid-voice")
    assert response.status_code == 404

# Test generate with specific voice
def test_generate_with_voice():
    response = client.post("/api/tts/generate", json={
        "text": "Test",
        "voice": "en-US-JennyNeural"
    })
    assert response.status_code == 200
```

### 6.2 Frontend Testing

Manual testing checklist:
- [ ] Voice dropdown loads with all 5 voices
- [ ] Voice selection persists across page reloads
- [ ] Preview plays audio within 1 second
- [ ] Only one preview plays at a time
- [ ] Generated audio uses selected voice
- [ ] Voice info tooltip displays correctly
- [ ] All voices can be previewed
- [ ] All voices can be used for generation

---

## 7. Migration Notes

No database migrations required. All changes are additive:
- New API endpoints
- New static files (preview audio)
- Frontend enhancements

Backward compatibility maintained:
- If no voice specified, default voice is used
- Existing generated files remain accessible

---

## 8. Performance Considerations

- **Preview files**: Pre-generated and cached (5-10KB each)
- **Voice list**: Returned from in-memory config (no DB query)
- **Preview playback**: Uses browser's native audio handling
- **localStorage**: Minimal data stored (one voice ID string)

---

## 9. File Structure Changes

```
mytts/
├── backend/
│   ├── api/routes/tts.py        # Add GET /voices, GET /preview/{voice_id}
│   ├── config.py                 # Add VoiceInfo model, available_voices list
│   └── models/responses.py       # Add VoiceListResponse
├── static/
│   ├── audio/
│   │   └── previews/             # NEW: Voice preview MP3 files
│   │       ├── en-US-GuyNeural.mp3
│   │       ├── en-US-JennyNeural.mp3
│   │       ├── en-GB-RyanNeural.mp3
│   │       ├── en-GB-SoniaNeural.mp3
│   │       └── en-AU-NatashaNeural.mp3
│   ├── css/styles.css            # Add voice selector styles
│   └── js/app.js                 # Add voice management logic
├── scripts/
│   └── generate_voice_previews.py # NEW: Script to generate previews
└── backend/templates/index.html  # Add voice selector UI
```

---

## 10. Implementation Order

1. **Backend foundation** (30 min)
   - Add VoiceInfo model to config.py
   - Add voice list endpoint
   - Add preview endpoint with placeholder

2. **Generate previews** (15 min)
   - Create scripts/generate_voice_previews.py
   - Run script to generate all preview files

3. **Frontend - Voice dropdown** (30 min)
   - Add voice selector HTML
   - Add voice loading logic
   - Add CSS styles

4. **Frontend - Preview feature** (20 min)
   - Add preview button
   - Add preview playback logic

5. **Frontend - Persistence** (10 min)
   - Add localStorage save/restore

6. **Integration & Testing** (20 min)
   - Test all voice selections
   - Test previews
   - Test generation with different voices

**Total estimated time: ~2 hours**
