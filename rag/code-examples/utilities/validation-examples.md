---
layout: default
title: Validation Code Examples
description: Data validation ensures data quality and prevents invalid data from entering the system
permalink: /rag/development/formulas-validation-rules.html' | relative_url }}">Formulas and Validation Rules</a>

**Problem**:
You need to validate field values before saving records.

**Solution**:

**Apex** (`ValidationService.cls`):
```apex
/**
 * Service for field-level validation
 */
public with sharing class ValidationService {
    
    /**
     * Validates email address format
     * @param email Email to validate
     * @return Validation result
     */
    public static ValidationResult validateEmail(String email) {
        ValidationResult result = new ValidationResult();
        
        if (String.isBlank(email)) {
            result.isValid = false;
            result.errorMessage = 'Email is required';
            return result;
        }
        
        // Basic email format validation
        String emailRegex = '^[a-zA-Z0-9._|\\\\%#~`=?&/$!*+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$';
        Pattern emailPattern = Pattern.compile(emailRegex);
        Matcher emailMatcher = emailPattern.matcher(email);
        
        if (!emailMatcher.matches()) {
            result.isValid = false;
            result.errorMessage = 'Invalid email format';
            return result;
        }
        
        result.isValid = true;
        return result;
    }
    
    /**
     * Validates phone number format
     * @param phone Phone to validate
     * @return Validation result
     */
    public static ValidationResult validatePhone(String phone) {
        ValidationResult result = new ValidationResult();
        
        if (String.isBlank(phone)) {
            result.isValid = true; // Phone is optional
            return result;
        }
        
        // Remove formatting characters
        String cleanedPhone = phone.replaceAll('[^0-9]', '');
        
        // Validate length (10 digits for US phone)
        if (cleanedPhone.length() < 10 || cleanedPhone.length() > 15) {
            result.isValid = false;
            result.errorMessage = 'Phone number must be between 10 and 15 digits';
            return result;
        }
        
        result.isValid = true;
        return result;
    }
    
    /**
     * Validates required field
     * @param value Field value
     * @param fieldName Field name for error message
     * @return Validation result
     */
    public static ValidationResult validateRequired(Object value, String fieldName) {
        ValidationResult result = new ValidationResult();
        
        if (value == null || 
            (value instanceof String && String.isBlank((String) value))) {
            result.isValid = false;
            result.errorMessage = fieldName + ' is required';
            return result;
        }
        
        result.isValid = true;
        return result;
    }
    
    /**
     * Validates number range
     * @param value Number value
     * @param min Minimum value
     * @param max Maximum value
     * @param fieldName Field name for error message
     * @return Validation result
     */
    public static ValidationResult validateRange(Decimal value, Decimal min, Decimal max, String fieldName) {
        ValidationResult result = new ValidationResult();
        
        if (value == null) {
            result.isValid = false;
            result.errorMessage = fieldName + ' is required';
            return result;
        }
        
        if (value < min || value > max) {
            result.isValid = false;
            result.errorMessage = fieldName + ' must be between ' + min + ' and ' + max;
            return result;
        }
        
        result.isValid = true;
        return result;
    }
    
    /**
     * Validation result class
     */
    public class ValidationResult {
        public Boolean isValid { get; set; }
        public String errorMessage { get; set; }
        
        public ValidationResult() {
            this.isValid = true;
            this.errorMessage = '';
        }
    }
}
```

**Usage**:
```apex
// Validate email
ValidationService.ValidationResult emailResult = ValidationService.validateEmail(contact.Email);
if (!emailResult.isValid) {
    contact.addError('Email', emailResult.errorMessage);
}

// Validate phone
ValidationService.ValidationResult phoneResult = ValidationService.validatePhone(contact.Phone);
if (!phoneResult.isValid) {
    contact.addError('Phone', phoneResult.errorMessage);
}
```

**Best Practices**:
- Validate fields before DML
- Provide clear error messages
- Use consistent validation logic
- Return structured validation results

### Example 2: Record-Level Validation

**Pattern**: Validating entire records
**Use Case**: Ensuring records meet business rules
**Complexity**: Intermediate
**Related Patterns**: <a href="{{ '/rag/development/formulas-validation-rules.html' | relative_url }}">Formulas and Validation Rules</a>

**Problem**:
You need to validate entire records with multiple fields and business rules.

**Solution**:

**Apex** (`ContactValidationService.cls`):
```apex
/**
 * Service for Contact record validation
 */
