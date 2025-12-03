# Event-Driven Architecture

## What Was Actually Done

Event-driven integration patterns were designed and implemented using Salesforce Platform Events to decouple Salesforce from external systems. The primary use case was publishing business events from Salesforce that needed to propagate to downstream systems.

### Platform Events Implementation

Platform Events were published from Flows (preferred) and Apex to represent key business events such as:

- Application submission events
- Status change events (admitted, enrolled, withdrawn)
- Student data change events (address updates, contact information changes)
- Case status changes and milestone completions

The events were designed to include:
- External IDs for correlation with external systems
- Minimal necessary PII to balance functionality with privacy
- Change metadata (who made the change, when it occurred)

### External Event Bus Pattern

A reference architecture was designed where:
- Salesforce publishes Platform Events to an Event Channel
- The Event Channel routes events to an external event bus (Amazon EventBridge was the reference)
- EventBridge fans out events to multiple subscribers:
  - SIS integration services
  - Analytics pipelines
  - Internal microservices
  - Notification services

### Internal Event Consumption

Channel Members within Salesforce were designed to subscribe to the same Platform Events for:
- Internal logging and audit trail purposes
- Triggering internal automation workflows
- Maintaining event correlation logs

## Rules and Patterns

### Event Publication

- Prefer Flows over Apex for publishing Platform Events when the logic can be expressed declaratively
- Include external IDs in event payloads to enable correlation with external system records
- Minimize PII in event payloads; include only what's necessary for downstream processing
- Always include change metadata (modified by, modified date) for audit purposes

### Event Schema Design

- Design event schemas to be versioned and backward-compatible
- Use consistent naming conventions for event fields across different event types
- Include a correlation ID field to track related events across systems
- Design payloads to be self-contained; avoid requiring subscribers to query Salesforce for additional context

### Event-Driven Integration Flow

1. Business event occurs in Salesforce (record change, user action)
2. Flow or Apex publishes Platform Event with structured payload
3. Event Channel routes to external event bus
4. External subscribers process events asynchronously
5. Optional: Channel Members in Salesforce consume for internal logging/automation

### Error Handling

- Design event payloads to be idempotent where possible
- Implement retry logic at the event bus level, not in Salesforce
- Log failed event publications for troubleshooting
- Consider dead-letter queues for events that cannot be processed

## Suggested Improvements (From AI)

### Event Versioning Strategy

Implement a formal event versioning strategy:
- Include version numbers in event names or payloads
- Maintain backward compatibility for at least one major version
- Document breaking changes and migration paths
- Use custom metadata to manage event schema versions

### Event Monitoring and Observability

Enhance event observability:
- Create custom objects to track event publication status
- Implement dashboards showing event volume and error rates
- Set up alerts for event publication failures
- Track event processing latency from publication to external system acknowledgment

### Change Data Capture Integration

Consider using Change Data Capture (CDC) alongside Platform Events:
- CDC for high-volume, field-level change tracking
- Platform Events for business-level events requiring orchestration
- Use CDC events to trigger Platform Event publication for complex business logic

## To Validate

- Full implementation status of EventBridge integration (designed vs. production)
- Specific event types that were actually published in production
- Error handling and retry patterns implemented at the event bus level
- Performance characteristics of Platform Event publication under load

