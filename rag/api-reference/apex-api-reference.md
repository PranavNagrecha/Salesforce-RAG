---
title: "Apex API Reference"
level: "Intermediate"
tags:
  - api-reference
  - apex
  - reference
  - methods
last_reviewed: "2025-01-XX"
---

# Apex API Reference

> Quick reference for common Apex classes, methods, and patterns used in Salesforce development.

## Overview

This reference provides method signatures, parameters, return types, and usage examples for common Apex patterns used in Salesforce implementations.

## Service Layer Classes

### ContactUpdateService

**Purpose**: Service class for processing Contact updates with validation and business logic

#### Methods

##### processContacts(Set<Id> contactIds)
**Signature**: `public static List<Id> processContacts(Set<Id> contactIds)`

**Parameters**: 
- `contactIds` (Set<Id>): Contact IDs to update

**Returns**: `List<Id>`: List of processed Contact IDs

**Description**: Updates contacts with validation and business logic. Orchestrates workflow: query → validate → update → log.

**Example**:
```apex
Set<Id> contactIds = new Set<Id>{ '003000000000001', '003000000000002' };
List<Id> processedIds = ContactUpdateService.processContacts(contactIds);
```

**Related Patterns**: [Service Layer](/Salesforce-RAG/rag/development/apex-patterns.html#service-layer), <a href="{{ '/rag/api-reference/code-examples/apex/service-layer-examples.html' | relative_url }}">Service Layer Examples</a>

**Best Practices**:
- Always use `with sharing` or `without sharing` explicitly
- Delegate to Selector layer for queries
- Delegate to Domain layer for validation
- Handle errors gracefully with try-catch and logging
- Process collections (bulkification), not single records

---

## Domain Layer Classes

### ContactDomain

**Purpose**: Object-specific business logic and validation for Contact object

#### Methods

##### validateAndPrepareForUpdate(List<Contact> contacts)
**Signature**: `public static void validateAndPrepareForUpdate(List<Contact> contacts)`

**Parameters**: 
- `contacts` (List<Contact>): Contact records to validate and prepare

**Returns**: `void`

**Description**: Validates Contact records and applies business rules before update. Throws `ContactValidationException` if validation fails.

**Example**:
```apex
List<Contact> contacts = [SELECT Id, Email FROM Contact WHERE Id IN :contactIds];
ContactDomain.validateAndPrepareForUpdate(contacts);
update contacts;
```

**Related Patterns**: [Domain Layer](/Salesforce-RAG/rag/development/apex-patterns.html#domain-layer)

**Best Practices**:
- Should NOT contain SOQL queries (delegate to Selector layer)
- Should NOT contain external callouts (delegate to Integration layer)
- Can be called from triggers OR from Service layer
- Use directly in triggers for simple validation; use through Service layer for complex workflows

---

## Selector Layer Classes

### ContactSelector

**Purpose**: Data access layer for Contact object with security enforcement

#### Methods

##### selectById(Set<Id> ids)
**Signature**: `public static List<Contact> selectById(Set<Id> ids)`

**Parameters**: 
- `ids` (Set<Id>): Contact IDs to query

**Returns**: `List<Contact>`: List of Contact records

**Description**: Queries Contact records by ID with security enforcement. Uses `WITH SECURITY_ENFORCED` in SOQL query.

**Example**:
```apex
Set<Id> contactIds = new Set<Id>{ '003000000000001' };
List<Contact> contacts = ContactSelector.selectById(contactIds);
```

##### selectByExternalId(Set<String> externalIds)
**Signature**: `public static List<Contact> selectByExternalId(Set<String> externalIds)`

**Parameters**: 
- `externalIds` (Set<String>): External ID values to query

**Returns**: `List<Contact>`: List of Contact records

**Description**: Queries Contact records by External ID field with security enforcement.

**Example**:
```apex
Set<String> externalIds = new Set<String>{ 'EXT-001', 'EXT-002' };
List<Contact> contacts = ContactSelector.selectByExternalId(externalIds);
```

**Related Patterns**: [Selector Layer](/Salesforce-RAG/rag/development/apex-patterns.html#selector-layer)

**Best Practices**:
- ALL SOQL queries MUST use `WITH SECURITY_ENFORCED` or `WITH USER_MODE`
- Provide reusable query methods with specific method names
- Should NOT contain business logic (delegate to Domain layer)
- Should NOT contain external callouts (delegate to Integration layer)
- Use indexed fields in WHERE clauses for performance

---

## Integration Layer Classes

### RestIntegrationService

**Purpose**: External API integration with error handling and retry logic

#### Methods

##### makeCallout(String endpoint, String method, Map<String, Object> payload)
**Signature**: `public static HttpResponse makeCallout(String endpoint, String method, Map<String, Object> payload)`

**Parameters**: 
- `endpoint` (String): API endpoint (from Named Credential)
- `method` (String): HTTP method (GET, POST, PUT, DELETE)
- `payload` (Map<String, Object>): Request payload

**Returns**: `HttpResponse`: HTTP response from external system

**Description**: Makes HTTP callout to external system using Named Credentials. Includes error handling and retry logic.

**Example**:
```apex
Map<String, Object> payload = new Map<String, Object>{
    'name' => 'Test',
    'email' => 'test@example.com'
};
HttpResponse response = RestIntegrationService.makeCallout(
    'callout:MyNamedCredential/api/endpoint',
    'POST',
    payload
);
```

**Related Patterns**: [Integration Layer](/Salesforce-RAG/rag/development/apex-patterns.html#integration-layer)

**Best Practices**:
- Use Named Credentials for endpoints (NO hardcoded URLs)
- Centralize error handling and retry logic
- Should NOT contain business logic (delegate to Service layer)
- Should NOT contain SOQL queries (delegate to Selector layer)
- Handle authentication and token management

---

## Utility Classes

### LOG_LogMessageUtility

**Purpose**: Structured logging utility with platform event fallback

#### Methods

##### logInfo(String className, String methodName, String message)
**Signature**: `public static void logInfo(String className, String methodName, String message)`

**Parameters**: 
- `className` (String): Name of the class logging the message
- `methodName` (String): Name of the method logging the message
- `message` (String): Log message

**Returns**: `void`

**Description**: Logs informational message to custom logging object. Falls back to Platform Event if DML fails.

**Example**:
```apex
LOG_LogMessageUtility.logInfo(
    'ContactUpdateService',
    'processContacts',
    'Successfully updated ' + contacts.size() + ' contacts'
);
```

##### logError(String className, String methodName, String message, Exception e)
**Signature**: `public static void logError(String className, String methodName, String message, Exception e)`

**Parameters**: 
- `className` (String): Name of the class logging the error
- `methodName` (String): Name of the method logging the error
- `message` (String): Error message
- `e` (Exception): Exception object

**Returns**: `void`

**Description**: Logs error to custom logging object. Falls back to Platform Event if DML fails.

**Example**:
```apex
try {
    update contacts;
} catch (Exception e) {
    LOG_LogMessageUtility.logError(
        'ContactUpdateService',
        'processContacts',
        'Error updating contacts: ' + e.getMessage(),
        e
    );
    throw e;
}
```

**Related Patterns**: <a href="{{ '/rag/api-reference/development/error-handling-and-logging.html' | relative_url }}">Error Handling and Logging</a>

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

- <a href="{{ '/rag/api-reference/development/apex-patterns.html' | relative_url }}">Apex Patterns</a> - Complete Apex design patterns
- <a href="{{ '/rag/api-reference/code-examples/apex/service-layer-examples.html' | relative_url }}">Service Layer Examples</a> - Service layer code examples
- <a href="{{ '/rag/api-reference/development/error-handling-and-logging.html' | relative_url }}">Error Handling</a> - Error handling patterns
- <a href="{{ '/rag/api-reference/development/soql-query-patterns.html' | relative_url }}">SOQL Patterns</a> - SOQL query patterns

