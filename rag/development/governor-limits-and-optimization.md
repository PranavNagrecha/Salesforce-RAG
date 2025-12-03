---
layout: default
title: Governor Limits and Performance Optimization
description: This topic covers Salesforce governor limits, performance optimization strategies, SOQL query optimization, selective query patterns, and resource management best practices
permalink: /rag/development/governor-limits-and-optimization.html
level: Intermediate
tags:
  - apex
  - performance
  - governor-limits
last_reviewed: 2025-12-03
---

# Governor Limits and Performance Optimization

> **Based on Real Implementation Experience**: These patterns come from large orgs with complex automations, integrations, and millions of records where governor limits are hit daily if code and Flows are not designed correctly.

## Overview

Governor limits are **hard platform constraints** that protect Salesforce multi-tenancy. Well-designed solutions treat limits as a **design input**, not an afterthought. This topic describes how to design Flows and Apex so they are **bulk-safe, selective, and resilient** under load.

This file focuses on:

- Core governor limit categories.
- Bulkification patterns for triggers, Flows, and Apex.
- SOQL and DML optimization strategies.
- Caching and reuse patterns.
- Practical troubleshooting when limits are hit in production.

## Prerequisites

- **Required Knowledge**:
  - Basic Apex syntax and trigger concepts.
  - Understanding of **record-triggered Flows**.
  - Familiarity with Salesforce data model and relationships.

- **Recommended Reading**:
  - <a href="{{ '/rag/development/order-of-execution.html' | relative_url }}">Order of Execution</a> - When triggers and Flows run.
  - <a href="{{ '/rag/development/apex-patterns.html' | relative_url }}">Apex Patterns</a> - Layered architecture (service, domain, selector).
  - <a href="{{ '/rag/development/soql-query-patterns.html' | relative_url }}">SOQL Query Patterns</a> - Detailed query patterns and anti-patterns.
  - <a href="{{ '/rag/troubleshooting/governor-limit-errors.html' | relative_url }}">Governor Limit Errors</a> - Error messages and resolutions.

## When to Use

### Use These Patterns When

- Designing **new** Flows, triggers, or Apex services.
- Refactoring legacy logic that occasionally hits governor limits.
- Building **high-volume** integrations (batch loads, CDC, Platform Events).
- Implementing features on **objects with millions of records**.
- Preparing for performance or load testing.

### Avoid Over-Optimizing When

- The automation runs on **low-volume** objects and is simple.
- Readability would be significantly harmed for marginal gains.
- You have no evidence of performance or limit issues and the code is already bulk-safe.

The goal is **safe by default**, then optimize where you have clear risk or evidence.

## Core Concepts

### Bulkification

Bulkification means designing logic to handle **many records in one transaction**:

- Always process **collections** (`List<SObject>`, `Set<Id>`) instead of single records.
- Never perform **DML or SOQL inside a loop**.
- Aggregate work into collections and perform **single DML** operations where possible.

### Selective Queries

Selective queries:

- Filter on **indexed fields** (Id, external Ids, some lookup fields).
- Return a **small subset of rows** relative to total table volume.
- Use **Query Plan** to validate selectivity.

### Workload Shaping

Workload shaping patterns:

- Moving heavy processing to **async Apex** (Batch, Queueable, @future).
- Splitting work across **time windows** or **smaller batches**.
- Using **Platform Events** or **CDC** for eventual consistency.

### Governor Limit Visibility

Use `Limits` methods in Apex and **debug logs** in lower environments to:

- Track how many queries and DML statements code uses in realistic bulk scenarios.
- Identify which components (Flow vs Apex vs managed package) consume limits.

## Patterns and Examples

### Pattern 1: Bulk-Safe Trigger or Record-Triggered Flow

**Intent**: Ensure that automation can safely process **200+ records** without hitting limits.

**Structure**:

- Accept all records as a **collection**.
- Derive **sets of Ids** needed for queries.
- Perform **one query per object** needed.
- Perform **at most one DML operation per object type** per logical outcome.

