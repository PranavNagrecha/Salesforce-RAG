---
layout: default
title: LWC Service Layer Code Examples
description: LWC service layer patterns provide reusable utility functions for common operations like data transformation, validation, formatting, and business logic
permalink: /rag/development/lwc-patterns.html#data-access-patterns' | relative_url }}">LWC Data Access Patterns</a>

**Problem**:
You need to format dates, currency, and other data types consistently across multiple components.

**Solution**:

**JavaScript** (`formattingService.js`):
```javascript
/**
 * Service for formatting data in LWC components
 */
export class FormattingService {
    /**
     * Formats a date to a readable string
     * @param {Date|string} date - Date to format
     * @param {string} locale - Locale string (default: 'en-US')
     * @returns {string} Formatted date string
     */
    static formatDate(date, locale = 'en-US') {
        if (!date) return '';
        
        const dateObj = typeof date === 'string' ? new Date(date) : date;
        if (isNaN(dateObj.getTime())) return '';
        
        return new Intl.DateTimeFormat(locale, {
            year: 'numeric',
            month: 'short',
            day: 'numeric'
        }).format(dateObj);
    }

    /**
     * Formats a currency value
     * @param {number} amount - Amount to format
     * @param {string} currency - Currency code (default: 'USD')
     * @param {string} locale - Locale string (default: 'en-US')
     * @returns {string} Formatted currency string
     */
    static formatCurrency(amount, currency = 'USD', locale = 'en-US') {
        if (amount === null || amount === undefined) return '';
        
        return new Intl.NumberFormat(locale, {
            style: 'currency',
            currency: currency
        }).format(amount);
    }

    /**
     * Formats a phone number
     * @param {string} phone - Phone number to format
     * @returns {string} Formatted phone number
     */
    static formatPhone(phone) {
        if (!phone) return '';
        
        // Remove all non-numeric characters
        const cleaned = phone.replace(/\D/g, '');
        
        // Format as (XXX) XXX-XXXX
        if (cleaned.length === 10) {
            return `(${cleaned.slice(0, 3)}) ${cleaned.slice(3, 6)}-${cleaned.slice(6)}`;
        }
        
        return phone;
    }

    /**
     * Formats a percentage value
     * @param {number} value - Percentage value (0-100)
     * @param {number} decimals - Number of decimal places (default: 1)
     * @returns {string} Formatted percentage string
     */
    static formatPercentage(value, decimals = 1) {
        if (value === null || value === undefined) return '';
        
        return `${value.toFixed(decimals)}%`;
    }
}
```

**Usage in Component** (`contactDisplay.js`):
```javascript
import { LightningElement, api, wire } from 'lwc';
import { getRecord } from 'lightning/uiRecordApi';
import CONTACT_PHONE_FIELD from '@salesforce/schema/Contact.Phone';
import { FormattingService } from 'c/formattingService';

export default class ContactDisplay extends LightningElement {
    @api recordId;

    @wire(getRecord, { recordId: '$recordId', fields: [CONTACT_PHONE_FIELD] })
    contact;

    get formattedPhone() {
        const phone = this.contact?.data?.fields?.Phone?.value;
        return FormattingService.formatPhone(phone);
    }
}
```

**Explanation**:
- Centralizes formatting logic for reuse across components
- Uses JavaScript Intl API for locale-aware formatting
- Handles null/undefined values gracefully
- Provides consistent formatting across the application

**Best Practices**:
- Create service classes for reusable utility functions
- Use static methods for stateless operations
- Handle null/undefined values consistently
- Use JavaScript Intl API for locale-aware formatting

### Example 2: Validation Service

**Pattern**: Utility service for data validation
**Use Case**: Validating user input before submission
**Complexity**: Intermediate
**Related Patterns**: <a href="{{ '/rag/development/lwc-patterns.html' | relative_url }}">LWC Patterns</a>

**Problem**:
You need to validate user input consistently across multiple components.

**Solution**:

