# Trigger Handler Template

**Use Case**: Basic trigger handler with Domain layer delegation

**Template**:
```apex
/**
 * Trigger handler for [ObjectName] object
 * Delegates to Domain layer for validation and Service layer for complex workflows
 */
public with sharing class [ObjectName]TriggerHandler {
    
    /**
     * Handles before insert events
     * @param newRecords List of new [ObjectName] records
     */
    public static void handleBeforeInsert(List<[ObjectName]> newRecords) {
        [ObjectName]Domain.validateForInsert(newRecords);
    }
    
    /**
     * Handles before update events
     * @param newRecords List of updated [ObjectName] records
     * @param oldRecords Map of old [ObjectName] records
     */
    public static void handleBeforeUpdate(List<[ObjectName]> newRecords, Map<Id, [ObjectName]> oldRecords) {
        [ObjectName]Domain.validateAndPrepareForUpdate(newRecords);
    }
    
    /**
     * Handles after insert events
     * @param newRecords List of new [ObjectName] records
     */
    public static void handleAfterInsert(List<[ObjectName]> newRecords) {
        // Post-insert processing
        // Delegate to Service layer for complex workflows
    }
    
    /**
     * Handles after update events
     * @param newRecords List of updated [ObjectName] records
     * @param oldRecords Map of old [ObjectName] records
     */
    public static void handleAfterUpdate(List<[ObjectName]> newRecords, Map<Id, [ObjectName]> oldRecords) {
        // Post-update processing
        // Delegate to Service layer for complex workflows
    }
}
```

**Trigger Template**:
```apex
trigger [ObjectName]Trigger on [ObjectName] (before insert, before update, after insert, after update) {
    if (Trigger.isBefore) {
        if (Trigger.isInsert) {
            [ObjectName]TriggerHandler.handleBeforeInsert(Trigger.new);
        } else if (Trigger.isUpdate) {
            [ObjectName]TriggerHandler.handleBeforeUpdate(Trigger.new, Trigger.oldMap);
        }
    } else if (Trigger.isAfter) {
        if (Trigger.isInsert) {
            [ObjectName]TriggerHandler.handleAfterInsert(Trigger.new);
        } else if (Trigger.isUpdate) {
            [ObjectName]TriggerHandler.handleAfterUpdate(Trigger.new, Trigger.oldMap);
        }
    }
}
```

**Customization Points**:
- Replace `[ObjectName]` with actual object name (e.g., `Contact`)
- Add specific trigger events as needed (before delete, after delete, after undelete)
- Add recursion prevention if needed
- Add field change detection logic
- Delegate to Service layer for complex workflows

**Related Patterns**:
- [Trigger Examples](rag/code-examples/apex/trigger-examples.md)
- [Apex Patterns](rag/development/apex-patterns.md)
- [Order of Execution](rag/development/order-of-execution.md)

