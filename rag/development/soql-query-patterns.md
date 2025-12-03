---
layout: default
title: SOQL Query Patterns
description: This document captures SOQL query patterns and practices derived from actual implementation experience across multiple Salesforce projects
permalink: /rag/development/soql-query-patterns.html
---

## What Was Actually Done

### Dynamic SOQL with Proper Escaping

**Implementation Evidence**: Built dynamic SOQL queries in LWC Apex controllers for program selection components where filters are selected dynamically by users.

**What Was Built**:
- Dynamic SOQL query builder that constructs WHERE clauses based on selected filters (category, region, status)
- Proper escaping using `String.escapeSingleQuotes()` to prevent SOQL injection
- Conditional WHERE clause construction - only adds filters when values are selected
- LIMIT 100 on list queries to prevent large result sets
- ORDER BY optimization using `ORDER BY Display_Name__c ASC` for consistent sorting

**Example Pattern**:
```apex
// Dynamic SOQL with proper escaping
String query = 'SELECT Id, Display_Name__c, Name FROM Account WHERE RecordType.Name = \'Custom_Record_Type\'';
List<String> conditions = new List<String>();

if (categoryId != null && categoryId != '') {
    conditions.add('Category__c = \'' + String.escapeSingleQuotes(categoryId) + '\'');
}
if (region != null && region != '') {
    conditions.add('Region__c = \'' + String.escapeSingleQuotes(region) + '\'');
}
if (status != null && status != '') {
    conditions.add('Status__c = \'' + String.escapeSingleQuotes(status) + '\'');
}

if (!conditions.isEmpty()) {
    query += ' AND ' + String.join(conditions, ' AND ');
}

query += ' ORDER BY Display_Name__c ASC LIMIT 100';
List<Account> records = Database.query(query);
```

**Why This Approach**:
- Need to filter by different combinations of category/region/status - dynamic query allows flexibility
- Proper escaping prevents SOQL injection attacks
- LIMIT prevents large result sets that could cause heap size issues
- Conditional WHERE clauses ensure selective queries only when filters are applied

### Relationship Queries in Production

**Implementation Evidence**: Used relationship queries in multiple implementations to combine parent/child data in single queries, reducing governor limit usage.

**What Was Built**:
- Relationship queries using dot notation to access parent object fields
- Combined Contact and Account data in scoring calculations
- Combined parent and child object data in selection components
- Used relationship queries in debugging to trace data lineage

**Example Patterns**:
```apex
// Scoring calculation - relationship query to get Contact with Account data
List<Contact> contacts = [
    SELECT Id, Name, Email, 
           Account.Industry,
           Account.AnnualRevenue
    FROM Contact
    WHERE Id = :contactId
    WITH SECURITY_ENFORCED
    LIMIT 1
];

// Selection component - relationship query to get parent with related data
List<Account> accounts = [
    SELECT Id, Display_Name__c, Name,
           Parent_Object__r.Name,
           Parent_Object__r.Id
    FROM Account
    WHERE RecordType.Name = 'Custom_Record_Type'
    AND Parent_Object__c = :parentId
    WITH SECURITY_ENFORCED
    ORDER BY Display_Name__c ASC
    LIMIT 100
];
```

**Why This Approach**:
- Reduces number of queries (governor limit optimization)
- Single query retrieves data from both parent and child objects
- More efficient than separate queries
- Essential for governor limit management in complex components

### Cascading Load Pattern with Cacheable Methods

**Implementation Evidence**: Built selection component with cascading load pattern where data loads progressively based on user selections.

**What Was Built**:
- Primary options load first (cacheable method)
- Secondary options load after primary selection (cacheable method, filtered by primary)
- Tertiary options load after secondary selection (cacheable method, filtered by secondary)
- Final records load after all selections (cacheable method, filtered by all selections)
- All getter methods use `@AuraEnabled(cacheable=true)` for performance
- Picklist metadata used for reference data (cached by Salesforce, no queries needed)

