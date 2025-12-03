---
layout: default
title: LWC Accessibility Errors and Solutions
description: This guide provides solutions for common LWC accessibility errors encountered during Salesforce development, including error messages, causes, solutions, and prevention strategies
permalink: /rag/troubleshooting/lwc-accessibility-errors.html
---

# LWC Accessibility Errors and Solutions

> Troubleshooting guide for common Lightning Web Component accessibility errors with solutions and prevention strategies.

## Overview

This guide provides solutions for common LWC accessibility errors encountered during Salesforce development, including error messages, causes, solutions, and prevention strategies. All solutions follow WCAG 2.2 standards.

**Related Patterns**:
- <a href="{{ '/rag/mcp-knowledge/lwc-accessibility.html' | relative_url }}">LWC Accessibility Guidelines</a> - WCAG 2.2 compliance guidance
- <a href="{{ '/rag/code-examples/lwc/accessibility-examples.html' | relative_url }}">LWC Accessibility Examples</a> - Accessibility code examples
- <a href="{{ '/rag/testing/lwc-accessibility-testing.html' | relative_url }}">LWC Accessibility Testing</a> - Testing patterns

## Prerequisites

**Required Knowledge**:
- Understanding of Lightning Web Component (LWC) development
- Knowledge of HTML accessibility attributes and ARIA
- Understanding of WCAG 2.2 accessibility standards
- Familiarity with screen readers and assistive technologies
- Basic knowledge of keyboard navigation patterns

**Recommended Reading**:
- `rag/mcp-knowledge/lwc-accessibility.md` - WCAG 2.2 compliance guidance
- `rag/code-examples/lwc/accessibility-examples.md` - Accessibility code examples
- `rag/testing/lwc-accessibility-testing.md` - Testing patterns
- `rag/troubleshooting/common-lwc-errors.md` - Common LWC errors

## Common Accessibility Errors

### Error 1: Missing Form Labels

**Error Message**: "Form control has no associated label" (axe-core, Lighthouse)

**Common Causes**:
- Input field without `label` attribute
- Custom input without `<label>` element
- Placeholder text used instead of label
- Label not programmatically associated

**Solutions**:

#### Solution 1: Use Lightning Base Component Label Attribute

**Before: Missing label**
```html
<lightning-input
    name="email"
    value={email}
    onchange={handleChange}>
</lightning-input>
```

**After: With label**
```html
<lightning-input
    label="Email Address"
    name="email"
    value={email}
    onchange={handleChange}
    required>
</lightning-input>
```

#### Solution 2: Use Native Label Element

**Before: Custom input without label**
```html
<input
    type="text"
    name="customField"
    value={customValue}
    onchange={handleChange}>
```

**After: With label**
```html
<label for="custom-field">
    Custom Field
    <input
        type="text"
        id="custom-field"
        name="customField"
        value={customValue}
        onchange={handleChange}>
</label>
```

#### Solution 3: Use ARIA Label When Visual Label Not Feasible

**Before: Icon-only input**
```html
<div class="search-container">
    <lightning-icon icon-name="utility:search"></lightning-icon>
    <input type="search" name="search">
</div>
```

**After: With ARIA label**
```html
<div class="search-container">
    <lightning-icon icon-name="utility:search" alternative-text="Search"></lightning-icon>
    <input
        type="search"
        name="search"
        aria-label="Search contacts"
        aria-describedby="search-help">
    <span id="search-help" class="slds-assistive-text">Enter contact name or email</span>
</div>
```

**Prevention**:
- Always include `label` attribute for Lightning Base Components
- Use `<label>` with `for`/`id` for custom inputs
- Never rely on placeholder text alone
- Test with screen reader to verify labels are announced

---

### Error 2: Missing ARIA Labels

**Error Message**: "Element has no accessible name" (axe-core, Lighthouse)

**Common Causes**:
- Icon-only buttons without `aria-label`
- Custom interactive components without accessible names
- Decorative images without `alt=""`
- Links without descriptive text

**Solutions**:

#### Solution 1: Add ARIA Label to Icon Buttons

**Before: Icon button without label**
```html
<button class="slds-button slds-button_icon" onclick={handleClick}>
    <lightning-icon icon-name="utility:close"></lightning-icon>
</button>
```

