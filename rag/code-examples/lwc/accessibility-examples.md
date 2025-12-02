# LWC Accessibility Code Examples

> This file contains complete, working code examples for Lightning Web Component accessibility patterns.
> All examples are copy-paste ready and follow WCAG 2.2 standards and Salesforce best practices.

## Overview

Accessibility in Lightning Web Components ensures that all users, including those using assistive technologies, can access and interact with your components. These examples demonstrate practical implementation of accessibility patterns.

**Related Patterns**:
- [LWC Accessibility Guidelines](../../mcp-knowledge/lwc-accessibility.md) - WCAG 2.2 compliance guidance
- [LWC Patterns](../../development/lwc-patterns.md) - General LWC patterns
- [Design System Patterns](../../mcp-knowledge/design-system-patterns.md) - SLDS accessibility

## Form Accessibility Examples

### Example 1: Accessible Form with Proper Labels

**Pattern**: Form with programmatically associated labels
**Use Case**: Contact form with accessible inputs
**WCAG Criteria**: SC 1.3.1 (iii) - Info and Relationships, SC 4.1.2 (i) - Name
**Complexity**: Basic

**Problem**:
Form inputs need programmatically associated labels for screen readers and keyboard navigation.

**Solution**:

**HTML** (`contactForm.html`):
```html
<template>
    <lightning-card title="Contact Form" icon-name="standard:contact">
        <div class="slds-p-around_medium">
            <form onsubmit={handleSubmit}>
                <div class="slds-form-element">
                    <lightning-input
                        label="First Name"
                        name="firstName"
                        value={firstName}
                        onchange={handleInputChange}
                        required
                        autocomplete="given-name"
                        aria-describedby="firstName-help">
                    </lightning-input>
                    <div id="firstName-help" class="slds-form-element__help">
                        Enter your legal first name
                    </div>
                </div>

                <div class="slds-form-element">
                    <lightning-input
                        label="Last Name"
                        name="lastName"
                        value={lastName}
                        onchange={handleInputChange}
                        required
                        autocomplete="family-name">
                    </lightning-input>
                </div>

                <div class="slds-form-element">
                    <lightning-input
                        type="email"
                        label="Email"
                        name="email"
                        value={email}
                        onchange={handleInputChange}
                        required
                        autocomplete="email"
                        aria-describedby="email-error"
                        message-when-value-missing="Email is required">
                    </lightning-input>
                    <div id="email-error" class="slds-form-element__help" role="alert" if:true={emailError}>
                        {emailError}
                    </div>
                </div>

                <div class="slds-form-element">
                    <lightning-input
                        type="tel"
                        label="Phone"
                        name="phone"
                        value={phone}
                        onchange={handleInputChange}
                        autocomplete="tel">
                    </lightning-input>
                </div>

                <div class="slds-m-top_medium">
                    <lightning-button
                        type="submit"
                        label="Submit"
                        variant="brand"
                        onclick={handleSubmit}>
                    </lightning-button>
                    <lightning-button
                        label="Cancel"
                        variant="neutral"
                        onclick={handleCancel}>
                    </lightning-button>
                </div>
            </form>
        </div>
    </lightning-card>
</template>
```

**JavaScript** (`contactForm.js`):
```javascript
import { LightningElement, track } from 'lwc';
import { ShowToastEvent } from 'lightning/platformShowToastEvent';

export default class ContactForm extends LightningElement {
    @track firstName = '';
    @track lastName = '';
    @track email = '';
    @track phone = '';
    @track emailError = '';

    handleInputChange(event) {
        const field = event.target.name;
        this[field] = event.target.value;
        
        // Clear error when user starts typing
        if (field === 'email') {
            this.emailError = '';
        }
    }

    handleSubmit(event) {
        event.preventDefault();
        
        // Validate email
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (this.email && !emailRegex.test(this.email)) {
            this.emailError = 'Please enter a valid email address';
            // Focus on email field for screen reader users
            this.template.querySelector('[name="email"]').focus();
            return;
        }

        // Submit form
        this.dispatchEvent(
            new ShowToastEvent({
                title: 'Success',
                message: 'Contact form submitted successfully',
                variant: 'success'
            })
        );
    }

    handleCancel() {
        // Reset form
        this.firstName = '';
        this.lastName = '';
        this.email = '';
        this.phone = '';
        this.emailError = '';
    }
}
```

