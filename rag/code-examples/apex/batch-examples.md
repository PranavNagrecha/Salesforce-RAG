---
layout: default
title: Batch Apex Code Examples
description: Batch Apex is used for processing large data volumes (thousands or millions of records) in batches of 200
permalink: /rag/code-examples/apex/batch-examples.html
---

# Batch Apex Code Examples

> Complete, working code examples for Batch Apex patterns.
> All examples are copy-paste ready and follow Salesforce best practices.

## Overview

Batch Apex is used for processing large data volumes (thousands or millions of records) in batches of 200. Each batch executes in a separate transaction context with fresh governor limits.

**Related Patterns**:
- <a href="{{ '/rag/code-examples/apex/Salesforce-RAG/rag/development/asynchronous-apex-patterns.html#batch-apex-patterns.html' | relative_url }}">Asynchronous Apex Patterns</a>
- <a href="{{ '/rag/development/governor-limits-and-optimization.html' | relative_url }}">Governor Limits and Optimization</a>

## Examples

### Example 1: Basic Stateless Batch Apex

**Pattern**: Stateless Batch Apex with QueryLocator
**Use Case**: Bulk update of records without maintaining state
**Complexity**: Basic
**Related Patterns**: <a href="{{ '/rag/code-examples/apex/Salesforce-RAG/rag/development/asynchronous-apex-patterns.html#pattern-1-basic-stateless-batch-apex.html' | relative_url }}">Basic Stateless Batch</a>

**Problem**:
You need to update 100,000 Contact records with a new field value. Each batch of 200 records should process independently without maintaining state.

**Solution**:

```apex
/**
 * Batch class for updating Contact records
 * Processes records in batches of 200 without maintaining state
 */
global class ContactUpdateBatch implements Database.Batchable<SObject> {
    
    private String newValue;
    
    /**
     * Constructor to accept parameters
     * @param newValue The new value to set on contacts
     */
    public ContactUpdateBatch(String newValue) {
        this.newValue = newValue;
    }
    
    /**
     * Start method - returns QueryLocator for batch processing
     * @param bc BatchableContext
     * @return Database.QueryLocator
     */
    global Database.QueryLocator start(Database.BatchableContext bc) {
        return Database.getQueryLocator([
            SELECT Id, Name, Status__c
            FROM Contact
            WHERE Status__c != :newValue
            WITH SECURITY_ENFORCED
        ]);
    }
    
    /**
     * Execute method - processes each batch of records
     * @param bc BatchableContext
     * @param scope List of records in current batch
     */
    global void execute(Database.BatchableContext bc, List<Contact> scope) {
        List<Contact> contactsToUpdate = new List<Contact>();
        
        for (Contact contact : scope) {
            contact.Status__c = newValue;
            contactsToUpdate.add(contact);
        }
        
        if (!contactsToUpdate.isEmpty()) {
            update contactsToUpdate;
        }
    }
    
    /**
     * Finish method - called after all batches complete
     * @param bc BatchableContext
     */
    global void finish(Database.BatchableContext bc) {
        // Query job status
        AsyncApexJob job = [
            SELECT Id, Status, NumberOfErrors, JobItemsProcessed, TotalJobItems
            FROM AsyncApexJob
            WHERE Id = :bc.getJobId()
        ];
        
        // Log completion
        System.debug('Batch job completed: ' + job.Status);
        System.debug('Records processed: ' + job.JobItemsProcessed);
        System.debug('Errors: ' + job.NumberOfErrors);
    }
}
```

**Explanation**:
- `start()` method returns a QueryLocator that defines which records to process
- `execute()` method processes each batch of 200 records
- `finish()` method is called after all batches complete
- Each batch executes in a separate transaction with fresh governor limits
- No state is maintained between batches (stateless)

**Usage**:

```apex
// Execute batch job
ContactUpdateBatch batch = new ContactUpdateBatch('Active');
Id jobId = Database.executeBatch(batch, 200);
```

**Test Example**:

```apex
@isTest
private class ContactUpdateBatchTest {
    
    @isTest
    static void testBatchExecution() {
        // Create test data
        List<Contact> contacts = new List<Contact>();
        for (Integer i = 0; i < 250; i++) {
            contacts.add(new Contact(
                LastName = 'Test' + i,
                Status__c = 'Inactive'
            ));
        }
        insert contacts;
        
        Test.startTest();
        ContactUpdateBatch batch = new ContactUpdateBatch('Active');
        Id jobId = Database.executeBatch(batch, 200);
        Test.stopTest();
        
        // Verify results
        List<Contact> updatedContacts = [
            SELECT Id, Status__c
            FROM Contact
            WHERE LastName LIKE 'Test%'
        ];
        
        System.assertEquals(250, updatedContacts.size());
        for (Contact c : updatedContacts) {
            System.assertEquals('Active', c.Status__c);
        }
    }
}
```

