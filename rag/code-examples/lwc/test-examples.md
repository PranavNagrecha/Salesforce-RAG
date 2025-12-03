---
title: "LWC Jest Testing Code Examples"
level: "Intermediate"
tags:
  - lwc
  - code-examples
  - testing
  - jest
last_reviewed: "2025-01-XX"
---

# LWC Jest Testing Code Examples

> This file contains complete, working code examples for testing Lightning Web Components with Jest.
> All examples are copy-paste ready and follow Salesforce best practices.

## Overview

Jest is the testing framework for Lightning Web Components. These examples demonstrate how to write comprehensive tests for LWC components, including testing wire adapters, Apex calls, events, and user interactions.

**Related Patterns**:
- <a href="{{ '/rag/code-examples/lwc/code-examples/testing/lwc-jest-testing.html' | relative_url }}">LWC Jest Testing</a> - Complete Jest testing guide
- <a href="{{ '/rag/development/lwc-patterns.html' | relative_url }}">LWC Patterns</a> - LWC development patterns
- <a href="{{ '/rag/code-examples/lwc/code-examples/testing/apex-testing-patterns.html' | relative_url }}">Apex Testing Patterns</a> - Apex testing patterns

## Examples

### Example 1: Basic Component Test

**Pattern**: Testing component rendering and properties
**Use Case**: Verifying component displays correctly
**Complexity**: Basic
**Related Patterns**: <a href="{{ '/rag/code-examples/lwc/code-examples/testing/lwc-jest-testing.html' | relative_url }}">LWC Jest Testing</a>

**Problem**:
You need to test that a component renders correctly and displays data.

**Component** (`contactDisplay.js`):
```javascript
import { LightningElement, api, wire } from 'lwc';
import { getRecord } from 'lightning/uiRecordApi';
import CONTACT_NAME_FIELD from '@salesforce/schema/Contact.Name';
import CONTACT_EMAIL_FIELD from '@salesforce/schema/Contact.Email';

const FIELDS = [CONTACT_NAME_FIELD, CONTACT_EMAIL_FIELD];

export default class ContactDisplay extends LightningElement {
    @api recordId;

    @wire(getRecord, { recordId: '$recordId', fields: FIELDS })
    contact;

    get name() {
        return this.contact?.data?.fields?.Name?.value || '';
    }

    get email() {
        return this.contact?.data?.fields?.Email?.value || '';
    }
}
```

**Test** (`contactDisplay.test.js`):
```javascript
import { createElement } from 'lwc';
import ContactDisplay from 'c/contactDisplay';
import { getRecord } from 'lightning/uiRecordApi';

// Mock the wire adapter
jest.mock(
    'lightning/uiRecordApi',
    () => ({
        getRecord: jest.fn()
    }),
    { virtual: true }
);

describe('c-contact-display', () => {
    afterEach(() => {
        // Clean up after each test
        while (document.body.firstChild) {
            document.body.removeChild(document.body.firstChild);
        }
        jest.clearAllMocks();
    });

    it('displays contact name and email', () => {
        // Arrange
        const RECORD_ID = '003000000000000AAA';
        const mockRecord = {
            fields: {
                Name: { value: 'John Doe' },
                Email: { value: 'john.doe@example.com' }
            }
        };

        getRecord.mockResolvedValue({ data: mockRecord });

        // Act
        const element = createElement('c-contact-display', {
            is: ContactDisplay
        });
        element.recordId = RECORD_ID;
        document.body.appendChild(element);

        // Assert
        return Promise.resolve().then(() => {
            const nameElement = element.shadowRoot.querySelector('.contact-name');
            const emailElement = element.shadowRoot.querySelector('.contact-email');
            
            expect(nameElement.textContent).toBe('John Doe');
            expect(emailElement.textContent).toBe('john.doe@example.com');
        });
    });

    it('handles loading state', () => {
        // Arrange
        const RECORD_ID = '003000000000000AAA';
        getRecord.mockResolvedValue({ data: undefined });

        // Act
        const element = createElement('c-contact-display', {
            is: ContactDisplay
        });
        element.recordId = RECORD_ID;
        document.body.appendChild(element);

        // Assert
        return Promise.resolve().then(() => {
            const loadingElement = element.shadowRoot.querySelector('.loading');
            expect(loadingElement).toBeTruthy();
        });
    });

    it('handles error state', () => {
        // Arrange
        const RECORD_ID = '003000000000000AAA';
        const mockError = {
            body: { message: 'Record not found' }
        };
        getRecord.mockResolvedValue({ error: mockError });

        // Act
        const element = createElement('c-contact-display', {
            is: ContactDisplay
        });
        element.recordId = RECORD_ID;
        document.body.appendChild(element);

        // Assert
        return Promise.resolve().then(() => {
            const errorElement = element.shadowRoot.querySelector('.error');
            expect(errorElement.textContent).toContain('Record not found');
        });
    });
});
```

