# Performance Tuning for Salesforce

## Overview

This guide covers performance tuning patterns for Salesforce, including query/selectivity tuning, Large Data Volume (LDV) handling, governor limit mitigation, and caching strategies. These patterns are essential for optimizing Salesforce performance, handling large datasets, and ensuring system scalability.

**Related Patterns**:
- [Governor Limits and Optimization](rag/development/governor-limits-and-optimization.md) - Governor limits and resource management
- [SOQL Query Patterns](rag/development/soql-query-patterns.md) - SOQL query best practices
- [Monitoring and Alerting](rag/observability/monitoring-alerting.md) - Performance monitoring patterns

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

## Related Patterns

- [Governor Limits and Optimization](rag/development/governor-limits-and-optimization.md) - Governor limits and resource management
- [SOQL Query Patterns](rag/development/soql-query-patterns.md) - SOQL query best practices
- [Monitoring and Alerting](rag/observability/monitoring-alerting.md) - Performance monitoring
- [Asynchronous Apex Patterns](rag/development/asynchronous-apex-patterns.md) - Async processing for performance