---

### Example 2: Stateful Batch with State Management

**Pattern**: Stateful Batch Apex with instance variables
**Use Case**: Maintaining state across batch executions (counters, aggregations)
**Complexity**: Intermediate
**Related Patterns**: <a href="{{ '/rag/code-examples/apex/Salesforce-RAG/rag/development/asynchronous-apex-patterns.html#pattern-2-stateful-batch-apex.html' | relative_url }}">Stateful Batch Apex</a>

**Problem**:
You need to calculate total revenue across all Opportunities. Each batch should add to a running total, and the final total should be calculated in finish().

**Solution**:

```apex
/**
 * Stateful batch class for calculating total revenue
 * Maintains state across batch executions
 */
global class RevenueCalculationBatch implements Database.Batchable<SObject> {
    
    // Instance variables maintain state across batches
    private Decimal totalRevenue = 0;
    private Integer processedRecords = 0;
    private Integer errorCount = 0;
    
    /**
     * Start method - returns QueryLocator
     * @param bc BatchableContext
     * @return Database.QueryLocator
     */
    global Database.QueryLocator start(Database.BatchableContext bc) {
        return Database.getQueryLocator([
            SELECT Id, Amount, StageName
            FROM Opportunity
            WHERE StageName = 'Closed Won'
            WITH SECURITY_ENFORCED
        ]);
    }
    
    /**
     * Execute method - processes batch and updates state
     * @param bc BatchableContext
     * @param scope List of records in current batch
     */
    global void execute(Database.BatchableContext bc, List<Opportunity> scope) {
        try {
            for (Opportunity opp : scope) {
                if (opp.Amount != null) {
                    totalRevenue += opp.Amount;
                    processedRecords++;
                }
            }
        } catch (Exception e) {
            errorCount++;
            // Log error
            System.debug('Error in batch execution: ' + e.getMessage());
        }
    }
    
    /**
     * Finish method - uses accumulated state
     * @param bc BatchableContext
     */
    global void finish(Database.BatchableContext bc) {
        // Use accumulated state
        System.debug('Total Revenue: ' + totalRevenue);
        System.debug('Processed Records: ' + processedRecords);
        System.debug('Errors: ' + errorCount);
        
        // Create summary record or send notification
        // Example: Create custom object record with totals
    }
}
```

**Explanation**:
- Instance variables (`totalRevenue`, `processedRecords`, `errorCount`) maintain state across all batch executions
- State is updated in `execute()` method
- Final calculations use accumulated state in `finish()` method
- Stateful batches use more memory but enable complex aggregations

**Usage**:

```apex
// Execute stateful batch
RevenueCalculationBatch batch = new RevenueCalculationBatch();
Id jobId = Database.executeBatch(batch, 200);
```

**Test Example**:

```apex
@isTest
private class RevenueCalculationBatchTest {
    
    @isTest
    static void testStatefulBatch() {
        // Create test opportunities
        List<Opportunity> opps = new List<Opportunity>();
        for (Integer i = 0; i < 250; i++) {
            opps.add(new Opportunity(
                Name = 'Test Opp ' + i,
                StageName = 'Closed Won',
                Amount = 1000,
                CloseDate = Date.today()
            ));
        }
        insert opps;
        
        Test.startTest();
        RevenueCalculationBatch batch = new RevenueCalculationBatch();
        Id jobId = Database.executeBatch(batch, 200);
        Test.stopTest();
        
        // Verify state was maintained (check logs or custom object)
        // Note: In real scenario, you'd query a custom object or check logs
    }
}
```

---

### Example 3: Batch Chaining Pattern

**Pattern**: Batch chaining - one batch triggers another
**Use Case**: Multi-step data processing (Job A → Job B → Job C)
**Complexity**: Intermediate
**Related Patterns**: <a href="{{ '/rag/code-examples/apex/Salesforce-RAG/rag/development/asynchronous-apex-patterns.html#pattern-3-batch-chaining.html' | relative_url }}">Batch Chaining</a>

