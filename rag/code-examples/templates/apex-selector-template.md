---
layout: default
title: Selector Class Template
description: Documentation for Selector Class Template
permalink: /rag/code-examples/templates/apex-selector-template.html
---

# Selector Class Template

**Use Case**: Basic selector class with security enforcement

**Template**:
```apex
/**
 * Selector class for [ObjectName] object
 * Centralized SOQL queries with security enforcement
 */
public with sharing class [ObjectName]Selector {
    
    /**
     * Default field list for [ObjectName] queries
     */
    private static final List<String> DEFAULT_FIELDS = new List<String>{
        'Id', 'Name' // Add other default fields
    };
    
    /**
     * Queries [ObjectName] records by ID
     * @param ids Set of [ObjectName] IDs to query
     * @return List of [ObjectName] records
     */
    public static List<[ObjectName]> selectById(Set<Id> ids) {
        if (ids == null || ids.isEmpty()) {
            return new List<[ObjectName]>();
        }
        
        return [
            SELECT Id, Name // Add other fields
            FROM [ObjectName]
            WHERE Id IN :ids
            WITH SECURITY_ENFORCED
            LIMIT 10000
        ];
    }
    
    /**
     * Queries [ObjectName] records by External ID
     * @param externalIds Set of External ID values
     * @return List of [ObjectName] records
     */
    public static List<[ObjectName]> selectByExternalId(Set<String> externalIds) {
        if (externalIds == null || externalIds.isEmpty()) {
            return new List<[ObjectName]>();
        }
        
        return [
            SELECT Id, Name, ExternalId__c // Add other fields
            FROM [ObjectName]
            WHERE ExternalId__c IN :externalIds
            WITH SECURITY_ENFORCED
            LIMIT 10000
        ];
    }
}
```

**Customization Points**:
- Replace `[ObjectName]` with actual object name (e.g., `Contact`)
- Add default fields to `DEFAULT_FIELDS` list
- Add fields to SELECT clauses
- Add additional query methods as needed
- Customize WHERE clauses for specific use cases

**Related Patterns**:
- <a href="{{ '/rag/development/soql-query-patterns.html' | relative_url }}">SOQL Patterns</a>