**Explanation**:
- **Labels**: All inputs use `label` attribute (Lightning Base Components handle this automatically)
- **Autocomplete**: Uses appropriate autocomplete tokens for personal information
- **Error Messages**: Uses `aria-describedby` to associate error messages with inputs
- **Role Alert**: Error messages use `role="alert"` for screen reader announcements
- **Focus Management**: Focuses on error field when validation fails

---

### Example 2: Form with Fieldset and Legend

**Pattern**: Grouped form controls with fieldset/legend
**Use Case**: Address form with grouped fields
**WCAG Criteria**: SC 1.3.1 (iii) - Info and Relationships
**Complexity**: Intermediate

**Problem**:
Related form controls need to be grouped with descriptive labels for screen readers.

**Solution**:

**HTML** (`addressForm.html`):
```html
<template>
    <lightning-card title="Address Information">
        <div class="slds-p-around_medium">
            <form onsubmit={handleSubmit}>
                <fieldset class="slds-form-element">
                    <legend class="slds-form-element__legend slds-form-element__label">
                        Mailing Address
                    </legend>
                    
                    <div class="slds-form-element">
                        <lightning-input
                            label="Street Address"
                            name="street"
                            value={street}
                            onchange={handleInputChange}
                            autocomplete="street-address">
                        </lightning-input>
                    </div>

                    <div class="slds-form-element">
                        <lightning-input
                            label="City"
                            name="city"
                            value={city}
                            onchange={handleInputChange}
                            autocomplete="address-level2">
                        </lightning-input>
                    </div>

                    <div class="slds-form-element">
                        <lightning-input
                            label="State"
                            name="state"
                            value={state}
                            onchange={handleInputChange}
                            autocomplete="address-level1">
                        </lightning-input>
                    </div>

                    <div class="slds-form-element">
                        <lightning-input
                            label="ZIP Code"
                            name="zip"
                            value={zip}
                            onchange={handleInputChange}
                            autocomplete="postal-code">
                        </lightning-input>
                    </div>
                </fieldset>

                <div class="slds-m-top_medium">
                    <lightning-button
                        type="submit"
                        label="Save Address"
                        variant="brand">
                    </lightning-button>
                </div>
            </form>
        </div>
    </lightning-card>
</template>
```

**JavaScript** (`addressForm.js`):
```javascript
import { LightningElement, track } from 'lwc';

export default class AddressForm extends LightningElement {
    @track street = '';
    @track city = '';
    @track state = '';
    @track zip = '';

    handleInputChange(event) {
        const field = event.target.name;
        this[field] = event.target.value;
    }

    handleSubmit(event) {
        event.preventDefault();
        // Handle form submission
    }
}
```

**Explanation**:
- **Fieldset**: Groups related form controls
- **Legend**: Provides descriptive label for the group
- **Autocomplete**: Uses appropriate autocomplete tokens for address fields
- **Screen Reader**: Screen readers announce "Mailing Address, Street Address" when focusing on street field

---

## Keyboard Navigation Examples

### Example 3: Keyboard-Accessible Custom Component

**Pattern**: Custom interactive component with keyboard support
**Use Case**: Custom toggle switch component
**WCAG Criteria**: SC 2.1.1 - Keyboard, SC 4.1.2 (ii) - Role
**Complexity**: Intermediate

**Problem**:
Custom interactive components must be keyboard accessible and have proper ARIA roles.

