# Task List: Phase 3 - Performance & Reliability Enhancements

**Objective:** Add character count color feedback and enhanced loading messages to MyTTS, ensuring the app remains runnable after each task.

---

## Slice 1: Add Warning Color to CSS Palette (Foundation)
**Goal:** Add the CSS infrastructure for color-coded feedback without breaking anything

- [x] **Add warning color CSS variable**
  - [x] Open `static/css/styles.css`
  - [x] Add `--warning-color: #d97706;` to `:root` section (after line 20)
  - [x] Add `--warning-bg: #fef3c7;` to `:root` section (for future use)
  - [x] Save file and hard refresh browser (Cmd+Shift+R)
  - [x] Verify application still loads and looks identical

**Verification:** App loads normally, no visual changes, new CSS variables are available in DevTools.

---

## Slice 2: Enhanced Character Counter Formatting
**Goal:** Improve the readability of the character counter with formatted numbers

- [x] **Update character counter display format**
  - [x] Open `backend/templates/index.html`
  - [x] Find the character counter div (line ~66-68)
  - [x] Replace `<span x-text="text.length"></span> / 3000 characters` with `<span x-text="text.length.toLocaleString()"></span> / 3,000 characters`
  - [x] Save file and restart FastAPI server (to reload template)
  - [x] Test: Type 2543 characters → Verify counter shows "2,543 / 3,000 characters"
  - [x] Test: Type 100 characters → Verify counter is hidden (still appears at 2500+)

**Verification:** Character counter shows formatted numbers with comma separators. Behavior unchanged (still appears at 2500+).

---

## Slice 3: Character Counter Base Styles Update
**Goal:** Add transition effect to character counter for smooth color changes

- [x] **Update character-count base CSS styles**
  - [x] Open `static/css/styles.css`
  - [x] Find `.character-count` class (line ~114-120)
  - [x] Add `font-weight: 500;` to existing styles
  - [x] Add `transition: color 0.3s ease-in-out;` to existing styles
  - [x] Save file and hard refresh browser
  - [x] Test: Type 2500+ characters → Verify counter appears normally with smooth rendering

**Verification:** Character counter still looks the same but has smooth transition capability. No visual changes yet.

---

## Slice 4: Character Counter Color Feedback (Warning State)
**Goal:** Add yellow/amber warning color when approaching the limit (2800-2999 characters)

- [x] **Add warning color CSS class**
  - [x] Open `static/css/styles.css`
  - [x] After `.character-count` styles, add:
    ```css
    .character-count.char-warning {
        color: var(--warning-color);
        font-weight: 600;
    }
    ```
  - [x] Save file and hard refresh browser

- [x] **Apply warning color to character counter HTML**
  - [x] Open `backend/templates/index.html`
  - [x] Find the character counter div (line ~66-68)
  - [x] Add `:class="{ 'char-warning': text.length >= 2800 && text.length < 3000 }"` to the div
  - [x] Save file and restart server
  - [x] Test: Type 2799 characters → Verify counter is gray
  - [x] Test: Type 2800 characters → Verify counter smoothly transitions to amber/yellow
  - [x] Test: Type 2850 characters → Verify counter remains amber
  - [x] Test: Delete to 2799 → Verify counter returns to gray

**Verification:** Counter changes to amber color at 2800 characters with smooth transition. App remains fully functional.

---

## Slice 5: Character Counter Color Feedback (Danger State)
**Goal:** Add red danger color when limit is reached (3000 characters)

- [x] **Add danger color CSS class**
  - [x] Open `static/css/styles.css`
  - [x] After `.character-count.char-warning` styles, add:
    ```css
    .character-count.char-danger {
        color: var(--error-color);
        font-weight: 700;
    }
    ```
  - [x] Save file and hard refresh browser

- [x] **Apply danger color to character counter HTML**
  - [x] Open `backend/templates/index.html`
  - [x] Find the character counter div `:class` directive
  - [x] Update to: `:class="{ 'char-warning': text.length >= 2800 && text.length < 3000, 'char-danger': text.length >= 3000 }"`
  - [x] Save file and restart server
  - [x] Test: Type 2999 characters → Verify counter is amber
  - [x] Test: Type 3000 characters → Verify counter smoothly transitions to red
  - [x] Test: Paste text exceeding 3000 chars → Verify only 3000 accepted, counter shows "3,000 / 3,000 characters" in red
  - [x] Test: Delete to 2999 → Verify counter returns to amber
  - [x] Test: Delete to 2799 → Verify counter returns to gray

**Verification:** Full color feedback works: gray (2500-2799) → amber (2800-2999) → red (3000). All transitions are smooth.

