# Task List: Voice Control Settings

**Objective:** Add speech rate and pitch controls to allow users to customize voice output while maintaining quality.

---

## Slice 1: Backend API Support for Rate/Pitch Parameters
**Goal:** Enable the API to accept rate and pitch parameters (with defaults), so existing functionality continues to work

- [x] **Update request model with rate/pitch fields**
  - [x] Open `backend/models/requests.py`
  - [x] Add `import re` at the top if not present
  - [x] Add `rate` field with default `"+0%"` and regex validator
  - [x] Add `pitch` field with default `"+0Hz"` and regex validator
  - [x] Test: Existing API calls without rate/pitch should still work (defaults applied)

- [x] **Update TTS service to accept rate/pitch**
  - [x] Open `backend/core/tts/service.py`
  - [x] Add `rate: str = "+0%"` and `pitch: str = "+0Hz"` parameters to `generate()` method
  - [x] Pass `rate=rate` and `pitch=pitch` to `Communicate()` constructor
  - [x] Test: Generate audio with default settings → Should work as before

- [x] **Update API route to pass rate/pitch to service**
  - [x] Open `backend/api/routes/tts.py`
  - [x] Update the `tts_service.generate()` call to include `rate=request.rate, pitch=request.pitch`
  - [x] Test: API accepts rate/pitch in request body → Audio generates correctly

**Verification:** App works exactly as before. API now accepts optional rate/pitch parameters with sensible defaults.

---

## Slice 2: Add Speed Dropdown (UI Only, Not Wired)
**Goal:** Display the Speed dropdown in the UI below voice selector

- [x] **Add CSS styles for voice controls**
  - [x] Open `static/css/styles.css`
  - [x] Add `.voice-controls`, `.control-row`, `.control-group`, `.control-dropdown` styles
  - [x] Save file and hard refresh browser

- [x] **Add Speed dropdown state and options to Alpine.js**
  - [x] Open `static/js/app.js`
  - [x] Add `selectedRate: '1.0x'` to state properties
  - [x] Add `rateOptions: ['0.75x', '1.0x', '1.25x', '1.5x']` to state
  - [x] Save file

- [x] **Add Speed dropdown HTML**
  - [x] Open `backend/templates/index.html`
  - [x] Add `.voice-controls` section after `.voice-section`
  - [x] Add Speed dropdown with `x-model="selectedRate"` and `:disabled="isLoading"`
  - [x] Test: Speed dropdown appears below voice selector with 4 options
  - [x] Test: Dropdown is disabled during audio generation

**Verification:** Speed dropdown is visible and interactive. Selecting options updates UI but doesn't affect audio generation yet.

---

## Slice 3: Add Pitch Dropdown (UI Only, Not Wired)
**Goal:** Display the Pitch dropdown next to Speed dropdown

- [x] **Add Pitch dropdown state and options to Alpine.js**
  - [x] Open `static/js/app.js`
  - [x] Add `selectedPitch: '0%'` to state properties
  - [x] Add `pitchOptions: ['-20%', '-10%', '0%', '+10%', '+20%']` to state
  - [x] Save file

- [x] **Add Pitch dropdown HTML**
  - [x] Open `backend/templates/index.html`
  - [x] Add Pitch dropdown in the same `.control-row` as Speed dropdown
  - [x] Use `x-model="selectedPitch"` and `:disabled="isLoading"`
  - [x] Test: Both Speed and Pitch dropdowns appear side by side
  - [x] Test: Both dropdowns are disabled during audio generation

**Verification:** Both dropdowns are visible and interactive. Layout is side by side on desktop.

---

## Slice 4: Wire Speed and Pitch to Audio Generation
**Goal:** Selected settings are applied when generating audio

- [x] **Add conversion functions to Alpine.js**
  - [x] Open `static/js/app.js`
  - [x] Add `convertRate(rate)` method: converts "1.25x" → "+25%"
  - [x] Add `convertPitch(pitch)` method: converts "-20%" → "-20Hz" and "0%" → "+0Hz"
  - [x] Save file

- [x] **Update generateAudio() to send rate/pitch**
  - [x] Open `static/js/app.js`
  - [x] Find `generateAudio()` method and the `fetch()` call
  - [x] Add `rate: this.convertRate(this.selectedRate)` to request body
  - [x] Add `pitch: this.convertPitch(this.selectedPitch)` to request body
  - [x] Test: Generate audio with 0.75x speed → Audio is noticeably slower
  - [x] Test: Generate audio with 1.5x speed → Audio is noticeably faster
  - [x] Test: Generate audio with -20% pitch → Voice is lower
  - [x] Test: Generate audio with +20% pitch → Voice is higher

**Verification:** Audio generation respects Speed and Pitch selections. Different settings produce audibly different results.

