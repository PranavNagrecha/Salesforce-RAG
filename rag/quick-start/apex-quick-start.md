# Apex Quick Start Guide

> Getting started with Apex development in Salesforce.

## Overview

This quick-start guide provides step-by-step instructions for creating your first Apex classes following best practices.

## Prerequisites

- Salesforce Developer Edition or Sandbox
- VS Code with Salesforce Extensions
- Basic understanding of object-oriented programming

## Step 1: Create Your First Service Class

### What is a Service Class?

A Service class orchestrates workflows: query → validate → update → log. It delegates to Selector and Domain layers.

### Implementation

1. **Create the Service Class**:

```apex
/**
 * Service class for Contact operations
 */
public with sharing class ContactUpdateService {
    
    public static List<Id> processContacts(Set<Id> contactIds) {
        // 1. Query using Selector
        List<Contact> contacts = ContactSelector.selectById(contactIds);
        
        if (contacts.isEmpty()) {
            return new List<Id>();
        }
        
        // 2. Validate using Domain
        ContactDomain.validateAndPrepareForUpdate(contacts);
        
        // 3. Update records
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

2. **Save the file** as `ContactUpdateService.cls` in `force-app/main/default/classes/`

---

## Step 2: Create Selector Class

### What is a Selector Class?

A Selector class provides centralized SOQL queries with security enforcement.

### Implementation

1. **Create the Selector Class**:

```apex
/**
 * Selector class for Contact object
 */
public with sharing class ContactSelector {
    
    public static List<Contact> selectById(Set<Id> ids) {
        if (ids == null || ids.isEmpty()) {
            return new List<Contact>();
        }
        
        return [
            SELECT Id, Name, Email, Phone
            FROM Contact
            WHERE Id IN :ids
            WITH SECURITY_ENFORCED
            LIMIT 10000
        ];
    }
}
```

2. **Save the file** as `ContactSelector.cls`

---

## Step 3: Create Domain Class

### What is a Domain Class?

A Domain class encapsulates object-specific business logic and validation.

### Implementation

1. **Create the Domain Class**:

```apex
/**
 * Domain class for Contact object
 */
public with sharing class ContactDomain {
    
    public static void validateAndPrepareForUpdate(List<Contact> contacts) {
        if (contacts == null || contacts.isEmpty()) {
            return;
        }
        
        for (Contact contact : contacts) {
            // Validate required fields
            if (String.isBlank(contact.LastName)) {
                throw new ContactValidationException('Last Name is required');
            }
            
            // Apply business rules
            if (String.isBlank(contact.Phone)) {
                contact.Phone = 'Not Provided';
            }
        }
    }
    
    public class ContactValidationException extends Exception {}
}
```

2. **Save the file** as `ContactDomain.cls`

---

## Step 4: Create Test Class

### What is a Test Class?

A Test class verifies your Apex code works correctly and provides code coverage.

### Implementation

1. **Create the Test Class**:

```apex
@isTest
private class ContactUpdateServiceTest {
    
    @isTest
    static void testProcessContacts_Success() {
        // Create test data
        List<Contact> testContacts = new List<Contact>{
            new Contact(LastName = 'Test1', Email = 'test1@example.com'),
            new Contact(LastName = 'Test2', Email = 'test2@example.com')
        };
        insert testContacts;
        
        Set<Id> contactIds = new Set<Id>();
        for (Contact c : testContacts) {
            contactIds.add(c.Id);
        }
        
        Test.startTest();
        List<Id> result = ContactUpdateService.processContacts(contactIds);
        Test.stopTest();
        
        // Verify results
        System.assertEquals(2, result.size(), 'Should process 2 contacts');
    }
}
```

2. **Save the file** as `ContactUpdateServiceTest.cls`

---

## Step 5: Deploy and Test

### Deploy to Org

1. **Right-click** on the class file in VS Code
2. **Select** "SFDX: Deploy Source to Org"
3. **Verify** deployment succeeds

### Run Tests

1. **Open** Developer Console or use VS Code
2. **Run** test class: `ContactUpdateServiceTest`
3. **Verify** all tests pass and code coverage is 100%

---

## Complete Example

Here's a complete working example you can copy:

### Service Class
```apex
public with sharing class ContactUpdateService {
    public static List<Id> processContacts(Set<Id> contactIds) {
        List<Contact> contacts = ContactSelector.selectById(contactIds);
        if (contacts.isEmpty()) return new List<Id>();
        ContactDomain.validateAndPrepareForUpdate(contacts);
        update contacts;
        List<Id> processedIds = new List<Id>();
        for (Contact c : contacts) processedIds.add(c.Id);
        return processedIds;
    }
}
```

### Selector Class
```apex
public with sharing class ContactSelector {
    public static List<Contact> selectById(Set<Id> ids) {
        if (ids == null || ids.isEmpty()) return new List<Contact>();
        return [SELECT Id, Name, Email FROM Contact WHERE Id IN :ids WITH SECURITY_ENFORCED LIMIT 10000];
    }
}
```

### Domain Class
```apex
public with sharing class ContactDomain {
    public static void validateAndPrepareForUpdate(List<Contact> contacts) {
        if (contacts == null || contacts.isEmpty()) return;
        for (Contact c : contacts) {
            if (String.isBlank(c.LastName)) throw new ContactValidationException('Last Name required');
        }
    }
    public class ContactValidationException extends Exception {}
}
```

### Test Class
```apex
@isTest
private class ContactUpdateServiceTest {
    @isTest
    static void testProcessContacts_Success() {
        List<Contact> contacts = new List<Contact>{
            new Contact(LastName = 'Test1'),
            new Contact(LastName = 'Test2')
        };
        insert contacts;
        Set<Id> ids = new Set<Id>();
        for (Contact c : contacts) ids.add(c.Id);
        Test.startTest();
        List<Id> result = ContactUpdateService.processContacts(ids);
        Test.stopTest();
        System.assertEquals(2, result.size());
    }
}
```

---

## Next Steps

1. **Learn More Patterns**:
   - [Apex Patterns](../development/apex-patterns.md) - Complete Apex patterns
   - [Service Layer Examples](../code-examples/apex/service-layer-examples.md) - Service examples
   - [Selector Layer Examples](../code-examples/apex/selector-layer-examples.md) - Selector examples

2. **Explore Templates**:
   - [Service Template](../code-examples/templates/apex-service-template.md)
   - [Selector Template](../code-examples/templates/apex-selector-template.md)
   - [Domain Template](../code-examples/templates/apex-domain-template.md)

3. **Understand Best Practices**:
   - [Error Handling](../development/error-handling-and-logging.md)
   - [Governor Limits](../development/governor-limits-and-optimization.md)
   - [Testing Patterns](../testing/apex-testing-patterns.md)

---

## Related Resources

- [Apex Patterns](../development/apex-patterns.md) - Complete Apex patterns
- [Code Examples](../code-examples) - Working code examples
- [API Reference](../api-reference/apex-api-reference.md) - API reference

