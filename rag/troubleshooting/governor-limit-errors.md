---
layout: default
title: Governor Limit Errors and Solutions
description: This guide provides solutions for governor limit errors, including error messages, causes, solutions, and prevention strategies
permalink: /rag/troubleshooting/governor-limit-errors.html
---

# Governor Limit Errors and Solutions

> Troubleshooting guide for Salesforce governor limit errors with solutions and optimization strategies.

## Overview

This guide provides solutions for governor limit errors, including error messages, causes, solutions, and prevention strategies.

## Prerequisites

**Required Knowledge**:
- Understanding of Salesforce governor limits
- Knowledge of Apex programming and SOQL queries
- Understanding of bulkification patterns
- Familiarity with error handling

**Recommended Reading**:
- <a href="{{ '/rag/development/governor-limits-and-optimization.html' | relative_url }}">Governor Limits and Optimization</a> - Limit management and optimization
- <a href="{{ '/rag/development/soql-query-patterns.html' | relative_url }}">SOQL Query Patterns</a> - Query optimization
- <a href="{{ '/rag/development/apex-patterns.html' | relative_url }}">Apex Patterns</a> - Bulkification patterns
- <a href="{{ '/rag/development/error-handling-and-logging.html' | relative_url }}">Error Handling and Logging</a> - Error handling patterns

## Too many SOQL queries

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
    // Process - 1 query per iteration
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
]); // Single query for all accounts

for (Contact contact : contacts) {
    Account account = accountMap.get(contact.AccountId);
    // Process
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
]; // Single query with related data
```

**Prevention**:
- Never put SOQL in loops
- Always bulkify triggers and batch classes
- Use relationship queries when possible
- Monitor query count proactively

**Related Patterns**: <a href="{{ '/rag/development/soql-query-patterns.html' | relative_url }}">SOQL Patterns</a>, <a href="{{ '/rag/development/governor-limits-and-optimization.html' | relative_url }}">Governor Limits</a>

---

## Too many DML statements

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
    update contact; // 1 DML per iteration
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
public class ContactUpdateBatch implements Database.Batchable<SObject> {
    public Database.QueryLocator start(Database.BatchableContext context) {
        return Database.getQueryLocator('SELECT Id FROM Contact');
    }
    
    public void execute(Database.BatchableContext context, List<Contact> scope) {
        // Process in batches of 200
        for (Contact c : scope) {
            c.Email = 'updated@example.com';
        }
        update scope; // DML per batch
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

**Related Patterns**: <a href="{{ '/rag/troubleshooting/Salesforce-RAG/rag/development/apex-patterns.html#bulkification.html' | relative_url }}">Apex Patterns</a>, <a href="{{ '/rag/development/governor-limits-and-optimization.html' | relative_url }}">Governor Limits</a>

---

## Too many callouts

**Error Message**: `LimitException: Too many callouts: 101 out of 100`

**Common Causes**:
- HTTP callout inside loop
- Multiple callouts in same transaction
- Not using async processing

**Solutions**:

### Solution 1: Use @future or Queueable

**Before: Callout in loop**
```apex
for (Contact contact : contacts) {
    HttpResponse response = makeHttpCallout(contact.Id); // Callout in loop
}
```

**After: Batch callouts**
```apex
Set<Id> contactIds = new Set<Id>();
for (Contact contact : contacts) {
    contactIds.add(contact.Id);
}

// Process callouts in batches
processCalloutsAsync(contactIds);

