# Platform Events and EventBridge Integration

## What Was Actually Done

Platform Events were used to implement event-driven integration patterns, publishing business events from Salesforce that could be consumed by external systems via an external event bus (Amazon EventBridge was the reference architecture).

### Platform Events Implementation

Platform Events were published from Flows (preferred) and Apex to represent key business events:

- Application submission events when students submit applications
- Status change events (admitted, enrolled, withdrawn) for student lifecycle tracking
- Student data change events (address updates, contact information changes) that need to propagate to external systems
- Case status changes and milestone completions in public sector implementations

### Event Payload Design

Event payloads were designed to include:

- External IDs for correlation with external system records
- Minimal necessary PII to balance functionality with privacy requirements
- Change metadata (who made the change, when it occurred) for audit purposes
- Business context fields needed by downstream systems

### External Event Bus Pattern

A reference architecture was designed where:

- Salesforce publishes Platform Events to an Event Channel
- The Event Channel routes events to an external event bus (Amazon EventBridge)
- EventBridge fans out events to multiple subscribers:
  - SIS integration services for updating student records
  - Analytics pipelines for reporting and insights
  - Internal microservices for business logic processing
  - Notification services for sending communications

### Internal Event Consumption

Channel Members within Salesforce were designed to subscribe to the same Platform Events for:

- Internal logging and audit trail purposes
- Triggering internal automation workflows based on events
- Maintaining event correlation logs for troubleshooting
- Supporting internal reporting and analytics

## Rules and Patterns

### Platform Event Publication

- Prefer Flows over Apex for publishing Platform Events when the logic can be expressed declaratively
- Include external IDs in event payloads to enable correlation with external system records
- Minimize PII in event payloads; include only what's necessary for downstream processing
- Always include change metadata (modified by, modified date) for audit purposes
- Design event payloads to be self-contained; avoid requiring subscribers to query Salesforce for additional context

### Event Schema Design

- Design event schemas to be versioned and backward-compatible
- Use consistent naming conventions for event fields across different event types
- Include a correlation ID field to track related events across systems
- Document event schemas and provide examples for subscribers
- Consider event size limits when designing payloads

### Event-Driven Integration Flow

1. Business event occurs in Salesforce (record change, user action, automation trigger)
2. Flow or Apex publishes Platform Event with structured payload
3. Event Channel routes to external event bus (EventBridge)
4. External subscribers process events asynchronously
5. Optional: Channel Members in Salesforce consume for internal logging/automation

### Error Handling

- Design event payloads to be idempotent where possible
- Implement retry logic at the event bus level, not in Salesforce
- Log failed event publications for troubleshooting
- Consider dead-letter queues for events that cannot be processed
- Monitor event publication success rates

### EventBridge Integration

- Use EventBridge as the central event router for cross-system communication
- Design event rules in EventBridge to route events to appropriate subscribers
- Implement event filtering at the EventBridge level to reduce processing load
- Use EventBridge's built-in retry and dead-letter queue capabilities
- Monitor EventBridge metrics (invocations, errors, throttles)

## Suggested Improvements (From AI)

### Event Versioning Strategy

Implement a formal event versioning strategy:
- Include version numbers in event names or payloads
- Maintain backward compatibility for at least one major version
- Document breaking changes and migration paths
- Use custom metadata to manage event schema versions
- Create event schema registry for subscribers to discover available events

### Event Monitoring and Observability

Enhance event observability:
- Create custom objects to track event publication status
- Implement dashboards showing event volume and error rates
- Set up alerts for event publication failures
- Track event processing latency from publication to external system acknowledgment
- Integrate with centralized logging platforms for cross-system correlation

### Change Data Capture Integration

Consider using Change Data Capture (CDC) alongside Platform Events:
- CDC for high-volume, field-level change tracking
- Platform Events for business-level events requiring orchestration
- Use CDC events to trigger Platform Event publication for complex business logic
- Combine both patterns for comprehensive change tracking

### Event Replay Capabilities

Implement event replay for recovery scenarios:
- Store events in a durable event store
- Provide ability to replay events for specific time ranges
- Support selective replay for specific event types or records
- Document replay procedures for operations teams

## To Validate

- Full implementation status of EventBridge integration (designed vs. production)
- Specific event types that were actually published in production
- Event payload schemas and field definitions
- Error handling and retry patterns implemented at the event bus level
- Performance characteristics of Platform Event publication under load
- EventBridge rule configurations and routing logic
- Channel Member implementations for internal event consumption