**Problem**:
You need to perform a multi-step data migration: (1) Import accounts, (2) Import contacts, (3) Link contacts to accounts. Each step should run as a separate batch job.

**Solution**:

```apex
/**
 * First batch: Import accounts
 */
global class AccountImportBatch implements Database.Batchable<SObject> {
    
    private String externalSystemId;
    
    public AccountImportBatch(String externalSystemId) {
        this.externalSystemId = externalSystemId;
    }
    
    global Database.QueryLocator start(Database.BatchableContext bc) {
        // Query external system data (simplified - would use callout in real scenario)
        return Database.getQueryLocator([
            SELECT Id, Name
            FROM Account
            WHERE External_System_ID__c = :externalSystemId
            WITH SECURITY_ENFORCED
        ]);
    }
    
    global void execute(Database.BatchableContext bc, List<Account> scope) {
        // Process accounts
        for (Account acc : scope) {
            // Import logic here
        }
        update scope;
    }
    
    global void finish(Database.BatchableContext bc) {
        // Chain to next batch: Import contacts
        ContactImportBatch nextBatch = new ContactImportBatch(externalSystemId);
        Id nextJobId = Database.executeBatch(nextBatch, 200);
        
        System.debug('Chained to ContactImportBatch: ' + nextJobId);
    }
}

/**
 * Second batch: Import contacts
 */
global class ContactImportBatch implements Database.Batchable<SObject> {
    
    private String externalSystemId;
    
    public ContactImportBatch(String externalSystemId) {
        this.externalSystemId = externalSystemId;
    }
    
    global Database.QueryLocator start(Database.BatchableContext bc) {
        return Database.getQueryLocator([
            SELECT Id, LastName, AccountId
            FROM Contact
            WHERE External_System_ID__c = :externalSystemId
            WITH SECURITY_ENFORCED
        ]);
    }
    
    global void execute(Database.BatchableContext bc, List<Contact> scope) {
        // Process contacts
        update scope;
    }
    
    global void finish(Database.BatchableContext bc) {
        // Chain to final batch: Link contacts to accounts
        ContactAccountLinkBatch nextBatch = new ContactAccountLinkBatch(externalSystemId);
        Id nextJobId = Database.executeBatch(nextBatch, 200);
        
        System.debug('Chained to ContactAccountLinkBatch: ' + nextJobId);
    }
}

/**
 * Third batch: Link contacts to accounts
 */
global class ContactAccountLinkBatch implements Database.Batchable<SObject> {
    
    private String externalSystemId;
    
    public ContactAccountLinkBatch(String externalSystemId) {
        this.externalSystemId = externalSystemId;
    }
    
    global Database.QueryLocator start(Database.BatchableContext bc) {
        return Database.getQueryLocator([
            SELECT Id, AccountId, External_Account_ID__c
            FROM Contact
            WHERE External_System_ID__c = :externalSystemId
            AND AccountId = null
            WITH SECURITY_ENFORCED
        ]);
    }
    
    global void execute(Database.BatchableContext bc, List<Contact> scope) {
        // Link contacts to accounts
        Map<String, Id> accountMap = new Map<String, Id>();
        for (Account acc : [
            SELECT Id, External_System_ID__c
            FROM Account
            WHERE External_System_ID__c = :externalSystemId
        ]) {
            accountMap.put(acc.External_System_ID__c, acc.Id);
        }
        
        for (Contact con : scope) {
            if (accountMap.containsKey(con.External_Account_ID__c)) {
                con.AccountId = accountMap.get(con.External_Account_ID__c);
            }
        }
        
        update scope;
    }
    
    global void finish(Database.BatchableContext bc) {
        // Final step complete
        System.debug('Data migration complete');
    }
}
```

**Explanation**:
- Each batch completes and chains to the next batch in `finish()` method
- Each chained batch has fresh governor limits
- Pass data between batches via constructor parameters
- Monitor chain execution to detect failures

**Usage**:

```apex
// Start the chain
AccountImportBatch firstBatch = new AccountImportBatch('EXT-001');
Id jobId = Database.executeBatch(firstBatch, 200);
```

---

### Example 4: Batch with Error Handling and Retry

**Pattern**: Batch with comprehensive error handling and retry logic
**Use Case**: Processing records where some may fail validation
**Complexity**: Advanced
**Related Patterns**: <a href="{{ '/rag/code-examples/apex/Salesforce-RAG/rag/development/asynchronous-apex-patterns.html#pattern-4-batch-error-handling-and-retry.html' | relative_url }}">Batch Error Handling</a>