**Solution**:

**HTML** (`customToggle.html`):
```html
<template>
    <div class="slds-form-element">
        <label class="slds-form-element__label" for="toggle-{uniqueId}">
            {label}
        </label>
        <div class="slds-form-element__control">
            <div
                class="slds-checkbox_toggle slds-grid"
                role="switch"
                aria-checked={checked}
                aria-labelledby="toggle-{uniqueId}"
                tabindex="0"
                onkeydown={handleKeyDown}
                onclick={handleToggle}>
                <span class="slds-checkbox_faux_container" aria-live="polite">
                    <span class="slds-checkbox_faux"></span>
                    <span class="slds-checkbox_on">Enabled</span>
                    <span class="slds-checkbox_off">Disabled</span>
                </span>
            </div>
        </div>
    </div>
</template>
```

**JavaScript** (`customToggle.js`):
```javascript
import { LightningElement, api } from 'lwc';

export default class CustomToggle extends LightningElement {
    @api label = 'Toggle';
    @api checked = false;
    
    uniqueId = Math.random().toString(36).substring(7);

    handleToggle() {
        this.checked = !this.checked;
        this.dispatchEvent(
            new CustomEvent('change', {
                detail: { checked: this.checked }
            })
        );
    }

    handleKeyDown(event) {
        // Support Space and Enter keys
        if (event.key === ' ' || event.key === 'Enter') {
            event.preventDefault();
            this.handleToggle();
        }
    }
}
```

**CSS** (`customToggle.css`):
```css
.slds-checkbox_toggle:focus {
    outline: 2px solid #0176d3;
    outline-offset: 2px;
}

.slds-checkbox_toggle[aria-checked="true"] .slds-checkbox_faux {
    background-color: #0176d3;
}
```

**Explanation**:
- **Role**: Uses `role="switch"` for custom toggle
- **ARIA State**: Uses `aria-checked` to indicate state
- **Keyboard Support**: Handles Space and Enter keys
- **Focus Indicator**: Visible focus outline for keyboard users
- **Tabindex**: Uses `tabindex="0"` to make div focusable
- **ARIA Live**: Uses `aria-live="polite"` for state announcements

---

### Example 4: Focus Management in Modal

**Pattern**: Modal dialog with focus trapping
**Use Case**: Accessible modal dialog
**WCAG Criteria**: SC 2.1.1 - Keyboard, SC 2.4.3 - Focus Order
**Complexity**: Advanced

**Problem**:
Modal dialogs must trap focus and return focus to trigger element when closed.

**Solution**:

**HTML** (`accessibleModal.html`):
```html
<template>
    <template if:true={isOpen}>
        <section
            role="dialog"
            aria-modal="true"
            aria-labelledby="modal-title"
            aria-describedby="modal-description"
            class="slds-modal slds-fade-in-open"
            tabindex="-1">
            <div class="slds-modal__container">
                <header class="slds-modal__header">
                    <h2 id="modal-title" class="slds-modal__title slds-hyphenate">
                        {title}
                    </h2>
                    <button
                        class="slds-button slds-button_icon slds-modal__close slds-button_icon-inverse"
                        title="Close"
                        aria-label="Close {title}"
                        onclick={handleClose}>
                        <lightning-icon icon-name="utility:close" size="small"></lightning-icon>
                        <span class="slds-assistive-text">Close</span>
                    </button>
                </header>
                <div class="slds-modal__content slds-p-around_medium" id="modal-description">
                    <slot></slot>
                </div>
                <footer class="slds-modal__footer">
                    <lightning-button
                        label="Cancel"
                        variant="neutral"
                        onclick={handleClose}>
                    </lightning-button>
                    <lightning-button
                        label="Confirm"
                        variant="brand"
                        onclick={handleConfirm}>
                    </lightning-button>
                </footer>
            </div>
        </section>
        <div class="slds-backdrop slds-backdrop_open" role="presentation"></div>
    </template>
</template>
```

