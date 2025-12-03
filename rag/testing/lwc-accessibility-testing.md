---
title: "LWC Accessibility Testing Patterns"
level: "Intermediate"
tags:
  - testing
  - lwc
  - accessibility
  - wcag
last_reviewed: "2025-01-XX"
---

# LWC Accessibility Testing Patterns

> Comprehensive testing patterns and examples for Lightning Web Component accessibility validation.

## Overview

This guide provides testing patterns, best practices, and examples for ensuring Lightning Web Components meet WCAG 2.2 accessibility standards. It covers Jest accessibility testing, manual testing checklists, and automated testing tools.

**Related Patterns**:
- [LWC Accessibility Guidelines](mcp-knowledge/lwc-accessibility.html) - WCAG 2.2 compliance guidance
- [LWC Accessibility Examples](code-examples/lwc/accessibility-examples.html) - Accessibility code examples
- [Testing Strategy](project-methods/testing-strategy.html) - Overall testing strategy

## Core Principles

### Accessibility Testing Levels

1. **Automated Testing**: Use tools to catch common issues
2. **Manual Testing**: Verify with keyboard and screen readers
3. **User Testing**: Test with actual assistive technology users

### Testing Checklist

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

---

## Jest Accessibility Testing

### Pattern 1: Using @salesforce/sa11y for Accessibility Tests

**When to use**: Automated accessibility testing in Jest test suites

**Implementation**:

**Setup** (`jest.config.js`):
```javascript
module.exports = {
    testEnvironment: 'jsdom',
    setupFilesAfterEnv: ['<rootDir>/jest.setup.js'],
    moduleNameMapper: {
        '^@salesforce/apex$': '<rootDir>/force-app/test/jest-mocks/apex',
        '^lightning/platformShowToastEvent$': '<rootDir>/force-app/test/jest-mocks/lightning/platformShowToastEvent',
    }
};
```

**Jest Setup** (`jest.setup.js`):
```javascript
import { jest } from '@jest/globals';
import { axe, toHaveNoViolations } from 'jest-axe';

// Extend Jest matchers
expect.extend(toHaveNoViolations);

// Mock Salesforce modules
global.LightningElement = class LightningElement {};
```

**Test Example** (`contactForm.test.js`):
```javascript
import { createElement } from 'lwc';
import ContactForm from 'c/contactForm';
import { axe, toHaveNoViolations } from 'jest-axe';

describe('c-contact-form accessibility', () => {
    afterEach(() => {
        while (document.body.firstChild) {
            document.body.removeChild(document.body.firstChild);
        }
    });

    it('should have no accessibility violations', async () => {
        const element = createElement('c-contact-form', {
            is: ContactForm
        });
        document.body.appendChild(element);

        const results = await axe(element);
        expect(results).toHaveNoViolations();
    });

    it('should have accessible form labels', () => {
        const element = createElement('c-contact-form', {
            is: ContactForm
        });
        document.body.appendChild(element);

        const firstNameInput = element.shadowRoot.querySelector('lightning-input[name="firstName"]');
        expect(firstNameInput.label).toBe('First Name');
        expect(firstNameInput.getAttribute('aria-describedby')).toBeTruthy();
    });

    it('should announce errors to screen readers', () => {
        const element = createElement('c-contact-form', {
            is: ContactForm
        });
        document.body.appendChild(element);

        const errorDiv = element.shadowRoot.querySelector('[role="alert"]');
        expect(errorDiv).toBeTruthy();
    });
});
```

**Best Practices**:
- Run accessibility tests in CI/CD pipeline
- Test all interactive components
- Test error states and loading states
- Test with different data scenarios

---

### Pattern 2: Testing Keyboard Navigation

**When to use**: Verify keyboard accessibility of custom components

**Implementation**:

**Test Example** (`customToggle.test.js`):
```javascript
import { createElement } from 'lwc';
import CustomToggle from 'c/customToggle';
import { fireEvent } from 'lwc';

describe('c-custom-toggle keyboard navigation', () => {
    let element;

    beforeEach(() => {
        element = createElement('c-custom-toggle', {
            is: CustomToggle
        });
        element.label = 'Enable notifications';
        document.body.appendChild(element);
    });

    afterEach(() => {
        while (document.body.firstChild) {
            document.body.removeChild(document.body.firstChild);
        }
    });

    it('should be focusable with Tab key', () => {
        const toggle = element.shadowRoot.querySelector('[role="switch"]');
        expect(toggle.getAttribute('tabindex')).toBe('0');
    });

    it('should toggle on Space key', () => {
        const toggle = element.shadowRoot.querySelector('[role="switch"]');
        const initialChecked = toggle.getAttribute('aria-checked');
        
        fireEvent(toggle, new KeyboardEvent('keydown', { key: ' ' }));
        
        const newChecked = toggle.getAttribute('aria-checked');
        expect(newChecked).not.toBe(initialChecked);
    });

    it('should toggle on Enter key', () => {
        const toggle = element.shadowRoot.querySelector('[role="switch"]');
        const initialChecked = toggle.getAttribute('aria-checked');
        
        fireEvent(toggle, new KeyboardEvent('keydown', { key: 'Enter' }));
        
        const newChecked = toggle.getAttribute('aria-checked');
        expect(newChecked).not.toBe(initialChecked);
    });

    it('should have visible focus indicator', () => {
        const toggle = element.shadowRoot.querySelector('[role="switch"]');
        toggle.focus();
        
        const styles = window.getComputedStyle(toggle);
        expect(styles.outline).not.toBe('none');
    });
});
```

