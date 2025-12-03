# LWC Accessibility - MCP Knowledge

> This file contains knowledge extracted from Salesforce MCP Service tools.  
> It complements the lived-experience patterns in `rag/development/` and `rag/patterns/`.

## Overview

Comprehensive accessibility guidelines for Lightning Web Components, based on WCAG 2.2 (Web Content Accessibility Guidelines) standards.

**Source**: Salesforce MCP Service - `mcp_salesforce_guide_lwc_accessibility`

## Key Accessibility Patterns

### Images (SC 1.1.1 - Non-text Content)

#### Decorative Images
- Must have `alt=""` (empty alt attribute)
- Can use `aria-hidden="true"` for decorative images that must remain in DOM
- Do not provide descriptive alt text for decorative images
- If decorative image is a link: Add `aria-label` or `title` to anchor tag

#### Informative Images
- Must have descriptive `alt` attribute
- Alt text should describe the information conveyed
- Avoid generic alt text like "image", "picture", "photo"

### Lists (SC 1.3.1 (i) - Info and Relationships)

#### List Markup
- Use `<ol>` for ordered lists
- Use `<ul>` for unordered lists
- Use `<dl>` for description lists (name-value pairs)
- For description lists with `for:each`: Wrap each entry in `<div>` with `key` attribute

### Form Labels (SC 1.3.1 (iii))

#### Label Association
- Every form control must have programmatically associated label
- Use `<label>` with matching `for`/`id` attributes
- Use `aria-label` or `aria-labelledby` when visual labels not feasible
- Lightning Base Components: Use `label` attribute

#### Label Content
- Must be descriptive and meaningful
- No nested interactive elements in labels
- Not just placeholder or title text
- Group controls need group and individual labels

### Input Purpose (SC 1.3.5)

#### Autocomplete Attributes
- Personal information fields: Use appropriate autocomplete tokens
- Non-personal fields: Omit autocomplete or use `autocomplete="off"`
- Security-sensitive fields: Must use `autocomplete="off"`
- Non-primary user fields: Absence of autocomplete is permissible

#### Valid Autocomplete Tokens
- Name: `name`, `given-name`, `family-name`
- Email: `email`
- Phone: `tel`, `tel-national`
- Address: `street-address`, `address-line1`, `address-level2`, `country`
- Credentials: `username`, `current-password`, `new-password`

### Keyboard Accessibility (SC 2.1.1)

#### Keyboard Operability
- All functionality must be operable through keyboard
- Interactive controls must be focusable
- Custom input implementations need keyboard equivalents
- Tooltips must be accessible via keyboard

#### Tabindex Patterns
- Avoid `tabindex` values greater than 0
- Use `tabindex="0"` for non-semantic interactive elements
- Do not create keyboard traps (parent focusable, child not focusable)
- Semantic elements (buttons, links) don't need explicit tabindex

### Link Purpose (SC 2.4.4)

#### Descriptive Link Text
- Link text must be descriptive enough to convey purpose
- Avoid vague text: "click here", "read more", "more"
- Icon links need `aria-label` or accessible name
- Multiple links with same text must point to same destination

### Pointer Gestures (SC 2.5.1)

#### Single Pointer Alternatives
- Multipoint gestures must have single pointer alternatives
- Path-based gestures must have single pointer alternatives
- Examples: Carousel with prev/next buttons, map with zoom controls

### Pointer Cancellation (SC 2.5.2)

#### Cancellation Requirements
- Down event should not operate function (preferred)
- Method to cancel or abort action
- Up-event reverses down event action
- Down event only if essential to functionality

### Dragging Movements (SC 2.5.7)

#### Single Pointer Alternatives
- Dragging operations must have single pointer alternatives
- Examples: Text input for color picker, up/down controls for lists
- Keyboard equivalence does not automatically meet this requirement

### Label in Name (SC 2.5.3)

#### Accessible Name Matching
- Accessible name must contain visible label text
- Use accessible name computation algorithm
- `aria-label` should include or prefix visible text
- Accessible description (aria-describedby) is separate from name

### On Focus (SC 3.2.1)

#### Context Changes
- Focus alone must not initiate context changes
- Context changes require explicit user activation
- Minor changes (tooltips, styling) are acceptable
- Form submission, modal opening require explicit activation

### On Input (SC 3.2.2)

#### Predictable Behavior
- Changing form control settings should not trigger unexpected context changes
- Users must be forewarned if context change is expected
- Provide submit button for form submission
- Explain context changes before control activation

### Name (SC 4.1.2 (i))

#### Accessible Names
- All UI components must have programmatically determinable name
- Use `aria-label`, `aria-labelledby`, or native labeling
- Lightning Base Components handle names automatically
- Generic layout elements (div, span) don't require names unless interactive

### Role (SC 4.1.2 (ii))

#### Programmatic Roles
- All UI components must have programmatically determinable role
- Semantic HTML provides implicit roles
- Custom controls need explicit ARIA roles
- Role relationships must be maintained (e.g., listitem requires list parent)

### Value (SC 4.1.2 (iii))

#### Programmatic Values
- User-settable values must be programmatically set
- ARIA state/property values must be valid
- Boolean attributes: Present = true, absent = false
- Numeric attributes must use numeric values

### Regions (SC 1.3.1 (iv))

#### Semantic Regions
- Use semantic HTML: `<header>`, `<nav>`, `<main>`, `<aside>`, `<footer>`, `<section>`
- Only one `<main>` element without hidden attribute
- Use ARIA landmark roles when semantic HTML not possible
- Each region should have descriptive label or heading

## Integration with Existing RAG

**Related Patterns**:
- [LWC Patterns](development/lwc-patterns.html) - Accessibility considerations
- [Design System Patterns](mcp-knowledge/design-system-patterns.html) - SLDS accessibility

**How This Complements Existing RAG**:
- Provides comprehensive WCAG compliance guidance
- Validates accessibility patterns in existing LWC code
- Adds specific accessibility requirements for common patterns
- Emphasizes keyboard navigation and screen reader support

