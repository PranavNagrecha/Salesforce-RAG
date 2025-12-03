---
title: "Governor Limits and Performance Optimization"
level: "Advanced"
tags:
  - apex
  - development
  - patterns
  - governor-limits
  - performance
  - optimization
last_reviewed: "2025-01-XX"
---

# Governor Limits and Performance Optimization

## Overview

This topic covers Salesforce governor limits, performance optimization strategies, SOQL query optimization, selective query patterns, and resource management best practices. These patterns are especially relevant for integration-heavy systems with large data volumes, where proper limit management becomes critical for system performance and scalability.

## Prerequisites

**Required Knowledge**:
- Understanding of Salesforce governor limits
- Knowledge of SOQL query syntax and optimization
- Understanding of Apex programming fundamentals
- Familiarity with DML operations and bulkification

**Recommended Reading**:
- [Apex Patterns](apex-patterns.md) - Apex class structure and bulkification patterns
- [SOQL Query Patterns](soql-query-patterns.md) - Query optimization and selectivity
- [Asynchronous Apex Patterns](asynchronous-apex-patterns.md) - Async processing for large operations
- [Order of Execution](order-of-execution.md) - Transaction execution order

## Consensus Best Practices

- **Always bulkify operations**: Process collections of records, never single records in loops. This reduces the number of DML operations and SOQL queries, staying within governor limits and improving performance.

- **Avoid SOQL and DML in loops**: Never place SOQL queries or DML operations inside loops. Gather all necessary data before loops and perform operations on collections outside loops to prevent hitting governor limits.

- **Use selective WHERE clauses**: Always use indexed fields in WHERE clauses to ensure query selectivity. Queries that return more than 10% of records in an object may be non-selective and cause performance issues.

- **Optimize SOQL queries**: Retrieve only necessary fields, use relationship queries to combine data, leverage aggregate queries for counts, and use subqueries for related data to minimize the number of queries.

- **Monitor governor limit usage**: Use `Limits` class methods to check current usage and implement proactive limit checking. Log limit usage in production to identify optimization opportunities.

- **Use asynchronous processing for large operations**: Use Batch Apex, Queueable Apex, or Scheduled Apex for operations that exceed synchronous limits or process large data volumes.

- **Implement query result pagination**: For large result sets, use OFFSET or implement cursor-based pagination to process data in manageable chunks without hitting heap size limits.

- **Optimize heap size usage**: Avoid storing large collections in memory, use streaming patterns for large datasets, and release object references when no longer needed to prevent heap size exceptions.

- **Use Bulk API for large data operations**: When processing thousands or millions of records, use Bulk API 2.0 instead of standard REST/SOAP API to handle large volumes efficiently and respect API limits.

- **Test with maximum data volumes**: Always test with bulk data (200+ records minimum) to ensure code handles governor limits correctly and performs well under load.

## Key Patterns and Examples

### Pattern 1: Governor Limits Monitoring and Proactive Checking

**When to use**: When you need to monitor resource usage, prevent limit exceptions, or implement graceful degradation when approaching limits.

**Implementation approach**:
- Use `Limits` class methods to check current usage (e.g., `Limits.getQueries()`, `Limits.getDmlStatements()`, `Limits.getCpuTime()`)
- Implement proactive limit checking before expensive operations
- Log limit usage for monitoring and optimization
- Implement fallback mechanisms when approaching limits
- Use `Test.startTest()` and `Test.stopTest()` to reset limits in test contexts

**Why it's recommended**: Proactive limit checking prevents unexpected exceptions and enables graceful degradation. Monitoring limit usage helps identify optimization opportunities and ensures code performs well under load. This pattern is especially important in integration-heavy systems where resource usage can vary significantly.

**Example scenario**: Before executing a batch of DML operations, check `Limits.getDmlStatements()` and `Limits.getLimitDmlStatements()`. If usage exceeds 80% of the limit, log a warning and consider deferring non-critical operations to a Queueable job.

