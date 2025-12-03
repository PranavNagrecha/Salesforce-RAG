---
title: "Change Data Capture (CDC) Patterns"
level: "Intermediate"
tags:
  - integrations
  - cdc
  - change-data-capture
  - real-time
  - event-driven
last_reviewed: "2025-01-XX"
---

# Change Data Capture (CDC) Patterns

## Overview

Change Data Capture (CDC) provides real-time change notifications for Salesforce records. CDC events are published automatically when records are created, updated, deleted, or undeleted. This guide covers CDC event processing patterns, error handling, and integration strategies.

**Related Patterns**:
- [Event-Driven Architecture](../architecture/event-driven-architecture.md) - Platform Events and event-driven patterns
- [Integration Patterns](etl-vs-api-vs-events.md) - Integration pattern selection

## Prerequisites

**Required Knowledge**:
- Understanding of Salesforce event-driven architecture
- Knowledge of Platform Events and event processing
- Understanding of integration patterns (ETL, API, Events)
- Familiarity with error handling and retry patterns

**Recommended Reading**:
- [Event-Driven Architecture](../architecture/event-driven-architecture.md) - Platform Events patterns
- [ETL vs API vs Events](etl-vs-api-vs-events.md) - Integration pattern selection
- [Error Handling and Logging](../development/error-handling-and-logging.md) - Error handling patterns

## Consensus Best Practices

- **Use CDC for real-time change tracking**: Track field-level changes in real-time
- **Process CDC events asynchronously**: Use triggers or Platform Events to process CDC events
- **Implement error handling and replay**: Handle CDC event failures and support event replay
- **Use CDC with Platform Events**: Combine CDC with Platform Events for complex business logic
- **Monitor CDC event processing**: Track event processing and detect failures
- **Design idempotent event handlers**: Ensure event handlers can safely process duplicate events
- **Handle event retention limits**: CDC events have 24-hour retention; plan for event replay

## Decision Framework: When to Use CDC

### Use CDC When:
- Need **real-time change notifications** for record changes
- Need **field-level change tracking** (which fields changed)
- Processing **high-volume change events** (millions of events)
- Need **event replay capability** for error recovery
- Integrating with **external systems** that need real-time sync
- Building **real-time data pipelines** or **event-driven architectures**

### Use Platform Events When:
- Need **custom event payloads** with business logic
- Need **event publishing control** (when to publish)
- Need **longer event retention** (more than 24 hours)
- Need **event filtering** before publishing
- Building **custom event-driven workflows**

### Use Other Patterns When:
- Need **batch synchronization** (use ETL)
- Need **request-response** patterns (use API)
- Need **simple automation** (use Flow or Process Builder)

## CDC Event Processing Patterns

### Pattern 1: Trigger-Based CDC Processing

**When to use**: Processing CDC events directly in Apex triggers.

**Implementation approach**:
- Create trigger on CDC change event object (e.g., `ContactChangeEvent`)
- Process change events in trigger handler
- Handle create, update, delete, and undelete operations
- Implement bulkification for high-volume events

**Why it's recommended**: Trigger-based processing provides direct access to CDC events and allows immediate processing. It's ideal for simple event processing scenarios.

**Example scenario**: Processing Contact change events to sync data to external system. Trigger processes events and calls external API for each change.

**Key Points**:
- CDC change event objects end with `__ChangeEvent`
- Events include `ChangeType` field (CREATE, UPDATE, DELETE, UNDELETE)
- Events include `ChangeEventHeader` with metadata
- Process events in bulk to avoid governor limits

### Pattern 2: Platform Event Integration with CDC

**When to use**: Combining CDC with Platform Events for complex business logic.

**Implementation approach**:
- Process CDC events in trigger
- Publish Platform Events from CDC trigger
- Process Platform Events in separate subscribers
- Enable complex event-driven workflows

**Why it's recommended**: Platform Events provide more flexibility than CDC alone, allowing custom payloads, longer retention, and complex event routing. This pattern combines real-time change tracking with flexible event processing.

**Example scenario**: Contact changes trigger CDC events, which publish Platform Events with enriched data. Multiple subscribers process Platform Events for different purposes (sync, notifications, analytics).

**Key Points**:
- CDC provides change detection
- Platform Events provide business logic and routing
- Enables complex event-driven workflows
- Supports multiple subscribers

