---
layout: default
title: Lightning Web Component Code Examples
description: Lightning Web Components (LWC) are modern, standards-based web components for building custom user interfaces in Salesforce
permalink: /rag/code-examples/lwc/component-examples.html
level: Intermediate
tags:
  - code-examples
  - lwc
  - lightning-web-components
  - ui-components
last_reviewed: 2025-12-03
---

# Lightning Web Component Code Examples

## Overview

Lightning Web Components (LWC) provide modern, standards-based web components for building custom user interfaces in Salesforce. These examples demonstrate common patterns for:

- **Data display components**: Showing record data with LDS wire adapters
- **Form components**: Creating and editing records
- **List components**: Displaying collections with search and pagination
- **Interactive components**: User interactions with event handling
- **Console-style components**: Aggregating data from multiple sources

## When to Use

### Use LWCs When

- Need complex UI that standard page layouts cannot handle
- Need to combine data from multiple objects or systems
- Need responsive, interactive user experiences
- Need client-side filtering, sorting, or calculations
- Need to work in Experience Cloud portals
- Need real-time updates and reactive data

### Avoid LWCs When

- Standard page layouts can handle the requirement
- Screen Flows can provide the needed user experience
- Need simple field display (use standard components)
- Need offline capabilities (not supported)
- Need complex server-side processing (use Apex + Flow)

## Example 1: Record Display Component

**Use Case**: Display Contact record data with formatted fields and related information.

**Component Name**: `contactDisplay`

**JavaScript** (`contactDisplay.js`):
```javascript
import { LightningElement, api, wire } from 'lwc';
import { getRecord, getFieldValue } from 'lightning/uiRecordApi';
import CONTACT_NAME_FIELD from '@salesforce/schema/Contact.Name';
import CONTACT_EMAIL_FIELD from '@salesforce/schema/Contact.Email';
import CONTACT_PHONE_FIELD from '@salesforce/schema/Contact.Phone';
import CONTACT_TITLE_FIELD from '@salesforce/schema/Contact.Title';
import CONTACT_ACCOUNT_FIELD from '@salesforce/schema/Contact.AccountId';

const FIELDS = [
    CONTACT_NAME_FIELD,
    CONTACT_EMAIL_FIELD,
    CONTACT_PHONE_FIELD,
    CONTACT_TITLE_FIELD,
    CONTACT_ACCOUNT_FIELD
];

export default class ContactDisplay extends LightningElement {
    @api recordId;

    @wire(getRecord, { recordId: '$recordId', fields: FIELDS })
    contact;

    get name() {
        return getFieldValue(this.contact.data, CONTACT_NAME_FIELD);
    }

    get email() {
        return getFieldValue(this.contact.data, CONTACT_EMAIL_FIELD);
    }

    get phone() {
        return getFieldValue(this.contact.data, CONTACT_PHONE_FIELD);
    }

    get title() {
        return getFieldValue(this.contact.data, CONTACT_TITLE_FIELD);
    }

    get accountId() {
        return getFieldValue(this.contact.data, CONTACT_ACCOUNT_FIELD);
    }

    get hasContact() {
        return this.contact && this.contact.data;
    }

    get error() {
        return this.contact && this.contact.error;
    }
}
```

**HTML Template** (`contactDisplay.html`):
```html
<template>
    <lightning-card title="Contact Information" icon-name="standard:contact">
        <template if:true={error}>
            <div class="slds-text-color_error">
                Error loading contact: {error.body.message}
            </div>
        </template>

        <template if:true={hasContact}>
            <div class="slds-p-around_medium">
                <dl class="slds-list_horizontal slds-wrap">
                    <dt class="slds-item_label slds-text-color_weak slds-truncate" title="Name">Name:</dt>
                    <dd class="slds-item_detail slds-truncate">{name}</dd>

                    <dt class="slds-item_label slds-text-color_weak slds-truncate" title="Email">Email:</dt>
                    <dd class="slds-item_detail slds-truncate">
                        <a href="mailto:{email}">{email}</a>
                    </dd>

                    <dt class="slds-item_label slds-text-color_weak slds-truncate" title="Phone">Phone:</dt>
                    <dd class="slds-item_detail slds-truncate">{phone}</dd>

                    <dt class="slds-item_label slds-text-color_weak slds-truncate" title="Title">Title:</dt>
                    <dd class="slds-item_detail slds-truncate">{title}</dd>
                </dl>

                <template if:true={accountId}>
                    <div class="slds-m-top_medium">
                        <lightning-formatted-url 
                            value="/lightning/r/Account/{accountId}/view"
                            label="View Account">
                        </lightning-formatted-url>
                    </div>
                </template>
            </div>
        </template>

        <template if:false={hasContact}>
            <div class="slds-p-around_medium">
                <lightning-spinner alternative-text="Loading"></lightning-spinner>
            </div>
        </template>
    </lightning-card>
</template>
```

