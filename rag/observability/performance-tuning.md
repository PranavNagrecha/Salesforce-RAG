---
title: "Performance Tuning for Salesforce"
level: "Advanced"
tags:
  - observability
  - performance
  - optimization
  - ldv
last_reviewed: "2025-01-XX"
---

# Performance Tuning for Salesforce

## Overview

This guide covers performance tuning patterns for Salesforce, including query/selectivity tuning, Large Data Volume (LDV) handling, governor limit mitigation, and caching strategies. These patterns are essential for optimizing Salesforce performance, handling large datasets, and ensuring system scalability.

**Related Patterns**:
- <a href="{{ '/rag/development/governor-limits-and-optimization.html' | relative_url }}">Governor Limits and Optimization</a> - Governor limits and resource management
- <a href="{{ '/rag/development/soql-query-patterns.html' | relative_url }}">SOQL Query Patterns</a> - SOQL query best practices
- <a href="{{ '/rag/observability/monitoring-alerting.html' | relative_url }}">Monitoring and Alerting</a> - Performance monitoring patterns

## Consensus Best Practices

- **Optimize queries for selectivity**: Use indexed fields and ensure queries return less than 10% of records
- **Plan for Large Data Volumes**: Design data models and queries with LDV in mind from the start
- **Monitor governor limit usage**: Proactively monitor and optimize limit usage
- **Implement caching strategically**: Use Platform Cache for frequently accessed, rarely changing data
- **Profile and measure**: Always measure performance before and after optimization
- **Test with production-like data volumes**: Test performance with realistic data volumes
- **Optimize iteratively**: Make incremental optimizations and measure impact
- **Document performance baselines**: Establish and maintain performance baselines

## Query/Selectivity Tuning

### Indexed Field Patterns

**Standard Indexed Fields**:
- **Id**: Always indexed, most selective
- **Name**: Indexed on most objects
- **Email**: Indexed on Contact and User
- **External ID fields**: Custom indexed fields
- **Lookup fields**: Indexed for relationship queries
- **Date fields**: Indexed for date range queries
- **Unique fields**: Automatically indexed

**Custom Indexed Fields**:
- Create custom indexes for frequently queried fields
- Use compound indexes for multi-field queries
- Request Salesforce support for additional indexes if needed
- Document indexed fields and query patterns

**Index Usage Best Practices**:
- Always use indexed fields in WHERE clauses
- Combine multiple indexed fields for better selectivity
- Avoid functions on indexed fields (e.g., `UPPER(Email)`)
- Use date ranges with indexed date fields

### Selective Query Optimization

**Selectivity Threshold**:
- Queries should return less than 10% of records
- Non-selective queries may be blocked in production
- Combine indexed fields to improve selectivity
- Use date filters to improve selectivity

**Selectivity Patterns**:
- **Single field**: Use highly selective indexed field
- **Multiple fields**: Combine indexed fields with AND
- **Date ranges**: Use indexed date fields with ranges
- **External IDs**: Use external ID fields for lookups

**Selectivity Analysis**:
- Use Query Plan tool in Developer Console
- Analyze query execution plans
- Identify non-selective queries
- Optimize queries based on plan analysis

### Query Plan Analysis

**Query Plan Tool**:
- Access via Developer Console or VS Code
- Shows index usage and selectivity
- Identifies full table scans
- Suggests optimization opportunities

**Query Plan Interpretation**:
- **Index**: Query uses index (optimal)
- **Table Scan**: Full table scan (non-optimal)
- **Cardinality**: Number of rows examined
- **Selectivity**: Percentage of records returned

**Optimization Based on Plan**:
- Add indexed fields to WHERE clause
- Refine date ranges for better selectivity
- Combine multiple indexed fields
- Consider custom indexes for frequent queries

## Large Data Volumes (LDV)

### LDV Handling Strategies

**LDV Definition**:
- Typically 1 million+ records per object
- Varies by object type and query patterns
- Consider query volume, not just record count
- Plan for growth over time

**LDV Design Principles**:
- Design data model for LDV from start
- Use indexed fields for all queries
- Implement data archiving strategies
- Plan for query optimization

### Data Archiving Patterns

**Archiving Strategies**:
- **Soft delete**: Mark records as archived, filter in queries
- **Separate archive object**: Move old records to archive object
- **External archive**: Export to external system
- **Data deletion**: Delete truly obsolete data

**Archiving Implementation**:
- Use Batch Apex for large archiving operations
- Schedule archiving during low-usage periods
- Maintain referential integrity during archiving
- Document archiving procedures

