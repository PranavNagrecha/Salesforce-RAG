# LWC Service Layer Code Examples

> This file contains complete, working code examples for LWC service layer patterns.
> All examples demonstrate how to structure reusable service logic in LWC components.

## Overview

LWC service layer patterns provide reusable business logic that can be shared across multiple components. These patterns help organize code, improve testability, and enable code reuse.

**Related Patterns**:
- [LWC Patterns](../development/lwc-patterns.md) - LWC development patterns
- [Service Layer Examples](apex/service-layer-examples.md) - Apex service layer patterns

## Examples

### Example 1: Data Transformation Service

**Pattern**: Centralized data transformation logic
**Use Case**: Transforming data for display across multiple components
**Complexity**: Basic
**Related Patterns**: [LWC Patterns](../development/lwc-patterns.md)

**Problem**:
You need to transform data consistently across multiple components.

**Solution**:

**JavaScript** (`dataTransformService.js`):
```javascript
/**
 * Service for transforming data for display
 */
export default class DataTransformService {
    
    /**
     * Formats a date for display
     * @param {Date|string} dateValue - Date to format
     * @param {string} format - Format string (default: 'MM/DD/YYYY')
     * @returns {string} Formatted date string
     */
    static formatDate(dateValue, format = 'MM/DD/YYYY') {
        if (!dateValue) {
            return '';
        }
        
        const date = new Date(dateValue);
        if (isNaN(date.getTime())) {
            return '';
        }
        
        const month = String(date.getMonth() + 1).padStart(2, '0');
        const day = String(date.getDate()).padStart(2, '0');
        const year = date.getFullYear();
        
        return format
            .replace('MM', month)
            .replace('DD', day)
            .replace('YYYY', year);
    }
    
    /**
     * Formats currency for display
     * @param {number} amount - Amount to format
     * @param {string} currency - Currency code (default: 'USD')
     * @returns {string} Formatted currency string
     */
    static formatCurrency(amount, currency = 'USD') {
        if (amount === null || amount === undefined) {
            return '';
        }
        
        return new Intl.NumberFormat('en-US', {
            style: 'currency',
            currency: currency
        }).format(amount);
    }
    
    /**
     * Truncates text to specified length
     * @param {string} text - Text to truncate
     * @param {number} maxLength - Maximum length
     * @returns {string} Truncated text
     */
    static truncateText(text, maxLength = 50) {
        if (!text || text.length <= maxLength) {
            return text;
        }
        
        return text.substring(0, maxLength) + '...';
    }
}
```

**Usage in Component**:
```javascript
import { LightningElement } from 'lwc';
import DataTransformService from 'c/dataTransformService';

export default class MyComponent extends LightningElement {
    formattedDate = DataTransformService.formatDate(new Date());
    formattedAmount = DataTransformService.formatCurrency(1234.56);
}
```

**Explanation**:
- Centralizes data transformation logic
- Reusable across multiple components
- Easy to test and maintain
- Follows single responsibility principle

**Best Practices**:
- Keep service methods pure (no side effects)
- Use static methods for utility functions
- Document method parameters and return values
- Handle edge cases (null, undefined, invalid input)

### Example 2: Validation Service

**Pattern**: Centralized validation logic
**Use Case**: Validating user input consistently
**Complexity**: Intermediate
**Related Patterns**: [LWC Patterns](../development/lwc-patterns.md)

**Problem**:
You need to validate user input consistently across multiple components.

**Solution**:

**JavaScript** (`validationService.js`):
```javascript
/**
 * Service for validating user input
 */
export default class ValidationService {
    
    /**
     * Validates email address
     * @param {string} email - Email to validate
     * @returns {object} Validation result with isValid and message
     */
    static validateEmail(email) {
        if (!email) {
            return {
                isValid: false,
                message: 'Email is required'
            };
        }
        
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(email)) {
            return {
                isValid: false,
                message: 'Invalid email format'
            };
        }
        
        return {
            isValid: true,
            message: ''
        };
    }
    
    /**
     * Validates phone number
     * @param {string} phone - Phone to validate
     * @returns {object} Validation result
     */
    static validatePhone(phone) {
        if (!phone) {
            return {
                isValid: false,
                message: 'Phone is required'
            };
        }
        
        const phoneRegex = /^[\d\s\-\(\)]+$/;
        if (!phoneRegex.test(phone) || phone.replace(/\D/g, '').length < 10) {
            return {
                isValid: false,
                message: 'Invalid phone number format'
            };
        }
        
        return {
            isValid: true,
            message: ''
        };
    }
    
    /**
     * Validates required field
     * @param {*} value - Value to validate
     * @param {string} fieldName - Field name for error message
     * @returns {object} Validation result
     */
    static validateRequired(value, fieldName) {
        if (value === null || value === undefined || value === '') {
            return {
                isValid: false,
                message: `${fieldName} is required`
            };
        }
        
        return {
            isValid: true,
            message: ''
        };
    }
}
```

**Usage in Component**:
```javascript
import { LightningElement, track } from 'lwc';
import ValidationService from 'c/validationService';

export default class ContactForm extends LightningElement {
    @track email = '';
    @track emailError = '';

    handleEmailChange(event) {
        this.email = event.target.value;
        const validation = ValidationService.validateEmail(this.email);
        this.emailError = validation.isValid ? '' : validation.message;
    }
}
```

**Explanation**:
- Centralizes validation logic
- Consistent validation across components
- Returns structured validation results
- Easy to extend with new validation rules

**Best Practices**:
- Return consistent validation result structure
- Provide clear error messages
- Validate on user input (real-time feedback)
- Combine multiple validations as needed

## Related Examples

- [Component Examples](lwc/component-examples.md) - LWC component implementations
- [Wire Examples](lwc/wire-examples.md) - Wire adapter patterns
- [Apex Service Layer Examples](apex/service-layer-examples.md) - Server-side service patterns

## See Also

- [LWC Patterns](../development/lwc-patterns.md) - Complete LWC development patterns
- [LWC Best Practices](../mcp-knowledge/lwc-best-practices.md) - Official LWC best practices

