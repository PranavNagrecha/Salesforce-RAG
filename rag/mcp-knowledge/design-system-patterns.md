# Salesforce Lightning Design System (SLDS) Patterns - MCP Knowledge

> This file contains knowledge extracted from Salesforce MCP Service tools.  
> It complements the lived-experience patterns in `rag/development/` and `rag/patterns/`.

## Overview

Comprehensive guidelines for using Salesforce Lightning Design System (SLDS) to design enterprise software, covering UX principles, visual design, component usage, interaction patterns, and accessibility.

**Source**: Salesforce MCP Service - `mcp_salesforce_guide_design_general`

## UX Principles

- The design should be easy to learn, understand, and navigate without explicit instruction
- Respect progressive disclosure: don't overwhelm users
- Use space, layouts, and data-density strategically to drive clarity
- Use consistent interactions across flows, apps, and pages
- Always test with assistive technologies, Salesforce customers, and internal users

## Visual Design

### SLDS Utility Classes
- Use SLDS utility classes and styling hook values for visual consistency
- Follow SLDS spacing scale for margins and padding
- Apply styling hooks (`--slds-c-color-background`) instead of hardcoded values
- Maintain brand-appropriate themes using semantic styling hooks

### Information Hierarchy
- Establish hierarchy using SLDS typography heading levels and card components
- All text and interactive elements must meet WCAG 2.1 color contrast standards
- All content must be in card containers

### Grid System
- SLDS grid system is a responsive base-8 grid
- All spacing values are multiples or fractions of 8
- Micro content layouts within a card must use the SLDS grid
- Macro parent layouts containing multiple cards must also use the SLDS grid
- Spacing within cards and between cards must be consistent
- Cards must align vertically and horizontally within the grid
- Content cards never touch viewport edges

### Spacing and Layout
- Use SLDS utility classes for spacing, alignment, text, and sizing
- Examples: `slds-m-around_medium`, `slds-text-align_center`, `slds-p-horizontal_small`
- Avoid custom classes for these purposes unless absolutely necessary
- Default card spacing: `slds-p-around_small` if not specified

### Icons
- Only use SLDS icons for iconography
- Always use `<lightning-icon>` for SLDS icons
- Standard Object icons should be used adjacent to record titles
- Utility icons should be used for most other icon needs
- Never use Action icons in web apps (only in native mobile apps)

## Component Usage

### Lightning Base Components
- Use Lightning Web Components from component reference whenever possible
- Use Lightning Base Components (e.g., `<lightning-card>`, `<lightning-datatable>`, `<lightning-button>`) instead of raw SLDS markup
- Only use SLDS markup if a Lightning Base Component does not exist for the use case

### Customization
- If a Lightning Web Component needs customization, use styling hooks and slots
- Only override SLDS CSS with styling hooks, nothing else
- Follow structural markup patterns for each component
- Apply utility classes rather than custom CSS to reduce override complexity

### Component Composition
- Compose larger components by using a combination of smaller Lightning Base Components
- Break down large UIs into smaller, reusable LWC components
- Each component should have its own folder using kebab-case
- Main class should use PascalCase

### State Management
- All components that display data must handle empty, loading, and error states gracefully
- Use SLDS illustrations or messages where appropriate

## Interaction Patterns

### Modals and Dialogs
- Use modal dialogs (`slds-modal`) for focused, interruptive tasks
- Modals must use `role="dialog"` and trap focus

### Notifications
- Use toast notifications (`slds-notify_toast`) for transient system feedback
- Toasts must be `aria-live` regions to announce updates

### Loading States
- Apply spinners and skeletons to communicate loading states
- Interactive elements must have default, hover, focus, active, pressed, and visited states

### Keyboard Navigation
- Always provide a visible focus state for keyboard users
- Use appropriate `aria-` attributes and roles to support interactivity
- Avoid nesting interactive elements inside links or buttons
- Buttons and actions should always be right-aligned along the right side of containers

## Accessibility

### WCAG Compliance
- Every component must be accessible per WCAG 2.1 guidelines
- Use SLDS color utility classes and tokens for all color styling
- Associate labels with inputs via `for` and `id` or ARIA attributes
- Maintain appropriate color contrast and keyboard navigability
- Maintain an appropriate tab order for keyboard users

### Tables
- All tables must include `role="grid"`
- Use `scope="col"` for column headers
- Add ARIA attributes (`aria-label`, `aria-labelledby`, `aria-describedby`) to all interactive elements and tables

## Form Design

### Lightning Base Components
- Use Lightning Base Components for all form elements
- Examples: `<lightning-input>`, `<lightning-combobox>`, `<lightning-radio-group>`, `<lightning-textarea>`
- Do not use raw `<input>`, `<select>`, or `<textarea>` unless a Lightning Base Component does not exist

### Form Structure
- Use `slds-form-element` for grouping input + label + help text
- Label every input field with `<label>` or `aria-label`
- Show validation errors inline with helper text and an error icon
- Group related inputs using `fieldset` + `legend` when needed

### Input Types
- Use correct input types (e.g., `type="email"`) and patterns
- Utilize semantic styling hook colors for error and warning states
- Use edit and read-only modes for data

## Feedback and Validation

### Error Handling
- Use error and warning classes to indicate form validation issues
- Add `role="alert"` for inline error messages
- Use `aria-describedby` to associate help or error text

### Success Feedback
- Provide confirmation and success feedback with toasts or banners

## Layout and Responsiveness

### Responsive Design
- Ensure all layouts are responsive using SLDS grid and utility classes
- Test components at multiple breakpoints (`slds-size_1-of-1`, `slds-medium-size_1-of-2`, etc.)
- Avoid fixed pixel widths
- Use breakpoints to resize and reflow with `slds-grid`

### Responsive Utilities
- Leverage responsive utility classes (`slds-medium-size_...`, etc.)
- All designs must be responsive and adaptable to zooming
- Use percentages or percentage-related units, not fixed pixels

## Consistency and Reusability

### Component Reuse
- Reuse SLDS components across products and clouds
- Follow documented slot and modifier patterns for extending components
- Align styles with styling hooks
- Minimize overrides and avoid one-off custom styles

## Theming and Customization

### Styling Hooks
- Use styling hooks and CSS custom properties to theme, not CSS overrides
- Never redefine global styling hook values to apply custom styles
- Customizations must be scoped to replacing the values of component-scoped styling hooks (`slds-c-*`)
- Never use `!important` or manual overrides of SLDS styles
- Verify customizations meet SLDS accessibility requirements

### Inline Styles
- Do not use inline style attributes in any HTML or JSX
- All layout, spacing, and visual styling must be achieved using SLDS utility classes or component CSS files

## Integration with Existing RAG

**Related Patterns**:
- [LWC Patterns](../development/lwc-patterns.md) - Component implementation patterns
- [LWC Accessibility](lwc-accessibility.md) - Accessibility requirements

**How This Complements Existing RAG**:
- Provides official SLDS design guidelines
- Validates visual design and layout patterns
- Emphasizes component composition and reusability
- Adds responsive design and theming patterns

