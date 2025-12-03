---
title: "SIS Synchronization Patterns"
level: "Advanced"
tags:
  - integrations
  - etl
  - sis
  - education-cloud
  - batch-processing
  - high-volume
last_reviewed: "2025-01-XX"
---

# SIS Synchronization Patterns

## Overview

High-volume batch synchronization patterns for integrating Salesforce Education Cloud with legacy Student Information Systems (SIS). These patterns handle hundreds of thousands of student records daily through ETL platforms with file-based staging and dynamic SQL batching.

## Prerequisites

**Required Knowledge**:
- Understanding of ETL platforms (Dell Boomi, MuleSoft) and their capabilities
- Knowledge of high-volume batch processing patterns
- Familiarity with External IDs and composite key strategies
- Understanding of Bulk API and asynchronous job processing
- Knowledge of SQL batching and IN-clause query patterns
- Experience with error handling and retry logic for integrations

**Recommended Reading**:
- `rag/integrations/integration-platform-patterns.md` - ETL platform patterns
- `rag/data-modeling/external-ids-and-integration-keys.md` - External ID strategies
- `rag/integrations/etl-vs-api-vs-events.md` - Integration pattern selection
- `rag/data-modeling/data-migration-patterns.md` - Data migration strategies
- `rag/development/asynchronous-apex-patterns.md` - Asynchronous processing patterns

## Integration Architecture

### Source System

**Oracle-based Student Information System (SIS)**:

- Legacy SIS with Oracle database backend
- Primary student system of record
- Contains student identifiers (EMPLIDs), academic records, enrollment data
- Requires batch-oriented integration approach

### Target System

**Salesforce Education Cloud**:

- Education Cloud (EDA) data model
- Contacts as primary student records
- Program Enrollment and Course Enrollment objects
- Application objects for application tracking

### Integration Platform

**Dell Boomi ETL Platform**:

- Primary ETL platform for high-volume batch integrations
- Handles data transformation and routing
- Manages file-based staging for large data sets
- Supports dynamic SQL IN-clause batching

## High-Volume Batch Pattern

### Volume Characteristics

**Scale**: 300,000+ student records (EMPLIDs) synchronized daily

**Requirements**:
- Chunking strategies for large data sets
- Robust retry/error handling
- Careful management of API limits
- File-based staging for very large ID lists

### File-Based Staging Pattern

**Pattern**: Large ID lists written to disk, then processed in batches

**Implementation**:
1. Salesforce sends large lists of IDs (e.g., EMPLIDs) to Boomi
2. Boomi writes ID lists to disk as files
3. Boomi reads files back and dynamically splits into batched SQL IN-clause queries
4. Oracle database processes queries in manageable chunks (1,000 IDs per IN clause)
5. Results returned in structured payloads back to Salesforce

**When to use**: ID lists exceeding 50,000 records

**Benefits**:
- Handles very large data sets
- Reduces memory usage
- Enables efficient database querying
- Supports retry operations

### Dynamic SQL IN-Clause Batching

**Pattern**: ID lists split into batched SQL IN-clause queries

**Implementation**:
- Dynamically split large ID lists into SQL IN-clause batches
- Typically 1,000 IDs per IN clause
- Use parameterized queries to prevent SQL injection
- Handle Oracle-specific data types and formats correctly
- Implement connection pooling to manage database connections efficiently

**Benefits**:
- Works within database query size limits
- Maintains performance
- Enables efficient processing
- Supports large data volumes

## Data Synchronization Strategy

### Idempotent Upserts

**Pattern**: Use External IDs for upsert operations

**Implementation**:
- External IDs mirror SIS primary keys (EMPLID) for stable record mapping
- Use upsert operations with External IDs to enable idempotent synchronization
- Support retry logic for failed operations
- Enable partial syncs without data loss

**Benefits**:
- Safe retry of failed operations
- Prevents duplicate records
- Enables reconciliation between systems
- Supports incremental synchronization

### Composite External IDs

**Pattern**: Account-level external IDs using composite keys

**Implementation**:
- Composite external IDs for objects where external systems use multi-column primary keys
- Example: Institution + Program + Effective Date
- Concatenate component fields with delimiter (pipe `|` or dash `-`)
- Ensure delimiter doesn't appear in component field values
- Handle null values in component fields appropriately

**Benefits**:
- Supports complex external system keys
- Enables stable record mapping
- Handles time-versioned records
- Maintains data integrity

