---
layout: default
title: Performance Tuning for Salesforce
description: This guide covers performance tuning patterns for Salesforce, including query/selectivity tuning, Large Data Volume (LDV) handling, governor limit mitigation, and caching strategies
permalink: /rag/observability/performance-tuning.html
level: Advanced
tags:
  - observability
  - performance
  - optimization
  - ldv
  - caching
last_reviewed: 2025-12-03
---

# Performance Tuning for Salesforce

## Overview

Performance tuning patterns optimize Salesforce org performance for large data volumes, complex queries, and high user concurrency. This guide covers query optimization, LDV handling, governor limit mitigation, and caching strategies.

**Core Principle**: Optimize for performance proactively through selective queries, efficient data access patterns, caching, and async processing. Performance is a feature, not an afterthought.

## Prerequisites

**Required Knowledge**:
- Understanding of Salesforce governor limits
- Familiarity with SOQL query optimization
- Knowledge of Large Data Volume (LDV) patterns
- Understanding of caching strategies
- Knowledge of async processing patterns

**Recommended Reading**:
- <a href="{{ '/rag/development/governor-limits-and-optimization.html' | relative_url }}">Governor Limits and Optimization</a> - Governor limit patterns
- <a href="{{ '/rag/development/soql-query-patterns.html' | relative_url }}">SOQL Query Patterns</a> - Query optimization patterns
- <a href="{{ '/rag/development/asynchronous-apex-patterns.html' | relative_url }}">Asynchronous Apex Patterns</a> - Async processing patterns

## When to Use Performance Tuning

### Use Performance Tuning When

- **Large data volumes**: Org has millions of records
- **Performance issues**: Experiencing slow page loads or timeouts
- **Governor limit violations**: Hitting governor limits frequently
- **High concurrency**: Many concurrent users
- **Complex queries**: Complex SOQL queries taking too long
- **Integration performance**: Integrations are slow

### Avoid Performance Tuning When

- **Small orgs**: Small data volumes, no performance issues
- **Premature optimization**: Optimizing before identifying issues
- **Limited resources**: Don't have resources for optimization
- **Simple use cases**: Basic functionality, no performance concerns

## Query Optimization Patterns

### Pattern 1: Selective Query Optimization

**Purpose**: Optimize queries to be selective (return <10% of records).

**Implementation**:
- **Indexed Fields**: Use indexed fields in WHERE clauses
- **Selective Filters**: Use filters that return <10% of records
- **Query Plan**: Use Query Plan to verify selectivity
- **Composite Indexes**: Use composite indexes for multi-field filters

**Best Practices**:
- Use indexed fields (Id, Name, Email, External IDs, etc.)
- Avoid functions on indexed fields (UPPER, LOWER, etc.)
- Use selective filters
- Verify selectivity with Query Plan
- Create custom indexes for common queries

### Pattern 2: Query Result Optimization

**Purpose**: Minimize data retrieved by queries.

**Implementation**:
- **Field Selection**: Select only needed fields
- **Limit Clauses**: Use LIMIT to restrict results
- **Pagination**: Implement pagination for large result sets
- **Relationship Queries**: Use relationship queries to avoid multiple queries

**Best Practices**:
- Select only needed fields
- Use LIMIT clauses
- Implement pagination
- Use relationship queries
- Avoid SELECT * (select all fields)

### Pattern 3: Query Bulkification

**Purpose**: Design queries to handle bulk operations efficiently.

**Implementation**:
- **Bulk Queries**: Query collections, not single records
- **Bulk DML**: Use bulk DML operations
- **Avoid Loops**: Avoid queries in loops
- **Collection Processing**: Process collections efficiently

**Best Practices**:
- Query collections
- Use bulk DML
- Avoid queries in loops
- Process collections efficiently
- Test with 200+ records

## Large Data Volume (LDV) Patterns

### Pattern 1: LDV Query Optimization

**Purpose**: Optimize queries for large data volumes.

