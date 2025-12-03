---
layout: default
title: LWC Data Attribute Patterns
description: Patterns for using data-* attributes in Lightning Web Components to pass context, IDs, and metadata into event handlers
permalink: /rag/development/lwc-data-attributes-patterns.html
---

## What Was Actually Done

- Used `data-*` attributes on HTML elements in LWCs to carry record IDs, indexes, and contextual flags into event handlers.
- Standardized attribute naming (e.g., `data-record-id`, `data-index`, `data-action`) to keep templates readable.
- Parsed dataset values in handlers instead of binding inline functions, avoiding performance and readability issues.

## Patterns

### Pattern 1: Record Id on Button

**Template**:
```html
<template for:each={records} for:item="record">
    <lightning-button
        key={record.Id}
        data-record-id={record.Id}
        label="View"
        variant="brand-outline"
        onclick={handleViewClick}>
    </lightning-button>
</template>
```

**Controller**:
```js
handleViewClick(event) {
    const recordId = event.currentTarget.dataset.recordId;
    // Use recordId to navigate or fire event
}
```

### Pattern 2: Row Index and Action

**Template**:
```html
<template for:each={rows} for:item="row" for:index="index">
    <tr key={row.id}>
        <td>{row.name}</td>
        <td>
            <button
                data-index={index}
                data-action="edit"
                onclick={handleRowAction}>
                Edit
            </button>
            <button
                data-index={index}
                data-action="delete"
                onclick={handleRowAction}>
                Delete
            </button>
        </td>
    </tr>
</template>
```

**Controller**:
```js
handleRowAction(event) {
    const index = Number(event.currentTarget.dataset.index);
    const action = event.currentTarget.dataset.action;
    const row = this.rows[index];
    // Branch on action and operate on row
}
```

## To Validate

- Ensure data attribute naming is consistent across LWCs (e.g., `data-record-id`, not mixed styles).
- Confirm handlers always use `event.currentTarget`, not `event.target`, for reliable dataset access.