### Integration Job Tracking

**Pattern**: Standard fields on all integrated objects

**Fields**:
- `Last_Sync_Timestamp__c` (DateTime) - when record was last synced
- `Last_Sync_Status__c` (Picklist: Success, Error, In Progress) - sync job status
- `Last_Sync_Error__c` (Long Text Area) - error message if sync failed
- `Integration_Job_ID__c` (Text) - correlation ID with external system
- `Record_Source__c` (Picklist: Integration, Manual Entry, Migration) - how record was created

**Usage**:
- Troubleshoot integration failures
- Identify records that haven't synced recently
- Correlate Salesforce records with external system job logs
- Build dashboards showing integration health
- Audit data changes and integration activity

## Data Transformation

### SIS to Salesforce Mapping

**Mapping**:
- SIS student identifiers (EMPLID) → Contact External ID
- SIS academic records → Program Enrollment objects
- SIS enrollment data → Course Enrollment objects
- SIS application data → Application objects

### Data Type Conversions

**Handling**:
- Dates: Handle SIS date formats and timezone conversions
- Numbers: Handle decimal precision and formatting
- Text: Handle encoding, special characters, and length limits
- Null values: Transform null values appropriately (empty strings vs. null)

### Data Validation

**Validation**:
- Apply data validation rules before sending to Salesforce
- Handle data inconsistencies from legacy systems
- Validate external IDs before upsert operations
- Check required fields and data formats

## Error Handling and Retry Logic

### Error Capture

**Pattern**: Error capture at each step of the process

**Implementation**:
- Capture error details at each step
- Log errors to centralized logging system
- Track which records failed and why
- Support error reporting and analysis

### Retry Logic

**Pattern**: Retry logic with exponential backoff

**Implementation**:
- Retry transient failures automatically
- Use exponential backoff for retries
- Track retry attempts
- Escalate persistent failures
- Support manual retry for failed records

### Dead-Letter Queues

**Pattern**: Dead-letter queues for records that cannot be processed

**Implementation**:
- Store unprocessable records for manual review
- Enable manual correction and reprocessing
- Track error patterns for system improvements
- Support data quality improvements

## Performance Optimization

### Chunking Strategy

**Pattern**: Break large data sets into manageable chunks

**Implementation**:
- Typically 1,000-10,000 records per batch
- Adjust chunk size based on data complexity
- Monitor performance and adjust as needed
- Balance between throughput and resource usage

### Batch Operations

**Pattern**: Use bulk operations for efficiency

**Implementation**:
- Use bulk API when processing large volumes
- Respect Salesforce API limits (typically 2,000 records per call)
- Implement retry logic for API limit exceptions
- Monitor API usage and optimize

### Connection Management

**Pattern**: Efficient database connection management

**Implementation**:
- Implement connection pooling
- Reuse connections when possible
- Monitor connection usage
- Handle connection failures gracefully

## Monitoring and Observability

### Integration Health Dashboards

**Metrics**:
- Records processed per run
- Success/failure rates
- Processing time
- Error rates by type
- Records pending sync

### Alerting

**Alerts**:
- High error rates
- Processing time exceeding thresholds
- Integration job failures
- Data quality issues
- API limit warnings

### Logging

**Logging**:
- Log all integration operations
- Track processing metrics
- Record error details
- Support troubleshooting workflows
- Enable audit trails

## Best Practices

### Chunking and Batching

- Break large data sets into manageable chunks (1,000-10,000 records per batch)
- Use file-based staging for ID lists exceeding 50,000 records
- Dynamically split large ID lists into SQL IN-clause batches (1,000 IDs per IN clause)
- Monitor performance and adjust chunk sizes as needed

### External ID Strategy

- Always use external IDs for objects that receive data from integrations
- Design external IDs to be stable and unique (mirror external system primary keys)
- Use composite external IDs when external systems use multi-column keys
- Include timestamp fields to track last sync time

### Error Handling

- Capture error details at each step
- Implement retry logic for transient failures
- Use dead-letter queues for unprocessable records
- Log all errors for troubleshooting
- Support manual retry for failed records

### Performance

- Use bulk operations for efficiency
- Implement connection pooling
- Monitor API usage and optimize
- Profile integration performance
- Adjust chunk sizes based on performance data

### Monitoring

- Build dashboards showing integration health
- Set up alerts for integration failures
- Log all operations for troubleshooting
- Track processing metrics
- Enable audit trails