**Best Practices**:
- Test all keyboard shortcuts
- Verify focus indicators are visible
- Test focus order (tab order)
- Test focus trapping in modals

---

### Pattern 3: Testing ARIA Attributes

**When to use**: Verify ARIA attributes are correctly applied

**Implementation**:

**Test Example** (`accessibleModal.test.js`):
```javascript
import { createElement } from 'lwc';
import AccessibleModal from 'c/accessibleModal';

describe('c-accessible-modal ARIA attributes', () => {
    let element;

    beforeEach(() => {
        element = createElement('c-accessible-modal', {
            is: AccessibleModal
        });
        element.title = 'Confirm Action';
        element.isOpen = true;
        document.body.appendChild(element);
    });

    afterEach(() => {
        while (document.body.firstChild) {
            document.body.removeChild(document.body.firstChild);
        }
    });

    it('should have role="dialog"', () => {
        const modal = element.shadowRoot.querySelector('[role="dialog"]');
        expect(modal).toBeTruthy();
        expect(modal.getAttribute('role')).toBe('dialog');
    });

    it('should have aria-modal="true"', () => {
        const modal = element.shadowRoot.querySelector('[role="dialog"]');
        expect(modal.getAttribute('aria-modal')).toBe('true');
    });

    it('should have aria-labelledby pointing to title', () => {
        const modal = element.shadowRoot.querySelector('[role="dialog"]');
        const titleId = modal.getAttribute('aria-labelledby');
        const title = element.shadowRoot.querySelector(`#${titleId}`);
        expect(title).toBeTruthy();
        expect(title.textContent).toBe('Confirm Action');
    });

    it('should have aria-describedby pointing to description', () => {
        const modal = element.shadowRoot.querySelector('[role="dialog"]');
        const descriptionId = modal.getAttribute('aria-describedby');
        const description = element.shadowRoot.querySelector(`#${descriptionId}`);
        expect(description).toBeTruthy();
    });

    it('should have accessible close button', () => {
        const closeButton = element.shadowRoot.querySelector('button[aria-label*="Close"]');
        expect(closeButton).toBeTruthy();
    });
});
```

**Best Practices**:
- Verify all ARIA roles are correct
- Verify ARIA states (aria-checked, aria-expanded, etc.)
- Verify ARIA properties (aria-label, aria-labelledby, etc.)
- Verify ARIA relationships are maintained

---

## Manual Testing Checklists

### Keyboard Navigation Checklist

**Test Steps**:
1. **Tab Navigation**:
   - [ ] Tab through all interactive elements
   - [ ] Focus order is logical
   - [ ] No keyboard traps
   - [ ] Focus returns after modal close

2. **Keyboard Shortcuts**:
   - [ ] Enter key activates buttons
   - [ ] Space key activates buttons/checkboxes
   - [ ] Escape key closes modals
   - [ ] Arrow keys work in lists/menus

3. **Focus Indicators**:
   - [ ] Focus is visible on all elements
   - [ ] Focus outline meets contrast requirements
   - [ ] Focus doesn't disappear unexpectedly

**Tools**:
- Keyboard only (no mouse)
- Browser DevTools (Elements → Accessibility)

---

### Screen Reader Testing Checklist

**Test Steps**:
1. **Form Labels**:
   - [ ] All inputs are announced with labels
   - [ ] Error messages are announced
   - [ ] Help text is announced

2. **Navigation**:
   - [ ] Headings are announced
   - [ ] Landmarks are announced
   - [ ] Links are announced with purpose

3. **Dynamic Content**:
   - [ ] Loading states are announced
   - [ ] Error messages are announced
   - [ ] Success messages are announced

4. **Images**:
   - [ ] Informative images have alt text
   - [ ] Decorative images are ignored

**Screen Readers**:
- **Windows**: NVDA (free), JAWS (paid)
- **macOS/iOS**: VoiceOver (built-in)
- **Android**: TalkBack (built-in)

**Testing Commands**:
- **NVDA**: Insert+F7 (elements list), Insert+Arrow keys (navigation)
- **VoiceOver**: VO+F7 (elements list), VO+Arrow keys (navigation)

---

### Color Contrast Testing Checklist

**Test Steps**:
1. **Text Contrast**:
   - [ ] Normal text: 4.5:1 contrast ratio
   - [ ] Large text: 3:1 contrast ratio
   - [ ] UI components: 3:1 contrast ratio

2. **Focus Indicators**:
   - [ ] Focus outline: 3:1 contrast ratio
   - [ ] Focus is visible on all backgrounds

3. **Color Blindness**:
   - [ ] Information not conveyed by color alone
   - [ ] Icons/text accompany color indicators

**Tools**:
- WebAIM Contrast Checker: https://webaim.org/resources/contrastchecker/
- Chrome DevTools (Lighthouse)
- Color Oracle (color blindness simulator)

---

## Automated Testing Tools

### Tool 1: axe-core Integration

**When to use**: Automated accessibility scanning in CI/CD

**Implementation**:

**Installation**:
```bash
npm install --save-dev @axe-core/cli jest-axe
```

**CI/CD Script** (`scripts/test-accessibility.sh`):
```bash
#!/bin/bash
# Run accessibility tests

