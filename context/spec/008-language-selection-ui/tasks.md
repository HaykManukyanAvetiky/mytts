# Tasks: Language Selection UI

**Specification:** `context/spec/008-language-selection-ui/`
**Status:** Ready for Implementation

---

## Slice 1: Add `/languages` API endpoint
*Smallest piece of backend functionality - returns list of available languages*

- [x] **1.1** Add `LanguageListResponse` model to `backend/models/responses.py` **[Agent: fastapi-expert]**
- [x] **1.2** Add `GET /api/tts/languages` endpoint to `backend/api/routes/tts.py` that returns sorted unique languages from voices.json **[Agent: fastapi-expert]**
- [x] **1.3** Verify endpoint works: `curl http://localhost:8000/api/tts/languages` returns 5 languages **[Agent: fastapi-expert]**

---

## Slice 2: Add language filtering to `/voices` endpoint
*Extend existing endpoint with optional query parameter - backward compatible*

- [x] **2.1** Modify `GET /api/tts/voices` to accept optional `?language=` query parameter **[Agent: fastapi-expert]**
- [x] **2.2** Add language validation - return 400 with available languages list for invalid language **[Agent: fastapi-expert]**
- [x] **2.3** Verify backward compatibility: `curl http://localhost:8000/api/tts/voices` still returns all 78 voices **[Agent: fastapi-expert]**
- [x] **2.4** Verify filtering: `curl http://localhost:8000/api/tts/voices?language=English` returns only English voices **[Agent: fastapi-expert]**

---

## Slice 3: Add language dropdown to frontend UI
*Visible UI element with static "All Languages" option - not yet wired to API*

- [x] **3.1** Add `selectedLanguage` and `languages` state properties to `ttsApp()` in `static/js/app.js` **[Agent: alpine-js-expert]**
- [x] **3.2** Add `.language-section` CSS styles to `static/css/styles.css` **[Agent: alpine-js-expert]**
- [x] **3.3** Add language dropdown HTML above voice dropdown in `backend/templates/index.html` **[Agent: alpine-js-expert]**
- [ ] **3.4** Verify dropdown appears in browser with "All Languages" option visible **[Agent: alpine-js-expert]**

---

## Slice 4: Wire language dropdown to API
*Language dropdown now fetches and displays actual languages from backend*

- [ ] **4.1** Add `loadLanguages()` method to `ttsApp()` that fetches from `/api/tts/languages` **[Agent: alpine-js-expert]**
- [ ] **4.2** Update `init()` to call `loadLanguages()` on page load **[Agent: alpine-js-expert]**
- [ ] **4.3** Verify dropdown shows all 5 languages: English, French, German, Portuguese, Spanish **[Agent: alpine-js-expert]**

---

## Slice 5: Implement language filtering behavior
*Selecting a language filters the voice dropdown*

- [ ] **5.1** Add `onLanguageChange()` method that re-fetches voices with `?language=` parameter **[Agent: alpine-js-expert]**
- [ ] **5.2** Update `loadVoices()` to use `selectedLanguage` when fetching voices **[Agent: alpine-js-expert]**
- [ ] **5.3** Wire `@change="onLanguageChange"` to language dropdown in template **[Agent: alpine-js-expert]**
- [ ] **5.4** Verify selecting "Spanish" shows only Spanish voices in voice dropdown **[Agent: alpine-js-expert]**

---

## Slice 6: Default to English and auto-select first voice
*Polish the default behavior and voice reset on language change*

- [ ] **6.1** Set `selectedLanguage: 'English'` as default in `ttsApp()` **[Agent: alpine-js-expert]**
- [ ] **6.2** Ensure `onLanguageChange()` auto-selects first voice when language changes **[Agent: alpine-js-expert]**
- [ ] **6.3** Verify page loads with English pre-selected and English voices visible **[Agent: alpine-js-expert]**
- [ ] **6.4** Verify changing language to French auto-selects first French voice **[Agent: alpine-js-expert]**

---

## Slice 7: Add backend tests
*Automated tests for new API functionality*

- [ ] **7.1** Create `tests/integration/test_language_api.py` with test fixtures **[Agent: pytest-expert]**
- [ ] **7.2** Add test for `/languages` endpoint returning 5 languages **[Agent: pytest-expert]**
- [ ] **7.3** Add test for `/voices?language=English` filtering correctly **[Agent: pytest-expert]**
- [ ] **7.4** Add test for `/voices?language=InvalidLang` returning 400 error **[Agent: pytest-expert]**
- [ ] **7.5** Add test for `/voices` without parameter returning all voices (backward compatibility) **[Agent: pytest-expert]**
- [ ] **7.6** Run all tests and verify they pass: `pytest tests/integration/test_language_api.py -v` **[Agent: pytest-expert]**

---

## Summary

| Slice | Description | Agent(s) | Tasks |
|-------|-------------|----------|-------|
| 1 | `/languages` endpoint | fastapi-expert | 3 |
| 2 | `/voices?language=` filter | fastapi-expert | 4 |
| 3 | Language dropdown UI | alpine-js-expert | 4 |
| 4 | Wire dropdown to API | alpine-js-expert | 3 |
| 5 | Filtering behavior | alpine-js-expert | 4 |
| 6 | Default & auto-select | alpine-js-expert | 4 |
| 7 | Backend tests | pytest-expert | 6 |

**Total: 7 slices, 28 tasks**