### Pattern 3: CDC Error Handling and Replay

**When to use**: Handling CDC event processing failures and supporting event replay.

**Implementation approach**:
- Implement error handling in CDC event processors
- Log failed events to custom object
- Support event replay from logs
- Implement retry logic for transient errors

**Why it's recommended**: CDC events have 24-hour retention. Failed events must be logged and replayed before retention expires. This pattern ensures no events are lost.

**Example scenario**: CDC event processing fails due to external API timeout. Failed events are logged, and replay mechanism processes them after API recovers.

**Key Points**:
- CDC events have 24-hour retention
- Log failed events immediately
- Implement replay mechanism
- Handle duplicate events (idempotent processing)

### Pattern 4: CDC Event Replay Strategies

**When to use**: Replaying CDC events after processing failures or system outages.

**Implementation approach**:
- Store CDC event data in custom objects
- Implement replay mechanism to process stored events
- Support selective replay (by date, object, or criteria)
- Handle duplicate event processing

**Why it's recommended**: Event replay is essential for error recovery and system maintenance. This pattern ensures reliable event processing even after failures.

**Example scenario**: System outage causes CDC events to be missed. Replay mechanism processes stored events after system recovery.

**Key Points**:
- Store event data for replay
- Support selective replay
- Handle duplicate events
- Monitor replay progress

### Pattern 5: CDC for Real-Time Integrations

**When to use**: Real-time synchronization with external systems using CDC events.

**Implementation approach**:
- Process CDC events in triggers
- Transform event data for external system
- Call external API for each change
- Handle API errors and retries

**Why it's recommended**: CDC provides real-time change notifications, enabling real-time integration with external systems. This pattern ensures external systems stay in sync with Salesforce.

**Example scenario**: Contact changes in Salesforce trigger CDC events, which call external CRM API to sync contact data in real-time.

**Key Points**:
- Real-time change notifications
- Transform data for external system
- Handle API callouts and errors
- Implement retry logic

## CDC Error Handling

### Retry Strategies

**Exponential Backoff**: Retry failed events with increasing delays (1s, 2s, 4s, 8s).

**Queueable Retry**: Enqueue failed events to Queueable jobs for retry.

**Scheduled Retry**: Schedule failed events for retry at later time.

**Dead Letter Queue**: Store permanently failed events for manual review.

### Event Replay Patterns

**Full Replay**: Replay all events from a specific date/time.

**Selective Replay**: Replay events matching specific criteria (object, field, change type).

**Incremental Replay**: Replay only events that failed processing.

**Idempotent Replay**: Ensure replay can safely process duplicate events.

## CDC Monitoring and Observability

### Event Processing Metrics

- **Events Processed**: Count of events successfully processed
- **Events Failed**: Count of events that failed processing
- **Processing Time**: Time to process events
- **Event Lag**: Delay between event creation and processing

### Monitoring Patterns

- **Query CDC Event Logs**: Query custom logging objects for event processing history
- **Track Event Processing Status**: Monitor event processing success/failure rates
- **Alert on Failures**: Send notifications when event processing fails
- **Monitor Event Retention**: Track events approaching 24-hour retention limit

## Related Patterns

- [Event-Driven Architecture](../architecture/event-driven-architecture.md) - Platform Events and event-driven patterns
- [Integration Patterns](etl-vs-api-vs-events.md) - Integration pattern selection
- [Monitoring and Alerting](../observability/monitoring-alerting.md) - CDC monitoring and event processing metrics

## Tradeoffs: CDC vs Platform Events vs Other Patterns

### CDC Advantages

- **Automatic event publishing**: No code needed to publish events
- **Field-level change tracking**: Know exactly which fields changed
- **High volume support**: Can handle millions of events
- **Event replay**: Support for replaying events within retention period

### CDC Limitations

