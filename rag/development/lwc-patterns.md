# Lightning Web Component (LWC) Patterns

## Overview

LWCs are built for complex business logic that standard page layouts cannot handle. Components are designed to make complex processes usable for non-technical users and hide integration complexity behind simple interfaces.

## When to Use LWCs

LWCs are surgical tools for complex UI needs when:

- Need to combine data from multiple objects/systems
- Need complex client-side decisions and filtering
- Need responsive, interactive experiences
- Need to work cleanly in Experience Cloud portals
- Standard layouts or Flows cannot handle the requirement

## Component Patterns

### Console-Style LWCs

**Purpose**: Agent consoles for case workers, advisors, internal staff

**Features**:
- Aggregate data from multiple related records (Cases, Contacts, external system results)
- Show "at-a-glance" status, flags, and next actions
- Use `@wire` adapters to fetch data via Apex or LDS
- Implement local state + imperative Apex calls for actions (e.g., re-run external check, update status)
- Avoid heavy logic in components by pushing orchestration into Apex/services

### Fraud/Risk Scoring LWC

**Purpose**: Display fraud or risk scores for clients/cases

**Features**:
- Shows fraud or risk score based on rules and/or external scoring engine
- Displays score with clear visual indicators (color, icons, messaging)
- Pulls scores from either custom object populated by integration, or Apex making callout to integration layer
- Handles no-score scenarios (e.g., new client)
- Supports multiple rulesets or sources (system score vs manual overrides)
- LWC is mostly presentation + lightweight orchestration
- Apex service layer encapsulates callout details, error handling, and mapping from external payload → internal score model