**Implementation**:
- **Selective Queries**: Ensure queries are selective
- **Indexed Fields**: Use indexed fields
- **Date Range Filters**: Use date range filters
- **Pagination**: Implement pagination
- **Async Processing**: Use async processing for large datasets

**Best Practices**:
- Ensure selectivity
- Use indexed fields
- Use date ranges
- Implement pagination
- Use async processing

### Pattern 2: LDV Data Access Patterns

**Purpose**: Optimize data access for large volumes.

**Implementation**:
- **Batch Processing**: Process data in batches
- **Incremental Processing**: Process only changed records
- **Data Archiving**: Archive old data
- **Data Partitioning**: Partition data by date or category

**Best Practices**:
- Process in batches
- Process incrementally
- Archive old data
- Partition data
- Monitor data growth

### Pattern 3: LDV Reporting Optimization

**Purpose**: Optimize reports for large data volumes.

**Implementation**:
- **Report Filters**: Use selective report filters
- **Summary Reports**: Use summary reports when possible
- **Scheduled Reports**: Schedule reports for off-peak times
- **Report Caching**: Use report caching

**Best Practices**:
- Use selective filters
- Use summary reports
- Schedule reports
- Use report caching
- Optimize report formulas

## Caching Strategies

### Pattern 1: Platform Cache

**Purpose**: Use Platform Cache to reduce query load.

**Implementation**:
- **Session Cache**: Cache user-specific data
- **Org Cache**: Cache org-wide data
- **Cache Keys**: Use descriptive cache keys
- **Cache TTL**: Set appropriate time-to-live (TTL)

**Example**:
```apex
public class CacheService {
    public static Object getCachedData(String key) {
        Cache.OrgPartition orgPartition = Cache.Org.getPartition('local.Default');
        return orgPartition.get(key);
    }
    
    public static void setCachedData(String key, Object data, Integer ttlSeconds) {
        Cache.OrgPartition orgPartition = Cache.Org.getPartition('local.Default');
        orgPartition.put(key, data, ttlSeconds);
    }
}
```

**Best Practices**:
- Cache frequently accessed data
- Use appropriate cache partitions
- Set TTL appropriately
- Handle cache misses
- Monitor cache usage

### Pattern 2: Custom Settings Cache

**Purpose**: Use Custom Settings for configuration caching.

**Implementation**:
- **Hierarchy Custom Settings**: For user-specific configuration
- **List Custom Settings**: For org-wide configuration
- **Access Patterns**: Access Custom Settings directly (cached by platform)

**Best Practices**:
- Use Custom Settings for configuration
- Access directly (no queries needed)
- Use hierarchy for user-specific
- Use list for org-wide
- Update via metadata deployment

### Pattern 3: Custom Metadata Cache

**Purpose**: Use Custom Metadata for package-deployable configuration.

**Implementation**:
- **Custom Metadata Types**: Define Custom Metadata Types
- **Metadata Records**: Create metadata records
- **Access Patterns**: Access via SOQL (cached by platform)

**Best Practices**:
- Use Custom Metadata for configuration
- Access via SOQL (cached)
- Package-deployable
- Update via metadata deployment
- Use for feature flags

## Governor Limit Mitigation

### Pattern 1: Async Processing

**Purpose**: Move processing to async to avoid governor limits.

**Implementation**:
- **Queueable Apex**: For lightweight async processing
- **Batch Apex**: For large dataset processing
- **Scheduled Apex**: For time-based processing
- **Platform Events**: For event-driven async processing

**Best Practices**:
- Use async for long-running operations
- Use Batch for large datasets
- Use Queueable for lightweight async
- Use Scheduled for time-based
- Monitor async job execution

### Pattern 2: Governor Limit Monitoring

**Purpose**: Monitor governor limit usage proactively.

**Implementation**:
- **Limit Tracking**: Track limit usage
- **Limit Monitoring**: Monitor approaching limits
- **Alerting**: Alert when approaching limits
- **Optimization**: Optimize when limits approached

**Best Practices**:
- Track limit usage
- Monitor proactively
- Alert on high usage
- Optimize before limits
- Create limit dashboards

