# Technical Specification: Additional Language Voices

- **Functional Specification:** `context/spec/006-additional-language-voices/functional-spec.md`
- **Status:** Draft
- **Author(s):** Claude (AI Assistant)

---

## 1. High-Level Technical Approach

This feature requires **configuration changes only** - no architectural changes to the codebase. The existing system is designed to dynamically load voices from configuration:

1. **Backend:** Add voice entries to `backend/config.py` for all Edge TTS voices in Spanish, French, German, and Portuguese
2. **Preview Script:** Update `scripts/generate_voice_previews.py` to use language-appropriate preview text
3. **Preview Files:** Generate preview MP3 files for all new voices

The frontend automatically adapts since it dynamically fetches the voice list from `/api/tts/voices` and renders the UI based on voice metadata.

---

## 2. Proposed Solution & Implementation Plan (The "How")

### 2.1 Configuration Changes

**File:** `backend/config.py`

Add all available Edge TTS voices for the four target languages to the `available_voices` list. Each voice entry follows the existing `VoiceInfo` schema:

```python
VoiceInfo(
    id="es-ES-AlvaroNeural",      # Edge TTS identifier
    name="Alvaro",                 # Display name
    gender="Male",                 # "Male" or "Female"
    accent="Spain",                # Regional variant
    language="Spanish",            # Language name
    style="Professional",          # Voice style
    description="A clear Spanish male voice with Castilian accent.",
    preview_file="es-ES-AlvaroNeural.mp3"
)
```

**Languages and Expected Regions:**
- **Spanish:** Spain (es-ES), Mexico (es-MX), Argentina (es-AR), Colombia (es-CO), etc.
- **French:** France (fr-FR), Canada (fr-CA), Belgium (fr-BE), Switzerland (fr-CH)
- **German:** Germany (de-DE), Austria (de-AT), Switzerland (de-CH)
- **Portuguese:** Brazil (pt-BR), Portugal (pt-PT)

All voices available in Edge TTS for these locales will be included.

### 2.2 Preview Script Enhancement

**File:** `scripts/generate_voice_previews.py`

Update the script to use language-specific preview text:

```python
PREVIEW_TEXTS = {
    "English": "Hello, this is a preview of this voice. I can help you create natural-sounding speech.",
    "Spanish": "Hola, esta es una vista previa de esta voz. Puedo ayudarte a crear un habla natural.",
    "French": "Bonjour, ceci est un aperçu de cette voix. Je peux vous aider à créer un discours naturel.",
    "German": "Hallo, dies ist eine Vorschau dieser Stimme. Ich kann Ihnen helfen, natürlich klingende Sprache zu erstellen.",
    "Portuguese": "Olá, esta é uma prévia desta voz. Posso ajudá-lo a criar uma fala natural."
}
```

The script will select the appropriate preview text based on the voice's `language` field.

### 2.3 Voice Discovery

Before implementation, query Edge TTS for all available voices in the target languages:

```bash
edge-tts --list-voices | grep -E "^(es-|fr-|de-|pt-)"
```

This will provide the complete list of voice IDs, names, and genders to add to configuration.

### 2.4 No API Changes Required

The existing API endpoints require no modification:
- `GET /api/tts/voices` - Already returns all voices from configuration
- `POST /api/tts/generate` - Already validates against configured voices and passes voice ID to Edge TTS

### 2.5 No Frontend Changes Required

The frontend automatically handles new voices because:
- Voice list is fetched dynamically from the API
- Voice labels are generated from metadata: `"{name} ({gender}, {accent})"`
- Voice info cards display `style` and `description` automatically
- The dropdown accommodates any number of voices

---

## 3. Impact and Risk Analysis

### System Dependencies

- **Edge TTS API:** Relies on Microsoft's Edge TTS service continuing to provide these voices
- **Configuration File:** All changes isolated to `config.py` - no database or service dependencies
- **Preview Audio:** Requires disk space for preview MP3 files (~50KB per voice)

### Potential Risks & Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Voice ID changes in Edge TTS | Low | High | Document voice IDs; periodically verify against Edge TTS API |
| Increased voice dropdown size | Medium | Low | Future: Add language filter UI (separate roadmap item) |
| Preview generation failure | Low | Low | Script skips existing files; can regenerate individual voices |
| Non-English character encoding | Low | Medium | Edge TTS handles Unicode natively; test with accented characters |

### Backward Compatibility

- **No breaking changes:** All existing English voices remain unchanged
- **Default behavior preserved:** English remains the default language on app load
- **API contract unchanged:** Response structure identical, just more voices in the list

---

## 4. Testing Strategy

### Manual Testing

1. **Voice Configuration:**
   - Verify all new voices appear in the voice dropdown
   - Confirm voice metadata (name, gender, accent, language) displays correctly

2. **TTS Generation:**
   - For each language, test generation with sample text in that language
   - Verify speech rate controls (0.75x - 1.5x) work correctly
   - Verify pitch controls (-20% to +20%) work correctly

3. **Preview Playback:**
   - Confirm preview audio files are served correctly
   - Verify preview plays in the correct language

4. **Regression Testing:**
   - Verify English voices still work identically
   - Confirm default voice selection on app load is English

### Automated Testing

- Add unit tests for voice configuration validation
- Verify all configured voice IDs are valid Edge TTS identifiers