**Archiving Considerations**:
- Compliance and retention requirements
- Data access patterns (how often is old data accessed?)
- Recovery procedures if archived data needed
- Integration with external systems

### LDV Query Optimization

**Query Optimization for LDV**:
- Always use indexed fields
- Ensure queries are selective (<10% of records)
- Use date ranges to limit result sets
- Implement pagination for large result sets

**LDV-Specific Patterns**:
- **Date-based partitioning**: Use date fields to partition data
- **External ID lookups**: Use external IDs for efficient lookups
- **Aggregate queries**: Use aggregate queries instead of retrieving all records
- **Batch processing**: Process large datasets in batches

**LDV Monitoring**:
- Monitor query performance in LDV orgs
- Track query execution times
- Identify slow queries
- Optimize based on monitoring data

## Governor Limit Mitigation

### Proactive Limit Monitoring

**Limit Monitoring Patterns**:
- Use `Limits` class to check current usage
- Monitor limit usage in production
- Set thresholds for limit warnings
- Alert on approaching limits

**Limit Monitoring Implementation**:
- Log limit usage in production
- Track limit usage trends
- Identify limit-heavy operations
- Optimize based on monitoring data

### Limit Avoidance Patterns

**Query Limit Avoidance**:
- Minimize number of SOQL queries
- Use relationship queries to combine data
- Use aggregate queries for counts
- Cache query results when appropriate

**DML Limit Avoidance**:
- Bulkify all DML operations
- Process records in collections
- Avoid DML in loops
- Use Bulk API for large operations

**CPU Time Limit Avoidance**:
- Optimize algorithm complexity
- Use efficient data structures
- Cache expensive calculations
- Move complex logic to async processing

### Limit Optimization

**Optimization Strategies**:
- **Combine operations**: Reduce number of operations
- **Cache results**: Avoid redundant operations
- **Async processing**: Move to async for large operations
- **Bulk operations**: Process in bulk instead of individually

**Optimization Examples**:
- Combine multiple queries into relationship queries
- Use aggregate queries instead of retrieving all records
- Cache frequently accessed data
- Use Batch Apex for large operations

## Caching Strategies

### Platform Cache Patterns

**Platform Cache Types**:
- **Org Cache**: Shared across all users in org
- **Session Cache**: Per-user session cache
- **Partition Cache**: Named partitions for organization

**Cache Usage Patterns**:
- Cache frequently accessed, rarely changing data
- Cache expensive calculations
- Cache external API responses
- Cache query results for read-heavy scenarios

**Cache Best Practices**:
- Set appropriate TTL (Time To Live)
- Handle cache misses gracefully
- Invalidate cache on data changes
- Monitor cache hit rates

### Custom Caching Implementments

**Custom Cache Patterns**:
- Use Custom Settings for configuration cache
- Use Custom Metadata for metadata cache
- Use static variables for request-scoped cache
- Use Platform Cache for cross-request cache

**Custom Cache Implementation**:
- Implement cache wrapper classes
- Handle cache invalidation
- Monitor cache performance
- Document cache usage

### Cache Invalidation

**Invalidation Strategies**:
- **Time-based**: Invalidate after TTL expires
- **Event-based**: Invalidate on data changes
- **Manual**: Invalidate on demand
- **Version-based**: Invalidate on version changes

**Invalidation Patterns**:
- Invalidate on DML operations
- Invalidate on configuration changes
- Invalidate on external system updates
- Document invalidation triggers

**Invalidation Best Practices**:
- Invalidate related cache entries
- Handle cache invalidation gracefully
- Monitor invalidation patterns
- Optimize invalidation frequency

## Performance Monitoring

### Performance Metrics

**Key Performance Metrics**:
- Query execution time
- Page load time
- API response time
- Transaction processing time
- Governor limit usage

**Performance Baselines**:
- Establish performance baselines
- Track performance trends
- Set performance targets
- Alert on performance degradation

### Performance Testing

**Testing Strategies**:
- Load testing with realistic data volumes
- Stress testing to find limits
- Performance testing in production-like environments
- Continuous performance monitoring

**Testing Tools**:
- Salesforce Performance Testing tools
- External load testing tools
- Custom performance test scripts
- Production monitoring

## Q&A

### Q: How do I optimize SOQL queries for performance?

**A**: Optimize SOQL queries by: (1) **Using indexed fields** in WHERE clauses (Id, Name, Email, External IDs, Lookup fields, Date fields), (2) **Ensuring selectivity** (queries return less than 10% of records), (3) **Using selective filters** (multiple indexed fields), (4) **Limiting fields** (select only needed fields), (5) **Using LIMIT clause** when possible, (6) **Avoiding functions** in WHERE clauses (prevents index usage).

