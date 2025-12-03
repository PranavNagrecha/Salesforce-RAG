---
layout: default
title: Event-Driven Architecture
description: Event-driven integration patterns decouple Salesforce from external systems by publishing business events that can be consumed asynchronously by multiple subscribers
permalink: /rag/architecture/event-driven-architecture.html
---

# Event-Driven Architecture

## Overview

Event-driven integration patterns decouple Salesforce from external systems by publishing business events that can be consumed asynchronously by multiple subscribers. This pattern enables scalable, resilient integrations that can handle high-volume scenarios and support multiple downstream systems.

## Implementation Pattern

### Platform Events as Foundation

Platform Events serve as the primary mechanism for publishing business events from Salesforce:

- **Publication Sources**: Platform Events published from Flows (preferred) and Apex
- **Event Types**: Business events such as:
  - Application submissions
  - Status changes (admitted, enrolled, withdrawn)
  - Data changes requiring external propagation (student updates, address changes)
  - Case status changes and milestone completions
- **Payload Design**: Event payloads include:
  - External IDs for correlation with external system records
  - Minimal necessary PII to balance functionality with privacy requirements
  - Change metadata (who made the change, when it occurred)
  - Business context fields needed by downstream systems

### External Event Bus Architecture

Reference architecture pattern where:

1. **Salesforce** publishes Platform Events to an Event Channel
2. **Event Channel** routes events to an external event bus (e.g., Amazon EventBridge)
3. **External Event Bus** fans out events to multiple subscribers:
   - Student Information System (SIS) integration services
   - Analytics pipelines
   - Internal microservices
   - Notification services

### Internal Event Consumption

Channel Members within Salesforce subscribe to the same Platform Events for:

- Internal logging and audit trail purposes
- Triggering internal automation workflows
- Maintaining event correlation logs for troubleshooting
- Supporting internal reporting and analytics

## Key Architectural Decisions

### Prefer Flows Over Apex

Use declarative automation (Flows) when possible for event publication. Reserve Apex for complex logic that cannot be expressed declaratively.

**Rationale**: Maintains declarative-first philosophy, reduces code maintenance, enables business users to modify event publication logic.

### Self-Contained Payloads

Include all necessary context in event payloads. Avoid requiring subscribers to query Salesforce for additional information.

**Rationale**: Reduces coupling between systems, improves performance, enables offline processing.

### Minimize PII

Balance functionality with privacy requirements. Include only necessary PII in event payloads.

**Rationale**: Reduces privacy risk, supports compliance requirements, enables broader event sharing.

### Idempotent Design

Design event payloads to be idempotent where possible, enabling safe retry operations.

**Rationale**: Handles network failures gracefully, supports event replay scenarios, prevents duplicate processing.

## Event Schema Design Principles

### Versioning Strategy

- Design event schemas to be versioned and backward-compatible
- Use consistent naming conventions for event fields across different event types
- Include a correlation ID field to track related events across systems
- Document event schemas and provide examples for subscribers

### Payload Structure

- Include external IDs for correlation
- Include change metadata (modified by, modified date)
- Include business context fields needed by subscribers
- Consider event size limits when designing payloads

## Integration Flow

1. Business event occurs in Salesforce (record change, user action, automation trigger)
2. Flow or Apex publishes Platform Event with structured payload
3. Event Channel routes to external event bus
4. External subscribers process events asynchronously
5. Optional: Channel Members in Salesforce consume for internal logging/automation

## Error Handling Patterns

### Idempotency

Design event payloads to be idempotent where possible, enabling safe retry operations without side effects.

### Retry Logic

Implement retry logic at the event bus level, not in Salesforce. Let the external event bus handle retries and dead-letter queues.

### Logging

Log failed event publications for troubleshooting. Track event publication success rates and monitor for failures.

### Dead-Letter Queues

Consider dead-letter queues for events that cannot be processed after retries. Enable manual review and reprocessing.

## Best Practices

### Event Publication

- Prefer Flows over Apex when logic can be expressed declaratively
- Always include external IDs in event payloads
- Minimize PII; include only what's necessary
- Always include change metadata for audit purposes
- Design payloads to be self-contained

### Event Consumption

- Implement idempotent processing logic in subscribers
- Handle event ordering requirements explicitly
- Monitor event processing latency
- Implement proper error handling and logging

### Monitoring and Observability

- Create custom objects to track event publication status
- Implement dashboards showing event volume and error rates
- Set up alerts for event publication failures
- Track event processing latency from publication to external system acknowledgment
- Integrate with centralized logging platforms for cross-system correlation