### Pattern 2: Selective Query Optimization

**When to use**: When designing SOQL queries that need to perform well and avoid non-selective query warnings.

**Implementation approach**:
- Use indexed fields in WHERE clauses (Id, Name, Email, External ID fields, date fields, lookup fields)
- Ensure queries return less than 10% of records in the object (selective threshold)
- Combine multiple indexed fields for better selectivity
- Use date range filters with indexed date fields
- Avoid functions on indexed fields in WHERE clauses (e.g., `UPPER(Email)`)
- Use `WITH SECURITY_ENFORCED` or `WITH USER_MODE` which can improve query performance

**Why it's recommended**: Selective queries use indexes efficiently, reducing query time and database load. Non-selective queries can cause performance issues and may be blocked in production. This pattern is critical for high-volume systems where query performance directly impacts user experience.

**Example scenario**: A query filtering on `Industry = 'Technology'` may be non-selective if Technology represents 30% of accounts. Adding a date filter on `CreatedDate` (indexed) and combining with `AnnualRevenue > 1000000` (indexed) makes the query selective and performant.

### Pattern 3: Query Result Pagination

**When to use**: When processing large result sets that could exceed heap size limits or when you need to process data in manageable chunks.

**Implementation approach**:
- Use `LIMIT` clause to restrict result set size
- Use `OFFSET` for simple pagination (limited to 2,000 records)
- Implement cursor-based pagination using `Id > lastProcessedId ORDER BY Id LIMIT 2000` for large datasets
- Process results in batches and continue until no more records
- Use Batch Apex for very large datasets (millions of records)

**Why it's recommended**: Pagination prevents heap size exceptions and allows processing of large datasets without hitting memory limits. Cursor-based pagination is more efficient than OFFSET for large datasets and doesn't have the 2,000 record limit. This pattern is essential for data migration, reporting, and integration scenarios.

**Example scenario**: Processing 100,000 Account records requires pagination. Use cursor-based pagination: query `SELECT Id FROM Account WHERE Id > :lastId ORDER BY Id LIMIT 2000`, process the batch, then continue with the last Id from the batch until no more records.

### Pattern 4: Asynchronous Processing for Large Operations

**When to use**: When operations exceed synchronous limits, process large data volumes, or need to perform long-running tasks.

**Implementation approach**:
- Use Batch Apex for processing thousands or millions of records
- Use Queueable Apex for chaining jobs or callouts after DML
- Use Scheduled Apex for time-based operations
- Implement proper error handling and retry logic
- Monitor job status and handle failures gracefully

**Why it's recommended**: Asynchronous processing provides separate governor limit contexts, allowing processing of large datasets without hitting synchronous limits. It also improves user experience by not blocking the UI. This pattern is essential for integration scenarios, data migrations, and bulk operations.

**Example scenario**: A nightly sync of 500,000 records from an external system uses Batch Apex to process records in batches of 200. Each batch executes in its own context with fresh governor limits, allowing the entire sync to complete successfully.

**Related**: [Asynchronous Apex Patterns](asynchronous-apex-patterns.md) - Complete guide to Batch, Queueable, and Scheduled Apex patterns
- [Performance Tuning](../observability/performance-tuning.md) - LDV handling, caching strategies, and advanced performance optimization

### Pattern 5: Heap Size Optimization

**When to use**: When processing large datasets, storing large collections, or experiencing heap size exceptions.

**Implementation approach**:
- Avoid storing large collections in memory
- Process data in streams rather than loading everything into memory
- Use `transient` keyword for Visualforce variables that don't need to be serialized
- Release object references when no longer needed (set to null)
- Use Database.query() with LIMIT instead of storing all results
- Implement pagination for large result sets

**Why it's recommended**: Heap size limits (6MB synchronous, 12MB asynchronous) can be exceeded when storing large collections. Optimizing heap usage prevents exceptions and improves performance. This pattern is critical for batch processing, reporting, and data transformation scenarios.

