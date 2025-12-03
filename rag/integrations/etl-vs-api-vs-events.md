---
title: "ETL vs API vs Events: Integration Pattern Selection"
level: "Intermediate"
tags:
  - integrations
  - patterns
  - etl
  - api
  - platform-events
  - decision-framework
last_reviewed: "2025-01-XX"
---

# ETL vs API vs Events: Integration Pattern Selection

## Overview

Different integration patterns serve different use cases. Understanding when to use ETL (batch), API (synchronous), or Events (asynchronous) is critical for building scalable, maintainable integrations.

## Integration Pattern Types

### ETL (Extract, Transform, Load) - Batch Integration

**Pattern**: Scheduled or on-demand batch synchronization of large data sets

**Characteristics**:
- High-volume data transfer (hundreds of thousands of records)
- Scheduled execution (nightly, hourly, on-demand)
- Idempotent operations using External IDs
- File-based staging for very large data sets
- Error handling with retry logic and job tracking

**Use Cases**:
- Student Information System (SIS) synchronization (300K+ records daily)
- Legacy system data migration
- Periodic data reconciliation
- Bulk data updates from external systems

**Tools**: Dell Boomi, MuleSoft, Salesforce Bulk API

### API (REST/SOAP) - Synchronous Integration

**Pattern**: Real-time or near-real-time request/response integration

**Characteristics**:
- Synchronous or near-synchronous calls
- Request/response pattern
- Immediate feedback required
- Lower volume per call
- Error handling with retry logic

**Use Cases**:
- Notice generation requests
- Status checks for pending operations
- User search and lookup
- Document retrieval
- Real-time data validation

**Tools**: REST APIs, SOAP APIs, Named Credentials, Custom Metadata Types

### Events (Platform Events) - Asynchronous Integration

**Pattern**: Event-driven, publish-subscribe integration

**Characteristics**:
- Asynchronous processing
- Decoupled systems
- Fan-out to multiple subscribers
- Event-driven triggers
- Self-contained payloads

**Use Cases**:
- Application submission events
- Status change notifications
- Data change propagation
- Cross-system orchestration
- Analytics pipeline feeds

**Tools**: Platform Events, Event Channels, External Event Bus (EventBridge)

## Pattern Selection Criteria

### Use ETL When

- **Volume**: Processing hundreds of thousands or millions of records
- **Timing**: Scheduled or periodic synchronization is acceptable
- **Source System**: Legacy systems with batch-oriented interfaces
- **Data Model**: Large-scale data migration or synchronization
- **Performance**: Bulk operations are more efficient than individual calls

**Example**: Daily synchronization of 300,000+ student records from Oracle SIS to Salesforce Education Cloud

### Use API When

- **Timing**: Real-time or near-real-time response required
- **Volume**: Lower volume per transaction
- **Interaction**: User-initiated actions requiring immediate feedback
- **Source System**: Modern systems with REST/SOAP APIs
- **Feedback**: Immediate success/failure response needed

**Example**: Notice generation request where user needs immediate confirmation

### Use Events When

- **Decoupling**: Systems should be decoupled
- **Multiple Subscribers**: Multiple systems need to react to the same event
- **Asynchronous**: Asynchronous processing is acceptable or preferred
- **Orchestration**: Cross-system orchestration required
- **Scalability**: High-volume event scenarios requiring scalable processing

**Example**: Application submission event that triggers SIS sync, analytics pipeline, and notification service

## Hybrid Patterns

### ETL + Events

Combine ETL for bulk synchronization with Events for real-time updates:

- ETL handles initial load and periodic reconciliation
- Events handle incremental updates and business events
- Provides both bulk efficiency and real-time responsiveness

### API + Events

Combine API for immediate responses with Events for downstream processing:

- API provides immediate user feedback
- Events trigger downstream processing and notifications
- Balances user experience with system decoupling

## Implementation Patterns

### ETL Implementation Pattern

**File-Based Staging for Large Data Sets**:
- Write large ID lists to disk
- Dynamically split into batched SQL IN-clause queries
- Process in manageable chunks (1,000-10,000 records per batch)
- Use External IDs for idempotent upserts

**Job Tracking**:
- Integration job tracking fields on all integrated objects
- Correlation IDs linking Salesforce records to external system job logs
- Status fields: `Last_Sync_Timestamp__c`, `Last_Sync_Status__c`, `Last_Sync_Error__c`, `Integration_Job_ID__c`

**Error Handling**:
- Error capture at each step
- Retry logic with exponential backoff
- Dead-letter queues for records that cannot be processed
- Comprehensive logging for troubleshooting

### API Implementation Pattern

**Named Credentials**:
- All API endpoints use Named Credentials (no hardcoded URLs)
- Environment-specific endpoint configurations
- Centralized authentication management

**Custom Metadata Types**:
- Interface configuration stored in Custom Metadata Types
- Environment-specific settings (endpoints, timeouts, headers)
- Reusable across multiple integrations

**Error Handling**:
- Standardized error responses
- Retry logic for transient failures
- Comprehensive logging to `LOG_LogMessage__c` object
- User-friendly error messages

### Events Implementation Pattern

**Event Publication**:
- Prefer Flows over Apex for declarative event publication
- Self-contained payloads with all necessary context
- Minimal PII to balance functionality with privacy
- Idempotent design for safe retry operations

