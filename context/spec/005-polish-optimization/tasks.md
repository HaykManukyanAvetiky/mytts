# Task List: Polish & Optimization

**Objective:** Add responsive design support for tablet and large phone devices, and improve first-time user experience with clear placeholder text.

---

## Slice 1: Update Placeholder Text
**Goal:** First-time users see helpful instructions in the text area

- [x] **Update textarea placeholder**
  - [x] Open `backend/templates/index.html`
  - [x] Change placeholder from `"Enter your text here..."` to `"Paste your script here..."`
  - [x] Test: Refresh page → New placeholder text appears
  - [x] Test: Type text → Placeholder disappears
  - [x] Test: Clear text → Placeholder reappears

**Verification:** App works as before. Placeholder text is more instructive for content creators.

---

## Slice 2: Add Tablet Breakpoint (768px-1023px)
**Goal:** Interface adapts appropriately on tablet-sized screens

- [x] **Add tablet media query**
  - [x] Open `static/css/styles.css`
  - [x] Add `@media (max-width: 1023px)` query with container adjustments
  - [x] Test: Resize browser to 900px → Container uses full width with appropriate padding
  - [x] Test: All controls remain side-by-side at this size

**Verification:** App displays correctly on tablet screens. No layout breaks.

---

## Slice 3: Add Large Phone Breakpoint (480px-767px)
**Goal:** Controls stack vertically on smaller screens for better usability

- [x] **Add large phone media query**
  - [x] Open `static/css/styles.css`
  - [x] Add `@media (max-width: 767px)` query
  - [x] Add `.control-row { flex-direction: column }` to stack Speed/Pitch dropdowns
  - [x] Add `.voice-selector { flex-direction: column }` to stack voice dropdown and preview button
  - [x] Add full-width rules for `.voice-dropdown` and `.btn-preview`
  - [x] Test: Resize browser to 600px → Speed/Pitch dropdowns stack vertically
  - [x] Test: Voice selector and Preview button stack vertically
  - [x] Test: All elements take full container width

**Verification:** App is usable on large phone screens with stacked controls.

---

## Slice 4: Add Small Phone Breakpoint (below 480px) & Touch Targets
**Goal:** Reduced padding and guaranteed touch-friendly tap targets on smallest supported screens

- [x] **Add small phone media query**
  - [x] Open `static/css/styles.css`
  - [x] Add `@media (max-width: 479px)` query
  - [x] Add reduced header font sizes (h1: 1.75rem, subtitle: 0.875rem)
  - [x] Add reduced container and form-container padding
  - [x] Add `min-height: 44px` for all interactive elements (buttons, dropdowns)
  - [x] Test: Resize browser to 400px → Reduced padding and font sizes apply
  - [x] Test: All buttons and dropdowns have adequate tap target size

**Verification:** App remains functional on smallest supported screens with touch-friendly controls.

---

## Slice 5: Remove Old 640px Media Query
**Goal:** Clean up CSS by removing redundant breakpoint

- [x] **Refactor existing media query**
  - [x] Open `static/css/styles.css`
  - [x] Locate existing `@media (max-width: 640px)` query
  - [x] Verify all its rules are covered by new breakpoints (479px and 767px)
  - [x] Remove the old 640px media query
  - [x] Test: Resize through all breakpoints → No visual regressions

**Verification:** CSS is clean with no overlapping breakpoints. All responsive behavior intact.

---

## Slice 6: Comprehensive Testing & Verification
**Goal:** Verify all acceptance criteria and cross-browser compatibility

- [x] **Desktop Testing (1024px+)**
  - [x] Layout unchanged from current design
  - [x] All controls side-by-side

- [x] **Tablet Testing (768px-1023px)**
  - [x] Container adapts with appropriate spacing
  - [x] All elements accessible and properly sized

- [x] **Large Phone Testing (480px-767px)**
  - [x] Speed/Pitch dropdowns stack vertically
  - [x] Voice selector and Preview button stack vertically
  - [x] Text area usable for text entry

- [x] **Small Phone Testing (below 480px)**
  - [x] Reduced padding and font sizes apply
  - [x] All interactive elements have 44px minimum touch targets

- [x] **Cross-Browser Testing**
  - [x] Chrome on desktop
  - [x] Firefox on desktop
  - [x] Safari on desktop

- [x] **Functional Regression**
  - [x] Voice selection still works
  - [x] Speed/Pitch controls still work
  - [x] Audio generation still works
  - [x] Audio playback and download still work

**Verification:** All acceptance criteria from functional spec are met. No regressions.

---

## Slice 7: Documentation Update
**Goal:** Update project documentation to reflect completion

- [x] **Update roadmap**
  - [x] Open `context/product/roadmap.md`
  - [x] Mark "Polish & Optimization" as completed [x]
  - [x] Mark "Responsive Design" as completed [x]
  - [x] Mark "Clear Instructions" as completed [x]

- [x] **Update spec status**
  - [x] Open `context/spec/005-polish-optimization/functional-spec.md`
  - [x] Update status from "Draft" to "✅ Completed"
  - [x] Mark all acceptance criteria as [x]

**Verification:** Documentation reflects Phase 3 Polish & Optimization as complete.

---

## Summary

| Slice | Description | Key Files |
|-------|-------------|-----------|
| 1 | Update placeholder text | `index.html` |
| 2 | Tablet breakpoint (1023px) | `styles.css` |
| 3 | Large phone breakpoint (767px) | `styles.css` |
| 4 | Small phone breakpoint (479px) + touch targets | `styles.css` |
| 5 | Remove old 640px query | `styles.css` |
| 6 | Comprehensive testing | (testing only) |
| 7 | Documentation update | `roadmap.md`, `functional-spec.md` |

**Total Slices:** 7
**Files Modified:** 3 (`styles.css`, `index.html`, `roadmap.md`)

Each slice keeps the application runnable and adds incremental value.
