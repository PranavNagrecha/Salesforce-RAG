# Common LWC Errors and Solutions

> Troubleshooting guide for common Lightning Web Component errors with solutions and prevention strategies.

## Overview

This guide provides solutions for common LWC errors encountered during Salesforce development, including error messages, causes, solutions, and prevention strategies.

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

**Related Patterns**: [LWC Patterns](../development/lwc-patterns.md), [LDS Patterns](../mcp-knowledge/lds-patterns.md)

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

**Related Patterns**: [LWC Best Practices](rag/mcp-knowledge/lwc-best-practices.md#property-and-attribute-naming)

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

**Related Patterns**: [LWC Best Practices](rag/mcp-knowledge/lwc-best-practices.md#custom-events)

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

**Related Patterns**: [LWC API Reference](rag/api-reference/lwc-api-reference.md#wire), [LDS Patterns](../mcp-knowledge/lds-patterns.md)

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

**Related Patterns**: [LWC Best Practices](rag/mcp-knowledge/lwc-best-practices.md#multiple-templates)

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

**Related Patterns**: [LWC Best Practices](../mcp-knowledge/lwc-best-practices.md)

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

**Related Patterns**: [LDS Patterns](../mcp-knowledge/lds-patterns.md), [LWC API Reference](../api-reference/lwc-api-reference.md)

---

## Related Patterns

- [LWC Patterns](../development/lwc-patterns.md) - Complete LWC patterns
- [LWC Best Practices](../mcp-knowledge/lwc-best-practices.md) - LWC best practices
- [LDS Patterns](../mcp-knowledge/lds-patterns.md) - Lightning Data Service patterns
- [Error Handling](../development/error-handling-and-logging.md) - Error handling patterns

