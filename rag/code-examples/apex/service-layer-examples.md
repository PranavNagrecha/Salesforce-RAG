# Service Layer Code Examples

> This file contains complete, working code examples for Apex Service Layer patterns.
> All examples are copy-paste ready and follow Salesforce best practices.

## Overview

The Service Layer coordinates between domain, selector, and integration layers. It orchestrates complex workflows and exposes clean method signatures for Flows and LWCs.

**Related Patterns**:

- <a href="{{ '/rag/code-examples/apex/Salesforce-RAG/rag/development/apex-patterns.html#apex-class-layering.html' | relative_url }}">Apex Class Layering</a>
- <a href="{{ '/rag/code-examples/apex/Salesforce-RAG/rag/development/apex-patterns.html#service-layer.html' | relative_url }}">Service Layer Pattern</a>

## Examples

### Example 1: Basic Service Class

**Pattern**: Service Layer with Domain and Selector Delegation
**Use Case**: Orchestrating a simple update workflow
**Complexity**: Basic
**Related Patterns**: <a href="{{ '/rag/code-examples/apex/Salesforce-RAG/rag/development/apex-patterns.html#domain-layer.html' | relative_url }}">Domain Layer</a>, <a href="{{ '/rag/code-examples/apex/Salesforce-RAG/rag/development/apex-patterns.html#selector-layer.html' | relative_url }}">Selector Layer</a>

**Problem**:
You need to update records with validation and business logic. The service layer orchestrates the workflow by delegating to domain and selector layers.

**Solution**:

```apex
/**
 * Service class for processing Contact updates
 * Orchestrates workflow: query → validate → update → log
 */
public with sharing class ContactUpdateService {
  
    /**
     * Updates contacts with validation and business logic
     * @param contactIds Set of Contact IDs to update
     * @return List of processed Contact IDs
     */
    public static List<Id> processContacts(Set<Id> contactIds) {
        // Validate input
        if (contactIds == null || contactIds.isEmpty()) {
            throw new IllegalArgumentException('Contact IDs cannot be null or empty');
        }
      
        try {
            // 1. Query contacts using Selector layer
            List<Contact> contacts = ContactSelector.selectByIds(contactIds);
          
            if (contacts.isEmpty()) {
                return new List<Id>();
            }
          
            // 2. Validate and apply business rules using Domain layer
            ContactDomain.validateAndPrepareForUpdate(contacts);
          
            // 3. Perform DML operation
            update contacts;
          
            // 4. Log success
            LOG_LogMessageUtility.logInfo(
                'ContactUpdateService',
                'processContacts',
                'Successfully updated ' + contacts.size() + ' contacts'
            );
          
            // 5. Return processed IDs
            List<Id> processedIds = new List<Id>();
            for (Contact c : contacts) {
                processedIds.add(c.Id);
            }
            return processedIds;
          
        } catch (Exception e) {
            // Log error and rethrow
            LOG_LogMessageUtility.logError(
                'ContactUpdateService',
                'processContacts',
                'Error updating contacts: ' + e.getMessage(),
                e
            );
            throw new ContactUpdateException('Failed to update contacts: ' + e.getMessage(), e);
        }
    }
  
    /**
     * Custom exception for Contact update errors
     */
    public class ContactUpdateException extends Exception {}
}
```

**Explanation**:

- **Delegation**: Service delegates to Selector (data access) and Domain (validation)
- **Error Handling**: Wraps operations in try-catch with logging
- **Bulkification**: Processes collections, not single records
- **Security**: Uses `with sharing` to respect sharing rules
- **Logging**: Logs both success and errors

**Usage**:

```apex
// In a trigger, Flow, or LWC
Set<Id> contactIds = new Set<Id>{ '003000000000001', '003000000000002' };
List<Id> processedIds = ContactUpdateService.processContacts(contactIds);
```

**Test Example**:

```apex
@isTest
private class ContactUpdateServiceTest {
  
    @isTest
    static void testProcessContacts_Success() {
        // Create test data
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
        List<Id> processedIds = ContactUpdateService.processContacts(contactIds);
        Test.stopTest();
      
        // Verify results
        System.assertEquals(2, processedIds.size(), 'Should process 2 contacts');
        System.assert(processedIds.contains(testContacts[0].Id), 'Should contain first contact');
        System.assert(processedIds.contains(testContacts[1].Id), 'Should contain second contact');
    }
  
    @isTest
    static void testProcessContacts_EmptyInput() {
        Test.startTest();
        try {
            ContactUpdateService.processContacts(new Set<Id>());
            System.assert(false, 'Should throw exception for empty input');
        } catch (IllegalArgumentException e) {
            System.assert(e.getMessage().contains('cannot be null or empty'), 'Should throw appropriate error');
        }
        Test.stopTest();
    }
}
```

**Variations**:

- **Variation 1: Service with Integration Callout**
  ```apex
  // After update, call external system
  public static List<Id> processContactsWithSync(Set<Id> contactIds) {
      List<Id> processedIds = processContacts(contactIds);
      // Call integration layer to sync to external system
      ExternalSystemIntegrationService.syncContacts(processedIds);
      return processedIds;
  }
  ```

---

### Example 2: Service with Complex Workflow

**Pattern**: Service Layer Orchestrating Multi-Step Workflow
**Use Case**: Complex business process with multiple steps
**Complexity**: Intermediate
**Related Patterns**: <a href="{{ '/rag/code-examples/apex/Salesforce-RAG/rag/development/apex-patterns.html#service-layer.html' | relative_url }}">Service Layer</a>, <a href="{{ '/rag/development/error-handling-and-logging.html' | relative_url }}">Error Handling</a>

**Problem**:
You need to orchestrate a complex workflow: query related records → validate → update multiple objects → send notifications → log results.

**Solution**:

```apex
/**
 * Service class for processing Account and related Contact updates
 * Orchestrates complex workflow with multiple steps
 */
public with sharing class AccountContactUpdateService {
  
    /**
     * Processes Account and related Contacts in a coordinated workflow
     * @param accountId Account ID to process
     * @return ProcessingResult with success status and details
     */
    public static ProcessingResult processAccountWithContacts(Id accountId) {
        ProcessingResult result = new ProcessingResult();
        result.accountId = accountId;
      
        try {
            // Step 1: Query Account and related Contacts using Selector
            Account account = AccountSelector.selectByIdWithContacts(accountId);
            if (account == null) {
                result.addError('Account not found: ' + accountId);
                return result;
            }
          
            // Step 2: Validate Account using Domain layer
            AccountDomain.validateForUpdate(account);
          
            // Step 3: Validate related Contacts using Domain layer
            List<Contact> contacts = account.Contacts;
            if (contacts != null && !contacts.isEmpty()) {
                ContactDomain.validateAndPrepareForUpdate(contacts);
            }
          
            // Step 4: Update Account
            update account;
            result.addSuccess('Account updated successfully');
          
            // Step 5: Update Contacts if any
            if (contacts != null && !contacts.isEmpty()) {
                update contacts;
                result.addSuccess('Updated ' + contacts.size() + ' contacts');
            }
          
            // Step 6: Send notification (could be async)
            NotificationService.sendAccountUpdateNotification(accountId);
          
            result.isSuccess = true;
          
            // Step 7: Log success
            LOG_LogMessageUtility.logInfo(
                'AccountContactUpdateService',
                'processAccountWithContacts',
                'Successfully processed Account: ' + accountId
            );
          
        } catch (AccountDomain.AccountValidationException e) {
            result.addError('Validation failed: ' + e.getMessage());
            LOG_LogMessageUtility.logError(
                'AccountContactUpdateService',
                'processAccountWithContacts',
                'Validation error: ' + e.getMessage(),
                e
            );
        } catch (Exception e) {
            result.addError('Unexpected error: ' + e.getMessage());
            LOG_LogMessageUtility.logError(
                'AccountContactUpdateService',
                'processAccountWithContacts',
                'Error processing Account: ' + e.getMessage(),
                e
            );
        }
      
        return result;
    }
  
    /**
     * Result class for processing operations
     */
    public class ProcessingResult {
        public Id accountId;
        public Boolean isSuccess = false;
        public List<String> messages = new List<String>();
        public List<String> errors = new List<String>();
      
        public void addSuccess(String message) {
            messages.add(message);
        }
      
        public void addError(String error) {
            errors.add(error);
            isSuccess = false;
        }
    }
}
```

