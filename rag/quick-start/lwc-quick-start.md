---
title: "LWC Quick Start Guide"
level: "Beginner"
tags:
  - quick-start
  - lwc
  - lightning-web-components
  - getting-started
last_reviewed: "2025-01-XX"
---

# LWC Quick Start Guide

> Getting started with Lightning Web Components development in Salesforce.

## Overview

This quick-start guide provides step-by-step instructions for creating your first Lightning Web Component following best practices.

## Prerequisites

- Salesforce Developer Edition or Sandbox
- VS Code with Salesforce Extensions
- Basic understanding of JavaScript and HTML

## Step 1: Create Your First Component

### What is an LWC?

A Lightning Web Component is a reusable UI component built with modern web standards.

### Implementation

1. **Create Component Folder**: `force-app/main/default/lwc/contactViewer/`

2. **Create JavaScript File** (`contactViewer.js`):

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

3. **Create HTML Template** (`contactViewer.html`):

```html
<template>
    <lightning-card title="Contact Details">
        <template lwc:if={contactName}>
            <div class="slds-p-around_small">
                <p><strong>Name:</strong> {contactName}</p>
                <p><strong>Email:</strong> {contactEmail}</p>
            </div>
        </template>
        <template lwc:elseif={error}>
            <div class="slds-text-color_error">
                Error: {error}
            </div>
        </template>
        <template lwc:else>
            <div class="slds-p-around_small">
                Loading...
            </div>
        </template>
    </lightning-card>
</template>
```

4. **Create Meta XML** (`contactViewer.js-meta.xml`):

```xml
<?xml version="1.0" encoding="UTF-8"?>
<LightningComponentBundle xmlns="http://soap.sforce.com/2006/04/metadata">
    <apiVersion>60.0</apiVersion>
    <isExposed>true</isExposed>
    <targets>
        <target>lightning__RecordPage</target>
    </targets>
    <targetConfigs>
        <targetConfig targets="lightning__RecordPage">
            <property name="recordId" type="String" />
        </targetConfig>
    </targetConfigs>
</LightningComponentBundle>
```

---

## Step 2: Add Interactivity

### Add Button and Event Handling

1. **Update HTML**:

```html
<template>
    <lightning-card title="Contact Details">
        <template lwc:if={contactName}>
            <div class="slds-p-around_small">
                <p><strong>Name:</strong> {contactName}</p>
                <p><strong>Email:</strong> {contactEmail}</p>
                <lightning-button 
                    label="Update Contact" 
                    onclick={handleUpdate}
                    class="slds-m-top_small">
                </lightning-button>
            </div>
        </template>
    </lightning-card>
</template>
```

2. **Update JavaScript**:

```javascript
import { LightningElement, wire, api } from 'lwc';
import { getRecord, updateRecord } from 'lightning/uiRecordApi';
import { ShowToastEvent } from 'lightning/platformShowToastEvent';
import NAME_FIELD from '@salesforce/schema/Contact.Name';
import EMAIL_FIELD from '@salesforce/schema/Contact.Email';

export default class ContactViewer extends LightningElement {
    @api recordId;
    
    @wire(getRecord, { 
        recordId: '$recordId', 
        fields: [NAME_FIELD, EMAIL_FIELD] 
    })
    wiredRecord;
    
    handleUpdate() {
        const fields = {
            Id: this.recordId,
            [EMAIL_FIELD.fieldApiName]: 'updated@example.com'
        };
        
        updateRecord({ fields })
            .then(() => {
                this.showToast('Success', 'Contact updated', 'success');
            })
            .catch(error => {
                this.showToast('Error', this.reduceErrors(error), 'error');
            });
    }
    
    showToast(title, message, variant) {
        const evt = new ShowToastEvent({
            title: title,
            message: message,
            variant: variant
        });
        this.dispatchEvent(evt);
    }
    
    reduceErrors(errors) {
        if (Array.isArray(errors)) {
            return errors.map(error => error.message).join(', ');
        }
        return errors.message || 'An unexpected error occurred';
    }
}
```

---

## Step 3: Deploy and Test

### Deploy to Org

1. **Right-click** on component folder in VS Code
2. **Select** "SFDX: Deploy Source to Org"
3. **Verify** deployment succeeds

### Add to Record Page

1. **Open** Lightning App Builder
2. **Edit** a Contact record page
3. **Drag** `contactViewer` component onto page
4. **Save** and activate

---

## Complete Example

Here's a complete working example:

### JavaScript (`contactViewer.js`)
```javascript
import { LightningElement, wire, api } from 'lwc';
import { getRecord } from 'lightning/uiRecordApi';
import NAME_FIELD from '@salesforce/schema/Contact.Name';
import EMAIL_FIELD from '@salesforce/schema/Contact.Email';

export default class ContactViewer extends LightningElement {
    @api recordId;
    contactName;
    contactEmail;
    error;
    
    @wire(getRecord, { 
        recordId: '$recordId', 
        fields: [NAME_FIELD, EMAIL_FIELD] 
    })
    wiredRecord({ data, error }) {
        if (data) {
            this.contactName = data.fields.Name.value;
            this.contactEmail = data.fields.Email.value;
            this.error = undefined;
        } else if (error) {
            this.error = this.reduceErrors(error);
            this.contactName = undefined;
            this.contactEmail = undefined;
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

### HTML (`contactViewer.html`)
```html
<template>
    <lightning-card title="Contact Details">
        <template lwc:if={contactName}>
            <div class="slds-p-around_small">
                <p><strong>Name:</strong> {contactName}</p>
                <p><strong>Email:</strong> {contactEmail}</p>
            </div>
        </template>
        <template lwc:elseif={error}>
            <div class="slds-text-color_error slds-p-around_small">
                Error: {error}
            </div>
        </template>
        <template lwc:else>
            <div class="slds-p-around_small">
                Loading...
            </div>
        </template>
    </lightning-card>
</template>
```

---

## Next Steps

1. **Learn More Patterns**:
   - <a href="{{ '/rag/quick-start/development/lwc-patterns.html' | relative_url }}">LWC Patterns</a> - Complete LWC patterns
   - <a href="{{ '/rag/quick-start/mcp-knowledge/lwc-best-practices.html' | relative_url }}">LWC Best Practices</a> - Best practices
   - <a href="{{ '/rag/quick-start/mcp-knowledge/lds-patterns.html' | relative_url }}">LDS Patterns</a> - Data service patterns

2. **Explore Examples**:
   - <a href="{{ '/rag/quick-start/api-reference/lwc-api-reference.html' | relative_url }}">LWC API Reference</a> - API reference
   - <a href="{{ '/rag/quick-start/api-reference/lds-api-reference.html' | relative_url }}">LDS API Reference</a> - LDS reference

3. **Understand Best Practices**:
   - <a href="{{ '/rag/quick-start/mcp-knowledge/lwc-accessibility.html' | relative_url }}">LWC Accessibility</a> - Accessibility
   - <a href="{{ '/rag/quick-start/mcp-knowledge/design-system-patterns.html' | relative_url }}">Design System Patterns</a> - SLDS patterns

---

## Related Resources

- <a href="{{ '/rag/quick-start/development/lwc-patterns.html' | relative_url }}">LWC Patterns</a> - Complete LWC patterns
- <a href="{{ '/rag/quick-start/mcp-knowledge/lwc-best-practices.html' | relative_url }}">LWC Best Practices</a> - Best practices
- <a href="{{ '/rag/quick-start/api-reference/lwc-api-reference.html' | relative_url }}">LWC API Reference</a> - API reference

