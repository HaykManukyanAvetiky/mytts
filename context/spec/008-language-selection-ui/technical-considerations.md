# Technical Specification: Language Selection UI

- **Functional Specification:** `context/spec/008-language-selection-ui/functional-spec.md`
- **Status:** Draft
- **Author(s):** Claude/Architect

---

## 1. High-Level Technical Approach

This feature adds language filtering to the voice selection UI. The implementation involves:

1. **Backend API:** Add optional `?language=` query parameter to `/voices` endpoint and new `/languages` endpoint
2. **Frontend UI:** Add language dropdown above voice dropdown, re-fetch voices when language changes
3. **No database changes:** Uses existing `language` field in `voices.json`
4. **No new dependencies:** Leverages existing Alpine.js and FastAPI patterns

**Files to modify:**
- `backend/api/routes/tts.py` - Add `/languages` endpoint and modify `/voices`
- `backend/models/responses.py` - Add `LanguageListResponse` model
- `backend/templates/index.html` - Add language dropdown UI
- `static/js/app.js` - Add language state and fetch logic
- `static/css/styles.css` - Add language section styling

---

## 2. Proposed Solution & Implementation Plan

### 2.1 API Changes

#### New Endpoint: `GET /api/tts/languages`

**File:** `backend/api/routes/tts.py`

```python
@router.get("/languages", response_model=LanguageListResponse)
async def get_languages() -> LanguageListResponse:
    """Get list of available languages for TTS voices."""
    all_voices = load_voices_from_json()
    languages = sorted(set(v.language for v in all_voices))
    return LanguageListResponse(languages=languages)
```

**Response:**
```json
{
  "languages": ["English", "French", "German", "Portuguese", "Spanish"]
}
```

#### Modified Endpoint: `GET /api/tts/voices`

**File:** `backend/api/routes/tts.py` (lines 65-81)

```python
from typing import Optional
from fastapi import Query, HTTPException

@router.get("/voices", response_model=VoiceListResponse)
async def get_voices(
    language: Optional[str] = Query(
        None,
        description="Filter voices by language (e.g., 'English', 'Spanish')"
    ),
) -> VoiceListResponse:
    """Get list of available TTS voices with optional language filtering."""
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
```

**Usage:**
- `GET /api/tts/voices` → All 84 voices
- `GET /api/tts/voices?language=English` → Only English voices
- `GET /api/tts/voices?language=InvalidLang` → 400 error

#### New Response Model

**File:** `backend/models/responses.py`

```python
class LanguageListResponse(BaseModel):
    """Response model for language list endpoint."""
    languages: list[str] = Field(
        ...,
        description="List of available languages"
    )
```

---

### 2.2 Frontend Changes

#### State Changes

**File:** `static/js/app.js`

Add to `ttsApp()` return object:
```javascript
// Language selection state
selectedLanguage: 'English',      // Default language
languages: [],                    // Available languages from API
```

#### New Methods

**File:** `static/js/app.js`

```javascript
async loadLanguages() {
    try {
        const response = await fetch('/api/tts/languages');
        if (response.ok) {
            const data = await response.json();
            this.languages = data.languages;
        }
    } catch (err) {
        console.error('Failed to load languages:', err);
    }
},

async onLanguageChange() {
    // Re-fetch voices filtered by selected language
    this.loadingVoices = true;

    try {
        const url = this.selectedLanguage === 'All'
            ? '/api/tts/voices'
            : `/api/tts/voices?language=${encodeURIComponent(this.selectedLanguage)}`;

        const response = await fetch(url);
        if (response.ok) {
            const data = await response.json();
            this.voices = data.voices;

            // Auto-select first voice in new language
            this.selectedVoice = this.voices.length > 0 ? this.voices[0].id : null;
        }
    } catch (err) {
        console.error('Failed to load voices:', err);
    } finally {
        this.loadingVoices = false;
    }
},
```

Update `init()`:
```javascript
async init() {
    await this.loadLanguages();
    await this.loadVoices();  // Modified to use selectedLanguage
}
```

Update `loadVoices()`:
```javascript
async loadVoices() {
    this.loadingVoices = true;
    try {
        const url = this.selectedLanguage === 'All'
            ? '/api/tts/voices'
            : `/api/tts/voices?language=${encodeURIComponent(this.selectedLanguage)}`;

        const response = await fetch(url);
        // ... rest unchanged
    }
}
```

#### Template Changes

**File:** `backend/templates/index.html`

Insert before `.voice-section` div (around line 20):

```html
<!-- Language Selection -->
<div class="language-section">
    <label for="language-select">Select Language:</label>
    <select
        id="language-select"
        class="voice-dropdown"
        x-model="selectedLanguage"
        @change="onLanguageChange"
        :disabled="loadingVoices"
    >
        <option value="All">All Languages</option>
        <template x-for="lang in languages" :key="lang">
            <option :value="lang" x-text="lang"></option>
        </template>
    </select>
</div>
```

#### CSS Changes

**File:** `static/css/styles.css`

```css
/* Language Section - same styling as voice section */
.language-section {
    margin-bottom: var(--spacing-md);
}

.language-section label {
    display: block;
    font-weight: 600;
    margin-bottom: var(--spacing-xs);
    color: var(--text-color);
}
```

---

## 3. Impact and Risk Analysis

### System Dependencies

| Component | Impact |
|-----------|--------|
| `/voices` endpoint | Modified - adds optional `language` parameter |
| `/languages` endpoint | New endpoint |
| `voices.json` | No changes - uses existing `language` field |
| Frontend state | New `selectedLanguage` and `languages` properties |
| Voice preview | No changes - works with filtered voices |
| TTS generation | No changes - voice ID unchanged |

### Potential Risks & Mitigations

| Risk | Mitigation |
|------|------------|
| Invalid language parameter | Return 400 with list of valid languages |
| Empty voice list for language | Frontend handles empty state gracefully |
| Breaking existing API clients | `language` param is optional, defaults to all |
| Language names change in voices.json | Languages derived dynamically, no hardcoding |

---

## 4. Testing Strategy

### Backend Tests

**File:** `tests/integration/test_language_api.py`

```python
import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_get_languages(client: AsyncClient):
    """Test /languages endpoint returns available languages."""
    response = await client.get("/api/tts/languages")
    assert response.status_code == 200
    data = response.json()
    assert "languages" in data
    assert "English" in data["languages"]
    assert len(data["languages"]) == 5

@pytest.mark.asyncio
async def test_voices_filter_by_language(client: AsyncClient):
    """Test /voices?language=X filters correctly."""
    response = await client.get("/api/tts/voices?language=English")
    assert response.status_code == 200
    data = response.json()
    assert all(v["language"] == "English" for v in data["voices"])

@pytest.mark.asyncio
async def test_voices_invalid_language(client: AsyncClient):
    """Test /voices with invalid language returns 400."""
    response = await client.get("/api/tts/voices?language=InvalidLang")
    assert response.status_code == 400
    assert "Invalid language" in response.json()["detail"]

@pytest.mark.asyncio
async def test_voices_no_filter_returns_all(client: AsyncClient):
    """Test /voices without filter returns all voices."""
    response = await client.get("/api/tts/voices")
    assert response.status_code == 200
    data = response.json()
    assert len(data["voices"]) >= 80  # All 84 voices
```

### Manual Testing Checklist

- [ ] Language dropdown appears above voice dropdown
- [ ] Default selection is "English"
- [ ] Selecting a language filters voices correctly
- [ ] "All Languages" shows all 84 voices
- [ ] Changing language auto-selects first voice in new language
- [ ] Voice preview works after language change
- [ ] TTS generation works with filtered voices