## Related Patterns

**See Also**:
- <a href="{{ '/rag/integrations/change-data-capture-patterns.html' | relative_url }}">Change Data Capture Patterns</a> - CDC event processing patterns
- <a href="{{ '/rag/architecture/code-examples/integrations/platform-events-examples.html' | relative_url }}">Platform Events Examples</a> - Platform Events code examples

**Related Domains**:
- <a href="{{ '/rag/integrations/integration-platform-patterns.html' | relative_url }}">Integration Platform Patterns</a> - Integration platform patterns
- <a href="{{ '/rag/integrations/etl-vs-api-vs-events.html' | relative_url }}">ETL vs API vs Events</a> - Integration pattern selection

### Change Data Capture Integration

Consider using Change Data Capture (CDC) alongside Platform Events:

**Related**: <a href="{{ '/rag/integrations/change-data-capture-patterns.html' | relative_url }}">Change Data Capture Patterns</a> - Complete CDC patterns guide, <a href="{{ '/rag/architecture/code-examples/integrations/cdc-examples.html' | relative_url }}">CDC Examples</a>

- CDC for high-volume, field-level change tracking
- Platform Events for business-level events requiring orchestration
- Use CDC events to trigger Platform Event publication for complex business logic
- Combine both patterns for comprehensive change tracking

### Event Replay Capabilities

For recovery scenarios, consider implementing event replay:

- Store events in a durable event store
- Provide ability to replay events for specific time ranges
- Support selective replay for specific event types or records
- Document replay procedures for operations teams

## Tradeoffs and Considerations

### Advantages

- Decouples Salesforce from external systems
- Enables asynchronous processing
- Supports fan-out to multiple subscribers
- Reduces direct API dependencies
- Improves system resilience

### Challenges

- Event ordering may be complex in distributed systems
- Requires careful schema versioning
- Monitoring and observability across systems
- Event replay and recovery scenarios
- PII handling and privacy compliance

## When to Use This Pattern

Use event-driven architecture when:

- Multiple systems need to react to the same business events
- Asynchronous processing is acceptable or preferred
- Decoupling Salesforce from external systems is important
- High-volume event scenarios require scalable processing
- Event replay or audit requirements exist

## When Not to Use This Pattern

Avoid event-driven architecture when:

- Synchronous, immediate responses are required
- Event ordering is critical and complex to maintain
- Simple point-to-point integrations are sufficient
- Event volume is very low and overhead isn't justified

## Q&A

### Q: What is the difference between Platform Events and Change Data Capture (CDC)?

**A**: **Platform Events** are custom events you publish explicitly from your code/flows for business events. **CDC** automatically publishes change events when records are created, updated, or deleted. Use Platform Events for business events (e.g., "application submitted"); use CDC for data change tracking.

### Q: Should I use Flows or Apex to publish Platform Events?

**A**: Prefer **Flows** for event publication when possible, as they're declarative and easier to maintain. Reserve **Apex** for complex logic that cannot be expressed declaratively. Flows are preferred for most event publication scenarios.

### Q: How do I handle event ordering in event-driven architecture?

**A**: Event ordering can be complex. Use sequence numbers or timestamps in event payloads if ordering matters. Consider using a single-threaded subscriber or implementing ordering logic in the subscriber. For most use cases, exact ordering may not be required.

### Q: What happens if an event subscriber fails?

**A**: Implement retry logic in subscribers, use event replay capabilities, and monitor event delivery. Design subscribers to be idempotent so they can safely replay events. Use dead letter queues for events that fail after multiple retry attempts.

### Q: How do I design event payloads?

**A**: Include External IDs for correlation, minimal necessary PII, change metadata (who, when), and business context fields needed by downstream systems. Keep payloads focused - include only what subscribers need, not entire record data.

### Q: Can I use Platform Events for internal automation?

**A**: Yes, Platform Events can be consumed by Channel Members within Salesforce for internal automation, logging, audit trails, and triggering workflows. This enables decoupled internal automation patterns.

### Q: What are the performance implications of event-driven architecture?

**A**: Events are asynchronous and scalable, enabling high-volume scenarios. However, there's no immediate feedback, and event processing adds latency. Monitor event delivery, subscriber performance, and implement proper error handling and retry logic.

### Q: How do I test event-driven integrations?

**A**: Publish test events, verify subscribers receive events, test error scenarios and retry logic, test event replay, and verify idempotency. Use test events with known payloads and verify subscriber behavior in different scenarios.