**Explanation**:

- **Orchestration**: Coordinates multiple steps in sequence
- **Error Handling**: Catches specific exceptions (validation) and general exceptions
- **Result Object**: Returns structured result with success/error details
- **Delegation**: Uses Selector, Domain, and other Service layers
- **Logging**: Logs at each critical step

**Usage**:

```apex
// In a Flow, trigger, or LWC
Id accountId = '001000000000001';
AccountContactUpdateService.ProcessingResult result = 
    AccountContactUpdateService.processAccountWithContacts(accountId);

if (result.isSuccess) {
    System.debug('Success: ' + result.messages);
} else {
    System.debug('Errors: ' + result.errors);
}
```

**Test Example**:

```apex
@isTest
private class AccountContactUpdateServiceTest {
  
    @isTest
    static void testProcessAccountWithContacts_Success() {
        // Create test data
        Account testAccount = new Account(Name = 'Test Account');
        insert testAccount;
      
        List<Contact> testContacts = new List<Contact>{
            new Contact(AccountId = testAccount.Id, LastName = 'Contact1', Email = 'c1@example.com'),
            new Contact(AccountId = testAccount.Id, LastName = 'Contact2', Email = 'c2@example.com')
        };
        insert testContacts;
      
        Test.startTest();
        AccountContactUpdateService.ProcessingResult result = 
            AccountContactUpdateService.processAccountWithContacts(testAccount.Id);
        Test.stopTest();
      
        // Verify results
        System.assert(result.isSuccess, 'Should succeed');
        System.assertEquals(testAccount.Id, result.accountId, 'Should return correct account ID');
        System.assert(result.messages.size() > 0, 'Should have success messages');
    }
}
```

---

### Example 3: Service with Queueable for Async Processing

**Pattern**: Service Layer with Asynchronous Processing
**Use Case**: Long-running operations that should be async
**Complexity**: Advanced
**Related Patterns**: <a href="{{ '/rag/code-examples/apex/Salesforce-RAG/rag/development/apex-patterns.html#queueable.html' | relative_url }}">Queueable Pattern</a>, <a href="{{ '/rag/code-examples/apex/Salesforce-RAG/rag/development/apex-patterns.html#asynchronous-apex-patterns.html' | relative_url }}">Asynchronous Apex</a>

**Problem**:
You need to process a large number of records asynchronously, potentially chaining multiple jobs.

**Solution**:

```apex
/**
 * Service class for bulk Contact processing
 * Uses Queueable for asynchronous processing
 */
public with sharing class ContactBulkProcessService {
  
    /**
     * Enqueues async job to process contacts
     * @param contactIds Set of Contact IDs to process
     * @return Job ID of enqueued job
     */
    public static Id processContactsAsync(Set<Id> contactIds) {
        if (contactIds == null || contactIds.isEmpty()) {
            throw new IllegalArgumentException('Contact IDs cannot be null or empty');
        }
      
        // Enqueue Queueable job
        ContactBulkProcessQueueable job = new ContactBulkProcessQueueable(contactIds);
        Id jobId = System.enqueueJob(job);
      
        LOG_LogMessageUtility.logInfo(
            'ContactBulkProcessService',
            'processContactsAsync',
            'Enqueued job ' + jobId + ' to process ' + contactIds.size() + ' contacts'
        );
      
        return jobId;
    }
  
    /**
     * Queueable class for processing contacts asynchronously
     */
    public class ContactBulkProcessQueueable implements Queueable {
        private Set<Id> contactIds;
      
        public ContactBulkProcessQueueable(Set<Id> contactIds) {
            this.contactIds = contactIds;
        }
      
        public void execute(QueueableContext context) {
            try {
                // Process contacts in batches
                List<Contact> contacts = ContactSelector.selectByIds(contactIds);
              
                if (contacts.isEmpty()) {
                    return;
                }
              
                // Apply business logic
                ContactDomain.validateAndPrepareForUpdate(contacts);
              
                // Update contacts
                update contacts;
              
                // Log success
                LOG_LogMessageUtility.logInfo(
                    'ContactBulkProcessQueueable',
                    'execute',
                    'Successfully processed ' + contacts.size() + ' contacts in job ' + context.getJobId()
                );
              
            } catch (Exception e) {
                LOG_LogMessageUtility.logError(
                    'ContactBulkProcessQueueable',
                    'execute',
                    'Error processing contacts in job ' + context.getJobId() + ': ' + e.getMessage(),
                    e
                );
                throw e; // Re-throw to mark job as failed
            }
        }
    }
}
```

