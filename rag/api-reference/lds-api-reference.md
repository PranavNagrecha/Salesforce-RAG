---
title: "Lightning Data Service (LDS) API Reference"
level: "Intermediate"
tags:
  - api-reference
  - lds
  - lightning-data-service
  - reference
  - wire-adapters
last_reviewed: "2025-01-XX"
---

# Lightning Data Service (LDS) API Reference

> Quick reference for Lightning Data Service wire adapters and methods.

## Overview

This reference provides API signatures, parameters, and usage examples for Lightning Data Service adapters used in Lightning Web Components.

## Record Access

### getRecord

**Purpose**: Retrieve a single record with specified fields

**Module**: `lightning/uiRecordApi`

**Signature**: `@wire(getRecord, { recordId: '$recordId', fields: fields })`

**Parameters**: 
- `recordId` (String): Record ID (reactive with `$` prefix)
- `fields` (Array): Array of field API names or schema imports

**Returns**: `{ data, error }`: Object with:
- `data`: Record data with fields accessible via `data.fields.FieldName.value`
- `error`: Error object if query fails

**Description**: Retrieves a single record with specified fields. Automatically caches and updates. Respects field-level security.

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
            this.contactName = data.fields.Name.value;
            this.contactEmail = data.fields.Email.value;
        } else if (error) {
            this.error = this.reduceErrors(error);
        }
    }
    
    reduceErrors(errors) {
        if (Array.isArray(errors)) {
            return errors.map(error => error.message).join(', ');
        }
        return errors.message || 'An unexpected error occurred';
    }
}
```

**Related Patterns**: [LDS Patterns](/rag/mcp-knowledge/lds-patterns.html), [LWC API Reference](/rag/api-reference/lwc-api-reference.html)

**Best Practices**:
- Use schema imports instead of string literals
- Always handle both `data` and `error`
- Use `refreshApex()` after mutations
- Access fields via `data.fields.FieldName.value`

---

### getRecords

**Purpose**: Retrieve multiple records by IDs

**Module**: `lightning/uiRecordApi`

**Signature**: `@wire(getRecords, { recordIds: '$recordIds', fields: fields })`

**Parameters**: 
- `recordIds` (Array<String>): Array of record IDs (reactive with `$` prefix)
- `fields` (Array): Array of field API names or schema imports

**Returns**: `{ data, error }`: Object with:
- `data`: Object with `records` array containing record data
- `error`: Error object if query fails

**Example**:
```javascript
import { getRecords } from 'lightning/uiRecordApi';
import NAME_FIELD from '@salesforce/schema/Contact.Name';

@wire(getRecords, {
    recordIds: '$contactIds',
    fields: [NAME_FIELD]
})
wiredContacts({ data, error }) {
    if (data) {
        this.contacts = data.records;
    }
}
```

---

## Record Mutations

### updateRecord

**Purpose**: Update a single record

**Module**: `lightning/uiRecordApi`

**Signature**: `updateRecord({ fields })`

**Parameters**: 
- `fields` (Object): Object with `Id` and fields to update

**Returns**: `Promise<void>`

**Description**: Updates a record. Must refresh cache after update using `refreshApex()`.

**Example**:
```javascript
import { updateRecord } from 'lightning/uiRecordApi';
import { refreshApex } from '@salesforce/apex';
import NAME_FIELD from '@salesforce/schema/Contact.Name';

async handleUpdate() {
    const fields = {
        Id: this.recordId,
        [NAME_FIELD.fieldApiName]: 'Updated Name'
    };
    try {
        await updateRecord({ fields });
        await refreshApex(this.wiredRecord);
        this.showToast('Success', 'Record updated', 'success');
    } catch (error) {
        this.showToast('Error', this.reduceErrors(error), 'error');
    }
}
```

**Best Practices**:
- Always refresh cache after update
- Use schema imports for field references
- Handle errors with try-catch
- Provide user feedback (toast notifications)

---

### createRecord

**Purpose**: Create a new record

**Module**: `lightning/uiRecordApi`

**Signature**: `createRecord({ apiName, fields })`

**Parameters**: 
- `apiName` (String): API name of the object
- `fields` (Object): Object with fields to set

**Returns**: `Promise<Record>`: Promise resolving to created record

**Example**:
```javascript
import { createRecord } from 'lightning/uiRecordApi';
import CONTACT_OBJECT from '@salesforce/schema/Contact';
import NAME_FIELD from '@salesforce/schema/Contact.Name';
import EMAIL_FIELD from '@salesforce/schema/Contact.Email';

