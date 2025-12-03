---
layout: default
title: Common Apex Errors and Solutions
description: This guide provides solutions for common Apex errors encountered during Salesforce development, including error messages, causes, solutions, and prevention strategies
permalink: /rag/troubleshooting/common-apex-errors.html
---

# Common Apex Errors and Solutions

> Troubleshooting guide for common Apex errors with solutions and prevention strategies.

## Overview

This guide provides solutions for common Apex errors encountered during Salesforce development, including error messages, causes, solutions, and prevention strategies.

## UNABLE_TO_LOCK_ROW

**Error Message**: `UNABLE_TO_LOCK_ROW: unable to obtain exclusive access to this record`

**Common Causes**:
- Concurrent updates to the same record
- Long-running transactions holding locks
- Batch jobs updating the same records simultaneously
- Multiple processes trying to update the same record at once

**Solutions**:

### Solution 1: Retry Logic with Exponential Backoff

**Before: No retry**
```apex
update contacts; // Fails if lock conflict
```

**After: With retry**
```apex
public static void updateWithRetry(List<Contact> contacts) {
    Integer maxRetries = 3;
    Integer retryCount = 0;
    Boolean success = false;
    
    while (retryCount < maxRetries && !success) {
        try {
            update contacts;
            success = true;
        } catch (DmlException e) {
            if (e.getMessage().contains('UNABLE_TO_LOCK_ROW') && retryCount < maxRetries - 1) {
                retryCount++;
                // Exponential backoff: 100ms, 200ms, 400ms
                Long waitTime = (Long)Math.pow(2, retryCount - 1) * 100;
                // Note: Cannot use Thread.sleep in Apex, use Queueable instead
            } else {
                throw e;
            }
        }
    }
}
```

**Queueable Retry Pattern**:
```apex
public class ContactUpdateRetryQueueable implements Queueable {
    private List<Contact> contacts;
    private Integer retryCount;
    private static final Integer MAX_RETRIES = 3;
    
    public ContactUpdateRetryQueueable(List<Contact> contacts, Integer retryCount) {
        this.contacts = contacts;
        this.retryCount = retryCount;
    }
    
    public void execute(QueueableContext context) {
        try {
            update contacts;
        } catch (DmlException e) {
            if (e.getMessage().contains('UNABLE_TO_LOCK_ROW') && retryCount < MAX_RETRIES) {
                // Enqueue retry with delay
                System.enqueueJob(new ContactUpdateRetryQueueable(contacts, retryCount + 1));
            } else {
                LOG_LogMessageUtility.logError(
                    'ContactUpdateRetryQueueable',
                    'execute',
                    'Failed after ' + retryCount + ' retries: ' + e.getMessage(),
                    e
                );
                throw e;
            }
        }
    }
}
```

### Solution 2: Use Queueable for Async Processing

```apex
// Instead of synchronous update
update contacts;

// Use Queueable
System.enqueueJob(new ContactUpdateQueueable(contacts));
```

### Solution 3: Reduce Transaction Scope

```apex
// Bad: Large transaction scope
public static void processAllContacts() {
    List<Contact> allContacts = [SELECT Id FROM Contact];
    // Long processing...
    update allContacts; // Large lock scope
}

// Good: Smaller transaction scope
public static void processContactsInBatches() {
    List<Contact> contacts = [SELECT Id FROM Contact LIMIT 200];
    update contacts; // Smaller lock scope
    // Process next batch if needed
}
```

**Prevention**:
- Implement retry logic for DML operations
- Use Queueable for async processing when possible
- Reduce transaction scope (process in smaller batches)
- Avoid long-running transactions
- Use Platform Events for decoupled processing

**Related Patterns**: <a href="{{ '/rag/development/locking-and-concurrency-strategies.html' | relative_url }}">Locking and Concurrency</a>

---

## LIST_EXCEPTION: List index out of bounds

**Error Message**: `ListException: List index out of bounds: X`

**Common Causes**:
- Accessing list element at index that doesn't exist
- Assuming list has elements without checking size
- Off-by-one errors in loops
- Accessing list after filtering/removing elements

**Solutions**:

### Solution 1: Check List Size Before Access

**Before: No size check**
```apex
List<Contact> contacts = [SELECT Id FROM Contact LIMIT 1];
Contact firstContact = contacts[0]; // Fails if no results
```

**After: With size check**
```apex
List<Contact> contacts = [SELECT Id FROM Contact LIMIT 1];
if (!contacts.isEmpty()) {
    Contact firstContact = contacts[0];
} else {
    // Handle empty list
}
```

### Solution 2: Use Safe Access Pattern

```apex
List<Contact> contacts = [SELECT Id FROM Contact LIMIT 1];
Contact firstContact = contacts.size() > 0 ? contacts[0] : null;
```

### Solution 3: Validate in Loops

**Before: Unsafe loop**
```apex
for (Integer i = 0; i <= contacts.size(); i++) { // Off-by-one error
    Contact c = contacts[i];
}
```

