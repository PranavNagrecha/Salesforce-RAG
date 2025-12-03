---
title: "Test Data Factory Patterns"
level: "Intermediate"
tags:
  - testing
  - apex
  - test-data-factories
  - test-classes
last_reviewed: "2025-01-XX"
---

# Test Data Factory Patterns

> Patterns and examples for creating reusable test data factories in Apex.

## Overview

Test data factories provide reusable methods for creating test data, ensuring consistency and reducing duplication across test classes.

**Related Patterns**:
- <a href="{{ '/rag/testing/testing/apex-testing-patterns.html' | relative_url }}">Apex Testing Patterns</a> - Testing patterns
- <a href="{{ '/rag/testing/project-methods/testing-strategy.html' | relative_url }}">Testing Strategy</a> - Testing strategy

## Core Principles

### Factory Design
- Make factory methods `public static`
- Support both insert and non-insert scenarios
- Create related records together
- Use consistent naming conventions
- Support bulk data creation

### Data Consistency
- Use consistent field values
- Set required fields automatically
- Handle relationships correctly
- Support customization via parameters

## Patterns

### Pattern 1: Basic Factory Method

**When to use**: Simple test data creation

**Implementation**:
```apex
@isTest
public class TestDataFactory {
    
    /**
     * Creates test Contact records
     * @param count Number of contacts to create
     * @param doInsert Whether to insert records
     * @return List of Contact records
     */
    public static List<Contact> createContacts(Integer count, Boolean doInsert) {
        List<Contact> contacts = new List<Contact>();
        
        for (Integer i = 0; i < count; i++) {
            contacts.add(new Contact(
                LastName = 'TestContact' + i,
                Email = 'test' + i + '@example.com',
                Phone = '555-000' + i
            ));
        }
        
        if (doInsert) {
            insert contacts;
        }
        
        return contacts;
    }
}
```

**Usage**:
```apex
@isTest
private class MyTestClass {
    @isTest
    static void testMethod() {
        List<Contact> contacts = TestDataFactory.createContacts(5, true);
        // Use contacts in test
    }
}
```

---

### Pattern 2: Factory with Relationships

**When to use**: Creating related records together

**Implementation**:
```apex
@isTest
public class TestDataFactory {
    
    /**
     * Creates Account with related Contacts
     * @param accountName Account name
     * @param contactCount Number of contacts
     * @return Account with related contacts
     */
    public static Account createAccountWithContacts(String accountName, Integer contactCount) {
        Account acc = new Account(Name = accountName);
        insert acc;
        
        List<Contact> contacts = new List<Contact>();
        for (Integer i = 0; i < contactCount; i++) {
            contacts.add(new Contact(
                LastName = 'Contact' + i,
                AccountId = acc.Id
            ));
        }
        insert contacts;
        
        return acc;
    }
    
    /**
     * Creates Contact with Account
     * @param contactLastName Contact last name
     * @param accountName Account name
     * @return Contact with related Account
     */
    public static Contact createContactWithAccount(String contactLastName, String accountName) {
        Account acc = new Account(Name = accountName);
        insert acc;
        
        Contact con = new Contact(
            LastName = contactLastName,
            AccountId = acc.Id
        );
        insert con;
        
        return con;
    }
}
```

**Usage**:
```apex
@isTest
private class MyTestClass {
    @isTest
    static void testMethod() {
        Account acc = TestDataFactory.createAccountWithContacts('Test Account', 5);
        // Use account and contacts
    }
}
```

---

### Pattern 3: Factory with Customization

**When to use**: Allowing test-specific customization

**Implementation**:
```apex
@isTest
public class TestDataFactory {
    
    /**
     * Creates test Contact with customizable fields
     * @param count Number of contacts
     * @param doInsert Whether to insert
     * @param customFields Map of field API names to values
     * @return List of Contact records
     */
    public static List<Contact> createContacts(
        Integer count, 
        Boolean doInsert, 
        Map<String, Object> customFields
    ) {
        List<Contact> contacts = new List<Contact>();
        
        for (Integer i = 0; i < count; i++) {
            Contact con = new Contact(
                LastName = 'TestContact' + i,
                Email = 'test' + i + '@example.com'
            );
            
            // Apply custom fields
            if (customFields != null) {
                for (String fieldName : customFields.keySet()) {
                    con.put(fieldName, customFields.get(fieldName));
                }
            }
            
            contacts.add(con);
        }
        
        if (doInsert) {
            insert contacts;
        }
        
        return contacts;
    }
}
```

**Usage**:
```apex
@isTest
private class MyTestClass {
    @isTest
    static void testMethod() {
        Map<String, Object> customFields = new Map<String, Object>{
            'Phone' => '555-1234',
            'Title' => 'Manager'
        };
        
        List<Contact> contacts = TestDataFactory.createContacts(5, true, customFields);
        // Contacts have custom Phone and Title values
    }
}
```

---

### Pattern 4: Bulk Data Factory

**When to use**: Creating large datasets for bulk testing

