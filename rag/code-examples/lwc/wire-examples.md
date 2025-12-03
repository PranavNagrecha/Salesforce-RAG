---
title: "LWC Wire Service Code Examples"
level: "Intermediate"
tags:
  - lwc
  - code-examples
  - wire-service
  - data-access
last_reviewed: "2025-01-XX"
---

# LWC Wire Service Code Examples

> This file contains complete, working code examples for LWC wire service patterns.
> All examples are copy-paste ready and follow Salesforce best practices.

## Overview

Wire services provide reactive data access in Lightning Web Components. The `@wire` decorator automatically manages data fetching, caching, and reactivity. This document demonstrates common wire service patterns for accessing Salesforce data.

**Related Patterns**:
- <a href="{{ '/rag/development/lwc-patterns.html' | relative_url }}">LWC Patterns</a> - LWC development patterns and best practices
- <a href="{{ '/rag/code-examples/lwc/code-examples/api-reference/lds-api-reference.html' | relative_url }}">LDS API Reference</a> - Lightning Data Service API reference
- <a href="{{ '/rag/code-examples/lwc/code-examples/mcp-knowledge/lds-patterns.html' | relative_url }}">LDS Patterns</a> - Lightning Data Service patterns

## Examples

### Example 1: Basic Wire with getRecord

