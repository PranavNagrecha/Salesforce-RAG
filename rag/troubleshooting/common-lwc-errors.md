---
layout: default
title: Common LWC Errors and Solutions
description: This guide provides solutions for common LWC errors encountered during Salesforce development, including error messages, causes, solutions, and prevention strategies
permalink: /rag/troubleshooting/common-lwc-errors.html

## Cannot read property 'value' of undefined

**Error Message**: `Cannot read property 'value' of undefined` (JavaScript console)

**Common Causes**:
- Accessing field value before data is loaded
- Wire adapter hasn't returned data yet
- Field doesn't exist in query result
- Null/undefined record data

**Solutions**:

### Solution 1: Check Data Before Access

**Before: No null check**
```javascript
@wire(getRecord, { recordId: '$recordId' })
wiredRecord;

get contactName() {
    return this.wiredRecord.data.fields.Name.value; // Fails if data is undefined
}
```

**After: With null check**
```javascript
@wire(getRecord, { recordId: '$recordId' })
wiredRecord;

get contactName() {
    return this.wiredRecord.data?.fields?.Name?.value || '';
}

// Or in template
// {wiredRecord.data?.fields?.Name?.value}
```

### Solution 2: Handle Wire Function

**Before: Direct property access**
```javascript
@wire(getRecord, { recordId: '$recordId' })
wiredRecord;

connectedCallback() {
    this.name = this.wiredRecord.data.fields.Name.value; // Fails
}
```

**After: Wire function**
```javascript
@wire(getRecord, { recordId: '$recordId' })
wiredRecord({ data, error }) {
    if (data) {
        this.name = data.fields.Name.value;
    } else if (error) {
        this.error = this.reduceErrors(error);
    }
}
```

**Prevention**:
- Always use optional chaining (`?.`) when accessing wire data
- Handle both `data` and `error` in wire functions
- Check for null/undefined before accessing nested properties
- Use loading states to prevent access before data loads

**Related Patterns**: <a href="{{ '/rag/development/lwc-patterns.html' | relative_url }}">LWC Patterns</a>, <a href="{{ '/rag/mcp-knowledge/lds-patterns.html' | relative_url }}">LDS Patterns</a>

---

## LWC1503: Invalid property

**Error Message**: `LWC1503: Invalid property "propertyName" of element <c-my-component>`

**Common Causes**:
- Property not decorated with `@api`
- Property name doesn't match HTML attribute (case sensitivity)
- Property not exposed in component

**Solutions**:

### Solution 1: Add @api Decorator

**Before: Missing @api**
```javascript
export default class MyComponent extends LightningElement {
    recordId; // Not accessible from parent
}
```

**After: With @api**
```javascript
import { LightningElement, api } from 'lwc';

export default class MyComponent extends LightningElement {
    @api recordId; // Now accessible from parent
}
```

### Solution 2: Match HTML Attribute Case

**Before: Case mismatch**
```javascript
@api recordId; // camelCase in JS
```

```html
<!-- HTML: kebab-case -->
<c-my-component record-id="003000000000001"></c-my-component>
```

**After: Correct usage**
```html
<!-- HTML attribute matches JS property (kebab-case) -->
<c-my-component record-id="003000000000001"></c-my-component>
```

**Prevention**:
- Always use `@api` for properties exposed to parent components
- Use camelCase in JavaScript, kebab-case in HTML
- Verify property names match between JS and HTML

**Related Patterns**: <a href="{{ '/rag/mcp-knowledge/lwc-best-practices.html#property-and-attribute-naming' | relative_url }}">LWC Best Practices</a>

---

## LWC1009: Invalid event name

**Error Message**: `LWC1009: Invalid event name. Event name must start with a lowercase letter`

**Common Causes**:
- Event name uses camelCase or uppercase
- Event name starts with uppercase letter
- Event name doesn't follow lowercase convention

**Solutions**:

### Solution 1: Use Lowercase Event Names

