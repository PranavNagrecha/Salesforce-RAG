# Test Data Factory Patterns

> Patterns and examples for creating reusable test data factories in Apex.

## Overview

Test data factories provide reusable methods for creating test data, ensuring consistency and reducing duplication across test classes.

**Related Patterns**:
- [Apex Testing Patterns](rag/testing/apex-testing-patterns.md) - Testing patterns
- [Testing Strategy](rag/project-methods/testing-strategy.md) - Testing strategy

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

## Related Patterns

- [Apex Testing Patterns](rag/testing/apex-testing-patterns.md) - Testing patterns
- [Testing Strategy](rag/project-methods/testing-strategy.md) - Testing strategy
- [Test Class Template](rag/code-examples/templates/test-class-template.md) - Test class template

