---
title: "Data Storage Planning in Salesforce"
source: "The Salesforce Master Class wiki"
source_url: "https://github.com/Coding-With-The-Force/The-Salesforce-Master-Class/wiki"
topic: "Topic 4: The Complete Guide To Salesforce Architecture"
section: "Data Storage in Salesforce"
level: "Intermediate"
tags:
  - salesforce
  - architecture
  - data-storage
  - capacity-planning
  - best-practices
last_reviewed: "2025-01-XX"
---

# Overview

Data storage planning is critical for Salesforce orgs to ensure adequate capacity, manage costs, and plan for growth. Understanding how Salesforce calculates storage, what counts toward storage limits, and how to plan for future needs enables effective capacity management.

Data storage planning encompasses calculating current storage usage, understanding storage limits by edition, identifying objects that don't count toward storage, planning for future growth, and managing storage efficiently. The approach differs by Salesforce edition and org type.

Most organizations need to monitor storage usage regularly and plan for growth. Understanding storage calculation and limits enables proactive capacity management and cost planning.

# Core Concepts

## How Salesforce Calculates Storage

**What it is**: Salesforce calculates storage based on data and file storage, with different limits for different storage types.

**Storage components**:
- **Data storage**: Records in standard and custom objects
- **File storage**: Files, attachments, and documents
- **Big Object storage**: Big Objects (separate limit, doesn't count toward data storage)

**Storage calculation**:
- **Data storage**: Each record counts toward storage (typically 2KB per record, varies by object)
- **File storage**: Files and attachments count toward file storage (actual file size)
- **Field history**: Field history tracking counts toward data storage
- **Recycle Bin**: Deleted records count toward storage for 15 days

**Storage limits by edition**:
- **Professional**: 1 GB data, 1 GB file
- **Enterprise**: 10 GB data, 10 GB file (can purchase additional)
- **Performance**: 10 GB data, 10 GB file (can purchase additional)
- **Unlimited**: 10 GB data, 10 GB file (can purchase additional)

## Calculating Current Storage

**What it is**: Determining how much storage is currently used in org.

**Calculation approach**:
- **Data storage**: Sum of records across all objects (typically 2KB per record)
- **File storage**: Sum of file sizes (ContentVersion, Attachments)
- **Field history**: Sum of field history records
- **Recycle Bin**: Sum of deleted records (counts for 15 days)

**Tools for calculation**:
- **Setup → Storage Usage**: View storage by object and file type
- **Data Storage page**: Detailed breakdown of data storage by object
- **File Storage page**: Detailed breakdown of file storage
- **SOQL queries**: Query object counts and file sizes

**Best practices**:
- Monitor storage usage regularly
- Track storage trends over time
- Identify objects using most storage
- Plan for growth based on trends

## Objects That Don't Count Toward Storage

**What it is**: Some objects don't count toward data storage limits.

**Objects that don't count**:
- **Big Objects**: Have separate storage limit
- **Platform Events**: Don't count toward data storage
- **Change Data Capture events**: Don't count toward data storage
- **Knowledge Article Versions**: Don't count (archived versions)
- **Email Templates**: Don't count toward data storage
- **Reports and Dashboards**: Don't count toward data storage

**Why it matters**: Understanding what doesn't count helps with storage planning and optimization.

## Planning for Future Growth

**What it is**: Estimating future storage needs based on growth trends and business plans.

**Planning approach**:
- **Historical growth**: Analyze storage growth over past periods
- **Business growth**: Project storage based on business growth (users, transactions, data)
- **Data retention**: Consider data retention policies and archiving
- **Big Object usage**: Plan for Big Objects if using for historical data

**Growth factors**:
- **User growth**: More users = more data
- **Transaction volume**: More transactions = more records
- **Data retention**: Longer retention = more storage
- **File usage**: More files = more file storage

**Best practices**:
- Project storage needs 12-24 months ahead
- Include buffer for unexpected growth
- Plan for data archiving if needed
- Consider Big Objects for historical data

# Deep-Dive Patterns & Best Practices

## Storage Optimization Strategies

### Data Archiving

**What it is**: Moving old or infrequently accessed data to Big Objects or external storage.

**When to use**: When data storage is approaching limits, or when old data is rarely accessed.

**Approach**:
- Identify old or infrequently accessed data
- Move to Big Objects (for historical data)
- Or export to external storage and delete from Salesforce
- Update processes to archive data regularly

**Benefits**: Reduces data storage usage, maintains access to historical data, enables compliance.

### File Storage Management

**What it is**: Managing file storage efficiently to avoid exceeding limits.

**Strategies**:
- **Use ContentVersion instead of Attachments**: More efficient
- **Archive old files**: Move old files to external storage
- **Compress files**: Reduce file sizes when possible
- **Delete unused files**: Remove files that are no longer needed

**Best practices**:
- Monitor file storage usage
- Set up processes to archive old files
- Use external file storage for large files
- Regularly clean up unused files

### Field History Optimization

**What it is**: Managing field history tracking to minimize storage impact.

**Strategies**:
- **Track only necessary fields**: Don't track all fields
- **Set retention policies**: Archive or delete old field history
- **Use Big Objects for history**: Store field history in Big Objects

**Best practices**:
- Review field history tracking regularly
- Track only fields that need auditing
- Archive old field history if needed

## Storage Monitoring

### Regular Monitoring

**What it is**: Regularly checking storage usage to identify trends and issues.

**Monitoring approach**:
- **Weekly or monthly reviews**: Check storage usage regularly
- **Trend analysis**: Track storage growth over time
- **Alert thresholds**: Set up alerts when storage approaches limits
- **Object-level analysis**: Identify objects using most storage

**Tools**:
- Setup → Storage Usage
- Data Storage and File Storage pages
- Custom reports on object counts
- Storage monitoring tools

### Storage Alerts

**What it is**: Setting up alerts when storage approaches limits.

**Alert thresholds**:
- **Warning**: 75% of storage used
- **Critical**: 90% of storage used
- **Action required**: 95% of storage used

**Best practices**:
- Set up alerts early
- Include storage trends in alerts
- Plan for storage increases before hitting limits

# Implementation Guide

## Prerequisites

- Understanding of current storage usage
- Knowledge of storage limits by edition
- Understanding of data growth trends
- Access to storage monitoring tools

## High-Level Steps

1. **Assess current storage**: Calculate current data and file storage usage
2. **Identify storage trends**: Analyze storage growth over time
3. **Project future needs**: Estimate storage needs based on growth
4. **Plan optimization**: Identify opportunities to optimize storage
5. **Implement optimization**: Archive data, manage files, optimize field history
6. **Monitor regularly**: Set up monitoring and alerts
7. **Plan for growth**: Purchase additional storage if needed

## Key Configuration Decisions

**Storage monitoring frequency**: How often to monitor? Weekly or monthly depending on growth rate.

**Alert thresholds**: When to alert? Typically 75% warning, 90% critical.

**Archiving strategy**: When to archive? Depends on data access patterns and retention requirements.

**Storage purchase**: When to purchase additional storage? Plan ahead, don't wait until limit is reached.

# Common Pitfalls & Anti-Patterns

## Bad Pattern: Not Monitoring Storage

**Why it's bad**: Storage limits can be hit unexpectedly, causing data load failures and user issues.

**Better approach**: Monitor storage regularly. Set up alerts. Plan for growth. Purchase additional storage before hitting limits.

## Bad Pattern: Tracking All Fields for History

**Why it's bad**: Field history tracking consumes significant storage. Tracking unnecessary fields wastes storage.

**Better approach**: Track only fields that need auditing. Review field history tracking regularly. Archive old field history.

## Bad Pattern: Not Archiving Old Data

**Why it's bad**: Old data accumulates, consuming storage without providing value.

**Better approach**: Implement data archiving strategy. Move old data to Big Objects or external storage. Set up regular archiving processes.

## Bad Pattern: Ignoring File Storage

**Why it's bad**: File storage can grow quickly and is often overlooked in storage planning.

**Better approach**: Monitor file storage separately. Implement file archiving. Use external storage for large files. Clean up unused files regularly.

# Real-World Scenarios

## Scenario 1: Approaching Data Storage Limit

**Problem**: Org is at 85% of data storage limit, growing at 5% per month.

**Context**: Enterprise edition, 10 GB data storage limit, no archiving strategy.

**Solution**: Implement data archiving strategy. Move old records (older than 2 years) to Big Objects. Set up regular archiving process. Monitor storage trends. Plan for storage purchase if needed.

## Scenario 2: High File Storage Usage

**Problem**: File storage is at 90% of limit, mostly from old attachments.

**Context**: Many old attachments, no file management process.

**Solution**: Archive old attachments (older than 1 year) to external storage. Implement file retention policy. Use ContentVersion instead of Attachments for new files. Set up regular file cleanup process.

## Scenario 3: Planning for Rapid Growth

**Problem**: Organization is growing rapidly, need to plan for storage needs.

**Context**: Adding 100 users per quarter, transaction volume increasing, need 24-month storage plan.

**Solution**: Analyze historical growth trends. Project storage needs based on user and transaction growth. Plan for data archiving. Budget for additional storage purchases. Set up monitoring and alerts.

# Checklist / Mental Model

## Storage Planning

- [ ] Assess current storage usage (data and file)
- [ ] Identify storage trends (growth rate, patterns)
- [ ] Project future storage needs (12-24 months)
- [ ] Identify optimization opportunities (archiving, cleanup)
- [ ] Plan for storage purchases if needed
- [ ] Set up monitoring and alerts

## Storage Management

- [ ] Monitor storage regularly (weekly or monthly)
- [ ] Review storage trends and projections
- [ ] Implement archiving strategies
- [ ] Clean up unused data and files
- [ ] Optimize field history tracking
- [ ] Purchase additional storage before hitting limits

## Mental Model: Proactive Capacity Management

Think of storage planning as proactive capacity management. Monitor regularly, plan for growth, optimize usage, and purchase additional storage before hitting limits. Don't wait until storage is full to act.

# Key Terms & Definitions

- **Data storage**: Storage for records in standard and custom objects
- **File storage**: Storage for files, attachments, and documents
- **Big Objects**: Objects designed for large data volumes with separate storage limit
- **Field history**: Historical tracking of field value changes
- **Recycle Bin**: Deleted records that count toward storage for 15 days
- **Storage limits**: Maximum storage allowed by Salesforce edition

## Q&A

### Q: How do I calculate current storage usage in Salesforce?

**A**: Calculate usage by: (1) **Use Setup → Storage Usage** to view storage by object and file type, (2) **Use Data Storage and File Storage pages** for detailed breakdowns, (3) **Calculate data storage** by summing records (typically 2KB per record), (4) **Calculate file storage** by summing file sizes. Regular monitoring helps track usage and plan for growth.

### Q: What objects don't count toward data storage limits?

**A**: Objects that don't count: (1) **Big Objects** (separate limit), (2) **Platform Events**, (3) **Change Data Capture events**, (4) **Knowledge Article Versions** (archived), (5) **Email Templates**, (6) **Reports and Dashboards**. Understanding what doesn't count helps with storage planning and optimization.

### Q: How do I plan for future storage growth?

**A**: Plan by: (1) **Analyze historical storage growth trends**, (2) **Project storage** based on business growth (users, transactions, data), (3) **Consider data retention policies** and archiving, (4) **Plan 12-24 months ahead**, (5) **Include buffer** for unexpected growth. Proactive planning prevents storage issues.

### Q: What's the difference between data storage and file storage?

**A**: **Data storage** is for records in objects (typically 2KB per record). **File storage** is for files, attachments, and documents (actual file size). Both have separate limits and should be monitored separately. Data storage and file storage are calculated and managed independently.

### Q: How do I optimize storage usage?

**A**: Optimize by: (1) **Archive old data** to Big Objects or external storage, (2) **Manage file storage** (use ContentVersion, archive old files, compress files), (3) **Optimize field history tracking** (track only necessary fields, archive old history), (4) **Regularly clean up** unused data and files, (5) **Monitor storage usage** regularly.

### Q: When should I purchase additional storage?

**A**: Purchase when: (1) **Approaching 80-85% of limit** (plan ahead, don't wait), (2) **Growth projections indicate need** (plan for future growth), (3) **As part of capacity planning** (include in budget). Don't wait until limit is reached - purchase proactively to avoid issues.

### Q: How do I monitor storage usage effectively?

**A**: Monitor by: (1) **Monitor regularly** (weekly or monthly), (2) **Set up alerts** at 75% (warning), 90% (critical), 95% (action required), (3) **Track storage trends** over time, (4) **Identify objects using most storage**, (5) **Include storage trends** in monitoring dashboards. Regular monitoring enables proactive management.

### Q: What's the best approach for data archiving?

**A**: Archive by: (1) **Identify old or infrequently accessed data**, (2) **Move to Big Objects** for historical data, (3) **Export to external storage** and delete from Salesforce, (4) **Set up regular archiving processes**, (5) **Update processes** to archive data automatically. Archiving helps manage storage and maintain performance.

### Q: How do I handle file storage management?

**A**: Manage file storage by: (1) **Use ContentVersion** instead of Attachments (more efficient), (2) **Archive old files** to external storage, (3) **Compress files** when possible, (4) **Delete unused files** regularly, (5) **Set up file retention policies**, (6) **Monitor file storage separately** from data storage. File storage has separate limits and requires separate management.

### Q: What storage limits apply to different Salesforce editions?

**A**: Storage limits: (1) **Professional** - 1 GB data, 1 GB file, (2) **Enterprise/Performance/Unlimited** - 10 GB data, 10 GB file (can purchase additional), (3) **Big Objects** have separate storage limits (don't count toward data storage). Understand limits for your edition and plan accordingly. Additional storage can be purchased for Enterprise+ editions.

