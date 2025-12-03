---
layout: default
title: Domain Layer Examples
description: Code examples for Domain Layer Examples
permalink: /rag/code-examples/apex/domain-layer-examples.html
---

# Domain Layer Code Examples

> This file contains complete, working code examples for Apex Domain Layer patterns.  
> All examples are copy-paste ready and follow Salesforce best practices.

## Overview

The Domain Layer encapsulates object-specific business logic and validation. It can be called from triggers OR from Service layer, and should NOT contain SOQL queries or external callouts.

**Related Patterns**:
- <a href="{{ '/rag/code-examples/apex/Salesforce-RAG/rag/development/apex-patterns.html#apex-class-layering.html' | relative_url }}">Apex Class Layering</a>
- <a href="{{ '/rag/code-examples/apex/Salesforce-RAG/rag/development/apex-patterns.html#domain-layer.html' | relative_url }}">Domain Layer Pattern</a>

## Examples

### Example 1: Basic Domain Class
**Pattern**: Domain Layer with Validation  
**Use Case**: Object-specific validation and business rules  
**Complexity**: Basic  
**Related Patterns**: <a href="{{ '/rag/code-examples/apex/Salesforce-RAG/rag/development/apex-patterns.html#domain-layer.html' | relative_url }}">Domain Layer</a>

**Problem**: 
You need to validate Contact records and apply business rules before DML operations. The domain layer encapsulates Contact-specific logic.

**Solution**:
```apex
/**
 * Domain class for Contact object
 * Encapsulates Contact-specific business logic and validation
 */
public with sharing class ContactDomain {
    
    /**
     * Validates and prepares Contact records for update
     * @param contacts List of Contact records to validate
     * @throws ContactValidationException if validation fails
     */
    public static void validateAndPrepareForUpdate(List<Contact> contacts) {
        if (contacts == null || contacts.isEmpty()) {
            return;
        }
        
        for (Contact contact : contacts) {
            // Validate required fields
            if (String.isBlank(contact.LastName)) {
                throw new ContactValidationException('Last Name is required');
            }
            
            // Validate email format
            if (String.isNotBlank(contact.Email) && !isValidEmail(contact.Email)) {
                throw new ContactValidationException('Invalid email format: ' + contact.Email);
            }
            
            // Apply business rules
            applyBusinessRules(contact);
        }
    }
    
    /**
     * Validates Contact for insert
     * @param contacts List of Contact records to validate
     */
    public static void validateForInsert(List<Contact> contacts) {
        validateAndPrepareForUpdate(contacts);
        
        // Additional insert-specific validation
        for (Contact contact : contacts) {
            // Check for duplicates
            if (hasDuplicateEmail(contact.Email)) {
                throw new ContactValidationException('Contact with this email already exists');
            }
        }
    }
    
    /**
     * Applies business rules to Contact
     * @param contact Contact record to update
     */
    private static void applyBusinessRules(Contact contact) {
        // Business rule: Set default values
        if (String.isBlank(contact.Phone)) {
            contact.Phone = 'Not Provided';
        }
        
        // Business rule: Format name
        if (String.isNotBlank(contact.FirstName) && String.isNotBlank(contact.LastName)) {
            contact.FullName__c = contact.FirstName + ' ' + contact.LastName;
        }
    }
    
    /**
     * Validates email format
     * @param email Email address to validate
     * @return true if valid email format
     */
    private static Boolean isValidEmail(String email) {
        String emailRegex = '^[a-zA-Z0-9._|\\\\%#~`=?&/$^*!}{+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,4}$';
        Pattern emailPattern = Pattern.compile(emailRegex);
        return emailPattern.matcher(email).matches();
    }
    
    /**
     * Checks if email already exists (simplified - would use Selector in real implementation)
     * @param email Email to check
     * @return true if duplicate exists
     */
    private static Boolean hasDuplicateEmail(String email) {
        // Note: In real implementation, delegate to Selector layer
        // This is simplified for example
        return false;
    }
    
    /**
     * Custom exception for Contact validation errors
     */
    public class ContactValidationException extends Exception {}
}
```

**Explanation**:
- **Encapsulation**: All Contact-specific logic in one place
- **Validation**: Validates required fields and formats
- **Business Rules**: Applies business rules (default values, formatting)
- **Reusability**: Can be called from triggers or Service layer
- **No SOQL**: Delegates data access to Selector layer (shown in simplified form)

**Usage**:
```apex
// In a trigger
trigger ContactTrigger on Contact (before insert, before update) {
    if (Trigger.isBefore) {
        if (Trigger.isInsert) {
            ContactDomain.validateForInsert(Trigger.new);
        } else if (Trigger.isUpdate) {
            ContactDomain.validateAndPrepareForUpdate(Trigger.new);
        }
    }
}

// Or from Service layer
List<Contact> contacts = ContactSelector.selectByIds(contactIds);
ContactDomain.validateAndPrepareForUpdate(contacts);
update contacts;
```

**Test Example**:
```apex
@isTest
private class ContactDomainTest {
    