@future(callout=true)
public static void processCalloutsAsync(Set<Id> contactIds) {
    List<Id> idList = new List<Id>(contactIds);
    // Process in batches of 100 (callout limit)
    for (Integer i = 0; i < idList.size(); i += 100) {
        List<Id> batch = new List<Id>();
        for (Integer j = i; j < Math.min(i + 100, idList.size()); j++) {
            batch.add(idList[j]);
        }
        makeBatchCallout(batch);
    }
}
```

**Prevention**:
- Never put callouts in loops
- Use @future or Queueable for async callouts
- Batch callouts when possible
- Monitor callout count

**Related Patterns**: <a href="{{ '/rag/troubleshooting/Salesforce-RAG/rag/development/apex-patterns.html#asynchronous-apex-patterns.html' | relative_url }}">Apex Patterns</a>

---

## CPU time limit exceeded

**Error Message**: `LimitException: Apex CPU time limit exceeded`

**Common Causes**:
- Complex calculations in loops
- Inefficient algorithms
- Large data processing in single transaction
- Recursive calls

**Solutions**:

### Solution 1: Optimize Algorithms

**Before: Inefficient nested loops**
```apex
for (Contact contact : contacts) {
    for (Account account : accounts) {
        if (contact.AccountId == account.Id) {
            // Process - O(n*m) complexity
        }
    }
}
```

**After: Optimized with Map**
```apex
Map<Id, Account> accountMap = new Map<Id, Account>(accounts);
for (Contact contact : contacts) {
    Account account = accountMap.get(contact.AccountId);
    if (account != null) {
        // Process - O(n) complexity
    }
}
```

### Solution 2: Use Batch Processing

```apex
// For large datasets, use batch processing
public class LargeDataProcessor implements Database.Batchable<SObject> {
    public Database.QueryLocator start(Database.BatchableContext context) {
        return Database.getQueryLocator('SELECT Id FROM Contact');
    }
    
    public void execute(Database.BatchableContext context, List<Contact> scope) {
        // Process in smaller batches
        processBatch(scope);
    }
    
    public void finish(Database.BatchableContext context) {
        // Cleanup
    }
}
```

**Prevention**:
- Optimize algorithms (avoid nested loops when possible)
- Use Maps for lookups instead of nested loops
- Use batch processing for large datasets
- Monitor CPU time usage

**Related Patterns**: <a href="{{ '/rag/development/governor-limits-and-optimization.html' | relative_url }}">Governor Limits</a>, <a href="{{ '/rag/development/apex-patterns.html' | relative_url }}">Apex Patterns</a>

---

## Heap size limit exceeded

**Error Message**: `LimitException: Apex heap size too large: XXXX`

**Common Causes**:
- Loading too much data into memory
- Large collections not released
- Memory leaks in loops
- Processing large datasets in single transaction

**Solutions**:

### Solution 1: Process in Smaller Batches

**Before: Loading all data**
```apex
List<Contact> allContacts = [SELECT Id, Name, Email, Phone, MailingAddress FROM Contact];
// Process all at once - may exceed heap
```

**After: Process in batches**
```apex
Integer batchSize = 200;
Integer offset = 0;
Boolean hasMore = true;

while (hasMore) {
    List<Contact> batch = [
        SELECT Id, Name, Email 
        FROM Contact 
        LIMIT :batchSize 
        OFFSET :offset
        WITH SECURITY_ENFORCED
    ];
    
    if (batch.isEmpty()) {
        hasMore = false;
    } else {
        processBatch(batch);
        offset += batchSize;
    }
}
```

### Solution 2: Select Only Needed Fields

**Before: Selecting all fields**
```apex
List<Contact> contacts = [SELECT FIELDS(ALL) FROM Contact LIMIT 200];
// Loads all fields - large heap usage
```

**After: Select only needed fields**
```apex
List<Contact> contacts = [
    SELECT Id, Name, Email 
    FROM Contact 
    LIMIT 200
    WITH SECURITY_ENFORCED
]; // Minimal fields - smaller heap
```

**Prevention**:
- Select only needed fields in queries
- Process data in smaller batches
- Release large collections when done
- Use batch processing for large datasets
- Avoid loading entire datasets into memory

**Related Patterns**: <a href="{{ '/rag/development/governor-limits-and-optimization.html' | relative_url }}">Governor Limits</a>, <a href="{{ '/rag/development/soql-query-patterns.html' | relative_url }}">SOQL Patterns</a>

---

## Too many future calls

**Error Message**: `LimitException: Too many future calls: 51 out of 50`

**Common Causes**:
- @future method called in loop
- Multiple @future calls in same transaction
- Recursive @future calls

**Solutions**:

### Solution 1: Batch Future Calls

**Before: Future in loop**
```apex
for (Contact contact : contacts) {
    processAsync(contact.Id); // Future call in loop
}

@future
public static void processAsync(Id contactId) {
    // Process
}
```

**After: Batch future call**
```apex
Set<Id> contactIds = new Set<Id>();
for (Contact contact : contacts) {
    contactIds.add(contact.Id);
}
processBatchAsync(contactIds); // Single future call

