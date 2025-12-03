---
layout: default
title: LWC List View Button Examples
description: Examples for adding custom LWC-powered buttons to list views
permalink: /rag/code-examples/lwc/list-view-button-examples.html
---

## Scenario

Expose an LWC as a list view button that operates on selected records using the `lightning__ListView` page type.

## Example: List View Action LWC

**Controller**:
```js
import { LightningElement, wire } from 'lwc';
import { CurrentPageReference } from 'lightning/navigation';

export default class ListViewActionExample extends LightningElement {
    selectedRecordIds = [];

    @wire(CurrentPageReference)
    getStateParameters(currentPageReference) {
        if (currentPageReference?.state?.selectedIds) {
            this.selectedRecordIds = currentPageReference.state.selectedIds.split(',');
        }
    }
}
```

## To Validate

- Confirm the component is exposed with `lightning__ListView` in its metadata.
- Ensure limits are respected when processing many selected records.


