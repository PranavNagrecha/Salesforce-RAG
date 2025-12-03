---
title: "Data Reconciliation Techniques"
level: "Intermediate"
tags:
  - troubleshooting
  - data-quality
  - reconciliation
  - integration
last_reviewed: "2025-01-XX"
---

# Data Reconciliation Techniques

## Overview

Systematic approaches to reconciling data between Salesforce and external systems, identifying discrepancies, and ensuring data consistency. These techniques use external IDs, integration job tracking, and comparison queries to validate data synchronization.

## Prerequisites

**Required Knowledge**:
- Understanding of SOQL query syntax
- Knowledge of external IDs and integration keys
- Understanding of integration patterns and data synchronization
- Familiarity with data quality concepts

**Recommended Reading**:
- <a href="{{ '/rag/troubleshooting/data-modeling/external-ids-and-integration-keys.html' | relative_url }}">External IDs and Integration Keys</a> - External ID patterns
- <a href="{{ '/rag/troubleshooting/integration-debugging.html' | relative_url }}">Integration Debugging</a> - Debugging integration issues
- <a href="{{ '/rag/troubleshooting/integrations/etl-vs-api-vs-events.html' | relative_url }}">ETL vs API vs Events</a> - Integration pattern selection
- <a href="{{ '/rag/troubleshooting/data-modeling/data-migration-patterns.html' | relative_url }}">Data Migration Patterns</a> - Data validation patterns

## Reconciliation Patterns

### External ID-Based Reconciliation

**Pattern**: Use external IDs to correlate records between systems

**Implementation**:
- External IDs mirror external system primary keys (e.g., EMPLID)
- Use external IDs to find corresponding records in both systems
- Compare field values between systems
- Identify records that exist in one system but not the other
- Track reconciliation results

**Benefits**:
- Stable record correlation
- Efficient record matching
- Supports automated reconciliation
- Enables discrepancy identification

### Integration Job Tracking Reconciliation

**Pattern**: Use integration job tracking fields to correlate sync operations

**Fields**:
- `Last_Sync_Timestamp__c` - when record was last synced
- `Last_Sync_Status__c` - sync job status (Success, Error, In Progress)
- `Last_Sync_Error__c` - error message if sync failed
- `Integration_Job_ID__c` - correlation ID with external system

**Usage**:
- Correlate Salesforce records with external system job logs
- Identify records that haven't synced recently
- Track sync success/failure rates
- Build reconciliation reports

### Field-Level Reconciliation

**Pattern**: Compare specific field values between systems

**Implementation**:
- Compare critical fields between Salesforce and external system
- Identify field-level discrepancies
- Track which fields differ and by how much
- Prioritize reconciliation based on field importance
- Document reconciliation results

**Use Cases**:
- Status field reconciliation
- Date field reconciliation
- Numeric field reconciliation
- Text field reconciliation

## Reconciliation Workflows

### Automated Reconciliation

**Pattern**: Automated reconciliation processes using scheduled jobs

**Implementation**:
- Scheduled Apex jobs to compare data
- Query both systems using external IDs
- Compare field values programmatically
- Generate reconciliation reports
- Alert on discrepancies

**Benefits**:
- Regular reconciliation without manual effort
- Early detection of discrepancies
- Consistent reconciliation process
- Scalable to large data volumes

### Manual Reconciliation

**Pattern**: Manual reconciliation processes for critical data

**Implementation**:
- Export data from both systems
- Compare using external IDs
- Identify discrepancies manually
- Document reconciliation results
- Update records as needed

**Use Cases**:
- One-time reconciliation after migration
- Critical data validation
- Complex reconciliation scenarios
- Ad-hoc reconciliation needs

### Incremental Reconciliation

**Pattern**: Reconcile only records that have changed since last reconciliation

**Implementation**:
- Track last reconciliation timestamp
- Query only records modified since last reconciliation
- Compare changed records
- Update reconciliation timestamp
- More efficient than full reconciliation