**Implementation Pattern**:
- On-demand calculation (doesn't auto-calculate on page load)
- Cacheable methods for data fetch and calculation
- Detailed breakdown showing all factors with values and coefficients
- Override conditions checked first (business rules before model)
- Feedback mechanism for user input

### Program-Selection LWC

**Purpose**: Let applicants or staff select academic programs with real eligibility rules

**Features**:
- Filterable/searchable list or grid of programs
- Enforces eligibility rules (e.g., "Only show Hybrid programs if X conditions are met")
- Writes final selection back to Application object and Program Enrollment or related record
- Uses structured metadata/config (program catalog, flags) rather than hard-coded lists
- Handles edge cases: applicant switching programs mid-process, inactive/retired programs, terms where program is not offered

**Implementation Pattern**:
- Cascading dropdown pattern: Term → Area → Level → Program → Delivery Mode
- Each step filters next step's options
- Only loads data when previous step selected (reduces initial load time)
- Compact view pattern: shows selected values in compact form, allows editing
- Auto-selection logic: if program has only one delivery option, auto-selects it
- Responsive design: mobile-first with breakpoints, flexible layouts

### Advisor Management LWC

**Purpose**: Staff management of advisor information

**Features**:
- View and edit advisor-specific fields (availability days, times, nickname)
- Pagination for large datasets (15 advisors per page)
- Search functionality (by name or email)
- Inline editing without full page refresh
- Works with field-level security

**Implementation Pattern**:
- Server-side pagination (Apex handles offset/limit)
- Server-side search (Apex handles filtering)
- Lightning Data Table with editable columns
- Draft values tracked locally
- Batch update on save (all edited rows in one DML)
- System mode updates (`without sharing`) to bypass FLS for updates

## Reusable LWC Patterns

### Service-Layer Pattern

**Pattern**: Apex classes expose clean methods for LWCs

- Methods like `getXXXViewModel(Id recordId)` and `performAction(...)`
- LWCs don't "know" SOQL details; they deal with DTO-style payloads
- Encapsulates business logic and data access
- Enables reuse across multiple components

### Config-Driven UI

**Pattern**: Use custom metadata / custom settings to drive:

- Which fields show up
- Thresholds (e.g., risk score color bands)
- Text/labels that might vary by environment or client
- Business rules and configuration

**Benefits**: Environment-specific configuration without code changes

### Performance-Aware Patterns

**Pattern**: Optimize for performance

- Batch reads into a single wired Apex method when possible
- Use `refreshApex` carefully to avoid hammering the org
- Defer heavy recalculation to async jobs if needed
- Cacheable methods for read-only operations
- On-demand loading for heavy data

## Data Access Patterns

### @wire for Reactive Data Access

- Use `@wire` for reactive data access when possible
- Support automatic data refresh
- Handle loading and error states
- Abstract SOQL details from components

### Imperative Apex Calls

- Use imperative Apex calls for actions and updates
- Support user-initiated operations
- Handle loading states appropriately
- Provide immediate feedback

### Batching Data Reads

- Batch data reads into single Apex methods
- Reduce server round trips
- Improve performance
- Simplify component logic

### Caching

- Cache data in component state when appropriate
- Use `@AuraEnabled(cacheable=true)` for read-only operations
- Cache reference data (terms, areas, levels)
- Cache busting with random parameter when fresh data needed

### LDS (Lightning Data Service)

- Use LDS for standard objects when possible
- Leverage platform caching
- Reduce custom Apex code
- Improve performance

## Error Handling

### User-Friendly Messages

- Handle errors gracefully with user-friendly messages
- Provide actionable guidance
- Support error recovery workflows
- Use toast notifications appropriately

### Error Logging

- Log errors for troubleshooting
- Include context about what failed
- Support error analysis
- Enable debugging workflows

### Validation

- Validate input before making server calls
- Provide immediate feedback
- Prevent invalid submissions
- Guide users to correct errors

### Loading States

- Handle loading states appropriately
- Show progress indicators
- Prevent multiple submissions
- Provide feedback during operations

## Performance Optimization

### Minimize Server Round Trips

- Batch operations when possible
- Use cacheable methods for read-only data
- Combine related queries
- Reduce unnecessary calls

### Use refreshApex Carefully

- Don't overuse `refreshApex`
- Only refresh when necessary
- Consider caching strategies
- Monitor performance impact

### Defer Heavy Calculations

- Defer heavy recalculation to async jobs if needed
- On-demand calculation for expensive operations
- Lazy loading for large data sets
- Progressive disclosure of information

### Performance-Optimized LWC Controller Pattern

**When to use**: When building Lightning Web Component controllers that need to fetch and process data efficiently.

**Implementation approach**:
- Don't auto-calculate on page load (user must click button) - prevents unnecessary Apex calls
- Use `@AuraEnabled(cacheable=true)` for read-only operations
- Implement cache busting with random parameter when fresh data needed (e.g., `System.currentTimeMillis()`)
- Fetch all required data in single Apex call (not multiple separate queries)
- Use relationship queries to combine data in single query
- Only select necessary fields (not entire objects)
- Use lazy loading for detailed breakdowns (hidden in tabs, loaded when expanded)

**Why it's recommended**: Auto-calculating on page load creates unnecessary Apex calls and slows page load times. Cacheable methods with cache busting provide best of both worlds (performance + fresh data). Single Apex calls reduce network latency. Lazy loading improves perceived performance.

**Real example**: Fraud score calculation component. Doesn't auto-calculate on load - user must click "Calculate" button. Uses cacheable methods with cache busting. Fetches all required data in single call. Lazy loads detailed breakdown in tabs.

**Lessons learned**:
- Not auto-calculating on load significantly improves page load times
- Cacheable methods with cache busting provide best of both worlds (performance + fresh data)
- User control over when to calculate improves perceived performance
- Single Apex calls reduce network latency

### Optimize Data Queries

- Optimize data queries in Apex
- Use selective WHERE clauses
- Limit result sets appropriately
- Cache frequently accessed data

## Accessibility

Accessibility ensures that all users, including those using assistive technologies, can access and interact with your components. All LWC components should follow WCAG 2.2 standards.

**Related Resources**:
- [LWC Accessibility Guidelines](rag/mcp-knowledge/lwc-accessibility.md) - Comprehensive WCAG 2.2 compliance guidance
- [LWC Accessibility Examples](rag/code-examples/lwc/accessibility-examples.md) - Complete working code examples
- [LWC Accessibility Testing](rag/testing/lwc-accessibility-testing.md) - Testing patterns and tools
- [LWC Accessibility Troubleshooting](rag/troubleshooting/lwc-accessibility-errors.md) - Common errors and fixes
- [LWC Accessibility Quick Start](rag/quick-start/lwc-accessibility-quick-start.md) - Quick start guide

### WCAG Guidelines

- Follow WCAG 2.2 guidelines for accessibility
- Ensure keyboard navigation works for all interactive elements
- Support screen readers (NVDA, JAWS, VoiceOver)
- Provide alternative text for images
- Maintain proper color contrast (4.5:1 for normal text, 3:1 for large text)
- Test with keyboard-only navigation
- Test with screen readers

### Form Accessibility

- **Labels**: All form controls must have programmatically associated labels
  - Use `label` attribute for Lightning Base Components
  - Use `<label>` with `for`/`id` for custom inputs
  - Use `aria-label` when visual labels not feasible
- **Error Messages**: Use `role="alert"` and `aria-describedby` for error messages
- **Autocomplete**: Use appropriate autocomplete tokens for personal information fields
- **Fieldset/Legend**: Use fieldset/legend for grouped form controls

**Example**: See [Accessible Form Examples](rag/code-examples/lwc/accessibility-examples.md#form-accessibility-examples)

### Keyboard Navigation

- **Focus Indicators**: All interactive elements must have visible focus indicators (2px outline, 3:1 contrast)
- **Tab Order**: Logical tab order through all interactive elements
- **Keyboard Shortcuts**: Support Enter, Space, Escape keys appropriately
- **Focus Trapping**: Modals must trap focus and close on Escape key
- **Focus Return**: Focus returns to trigger element after modal close
- **No Keyboard Traps**: Ensure users can navigate away from all areas

**Example**: See [Keyboard Navigation Examples](rag/code-examples/lwc/accessibility-examples.md#keyboard-navigation-examples)

### Semantic HTML

- Use semantic HTML elements (`<header>`, `<nav>`, `<main>`, `<footer>`, `<section>`)
- Proper heading hierarchy (h1 → h2 → h3, no skipping levels)
- Meaningful form labels (not just placeholder text)
- Accessible form controls
- Proper list markup (`<ul>`, `<ol>`, `<dl>`)
- Proper table structure with headers and scope attributes

**Example**: See [Semantic HTML Examples](rag/code-examples/lwc/accessibility-examples.md#semantic-html-examples)

### ARIA Labels and Attributes

- **ARIA Labels**: Provide `aria-label` for icon-only buttons and custom components
- **ARIA Roles**: Use appropriate `role` attributes for custom interactive components
- **ARIA States**: Use ARIA states (aria-checked, aria-expanded, aria-busy, etc.)
- **ARIA Live Regions**: Use `aria-live="polite"` for status updates, `aria-live="assertive"` for errors
- **ARIA Descriptions**: Use `aria-describedby` to associate help text and error messages
- **Modal Dialogs**: Use `role="dialog"` and `aria-modal="true"` for modals

**Example**: See [ARIA Patterns Examples](rag/code-examples/lwc/accessibility-examples.md#aria-patterns)

### Image Accessibility

- **Decorative Images**: Use `alt=""` and optionally `aria-hidden="true"`
- **Informative Images**: Use descriptive `alt` text that conveys the information
- **Image Links**: Provide `aria-label` on the link, use `alt=""` on the image
- **Complex Images**: Use `aria-describedby` with `figcaption` for detailed descriptions

**Example**: See [Image Accessibility Examples](rag/code-examples/lwc/accessibility-examples.md#image-accessibility)

### Color and Contrast

- **Text Contrast**: Normal text must meet 4.5:1 contrast ratio, large text 3:1
- **Focus Indicators**: Focus outlines must meet 3:1 contrast ratio
- **Not Color Alone**: Information must not be conveyed by color alone (use icons/text)
- **SLDS Tokens**: Use SLDS color tokens for proper contrast

**Example**: See [Color and Contrast Examples](rag/code-examples/lwc/accessibility-examples.md#color-and-contrast)

### Dynamic Content Accessibility

- **Loading States**: Use `aria-live="polite"` and `aria-busy="true"` for loading states
- **Error Messages**: Use `role="alert"` and `aria-live="assertive"` for errors
- **Success Messages**: Use `role="status"` and `aria-live="polite"` for success messages
- **Status Updates**: Announce dynamic content changes to screen readers

**Example**: See [Dynamic Content Examples](rag/code-examples/lwc/accessibility-examples.md#dynamic-content-accessibility)

### Testing Accessibility

- **Automated Testing**: Use axe-core, Lighthouse, or Salesforce Accessibility Scanner
- **Manual Testing**: Test with keyboard-only navigation
- **Screen Reader Testing**: Test with NVDA (Windows), JAWS (Windows), or VoiceOver (macOS/iOS)
- **Color Contrast Testing**: Use WebAIM Contrast Checker
- **Jest Testing**: Include accessibility tests in Jest test suites

**See**: [LWC Accessibility Testing](rag/testing/lwc-accessibility-testing.md) for complete testing patterns

### Common Accessibility Mistakes

- Missing form labels
- Missing ARIA labels on icon buttons
- Keyboard traps in modals
- Missing focus indicators
- Insufficient color contrast
- Missing alt text on images
- Incorrect heading hierarchy
- Missing semantic HTML

**See**: [LWC Accessibility Troubleshooting](rag/troubleshooting/lwc-accessibility-errors.md) for solutions to common errors

## Responsive Design

### Mobile-First Approach

- Mobile-first design with breakpoints
- Flexible layouts for different screen sizes
- Touch-friendly targets
- Responsive typography

### Breakpoints

- Use consistent breakpoints (e.g., 768px)
- Adapt layouts for different screen sizes
- Test on multiple devices
- Ensure usability across devices

## Best Practices Summary

### Component Design

- Break work into focused, reusable components
- Keep components small and single-purpose
- Use composition over complex monolithic components
- Separate presentation from business logic
- Push complex logic to Apex service layer

### Data Access

- Use `@wire` for reactive data access when possible
- Use imperative Apex calls for actions and updates
- Batch data reads into single Apex methods
- Cache data in component state when appropriate
- Use LDS for standard objects when possible

### Error Handling

- Handle errors gracefully with user-friendly messages
- Log errors for troubleshooting
- Provide recovery paths for users
- Validate input before making server calls
- Handle loading states appropriately

### Performance

- Minimize server round trips
- Use `refreshApex` carefully
- Defer heavy calculations to async jobs if needed
- Optimize data queries in Apex
- Use lazy loading for large data sets

### Accessibility

- Follow WCAG guidelines for accessibility
- Use semantic HTML
- Provide ARIA labels where needed
- Ensure keyboard navigation works
- Test with screen readers