**Key Points**:
- Use `@wire(getRecord)` for reactive record data access
- Use `getFieldValue` utility for safe field access
- Handle loading, error, and data states
- Use Lightning Design System components for consistent UI
- Follow accessibility best practices (labels, semantic HTML)

## Example 2: Record Edit Form Component

**Use Case**: Create or edit Contact records with validation and error handling.

**Component Name**: `contactEditForm`

**JavaScript** (`contactEditForm.js`):
```javascript
import { LightningElement, api, track } from 'lwc';
import { ShowToastEvent } from 'lightning/platformShowToastEvent';
import { NavigationMixin } from 'lightning/navigation';
import CONTACT_OBJECT from '@salesforce/schema/Contact';
import CONTACT_FIRST_NAME_FIELD from '@salesforce/schema/Contact.FirstName';
import CONTACT_LAST_NAME_FIELD from '@salesforce/schema/Contact.LastName';
import CONTACT_EMAIL_FIELD from '@salesforce/schema/Contact.Email';
import CONTACT_PHONE_FIELD from '@salesforce/schema/Contact.Phone';

export default class ContactEditForm extends NavigationMixin(LightningElement) {
    @api recordId;
    @track error;

    objectApiName = CONTACT_OBJECT;
    fields = [
        CONTACT_FIRST_NAME_FIELD,
        CONTACT_LAST_NAME_FIELD,
        CONTACT_EMAIL_FIELD,
        CONTACT_PHONE_FIELD
    ];

    handleSuccess(event) {
        const evt = new ShowToastEvent({
            title: 'Contact saved',
            message: 'Contact record has been saved successfully',
            variant: 'success'
        });
        this.dispatchEvent(evt);

        // Navigate to the record page
        this[NavigationMixin.Navigate]({
            type: 'standard__recordPage',
            attributes: {
                recordId: event.detail.id,
                objectApiName: 'Contact',
                actionName: 'view'
            }
        });
    }

    handleError(event) {
        this.error = event.detail.detail;
        const evt = new ShowToastEvent({
            title: 'Error saving contact',
            message: this.error,
            variant: 'error'
        });
        this.dispatchEvent(evt);
    }

    handleCancel() {
        // Navigate back or close modal
        this[NavigationMixin.Navigate]({
            type: 'standard__objectPage',
            attributes: {
                objectApiName: 'Contact',
                actionName: 'list'
            }
        });
    }
}
```

**HTML Template** (`contactEditForm.html`):
```html
<template>
    <lightning-card title={formTitle} icon-name="standard:contact">
        <div class="slds-p-around_medium">
            <lightning-record-edit-form
                object-api-name={objectApiName}
                record-id={recordId}
                onsuccess={handleSuccess}
                onerror={handleError}>
                
                <lightning-messages></lightning-messages>

                <div class="slds-grid slds-gutters">
                    <div class="slds-col slds-size_1-of-2">
                        <lightning-input-field field-name={fields[0]}></lightning-input-field>
                    </div>
                    <div class="slds-col slds-size_1-of-2">
                        <lightning-input-field field-name={fields[1]}></lightning-input-field>
                    </div>
                </div>

                <div class="slds-grid slds-gutters slds-m-top_small">
                    <div class="slds-col slds-size_1-of-2">
                        <lightning-input-field field-name={fields[2]}></lightning-input-field>
                    </div>
                    <div class="slds-col slds-size_1-of-2">
                        <lightning-input-field field-name={fields[3]}></lightning-input-field>
                    </div>
                </div>

                <div class="slds-m-top_medium">
                    <lightning-button
                        type="submit"
                        label="Save"
                        variant="brand">
                    </lightning-button>
                    <lightning-button
                        type="button"
                        label="Cancel"
                        onclick={handleCancel}
                        class="slds-m-left_small">
                    </lightning-button>
                </div>
            </lightning-record-edit-form>
        </div>
    </lightning-card>
</template>
```

**Key Points**:
- Use `lightning-record-edit-form` for create/edit functionality
- Handle success and error events
- Use NavigationMixin for navigation after save
- Show toast notifications for user feedback
- Use Lightning Design System grid for responsive layout

## Example 3: List Component with Search and Pagination

**Use Case**: Display a list of Contacts with search functionality and pagination.

**Component Name**: `contactList`