**Pattern**: Reactive record data access
**Use Case**: Displaying record data that updates automatically
**Complexity**: Basic
**Related Patterns**: [LWC Data Access Patterns](../development/lwc-patterns.html#data-access-patterns)

**Problem**:
You need to display record data that automatically updates when the record changes.

**Solution**:

**JavaScript** (`contactDisplay.js`):
```javascript
import { LightningElement, api, wire } from 'lwc';
import { getRecord, getFieldValue } from 'lightning/uiRecordApi';
import CONTACT_NAME_FIELD from '@salesforce/schema/Contact.Name';
import CONTACT_EMAIL_FIELD from '@salesforce/schema/Contact.Email';
import CONTACT_PHONE_FIELD from '@salesforce/schema/Contact.Phone';
import CONTACT_ACCOUNT_FIELD from '@salesforce/schema/Contact.AccountId';

const FIELDS = [
    CONTACT_NAME_FIELD,
    CONTACT_EMAIL_FIELD,
    CONTACT_PHONE_FIELD,
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

    get accountId() {
        return getFieldValue(this.contact.data, CONTACT_ACCOUNT_FIELD);
    }

    get hasData() {
        return this.contact && this.contact.data;
    }

    get hasError() {
        return this.contact && this.contact.error;
    }
}
```

**HTML** (`contactDisplay.html`):
```html
<template>
    <lightning-card title="Contact Information" icon-name="standard:contact">
        <div class="slds-p-around_medium">
            <template if:true={hasData}>
                <dl class="slds-list_horizontal slds-wrap">
                    <dt class="slds-item_label slds-text-color_weak">Name:</dt>
                    <dd class="slds-item_detail">{name}</dd>
                    <dt class="slds-item_label slds-text-color_weak">Email:</dt>
                    <dd class="slds-item_detail">{email}</dd>
                    <dt class="slds-item_label slds-text-color_weak">Phone:</dt>
                    <dd class="slds-item_detail">{phone}</dd>
                </dl>
            </template>
            <template if:true={hasError}>
                <div class="slds-text-color_error">
                    Error loading contact: {contact.error.body.message}
                </div>
            </template>
        </div>
    </lightning-card>
</template>
```

**Explanation**:
- Uses `@wire(getRecord)` for reactive data access
- Automatically updates when record changes
- Uses `getFieldValue` helper for safe field access
- Handles loading and error states

**Best Practices**:
- Use `@wire` for reactive data that should update automatically
- Always handle loading and error states
- Use `getFieldValue` helper for safe field access
- Import field references from `@salesforce/schema`

### Example 2: Wire with Relationship Queries

**Pattern**: Accessing related record data
**Use Case**: Displaying data from parent or child records
**Complexity**: Intermediate
**Related Patterns**: [LWC Data Access Patterns](../development/lwc-patterns.html#data-access-patterns)

**Problem**:
You need to display data from related records (parent or child objects).

**Solution**:

**JavaScript** (`contactWithAccount.js`):
```javascript
import { LightningElement, api, wire } from 'lwc';
import { getRecord, getFieldValue } from 'lightning/uiRecordApi';
import CONTACT_NAME_FIELD from '@salesforce/schema/Contact.Name';
import CONTACT_ACCOUNT_FIELD from '@salesforce/schema/Contact.AccountId';
import ACCOUNT_NAME_FIELD from '@salesforce/schema/Account.Name';
import ACCOUNT_INDUSTRY_FIELD from '@salesforce/schema/Account.Industry';

const CONTACT_FIELDS = [CONTACT_NAME_FIELD, CONTACT_ACCOUNT_FIELD];
const ACCOUNT_FIELDS = [ACCOUNT_NAME_FIELD, ACCOUNT_INDUSTRY_FIELD];

export default class ContactWithAccount extends LightningElement {
    @api recordId;
    accountId;

    @wire(getRecord, { recordId: '$recordId', fields: CONTACT_FIELDS })
    wiredContact({ data, error }) {
        if (data) {
            this.accountId = getFieldValue(data, CONTACT_ACCOUNT_FIELD);
        } else if (error) {
            console.error('Error loading contact:', error);
        }
    }

    @wire(getRecord, { recordId: '$accountId', fields: ACCOUNT_FIELDS })
    account;

    get contactName() {
        return this.wiredContact?.data ? 
            getFieldValue(this.wiredContact.data, CONTACT_NAME_FIELD) : '';
    }

    get accountName() {
        return getFieldValue(this.account?.data, ACCOUNT_NAME_FIELD);
    }

    get accountIndustry() {
        return getFieldValue(this.account?.data, ACCOUNT_INDUSTRY_FIELD);
    }
}
```

**HTML** (`contactWithAccount.html`):
```html
<template>
    <lightning-card title="Contact and Account">
        <div class="slds-p-around_medium">
            <div class="slds-text-heading_small slds-m-bottom_small">
                Contact: {contactName}
            </div>
            <template if:true={account.data}>
                <div class="slds-m-top_medium">
                    <div class="slds-text-body_regular">
                        <strong>Account:</strong> {accountName}
                    </div>
                    <div class="slds-text-body_regular">
                        <strong>Industry:</strong> {accountIndustry}
                    </div>
                </div>
            </template>
        </div>
    </lightning-card>
</template>
```

**Explanation**:
- Uses multiple wire adapters for related data
- First wire gets contact, second wire gets account based on contact's account ID
- Handles reactive updates when either record changes
- Uses optional chaining for safe property access

**Best Practices**:
- Chain wire adapters when accessing related records
- Use optional chaining to prevent null reference errors
- Handle loading states for each wire adapter separately

### Example 3: Wire with Apex Method

**Pattern**: Reactive Apex method calls
**Use Case**: Calling Apex methods that return data reactively
**Complexity**: Intermediate
**Related Patterns**: <a href="{{ '/rag/development/lwc-patterns.html' | relative_url }}">LWC Patterns</a>

**Problem**:
You need to call an Apex method and have the data update reactively when parameters change.

**Solution**:

**Apex** (`ContactService.cls`):
```apex
public with sharing class ContactService {
    @AuraEnabled(cacheable=true)
    public static List<Contact> getContactsByAccount(Id accountId) {
        return [
            SELECT Id, Name, Email, Phone
            FROM Contact
            WHERE AccountId = :accountId
            WITH SECURITY_ENFORCED
            ORDER BY Name
        ];
    }
}
```

**JavaScript** (`accountContacts.js`):
```javascript
import { LightningElement, api, wire } from 'lwc';
import getContactsByAccount from '@salesforce/apex/ContactService.getContactsByAccount';
import { getRecord, getFieldValue } from 'lightning/uiRecordApi';
import ACCOUNT_NAME_FIELD from '@salesforce/schema/Account.Name';

export default class AccountContacts extends LightningElement {
    @api recordId;
    accountName;

    @wire(getRecord, { recordId: '$recordId', fields: [ACCOUNT_NAME_FIELD] })
    wiredAccount({ data, error }) {
        if (data) {
            this.accountName = getFieldValue(data, ACCOUNT_NAME_FIELD);
        }
    }

    @wire(getContactsByAccount, { accountId: '$recordId' })
    contacts({ data, error }) {
        if (data) {
            console.log('Contacts loaded:', data);
        } else if (error) {
            console.error('Error loading contacts:', error);
        }
    }

    get hasContacts() {
        return this.contacts && this.contacts.data && this.contacts.data.length > 0;
    }

    get contactsList() {
        return this.contacts?.data || [];
    }
}
```

**HTML** (`accountContacts.html`):
```html
<template>
    <lightning-card title="Contacts for {accountName}">
        <div class="slds-p-around_medium">
            <template if:true={hasContacts}>
                <template for:each={contactsList} for:item="contact">
                    <div key={contact.Id} class="slds-m-bottom_small">
                        <div class="slds-text-heading_small">{contact.Name}</div>
                        <div class="slds-text-body_regular slds-text-color_weak">
                            {contact.Email} | {contact.Phone}
                        </div>
                    </div>
                </template>
            </template>
            <template if:false={hasContacts}>
                <div class="slds-text-body_regular">
                    No contacts found for this account.
                </div>
            </template>
        </div>
    </lightning-card>
</template>
```

**Explanation**:
- Uses `@wire` with Apex method for reactive data access
- Apex method must be `@AuraEnabled(cacheable=true)` for wire
- Automatically re-executes when reactive parameters change
- Handles loading and error states

**Best Practices**:
- Use `cacheable=true` for Apex methods used with `@wire`
- Use reactive parameters (prefixed with `$`) for automatic updates
- Handle loading and error states
- Use `WITH SECURITY_ENFORCED` in Apex queries

### Example 4: Wire with getObjectInfo

**Pattern**: Accessing object metadata
**Use Case**: Getting field labels, picklist values, or object metadata
**Complexity**: Intermediate
**Related Patterns**: <a href="{{ '/rag/development/lwc-patterns.html' | relative_url }}">LWC Patterns</a>

**Problem**:
You need to access object metadata like field labels or picklist values.

**Solution**:

**JavaScript** (`dynamicForm.js`):
```javascript
import { LightningElement, api, wire } from 'lwc';
import { getObjectInfo } from 'lightning/uiObjectInfoApi';
import CONTACT_OBJECT from '@salesforce/schema/Contact';

export default class DynamicForm extends LightningElement {
    @api recordId;

    @wire(getObjectInfo, { objectApiName: CONTACT_OBJECT })
    objectInfo;

    get fields() {
        if (!this.objectInfo?.data) {
            return [];
        }

        const fieldMap = this.objectInfo.data.fields;
        const fieldList = [];

        // Get specific fields
        const fieldNames = ['Name', 'Email', 'Phone', 'Title'];
        
        fieldNames.forEach(fieldName => {
            if (fieldMap[fieldName]) {
                fieldList.push({
                    apiName: fieldName,
                    label: fieldMap[fieldName].label,
                    type: fieldMap[fieldName].dataType,
                    required: !fieldMap[fieldName].updateable || fieldMap[fieldName].required
                });
            }
        });

        return fieldList;
    }

    get picklistValues() {
        if (!this.objectInfo?.data) {
            return {};
        }

        const fieldMap = this.objectInfo.data.fields;
        const picklistMap = {};

        Object.keys(fieldMap).forEach(fieldName => {
            const field = fieldMap[fieldName];
            if (field.dataType === 'Picklist' && field.picklistValues) {
                picklistMap[fieldName] = field.picklistValues.map(pv => ({
                    label: pv.label,
                    value: pv.value
                }));
            }
        });

        return picklistMap;
    }
}
```

**Explanation**:
- Uses `getObjectInfo` to access object metadata
- Retrieves field labels, types, and picklist values
- Enables dynamic form generation
- Handles metadata loading states

**Best Practices**:
- Use `getObjectInfo` for dynamic UI generation
- Cache metadata when possible
- Handle loading states for metadata
- Use field metadata for validation and formatting

## Related Examples

- <a href="{{ '/rag/code-examples/lwc/code-examples/lwc/component-examples.html' | relative_url }}">Component Examples</a> - LWC component implementations
- <a href="{{ '/rag/code-examples/lwc/code-examples/lwc/service-examples.html' | relative_url }}">Service Examples</a> - LWC service layer patterns
- <a href="{{ '/rag/code-examples/lwc/code-examples/apex/service-layer-examples.html' | relative_url }}">Apex Service Layer Examples</a> - Apex service methods

## See Also

- <a href="{{ '/rag/development/lwc-patterns.html' | relative_url }}">LWC Patterns</a> - Complete LWC development patterns
- <a href="{{ '/rag/code-examples/lwc/code-examples/api-reference/lds-api-reference.html' | relative_url }}">LDS API Reference</a> - Lightning Data Service API reference
- <a href="{{ '/rag/code-examples/lwc/code-examples/mcp-knowledge/lds-patterns.html' | relative_url }}">LDS Patterns</a> - Lightning Data Service patterns
- <a href="{{ '/rag/code-examples/lwc/code-examples/api-reference/lwc-api-reference.html' | relative_url }}">LWC API Reference</a> - Complete LWC API reference
