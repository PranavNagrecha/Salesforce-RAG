---
title: "Platform Events API Reference"
level: "Intermediate"
tags:
  - api-reference
  - platform-events
  - events
  - reference
  - integration
last_reviewed: "2025-01-XX"
---

# Platform Events API Reference

> Quick reference for Platform Events publication, subscription, and payload patterns.

## Overview

This reference provides API signatures, parameters, and usage examples for Platform Events in Salesforce.

## Publishing Events

### From Apex

**Class Declaration**:
```apex
public with sharing class EventPublisher {
    public static void publishEvent(String recordId, String action) {
        // Create event instance
        CustomEvent__e event = new CustomEvent__e(
            RecordId__c = recordId,
            Action__c = action,
            Timestamp__c = Datetime.now()
        );
        
        // Publish event
        List<Database.SaveResult> results = EventBus.publish(
            new List<CustomEvent__e>{ event }
        );
        
        // Handle results
        for (Database.SaveResult result : results) {
            if (!result.isSuccess()) {
                // Log error
                LOG_LogMessageUtility.logError(
                    'EventPublisher',
                    'publishEvent',
                    'Failed to publish event: ' + result.getErrors()[0].getMessage(),
                    null
                );
            }
        }
    }
}
```

**Method Signature**: `EventBus.publish(List<SObject> events)`

**Parameters**: 
- `events` (List<SObject>): List of Platform Event records to publish

**Returns**: `List<Database.SaveResult>`: Results of publish operation

**Best Practices**:
- Publish events in bulk when possible
- Handle publish failures gracefully
- Include timestamp and idempotency keys
- Keep payloads self-contained and minimal

**Related Patterns**: [Event-Driven Architecture](../architecture/event-driven-architecture.html)

---

### From Flow

**Flow Action**: Use "Publish Platform Event" action

**Configuration**:
- Select Platform Event object
- Map field values
- Handle errors

**Best Practices**:
- Use Flow for simple event publishing
- Use Apex for complex payload construction
- Handle errors in Flow

---

## Subscribing to Events

### Apex Subscription (Trigger)

**Trigger Pattern**:
```apex
trigger CustomEventTrigger on CustomEvent__e (after insert) {
    CustomEventTriggerHandler.handleEvents(Trigger.new);
}
```

**Handler Pattern**:
```apex
public with sharing class CustomEventTriggerHandler {
    public static void handleEvents(List<CustomEvent__e> events) {
        List<Id> recordIds = new List<Id>();
        for (CustomEvent__e event : events) {
            recordIds.add(event.RecordId__c);
        }
        
        // Process events
        processRecords(recordIds);
    }
    
    private static void processRecords(List<Id> recordIds) {
        // Business logic
    }
}
```

**Best Practices**:
- Use trigger handlers for event processing
- Bulkify event processing
- Handle errors gracefully
- Log event processing

---

### LWC Subscription (Lightning Message Service)

**Note**: Platform Events can be consumed via Lightning Message Service in LWC.

**Example**:
```javascript
import { subscribe, MessageContext, APPLICATION_SCOPE } from 'lightning/messageService';
import PLATFORM_EVENT_CHANNEL from '@salesforce/messageChannel/PlatformEventChannel__c';

@wire(MessageContext)
messageContext;

connectedCallback() {
    this.subscription = subscribe(
        this.messageContext,
        PLATFORM_EVENT_CHANNEL,
        (message) => this.handleEvent(message),
        { scope: APPLICATION_SCOPE }
    );
}

disconnectedCallback() {
    if (this.subscription) {
        unsubscribe(this.subscription);
    }
}
```

---

## Event Payload Design

### Self-Contained Payloads

**Best Practice**: Include all necessary data in event payload

**Example**:
```apex
public class EventPayload {
    public String recordId;
    public String action;
    public Datetime timestamp;
    public Map<String, Object> context;
    
    // Include minimal necessary data
    // Avoid including full record data
}
```

### Idempotency

**Best Practice**: Include idempotency key to prevent duplicate processing

**Example**:
```apex
CustomEvent__e event = new CustomEvent__e(
    RecordId__c = recordId,
    Action__c = action,
    IdempotencyKey__c = recordId + '-' + action + '-' + String.valueOf(Datetime.now().getTime())
);
```

### Minimal PII

**Best Practice**: Minimize personally identifiable information in events

**Example**:
```apex
// Good: Minimal PII
CustomEvent__e event = new CustomEvent__e(
    RecordId__c = recordId,
    Action__c = 'update'
);

// Bad: Too much PII
CustomEvent__e event = new CustomEvent__e(
    RecordId__c = recordId,
    ContactName__c = contact.Name,
    ContactEmail__c = contact.Email,
    ContactPhone__c = contact.Phone
);
```

**Related Patterns**: [Event-Driven Architecture](/Salesforce-RAG/rag/architecture/event-driven-architecture.html#event-payload-design)

---

## Error Handling

### Publish Errors

**Pattern**: Handle Database.SaveResult errors

```apex
List<Database.SaveResult> results = EventBus.publish(events);

for (Database.SaveResult result : results) {
    if (!result.isSuccess()) {
        for (Database.Error error : result.getErrors()) {
            LOG_LogMessageUtility.logError(
                'EventPublisher',
                'publishEvent',
                'Publish error: ' + error.getMessage(),
                null
            );
        }
    }
}
```

### Subscription Errors

**Pattern**: Handle errors in event processing

```apex
public static void handleEvents(List<CustomEvent__e> events) {
    try {
        processEvents(events);
    } catch (Exception e) {
        LOG_LogMessageUtility.logError(
            'CustomEventTriggerHandler',
            'handleEvents',
            'Error processing events: ' + e.getMessage(),
            e
        );
        // Optionally publish error event or notify admins
    }
}
```

**Related Patterns**: [Error Handling](../development/error-handling-and-logging.html)

---

## Related Patterns

- [Event-Driven Architecture](../architecture/event-driven-architecture.html) - Complete event-driven patterns
- [Integration Patterns](../integrations) - Integration with external systems
- [Error Handling](../development/error-handling-and-logging.html) - Error handling patterns

