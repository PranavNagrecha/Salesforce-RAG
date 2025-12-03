# LWC Wire Service Code Examples

> This file contains complete, working code examples for Lightning Web Component wire service patterns.
> All examples demonstrate reactive data access using @wire decorator.

## Overview

Wire services provide reactive data access in Lightning Web Components. They automatically update when parameters change and handle loading and error states.

**Related Patterns**:
- [LWC Patterns](../development/lwc-patterns.md) - LWC development patterns
- [LDS API Reference](../api-reference/lds-api-reference.md) - Lightning Data Service API

## Examples

### Example 1: Basic Wire to getRecord

**Pattern**: Reactive record data access
**Use Case**: Displaying record data that updates automatically
**Complexity**: Basic
**Related Patterns**: [LWC Data Access Patterns](../development/lwc-patterns.md#data-access-patterns)

**Problem**:
You need to display record data that updates when the record changes.

**Solution**:

**JavaScript** (`recordDisplay.js`):
```javascript
import { LightningElement, api, wire } from 'lwc';
import { getRecord } from 'lightning/uiRecordApi';
import ACCOUNT_NAME_FIELD from '@salesforce/schema/Account.Name';
import ACCOUNT_INDUSTRY_FIELD from '@salesforce/schema/Account.Industry';

const FIELDS = [ACCOUNT_NAME_FIELD, ACCOUNT_INDUSTRY_FIELD];

export default class RecordDisplay extends LightningElement {
    @api recordId;

    @wire(getRecord, { recordId: '$recordId', fields: FIELDS })
    account;

    get accountName() {
        return this.account?.data?.fields?.Name?.value || '';
    }

    get accountIndustry() {
        return this.account?.data?.fields?.Industry?.value || '';
    }

    get isLoading() {
        return !this.account?.data && !this.account?.error;
    }
}
```

**HTML** (`recordDisplay.html`):
```html
<template>
    <template if:true={isLoading}>
        <lightning-spinner></lightning-spinner>
    </template>
    
    <template if:true={account.data}>
        <lightning-card title="Account Information">
            <div class="slds-p-around_medium">
                <p>Name: {accountName}</p>
                <p>Industry: {accountIndustry}</p>
            </div>
        </lightning-card>
    </template>
    
    <template if:true={account.error}>
        <div class="slds-text-color_error">
            Error: {account.error.body.message}
        </div>
    </template>
</template>
```

**Explanation**:
- `@wire` automatically provides data when `recordId` changes
- Uses optional chaining for safe property access
- Handles loading, data, and error states
- Reactive - updates automatically when record changes

**Best Practices**:
- Always handle loading and error states
- Use optional chaining to prevent null reference errors
- Import field references from `@salesforce/schema`
- Use reactive parameters (prefixed with `$`) for automatic updates

### Example 2: Wire to getObjectInfo

**Pattern**: Reactive object metadata access
**Use Case**: Getting object information for dynamic forms
**Complexity**: Intermediate
**Related Patterns**: [LWC Patterns](../development/lwc-patterns.md)

**Problem**:
You need to get object metadata to build dynamic forms or validate field access.

**Solution**:

**JavaScript** (`objectInfo.js`):
```javascript
import { LightningElement, wire } from 'lwc';
import { getObjectInfo } from 'lightning/uiObjectInfoApi';
import ACCOUNT_OBJECT from '@salesforce/schema/Account';

export default class ObjectInfo extends LightningElement {
    @wire(getObjectInfo, { objectApiName: ACCOUNT_OBJECT })
    objectInfo;

    get objectLabel() {
        return this.objectInfo?.data?.label || '';
    }

    get objectLabelPlural() {
        return this.objectInfo?.data?.labelPlural || '';
    }

    get fields() {
        return this.objectInfo?.data?.fields || {};
    }

    get fieldList() {
        return Object.keys(this.fields).map(key => ({
            apiName: key,
            label: this.fields[key].label
        }));
    }
}
```

**HTML** (`objectInfo.html`):
```html
<template>
    <template if:true={objectInfo.data}>
        <lightning-card title="Object Information">
            <div class="slds-p-around_medium">
                <p>Label: {objectLabel}</p>
                <p>Plural Label: {objectLabelPlural}</p>
                <p>Fields: {fieldList.length}</p>
            </div>
        </lightning-card>
    </template>
</template>
```

**Explanation**:
- Gets object metadata reactively
- Can be used to build dynamic forms
- Provides field information for validation
- Updates automatically when object metadata changes

**Best Practices**:
- Use for dynamic form generation
- Cache object info when used multiple times
- Handle loading states appropriately

### Example 3: Wire to getPicklistValues

**Pattern**: Reactive picklist values access
**Use Case**: Getting picklist values for dropdowns
**Complexity**: Intermediate
**Related Patterns**: [LWC Patterns](../development/lwc-patterns.md)

**Problem**:
You need to get picklist values for a dropdown that updates when record type changes.

**Solution**:

**JavaScript** (`picklistValues.js`):
```javascript
import { LightningElement, api, wire } from 'lwc';
import { getPicklistValues } from 'lightning/uiObjectInfoApi';
import ACCOUNT_INDUSTRY_FIELD from '@salesforce/schema/Account.Industry';

export default class PicklistValues extends LightningElement {
    @api recordTypeId;

    @wire(getPicklistValues, {
        recordTypeId: '$recordTypeId',
        fieldApiName: ACCOUNT_INDUSTRY_FIELD
    })
    industryOptions;

    get options() {
        if (!this.industryOptions?.data?.values) {
            return [];
        }
        
        return this.industryOptions.data.values.map(value => ({
            label: value.label,
            value: value.value
        }));
    }
}
```

**HTML** (`picklistValues.html`):
```html
<template>
    <lightning-card title="Industry Selection">
        <div class="slds-p-around_medium">
            <lightning-combobox
                label="Industry"
                options={options}
                value={selectedValue}
                onchange={handleChange}>
            </lightning-combobox>
        </div>
    </lightning-card>
</template>
```

**Explanation**:
- Gets picklist values reactively based on record type
- Updates automatically when record type changes
- Provides values for dropdown components
- Handles record type-specific picklist values

**Best Practices**:
- Use reactive parameters for record type
- Transform wire data to component-friendly format
- Handle cases where picklist values aren't available

### Example 4: Wire to Apex Method

**Pattern**: Reactive Apex method calls
**Use Case**: Getting data from Apex that should update automatically
**Complexity**: Intermediate
**Related Patterns**: [LWC Patterns](../development/lwc-patterns.md), [Apex Patterns](../development/apex-patterns.md)

**Problem**:
You need to call an Apex method reactively when parameters change.

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
            LIMIT 100
        ];
    }
}
```

**JavaScript** (`contactList.js`):
```javascript
import { LightningElement, api, wire } from 'lwc';
import getContactsByAccount from '@salesforce/apex/ContactService.getContactsByAccount';

