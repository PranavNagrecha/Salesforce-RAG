---
title: "LWC API Reference"
level: "Intermediate"
tags:
  - api-reference
  - lwc
  - lightning-web-components
  - reference
  - methods
last_reviewed: "2025-01-XX"
---

# LWC API Reference

> Quick reference for Lightning Web Component modules, decorators, and wire adapters.

## Overview

This reference provides API signatures, parameters, and usage examples for common LWC modules and patterns.

## Core Modules

### lightning/platformShowToastEvent

**Purpose**: Display toast notifications to users

#### Methods

##### showToastEvent(options)
**Signature**: `dispatchEvent(new ShowToastEvent(options))`

**Parameters**: 
- `options` (Object): Configuration object with properties:
  - `title` (String): Toast title
  - `message` (String): Toast message
  - `variant` (String): 'success', 'error', 'warning', 'info'
  - `mode` (String): 'dismissable', 'pester', 'sticky'

**Returns**: `void` (dispatches event)

**Description**: Displays a toast notification to the user.

**Example**:
```javascript
import { ShowToastEvent } from 'lightning/platformShowToastEvent';

handleSuccess() {
    const evt = new ShowToastEvent({
        title: 'Success',
        message: 'Record updated successfully',
        variant: 'success',
        mode: 'dismissable'
    });
    this.dispatchEvent(evt);
}
```

**Related Patterns**: <a href="{{ '/rag/development/lwc-patterns.html' | relative_url }}">LWC Patterns</a>, <a href="{{ '/rag/api-reference/mcp-knowledge/design-system-patterns.html' | relative_url }}">Design System Patterns</a>

---

### lightning/navigation

**Purpose**: Navigate to pages, records, and URLs

#### Methods

##### NavigationMixin.Navigate(options)
**Signature**: `this<a href="{{ '/rag/api-reference/options.html' | relative_url }}">NavigationMixin.Navigate</a>`

**Parameters**: 
- `options` (Object): Navigation configuration:
  - `type` (String): 'standard__recordPage', 'standard__webPage', etc.
  - `attributes` (Object): Page-specific attributes (recordId, objectApiName, etc.)

**Returns**: `Promise<void>`

**Description**: Navigates to a Salesforce page or external URL.

**Example**:
```javascript
import { NavigationMixin } from 'lightning/navigation';

export default class MyComponent extends NavigationMixin(LightningElement) {
    handleNavigate() {
        this[NavigationMixin.Navigate]({
            type: 'standard__recordPage',
            attributes: {
                recordId: this.recordId,
                objectApiName: 'Contact',
                actionName: 'view'
            }
        });
    }
}
```

**Related Patterns**: <a href="{{ '/rag/development/lwc-patterns.html' | relative_url }}">LWC Patterns</a>

---

## Lightning Data Service (LDS)

### lightning/uiRecordApi

**Purpose**: Access Salesforce records via Lightning Data Service

#### Wire Adapters

##### getRecord(recordId, fields)
**Signature**: `@wire(getRecord, { recordId: '$recordId', fields: fields })`

**Parameters**: 
- `recordId` (String): Record ID (reactive with `$` prefix)
- `fields` (Array): Array of field API names or schema imports

**Returns**: `{ data, error }`: Object with record data or error

**Description**: Retrieves a single record with specified fields. Automatically caches and updates.

**Example**:
```javascript
import { LightningElement, wire, api } from 'lwc';
import { getRecord } from 'lightning/uiRecordApi';
import NAME_FIELD from '@salesforce/schema/Contact.Name';
import EMAIL_FIELD from '@salesforce/schema/Contact.Email';

export default class ContactViewer extends LightningElement {
    @api recordId;
    
    @wire(getRecord, { 
        recordId: '$recordId', 
        fields: [NAME_FIELD, EMAIL_FIELD] 
    })
    wiredRecord({ data, error }) {
        if (data) {
            this.contact = data;
        } else if (error) {
            this.error = this.reduceErrors(error);
        }
    }
}
```

##### updateRecord(fields)
**Signature**: `updateRecord({ fields })`

**Parameters**: 
- `fields` (Object): Object with Id and fields to update

**Returns**: `Promise<void>`

**Description**: Updates a record. Must refresh cache after update.

**Example**:
```javascript
import { updateRecord } from 'lightning/uiRecordApi';
import { refreshApex } from '@salesforce/apex';

async handleUpdate() {
    const fields = {
        Id: this.recordId,
        Name: 'Updated Name'
    };
    await updateRecord({ fields });
    await refreshApex(this.wiredRecord);
}
```