**After: With ARIA label**
```html
<button
    class="slds-button slds-button_icon"
    onclick={handleClick}
    aria-label="Close dialog"
    title="Close">
    <lightning-icon
        icon-name="utility:close"
        alternative-text="Close">
    </lightning-icon>
    <span class="slds-assistive-text">Close</span>
</button>
```

#### Solution 2: Add ARIA Label to Custom Components

**Before: Custom toggle without label**
```html
<div class="toggle" onclick={handleToggle} tabindex="0">
    <span class="toggle-slider"></span>
</div>
```

**After: With ARIA label and role**
```html
<div
    class="toggle"
    role="switch"
    aria-label="Enable notifications"
    aria-checked={isEnabled}
    onclick={handleToggle}
    onkeydown={handleKeyDown}
    tabindex="0">
    <span class="toggle-slider"></span>
</div>
```

**Prevention**:
- Always provide `aria-label` for icon-only buttons
- Use `role` and ARIA attributes for custom components
- Test with screen reader to verify names are announced

---

### Error 3: Keyboard Traps

**Error Message**: "Focus is trapped" (manual testing, axe-core)

**Common Causes**:
- Modal dialog doesn't trap focus
- Focus escapes modal boundaries
- No way to close modal with keyboard
- Focus doesn't return after modal close

**Solutions**:

#### Solution 1: Implement Focus Trapping in Modal

**Before: Modal without focus trap**
```javascript
handleOpen() {
    this.isOpen = true;
}
```

**After: With focus trap**
```javascript
handleOpen() {
    this.isOpen = true;
    this.previousActiveElement = document.activeElement;
    this.trapFocus();
}

trapFocus() {
    const modal = this.template.querySelector('[role="dialog"]');
    const focusableElements = modal.querySelectorAll(
        'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
    );
    const firstElement = focusableElements[0];
    const lastElement = focusableElements[focusableElements.length - 1];

    modal.addEventListener('keydown', (e) => {
        if (e.key === 'Tab') {
            if (e.shiftKey) {
                if (document.activeElement === firstElement) {
                    e.preventDefault();
                    lastElement.focus();
                }
            } else {
                if (document.activeElement === lastElement) {
                    e.preventDefault();
                    firstElement.focus();
                }
            }
        }
        if (e.key === 'Escape') {
            this.handleClose();
        }
    });
}

handleClose() {
    this.isOpen = false;
    if (this.previousActiveElement) {
        this.previousActiveElement.focus();
    }
}
```

**Prevention**:
- Always trap focus in modals
- Provide Escape key to close
- Return focus to trigger element
- Test with keyboard-only navigation

---

### Error 4: Missing Focus Indicators

**Error Message**: "Focus indicator not visible" (manual testing, Lighthouse)

**Common Causes**:
- CSS removes default focus outline
- Custom focus styles don't meet contrast requirements
- Focus styles removed for mouse users
- No focus indicator on custom components

**Solutions**:

#### Solution 1: Add Visible Focus Styles

**Before: No focus indicator**
```css
.custom-button {
    border: none;
    outline: none; /* Removes focus indicator */
}
```

**After: With focus indicator**
```css
.custom-button {
    border: none;
}

.custom-button:focus {
    outline: 2px solid #0176d3;
    outline-offset: 2px;
}

.custom-button:focus-visible {
    outline: 2px solid #0176d3;
    outline-offset: 2px;
}
```

#### Solution 2: Use SLDS Focus Styles

**Before: Custom focus styles**
```css
.my-component:focus {
    outline: 1px solid gray; /* Low contrast */
}
```

**After: Using SLDS tokens**
```css
.my-component:focus {
    outline: 2px solid var(--slds-g-color-brand-base-60, #0176d3);
    outline-offset: 2px;
}
```

**Prevention**:
- Never remove focus indicators
- Use high-contrast focus styles (3:1 minimum)
- Test focus visibility on all backgrounds
- Use `:focus-visible` for mouse/keyboard distinction

---

### Error 5: Insufficient Color Contrast

**Error Message**: "Text has insufficient color contrast" (Lighthouse, axe-core)

**Common Causes**:
- Text color doesn't meet 4.5:1 contrast ratio
- Large text doesn't meet 3:1 contrast ratio
- UI components don't meet 3:1 contrast ratio
- Custom colors not tested for contrast

**Solutions**:

#### Solution 1: Use SLDS Color Tokens

