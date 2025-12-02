# Service Class Template

**Use Case**: Basic service class with error handling and logging

**Template**:
```apex
/**
 * Service class for [ObjectName] operations
 * Orchestrates workflow: query → validate → update → log
 */
public with sharing class [ClassName]Service {
    
    /**
     * [Method description]
     * @param [param] [Description]
     * @return [Description]
     */
    public static [ReturnType] [methodName]([Parameters]) {
        // Validate input
        if ([input] == null || [input].isEmpty()) {
            throw new IllegalArgumentException('[Input] cannot be null or empty');
        }
        
        try {
            // 1. Query using Selector layer
            List<[ObjectName]> records = [ObjectName]Selector.selectById([ids]);
            
            if (records.isEmpty()) {
                return [emptyResult];
            }
            
            // 2. Validate and apply business rules using Domain layer
            [ObjectName]Domain.validateAndPrepareForUpdate(records);
            
            // 3. Perform DML operation
            update records;
            
            // 4. Log success
            LOG_LogMessageUtility.logInfo(
                '[ClassName]Service',
                '[methodName]',
                'Successfully processed ' + records.size() + ' records'
            );
            
            // 5. Return result
            return [result];
            
        } catch (Exception e) {
            // Log error and rethrow
            LOG_LogMessageUtility.logError(
                '[ClassName]Service',
                '[methodName]',
                'Error processing records: ' + e.getMessage(),
                e
            );
            throw new [CustomException]('Failed to process records: ' + e.getMessage(), e);
        }
    }
    
    /**
     * Custom exception for [ClassName] errors
     */
    public class [CustomException] extends Exception {}
}
```

**Customization Points**:
- Replace `[ClassName]` with actual class name (e.g., `ContactUpdateService`)
- Replace `[ObjectName]` with actual object name (e.g., `Contact`)
- Replace `[methodName]` with actual method name
- Replace `[Parameters]` with actual parameters
- Replace `[ReturnType]` with actual return type
- Replace `[CustomException]` with custom exception name
- Add domain/selector delegation as needed
- Add additional workflow steps as needed

**Example Usage**:
```apex
// After customization:
public with sharing class ContactUpdateService {
    public static List<Id> processContacts(Set<Id> contactIds) {
        // Implementation
    }
    
    public class ContactUpdateException extends Exception {}
}
```

**Related Patterns**:
- [Service Layer Examples](../apex/service-layer-examples.md)
- [Apex Patterns](rag/development/apex-patterns.md#service-layer)