**JavaScript** (`validationService.js`):
```javascript
/**
 * Service for validating data in LWC components
 */
export class ValidationService {
    /**
     * Validates an email address
     * @param {string} email - Email to validate
     * @returns {object} Validation result with isValid and message
     */
    static validateEmail(email) {
        if (!email) {
            return { isValid: false, message: 'Email is required' };
        }

        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(email)) {
            return { isValid: false, message: 'Invalid email format' };
        }

        return { isValid: true, message: '' };
    }

    /**
     * Validates a phone number
     * @param {string} phone - Phone number to validate
     * @returns {object} Validation result with isValid and message
     */
    static validatePhone(phone) {
        if (!phone) {
            return { isValid: false, message: 'Phone number is required' };
        }

        const cleaned = phone.replace(/\D/g, '');
        if (cleaned.length < 10) {
            return { isValid: false, message: 'Phone number must have at least 10 digits' };
        }

        return { isValid: true, message: '' };
    }

    /**
     * Validates a required field
     * @param {any} value - Value to validate
     * @param {string} fieldName - Name of the field for error message
     * @returns {object} Validation result with isValid and message
     */
    static validateRequired(value, fieldName) {
        if (value === null || value === undefined || value === '') {
            return { isValid: false, message: `${fieldName} is required` };
        }

        return { isValid: true, message: '' };
    }

    /**
     * Validates a number range
     * @param {number} value - Value to validate
     * @param {number} min - Minimum value
     * @param {number} max - Maximum value
     * @returns {object} Validation result with isValid and message
     */
    static validateRange(value, min, max) {
        if (value === null || value === undefined) {
            return { isValid: false, message: 'Value is required' };
        }

        if (value < min || value > max) {
            return { isValid: false, message: `Value must be between ${min} and ${max}` };
        }

        return { isValid: true, message: '' };
    }

    /**
     * Validates multiple fields and returns combined result
     * @param {Array} validations - Array of validation results
     * @returns {object} Combined validation result
     */
    static combineValidations(validations) {
        const allValid = validations.every(v => v.isValid);
        const messages = validations
            .filter(v => !v.isValid)
            .map(v => v.message)
            .join(', ');

        return {
            isValid: allValid,
            message: messages
        };
    }
}
```

**Usage in Component** (`contactForm.js`):
```javascript
import { LightningElement, track } from 'lwc';
import { ValidationService } from 'c/validationService';
import { ShowToastEvent } from 'lightning/platformShowToastEvent';

export default class ContactForm extends LightningElement {
    @track email = '';
    @track phone = '';
    @track errors = {};

    handleEmailChange(event) {
        this.email = event.target.value;
        this.validateField('email', this.email);
    }

    handlePhoneChange(event) {
        this.phone = event.target.value;
        this.validateField('phone', this.phone);
    }

    validateField(fieldName, value) {
        let validation;
        
        switch (fieldName) {
            case 'email':
                validation = ValidationService.validateEmail(value);
                break;
            case 'phone':
                validation = ValidationService.validatePhone(value);
                break;
            default:
                return;
        }

        if (!validation.isValid) {
            this.errors = { ...this.errors, [fieldName]: validation.message };
        } else {
            const newErrors = { ...this.errors };
            delete newErrors[fieldName];
            this.errors = newErrors;
        }
    }

    handleSubmit() {
        const emailValidation = ValidationService.validateEmail(this.email);
        const phoneValidation = ValidationService.validatePhone(this.phone);
        
        const combined = ValidationService.combineValidations([emailValidation, phoneValidation]);
        
        if (!combined.isValid) {
            this.showToast('Validation Error', combined.message, 'error');
            return;
        }

        // Proceed with submission
        this.submitForm();
    }

    submitForm() {
        // Form submission logic
    }

    showToast(title, message, variant) {
        const evt = new ShowToastEvent({ title, message, variant });
        this.dispatchEvent(evt);
    }
}
```

**Explanation**:
- Centralizes validation logic for consistency
- Returns structured validation results
- Supports combining multiple validations
- Provides clear error messages

**Best Practices**:
- Use service classes for reusable validation logic
- Return structured validation results
- Provide clear, user-friendly error messages
- Support combining multiple validations

### Example 3: Data Transformation Service

**Pattern**: Utility service for data transformation
**Use Case**: Transforming data between formats (e.g., API response to component data)
**Complexity**: Intermediate
**Related Patterns**: <a href="{{ '/rag/development/lwc-patterns.html' | relative_url }}">LWC Patterns</a>

**Problem**:
You need to transform data from Apex responses or API calls into formats suitable for component display.

**Solution**:

