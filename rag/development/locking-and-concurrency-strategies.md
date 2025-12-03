---
layout: default
title: Locking and Concurrency Strategies
description: Patterns for handling row locking, UNABLE_TO_LOCK_ROW errors, and high-concurrency scenarios in Salesforce
permalink: /rag/development/locking-and-concurrency-strategies.html
level: Advanced
tags:
  - concurrency
  - locking
  - performance
last_reviewed: 2025-12-03
---

# Locking and Concurrency Strategies

> **Based on Real Implementation Experience**: This guide reflects patterns from **high-volume portals, integrations, and batch jobs** where locking issues are common.

## Overview

Salesforce uses **record-level locks** to ensure data integrity:

- Multiple transactions updating the **same records** at the same time can cause `UNABLE_TO_LOCK_ROW` errors.
- Poorly designed automations can create **hot spots** where many transactions compete for the same records.

This document describes strategies to **avoid, detect, and handle** locking issues.

## Prerequisites

- **Required Knowledge**:
  - Basic understanding of DML operations and transactions in Apex and Flows.

- **Recommended Reading**:
  - <a href="{{ '/rag/development/governor-limits-and-optimization.html' | relative_url }}">Governor Limits and Optimization</a>
  - <a href="{{ '/rag/troubleshooting/governor-limit-errors.html' | relative_url }}">Governor Limit Errors</a>

## When to Use These Patterns

- High-concurrency environments (Experience Cloud portals, heavy API integrations).
- **Batch and async jobs** that process records also touched by users.
- Objects with **roll-up summaries**, **parent-child dependencies**, or **sharing recalculation**.

## Core Concepts

### Lock Scope

- Locks are taken on **records being modified** and sometimes on **related records** (e.g., parent records for roll-up summaries).
- Operations that update many related child records can increase lock scope.

### Hot Spots

Hot spots are records that many transactions try to update at once, for example:

- A single `Account` with thousands of related `Contact` or `Case` updates.
- `Campaign` or `Opportunity` records updated by multiple jobs.

## Patterns and Examples

### Pattern 1: Orderly Processing by Parent Id

- Process child records **grouped by parent Id**.
- Use **ordered queries** and **Batch Apex** to reduce contention.

### Pattern 2: Retry with Backoff

- Catch `DmlException` with `UNABLE_TO_LOCK_ROW`.
- Retry a **small number of times** with increasing delays (in async Apex).
- Log failures after max retries.

### Pattern 3: Reduce Unnecessary Updates

- Avoid DML when **no actual data change** is required.
- Compare fields before performing updates to reduce lock frequency.

## Edge Cases and Limitations

- Some locking behavior is **not fully documented**, especially around managed packages.
- High-volume **sharing recalculation** can exacerbate locking problems.

## Related Patterns

- <a href="{{ '/rag/development/asynchronous-apex-patterns.html' | relative_url }}">Asynchronous Apex Patterns</a>
- <a href="{{ '/rag/development/error-handling-and-logging.html' | relative_url }}">Error Handling and Logging Framework</a>

## Q&A

### Q: How can I reproduce locking issues in a sandbox?

**A**: Use **anonymous Apex** and **multiple concurrent test runs** (e.g., via separate users or scripts) to simulate simultaneous updates to the same records. Also, run **Batch Apex** and interactive updates at the same time to mimic production concurrency.

