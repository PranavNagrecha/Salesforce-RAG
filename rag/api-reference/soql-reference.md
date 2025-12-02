# SOQL Reference

> Quick reference for SOQL syntax, functions, and common query patterns.

## Overview

This reference provides SOQL syntax, functions, and common query patterns for Salesforce data access.

## Basic SOQL Syntax

### SELECT Statement

**Basic Structure**:
```sql
SELECT Field1, Field2, Field3
FROM ObjectName
WHERE Condition
ORDER BY Field1
LIMIT 100
```

**Example**:
```sql
SELECT Id, Name, Email
FROM Contact
WHERE Email != null
ORDER BY Name
LIMIT 100
```

---

## Relationship Queries

### Parent Object Fields

**Syntax**: Use dot notation to access parent object fields

**Example**:
```sql
SELECT Id, Name, Account.Name, Account.Industry
FROM Contact
WHERE Account.Industry = 'Technology'
```

**Related Patterns**: [SOQL Query Patterns](rag/development/soql-query-patterns.md#relationship-queries)

---

### Child Object Subqueries

**Syntax**: Use subquery syntax to access child records

**Example**:
```sql
SELECT Id, Name, 
    (SELECT Id, Subject, Status FROM Cases)
FROM Account
WHERE Id = '001000000000001'
```

**Related Patterns**: [SOQL Query Patterns](rag/development/soql-query-patterns.md#relationship-queries)

---

## Aggregate Queries

### COUNT

**Syntax**: `SELECT COUNT() FROM ObjectName`

**Example**:
```sql
SELECT COUNT() FROM Contact WHERE AccountId = '001000000000001'
```

### SUM, AVG, MIN, MAX

**Syntax**: `SELECT SUM(FieldName), AVG(FieldName) FROM ObjectName`

**Example**:
```sql
SELECT SUM(Amount), AVG(Amount), MIN(Amount), MAX(Amount)
FROM Opportunity
WHERE StageName = 'Closed Won'
```

### GROUP BY

**Syntax**: `SELECT Field, AggregateFunction() FROM ObjectName GROUP BY Field`

**Example**:
```sql
SELECT AccountId, COUNT(Id) contactCount
FROM Contact
GROUP BY AccountId
HAVING COUNT(Id) > 5
```

**Related Patterns**: [SOQL Query Patterns](rag/development/soql-query-patterns.md#aggregate-queries)

---

## Date and Time Functions

### TODAY

**Syntax**: `WHERE DateField = TODAY`

**Example**:
```sql
SELECT Id, Name, CreatedDate
FROM Contact
WHERE CreatedDate = TODAY
```

### LAST_N_DAYS

**Syntax**: `WHERE DateField = LAST_N_DAYS:n`

**Example**:
```sql
SELECT Id, Name, CreatedDate
FROM Contact
WHERE CreatedDate = LAST_N_DAYS:30
```

### Date Literals

Common date literals:
- `TODAY`
- `YESTERDAY`
- `TOMORROW`
- `LAST_N_DAYS:n`
- `NEXT_N_DAYS:n`
- `LAST_WEEK`
- `THIS_WEEK`
- `NEXT_WEEK`
- `LAST_MONTH`
- `THIS_MONTH`
- `NEXT_MONTH`
- `LAST_YEAR`
- `THIS_YEAR`
- `NEXT_YEAR`

**Related Patterns**: [SOQL Query Patterns](rag/development/soql-query-patterns.md#date-and-time-queries)

---

## Security Enforcement

### WITH SECURITY_ENFORCED

**Syntax**: `SELECT ... FROM ObjectName WITH SECURITY_ENFORCED`

**Description**: Enforces field-level and object-level security. Query fails if user doesn't have access.

**Example**:
```sql
SELECT Id, Name, Email
FROM Contact
WITH SECURITY_ENFORCED
WHERE AccountId = :accountId
```

**Best Practices**:
- ALWAYS use `WITH SECURITY_ENFORCED` or `WITH USER_MODE` in Apex queries
- Required for security compliance
- Fails fast if user lacks access

**Related Patterns**: [Apex Patterns](rag/development/apex-patterns.md#security-enforcement), [Security Patterns](rag/security/)

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

**Related Patterns**: [SOQL Query Patterns](rag/development/soql-query-patterns.md#cursor-based-pagination), [Governor Limits](rag/development/governor-limits-and-optimization.md)

---

## Dynamic SOQL

**Syntax**: Build query string dynamically

**Example**:
```apex
String objectName = 'Contact';
String fieldName = 'Name';
String searchValue = 'John';

String query = 'SELECT Id, ' + fieldName + 
               ' FROM ' + objectName + 
               ' WHERE ' + fieldName + ' LIKE \'%' + 
               String.escapeSingleQuotes(searchValue) + '%\'' +
               ' WITH SECURITY_ENFORCED' +
               ' LIMIT 100';

List<SObject> results = Database.query(query);
```

**Best Practices**:
- Always use `String.escapeSingleQuotes()` for user input
- Include `WITH SECURITY_ENFORCED`
- Validate object and field names
- Use bind variables when possible

**Related Patterns**: [SOQL Query Patterns](rag/development/soql-query-patterns.md#dynamic-soql)

---

## Maintenance Queries

### Unused Permission Sets

```sql
SELECT Id, Name, (SELECT Id FROM Assignments)
FROM PermissionSet
WHERE IsCustom = true
AND Id NOT IN (SELECT PermissionSetId FROM PermissionSetAssignment)
```

### Unused Roles

```sql
SELECT Id, Name, (SELECT Id FROM Users)
FROM UserRole
WHERE Id NOT IN (SELECT UserRoleId FROM User WHERE IsActive = true)
```

### Unused Profiles

```sql
SELECT Id, Name, (SELECT Id FROM Users)
FROM Profile
WHERE Id NOT IN (SELECT ProfileId FROM User WHERE IsActive = true)
```

**Related Patterns**: [SOQL Query Patterns](rag/development/soql-query-patterns.md#maintenance-queries)

---

## Related Patterns

- [SOQL Query Patterns](rag/development/soql-query-patterns.md) - Complete SOQL patterns and examples
- [Apex Patterns](rag/development/apex-patterns.md) - Apex query patterns
- [Governor Limits](rag/development/governor-limits-and-optimization.md) - Query optimization
- [Selector Layer](rag/development/apex-patterns.md#selector-layer) - Selector pattern implementation

