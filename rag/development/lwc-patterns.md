---
title: "Lightning Web Component (LWC) Patterns"
level: "Intermediate"
tags:
  - lwc
  - development
  - patterns
  - lightning-web-components
  - frontend
last_reviewed: "2025-01-XX"
---

# Lightning Web Component (LWC) Patterns

## Overview

LWCs are built for complex business logic that standard page layouts cannot handle. Components are designed to make complex processes usable for non-technical users and hide integration complexity behind simple interfaces.

Lightning Web Components (LWC) are modern, standards-based web components built on web standards (Web Components, ES6+, CSS) that enable developers to build custom user interfaces for Salesforce. Understanding LWC fundamentals, component architecture, and patterns enables developers to build responsive, accessible, and performant user interfaces.

## Prerequisites

**Required Knowledge**:
- JavaScript (ES6+) fundamentals
- HTML and CSS basics
- Understanding of Salesforce data model
- Basic understanding of Apex (for calling server-side methods)

**Recommended Reading**:
- <a href="{{ '/rag/development/apex-patterns.html' | relative_url }}">Apex Patterns</a> - Apex service layer patterns for LWC integration
- <a href="{{ '/rag/development/lightning-app-builder.html' | relative_url }}">Lightning App Builder</a> - Understanding when to use declarative vs custom components
- <a href="{{ '/rag/testing/lwc-accessibility-testing.html' | relative_url }}">LWC Accessibility Testing</a> - Accessibility best practices

## LWC Fundamentals

### Component Structure

**Component bundle**:
- **JavaScript file**: Component logic and behavior
- **HTML template**: Component markup and structure
- **CSS file**: Component styling (optional)
- **XML metadata file**: Component configuration and targets

**Component lifecycle**:
- `constructor()`: Component initialization
- `connectedCallback()`: Component added to DOM
- `renderedCallback()`: Component rendered
- `disconnectedCallback()`: Component removed from DOM

**Best practice**: Understand component lifecycle hooks. Use lifecycle hooks appropriately. Avoid heavy operations in constructor. Use `connectedCallback` for initialization.

### Decorators and Properties

**@api**: Public properties and methods exposed to parent components.

**@track**: Reactive properties that trigger re-render when changed (deprecated in modern LWC, properties are reactive by default).

**@wire**: Reactive service that automatically provides data or calls methods.

**@AuraEnabled**: Methods callable from Aura components or external contexts.

**Best practice**: Use `@api` for public properties. Use `@wire` for reactive data access. Properties are reactive by default (no need for `@track` in modern LWC).

### Data Access Patterns

**Lightning Data Service (LDS)**:
- `getRecord`: Get single record data
- `getRecordUi`: Get record data with layout information
- `updateRecord`: Update record data
- `createRecord`: Create new record
- `deleteRecord`: Delete record

**Wire adapters**:
- `@wire(getRecord, { recordId: '$recordId', fields: FIELDS })` for record data
- `@wire(getObjectInfo, { objectApiName: ACCOUNT_OBJECT })` for object metadata
- `@wire(getPicklistValues, { recordTypeId: '$recordTypeId', fieldApiName: FIELD })` for picklist values

**Imperative Apex calls**:
- Use `methodName({ params })` for on-demand Apex calls
- Handle promises with `.then()` and `.catch()`
- Use for actions that aren't reactive

**Best practice**: Use LDS wire adapters for reactive data access. Use imperative Apex calls for on-demand actions. Handle errors appropriately.

### Event Handling

**Component events**: Communication between child and parent components.

**Lightning Message Service**: Communication between components that aren't in parent-child relationship.

**Standard events**: Platform events like `recordUpdated`, `recordCreated`.

**Best practice**: Use component events for parent-child communication. Use Lightning Message Service for cross-component communication. Handle events appropriately.

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

### Dynamic Field Display Patterns

**Pattern**: Dynamically show fields in `lightning-record-edit-form` based on Custom Metadata configuration

