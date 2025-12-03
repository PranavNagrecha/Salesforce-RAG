---
title: "Apex Testing Patterns"
level: "Intermediate"
tags:
  - testing
  - apex
  - test-classes
  - test-data-factories
last_reviewed: "2025-01-XX"
---

# Apex Testing Patterns

> Comprehensive testing patterns and examples for Apex development.

## Overview

This guide provides testing patterns, best practices, and examples for Apex test classes, covering unit testing, integration testing, and test data factories.

**Related Patterns**:
- <a href="{{ '/rag/testing/project-methods/testing-strategy.html' | relative_url }}">Testing Strategy</a> - Overall testing strategy
- <a href="{{ '/rag/development/apex-patterns.html' | relative_url }}">Apex Patterns</a> - Apex development patterns

## Core Principles

### Test Class Structure
- Use `@isTest` annotation
- Make test classes `private`
- Use descriptive test method names: `test[MethodName]_[Scenario]`
- Use `Test.startTest()` and `Test.stopTest()` to reset governor limits
- Minimize logic within test blocks

### Test Data Factories
- Create reusable test data factory methods
- Avoid `@SeeAllData` annotation
- Use factories for consistent test data
- Support bulk test data creation

### Assertions
- Always include assertions
- Use new Salesforce Assert Class: `System.Assert`
- Verify both positive and negative scenarios
- Test edge cases and error conditions

## Patterns

### Pattern 1: Basic Test Class Structure

**When to use**: Standard test class for any Apex class

**Implementation**:
```apex
@isTest
private class ContactServiceTest {
    
    @isTest
    static void testProcessContacts_Success() {
        // Arrange: Create test data
        List<Contact> testContacts = createTestContacts(2);
        insert testContacts;
        
        Set<Id> contactIds = new Set<Id>();
        for (Contact c : testContacts) {
            contactIds.add(c.Id);
        }
        
        // Act: Execute code under test
        Test.startTest();
        List<Id> result = ContactService.processContacts(contactIds);
        Test.stopTest();
        
        // Assert: Verify results
        System.assertEquals(2, result.size(), 'Should process 2 contacts');
    }
    
    private static List<Contact> createTestContacts(Integer count) {
        List<Contact> contacts = new List<Contact>();
        for (Integer i = 0; i < count; i++) {
            contacts.add(new Contact(
                LastName = 'Test' + i,
                Email = 'test' + i + '@example.com'
            ));
        }
        return contacts;
    }
}
```

**Best Practices**:
- Use Arrange-Act-Assert pattern
- Create test data in setup methods or factories
- Use descriptive test method names
- Include assertions with messages

---

### Pattern 2: Test Data Factory