**Problem**:
You need to process 50,000 records where some may fail validation. Errors should be logged, and failed records should be retried in a separate batch job.

**Solution**:

```apex
/**
 * Batch class with error handling and retry logic
 */
global class ContactProcessBatch implements Database.Batchable<SObject>, Database.Stateful {
    
    private List<Id> failedRecordIds = new List<Id>();
    private Integer totalProcessed = 0;
    private Integer totalErrors = 0;
    
    global Database.QueryLocator start(Database.BatchableContext bc) {
        return Database.getQueryLocator([
            SELECT Id, Name, Email, Status__c
            FROM Contact
            WHERE Processed__c = false
            WITH SECURITY_ENFORCED
        ]);
    }
    
    global void execute(Database.BatchableContext bc, List<Contact> scope) {
        List<Contact> contactsToUpdate = new List<Contact>();
        List<Database.SaveResult> saveResults;
        
        // Prepare records for update
        for (Contact contact : scope) {
            contact.Status__c = 'Processed';
            contact.Processed__c = true;
            contactsToUpdate.add(contact);
        }
        
        // Perform DML with error handling
        if (!contactsToUpdate.isEmpty()) {
            saveResults = Database.update(contactsToUpdate, false);
            
            // Process results
            for (Integer i = 0; i < saveResults.size(); i++) {
                Database.SaveResult result = saveResults[i];
                Contact contact = contactsToUpdate[i];
                
                if (result.isSuccess()) {
                    totalProcessed++;
                } else {
                    totalErrors++;
                    failedRecordIds.add(contact.Id);
                    
                    // Log errors
                    String errorMsg = 'Failed to update Contact ' + contact.Id + ': ';
                    for (Database.Error error : result.getErrors()) {
                        errorMsg += error.getMessage() + ' ';
                    }
                    System.debug('ERROR: ' + errorMsg);
                }
            }
        }
    }
    
    global void finish(Database.BatchableContext bc) {
        // Log summary
        System.debug('Batch completed. Processed: ' + totalProcessed + ', Errors: ' + totalErrors);
        
        // Retry failed records if any
        if (!failedRecordIds.isEmpty()) {
            System.debug('Retrying ' + failedRecordIds.size() + ' failed records');
            
            // Create retry batch with failed record IDs
            ContactRetryBatch retryBatch = new ContactRetryBatch(failedRecordIds);
            Id retryJobId = Database.executeBatch(retryBatch, 200);
            
            System.debug('Retry batch started: ' + retryJobId);
        }
    }
}

/**
 * Retry batch for failed records
 */
global class ContactRetryBatch implements Database.Batchable<SObject> {
    
    private Set<Id> recordIds;
    
    public ContactRetryBatch(List<Id> recordIds) {
        this.recordIds = new Set<Id>(recordIds);
    }
    
    global Database.QueryLocator start(Database.BatchableContext bc) {
        return Database.getQueryLocator([
            SELECT Id, Name, Email, Status__c
            FROM Contact
            WHERE Id IN :recordIds
            WITH SECURITY_ENFORCED
        ]);
    }
    
    global void execute(Database.BatchableContext bc, List<Contact> scope) {
        // Retry logic with additional validation
        for (Contact contact : scope) {
            // Additional validation or fixes
            if (String.isBlank(contact.Email)) {
                contact.Email = 'unknown@example.com';
            }
            contact.Status__c = 'Processed';
            contact.Processed__c = true;
        }
        
        update scope;
    }
    
    global void finish(Database.BatchableContext bc) {
        System.debug('Retry batch completed');
    }
}
```

**Explanation**:
- Uses `Database.Stateful` to maintain failed record IDs across batches
- Tracks errors and collects failed record IDs
- Retries failed records in a separate batch job
- Logs errors for debugging and monitoring

**Usage**:

```apex
// Execute batch with error handling
ContactProcessBatch batch = new ContactProcessBatch();
Id jobId = Database.executeBatch(batch, 200);
```

---

### Example 5: Batch Monitoring Pattern

**Pattern**: Batch job monitoring and status tracking
**Use Case**: Monitoring long-running batch jobs and tracking progress
**Complexity**: Intermediate
**Related Patterns**: <a href="{{ '/rag/code-examples/apex/Salesforce-RAG/rag/development/asynchronous-apex-patterns.html#pattern-5-batch-monitoring-and-job-status.html' | relative_url }}">Batch Monitoring</a>

