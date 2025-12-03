---
title: "Gigantic Data Loads in Salesforce"
source: "The Salesforce Master Class wiki"
source_url: "https://github.com/Coding-With-The-Force/The-Salesforce-Master-Class/wiki"
topic: "Topic 4: The Complete Guide To Salesforce Architecture"
section: "Gigantic Data Loads"
level: "Advanced"
tags:
  - salesforce
  - architecture
  - data-loads
  - bulk-operations
  - best-practices
last_reviewed: "2025-01-XX"
---

# Overview

Large data loads are a critical architectural consideration for Salesforce implementations. Loading millions of records requires specialized tools, careful planning, and understanding of platform limitations. Poorly executed large data loads can cause performance issues, data quality problems, and system instability.

Large data load planning encompasses selecting appropriate tools (Data Loader, Bulk API, ETL tools), understanding data volume and complexity, planning for data quality (deduplication, cleanup), preventing data skew, and ensuring proper testing environments. The approach differs significantly from small data loads.

Most organizations use Data Loader or Bulk API for large data loads, with ETL tools (MuleSoft, Dell Boomi) for very large or complex loads. Understanding tool capabilities, platform limitations, and best practices enables successful large data load execution.

# Core Concepts

## Tools for Large Data Loads

### Data Loader

**What it is**: Salesforce-provided tool for importing and exporting large volumes of data.

**Key characteristics**:
- GUI and command-line interfaces
- Supports CSV file import/export
- Handles up to 5 million records
- Automatic retry on errors
- Batch processing

**Advantages**:
- Free and included with Salesforce
- Easy to use (GUI interface)
- Good error handling
- Supports insert, update, upsert, delete, hard delete

**Disadvantages**:
- Limited to 5 million records
- Requires manual file preparation
- May be slow for very large loads
- Limited transformation capabilities

**When to use**: Medium to large data loads (hundreds of thousands to millions of records), straightforward data loads, one-time or occasional loads.

### Bulk API

**What it is**: Salesforce API designed for loading large volumes of data programmatically.

**Key characteristics**:
- REST and SOAP interfaces
- Asynchronous processing
- Handles very large volumes (millions of records)
- Job-based processing
- Detailed status and error reporting

**Advantages**:
- Handles very large volumes
- Programmatic control
- Good for automation
- Detailed error reporting
- Can be integrated into ETL processes

**Disadvantages**:
- Requires programming/scripting
- More complex than Data Loader
- Requires understanding of API

**When to use**: Very large data loads (millions of records), automated loads, integration with ETL tools, programmatic control needed.

### ETL Tools (MuleSoft, Dell Boomi)

**What it is**: Enterprise integration platforms that can handle large data loads with transformation capabilities.

**Key characteristics**:
- Visual data transformation
- Handles very large volumes
- Transformation and mapping capabilities
- Scheduling and automation
- Error handling and monitoring

**Advantages**:
- Handles very large volumes
- Data transformation capabilities
- Scheduling and automation
- Error handling and monitoring
- Integration with multiple systems

**Disadvantages**:
- Requires ETL tool licenses
- More complex setup
- Requires ETL tool expertise

**When to use**: Very large data loads with transformation needs, ongoing data synchronization, integration with multiple systems.

## Data Quality Considerations

### Deduplication

**What it is**: Identifying and handling duplicate records before or during data load.

**Key approaches**:
- **Pre-load deduplication**: Remove duplicates in source system before load
- **Salesforce duplicate rules**: Use Salesforce duplicate detection during load
- **External ID matching**: Use external IDs to identify and update existing records
- **Post-load deduplication**: Identify and merge duplicates after load

**Best practices**:
- Deduplicate before load when possible (more efficient)
- Use external IDs for upsert operations
- Configure duplicate rules for ongoing prevention
- Plan for duplicate handling strategy

### Data Cleanup

**What it is**: Cleaning and standardizing data before load to ensure quality.