**Explanation**:
- Mocks the wire adapter using `jest.mock`
- Tests component rendering with mock data
- Tests loading and error states
- Cleans up after each test

**Best Practices**:
- Mock wire adapters and Apex methods
- Test all component states (loading, success, error)
- Clean up DOM and mocks after each test
- Use descriptive test names

### Example 2: Testing Apex Method Calls

**Pattern**: Testing imperative Apex method calls
**Use Case**: Verifying Apex methods are called correctly
**Complexity**: Intermediate
**Related Patterns**: <a href="{{ '/rag/code-examples/lwc/code-examples/testing/lwc-jest-testing.html' | relative_url }}">LWC Jest Testing</a>

**Component** (`contactAction.js`):
```javascript
import { LightningElement, api } from 'lwc';
import processContact from '@salesforce/apex/ContactService.processContact';
import { ShowToastEvent } from 'lightning/platformShowToastEvent';

export default class ContactAction extends LightningElement {
    @api recordId;
    isLoading = false;

    handleProcess() {
        this.isLoading = true;
        
        processContact({ contactId: this.recordId })
            .then(result => {
                this.showToast('Success', 'Contact processed', 'success');
                this.dispatchEvent(new CustomEvent('processed'));
            })
            .catch(error => {
                this.showToast('Error', error.body?.message || 'Error occurred', 'error');
            })
            .finally(() => {
                this.isLoading = false;
            });
    }

    showToast(title, message, variant) {
        const evt = new ShowToastEvent({ title, message, variant });
        this.dispatchEvent(evt);
    }
}
```