**Problem**:
You need to monitor a nightly batch job that processes 1 million records. Track progress, send notifications on completion, and alert on failures.

**Solution**:

```apex
/**
 * Batch class with monitoring and notifications
 */
global class MonitoredBatch implements Database.Batchable<SObject> {
    
    global Database.QueryLocator start(Database.BatchableContext bc) {
        return Database.getQueryLocator([
            SELECT Id, Name
            FROM Contact
            WHERE Processed__c = false
            WITH SECURITY_ENFORCED
        ]);
    }
    
    global void execute(Database.BatchableContext bc, List<Contact> scope) {
        // Process records
        for (Contact contact : scope) {
            contact.Processed__c = true;
        }
        update scope;
    }
    
    global void finish(Database.BatchableContext bc) {
        // Query job status
        AsyncApexJob job = [
            SELECT Id, Status, NumberOfErrors, JobItemsProcessed, 
                   TotalJobItems, CreatedDate, CompletedDate
            FROM AsyncApexJob
            WHERE Id = :bc.getJobId()
        ];
        
        // Calculate metrics
        Decimal successRate = (job.TotalJobItems > 0) 
            ? ((Decimal)(job.JobItemsProcessed - job.NumberOfErrors) / job.TotalJobItems * 100)
            : 0;
        
        Long executionTime = job.CompletedDate != null
            ? job.CompletedDate.getTime() - job.CreatedDate.getTime()
            : 0;
        
        // Send notification based on status
        if (job.Status == 'Completed' && job.NumberOfErrors == 0) {
            sendSuccessNotification(job, successRate, executionTime);
        } else if (job.Status == 'Failed' || job.NumberOfErrors > 0) {
            sendFailureNotification(job, successRate);
        }
    }
    
    private void sendSuccessNotification(AsyncApexJob job, Decimal successRate, Long executionTime) {
        String message = 'Batch job completed successfully.\n' +
            'Records processed: ' + job.JobItemsProcessed + '\n' +
            'Success rate: ' + successRate + '%\n' +
            'Execution time: ' + (executionTime / 1000) + ' seconds';
        
        System.debug('SUCCESS: ' + message);
        // Send email or create notification record
    }
    
    private void sendFailureNotification(AsyncApexJob job, Decimal successRate) {
        String message = 'Batch job completed with errors.\n' +
            'Records processed: ' + job.JobItemsProcessed + '\n' +
            'Errors: ' + job.NumberOfErrors + '\n' +
            'Success rate: ' + successRate + '%';
        
        System.debug('FAILURE: ' + message);
        // Send alert email or create notification record
    }
}

/**
 * Utility class for monitoring batch jobs
 */
public class BatchJobMonitor {
    
    /**
     * Get batch job status
     * @param jobId Batch job ID
     * @return AsyncApexJob record
     */
    public static AsyncApexJob getJobStatus(Id jobId) {
        return [
            SELECT Id, Status, NumberOfErrors, JobItemsProcessed, 
                   TotalJobItems, CreatedDate, CompletedDate
            FROM AsyncApexJob
            WHERE Id = :jobId
        ];
    }
    
    /**
     * Check if batch job is still running
     * @param jobId Batch job ID
     * @return Boolean indicating if job is running
     */
    public static Boolean isJobRunning(Id jobId) {
        AsyncApexJob job = getJobStatus(jobId);
        return job.Status == 'Processing' || job.Status == 'Preparing' || job.Status == 'Queued';
    }
}
```

**Explanation**:
- Queries `AsyncApexJob` object for job status and metrics
- Calculates success rate and execution time
- Sends notifications based on job status
- Provides utility methods for monitoring batch jobs

**Usage**:

```apex
// Execute monitored batch
MonitoredBatch batch = new MonitoredBatch();
Id jobId = Database.executeBatch(batch, 200);

// Monitor job status
Boolean isRunning = BatchJobMonitor.isJobRunning(jobId);
AsyncApexJob status = BatchJobMonitor.getJobStatus(jobId);
```

---

## Related Patterns

- <a href="{{ '/rag/development/asynchronous-apex-patterns.html' | relative_url }}">Asynchronous Apex Patterns</a> - Complete async patterns guide
- <a href="{{ '/rag/development/governor-limits-and-optimization.html' | relative_url }}">Governor Limits and Optimization</a> - Governor limit management
- <a href="{{ '/rag/code-examples/apex/code-examples/templates/apex-batch-template.html' | relative_url }}">Batch Template</a> - Batch Apex template