**Before: CamelCase event name**
```javascript
const event = new CustomEvent('recordUpdate', { // Invalid
    detail: { recordId: this.recordId }
});
```

**After: Lowercase event name**
```javascript
const event = new CustomEvent('recordupdate', { // Valid
    detail: { recordId: this.recordId }
});
```

### Solution 2: HTML Event Handler

**Before: CamelCase in HTML**
```html
<template>
    <lightning-button onrecordupdate={handleUpdate}></lightning-button>
</template>
```

**After: Lowercase in HTML**
```html
<template>
    <lightning-button onrecordupdate={handleUpdate}></lightning-button>
</template>
```

**Prevention**:
- Always use lowercase for event names
- Event names in JavaScript: lowercase
- Event handlers in HTML: `on` + lowercase event name
- Follow LWC naming conventions strictly

**Related Patterns**: <a href="{{ '/rag/mcp-knowledge/lwc-best-practices.html#custom-events' | relative_url }}">LWC Best Practices</a>

---

## LWC1010: Invalid @wire target

**Error Message**: `LWC1010: Invalid @wire target. @wire can only be applied to a property or a method`

**Common Causes**:
- @wire applied incorrectly
- @wire on wrong target
- Syntax error in @wire usage

**Solutions**:

### Solution 1: Correct @wire on Property

**Before: Incorrect usage**
```javascript
@wire(getRecord, { recordId: '$recordId' })
wiredRecord() { // Method - incorrect for simple wire
    // ...
}
```

**After: Property wire**
```javascript
@wire(getRecord, { recordId: '$recordId' })
wiredRecord; // Property - correct
```

### Solution 2: Correct @wire on Method

**Before: Missing method**
```javascript
@wire(getRecord, { recordId: '$recordId' })
// Missing method or property
```

**After: Wire function**
```javascript
@wire(getRecord, { recordId: '$recordId' })
wiredRecord({ data, error }) { // Method - correct for wire function
    if (data) {
        this.record = data;
    }
}
```

**Prevention**:
- Use property for simple wire: `@wire(adapter) propertyName;`
- Use method for wire function: `@wire(adapter) methodName({ data, error }) {}`
- Don't mix patterns incorrectly

**Related Patterns**: <a href="{{ '/rag/api-reference/lwc-api-reference.html#wire' | relative_url }}">LWC API Reference</a>, <a href="{{ '/rag/mcp-knowledge/lds-patterns.html' | relative_url }}">LDS Patterns</a>

---

## LWC1007: Multiple templates found

**Error Message**: `LWC1007: Multiple templates found. A component can only have one template`

**Common Causes**:
- Multiple HTML files in component folder
- Incorrect template structure
- Missing render() method for multiple templates

**Solutions**:

### Solution 1: Single Template (Preferred)

**Before: Multiple templates without render()**
```
myComponent/
├── myComponent.js
├── myComponent.html
└── myComponentAlt.html // Error: multiple templates
```

**After: Single template**
```
myComponent/
├── myComponent.js
└── myComponent.html // Single template
```

### Solution 2: Multiple Templates with render()

**Before: Missing render()**
```javascript
import templateOne from './templateOne.html';
import templateTwo from './templateTwo.html';

export default class MyComponent extends LightningElement {
    // Missing render() method
}
```

**After: With render()**
```javascript
import { LightningElement } from 'lwc';
import templateOne from './templateOne.html';
import templateTwo from './templateTwo.html';

export default class MyComponent extends LightningElement {
    showTemplateTwo = false;
    
    render() {
        return this.showTemplateTwo ? templateTwo : templateOne;
    }
}
```

**Prevention**:
- Use single template when possible
- Implement `render()` method for multiple templates
- Return template reference, not string

**Related Patterns**: <a href="{{ '/rag/mcp-knowledge/lwc-best-practices.html#multiple-templates' | relative_url }}">LWC Best Practices</a>

---