**Query Pattern**:
```apex
@AuraEnabled(cacheable=true)
public static List<Account> getRecords(String categoryId, String region, String status) {
    // Dynamic SOQL builds WHERE clauses only for selected filters
    // Ensures selective queries
    // LIMIT 100 prevents large result sets
    // ORDER BY for consistent sorting
}
```

**Why This Approach**:
- Cascading loads reduce initial page load time
- Only loads data that's needed based on user selections
- Cacheable methods reduce server round trips
- Picklist metadata avoids queries entirely for static reference data

### Query Optimizations Implemented

**Implementation Evidence**: Optimized queries in multiple components and batch processes to improve performance and respect governor limits.

**What Was Optimized**:

1. **Minimal Field Selection**:
   - Only select fields actually needed: `Id`, `Display_Name__c`, `Name` for records
   - Not selecting entire object
   - Reduces data transfer and improves performance

2. **Selective WHERE Clauses**:
   - All queries use indexed fields (Id fields) for optimal performance
   - Dynamic WHERE clauses only added when filters are selected
   - Ensures queries remain selective

3. **LIMIT Clauses**:
   - `LIMIT 1` for single record queries (fraud scoring)
   - `LIMIT 100` for program selection queries
   - Prevents large result sets and heap size issues

4. **Conditional Queries**:
   - Only query for related records when parent record exists
   - Avoids unnecessary queries when data doesn't exist
   - Reduces governor limit usage

5. **Combined Queries**:
   - Found two separate queries that could be combined using relationship syntax
   - Optimized to single query with relationship fields
   - Reduced query count

### SOQL Debugging Patterns

**Implementation Evidence**: Used SOQL extensively for troubleshooting integration failures, data quality issues, and root cause analysis.

**What Was Done**:

1. **History Object Queries**:
   - Query ContactHistory, AccountHistory, CaseHistory to track field changes
   - Used to understand what changed and when
   - Essential for troubleshooting data synchronization issues

2. **Error Field Queries**:
   - Query error fields on records to identify failure patterns
   - Correlate errors with record types, owners, and sources
   - Use aggregate queries to identify common error patterns

3. **Root Cause Analysis Queries**:
   - Query multiple objects to find relationships
   - Use aggregate queries to identify patterns
   - Trace data lineage using relationship queries

4. **Metadata Queries**:
   - Query metadata when configuration issues are suspected
   - Use VS Code + Salesforce Extensions to retrieve and inspect metadata
   - Analyze object and field configurations

**Example Debugging Queries**:
```sql
-- Find records with errors
SELECT Id, Name, Error_Field__c, RecordType.Name, Owner.Name
FROM Lead
WHERE Error_Field__c != NULL
ORDER BY CreatedDate DESC

-- Track changes using history
SELECT Id, Field, OldValue, NewValue, CreatedDate, CreatedBy.Name
FROM ContactHistory
WHERE ContactId = '003...'
ORDER BY CreatedDate DESC

-- Aggregate query to find error patterns
SELECT RecordType.Name, COUNT(Id), Error_Field__c
FROM Lead
WHERE Error_Field__c != NULL
GROUP BY RecordType.Name, Error_Field__c
```

### Security Enforcement in All Queries

**Implementation Evidence**: Established code standards requiring security enforcement in all SOQL queries.

**What Was Implemented**:
- ALL SOQL queries MUST use `WITH SECURITY_ENFORCED` or `WITH USER_MODE`
- Enforced in code review process
- Found and fixed queries missing security enforcement
- Documented security decisions when using `without sharing`

**Example**:
```apex
List<Contact> contacts = [
    SELECT Id, Name, Email
    FROM Contact
    WHERE Id = :contactId
    WITH SECURITY_ENFORCED  // Always required
    LIMIT 1
];
```

### Bulkification Patterns

**Implementation Evidence**: Built batch processes and bulk operations that avoid SOQL in loops.

**What Was Built**:

1. **Bulk Query Pattern in Batch Apex**:
   - Query all parent records in start method
   - Collect all related record IDs in execute method
   - Query all related data in bulk (parent records, child records, lookup records)
   - Process all records in batch together
   - Single DML update for all records in batch
   - Avoids SOQL in loops