##### getObjectInfo(objectApiName)
**Signature**: `@wire(getObjectInfo, { objectApiName: objectApiName })`

**Parameters**: 
- `objectApiName` (String): API name of the object

**Returns**: `{ data, error }`: Object with object metadata or error

**Description**: Retrieves object metadata including fields, record types, and layouts.

**Example**:
```javascript
import { getObjectInfo } from 'lightning/uiObjectInfoApi';
import ACCOUNT_OBJECT from '@salesforce/schema/Account';

@wire(getObjectInfo, { objectApiName: ACCOUNT_OBJECT })
wiredObjectInfo({ data, error }) {
    if (data) {
        this.objectInfo = data;
    }
}
```

**Related Patterns**: <a href="{{ '/rag/api-reference/mcp-knowledge/lds-patterns.html' | relative_url }}">LDS Patterns</a>, <a href="{{ '/rag/development/lwc-patterns.html' | relative_url }}">LWC Patterns</a>

---

### lightning/uiListApi

**Purpose**: Query and access lists of records

#### Wire Adapters

##### getListUi(objectApiName, listViewApiName)
**Signature**: `@wire(getListUi, { objectApiName: objectApiName, listViewApiName: listViewApiName })`

**Parameters**: 
- `objectApiName` (String): API name of the object
- `listViewApiName` (String): API name of the list view

**Returns**: `{ data, error }`: Object with list data or error

**Description**: Retrieves list view data for an object.

**Example**:
```javascript
import { getListUi } from 'lightning/uiListApi';
import ACCOUNT_OBJECT from '@salesforce/schema/Account';

@wire(getListUi, {
    objectApiName: ACCOUNT_OBJECT,
    listViewApiName: 'AllAccounts'
})
wiredAccounts({ data, error }) {
    if (data) {
        this.accounts = data.records.records;
    }
}
```

**Related Patterns**: <a href="{{ '/rag/api-reference/mcp-knowledge/lds-patterns.html' | relative_url }}">LDS Patterns</a>

---

## Lightning Message Service

### lightning/messageService

**Purpose**: Cross-component communication without parent-child relationship

#### Methods

##### publish(messageContext, messageChannel, messagePayload)
**Signature**: `publish(messageContext, messageChannel, messagePayload)`

**Parameters**: 
- `messageContext` (MessageContext): Message context from `@wire(MessageContext)` or `createMessageContext()`
- `messageChannel` (Object): Message channel import
- `messagePayload` (Object): JSON object with message data (no functions or symbols)

**Returns**: `void`

**Description**: Publishes a message to subscribers on the message channel.

**Example**:
```javascript
import { publish, MessageContext } from 'lightning/messageService';
import CHANNEL_NAME from '@salesforce/messageChannel/MyChannel__c';

@wire(MessageContext)
messageContext;

handlePublish() {
    const payload = { recordId: this.recordId, action: 'update' };
    publish(this.messageContext, CHANNEL_NAME, payload);
}
```

##### subscribe(messageContext, messageChannel, listener, subscriberOptions)
**Signature**: `subscribe(messageContext, messageChannel, listener, subscriberOptions)`

**Parameters**: 
- `messageContext` (MessageContext): Message context
- `messageChannel` (Object): Message channel import
- `listener` (Function): Function to handle received messages
- `subscriberOptions` (Object, optional): `{ scope: APPLICATION_SCOPE }` for cross-app communication

**Returns**: `Subscription` (object to unsubscribe)

**Description**: Subscribes to messages on a message channel. Must be called in `connectedCallback()`.

**Example**:
```javascript
import { subscribe, MessageContext, APPLICATION_SCOPE } from 'lightning/messageService';
import CHANNEL_NAME from '@salesforce/messageChannel/MyChannel__c';

@wire(MessageContext)
messageContext;

connectedCallback() {
    this.subscription = subscribe(
        this.messageContext,
        CHANNEL_NAME,
        (message) => this.handleMessage(message),
        { scope: APPLICATION_SCOPE }
    );
}

disconnectedCallback() {
    if (this.subscription) {
        unsubscribe(this.subscription);
    }
}
```

**Related Patterns**: <a href="{{ '/rag/api-reference/mcp-knowledge/lwc-best-practices.html' | relative_url }}">LWC Best Practices</a>

---

## Schema Imports

### @salesforce/schema

**Purpose**: Import object and field references for referential integrity

#### Usage

