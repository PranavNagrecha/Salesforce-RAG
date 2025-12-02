# Data Quality and Stewardship for Salesforce

## Overview

This guide covers data quality and stewardship patterns for Salesforce, including duplicate prevention beyond leads, survivorship rules, and master data governance. These patterns are essential for maintaining data integrity, preventing duplicates, and ensuring consistent data across the organization.

**Related Patterns**:
- [Lead Management Patterns](rag/data-modeling/lead-management-patterns.md) - Lead duplicate prevention
- [Data Reconciliation](rag/troubleshooting/data-reconciliation.md) - Data reconciliation patterns
- [External IDs and Integration Keys](rag/data-modeling/external-ids-and-integration-keys.md) - External ID patterns

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

## Related Patterns

- [Lead Management Patterns](rag/data-modeling/lead-management-patterns.md) - Lead duplicate prevention
- [Data Reconciliation](rag/troubleshooting/data-reconciliation.md) - Data reconciliation patterns
- [External IDs and Integration Keys](rag/data-modeling/external-ids-and-integration-keys.md) - External ID patterns
- [Data Migration Patterns](rag/data-modeling/data-migration-patterns.md) - Data migration quality patterns

