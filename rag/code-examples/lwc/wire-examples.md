---
layout: default
title: LWC Wire Service Code Examples
description: Wire services provide reactive data access in Lightning Web Components
permalink: /rag/development/lwc-patterns.html' | relative_url }}">LWC Patterns</a>

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

- <a href="{{ '/rag/development/lwc-patterns.html' | relative_url }}">LWC Patterns</a> - Complete LWC development patterns
- <a href="{{ '/rag/api-reference/lds-api-reference.html' | relative_url }}">LDS API Reference</a> - Lightning Data Service API reference
- <a href="{{ '/rag/mcp-knowledge/lds-patterns.html' | relative_url }}">LDS Patterns</a> - Lightning Data Service patterns
- <a href="{{ '/rag/api-reference/lwc-api-reference.html' | relative_url }}">LWC API Reference</a> - Complete LWC API reference