**Explanation**:

- **Async Processing**: Uses Queueable for long-running operations
- **Job Tracking**: Returns job ID for tracking
- **Error Handling**: Logs errors and re-throws to mark job as failed
- **Bulkification**: Processes collections asynchronously
- **Logging**: Logs job start and completion

**Usage**:

```apex
// In a trigger or Flow
Set<Id> contactIds = new Set<Id>{ '003000000000001', '003000000000002' };
Id jobId = ContactBulkProcessService.processContactsAsync(contactIds);
System.debug('Job ID: ' + jobId);
```

**Test Example**:

```apex
@isTest
private class ContactBulkProcessServiceTest {
  
    @isTest
    static void testProcessContactsAsync() {
        // Create test data
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
        Id jobId = ContactBulkProcessService.processContactsAsync(contactIds);
        Test.stopTest();
      
        // Verify job was enqueued
        System.assertNotEquals(null, jobId, 'Job ID should not be null');
      
        // Verify contacts were processed (in real scenario, would query updated records)
    }
}
```

---

## Common Patterns

### Pattern 1: Service with Flow Integration

Services can be called from Flows using `@InvocableMethod`:

```apex
public with sharing class ContactUpdateService {
  
    @InvocableMethod(label='Process Contacts' description='Updates contacts with validation')
    public static List<ProcessingResult> processContactsInvocable(List<ContactInput> inputs) {
        List<ProcessingResult> results = new List<ProcessingResult>();
      
        for (ContactInput input : inputs) {
            ProcessingResult result = new ProcessingResult();
            try {
                List<Id> processedIds = processContacts(input.contactIds);
                result.isSuccess = true;
                result.processedCount = processedIds.size();
            } catch (Exception e) {
                result.isSuccess = false;
                result.errorMessage = e.getMessage();
            }
            results.add(result);
        }
      
        return results;
    }
  
    public class ContactInput {
        @InvocableVariable(label='Contact IDs' required=true)
        public Set<Id> contactIds;
    }
  
    public class ProcessingResult {
        @InvocableVariable
        public Boolean isSuccess;
      
        @InvocableVariable
        public Integer processedCount;
      
        @InvocableVariable
        public String errorMessage;
    }
}
```

### Pattern 2: Service with LWC Integration

Services expose clean methods for LWCs:

```apex
public with sharing class ContactService {
  
    @AuraEnabled(cacheable=false)
    public static ContactViewModel getContactDetails(Id contactId) {
        Contact contact = ContactSelector.selectById(contactId);
        return new ContactViewModel(contact);
    }
  
    @AuraEnabled(cacheable=false)
    public static void updateContact(ContactViewModel viewModel) {
        Contact contact = ContactSelector.selectById(viewModel.id);
        // Map view model to contact
        contact.Email = viewModel.email;
        contact.Phone = viewModel.phone;
      
        ContactDomain.validateAndPrepareForUpdate(new List<Contact>{ contact });
        update contact;
    }
  
    public class ContactViewModel {
        @AuraEnabled public Id id;
        @AuraEnabled public String email;
        @AuraEnabled public String phone;
      
        public ContactViewModel(Contact c) {
            this.id = c.Id;
            this.email = c.Email;
            this.phone = c.Phone;
        }
    }
}
```

---

## Best Practices

1. **Always use `with sharing` or `without sharing`** explicitly
2. **Delegate to appropriate layers** (Selector for queries, Domain for validation)
3. **Handle errors gracefully** with try-catch and logging
4. **Process collections** (bulkification), not single records
5. **Return structured results** for complex operations
6. **Log all operations** for debugging and audit trails
7. **Use meaningful method names** that describe what they do
8. **Document method parameters and return values**