**JavaScript** (`accessibleModal.js`):
```javascript
import { LightningElement, api } from 'lwc';

export default class AccessibleModal extends LightningElement {
    @api title = 'Modal Title';
    @api isOpen = false;
    
    previousActiveElement = null;

    connectedCallback() {
        // Store previous active element when modal opens
        if (this.isOpen) {
            this.previousActiveElement = document.activeElement;
            this.trapFocus();
        }
    }

    renderedCallback() {
        if (this.isOpen) {
            // Focus on modal when opened
            const modal = this.template.querySelector('[role="dialog"]');
            if (modal) {
                modal.focus();
            }
            this.trapFocus();
        }
    }

    trapFocus() {
        const modal = this.template.querySelector('[role="dialog"]');
        if (!modal) return;

        const focusableElements = modal.querySelectorAll(
            'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
        );
        const firstElement = focusableElements[0];
        const lastElement = focusableElements[focusableElements.length - 1];

        // Trap focus within modal
        modal.addEventListener('keydown', (e) => {
            if (e.key === 'Tab') {
                if (e.shiftKey) {
                    if (document.activeElement === firstElement) {
                        e.preventDefault();
                        lastElement.focus();
                    }
                } else {
                    if (document.activeElement === lastElement) {
                        e.preventDefault();
                        firstElement.focus();
                    }
                }
            }
            if (e.key === 'Escape') {
                this.handleClose();
            }
        });
    }

    handleClose() {
        this.isOpen = false;
        // Return focus to previous element
        if (this.previousActiveElement) {
            this.previousActiveElement.focus();
        }
        this.dispatchEvent(new CustomEvent('close'));
    }

    handleConfirm() {
        this.dispatchEvent(new CustomEvent('confirm'));
        this.handleClose();
    }
}
```

**Explanation**:
- **Role Dialog**: Uses `role="dialog"` for modal
- **ARIA Modal**: Uses `aria-modal="true"` to indicate modal state
- **ARIA Labels**: Uses `aria-labelledby` and `aria-describedby`
- **Focus Trap**: Traps focus within modal using keyboard event listeners
- **Escape Key**: Closes modal on Escape key
- **Focus Return**: Returns focus to trigger element when closed
- **Backdrop**: Uses `role="presentation"` for decorative backdrop

---

## ARIA Patterns

### Example 5: ARIA Live Regions for Dynamic Content

**Pattern**: ARIA live regions for screen reader announcements
**Use Case**: Real-time status updates
**WCAG Criteria**: SC 4.1.3 - Status Messages
**Complexity**: Basic

**Problem**:
Dynamic content changes need to be announced to screen reader users.

**Solution**:

**HTML** (`statusUpdates.html`):
```html
<template>
    <lightning-card title="Status Updates">
        <div class="slds-p-around_medium">
            <div
                role="status"
                aria-live="polite"
                aria-atomic="true"
                class="slds-text-body_small">
                {statusMessage}
            </div>

            <div class="slds-m-top_medium">
                <lightning-button
                    label="Start Process"
                    variant="brand"
                    onclick={handleStart}
                    if:false={isProcessing}>
                </lightning-button>
                <lightning-button
                    label="Stop Process"
                    variant="destructive"
                    onclick={handleStop}
                    if:true={isProcessing}>
                </lightning-button>
            </div>

            <div
                role="alert"
                aria-live="assertive"
                class="slds-m-top_medium"
                if:true={errorMessage}>
                <div class="slds-text-color_error">
                    {errorMessage}
                </div>
            </div>
        </div>
    </lightning-card>
</template>
```

