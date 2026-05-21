# Functional Specification: Additional Language Voices

- **Roadmap Item:** Add support for major European languages using Edge TTS's multilingual voice options
- **Status:** Completed
- **Author:** Claude (AI Assistant)

---

## 1. Overview and Rationale (The "Why")

### Purpose
Expand MyTTS's text-to-speech capabilities beyond English to support content creators who produce content in European languages. This enables the product to serve a broader international audience of YouTubers, podcasters, and video editors.

### Problem Being Solved
Currently, MyTTS only supports English voices. Content creators who work in Spanish, French, German, or Portuguese cannot use the application for their voiceover needs, limiting the product's usefulness to English-speaking markets only.

### Desired Outcome
Users can generate high-quality TTS audio in Spanish, French, German, and Portuguese with the same ease and reliability they currently experience with English voices.

### Success Criteria
- [x] All four European languages have working TTS generation
- [x] Voice quality for new languages is comparable to existing English voices
- [x] Speech rate and pitch controls function correctly for all new language voices
- [x] No degradation to existing English voice functionality

---

## 2. Functional Requirements (The "What")

### 2.1 Spanish Voice Support
- The system must include all Spanish voices available in the Edge TTS library
- This includes any regional variants (e.g., Spain Spanish, Latin American Spanish) that Edge TTS provides
- **Acceptance Criteria:**
  - [x] All available Spanish voices from Edge TTS are accessible in the application
  - [x] Spanish voices generate audio successfully when Spanish text is provided
  - [x] Speech rate control (0.75x, 1.0x, 1.15x, 1.25x, 1.5x) works correctly with Spanish voices
  - [x] Pitch control (-20%, -10%, 0%, +10%, +20%) works correctly with Spanish voices

### 2.2 French Voice Support
- The system must include all French voices available in the Edge TTS library
- This includes any regional variants that Edge TTS provides
- **Acceptance Criteria:**
  - [x] All available French voices from Edge TTS are accessible in the application
  - [x] French voices generate audio successfully when French text is provided
  - [x] Speech rate control works correctly with French voices
  - [x] Pitch control works correctly with French voices

### 2.3 German Voice Support
- The system must include all German voices available in the Edge TTS library
- **Acceptance Criteria:**
  - [x] All available German voices from Edge TTS are accessible in the application
  - [x] German voices generate audio successfully when German text is provided
  - [x] Speech rate control works correctly with German voices
  - [x] Pitch control works correctly with German voices

### 2.4 Portuguese Voice Support
- The system must include all Portuguese voices available in the Edge TTS library
- This includes any regional variants (e.g., Brazilian Portuguese, European Portuguese) that Edge TTS provides
- **Acceptance Criteria:**
  - [x] All available Portuguese voices from Edge TTS are accessible in the application
  - [x] Portuguese voices generate audio successfully when Portuguese text is provided
  - [x] Speech rate control works correctly with Portuguese voices
  - [x] Pitch control works correctly with Portuguese voices

### 2.5 Default Language Behavior
- English remains the default language when the application loads
- The existing English voice selection remains unchanged
- **Acceptance Criteria:**
  - [x] When the app first loads, English is the selected language
  - [x] Existing English voices continue to work exactly as before
  - [x] No changes to the default user experience for English users

### 2.6 Language-Text Mismatch Handling
- No validation is required between selected voice language and input text language
- Users are responsible for matching their text to the selected voice language
- The TTS engine will attempt to pronounce whatever text is provided
- **Acceptance Criteria:**
  - [x] The system does not block or warn when text language doesn't match voice language
  - [x] Generation proceeds regardless of text/voice language combination

### 2.7 Voice Preview Support (Added During Implementation)
- Voice preview audio files generated in each voice's native language
- Preview script updated to support multi-language preview texts
- **Acceptance Criteria:**
  - [x] Preview script includes language-specific sample texts
  - [x] Preview MP3 files generated for all new language voices
  - [x] Previews accessible via `/api/tts/preview/{voice_id}` endpoint

---

## 3. Scope and Boundaries

### In-Scope
- Adding Spanish, French, German, and Portuguese voices from Edge TTS
- Including all regional variants available in Edge TTS for these languages
- Ensuring speech rate and pitch controls work with all new voices
- Maintaining English as the default language
- Backend/API support for the new language voices
- Voice preview samples for new languages

### Out-of-Scope
- **Language Selection UI:** The user interface dropdown for selecting languages is a separate roadmap item and will be covered in its own specification
- **Phase 5: Mac Desktop App:** Native Mac application with system integration
- **Asian languages:** Japanese, Chinese, and other non-European languages
- **Language auto-detection:** Detecting user's browser language to pre-select a language
- **Text-language validation:** Warning or blocking when text doesn't match voice language

---

## 4. Implementation Notes (Post-Completion)

### Final Voice Counts
| Language | Voices | Regional Variants |
|----------|--------|-------------------|
| English | 5 | US, UK, Australia |
| Spanish | 45 | 22 regions (Spain, Mexico, Argentina, Colombia, etc.) |
| French | 13 | France, Canada, Belgium, Switzerland |
| German | 10 | Germany, Austria, Switzerland |
| Portuguese | 5 | Brazil, Portugal |
| **Total** | **78** | |

### Discovery: Unavailable Spanish Voices
During implementation, 32 Spanish voices listed in Edge TTS were found to be unavailable (returning "NoAudioReceived" errors). These were removed from the configuration:
- **Spain (es-ES):** 17 voices removed (only 3 work: Alvaro, Elvira, Ximena)
- **Mexico (es-MX):** 15 voices removed (only 2 work: Dalia, Jorge)
- **All other Spanish regions:** 100% working (40 voices across 20 countries)

### Files Modified
- `backend/config.py` - 78 voice configurations
- `scripts/generate_voice_previews.py` - Multi-language preview text support
- `static/audio/previews/` - 78 preview MP3 files generated
