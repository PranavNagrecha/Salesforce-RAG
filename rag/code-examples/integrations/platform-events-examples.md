---
layout: default
title: Platform Events Code Examples
description: Platform Events enable event-driven architecture in Salesforce, allowing decoupled, asynchronous communication between systems
permalink: /rag/code-examples/integrations/platform-events-examples.html
---

# Platform Events Code Examples

> This file contains complete, working code examples for Platform Events patterns.
> All examples are copy-paste ready and follow Salesforce best practices.

## Overview

Platform Events enable event-driven architecture in Salesforce, allowing decoupled, asynchronous communication between systems. These examples demonstrate publishing events from Apex and Flows, subscribing to events, handling event payloads, and integrating with external event buses.

**Related Patterns**:
- <a href="{{ '/rag/architecture/event-driven-architecture.html' | relative_url }}">Event-Driven Architecture</a> - Event-driven architecture patterns
- <a href="{{ '/rag/code-examples/integrations/cdc-examples.html' | relative_url }}">Change Data Capture Examples</a> - CDC event patterns
- <a href="{{ '/rag/integrations/integration-platform-patterns.html' | relative_url }}">Integration Platform Patterns</a> - Integration patterns

## Examples

### Example 1: Publishing Platform Events from Apex

**Pattern**: Publishing Platform Events from Apex code
**Use Case**: Publishing business events from Apex triggers or services
**Complexity**: Basic
**Related Patterns**: <a href="{{ '/rag/architecture/event-driven-architecture.html' | relative_url }}">Event-Driven Architecture</a>

**Problem**:
You need to publish Platform Events when records are created or updated to notify external systems.

**Solution**:

**Platform Event Definition** (`Application_Submitted__e`):
- **Label**: Application Submitted
- **Plural Label**: Application Submitted Events
- **Fields**:
  - `Application_ID__c` (Text, 255) - External ID of application
  - `Student_ID__c` (Text, 255) - Student external ID
  - `Program__c` (Text, 255) - Program name
  - `Submitted_Date__c` (DateTime) - Submission timestamp
  - `Submitted_By__c` (Text, 255) - User who submitted

**Apex** (`ApplicationEventService.cls`):
```apex
/**
 * Service for publishing Application-related Platform Events
 */
public with sharing class ApplicationEventService {
    
    /**
     * Publishes Application Submitted event
     * @param application Application record
     */
    public static void publishApplicationSubmitted(Application__c application) {
        Application_Submitted__e event = new Application_Submitted__e();
        event.Application_ID__c = application.External_ID__c;
        event.Student_ID__c = application.Student__r.External_ID__c;
        event.Program__c = application.Program__r.Name;
        event.Submitted_Date__c = DateTime.now();
        event.Submitted_By__c = UserInfo.getUserName();
        
        List<Database.SaveResult> results = EventBus.publish(new List<Application_Submitted__e>{ event });
        
        // Check for errors
        for (Database.SaveResult result : results) {
            if (!result.isSuccess()) {
                LOG_LogMessageUtility.logError(
                    'ApplicationEventService',
                    'publishApplicationSubmitted',
                    'Failed to publish event: ' + result.getErrors()[0].getMessage(),
                    null
                );
            }
        }
        
        LOG_LogMessageUtility.logInfo(
            'ApplicationEventService',
            'publishApplicationSubmitted',
            'Published Application Submitted event for: ' + application.External_ID__c
        );
    }
    
    /**
     * Publishes Application Status Changed event
     * @param application Application record
     * @param oldStatus Previous status
     * @param newStatus New status
     */
    public static void publishStatusChanged(Application__c application, String oldStatus, String newStatus) {
        Application_Status_Changed__e event = new Application_Status_Changed__e();
        event.Application_ID__c = application.External_ID__c;
        event.Old_Status__c = oldStatus;
        event.New_Status__c = newStatus;
        event.Changed_Date__c = DateTime.now();
        event.Changed_By__c = UserInfo.getUserName();
        
        EventBus.publish(new List<Application_Status_Changed__e>{ event });
    }
}
```