**JavaScript** (`statusUpdates.js`):
```javascript
import { LightningElement, track } from 'lwc';

export default class StatusUpdates extends LightningElement {
    @track statusMessage = 'Ready to start';
    @track isProcessing = false;
    @track errorMessage = '';

    handleStart() {
        this.isProcessing = true;
        this.statusMessage = 'Processing started...';
        this.errorMessage = '';
        
        // Simulate async operation
        setTimeout(() => {
            this.statusMessage = 'Processing completed successfully';
            this.isProcessing = false;
        }, 3000);
    }

    handleStop() {
        this.isProcessing = false;
        this.statusMessage = 'Processing stopped by user';
    }
}
```

**Explanation**:
- **ARIA Live Polite**: Uses `aria-live="polite"` for non-urgent updates
- **ARIA Live Assertive**: Uses `aria-live="assertive"` for error messages
- **ARIA Atomic**: Uses `aria-atomic="true"` to announce entire region
- **Role Status**: Uses `role="status"` for status updates
- **Role Alert**: Uses `role="alert"` for error messages

---

### Example 6: ARIA Labels and Descriptions

**Pattern**: Accessible names and descriptions for custom components
**Use Case**: Custom button with icon
**WCAG Criteria**: SC 4.1.2 (i) - Name, SC 4.1.2 (iii) - Value
**Complexity**: Basic

**Problem**:
Icon-only buttons need accessible names for screen readers.

**Solution**:

**HTML** (`iconButton.html`):
```html
<template>
    <button
        type="button"
        class="slds-button slds-button_icon"
        aria-label={ariaLabel}
        aria-describedby={describedById}
        onclick={handleClick}
        title={tooltip}>
        <lightning-icon
            icon-name={iconName}
            size="small"
            alternative-text={iconAltText}>
        </lightning-icon>
        <span class="slds-assistive-text">{assistiveText}</span>
    </button>
    <div
        id={describedById}
        class="slds-assistive-text">
        {description}
    </div>
</template>
```

**JavaScript** (`iconButton.js`):
```javascript
import { LightningElement, api } from 'lwc';

export default class IconButton extends LightningElement {
    @api iconName = 'utility:add';
    @api ariaLabel = 'Add item';
    @api description = 'Click to add a new item to the list';
    @api tooltip = 'Add';
    
    get iconAltText() {
        return this.ariaLabel;
    }
    
    get assistiveText() {
        return this.ariaLabel;
    }
    
    get describedById() {
        return `desc-${Math.random().toString(36).substring(7)}`;
    }

    handleClick() {
        this.dispatchEvent(new CustomEvent('click'));
    }
}
```

**Explanation**:
- **ARIA Label**: Provides accessible name for button
- **ARIA Describedby**: Associates description with button
- **Assistive Text**: Hidden text for screen readers
- **Icon Alt Text**: Provides alternative text for icon
- **Title**: Provides tooltip for mouse users

---

## Image Accessibility

### Example 7: Decorative vs Informative Images

**Pattern**: Proper alt text for images
**Use Case**: Image gallery with mixed decorative and informative images
**WCAG Criteria**: SC 1.1.1 - Non-text Content
**Complexity**: Basic

**Problem**:
Images need appropriate alt text based on whether they're decorative or informative.

**Solution**:

**HTML** (`imageGallery.html`):
```html
<template>
    <lightning-card title="Image Gallery">
        <div class="slds-p-around_medium">
            <!-- Decorative image (border/divider) -->
            <img
                src="/assets/images/divider.png"
                alt=""
                class="slds-m-vertical_medium"
                aria-hidden="true">
            
            <!-- Informative image (chart) -->
            <img
                src="/assets/images/sales-chart.png"
                alt="Sales chart showing 25% increase in Q4 2023 compared to Q3 2023"
                class="slds-m-vertical_medium">
            
            <!-- Image as link -->
            <a href={imageLink} aria-label="View full-size product image: {productName}">
                <img
                    src={productImage}
                    alt=""
                    aria-hidden="true">
            </a>
            
            <!-- Complex informative image -->
            <figure>
                <img
                    src="/assets/images/diagram.png"
                    alt=""
                    aria-describedby="diagram-description">
                <figcaption id="diagram-description">
                    System architecture diagram showing three-tier structure: 
                    presentation layer, business logic layer, and data layer.
                </figcaption>
            </figure>
        </div>
    </lightning-card>
</template>
```