**When to use**: When field visibility needs to be configurable without code changes, or when different user types need different field sets.

**Implementation approach**:
- Store field API names in Custom Metadata Types
- Fetch field configurations from Apex
- Dynamically render fields in `lightning-record-edit-form` based on metadata
- Support conditional field display based on record type, user profile, or other criteria

**Why it's recommended**: Instead of hardcoding field names in LWC components, storing field APIs in Custom Metadata allows administrators to configure which fields appear without code changes. This enables environment-specific configurations and easier maintenance.

**Example scenario**: A record edit form that needs to show different fields based on the record type. Field configurations are stored in Custom Metadata, fetched by Apex, and dynamically rendered in the LWC component.

**Implementation Pattern**:

#### Step 1: Custom Metadata Type Structure

Create a Custom Metadata Type `Field_Configuration__mdt` with fields:
- `Field_API_Name__c` (Text) - The API name of the field
- `Object_API_Name__c` (Text) - The object API name
- `Record_Type__c` (Text) - Optional: Record type filter
- `Display_Order__c` (Number) - Order in which fields should appear
- `Is_Required__c` (Checkbox) - Whether field is required
- `Is_Active__c` (Checkbox) - Whether field should be displayed

#### Step 2: Apex Method to Fetch Field Configurations

```apex
public with sharing class FieldConfigurationService {
    
    /**
     * Gets field configurations for an object and optional record type
     * @param objectApiName Object API name
     * @param recordTypeId Optional record type ID
     * @return List of field API names in display order
     */
    @AuraEnabled(cacheable=true)
    public static List<String> getFieldConfigurations(String objectApiName, String recordTypeId) {
        List<String> fieldApiNames = new List<String>();
        
        // Query Custom Metadata
        List<Field_Configuration__mdt> configs = [
            SELECT Field_API_Name__c, Display_Order__c
            FROM Field_Configuration__mdt
            WHERE Object_API_Name__c = :objectApiName
            AND Is_Active__c = true
            ORDER BY Display_Order__c ASC
        ];
        
        // Extract field API names
        for (Field_Configuration__mdt config : configs) {
            fieldApiNames.add(config.Field_API_Name__c);
        }
        
        return fieldApiNames;
    }
}
```

#### Step 3: LWC Component with Dynamic Fields

```javascript
import { LightningElement, wire, api } from 'lwc';
import { getFieldConfigurations } from 'c/fieldConfigurationService';
import { ShowToastEvent } from 'lightning/platformShowToastEvent';

export default class DynamicRecordEditForm extends LightningElement {
    @api recordId;
    @api objectApiName;
    
    fieldApiNames = [];
    isLoading = true;
    
    @wire(getFieldConfigurations, { 
        objectApiName: '$objectApiName',
        recordTypeId: null 
    })
    wiredFieldConfigurations({ data, error }) {
        if (data) {
            this.fieldApiNames = data;
            this.isLoading = false;
        } else if (error) {
            this.showError('Error loading field configuration', error);
            this.isLoading = false;
        }
    }
    
    handleSuccess(event) {
        this.showSuccess('Record saved successfully');
        // Optionally refresh or navigate
    }
    
    handleError(event) {
        this.showError('Error saving record', event.detail);
    }
    
    showSuccess(message) {
        this.dispatchEvent(new ShowToastEvent({
            title: 'Success',
            message: message,
            variant: 'success'
        }));
    }
    
    showError(title, message) {
        this.dispatchEvent(new ShowToastEvent({
            title: title,
            message: message,
            variant: 'error'
        }));
    }
}
```

#### Step 4: HTML Template with Dynamic Fields

```html
<template>
    <lightning-card title="Edit Record">
        <template if:true={isLoading}>
            <lightning-spinner alternative-text="Loading"></lightning-spinner>
        </template>
        
        <template if:false={isLoading}>
            <lightning-record-edit-form
                record-id={recordId}
                object-api-name={objectApiName}
                onsuccess={handleSuccess}
                onerror={handleError}>
                
                <template for:each={fieldApiNames} for:item="fieldApiName">
                    <lightning-input-field
                        key={fieldApiName}
                        field-name={fieldApiName}>
                    </lightning-input-field>
                </template>
                
                <lightning-button
                    class="slds-m-top_small"
                    type="submit"
                    label="Save">
                </lightning-button>
            </lightning-record-edit-form>
        </template>
    </lightning-card>
</template>
```

