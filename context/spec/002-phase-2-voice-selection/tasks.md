# Task List: Phase 2 - Voice Selection

**Objective:** Add voice selection and preview capabilities to MyTTS, ensuring the app remains runnable after each major task.

---

## Slice 1: Voice Configuration & Data Models
**Goal:** Add voice metadata configuration to the backend (foundation work)

- [x] **Add VoiceInfo model to backend/config.py**
  - [x] Create `VoiceInfo` Pydantic model with fields: id, name, gender, accent, language, style, description, preview_file
  - [x] Add `available_voices` list to `Settings` class with 5 voice configurations:
    - en-US-GuyNeural (Male, US, Professional)
    - en-US-JennyNeural (Female, US, Friendly)
    - en-GB-RyanNeural (Male, UK, Professional)
    - en-GB-SoniaNeural (Female, UK, Neutral)
    - en-AU-NatashaNeural (Female, Australian, Friendly)

- [x] **Add VoiceListResponse model**
  - [x] Create `backend/models/responses.py` entry for `VoiceListResponse`
  - [x] Add `voices: List[VoiceInfo]` field

- [x] **Verify configuration**
  - [x] Import Settings in Python REPL
  - [x] Verify `settings.available_voices` returns list of 5 voices
  - [x] Verify all voice attributes are accessible

**Verification:** Can instantiate Settings and access voice configurations with correct data.

---

## Slice 2: Voice List API Endpoint
**Goal:** Implement GET /api/tts/voices endpoint to return available voices

- [x] **Add voice list endpoint**
  - [x] In `backend/api/routes/tts.py`, add `GET /voices` route
  - [x] Use `get_settings()` dependency to access voice configuration
  - [x] Return `VoiceListResponse` with all available voices

- [x] **Test endpoint**
  - [x] Start server
  - [x] Use curl to GET `http://localhost:8000/api/tts/voices`
  - [x] Verify response contains array of 5 voices
  - [x] Verify each voice has all required fields (id, name, gender, accent, etc.)

**Verification:** API returns 200 with correct JSON containing all voice metadata.

---

## Slice 3: Voice Preview Generation Script
**Goal:** Create script to generate voice preview audio files

- [x] **Create preview generation script**
  - [x] Create `scripts/` directory if not exists
  - [x] Create `scripts/generate_voice_previews.py`
  - [x] Define preview text constant: "Hello, this is a preview of this voice. I can help you create natural-sounding speech for your videos and podcasts."
  - [x] Implement `generate_previews()` async function that:
    - Loads settings and gets available voices
    - Creates `static/audio/previews/` directory
    - Generates MP3 for each voice using EdgeTTSService
    - Skips if preview file already exists

- [x] **Run script to generate previews**
  - [x] Activate virtual environment
  - [x] Run `python scripts/generate_voice_previews.py`
  - [x] Verify 5 MP3 files created in `static/audio/previews/`
  - [x] Verify each file is playable (5-10KB size)

**Verification:** All 5 preview MP3 files exist and can be played.

---

## Slice 4: Voice Preview API Endpoint
**Goal:** Implement GET /api/tts/preview/{voice_id} to serve preview audio

- [x] **Add preview serving endpoint**
  - [x] In `backend/api/routes/tts.py`, add `GET /preview/{voice_id}` route
  - [x] Find voice in `settings.available_voices` by ID
  - [x] Return 404 if voice not found
  - [x] Construct path to preview file: `static/audio/previews/{preview_file}`
  - [x] Return 404 if file doesn't exist
  - [x] Use `FileResponse` to serve MP3 with `media_type="audio/mpeg"`

- [x] **Test endpoint**
  - [x] Use curl to GET `http://localhost:8000/api/tts/preview/en-US-GuyNeural`
  - [x] Verify MP3 file downloads
  - [x] Test with invalid voice ID, verify 404 response
  - [x] Navigate to preview URL in browser, verify audio plays

**Verification:** Can access preview audio via URL, browser plays audio.

---

## Slice 5: Voice Validation in Generate Endpoint
**Goal:** Add voice ID validation to POST /api/tts/generate

- [x] **Add voice validation**
  - [x] In `generate_tts()` function in `backend/api/routes/tts.py`
  - [x] Add validation check: if `request.voice` is provided, verify it exists in `settings.available_voices`
  - [x] Raise `HTTPException` 400 with helpful message if invalid voice ID
  - [x] List available voices in error message

- [x] **Test validation**
  - [x] POST with valid voice ID (e.g., "en-US-JennyNeural"), verify generation succeeds
  - [x] POST with invalid voice ID, verify 400 error with helpful message
  - [x] POST with null voice, verify uses default voice (backward compatibility)

**Verification:** API rejects invalid voice IDs with clear error message, accepts valid voices.

---

## Slice 6: Frontend - Voice Data Loading
**Goal:** Add voice loading logic to Alpine.js app

- [x] **Update static/js/app.js**
  - [x] Add new state properties: `voices`, `selectedVoice`, `loadingVoices`, `previewingVoice`, `previewAudio`
  - [x] Add `init()` method to initialize app
  - [x] Add `loadVoices()` async method:
    - Fetch from `/api/tts/voices`
    - Store voices in state
    - Set default voice if none selected
  - [x] Add `restoreVoiceSelection()` method to read from localStorage
  - [x] Add `saveVoiceSelection()` method to write to localStorage
  - [x] Add `onVoiceChange()` method to handle dropdown changes
  - [x] Add `getVoiceLabel(voice)` helper to format display label

- [x] **Test in browser console**
  - [x] Open app, check Network tab for `/api/tts/voices` request
  - [x] In console, verify voices array is populated
  - [x] Verify selectedVoice is set

