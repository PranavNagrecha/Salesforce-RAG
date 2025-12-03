# Lightning Data Service (LDS) Patterns - MCP Knowledge

> This file contains knowledge extracted from Salesforce MCP Service tools.  
> It complements the lived-experience patterns in `rag/development/` and `rag/patterns/`.

## Overview

Guidelines for building, reviewing, and maintaining Lightning Web Components that interact with Salesforce's Lightning Data Service, focusing on data consistency, referential integrity, and choosing UIAPI vs Apex.

**Source**: Salesforce MCP Service - `mcp_salesforce_guide_lds_development`, `mcp_salesforce_guide_lds_data_consistency`, `mcp_salesforce_guide_lds_referential_integrity`

## Core Principles

### Data Consistency
- Keep UI in sync with server-side data
- Use `refreshApex` or `notifyRecordUpdateAvailable` after mutations
- Refresh LDS cache when Apex mutates data

### Referential Integrity
- Import object and field references from `@salesforce/schema`
- Use constants instead of string literals
- Protects against metadata changes and refactors

### Choosing UIAPI vs Apex
- Prefer **LDS/UIAPI** for CRUD on standard and custom objects
- Use **Apex** only when business logic or bulk operations exceed LDS capabilities
- Favor base components for simple record UIs

## Recommended Solutions for Common Pitfalls

| Pitfall | Correct Approach |
| --- | --- |
| Overusing Apex instead of LDS | Replace simple SOQL Apex calls with UIAPI wire adaptors (`getRecord`, `getObjectInfo`, etc.) or base record form components |
| Stale Data due to Caching | After any record mutation call `refreshApex(wiredResult)` **or** `notifyRecordUpdateAvailable([{recordId}])` |
| Mixing Apex & LDS without Sync | Whenever Apex mutates data also refresh the LDS cache, e.g., call `refreshApex` on wired results or publish `notifyRecordUpdateAvailable` |
| Hand-rolling simple forms | Use `lightning-record-form`, `lightning-record-edit-form`, or `lightning-record-view-form` which provide built-in validation and SLDS styling |
| Not importing schema references | `import NAME_FIELD from '@salesforce/schema/Account.Name'` and use constants instead of string literals like `'Name'` |

## Review Checklist

### 1. Hand-Rolling Forms Instead of Using Base Components
- Does the component implement a custom form for single-record CRUD where base record form components would suffice?
- Is there validation logic that duplicates what base record form components provide natively?
- Are standard SLDS styles recreated manually instead of leveraging the styling baked into base components?

### 2. Not Importing References to Salesforce Objects and Fields
- Are object or field API names referenced as hard-coded strings rather than constants imported from `@salesforce/schema`?
- In the template, are field values accessed directly via expressions like `record.data.fields.Name.value` without schema imports?
- Does the JavaScript file lack any `@salesforce/schema` import even though the component interacts with Salesforce fields?

### 3. Mixing Apex Calls with LDS Without Synchronization
- Does the component read data via LDS and mutate the same record through Apex without a subsequent cache refresh?
- Does it fetch data through Apex yet rely on LDS cache for display without synchronizing after updates?
- Are multiple data sources (Apex imperatively and LDS declaratively) touching the same object without an explicit refresh strategy?

### 4. Overusing Apex Instead of LDS
- Does the component call Apex solely to retrieve or update a single record that `getRecord`, `updateRecord`, or a base record form could handle?
- Is Apex used just to run a simple SOQL query whose fields are available through standard LDS wire adaptors?
- Are custom Apex methods present for basic CRUD while no LDS/UIAPI calls appear in the code?

## Best Practices

### Schema Imports
```javascript
// Good: Import schema references
import NAME_FIELD from '@salesforce/schema/Account.Name';
import ACCOUNT_OBJECT from '@salesforce/schema/Account';

// Bad: Hard-coded strings
const fieldName = 'Name';
const objectName = 'Account';
```

### Data Refresh
```javascript
// After Apex mutation, refresh LDS cache
import { refreshApex } from '@salesforce/apex';

@wire(getRecord, { recordId: '$recordId' })
wiredRecord;

async handleUpdate() {
    await updateRecord({ fields: { Id: this.recordId, Name: 'New Name' } });
    // Refresh the wired result
    await refreshApex(this.wiredRecord);
}
```

### Base Components
- Use `lightning-record-form` for create/edit forms
- Use `lightning-record-edit-form` for edit-only forms
- Use `lightning-record-view-form` for read-only forms
- These provide built-in validation, SLDS styling, and field-level security

## Integration with Existing RAG

**Related Patterns**:
- [LWC Patterns](../development/lwc-patterns.html) - LWC component patterns
- [Apex Patterns](../development/apex-patterns.html) - When to use Apex vs LDS
- [SOQL Patterns](../development/soql-query-patterns.html) - Query patterns

**How This Complements Existing RAG**:
- Provides official guidance on LDS usage
- Validates when to use LDS vs Apex
- Emphasizes schema imports for referential integrity
- Adds data consistency patterns

