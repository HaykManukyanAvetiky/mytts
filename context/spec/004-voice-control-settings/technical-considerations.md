# Technical Specification: Voice Control Settings

- **Functional Specification:** [004-voice-control-settings/functional-spec.md](./functional-spec.md)
- **Status:** ✅ Completed
- **Author:** Engineering Team

---

## 1. High-Level Technical Approach

This feature adds speech rate and pitch controls to allow users to customize voice output. The implementation spans both frontend and backend:

**Frontend (Alpine.js + HTML):**
- Add two dropdown controls below voice selector
- Store user-friendly values (0.75x, 1.0x, -20%, +10%, etc.)
- Convert to edge-tts format before API calls
- Persist settings in localStorage

**Backend (FastAPI + edge-tts):**
- Update request model to accept `rate` and `pitch` parameters
- Pass parameters to edge-tts `Communicate` class
- Validate parameter formats

**No database changes required** - settings persist client-side only.

---

## 2. Proposed Solution & Implementation Plan (The "How")

### 2.1 Frontend Changes

#### State Properties (`static/js/app.js`)

Add new state properties to the Alpine.js app:

```javascript
// Voice control settings
selectedRate: '1.0x',      // User-friendly format
selectedPitch: '0%',       // User-friendly format

// Dropdown options
rateOptions: ['0.75x', '1.0x', '1.25x', '1.5x'],
pitchOptions: ['-20%', '-10%', '0%', '+10%', '+20%'],
```

#### Conversion Functions (`static/js/app.js`)

Add helper methods to convert user-friendly values to edge-tts format:

```javascript
/**
 * Convert rate (0.75x, 1.0x, etc.) to edge-tts format (+0%, -25%, etc.)
 */
convertRate(rate) {
    const multiplier = parseFloat(rate);  // "1.25x" → 1.25
    const percentage = Math.round((multiplier - 1) * 100);
    return percentage >= 0 ? `+${percentage}%` : `${percentage}%`;
},

/**
 * Convert pitch (-20%, +10%, etc.) to edge-tts format (-20Hz, +10Hz, etc.)
 */
convertPitch(pitch) {
    return pitch.replace('%', 'Hz');
},
```

**Conversion Reference:**

| User Value | Edge-tts Rate |
|------------|---------------|
| 0.75x | -25% |
| 1.0x | +0% |
| 1.25x | +25% |
| 1.5x | +50% |

| User Value | Edge-tts Pitch |
|------------|----------------|
| -20% | -20Hz |
| -10% | -10Hz |
| 0% | +0Hz |
| +10% | +10Hz |
| +20% | +20Hz |

#### localStorage Persistence (`static/js/app.js`)

Add persistence methods following the existing pattern for voice selection:

```javascript
restoreVoiceControls() {
    const savedRate = localStorage.getItem('selectedRate');
    const savedPitch = localStorage.getItem('selectedPitch');
    if (savedRate && this.rateOptions.includes(savedRate)) {
        this.selectedRate = savedRate;
    }
    if (savedPitch && this.pitchOptions.includes(savedPitch)) {
        this.selectedPitch = savedPitch;
    }
},

saveVoiceControls() {
    localStorage.setItem('selectedRate', this.selectedRate);
    localStorage.setItem('selectedPitch', this.selectedPitch);
},

onRateChange() {
    this.saveVoiceControls();
},

onPitchChange() {
    this.saveVoiceControls();
},
```

Update `init()` to restore settings:
```javascript
async init() {
    await this.loadVoices();
    this.restoreVoiceSelection();
    this.restoreVoiceControls();  // Add this line
},
```

#### Update generateAudio() (`static/js/app.js`)

Modify the API call to include rate and pitch:

```javascript
body: JSON.stringify({
    text: this.text,
    voice: this.selectedVoice,
    rate: this.convertRate(this.selectedRate),
    pitch: this.convertPitch(this.selectedPitch)
}),
```

#### HTML Template (`backend/templates/index.html`)

Add controls section after the voice selector (after `.voice-section`):

```html
<!-- Voice Control Settings -->
<div class="voice-controls">
    <div class="control-row">
        <div class="control-group">
            <label for="rate-select">Speed:</label>
            <select
                id="rate-select"
                class="control-dropdown"
                x-model="selectedRate"
                @change="onRateChange"
                :disabled="isLoading"
            >
                <template x-for="rate in rateOptions" :key="rate">
                    <option :value="rate" x-text="rate"></option>
                </template>
            </select>
        </div>
        <div class="control-group">
            <label for="pitch-select">Pitch:</label>
            <select
                id="pitch-select"
                class="control-dropdown"
                x-model="selectedPitch"
                @change="onPitchChange"
                :disabled="isLoading"
            >
                <template x-for="pitch in pitchOptions" :key="pitch">
                    <option :value="pitch" x-text="pitch"></option>
                </template>
            </select>
        </div>
    </div>
</div>
```

#### CSS Styles (`static/css/styles.css`)

Add styles for the new controls:

