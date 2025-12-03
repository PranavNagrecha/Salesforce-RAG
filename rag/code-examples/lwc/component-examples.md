# Lightning Web Component Code Examples

> This file contains complete, working code examples for Lightning Web Component patterns.
> All examples are copy-paste ready and follow Salesforce best practices.

## Overview

Lightning Web Components (LWC) are modern, standards-based web components for building custom user interfaces in Salesforce. These examples demonstrate common LWC patterns for data access, user interactions, and business logic.

**Related Patterns**:
- [LWC Patterns](/rag/code-examples/development/lwc-patterns.html) - LWC development patterns and best practices
- [LWC API Reference](/rag/code-examples/api-reference/lwc-api-reference.html) - LWC API method signatures

## Examples

### Example 1: Basic Record Display Component

**Pattern**: Display record data using Lightning Data Service
**Use Case**: Displaying record information on a record page
**Complexity**: Basic
**Related Patterns**: [LWC Data Access Patterns](../development/lwc-patterns.html#data-access-patterns)

**Problem**:
You need to display record data in a custom component on a record page.

**Solution**:

**JavaScript** (`contactDisplay.js`):
```javascript
import { LightningElement, api, wire } from 'lwc';
import { getRecord } from 'lightning/uiRecordApi';
import CONTACT_NAME_FIELD from '@salesforce/schema/Contact.Name';
import CONTACT_EMAIL_FIELD from '@salesforce/schema/Contact.Email';
import CONTACT_PHONE_FIELD from '@salesforce/schema/Contact.Phone';

const FIELDS = [CONTACT_NAME_FIELD, CONTACT_EMAIL_FIELD, CONTACT_PHONE_FIELD];

export default class ContactDisplay extends LightningElement {
    @api recordId;

    @wire(getRecord, { recordId: '$recordId', fields: FIELDS })
    contact;

    get contactName() {
        return this.contact?.data?.fields?.Name?.value || '';
    }

    get contactEmail() {
        return this.contact?.data?.fields?.Email?.value || '';
    }

    get contactPhone() {
        return this.contact?.data?.fields?.Phone?.value || '';
    }
}
```

**HTML** (`contactDisplay.html`):
```html
<template>
    <lightning-card title="Contact Information" icon-name="standard:contact">
        <div class="slds-p-around_medium">
            <template if:true={contact.data}>
                <dl class="slds-list_horizontal slds-wrap">
                    <dt class="slds-item_label slds-text-color_weak">Name:</dt>
                    <dd class="slds-item_detail">{contactName}</dd>
                    <dt class="slds-item_label slds-text-color_weak">Email:</dt>
                    <dd class="slds-item_detail">{contactEmail}</dd>
                    <dt class="slds-item_label slds-text-color_weak">Phone:</dt>
                    <dd class="slds-item_detail">{contactPhone}</dd>
                </dl>
            </template>
            <template if:true={contact.error}>
                <div class="slds-text-color_error">
                    Error loading contact: {contact.error}
                </div>
            </template>
        </div>
    </lightning-card>
</template>
```

**Explanation**:
- Uses `@wire(getRecord)` for reactive data access
- Displays record fields using Lightning Data Service
- Handles loading and error states
- Uses optional chaining (`?.`) for safe property access

**Best Practices**:
- Use `@wire` for reactive data that should update automatically
- Always handle loading and error states
- Use optional chaining to prevent null reference errors
- Import field references from `@salesforce/schema`

### Example 2: Component with Imperative Apex Call

**Pattern**: Calling Apex methods imperatively for user actions
**Use Case**: Performing actions that require user interaction
**Complexity**: Intermediate
**Related Patterns**: [LWC Data Access Patterns](../development/lwc-patterns.html#data-access-patterns)

**Problem**:
You need to call an Apex method when a user clicks a button.

**Solution**:

**JavaScript** (`contactAction.js`):
```javascript
import { LightningElement, api } from 'lwc';
import processContacts from '@salesforce/apex/ContactService.processContacts';
import { ShowToastEvent } from 'lightning/platformShowToastEvent';

export default class ContactAction extends LightningElement {
    @api recordId;
    isLoading = false;

    handleProcess() {
        this.isLoading = true;
        
        processContacts({ contactIds: [this.recordId] })
            .then(result => {
                this.showToast('Success', 'Contact processed successfully', 'success');
                this.dispatchEvent(new CustomEvent('refresh'));
            })
            .catch(error => {
                this.showToast('Error', error.body?.message || 'An error occurred', 'error');
            })
            .finally(() => {
                this.isLoading = false;
            });
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

**HTML** (`contactAction.html`):
```html
<template>
    <lightning-card title="Contact Actions">
        <div class="slds-p-around_medium">
            <lightning-button
                label="Process Contact"
                onclick={handleProcess}
                variant="brand"
                disabled={isLoading}>
            </lightning-button>
        </div>
    </lightning-card>
</template>
```

**Explanation**:
- Uses imperative Apex call for user-initiated actions
- Handles loading state to prevent multiple clicks
- Shows toast notifications for success and error
- Dispatches custom event to refresh parent component

**Best Practices**:
- Use imperative calls for user actions (not reactive data)
- Always handle loading states
- Provide user feedback with toast notifications
- Handle errors gracefully

### Example 3: Component with Form Input

**Pattern**: Collecting user input and updating records
**Use Case**: Allowing users to edit record data
**Complexity**: Intermediate
**Related Patterns**: [LWC Patterns](/rag/code-examples/development/lwc-patterns.html)

**Problem**:
You need to allow users to edit record fields in a custom component.

**Solution**:

**JavaScript** (`contactEdit.js`):
```javascript
import { LightningElement, api, track } from 'lwc';
import { updateRecord } from 'lightning/uiRecordApi';
import { ShowToastEvent } from 'lightning/platformShowToastEvent';
import CONTACT_ID_FIELD from '@salesforce/schema/Contact.Id';
import CONTACT_EMAIL_FIELD from '@salesforce/schema/Contact.Email';

export default class ContactEdit extends LightningElement {
    @api recordId;
    @track email = '';

    handleEmailChange(event) {
        this.email = event.target.value;
    }

    handleSave() {
        const fields = {};
        fields[CONTACT_ID_FIELD.fieldApiName] = this.recordId;
        fields[CONTACT_EMAIL_FIELD.fieldApiName] = this.email;

        const recordInput = { fields };

        updateRecord(recordInput)
            .then(() => {
                this.showToast('Success', 'Contact updated successfully', 'success');
                this.dispatchEvent(new CustomEvent('refresh'));
            })
            .catch(error => {
                this.showToast('Error', error.body?.message || 'Update failed', 'error');
            });
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

**HTML** (`contactEdit.html`):
```html
<template>
    <lightning-card title="Edit Contact">
        <div class="slds-p-around_medium">
            <lightning-input
                label="Email"
                type="email"
                value={email}
                onchange={handleEmailChange}>
            </lightning-input>
            <div class="slds-m-top_medium">
                <lightning-button
                    label="Save"
                    onclick={handleSave}
                    variant="brand">
                </lightning-button>
            </div>
        </div>
    </lightning-card>
</template>
```

**Explanation**:
- Uses `updateRecord` from Lightning Data Service
- Handles form input with change handlers
- Updates record with user input
- Provides feedback with toast notifications

**Best Practices**:
- Use Lightning Data Service for standard object updates when possible
- Validate input before saving
- Provide clear user feedback
- Handle errors gracefully

## Related Examples

- [Service Layer Examples](/rag/code-examples/lwc/apex/service-layer-examples.html) - Apex service methods called from LWC
- [Accessibility Examples](/rag/code-examples/lwc/lwc/accessibility-examples.html) - Accessible LWC patterns
- [LWC API Reference](/rag/code-examples/api-reference/lwc-api-reference.html) - Complete LWC API reference

## See Also

- [LWC Patterns](/rag/code-examples/development/lwc-patterns.html) - Complete LWC development patterns
- [LWC Best Practices](/rag/code-examples/mcp-knowledge/lwc-best-practices.html) - Official LWC best practices
- [LWC Development Guide](/rag/code-examples/mcp-knowledge/lwc-development-guide.html) - LWC development guidance

