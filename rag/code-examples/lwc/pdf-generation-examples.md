---
layout: default
title: LWC PDF Generation Examples
description: Examples for generating PDFs from Lightning Web Components using Apex and external services
permalink: /rag/code-examples/lwc/pdf-generation-examples.html
---

## Scenario

Generate a PDF document from LWC data by invoking Apex that renders a template and calls a PDF engine.

## Example: LWC Invoking Apex for PDF

**Template**:
```html
<template>
    <lightning-button
        label="Generate PDF"
        variant="brand"
        onclick={handleGeneratePdf}>
    </lightning-button>
</template>
```

**Controller**:
```js
import { LightningElement, api } from 'lwc';
import generatePdf from '@salesforce/apex/PdfService.generatePdf';

export default class PdfGenerator extends LightningElement {
    @api recordId;

    async handleGeneratePdf() {
        await generatePdf({ recordId: this.recordId });
        // Optionally show toast or navigate to file
    }
}
```

## To Validate

- Confirm the org’s PDF generation approach (Visualforce, external service, or third-party package).
- Ensure Apex respects governor limits when generating PDFs in bulk.


