---
layout: default
title: Apex API Reference
description: This reference provides method signatures, parameters, return types, and usage examples for common Apex patterns used in Salesforce implementations
permalink: /rag/api-reference/apex-api-reference.html

**Best Practices**:
- ALL exceptions MUST be logged
- NO System.debug statements in production code
- Use structured logging format
- Integrate with centralized logging platforms (OpenSearch, Splunk)

---

## Standard Apex Classes

### Database

**Purpose**: Database operations with partial success handling

#### Methods

##### upsert(List<SObject> records, Schema.SObjectField externalIdField)
**Signature**: `public static Database.UpsertResult[] upsert(List<SObject> records, Schema.SObjectField externalIdField)`

**Parameters**: 
- `records` (List<SObject>): Records to upsert
- `externalIdField` (Schema.SObjectField): External ID field to use for matching

**Returns**: `Database.UpsertResult[]`: Array of upsert results

**Description**: Upserts records using external ID field. Returns results for partial success handling.

**Example**:
```apex
List<Contact> contacts = new List<Contact>{
    new Contact(ExternalId__c = 'EXT-001', LastName = 'Test1'),
    new Contact(ExternalId__c = 'EXT-002', LastName = 'Test2')
};
Database.UpsertResult[] results = Database.upsert(
    contacts,
    Contact.ExternalId__c,
    false // allOrNone = false for partial success
);
```

**Best Practices**:
- Use external ID fields for idempotent operations
- Set `allOrNone = false` for partial success handling
- Process results to handle partial failures
- Log errors for failed records

---

### Test

**Purpose**: Test execution and governor limit management

#### Methods

##### startTest()
**Signature**: `public static void startTest()`

**Returns**: `void`

**Description**: Marks the start of a test. Resets governor limits for testing.

**Example**:
```apex
@isTest
static void testMethod() {
    // Setup test data
    List<Contact> testContacts = createTestContacts();
    
    Test.startTest();
    // Execute code under test
    ContactUpdateService.processContacts(getContactIds(testContacts));
    Test.stopTest();
    
    // Verify results
    System.assertEquals(2, [SELECT COUNT() FROM Contact]);
}
```

##### stopTest()
**Signature**: `public static void stopTest()`

**Returns**: `void`

**Description**: Marks the end of a test. Executes any queued asynchronous jobs.

**Best Practices**:
- Use `Test.startTest()` and `Test.stopTest()` to reset governor limits
- Minimize logic within test blocks
- Execute async jobs between startTest and stopTest
- Verify results after stopTest

---

## Related Patterns

- <a href="{{ '/rag/development/soql-query-patterns.html' | relative_url }}">SOQL Patterns</a> - SOQL query patterns