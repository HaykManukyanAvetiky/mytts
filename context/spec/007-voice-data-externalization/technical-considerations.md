# Technical Considerations: Voice Data Externalization

- **Functional Spec:** [functional-spec.md](./functional-spec.md)
- **Status:** Draft
- **Author:** Claude (AI Assistant)

---

## 1. Architecture Overview

### Current State
Voice configurations are hardcoded in `backend/config.py` as a list of `VoiceInfo` instances, consuming ~900+ lines of code. The `get_voices()` function returns this static list.

### Target State
Voice data stored in `backend/data/voices.json`. The `get_voices()` function loads from JSON once at startup using `@lru_cache`, returning the same `List[VoiceInfo]` type for backward compatibility.

```
backend/
├── config.py          # VoiceInfo model + get_voices() loader (~80 lines)
├── data/
│   └── voices.json    # All 78 voice configurations
└── main.py            # Startup validation
```

---

## 2. JSON File Structure

### File Location
`backend/data/voices.json`

### Schema
```json
{
  "version": "1.0.0",
  "updated": "2025-12-18",
  "voices": [
    {
      "id": "en-US-GuyNeural",
      "name": "Guy",
      "gender": "Male",
      "accent": "US",
      "language": "English",
      "style": "Professional",
      "description": "A clear, professional American male voice ideal for narration and corporate content.",
      "preview_file": "en-US-GuyNeural.mp3"
    }
  ]
}
```

### Required Fields per Voice
All fields are required (matching current VoiceInfo model):
- `id` (str): Edge TTS voice identifier
- `name` (str): Display name
- `gender` (str): "Male" or "Female"
- `accent` (str): Regional accent (e.g., "US", "UK", "Spain")
- `language` (str): Language name (e.g., "English", "Spanish")
- `style` (str): Voice style description
- `description` (str): Full description for UI
- `preview_file` (str): Preview audio filename

---

## 3. Implementation Approach

### 3.1 Pydantic Validation Model

Add a new model for validating the entire JSON structure:

```python
from pydantic import BaseModel
from typing import List

class VoicesConfig(BaseModel):
    """Validates the voices.json file structure."""
    version: str
    updated: str
    voices: List[VoiceInfo]
```

### 3.2 Loading Function with Cache

Replace the hardcoded voice list with a cached loader:

```python
import json
from functools import lru_cache
from pathlib import Path

VOICES_FILE = Path(__file__).parent / "data" / "voices.json"

class VoiceLoadError(Exception):
    """Raised when voice data cannot be loaded."""
    pass

@lru_cache(maxsize=1)
def load_voices_from_json() -> List[VoiceInfo]:
    """Load voice configurations from JSON file.

    Uses @lru_cache to ensure file is read only once at startup.

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

def get_voices() -> List[VoiceInfo]:
    """Returns all available voices."""
    return load_voices_from_json()
```

### 3.3 Startup Validation

Add validation in `main.py` to fail fast on startup:

```python
from backend.config import get_voices, VoiceLoadError

# Validate voice configuration on startup
try:
    voices = get_voices()
    print(f"Loaded {len(voices)} voice configurations")
except VoiceLoadError as e:
    print(f"ERROR: {e}")
    sys.exit(1)
```

---

## 4. Migration Plan

### Step 1: Create JSON File
Extract current voice data from `config.py` into `backend/data/voices.json`.

### Step 2: Add Loading Logic
Add `VoicesConfig` model, `VoiceLoadError` exception, and `load_voices_from_json()` function to `config.py`.

### Step 3: Update get_voices()
Modify `get_voices()` to call `load_voices_from_json()` instead of returning hardcoded list.

### Step 4: Add Startup Validation
Add voice loading validation to `main.py` startup sequence.

### Step 5: Remove Hardcoded Voices
Delete all `VoiceInfo(...)` instances from `config.py`.

### Step 6: Verify
- Test `/api/tts/voices` endpoint returns all 78 voices
- Test TTS generation with voices from each language
- Test error handling by renaming/corrupting JSON file

---

## 5. Error Handling

### Missing File
```
ERROR: Voice configuration file not found: /path/to/backend/data/voices.json
Please ensure backend/data/voices.json exists.
```

### Invalid JSON Syntax
```
ERROR: Invalid JSON in voice configuration file: /path/to/backend/data/voices.json
Parse error at line 45, column 12: Expecting ',' delimiter
```

### Missing Required Field
```
ERROR: Invalid voice configuration structure:
1 validation error for VoicesConfig
voices -> 5 -> accent
  field required (type=value_error.missing)
```

---

## 6. Backward Compatibility

### API Contract
The `/api/tts/voices` endpoint response format remains unchanged:
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
      "description": "...",
      "preview_file": "en-US-GuyNeural.mp3"
    }
  ]
}
```

### Internal API
`get_voices()` continues to return `List[VoiceInfo]` - no changes needed to callers.

### TTS Generation
Voice validation in `/api/tts/generate` continues to work unchanged since it validates against `get_voices()` output.

---

## 7. Files to Modify

| File | Changes |
|------|---------|
| `backend/config.py` | Add VoicesConfig model, VoiceLoadError, load_voices_from_json(); remove 78 hardcoded voices |
| `backend/main.py` | Add startup validation for voice loading |
| `backend/data/voices.json` | New file with all 78 voice configurations |

---

## 8. Testing Strategy

1. **Unit Test**: Verify `load_voices_from_json()` returns correct voice count
2. **Error Test**: Verify clear errors for missing file, invalid JSON, missing fields
3. **API Test**: Verify `/api/tts/voices` returns same data as before
4. **Integration Test**: Generate TTS with at least one voice per language
5. **Regression Test**: Verify speech rate and pitch controls still work