## Tradeoffs

### Advantages

- Handles very large data volumes efficiently
- Supports stable record mapping through external IDs
- Enables safe retry operations
- Provides comprehensive error handling
- Supports reconciliation between systems

### Challenges

- Complex file-based staging implementation
- Requires careful chunk size management
- Error recovery can be complex
- Performance tuning required
- Monitoring and observability complexity

## When to Use This Pattern

Use SIS synchronization patterns when:

- Integrating with legacy SIS systems
- Processing hundreds of thousands of records daily
- Need stable record mapping between systems
- Require batch-oriented integration approach
- Need to support retry and error recovery

## When Not to Use This Pattern

Avoid this pattern when:

- Real-time synchronization required
- Low data volumes (can use simpler patterns)
- No legacy system integration
- Different integration requirements exist

## Q&A

### Q: What are SIS synchronization patterns?

**A**: **SIS synchronization patterns** are high-volume batch synchronization patterns for integrating Salesforce Education Cloud with legacy Student Information Systems (SIS). They handle hundreds of thousands of student records daily through ETL platforms (Dell Boomi, MuleSoft) with file-based staging and dynamic SQL batching.

### Q: How do I handle high-volume batch synchronization?

**A**: Handle high-volume batch sync by: (1) **Using ETL platforms** (Dell Boomi, MuleSoft) for transformation, (2) **File-based staging** for large datasets (ID lists exceeding 50,000 records), (3) **Dynamic SQL batching** (split large ID lists into SQL IN-clause batches of 1,000 IDs), (4) **Chunking strategy** (1,000-10,000 records per batch), (5) **Bulk operations** (use Bulk API for efficiency), (6) **Connection pooling** (efficient database connection management).

### Q: What is the recommended chunk size for batch processing?

**A**: Recommended chunk sizes: (1) **1,000-10,000 records per batch** (adjust based on data complexity), (2) **1,000 IDs per SQL IN-clause** (for dynamic SQL batching), (3) **2,000 records per Bulk API call** (Salesforce API limit). Monitor performance and adjust chunk sizes as needed. Balance between throughput and resource usage.

### Q: How do I use external IDs for SIS synchronization?