## TypeError: Cannot read property 'dispatchEvent' of undefined

**Error Message**: `TypeError: Cannot read property 'dispatchEvent' of undefined`

**Common Causes**:
- Calling `dispatchEvent` outside component context
- `this` context lost in callback
- Arrow function vs regular function context

**Solutions**:

### Solution 1: Preserve 'this' Context

**Before: Lost context**
```javascript
handleClick() {
    setTimeout(function() {
        this.dispatchEvent(new CustomEvent('update')); // 'this' is undefined
    }, 1000);
}
```

**After: Arrow function**
```javascript
handleClick() {
    setTimeout(() => {
        this.dispatchEvent(new CustomEvent('update')); // 'this' preserved
    }, 1000);
}
```

### Solution 2: Store Reference

**Before: Context issue**
```javascript
connectedCallback() {
    this.template.addEventListener('click', this.handleClick); // Context lost
}

handleClick() {
    this.dispatchEvent(new CustomEvent('update')); // 'this' undefined
}
```

**After: Bound method**
```javascript
connectedCallback() {
    this.handleClick = this.handleClick.bind(this);
    this.template.addEventListener('click', this.handleClick);
}

handleClick() {
    this.dispatchEvent(new CustomEvent('update')); // Works
}
```

**Prevention**:
- Use arrow functions to preserve `this` context
- Bind methods when passing as callbacks
- Avoid using `this` in unbound callbacks

**Related Patterns**: <a href="{{ '/rag/mcp-knowledge/lwc-best-practices.html' | relative_url }}">LWC Best Practices</a>

---

## Wire adapter error: Invalid parameter

**Error Message**: `Wire adapter error: Invalid parameter "recordId"`

**Common Causes**:
- Parameter not reactive (missing `$` prefix)
- Parameter type mismatch
- Parameter value is null/undefined when required

**Solutions**:

### Solution 1: Use Reactive Parameters

**Before: Not reactive**
```javascript
@wire(getRecord, { recordId: this.recordId }) // Not reactive
wiredRecord;
```

**After: Reactive with $**
```javascript
@wire(getRecord, { recordId: '$recordId' }) // Reactive
wiredRecord;
```

### Solution 2: Handle Null Parameters

**Before: Null parameter**
```javascript
@api recordId; // May be null initially

@wire(getRecord, { recordId: '$recordId' })
wiredRecord; // Fails if recordId is null
```

**After: Conditional wire**
```javascript
@api recordId;

get hasRecordId() {
    return this.recordId != null;
}

@wire(getRecord, { 
    recordId: '$recordId' 
})
wiredRecord({ data, error }) {
    if (this.hasRecordId && data) {
        this.record = data;
    }
}
```

**Prevention**:
- Always use `$` prefix for reactive parameters
- Check for null/undefined before wiring
- Validate parameter types
- Handle parameter changes properly

**Related Patterns**: <a href="{{ '/rag/mcp-knowledge/lds-patterns.html' | relative_url }}">LDS Patterns</a>, <a href="{{ '/rag/api-reference/lwc-api-reference.html' | relative_url }}">LWC API Reference</a>

---

## INVALID_FIELD_FOR_INSERT_UPDATE: Unable to create/update fields

**Error Message**: `INVALID_FIELD_FOR_INSERT_UPDATE: Unable to create/update fields: [FieldName]`

**Common Causes**:
- Field not added to page layout (most common cause)
- Field-Level Security (FLS) permissions not granted
- Field accessibility settings restrict access
- Profile or Permission Set doesn't have field access
- Field not included in object's field-level security settings

**Solutions**:

### Solution 1: Add Field to Page Layout (CRITICAL STEP)

**Most Important**: Even if a field has proper FLS permissions, it must be added to the page layout for `lightning-record-edit-form` to work.

**Before: Field missing from layout**
```
Field has FLS permissions ✓
Field has object permissions ✓
Field NOT on page layout ✗
Result: Error "Unable to create/update fields"
```