**JavaScript** (`contactList.js`):
```javascript
import { LightningElement, wire, track } from 'lwc';
import { ShowToastEvent } from 'lightning/platformShowToastEvent';
import getContacts from '@salesforce/apex/ContactController.getContacts';

const COLUMNS = [
    { label: 'Name', fieldName: 'Name', type: 'text' },
    { label: 'Email', fieldName: 'Email', type: 'email' },
    { label: 'Phone', fieldName: 'Phone', type: 'phone' },
    { label: 'Title', fieldName: 'Title', type: 'text' }
];

export default class ContactList extends LightningElement {
    columns = COLUMNS;
    @track contacts = [];
    @track error;
    @track searchKey = '';
    @track pageSize = 10;
    @track currentPage = 1;
    @track totalRecords = 0;

    @wire(getContacts, { 
        searchKey: '$searchKey',
        pageSize: '$pageSize',
        pageNumber: '$currentPage'
    })
    wiredContacts({ error, data }) {
        if (data) {
            this.contacts = data.records;
            this.totalRecords = data.totalRecords;
            this.error = undefined;
        } else if (error) {
            this.error = error;
            this.contacts = [];
            this.showToast('Error', error.body.message, 'error');
        }
    }

    handleSearchChange(event) {
        this.searchKey = event.target.value;
        this.currentPage = 1; // Reset to first page on new search
    }

    handlePreviousPage() {
        if (this.currentPage > 1) {
            this.currentPage = this.currentPage - 1;
        }
    }

    handleNextPage() {
        const totalPages = Math.ceil(this.totalRecords / this.pageSize);
        if (this.currentPage < totalPages) {
            this.currentPage = this.currentPage + 1;
        }
    }

    get isFirstPage() {
        return this.currentPage === 1;
    }

    get isLastPage() {
        return this.currentPage >= Math.ceil(this.totalRecords / this.pageSize);
    }

    get pageInfo() {
        const start = (this.currentPage - 1) * this.pageSize + 1;
        const end = Math.min(this.currentPage * this.pageSize, this.totalRecords);
        return `Showing ${start}-${end} of ${this.totalRecords}`;
    }

    showToast(title, message, variant) {
        const evt = new ShowToastEvent({
            title: title,
            message: message,
            variant: variant
        });
        this.dispatchEvent(evt);
    }
}
```

**HTML Template** (`contactList.html`):
```html
<template>
    <lightning-card title="Contacts" icon-name="standard:contact">
        <div class="slds-p-around_medium">
            <div class="slds-grid slds-gutters slds-m-bottom_medium">
                <div class="slds-col slds-size_1-of-1">
                    <lightning-input
                        type="search"
                        label="Search Contacts"
                        value={searchKey}
                        onchange={handleSearchChange}
                        placeholder="Search by name or email...">
                    </lightning-input>
                </div>
            </div>

            <template if:true={error}>
                <div class="slds-text-color_error">
                    Error loading contacts: {error.body.message}
                </div>
            </template>

            <template if:true={contacts}>
                <lightning-datatable
                    key-field="Id"
                    data={contacts}
                    columns={columns}
                    hide-checkbox-column>
                </lightning-datatable>

                <div class="slds-m-top_medium slds-grid slds-grid_align-spread">
                    <div class="slds-col">
                        <lightning-button
                            label="Previous"
                            onclick={handlePreviousPage}
                            disabled={isFirstPage}>
                        </lightning-button>
                        <lightning-button
                            label="Next"
                            onclick={handleNextPage}
                            disabled={isLastPage}
                            class="slds-m-left_small">
                        </lightning-button>
                    </div>
                    <div class="slds-col slds-text-align_right">
                        <span class="slds-text-color_weak">{pageInfo}</span>
                    </div>
                </div>
            </template>

            <template if:false={contacts}>
                <div class="slds-p-around_medium">
                    <lightning-spinner alternative-text="Loading"></lightning-spinner>
                </div>
            </template>
        </div>
    </lightning-card>
</template>
```

**Apex Controller** (`ContactController.cls`):
```apex
public with sharing class ContactController {
    @AuraEnabled(cacheable=true)
    public static ContactListResult getContacts(String searchKey, Integer pageSize, Integer pageNumber) {
        Integer offset = (pageNumber - 1) * pageSize;
        String searchPattern = '%' + String.escapeSingleQuotes(searchKey) + '%';
        
        String query = 'SELECT Id, Name, Email, Phone, Title FROM Contact';
        String whereClause = '';
        
        if (String.isNotBlank(searchKey)) {
            whereClause = ' WHERE (Name LIKE :searchPattern OR Email LIKE :searchPattern)';
        }
        
        query += whereClause + ' WITH SECURITY_ENFORCED ORDER BY Name LIMIT :pageSize OFFSET :offset';
        
        List<Contact> contacts = Database.query(query);
        
        // Get total count
        String countQuery = 'SELECT COUNT() FROM Contact' + whereClause;
        Integer totalRecords = Database.countQuery(countQuery);
        
        return new ContactListResult(contacts, totalRecords);
    }
    
    public class ContactListResult {
        @AuraEnabled public List<Contact> records;
        @AuraEnabled public Integer totalRecords;
        
        public ContactListResult(List<Contact> records, Integer totalRecords) {
            this.records = records;
            this.totalRecords = totalRecords;
        }
    }
}
```