2. **Bulk Data Loading**:
   - Query all required data upfront
   - Store in collections for processing
   - Avoid querying inside loops
   - Process collections in bulk

**Example Pattern**:
```apex
// Batch Apex - bulk query pattern
global Database.QueryLocator start(Database.BatchableContext bc) {
    return Database.getQueryLocator('SELECT Id, Related_Record__c FROM Custom_Object__c');
}

global void execute(Database.BatchableContext bc, List<Custom_Object__c> records) {
    // Collect all IDs
    Set<Id> relatedIds = new Set<Id>();
    Set<Id> recordIds = new Set<Id>();
    for (Custom_Object__c rec : records) {
        relatedIds.add(rec.Related_Record__c);
        recordIds.add(rec.Id);
    }
    
    // Bulk query all related data
    Map<Id, Contact> relatedRecords = new Map<Id, Contact>([
        SELECT Id, Name, Email FROM Contact WHERE Id IN :relatedIds
    ]);
    
    // Process and update in bulk
    // Single DML for all records
}
```

### Maintenance Queries for Org Cleanup

**Implementation Evidence**: Created and published Medium articles with SOQL queries for identifying unused components in Salesforce orgs.

**What Was Created**:

1. **Unused Permission Sets**:
```sql
SELECT Id, Name, CreatedBy.Name, Description
FROM PermissionSet
WHERE IsCustom = TRUE
  AND Id NOT IN (SELECT PermissionSetId FROM PermissionSetAssignment)
  AND Id NOT IN (SELECT PermissionSetId FROM PermissionSetGroupComponent)
```

2. **Unused Permission Set Groups**:
```sql
SELECT Id, Name, CreatedBy.Name, Description
FROM PermissionSetGroup
WHERE Id NOT IN (SELECT PermissionSetGroupId FROM PermissionSetAssignment)
  AND Id NOT IN (SELECT ParentId FROM PermissionSetGroupComponent)
```

3. **Unused Roles**:
```sql
SELECT Id, Name, DeveloperName
FROM UserRole
WHERE Id NOT IN (SELECT UserRoleId FROM User WHERE IsActive = TRUE)
```

4. **Roles with Only Inactive Users**:
```sql
SELECT Id, Name, DeveloperName
FROM UserRole
WHERE Id IN (
  SELECT UserRoleId FROM User WHERE IsActive = FALSE
)
AND Id NOT IN (
  SELECT UserRoleId FROM User WHERE IsActive = TRUE
)
```

5. **Unused Profiles**:
```sql
SELECT Id, Name
FROM Profile
WHERE Id NOT IN (SELECT ProfileId FROM User WHERE IsActive = TRUE)
```

6. **Public Groups with No Members**:
```sql
SELECT Id, Name, DeveloperName
FROM Group
WHERE Type = 'Regular'
  AND Id NOT IN (SELECT GroupId FROM GroupMember)
```

7. **Queues with No Members**:
```sql
SELECT Id, Name
FROM Group
WHERE Type = 'Queue'
  AND Id NOT IN (SELECT GroupId FROM GroupMember)
```

8. **Permission Sets with 'Manage Users' Permission**:
```sql
SELECT Id, Name, Label, IsOwnedByProfile
FROM PermissionSet
WHERE PermissionsManageUsers = TRUE AND IsCustom = TRUE
```

9. **Profiles with 'Manage Users' Permission**:
```sql
SELECT Id, Name
FROM Profile
WHERE PermissionsManageUsers = TRUE
```

10. **Profiles and Permission Sets with Excessive Administrative Permissions**:
```sql
SELECT Id, Name, Label, IsOwnedByProfile,
  PermissionsModifyAllData,
  PermissionsManageUsers,
  PermissionsAuthorApex,
  PermissionsViewAllData,
  PermissionsInstallPackaging
FROM PermissionSet
WHERE IsOwnedByProfile = TRUE
  AND (
    PermissionsModifyAllData = TRUE OR
    PermissionsManageUsers = TRUE OR
    PermissionsAuthorApex = TRUE OR
    PermissionsViewAllData = TRUE OR
    PermissionsInstallPackaging = TRUE
  )
```