**Verification:** Voices load from API and populate app state correctly.

---

## Slice 7: Frontend - Voice Dropdown UI
**Goal:** Add voice selector dropdown to HTML template

- [x] **Update backend/templates/index.html**
  - [x] Add `x-init="init()"` to container div
  - [x] Add voice-section div before text input
  - [x] Add label "Select Voice:"
  - [x] Add `<select>` element:
    - `x-model="selectedVoice"`
    - `@change="onVoiceChange"`
    - `:disabled="loadingVoices"`
  - [x] Use `x-for` to loop through voices and create `<option>` elements
  - [x] Display voice label using `getVoiceLabel(voice)`

- [x] **Add CSS styles to static/css/styles.css**
  - [x] Add `.voice-section` styles (margin-bottom)
  - [x] Add `.voice-selector` styles (flexbox layout)
  - [x] Add `.voice-dropdown` styles (padding, border, border-radius, hover effects)
  - [x] Add disabled state styles

- [x] **Test in browser**
  - [x] Open app, verify dropdown appears with 5 voices
  - [x] Select different voices, verify selection changes
  - [x] Check localStorage in DevTools, verify voice saved

**Verification:** Voice dropdown displays all voices, selection works, persists across page reloads.

---

## Slice 8: Frontend - Voice Info Display
**Goal:** Show voice details (style, description) when voice is selected

- [x] **Update backend/templates/index.html**
  - [x] Add `.voice-info` div below dropdown
  - [x] Use `x-show` to display only when voice is selected
  - [x] Loop through voices, show details for selected voice
  - [x] Display `voice.style` as badge
  - [x] Display `voice.description` as text

- [x] **Add CSS styles**
  - [x] Add `.voice-info` styles (margin, padding, background, border-radius)
  - [x] Add `.voice-details` styles (font-size, color)
  - [x] Add `.voice-style` badge styles (inline-block, padding, background, color)
  - [x] Add `.voice-description` styles

- [x] **Test in browser**
  - [x] Select different voices
  - [x] Verify voice info updates correctly
  - [x] Verify style badge and description display properly

**Verification:** Voice information displays correctly when voice is selected.

---

## Slice 9: Frontend - Voice Preview Functionality
**Goal:** Add preview button and audio playback logic

- [x] **Update static/js/app.js**
  - [x] Add `previewVoice(voiceId)` async method:
    - Stop any currently playing preview
    - Toggle preview if same voice clicked
    - Create new Audio object with preview URL
    - Handle onended and onerror events
    - Play audio
    - Update `previewingVoice` state

- [x] **Update backend/templates/index.html**
  - [x] Add preview button next to dropdown
  - [x] Bind `@click="previewVoice(selectedVoice)"`
  - [x] Bind `:disabled` to loading states
  - [x] Use `x-show` to toggle button text (Preview / Stop)
  - [x] Add `:class="{ 'playing': previewingVoice === selectedVoice }"`

- [x] **Add CSS styles**
  - [x] Add `.btn-preview` styles (padding, background, color, border-radius)
  - [x] Add hover effects
  - [x] Add `.btn-preview.playing` styles (different background color)
  - [x] Add disabled state styles

- [x] **Test in browser**
  - [x] Click preview button, verify audio plays
  - [x] Click again, verify audio stops
  - [x] Switch voices and preview, verify only one plays at a time
  - [x] Verify visual feedback (button changes color when playing)

**Verification:** Voice preview plays audio immediately, visual feedback works, only one preview at a time.

---

## Slice 10: Frontend - Voice Integration with Generate
**Goal:** Use selected voice when generating TTS audio

- [x] **Update generateAudio() method**
  - [x] Modify fetch body to include: `voice: this.selectedVoice`
  - [x] Verify voice parameter is sent in API request

- [x] **Test end-to-end**
  - [x] Select voice "en-US-JennyNeural"
  - [x] Enter text and generate
  - [x] Play generated audio, verify it uses Jenny's voice (female, friendly)
  - [x] Select different voice, re-generate, verify audio changes
  - [x] Test with all 5 voices

**Verification:** Generated audio uses the selected voice, changing voice works correctly.

---

## Slice 11: Polish & Documentation
**Goal:** Final touches and update documentation

- [x] **Update README.md**
  - [x] Add Phase 2 features to Features section
  - [x] Document voice selection capability
  - [x] Document voice preview feature
  - [x] Add note about 5 available voices
  - [x] Update Usage section with voice selection steps

- [x] **Final UI polish**
  - [x] Ensure voice selector looks polished and professional
  - [x] Verify all hover states and transitions
  - [x] Test responsive layout with voice selector
  - [x] Verify visual consistency with Phase 1 UI

- [x] **End-to-end testing**
  - [x] Test complete flow: select voice → preview → enter text → generate → play
  - [x] Test voice persistence: select voice → refresh page → verify voice remembered
  - [x] Test all 5 voices for both preview and generation
  - [x] Test error scenarios (invalid voice, preview fails, etc.)
  - [x] Verify Phase 1 functionality still works (validation, error handling, etc.)

**Verification:** Complete manual test checklist passes, documentation updated, UI looks polished.

---

## Summary

**Total Slices:** 11
**Estimated Time:** ~2 hours
**Dependencies:** Phase 1 must be complete

Each slice keeps the application runnable and adds incremental value:
1. ✅ Configuration ready
2. ✅ API returns voice list
3. ✅ Preview files generated
4. ✅ Preview API works
5. ✅ Voice validation added
6. ✅ Frontend loads voices
7. ✅ Dropdown UI works
8. ✅ Voice info displays
9. ✅ Preview plays audio
10. ✅ Generation uses selected voice
11. ✅ Polished and documented
