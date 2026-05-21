# Product Roadmap: MyTTS

_This roadmap outlines our strategic direction based on customer needs and business goals. It focuses on the "what" and "why," not the technical "how."_

---

### Phase 1: Core TTS Functionality ✅

_The highest priority features that form the minimal viable product - a working text-to-speech generator._

- [x] **Basic Web Interface**
  - [x] **Single-Page Application Setup:** Create a simple, clean web page where users can access all TTS functionality without navigation or page reloads.
  - [x] **Text Input Field:** Provide a large text area where users can paste or type their script content (plain text only).

- [x] **TTS Generation Engine**
  - [x] **Free TTS API Integration:** Integrate with a free TTS service (gTTS or Edge TTS) to convert text to speech with reliable voice quality.
  - [x] **Basic Error Handling:** Display clear error messages when generation fails due to API issues, text length, or connectivity problems.

---

### Phase 2: Voice Options & Output ✅

_Once the basic generation works, add voice selection and audio output capabilities._

- [x] **Voice Selection**
  - [x] **Multiple English Voice Options:** Provide a dropdown menu with at least 3-5 different English voices/accents for users to choose from.
  - [x] **Voice Preview Samples:** Allow users to hear short samples of each voice before generating their full script.

- [x] **Audio Output & Download**
  - [x] **In-Browser Audio Player:** Embed an HTML5 audio player that allows users to preview the generated speech immediately in their browser.
  - [x] **Download as MP3:** Provide a download button that saves the generated audio as an MP3 file to the user's device.

---

### Phase 3: User Experience Enhancements

_Features to improve usability and reliability for daily content creator workflows._

- [x] **Performance & Reliability**
  - [x] **Character Count Display:** Show a real-time character/word count to help users understand how much text they're converting.
  - [x] **Generation Progress Indicator:** Display a loading spinner or progress message while audio is being generated.

- [x] **Voice Control Settings**
  - [x] **Speech Rate Control:** Allow users to adjust the speaking speed (slower/faster) while maintaining voice quality.
  - [x] **Pitch Control:** Allow users to adjust voice pitch (higher/lower) without distortion or quality loss.

- [x] **Polish & Optimization**
  - [x] **Responsive Design:** Ensure the interface works well on both desktop and tablet devices (mobile native app is out of scope).
  - [x] **Clear Instructions:** Add minimal help text or tooltips to guide first-time users through the generation process.

---

### Bug Fixes

- [x] **Speed and Pitch Bug**
  - [x] **Replace Dropdowns with Radio Buttons:** Speed and Pitch dropdown controls not appearing on Mac. Convert to always-visible button groups for better cross-platform compatibility.
  - [x] **Fix Script Loading Order:** Alpine.js must load after app.js to ensure ttsApp function is available.
  - [x] **Add 1.15x Speed Option:** Added intermediate speed option between 1.0x and 1.25x for finer control.

---

### Phase 4: Multiple Language Support

_Expand TTS capabilities to support content creators worldwide._

- [ ] **Language Expansion**
  - [x] **Additional Language Voices:** Add support for major European languages (Spanish, French, German, Portuguese) using Edge TTS's multilingual voice options. Added 73 new voices across 4 languages.
  - [x] **Voice Data Externalization:** Move voice configurations from hardcoded Python code to an external data source (SQLite or JSON/YAML file) for easier maintenance, updates, and cleaner code architecture. Implemented with `backend/data/voices.json` and Pydantic validation.
  - [ ] **Language Selection UI:** Add a language selector dropdown that filters available voices by the selected language.
  - [ ] **Test Suite Organization:** Consolidate scattered test scripts and reports from the project root into a structured `tests/` folder with proper pytest-compatible unit tests for voice validation, API endpoints, and TTS generation.

---

### Phase 5: Mac Desktop App

_Native Mac application for better desktop integration and convenience._

- [ ] **Desktop Application**
  - [ ] **Native Mac App:** Build a standalone macOS application using a framework like Electron or Tauri.
  - [ ] **System Integration:** Menu bar access, keyboard shortcuts, and native file dialogs for saving audio.
