---
layout: default
title: Large Data Loads
description: Patterns for loading and migrating large data volumes into Salesforce safely
permalink: /rag/development/large-data-loads.html
level: Intermediate
tags:
  - data-migration
  - performance
last_reviewed: 2025-12-03
---

# Large Data Loads

> **Based on Real Implementation Experience**: These patterns are drawn from migrations involving **tens of millions of records** and repeated cutovers across sandboxes and production.

## Overview

Large data loads introduce challenges around:

- **Governor limits** (queries, DML, heap).
- **Locking and concurrency**.
- **Data quality and reconciliation**.

This document provides a high-level view of data load patterns and defers detailed migration strategy to `data-migration-patterns.md`.

## Prerequisites

- **Required Knowledge**:
  - Basic understanding of Salesforce objects and relationships.
  - Familiarity with **Bulk API**, **Data Loader**, or ETL tools.

- **Recommended Reading**:
  - <a href="{{ '/rag/data-modeling/data-migration-patterns.html' | relative_url }}">Data Migration Patterns</a>
  - <a href="{{ '/rag/development/governor-limits-and-optimization.html' | relative_url }}">Governor Limits and Optimization</a>
  - <a href="{{ '/rag/troubleshooting/data-reconciliation.html' | relative_url }}">Data Reconciliation</a>

## When to Use These Patterns

- Initial **org cutover** from legacy systems.
- Large one-time **backfills** (e.g., historical cases, opportunities).
- Scheduled **nightly or weekly syncs** that move large volumes.

## Core Concepts

### Staging vs. Direct Load

- **Staging**: Load into **staging objects** first, then transform into target structures.
- **Direct**: Load directly into target objects when transformation is simple.

### Idempotent Loads

- Use **external Ids** and **upsert**.
- Design loads so they can be **re-run safely** without duplicates.

## Patterns and Examples

### Pattern 1: Staged Migration

- Load raw data into **staging objects**.
- Run **Batch Apex** or ETL to transform and load into core objects.
- Capture errors and **rejected records** for review.

### Pattern 2: Throttled Nightly Loads

- Break large jobs into **smaller batches**.
- Schedule at **low-traffic windows**.
- Use **Queueable** and **Batch** combinations with clear monitoring.

## Edge Cases and Limitations

- **Sharing recalculation** can cause performance issues when loading records that impact roles and sharing rules.
- **Workflow, Process Builder, and Flows** may trigger unexpectedly during loads; consider **bypass flags** or load into maintenance windows.

## Related Patterns

- <a href="{{ '/rag/data-modeling/external-ids-and-integration-keys.html' | relative_url }}">External IDs and Integration Keys</a>
- <a href="{{ '/rag/troubleshooting/governor-limit-errors.html' | relative_url }}">Governor Limit Errors</a>

## Q&A

### Q: Should I disable automations during large data loads?

**A**: Usually **yes** for non-critical automations, but plan and test carefully. Use **bypass flags** or temporary configuration where possible instead of deleting logic. Validate that required business rules (e.g., data quality) are still enforced appropriately.

