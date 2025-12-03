# Selector Layer Code Examples

> This file contains complete, working code examples for Apex Selector Layer patterns.  
> All examples are copy-paste ready and follow Salesforce best practices.

## Overview

The Selector Layer provides centralized SOQL queries and data access abstraction. It enforces security, optimizes queries, and provides reusable query methods.

**Related Patterns**:
- <a href="{{ '/rag/code-examples/apex/Salesforce-RAG/rag/development/apex-patterns.html#apex-class-layering.html' | relative_url }}">Apex Class Layering</a>
- <a href="{{ '/rag/code-examples/apex/Salesforce-RAG/rag/development/apex-patterns.html#selector-layer.html' | relative_url }}">Selector Layer Pattern</a>

## Examples

### Example 1: Basic Selector Class
**Pattern**: Selector Layer with Security Enforcement  
**Use Case**: Centralized data access for Contact object  
**Complexity**: Basic  
**Related Patterns**: <a href="{{ '/rag/code-examples/apex/Salesforce-RAG/rag/development/apex-patterns.html#selector-layer.html' | relative_url }}">Selector Layer</a>

**Problem**: 
You need to query Contact records with security enforcement and provide reusable query methods.

**Solution**:
```apex
/**
 * Selector class for Contact object
 * Centralized SOQL queries with security enforcement
 */
public with sharing class ContactSelector {
    
    /**
     * Default field list for Contact queries
     */
    private static final List<String> DEFAULT_FIELDS = new List<String>{
        'Id', 'Name', 'FirstName', 'LastName', 'Email', 'Phone', 'AccountId'
    };
    
    /**
     * Queries Contact records by ID
     * @param ids Set of Contact IDs to query
     * @return List of Contact records
     */
    public static List<Contact> selectById(Set<Id> ids) {
        if (ids == null || ids.isEmpty()) {
            return new List<Contact>();
        }
        
        String fields = String.join(DEFAULT_FIELDS, ', ');
        String query = 'SELECT ' + fields + 
                      ' FROM Contact' +
                      ' WHERE Id IN :ids' +
                      ' WITH SECURITY_ENFORCED' +
                      ' LIMIT 10000';
        
        return Database.query(query);
    }
    
    /**
     * Queries Contact records by External ID
     * @param externalIds Set of External ID values
     * @return List of Contact records
     */
    public static List<Contact> selectByExternalId(Set<String> externalIds) {
        if (externalIds == null || externalIds.isEmpty()) {
            return new List<Contact>();
        }
        
        String fields = String.join(DEFAULT_FIELDS, ', ');
        return [
            SELECT Id, Name, FirstName, LastName, Email, Phone, AccountId, ExternalId__c
            FROM Contact
            WHERE ExternalId__c IN :externalIds
            WITH SECURITY_ENFORCED
            LIMIT 10000
        ];
    }
    
    /**
     * Queries Contact records by Account ID
     * @param accountIds Set of Account IDs
     * @return List of Contact records
     */
    public static List<Contact> selectByAccountId(Set<Id> accountIds) {
        if (accountIds == null || accountIds.isEmpty()) {
            return new List<Contact>();
        }
        
        return [
            SELECT Id, Name, FirstName, LastName, Email, Phone, AccountId, Account.Name
            FROM Contact
            WHERE AccountId IN :accountIds
            WITH SECURITY_ENFORCED
            LIMIT 10000
        ];
    }
}
```

**Explanation**:
- **Security**: Uses `WITH SECURITY_ENFORCED` in all queries
- **Reusability**: Provides specific query methods
- **Bulkification**: Handles collections, not single records
- **Default Fields**: Defines standard field list
- **Null Safety**: Handles null/empty input gracefully

**Usage**:
```apex
Set<Id> contactIds = new Set<Id>{ '003000000000001', '003000000000002' };
List<Contact> contacts = ContactSelector.selectById(contactIds);
```

