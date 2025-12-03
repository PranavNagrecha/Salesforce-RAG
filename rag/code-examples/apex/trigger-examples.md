---
layout: default
title: Trigger Handler Code Examples
description: Trigger handlers process trigger events with bulkification, error handling, and proper layer delegation
permalink: /rag/code-examples/apex/trigger-examples.html

**Problem**: 
You need a trigger handler that validates Contact records before insert/update.

**Solution**:
```apex
/**
 * Trigger handler for Contact object
 * Delegates to Domain layer for validation
 */
public with sharing class ContactTriggerHandler {
    
    /**
     * Handles before insert events
     * @param newContacts List of new Contact records
     */
    public static void handleBeforeInsert(List<Contact> newContacts) {
        ContactDomain.validateForInsert(newContacts);
    }
    
    /**
     * Handles before update events
     * @param newContacts List of updated Contact records
     * @param oldContacts Map of old Contact records
     */
    public static void handleBeforeUpdate(List<Contact> newContacts, Map<Id, Contact> oldContacts) {
        ContactDomain.validateAndPrepareForUpdate(newContacts);
    }
    
    /**
     * Handles after insert events
     * @param newContacts List of new Contact records
     */
    public static void handleAfterInsert(List<Contact> newContacts) {
        // Post-insert processing (e.g., create related records, send notifications)
    }
    
    /**
     * Handles after update events
     * @param newContacts List of updated Contact records
     * @param oldContacts Map of old Contact records
     */
    public static void handleAfterUpdate(List<Contact> newContacts, Map<Id, Contact> oldContacts) {
        // Post-update processing
    }
}
```

**Trigger**:
```apex
trigger ContactTrigger on Contact (before insert, before update, after insert, after update) {
    if (Trigger.isBefore) {
        if (Trigger.isInsert) {
            ContactTriggerHandler.handleBeforeInsert(Trigger.new);
        } else if (Trigger.isUpdate) {
            ContactTriggerHandler.handleBeforeUpdate(Trigger.new, Trigger.oldMap);
        }
    } else if (Trigger.isAfter) {
        if (Trigger.isInsert) {
            ContactTriggerHandler.handleAfterInsert(Trigger.new);
        } else if (Trigger.isUpdate) {
            ContactTriggerHandler.handleAfterUpdate(Trigger.new, Trigger.oldMap);
        }
    }
}
```

**Explanation**:
- **Thin Trigger**: Trigger only routes to handler
- **Bulkification**: Handles collections, not single records
- **Delegation**: Delegates to Domain layer for validation
- **Separation**: Before vs after logic separated
- For broader framework guidance, see `trigger-framework-patterns.md` under Development patterns.

**Test Example**:
```apex
@isTest
private class ContactTriggerHandlerTest {
    
    @isTest
    static void testHandleBeforeInsert_Success() {
        List<Contact> contacts = new List<Contact>{
            new Contact(LastName = 'Test1', Email = 'test1@example.com'),
            new Contact(LastName = 'Test2', Email = 'test2@example.com')
        };
        
        Test.startTest();
        insert contacts;
        Test.stopTest();
        
        // Verify records inserted
        System.assertEquals(2, [SELECT COUNT() FROM Contact], 'Should insert 2 contacts');
    }
    
    @isTest
    static void testHandleBeforeInsert_ValidationFailure() {
        List<Contact> contacts = new List<Contact>{
            new Contact(Email = 'test@example.com')
            // Missing LastName
        };
        
        Test.startTest();
        try {
            insert contacts;
            System.assert(false, 'Should throw validation error');
        } catch (DmlException e) {
            System.assert(e.getMessage().contains('Last Name'), 'Should validate Last Name');
        }
        Test.stopTest();
    }
}
```

---

### Example 2: Trigger Handler with Service Layer
**Pattern**: Trigger Handler with Service Layer for Complex Workflows  
**Use Case**: Complex business processes triggered by DML  
**Complexity**: Intermediate

**Problem**: 
You need to orchestrate complex workflows when Contacts are updated, requiring Service layer coordination.

