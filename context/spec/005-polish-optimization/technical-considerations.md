# Technical Specification: Polish & Optimization

- **Functional Specification:** [005-polish-optimization/functional-spec.md](./functional-spec.md)
- **Status:** ✅ Completed
- **Author:** Engineering Team

---

## 1. High-Level Technical Approach

This feature is a **CSS-only implementation** with one minor HTML update. No backend or JavaScript changes are required.

**Summary:**
- Add two new CSS media query breakpoints for tablet (768px) and large phone (480px)
- Stack Speed/Pitch dropdowns vertically on screens below 768px
- Make voice selector full-width on smaller screens
- Update placeholder text to be more instructive
- Ensure minimum 44px touch targets for all interactive elements

---

## 2. Proposed Solution & Implementation Plan (The "How")

### 2.1 CSS Changes (`static/css/styles.css`)

#### New Media Query: Tablet (max-width: 1023px)

```css
@media (max-width: 1023px) {
    .container {
        max-width: 100%;
        padding: var(--spacing-lg) var(--spacing-md);
    }
}
```

#### New Media Query: Small Tablet / Large Phone (max-width: 767px)

```css
@media (max-width: 767px) {
    /* Stack Speed/Pitch dropdowns vertically */
    .control-row {
        flex-direction: column;
        gap: var(--spacing-sm);
    }

    /* Voice selector takes full width, stack with preview button */
    .voice-selector {
        flex-direction: column;
        gap: var(--spacing-sm);
    }

    .voice-dropdown {
        width: 100%;
    }

    .btn-preview {
        width: 100%;
    }
}
```

#### Updated Media Query: Large Phone (max-width: 479px)

```css
@media (max-width: 479px) {
    header h1 {
        font-size: 1.75rem;
    }

    .subtitle {
        font-size: 0.875rem;
    }

    .container {
        padding: var(--spacing-sm);
    }

    .form-container {
        padding: var(--spacing-sm);
    }

    /* Ensure adequate touch targets */
    .btn-primary,
    .btn-secondary,
    .btn-preview,
    .voice-dropdown,
    .control-dropdown {
        min-height: 44px;
    }
}
```

#### Update Existing 640px Media Query

The existing `@media (max-width: 640px)` query will be **removed** and its rules integrated into the new breakpoints above to avoid overlap and confusion.

### 2.2 HTML Changes (`backend/templates/index.html`)

#### Update Placeholder Text

Change the textarea placeholder from:
```html
placeholder="Enter your text here..."
```

To:
```html
placeholder="Paste your script here..."
```

---

## 3. Impact and Risk Analysis

### System Dependencies

| Component | Impact |
|-----------|--------|
| `static/css/styles.css` | New media queries added, existing 640px query refactored |
| `backend/templates/index.html` | Minor placeholder text update |
| No backend changes | N/A |
| No JavaScript changes | N/A |

### Potential Risks & Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Layout breaks on edge-case screen sizes | Low | Medium | Test on multiple device simulators and real devices |
| Existing 640px query removal causes regression | Low | Low | Integrate all existing rules into new breakpoint structure |
| Touch targets too small on some devices | Very Low | Low | Enforce 44px minimum height on interactive elements |

---

## 4. Testing Strategy

### Manual Testing Checklist

**Desktop (1024px+):**
- [ ] Layout unchanged from current design
- [ ] All controls side-by-side as before

**Tablet (768px-1023px):**
- [ ] Container adapts with appropriate spacing
- [ ] All elements remain accessible and properly sized

**Large Phone (480px-767px):**
- [ ] Speed/Pitch dropdowns stack vertically
- [ ] Voice selector and Preview button stack vertically
- [ ] All elements take full container width
- [ ] Text area remains usable for text entry

**Small Phone (below 480px):**
- [ ] Reduced padding and font sizes apply
- [ ] All interactive elements have minimum 44px touch targets
- [ ] Interface remains functional (though out-of-scope for optimization)

**Placeholder Text:**
- [ ] New placeholder "Paste your script here..." appears when textarea is empty
- [ ] Placeholder disappears when user types
- [ ] Placeholder reappears when text is cleared

**Cross-Browser:**
- [ ] Chrome, Firefox, Safari on desktop
- [ ] Chrome, Safari on mobile/tablet

---

## 5. Files to Modify

| File | Changes |
|------|---------|
| `static/css/styles.css` | Add tablet/phone media queries, refactor existing 640px query |
| `backend/templates/index.html` | Update textarea placeholder text |