**After: Safe loop**
```apex
for (Integer i = 0; i < contacts.size(); i++) { // Correct bounds
    Contact c = contacts[i];
}

// Or use foreach (preferred)
for (Contact c : contacts) {
    // Process contact
}
```

**Prevention**:
- Always check `isEmpty()` or `size() > 0` before accessing list elements
- Use foreach loops when possible (safer)
- Validate list size in loops
- Handle empty list cases explicitly

---

## NULL_POINTER_EXCEPTION

**Error Message**: `NullPointerException: Attempt to de-reference a null object`

**Common Causes**:
- Accessing properties/methods on null objects
- Not checking for null before accessing
- Uninitialized variables
- Query returning no results

**Solutions**:

### Solution 1: Null Check Before Access

**Before: No null check**
```apex
Contact contact = [SELECT Id, Account.Name FROM Contact WHERE Id = :contactId LIMIT 1];
String accountName = contact.Account.Name; // Fails if Account is null
```

**After: With null check**
```apex
Contact contact = [SELECT Id, Account.Name FROM Contact WHERE Id = :contactId LIMIT 1];
String accountName = contact?.Account?.Name; // Safe navigation (if supported)
// Or
String accountName = (contact != null && contact.Account != null) 
    ? contact.Account.Name 
    : null;
```

### Solution 2: Initialize Variables

**Before: Uninitialized**
```apex
List<Contact> contacts; // null
contacts.add(new Contact()); // NullPointerException
```

**After: Initialized**
```apex
List<Contact> contacts = new List<Contact>();
contacts.add(new Contact());
```

### Solution 3: Handle Query Results

**Before: Assumes result exists**
```apex
Contact contact = [SELECT Id FROM Contact WHERE Id = :contactId LIMIT 1];
String contactId = contact.Id; // Fails if no result
```

**After: Handles no result**
```apex
List<Contact> contacts = [SELECT Id FROM Contact WHERE Id = :contactId LIMIT 1];
if (!contacts.isEmpty()) {
    Contact contact = contacts[0];
    String contactId = contact.Id;
} else {
    // Handle no result
}
```

**Prevention**:
- Always check for null before accessing properties
- Initialize collections before use
- Handle empty query results
- Use defensive programming patterns

---

## QUERY_EXCEPTION: No such column

**Error Message**: `QueryException: No such column 'FieldName' on entity 'ObjectName'`

**Common Causes**:
- Field doesn't exist on object
- Field API name is incorrect
- Field not accessible due to FLS
- Typo in field name

**Solutions**:

### Solution 1: Verify Field Exists

**Before: Hard-coded field name**
```apex
List<Contact> contacts = [SELECT Id, CustomField__c FROM Contact];
```

**After: Use schema imports**
```apex
import CUSTOM_FIELD from '@salesforce/schema/Contact.CustomField__c';

List<Contact> contacts = [
    SELECT Id, CustomField__c 
    FROM Contact 
    WITH SECURITY_ENFORCED
];
```

### Solution 2: Use Schema Describe

```apex
Schema.SObjectType contactType = Schema.getGlobalDescribe().get('Contact');
Schema.DescribeSObjectResult contactDescribe = contactType.getDescribe();
Map<String, Schema.SObjectField> fields = contactDescribe.fields.getMap();

if (fields.containsKey('CustomField__c')) {
    // Field exists, use it
} else {
    // Handle missing field
}
```

**Prevention**:
- Use schema imports for field references
- Verify field API names in setup
- Use `WITH SECURITY_ENFORCED` to catch FLS issues
- Test queries in developer console first

**Related Patterns**: <a href="{{ '/rag/development/soql-query-patterns.html' | relative_url }}">SOQL Patterns</a>, <a href="{{ '/rag/mcp-knowledge/lds-patterns.html' | relative_url }}">LDS Referential Integrity</a>

---

## DML_EXCEPTION: Required field missing

**Error Message**: `DmlException: Required field is missing: [FieldName]`

**Common Causes**:
- Required field not set before insert/update
- Required field set to null
- Validation rule preventing save

**Solutions**:

### Solution 1: Set Required Fields

**Before: Missing required field**
```apex
Contact contact = new Contact();
contact.Email = 'test@example.com';
insert contact; // Fails: LastName is required
```

**After: Set required fields**
```apex
Contact contact = new Contact();
contact.LastName = 'Test'; // Required field
contact.Email = 'test@example.com';
insert contact;
```

### Solution 2: Handle Validation Errors

```apex
try {
    insert contacts;
} catch (DmlException e) {
    for (Integer i = 0; i < e.getNumDml(); i++) {
        Integer recordIndex = e.getDmlIndex(i);
        String errorMessage = e.getDmlMessage(i);
        
        if (errorMessage.contains('Required field')) {
            // Handle required field error
            Contact failedContact = contacts[recordIndex];
            // Set required field or log error
        }
    }
}
```

**Prevention**:
- Always set required fields before DML
- Check object requirements in setup
- Handle validation errors gracefully
- Use base Lightning components which handle required fields

