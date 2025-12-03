---
layout: default
title: LWC Word Document Generation Examples
description: Examples for generating Word documents from Lightning Web Components using Apex and external services
permalink: /rag/code-examples/lwc/word-document-generation-examples.html
---

## Scenario

Generate a Word document (DOCX) from Salesforce data by calling Apex from LWC, which then calls an external document generation service.

## Example: LWC Invoking Apex for DOCX

**Controller**:
```js
import { LightningElement, api } from 'lwc';
import generateDoc from '@salesforce/apex/DocxService.generateDocument';

export default class DocxGenerator extends LightningElement {
    @api recordId;

    async handleGenerateDoc() {
        await generateDoc({ recordId: this.recordId });
    }
}
```

## To Validate

- Confirm the chosen document generation engine and authentication mechanism.
- Ensure generated documents are stored in Files with appropriate sharing.