**When to use**: Reusable test data across multiple test classes

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
    
    /**
     * Creates test Account with Contacts
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

**Best Practices**:
- Make factory methods `public static`
- Support both insert and non-insert scenarios
- Create related records together
- Use consistent naming conventions

---

### Pattern 3: Bulk Testing

**When to use**: Testing bulkification and governor limits

**Implementation**:
```apex
@isTest
private class ContactServiceTest {
    
    @isTest
    static void testProcessContacts_Bulk() {
        // Create bulk test data (200+ records)
        List<Contact> testContacts = TestDataFactory.createContacts(200, true);
        
        Set<Id> contactIds = new Set<Id>();
        for (Contact c : testContacts) {
            contactIds.add(c.Id);
        }
        
        Test.startTest();
        List<Id> result = ContactService.processContacts(contactIds);
        Test.stopTest();
        
        // Verify bulk processing
        System.assertEquals(200, result.size(), 'Should process all 200 contacts');
        
        // Verify no governor limit errors
        // (Test will fail if limits exceeded)
    }
}
```

**Best Practices**:
- Test with 200+ records to verify bulkification
- Verify all records processed correctly
- Test governor limit compliance
- Use `Test.startTest()` and `Test.stopTest()` to reset limits

---

### Pattern 4: Error Scenario Testing

**When to use**: Testing error handling and exceptions

**Implementation**:
```apex
@isTest
private class ContactServiceTest {
    
    @isTest
    static void testProcessContacts_InvalidInput() {
        // Test with null input
        Test.startTest();
        try {
            ContactService.processContacts(null);
            System.assert(false, 'Should throw exception');
        } catch (IllegalArgumentException e) {
            System.assert(e.getMessage().contains('cannot be null'), 'Should throw appropriate error');
        }
        Test.stopTest();
    }
    
    @isTest
    static void testProcessContacts_EmptySet() {
        // Test with empty set
        Test.startTest();
        List<Id> result = ContactService.processContacts(new Set<Id>());
        Test.stopTest();
        
        System.assertEquals(0, result.size(), 'Should return empty list');
    }
}
```

**Best Practices**:
- Test all error scenarios
- Verify exception types and messages
- Test edge cases (null, empty, invalid input)
- Use try-catch for expected exceptions

---

### Pattern 5: Mocking and Dependency Injection

**When to use**: Testing classes with external dependencies

**Implementation**:
```apex
// Interface for dependency
public interface IHttpService {
    HttpResponse makeCallout(String endpoint);
}

// Implementation
public class HttpService implements IHttpService {
    public HttpResponse makeCallout(String endpoint) {
        // Real implementation
    }
}

// Mock implementation
@isTest
private class MockHttpService implements IHttpService {
    public HttpResponse makeCallout(String endpoint) {
        HttpResponse res = new HttpResponse();
        res.setStatusCode(200);
        res.setBody('{"success": true}');
        return res;
    }
}

// Service using dependency injection
public class ContactSyncService {
    private IHttpService httpService;
    
    public ContactSyncService(IHttpService httpService) {
        this.httpService = httpService;
    }
    
    public void syncContact(Contact contact) {
        HttpResponse res = httpService.makeCallout('/api/contacts');
        // Process response
    }
}

// Test with mock
@isTest
private class ContactSyncServiceTest {
    @isTest
    static void testSyncContact_Success() {
        MockHttpService mockHttp = new MockHttpService();
        ContactSyncService service = new ContactSyncService(mockHttp);
        
        Contact testContact = TestDataFactory.createContacts(1, true)[0];
        
        Test.startTest();
        service.syncContact(testContact);
        Test.stopTest();
        
        // Verify sync completed
    }
}
```

**Best Practices**:
- Use interfaces for dependencies
- Create mock implementations for testing
- Inject dependencies via constructor
- Test both success and error scenarios with mocks

---

### Pattern 6: Test Coverage Strategies

**When to use**: Ensuring comprehensive test coverage

**Implementation**:
```apex
@isTest
private class ContactServiceTest {
    
    // Test all public methods
    @isTest
    static void testProcessContacts_Success() { }
    
    @isTest
    static void testProcessContacts_Error() { }
    
    @isTest
    static void testProcessContacts_Bulk() { }
    
    // Test all branches
    @isTest
    static void testProcessContacts_WithAccount() { }
    
    @isTest
    static void testProcessContacts_WithoutAccount() { }
    
    // Test edge cases
    @isTest
    static void testProcessContacts_SingleRecord() { }
    
    @isTest
    static void testProcessContacts_MaxRecords() { }
}
```

**Best Practices**:
- Aim for 100% code coverage (minimum 90%)
- Test all public methods
- Test all code branches (if/else, switch)
- Test edge cases and error scenarios
- Use code coverage tools to identify gaps

---

## Common Patterns Summary

### Test Method Naming
- `test[MethodName]_[Scenario]` - Standard pattern
- Examples: `testProcessContacts_Success`, `testProcessContacts_Error`, `testProcessContacts_Bulk`

### Test Structure
1. **Arrange**: Create test data
2. **Act**: Execute code under test
3. **Assert**: Verify results

### Test Data Creation
- Use test data factories
- Support bulk data creation
- Create related records together

### Assertions
- Always include assertions
- Use descriptive assertion messages
- Verify both positive and negative scenarios

---

## Best Practices

1. **Use `@isTest` annotation** for all test classes
2. **Make test classes `private`**
3. **Use descriptive test method names**
4. **Use `Test.startTest()` and `Test.stopTest()`** to reset governor limits
5. **Minimize logic within test blocks**
6. **Create test data factories** for reusability
7. **Test with bulk data** (200+ records)
8. **Include assertions** in all tests
9. **Test error scenarios** and edge cases
10. **Aim for 100% code coverage** (minimum 90%)
11. **Avoid `@SeeAllData` annotation**
12. **Use mocking** for external dependencies

---

## Q&A

### Q: What is the minimum code coverage required for Apex classes?

**A**: The **minimum code coverage is 75%** for deployment, but best practice is to **aim for 100% coverage** (with a minimum of 90%). Higher coverage reduces risk of bugs in production and ensures all code paths are tested. Focus on quality over quantity - meaningful assertions are more important than just hitting lines.

### Q: Should I use @SeeAllData annotation in test classes?

**A**: **No, avoid `@SeeAllData` annotation**. Test classes should create their own test data using test data factories. Using `@SeeAllData` makes tests dependent on org data, unreliable, and difficult to maintain. Always create test data within test methods or use test data factories.

### Q: What is the purpose of Test.startTest() and Test.stopTest()?

**A**: `Test.startTest()` and `Test.stopTest()` **reset governor limits** for code between these calls. This allows you to test governor limit scenarios and ensures your test code has fresh limits. Minimize logic within these blocks - they're primarily for testing governor limit scenarios.

### Q: How do I test bulk operations (200+ records)?

**A**: Test bulk operations by: (1) **Creating 200+ test records** using test data factories, (2) **Calling your method with bulk data**, (3) **Asserting results for all records**, (4) **Testing both positive and negative scenarios**. This ensures your code handles bulk operations correctly and doesn't hit governor limits.

### Q: What is a test data factory and why should I use one?

**A**: A **test data factory** is a reusable class or method that creates test data. Use factories to: (1) **Ensure consistent test data** across tests, (2) **Reduce code duplication**, (3) **Make tests easier to maintain**, (4) **Support bulk test data creation**. Create factory methods for common test data scenarios.

### Q: How do I test private methods in Apex?

**A**: **Test private methods indirectly** by testing the public methods that call them. If you need to test private methods directly, you can use the `@TestVisible` annotation to make them accessible to test classes, but prefer testing through public interfaces when possible.

### Q: Should I test getters and setters?

**A**: **Generally no**, unless they contain business logic. Simple getters and setters don't need explicit testing. However, if getters/setters contain validation, transformation, or business logic, they should be tested. Focus testing on methods with business logic.

### Q: How do I test async methods (@future, Queueable, Batchable)?

**A**: Test async methods by: (1) **Calling the async method** in your test, (2) **Using `Test.startTest()` and `Test.stopTest()`** to execute async methods synchronously in tests, (3) **Asserting results** after `Test.stopTest()`. For Batchable classes, use `Database.executeBatch()` and `Test.stopTest()` to execute the batch.

### Q: What assertions should I include in test methods?

**A**: Include assertions that verify: (1) **Expected outcomes** (records created, updated, deleted), (2) **Data correctness** (field values are correct), (3) **Error handling** (exceptions thrown when expected), (4) **Business logic** (calculations, validations work correctly). Use the new Salesforce `System.Assert` class for assertions.

### Q: How do I test error scenarios and exceptions?

**A**: Test error scenarios by: (1) **Creating test data that triggers errors** (invalid data, missing required fields), (2) **Using try-catch blocks** to verify exceptions are thrown, (3) **Asserting exception types and messages**, (4) **Testing both positive and negative scenarios**. Ensure your code handles errors gracefully.

## Related Patterns

- <a href="{{ '/rag/testing/project-methods/testing-strategy.html' | relative_url }}">Testing Strategy</a> - Overall testing strategy
- <a href="{{ '/rag/development/apex-patterns.html' | relative_url }}">Apex Patterns</a> - Apex development patterns
- <a href="{{ '/rag/testing/code-examples/templates/test-class-template.html' | relative_url }}">Test Class Template</a> - Test class template

