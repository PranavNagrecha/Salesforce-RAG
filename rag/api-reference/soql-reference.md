---
layout: default
title: SOQL Reference
description: This reference provides SOQL syntax, functions, and common query patterns for Salesforce data access
permalink: /rag/api-reference/soql-reference.html

---

### WITH USER_MODE

**Syntax**: `SELECT ... FROM ObjectName WITH USER_MODE`

**Description**: Executes query in user mode, respecting all security settings.

**Example**:
```sql
SELECT Id, Name
FROM Contact
WITH USER_MODE
WHERE AccountId = :accountId
```

---

## Common Query Patterns

### IN Clause

**Syntax**: `WHERE Field IN (value1, value2, value3)`

**Example**:
```sql
SELECT Id, Name
FROM Contact
WHERE AccountId IN ('001000000000001', '001000000000002')
```

**Apex Example**:
```apex
Set<Id> accountIds = new Set<Id>{ '001000000000001', '001000000000002' };
List<Contact> contacts = [
    SELECT Id, Name
    FROM Contact
    WHERE AccountId IN :accountIds
    WITH SECURITY_ENFORCED
];
```

---

### LIKE Pattern Matching

**Syntax**: `WHERE Field LIKE 'pattern%'`

**Example**:
```sql
SELECT Id, Name
FROM Contact
WHERE Name LIKE 'John%'
```

**Patterns**:
- `'John%'` - Starts with "John"
- `'%John'` - Ends with "John"
- `'%John%'` - Contains "John"

---

### NULL Checks

**Syntax**: `WHERE Field = null` or `WHERE Field != null`

**Example**:
```sql
SELECT Id, Name, Email
FROM Contact
WHERE Email != null
```

---

### Date Comparisons

**Syntax**: `WHERE DateField > DateValue`

**Example**:
```sql
SELECT Id, Name, CreatedDate
FROM Contact
WHERE CreatedDate > 2024-01-01T00:00:00Z
```

---

## Cursor-Based Pagination

**Syntax**: Use `OFFSET` or cursor-based approach

**Example with OFFSET**:
```sql
SELECT Id, Name
FROM Contact
ORDER BY CreatedDate
LIMIT 200
OFFSET 0
```

**Example with Cursor**:
```apex
// First query
List<Contact> contacts = [
    SELECT Id, Name, CreatedDate
    FROM Contact
    ORDER BY CreatedDate
    LIMIT 200
    WITH SECURITY_ENFORCED
];

// Next page using last record's CreatedDate
DateTime lastDate = contacts[contacts.size() - 1].CreatedDate;
List<Contact> nextPage = [
    SELECT Id, Name, CreatedDate
    FROM Contact
    WHERE CreatedDate > :lastDate
    ORDER BY CreatedDate
    LIMIT 200
    WITH SECURITY_ENFORCED
];
```

**Best Practices**:
- Use cursor-based pagination for large datasets
- `OFFSET` has performance limitations (max 2000)
- Cursor-based approach scales better

**Related Patterns**: <a href="{{ '/rag/development/apex-patterns.html#selector-layer' | relative_url }}">Selector Layer</a> - Selector pattern implementation