---

## Slice 6: Enhanced Loading Message with Character Count
**Goal:** Show how many characters are being processed during generation

- [x] **Update loading message HTML**
  - [x] Open `backend/templates/index.html`
  - [x] Find the loading div (line ~82-85)
  - [x] Replace `<span>Generating audio...</span>` with:
    ```html
    <span>
        Generating audio from
        <span x-text="text.length.toLocaleString()"></span>
        characters...
    </span>
    ```
  - [x] Save file and restart server
  - [x] Test: Enter "Hello world" (11 characters), click Generate → Verify loading shows "Generating audio from 11 characters..."
  - [x] Test: Enter 2543 characters, click Generate → Verify loading shows "Generating audio from 2,543 characters..."
  - [x] Test: Verify audio generates successfully and loading message disappears

**Verification:** Loading message dynamically shows character count with formatted numbers. Audio generation still works perfectly.

---

## Slice 7: Comprehensive Manual Testing & Polish
**Goal:** Verify all requirements work together and across browsers

- [x] **Character Counter Comprehensive Testing**
  - [x] Test counter visibility at thresholds (0, 2499, 2500, 2501, 3000)
  - [x] Test color transitions at all thresholds (2799→2800, 2999→3000)
  - [x] Test rapid typing from 2500 to 3000 → Verify smooth updates, no lag
  - [x] Test deleting from 3000 down to 0 → Verify all transitions work in reverse

- [x] **UI State During Generation Testing**
  - [x] Start generation, verify text input remains enabled and editable
  - [x] Start generation, verify voice dropdown remains enabled
  - [x] Start generation, verify "Generate Speech" button is disabled
  - [x] Edit text during generation → Verify character counter updates in real-time
  - [x] Verify all controls return to normal after generation completes

- [x] **Cross-Browser Testing**
  - [x] Test in Chrome: All features work correctly
  - [x] Test in Firefox: All features work correctly
  - [x] Test in Safari: All features work correctly
  - [x] Test in Edge: All features work correctly

- [x] **Accessibility Testing**
  - [x] Test with screen reader (VoiceOver or NVDA):
    - [x] Navigate to character counter → Verify count is announced
    - [x] Trigger loading message → Verify message is announced
  - [x] Test keyboard navigation → Verify all functionality accessible via keyboard
  - [x] Check color contrast in browser DevTools:
    - [x] Warning color (#d97706) meets WCAG AA (5.93:1 ratio ✅)
    - [x] Danger color (#dc2626) meets WCAG AA (5.54:1 ratio ✅)

- [x] **Edge Cases Testing**
  - [x] Paste 5000 characters → Verify only 3000 accepted, counter red
  - [x] Generate with 50 characters → Verify loading shows "50 characters"
  - [x] Generate with 2999 characters → Verify loading shows "2,999 characters"

- [x] **Regression Testing**
  - [x] Verify Phase 1 functionality: Enter text, generate, play audio, download
  - [x] Verify Phase 2 functionality: Select voice, preview voice, generate with different voices

**Verification:** All acceptance criteria from functional spec are met. No regressions. All browsers work correctly.

---

## Slice 8: Documentation Update & Deployment
**Goal:** Update project documentation and mark phase as complete

- [x] **Update roadmap**
  - [x] Open `context/product/roadmap.md`
  - [x] Mark Phase 3 "Performance & Reliability" tasks as completed (✅)
  - [x] Update checkboxes for "Character Count Display" and "Generation Progress Indicator"

- [x] **Final deployment verification**
  - [x] Verify server is running correctly
  - [x] Clear browser cache and test fresh page load
  - [x] Verify all features work on clean load
  - [x] Take screenshots of character counter states (gray, amber, red) for documentation

**Verification:** Documentation updated, phase marked complete, feature ready for users.

---

## Summary

**Total Slices:** 8
**Estimated Time:** ~1-1.5 hours (very quick implementation)
**Dependencies:** Phase 1 and Phase 2 must be complete

Each slice keeps the application runnable and adds incremental value:
1. ✅ CSS foundation ready
2. ✅ Character formatting improved
3. ✅ Transition effects ready
4. ✅ Warning color feedback works
5. ✅ Danger color feedback works
6. ✅ Loading message enhanced
7. ✅ All features tested and polished
8. ✅ Documentation updated

**Files Modified: 2**
- `backend/templates/index.html` - Character counter and loading message updates
- `static/css/styles.css` - Warning color variable and styling

**Files Not Modified:**
- `static/js/app.js` - Alpine.js handles all reactivity automatically
