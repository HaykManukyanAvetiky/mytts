# Tasks: Additional Language Voices

## Slice 1: Add Spanish Voices (First Language)
_After this slice: Users can select and generate TTS with Spanish voices_

- [x] **Sub-task 1.1:** Query Edge TTS to discover all available Spanish voices (es-ES, es-MX, es-AR, es-CO, etc.) and document their IDs, names, and genders. **[Agent: python-expert]**
- [x] **Sub-task 1.2:** Add all Spanish voice entries to `backend/config.py` with appropriate metadata (name, gender, accent, language, style, description). **[Agent: python-expert]**
- [x] **Sub-task 1.3:** Test that Spanish voices appear in the voice dropdown and generate audio correctly with sample Spanish text. **[Agent: python-expert]**

## Slice 2: Add French Voices
_After this slice: Users can select and generate TTS with French voices_

- [x] **Sub-task 2.1:** Query Edge TTS to discover all available French voices (fr-FR, fr-CA, fr-BE, fr-CH) and document their details. **[Agent: python-expert]**
- [x] **Sub-task 2.2:** Add all French voice entries to `backend/config.py` with appropriate metadata. **[Agent: python-expert]**
- [x] **Sub-task 2.3:** Test that French voices appear in the dropdown and generate audio correctly with sample French text. **[Agent: python-expert]**

## Slice 3: Add German Voices
_After this slice: Users can select and generate TTS with German voices_

- [x] **Sub-task 3.1:** Query Edge TTS to discover all available German voices (de-DE, de-AT, de-CH) and document their details. **[Agent: python-expert]**
- [x] **Sub-task 3.2:** Add all German voice entries to `backend/config.py` with appropriate metadata. **[Agent: python-expert]**
- [x] **Sub-task 3.3:** Test that German voices appear in the dropdown and generate audio correctly with sample German text. **[Agent: python-expert]**

## Slice 4: Add Portuguese Voices
_After this slice: Users can select and generate TTS with Portuguese voices_

- [x] **Sub-task 4.1:** Query Edge TTS to discover all available Portuguese voices (pt-BR, pt-PT) and document their details. **[Agent: python-expert]**
- [x] **Sub-task 4.2:** Add all Portuguese voice entries to `backend/config.py` with appropriate metadata. **[Agent: python-expert]**
- [x] **Sub-task 4.3:** Test that Portuguese voices appear in the dropdown and generate audio correctly with sample Portuguese text. **[Agent: python-expert]**

## Slice 5: Update Preview Script for Multi-Language Support
_After this slice: Preview script supports generating previews in each voice's native language_

- [x] **Sub-task 5.1:** Update `scripts/generate_voice_previews.py` to include language-specific preview texts (Spanish, French, German, Portuguese). **[Agent: python-expert]**
- [x] **Sub-task 5.2:** Modify the script to select preview text based on the voice's `language` field. **[Agent: python-expert]**

## Slice 6: Generate Voice Preview Files
_After this slice: All new language voices have preview audio files users can listen to_

- [x] **Sub-task 6.1:** Run the updated preview script to generate MP3 preview files for all new Spanish, French, German, and Portuguese voices. **[Agent: python-expert]**
- [x] **Sub-task 6.2:** Verify all preview files are created in `static/audio/previews/` and play correctly in the browser. **[Agent: python-expert]**

## Slice 7: Final Verification and Regression Testing
_After this slice: Feature is complete and verified working_

- [x] **Sub-task 7.1:** Verify English voices remain the default and work exactly as before. **[Agent: python-expert]**
- [x] **Sub-task 7.2:** Test speech rate controls (0.75x - 1.5x) with at least one voice from each new language. **[Agent: python-expert]**
- [x] **Sub-task 7.3:** Test pitch controls (-20% to +20%) with at least one voice from each new language. **[Agent: python-expert]**