**JavaScript** (`imageGallery.js`):
```javascript
import { LightningElement, api } from 'lwc';

export default class ImageGallery extends LightningElement {
    @api productImage = '/assets/images/product.jpg';
    @api productName = 'Product Name';
    @api imageLink = '/products/123';
}
```

**Explanation**:
- **Decorative Images**: Use `alt=""` and optionally `aria-hidden="true"`
- **Informative Images**: Use descriptive alt text
- **Image Links**: Provide `aria-label` on link, use `alt=""` on image
- **Complex Images**: Use `aria-describedby` with `figcaption` for detailed descriptions

---

## Semantic HTML Examples

### Example 8: Proper Heading Hierarchy

**Pattern**: Semantic heading structure
**Use Case**: Component with multiple sections
**WCAG Criteria**: SC 1.3.1 (i) - Info and Relationships
**Complexity**: Basic

**Problem**:
Headings must follow proper hierarchy (h1 → h2 → h3) for screen reader navigation.

**Solution**:

**HTML** (`documentStructure.html`):
```html
<template>
    <article>
        <header>
            <h1>Document Title</h1>
            <p class="slds-text-body_small">Published on {publishDate}</p>
        </header>
        
        <main>
            <section>
                <h2>Introduction</h2>
                <p>Introduction content...</p>
            </section>
            
            <section>
                <h2>Main Content</h2>
                <h3>Subsection 1</h3>
                <p>Subsection content...</p>
                
                <h3>Subsection 2</h3>
                <p>Subsection content...</p>
            </section>
            
            <section>
                <h2>Conclusion</h2>
                <p>Conclusion content...</p>
            </section>
        </main>
        
        <footer>
            <p class="slds-text-body_small">Copyright {currentYear}</p>
        </footer>
    </article>
</template>
```

**JavaScript** (`documentStructure.js`):
```javascript
import { LightningElement } from 'lwc';

export default class DocumentStructure extends LightningElement {
    publishDate = new Date().toLocaleDateString();
    currentYear = new Date().getFullYear();
}
```

**Explanation**:
- **Semantic HTML**: Uses `<article>`, `<header>`, `<main>`, `<section>`, `<footer>`
- **Heading Hierarchy**: Proper h1 → h2 → h3 structure
- **Screen Reader Navigation**: Screen readers can navigate by headings
- **Landmarks**: Semantic regions provide navigation landmarks

---

### Example 9: Accessible Data Table

**Pattern**: Accessible table with proper structure
**Use Case**: Data table with sortable columns
**WCAG Criteria**: SC 1.3.1 (i) - Info and Relationships, SC 4.1.2 (ii) - Role
**Complexity**: Intermediate

**Problem**:
Data tables need proper structure, headers, and ARIA attributes for screen readers.

**Solution**:

