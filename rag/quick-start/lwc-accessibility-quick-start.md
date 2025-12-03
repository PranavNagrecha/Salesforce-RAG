---
title: "LWC Accessibility Quick Start Guide"
level: "Beginner"
tags:
  - quick-start
  - lwc
  - accessibility
  - wcag
  - getting-started
last_reviewed: "2025-01-XX"
---

# LWC Accessibility Quick Start Guide

> Getting started with Lightning Web Component accessibility in Salesforce.

## Overview

This quick-start guide provides step-by-step instructions for making Lightning Web Components accessible, following WCAG 2.2 standards and Salesforce best practices.

**Related Patterns**:
- <a href="{{ '/rag/quick-start/mcp-knowledge/lwc-accessibility.html' | relative_url }}">LWC Accessibility Guidelines</a> - WCAG 2.2 compliance guidance
- <a href="{{ '/rag/quick-start/code-examples/lwc/accessibility-examples.html' | relative_url }}">LWC Accessibility Examples</a> - Complete code examples
- <a href="{{ '/rag/quick-start/testing/lwc-accessibility-testing.html' | relative_url }}">LWC Accessibility Testing</a> - Testing patterns
- <a href="{{ '/rag/quick-start/troubleshooting/lwc-accessibility-errors.html' | relative_url }}">LWC Accessibility Troubleshooting</a> - Common errors and fixes

## Quick Accessibility Checklist

Use this checklist when building or reviewing LWC components:

### Form Accessibility
- [ ] All form controls have `label` attribute (Lightning Base Components)
- [ ] Custom inputs have `<label>` with `for`/`id` attributes
- [ ] Error messages use `role="alert"` and `aria-describedby`
- [ ] Autocomplete attributes are used for personal information fields
- [ ] Fieldset/legend used for grouped form controls

### Keyboard Navigation
- [ ] All interactive elements are keyboard accessible
- [ ] Focus indicators are visible (2px outline, 3:1 contrast)
- [ ] Tab order is logical
- [ ] Modals trap focus and close on Escape key
- [ ] Focus returns to trigger element after modal close

### ARIA Attributes
- [ ] Icon-only buttons have `aria-label`
- [ ] Custom components have appropriate `role`
- [ ] ARIA states are used (aria-checked, aria-expanded, etc.)
- [ ] ARIA live regions for dynamic content (aria-live="polite" or "assertive")
- [ ] Modal dialogs have `role="dialog"` and `aria-modal="true"`

### Images
- [ ] Decorative images have `alt=""` and optionally `aria-hidden="true"`
- [ ] Informative images have descriptive `alt` text
- [ ] Image links have `aria-label` on the link

### Semantic HTML
- [ ] Proper heading hierarchy (h1 → h2 → h3, no skipping)
- [ ] Semantic regions used (header, nav, main, footer, section)
- [ ] Lists use proper markup (ul, ol, dl)
- [ ] Tables have proper structure (thead, tbody, scope attributes)

### Color and Contrast
- [ ] Text meets 4.5:1 contrast ratio (normal text) or 3:1 (large text)
- [ ] Focus indicators meet 3:1 contrast ratio
- [ ] Information not conveyed by color alone (use icons/text)

---

## Step-by-Step: Making an Existing Component Accessible

### Step 1: Add Form Labels

**Before**:
```html
<lightning-input
    name="email"
    value={email}
    onchange={handleChange}>
</lightning-input>
```

**After**:
```html
<lightning-input
    label="Email Address"
    name="email"
    value={email}
    onchange={handleChange}
    required
    message-when-value-missing="Email is required">
</lightning-input>
```

---

### Step 2: Add Keyboard Support

**Before**:
```html
<div class="custom-button" onclick={handleClick}>
    Click me
</div>
```

**After**:
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

**JavaScript**:
```javascript
handleKeyDown(event) {
    if (event.key === ' ' || event.key === 'Enter') {
        event.preventDefault();
        this.handleClick();
    }
}
```

---

### Step 3: Add ARIA Labels to Icon Buttons

**Before**:
```html
<button class="slds-button slds-button_icon" onclick={handleClose}>
    <lightning-icon icon-name="utility:close"></lightning-icon>
</button>
```

**After**:
```html
<button
    class="slds-button slds-button_icon"
    onclick={handleClose}
    aria-label="Close dialog"
    title="Close">
    <lightning-icon
        icon-name="utility:close"
        alternative-text="Close">
    </lightning-icon>
    <span class="slds-assistive-text">Close</span>
</button>
```

---

### Step 4: Add Focus Indicators

**Before** (CSS):
```css
.custom-button {
    border: none;
    outline: none; /* Removes focus indicator */
}
```

**After** (CSS):
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

---

### Step 5: Add Error Message Accessibility

**Before**:
```html
<div class="error" if:true={errorMessage}>
    {errorMessage}
</div>
```

**After**:
```html
<div
    role="alert"
    aria-live="assertive"
    class="error"
    if:true={errorMessage}>
    {errorMessage}
</div>
```