**Key cleanup tasks**:
- **Data standardization**: Standardize formats (dates, phone numbers, addresses)
- **Data validation**: Validate data against business rules
- **Missing data handling**: Handle missing required fields
- **Data transformation**: Transform data to match Salesforce format

**Best practices**:
- Clean data in source system when possible
- Use ETL tools for transformation if needed
- Validate data before load
- Handle errors gracefully

## Preventing Data Skew

**What it is**: Uneven distribution of records that can cause performance issues.

**Common skew scenarios**:
- **Account ownership skew**: Too many records owned by single user
- **Lookup relationship skew**: Too many child records related to single parent
- **Master-detail skew**: Too many detail records for single master

**Prevention strategies**:
- **Distribute ownership**: Spread record ownership across multiple users
- **Balance relationships**: Avoid creating relationships with extreme skew
- **Use sharing instead of ownership**: Use sharing rules for access instead of ownership changes
- **Monitor for skew**: Regularly check for data skew patterns

**Best practices**:
- Plan data model to avoid skew
- Distribute ownership during data load
- Monitor for skew after load
- Address skew issues proactively

## Testing Environments

**What it is**: Using appropriate environments for testing large data loads before production.

**Environment considerations**:
- **Sandbox with data**: Load data into sandbox to test process
- **Data volume**: Use representative data volumes for testing
- **Performance testing**: Test performance impact of large data loads
- **Error handling testing**: Test error scenarios and recovery

**Best practices**:
- Test in sandbox first
- Use representative data volumes
- Test performance impact
- Test error scenarios
- Validate data quality after load

# Deep-Dive Patterns & Best Practices

## Data Load Planning

### Assessment Phase

**Key activities**:
- **Data volume assessment**: How many records? What objects?
- **Data complexity assessment**: What transformations needed? What relationships?
- **Timeline assessment**: When is load needed? What's the deadline?
- **Resource assessment**: What tools and skills available?

**Deliverables**:
- Data load plan
- Tool selection
- Timeline and resource plan
- Risk assessment

### Preparation Phase

**Key activities**:
- **Data extraction**: Extract data from source system
- **Data transformation**: Transform data to Salesforce format
- **Data validation**: Validate data quality
- **Deduplication**: Identify and handle duplicates
- **File preparation**: Prepare files for load

**Deliverables**:
- Transformed data files
- Data quality report
- Deduplication report
- Load files ready for import

### Execution Phase

**Key activities**:
- **Load execution**: Execute data load using selected tool
- **Monitoring**: Monitor load progress and errors
- **Error handling**: Handle errors and retry failed records
- **Validation**: Validate loaded data

**Deliverables**:
- Load execution report
- Error report
- Data validation report

### Validation Phase

**Key activities**:
- **Data validation**: Validate data quality and completeness
- **Relationship validation**: Validate relationships and lookups
- **Performance validation**: Validate performance impact
- **User validation**: Validate with business users

**Deliverables**:
- Data validation report
- Performance report
- User acceptance

## Bulk API Patterns

### Job Creation

**Pattern**: Create Bulk API job, upload data, close job, monitor status.

**Steps**:
1. Create job with object and operation
2. Upload CSV data in batches
3. Close job to start processing
4. Monitor job status
5. Retrieve results and handle errors

**Best practices**:
- Use appropriate batch size (typically 10,000 records)
- Monitor job status regularly
- Handle errors appropriately
- Retry failed batches

### Error Handling

**Pattern**: Retrieve failed records, analyze errors, fix data, retry.

**Steps**:
1. Retrieve failed records from job
2. Analyze error messages
3. Fix data issues
4. Retry failed records
5. Validate successful load

**Best practices**:
- Log all errors for analysis
- Categorize errors (data quality, validation, system)
- Fix root causes, not just symptoms
- Retry with fixed data

# Implementation Guide

## Prerequisites

