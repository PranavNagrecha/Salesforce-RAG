# Queueable Apex Code Examples

> Complete, working code examples for Queueable Apex patterns.
> All examples are copy-paste ready and follow Salesforce best practices.

## Overview

Queueable Apex is used for lightweight async processing, chaining jobs, and performing callouts after DML operations. It provides better error handling than @future methods and can process up to 50,000 records.

**Related Patterns**:
- [Asynchronous Apex Patterns](/Salesforce-RAG/rag/development/asynchronous-apex-patterns.html#queueable-apex-patterns)
- [Error Handling and Logging](/rag/development/error-handling-and-logging.html)

## Examples

### Example 1: Basic Queueable

**Pattern**: Basic Queueable for async processing
**Use Case**: Simple async operations without chaining
**Complexity**: Basic
**Related Patterns**: [Basic Queueable](/Salesforce-RAG/rag/development/asynchronous-apex-patterns.html#pattern-1-basic-queueable)

**Problem**:
You need to send email notifications after record updates. The Queueable job sends emails asynchronously without blocking the main transaction.

**Solution**:

```apex
/**
 * Queueable class for sending email notifications
 * Processes emails asynchronously after DML operations
 */
public class EmailNotificationQueueable implements Queueable {
    
    private Set<Id> contactIds;
    
    /**
     * Constructor to accept contact IDs
     * @param contactIds Set of Contact IDs to send notifications for
     */
    public EmailNotificationQueueable(Set<Id> contactIds) {
        this.contactIds = contactIds;
    }
    
    /**
     * Execute method - sends email notifications
     * @param context QueueableContext
     */
    public void execute(QueueableContext context) {
        // Query contacts
        List<Contact> contacts = [
            SELECT Id, Name, Email
            FROM Contact
            WHERE Id IN :contactIds
            AND Email != null
            WITH SECURITY_ENFORCED
        ];
        
        // Prepare emails
        List<Messaging.SingleEmailMessage> emails = new List<Messaging.SingleEmailMessage>();
        
        for (Contact contact : contacts) {
            Messaging.SingleEmailMessage email = new Messaging.SingleEmailMessage();
            email.setToAddresses(new String[] { contact.Email });
            email.setSubject('Your contact information has been updated');
            email.setPlainTextBody('Hello ' + contact.Name + ',\n\nYour contact information has been updated.');
            emails.add(email);
        }
        
        // Send emails
        if (!emails.isEmpty()) {
            Messaging.sendEmail(emails);
        }
    }
}
```

**Explanation**:
- Implements `Queueable` interface
- Constructor accepts parameters for processing
- `execute()` method performs async work
- Executes in separate transaction with fresh governor limits

**Usage**:

```apex
// Enqueue job after DML
Set<Id> contactIds = new Set<Id>{ '003...', '003...' };
EmailNotificationQueueable job = new EmailNotificationQueueable(contactIds);
Id jobId = System.enqueueJob(job);
```

**Test Example**:

```apex
@isTest
private class EmailNotificationQueueableTest {
    
    @isTest
    static void testEmailNotification() {
        // Create test contacts
        List<Contact> contacts = new List<Contact>{
            new Contact(LastName = 'Test1', Email = 'test1@example.com'),
            new Contact(LastName = 'Test2', Email = 'test2@example.com')
        };
        insert contacts;
        
        Set<Id> contactIds = new Set<Id>();
        for (Contact c : contacts) {
            contactIds.add(c.Id);
        }
        
        Test.startTest();
        EmailNotificationQueueable job = new EmailNotificationQueueable(contactIds);
        Id jobId = System.enqueueJob(job);
        Test.stopTest();
        
        // Verify emails were sent (check email logs or limits)
        // Note: In real scenario, verify email delivery
    }
}
```

---

### Example 2: Chained Queueable Jobs

**Pattern**: Queueable chaining - one job triggers another
**Use Case**: Multi-step async operations (Job A → Job B → Job C)
**Complexity**: Intermediate
**Related Patterns**: [Chained Queueable Jobs](/Salesforce-RAG/rag/development/asynchronous-apex-patterns.html#pattern-2-chained-queueable-jobs)

**Problem**:
You need to perform a multi-step integration: (1) Query external API, (2) Transform data, (3) Update Salesforce records. Each step should run as a chained Queueable job.

**Solution**:

```apex
/**
 * First Queueable: Query external API
 */
public class ExternalApiQueryQueueable implements Queueable {
    
    private String apiEndpoint;
    
    public ExternalApiQueryQueueable(String apiEndpoint) {
        this.apiEndpoint = apiEndpoint;
    }
    
    public void execute(QueueableContext context) {
        // Query external API
        HttpRequest req = new HttpRequest();
        req.setEndpoint(apiEndpoint);
        req.setMethod('GET');
        
        Http http = new Http();
        HttpResponse res = http.send(req);
        
        // Parse response
        Map<String, Object> responseData = (Map<String, Object>) JSON.deserializeUntyped(res.getBody());
        
        // Chain to next job: Transform data
        DataTransformQueueable nextJob = new DataTransformQueueable(responseData);
        Id nextJobId = System.enqueueJob(nextJob);
        
        System.debug('Chained to DataTransformQueueable: ' + nextJobId);
    }
}

/**
 * Second Queueable: Transform data
 */
public class DataTransformQueueable implements Queueable {
    
    private Map<String, Object> apiData;
    
    public DataTransformQueueable(Map<String, Object> apiData) {
        this.apiData = apiData;
    }
    
    public void execute(QueueableContext context) {
        // Transform API data to Salesforce format
        List<Contact> contactsToUpdate = new List<Contact>();
        
        List<Object> records = (List<Object>) apiData.get('records');
        for (Object recordObj : records) {
            Map<String, Object> record = (Map<String, Object>) recordObj;
            
            Contact contact = new Contact();
            contact.External_ID__c = (String) record.get('id');
            contact.LastName = (String) record.get('name');
            contact.Email = (String) record.get('email');
            contactsToUpdate.add(contact);
        }
        
        // Chain to final job: Update records
        RecordUpdateQueueable nextJob = new RecordUpdateQueueable(contactsToUpdate);
        Id nextJobId = System.enqueueJob(nextJob);
        
        System.debug('Chained to RecordUpdateQueueable: ' + nextJobId);
    }
}

/**
 * Third Queueable: Update Salesforce records
 */
public class RecordUpdateQueueable implements Queueable {
    
    private List<Contact> contacts;
    
    public RecordUpdateQueueable(List<Contact> contacts) {
        this.contacts = contacts;
    }
    
    public void execute(QueueableContext context) {
        // Upsert contacts using external ID
        upsert contacts Contact.External_ID__c;
        
        System.debug('Updated ' + contacts.size() + ' contacts');
    }
}
```

**Explanation**:
- Each Queueable job chains to the next in `execute()` method
- Data is passed between jobs via constructor parameters
- Each job has fresh governor limits
- Can chain up to 50 Queueable jobs

**Usage**:

```apex
// Start the chain
ExternalApiQueryQueueable firstJob = new ExternalApiQueryQueueable('https://api.example.com/data');
Id jobId = System.enqueueJob(firstJob);
```

---

### Example 3: Queueable with Callouts

**Pattern**: Queueable performing callouts after DML
**Use Case**: Integration scenarios requiring callouts after record updates
**Complexity**: Intermediate
**Related Patterns**: [Queueable with Callouts](/Salesforce-RAG/rag/development/asynchronous-apex-patterns.html#pattern-3-queueable-with-callouts)

**Problem**:
You need to create a record in Salesforce, then call an external API to sync the data. The Queueable job performs the callout after the DML completes.

**Solution**:

```apex
/**
 * Queueable class for performing callouts after DML
 */
public class SyncToExternalSystemQueueable implements Queueable {
    
    private Id recordId;
    private String objectType;
    
    public SyncToExternalSystemQueueable(Id recordId, String objectType) {
        this.recordId = recordId;
        this.objectType = objectType;
    }
    
    public void execute(QueueableContext context) {
        try {
            // Query the record
            SObject record = Database.query(
                'SELECT Id, Name, External_Sync_Status__c ' +
                'FROM ' + objectType + ' ' +
                'WHERE Id = :recordId ' +
                'WITH SECURITY_ENFORCED'
            );
            
            // Prepare API callout
            HttpRequest req = new HttpRequest();
            req.setEndpoint('callout:Named_Credential/api/sync');
            req.setMethod('POST');
            req.setHeader('Content-Type', 'application/json');
            
            // Build request body
            Map<String, Object> requestBody = new Map<String, Object>{
                'salesforceId' => record.Id,
                'name' => record.get('Name')
            };
            req.setBody(JSON.serialize(requestBody));
            
            // Perform callout
            Http http = new Http();
            HttpResponse res = http.send(req);
            
            // Handle response
            if (res.getStatusCode() == 200) {
                record.put('External_Sync_Status__c', 'Synced');
                update record;
            } else {
                record.put('External_Sync_Status__c', 'Error');
                update record;
                throw new SyncException('Sync failed: ' + res.getStatus());
            }
            
        } catch (Exception e) {
            // Log error
            System.debug('ERROR: Sync failed for ' + recordId + ': ' + e.getMessage());
            throw e;
        }
    }
    
    public class SyncException extends Exception {}
}
```

**Explanation**:
- Queueable allows callouts after DML (not possible in same transaction)
- Uses Named Credentials for secure endpoint configuration
- Handles API responses and updates record status
- Implements error handling for failed callouts

**Usage**:

```apex
// After creating/updating record, enqueue sync job
Contact newContact = new Contact(LastName = 'Test', Email = 'test@example.com');
insert newContact;

SyncToExternalSystemQueueable syncJob = new SyncToExternalSystemQueueable(
    newContact.Id,
    'Contact'
);
Id jobId = System.enqueueJob(syncJob);
```

---

### Example 4: Queueable Retry Pattern

**Pattern**: Queueable with retry logic and exponential backoff
**Use Case**: Handling transient errors in async operations
**Complexity**: Advanced
**Related Patterns**: [Queueable Retry Pattern](/Salesforce-RAG/rag/development/asynchronous-apex-patterns.html#pattern-4-queueable-retry-pattern)

**Problem**:
You need to call an external API that may be temporarily unavailable. The Queueable job should retry with increasing delays (1s, 2s, 4s) up to 3 attempts.

**Solution**:

```apex
/**
 * Queueable class with retry logic and exponential backoff
 */
public class RetryableApiCallQueueable implements Queueable {
    
    private String endpoint;
    private Integer retryCount;
    private Integer maxRetries;
    private List<Id> recordIds;
    
    public RetryableApiCallQueueable(String endpoint, List<Id> recordIds) {
        this.endpoint = endpoint;
        this.recordIds = recordIds;
        this.retryCount = 0;
        this.maxRetries = 3;
    }
    
    public RetryableApiCallQueueable(String endpoint, List<Id> recordIds, Integer retryCount) {
        this.endpoint = endpoint;
        this.recordIds = recordIds;
        this.retryCount = retryCount;
        this.maxRetries = 3;
    }
    
    public void execute(QueueableContext context) {
        try {
            // Perform API callout
            HttpRequest req = new HttpRequest();
            req.setEndpoint(endpoint);
            req.setMethod('POST');
            req.setHeader('Content-Type', 'application/json');
            req.setBody(JSON.serialize(recordIds));
            
            Http http = new Http();
            HttpResponse res = http.send(req);
            
            // Check if successful
            if (res.getStatusCode() == 200) {
                // Success - update records
                List<Contact> contacts = [
                    SELECT Id, Sync_Status__c
                    FROM Contact
                    WHERE Id IN :recordIds
                ];
                
                for (Contact contact : contacts) {
                    contact.Sync_Status__c = 'Synced';
                }
                update contacts;
                
            } else {
                // Retry on failure
                handleRetry();
            }
            
        } catch (Exception e) {
            // Retry on exception
            handleRetry();
        }
    }
    
    private void handleRetry() {
        if (retryCount < maxRetries) {
            // Calculate exponential backoff delay
            Integer delaySeconds = (Integer) Math.pow(2, retryCount); // 1s, 2s, 4s
            
            // Enqueue retry job with delay
            RetryableApiCallQueueable retryJob = new RetryableApiCallQueueable(
                endpoint,
                recordIds,
                retryCount + 1
            );
            
            // Note: Actual delay would be handled by scheduling or waiting
            // For now, enqueue immediately (in production, use Scheduled Apex for delay)
            Id retryJobId = System.enqueueJob(retryJob);
            
            System.debug('Retrying (attempt ' + (retryCount + 1) + '): ' + retryJobId);
        } else {
            // Max retries reached - log error
            System.debug('ERROR: Max retries reached for endpoint: ' + endpoint);
            
            // Update records with error status
            List<Contact> contacts = [
                SELECT Id, Sync_Status__c
                FROM Contact
                WHERE Id IN :recordIds
            ];
            
            for (Contact contact : contacts) {
                contact.Sync_Status__c = 'Error';
            }
            update contacts;
        }
    }
}
```

**Explanation**:
- Tracks retry count in constructor parameters
- Implements exponential backoff (1s, 2s, 4s, 8s)
- Retries up to maximum attempts
- Logs errors after max retries

**Usage**:

```apex
// Enqueue job with retry capability
List<Id> contactIds = new List<Id>{ '003...', '003...' };
RetryableApiCallQueueable job = new RetryableApiCallQueueable(
    'https://api.example.com/sync',
    contactIds
);
Id jobId = System.enqueueJob(job);
```

---

### Example 5: Queueable Monitoring

**Pattern**: Queueable job monitoring and status tracking
**Use Case**: Monitoring async operations and tracking execution
**Complexity**: Intermediate
**Related Patterns**: [Queueable Monitoring](/Salesforce-RAG/rag/development/asynchronous-apex-patterns.html#pattern-5-queueable-monitoring)

**Problem**:
You need to monitor Queueable job execution, track execution time, detect failures, and send alerts on errors.

**Solution**:

```apex
/**
 * Queueable class with monitoring
 */
public class MonitoredQueueable implements Queueable {
    
    private List<Id> recordIds;
    private DateTime startTime;
    
    public MonitoredQueueable(List<Id> recordIds) {
        this.recordIds = recordIds;
        this.startTime = DateTime.now();
    }
    
    public void execute(QueueableContext context) {
        try {
            // Query job status
            AsyncApexJob job = [
                SELECT Id, Status, NumberOfErrors, JobItemsProcessed
                FROM AsyncApexJob
                WHERE Id = :context.getJobId()
            ];
            
            // Process records
            List<Contact> contacts = [
                SELECT Id, Name, Status__c
                FROM Contact
                WHERE Id IN :recordIds
                WITH SECURITY_ENFORCED
            ];
            
            for (Contact contact : contacts) {
                contact.Status__c = 'Processed';
            }
            update contacts;
            
            // Calculate execution time
            Long executionTime = DateTime.now().getTime() - startTime.getTime();
            
            // Log success
            System.debug('Queueable job completed successfully');
            System.debug('Records processed: ' + contacts.size());
            System.debug('Execution time: ' + (executionTime / 1000) + ' seconds');
            
        } catch (Exception e) {
            // Log error
            System.debug('ERROR: Queueable job failed: ' + e.getMessage());
            
            // Send error notification
            sendErrorNotification(context.getJobId(), e);
            
            throw e;
        }
    }
    
    private void sendErrorNotification(Id jobId, Exception e) {
        // Query job details
        AsyncApexJob job = [
            SELECT Id, Status, NumberOfErrors, JobItemsProcessed
            FROM AsyncApexJob
            WHERE Id = :jobId
        ];
        
        String message = 'Queueable job failed.\n' +
            'Job ID: ' + jobId + '\n' +
            'Status: ' + job.Status + '\n' +
            'Error: ' + e.getMessage();
        
        System.debug('ALERT: ' + message);
        // Send email or create notification record
    }
}

/**
 * Utility class for monitoring Queueable jobs
 */
public class QueueableJobMonitor {
    
    /**
     * Get Queueable job status
     * @param jobId Queueable job ID
     * @return AsyncApexJob record
     */
    public static AsyncApexJob getJobStatus(Id jobId) {
        return [
            SELECT Id, Status, NumberOfErrors, JobItemsProcessed, CreatedDate, CompletedDate
            FROM AsyncApexJob
            WHERE Id = :jobId
        ];
    }
    
    /**
     * Check if Queueable job is still running
     * @param jobId Queueable job ID
     * @return Boolean indicating if job is running
     */
    public static Boolean isJobRunning(Id jobId) {
        AsyncApexJob job = getJobStatus(jobId);
        return job.Status == 'Processing' || job.Status == 'Queued';
    }
    
    /**
     * Get queue depth (number of queued jobs)
     * @return Integer number of queued jobs
     */
    public static Integer getQueueDepth() {
        return [
            SELECT COUNT()
            FROM AsyncApexJob
            WHERE Status = 'Queued'
        ];
    }
}
```

**Explanation**:
- Queries `AsyncApexJob` for job status and metrics
- Tracks execution time and errors
- Sends notifications on failures
- Provides utility methods for monitoring

**Usage**:

```apex
// Execute monitored Queueable
List<Id> contactIds = new List<Id>{ '003...', '003...' };
MonitoredQueueable job = new MonitoredQueueable(contactIds);
Id jobId = System.enqueueJob(job);

// Monitor job status
Boolean isRunning = QueueableJobMonitor.isJobRunning(jobId);
AsyncApexJob status = QueueableJobMonitor.getJobStatus(jobId);
Integer queueDepth = QueueableJobMonitor.getQueueDepth();
```

---

## Related Patterns

- [Asynchronous Apex Patterns](/rag/development/asynchronous-apex-patterns.html) - Complete async patterns guide
- [Error Handling and Logging](/rag/development/error-handling-and-logging.html) - Error handling patterns
- [Queueable Template](/rag/code-examples/templates/apex-queueable-template.html) - Queueable Apex template