---

### Step 6: Fix Image Alt Text

**Before**:
```html
<img src="/assets/chart.png" class="chart">
```

**After** (Informative):
```html
<img
    src="/assets/chart.png"
    alt="Sales chart showing 25% increase in Q4 2023"
    class="chart">
```

**After** (Decorative):
```html
<img
    src="/assets/divider.png"
    alt=""
    class="divider"
    aria-hidden="true">
```

---

### Step 7: Fix Heading Hierarchy

**Before**:
```html
<h1>Page Title</h1>
<h3>Section Title</h3> <!-- Should be h2 -->
<h4>Subsection</h4> <!-- Should be h3 -->
```

**After**:
```html
<h1>Page Title</h1>
<h2>Section Title</h2>
<h3>Subsection</h3>
```

---

### Step 8: Add Semantic HTML

**Before**:
```html
<div class="header">...</div>
<div class="main">...</div>
<div class="footer">...</div>
```

**After**:
```html
<header>...</header>
<main>...</main>
<footer>...</footer>
```

---

## Essential Patterns

### Pattern 1: Accessible Form

**Complete Example**:
```html
<template>
    <lightning-card title="Contact Form">
        <div class="slds-p-around_medium">
            <form onsubmit={handleSubmit}>
                <div class="slds-form-element">
                    <lightning-input
                        label="First Name"
                        name="firstName"
                        value={firstName}
                        onchange={handleInputChange}
                        required
                        autocomplete="given-name"
                        aria-describedby="firstName-help">
                    </lightning-input>
                    <div id="firstName-help" class="slds-form-element__help">
                        Enter your legal first name
                    </div>
                </div>

                <div class="slds-form-element">
                    <lightning-input
                        type="email"
                        label="Email"
                        name="email"
                        value={email}
                        onchange={handleInputChange}
                        required
                        autocomplete="email"
                        aria-describedby="email-error"
                        message-when-value-missing="Email is required">
                    </lightning-input>
                    <div
                        id="email-error"
                        class="slds-form-element__help"
                        role="alert"
                        if:true={emailError}>
                        {emailError}
                    </div>
                </div>

                <div class="slds-m-top_medium">
                    <lightning-button
                        type="submit"
                        label="Submit"
                        variant="brand">
                    </lightning-button>
                </div>
            </form>
        </div>
    </lightning-card>
</template>
```

---

### Pattern 2: Accessible Button

**Complete Example**:
```html
<template>
    <button
        type="button"
        class="slds-button slds-button_brand"
        aria-label={ariaLabel}
        onclick={handleClick}
        onkeydown={handleKeyDown}>
        <lightning-icon
            if:true={iconName}
            icon-name={iconName}
            size="small"
            alternative-text={iconAltText}>
        </lightning-icon>
        <span if:true={label}>{label}</span>
        <span class="slds-assistive-text" if:true={assistiveText}>
            {assistiveText}
        </span>
    </button>
</template>
```

**JavaScript**:
```javascript
import { LightningElement, api } from 'lwc';

export default class AccessibleButton extends LightningElement {
    @api label = '';
    @api iconName = '';
    @api ariaLabel = '';
    @api assistiveText = '';

    get iconAltText() {
        return this.ariaLabel || this.label;
    }

    handleKeyDown(event) {
        if (event.key === ' ' || event.key === 'Enter') {
            event.preventDefault();
            this.handleClick();
        }
    }

    handleClick() {
        this.dispatchEvent(new CustomEvent('click'));
    }
}
```

---

### Pattern 3: Accessible Modal

**Complete Example**:
```html
<template>
    <template if:true={isOpen}>
        <section
            role="dialog"
            aria-modal="true"
            aria-labelledby="modal-title"
            aria-describedby="modal-description"
            class="slds-modal slds-fade-in-open"
            tabindex="-1">
            <div class="slds-modal__container">
                <header class="slds-modal__header">
                    <h2 id="modal-title" class="slds-modal__title">
                        {title}
                    </h2>
                    <button
                        class="slds-button slds-button_icon slds-modal__close"
                        aria-label="Close {title}"
                        onclick={handleClose}>
                        <lightning-icon icon-name="utility:close" size="small"></lightning-icon>
                        <span class="slds-assistive-text">Close</span>
                    </button>
                </header>
                <div class="slds-modal__content" id="modal-description">
                    <slot></slot>
                </div>
                <footer class="slds-modal__footer">
                    <lightning-button
                        label="Cancel"
                        variant="neutral"
                        onclick={handleClose}>
                    </lightning-button>
                    <lightning-button
                        label="Confirm"
                        variant="brand"
                        onclick={handleConfirm}>
                    </lightning-button>
                </footer>
            </div>
        </section>
        <div class="slds-backdrop slds-backdrop_open" role="presentation"></div>
    </template>
</template>
```