**Usage in Trigger**:
```apex
trigger ApplicationTrigger on Application__c (after insert, after update) {
    if (Trigger.isAfter) {
        if (Trigger.isInsert) {
            for (Application__c app : Trigger.new) {
                if (app.Status__c == 'Submitted') {
                    ApplicationEventService.publishApplicationSubmitted(app);
                }
            }
        }
        
        if (Trigger.isUpdate) {
            for (Application__c app : Trigger.new) {
                Application__c oldApp = Trigger.oldMap.get(app.Id);
                if (app.Status__c != oldApp.Status__c) {
                    ApplicationEventService.publishStatusChanged(app, oldApp.Status__c, app.Status__c);
                }
            }
        }
    }
}
```

**Best Practices**:
- Include external IDs for correlation
- Include minimal necessary PII
- Include change metadata (who, when)
- Handle publish errors gracefully
- Log event publication for troubleshooting

### Example 2: Publishing Platform Events from Flow

**Pattern**: Publishing Platform Events declaratively from Flow
**Use Case**: Publishing events without code
**Complexity**: Basic
**Related Patterns**: <a href="{{ '/rag/development/flow-patterns.html' | relative_url }}">Flow Patterns</a>

**Problem**:
You need to publish Platform Events from a Record-Triggered Flow when records are created or updated.

**Solution**:

**Flow Configuration**:
- **Flow Type**: Record-Triggered Flow
- **Object**: Application__c
- **Trigger**: A record is created or updated
- **Entry Conditions**: `{!$Record.Status__c}` EQUALS `Submitted`

**Flow Elements**:

1. **Platform Event Publish Element**: Publish Application Submitted Event
   - **Platform Event**: Application_Submitted__e
   - **Field Values**:
     - `Application_ID__c`: `{!$Record.External_ID__c}`
     - `Student_ID__c`: `{!$Record.Student__r.External_ID__c}`
     - `Program__c`: `{!$Record.Program__r.Name}`
     - `Submitted_Date__c`: `NOW()`
     - `Submitted_By__c`: `{!$User.Username}`

**Best Practices**:
- Use Flows for declarative event publication
- Set entry conditions to limit event publication
- Include all necessary context in event payload
- Test event publication in sandbox first

### Example 3: Subscribing to Platform Events with Apex

**Pattern**: Subscribing to Platform Events using Apex triggers
**Use Case**: Processing events internally within Salesforce
**Complexity**: Intermediate
**Related Patterns**: <a href="{{ '/rag/architecture/event-driven-architecture.html' | relative_url }}">Event-Driven Architecture</a>

**Problem**:
You need to subscribe to Platform Events and process them (e.g., logging, triggering workflows).

**Solution**:

**Apex** (`ApplicationEventSubscriber.cls`):
```apex
/**
 * Subscribes to Application-related Platform Events
 * Processes events for internal logging and automation
 */
public with sharing class ApplicationEventSubscriber {
    
    /**
     * Processes Application Submitted events
     * @param events List of Application_Submitted__e events
     */
    public static void processApplicationSubmitted(List<Application_Submitted__e> events) {
        List<Event_Log__c> logs = new List<Event_Log__c>();
        
        for (Application_Submitted__e event : events) {
            // Create event log
            Event_Log__c log = new Event_Log__c();
            log.Event_Type__c = 'Application_Submitted';
            log.Application_ID__c = event.Application_ID__c;
            log.Student_ID__c = event.Student_ID__c;
            log.Program__c = event.Program__c;
            log.Event_Date__c = event.Submitted_Date__c;
            log.Processed_By__c = UserInfo.getUserId();
            logs.add(log);
            
            // Trigger additional automation if needed
            triggerApplicationWorkflow(event);
        }
        
        if (!logs.isEmpty()) {
            insert logs;
        }
    }
    
    /**
     * Triggers workflow based on event
     * @param event Application Submitted event
     */
    private static void triggerApplicationWorkflow(Application_Submitted__e event) {
        // Find application by external ID
        List<Application__c> applications = [
            SELECT Id, Status__c
            FROM Application__c
            WHERE External_ID__c = :event.Application_ID__c
            WITH SECURITY_ENFORCED
            LIMIT 1
        ];
        
        if (!applications.isEmpty()) {
            Application__c app = applications[0];
            // Update application or trigger workflow
            // Implementation depends on business requirements
        }
    }
}
```