**Solution**:
```apex
/**
 * Trigger handler with Service layer for complex workflows
 */
public with sharing class ContactTriggerHandler {
    
    public static void handleAfterUpdate(List<Contact> newContacts, Map<Id, Contact> oldContacts) {
        // Identify contacts that need processing
        List<Contact> contactsToProcess = new List<Contact>();
        
        for (Contact newContact : newContacts) {
            Contact oldContact = oldContacts.get(newContact.Id);
            
            // Only process if Email changed
            if (newContact.Email != oldContact.Email) {
                contactsToProcess.add(newContact);
            }
        }
        
        if (!contactsToProcess.isEmpty()) {
            // Delegate to Service layer for complex workflow
            Set<Id> contactIds = new Set<Id>();
            for (Contact c : contactsToProcess) {
                contactIds.add(c.Id);
            }
            
            ContactUpdateService.processContacts(contactIds);
        }
    }
}
```

**Best Practices**:
- Use Service layer for complex workflows
- Use Domain layer for simple validation
- Check field changes before processing
- Bulkify all operations

---

### Example 3: Trigger Handler with Recursion Prevention
**Pattern**: Trigger Handler with Recursion Prevention  
**Use Case**: Preventing infinite trigger loops  
**Complexity**: Intermediate

**Problem**: 
You need to prevent trigger recursion when updates trigger additional updates.

**Solution**:
```apex
/**
 * Trigger handler with recursion prevention
 */
public with sharing class ContactTriggerHandler {
    
    private static Boolean isExecuting = false;
    
    public static void handleAfterUpdate(List<Contact> newContacts, Map<Id, Contact> oldContacts) {
        // Prevent recursion
        if (isExecuting) {
            return;
        }
        
        isExecuting = true;
        
        try {
            // Process updates
            List<Contact> contactsToUpdate = new List<Contact>();
            
            for (Contact newContact : newContacts) {
                Contact oldContact = oldContacts.get(newContact.Id);
                
                // Business logic that might trigger another update
                if (newContact.Email != oldContact.Email && String.isBlank(newContact.EmailVerified__c)) {
                    newContact.EmailVerified__c = 'Pending';
                    contactsToUpdate.add(newContact);
                }
            }
            
            if (!contactsToUpdate.isEmpty()) {
                // This update won't trigger recursion due to isExecuting flag
                update contactsToUpdate;
            }
            
        } finally {
            isExecuting = false;
        }
    }
}
```

**Alternative: Compare Field Values**
```apex
public static void handleAfterUpdate(List<Contact> newContacts, Map<Id, Contact> oldContacts) {
    List<Contact> contactsToUpdate = new List<Contact>();
    
    for (Contact newContact : newContacts) {
        Contact oldContact = oldContacts.get(newContact.Id);
        
        // Only process if specific field changed
        if (newContact.Email != oldContact.Email) {
            // Process only if field actually changed
            // This prevents recursion if update doesn't change the field
        }
    }
}
```

**Best Practices**:
- Use static flags for recursion prevention
- Compare old vs new values before processing
- Use try-finally to ensure flag is reset
- Document recursion prevention strategy

---

## Common Patterns

### Pattern 1: Thin Trigger
```apex
trigger ContactTrigger on Contact (before insert, before update) {
    if (Trigger.isBefore) {
        if (Trigger.isInsert) {
            ContactTriggerHandler.handleBeforeInsert(Trigger.new);
        }
    }
}
```

### Pattern 2: Bulkification
```apex
// Always process collections
public static void handleBeforeInsert(List<Contact> newContacts) {
    // Process all records, not single record
}
```

### Pattern 3: Field Change Detection
```apex
for (Contact newContact : newContacts) {
    Contact oldContact = oldContacts.get(newContact.Id);
    if (newContact.Email != oldContact.Email) {
        // Process only if field changed
    }
}
```

---

## Best Practices

1. **Keep triggers thin** - delegate to handlers
2. **Always bulkify** - process collections, not single records
3. **Use Domain layer** for simple validation
4. **Use Service layer** for complex workflows
5. **Prevent recursion** with static flags or field comparison
6. **Handle errors gracefully** with try-catch
7. **Log trigger execution** for debugging
8. **Test with bulk data** (200+ records)
9. **One trigger per object** (enforce via framework)
10. **Document trigger logic** clearly

---

## Related Patterns

- <a href="{{ '/rag/development/order-of-execution.html' | relative_url }}">Order of Execution</a> - Execution order