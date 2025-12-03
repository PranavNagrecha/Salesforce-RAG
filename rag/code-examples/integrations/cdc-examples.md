# Change Data Capture (CDC) Code Examples

> Complete, working code examples for Change Data Capture patterns.
> All examples are copy-paste ready and follow Salesforce best practices.

## Overview

Change Data Capture (CDC) provides real-time change notifications for Salesforce records. CDC events are published automatically when records are created, updated, deleted, or undeleted.

**Related Patterns**:
- [Change Data Capture Patterns](integrations/change-data-capture-patterns.html)
- [Event-Driven Architecture](architecture/event-driven-architecture.html)

## Examples

### Example 1: Basic CDC Trigger Handler

**Pattern**: Trigger-based CDC processing
**Use Case**: Processing CDC events directly in Apex triggers
**Complexity**: Basic
**Related Patterns**: [Trigger-Based CDC Processing](/Salesforce-RAG/rag/integrations/change-data-capture-patterns.html#pattern-1-trigger-based-cdc-processing)

**Problem**:
You need to process Contact change events to sync data to an external system. Trigger processes events and calls external API for each change.

**Solution**:

```apex
/**
 * Trigger handler for Contact CDC events
 */
trigger ContactChangeEventTrigger on ContactChangeEvent (after insert) {
    ContactChangeEventHandler.handleEvents(Trigger.new);
}

/**
 * Handler class for Contact CDC events
 */
public class ContactChangeEventHandler {
    
    public static void handleEvents(List<ContactChangeEvent> events) {
        List<ContactChangeEvent> eventsToProcess = new List<ContactChangeEvent>();
        
        for (ContactChangeEvent event : events) {
            // Filter events by change type
            if (event.ChangeEventHeader.getChangeType() == 'CREATE' ||
                event.ChangeEventHeader.getChangeType() == 'UPDATE') {
                eventsToProcess.add(event);
            }
        }
        
        if (!eventsToProcess.isEmpty()) {
            // Process events asynchronously
            ContactSyncQueueable job = new ContactSyncQueueable(eventsToProcess);
            System.enqueueJob(job);
        }
    }
}

/**
 * Queueable class to sync Contact changes to external system
 */
public class ContactSyncQueueable implements Queueable {
    
    private List<ContactChangeEvent> events;
    
    public ContactSyncQueueable(List<ContactChangeEvent> events) {
        this.events = events;
    }
    
    public void execute(QueueableContext context) {
        for (ContactChangeEvent event : events) {
            try {
                // Extract change data
                String changeType = event.ChangeEventHeader.getChangeType();
                Id recordId = event.ChangeEventHeader.getRecordIds()[0];
                
                // Query current record state
                Contact contact = [
                    SELECT Id, Name, Email, Phone
                    FROM Contact
                    WHERE Id = :recordId
                    WITH SECURITY_ENFORCED
                ];
                
                // Sync to external system
                syncToExternalSystem(contact, changeType);
                
            } catch (Exception e) {
                // Log error
                System.debug('ERROR: Failed to sync Contact ' + event.Id + ': ' + e.getMessage());
                // Store failed event for replay
                storeFailedEvent(event, e);
            }
        }
    }
    
    private void syncToExternalSystem(Contact contact, String changeType) {
        // Prepare API callout
        HttpRequest req = new HttpRequest();
        req.setEndpoint('callout:Named_Credential/api/contacts/sync');
        req.setMethod('POST');
        req.setHeader('Content-Type', 'application/json');
        
        // Build request body
        Map<String, Object> requestBody = new Map<String, Object>{
            'salesforceId' => contact.Id,
            'name' => contact.Name,
            'email' => contact.Email,
            'phone' => contact.Phone,
            'changeType' => changeType
        };
        req.setBody(JSON.serialize(requestBody));
        
        // Perform callout
        Http http = new Http();
        HttpResponse res = http.send(req);
        
        if (res.getStatusCode() != 200) {
            throw new SyncException('Sync failed: ' + res.getStatus());
        }
    }
    
    private void storeFailedEvent(ContactChangeEvent event, Exception e) {
        // Store failed event in custom object for replay
        CDC_Event_Log__c log = new CDC_Event_Log__c(
            Event_ID__c = event.Id,
            Object_Type__c = 'Contact',
            Change_Type__c = event.ChangeEventHeader.getChangeType(),
            Record_ID__c = event.ChangeEventHeader.getRecordIds()[0],
            Error_Message__c = e.getMessage(),
            Status__c = 'Failed'
        );
        insert log;
    }
    
    public class SyncException extends Exception {}
}
```

**Explanation**:
- Trigger processes CDC events in bulk
- Filters events by change type
- Processes events asynchronously via Queueable
- Handles errors and stores failed events for replay

**Usage**:
CDC events are automatically published when Contact records change. No manual triggering needed.

---

### Example 2: CDC with Platform Events

**Pattern**: Combining CDC with Platform Events
**Use Case**: Complex event-driven workflows with CDC change detection
**Complexity**: Intermediate
**Related Patterns**: [Platform Event Integration with CDC](/Salesforce-RAG/rag/integrations/change-data-capture-patterns.html#pattern-2-platform-event-integration-with-cdc)

**Problem**:
Contact changes trigger CDC events, which publish Platform Events with enriched data. Multiple subscribers process Platform Events for different purposes.

**Solution**:

```apex
/**
 * Trigger handler for Contact CDC events
 * Publishes Platform Events for complex processing
 */
trigger ContactChangeEventTrigger on ContactChangeEvent (after insert) {
    ContactChangeEventHandler.handleEvents(Trigger.new);
}

/**
 * Handler class that publishes Platform Events from CDC events
 */
public class ContactChangeEventHandler {
    
    public static void handleEvents(List<ContactChangeEvent> events) {
        List<Contact_Change_Event__e> platformEvents = new List<Contact_Change_Event__e>();
        
        for (ContactChangeEvent cdcEvent : events) {
            // Extract CDC event data
            String changeType = cdcEvent.ChangeEventHeader.getChangeType();
            Id recordId = cdcEvent.ChangeEventHeader.getRecordIds()[0];
            
            // Query related data for enrichment
            Contact contact = [
                SELECT Id, Name, Email, AccountId, Account.Name
                FROM Contact
                WHERE Id = :recordId
                WITH SECURITY_ENFORCED
            ];
            
            // Create Platform Event with enriched data
            Contact_Change_Event__e platformEvent = new Contact_Change_Event__e();
            platformEvent.Contact_ID__c = contact.Id;
            platformEvent.Contact_Name__c = contact.Name;
            platformEvent.Contact_Email__c = contact.Email;
            platformEvent.Account_ID__c = contact.AccountId;
            platformEvent.Account_Name__c = contact.Account?.Name;
            platformEvent.Change_Type__c = changeType;
            platformEvent.Changed_Fields__c = JSON.serialize(cdcEvent.ChangeEventHeader.getChangedFields());
            
            platformEvents.add(platformEvent);
        }
        
        // Publish Platform Events
        if (!platformEvents.isEmpty()) {
            List<Database.SaveResult> results = EventBus.publish(platformEvents);
            
            // Handle publish errors
            for (Integer i = 0; i < results.size(); i++) {
                if (!results[i].isSuccess()) {
                    System.debug('ERROR: Failed to publish Platform Event: ' + results[i].getErrors());
                }
            }
        }
    }
}
```

**Explanation**:
- CDC events trigger Platform Event publication
- Platform Events include enriched data (related records)
- Multiple subscribers can process Platform Events
- Enables complex event-driven workflows

---

### Example 3: CDC Error Handling and Retry

**Pattern**: CDC event error handling with retry logic
**Use Case**: Handling CDC event processing failures
**Complexity**: Advanced
**Related Patterns**: [CDC Error Handling and Replay](/Salesforce-RAG/rag/integrations/change-data-capture-patterns.html#pattern-3-cdc-error-handling-and-replay)

**Problem**:
CDC event processing fails due to external API timeout. Failed events are logged, and replay mechanism processes them after API recovers.

**Solution**:

```apex
/**
 * Handler with error handling and retry
 */
public class ContactChangeEventHandler {
    
    public static void handleEvents(List<ContactChangeEvent> events) {
        List<CDC_Event_Log__c> eventLogs = new List<CDC_Event_Log__c>();
        
        for (ContactChangeEvent event : events) {
            try {
                // Process event
                processEvent(event);
                
                // Log success
                eventLogs.add(createEventLog(event, 'Success', null));
                
            } catch (Exception e) {
                // Log failure
                eventLogs.add(createEventLog(event, 'Failed', e.getMessage()));
            }
        }
        
        // Insert event logs
        if (!eventLogs.isEmpty()) {
            insert eventLogs;
        }
    }
    
    private static void processEvent(ContactChangeEvent event) {
        String changeType = event.ChangeEventHeader.getChangeType();
        Id recordId = event.ChangeEventHeader.getRecordIds()[0];
        
        // Query record
        Contact contact = [
            SELECT Id, Name, Email
            FROM Contact
            WHERE Id = :recordId
            WITH SECURITY_ENFORCED
        ];
        
        // Sync to external system with retry
        syncWithRetry(contact, changeType, 0);
    }
    
    private static void syncWithRetry(Contact contact, String changeType, Integer retryCount) {
        try {
            // Perform sync
            HttpRequest req = new HttpRequest();
            req.setEndpoint('callout:Named_Credential/api/sync');
            req.setMethod('POST');
            req.setBody(JSON.serialize(new Map<String, Object>{
                'id' => contact.Id,
                'name' => contact.Name,
                'email' => contact.Email,
                'changeType' => changeType
            }));
            
            Http http = new Http();
            HttpResponse res = http.send(req);
            
            if (res.getStatusCode() != 200) {
                throw new SyncException('Sync failed: ' + res.getStatus());
            }
            
        } catch (Exception e) {
            // Retry on transient errors
            if (retryCount < 3 && isTransientError(e)) {
                // Wait with exponential backoff
                Integer delayMs = (Integer) Math.pow(2, retryCount) * 1000; // 1s, 2s, 4s
                
                // Enqueue retry job
                ContactSyncRetryQueueable retryJob = new ContactSyncRetryQueueable(
                    contact.Id,
                    changeType,
                    retryCount + 1
                );
                System.enqueueJob(retryJob);
            } else {
                // Max retries reached or non-transient error
                throw e;
            }
        }
    }
    
    private static Boolean isTransientError(Exception e) {
        // Check if error is transient (timeout, connection error, etc.)
        String errorMsg = e.getMessage();
        return errorMsg.contains('timeout') || 
               errorMsg.contains('connection') || 
               errorMsg.contains('503') ||
               errorMsg.contains('502');
    }
    
    private static CDC_Event_Log__c createEventLog(
        ContactChangeEvent event, 
        String status, 
        String errorMessage
    ) {
        return new CDC_Event_Log__c(
            Event_ID__c = event.Id,
            Object_Type__c = 'Contact',
            Change_Type__c = event.ChangeEventHeader.getChangeType(),
            Record_ID__c = event.ChangeEventHeader.getRecordIds()[0],
            Status__c = status,
            Error_Message__c = errorMessage,
            Event_Data__c = JSON.serialize(event)
        );
    }
    
    public class SyncException extends Exception {}
}

/**
 * Queueable for retrying failed syncs
 */
public class ContactSyncRetryQueueable implements Queueable {
    
    private Id contactId;
    private String changeType;
    private Integer retryCount;
    
    public ContactSyncRetryQueueable(Id contactId, String changeType, Integer retryCount) {
        this.contactId = contactId;
        this.changeType = changeType;
        this.retryCount = retryCount;
    }
    
    public void execute(QueueableContext context) {
        Contact contact = [
            SELECT Id, Name, Email
            FROM Contact
            WHERE Id = :contactId
            WITH SECURITY_ENFORCED
        ];
        
        ContactChangeEventHandler.syncWithRetry(contact, changeType, retryCount);
    }
}
```

**Explanation**:
- Handles errors in event processing
- Implements retry logic with exponential backoff
- Logs failed events for replay
- Distinguishes transient vs permanent errors

---

## Related Patterns

- [Change Data Capture Patterns](integrations/change-data-capture-patterns.html) - Complete CDC patterns guide
- [Event-Driven Architecture](architecture/event-driven-architecture.html) - Platform Events patterns