**Benefits**:
- Faster reconciliation for large data sets
- Focus on recent changes
- Reduced system load
- More frequent reconciliation possible

## Discrepancy Identification

### Missing Records

**Pattern**: Identify records that exist in one system but not the other

**Implementation**:
- Query external system for all records
- Query Salesforce for all records with external IDs
- Compare lists to find missing records
- Identify records missing in Salesforce
- Identify records missing in external system

**Resolution**:
- Create missing records in target system
- Investigate why records weren't synced
- Update integration logic if needed
- Document resolution

### Field Value Discrepancies

**Pattern**: Identify records where field values differ between systems

**Implementation**:
- Compare field values for matched records
- Identify fields with different values
- Track discrepancy patterns
- Prioritize reconciliation based on field importance
- Document discrepancies

**Resolution**:
- Determine which system is source of truth
- Update target system with correct values
- Investigate why values diverged
- Update integration logic if needed

### Status Discrepancies

**Pattern**: Identify records with different status values

**Implementation**:
- Compare status fields between systems
- Identify status mismatches
- Track status transition patterns
- Understand status workflow differences
- Document status discrepancies

**Resolution**:
- Align status values between systems
- Update status workflow if needed
- Document status mapping rules
- Implement status synchronization

## Reconciliation Reporting

### Reconciliation Dashboards

**Metrics**:
- Total records reconciled
- Discrepancy count by type
- Reconciliation success rate
- Records pending reconciliation
- Reconciliation trends over time

### Reconciliation Reports

**Content**:
- List of discrepancies by type
- Records requiring manual review
- Reconciliation statistics
- Trend analysis
- Recommendations for resolution

### Alerting

**Alerts**:
- High discrepancy rates
- Critical field discrepancies
- Reconciliation job failures
- Data quality issues
- Integration failures

## Best Practices

### Regular Reconciliation

- Schedule regular reconciliation jobs
- Reconcile critical data more frequently
- Track reconciliation history
- Monitor reconciliation metrics
- Alert on significant discrepancies

### External ID Management

- Always use external IDs for integrated objects
- Ensure external IDs are stable and unique
- Document external ID strategy
- Validate external ID consistency
- Handle external ID changes appropriately

### Reconciliation Tracking

- Track reconciliation results
- Document discrepancies and resolutions
- Maintain reconciliation history
- Build reconciliation reports
- Share reconciliation findings

### Error Handling

- Handle reconciliation errors gracefully
- Log reconciliation failures
- Support manual reconciliation when needed
- Provide clear error messages
- Enable error recovery workflows

## Tools and Techniques

### SOQL Queries

- Query records by external ID
- Compare field values
- Identify missing records
- Track reconciliation status
- Generate reconciliation reports

### Integration Job Tracking

- Use job tracking fields for correlation
- Track sync success/failure
- Identify records needing reconciliation
- Correlate with external system logs
- Build reconciliation dashboards

### Data Export and Comparison

- Export data from both systems
- Compare using external IDs
- Identify discrepancies
- Generate reconciliation reports
- Document findings

## Tradeoffs

### Advantages

- Ensures data consistency between systems
- Identifies integration issues early
- Supports data quality improvement
- Enables audit and compliance

### Challenges

- Requires careful external ID management
- Can be time-intensive for large data sets
- Complex reconciliation logic
- Ongoing maintenance required

## When to Use Reconciliation

Use data reconciliation when:

- Integrating with external systems
- Need to ensure data consistency
- Data quality is critical
- Compliance requires data validation
- Integration issues need identification

## When Not to Use Reconciliation

Avoid reconciliation when:

- No external system integration
- Data volumes make reconciliation impractical
- Different validation approach preferred
- Real-time validation sufficient

## Q&A

### Q: What is data reconciliation in Salesforce?