**Test Example**:
```apex
@isTest
private class ContactSelectorTest {
    
    @isTest
    static void testSelectById_Success() {
        List<Contact> testContacts = new List<Contact>{
            new Contact(LastName = 'Test1', Email = 'test1@example.com'),
            new Contact(LastName = 'Test2', Email = 'test2@example.com')
        };
        insert testContacts;
        
        Set<Id> contactIds = new Set<Id>();
        for (Contact c : testContacts) {
            contactIds.add(c.Id);
        }
        
        Test.startTest();
        List<Contact> results = ContactSelector.selectById(contactIds);
        Test.stopTest();
        
        System.assertEquals(2, results.size(), 'Should return 2 contacts');
    }
    
    @isTest
    static void testSelectById_EmptyInput() {
        Test.startTest();
        List<Contact> results = ContactSelector.selectById(new Set<Id>());
        Test.stopTest();
        
        System.assertEquals(0, results.size(), 'Should return empty list');
    }
}
```

---

### Example 2: Selector with Relationship Queries
**Pattern**: Selector with Parent/Child Relationships  
**Use Case**: Querying records with related data  
**Complexity**: Intermediate

**Problem**: 
You need to query Contact records with related Account and Case data in a single query.

**Solution**:
```apex
/**
 * Selector with relationship queries
 */
public with sharing class ContactSelector {
    
    /**
     * Queries Contact with Account and Cases
     * @param contactIds Set of Contact IDs
     * @return List of Contact records with related data
     */
    public static List<Contact> selectByIdWithRelationships(Set<Id> contactIds) {
        if (contactIds == null || contactIds.isEmpty()) {
            return new List<Contact>();
        }
        
        return [
            SELECT Id, Name, Email, Phone,
                   Account.Id, Account.Name, Account.Industry,
                   (SELECT Id, Subject, Status, CaseNumber FROM Cases)
            FROM Contact
            WHERE Id IN :contactIds
            WITH SECURITY_ENFORCED
            LIMIT 10000
        ];
    }
    
    /**
     * Queries Contacts by Account with Account details
     * @param accountIds Set of Account IDs
     * @return List of Contact records with Account data
     */
    public static List<Contact> selectByAccountWithAccountDetails(Set<Id> accountIds) {
        if (accountIds == null || accountIds.isEmpty()) {
            return new List<Contact>();
        }
        
        return [
            SELECT Id, Name, Email, Phone,
                   Account.Id, Account.Name, Account.Industry, Account.AnnualRevenue
            FROM Contact
            WHERE AccountId IN :accountIds
            WITH SECURITY_ENFORCED
            LIMIT 10000
        ];
    }
}
```

**Explanation**:
- **Relationship Queries**: Uses dot notation for parent fields
- **Subqueries**: Uses subquery syntax for child records
- **Single Query**: Reduces SOQL query count
- **Security**: Enforces security on all queries

**Usage**:
```apex
Set<Id> contactIds = new Set<Id>{ '003000000000001' };
List<Contact> contacts = ContactSelector.selectByIdWithRelationships(contactIds);

for (Contact contact : contacts) {
    String accountName = contact.Account.Name; // Parent field
    List<Case> cases = contact.Cases; // Child records
}
```

---

### Example 3: Selector with Dynamic Queries
**Pattern**: Selector with Dynamic Field Selection  
**Use Case**: Flexible queries with optional fields  
**Complexity**: Advanced

**Problem**: 
You need flexible query methods that can include optional fields based on requirements.

**Solution**:
```apex
/**
 * Selector with dynamic field selection
 */
public with sharing class ContactSelector {
    
    private static final List<String> BASE_FIELDS = new List<String>{
        'Id', 'Name', 'Email'
    };
    
    /**
     * Queries Contacts with optional fields
     * @param contactIds Set of Contact IDs
     * @param includeAccount Include Account fields
     * @param includeCases Include Cases subquery
     * @return List of Contact records
     */
    public static List<Contact> selectByIdWithOptions(
        Set<Id> contactIds, 
        Boolean includeAccount, 
        Boolean includeCases
    ) {
        if (contactIds == null || contactIds.isEmpty()) {
            return new List<Contact>();
        }
        
        List<String> fields = new List<String>(BASE_FIELDS);
        
        if (includeAccount) {
            fields.add('Account.Id');
            fields.add('Account.Name');
        }
        
        String query = 'SELECT ' + String.join(fields, ', ');
        
        if (includeCases) {
            query += ', (SELECT Id, Subject, Status FROM Cases)';
        }
        
        query += ' FROM Contact' +
                ' WHERE Id IN :contactIds' +
                ' WITH SECURITY_ENFORCED' +
                ' LIMIT 10000';
        
        return Database.query(query);
    }
}
```