11. **Unused Reports**:
```sql
SELECT Id, Name, DeveloperName, LastReferencedDate
FROM Report
WHERE LastReferencedDate = NULL
  OR LastReferencedDate < LAST_N_YEARS:2
```

12. **Unused Email Templates**:
```sql
SELECT Id, Name, DeveloperName, LastUsedDate
FROM EmailTemplate
WHERE LastUsedDate = NULL
  OR LastUsedDate < LAST_N_YEARS:2
```

13. **Custom Permissions Not Assigned**:
```sql
SELECT Id, DeveloperName, MasterLabel
FROM CustomPermission
WHERE Id NOT IN (
  SELECT SetupEntityId
  FROM SetupEntityAccess
  WHERE SetupEntityType = 'CustomPermission'
)
```

14. **Objects Without Search Enabled**:
```sql
SELECT QualifiedApiName, Label, IsSearchable
FROM EntityDefinition
WHERE IsCustomizable = TRUE
  AND IsCustomSetting = FALSE
  AND IsSearchable = FALSE
  AND IsDeprecatedAndHidden = FALSE
ORDER BY QualifiedApiName
```

15. **Apex Classes with Outdated API Versions**:
```sql
SELECT Id, Name, ApiVersion
FROM ApexClass
WHERE ApiVersion < 50.0 AND NamespacePrefix = NULL
ORDER BY ApiVersion ASC, Name ASC
```

## Rules and Patterns

### Dynamic SOQL Rules

- **Always escape user input**: Use `String.escapeSingleQuotes()` for any user-provided values in dynamic SOQL queries
- **Build WHERE clauses conditionally**: Only add WHERE conditions when filters are actually selected
- **Use LIMIT clauses**: Always include LIMIT to prevent large result sets
- **Validate input before querying**: Check for null/empty values before building queries

### Relationship Query Rules

- **Use relationship queries instead of separate queries**: Combine parent/child data in single queries to reduce governor limit usage
- **Access parent fields with dot notation**: Use `ParentObject__r.Field__c` syntax
- **Filter on parent fields**: WHERE clauses can filter on parent object fields
- **Combine with security enforcement**: Always use `WITH SECURITY_ENFORCED` with relationship queries

### Query Optimization Rules

- **Select only necessary fields**: Don't select entire objects, only fields actually needed
- **Use indexed fields in WHERE clauses**: Id, Name, Email, External ID fields, date fields, lookup fields
- **Add LIMIT clauses**: Use `LIMIT 1` for single record queries, `LIMIT 100` for list queries
- **Use ORDER BY for consistency**: Sort results for predictable ordering
- **Combine queries when possible**: Use relationship syntax to combine separate queries into one

### Security Enforcement Rules

- **ALL SOQL queries MUST use `WITH SECURITY_ENFORCED` or `WITH USER_MODE`**: No exceptions
- **Respect field-level security**: Security enforcement ensures FLS is respected
- **Respect object-level security**: Security enforcement ensures OLS is respected
- **Document security decisions**: When using `without sharing`, document why

### Bulkification Rules

- **Never put SOQL in loops**: Always query collections upfront
- **Query all related data in bulk**: Collect IDs, then query all related records at once
- **Process collections, not single records**: Always work with collections
- **Use bulk DML**: Update/insert/delete collections, not single records

### Cascading Load Pattern Rules

- **Load data progressively**: Load initial data first, then load dependent data after user selections
- **Use cacheable methods**: Mark getter methods as `@AuraEnabled(cacheable=true)` for performance
- **Use picklist metadata when possible**: Avoid queries for static reference data
- **Filter queries based on selections**: Only query data relevant to current selections

### Debugging Query Rules