```css
/* Voice Control Settings */
.voice-controls {
    margin-bottom: var(--spacing-lg);
}

.control-row {
    display: flex;
    gap: var(--spacing-md);
}

.control-group {
    flex: 1;
    display: flex;
    flex-direction: column;
    gap: var(--spacing-xs);
}

.control-group label {
    font-weight: 600;
    font-size: 0.875rem;
    color: var(--text-color);
}

.control-dropdown {
    padding: var(--spacing-sm);
    border: 2px solid var(--border-color);
    border-radius: var(--radius-md);
    font-family: var(--font-family);
    font-size: 1rem;
    background-color: var(--white);
    cursor: pointer;
    transition: border-color 0.2s ease-in-out;
}

.control-dropdown:hover:not(:disabled) {
    border-color: var(--primary-color);
}

.control-dropdown:focus {
    outline: none;
    border-color: var(--primary-color);
    box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1);
}

.control-dropdown:disabled {
    background-color: var(--bg-color);
    cursor: not-allowed;
    opacity: 0.6;
}
```

---

### 2.2 Backend Changes

#### Request Model (`backend/models/requests.py`)

Add rate and pitch fields to `TTSGenerateRequest`:

```python
import re
from pydantic import field_validator

class TTSGenerateRequest(BaseModel):
    text: str = Field(
        ...,
        min_length=1,
        max_length=3000,
        description="Text to convert to speech"
    )
    voice: str | None = Field(
        None,
        description="Voice ID (optional)"
    )
    rate: str = Field(
        default="+0%",
        description="Speech rate (e.g., +0%, +25%, -25%)"
    )
    pitch: str = Field(
        default="+0Hz",
        description="Pitch adjustment (e.g., +0Hz, +10Hz, -20Hz)"
    )

    @field_validator("rate")
    @classmethod
    def validate_rate(cls, v: str) -> str:
        if not re.match(r"^[+-]\d+%$", v):
            raise ValueError("Rate must be in format +/-{number}% (e.g., +25%, -25%)")
        return v

    @field_validator("pitch")
    @classmethod
    def validate_pitch(cls, v: str) -> str:
        if not re.match(r"^[+-]\d+Hz$", v):
            raise ValueError("Pitch must be in format +/-{number}Hz (e.g., +10Hz, -20Hz)")
        return v
```

#### TTS Service (`backend/core/tts/service.py`)

Update `generate()` method to accept and pass rate/pitch:

```python
async def generate(
    self,
    text: str,
    voice: str | None,
    output_path: Path,
    rate: str = "+0%",
    pitch: str = "+0Hz",
) -> Path:
    try:
        communicate = Communicate(
            text=text,
            voice=voice or self.default_voice,
            rate=rate,
            pitch=pitch,
        )
        await communicate.save(str(output_path))
        return output_path
    except Exception as e:
        raise TTSGenerationError(f"Failed to generate audio: {str(e)}") from e
```

#### API Route (`backend/api/routes/tts.py`)

Update the generate endpoint to pass rate/pitch to the service:

```python
await tts_service.generate(
    text=request.text,
    voice=request.voice,
    output_path=output_path,
    rate=request.rate,
    pitch=request.pitch,
)
```

---

## 3. Impact and Risk Analysis

### System Dependencies

| Component | Impact |
|-----------|--------|
| `edge-tts` library | Uses existing rate/pitch parameters (already supported) |
| Frontend Alpine.js app | New state properties, methods, and UI elements |
| Backend API | Extended request model, service method signature |
| localStorage | Two new keys: `selectedRate`, `selectedPitch` |

### Potential Risks & Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Invalid rate/pitch causes generation failure | Low | Medium | Backend validation with Pydantic; frontend uses predefined options only |
| Edge-tts rejects parameters | Very Low | High | Parameters validated against edge-tts regex patterns before sending |
| localStorage unavailable | Very Low | Low | Graceful fallback to default values |
| Voice quality degradation at extreme settings | Low | Medium | Limited range (0.75x-1.5x, ±20%) keeps quality safe |

---

## 4. Testing Strategy

### Manual Testing Checklist

**Speed Control:**
- [ ] Default value is "1.0x" on fresh page load
- [ ] Dropdown shows all 4 options (0.75x, 1.0x, 1.25x, 1.5x)
- [ ] Selecting each option saves to localStorage
- [ ] Page refresh restores saved selection
- [ ] Generation uses selected rate (audibly different)
- [ ] Voice preview uses default rate (not affected)

**Pitch Control:**
- [ ] Default value is "0%" on fresh page load
- [ ] Dropdown shows all 5 options (-20%, -10%, 0%, +10%, +20%)
- [ ] Selecting each option saves to localStorage
- [ ] Page refresh restores saved selection
- [ ] Generation uses selected pitch (audibly different)
- [ ] Voice preview uses default pitch (not affected)

**UI Behavior:**
- [ ] Both dropdowns appear below voice selector
- [ ] Dropdowns are side by side on desktop
- [ ] Dropdowns are disabled during generation
- [ ] Dropdowns re-enable after generation completes

**Error Handling:**
- [ ] Generation with custom settings succeeds
- [ ] If generation fails, error message suggests resetting to defaults
- [ ] Invalid localStorage values fall back to defaults

**Regression Testing:**
- [ ] Existing voice selection still works
- [ ] Existing text generation still works
- [ ] Audio playback and download still work
- [ ] Character counter still works

---

## 5. Files to Modify

| File | Changes |
|------|---------|
| `static/js/app.js` | Add state, conversion functions, persistence, update generateAudio() |
| `backend/templates/index.html` | Add Speed and Pitch dropdown controls |
| `static/css/styles.css` | Add styles for control dropdowns |
| `backend/models/requests.py` | Add rate/pitch fields with validators |
| `backend/core/tts/service.py` | Add rate/pitch parameters to generate() |
| `backend/api/routes/tts.py` | Pass rate/pitch to service |