**JavaScript** (`transformationService.js`):
```javascript
/**
 * Service for transforming data in LWC components
 */
export class TransformationService {
    /**
     * Transforms a list of records into option list format
     * @param {Array} records - Records to transform
     * @param {string} labelField - Field to use as label
     * @param {string} valueField - Field to use as value
     * @returns {Array} Transformed option list
     */
    static transformToOptions(records, labelField, valueField) {
        if (!records || records.length === 0) {
            return [];
        }

        return records.map(record => ({
            label: record[labelField],
            value: record[valueField]
        }));
    }

    /**
     * Groups records by a field value
     * @param {Array} records - Records to group
     * @param {string} groupField - Field to group by
     * @returns {object} Grouped records
     */
    static groupBy(records, groupField) {
        if (!records || records.length === 0) {
            return {};
        }

        return records.reduce((groups, record) => {
            const key = record[groupField];
            if (!groups[key]) {
                groups[key] = [];
            }
            groups[key].push(record);
            return groups;
        }, {});
    }

    /**
     * Sorts records by a field
     * @param {Array} records - Records to sort
     * @param {string} sortField - Field to sort by
     * @param {string} direction - Sort direction ('asc' or 'desc')
     * @returns {Array} Sorted records
     */
    static sortBy(records, sortField, direction = 'asc') {
        if (!records || records.length === 0) {
            return [];
        }

        const sorted = [...records].sort((a, b) => {
            const aValue = a[sortField];
            const bValue = b[sortField];
            
            if (aValue < bValue) return direction === 'asc' ? -1 : 1;
            if (aValue > bValue) return direction === 'asc' ? 1 : -1;
            return 0;
        });

        return sorted;
    }

    /**
     * Filters records by a condition
     * @param {Array} records - Records to filter
     * @param {Function} predicate - Filter function
     * @returns {Array} Filtered records
     */
    static filter(records, predicate) {
        if (!records || records.length === 0) {
            return [];
        }

        return records.filter(predicate);
    }

    /**
     * Maps records to a new structure
     * @param {Array} records - Records to map
     * @param {Function} mapper - Mapping function
     * @returns {Array} Mapped records
     */
    static map(records, mapper) {
        if (!records || records.length === 0) {
            return [];
        }

        return records.map(mapper);
    }
}
```

**Usage in Component** (`contactList.js`):
```javascript
import { LightningElement, wire } from 'lwc';
import getContacts from '@salesforce/apex/ContactService.getContacts';
import { TransformationService } from 'c/transformationService';

export default class ContactList extends LightningElement {
    contacts = [];
    filteredContacts = [];
    sortField = 'Name';
    sortDirection = 'asc';

    @wire(getContacts)
    wiredContacts({ data, error }) {
        if (data) {
            this.contacts = data;
            this.applyFilters();
        } else if (error) {
            console.error('Error loading contacts:', error);
        }
    }

    handleSort(event) {
        this.sortField = event.detail.field;
        this.sortDirection = event.detail.direction;
        this.applyFilters();
    }

    handleFilter(event) {
        this.filterValue = event.detail.value;
        this.applyFilters();
    }

    applyFilters() {
        let result = [...this.contacts];

        // Apply filter
        if (this.filterValue) {
            result = TransformationService.filter(result, contact => 
                contact.Name.toLowerCase().includes(this.filterValue.toLowerCase())
            );
        }

        // Apply sort
        result = TransformationService.sortBy(result, this.sortField, this.sortDirection);

        this.filteredContacts = result;
    }
}
```

**Explanation**:
- Provides reusable data transformation utilities
- Supports common operations (filter, sort, group, map)
- Handles empty arrays gracefully
- Maintains immutability by creating new arrays

**Best Practices**:
- Use service classes for data transformation logic
- Maintain immutability (don't mutate input arrays)
- Handle edge cases (null, empty arrays)
- Provide clear, reusable transformation functions

## Related Examples

- <a href="{{ '/rag/development/lwc-patterns.html' | relative_url }}">LWC Patterns</a> - Complete LWC development patterns
- <a href="{{ '/rag/code-examples/lwc/mcp-knowledge/lwc-best-practices.html' | relative_url }}">LWC Best Practices</a> - Official LWC best practices
- <a href="{{ '/rag/api-reference/lwc-api-reference.html' | relative_url }}">LWC API Reference</a> - Complete LWC API reference