---

## Slice 5: Add localStorage Persistence
**Goal:** Settings are saved and restored across browser sessions

- [x] **Add persistence methods to Alpine.js**
  - [x] Open `static/js/app.js`
  - [x] Add `saveVoiceControls()` method to save both settings to localStorage
  - [x] Add `restoreVoiceControls()` method to restore settings from localStorage
  - [x] Add `onRateChange()` method that calls `saveVoiceControls()`
  - [x] Add `onPitchChange()` method that calls `saveVoiceControls()`
  - [x] Save file

- [x] **Wire change handlers in HTML**
  - [x] Open `backend/templates/index.html`
  - [x] Add `@change="onRateChange"` to Speed dropdown
  - [x] Add `@change="onPitchChange"` to Pitch dropdown
  - [x] Save file

- [x] **Restore settings on page load**
  - [x] Open `static/js/app.js`
  - [x] Update `init()` method to call `restoreVoiceControls()`
  - [x] Test: Change Speed to 1.5x, refresh page → Speed is still 1.5x
  - [x] Test: Change Pitch to +10%, refresh page → Pitch is still +10%
  - [x] Test: Clear localStorage, refresh page → Defaults are used (1.0x, 0%)

**Verification:** Settings persist across browser sessions. Invalid localStorage values fall back to defaults.

---

## Slice 6: Verify Voice Preview is Unaffected
**Goal:** Ensure voice preview always plays at default rate/pitch

- [x] **Verify preview behavior**
  - [x] Set Speed to 0.75x and Pitch to +20%
  - [x] Click "Preview" button for a voice
  - [x] Verify preview plays at normal speed and pitch (not affected by settings)
  - [x] Generate full audio → Verify it uses the custom settings
  - [x] Document: Preview intentionally uses defaults (no code changes needed if already working)

**Verification:** Voice preview is independent of Speed/Pitch settings. Only full generation uses custom settings.

---

## Slice 7: Comprehensive Testing & Polish
**Goal:** Verify all requirements and edge cases work correctly

- [x] **Speed Control Testing**
  - [x] Default value is "1.0x" on fresh page load
  - [x] Dropdown shows all 4 options (0.75x, 1.0x, 1.25x, 1.5x)
  - [x] Each option produces audibly different results
  - [x] Settings persist after page refresh

- [x] **Pitch Control Testing**
  - [x] Default value is "0%" on fresh page load
  - [x] Dropdown shows all 5 options (-20%, -10%, 0%, +10%, +20%)
  - [x] Each option produces audibly different results
  - [x] Settings persist after page refresh

- [x] **UI Behavior Testing**
  - [x] Both dropdowns appear below voice selector
  - [x] Dropdowns are side by side on desktop
  - [x] Dropdowns are disabled during generation
  - [x] Dropdowns re-enable after generation completes

- [x] **Error Handling Testing**
  - [x] Generation with all setting combinations succeeds
  - [x] Manually test invalid localStorage values → Falls back to defaults

- [x] **Regression Testing**
  - [x] Voice selection still works
  - [x] Text generation still works
  - [x] Audio playback and download still work
  - [x] Character counter still works
  - [x] Voice preview still works

**Verification:** All acceptance criteria from functional spec are met. No regressions in existing functionality.

---

## Slice 8: Documentation Update
**Goal:** Update project documentation to reflect completion

- [x] **Update roadmap**
  - [x] Open `context/product/roadmap.md`
  - [x] Mark "Voice Control Settings" as completed [x]
  - [x] Mark "Speech Rate Control" as completed [x]
  - [x] Mark "Pitch Control" as completed [x]

- [x] **Update spec status**
  - [x] Open `context/spec/004-voice-control-settings/functional-spec.md`
  - [x] Update status from "Draft" to "✅ Completed"
  - [x] Mark all acceptance criteria as [x]

**Verification:** Documentation reflects Phase 3 Voice Control Settings as complete.

---

## Summary

| Slice | Description | Key Files |
|-------|-------------|-----------|
| 1 | Backend API support | `requests.py`, `service.py`, `tts.py` |
| 2 | Speed dropdown (UI) | `styles.css`, `app.js`, `index.html` |
| 3 | Pitch dropdown (UI) | `app.js`, `index.html` |
| 4 | Wire to generation | `app.js` |
| 5 | localStorage persistence | `app.js`, `index.html` |
| 6 | Verify preview unaffected | (verification only) |
| 7 | Comprehensive testing | (testing only) |
| 8 | Documentation update | `roadmap.md`, `functional-spec.md` |

**Total Slices:** 8
**Files Modified:** 6 (`requests.py`, `service.py`, `tts.py`, `app.js`, `index.html`, `styles.css`)

Each slice keeps the application runnable and adds incremental value.