---

## LIMIT_EXCEPTION: Too many SOQL queries

**Error Message**: `LimitException: Too many SOQL queries: 101 out of 100`

**Common Causes**:
- SOQL query inside loop
- Trigger not bulkified
- Multiple queries in same transaction
- Recursive trigger calls

**Solutions**:

### Solution 1: Bulkify Queries

**Before: SOQL in loop**
```apex
for (Contact contact : contacts) {
    Account account = [SELECT Name FROM Account WHERE Id = :contact.AccountId];
    // Process account
}
```

**After: Bulkified**
```apex
Set<Id> accountIds = new Set<Id>();
for (Contact contact : contacts) {
    accountIds.add(contact.AccountId);
}

Map<Id, Account> accountMap = new Map<Id, Account>([
    SELECT Id, Name 
    FROM Account 
    WHERE Id IN :accountIds
    WITH SECURITY_ENFORCED
]);

for (Contact contact : contacts) {
    Account account = accountMap.get(contact.AccountId);
    // Process account
}
```

### Solution 2: Use Relationship Queries

**Before: Separate queries**
```apex
List<Contact> contacts = [SELECT Id, AccountId FROM Contact];
Set<Id> accountIds = new Set<Id>();
for (Contact c : contacts) {
    accountIds.add(c.AccountId);
}
List<Account> accounts = [SELECT Id, Name FROM Account WHERE Id IN :accountIds];
```

**After: Relationship query**
```apex
List<Contact> contacts = [
    SELECT Id, AccountId, Account.Name 
    FROM Contact 
    WHERE AccountId != null
    WITH SECURITY_ENFORCED
];
// Account.Name is already available
```

**Prevention**:
- Never put SOQL in loops
- Always bulkify triggers and batch classes
- Use relationship queries when possible
- Monitor governor limits proactively

**Related Patterns**: <a href="{{ '/rag/development/apex-patterns#bulkification.html' | relative_url }}">Apex Patterns</a>

---

## LIMIT_EXCEPTION: Too many DML statements

**Error Message**: `LimitException: Too many DML statements: 151 out of 150`

**Common Causes**:
- DML operation inside loop
- Trigger not bulkified
- Multiple DML operations in same transaction

**Solutions**:

### Solution 1: Bulkify DML

**Before: DML in loop**
```apex
for (Contact contact : contacts) {
    contact.Email = 'updated@example.com';
    update contact; // DML in loop
}
```

**After: Bulkified**
```apex
for (Contact contact : contacts) {
    contact.Email = 'updated@example.com';
}
update contacts; // Single DML for all records
```

### Solution 2: Batch Processing

```apex
// For very large lists, use batch processing
public class ContactUpdateBatch implements Database.Batchable<SObject> {
    public Database.QueryLocator start(Database.BatchableContext context) {
        return Database.getQueryLocator('SELECT Id FROM Contact');
    }
    
    public void execute(Database.BatchableContext context, List<Contact> scope) {
        // Process in batches of 200
        for (Contact c : scope) {
            c.Email = 'updated@example.com';
        }
        update scope;
    }
    
    public void finish(Database.BatchableContext context) {
        // Cleanup
    }
}
```

**Prevention**:
- Never put DML in loops
- Always bulkify DML operations
- Use batch processing for large datasets
- Process collections, not single records

**Related Patterns**: <a href="{{ '/rag/development/apex-patterns#bulkification.html' | relative_url }}">Apex Patterns</a>

---

## CALLOUT_EXCEPTION: Uncommitted work pending

**Error Message**: `CalloutException: You have uncommitted work pending. Please commit or rollback before calling out`

**Common Causes**:
- Making HTTP callout after DML in same transaction
- Callout in trigger after DML
- Callout in same transaction as DML

**Solutions**:

### Solution 1: Use @future or Queueable

**Before: Callout after DML**
```apex
update contacts;
// Make callout
HttpResponse response = makeHttpCallout(); // Fails
```

**After: Use @future**
```apex
update contacts;
// Enqueue callout for async execution
makeCalloutAsync(contactIds);

@future(callout=true)
public static void makeCalloutAsync(Set<Id> contactIds) {
    HttpResponse response = makeHttpCallout();
}
```

### Solution 2: Use Queueable

```apex
update contacts;
// Enqueue callout
System.enqueueJob(new CalloutQueueable(contactIds));

public class CalloutQueueable implements Queueable, Database.AllowsCallouts {
    private Set<Id> contactIds;
    
    public CalloutQueueable(Set<Id> contactIds) {
        this.contactIds = contactIds;
    }
    
    public void execute(QueueableContext context) {
        HttpResponse response = makeHttpCallout();
    }
}
```

**Prevention**:
- Use `@future(callout=true)` or Queueable for callouts after DML
- Separate DML and callout operations
- Plan transaction boundaries carefully

**Related Patterns**: <a href="{{ '/rag/development/apex-patterns.html' | relative_url }}">Apex Patterns</a> - Apex best practices