**Before: Custom colors with low contrast**
```css
.error-text {
    color: #ff0000; /* Red on white: 4.0:1 - fails */
}
```

**After: Using SLDS tokens**
```css
.error-text {
    color: var(--slds-g-color-error-base-10, #c23934); /* Meets 4.5:1 */
}
```

#### Solution 2: Adjust Colors to Meet Contrast

**Before: Low contrast text**
```html
<div style="color: #999999; background: #ffffff;">
    Low contrast text
</div>
```

**After: High contrast text**
```html
<div style="color: #3e3e3c; background: #ffffff;">
    High contrast text (7.1:1 ratio)
</div>
```

**Prevention**:
- Always use SLDS color tokens
- Test contrast with WebAIM Contrast Checker
- Verify contrast on all backgrounds
- Set minimum contrast requirements (4.5:1 for normal text)

---

### Error 6: Missing Alt Text

**Error Message**: "Image has no alt text" (axe-core, Lighthouse)

**Common Causes**:
- Images without `alt` attribute
- Decorative images with descriptive alt text
- Informative images without alt text
- Image links without accessible names

**Solutions**:

#### Solution 1: Decorative Images

**Before: Decorative image without alt**
```html
<img src="/assets/divider.png" class="divider">
```

**After: With empty alt**
```html
<img
    src="/assets/divider.png"
    alt=""
    class="divider"
    aria-hidden="true">
```

#### Solution 2: Informative Images

**Before: Informative image without alt**
```html
<img src="/assets/chart.png" class="chart">
```

**After: With descriptive alt**
```html
<img
    src="/assets/chart.png"
    alt="Sales chart showing 25% increase in Q4 2023 compared to Q3 2023"
    class="chart">
```

#### Solution 3: Image Links

**Before: Image link without accessible name**
```html
<a href="/products/123">
    <img src="/product.jpg">
</a>
```

**After: With aria-label on link**
```html
<a href="/products/123" aria-label="View product details: Product Name">
    <img src="/product.jpg" alt="" aria-hidden="true">
</a>
```

**Prevention**:
- Always include `alt` attribute
- Use `alt=""` for decorative images
- Use descriptive alt text for informative images
- Provide `aria-label` for image links

---

### Error 7: Incorrect Heading Hierarchy

**Error Message**: "Heading levels should increase by one" (axe-core, Lighthouse)

**Common Causes**:
- Skipping heading levels (h1 → h3)
- Multiple h1 elements
- Headings not in logical order
- Using headings for styling only

**Solutions**:

#### Solution 1: Fix Heading Hierarchy

**Before: Skipped heading levels**
```html
<h1>Page Title</h1>
<h3>Section Title</h3> <!-- Should be h2 -->
<h4>Subsection</h4> <!-- Should be h3 -->
```

**After: Correct hierarchy**
```html
<h1>Page Title</h1>
<h2>Section Title</h2>
<h3>Subsection</h3>
```

#### Solution 2: Single h1 Per Page

**Before: Multiple h1 elements**
```html
<h1>Main Title</h1>
<h1>Another Title</h1> <!-- Should be h2 -->
```

**After: Single h1**
```html
<h1>Main Title</h1>
<h2>Another Title</h2>
```

**Prevention**:
- Start with h1, then h2, then h3
- Never skip heading levels
- Use only one h1 per page
- Use headings for structure, not styling

---

### Error 8: Missing Semantic HTML

**Error Message**: "Element has no semantic meaning" (axe-core, manual testing)

**Common Causes**:
- Using `<div>` for everything
- Missing semantic regions (header, nav, main, footer)
- Lists not using `<ul>`, `<ol>`, or `<dl>`
- Tables not using proper table structure

**Solutions**:

#### Solution 1: Use Semantic Regions

**Before: All divs**
```html
<div class="header">
    <div class="nav">...</div>
</div>
<div class="main">...</div>
<div class="footer">...</div>
```

**After: Semantic HTML**
```html
<header>
    <nav>...</nav>
</header>
<main>...</main>
<footer>...</footer>
```

#### Solution 2: Use Proper List Markup

**Before: Div list**
```html
<div class="list">
    <div class="item">Item 1</div>
    <div class="item">Item 2</div>
</div>
```

**After: Semantic list**
```html
<ul class="list">
    <li>Item 1</li>
    <li>Item 2</li>
</ul>
```

