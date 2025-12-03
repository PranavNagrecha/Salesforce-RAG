# LWC Jest Testing Code Examples

> This file contains complete, working Jest test examples for Lightning Web Components.
> All examples follow Salesforce Jest testing best practices.

## Overview

Jest is the testing framework for Lightning Web Components. These examples demonstrate how to test LWC components, including rendering, user interactions, wire adapters, and Apex method calls.

**Related Patterns**:
- [LWC Jest Testing](../testing/lwc-jest-testing.md) - Complete LWC testing guide
- [LWC Patterns](../development/lwc-patterns.md) - LWC development patterns

## Examples

### Example 1: Basic Component Rendering Test

**Pattern**: Testing component rendering and basic functionality
**Use Case**: Verifying component displays correctly
**Complexity**: Basic
**Related Patterns**: [LWC Jest Testing](../testing/lwc-jest-testing.md)

**Problem**:
You need to test that a component renders correctly and displays expected content.

**Solution**:

**Component** (`contactDisplay.js`):
```javascript
import { LightningElement, api, wire } from 'lwc';
import { getRecord } from 'lightning/uiRecordApi';
import CONTACT_NAME_FIELD from '@salesforce/schema/Contact.Name';

const FIELDS = [CONTACT_NAME_FIELD];

export default class ContactDisplay extends LightningElement {
    @api recordId;

    @wire(getRecord, { recordId: '$recordId', fields: FIELDS })
    contact;

    get contactName() {
        return this.contact?.data?.fields?.Name?.value || '';
    }
}
```

**Test** (`contactDisplay.test.js`):
```javascript
import { createElement } from 'lwc';
import ContactDisplay from 'c/contactDisplay';
import { getRecord } from 'lightning/uiRecordApi';

// Mock Lightning Data Service
jest.mock(
    '@salesforce/apex/ContactService.getContact',
    () => {
        return {
            default: jest.fn()
        };
    },
    { virtual: true }
);

// Mock getRecord wire adapter
jest.mock('lightning/uiRecordApi', () => ({
    getRecord: jest.fn()
}));

describe('c-contact-display', () => {
    afterEach(() => {
        while (document.body.firstChild) {
            document.body.removeChild(document.body.firstChild);
        }
        jest.clearAllMocks();
    });

    it('renders contact name when data is available', () => {
        const RECORD_ID = '003000000000001AAA';
        const CONTACT_NAME = 'John Doe';

        // Mock wire adapter data
        getRecord.emit({
            data: {
                fields: {
                    Name: { value: CONTACT_NAME }
                }
            }
        });

        const element = createElement('c-contact-display', {
            is: ContactDisplay
        });
        element.recordId = RECORD_ID;
        document.body.appendChild(element);

        return Promise.resolve().then(() => {
            const nameElement = element.shadowRoot.querySelector('p');
            expect(nameElement.textContent).toBe(CONTACT_NAME);
        });
    });

    it('handles error state', () => {
        const RECORD_ID = '003000000000001AAA';

        // Mock wire adapter error
        getRecord.emit({
            error: {
                body: { message: 'Record not found' }
            }
        });

        const element = createElement('c-contact-display', {
            is: ContactDisplay
        });
        element.recordId = RECORD_ID;
        document.body.appendChild(element);

        return Promise.resolve().then(() => {
            const errorElement = element.shadowRoot.querySelector('.error');
            expect(errorElement).toBeTruthy();
        });
    });
});
```

**Explanation**:
- Mocks wire adapters using `jest.mock`
- Tests component rendering with mock data
- Tests error handling
- Uses `Promise.resolve()` to wait for async operations

**Best Practices**:
- Mock all external dependencies (wire adapters, Apex methods)
- Test both success and error scenarios
- Clean up DOM after each test
- Use descriptive test names

### Example 2: Testing User Interactions

**Pattern**: Testing user interactions and event handling
**Use Case**: Verifying button clicks and form submissions work correctly
**Complexity**: Intermediate
**Related Patterns**: [LWC Jest Testing](../testing/lwc-jest-testing.md)

**Problem**:
You need to test that user interactions (clicks, input changes) work correctly.

**Solution**:

**Component** (`contactForm.js`):
```javascript
import { LightningElement } from 'lwc';
import saveContact from '@salesforce/apex/ContactService.saveContact';

export default class ContactForm extends LightningElement {
    email = '';

    handleEmailChange(event) {
        this.email = event.target.value;
    }

    handleSave() {
        saveContact({ email: this.email })
            .then(() => {
                this.dispatchEvent(new CustomEvent('saved'));
            })
            .catch(error => {
                console.error('Error saving contact:', error);
            });
    }
}
```

**Test** (`contactForm.test.js`):
```javascript
import { createElement } from 'lwc';
import ContactForm from 'c/contactForm';
import saveContact from '@salesforce/apex/ContactService.saveContact';

// Mock Apex method
jest.mock(
    '@salesforce/apex/ContactService.saveContact',
    () => {
        return {
            default: jest.fn()
        };
    },
    { virtual: true }
);

describe('c-contact-form', () => {
    afterEach(() => {
        while (document.body.firstChild) {
            document.body.removeChild(document.body.firstChild);
        }
        jest.clearAllMocks();
    });

    it('updates email on input change', () => {
        const element = createElement('c-contact-form', {
            is: ContactForm
        });
        document.body.appendChild(element);

        const emailInput = element.shadowRoot.querySelector('lightning-input');
        emailInput.value = 'test@example.com';
        emailInput.dispatchEvent(new CustomEvent('change'));

        return Promise.resolve().then(() => {
            expect(element.email).toBe('test@example.com');
        });
    });

    it('calls Apex method on save', () => {
        const EMAIL = 'test@example.com';
        saveContact.mockResolvedValue({});

        const element = createElement('c-contact-form', {
            is: ContactForm
        });
        document.body.appendChild(element);

        // Set email value
        const emailInput = element.shadowRoot.querySelector('lightning-input');
        emailInput.value = EMAIL;
        emailInput.dispatchEvent(new CustomEvent('change'));

        return Promise.resolve().then(() => {
            const saveButton = element.shadowRoot.querySelector('lightning-button');
            saveButton.click();

            return Promise.resolve().then(() => {
                expect(saveContact).toHaveBeenCalledWith({ email: EMAIL });
            });
        });
    });

    it('dispatches saved event on successful save', () => {
        saveContact.mockResolvedValue({});

        const element = createElement('c-contact-form', {
            is: ContactForm
        });
        document.body.appendChild(element);

        const handler = jest.fn();
        element.addEventListener('saved', handler);

        const saveButton = element.shadowRoot.querySelector('lightning-button');
        saveButton.click();

        return Promise.resolve().then(() => {
            expect(handler).toHaveBeenCalled();
        });
    });
});
```

**Explanation**:
- Tests user input changes
- Tests button click interactions
- Mocks Apex method calls
- Verifies event dispatching
- Uses `Promise.resolve()` for async operations

**Best Practices**:
- Test all user interactions
- Verify event dispatching
- Mock Apex method calls
- Test both success and error scenarios

## Related Examples

- [Component Examples](lwc/component-examples.md) - LWC component implementations
- [Apex Testing Patterns](../testing/apex-testing-patterns.md) - Apex test patterns

## See Also

- [LWC Jest Testing](../testing/lwc-jest-testing.md) - Complete LWC testing guide
- [LWC Patterns](../development/lwc-patterns.md) - LWC development patterns

