---
layout: default
title: Governor Limit Errors and Solutions
description: This guide provides solutions for governor limit errors, including error messages, causes, solutions, and prevention strategies
permalink: /rag/troubleshooting/governor-limit-errors.html

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

**Related Patterns**: <a href="{{ '/rag/development/governor-limits-and-optimization.html' | relative_url }}">Governor Limits</a>

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

**Related Patterns**: <a href="{{ '/rag/development/governor-limits-and-optimization.html' | relative_url }}">Governor Limits</a>

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

**Related Patterns**: <a href="{{ '/rag/development/apex-patterns.html#asynchronous-apex-patterns' | relative_url }}">Apex Patterns</a>

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

**Related Patterns**: <a href="{{ '/rag/development/apex-patterns.html' | relative_url }}">Apex Patterns</a>

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

**Related Patterns**: <a href="{{ '/rag/development/soql-query-patterns.html' | relative_url }}">SOQL Patterns</a>

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

**Related Patterns**: <a href="{{ '/rag/development/soql-query-patterns.html' | relative_url }}">SOQL Patterns</a> - Query optimization
- <a href="{{ '/rag/troubleshooting/' | relative_url }}">Troubleshooting</a> - Other troubleshooting guides