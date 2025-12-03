---
layout: default
title: Data Quality and Stewardship for Salesforce
description: This guide covers data quality and stewardship patterns for Salesforce, including duplicate prevention beyond leads, survivorship rules, and master data governance
permalink: /rag/data-governance/data-quality-stewardship.html
---

# Data Quality and Stewardship for Salesforce

## Overview

This guide covers data quality and stewardship patterns for Salesforce, including duplicate prevention beyond leads, survivorship rules, and master data governance. These patterns are essential for maintaining data integrity, preventing duplicates, and ensuring consistent data across the organization.

**Related Patterns**:
- <a href="{{ '/rag/data-governance/data-modeling/lead-management-patterns.html' | relative_url }}">Lead Management Patterns</a> - Lead duplicate prevention
- <a href="{{ '/rag/data-governance/troubleshooting/data-reconciliation.html' | relative_url }}">Data Reconciliation</a> - Data reconciliation patterns
- <a href="{{ '/rag/data-governance/data-modeling/external-ids-and-integration-keys.html' | relative_url }}">External IDs and Integration Keys</a> - External ID patterns

## Consensus Best Practices

- **Prevent duplicates at creation**: Use duplicate rules and matching rules to prevent duplicates
- **Implement data quality checks**: Validate data quality at entry and through automation
- **Establish data stewardship**: Assign data owners and stewards for data quality
- **Monitor data quality metrics**: Track data quality KPIs and trends
- **Automate data quality processes**: Use automation to maintain data quality
- **Document data quality rules**: Document all data quality rules and procedures
- **Regular data quality reviews**: Conduct regular data quality audits
- **Train users on data quality**: Ensure users understand data quality requirements

## Duplicate Prevention Beyond Leads

### Account Duplicate Prevention

**Account Matching Strategies**:
- **Name matching**: Match on Account Name
- **Domain matching**: Match on Website domain
- **Billing address matching**: Match on billing address
- **D-U-N-S number matching**: Match on D-U-N-S number
- **Composite matching**: Combine multiple fields for matching

**Account Duplicate Rules**:
- Configure duplicate rules for Account object
- Use matching rules to define match criteria
- Set blocking vs. alerting rules
- Configure rule actions (block, alert, allow)

**Account Matching Best Practices**:
- Use multiple matching criteria
- Handle name variations (LLC, Inc., Corp.)
- Consider international naming conventions
- Test matching rules with real data
- Monitor duplicate rule effectiveness

### Contact Duplicate Prevention

**Contact Matching Strategies**:
- **Email matching**: Match on Email (primary identifier)
- **Name and email**: Match on Name + Email combination
- **Phone matching**: Match on Phone number
- **External ID matching**: Match on External ID from source system
- **Composite matching**: Combine multiple fields

**Contact Duplicate Rules**:
- Configure duplicate rules for Contact object
- Use matching rules for Contact matching
- Handle Contact-Account relationships
- Consider Contact conversion scenarios

**Contact Matching Best Practices**:
- Email is primary matching field
- Handle email variations (case, domains)
- Consider name variations and nicknames
- Test with real-world data scenarios
- Monitor duplicate prevention effectiveness

### Custom Duplicate Rules

**Custom Object Duplicate Prevention**:
- Create duplicate rules for custom objects
- Define custom matching criteria
- Configure rule actions
- Test custom duplicate rules

**Custom Matching Logic**:
- Use Apex for complex matching logic
- Implement fuzzy matching algorithms
- Handle data normalization
- Support multiple matching strategies

**Custom Duplicate Rule Patterns**:
- **External ID matching**: Match on External ID fields
- **Composite key matching**: Match on multiple fields
- **Fuzzy matching**: Match on similar but not identical values
- **Relationship-based matching**: Match based on relationships

### Matching Strategies

**Exact Matching**:
- Exact field value match
- Case-insensitive matching
- Trimmed value matching
- Most reliable but may miss variations

**Fuzzy Matching**:
- Similarity-based matching
- Handles typos and variations
- More complex to implement
- May produce false positives

**Composite Matching**:
- Combine multiple fields
- Weight fields by importance
- More accurate than single-field matching
- Requires careful tuning

## Survivorship Rules

### Data Merge Strategies

**Merge Decision Framework**:
- **Source priority**: Prefer data from trusted source
- **Recency**: Prefer most recent data
- **Completeness**: Prefer more complete records
- **Quality score**: Prefer higher quality data

**Merge Process**:
1. Identify duplicate records
2. Apply survivorship rules
3. Merge records into master record
4. Archive or delete duplicate records
5. Update related records

**Merge Best Practices**:
- Document merge rules
- Test merge procedures
- Maintain merge audit trail
- Handle merge conflicts
- Update related records

### Field-Level Survivorship