**Best Practices**:
- Use specific method names rather than abstract criteria methods
- Provide common query patterns as separate methods
- Use dynamic queries only when necessary
- Always include `WITH SECURITY_ENFORCED`

---

### Example 4: Selector with Schema Imports
**Pattern**: Selector Using Schema Imports for Referential Integrity  
**Use Case**: Type-safe field references  
**Complexity**: Intermediate

**Problem**: 
You want to use schema imports for field references to protect against metadata changes.

**Solution**:
```apex
/**
 * Selector using schema imports
 * Note: Schema imports are LWC feature, but pattern applies to Apex
 * For Apex, use string constants or describe calls
 */
public with sharing class ContactSelector {
    
    // Field API names as constants (Apex pattern)
    private static final String FIELD_ID = 'Id';
    private static final String FIELD_NAME = 'Name';
    private static final String FIELD_EMAIL = 'Email';
    private static final String FIELD_ACCOUNT_ID = 'AccountId';
    
    /**
     * Queries Contacts using field constants
     * @param contactIds Set of Contact IDs
     * @return List of Contact records
     */
    public static List<Contact> selectById(Set<Id> contactIds) {
        if (contactIds == null || contactIds.isEmpty()) {
            return new List<Contact>();
        }
        
        // In real implementation, could use Schema.describeSObjectResult
        // to get field API names dynamically
        return [
            SELECT Id, Name, Email, Phone, AccountId
            FROM Contact
            WHERE Id IN :contactIds
            WITH SECURITY_ENFORCED
            LIMIT 10000
        ];
    }
}
```

**Best Practices**:
- Use field constants for maintainability
- Consider using Schema.describeSObjectResult for dynamic field access
- Document field dependencies
- Update constants when fields change

---

## Common Patterns

### Pattern 1: Query by ID
```apex
public static List<Contact> selectById(Set<Id> ids) {
    // Query by ID with security enforcement
}
```

### Pattern 2: Query by External ID
```apex
public static List<Contact> selectByExternalId(Set<String> externalIds) {
    // Query by External ID for upsert operations
}
```

### Pattern 3: Query with Relationships
```apex
public static List<Contact> selectByIdWithAccount(Set<Id> ids) {
    // Query with parent object fields
}
```

### Pattern 4: Query with Subqueries
```apex
public static List<Contact> selectByIdWithCases(Set<Id> ids) {
    // Query with child object subquery
}
```

---

## Best Practices

1. **ALWAYS use `WITH SECURITY_ENFORCED`** or `WITH USER_MODE` in all queries
2. **Provide specific method names** (selectById, selectByExternalId) rather than abstract criteria methods
3. **Handle null/empty input** gracefully
4. **Use relationship queries** to reduce SOQL count
5. **Define default field lists** for consistency
6. **Should NOT contain business logic** (delegate to Domain layer)
7. **Should NOT contain external callouts** (delegate to Integration layer)
8. **Use indexed fields** in WHERE clauses for performance
9. **Limit query results** appropriately (LIMIT clause)
10. **Bulkify all queries** (process collections, not single records)

---

## Related Patterns

- <a href="{{ '/rag/code-examples/apex/code-examples/apex/service-layer-examples.html' | relative_url }}">Service Layer Examples</a> - Service layer patterns
- <a href="{{ '/rag/code-examples/apex/code-examples/apex/domain-layer-examples.html' | relative_url }}">Domain Layer Examples</a> - Domain layer patterns
- <a href="{{ '/rag/development/soql-query-patterns.html' | relative_url }}">SOQL Patterns</a> - SOQL query patterns
- <a href="{{ '/rag/development/apex-patterns.html' | relative_url }}">Apex Patterns</a> - Complete Apex patterns