**Implementation**:
```apex
@isTest
public class TestDataFactory {
    
    /**
     * Creates bulk test Contacts
     * @param count Number of contacts (supports large numbers)
     * @return List of Contact records (not inserted)
     */
    public static List<Contact> createBulkContacts(Integer count) {
        List<Contact> contacts = new List<Contact>();
        
        for (Integer i = 0; i < count; i++) {
            contacts.add(new Contact(
                LastName = 'BulkContact' + i,
                Email = 'bulk' + i + '@example.com'
            ));
        }
        
        return contacts;
    }
    
    /**
     * Creates and inserts bulk Contacts in batches
     * @param count Total number of contacts
     * @return List of inserted Contact IDs
     */
    public static List<Id> createAndInsertBulkContacts(Integer count) {
        List<Id> contactIds = new List<Id>();
        Integer batchSize = 200;
        
        for (Integer i = 0; i < count; i += batchSize) {
            List<Contact> batch = new List<Contact>();
            
            for (Integer j = i; j < Math.min(i + batchSize, count); j++) {
                batch.add(new Contact(
                    LastName = 'BulkContact' + j,
                    Email = 'bulk' + j + '@example.com'
                ));
            }
            
            insert batch;
            
            for (Contact c : batch) {
                contactIds.add(c.Id);
            }
        }
        
        return contactIds;
    }
}
```

**Usage**:
```apex
@isTest
private class MyTestClass {
    @isTest
    static void testBulkProcessing() {
        List<Id> contactIds = TestDataFactory.createAndInsertBulkContacts(500);
        // Test with 500 contacts
    }
}
```

---

## Best Practices

1. **Make factory methods `public static`** for reusability
2. **Support both insert and non-insert scenarios** via `doInsert` parameter
3. **Create related records together** in single factory methods
4. **Use consistent naming conventions** across factories
5. **Support bulk data creation** for bulk testing
6. **Allow customization** via parameters or maps
7. **Set required fields automatically** to avoid test failures
8. **Handle relationships correctly** (parent-child, lookups)
9. **Document factory methods** with clear parameter descriptions
10. **Use descriptive method names** that indicate what they create

---

## Q&A

### Q: What is a test data factory and why should I use one?

**A**: A **test data factory** is a reusable class or method that creates test data for testing. Use factories to: (1) **Ensure consistent test data** across tests, (2) **Reduce code duplication**, (3) **Make tests easier to maintain**, (4) **Support bulk test data creation**, (5) **Handle relationships correctly** (parent-child, lookups).

### Q: Should test data factory methods be static?

**A**: **Yes, make factory methods `public static`**. This allows you to call them without instantiating the factory class, makes them easy to use across test classes, and follows common Apex patterns. Static methods are ideal for utility functions like test data creation.

### Q: Should factory methods insert records or return records?

**A**: **Support both scenarios**. Create factory methods that can either insert records immediately or return records for customization before insertion. Use parameters like `Boolean doInsert` to control behavior. This provides flexibility for different test scenarios.

### Q: How do I handle relationships in test data factories?

**A**: Handle relationships by: (1) **Creating parent records first**, (2) **Passing parent record IDs to child record factories**, (3) **Creating related records together** in a single factory method, (4) **Using consistent field values** for relationship fields. Consider creating composite factory methods that create entire object hierarchies.

### Q: How do I support bulk data creation in test data factories?

**A**: Support bulk data creation by: (1) **Accepting a count parameter** for number of records to create, (2) **Using loops to create multiple records**, (3) **Using lists and bulk DML operations**, (4) **Ensuring unique field values** (e.g., unique names, emails) for each record. This enables testing bulk operations (200+ records).

### Q: Should I use default values or require all parameters in factory methods?

**A**: **Use default values for optional fields, require parameters for critical fields**. This makes factories easy to use for simple cases while allowing customization for complex scenarios. Document which parameters are required vs optional.

### Q: How do I make test data factories customizable?

**A**: Make factories customizable by: (1) **Accepting parameter maps** for field values, (2) **Providing method overloads** for different scenarios, (3) **Using builder patterns** for complex objects, (4) **Allowing field-by-field customization** while providing sensible defaults.

### Q: Should I create one factory class or multiple factory classes?

**A**: **Create one factory class per domain or object group**. Group related factories together (e.g., all Account/Contact factories in one class, all Case factories in another). This keeps factories organized and makes them easier to find and maintain.

### Q: How do I ensure test data factories set required fields automatically?

**A**: Ensure factories set required fields by: (1) **Identifying all required fields** for each object, (2) **Setting default values** for required fields in factory methods, (3) **Documenting required fields** in factory method comments, (4) **Testing factories** to ensure they don't fail due to missing required fields.

### Q: What naming conventions should I use for test data factory methods?

**A**: Use **descriptive method names** that indicate what they create, such as `createAccount()`, `createAccountWithContact()`, `createBulkAccounts()`. Follow consistent naming patterns across all factory methods. Consider including object type and key characteristics in the method name.

## Related Patterns

- <a href="{{ '/rag/testing/testing/apex-testing-patterns.html' | relative_url }}">Apex Testing Patterns</a> - Testing patterns
- <a href="{{ '/rag/testing/project-methods/testing-strategy.html' | relative_url }}">Testing Strategy</a> - Testing strategy
- <a href="{{ '/rag/testing/code-examples/templates/test-class-template.html' | relative_url }}">Test Class Template</a> - Test class template