**A**: **Data reconciliation** is the process of comparing data between Salesforce and external systems to ensure consistency, identify discrepancies, and validate data synchronization. It uses external IDs, integration job tracking, and comparison queries to validate that data matches between systems.

### Q: How do I use external IDs for data reconciliation?

**A**: Use external IDs for reconciliation by: (1) **Mirroring external system primary keys** in Salesforce external ID fields, (2) **Using external IDs to find corresponding records** in both systems, (3) **Comparing field values** between systems using external IDs, (4) **Identifying records** that exist in one system but not the other, (5) **Tracking reconciliation results** using external IDs as correlation keys.

### Q: What fields should I use for integration job tracking?

**A**: Use integration job tracking fields: (1) **`Last_Sync_Timestamp__c`** - when record was last synced, (2) **`Last_Sync_Status__c`** - sync job status (Success, Error, In Progress), (3) **`Last_Sync_Error__c`** - error message if sync failed, (4) **`Integration_Job_ID__c`** - correlation ID with external system. These fields enable tracking sync operations and identifying issues.

### Q: How do I identify discrepancies between systems?

**A**: Identify discrepancies by: (1) **Querying records by external ID** in both systems, (2) **Comparing field values** between systems, (3) **Identifying missing records** (exist in one system but not the other), (4) **Tracking reconciliation results** (match, mismatch, missing), (5) **Generating reconciliation reports** showing discrepancies. Use SOQL queries and comparison logic to find differences.

### Q: How often should I run data reconciliation?

**A**: Run reconciliation based on: (1) **Data criticality** (critical data more frequently), (2) **Integration frequency** (match reconciliation to sync frequency), (3) **Data volume** (larger volumes may need less frequent reconciliation), (4) **Business requirements** (compliance, audit needs). Common cadences: **Daily** for critical data, **Weekly** for standard data, **Monthly** for reference data.

### Q: What tools can I use for data reconciliation?

**A**: Use tools including: (1) **SOQL queries** to query and compare records, (2) **Integration job tracking fields** for correlation, (3) **Data export and comparison** (export from both systems, compare), (4) **Apex scripts** for automated reconciliation, (5) **ETL tools** for complex reconciliation, (6) **Reconciliation dashboards** for monitoring. Choose tools based on data volume and complexity.

### Q: How do I handle reconciliation errors?