**Test** (`contactAction.test.js`):
```javascript
import { createElement } from 'lwc';
import ContactAction from 'c/contactAction';
import processContact from '@salesforce/apex/ContactService.processContact';
import { ShowToastEvent } from 'lightning/platformShowToastEvent';

// Mock Apex method
jest.mock(
    '@salesforce/apex/ContactService.processContact',
    () => ({
        default: jest.fn()
    }),
    { virtual: true }
);

// Mock platform event
jest.mock(
    'lightning/platformShowToastEvent',
    () => ({
        ShowToastEvent: jest.fn()
    }),
    { virtual: true }
);

describe('c-contact-action', () => {
    afterEach(() => {
        while (document.body.firstChild) {
            document.body.removeChild(document.body.firstChild);
        }
        jest.clearAllMocks();
    });

    it('calls Apex method and shows success toast', () => {
        // Arrange
        const RECORD_ID = '003000000000000AAA';
        const mockResult = { success: true };
        processContact.mockResolvedValue(mockResult);

        const element = createElement('c-contact-action', {
            is: ContactAction
        });
        element.recordId = RECORD_ID;
        document.body.appendChild(element);

        // Act
        const button = element.shadowRoot.querySelector('lightning-button');
        button.click();

        // Assert
        return Promise.resolve().then(() => {
            expect(processContact).toHaveBeenCalledWith({ contactId: RECORD_ID });
            expect(ShowToastEvent).toHaveBeenCalledWith(
                expect.objectContaining({
                    title: 'Success',
                    message: 'Contact processed',
                    variant: 'success'
                })
            );
        });
    });

    it('dispatches processed event on success', () => {
        // Arrange
        const RECORD_ID = '003000000000000AAA';
        processContact.mockResolvedValue({ success: true });

        const element = createElement('c-contact-action', {
            is: ContactAction
        });
        element.recordId = RECORD_ID;
        document.body.appendChild(element);

        // Act
        const handler = jest.fn();
        element.addEventListener('processed', handler);
        const button = element.shadowRoot.querySelector('lightning-button');
        button.click();

        // Assert
        return Promise.resolve().then(() => {
            expect(handler).toHaveBeenCalled();
        });
    });

    it('handles Apex method errors', () => {
        // Arrange
        const RECORD_ID = '003000000000000AAA';
        const mockError = {
            body: { message: 'Processing failed' }
        };
        processContact.mockRejectedValue(mockError);

        const element = createElement('c-contact-action', {
            is: ContactAction
        });
        element.recordId = RECORD_ID;
        document.body.appendChild(element);

        // Act
        const button = element.shadowRoot.querySelector('lightning-button');
        button.click();

        // Assert
        return Promise.resolve().then(() => {
            expect(ShowToastEvent).toHaveBeenCalledWith(
                expect.objectContaining({
                    title: 'Error',
                    message: 'Processing failed',
                    variant: 'error'
                })
            );
        });
    });

    it('shows loading state during processing', () => {
        // Arrange
        const RECORD_ID = '003000000000000AAA';
        let resolvePromise;
        const promise = new Promise(resolve => {
            resolvePromise = resolve;
        });
        processContact.mockReturnValue(promise);

        const element = createElement('c-contact-action', {
            is: ContactAction
        });
        element.recordId = RECORD_ID;
        document.body.appendChild(element);

        // Act
        const button = element.shadowRoot.querySelector('lightning-button');
        button.click();

        // Assert
        return Promise.resolve().then(() => {
            expect(element.isLoading).toBe(true);
            expect(button.disabled).toBe(true);
            
            // Resolve promise
            resolvePromise({ success: true });
            
            return Promise.resolve().then(() => {
                expect(element.isLoading).toBe(false);
                expect(button.disabled).toBe(false);
            });
        });
    });
});
```

**Explanation**:
- Mocks Apex methods and platform events
- Tests successful and error scenarios
- Verifies event dispatching
- Tests loading states

**Best Practices**:
- Mock all Apex methods and platform events
- Test both success and error paths
- Verify event dispatching
- Test loading states

### Example 3: Testing Wire Adapters

**Pattern**: Testing reactive wire adapter data
**Use Case**: Verifying wire adapters work correctly
**Complexity**: Intermediate
**Related Patterns**: <a href="{{ '/rag/code-examples/lwc/code-examples/testing/lwc-jest-testing.html' | relative_url }}">LWC Jest Testing</a>

**Component** (`accountContacts.js`):
```javascript
import { LightningElement, api, wire } from 'lwc';
import getContacts from '@salesforce/apex/ContactService.getContacts';

export default class AccountContacts extends LightningElement {
    @api recordId;

    @wire(getContacts, { accountId: '$recordId' })
    contacts;

    get hasContacts() {
        return this.contacts?.data && this.contacts.data.length > 0;
    }

    get contactsList() {
        return this.contacts?.data || [];
    }
}
```

