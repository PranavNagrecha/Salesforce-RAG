---
layout: default
title: ETL vs API vs Events: Integration Pattern Selection
description: Decision framework for choosing between ETL, API, and event-driven integration patterns based on use case requirements
permalink: /rag/integrations/etl-vs-api-vs-events.html
level: Intermediate
tags:
  - integrations
  - decision-framework
  - etl
  - api
  - events
last_reviewed: 2025-12-03
---

# ETL vs API vs Events: Integration Pattern Selection

## Overview

Different integration patterns serve different use cases. This decision framework helps architects and developers choose the right integration pattern based on requirements for data volume, latency, directionality, and system coupling.

**Core Principle**: Choose the integration pattern that best matches your requirements for data volume, latency, directionality, and system coupling. There is no one-size-fits-all solution.

## Prerequisites

**Required Knowledge**:
- Understanding of Salesforce integration capabilities
- Familiarity with ETL tools and patterns
- Knowledge of REST/SOAP APIs
- Understanding of event-driven architecture
- Knowledge of data synchronization patterns

**Recommended Reading**:
- <a href="{{ '/rag/integrations/integration-platform-patterns.html' | relative_url }}">Integration Platform Patterns</a> - Integration platform patterns and best practices
- <a href="{{ '/rag/architecture/event-driven-architecture.html' | relative_url }}">Event-Driven Architecture</a> - Event-driven integration patterns
- <a href="{{ '/rag/integrations/change-data-capture-patterns.html' | relative_url }}">Change Data Capture Patterns</a> - CDC patterns for real-time synchronization

## When to Use Each Pattern

### Use ETL (Extract, Transform, Load) When

- **High data volume**: Need to move large datasets (millions of records)
- **Batch processing**: Can tolerate delays (hourly, daily, weekly syncs)
- **Bidirectional sync**: Need to sync data in both directions
- **Complex transformations**: Need extensive data transformation and cleansing
- **Historical data loads**: Need to load historical data or perform one-time migrations
- **System decoupling**: Source and target systems don't need real-time awareness
- **Cost optimization**: Need to minimize API call costs

**Common Use Cases**:
- Daily synchronization of master data
- Historical data migration
- Bulk data imports from legacy systems
- Data warehouse population
- Compliance and reporting data aggregation

### Use API (REST/SOAP) When

- **Real-time requirements**: Need immediate data synchronization
- **Request-response pattern**: Need synchronous request-response interactions
- **Low to medium volume**: Processing thousands, not millions of records
- **Transactional operations**: Need to perform business transactions (create orders, process payments)
- **User-initiated actions**: Actions triggered by user interactions
- **Error handling**: Need immediate error feedback
- **System coupling acceptable**: Systems can be directly coupled

**Common Use Cases**:
- User authentication and authorization
- Real-time order processing
- Payment processing
- Customer portal interactions
- Mobile app data access
- On-demand data retrieval

### Use Events (Platform Events, CDC, Streaming API) When

- **Event-driven architecture**: Need decoupled, asynchronous communication
- **Multiple subscribers**: Multiple systems need to react to the same event
- **Real-time notifications**: Need near-real-time event notifications
- **System decoupling**: Source system shouldn't know about subscribers
- **Scalability**: Need to handle high event volumes
- **Event sourcing**: Need event history for audit or replay
- **Microservices architecture**: Part of microservices-based system

**Common Use Cases**:
- Status change notifications
- Integration orchestration
- Audit and compliance logging
- Real-time dashboards and monitoring
- Multi-system synchronization
- Event-driven workflows

## Decision Framework

### Step 1: Assess Data Volume

**High Volume (Millions of records)**:
- ✅ ETL (Bulk API, Data Loader, ETL tools)
- ❌ API (too many calls, governor limits)
- ⚠️ Events (possible but requires careful design)

**Medium Volume (Thousands to hundreds of thousands)**:
- ✅ API (REST/SOAP with bulkification)
- ✅ ETL (if batch is acceptable)
- ✅ Events (if event-driven architecture)

**Low Volume (Hundreds to thousands)**:
- ✅ API (most flexible)
- ✅ Events (if event-driven)
- ⚠️ ETL (overkill for small volumes)

### Step 2: Assess Latency Requirements