**A**: Use external IDs by: (1) **Mirroring SIS primary keys** (e.g., EMPLID) in Salesforce external ID fields, (2) **Designing stable external IDs** (don't change over time), (3) **Using composite external IDs** when SIS uses multi-column keys, (4) **Including timestamp fields** to track last sync time, (5) **Using external IDs for record matching** (upsert operations). External IDs enable stable record mapping and idempotent operations.

### Q: How do I handle errors in high-volume batch synchronization?

**A**: Handle errors by: (1) **Capturing error details** at each step, (2) **Implementing retry logic** for transient failures (network, timeouts), (3) **Using dead-letter queues** for unprocessable records, (4) **Logging all errors** for troubleshooting, (5) **Supporting manual retry** for failed records, (6) **Tracking error patterns** for system improvements. Enable error recovery and data quality improvements.

### Q: How do I monitor SIS synchronization health?

**A**: Monitor by: (1) **Building dashboards** (records processed, success/failure rates, processing time), (2) **Setting up alerts** (high error rates, processing time thresholds, job failures), (3) **Logging all operations** (track processing metrics, error details), (4) **Tracking metrics** (records pending sync, error rates by type, API usage), (5) **Enabling audit trails** (support troubleshooting, compliance).

### Q: What are the performance optimization strategies for SIS sync?

**A**: Optimize performance by: (1) **Chunking large datasets** (manageable batch sizes), (2) **Using bulk operations** (Bulk API for efficiency), (3) **Implementing connection pooling** (reuse database connections), (4) **Monitoring API usage** (respect Salesforce limits), (5) **Profiling integration performance** (identify bottlenecks), (6) **Adjusting chunk sizes** based on performance data.

### Q: When should I use SIS synchronization patterns?

**A**: Use when: (1) **Integrating with legacy SIS systems** (Oracle-based, batch-oriented), (2) **Processing hundreds of thousands of records daily** (high-volume requirements), (3) **Need stable record mapping** (external IDs for matching), (4) **Require batch-oriented approach** (not real-time), (5) **Need error recovery** (retry logic, dead-letter queues). These patterns are designed for high-volume, batch-oriented SIS integrations.

### Q: What is the difference between file-based staging and direct API calls?

**A**: **File-based staging** stores ID lists in files when exceeding 50,000 records, then processes files in batches. **Direct API calls** make API calls directly without file staging. Use file-based staging for very large datasets (hundreds of thousands of records) to avoid memory issues and enable efficient batch processing. Direct API calls work for smaller datasets.

### Q: What are best practices for SIS synchronization?

**A**: Best practices include: (1) **Always use external IDs** for objects receiving integration data, (2) **Break large datasets into chunks** (1,000-10,000 records per batch), (3) **Use file-based staging** for ID lists exceeding 50,000 records, (4) **Implement retry logic** for transient failures, (5) **Monitor integration health** (dashboards, alerts, logging), (6) **Profile performance** and optimize, (7) **Support error recovery** (dead-letter queues, manual retry).

## Edge Cases and Limitations

### Edge Case 1: Very Large ID Lists (Hundreds of Thousands of Records)

**Scenario**: ID lists exceeding 100,000 records that cannot be processed in memory or via single API calls.

**Consideration**:
- Use file-based staging to write ID lists to disk
- Split large ID lists into multiple files (50,000-100,000 IDs per file)
- Process files sequentially to avoid memory issues
- Implement file cleanup after processing to manage disk space
- Monitor disk space usage during processing

### Edge Case 2: Database Connection Pool Exhaustion

**Scenario**: High-volume batch processing exhausts database connection pool, causing connection failures.

**Consideration**:
- Implement connection pooling with appropriate pool size
- Reuse connections when possible to reduce connection overhead
- Monitor connection usage and adjust pool size as needed
- Implement connection retry logic for transient connection failures
- Use connection timeout settings to prevent hanging connections

### Edge Case 3: SQL IN-Clause Size Limits

**Scenario**: Database systems have limits on SQL IN-clause size (e.g., Oracle limit of 1,000 items per IN clause).

**Consideration**:
- Split large ID lists into batches of 1,000 IDs per IN clause
- Use parameterized queries to prevent SQL injection
- Handle database-specific IN-clause limits (Oracle, SQL Server, etc.)
- Implement dynamic SQL generation to split large lists
- Test with database-specific limits before production

### Edge Case 4: Partial Batch Failures

**Scenario**: Some records in a batch fail while others succeed, requiring partial retry logic.

**Consideration**:
- Track individual record success/failure status
- Implement partial retry logic for failed records only
- Use dead-letter queues for records that cannot be processed
- Log detailed error information for troubleshooting
- Support manual retry for failed records

### Edge Case 5: External ID Collisions

**Scenario**: Multiple source systems use the same external ID values, causing conflicts.

**Consideration**:
- Design external IDs to include source system identifier (e.g., "SIS|EMPLID123")
- Use composite external IDs when source systems use multi-column keys
- Validate external ID uniqueness before upsert operations
- Handle external ID conflicts gracefully (log conflicts, skip or update based on business rules)
- Implement external ID conflict resolution strategies

### Edge Case 6: Time-Versioned Records

**Scenario**: Source system uses time-versioned records (effective dates) requiring composite external IDs.

**Consideration**:
- Use composite external IDs with effective date components
- Handle effective date ranges and overlaps
- Process time-versioned records in chronological order
- Support record updates when effective dates change
- Validate effective date logic (start date <= end date)

### Limitations

- **ETL Platform Capacity**: ETL platforms have processing limits (memory, CPU, connection limits)
- **Database Query Limits**: Database systems have IN-clause size limits (typically 1,000 items)
- **Salesforce API Limits**: Bulk API has daily limits (varies by org type) and batch size limits (2,000 records per call)
- **File System Storage**: File-based staging requires sufficient disk space for large ID lists
- **Event Retention**: Change events have 24-hour retention limits (standard CDC events)
- **Connection Pool Limits**: Database connection pools have maximum connection limits
- **Processing Time**: Large batches require extended processing time (hours for millions of records)
- **Error Recovery Complexity**: Partial failures require complex retry and recovery logic

## Related Patterns

- [ETL vs API vs Events](/rag/integrations/etl-vs-api-vs-events.html) - Integration pattern selection
- [Integration Platform Patterns](/rag/integrations/integration-platform-patterns.html) - MuleSoft and Dell Boomi patterns
- [Data Migration Patterns](/rag/data-modeling/data-migration-patterns.html) - Data migration strategies
- [External IDs and Integration Keys](/rag/data-modeling/external-ids-and-integration-keys.html) - External ID patterns

