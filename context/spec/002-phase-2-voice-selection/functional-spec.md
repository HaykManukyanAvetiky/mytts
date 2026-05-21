# Functional Specification: Phase 2 - Voice Selection

- **Roadmap Item:** Phase 2: Voice Options & Output
- **Status:** ✅ Completed
- **Author:** Product Team

---

## 1. Overview and Rationale (The "Why")

### Purpose
Enhance the MyTTS application by allowing users to choose from multiple English voices and preview them before generating their full script. This addresses the need for content creators to match voice characteristics to their content style (professional vs casual, male vs female, different accents).

### User Pain Point
Content creators currently have only one voice option (en-US-GuyNeural). Different types of content require different voice characteristics:
- Professional narrations need authoritative voices
- Casual content needs friendly, conversational voices
- Educational content benefits from clear, neutral voices
- Different audiences prefer different accents (US, UK, Australian, etc.)

### Desired Outcome
Enable users to:
1. Browse available English voices by category (gender, accent, style)
2. Hear short preview samples of each voice before committing to full generation
3. Select their preferred voice for TTS generation
4. Remember their last selected voice for convenience

### Success Metrics
- Users can preview at least 5 different English voices
- Voice preview plays within 1 second of clicking
- Users can change voice selection and re-generate with different voice
- 80%+ of users find a voice that suits their content needs

---

## 2. Functional Requirements (The "What")

### 2.1 Voice Dropdown Menu

**As a** content creator, **I want to** select from multiple English voices, **so that** I can choose the voice that best fits my content style.

**Acceptance Criteria:**
- [ ] A voice selection dropdown is displayed above or near the text input field
- [ ] The dropdown shows at least 5 different English voice options
- [ ] Each voice option displays: Voice name, Gender, and Accent (e.g., "Guy (Male, US)")
- [ ] The dropdown has a default selection (current: en-US-GuyNeural)
- [ ] Users can change the voice selection before or after entering text
- [ ] The selected voice is used for TTS generation when clicking "Generate Speech"
- [ ] The dropdown remains visible and accessible at all times

**Voice Categories:**
The dropdown should include voices representing:
- **Gender diversity**: Male and Female voices
- **Accent variety**: US, UK, Australian English
- **Style variety**: Professional, Friendly, Neutral

**Minimum Voice Set (5 voices):**
1. **en-US-GuyNeural** (Male, US) - Professional/Default
2. **en-US-JennyNeural** (Female, US) - Friendly
3. **en-GB-RyanNeural** (Male, UK) - Professional British
4. **en-GB-SoniaNeural** (Female, UK) - Neutral British
5. **en-AU-NatashaNeural** (Female, Australian) - Friendly Australian

### 2.2 Voice Preview Feature

**As a** content creator, **I want to** hear a short sample of each voice, **so that** I can make an informed decision before generating my full script.

**Acceptance Criteria:**
- [ ] Each voice option in the dropdown has a "Preview" button/icon next to it
- [ ] When clicking Preview, a short audio sample plays immediately
- [ ] The preview sample is 5-10 seconds long
- [ ] The preview sample text is consistent across all voices (e.g., "Hello, this is a preview of this voice. I can help you create natural-sounding speech for your videos and podcasts.")
- [ ] Preview audio plays without requiring full page generation
- [ ] Only one preview can play at a time (starting a new preview stops the previous one)
- [ ] A visual indicator shows which preview is currently playing
- [ ] Preview works even if no text is entered in the main text field

**Preview Interaction:**
- [ ] Click preview icon → Immediate audio playback
- [ ] Visual feedback: Icon changes to "Playing..." or shows loading state
- [ ] After preview completes: Icon returns to normal state
- [ ] User can stop preview by clicking the icon again

### 2.3 Voice Selection Persistence

**As a** content creator, **I want** the application to remember my last selected voice, **so that** I don't have to re-select it every time I use the app.

**Acceptance Criteria:**
- [ ] When a user selects a voice, it is saved to browser localStorage
- [ ] When the user returns to the application, the last selected voice is pre-selected in the dropdown
- [ ] If no voice has been selected before, the default voice (en-US-GuyNeural) is used
- [ ] Clearing browser data resets to the default voice

### 2.4 Voice Integration with TTS Generation

**As a** content creator, **I want** my selected voice to be used for TTS generation, **so that** I get audio in the voice I chose.

**Acceptance Criteria:**
- [ ] When "Generate Speech" is clicked, the currently selected voice is used
- [ ] The generated audio reflects the selected voice characteristics
- [ ] Users can generate with one voice, then change voice and re-generate without refreshing
- [ ] The audio filename includes a voice identifier (optional enhancement)
- [ ] Error messages clearly indicate if voice selection fails

### 2.5 Voice Information Display

**As a** content creator, **I want to** see information about each voice, **so that** I can understand the characteristics before selecting.

**Acceptance Criteria:**
- [ ] Each voice option displays: Name, Gender, and Accent/Region
- [ ] A tooltip or info icon provides additional details when hovered/clicked:
  - Voice style (Professional, Friendly, Neutral, etc.)
  - Best use cases (e.g., "Great for podcasts and narrations")
- [ ] The currently selected voice is clearly highlighted in the dropdown

---

## 3. Scope and Boundaries

### In-Scope for Phase 2

- Voice selection dropdown with at least 5 English voices
- Voice preview functionality with short audio samples
- Voice persistence using browser localStorage
- Integration of selected voice with TTS generation
- Voice information display (name, gender, accent)
- Visual feedback during preview playback

### Out-of-Scope for Phase 2

- **Voice customization** (speed, pitch, volume adjustments) - deferred to future phase
- **Multiple language support** (non-English voices) - deferred to future phase
- **Custom voice upload** or user-trained voices - out of scope for entire project
- **Voice comparison feature** (side-by-side comparison) - deferred to future phase
- **Voice favoriting/bookmarking** - deferred to future phase
- **Advanced voice filtering** (by age, emotion, etc.) - deferred to future phase
- **Voice recommendations** based on content type - deferred to future phase

---

## 4. User Stories Summary

1. **Voice Selection**: Select from dropdown → Generate with chosen voice
2. **Voice Preview**: Click preview icon → Hear 5-10 second sample → Make informed choice
3. **Voice Persistence**: Select voice → Return to app later → Voice still selected
4. **Voice Information**: Hover/view voice details → Understand characteristics → Select appropriate voice

---

## 5. Error Scenarios

| Scenario | Error Message | User Action |
|----------|--------------|-------------|
| Preview audio fails to load | "Unable to load voice preview. Please try again." | Click preview again or select different voice |
| Selected voice unavailable during generation | "The selected voice is currently unavailable. Using default voice instead." | Generation continues with default voice |
| No voices available (API issue) | "Voice options unavailable. Using default voice." | Can still generate with default voice |

---

## 6. Technical Considerations (High-Level)

- Voice preview audio samples should be pre-generated and cached for fast loading
- Voice metadata (name, gender, accent, description) should be stored in configuration
- Edge TTS supports multiple voices - full list available via `edge-tts --list-voices`
- Voice selection should be passed to backend API in the request payload
- Preview samples should be served as static files to avoid regeneration

---

## 7. Success Criteria

Phase 2 will be considered successful when:
- [ ] Users can select from at least 5 different English voices
- [ ] Voice preview samples play within 1 second
- [ ] Generated audio uses the selected voice correctly
- [ ] Voice selection persists across browser sessions
- [ ] All voice metadata is displayed clearly
- [ ] Error handling works for all voice-related failures