**Real-time (Seconds to minutes)**:
- ✅ API (synchronous request-response)
- ✅ Events (near-real-time notifications)
- ❌ ETL (batch processing too slow)

**Near-real-time (Minutes to hours)**:
- ✅ Events (event-driven with processing delays)
- ✅ API (if acceptable latency)
- ⚠️ ETL (if hourly sync is acceptable)

**Batch (Hours to days)**:
- ✅ ETL (designed for batch processing)
- ❌ API (unnecessary overhead)
- ❌ Events (not designed for batch)

### Step 3: Assess Directionality

**Unidirectional (Salesforce → External)**:
- ✅ Events (Platform Events, CDC)
- ✅ API (outbound callouts)
- ✅ ETL (scheduled exports)

**Unidirectional (External → Salesforce)**:
- ✅ API (inbound REST/SOAP)
- ✅ ETL (scheduled imports)
- ⚠️ Events (requires external system to subscribe)

**Bidirectional**:
- ✅ ETL (handles both directions)
- ✅ API (separate endpoints for each direction)
- ⚠️ Events (requires events in both directions)

### Step 4: Assess System Coupling

**Tight Coupling Acceptable**:
- ✅ API (direct system-to-system calls)
- ✅ ETL (direct database connections)

**Loose Coupling Required**:
- ✅ Events (decoupled via event bus)
- ⚠️ ETL (can be decoupled with message queues)
- ❌ API (creates tight coupling)

### Step 5: Assess Transformation Complexity

**Simple Mapping**:
- ✅ API (lightweight transformation)
- ✅ Events (minimal transformation)
- ⚠️ ETL (overkill for simple mapping)

**Complex Transformation**:
- ✅ ETL (designed for complex transformations)
- ⚠️ API (requires Apex transformation logic)
- ❌ Events (minimal transformation support)

## Pattern Comparison Matrix

| Criteria | ETL | API | Events |
|----------|-----|-----|--------|
| **Data Volume** | High (millions) | Low-Medium (thousands) | Medium-High (thousands-millions) |
| **Latency** | Batch (hours-days) | Real-time (seconds) | Near-real-time (minutes) |
| **Directionality** | Bidirectional | Unidirectional/Bidirectional | Unidirectional (typically) |
| **Coupling** | Medium | Tight | Loose |
| **Transformation** | Complex | Simple-Medium | Simple |
| **Error Handling** | Batch retry | Immediate feedback | Async retry |
| **Cost** | Low (bulk operations) | Medium (per API call) | Low (event subscriptions) |
| **Scalability** | High | Medium | High |
| **Complexity** | Medium-High | Low-Medium | Medium |

## Hybrid Approaches

### ETL + Events

**Pattern**: Use ETL for initial bulk load, then Events for incremental updates.

**Use Case**: Migrate historical data via ETL, then use CDC for real-time incremental sync.

**Example**:
- Initial load: ETL tool loads 10 million historical records
- Incremental sync: CDC publishes change events for new/updated records

### API + Events

**Pattern**: Use API for synchronous operations, Events for asynchronous notifications.

**Use Case**: Create record via API (immediate response), publish event for downstream systems.

**Example**:
- User creates Case via REST API (immediate response)
- Platform Event published for notification systems
- Multiple subscribers react to event (email, SMS, external system)

### ETL + API

**Pattern**: Use ETL for bulk operations, API for real-time operations.

**Use Case**: Bulk import via ETL, real-time updates via API.

**Example**:
- Daily bulk import of product catalog via ETL
- Real-time price updates via REST API

## Common Anti-Patterns

### ❌ Using API for High-Volume Batch Operations

**Problem**: Making millions of API calls for bulk data operations.

**Solution**: Use ETL tools with Bulk API or Data Loader.

**Impact**: Governor limit violations, performance issues, high costs.

### ❌ Using ETL for Real-Time Requirements

**Problem**: Using batch ETL when real-time sync is required.

**Solution**: Use API or Events for real-time requirements.

**Impact**: Business delays, poor user experience.

### ❌ Using Events for Simple Request-Response

**Problem**: Using events when synchronous request-response is needed.

**Solution**: Use API for synchronous operations.

**Impact**: Unnecessary complexity, delayed responses.

### ❌ Tight Coupling with Events

**Problem**: Subscribers directly depend on event structure.

