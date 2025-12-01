# SOQL Query Patterns

## Overview

This document captures SOQL query patterns and practices derived from actual implementation experience across multiple Salesforce projects. All patterns documented here are based on real work, including dynamic SOQL implementations, relationship queries, debugging patterns, and maintenance queries used in production systems.

**When to use this document**:
- Building dynamic SOQL queries with user input
- Implementing relationship queries to combine related data
- Optimizing queries for performance and governor limits
- Debugging integration failures and data issues
- Performing org maintenance and cleanup
- Building cascading load patterns for LWC components

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

## To Validate

- **Query selectivity thresholds**: While 10% is widely cited, actual performance depends on many factors. Optimal threshold may vary by object and query pattern.
- **Dynamic SOQL performance**: Dynamic queries may have different performance characteristics than static queries. Monitor query performance in production.
- **Cascading load timing**: Optimal timing for cascading loads may depend on user behavior and network conditions. Monitor user experience metrics.
- **Maintenance query frequency**: Frequency of running maintenance queries depends on org size, change frequency, and compliance requirements. Evaluate based on org characteristics.
