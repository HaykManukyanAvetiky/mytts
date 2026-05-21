# Functional Specification: Language Selection UI

- **Roadmap Item:** Add a language selector dropdown that filters available voices by the selected language.
- **Status:** Draft
- **Author:** Claude/Poe

---

## 1. Overview and Rationale (The "Why")

### Problem Statement
MyTTS now supports 73+ voices across 5 languages (English, Spanish, French, German, Portuguese). Currently, users see all voices in a single dropdown, making it difficult to:
- Find voices in their desired language quickly
- Browse available options within a specific language
- Understand which languages are supported

### Desired Outcome
A language selector dropdown will be added above the voice dropdown, allowing users to filter voices by language. This will:
- Make voice selection faster and more intuitive
- Clearly communicate available language options
- Prepare the UI for future language additions

### Success Criteria
- Users can filter voices by language with one click
- Voice selection time decreases (fewer scrolling through irrelevant options)
- Default behavior (English) works seamlessly for existing users
- UI remains simple and uncluttered

---

## 2. Functional Requirements (The "What")

### Requirement 1: Language Selector Dropdown
A dropdown control must be added above the voice selector to filter voices by language.

**Acceptance Criteria:**
- [ ] Language dropdown appears above the voice dropdown in the UI
- [ ] Dropdown displays available languages extracted from voice data
- [ ] Languages are listed in alphabetical order: All Languages, English, French, German, Portuguese, Spanish
- [ ] Dropdown uses the same visual style as the existing voice dropdown

### Requirement 2: Default Selection
The language selector must default to "English" on page load.

**Acceptance Criteria:**
- [ ] On initial page load, "English" is pre-selected in the language dropdown
- [ ] Voice dropdown shows only English voices by default
- [ ] First English voice is pre-selected in voice dropdown

### Requirement 3: "All Languages" Option
An "All Languages" option must allow users to see the complete voice list.

**Acceptance Criteria:**
- [ ] "All Languages" appears as the first option in the language dropdown
- [ ] When "All Languages" is selected, voice dropdown shows all 73+ voices
- [ ] Voices in "All Languages" view are grouped or sorted by language (e.g., English voices first, then French, etc.)

### Requirement 4: Filtering Behavior
When the user selects a language, the voice dropdown must filter to show only voices in that language.

**Acceptance Criteria:**
- [ ] Selecting "Spanish" shows only Spanish voices in the voice dropdown
- [ ] Voice count in dropdown matches the number of voices for selected language
- [ ] Filter is applied instantly without page reload
- [ ] If current voice is not in selected language, auto-select the first voice in the new language

### Requirement 5: Voice Reset on Language Change
When the user changes language, the voice selection must reset to the first voice in the new language.

**Acceptance Criteria:**
- [ ] Changing language from "English" to "French" auto-selects the first French voice
- [ ] The voice dropdown value updates visually to show the new selection
- [ ] If user had previously generated audio, no audio regeneration occurs automatically
- [ ] Voice preview (if applicable) does not auto-play on language change

### Requirement 6: API Compatibility
The existing `/voices` API endpoint must support optional language filtering.

**Acceptance Criteria:**
- [ ] `GET /voices` continues to return all voices (backward compatible)
- [ ] `GET /voices?language=Spanish` returns only Spanish voices
- [ ] `GET /voices?language=All` or no parameter returns all voices
- [ ] Invalid language parameter returns 400 error with message: "Invalid language. Available: English, Spanish, French, German, Portuguese"

### Requirement 7: Language Data Source
Available languages must be derived from the voice data, not hardcoded.

**Acceptance Criteria:**
- [ ] Language list is dynamically generated from unique `language` values in `voices.json`
- [ ] Adding a new language to `voices.json` automatically appears in the dropdown
- [ ] No hardcoded language list in frontend or backend code

---

## 3. Scope and Boundaries

### In-Scope
- Language selector dropdown above voice dropdown
- Client-side filtering of voices by language
- Optional API parameter for server-side language filtering
- Default to English on page load
- "All Languages" option to see all voices
- Auto-reset voice selection on language change

### Out-of-Scope
- Test Suite Organization (separate roadmap item)
- Native Mac App (Phase 5)
- System Integration (Phase 5)
- Language auto-detection from browser settings
- Remembering user's language preference across sessions
- Voice search or text-based filtering
- Voice grouping by accent within a language (e.g., US English vs UK English)