**A**: Handle reconciliation errors by: (1) **Logging reconciliation failures** with error details, (2) **Handling errors gracefully** (don't fail entire reconciliation), (3) **Supporting manual reconciliation** when needed, (4) **Providing clear error messages** for troubleshooting, (5) **Enabling error recovery workflows** (retry failed reconciliations), (6) **Alerting on significant discrepancies**.

### Q: What are best practices for data reconciliation?

**A**: Best practices include: (1) **Always use external IDs** for integrated objects, (2) **Schedule regular reconciliation jobs** (automated reconciliation), (3) **Track reconciliation results** and history, (4) **Monitor reconciliation metrics** (success rate, discrepancy count), (5) **Alert on significant discrepancies**, (6) **Document reconciliation processes**, (7) **Maintain reconciliation history** for audit purposes.

### Q: When should I use data reconciliation?

**A**: Use reconciliation when: (1) **Integrating with external systems** (ensure data consistency), (2) **Data quality is critical** (need to validate data), (3) **Compliance requires data validation** (audit requirements), (4) **Integration issues need identification** (troubleshooting), (5) **Data synchronization needs validation** (verify sync success).

### Q: What are the tradeoffs of data reconciliation?

**A**: Tradeoffs include: (1) **Advantages** - ensures data consistency, identifies issues early, supports data quality, enables audit/compliance, (2) **Challenges** - requires external ID management, time-intensive for large datasets, complex reconciliation logic, ongoing maintenance required. Balance reconciliation frequency with effort and data criticality.

## Edge Cases and Limitations

### Edge Case 1: Reconciliation with Missing External IDs

**Scenario**: Records missing External IDs making reconciliation impossible or inaccurate.

**Consideration**:
- Implement External ID population for existing records
- Use alternative matching strategies (name, email, etc.)
- Document External ID requirements
- Validate External ID population
- Handle records without External IDs gracefully
- Plan for External ID migration

### Edge Case 2: High-Volume Reconciliation Performance

**Scenario**: Reconciling millions of records causing performance issues and timeout errors.

**Consideration**:
- Implement batch reconciliation processing
- Use efficient SOQL queries (selective WHERE clauses)
- Process reconciliation in chunks
- Monitor reconciliation performance
- Consider async processing for large volumes
- Optimize reconciliation logic

### Edge Case 3: Reconciliation with Data Transformations

**Scenario**: Data transformed between systems (normalized, aggregated) making direct comparison difficult.

**Consideration**:
- Document data transformation rules
- Implement transformation-aware reconciliation
- Use business rules for comparison
- Test reconciliation with transformed data
- Consider reconciliation at transformation boundaries
- Document transformation impact on reconciliation

### Edge Case 4: Reconciliation During Active Integration

**Scenario**: Reconciliation running while integration is actively syncing data, causing false discrepancies.

**Consideration**:
- Schedule reconciliation during low-activity periods
- Use reconciliation windows
- Account for in-flight integration operations
- Implement reconciliation locking if needed
- Monitor reconciliation timing
- Document reconciliation scheduling

### Edge Case 5: Reconciliation with Soft Deletes

**Scenario**: Systems using soft deletes (status flags) instead of hard deletes, complicating reconciliation.

**Consideration**:
- Account for soft delete status in reconciliation
- Filter soft-deleted records appropriately
- Document soft delete handling
- Test reconciliation with soft deletes
- Consider reconciliation scope (active vs all records)
- Handle soft delete discrepancies

### Limitations

- **External ID Requirements**: Reconciliation requires External IDs for accurate matching
- **Performance Limits**: Large datasets may cause performance issues
- **Reconciliation Complexity**: Complex data transformations complicate reconciliation
- **Timing Constraints**: Reconciliation during active integration may show false discrepancies
- **Data Volume**: Very large datasets make reconciliation time-intensive
- **Transformation Complexity**: Data transformations may make direct comparison impossible
- **Reconciliation Frequency**: Frequent reconciliation may impact system performance

## Related Patterns

**See Also**:
- <a href="{{ '/rag/troubleshooting/integration-debugging.html' | relative_url }}">Integration Debugging</a> - Debugging integration issues

**Related Domains**:
- <a href="{{ '/rag/troubleshooting/data-modeling/external-ids-and-integration-keys.html' | relative_url }}">External IDs and Integration Keys</a> - External ID patterns for reconciliation
- <a href="{{ '/rag/troubleshooting/data-modeling/data-migration-patterns.html' | relative_url }}">Data Migration Patterns</a> - Data migration and validation
- <a href="{{ '/rag/troubleshooting/data-governance/data-quality-stewardship.html' | relative_url }}">Data Quality Stewardship</a> - Data quality management

- <a href="{{ '/rag/troubleshooting/integration-debugging.html' | relative_url }}">Integration Debugging</a> - Debugging integration issues
- <a href="{{ '/rag/troubleshooting/data-modeling/external-ids-and-integration-keys.html' | relative_url }}">External IDs and Integration Keys</a> - External ID patterns for reconciliation
- <a href="{{ '/rag/troubleshooting/data-modeling/data-migration-patterns.html' | relative_url }}">Data Migration Patterns</a> - Data validation patterns
- <a href="{{ '/rag/troubleshooting/integrations/etl-vs-api-vs-events.html' | relative_url }}">ETL vs API vs Events</a> - Integration pattern selection
- <a href="{{ '/rag/troubleshooting/integrations/sis-sync-patterns.html' | relative_url }}">SIS Sync Patterns</a> - High-volume synchronization patterns