**Solution**: Use event versioning and transformation layers.

**Impact**: Brittle integrations, difficult maintenance.

## Related Patterns

- <a href="{{ '/rag/integrations/integration-platform-patterns.html' | relative_url }}">Integration Platform Patterns</a> - Integration platforms and middleware patterns
- <a href="{{ '/rag/architecture/event-driven-architecture.html' | relative_url }}">Event-Driven Architecture</a> - Event-driven integration patterns
- <a href="{{ '/rag/integrations/change-data-capture-patterns.html' | relative_url }}">Change Data Capture Patterns</a> - CDC patterns for real-time sync
- <a href="{{ '/rag/integrations/callout-best-practices.html' | relative_url }}">Callout Best Practices</a> - API callout patterns and best practices
- <a href="{{ '/rag/integrations/sis-sync-patterns.html' | relative_url }}">SIS Sync Patterns</a> - High-volume batch synchronization patterns

## Q&A

### Q: When should I use ETL instead of API?

**A**: Use ETL when: (1) **High data volume** (millions of records), (2) **Batch processing acceptable** (hourly/daily syncs), (3) **Complex transformations** needed, (4) **Bidirectional sync** required, (5) **Cost optimization** important (bulk operations are cheaper). ETL is designed for bulk data movement and transformation.

### Q: When should I use API instead of ETL?

**A**: Use API when: (1) **Real-time requirements** (immediate synchronization), (2) **Low to medium volume** (thousands of records), (3) **Transactional operations** (create orders, process payments), (4) **User-initiated actions** (user interactions), (5) **Immediate error feedback** needed. API provides synchronous request-response interactions.

### Q: When should I use Events instead of API?

**A**: Use Events when: (1) **Event-driven architecture** (decoupled systems), (2) **Multiple subscribers** (multiple systems react to same event), (3) **Near-real-time notifications** (minutes latency acceptable), (4) **System decoupling** required (source doesn't know about subscribers), (5) **Scalability** important (high event volumes). Events enable asynchronous, decoupled communication.

### Q: Can I use multiple integration patterns together?

**A**: Yes, **hybrid approaches** are common: (1) **ETL + Events** (bulk load via ETL, incremental via events), (2) **API + Events** (synchronous operations via API, async notifications via events), (3) **ETL + API** (bulk operations via ETL, real-time via API). Choose patterns based on specific use case requirements.

### Q: How do I choose between REST API and SOAP API?

**A**: Choose **REST API** for: (1) **Modern integrations** (simpler, JSON-based), (2) **Mobile apps** (lightweight), (3) **Stateless operations** (REST is stateless). Choose **SOAP API** for: (1) **Enterprise integrations** (WS-Security, transactions), (2) **Complex operations** (SOAP supports complex types), (3) **Legacy systems** (many legacy systems use SOAP). REST is generally preferred for new integrations.

### Q: How do I choose between Platform Events and Change Data Capture?

**A**: Choose **Platform Events** for: (1) **Custom events** (business events, not just data changes), (2) **Event orchestration** (complex event-driven workflows), (3) **Custom payloads** (structured event data). Choose **Change Data Capture** for: (1) **Standard object changes** (automatic change notifications), (2) **Data synchronization** (sync data to external systems), (3) **Audit and compliance** (track all data changes). Use CDC for data changes, Platform Events for business events.

### Q: What are common mistakes when choosing integration patterns?

**A**: Common mistakes: (1) **Using API for high-volume batch** (use ETL instead), (2) **Using ETL for real-time requirements** (use API/Events), (3) **Using Events for simple request-response** (use API), (4) **Tight coupling with events** (use event versioning), (5) **Not considering hybrid approaches** (combine patterns when needed). Choose patterns based on requirements, not convenience.

### Q: How do I handle errors in each integration pattern?

**A**: **ETL**: (1) **Batch retry** (retry failed records in next batch), (2) **Error logging** (log errors to error object), (3) **Manual intervention** (review error reports). **API**: (1) **Immediate feedback** (return errors in response), (2) **Retry logic** (implement retry with exponential backoff), (3) **Error handling** (try-catch blocks, error responses). **Events**: (1) **Async retry** (subscribers implement retry), (2) **Dead letter queue** (failed events to DLQ), (3) **Event replay** (replay events for recovery).