- Understanding of data volume and complexity
- Access to appropriate tools (Data Loader, Bulk API, ETL tools)
- Understanding of Salesforce data model and relationships
- Testing environment with representative data

## High-Level Steps

1. **Assess data load**: Volume, complexity, timeline, resources
2. **Select tool**: Data Loader, Bulk API, or ETL tool based on requirements
3. **Plan data load**: Extract, transform, validate, deduplicate
4. **Prepare data**: Clean, transform, validate data files
5. **Test in sandbox**: Load data into sandbox, validate, test performance
6. **Execute production load**: Load data into production, monitor, handle errors
7. **Validate results**: Validate data quality, relationships, performance
8. **Document and handoff**: Document process, hand off to operations

## Key Configuration Decisions

**Tool selection**: Data Loader, Bulk API, or ETL tool? Depends on volume, complexity, and automation needs.

**Batch size**: How many records per batch? Typically 10,000 for Bulk API, depends on record complexity.

**Error handling strategy**: How to handle errors? Retry automatically, manual review, or combination.

**Data quality approach**: When to clean data? Before load, during load, or after load.

# Common Pitfalls & Anti-Patterns

## Bad Pattern: Loading Data Without Planning

**Why it's bad**: Large data loads without planning lead to errors, data quality issues, and performance problems.

**Better approach**: Plan data load thoroughly. Assess volume and complexity, select appropriate tool, prepare data, test in sandbox, then execute production load.

## Bad Pattern: Ignoring Data Skew

**Why it's bad**: Data skew causes performance issues that are difficult to fix after load.

**Better approach**: Plan data model to avoid skew. Distribute ownership, balance relationships, monitor for skew.

## Bad Pattern: Not Testing in Sandbox

**Why it's bad**: Testing large data loads in production risks data quality issues and performance problems.

**Better approach**: Always test large data loads in sandbox first. Use representative data volumes, test performance, validate data quality.

## Bad Pattern: Not Handling Errors

**Why it's bad**: Ignoring errors during load leads to incomplete or incorrect data.

**Better approach**: Monitor load progress, retrieve and analyze errors, fix data issues, retry failed records.

# Real-World Scenarios

## Scenario 1: Migrating Millions of Records from Legacy System

**Problem**: Need to migrate 5 million account and contact records from legacy CRM to Salesforce.

**Context**: One-time migration, data needs transformation, deduplication required, tight timeline.

**Solution**: Use Bulk API with ETL tool for transformation. Extract data, transform in ETL tool, deduplicate, load in batches using Bulk API. Test in sandbox first, then execute production load. Monitor progress and handle errors.

## Scenario 2: Ongoing Data Synchronization

**Problem**: Need to synchronize hundreds of thousands of records daily from external system.

**Context**: Ongoing synchronization, data changes frequently, needs to be automated.

**Solution**: Use ETL tool (MuleSoft or Dell Boomi) for ongoing synchronization. Schedule daily sync, use external IDs for upsert, handle errors automatically, monitor sync status.

## Scenario 3: Loading Data with Complex Relationships

**Problem**: Need to load accounts, contacts, opportunities, and cases with relationships between them.

**Context**: Multiple related objects, relationships must be maintained, data volume is large.

**Solution**: Load in order (accounts first, then contacts, then opportunities, then cases). Use external IDs to maintain relationships. Load in phases, validate relationships after each phase.

# Checklist / Mental Model

## Planning Large Data Load

- [ ] Assess data volume and complexity
- [ ] Select appropriate tool (Data Loader, Bulk API, ETL)
- [ ] Plan data extraction and transformation
- [ ] Plan deduplication strategy
- [ ] Plan data quality validation
- [ ] Plan for data skew prevention
- [ ] Plan testing approach

## Executing Large Data Load

- [ ] Extract and transform data
- [ ] Validate data quality
- [ ] Deduplicate data
- [ ] Test in sandbox
- [ ] Execute production load
- [ ] Monitor progress and errors
- [ ] Handle errors and retry
- [ ] Validate results