**Survivorship Rules by Field**:
- **Name fields**: Prefer most complete or recent
- **Address fields**: Prefer most recent or verified
- **Contact fields**: Prefer primary contact method
- **Custom fields**: Define rules per field type

**Field Priority Rules**:
- Define priority by field
- Handle null vs. populated values
- Consider data quality scores
- Support manual override

**Field Survivorship Implementation**:
- Configure merge field mapping
- Implement custom merge logic in Apex
- Test field survivorship rules
- Document field-level rules

### Merge Conflict Resolution

**Conflict Types**:
- **Data conflicts**: Different values for same field
- **Relationship conflicts**: Different related records
- **Ownership conflicts**: Different record owners
- **Sharing conflicts**: Different sharing rules

**Conflict Resolution Strategies**:
- **Automatic resolution**: Apply survivorship rules automatically
- **Manual resolution**: Require user input for conflicts
- **Hybrid approach**: Auto-resolve simple conflicts, manual for complex

**Conflict Resolution Best Practices**:
- Document conflict resolution rules
- Provide conflict resolution UI
- Maintain conflict resolution audit trail
- Train users on conflict resolution

## Master Data Governance

### Master Data Management Patterns

**Master Data Definition**:
- **Customer master data**: Accounts, Contacts
- **Product master data**: Products, Price Books
- **Reference data**: Picklist values, custom settings
- **Transactional data**: Opportunities, Cases

**Master Data Management**:
- Identify master data entities
- Define master data ownership
- Establish data governance processes
- Implement data quality controls

**Master Data Patterns**:
- **Single source of truth**: One authoritative source
- **Data synchronization**: Keep master data in sync
- **Data quality enforcement**: Enforce quality at source
- **Data stewardship**: Assign data stewards

### Data Stewardship Workflows

**Data Steward Roles**:
- **Data Owner**: Business owner of data domain
- **Data Steward**: Day-to-day data quality management
- **Data Custodian**: Technical data management
- **Data User**: End users of data

**Stewardship Responsibilities**:
- Monitor data quality
- Resolve data quality issues
- Maintain data quality rules
- Train users on data quality
- Report on data quality metrics

**Stewardship Workflows**:
- Data quality issue identification
- Issue assignment to stewards
- Issue resolution process
- Quality verification
- Issue closure and reporting

### Data Quality Metrics

**Data Quality KPIs**:
- **Completeness**: Percentage of required fields populated
- **Accuracy**: Percentage of accurate data values
- **Consistency**: Consistency across related records
- **Uniqueness**: Duplicate rate
- **Timeliness**: Data freshness and update frequency

**Metric Tracking**:
- Define data quality metrics
- Calculate metrics regularly
- Report metrics to stakeholders
- Set quality targets
- Monitor trends over time

**Metric Dashboards**:
- Create data quality dashboards
- Display key quality metrics
- Show trends over time
- Highlight quality issues
- Enable drill-down to details

### Data Quality Automation

**Automated Quality Checks**:
- Validation rules for data entry
- Automated duplicate detection
- Data quality scoring
- Automated data cleansing

**Quality Automation Patterns**:
- **Real-time validation**: Validate on data entry
- **Batch quality checks**: Periodic quality audits
- **Automated cleansing**: Fix common data issues
- **Quality scoring**: Calculate quality scores automatically

**Automation Best Practices**:
- Balance automation with user control
- Document automated processes
- Monitor automation effectiveness
- Allow manual override when needed

## Data Quality Monitoring

### Quality Monitoring Patterns

**Monitoring Approaches**:
- **Real-time monitoring**: Monitor quality during data entry
- **Batch monitoring**: Periodic quality audits
- **Event-driven monitoring**: Monitor on data changes
- **Continuous monitoring**: Ongoing quality tracking

**Monitoring Implementation**:
- Set up quality monitoring dashboards
- Configure quality alerts
- Schedule quality reports
- Review quality metrics regularly

### Quality Issue Management

**Issue Identification**:
- Automated duplicate detection
- Quality score thresholds
- User-reported issues
- Regular quality audits

**Issue Resolution**:
- Assign issues to data stewards
- Track issue resolution
- Verify resolution quality
- Close resolved issues

**Issue Tracking**:
- Maintain issue log
- Track issue status
- Measure resolution time
- Report on issue trends

## Q&A

### Q: How do I prevent duplicates beyond Leads in Salesforce?

**A**: Prevent duplicates by: (1) **Configuring duplicate rules** for Account, Contact, and other objects, (2) **Using matching rules** to define match criteria (Name, Email, Domain, Address), (3) **Setting blocking vs. alerting rules** (block duplicates or alert users), (4) **Using composite matching** (combine multiple fields), (5) **Implementing data quality checks** at entry, (6) **Using external IDs** for integration-based duplicates.