**JavaScript** (focus trapping):
```javascript
import { LightningElement, api } from 'lwc';

export default class AccessibleModal extends LightningElement {
    @api title = 'Modal Title';
    @api isOpen = false;
    
    previousActiveElement = null;

    renderedCallback() {
        if (this.isOpen) {
            this.previousActiveElement = document.activeElement;
            this.trapFocus();
        }
    }

    trapFocus() {
        const modal = this.template.querySelector('[role="dialog"]');
        if (!modal) return;

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
        this.dispatchEvent(new CustomEvent('close'));
    }

    handleConfirm() {
        this.dispatchEvent(new CustomEvent('confirm'));
        this.handleClose();
    }
}
```

---

### Pattern 4: Accessible Data Table

**Complete Example**:
```html
<template>
    <table
        class="slds-table slds-table_cell-buffer"
        role="table"
        aria-label="Contact list with {contactCount} contacts">
        <thead>
            <tr>
                <th scope="col">Name</th>
                <th scope="col">Email</th>
                <th scope="col">Phone</th>
            </tr>
        </thead>
        <tbody>
            <template for:each={contacts} for:item="contact">
                <tr key={contact.Id}>
                    <td data-label="Name">{contact.Name}</td>
                    <td data-label="Email">
                        <a href="mailto:{contact.Email}" aria-label="Email {contact.Name}">
                            {contact.Email}
                        </a>
                    </td>
                    <td data-label="Phone">{contact.Phone}</td>
                </tr>
            </template>
        </tbody>
    </table>
</template>
```

---

## Testing Your Component

### Quick Test Checklist

1. **Keyboard Navigation**:
   - [ ] Tab through all interactive elements
   - [ ] Focus indicators are visible
   - [ ] Enter/Space activate buttons
   - [ ] Escape closes modals

2. **Screen Reader** (NVDA, JAWS, or VoiceOver):
   - [ ] All form labels are announced
   - [ ] Error messages are announced
   - [ ] Button purposes are clear
   - [ ] Images have appropriate alt text

3. **Automated Testing**:
   - [ ] Run axe-core scan (no violations)
   - [ ] Run Lighthouse accessibility audit (90+ score)
   - [ ] Run Jest accessibility tests

### Testing Tools

- **axe DevTools**: Browser extension for accessibility testing
- **Lighthouse**: Chrome DevTools accessibility audit
- **WebAIM Contrast Checker**: Color contrast verification
- **Screen Readers**: NVDA (Windows), JAWS (Windows), VoiceOver (macOS/iOS)

---

## Common Fixes

### Fix 1: Missing Label
```html
<!-- Add label attribute -->
<lightning-input label="Email" ...>
```

### Fix 2: Missing ARIA Label
```html
<!-- Add aria-label -->
<button aria-label="Close dialog" ...>
```

### Fix 3: Missing Focus Indicator
```css
/* Add focus styles */
.button:focus {
    outline: 2px solid #0176d3;
    outline-offset: 2px;
}
```

### Fix 4: Missing Alt Text
```html
<!-- Add alt text -->
<img src="chart.png" alt="Sales chart showing Q4 results">
```

### Fix 5: Incorrect Heading Hierarchy
```html
<!-- Fix hierarchy -->
<h1>Title</h1>
<h2>Section</h2> <!-- Not h3 -->
```

---

## Next Steps

1. **Review Examples**: See <a href="{{ '/rag/quick-start/code-examples/lwc/accessibility-examples.html' | relative_url }}">LWC Accessibility Examples</a> for complete code examples
2. **Learn Guidelines**: Read <a href="{{ '/rag/quick-start/mcp-knowledge/lwc-accessibility.html' | relative_url }}">LWC Accessibility Guidelines</a> for WCAG 2.2 compliance
3. **Test Your Components**: Follow <a href="{{ '/rag/quick-start/testing/lwc-accessibility-testing.html' | relative_url }}">LWC Accessibility Testing</a> patterns
4. **Fix Issues**: Use <a href="{{ '/rag/quick-start/troubleshooting/lwc-accessibility-errors.html' | relative_url }}">LWC Accessibility Troubleshooting</a> for common errors

---

## Related Patterns

- <a href="{{ '/rag/quick-start/mcp-knowledge/lwc-accessibility.html' | relative_url }}">LWC Accessibility Guidelines</a> - WCAG 2.2 compliance guidance
- <a href="{{ '/rag/quick-start/code-examples/lwc/accessibility-examples.html' | relative_url }}">LWC Accessibility Examples</a> - Complete code examples
- <a href="{{ '/rag/quick-start/testing/lwc-accessibility-testing.html' | relative_url }}">LWC Accessibility Testing</a> - Testing patterns
- <a href="{{ '/rag/quick-start/troubleshooting/lwc-accessibility-errors.html' | relative_url }}">LWC Accessibility Troubleshooting</a> - Common errors and fixes
- <a href="{{ '/rag/quick-start/lwc-quick-start.html' | relative_url }}">LWC Quick Start</a> - General LWC quick start