    @isTest
    static void testValidateAndPrepareForUpdate_Success() {
        List<Contact> contacts = new List<Contact>{
            new Contact(LastName = 'Test1', Email = 'test1@example.com'),
            new Contact(LastName = 'Test2', Email = 'test2@example.com')
        };
        
        Test.startTest();
        ContactDomain.validateAndPrepareForUpdate(contacts);
        Test.stopTest();
        
        // Verify business rules applied
        System.assertEquals('Not Provided', contacts[0].Phone, 'Default phone should be set');
    }
    
    @isTest
    static void testValidateAndPrepareForUpdate_MissingLastName() {
        List<Contact> contacts = new List<Contact>{
            new Contact(Email = 'test@example.com')
            // Missing LastName
        };
        
        Test.startTest();
        try {
            ContactDomain.validateAndPrepareForUpdate(contacts);
            System.assert(false, 'Should throw exception');
        } catch (ContactDomain.ContactValidationException e) {
            System.assert(e.getMessage().contains('Last Name is required'), 'Should throw validation error');
        }
        Test.stopTest();
    }
    
    @isTest
    static void testValidateAndPrepareForUpdate_InvalidEmail() {
        List<Contact> contacts = new List<Contact>{
            new Contact(LastName = 'Test', Email = 'invalid-email')
        };
        
        Test.startTest();
        try {
            ContactDomain.validateAndPrepareForUpdate(contacts);
            System.assert(false, 'Should throw exception');
        } catch (ContactDomain.ContactValidationException e) {
            System.assert(e.getMessage().contains('Invalid email format'), 'Should throw email validation error');
        }
        Test.stopTest();
    }
}
```

---

### Example 2: Domain with Service Layer Integration
**Pattern**: Domain Layer Called from Service Layer  
**Use Case**: Complex workflows with domain validation  
**Complexity**: Intermediate

**Problem**: 
Service layer needs to validate and prepare records using domain logic before processing.

**Solution**:
```apex
/**
 * Service layer using Domain layer for validation
 */
public with sharing class ContactUpdateService {
    
    public static List<Id> processContacts(Set<Id> contactIds) {
        // 1. Query using Selector
        List<Contact> contacts = ContactSelector.selectByIds(contactIds);
        
        // 2. Validate using Domain layer
        ContactDomain.validateAndPrepareForUpdate(contacts);
        
        // 3. Perform DML
        update contacts;
        
        // 4. Return processed IDs
        List<Id> processedIds = new List<Id>();
        for (Contact c : contacts) {
            processedIds.add(c.Id);
        }
        return processedIds;
    }
}
```

**Related Examples**: <a href="{{ '/rag/code-examples/apex/code-examples/apex/service-layer-examples.html' | relative_url }}">Service Layer Examples</a>

---

### Example 3: Domain Used in Trigger
**Pattern**: Domain Layer Called Directly from Trigger  
**Use Case**: Simple validation in triggers  
**Complexity**: Basic

**Problem**: 
Trigger needs simple validation without complex orchestration.

**Solution**:
```apex
trigger ContactTrigger on Contact (before insert, before update) {
    if (Trigger.isBefore) {
        if (Trigger.isInsert) {
            ContactDomain.validateForInsert(Trigger.new);
        } else if (Trigger.isUpdate) {
            ContactDomain.validateAndPrepareForUpdate(Trigger.new);
        }
    }
}
```

**Best Practices**:
- Use Domain layer directly in triggers for simple validation
- Use Service layer for complex workflows
- Keep triggers thin (delegate to Domain or Service)

---

## Common Patterns

### Pattern 1: Validation Methods
```apex
public static void validateForInsert(List<Contact> contacts) {
    // Insert-specific validation
}

public static void validateForUpdate(List<Contact> contacts) {
    // Update-specific validation
}

public static void validateAndPrepareForUpdate(List<Contact> contacts) {
    // Validation + business rule application
}
```

### Pattern 2: Business Rule Application
```apex
private static void applyBusinessRules(Contact contact) {
    // Set default values
    // Calculate derived fields
    // Apply formatting
    // Enforce business constraints
}
```

### Pattern 3: Helper Methods
```apex
private static Boolean isValidEmail(String email) {
    // Validation logic
}

private static String formatPhone(String phone) {
    // Formatting logic
}
```

---

## Best Practices

1. **Encapsulate object-specific logic** in Domain layer
2. **Validate before DML** operations
3. **Apply business rules** consistently
4. **Do NOT contain SOQL** (delegate to Selector layer)
5. **Do NOT contain external callouts** (delegate to Integration layer)
6. **Can be called from triggers OR Service layer**
7. **Use custom exceptions** for validation errors
8. **Keep methods focused** on single responsibility

---

## Related Patterns

- <a href="{{ '/rag/code-examples/apex/code-examples/apex/service-layer-examples.html' | relative_url }}">Service Layer Examples</a> - Service layer patterns
- <a href="{{ '/rag/code-examples/apex/code-examples/apex/selector-layer-examples.html' | relative_url }}">Selector Layer Examples</a> - Data access patterns
- <a href="{{ '/rag/development/apex-patterns.html' | relative_url }}">Apex Patterns</a> - Complete Apex patterns