**Example (Apex)**:

- See <a href="{{ '/rag/code-examples/apex/trigger-examples.html' | relative_url }}">Trigger Handler Code Examples</a> for the full implementation.

### Pattern 2: Selector Layer with Caching

**Intent**: Centralize and optimize SOQL queries with optional in-transaction caching.

**Structure**:

- Use a **Selector class** per SObject.
- Provide methods like `selectByIds(Set<Id> ids)` and `selectByExternalIds(Set<String> extIds)`.
- Use a **static `Map<Id, SObject>`** for in-memory caching when appropriate.

### Pattern 3: Async Offload for Heavy Work

**Intent**: Move expensive work (complex calculations, callouts, large DML) to async Apex.

**Structure**:

- Trigger or Flow performs **minimal validation and logging**.
- Enqueues a **Queueable** or **Batch** job with the required context.
- Async job performs the heavy work and logs results.

See:

- <a href="{{ '/rag/development/asynchronous-apex-patterns.html' | relative_url }}">Asynchronous Apex Patterns</a>
- <a href="{{ '/rag/code-examples/apex/queueable-examples.html' | relative_url }}">Queueable Examples</a>

## Edge Cases and Limitations

- **Mixed DML**: User/provisioning operations may require separation into different transactions.
- **Managed Packages**: Hidden logic can consume limits; you may need to **simplify your side** or reduce event frequency.
- **LDV Objects**: Non-selective queries on objects with **millions of rows** will fail even if they work in sandboxes.
- **Portal and Integration Users**: High concurrency can make borderline patterns fail under load.

## Related Patterns

- <a href="{{ '/rag/development/soql-query-patterns.html' | relative_url }}">SOQL Query Patterns</a> - Deep dive on query design.
- <a href="{{ '/rag/development/large-data-loads.html' | relative_url }}">Large Data Loads</a> - Patterns for migrating and loading data at scale.
- <a href="{{ '/rag/patterns/cross-cutting-patterns.html' | relative_url }}">Cross-Cutting Patterns</a> - Bulkification and governor limit management across domains.
- <a href="{{ '/rag/integrations/change-data-capture-patterns.html' | relative_url }}">CDC Patterns</a> - Real-time patterns that interact with limit management.

## Q&A

### Q: How many records should I assume a trigger or Flow will process?

**A**: Always assume **at least 200 records** will be processed in a single transaction, because the platform batches DML operations. For integrations and data loads, assume **thousands of records per batch** and design patterns (batch Apex, Queueable) accordingly.

### Q: How do I know if a query is selective enough?

**A**: Use the **Query Plan** tool in Developer Console. A query is typically considered selective if it returns **less than 10%** of rows and uses an **indexed field** in the filter. Queries with a cost of **1 or 2** in Query Plan are usually safe; higher costs indicate potential issues, especially on LDV objects.

### Q: When should I move logic from Flow to Apex for performance?

**A**: Move logic to Apex when: (1) the Flow is approaching **element or CPU limits**, (2) you need **fine-grained control** over batching and retries, (3) you must handle **complex loops or calculations**, or (4) you need **robust error handling** and logging not easily modeled in Flow. Keep orchestration in Flow, but move heavy work to Apex services.

### Q: What is the safest way to handle large data loads?

**A**: Use **Bulk API** or **Batch Apex** with: (1) **idempotent logic** (safe to retry), (2) **external Ids** for upserts, (3) **chunked processing** (smaller batches if you hit limits), and (4) **staging tables or objects** when you need to preprocess data. See `large-data-loads.md` and `data-migration-patterns.md` for detailed patterns.

### Q: How can I prevent governor limit errors from breaking user-facing operations?

**A**: Design with **graceful degradation**: (1) perform **critical checks** first, (2) offload non-critical work to **async** jobs, (3) use **try-catch** with structured logging around DML and callouts, and (4) avoid chaining too many automations on a single transaction. Monitor logs and Platform Events to catch patterns early.