public with sharing class ContactValidationService {
    
    /**
     * Validates Contact record
     * @param contact Contact to validate
     * @return List of validation errors
     */
    public static List<String> validateContact(Contact contact) {
        List<String> errors = new List<String>();
        
        // Validate required fields
        ValidationService.ValidationResult lastNameResult = ValidationService.validateRequired(
            contact.LastName, 'Last Name'
        );
        if (!lastNameResult.isValid) {
            errors.add(lastNameResult.errorMessage);
        }
        
        // Validate email if provided
        if (String.isNotBlank(contact.Email)) {
            ValidationService.ValidationResult emailResult = ValidationService.validateEmail(contact.Email);
            if (!emailResult.isValid) {
                errors.add(emailResult.errorMessage);
            }
        }
        
        // Validate phone if provided
        if (String.isNotBlank(contact.Phone)) {
            ValidationService.ValidationResult phoneResult = ValidationService.validatePhone(contact.Phone);
            if (!phoneResult.isValid) {
                errors.add(phoneResult.errorMessage);
            }
        }
        
        // Business rule: Email or Phone required
        if (String.isBlank(contact.Email) && String.isBlank(contact.Phone)) {
            errors.add('Either Email or Phone is required');
        }
        
        // Business rule: Mailing Address required for certain record types
        if (contact.RecordTypeId == getRecordTypeId('Contact', 'Student')) {
            if (String.isBlank(contact.MailingStreet) || String.isBlank(contact.MailingCity)) {
                errors.add('Mailing Address is required for Student contacts');
            }
        }
        
        return errors;
    }
    
    /**
     * Validates and adds errors to Contact record
     * @param contact Contact to validate
     * @return True if valid, false otherwise
     */
    public static Boolean validateAndAddErrors(Contact contact) {
        List<String> errors = validateContact(contact);
        
        if (!errors.isEmpty()) {
            for (String error : errors) {
                contact.addError(error);
            }
            return false;
        }
        
        return true;
    }
    
    /**
     * Gets Record Type ID by name
     * @param objectType Object API name
     * @param recordTypeName Record Type name
     * @return Record Type ID
     */
    private static Id getRecordTypeId(String objectType, String recordTypeName) {
        Schema.RecordTypeInfo recordTypeInfo = Schema.getGlobalDescribe()
            .get(objectType)
            .getDescribe()
            .getRecordTypeInfosByName()
            .get(recordTypeName);
        
        return recordTypeInfo != null ? recordTypeInfo.getRecordTypeId() : null;
    }
}
```

**Usage**:
```apex
// Validate contact before insert/update
if (!ContactValidationService.validateAndAddErrors(contact)) {
    // Validation failed - errors added to contact
    return;
}

// Proceed with DML
insert contact;
```

**Best Practices**:
- Validate records before DML
- Add errors to records using addError()
- Return validation results for programmatic handling
- Include business rules in validation

### Example 3: Bulk Validation

**Pattern**: Validating multiple records efficiently
**Use Case**: Validating bulk data operations
**Complexity**: Intermediate
**Related Patterns**: <a href="{{ '/rag/data-governance/data-quality-stewardship.html' | relative_url }}">Data Quality Stewardship</a>

**Problem**:
You need to validate multiple records efficiently in bulk operations.

**Solution**:

**Apex** (`BulkValidationService.cls`):
```apex
/**
 * Service for bulk record validation
 */
public with sharing class BulkValidationService {
    
    /**
     * Validates list of contacts
     * @param contacts Contacts to validate
     * @return Map of contact index to validation errors
     */
    public static Map<Integer, List<String>> validateContacts(List<Contact> contacts) {
        Map<Integer, List<String>> errorsByIndex = new Map<Integer, List<String>>();
        
        for (Integer i = 0; i < contacts.size(); i++) {
            Contact contact = contacts[i];
            List<String> errors = ContactValidationService.validateContact(contact);
            
            if (!errors.isEmpty()) {
                errorsByIndex.put(i, errors);
            }
        }
        
        return errorsByIndex;
    }
    
    /**
     * Validates and adds errors to contacts
     * @param contacts Contacts to validate
     * @return Number of valid contacts
     */
    public static Integer validateAndAddErrors(List<Contact> contacts) {
        Integer validCount = 0;
        
        for (Integer i = 0; i < contacts.size(); i++) {
            Contact contact = contacts[i];
            List<String> errors = ContactValidationService.validateContact(contact);
            
            if (errors.isEmpty()) {
                validCount++;
            } else {
                // Add first error to contact (addError only allows one at a time in bulk)
                contact.addError(errors[0]);
                
                // Log additional errors
                if (errors.size() > 1) {
                    LOG_LogMessageUtility.logWarning(
                        'BulkValidationService',
                        'validateAndAddErrors',
                        'Contact ' + i + ' has multiple validation errors: ' + String.join(errors, ', ')
                    );
                }
            }
        }
        
        return validCount;
    }
    
    /**
     * Separates valid and invalid contacts
     * @param contacts Contacts to validate
     * @return Map with 'valid' and 'invalid' keys
     */
    public static Map<String, List<Contact>> separateValidAndInvalid(List<Contact> contacts) {
        Map<String, List<Contact>> result = new Map<String, List<Contact>>{
            'valid' => new List<Contact>(),
            'invalid' => new List<Contact>()
        };
        
        for (Contact contact : contacts) {
            List<String> errors = ContactValidationService.validateContact(contact);
            
            if (errors.isEmpty()) {
                result.get('valid').add(contact);
            } else {
                result.get('invalid').add(contact);
            }
        }
        
        return result;
    }
}
```

**Usage**:
```apex
// Validate bulk contacts
Map<String, List<Contact>> separated = BulkValidationService.separateValidAndInvalid(contacts);

// Process valid contacts
if (!separated.get('valid').isEmpty()) {
    insert separated.get('valid');
}

// Handle invalid contacts
if (!separated.get('invalid').isEmpty()) {
    LOG_LogMessageUtility.logWarning(
        'ContactService',
        'processContacts',
        'Skipped ' + separated.get('invalid').size() + ' invalid contacts'
    );
}
```

**Best Practices**:
- Validate records in bulk efficiently
- Separate valid and invalid records
- Process valid records, handle invalid separately
- Log validation failures for review

## Related Examples

- <a href="{{ '/rag/development/formulas-validation-rules.html' | relative_url }}">Formulas and Validation Rules</a> - Validation rule patterns
- <a href="{{ '/rag/data-governance/data-quality-stewardship.html' | relative_url }}">Data Quality Stewardship</a> - Data quality patterns

