---
layout: default
title: Lightning Web Component (LWC) Patterns
description: LWCs are built for complex business logic that standard page layouts cannot handle
permalink: /rag/development/lightning-app-builder.html' | relative_url }}">Lightning App Builder</a> - Understanding when to use declarative vs custom components
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

**Related Patterns**: <a href="{{ '/rag/development/order-of-execution.html' | relative_url }}">Order of Execution</a> - Understanding when LWCs execute

**Related Domains**:
- <a href="{{ '/rag/testing/lwc-accessibility-testing.html' | relative_url }}">LWC Accessibility Testing</a> - Accessibility testing patterns
- <a href="{{ '/rag/testing/lwc-jest-testing.html' | relative_url }}">LWC Jest Testing</a> - Unit testing Lightning Web Components
- <a href="{{ '/rag/troubleshooting/common-lwc-errors.html' | relative_url }}">Common LWC Errors</a> - Troubleshooting LWC issues
- <a href="{{ '/rag/troubleshooting/lwc-accessibility-errors.html' | relative_url }}">LWC Accessibility Errors</a> - Accessibility error resolution
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