echo "Running accessibility tests..."

# Run Jest tests with axe
npm run test:accessibility

# Run axe CLI on built components
npx @axe-core/cli https://your-sandbox-url.com/your-component

echo "Accessibility tests completed"
```

**Jest Integration**:
```javascript
// jest.setup.js
import { toHaveNoViolations } from 'jest-axe';
expect.extend(toHaveNoViolations);
```

**Best Practices**:
- Run in CI/CD pipeline
- Fail builds on violations
- Generate accessibility reports
- Track violations over time

---

### Tool 2: Lighthouse Accessibility Audit

**When to use**: Comprehensive accessibility auditing

**Implementation**:

**Chrome DevTools**:
1. Open DevTools (F12)
2. Go to Lighthouse tab
3. Select "Accessibility" category
4. Click "Generate report"

**CLI Usage**:
```bash
# Install Lighthouse CLI
npm install -g @lhci/cli

# Run accessibility audit
lhci autorun --collect.url=https://your-sandbox-url.com/your-component --collect.numberOfRuns=3
```

**Best Practices**:
- Run on all pages/components
- Set minimum accessibility score (90+)
- Include in CI/CD pipeline
- Track scores over time

---

### Tool 3: Salesforce Accessibility Scanner

**When to use**: Salesforce-specific accessibility validation

**Implementation**:

**Setup**:
1. Install Salesforce Accessibility Scanner extension
2. Enable in Salesforce org
3. Run scan on components

**Usage**:
```javascript
// In component test
import { runAccessibilityScan } from '@salesforce/accessibility-scanner';