**HTML** (`accessibleTable.html`):
```html
<template>
    <lightning-card title="Contact List">
        <div class="slds-p-around_medium">
            <table
                class="slds-table slds-table_cell-buffer slds-table_bordered"
                role="table"
                aria-label="Contact list with {contactCount} contacts">
                <thead>
                    <tr>
                        <th scope="col" aria-sort={nameSortDirection}>
                            <button
                                class="slds-button slds-button_reset"
                                onclick={handleSortName}
                                aria-label="Sort by name, {nameSortDirection}">
                                Name
                                <lightning-icon
                                    icon-name={nameSortIcon}
                                    size="x-small"
                                    alternative-text="Sort indicator">
                                </lightning-icon>
                            </button>
                        </th>
                        <th scope="col">Email</th>
                        <th scope="col">Phone</th>
                        <th scope="col">Actions</th>
                    </tr>
                </thead>
                <tbody>
                    <template for:each={contacts} for:item="contact">
                        <tr key={contact.Id}>
                            <td data-label="Name">{contact.Name}</td>
                            <td data-label="Email">
                                <a href="mailto:{contact.Email}" aria-label="Email {contact.Name}">
                                    {contact.Email}
                                </a>
                            </td>
                            <td data-label="Phone">{contact.Phone}</td>
                            <td data-label="Actions">
                                <lightning-button-icon
                                    icon-name="utility:edit"
                                    alternative-text="Edit {contact.Name}"
                                    onclick={handleEdit}
                                    data-id={contact.Id}>
                                </lightning-button-icon>
                            </td>
                        </tr>
                    </template>
                </tbody>
            </table>
        </div>
    </lightning-card>
</template>
```

**JavaScript** (`accessibleTable.js`):
```javascript
import { LightningElement, api, track } from 'lwc';

export default class AccessibleTable extends LightningElement {
    @api contacts = [];
    @track nameSortDirection = 'none';

    get contactCount() {
        return this.contacts.length;
    }

    get nameSortIcon() {
        if (this.nameSortDirection === 'ascending') {
            return 'utility:arrowup';
        } else if (this.nameSortDirection === 'descending') {
            return 'utility:arrowdown';
        }
        return 'utility:arrowup';
    }

    handleSortName() {
        if (this.nameSortDirection === 'none' || this.nameSortDirection === 'descending') {
            this.nameSortDirection = 'ascending';
            this.contacts.sort((a, b) => a.Name.localeCompare(b.Name));
        } else {
            this.nameSortDirection = 'descending';
            this.contacts.sort((a, b) => b.Name.localeCompare(a.Name));
        }
    }

    handleEdit(event) {
        const contactId = event.currentTarget.dataset.id;
        this.dispatchEvent(new CustomEvent('edit', { detail: { contactId } }));
    }
}
```

**Explanation**:
- **Role Table**: Uses `role="table"` for table structure
- **ARIA Label**: Provides table description
- **Scope Col**: Uses `scope="col"` for column headers
- **ARIA Sort**: Uses `aria-sort` to indicate sort state
- **Data Label**: Uses `data-label` for responsive table headers
- **Accessible Names**: All interactive elements have accessible names

---

## Dynamic Content Accessibility

### Example 10: Loading States with ARIA

**Pattern**: Accessible loading indicators
**Use Case**: Component with async data loading
**WCAG Criteria**: SC 4.1.3 - Status Messages
**Complexity**: Basic

**Problem**:
Loading states need to be announced to screen reader users.

**Solution**:

**HTML** (`loadingState.html`):
```html
<template>
    <lightning-card title="Data Loader">
        <div class="slds-p-around_medium">
            <div
                role="status"
                aria-live="polite"
                aria-busy={isLoading}
                class="slds-m-bottom_medium">
                <template if:true={isLoading}>
                    <lightning-spinner
                        alternative-text="Loading data"
                        size="medium">
                    </lightning-spinner>
                    <span class="slds-assistive-text">Loading data, please wait</span>
                </template>
                <template if:false={isLoading}>
                    <span>Data loaded successfully</span>
                </template>
            </div>

            <div if:true={hasData}>
                <!-- Content here -->
            </div>

            <div
                role="alert"
                if:true={errorMessage}>
                <div class="slds-text-color_error">
                    {errorMessage}
                </div>
            </div>
        </div>
    </lightning-card>
</template>
```

**JavaScript** (`loadingState.js`):
```javascript
import { LightningElement, track } from 'lwc';

export default class LoadingState extends LightningElement {
    @track isLoading = false;
    @track hasData = false;
    @track errorMessage = '';

    async loadData() {
        this.isLoading = true;
        this.errorMessage = '';
        
        try {
            // Simulate API call
            await new Promise(resolve => setTimeout(resolve, 2000));
            this.hasData = true;
        } catch (error) {
            this.errorMessage = 'Failed to load data: ' + error.message;
        } finally {
            this.isLoading = false;
        }
    }
}
```