### Q: What is query selectivity and why is it important?

**A**: **Query selectivity** is the percentage of records returned by a query. Queries should return **less than 10% of records** to be considered selective and use indexes efficiently. Non-selective queries (returning >10% of records) can't use indexes and perform full table scans, causing performance issues. Use indexed fields and multiple filters to improve selectivity.

### Q: How do I handle Large Data Volumes (LDV) in Salesforce?

**A**: Handle LDV by: (1) **Designing data models** with LDV in mind from the start, (2) **Using indexed fields** for queries, (3) **Implementing data archiving** strategies, (4) **Using Batch Apex** for large data processing, (5) **Optimizing queries** for selectivity, (6) **Using Platform Cache** for frequently accessed data, (7) **Monitoring query performance** regularly.

### Q: How do I mitigate governor limit issues?

**A**: Mitigate governor limits by: (1) **Bulkifying all code** (no DML/SOQL in loops), (2) **Using async processing** (Batch, Queueable, @future) for long-running operations, (3) **Optimizing queries** (reduce query count, improve selectivity), (4) **Using Platform Cache** to reduce query load, (5) **Monitoring limit usage** proactively, (6) **Breaking work into chunks** for large datasets.

### Q: When should I use Platform Cache?

**A**: Use Platform Cache for: (1) **Frequently accessed data** (read many times), (2) **Rarely changing data** (doesn't change often), (3) **Expensive to query** (complex queries, large datasets), (4) **Shared across users** (same data for multiple users), (5) **Not time-sensitive** (slight staleness acceptable). Don't cache frequently changing or user-specific data.

### Q: How do I measure performance improvements?

**A**: Measure performance by: (1) **Establishing baselines** (measure current performance), (2) **Profiling code** (identify bottlenecks), (3) **Measuring before and after** optimizations, (4) **Tracking metrics** (response times, query performance, governor limit usage), (5) **Using performance monitoring tools**, (6) **Testing with production-like data volumes**, (7) **Documenting performance improvements**.

### Q: What are best practices for performance tuning?

**A**: Best practices include: (1) **Optimize queries for selectivity** (use indexed fields, <10% of records), (2) **Plan for LDV** from the start, (3) **Monitor governor limit usage** proactively, (4) **Implement caching strategically** (Platform Cache for appropriate data), (5) **Profile and measure** (always measure before/after), (6) **Test with production-like data**, (7) **Optimize iteratively** (incremental improvements), (8) **Document performance baselines**.

### Q: How do I optimize queries that can't use indexes?

**A**: Optimize non-indexed queries by: (1) **Adding custom indexes** for frequently queried fields, (2) **Requesting Salesforce support** for additional indexes if needed, (3) **Restructuring queries** to use indexed fields, (4) **Using compound indexes** for multi-field queries, (5) **Reducing data volume** (archiving old data), (6) **Using Batch Apex** for large data processing, (7) **Caching query results** when appropriate.

### Q: What is the difference between Platform Cache and database queries?

**A**: **Platform Cache** stores data in memory for fast access (milliseconds), while **database queries** read from database (hundreds of milliseconds). Use cache for frequently accessed, rarely changing data. Cache has size limits and TTL (Time To Live), while database queries always return current data. Balance cache benefits with data freshness requirements.

### Q: How do I test performance with Large Data Volumes?

**A**: Test LDV performance by: (1) **Creating test data** that matches production volumes, (2) **Testing queries** with large datasets, (3) **Monitoring query performance** (response times, selectivity), (4) **Testing governor limit usage** (ensure no limit violations), (5) **Profiling code** to identify bottlenecks, (6) **Testing with realistic scenarios** (production-like usage patterns), (7) **Documenting performance characteristics**.

## Related Patterns

- <a href="{{ '/rag/development/governor-limits-and-optimization.html' | relative_url }}">Governor Limits and Optimization</a> - Governor limits and resource management
- <a href="{{ '/rag/development/soql-query-patterns.html' | relative_url }}">SOQL Query Patterns</a> - SOQL query best practices
- <a href="{{ '/rag/observability/monitoring-alerting.html' | relative_url }}">Monitoring and Alerting</a> - Performance monitoring
- <a href="{{ '/rag/development/asynchronous-apex-patterns.html' | relative_url }}">Asynchronous Apex Patterns</a> - Async processing for performance