**Prevention**:
- Use semantic HTML elements
- Use `<header>`, `<nav>`, `<main>`, `<footer>`, `<section>`
- Use proper list markup (`<ul>`, `<ol>`, `<dl>`)
- Use proper table structure

---

### Error 9: Dynamic Content Not Announced

**Error Message**: "Dynamic content changes not announced" (manual testing)

**Common Causes**:
- Loading states not announced
- Error messages not announced
- Success messages not announced
- Status updates not announced

**Solutions**:

#### Solution 1: Use ARIA Live Regions

**Before: Status not announced**
```html
<div class="status">
    {statusMessage}
</div>
```

**After: With ARIA live**
```html
<div
    role="status"
    aria-live="polite"
    aria-atomic="true"
    class="status">
    {statusMessage}
</div>
```

#### Solution 2: Use Role Alert for Errors

**Before: Error not announced**
```html
<div class="error">
    {errorMessage}
</div>
```

**After: With role alert**
```html
<div
    role="alert"
    aria-live="assertive"
    class="error">
    {errorMessage}
</div>
```

**Prevention**:
- Use `aria-live="polite"` for status updates
- Use `aria-live="assertive"` for errors
- Use `role="status"` for status messages
- Use `role="alert"` for error messages

---

### Error 10: Missing ARIA Roles

**Error Message**: "Element has no programmatic role" (axe-core, Lighthouse)

**Common Causes**:
- Custom components without roles
- Interactive elements without roles
- Landmarks without roles
- Tables without proper roles

**Solutions**:

#### Solution 1: Add Role to Custom Components

**Before: Custom button without role**
```html
<div class="custom-button" onclick={handleClick}>
    Click me
</div>
```

**After: With role**
```html
<div
    class="custom-button"
    role="button"
    aria-label="Click to submit form"
    onclick={handleClick}
    onkeydown={handleKeyDown}
    tabindex="0">
    Click me
</div>
```

#### Solution 2: Add Role to Custom Controls

**Before: Custom toggle without role**
```html
<div class="toggle" onclick={handleToggle}>
    <span class="slider"></span>
</div>
```

**After: With role and state**
```html
<div
    class="toggle"
    role="switch"
    aria-checked={isChecked}
    aria-label="Enable notifications"
    onclick={handleToggle}
    onkeydown={handleKeyDown}
    tabindex="0">
    <span class="slider"></span>
</div>
```

**Prevention**:
- Always add `role` to custom interactive components
- Use appropriate ARIA roles (button, switch, checkbox, etc.)
- Add ARIA states (aria-checked, aria-expanded, etc.)
- Test with screen reader to verify roles

---

## WCAG Violation Patterns

### Pattern 1: SC 1.3.1 (iii) - Form Label Violations

**Violation**: Form control has no programmatically associated label

**Common Scenarios**:
- Input without label
- Custom input without label
- Placeholder used instead of label

**Fix**:
- Add `label` attribute to Lightning Base Components
- Use `<label>` with `for`/`id` for custom inputs
- Use `aria-label` when visual label not feasible

---

### Pattern 2: SC 2.1.1 - Keyboard Violations

**Violation**: Functionality not operable through keyboard

**Common Scenarios**:
- Custom components not keyboard accessible
- Mouse-only interactions
- Keyboard traps

**Fix**:
- Add keyboard event handlers
- Use `tabindex="0"` for focusable elements
- Implement focus trapping in modals
- Test with keyboard-only navigation

---

### Pattern 3: SC 4.1.2 (i) - Name Violations

**Violation**: Element has no accessible name

**Common Scenarios**:
- Icon buttons without labels
- Custom components without names
- Images without alt text

**Fix**:
- Add `aria-label` to icon buttons
- Add accessible names to custom components
- Add `alt` text to images

---

### Pattern 4: SC 1.4.1 - Color Contrast Violations

**Violation**: Text has insufficient color contrast

**Common Scenarios**:
- Custom colors with low contrast
- Text on colored backgrounds
- Focus indicators with low contrast

**Fix**:
- Use SLDS color tokens
- Test contrast with WebAIM Contrast Checker
- Ensure 4.5:1 for normal text, 3:1 for large text

---

## Prevention Strategies

### Development Checklist