### Pattern 3: Resource Optimization

**Purpose**: Optimize resource usage to stay within limits.

**Implementation**:
- **Query Optimization**: Reduce query count
- **DML Optimization**: Reduce DML operations
- **CPU Optimization**: Optimize CPU usage
- **Heap Optimization**: Optimize heap usage

**Best Practices**:
- Reduce query count
- Reduce DML operations
- Optimize CPU usage
- Optimize heap usage
- Monitor resource usage

## Related Patterns

- <a href="{{ '/rag/development/governor-limits-and-optimization.html' | relative_url }}">Governor Limits and Optimization</a> - Governor limit patterns and optimization
- <a href="{{ '/rag/development/soql-query-patterns.html' | relative_url }}">SOQL Query Patterns</a> - Query optimization patterns
- <a href="{{ '/rag/development/asynchronous-apex-patterns.html' | relative_url }}">Asynchronous Apex Patterns</a> - Async processing patterns
- <a href="{{ '/rag/observability/monitoring-alerting.html' | relative_url }}">Monitoring and Alerting</a> - Performance monitoring

## Q&A

### Q: What are performance tuning patterns for Salesforce?

**A**: **Performance tuning patterns** optimize: (1) **Query performance** (selective queries, indexed fields), (2) **LDV handling** (large data volume optimization), (3) **Governor limit mitigation** (async processing, resource optimization), (4) **Caching strategies** (Platform Cache, Custom Settings), (5) **Data access patterns** (efficient data retrieval). Performance tuning ensures orgs perform well at scale.

### Q: How do I optimize SOQL queries for performance?

**A**: Optimize by: (1) **Use indexed fields** (Id, Name, Email, External IDs), (2) **Ensure selectivity** (queries return <10% of records), (3) **Select only needed fields** (avoid SELECT *), (4) **Use LIMIT clauses** (restrict result sets), (5) **Use Query Plan** (verify selectivity), (6) **Avoid functions on indexed fields** (UPPER, LOWER break indexes). Query optimization is critical for performance.

### Q: How do I handle Large Data Volumes (LDV)?

**A**: Handle LDV by: (1) **Optimize queries** (selective, indexed), (2) **Batch processing** (process in batches), (3) **Incremental processing** (process only changed records), (4) **Data archiving** (archive old data), (5) **Data partitioning** (partition by date/category), (6) **Async processing** (use Batch/Queueable). LDV requires careful optimization.

### Q: How do I use Platform Cache for performance?

**A**: Use Platform Cache by: (1) **Cache frequently accessed data** (reduce query load), (2) **Use appropriate partitions** (session vs org cache), (3) **Set TTL appropriately** (time-to-live), (4) **Handle cache misses** (fallback to queries), (5) **Monitor cache usage** (track cache hit rates). Platform Cache reduces query load and improves performance.

### Q: How do I mitigate governor limit violations?

**A**: Mitigate by: (1) **Async processing** (move to Batch/Queueable), (2) **Query optimization** (reduce query count), (3) **DML optimization** (reduce DML operations), (4) **Resource optimization** (optimize CPU/heap), (5) **Limit monitoring** (monitor limit usage), (6) **Alerting** (alert when approaching limits). Governor limit mitigation requires optimization and monitoring.

### Q: What are caching strategies for Salesforce?

**A**: Caching strategies: (1) **Platform Cache** (session/org cache for frequently accessed data), (2) **Custom Settings** (configuration caching, no queries), (3) **Custom Metadata** (package-deployable configuration, cached), (4) **Report Caching** (cache report results), (5) **LWC Caching** (cache component data). Caching reduces query load and improves performance.

### Q: How do I monitor performance?

**A**: Monitor by: (1) **Track query performance** (monitor query execution time), (2) **Monitor governor limits** (track limit usage), (3) **Track page load times** (monitor user experience), (4) **Create performance dashboards** (visualize performance metrics), (5) **Alert on degradation** (alert when performance degrades). Performance monitoring enables proactive optimization.