**Key Points**:
- Field configurations stored in Custom Metadata (not hardcoded in component)
- Apex method fetches configurations (cacheable for performance)
- LWC dynamically renders fields based on metadata
- Supports conditional display based on record type or other criteria
- No code changes needed to add/remove fields (just update Custom Metadata)

**Benefits**:
- **Configuration-driven**: Administrators can configure fields without code changes
- **Environment-specific**: Different field sets per environment via Custom Metadata
- **Maintainable**: Field changes don't require component updates
- **Flexible**: Supports conditional field display based on various criteria

**Related Patterns**: <a href="{{ '/rag/development/custom-settings-metadata-patterns.html' | relative_url }}">Custom Settings and Metadata Patterns</a>, [Config-Driven UI](#config-driven-ui)

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
- <a href="{{ '/rag/development/mcp-knowledge/lwc-accessibility.html' | relative_url }}">LWC Accessibility Guidelines</a> - Comprehensive WCAG 2.2 compliance guidance
- <a href="{{ '/rag/development/code-examples/lwc/accessibility-examples.html' | relative_url }}">LWC Accessibility Examples</a> - Complete working code examples
- <a href="{{ '/rag/testing/lwc-accessibility-testing.html' | relative_url }}">LWC Accessibility Testing</a> - Testing patterns and tools
- <a href="{{ '/rag/development/troubleshooting/lwc-accessibility-errors.html' | relative_url }}">LWC Accessibility Troubleshooting</a> - Common errors and fixes
- <a href="{{ '/rag/development/quick-start/lwc-accessibility-quick-start.html' | relative_url }}">LWC Accessibility Quick Start</a> - Quick start guide

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

**Example**: See <a href="{{ '/rag/development/Salesforce-RAG/rag/code-examples/lwc/accessibility-examples.html#form-accessibility-examples.html' | relative_url }}">Accessible Form Examples</a>

### Keyboard Navigation

- **Focus Indicators**: All interactive elements must have visible focus indicators (2px outline, 3:1 contrast)
- **Tab Order**: Logical tab order through all interactive elements
- **Keyboard Shortcuts**: Support Enter, Space, Escape keys appropriately
- **Focus Trapping**: Modals must trap focus and close on Escape key
- **Focus Return**: Focus returns to trigger element after modal close
- **No Keyboard Traps**: Ensure users can navigate away from all areas

**Example**: See <a href="{{ '/rag/development/Salesforce-RAG/rag/code-examples/lwc/accessibility-examples.html#keyboard-navigation-examples.html' | relative_url }}">Keyboard Navigation Examples</a>

### Semantic HTML

- Use semantic HTML elements (`<header>`, `<nav>`, `<main>`, `<footer>`, `<section>`)
- Proper heading hierarchy (h1 → h2 → h3, no skipping levels)
- Meaningful form labels (not just placeholder text)
- Accessible form controls
- Proper list markup (`<ul>`, `<ol>`, `<dl>`)
- Proper table structure with headers and scope attributes

**Example**: See <a href="{{ '/rag/development/Salesforce-RAG/rag/code-examples/lwc/accessibility-examples.html#semantic-html-examples.html' | relative_url }}">Semantic HTML Examples</a>

### ARIA Labels and Attributes

- **ARIA Labels**: Provide `aria-label` for icon-only buttons and custom components
- **ARIA Roles**: Use appropriate `role` attributes for custom interactive components
- **ARIA States**: Use ARIA states (aria-checked, aria-expanded, aria-busy, etc.)
- **ARIA Live Regions**: Use `aria-live="polite"` for status updates, `aria-live="assertive"` for errors
- **ARIA Descriptions**: Use `aria-describedby` to associate help text and error messages
- **Modal Dialogs**: Use `role="dialog"` and `aria-modal="true"` for modals

**Example**: See <a href="{{ '/rag/development/Salesforce-RAG/rag/code-examples/lwc/accessibility-examples.html#aria-patterns.html' | relative_url }}">ARIA Patterns Examples</a>

### Image Accessibility

- **Decorative Images**: Use `alt=""` and optionally `aria-hidden="true"`
- **Informative Images**: Use descriptive `alt` text that conveys the information
- **Image Links**: Provide `aria-label` on the link, use `alt=""` on the image
- **Complex Images**: Use `aria-describedby` with `figcaption` for detailed descriptions

**Example**: See <a href="{{ '/rag/development/Salesforce-RAG/rag/code-examples/lwc/accessibility-examples.html#image-accessibility.html' | relative_url }}">Image Accessibility Examples</a>

### Color and Contrast

- **Text Contrast**: Normal text must meet 4.5:1 contrast ratio, large text 3:1
- **Focus Indicators**: Focus outlines must meet 3:1 contrast ratio
- **Not Color Alone**: Information must not be conveyed by color alone (use icons/text)
- **SLDS Tokens**: Use SLDS color tokens for proper contrast

**Example**: See <a href="{{ '/rag/development/Salesforce-RAG/rag/code-examples/lwc/accessibility-examples.html#color-and-contrast.html' | relative_url }}">Color and Contrast Examples</a>

### Dynamic Content Accessibility

- **Loading States**: Use `aria-live="polite"` and `aria-busy="true"` for loading states
- **Error Messages**: Use `role="alert"` and `aria-live="assertive"` for errors
- **Success Messages**: Use `role="status"` and `aria-live="polite"` for success messages
- **Status Updates**: Announce dynamic content changes to screen readers

**Example**: See <a href="{{ '/rag/development/Salesforce-RAG/rag/code-examples/lwc/accessibility-examples.html#dynamic-content-accessibility.html' | relative_url }}">Dynamic Content Examples</a>

### Testing Accessibility

- **Automated Testing**: Use axe-core, Lighthouse, or Salesforce Accessibility Scanner
- **Manual Testing**: Test with keyboard-only navigation
- **Screen Reader Testing**: Test with NVDA (Windows), JAWS (Windows), or VoiceOver (macOS/iOS)
- **Color Contrast Testing**: Use WebAIM Contrast Checker
- **Jest Testing**: Include accessibility tests in Jest test suites

**See**: <a href="{{ '/rag/testing/lwc-accessibility-testing.html' | relative_url }}">LWC Accessibility Testing</a> for complete testing patterns

### Common Accessibility Mistakes

- Missing form labels
- Missing ARIA labels on icon buttons
- Keyboard traps in modals
- Missing focus indicators
- Insufficient color contrast
- Missing alt text on images
- Incorrect heading hierarchy
- Missing semantic HTML

**See**: <a href="{{ '/rag/development/troubleshooting/lwc-accessibility-errors.html' | relative_url }}">LWC Accessibility Troubleshooting</a> for solutions to common errors

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

## Related Patterns

**See Also**:
- <a href="{{ '/rag/development/apex-patterns.html' | relative_url }}">Apex Patterns</a> - Apex service layer patterns for LWC integration
- <a href="{{ '/rag/development/flow-patterns.html' | relative_url }}">Flow Patterns</a> - Understanding when to use declarative vs custom components
- <a href="{{ '/rag/development/lightning-app-builder.html' | relative_url }}">Lightning App Builder</a> - Declarative component configuration
- <a href="{{ '/rag/development/order-of-execution.html' | relative_url }}">Order of Execution</a> - Understanding when LWCs execute

**Related Domains**:
- <a href="{{ '/rag/testing/lwc-accessibility-testing.html' | relative_url }}">LWC Accessibility Testing</a> - Accessibility testing patterns
- <a href="{{ '/rag/testing/lwc-jest-testing.html' | relative_url }}">LWC Jest Testing</a> - Unit testing Lightning Web Components
- <a href="{{ '/rag/development/troubleshooting/common-lwc-errors.html' | relative_url }}">Common LWC Errors</a> - Troubleshooting LWC issues
- <a href="{{ '/rag/development/troubleshooting/lwc-accessibility-errors.html' | relative_url }}">LWC Accessibility Errors</a> - Accessibility error resolution
- <a href="{{ '/rag/code-examples/lwc.html' | relative_url }}">Code Examples</a> - Complete LWC code examples

## Q&A

### Q: When should I use LWC instead of standard page layouts or Flows?

**A**: Use LWC when you need to combine data from multiple objects or systems, require complex client-side decisions and filtering, need responsive interactive experiences, or standard layouts and Flows cannot handle the requirement. LWCs are surgical tools for complex UI needs that declarative tools cannot address.

### Q: What is the difference between `@wire` and imperative Apex calls?

**A**: `@wire` is reactive and automatically provides data when parameters change. Use `@wire` for data that should update automatically. Imperative Apex calls (`methodName({ params })`) are on-demand and give you control over when to fetch data. Use imperative calls for actions, updates, or when you need to control the timing of data access.

### Q: How do I handle errors in LWC components?

**A**: Wrap Apex calls in try-catch blocks. Display user-friendly error messages using `lightning-messages` or custom error components. Log errors to a logging service for troubleshooting. Provide recovery paths (e.g., retry buttons) when appropriate. Always handle loading states to show users when operations are in progress.

### Q: How do I optimize LWC performance?

**A**: Minimize server round trips by batching data requests into single Apex methods. Use cacheable methods with cache busting when fresh data is needed. Implement lazy loading for detailed breakdowns that aren't needed immediately. Defer heavy calculations to async jobs if needed. Use `refreshApex` carefully to avoid unnecessary server calls.

### Q: How do I make LWC components accessible?

**A**: Follow WCAG 2.2 guidelines. Use semantic HTML elements. Provide proper labels for all form inputs. Ensure keyboard navigation works for all interactive elements. Maintain proper focus indicators. Ensure sufficient color contrast. Test with screen readers. Use ARIA attributes when semantic HTML isn't sufficient.

### Q: Can I use LWC in Experience Cloud (Community) portals?

**A**: Yes, LWCs work in Experience Cloud portals. However, you need to ensure proper security and sharing. Use `with sharing` in Apex classes called from LWCs. Consider portal user permissions and sharing sets. Test thoroughly with different portal user types to ensure proper access control.

### Q: How do I pass data between parent and child LWC components?

**A**: Use `@api` properties to pass data from parent to child. Use component events to communicate from child to parent. Use Lightning Message Service for communication between components that aren't in a parent-child relationship. Use `@track` is not needed in modern LWC (properties are reactive by default).

### Q: How do I update records in LWC?

**A**: Use `updateRecord` from Lightning Data Service for standard objects when possible. Use imperative Apex calls with `@AuraEnabled` methods for custom objects or complex updates. Always handle errors and provide user feedback. Use `refreshApex` to update wire adapter data after updates if needed.

### Q: What is the best way to handle large data sets in LWC?

**A**: Implement pagination or infinite scroll for large lists. Use lazy loading to defer loading detailed data until needed. Consider server-side filtering and sorting to reduce data transfer. Use Platform Cache for frequently accessed data. Consider using Platform Events for real-time updates instead of polling.

### Q: How do I test LWC components?

**A**: Use Jest for unit testing LWC components. Test component rendering, user interactions, and data flow. Mock Apex methods and wire adapters. Test error handling scenarios. Use `@salesforce/sfdx-lwc-jest` for Salesforce-specific testing utilities. Aim for high code coverage, especially for business logic.
- Use semantic HTML
- Provide ARIA labels where needed
- Ensure keyboard navigation works
- Test with screen readers