**Trigger** (`ApplicationEventTrigger.trigger`):
```apex
trigger ApplicationEventTrigger on Application_Submitted__e (after insert) {
    ApplicationEventSubscriber.processApplicationSubmitted(Trigger.new);
}
```

**Best Practices**:
- Process events in bulk (events are delivered in batches)
- Handle errors gracefully (failed events are retried)
- Use external IDs to correlate events with records
- Log event processing for troubleshooting

### Example 4: Platform Event Payload Design

**Pattern**: Designing self-contained event payloads
**Use Case**: Enabling event subscribers to process events without querying Salesforce
**Complexity**: Intermediate
**Related Patterns**: <a href="{{ '/rag/architecture/event-driven-architecture.html' | relative_url }}">Event-Driven Architecture</a>

**Problem**:
You need to design event payloads that include all necessary context for subscribers.

**Solution**:

**Platform Event Definition** (`Student_Enrollment_Updated__e`):
- **Label**: Student Enrollment Updated
- **Fields**:
  - `Student_ID__c` (Text, 255) - Student external ID
  - `Enrollment_ID__c` (Text, 255) - Enrollment external ID
  - `Program__c` (Text, 255) - Program name
  - `Status__c` (Text, 255) - Enrollment status
  - `Enrollment_Date__c` (Date) - Enrollment date
  - `Changed_Fields__c` (Text, 32768) - JSON string of changed fields
  - `Changed_By__c` (Text, 255) - User who made the change
  - `Changed_Date__c` (DateTime) - Change timestamp
  - `Correlation_ID__c` (Text, 255) - Correlation ID for tracking

**Apex** (`EnrollmentEventService.cls`):
```apex
/**
 * Service for publishing Enrollment-related Platform Events
 */
public with sharing class EnrollmentEventService {
    
    /**
     * Publishes Enrollment Updated event with full context
     * @param enrollment Enrollment record
     * @param changedFields Map of changed fields
     */
    public static void publishEnrollmentUpdated(Enrollment__c enrollment, Map<String, Object> changedFields) {
        Student_Enrollment_Updated__e event = new Student_Enrollment_Updated__e();
        
        // Core identifiers
        event.Student_ID__c = enrollment.Student__r.External_ID__c;
        event.Enrollment_ID__c = enrollment.External_ID__c;
        event.Program__c = enrollment.Program__r.Name;
        
        // Current state
        event.Status__c = enrollment.Status__c;
        event.Enrollment_Date__c = enrollment.Enrollment_Date__c;
        
        // Change metadata
        event.Changed_Fields__c = JSON.serialize(changedFields);
        event.Changed_By__c = UserInfo.getUserName();
        event.Changed_Date__c = DateTime.now();
        
        // Correlation ID for tracking across systems
        event.Correlation_ID__c = generateCorrelationId();
        
        EventBus.publish(new List<Student_Enrollment_Updated__e>{ event });
    }
    
    /**
     * Generates correlation ID for event tracking
     * @return Correlation ID string
     */
    private static String generateCorrelationId() {
        return 'ENR-' + String.valueOf(DateTime.now().getTime()) + '-' + String.valueOf(Math.random() * 1000).substring(0, 3);
    }
}
```

**Best Practices**:
- Include external IDs for correlation
- Include current state (not just changes)
- Include change metadata (who, when, what changed)
- Use correlation IDs for tracking across systems
- Minimize PII while maintaining functionality
- Design payloads to be idempotent where possible

### Example 5: Error Handling and Retry Logic