**Key Points**:
- Use server-side pagination for large datasets
- Use server-side search for efficient filtering
- Use `@wire` with reactive parameters for automatic refresh
- Handle loading, error, and data states
- Use `lightning-datatable` for tabular data display
- Implement proper pagination controls

## Example 4: Interactive Component with Event Handling

**Use Case**: Component that handles user interactions and communicates with parent components.

**Component Name**: `contactCard`

**JavaScript** (`contactCard.js`):
```javascript
import { LightningElement, api } from 'lwc';
import { ShowToastEvent } from 'lightning/platformShowToastEvent';

export default class ContactCard extends LightningElement {
    @api contact;
    @api showActions = false;

    handleView() {
        // Dispatch custom event to parent
        const viewEvent = new CustomEvent('view', {
            detail: { contactId: this.contact.Id }
        });
        this.dispatchEvent(viewEvent);
    }

    handleEdit() {
        const editEvent = new CustomEvent('edit', {
            detail: { contactId: this.contact.Id }
        });
        this.dispatchEvent(editEvent);
    }

    handleDelete() {
        // Show confirmation dialog
        if (confirm('Are you sure you want to delete this contact?')) {
            const deleteEvent = new CustomEvent('delete', {
                detail: { contactId: this.contact.Id }
            });
            this.dispatchEvent(deleteEvent);
        }
    }

    get contactName() {
        return this.contact ? this.contact.Name : '';
    }

    get contactEmail() {
        return this.contact ? this.contact.Email : '';
    }

    get contactPhone() {
        return this.contact ? this.contact.Phone : '';
    }
}
```

**HTML Template** (`contactCard.html`):
```html
<template>
    <lightning-card>
        <div class="slds-p-around_medium">
            <div class="slds-media">
                <div class="slds-media__figure">
                    <lightning-icon icon-name="standard:contact" size="small"></lightning-icon>
                </div>
                <div class="slds-media__body">
                    <div class="slds-text-heading_small">{contactName}</div>
                    <div class="slds-text-body_small slds-m-top_x-small">
                        <template if:true={contactEmail}>
                            <div>Email: {contactEmail}</div>
                        </template>
                        <template if:true={contactPhone}>
                            <div>Phone: {contactPhone}</div>
                        </template>
                    </div>
                </div>
            </div>

            <template if:true={showActions}>
                <div class="slds-m-top_medium slds-button-group">
                    <lightning-button
                        label="View"
                        onclick={handleView}
                        variant="neutral">
                    </lightning-button>
                    <lightning-button
                        label="Edit"
                        onclick={handleEdit}
                        variant="brand">
                    </lightning-button>
                    <lightning-button
                        label="Delete"
                        onclick={handleDelete}
                        variant="destructive">
                    </lightning-button>
                </div>
            </template>
        </div>
    </lightning-card>
</template>
```

**Key Points**:
- Use custom events for parent-child communication
- Handle user interactions (clicks, confirmations)
- Use conditional rendering for optional features
- Follow event naming conventions (lowercase, descriptive)
- Pass data via event detail property

## Testing Considerations

### Test Scenarios

1. **Data Loading**:
   - Test with valid record IDs
   - Test with invalid record IDs
   - Test with missing data
   - Test error handling

2. **User Interactions**:
   - Test button clicks
   - Test form submissions
   - Test search functionality
   - Test pagination

3. **Event Handling**:
   - Test custom event dispatching
   - Test event data passing
   - Test parent component handling

4. **Rendering**:
   - Test conditional rendering
   - Test loading states
   - Test error states
   - Test empty states

### Best Practices

- Write Jest unit tests for all components
- Test with different data scenarios
- Test error scenarios
- Test accessibility (keyboard navigation, screen readers)
- Test on different devices (responsive design)
- Use `@wire` for reactive data access
- Handle all component states (loading, error, data)

## Related Patterns

- <a href="{{ '/rag/development/lwc-patterns.html' | relative_url }}">LWC Patterns</a> - Comprehensive LWC patterns and best practices
- <a href="{{ '/rag/code-examples/lwc/service-examples.html' | relative_url }}">LWC Service Examples</a> - Reusable service layer patterns
- <a href="{{ '/rag/code-examples/lwc/wire-examples.html' | relative_url }}">LWC Wire Examples</a> - Wire service patterns for data access
- <a href="{{ '/rag/code-examples/lwc/test-examples.html' | relative_url }}">LWC Test Examples</a> - Jest testing patterns for LWCs
- <a href="{{ '/rag/mcp-knowledge/lwc-best-practices.html' | relative_url }}">LWC Best Practices</a> - Official LWC best practices
