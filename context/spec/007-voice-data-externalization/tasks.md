# Tasks: Voice Data Externalization

## Slice 1: Create Voice Data JSON File
_After this slice: JSON file exists with all 78 voices; app still runs using hardcoded config_

- [x] **Sub-task 1.1:** Create `backend/data/` directory if it doesn't exist. **[Agent: python-expert]**
- [x] **Sub-task 1.2:** Extract all 78 voice configurations from `backend/config.py` and write to `backend/data/voices.json` with proper schema (version, updated, voices array). **[Agent: python-expert]**
- [x] **Sub-task 1.3:** Validate JSON file is valid and contains all required fields for each voice. **[Agent: python-expert]**

## Slice 2: Add JSON Loading Infrastructure
_After this slice: Loading function exists and is tested; app still runs using hardcoded config_

- [x] **Sub-task 2.1:** Add `VoicesConfig` Pydantic model to `backend/config.py` for validating JSON structure. **[Agent: python-expert]**
- [x] **Sub-task 2.2:** Add `VoiceLoadError` custom exception class to `backend/config.py`. **[Agent: python-expert]**
- [x] **Sub-task 2.3:** Add `load_voices_from_json()` function with `@lru_cache` decorator to `backend/config.py`. **[Agent: python-expert]**
- [x] **Sub-task 2.4:** Test the loading function independently to verify it returns correct voice count and data. **[Agent: python-expert]**

## Slice 3: Switch to JSON-Based Voice Loading
_After this slice: App loads voices from JSON file; API returns same data as before_

- [x] **Sub-task 3.1:** Modify `get_voices()` function to call `load_voices_from_json()` instead of returning hardcoded list. **[Agent: python-expert]**
- [x] **Sub-task 3.2:** Test `/api/tts/voices` endpoint returns all 78 voices with correct data. **[Agent: python-expert]**
- [x] **Sub-task 3.3:** Test TTS generation works with at least one voice from each language. **[Agent: python-expert]**

## Slice 4: Add Startup Validation
_After this slice: Server fails fast with clear error if JSON is missing or invalid_

- [x] **Sub-task 4.1:** Add voice loading validation to `backend/main.py` startup sequence. **[Agent: python-expert]**
- [x] **Sub-task 4.2:** Test error handling: rename JSON file and verify server fails with "file not found" message. **[Agent: python-expert]**
- [x] **Sub-task 4.3:** Test error handling: corrupt JSON syntax and verify server fails with parse error message. **[Agent: python-expert]**
- [x] **Sub-task 4.4:** Test error handling: remove required field from one voice and verify server fails with validation error. **[Agent: python-expert]**

## Slice 5: Remove Hardcoded Voices from Config
_After this slice: config.py is clean (~80 lines); all voice data in JSON only_

- [x] **Sub-task 5.1:** Remove all `VoiceInfo(...)` instances from `backend/config.py`. **[Agent: python-expert]**
- [x] **Sub-task 5.2:** Verify `config.py` is reduced to ~80 lines or less. **[Agent: python-expert]**
- [x] **Sub-task 5.3:** Verify server starts successfully and `/api/tts/voices` still returns all 78 voices. **[Agent: python-expert]**

## Slice 6: Final Verification and Regression Testing
_After this slice: Feature is complete and fully verified_

- [x] **Sub-task 6.1:** Verify API response format is identical to previous implementation. **[Agent: python-expert]**
- [x] **Sub-task 6.2:** Test speech rate controls with one voice per language. **[Agent: python-expert]**
- [x] **Sub-task 6.3:** Test pitch controls with one voice per language. **[Agent: python-expert]**
- [x] **Sub-task 6.4:** Verify frontend voice selector works without modification. **[Agent: python-expert]**