### Q: What are survivorship rules and when should I use them?

**A**: **Survivorship rules** determine which field values to keep when merging duplicate records. Use survivorship rules when: (1) **Merging duplicate records** (decide which values to keep), (2) **Data consolidation** (combining data from multiple sources), (3) **Master data management** (maintaining single source of truth). Rules can be: Most recent, Most complete, Specific field priority, Custom logic.

### Q: What is master data governance?

**A**: **Master data governance** is the process of managing master data (core business data like Accounts, Contacts) to ensure quality, consistency, and accuracy. It includes: (1) **Data stewardship** (assigning data owners and stewards), (2) **Data quality rules** (defining quality standards), (3) **Data quality monitoring** (tracking quality metrics), (4) **Data quality automation** (automated quality checks), (5) **Single source of truth** (one authoritative source).

### Q: What are data quality metrics and how do I track them?

**A**: Data quality metrics include: (1) **Completeness** - percentage of required fields populated, (2) **Accuracy** - percentage of accurate data values, (3) **Consistency** - consistency across related records, (4) **Uniqueness** - duplicate rate, (5) **Timeliness** - data freshness and update frequency. Track metrics by: defining metrics, calculating regularly, reporting to stakeholders, setting quality targets, monitoring trends.

### Q: How do I implement data stewardship?

**A**: Implement data stewardship by: (1) **Assigning data stewards** (Data Owner, Data Steward, Data Custodian roles), (2) **Defining stewardship responsibilities** (monitor quality, resolve issues, maintain rules), (3) **Creating stewardship workflows** (issue identification, assignment, resolution), (4) **Training stewards** on data quality, (5) **Providing tools** for stewards (dashboards, reports), (6) **Measuring stewardship effectiveness** (track resolution times, quality improvements).

### Q: How do I automate data quality checks?

**A**: Automate data quality by: (1) **Validation rules** for data entry (real-time validation), (2) **Automated duplicate detection** (duplicate rules, matching rules), (3) **Data quality scoring** (calculate quality scores automatically), (4) **Automated data cleansing** (fix common data issues), (5) **Batch quality checks** (periodic quality audits), (6) **Quality alerts** (notify on quality issues). Balance automation with user control.

### Q: What is the difference between blocking and alerting duplicate rules?

**A**: **Blocking rules** prevent duplicate records from being created (users must resolve duplicates before saving). **Alerting rules** allow duplicates but warn users (users can choose to proceed or resolve). Use blocking for critical duplicates (Accounts, Contacts), alerting for less critical duplicates. Configure rule actions (block, alert, allow) based on business requirements.

### Q: How do I monitor data quality?

**A**: Monitor data quality by: (1) **Setting up quality dashboards** (display key quality metrics), (2) **Configuring quality alerts** (notify on quality issues), (3) **Scheduling quality reports** (regular quality reports), (4) **Reviewing quality metrics** regularly, (5) **Tracking quality trends** over time, (6) **Identifying quality issues** (automated detection, user reports, audits), (7) **Measuring resolution** (track issue resolution times).

### Q: What are best practices for data quality?

**A**: Best practices include: (1) **Prevent duplicates at creation** (duplicate rules, matching rules), (2) **Implement data quality checks** (validation rules, automated checks), (3) **Establish data stewardship** (assign stewards, define responsibilities), (4) **Monitor data quality metrics** (track KPIs, trends), (5) **Automate data quality processes** (where possible), (6) **Document data quality rules** (clear procedures), (7) **Regular data quality reviews** (audits, improvements), (8) **Train users** on data quality requirements.

### Q: How do I handle data quality issues?

**A**: Handle data quality issues by: (1) **Identifying issues** (automated detection, user reports, audits), (2) **Assigning issues to stewards** (track assignment), (3) **Resolving issues** (follow resolution process), (4) **Verifying resolution** (quality verification), (5) **Closing issues** (document resolution), (6) **Reporting on issues** (track trends, resolution times), (7) **Preventing future issues** (update rules, train users).

## Related Patterns

- <a href="{{ '/rag/data-governance/data-modeling/lead-management-patterns.html' | relative_url }}">Lead Management Patterns</a> - Lead duplicate prevention
- <a href="{{ '/rag/data-governance/troubleshooting/data-reconciliation.html' | relative_url }}">Data Reconciliation</a> - Data reconciliation patterns
- <a href="{{ '/rag/data-governance/data-modeling/external-ids-and-integration-keys.html' | relative_url }}">External IDs and Integration Keys</a> - External ID patterns
- <a href="{{ '/rag/data-governance/data-modeling/data-migration-patterns.html' | relative_url }}">Data Migration Patterns</a> - Data migration quality patterns