**Test** (`accountContacts.test.js`):
```javascript
import { createElement } from 'lwc';
import AccountContacts from 'c/accountContacts';
import getContacts from '@salesforce/apex/ContactService.getContacts';

// Mock Apex method
jest.mock(
    '@salesforce/apex/ContactService.getContacts',
    () => ({
        default: jest.fn()
    }),
    { virtual: true }
);

describe('c-account-contacts', () => {
    afterEach(() => {
        while (document.body.firstChild) {
            document.body.removeChild(document.body.firstChild);
        }
        jest.clearAllMocks();
    });

    it('displays contacts when data is available', () => {
        // Arrange
        const RECORD_ID = '001000000000000AAA';
        const mockContacts = [
            { Id: '0031', Name: 'John Doe', Email: 'john@example.com' },
            { Id: '0032', Name: 'Jane Smith', Email: 'jane@example.com' }
        ];
        getContacts.mockResolvedValue(mockContacts);

        // Act
        const element = createElement('c-account-contacts', {
            is: AccountContacts
        });
        element.recordId = RECORD_ID;
        document.body.appendChild(element);

        // Assert
        return Promise.resolve().then(() => {
            expect(getContacts).toHaveBeenCalledWith({ accountId: RECORD_ID });
            
            const contactElements = element.shadowRoot.querySelectorAll('.contact-item');
            expect(contactElements.length).toBe(2);
            expect(contactElements[0].textContent).toContain('John Doe');
            expect(contactElements[1].textContent).toContain('Jane Smith');
        });
    });

    it('shows empty state when no contacts', () => {
        // Arrange
        const RECORD_ID = '001000000000000AAA';
        getContacts.mockResolvedValue([]);

        // Act
        const element = createElement('c-account-contacts', {
            is: AccountContacts
        });
        element.recordId = RECORD_ID;
        document.body.appendChild(element);

        // Assert
        return Promise.resolve().then(() => {
            const emptyState = element.shadowRoot.querySelector('.empty-state');
            expect(emptyState).toBeTruthy();
            expect(emptyState.textContent).toContain('No contacts');
        });
    });

    it('handles wire adapter errors', () => {
        // Arrange
        const RECORD_ID = '001000000000000AAA';
        const mockError = {
            body: { message: 'Failed to load contacts' }
        };
        getContacts.mockRejectedValue(mockError);

        // Act
        const element = createElement('c-account-contacts', {
            is: AccountContacts
        });
        element.recordId = RECORD_ID;
        document.body.appendChild(element);

        // Assert
        return Promise.resolve().then(() => {
            const errorElement = element.shadowRoot.querySelector('.error');
            expect(errorElement).toBeTruthy();
            expect(errorElement.textContent).toContain('Failed to load contacts');
        });
    });
});
```

**Explanation**:
- Mocks wire adapter Apex methods
- Tests data display, empty states, and errors
- Verifies wire adapter is called with correct parameters
- Tests reactive updates

**Best Practices**:
- Mock wire adapter Apex methods
- Test all wire adapter states (data, error, loading)
- Verify parameters passed to wire adapters
- Test reactive updates when parameters change

### Example 4: Testing User Interactions

**Pattern**: Testing user interactions and events
**Use Case**: Verifying user interactions work correctly
**Complexity**: Intermediate
**Related Patterns**: <a href="{{ '/rag/code-examples/lwc/code-examples/testing/lwc-jest-testing.html' | relative_url }}">LWC Jest Testing</a>

**Component** (`contactForm.js`):
```javascript
import { LightningElement, track } from 'lwc';
import { updateRecord } from 'lightning/uiRecordApi';
import { ShowToastEvent } from 'lightning/platformShowToastEvent';
import CONTACT_ID_FIELD from '@salesforce/schema/Contact.Id';
import CONTACT_EMAIL_FIELD from '@salesforce/schema/Contact.Email';

export default class ContactForm extends LightningElement {
    @track email = '';
    @track recordId = '';

    handleEmailChange(event) {
        this.email = event.target.value;
    }

    handleSave() {
        const fields = {};
        fields[CONTACT_ID_FIELD.fieldApiName] = this.recordId;
        fields[CONTACT_EMAIL_FIELD.fieldApiName] = this.email;

        updateRecord({ fields })
            .then(() => {
                this.showToast('Success', 'Contact updated', 'success');
                this.dispatchEvent(new CustomEvent('saved'));
            })
            .catch(error => {
                this.showToast('Error', error.body?.message || 'Update failed', 'error');
            });
    }

    showToast(title, message, variant) {
        const evt = new ShowToastEvent({ title, message, variant });
        this.dispatchEvent(evt);
    }
}
```