- **24-hour retention**: Events expire after 24 hours
- **No custom payloads**: Events contain only changed field data
- **No event filtering**: All changes generate events (can't filter)
- **Limited event metadata**: Less metadata than Platform Events

### Platform Events Advantages

- **Custom payloads**: Include any data in event payload
- **Longer retention**: Events retained longer than CDC
- **Event filtering**: Control when events are published
- **Rich metadata**: Include business context in events

### Platform Events Limitations

- **Manual publishing**: Must write code to publish events
- **No field-level tracking**: Don't automatically track field changes
- **Lower volume**: Not designed for millions of events

### When to Combine CDC and Platform Events

- **CDC for change detection**: Use CDC to detect changes
- **Platform Events for business logic**: Publish Platform Events from CDC triggers
- **Best of both worlds**: Real-time change tracking + flexible event processing

## Q&A

### Q: What is the difference between CDC and Platform Events?

**A**: **CDC** automatically publishes change events when records are created, updated, deleted, or undeleted. It provides field-level change tracking and has 24-hour retention. **Platform Events** are custom events you publish explicitly from code/flows, with custom payloads and longer retention. Use CDC for change tracking; use Platform Events for business events.

### Q: How do I enable CDC for an object?

**A**: Enable CDC in Setup → Integrations → Change Data Capture. Select objects to enable CDC for. Once enabled, CDC events are automatically published for all changes to those objects. No code is required to publish CDC events.

### Q: What is the retention period for CDC events?

**A**: CDC events have a **24-hour retention period**. Events expire after 24 hours and cannot be replayed. Plan for event replay within this window. For longer retention, consider using Platform Events or storing events in custom objects.

### Q: How do I process CDC events?

**A**: Create a trigger on the CDC event object (e.g., `CaseChangeEvent`), process events asynchronously (use triggers or Platform Events), implement error handling and replay logic, design idempotent event handlers, and monitor event processing. Process events in bulk to handle high volumes.

### Q: Can I filter CDC events?

**A**: **No, CDC events cannot be filtered** before publishing. All changes to enabled objects generate CDC events. If you need filtering, use CDC to detect changes and publish Platform Events with filtered logic, or filter events in your subscriber code.

### Q: How do I handle CDC event failures?

**A**: Implement error handling in CDC event triggers, log failures to custom logging objects, implement retry logic for transient failures, use event replay for failed events (within 24-hour window), and monitor event processing to detect failures early.

### Q: What are the performance implications of CDC?

**A**: CDC events are published automatically and don't impact transaction performance. However, processing CDC events in triggers can impact performance. Process events asynchronously, bulkify event processing, and monitor event processing performance. High-volume CDC scenarios may require careful design.

### Q: Can I combine CDC with Platform Events?

**A**: Yes, combining CDC with Platform Events is a common pattern. Use **CDC to detect changes** and **Platform Events for business logic**. Publish Platform Events from CDC triggers to add business context, filter events, or enable longer retention. This provides the best of both worlds.

## Edge Cases and Limitations

### CDC Event Retention

**Scenario**: CDC events have a 24-hour retention period and expire after that time.

**Consideration**:
- Process events within the retention window
- Implement event replay logic for failed events
- Store critical events in custom objects for longer retention
- Plan for event processing delays and failures

### High-Volume CDC Scenarios

**Scenario**: Objects with high change frequency can generate millions of CDC events.

**Consideration**:
- Process events in bulk to handle high volumes
- Use asynchronous processing (triggers or Platform Events)
- Implement event batching and throttling if needed
- Monitor event processing performance and adjust as needed

### CDC Event Filtering Limitations

**Scenario**: CDC events cannot be filtered before publishing; all changes generate events.

**Consideration**:
- Filter events in subscriber code if filtering is needed
- Use CDC to detect changes and publish Platform Events with filtered logic
- Consider using Platform Events directly if filtering is critical
- Plan for processing all events even if only some are needed

### Field-Level Change Tracking

**Scenario**: CDC provides field-level change tracking, but not all fields may be tracked.

**Consideration**:
- Verify which fields are included in CDC events
- Use ChangeEventHeader to identify changed fields
- Consider using Field History Tracking for additional change tracking
- Plan for fields that may not be tracked in CDC events

### Limitations

- **24-hour retention**: CDC events expire after 24 hours and cannot be replayed
- **No filtering**: CDC events cannot be filtered before publishing
- **Object limitations**: Not all objects support CDC (check object capabilities)
- **Field limitations**: Some fields may not be tracked in CDC events
- **Event size**: Large change events may have payload size limitations

## Related Patterns

- [Event-Driven Architecture](../architecture/event-driven-architecture.md) - Platform Events patterns
- [Integration Patterns](etl-vs-api-vs-events.md) - Integration pattern selection
- [CDC Examples](../code-examples/integrations/cdc-examples.md) - Complete CDC code examples