**After: Field added to layout**
```
Field has FLS permissions ✓
Field has object permissions ✓
Field on page layout ✓
Result: Field works correctly
```

**Steps to Fix**:
1. Go to **Setup** → **Object Manager** → Select your object
2. Click **Page Layouts**
3. Edit the page layout used by your component
4. Add the field to the layout (even if hidden or in a collapsed section)
5. Save the layout
6. Test the component again

**Note**: The field doesn't need to be visible on the layout - it just needs to be present. You can place it in a collapsed section or hide it if needed.

### Solution 2: Check Field-Level Security Permissions

**Before: Missing FLS permissions**
```apex
// User doesn't have read/edit access to field
// Component tries to update field
// Error: Unable to create/update fields
```

**After: Grant FLS permissions**
1. Go to **Setup** → **Object Manager** → Select your object
2. Click **Fields & Relationships** → Select the field
3. Click **Set Field-Level Security**
4. Grant **Read** and **Edit** access to appropriate Profiles or Permission Sets
5. Save

**Verification**:
- Check Profile: **Setup** → **Profiles** → Select profile → **Field-Level Security** → Verify field access
- Check Permission Set: **Setup** → **Permission Sets** → Select permission set → **Field Permissions** → Verify field access

### Solution 3: Verify Field Accessibility Settings

**Check Field Accessibility**:
1. Go to **Setup** → **Object Manager** → Select your object
2. Click **Fields & Relationships** → Select the field
3. Check **Field Accessibility** section
4. Ensure field is accessible (not restricted by object settings)

**Common Issues**:
- Field marked as "Required" but user doesn't have access
- Field restricted by object-level security
- Field not available for the record type

### Solution 4: Check Profile and Permission Set Permissions

**Verify Object Permissions**:
1. **Object Access**: Profile/Permission Set must have **Read** and **Edit** access to the object
2. **Field Access**: Profile/Permission Set must have **Read** and **Edit** access to the field
3. **Record Type Access**: If using record types, verify record type access

**Checklist**:
- [ ] Profile/Permission Set has object-level **Read** access
- [ ] Profile/Permission Set has object-level **Edit** access
- [ ] Profile/Permission Set has field-level **Read** access
- [ ] Profile/Permission Set has field-level **Edit** access
- [ ] Field is on the page layout (CRITICAL)
- [ ] Field accessibility is not restricted

### Solution 5: Complete Troubleshooting Checklist

**Step-by-Step Resolution**:

1. **Add Field to Page Layout** (MOST IMPORTANT)
   - Edit the page layout used by your component
   - Add the field to the layout
   - Save the layout

2. **Check Field-Level Security**
   - Verify field has Read and Edit permissions
   - Check both Profile and Permission Set permissions
   - Grant access if missing

3. **Verify Object Permissions**
   - Check object-level Read and Edit access
   - Verify record type access if applicable

4. **Check Field Accessibility**
   - Verify field is not restricted by object settings
   - Check field is available for the record type

5. **Test with Different Users**
   - Test with user who has full access (System Admin)
   - Test with user who has limited access
   - Compare results to identify permission gaps

**Prevention**:
- **Always add fields to page layouts** when using `lightning-record-edit-form`
- **Set FLS permissions** as part of field creation process
- **Document field requirements** in deployment checklists
- **Test with appropriate user profiles** before deployment
- **Include page layout updates** in deployment packages

**Common Scenario**:
A field has proper FLS permissions and object access, but the component still fails with "Unable to create/update fields". The issue is that the field is not on the page layout. Adding the field to the layout (even in a collapsed section) resolves the issue immediately.

**Related Patterns**: 
- <a href="{{ '/rag/development/error-handling-and-logging.html' | relative_url }}">Error Handling</a> - Error handling patterns
- <a href="{{ '/rag/troubleshooting/lwc-accessibility-errors.html' | relative_url }}">LWC Accessibility Errors</a> - Accessibility-specific errors