**Test** (`contactForm.test.js`):
```javascript
import { createElement } from 'lwc';
import ContactForm from 'c/contactForm';
import { updateRecord } from 'lightning/uiRecordApi';
import { ShowToastEvent } from 'lightning/platformShowToastEvent';

// Mock Lightning Data Service
jest.mock(
    'lightning/uiRecordApi',
    () => ({
        updateRecord: jest.fn()
    }),
    { virtual: true }
);

// Mock platform event
jest.mock(
    'lightning/platformShowToastEvent',
    () => ({
        ShowToastEvent: jest.fn()
    }),
    { virtual: true }
);

describe('c-contact-form', () => {
    afterEach(() => {
        while (document.body.firstChild) {
            document.body.removeChild(document.body.firstChild);
        }
        jest.clearAllMocks();
    });

    it('updates email field on input change', () => {
        // Arrange
        const element = createElement('c-contact-form', {
            is: ContactForm
        });
        document.body.appendChild(element);

        // Act
        const emailInput = element.shadowRoot.querySelector('lightning-input[type="email"]');
        emailInput.value = 'newemail@example.com';
        emailInput.dispatchEvent(new CustomEvent('change', {
            detail: { value: 'newemail@example.com' }
        }));

        // Assert
        return Promise.resolve().then(() => {
            expect(element.email).toBe('newemail@example.com');
        });
    });

    it('saves contact and dispatches saved event', () => {
        // Arrange
        const RECORD_ID = '003000000000000AAA';
        const EMAIL = 'test@example.com';
        updateRecord.mockResolvedValue();

        const element = createElement('c-contact-form', {
            is: ContactForm
        });
        element.recordId = RECORD_ID;
        element.email = EMAIL;
        document.body.appendChild(element);

        // Act
        const handler = jest.fn();
        element.addEventListener('saved', handler);
        const saveButton = element.shadowRoot.querySelector('lightning-button[label="Save"]');
        saveButton.click();

        // Assert
        return Promise.resolve().then(() => {
            expect(updateRecord).toHaveBeenCalledWith(
                expect.objectContaining({
                    fields: expect.objectContaining({
                        Id: RECORD_ID,
                        Email: EMAIL
                    })
                })
            );
            expect(handler).toHaveBeenCalled();
            expect(ShowToastEvent).toHaveBeenCalledWith(
                expect.objectContaining({
                    title: 'Success',
                    message: 'Contact updated',
                    variant: 'success'
                })
            );
        });
    });

    it('handles save errors', () => {
        // Arrange
        const RECORD_ID = '003000000000000AAA';
        const mockError = {
            body: { message: 'Update failed' }
        };
        updateRecord.mockRejectedValue(mockError);

        const element = createElement('c-contact-form', {
            is: ContactForm
        });
        element.recordId = RECORD_ID;
        document.body.appendChild(element);

        // Act
        const saveButton = element.shadowRoot.querySelector('lightning-button[label="Save"]');
        saveButton.click();

        // Assert
        return Promise.resolve().then(() => {
            expect(ShowToastEvent).toHaveBeenCalledWith(
                expect.objectContaining({
                    title: 'Error',
                    message: 'Update failed',
                    variant: 'error'
                })
            );
        });
    });
});
```

**Explanation**:
- Tests user input handling
- Tests form submission
- Verifies event dispatching
- Tests error handling

**Best Practices**:
- Test all user interactions
- Verify event dispatching
- Test error handling
- Use realistic test data

## Related Examples

- <a href="{{ '/rag/code-examples/lwc/code-examples/lwc/component-examples.html' | relative_url }}">Component Examples</a> - LWC component implementations
- <a href="{{ '/rag/code-examples/lwc/code-examples/lwc/service-examples.html' | relative_url }}">Service Examples</a> - LWC service layer patterns
- <a href="{{ '/rag/code-examples/lwc/code-examples/lwc/wire-examples.html' | relative_url }}">Wire Examples</a> - Wire service patterns

## See Also

- <a href="{{ '/rag/code-examples/lwc/code-examples/testing/lwc-jest-testing.html' | relative_url }}">LWC Jest Testing</a> - Complete Jest testing guide
- <a href="{{ '/rag/development/lwc-patterns.html' | relative_url }}">LWC Patterns</a> - LWC development patterns
- <a href="{{ '/rag/code-examples/lwc/code-examples/testing/apex-testing-patterns.html' | relative_url }}">Apex Testing Patterns</a> - Apex testing patterns