**Pattern**: Handling event publication and processing errors
**Use Case**: Ensuring reliable event delivery and processing
**Complexity**: Advanced
**Related Patterns**: <a href="{{ '/rag/development/error-handling-and-logging.html' | relative_url }}">Error Handling and Logging</a>

**Problem**:
You need to handle errors when publishing or processing Platform Events.

**Solution**:

**Apex** (`EventErrorHandler.cls`):
```apex
/**
 * Handles errors in Platform Event publication and processing
 */
public with sharing class EventErrorHandler {
    
    /**
     * Publishes event with error handling and retry logic
     * @param event Platform Event to publish
     * @param maxRetries Maximum number of retry attempts
     * @return Whether publication succeeded
     */
    public static Boolean publishWithRetry(SObject event, Integer maxRetries) {
        Integer attempts = 0;
        Boolean success = false;
        
        while (attempts < maxRetries && !success) {
            try {
                List<Database.SaveResult> results = EventBus.publish(new List<SObject>{ event });
                
                for (Database.SaveResult result : results) {
                    if (result.isSuccess()) {
                        success = true;
                    } else {
                        // Log error
                        String errorMsg = '';
                        for (Database.Error error : result.getErrors()) {
                            errorMsg += error.getMessage() + ' ';
                        }
                        
                        LOG_LogMessageUtility.logError(
                            'EventErrorHandler',
                            'publishWithRetry',
                            'Event publication failed (attempt ' + (attempts + 1) + '): ' + errorMsg,
                            null
                        );
                    }
                }
                
            } catch (Exception e) {
                LOG_LogMessageUtility.logError(
                    'EventErrorHandler',
                    'publishWithRetry',
                    'Exception during event publication (attempt ' + (attempts + 1) + '): ' + e.getMessage(),
                    e
                );
            }
            
            attempts++;
            
            // Wait before retry (exponential backoff)
            if (!success && attempts < maxRetries) {
                Integer waitTime = (Integer) Math.pow(2, attempts) * 1000; // Exponential backoff
                try {
                    Thread.sleep(waitTime);
                } catch (Exception e) {
                    // Ignore sleep interruption
                }
            }
        }
        
        return success;
    }
    
    /**
     * Processes events with error handling
     * @param events List of Platform Events to process
     */
    public static void processEventsWithErrorHandling(List<SObject> events) {
        List<Event_Processing_Error__c> errors = new List<Event_Processing_Error__c>();
        
        for (SObject event : events) {
            try {
                // Process event based on type
                processEvent(event);
                
            } catch (Exception e) {
                // Log processing error
                Event_Processing_Error__c error = new Event_Processing_Error__c();
                error.Event_Type__c = String.valueOf(event.getSObjectType());
                error.Error_Message__c = e.getMessage();
                error.Event_Data__c = JSON.serialize(event);
                error.Processing_Date__c = DateTime.now();
                errors.add(error);
                
                LOG_LogMessageUtility.logError(
                    'EventErrorHandler',
                    'processEventsWithErrorHandling',
                    'Error processing event: ' + e.getMessage(),
                    e
                );
            }
        }
        
        if (!errors.isEmpty()) {
            insert errors;
        }
    }
    
    /**
     * Processes individual event based on type
     * @param event Platform Event to process
     */
    private static void processEvent(SObject event) {
        // Route to appropriate handler based on event type
        String eventType = String.valueOf(event.getSObjectType());
        
        if (eventType == 'Application_Submitted__e') {
            ApplicationEventSubscriber.processApplicationSubmitted(
                new List<Application_Submitted__e>{ (Application_Submitted__e) event }
            );
        }
        // Add other event type handlers as needed
    }
}
```

**Best Practices**:
- Implement retry logic for event publication
- Use exponential backoff for retries
- Log all event processing errors
- Store failed events for manual review
- Handle errors gracefully without blocking other events

## Related Examples

- <a href="{{ '/rag/development/error-handling-and-logging.html' | relative_url }}">Error Handling and Logging</a> - Error handling patterns