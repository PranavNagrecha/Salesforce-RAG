---
layout: default
title: Domain Class Template
description: Documentation for Domain Class Template
permalink: /rag/code-examples/templates/apex-domain-template.html
---

# Domain Class Template

**Use Case**: Basic domain class with validation and business rules

**Template**:
```apex
/**
 * Domain class for [ObjectName] object
 * Encapsulates [ObjectName]-specific business logic and validation
 */
public with sharing class [ObjectName]Domain {
    
    /**
     * Validates and prepares [ObjectName] records for update
     * @param records List of [ObjectName] records to validate
     * @throws [ObjectName]ValidationException if validation fails
     */
    public static void validateAndPrepareForUpdate(List<[ObjectName]> records) {
        if (records == null || records.isEmpty()) {
            return;
        }
        
        for ([ObjectName] record : records) {
            // Validate required fields
            if (String.isBlank(record.[RequiredField]__c)) {
                throw new [ObjectName]ValidationException('[RequiredField] is required');
            }
            
            // Validate field formats
            if (String.isNotBlank(record.[FieldToValidate]__c) && !isValid[Field](record.[FieldToValidate]__c)) {
                throw new [ObjectName]ValidationException('Invalid [Field] format: ' + record.[FieldToValidate]__c);
            }
            
            // Apply business rules
            applyBusinessRules(record);
        }
    }
    
    /**
     * Validates [ObjectName] for insert
     * @param records List of [ObjectName] records to validate
     */
    public static void validateForInsert(List<[ObjectName]> records) {
        validateAndPrepareForUpdate(records);
        
        // Additional insert-specific validation
        for ([ObjectName] record : records) {
            // Insert-specific checks
        }
    }
    
    /**
     * Applies business rules to [ObjectName]
     * @param record [ObjectName] record to update
     */
    private static void applyBusinessRules([ObjectName] record) {
        // Business rule: Set default values
        if (String.isBlank(record.[FieldWithDefault]__c)) {
            record.[FieldWithDefault]__c = '[DefaultValue]';
        }
        
        // Business rule: Calculate derived fields
        if (String.isNotBlank(record.[Field1]__c) && String.isNotBlank(record.[Field2]__c)) {
            record.[DerivedField]__c = record.[Field1]__c + ' ' + record.[Field2]__c;
        }
    }
    
    /**
     * Validates [Field] format
     * @param [field] [Field] value to validate
     * @return true if valid format
     */
    private static Boolean isValid[Field](String [field]) {
        // Validation logic
        return true;
    }
    
    /**
     * Custom exception for [ObjectName] validation errors
     */
    public class [ObjectName]ValidationException extends Exception {}
}
```

**Customization Points**:
- Replace `[ObjectName]` with actual object name (e.g., `Contact`)
- Replace `[RequiredField]` with actual required field
- Replace `[FieldToValidate]` with field to validate
- Replace `[Field]` with field name for validation method
- Replace `[FieldWithDefault]` with field that needs default
- Replace `[DefaultValue]` with default value
- Replace `[Field1]`, `[Field2]`, `[DerivedField]` with actual fields
- Add validation logic as needed
- Add business rules as needed

**Related Patterns**:
- <a href="{{ '/rag/development/apex-patterns#domain-layer.html' | relative_url }}">Apex Patterns</a>