@future
public static void processBatchAsync(Set<Id> contactIds) {
    List<Contact> contacts = [SELECT Id FROM Contact WHERE Id IN :contactIds];
    // Process all in one future call
}
```

### Solution 2: Use Queueable Instead

```apex
// Queueable can be chained (no 50 limit)
System.enqueueJob(new ProcessQueueable(contactIds));

public class ProcessQueueable implements Queueable {
    private Set<Id> contactIds;
    
    public ProcessQueueable(Set<Id> contactIds) {
        this.contactIds = contactIds;
    }
    
    public void execute(QueueableContext context) {
        // Process
        // Can chain more Queueables if needed
    }
}
```

**Prevention**:
- Never call @future methods in loops
- Batch future calls when possible
- Use Queueable for chained async processing
- Monitor future call count

**Related Patterns**: <a href="{{ '/rag/troubleshooting/Salesforce-RAG/rag/development/apex-patterns.html#asynchronous-apex-patterns.html' | relative_url }}">Apex Patterns</a>

---

## Q&A

### Q: What are Salesforce governor limits and why do they exist?

**A**: **Governor limits** are runtime limits enforced by Salesforce to ensure fair resource usage and system stability. They prevent one organization from consuming excessive resources and ensure all organizations have access to shared platform resources. Limits include SOQL queries (100 per transaction), DML statements (150), CPU time (10 seconds), heap size (6MB/12MB), and callouts (100).

### Q: How do I fix "Too many SOQL queries" errors?

**A**: Fix SOQL query limit errors by: (1) **Bulkifying queries** (no queries in loops), (2) **Using maps** to store query results and reuse them, (3) **Querying once** and processing results in memory, (4) **Using aggregate queries** to get summary data, (5) **Optimizing queries** to get all needed data in one query. Never put SOQL queries inside loops - collect IDs first, then query once.

### Q: How do I prevent "Too many DML statements" errors?

**A**: Prevent DML limit errors by: (1) **Bulkifying DML operations** (collect records in lists, then DML once), (2) **Using collections** to batch DML operations, (3) **Avoiding DML in loops**, (4) **Using Database methods** with `allOrNone=false` for partial success, (5) **Batching operations** when processing large datasets. Always collect records first, then perform DML once.

### Q: What causes "CPU time limit exceeded" errors and how do I fix them?

**A**: **CPU time limit exceeded** occurs when code execution exceeds 10 seconds of CPU time. Fix by: (1) **Optimizing algorithms** (reduce complexity), (2) **Using asynchronous processing** (Batch, Queueable, @future) for long-running operations, (3) **Reducing loop iterations**, (4) **Caching expensive calculations**, (5) **Breaking work into smaller chunks**. Move long-running operations to async processing.

### Q: How do I handle "Heap size limit exceeded" errors?

**A**: Handle heap size errors by: (1) **Processing data in batches** instead of loading all at once, (2) **Clearing large collections** when no longer needed, (3) **Using streaming** for large datasets, (4) **Avoiding deep object hierarchies**, (5) **Using Batch Apex** for large data processing. Don't load all data into memory - process incrementally.

### Q: How do I prevent "Too many callouts" errors?

**A**: Prevent callout limit errors by: (1) **Batching callouts** when possible, (2) **Using async processing** (@future, Queueable) for callouts, (3) **Caching callout results** when appropriate, (4) **Using Platform Events** for decoupled integrations, (5) **Monitoring callout count** using `Limits.getCallouts()`. Move callouts to async processing when possible.

### Q: What is the difference between synchronous and asynchronous governor limits?

**A**: **Synchronous limits** apply to code running in the same transaction (SOQL: 100, DML: 150, CPU: 10s). **Asynchronous limits** are higher (SOQL: 200, DML: 150, CPU: 60s) and apply to Batch, Queueable, and @future methods. Use async processing when you need higher limits or long-running operations.

### Q: How do I monitor governor limits in my code?

**A**: Monitor limits using the **`Limits` class**: (1) **`Limits.getQueries()`** - current SOQL queries, (2) **`Limits.getDmlStatements()`** - current DML statements, (3) **`Limits.getCpuTime()`** - current CPU time, (4) **`Limits.getHeapSize()`** - current heap size, (5) **`Limits.getCallouts()`** - current callouts. Use these to check limits before operations and log warnings.

### Q: How do I optimize code to avoid governor limit errors?

**A**: Optimize code by: (1) **Bulkifying all operations** (no DML/SOQL in loops), (2) **Using efficient data structures** (maps, sets), (3) **Caching query results** and calculations, (4) **Using async processing** for long-running operations, (5) **Optimizing SOQL queries** (selective WHERE clauses, indexed fields), (6) **Reducing code complexity** (simpler algorithms), (7) **Testing with bulk data** (200+ records).

### Q: What should I do when I hit a governor limit in production?

**A**: When hitting limits in production: (1) **Identify the limit** (check error message and debug logs), (2) **Analyze the code** causing the limit, (3) **Implement bulkification** or optimization, (4) **Test thoroughly** in sandbox, (5) **Deploy fix** as soon as possible, (6) **Monitor** to ensure fix works, (7) **Consider async processing** if operation is long-running. Always have a rollback plan.

## Edge Cases and Limitations

### Edge Case 1: Cumulative Limit Usage Across Automation

**Scenario**: Multiple triggers, flows, and validation rules executing on the same record, causing cumulative governor limit usage.

**Consideration**:
- Monitor total limit usage across all automation
- Use `Limits` class to check usage before expensive operations
- Design automation to minimize cumulative usage
- Test with bulk data to identify limit issues
- Consider async processing for complex operations
- Document automation execution order

### Edge Case 2: Governor Limits in Complex Calculations

**Scenario**: Complex calculations or loops consuming excessive CPU time, causing CPU time limit exceptions.

**Consideration**:
- Optimize algorithms to reduce complexity
- Cache calculation results when possible
- Break complex operations into smaller chunks
- Use async processing for CPU-intensive operations
- Profile code to identify CPU bottlenecks
- Monitor CPU time usage

### Edge Case 3: Heap Size with Large Collections

**Scenario**: Processing large collections of records with complex objects causes heap size exceptions.

**Consideration**:
- Process records in smaller batches
- Select only necessary fields in queries
- Avoid storing entire record collections in memory
- Use streaming or cursor-based processing
- Consider Batch Apex for very large operations
- Monitor heap size usage

### Edge Case 4: SOQL Query Limits with Related Records

**Scenario**: Querying records with many related records (e.g., Account with 200 Contacts) causing SOQL query limit exceptions.

**Consideration**:
- Use relationship queries efficiently
- Consider separate queries for related records
- Use aggregate queries when appropriate
- Limit related record queries
- Monitor SOQL query count
- Optimize query structure

### Edge Case 5: DML Limits with Cascading Updates

**Scenario**: Updating records triggers cascading updates to related records, causing DML limit exceptions.

**Consideration**:
- Understand cascading update behavior
- Monitor DML statement count in complex operations
- Consider async processing for cascading updates
- Design data model to minimize cascading DML
- Test with realistic data volumes
- Document cascading update logic

### Limitations

- **Hard Limits**: Governor limits are hard limits that cannot be exceeded
- **Limit Checking Overhead**: Frequent limit checking adds small performance overhead
- **Async Limit Differences**: Async contexts have different limits but also different constraints
- **Limit Measurement**: Limit usage includes all processing, not just Apex execution
- **Batch Size Limits**: Batch Apex batch size limited by heap size and DML limits
- **Query Result Limits**: SOQL queries return maximum 50,000 records
- **CPU Time Measurement**: CPU time includes all processing, making optimization complex

## Related Patterns

**See Also**:
- <a href="{{ '/rag/troubleshooting/common-apex-errors.html' | relative_url }}">Common Apex Errors</a> - Other common Apex errors

**Related Domains**:
- <a href="{{ '/rag/development/governor-limits-and-optimization.html' | relative_url }}">Governor Limits and Optimization</a> - Complete governor limits guide
- <a href="{{ '/rag/development/apex-patterns.html' | relative_url }}">Apex Patterns</a> - Apex best practices
- <a href="{{ '/rag/development/soql-query-patterns.html' | relative_url }}">SOQL Patterns</a> - Query optimization

- <a href="{{ '/rag/development/governor-limits-and-optimization.html' | relative_url }}">Governor Limits and Optimization</a> - Complete governor limits guide
- <a href="{{ '/rag/development/apex-patterns.html' | relative_url }}">Apex Patterns</a> - Apex best practices
- <a href="{{ '/rag/development/soql-query-patterns.html' | relative_url }}">SOQL Patterns</a> - Query optimization
- <a href="{{ '/rag/troubleshooting/..html' | relative_url }}">Troubleshooting</a> - Other troubleshooting guides