**Event Routing**:
- Event Channel routes to external event bus
- External event bus fans out to multiple subscribers
- Channel Members in Salesforce subscribe for internal logging/automation

**Error Handling**:
- Idempotent payload design
- Retry logic at event bus level
- Dead-letter queues for unprocessable events
- Comprehensive logging and monitoring

## Best Practices

### ETL Best Practices

- Break large data sets into manageable chunks
- Use file-based staging for ID lists exceeding 50,000 records
- Implement error handling at every step
- Log all operations for troubleshooting and audit
- Use External IDs for idempotent operations
- Track integration jobs with correlation IDs

### API Best Practices

- Use Named Credentials for all endpoints
- Store configuration in Custom Metadata Types
- Implement comprehensive error handling
- Log all API calls for troubleshooting
- Use retry logic for transient failures
- Return standardized error responses

### Events Best Practices

- Prefer Flows over Apex when possible
- Design self-contained payloads
- Minimize PII in event payloads
- Include external IDs for correlation
- Design idempotent payloads
- Implement comprehensive monitoring

## Tradeoffs

### ETL Tradeoffs

**Advantages**:
- Efficient for large volumes
- Scheduled execution reduces system load
- Idempotent operations enable safe retries

**Disadvantages**:
- Not real-time
- Requires job scheduling and monitoring
- Error recovery can be complex

### API Tradeoffs

**Advantages**:
- Real-time or near-real-time
- Immediate feedback
- Direct request/response pattern

**Disadvantages**:
- Higher system load
- Tight coupling between systems
- Requires careful error handling

### Events Tradeoffs

**Advantages**:
- Decoupled systems
- Scalable processing
- Multiple subscribers

**Disadvantages**:
- Asynchronous (no immediate feedback)
- Event ordering complexity
- Requires monitoring and observability

## When to Combine Patterns

Combine patterns when:

- Initial load requires ETL, incremental updates use Events
- User actions use API, downstream processing uses Events
- Bulk reconciliation uses ETL, real-time updates use Events
- Different systems require different patterns

## Decision Framework

1. **Volume**: High volume → ETL, Low volume → API or Events
2. **Timing**: Scheduled → ETL, Real-time → API, Asynchronous → Events
3. **Coupling**: Tight coupling → API, Loose coupling → Events
4. **Subscribers**: Single → API or ETL, Multiple → Events
5. **Feedback**: Immediate → API, Delayed → ETL or Events

## Q&A

### Q: When should I use ETL vs API vs Events?

**A**: Use **ETL** for high-volume, scheduled batch synchronization (hundreds of thousands of records). Use **API** for real-time, synchronous integrations requiring immediate feedback. Use **Events** for asynchronous, decoupled integrations with multiple subscribers or when you need loose coupling between systems.

### Q: Can I combine different integration patterns?

**A**: Yes, combining patterns is common and recommended. For example: use ETL for initial data loads, Events for incremental updates, and API for user-initiated actions. Different systems may require different patterns based on their characteristics and requirements.

### Q: What are the performance implications of each pattern?

**A**: **ETL** handles high volumes efficiently but runs on a schedule. **API** provides immediate response but has lower throughput and requires synchronous processing. **Events** are asynchronous and scalable but don't provide immediate feedback. Choose based on volume, timing, and feedback requirements.

### Q: How do I handle errors in each integration pattern?

**A**: **ETL**: Use job tracking, retry logic, and error logging. **API**: Implement retry logic with exponential backoff, handle HTTP errors gracefully, and log failures. **Events**: Use event replay capabilities, implement idempotent subscribers, and monitor event delivery.

### Q: What are the tradeoffs between tight and loose coupling?

**A**: **Tight coupling (API)**: Provides immediate feedback and simpler error handling but creates dependencies between systems. **Loose coupling (Events)**: Enables scalability and resilience but requires more complex error handling and monitoring. Choose based on whether systems need to be decoupled.

### Q: How do I decide between REST API and SOAP API?

**A**: Use **REST API** for modern integrations, mobile apps, and when you need JSON payloads. Use **SOAP API** for legacy systems, when you need WSDL contracts, or when working with systems that only support SOAP. REST is generally preferred for new integrations.

### Q: What is the difference between Platform Events and Change Data Capture (CDC)?

**A**: **Platform Events** are custom events you publish explicitly from your code/flows. **CDC** automatically publishes change events when records are created, updated, or deleted. Use Platform Events for business events; use CDC for data change tracking.

### Q: How do I handle large data volumes in API integrations?

**A**: For large volumes, prefer ETL or Events over API. If API is required, implement pagination, batch processing, and consider using Bulk API for large operations. Monitor API call limits and implement rate limiting/throttling to avoid hitting governor limits.

## Related Patterns

- [Integration Platform Patterns](integration-platform-patterns.md) - MuleSoft and Dell Boomi patterns
- [SIS Sync Patterns](sis-sync-patterns.md) - High-volume ETL synchronization patterns
- [Change Data Capture Patterns](change-data-capture-patterns.md) - CDC for event-driven integration
- [Callout Best Practices](callout-best-practices.md) - API callout patterns
- [Event-Driven Architecture](../architecture/event-driven-architecture.md) - Platform Events patterns
- [Large Data Loads](../development/large-data-loads.md) - Bulk data operation patterns

