# Functional Specification: Voice Data Externalization

- **Roadmap Item:** Move voice configurations from hardcoded Python code to an external data source
- **Status:** Draft
- **Author:** Claude (AI Assistant)

---

## 1. Overview and Rationale (The "Why")

### Purpose
Move voice configuration data from hardcoded Python code to an external JSON file, making the codebase cleaner and voice data easier to maintain and update.

### Problem Being Solved
Currently, 78 voice configurations are hardcoded in `backend/config.py`, consuming ~900+ lines of code. This creates several issues:
- Code changes required to add/modify voices
- Large config file that's difficult to navigate
- Mixing of application logic with data
- Requires developer involvement for simple voice updates

### Desired Outcome
Voice data lives in a separate JSON file that can be edited independently of the application code. The config.py file is reduced from ~1000 lines to ~80 lines.

### Success Criteria
- All voice data stored in `backend/data/voices.json`
- `backend/config.py` contains no voice entries (only references the JSON file)
- Application loads voices from JSON on startup
- No change to API behavior or frontend functionality
- Clear error message if JSON file is missing or invalid

---

## 2. Functional Requirements (The "What")

### 2.1 Voice Data File
- Voice data must be stored in `backend/data/voices.json`
- The file must contain all 78 current voice configurations
- Each voice entry must include: id, name, gender, accent, language, style, description, preview_file
- **Acceptance Criteria:**
  - [ ] JSON file exists at `backend/data/voices.json`
  - [ ] File contains all 78 voices with complete metadata
  - [ ] File is valid JSON and can be parsed without errors

### 2.2 Application Startup Behavior
- The application must load voice data from the JSON file when the server starts
- Voices are loaded once at startup (not reloaded dynamically)
- **Acceptance Criteria:**
  - [ ] Server loads voices from JSON file on startup
  - [ ] Loaded voices are available via `/api/tts/voices` endpoint
  - [ ] Voice count matches the JSON file content

### 2.3 Error Handling
- If the JSON file is missing, the server must fail to start with a clear error message
- If the JSON file contains invalid JSON, the server must fail to start with a clear error message
- If a voice entry is missing required fields, the server must fail to start with a clear error message
- **Acceptance Criteria:**
  - [ ] Missing file: Server fails with message indicating file path
  - [ ] Invalid JSON: Server fails with message indicating parse error location
  - [ ] Invalid voice entry: Server fails with message indicating which field is missing

### 2.4 Backward Compatibility
- The API response format from `/api/tts/voices` must remain unchanged
- TTS generation with any voice must work exactly as before
- Frontend requires no changes
- **Acceptance Criteria:**
  - [ ] API response structure identical to current implementation
  - [ ] All existing voices work for TTS generation
  - [ ] Frontend voice selector works without modification

### 2.5 Code Cleanup
- Remove all hardcoded voice entries from `backend/config.py`
- Keep VoiceInfo model definition in config.py (for type validation)
- **Acceptance Criteria:**
  - [ ] No VoiceInfo instances in config.py (only the class definition)
  - [ ] config.py reduced to ~80 lines or less

---

## 3. Scope and Boundaries

### In-Scope
- Creating `backend/data/voices.json` with all voice data
- Modifying backend to load voices from JSON
- Removing hardcoded voices from config.py
- Error handling for missing/invalid JSON file
- Validating voice entries on load

### Out-of-Scope
- **Language Selection UI:** Separate roadmap item
- **Mac Desktop App:** Phase 5 roadmap item
- **Auto-reload on file change:** Voices load only on server restart
- **Admin UI for editing voices:** Manual JSON editing only
- **Voice data migration tools:** One-time manual conversion