it('should pass accessibility scan', async () => {
    const element = createElement('c-my-component', {
        is: MyComponent
    });
    document.body.appendChild(element);

    const results = await runAccessibilityScan(element);
    expect(results.violations.length).toBe(0);
});
```

**Best Practices**:
- Run on all LWC components
- Fix violations before deployment
- Include in pre-commit hooks

---

## Testing Patterns Summary

### Test Method Naming
- `test[ComponentName]_Accessibility` - Standard pattern
- Examples: `testContactForm_Accessibility`, `testModal_KeyboardNavigation`

### Test Structure
1. **Setup**: Create component and append to DOM
2. **Act**: Trigger interactions or check attributes
3. **Assert**: Verify accessibility requirements

### Common Test Patterns
- **Form Labels**: Verify all inputs have labels
- **Keyboard Navigation**: Test Tab, Enter, Space, Escape
- **ARIA Attributes**: Verify roles, states, properties
- **Focus Management**: Verify focus indicators and trapping
- **Screen Reader**: Verify announcements (manual testing)

---

## Best Practices

1. **Automate What You Can**: Use Jest and axe-core for automated testing
2. **Manual Testing is Essential**: Test with actual screen readers
3. **Test Early and Often**: Include accessibility in unit tests
4. **Test All States**: Loading, error, success, empty states
5. **Test with Real Users**: Include users with disabilities in testing
6. **Document Issues**: Track and fix accessibility violations
7. **Set Standards**: Define minimum accessibility requirements
8. **Train Team**: Ensure team understands accessibility requirements

---

## Q&A

### Q: How do I test LWC accessibility with Jest?

**A**: Test LWC accessibility with Jest by: (1) **Installing @salesforce/sa11y** package, (2) **Importing accessibility matchers** (`import '@salesforce/sa11y/dist/jest'`), (3) **Rendering component** in test, (4) **Using `expect(element).toBeAccessible()`** matcher, (5) **Running tests** to catch accessibility violations. Jest accessibility tests catch common issues automatically.

### Q: What accessibility testing tools should I use?

**A**: Use accessibility testing tools: (1) **@salesforce/sa11y** for Jest unit tests, (2) **axe-core** for automated testing, (3) **Lighthouse** for page-level testing, (4) **Pa11y** for command-line testing, (5) **Screen readers** (NVDA, JAWS, VoiceOver) for manual testing, (6) **WebAIM Contrast Checker** for color contrast. Combine automated and manual testing.

### Q: What should I test manually for accessibility?

**A**: Test manually: (1) **Keyboard navigation** (Tab, Enter, Space, Escape keys), (2) **Screen reader testing** (NVDA, JAWS, VoiceOver), (3) **Focus indicators** (visible focus styles), (4) **Color contrast** (verify on different backgrounds), (5) **Dynamic content announcements** (screen reader announces changes), (6) **Modal focus trapping** (focus stays in modal). Manual testing catches issues automated tools miss.

### Q: How do I test keyboard accessibility?

**A**: Test keyboard accessibility by: (1) **Using Tab key** to navigate through interactive elements, (2) **Using Enter/Space** to activate buttons/links, (3) **Using Escape** to close modals/cancel actions, (4) **Verifying focus order** (logical tab order), (5) **Verifying no keyboard traps** (can navigate away), (6) **Testing all interactive states** (loading, error, success). Disable mouse to test keyboard-only navigation.

### Q: How do I test with screen readers?

**A**: Test with screen readers by: (1) **Installing screen reader** (NVDA for Windows, VoiceOver for Mac, JAWS for Windows), (2) **Navigating component** using screen reader commands, (3) **Verifying announcements** (labels, roles, states), (4) **Verifying dynamic content** is announced, (5) **Verifying form labels** are read correctly, (6) **Testing all interactive elements**. Screen reader testing is essential for accessibility.

### Q: What accessibility issues can automated tools catch?

**A**: Automated tools catch: (1) **Missing labels** on form controls, (2) **Missing alt text** on images, (3) **Color contrast violations**, (4) **Missing ARIA attributes**, (5) **Incorrect heading hierarchy**, (6) **Keyboard accessibility issues** (some), (7) **Semantic HTML violations**. Automated tools catch about 30-40% of accessibility issues - manual testing is still essential.

### Q: What accessibility issues require manual testing?

**A**: Require manual testing: (1) **Screen reader announcements** (how content is read), (2) **Keyboard navigation flow** (logical tab order), (3) **Focus management** (focus trapping, focus indicators), (4) **Dynamic content announcements** (live regions), (5) **Context and meaning** (does content make sense when read), (6) **User experience** (is it usable with assistive technology). Manual testing catches issues automated tools miss.

### Q: How often should I test accessibility?

**A**: Test accessibility: (1) **During development** (include in unit tests), (2) **Before code review** (run automated tests), (3) **During code review** (review accessibility checklist), (4) **Before deployment** (full accessibility audit), (5) **After deployment** (verify in production), (6) **Regularly** (ongoing accessibility testing). Include accessibility in every development cycle.

### Q: What is the minimum accessibility standard I should meet?

**A**: Meet **WCAG 2.1 Level AA standards** as minimum: (1) **Level A** (basic accessibility - required), (2) **Level AA** (enhanced accessibility - recommended), (3) **Level AAA** (highest accessibility - optional). Most organizations target Level AA. Check your organization's accessibility requirements and compliance needs.

### Q: How do I integrate accessibility testing into CI/CD?

**A**: Integrate accessibility testing by: (1) **Running Jest accessibility tests** in CI pipeline, (2) **Running automated tools** (axe-core, Lighthouse) in CI, (3) **Failing builds** on accessibility violations, (4) **Reporting accessibility results** in CI output, (5) **Setting accessibility thresholds** (minimum score), (6) **Including accessibility in code review** process. Automate accessibility testing to catch issues early.

## Related Patterns

- [LWC Accessibility Guidelines](mcp-knowledge/lwc-accessibility.html) - WCAG 2.2 compliance guidance
- [LWC Accessibility Examples](code-examples/lwc/accessibility-examples.html) - Accessibility code examples
- [LWC Accessibility Troubleshooting](troubleshooting/lwc-accessibility-errors.html) - Common errors and fixes
- [Testing Strategy](project-methods/testing-strategy.html) - Overall testing strategy