**Example scenario**: Instead of querying all 50,000 Contacts into a List and processing in memory, use Batch Apex to process in chunks of 200, or use a cursor-based approach to process records one batch at a time without storing all results.

## Interactions With Existing RAG

**Connection to `rag/development/apex-patterns.md`**:
- The RAG file mentions governor limits and optimization (SOQL optimization, bulkification, monitoring limits) but focuses on implementation patterns. This document adds comprehensive guidance on specific governor limit types, limit values, query selectivity rules, and advanced optimization techniques.

**Connection to `rag/patterns/cross-cutting-patterns.md`**:
- The RAG file mentions governor limit management as a cross-cutting pattern and links to domain-specific documentation. This document adds detailed guidance on limit monitoring, proactive checking, and optimization strategies that complement the pattern summary.

**Connection to `rag/integrations/sis-sync-patterns.md`**:
- The RAG file describes high-volume batch synchronization patterns but focuses on integration-specific patterns. This document adds broader governor limit guidance that applies to all high-volume scenarios, not just SIS syncs.

**Gaps filled by this document**:
- The RAG files mention governor limits but don't provide comprehensive guidance on specific limit types and values, query selectivity rules, heap size optimization, or limit monitoring patterns. This document adds detailed guidance on these topics that are essential for performance optimization.

**Nuances added**:
- This document emphasizes query selectivity rules (10% threshold, indexed fields), specific governor limit values, heap size optimization patterns, and proactive limit monitoring that complement the RAG files' focus on bulkification and asynchronous patterns.

## Tradeoffs and Controversies

**Query selectivity threshold**: The 10% selectivity threshold is a guideline, not a hard rule. Some queries returning more than 10% may still perform well if they use indexes efficiently. The tradeoff is between strict adherence (may require complex WHERE clauses) and practical performance (some queries may work fine above 10%). The consensus is to aim for <10% but test actual performance.

**Batch size optimization**: Optimal batch sizes vary by use case. Smaller batches (100-200) are safer but slower. Larger batches (up to 2,000) are faster but risk hitting limits. The tradeoff is between safety (smaller batches) and performance (larger batches). The consensus is to start with 200 and adjust based on monitoring.

**Asynchronous vs synchronous**: Some operations can be done synchronously (faster, simpler) or asynchronously (avoids limits, more complex). The tradeoff is between simplicity (synchronous) and scalability (asynchronous). The consensus is to use asynchronous for operations that exceed limits or process large volumes.