- **Start with history objects**: Query history objects to understand what changed
- **Use aggregate queries for patterns**: COUNT, GROUP BY to identify common issues
- **Query multiple objects for context**: Use relationship queries to trace data lineage
- **Query error fields**: Look for error fields on records to identify failure patterns
- **Correlate with metadata**: Query metadata when configuration issues are suspected

### Maintenance Query Rules

- **Use NOT IN subqueries**: Find unused components by checking what's not referenced
- **Use date functions**: `LAST_N_YEARS:2` for time-based filtering
- **Combine conditions**: Use multiple NOT IN clauses to find truly unused components
- **Query metadata objects**: Use EntityDefinition, ApexClass, etc. for metadata analysis

## Edge Cases and Limitations

### Query Selectivity Limitations

**Scenario**: Queries that return more than 10% of records may be non-selective and cannot use indexes.

**Consideration**: 
- Use multiple indexed fields in WHERE clauses to improve selectivity
- Consider using date ranges or other selective filters
- For large datasets, use pagination or batch processing
- Monitor query performance and adjust filters as needed

### Relationship Query Limitations

**Scenario**: Parent-to-child or child-to-parent queries can return large result sets.

**Consideration**:
- Use LIMIT clauses in subqueries to control result size
- Consider using aggregate queries when only counts or summaries are needed
- Be aware of governor limits for relationship queries (200 parent records with 200 child records each = 40,000 total records)

### Dynamic SOQL Security Limitations

**Scenario**: Dynamic SOQL with user input requires careful handling to prevent injection.

**Consideration**:
- Always use `String.escapeSingleQuotes()` for user input
- Validate input before building queries
- Use bind variables when possible (preferred over string concatenation)
- Test with edge cases (null, empty strings, special characters)

### Large Data Volume Limitations

**Scenario**: Queries on objects with millions of records may have performance issues.

**Consideration**:
- Use indexed fields in WHERE clauses
- Consider using Bulk API for large data operations
- Implement pagination for large result sets
- Use asynchronous processing for large queries

### Limitations

- **SOQL cannot query all objects**: Some objects (like SetupEntityAccess) cannot be queried directly
- **Relationship query depth**: Cannot query more than 5 levels deep in relationships
- **Aggregate query limitations**: Cannot use aggregate functions with certain field types
- **Date function limitations**: Some date functions may not use indexes efficiently
- **Text search limitations**: SOQL text search is limited compared to SOSL

## Interactions With Other RAG Files

**Connection to `rag/development/governor-limits-and-optimization.md`**:
- This file provides practical query examples
- Governor limits file focuses on optimization strategies and selective query rules
- Use together: query examples here + optimization guidance there

**Connection to `rag/development/apex-patterns.md`**:
- This file provides query patterns used in Apex
- Apex patterns file focuses on class layering and Selector layer patterns
- Use together: query examples here + Apex implementation patterns there

**Connection to `rag/troubleshooting/integration-debugging.md`**:
- This file provides debugging query patterns
- Troubleshooting file focuses on debugging methodology
- Use together: query examples here + debugging approach there

## Related Patterns

**See Also**:
- <a href="{{ '/rag/troubleshooting/data-reconciliation.html' | relative_url }}">Data Reconciliation</a> - Query patterns for data validation

## Q&A

### Q: How do I write efficient SOQL queries?