- [ ] All form controls have labels
- [ ] All interactive elements are keyboard accessible
- [ ] Focus indicators are visible
- [ ] ARIA attributes are correct
- [ ] Color contrast meets WCAG standards
- [ ] Images have appropriate alt text
- [ ] Headings follow proper hierarchy
- [ ] Dynamic content is announced
- [ ] Modals trap focus
- [ ] Error messages are accessible

### Testing Checklist

- [ ] Run automated accessibility tests (axe-core, Lighthouse)
- [ ] Test with keyboard-only navigation
- [ ] Test with screen reader (NVDA, JAWS, VoiceOver)
- [ ] Verify color contrast
- [ ] Test all interactive states
- [ ] Test error and loading states

### Code Review Checklist

- [ ] Verify labels on all form controls
- [ ] Verify keyboard accessibility
- [ ] Verify ARIA attributes
- [ ] Verify color contrast
- [ ] Verify semantic HTML
- [ ] Verify focus management

---

## Q&A

### Q: What are the most common LWC accessibility errors?

**A**: Most common errors include: (1) **Missing form labels** (inputs without labels), (2) **Keyboard inaccessibility** (custom components not keyboard accessible), (3) **Missing focus indicators** (no visible focus styles), (4) **Insufficient color contrast** (text doesn't meet 4.5:1 ratio), (5) **Missing alt text** (images without alt attributes), (6) **Incorrect heading hierarchy** (skipped heading levels), (7) **Missing ARIA roles** (custom components without roles).

### Q: How do I fix missing form labels in LWC?

**A**: Fix missing labels by: (1) **Adding `label` attribute** to Lightning Base Components (`<lightning-input label="Email">`), (2) **Using `<label>` element** with `for`/`id` for custom inputs, (3) **Using `aria-label`** when visual label not feasible, (4) **Never using placeholder** as label replacement. All form controls must have programmatically associated labels.

### Q: How do I make custom components keyboard accessible?

**A**: Make components keyboard accessible by: (1) **Adding keyboard event handlers** (`onkeydown`, `onkeyup`), (2) **Using `tabindex="0"`** for focusable elements, (3) **Implementing Enter/Space** for activation, (4) **Implementing Escape** for cancellation, (5) **Trapping focus in modals** (prevent focus from escaping), (6) **Returning focus** to trigger element when closing.

### Q: What are the color contrast requirements for accessibility?

**A**: Color contrast requirements: (1) **Normal text** (under 18pt or 14pt bold) - **4.5:1 contrast ratio**, (2) **Large text** (18pt+ or 14pt+ bold) - **3:1 contrast ratio**, (3) **UI components** (buttons, form controls) - **3:1 contrast ratio**, (4) **Focus indicators** - **3:1 contrast ratio**. Use WebAIM Contrast Checker to verify contrast.

### Q: How do I handle images for accessibility?

**A**: Handle images by: (1) **Adding `alt` attribute** to all images, (2) **Using `alt=""`** for decorative images (empty alt), (3) **Using descriptive alt text** for informative images, (4) **Adding `aria-label`** to image links, (5) **Using `aria-hidden="true"`** for decorative images. Never omit alt attribute - use empty alt for decorative images.

### Q: What is the correct heading hierarchy?

**A**: Correct heading hierarchy: (1) **Start with h1** (one per page), (2) **Use h2** for major sections, (3) **Use h3** for subsections, (4) **Never skip levels** (h1 → h3 is wrong, use h1 → h2 → h3), (5) **Use headings for structure**, not styling. Headings should form a logical outline of the page content.

### Q: How do I announce dynamic content changes?

**A**: Announce dynamic content by: (1) **Using `aria-live="polite"`** for status updates (non-urgent), (2) **Using `aria-live="assertive"`** for errors (urgent), (3) **Using `role="status"`** for status messages, (4) **Using `role="alert"`** for error messages, (5) **Using `aria-atomic="true"`** to announce entire region. Screen readers will announce changes to live regions.

### Q: What ARIA roles should I use for custom components?

**A**: Use appropriate ARIA roles: (1) **`role="button"`** for custom buttons, (2) **`role="switch"`** for toggles, (3) **`role="checkbox"`** for custom checkboxes, (4) **`role="dialog"`** for modals, (5) **`role="alert"`** for error messages, (6) **`role="status"`** for status messages. Always add ARIA states (aria-checked, aria-expanded, etc.) to match component state.

### Q: How do I test LWC accessibility?

**A**: Test accessibility by: (1) **Running automated tests** (axe-core, Lighthouse, Jest with @salesforce/sa11y), (2) **Testing with keyboard-only navigation** (Tab, Enter, Space, Escape), (3) **Testing with screen readers** (NVDA, JAWS, VoiceOver), (4) **Verifying color contrast** (WebAIM Contrast Checker), (5) **Testing all interactive states** (loading, error, success), (6) **Testing focus management** (focus indicators, focus trapping).

### Q: What are best practices for preventing accessibility errors?

**A**: Best practices include: (1) **Always add labels** to form controls, (2) **Make all interactive elements keyboard accessible**, (3) **Never remove focus indicators**, (4) **Use SLDS color tokens** for proper contrast, (5) **Add alt text to all images**, (6) **Follow proper heading hierarchy**, (7) **Use semantic HTML** (header, nav, main, footer), (8) **Test with screen readers** regularly, (9) **Include accessibility in code reviews**.

## Edge Cases and Limitations

### Edge Case 1: Dynamic Content with Screen Readers

**Scenario**: Screen readers not announcing dynamic content changes, causing accessibility issues.

**Consideration**:
- Use `aria-live` regions for dynamic content
- Implement proper ARIA roles for live regions
- Test with actual screen readers
- Announce changes appropriately (polite vs assertive)
- Use `aria-atomic` for complete region announcements
- Document dynamic content behavior

### Edge Case 2: Keyboard Navigation in Complex Components

**Scenario**: Complex components with nested interactive elements causing keyboard navigation issues.

**Consideration**:
- Implement proper tab order
- Trap focus in modals and dialogs
- Return focus to trigger element
- Support Escape key for cancellation
- Test keyboard navigation thoroughly
- Document keyboard interaction patterns

### Edge Case 3: Color Contrast with Custom Themes

**Scenario**: Custom themes or branding causing color contrast violations.

**Consideration**:
- Verify contrast ratios meet WCAG requirements
- Test with color blindness simulators
- Don't rely on color alone for information
- Provide alternative indicators (icons, text)
- Document color contrast requirements
- Test with different themes

### Edge Case 4: Form Validation Accessibility

**Scenario**: Form validation errors not properly announced to screen readers.

**Consideration**:
- Associate error messages with form fields
- Use `aria-describedby` for error messages
- Use `aria-invalid` for invalid fields
- Announce errors immediately (assertive)
- Provide clear, actionable error messages
- Test with screen readers

### Edge Case 5: Third-Party Component Accessibility

**Scenario**: Third-party components or libraries not meeting accessibility standards.

**Consideration**:
- Evaluate third-party components for accessibility
- Request accessibility documentation
- Test third-party components with screen readers
- Consider accessibility in component selection
- Document accessibility limitations
- Provide alternatives when needed

### Limitations

- **Screen Reader Compatibility**: Different screen readers may interpret ARIA differently
- **Browser Support**: Some ARIA features have limited browser support
- **Testing Complexity**: Accessibility testing requires specialized tools and knowledge
- **Third-Party Components**: Third-party components may have accessibility limitations
- **WCAG Compliance**: Full WCAG 2.2 compliance requires ongoing effort
- **Dynamic Content**: Dynamic content accessibility can be complex
- **Keyboard Navigation**: Complex components may have keyboard navigation challenges

## Related Patterns

**See Also**:
- <a href="{{ '/rag/troubleshooting/common-lwc-errors.html' | relative_url }}">Common LWC Errors</a> - General LWC troubleshooting

**Related Domains**:
- <a href="{{ '/rag/mcp-knowledge/lwc-accessibility.html' | relative_url }}">LWC Accessibility Guidelines</a> - WCAG 2.2 compliance guidance
- <a href="{{ '/rag/code-examples/lwc/accessibility-examples.html' | relative_url }}">LWC Accessibility Examples</a> - Accessibility code examples
- <a href="{{ '/rag/testing/lwc-accessibility-testing.html' | relative_url }}">LWC Accessibility Testing</a> - Testing patterns
- <a href="{{ '/rag/troubleshooting/common-lwc-errors.html' | relative_url }}">Common LWC Errors</a> - General LWC troubleshooting