**Import Object**:
```javascript
import ACCOUNT_OBJECT from '@salesforce/schema/Account';
```

**Import Field**:
```javascript
import NAME_FIELD from '@salesforce/schema/Account.Name';
import EMAIL_FIELD from '@salesforce/schema/Contact.Email';
```

**Example**:
```javascript
import { LightningElement, wire, api } from 'lwc';
import { getRecord } from 'lightning/uiRecordApi';
import ACCOUNT_OBJECT from '@salesforce/schema/Account';
import NAME_FIELD from '@salesforce/schema/Account.Name';

export default class AccountViewer extends LightningElement {
    @api recordId;
    
    @wire(getRecord, {
        recordId: '$recordId',
        fields: [NAME_FIELD]
    })
    wiredAccount;
}
```

**Related Patterns**: <a href="{{ '/rag/api-reference/mcp-knowledge/lds-patterns.html' | relative_url }}">LDS Patterns</a>, <a href="{{ '/rag/api-reference/Salesforce-RAG/rag/mcp-knowledge/lds-patterns.html#referential-integrity.html' | relative_url }}">Referential Integrity</a>

---

## Decorators

### @api

**Purpose**: Expose public properties and methods for external access

**Usage**:
```javascript
import { LightningElement, api } from 'lwc';

export default class MyComponent extends LightningElement {
    @api recordId;
    @api title;
    
    @api
    get computedValue() {
        return this.recordId + ' - ' + this.title;
    }
    
    @api
    handleAction() {
        // Public method
    }
}
```

**Best Practices**:
- Only use on properties/methods intended for external access
- Only one decorator per field or method
- For getters/setters: Decorate only the getter
- Do not mutate @api properties internally

**Related Patterns**: <a href="{{ '/rag/api-reference/Salesforce-RAG/rag/mcp-knowledge/lwc-best-practices.html#decorators.html' | relative_url }}">LWC Best Practices</a>

---

### @wire

**Purpose**: Reactive data access from Lightning Data Service or Apex

**Usage**:
```javascript
import { LightningElement, wire, api } from 'lwc';
import { getRecord } from 'lightning/uiRecordApi';
import getContactData from '@salesforce/apex/ContactService.getContactData';

export default class MyComponent extends LightningElement {
    @api recordId;
    
    // Wire to LDS
    @wire(getRecord, { recordId: '$recordId' })
    wiredRecord;
    
    // Wire to Apex
    @wire(getContactData, { contactId: '$recordId' })
    wiredContactData({ data, error }) {
        if (data) {
            this.contact = data;
        } else if (error) {
            this.error = error;
        }
    }
}
```

**Best Practices**:
- Use `$` prefix for reactive parameters
- Handle both `data` and `error` in wire functions
- Use `refreshApex()` after mutations

**Related Patterns**: <a href="{{ '/rag/api-reference/mcp-knowledge/lds-patterns.html' | relative_url }}">LDS Patterns</a>, <a href="{{ '/rag/development/lwc-patterns.html' | relative_url }}">LWC Patterns</a>

---

### @track

**Purpose**: Track changes to object/array properties (not needed for primitives)

**Usage**:
```javascript
import { LightningElement, track } from 'lwc';

export default class MyComponent extends LightningElement {
    // Not needed for primitives
    message = 'Hello';
    
    // Needed when mutating nested properties
    @track complexObject = {
        nested: { value: 0 }
    };
    
    handleClick() {
        // This mutation requires @track
        this.complexObject.nested.value++;
    }
}
```

**Best Practices**:
- Only necessary for complex types when mutating properties
- Not needed for primitives (strings, numbers, booleans)
- Not needed when entire object/array is reassigned

**Related Patterns**: <a href="{{ '/rag/api-reference/Salesforce-RAG/rag/mcp-knowledge/lwc-best-practices.html#track-decorator.html' | relative_url }}">LWC Best Practices</a>

---

## Related Patterns

- <a href="{{ '/rag/development/lwc-patterns.html' | relative_url }}">LWC Patterns</a> - Complete LWC patterns
- <a href="{{ '/rag/api-reference/mcp-knowledge/lwc-best-practices.html' | relative_url }}">LWC Best Practices</a> - LWC best practices
- <a href="{{ '/rag/api-reference/mcp-knowledge/lds-patterns.html' | relative_url }}">LDS Patterns</a> - Lightning Data Service patterns
- <a href="{{ '/rag/api-reference/mcp-knowledge/design-system-patterns.html' | relative_url }}">Design System Patterns</a> - SLDS patterns

