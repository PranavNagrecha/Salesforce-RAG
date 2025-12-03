---
layout: default
title: Error Handling Code Examples
description: Robust error handling ensures applications gracefully handle failures and provide meaningful feedback
permalink: /rag/code-examples/utilities/error-handling-examples.html

**Problem**:
You need to handle exceptions gracefully in your Apex code.

**Solution**:

**Apex** (`ContactService.cls`):
```apex
/**
 * Service class with comprehensive error handling
 */
public with sharing class ContactService {
    
    /**
     * Updates contacts with error handling
     * @param contacts List of contacts to update
     * @return List of successfully updated contact IDs
     */
    public static List<Id> updateContacts(List<Contact> contacts) {
        List<Id> successIds = new List<Id>();
        List<Contact> contactsToUpdate = new List<Contact>();
        
        try {
            // Validate input
            if (contacts == null || contacts.isEmpty()) {
                throw new IllegalArgumentException('Contacts list cannot be null or empty');
            }
            
            // Prepare contacts for update
            for (Contact contact : contacts) {
                // Validate required fields
                if (String.isBlank(contact.LastName)) {
                    LOG_LogMessageUtility.logWarning(
                        'ContactService',
                        'updateContacts',
                        'Skipping contact with missing LastName: ' + contact.Id
                    );
                    continue;
                }
                contactsToUpdate.add(contact);
            }
            
            if (contactsToUpdate.isEmpty()) {
                LOG_LogMessageUtility.logWarning(
                    'ContactService',
                    'updateContacts',
                    'No valid contacts to update'
                );
                return successIds;
            }
            
            // Perform DML
            update contactsToUpdate;
            
            // Collect success IDs
            for (Contact contact : contactsToUpdate) {
                successIds.add(contact.Id);
            }
            
            LOG_LogMessageUtility.logInfo(
                'ContactService',
                'updateContacts',
                'Successfully updated ' + contactsToUpdate.size() + ' contacts'
            );
            
        } catch (DmlException e) {
            // Handle DML errors
            handleDmlException(e, contacts);
            
        } catch (IllegalArgumentException e) {
            // Handle validation errors
            LOG_LogMessageUtility.logError(
                'ContactService',
                'updateContacts',
                'Validation error: ' + e.getMessage(),
                e
            );
            throw e; // Re-throw validation errors
            
        } catch (Exception e) {
            // Handle unexpected errors
            LOG_LogMessageUtility.logError(
                'ContactService',
                'updateContacts',
                'Unexpected error: ' + e.getMessage(),
                e
            );
            throw new ContactServiceException('Failed to update contacts: ' + e.getMessage(), e);
        }
        
        return successIds;
    }
    
    /**
     * Handles DML exceptions with detailed error information
     * @param e DML exception
     * @param contacts Contacts that were being updated
     */
    private static void handleDmlException(DmlException e, List<Contact> contacts) {
        String errorMessage = 'DML error: ';
        
        for (Integer i = 0; i < e.getNumDml(); i++) {
            Integer recordIndex = e.getDmlIndex(i);
            String fieldErrors = '';
            
            for (String field : e.getDmlFieldNames(i)) {
                fieldErrors += field + ' ';
            }
            
            errorMessage += 'Record ' + recordIndex + 
                ' (' + contacts[recordIndex].Id + '): ' + 
                e.getDmlMessage(i) + 
                (String.isNotBlank(fieldErrors) ? ' Fields: ' + fieldErrors : '') + '; ';
        }
        
        LOG_LogMessageUtility.logError(
            'ContactService',
            'updateContacts',
            errorMessage,
            e
        );
        
        throw new ContactServiceException(errorMessage, e);
    }
    
    /**
     * Custom exception for Contact Service errors
     */
    public class ContactServiceException extends Exception {}
}
```

**Best Practices**:
- Always wrap DML in try-catch
- Validate input before processing
- Provide detailed error messages
- Log all errors for troubleshooting
- Use custom exceptions for business logic errors

### Example 2: Retry Logic with Exponential Backoff

**Pattern**: Retry logic with exponential backoff
**Use Case**: Handling transient failures (e.g., UNABLE_TO_LOCK_ROW)
**Complexity**: Intermediate
**Related Patterns**: <a href="{{ '/rag/development/locking-and-concurrency-strategies.html' | relative_url }}">Locking and Concurrency Strategies</a>

**Problem**:
You need to retry operations that may fail due to transient errors.

**Solution**:

**Apex** (`RetryService.cls`):
```apex
/**
 * Service for retrying operations with exponential backoff
 */
public with sharing class RetryService {
    
    private static final Integer MAX_RETRIES = 3;
    private static final Integer INITIAL_DELAY_MS = 1000; // 1 second
    
    /**
     * Retries an operation with exponential backoff
     * @param operation Operation to retry (callable)
     * @return Operation result
     */
    public static Object retryWithBackoff(RetryableOperation operation) {
        Integer attempt = 0;
        Exception lastException = null;
        
        while (attempt < MAX_RETRIES) {
            try {
                return operation.execute();
                
            } catch (DmlException e) {
                lastException = e;
                
                // Check if error is retryable
                if (isRetryableError(e)) {
                    attempt++;
                    
                    if (attempt < MAX_RETRIES) {
                        // Calculate delay with exponential backoff
                        Integer delayMs = INITIAL_DELAY_MS * (Integer) Math.pow(2, attempt - 1);
                        
                        LOG_LogMessageUtility.logWarning(
                            'RetryService',
                            'retryWithBackoff',
                            'Retryable error on attempt ' + attempt + 
                            ', retrying after ' + delayMs + 'ms: ' + e.getMessage()
                        );
                        
                        // Wait before retry
                        waitFor(delayMs);
                    }
                } else {
                    // Non-retryable error - throw immediately
                    throw e;
                }
                
            } catch (Exception e) {
                // Non-retryable error - throw immediately
                throw e;
            }
        }
        
        // Max retries reached
        throw new RetryException('Operation failed after ' + MAX_RETRIES + ' attempts: ' + 
            (lastException != null ? lastException.getMessage() : 'Unknown error'), lastException);
    }
    
    /**
     * Checks if error is retryable
     * @param e DML exception
     * @return True if error is retryable
     */
    private static Boolean isRetryableError(DmlException e) {
        String errorCode = e.getDmlType(0).name();
        
        // Retryable errors
        Set<String> retryableErrors = new Set<String>{
            'UNABLE_TO_LOCK_ROW',
            'REQUEST_RUNNING_TOO_LONG',
            'CONCURRENT_REQUEST_ERROR'
        };
        
        return retryableErrors.contains(errorCode);
    }
    
    /**
     * Waits for specified milliseconds
     * @param milliseconds Milliseconds to wait
     */
    private static void waitFor(Integer milliseconds) {
        Long startTime = System.currentTimeMillis();
        while (System.currentTimeMillis() - startTime < milliseconds) {
            // Busy wait (not ideal but works in Apex)
        }
    }
    
    /**
     * Interface for retryable operations
     */
    public interface RetryableOperation {
        Object execute();
    }
    
    /**
     * Custom exception for retry failures
     */
    public class RetryException extends Exception {}
}
```

**Usage**:
```apex
// Use retry service
List<Id> result = (List<Id>) RetryService.retryWithBackoff(new RetryService.RetryableOperation() {
    public Object execute() {
        return ContactService.updateContacts(contacts);
    }
});
```

**Best Practices**:
- Identify retryable vs non-retryable errors
- Use exponential backoff for retries
- Set maximum retry attempts
- Log retry attempts for monitoring

### Example 3: Queueable-Based Retry Pattern

**Pattern**: Retrying operations using Queueable
**Use Case**: Retrying operations asynchronously
**Complexity**: Intermediate
**Related Patterns**: <a href="{{ '/rag/development/asynchronous-apex-patterns.html' | relative_url }}">Asynchronous Apex Patterns</a>

**Problem**:
You need to retry operations asynchronously without blocking the current transaction.

**Solution**:

**Apex** (`QueueableRetryService.cls`):
```apex
/**
 * Queueable service for retrying operations
 */
public with sharing class QueueableRetryService implements Queueable {
    
    private String operationType;
    private Map<String, Object> operationParams;
    private Integer retryCount;
    private static final Integer MAX_RETRIES = 3;
    
    public QueueableRetryService(String operationType, Map<String, Object> operationParams) {
        this.operationType = operationType;
        this.operationParams = operationParams;
        this.retryCount = 0;
    }
    
    public QueueableRetryService(String operationType, Map<String, Object> operationParams, Integer retryCount) {
        this.operationType = operationType;
        this.operationParams = operationParams;
        this.retryCount = retryCount;
    }
    
    public void execute(QueueableContext context) {
        try {
            // Execute operation based on type
            Object result = executeOperation();
            
            LOG_LogMessageUtility.logInfo(
                'QueueableRetryService',
                'execute',
                'Operation succeeded: ' + operationType + ' (attempt ' + (retryCount + 1) + ')'
            );
            
        } catch (Exception e) {
            retryCount++;
            
            if (retryCount < MAX_RETRIES && isRetryableError(e)) {
                // Retry operation
                LOG_LogMessageUtility.logWarning(
                    'QueueableRetryService',
                    'execute',
                    'Operation failed, retrying: ' + operationType + 
                    ' (attempt ' + retryCount + ' of ' + MAX_RETRIES + ') - ' + e.getMessage()
                );
                
                System.enqueueJob(new QueueableRetryService(operationType, operationParams, retryCount));
                
            } else {
                // Max retries reached or non-retryable error
                LOG_LogMessageUtility.logError(
                    'QueueableRetryService',
                    'execute',
                    'Operation failed after ' + retryCount + ' attempts: ' + operationType + ' - ' + e.getMessage(),
                    e
                );
                
                // Mark operation as failed
                markOperationAsFailed(e);
            }
        }
    }
    
    /**
     * Executes operation based on type
     * @return Operation result
     */
    private Object executeOperation() {
        if (operationType == 'updateContacts') {
            List<Contact> contacts = (List<Contact>) operationParams.get('contacts');
            return ContactService.updateContacts(contacts);
        }
        // Add other operation types as needed
        
        throw new IllegalArgumentException('Unknown operation type: ' + operationType);
    }
    
    /**
     * Checks if error is retryable
     * @param e Exception
     * @return True if error is retryable
     */
    private Boolean isRetryableError(Exception e) {
        if (e instanceof DmlException) {
            DmlException dmlEx = (DmlException) e;
            String errorCode = dmlEx.getDmlType(0).name();
            return errorCode == 'UNABLE_TO_LOCK_ROW';
        }
        return false;
    }
    
    /**
     * Marks operation as failed
     * @param e Exception
     */
    private void markOperationAsFailed(Exception e) {
        // Implementation depends on use case
        // Could create a failure record, send notification, etc.
    }
}
```

**Usage**:
```apex
// Enqueue retryable operation
Map<String, Object> params = new Map<String, Object>{
    'contacts' => contactsToUpdate
};
System.enqueueJob(new QueueableRetryService('updateContacts', params));
```

**Best Practices**:
- Use Queueable for async retries
- Track retry count
- Only retry retryable errors
- Mark operations as failed after max retries

## Related Examples

- <a href="{{ '/rag/development/asynchronous-apex-patterns.html' | relative_url }}">Asynchronous Apex Patterns</a> - Async patterns