**A**: Write efficient queries by: (1) **Using indexed fields** in WHERE clauses (Id, Name, Email, External IDs, Lookup fields, Date fields), (2) **Ensuring selectivity** (queries return less than 10% of records), (3) **Selecting only needed fields** (don't use SELECT *), (4) **Using LIMIT clause** when possible, (5) **Avoiding functions** in WHERE clauses (prevents index usage), (6) **Using selective filters** (multiple indexed fields).

### Q: What is query selectivity and why does it matter?

**A**: **Query selectivity** is the percentage of records returned by a query. Queries should return **less than 10% of records** to be considered selective and use indexes efficiently. Non-selective queries (returning >10% of records) can't use indexes and perform full table scans, causing performance issues and potential governor limit violations. Use indexed fields and multiple filters to improve selectivity.

### Q: How do I write dynamic SOQL queries safely?

**A**: Write safe dynamic SOQL by: (1) **Using String.escapeSingleQuotes()** for user input (prevents SOQL injection), (2) **Validating input** before building queries, (3) **Using bind variables** when possible (preferred over string concatenation), (4) **Testing with edge cases** (null, empty strings, special characters), (5) **Using Database.query()** with proper escaping, (6) **Avoiding string concatenation** for user input.

### Q: How do I query related records efficiently?

**A**: Query related records by: (1) **Using relationship queries** (parent-to-child, child-to-parent), (2) **Limiting related records** (using LIMIT in subqueries), (3) **Selecting only needed fields** (don't query all fields), (4) **Using aggregate queries** when appropriate (COUNT, SUM, etc.), (5) **Avoiding nested queries** when not needed (can be expensive). Relationship queries enable efficient data retrieval across related objects.

### Q: What is the difference between SOQL and SOSL?

**A**: **SOQL (Salesforce Object Query Language)** queries specific objects and fields (structured queries). **SOSL (Salesforce Object Search Language)** searches across multiple objects using text search (unstructured search). Use SOQL for specific object queries, SOSL for text-based search across objects. SOQL is more precise, SOSL is more flexible for search scenarios.

### Q: How do I handle large result sets in SOQL?

**A**: Handle large result sets by: (1) **Using LIMIT clause** to restrict results, (2) **Using pagination** (OFFSET, LIMIT for page-by-page retrieval), (3) **Using WHERE filters** to reduce result set, (4) **Using Batch Apex** for processing large datasets, (5) **Using Bulk API** for very large datasets, (6) **Processing in chunks** (avoid loading all records at once).

### Q: How do I debug SOQL query issues?

**A**: Debug queries by: (1) **Using Query Plan** in Developer Console (analyze query performance), (2) **Checking query selectivity** (ensure <10% of records), (3) **Reviewing query logs** (identify slow queries), (4) **Testing queries** in Developer Console, (5) **Using EXPLAIN PLAN** for query analysis, (6) **Monitoring governor limits** (query count, rows returned). Query Plan shows whether indexes are used.

### Q: What are best practices for SOQL queries?

**A**: Best practices include: (1) **Use indexed fields** in WHERE clauses, (2) **Ensure selectivity** (<10% of records), (3) **Select only needed fields** (not SELECT *), (4) **Use LIMIT clause** when possible, (5) **Avoid functions in WHERE** (prevents index usage), (6) **Escape user input** (String.escapeSingleQuotes()), (7) **Test query performance** (use Query Plan), (8) **Monitor governor limits** (query count, rows).

### Q: How do I optimize queries for governor limits?

**A**: Optimize by: (1) **Reducing query count** (combine queries when possible), (2) **Using relationship queries** (retrieve related data in one query), (3) **Limiting result sets** (use LIMIT, WHERE filters), (4) **Caching query results** (Platform Cache for frequently accessed data), (5) **Using aggregate queries** (COUNT, SUM instead of retrieving all records), (6) **Bulkifying code** (no queries in loops).

### Q: When should I use relationship queries vs. separate queries?

**A**: Use **relationship queries** when: (1) **Retrieving related data** (parent-to-child, child-to-parent), (2) **Reducing query count** (one query instead of multiple), (3) **Data is needed together** (related records used together). Use **separate queries** when: (1) **Data is independent** (not used together), (2) **Different filters needed** (different WHERE conditions), (3) **Avoiding large result sets** (relationship queries can return many records).

## To Validate

- **Query selectivity thresholds**: While 10% is widely cited, actual performance depends on many factors. Optimal threshold may vary by object and query pattern.
- **Dynamic SOQL performance**: Dynamic queries may have different performance characteristics than static queries. Monitor query performance in production.
- **Cascading load timing**: Optimal timing for cascading loads may depend on user behavior and network conditions. Monitor user experience metrics.
- **Maintenance query frequency**: Frequency of running maintenance queries depends on org size, change frequency, and compliance requirements. Evaluate based on org characteristics.