**Explanation**:
- **ARIA Busy**: Uses `aria-busy` to indicate loading state
- **ARIA Live**: Uses `aria-live="polite"` for status updates
- **Role Status**: Uses `role="status"` for status messages
- **Role Alert**: Uses `role="alert"` for error messages
- **Assistive Text**: Provides screen reader announcements

---

## Color and Contrast

### Example 11: Not Relying on Color Alone

**Pattern**: Using multiple indicators for information
**Use Case**: Status indicators with icons and text
**WCAG Criteria**: SC 1.4.1 - Use of Color
**Complexity**: Basic

**Problem**:
Information must not be conveyed by color alone.

**Solution**:

**HTML** (`statusIndicator.html`):
```html
<template>
    <div class="slds-p-around_medium">
        <div class="slds-grid slds-gutters">
            <template for:each={statuses} for:item="status">
                <div key={status.id} class="slds-col slds-size_1-of-3">
                    <div class="slds-box">
                        <div class="slds-media">
                            <div class="slds-media__figure">
                                <lightning-icon
                                    icon-name={status.icon}
                                    size="small"
                                    alternative-text={status.label}
                                    class={status.iconClass}>
                                </lightning-icon>
                            </div>
                            <div class="slds-media__body">
                                <p class="slds-text-heading_small">{status.label}</p>
                                <p class="slds-text-body_small">{status.description}</p>
                            </div>
                        </div>
                    </div>
                </div>
            </template>
        </div>
    </div>
</template>
```

**JavaScript** (`statusIndicator.js`):
```javascript
import { LightningElement } from 'lwc';

export default class StatusIndicator extends LightningElement {
    statuses = [
        {
            id: '1',
            label: 'Success',
            description: 'Operation completed successfully',
            icon: 'utility:success',
            iconClass: 'slds-icon-text-success'
        },
        {
            id: '2',
            label: 'Warning',
            description: 'Operation completed with warnings',
            icon: 'utility:warning',
            iconClass: 'slds-icon-text-warning'
        },
        {
            id: '3',
            label: 'Error',
            description: 'Operation failed',
            icon: 'utility:error',
            iconClass: 'slds-icon-text-error'
        }
    ];
}
```

**Explanation**:
- **Multiple Indicators**: Uses icon, text, and color
- **Icon Alt Text**: Provides alternative text for icons
- **Text Labels**: Clear text labels for each status
- **Color Contrast**: Uses SLDS color tokens for proper contrast
- **Screen Reader**: Screen readers announce icon names and text

---

## Testing Notes

### Screen Reader Testing
- Test with NVDA (Windows), JAWS (Windows), or VoiceOver (macOS/iOS)
- Verify all interactive elements are announced
- Verify form labels are associated correctly
- Verify error messages are announced
- Verify loading states are announced

### Keyboard Navigation Testing
- Tab through all interactive elements
- Verify focus indicators are visible
- Verify keyboard shortcuts work (Enter, Space, Escape)
- Verify focus trapping in modals
- Verify focus return after modal close

### Color Contrast Testing
- Use tools like WebAIM Contrast Checker
- Verify text meets WCAG AA standards (4.5:1 for normal text, 3:1 for large text)
- Verify focus indicators meet 3:1 contrast ratio
- Test with color blindness simulators

---

## Related Examples

- [Accessible Component Template](../templates/lwc-accessible-component-template.md) - Template for accessible components
- [Accessibility Testing](../../testing/lwc-accessibility-testing.md) - Testing patterns
- [Accessibility Troubleshooting](../../troubleshooting/lwc-accessibility-errors.md) - Common errors and fixes