export default class ContactList extends LightningElement {
    @api recordId;

    @wire(getContactsByAccount, { accountId: '$recordId' })
    contacts;

    get contactList() {
        return this.contacts?.data || [];
    }

    get hasContacts() {
        return this.contactList.length > 0;
    }

    get isLoading() {
        return !this.contacts?.data && !this.contacts?.error;
    }
}
```

**HTML** (`contactList.html`):
```html
<template>
    <lightning-card title="Contacts">
        <template if:true={isLoading}>
            <lightning-spinner></lightning-spinner>
        </template>
        
        <template if:true={hasContacts}>
            <ul class="slds-list_dotted">
                <template for:each={contactList} for:item="contact">
                    <li key={contact.Id}>
                        {contact.Name} - {contact.Email}
                    </li>
                </template>
            </ul>
        </template>
        
        <template if:true={contacts.error}>
            <div class="slds-text-color_error">
                Error loading contacts
            </div>
        </template>
    </lightning-card>
</template>
```

**Explanation**:
- Uses `@wire` with Apex method for reactive data
- Apex method must be `@AuraEnabled(cacheable=true)`
- Updates automatically when `recordId` changes
- Handles loading and error states

**Best Practices**:
- Use `cacheable=true` for wire-able Apex methods
- Use reactive parameters (prefixed with `$`) for automatic updates
- Always handle loading and error states
- Use `WITH SECURITY_ENFORCED` in Apex queries

## Related Examples

- [Component Examples](lwc/component-examples.md) - Complete LWC component examples
- [Service Examples](lwc/service-examples.md) - LWC service layer patterns
- [Apex Service Layer Examples](apex/service-layer-examples.md) - Server-side service patterns

## See Also

- [LWC Patterns](../development/lwc-patterns.md) - Complete LWC development patterns
- [LDS API Reference](../api-reference/lds-api-reference.md) - Lightning Data Service API reference
- [LWC API Reference](../api-reference/lwc-api-reference.md) - LWC API reference