## Mental Model: Plan, Test, Execute, Validate

Think of large data loads as four-phase process: Plan thoroughly, test in sandbox, execute carefully, validate results. Each phase is critical for success.

# Key Terms & Definitions

- **Data Loader**: Salesforce tool for importing/exporting large volumes of data
- **Bulk API**: Salesforce API for programmatic large data loads
- **ETL**: Extract, Transform, Load - process for data integration
- **Data skew**: Uneven distribution of records causing performance issues
- **Deduplication**: Identifying and handling duplicate records
- **Upsert**: Insert new records or update existing records based on external ID
- **Batch processing**: Processing data in batches rather than all at once

# RAG-Friendly Q&A Seeds

**Q: What tools should I use for large data loads in Salesforce?**

**A**: Use Data Loader for medium to large loads (hundreds of thousands to millions of records). Use Bulk API for very large loads or programmatic control. Use ETL tools (MuleSoft, Dell Boomi) for very large loads with transformation needs or ongoing synchronization.

**Q: How do I prevent data skew during large data loads?**

**A**: Plan data model to avoid skew. Distribute record ownership across multiple users, balance relationships to avoid extreme skew, use sharing rules instead of ownership changes when possible, and monitor for skew patterns after load.

**Q: What's the best approach for deduplication during large data loads?**

**A**: Deduplicate before load when possible (more efficient). Use external IDs for upsert operations to identify existing records. Configure duplicate rules for ongoing prevention. Plan for duplicate handling strategy (merge, update, or skip).

**Q: How do I handle errors during large data loads?**

**A**: Monitor load progress regularly. Retrieve failed records, analyze error messages, categorize errors (data quality, validation, system), fix root causes, and retry failed records. Log all errors for analysis and improvement.

**Q: Should I test large data loads in sandbox first?**

**A**: Yes, always test large data loads in sandbox first. Use representative data volumes, test performance impact, validate data quality, test error scenarios, and validate relationships. Only execute production load after successful sandbox testing.

**Q: What's the difference between Data Loader and Bulk API?**

**A**: Data Loader is GUI/command-line tool, easier to use, handles up to 5 million records. Bulk API is programmatic, handles very large volumes, better for automation and integration. Choose based on volume, complexity, and automation needs.

**Q: How do I load data with complex relationships between objects?**

**A**: Load objects in order (parent objects first, then child objects). Use external IDs to maintain relationships. Load in phases, validate relationships after each phase. Use upsert operations to handle existing records.

**Q: What batch size should I use for Bulk API loads?**

**A**: Typically 10,000 records per batch for Bulk API, but depends on record complexity. Larger batches are more efficient but may hit limits. Smaller batches are safer but slower. Test to find optimal batch size for your data.

**Q: How do I handle ongoing data synchronization with large volumes?**

**A**: Use ETL tools (MuleSoft, Dell Boomi) for ongoing synchronization. Schedule regular syncs, use external IDs for upsert operations, handle errors automatically, monitor sync status, and optimize for performance.

**Q: What data quality considerations are important for large data loads?**

**A**: Clean and standardize data before load, validate data against business rules, handle missing required fields, transform data to match Salesforce format, and validate data quality after load. Plan for data quality throughout load process.

## Related Patterns

- [Data Migration Patterns](../data-modeling/data-migration-patterns.md) - Data migration strategies and patterns
- [External IDs and Integration Keys](../data-modeling/external-ids-and-integration-keys.md) - External ID patterns for data loads
- [ETL vs API vs Events](../integrations/etl-vs-api-vs-events.md) - Integration pattern selection for large loads
- [Governor Limits and Optimization](governor-limits-and-optimization.md) - Limit management for large operations
- [SIS Sync Patterns](../integrations/sis-sync-patterns.md) - High-volume batch synchronization patterns

