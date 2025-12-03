---
layout: default
title: Asynchronous Apex Patterns
description: Comprehensive patterns for Batch, Queueable, Scheduled, and future methods in Salesforce
permalink: /rag/development/asynchronous-apex-patterns.html
level: Intermediate
tags:
  - apex
  - async
  - performance
last_reviewed: 2025-12-03
---

# Asynchronous Apex Patterns

> **Based on Real Implementation Experience**: These patterns come from high-volume integrations, data migrations, and long-running processes where synchronous Apex or Flow is not sufficient.

## Overview

Asynchronous Apex APIs—**Batch**, **Queueable**, **Scheduled**, and `@future`—allow you to:

- Process **large data volumes** without blocking user transactions.
- Perform **callouts after DML**.
- Run logic on a **schedule** or in response to **events**.

This document describes when to use each mechanism and how to structure code so that async jobs are **testable, observable, and safe**.

## Prerequisites

- **Required Knowledge**:
  - Core Apex language features.
  - Synchronous trigger and service patterns (see `apex-patterns.md`).

- **Recommended Reading**:
  - <a href="{{ '/rag/development/governor-limits-and-optimization.html' | relative_url }}">Governor Limits and Optimization</a>
  - <a href="{{ '/rag/code-examples/apex/batch-examples.html' | relative_url }}">Batch Apex Code Examples</a>
  - <a href="{{ '/rag/code-examples/apex/queueable-examples.html' | relative_url }}">Queueable Apex Code Examples</a>
  - <a href="{{ '/rag/code-examples/apex/scheduled-examples.html' | relative_url }}">Scheduled Apex Code Examples</a>

## When to Use

### Use Async Apex When

- Processing **large datasets** (tens or hundreds of thousands of records).
- Making **callouts** after DML, especially from triggers or record-triggered Flows.
- Running **periodic maintenance jobs** (nightly cleanup, recalculation, sync).
- Chaining **multi-step workflows** that would hit limits in a single transaction.

### Avoid Async Apex When

- You only have **a few records** and simple logic (synchronous is enough).
- You need **immediate user feedback** in the same transaction.
- The pattern can be satisfied with **record-triggered Flows with async paths** and is easier to maintain declaratively.

## Core Concepts

### Transaction Boundaries

Each async job runs in its own **transaction** with its **own governor limits**. This allows you to:

- Reset limits after heavy synchronous work.
- Break work into multiple independent units.

### Idempotency

Async jobs should be **idempotent**:

- Safe to retry without corrupting data.
- Use **external Ids** or **status flags** to avoid double-processing.

### Visibility and Monitoring

Use:

- `AsyncApexJob` queries for status.
- Structured logging (see `error-handling-and-logging.md`).
- Platform Events where appropriate to signal completion.

## Patterns and Examples

### Pattern 1: Queueable for Post-Commit Work

**Intent**: Perform work that should happen **after** the main transaction commits (e.g., callouts, notifications).

**Structure**:

- Trigger/Flow enqueues a **Queueable** with the required context.
- Queueable:
  - Queries records.
  - Performs callouts or DML.
  - Logs results and errors.

See <a href="{{ '/rag/code-examples/apex/queueable-examples.html' | relative_url }}">Queueable Examples</a> for code.

### Pattern 2: Batch Apex for Large Data Volumes

**Intent**: Process **hundreds of thousands or millions** of records safely.

**Structure**:

- Implement `Database.Batchable<SObject>`.
- Use a **selective query** in `start`.
- Perform processing in `execute` with bulk-safe DML.
- Summarize results in `finish`.

See <a href="{{ '/rag/code-examples/apex/batch-examples.html' | relative_url }}">Batch Examples</a> and `apex-batch-template.md`.

### Pattern 3: Scheduled Apex for Time-Based Jobs

**Intent**: Run jobs at **fixed times** (nightly, weekly, hourly).

**Structure**:

- Implement `Schedulable`.
- In `execute`, enqueue **Queueable** or start **Batch** job.
- Use the **UI or cron expression** to schedule.

## Edge Cases and Limitations

- Org-wide limits on **concurrent async jobs** (Batch, Queueable, future).
- **Chaining** too many jobs can starve other processes.
- Async jobs can **fail silently** if not monitored; always log and alert.
- Async work on records that are frequently updated can cause **locking conflicts**; coordinate with locking strategies.

## Related Patterns

- <a href="{{ '/rag/development/locking-and-concurrency-strategies.html' | relative_url }}">Locking and Concurrency Strategies</a>
- <a href="{{ '/rag/development/error-handling-and-logging.html' | relative_url }}">Error Handling and Logging Framework</a>
- <a href="{{ '/rag/integrations/change-data-capture-patterns.html' | relative_url }}">Change Data Capture Patterns</a>

## Q&A

### Q: When should I choose Batch Apex over Queueable?

**A**: Use **Batch** when you need to process **very large datasets**, need **chunking** with per-batch context, or want to **track progress** across many records. Use **Queueable** for **lighter workloads**, **callouts**, and **chaining a few jobs** where you control the scope.

### Q: How many Queueable jobs can I chain?

**A**: Salesforce enforces limits on **concurrent async jobs** and **job chaining**. As a good practice, keep chains **short and intentional**, and consider **Batch** or **multiple entry points** if you need deeper workflows. Always consult the latest governor limits documentation.

### Q: How do I test asynchronous Apex?

**A**: Use `Test.startTest()` and `Test.stopTest()` to ensure async jobs run within the test context. Assert on the **final state of records**, **logs**, or **AsyncApexJob** records. For callouts, use `Test.setMock()` with `HttpCalloutMock` implementations.