async handleCreate() {
    const fields = {
        [NAME_FIELD.fieldApiName]: 'New Contact',
        [EMAIL_FIELD.fieldApiName]: 'new@example.com'
    };
    try {
        const record = await createRecord({
            apiName: CONTACT_OBJECT.objectApiName,
            fields
        });
        this.showToast('Success', 'Record created', 'success');
        // Navigate to new record
        this[NavigationMixin.Navigate]({
            type: 'standard__recordPage',
            attributes: {
                recordId: record.id,
                actionName: 'view'
            }
        });
    } catch (error) {
        this.showToast('Error', this.reduceErrors(error), 'error');
    }
}
```

---

### deleteRecord

**Purpose**: Delete a record

**Module**: `lightning/uiRecordApi`

**Signature**: `deleteRecord(recordId)`

**Parameters**: 
- `recordId` (String): ID of record to delete

**Returns**: `Promise<void>`

**Example**:
```javascript
import { deleteRecord } from 'lightning/uiRecordApi';

async handleDelete() {
    try {
        await deleteRecord(this.recordId);
        this.showToast('Success', 'Record deleted', 'success');
    } catch (error) {
        this.showToast('Error', this.reduceErrors(error), 'error');
    }
}
```

---

## Object Metadata

### getObjectInfo

**Purpose**: Retrieve object metadata

**Module**: `lightning/uiObjectInfoApi`

**Signature**: `@wire(getObjectInfo, { objectApiName: objectApiName })`

**Parameters**: 
- `objectApiName` (String): API name of the object (use schema import)

**Returns**: `{ data, error }`: Object with:
- `data`: Object metadata including fields, record types, layouts
- `error`: Error object if query fails

**Example**:
```javascript
import { getObjectInfo } from 'lightning/uiObjectInfoApi';
import ACCOUNT_OBJECT from '@salesforce/schema/Account';

@wire(getObjectInfo, { objectApiName: ACCOUNT_OBJECT })
wiredObjectInfo({ data, error }) {
    if (data) {
        this.objectInfo = data;
        this.fields = data.fields;
        this.recordTypes = data.recordTypeInfos;
    }
}
```

---

### getObjectInfos

**Purpose**: Retrieve metadata for multiple objects

**Module**: `lightning/uiObjectInfoApi`

**Signature**: `@wire(getObjectInfos, { objectApiNames: objectApiNames })`

**Parameters**: 
- `objectApiNames` (Array<String>): Array of object API names

**Returns**: `{ data, error }`: Object with metadata for all requested objects

---

## List Views

### getListUi

**Purpose**: Retrieve list view data

**Module**: `lightning/uiListApi`

**Signature**: `@wire(getListUi, { objectApiName: objectApiName, listViewApiName: listViewApiName })`

**Parameters**: 
- `objectApiName` (String): API name of the object
- `listViewApiName` (String): API name of the list view

**Returns**: `{ data, error }`: Object with list view data

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

---

## Cache Management

### refreshApex

**Purpose**: Refresh cached wire adapter result

**Module**: `@salesforce/apex`

**Signature**: `refreshApex(wiredResult)`

**Parameters**: 
- `wiredResult` (Object): The result object from a `@wire` adapter

**Returns**: `Promise<void>`

**Description**: Refreshes the cached result of a wire adapter. Use after mutations to keep UI in sync.

**Example**:
```javascript
import { refreshApex } from '@salesforce/apex';

@wire(getRecord, { recordId: '$recordId' })
wiredRecord;

async handleUpdate() {
    await updateRecord({ fields: { Id: this.recordId, Name: 'New Name' } });
    await refreshApex(this.wiredRecord);
}
```

**Best Practices**:
- Always refresh after mutations
- Use with both LDS and Apex wire adapters
- Handle errors from refresh operation

---

### notifyRecordUpdateAvailable

**Purpose**: Notify LDS cache that a record has been updated

**Module**: `lightning/uiRecordApi`

**Signature**: `notifyRecordUpdateAvailable(recordInputs)`

**Parameters**: 
- `recordInputs` (Array<Object>): Array of objects with `recordId` property

**Returns**: `Promise<void>`

**Description**: Notifies LDS cache that records have been updated externally (e.g., by Apex). Alternative to `refreshApex()`.

**Example**:
```javascript
import { notifyRecordUpdateAvailable } from 'lightning/uiRecordApi';

async handleApexUpdate() {
    // Update via Apex
    await updateContactViaApex({ recordId: this.recordId });
    
    // Notify LDS cache
    await notifyRecordUpdateAvailable([{ recordId: this.recordId }]);
}
```

**Best Practices**:
- Use when Apex mutates data that LDS is displaying
- Prefer over `refreshApex()` for external updates
- Can notify multiple records at once

---

## Related Patterns

- [LDS Patterns](/rag/mcp-knowledge/lds-patterns.html) - Complete LDS guidance
- [LWC API Reference](/rag/api-reference/lwc-api-reference.html) - LWC module reference
- [LWC Patterns](/rag/development/lwc-patterns.html) - LWC component patterns