**Limit monitoring overhead**: Proactive limit checking adds code complexity and slight performance overhead. The tradeoff is between safety (checking limits) and simplicity (assuming limits won't be hit). The consensus is to check limits for expensive operations but not for every simple operation.

**Heap size vs query count**: Sometimes you can reduce query count by loading more data into memory, but this increases heap usage. The tradeoff is between query efficiency (fewer queries) and memory efficiency (less heap). The consensus is to balance both, preferring fewer queries when heap allows, but paginating when heap becomes a concern.

These tradeoffs require human judgment based on specific use cases, data volumes, and performance requirements.

## Sources Used

- Salesforce Developer Documentation: Apex Governor Limits
- Salesforce Developer Documentation: SOQL and SOSL Reference
- Salesforce Developer Documentation: Query Optimization
- Trailhead: Apex Basics & Database module
- Trailhead: Asynchronous Apex module
- Trailhead: Large Data Volumes module
- Official Salesforce Blogs: Performance Best Practices
- Salesforce Stack Exchange: Governor limits and optimization discussions
- "Advanced Apex Programming" by Dan Appleman (conceptual references on governor limits)

## To Evaluate

- **Query selectivity threshold**: While 10% is widely cited, actual performance depends on many factors (index usage, data distribution, query complexity). The optimal threshold may vary by object and query pattern.

- **Batch size optimization**: Optimal batch sizes depend on record complexity, DML operations per record, and system load. The decision requires evaluation based on monitoring and testing.

- **Limit monitoring frequency**: The frequency of limit checking (every operation vs. only expensive operations) requires evaluation based on performance impact and code complexity.

- **Heap size optimization strategies**: The balance between query efficiency and heap usage requires evaluation based on data volumes, record complexity, and available memory.

## Q&A

### Q: What are the most important governor limits to monitor?

**A**: Monitor **SOQL queries** (100 synchronous, 200 async), **DML statements** (150 synchronous, 200 async), **CPU time** (10,000ms synchronous, 60,000ms async), **heap size** (6MB synchronous, 12MB async), and **callouts** (100 synchronous, unlimited async). Use `Limits` class methods to check current usage.

### Q: How do I make SOQL queries selective?

**A**: Use **indexed fields** in WHERE clauses (e.g., Id, Name, Email, Status, Type), ensure queries return less than 10% of records, use selective criteria (e.g., Status = 'Active'), and avoid formula fields in WHERE clauses. Selective queries use indexes and perform much better.

### Q: What is the difference between bulkification and optimization?

**A**: **Bulkification** ensures code handles collections of records (avoids loops with DML/SOQL). **Optimization** improves performance and reduces resource usage (selective queries, efficient algorithms). Both are important: bulkification prevents limit exceptions, optimization improves performance.

### Q: How do I handle governor limit exceptions gracefully?

**A**: Implement proactive limit checking using `Limits` class methods, implement graceful degradation when approaching limits, use async processing for large operations, batch operations to stay within limits, and log limit usage for monitoring. Handle exceptions with appropriate error messages.

### Q: When should I use Batch Apex vs standard DML?

**A**: Use **Batch Apex** for processing thousands or millions of records, operations that exceed synchronous limits, or when you need separate transaction contexts. Use **standard DML** for smaller operations (hundreds of records) that fit within synchronous limits.

### Q: What is query selectivity and why does it matter?

**A**: **Query selectivity** refers to how selective a query is (how many records it returns relative to total records). Queries returning more than 10% of records may be non-selective and cause performance issues. Use indexed fields and selective criteria to ensure queries are selective.

### Q: How do I optimize heap size usage?

**A**: Avoid storing large collections in memory, use streaming patterns for large datasets, release object references when no longer needed, process data in batches, use efficient data structures, and avoid unnecessary object creation. Monitor heap usage with `Limits.getHeapSize()`.

### Q: What are the governor limits for async Apex?

**A**: Async Apex (Batch, Queueable, Scheduled) has **higher limits** than synchronous: 200 SOQL queries, 200 DML statements, 60,000ms CPU time, 12MB heap size. However, there are limits on concurrent jobs (50 batch jobs, 50,000 Queueable jobs per 24 hours).

## Edge Cases and Limitations

### Large Data Volume Scenarios

- **Non-selective queries**: Queries returning >10% of records may be non-selective
- **Heap size limits**: Large collections can exceed heap size limits
- **Batch job limits**: 50 concurrent batch jobs, 250,000 batch executions per 24 hours
- **Query timeout**: Very large queries may timeout

### Performance Considerations

- **Index usage**: Queries must use indexed fields for optimal performance
- **Query complexity**: Complex queries with many joins may be slow
- **Data skew**: Uneven data distribution can impact query performance
- **Concurrent operations**: High concurrency can cause contention and performance issues

## Related Patterns

- [SOQL Query Patterns](soql-query-patterns.md) - Query optimization and selectivity
- [Asynchronous Apex Patterns](asynchronous-apex-patterns.md) - Batch, Queueable, and Scheduled Apex for large operations
- [Large Data Loads](large-data-loads.md) - Bulk API and data load optimization
- [Locking and Concurrency Strategies](locking-and-concurrency-strategies.md) - Concurrency and resource management
- [Error Handling and Logging](error-handling-and-logging.md) - Error handling for limit exceptions
- [Apex Patterns](apex-patterns.md) - Bulkification and optimization patterns

