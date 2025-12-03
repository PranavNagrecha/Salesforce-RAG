---
title: "Data Migration Patterns"
level: "Intermediate"
tags:
  - data-modeling
  - data-migration
  - data-import
  - transformation
last_reviewed: "2025-01-XX"
---

# Data Migration Patterns

## Overview

This guide covers data migration strategies, transformation patterns, validation approaches, and rollback strategies for moving data into and within Salesforce. These patterns are essential for data imports, system migrations, and data synchronization.

**Related Patterns**:
- [External IDs and Integration Keys](external-ids-and-integration-keys.md) - External ID patterns for migration
- [ETL vs API vs Events](../integrations/etl-vs-api-vs-events.md) - Integration pattern selection

## Prerequisites

**Required Knowledge**:
- Understanding of Salesforce data model and object relationships
- Familiarity with data import tools (Data Import Wizard, Data Loader, Bulk API)
- Knowledge of External IDs and their use in record matching
- Understanding of data validation rules and required fields
- Basic knowledge of CSV file formats and data transformation

**Recommended Reading**:
- `rag/data-modeling/external-ids-and-integration-keys.md` - External ID patterns
- `rag/integrations/etl-vs-api-vs-events.md` - Integration pattern selection
- `rag/development/large-data-loads.md` - Large data volume handling
- `rag/integrations/callout-best-practices.md` - API call patterns

## Consensus Best Practices

- **Plan migrations carefully**: Understand data volume, relationships, and dependencies
- **Use external IDs**: Use external IDs for record matching and idempotent operations
- **Validate before migration**: Validate data quality before importing
- **Test with sample data**: Test migration with small datasets first
- **Implement rollback strategies**: Plan for data rollback in case of failures
- **Monitor migration progress**: Track migration status and detect failures
- **Handle errors gracefully**: Log errors and continue processing when possible

## Data Import Strategies

### Pattern 1: Data Import Wizard

**When to use**: Small datasets (up to 50,000 records), simple imports, non-technical users.

**Implementation approach**:
- Use Salesforce Data Import Wizard
- Prepare CSV files with required fields
- Map fields during import
- Review import results

**Why it's recommended**: Data Import Wizard is simple and doesn't require code. It's ideal for small, one-time imports.

**Key Points**:
- Limited to 50,000 records
- Manual process
- Good for simple imports
- No automation

### Pattern 2: Data Loader Patterns

**When to use**: Larger datasets, automated imports, command-line operations.

**Implementation approach**:
- Use Data Loader for bulk operations
- Prepare CSV files
- Use command-line for automation
- Handle errors and retries

**Why it's recommended**: Data Loader handles larger volumes and can be automated. It's ideal for regular imports and larger datasets.

**Key Points**:
- Handles millions of records
- Can be automated
- Command-line interface
- Error handling support

### Pattern 3: Bulk API for Migration

**When to use**: Very large datasets (millions of records), programmatic imports.

**Implementation approach**:
- Use Bulk API for large volumes
- Process in batches
- Handle job status and errors
- Implement retry logic

**Why it's recommended**: Bulk API is designed for large volumes and provides better performance than REST API. It's essential for large-scale migrations.

**Key Points**:
- Handles millions of records
- Asynchronous processing
- Better performance
- Requires programming

## Data Transformation Patterns

### Pattern 1: Field Mapping Strategies

**When to use**: Mapping fields from source system to Salesforce.

**Implementation approach**:
- Create field mapping configuration
- Transform data during import
- Handle data type conversions
- Map related records

**Why it's recommended**: Field mapping ensures data is correctly transformed and imported. This is essential for system migrations.

**Key Points**:
- Map source fields to target fields
- Handle data type conversions
- Map related records (lookups, master-detail)
- Validate mappings

### Pattern 2: Data Cleansing Patterns

**When to use**: Cleaning data before or during migration.

**Implementation approach**:
- Remove duplicates
- Standardize data formats
- Fix data quality issues
- Validate data before import

**Why it's recommended**: Data cleansing improves data quality and reduces errors during migration. This is essential for successful migrations.

**Key Points**:
- Remove duplicates
- Standardize formats
- Fix quality issues
- Validate data

### Pattern 3: Data Enrichment Patterns

**When to use**: Enriching data during migration with additional information.

**Implementation approach**:
- Add default values
- Calculate derived fields
- Enrich with related data
- Add timestamps and audit fields

**Why it's recommended**: Data enrichment adds value during migration and ensures complete records. This improves data quality.

**Key Points**:
- Add default values
- Calculate fields
- Enrich with related data
- Add audit fields

## Data Validation During Migration

### Pattern 1: Pre-Migration Validation

**When to use**: Validating data before starting migration.

**Implementation approach**:
- Validate data quality
- Check for duplicates
- Validate relationships
- Verify required fields

**Why it's recommended**: Pre-migration validation catches issues early and prevents failed migrations. This saves time and reduces errors.

**Key Points**:
- Validate before migration starts
- Check data quality
- Verify relationships
- Fix issues before import

### Pattern 2: During-Migration Validation

**When to use**: Validating data during migration process.

**Implementation approach**:
- Validate each record before import
- Handle validation errors
- Log validation failures
- Continue processing valid records

**Why it's recommended**: During-migration validation catches issues as they occur and allows processing to continue. This improves migration success rates.

**Key Points**:
- Validate each record
- Handle errors gracefully
- Log failures
- Continue processing

### Pattern 3: Post-Migration Validation

**When to use**: Validating data after migration completes.

**Implementation approach**:
- Compare record counts
- Validate data integrity
- Check relationships
- Verify business rules

**Why it's recommended**: Post-migration validation ensures migration success and data integrity. This is essential for production migrations.

**Key Points**:
- Compare counts
- Validate integrity
- Check relationships
- Verify business rules

## Rollback Strategies

### Pattern 1: Backup Strategies

**When to use**: Creating backups before migration.

**Implementation approach**:
- Export data before migration
- Store backups securely
- Document backup locations
- Test backup restoration

**Why it's recommended**: Backups enable rollback in case of migration failures. This is essential for production migrations.

**Key Points**:
- Export before migration
- Store securely
- Document locations
- Test restoration

### Pattern 2: Rollback Procedures

**When to use**: Rolling back data after migration failures.

**Implementation approach**:
- Identify records to rollback
- Delete or update records
- Restore from backup
- Verify rollback success

**Why it's recommended**: Rollback procedures enable recovery from migration failures. This is essential for production reliability.

**Key Points**:
- Identify records
- Delete or update
- Restore from backup
- Verify success

### Pattern 3: Data Recovery Patterns

**When to use**: Recovering data after migration issues.

**Implementation approach**:
- Identify affected records
- Restore from backup
- Re-import corrected data
- Verify recovery

**Why it's recommended**: Data recovery patterns enable recovery from migration issues. This ensures data integrity.

**Key Points**:
- Identify affected records
- Restore from backup
- Re-import data
- Verify recovery

## Migration Best Practices

### Migration Planning

- **Understand data volume**: Know how much data to migrate
- **Map relationships**: Understand record relationships
- **Plan dependencies**: Migrate in correct order
- **Estimate time**: Estimate migration duration

### Testing Strategies

- **Test with sample data**: Test with small datasets first
- **Test in sandbox**: Test migration in sandbox before production
- **Test rollback**: Test rollback procedures
- **Test validation**: Test validation logic

### Migration Monitoring

- **Track progress**: Monitor migration progress
- **Detect failures**: Identify and handle failures
- **Log operations**: Log all migration operations
- **Send notifications**: Notify on completion or failure

## Q&A

### Q: What is the best tool for importing data into Salesforce?

**A**: The best tool depends on data volume and requirements: **Data Import Wizard** for small datasets (up to 50,000 records) and simple imports, **Data Loader** for larger datasets and automated imports, **Bulk API** for very large datasets (millions of records) and programmatic control, **ETL tools** (MuleSoft, Boomi) for complex transformations and multi-system migrations.

### Q: How do I handle record relationships during migration?

**A**: Use **External IDs** to map relationships. Create External ID fields on parent objects, populate them with source system IDs, then reference those External IDs in child records. This enables idempotent operations and allows you to migrate parent records first, then child records referencing parent External IDs.

### Q: What is the recommended approach for validating data before migration?

**A**: Validate data **before migration** by: (1) Checking data quality (completeness, accuracy, format), (2) Validating relationships (parent records exist), (3) Checking business rules (validation rules, required fields), (4) Testing with sample data first, (5) Using staging objects for complex validation.

### Q: How do I implement rollback strategies for data migrations?

**A**: Implement rollback by: (1) **Backing up data** before migration, (2) **Logging all operations** (what was created/updated/deleted), (3) **Using External IDs** to track source records, (4) **Creating rollback scripts** that can reverse operations, (5) **Testing rollback procedures** in sandbox before production.

### Q: What is the difference between upsert and insert/update operations?

**A**: **Upsert** uses External IDs or a specified field to match existing records and update them, or create new records if no match is found. **Insert** always creates new records. **Update** requires existing record IDs. Use upsert for idempotent operations where you want to update existing records or create new ones based on External IDs.

### Q: How do I handle large data migrations (millions of records)?

**A**: For large migrations: (1) Use **Bulk API** or **Bulk API 2.0** for high-volume operations, (2) **Batch processing** - split into smaller batches, (3) **Parallel processing** - run multiple batches concurrently, (4) **Monitor progress** - track batch completion and failures, (5) **Error handling** - log errors and retry failed records, (6) **Test with sample data** first.

### Q: What should I consider when migrating data between Salesforce orgs?

**A**: When migrating between orgs: (1) **Field mapping** - map source fields to target fields, (2) **Data transformation** - transform data to match target org structure, (3) **Relationship preservation** - maintain relationships using External IDs, (4) **Permission considerations** - ensure user has access to create/update records, (5) **Validation rules** - understand target org validation rules, (6) **Test in sandbox** first.

### Q: How do I ensure data migration is idempotent?

**A**: Make migrations idempotent by: (1) **Using External IDs** for record matching, (2) **Using upsert operations** instead of insert/update, (3) **Checking for existing records** before creating, (4) **Logging operations** to track what was done, (5) **Testing with re-runs** to ensure same results.

## Edge Cases and Limitations

### Edge Case 1: Large Data Volumes (Millions of Records)

**Scenario**: Migrating millions of records that exceed Bulk API job limits or require extended processing time.

**Consideration**: 
- Use Bulk API 2.0 for very large datasets (supports larger job sizes)
- Implement chunking strategies (split into multiple jobs of 1-10 million records)
- Consider parallel processing with multiple Bulk API jobs
- Monitor job status and implement retry logic for failed jobs
- Use file-based staging for ID lists exceeding 50,000 records

### Edge Case 2: Complex Relationship Dependencies

**Scenario**: Migrating records with complex parent-child relationships where child records must reference parent records that don't exist yet.

**Consideration**:
- Migrate parent records first, then child records
- Use External IDs to establish relationships before parent records are fully created
- Implement dependency resolution logic to handle circular dependencies
- Use staging objects for complex relationship mapping
- Validate relationships after migration

### Edge Case 3: Data Type Mismatches and Format Issues

**Scenario**: Source system data types don't match Salesforce field types, or data formats are incompatible.

**Consideration**:
- Implement data transformation logic to convert data types
- Handle date/time format conversions and timezone issues
- Convert text to numbers, handle decimal precision
- Truncate text fields that exceed Salesforce field length limits
- Handle null values appropriately (empty strings vs. null)

### Edge Case 4: Validation Rule Failures During Migration

**Scenario**: Records fail validation rules during migration, causing partial failures.

**Consideration**:
- Review and understand target org validation rules before migration
- Pre-validate data against validation rules before import
- Use staging objects to validate data before moving to target objects
- Handle validation errors gracefully (log errors, continue processing valid records)
- Consider temporarily disabling validation rules for migration (if approved)

### Edge Case 5: Concurrent Migration Operations

**Scenario**: Multiple migration jobs running concurrently, causing lock contention or data conflicts.

**Consideration**:
- Coordinate migration jobs to avoid concurrent operations on same objects
- Use Bulk API job status to ensure jobs complete before starting new ones
- Implement locking mechanisms for critical migration operations
- Monitor for lock contention and adjust job scheduling
- Use serial processing for objects with high contention

### Limitations

- **Data Import Wizard**: Limited to 50,000 records per import, manual process, no automation
- **Data Loader**: Requires command-line access, limited error handling capabilities
- **Bulk API**: Not real-time (jobs run asynchronously), requires job status polling
- **Validation Rules**: Cannot be bypassed during standard data import (except via API with proper permissions)
- **Relationship Limits**: Master-detail relationships cannot be changed after record creation
- **Field Length Limits**: Text fields have maximum length limits (255-131,072 characters depending on field type)
- **API Limits**: Daily API limits constrain migration volume and frequency

## Related Patterns

- [External IDs and Integration Keys](external-ids-and-integration-keys.md) - External ID patterns
- [ETL vs API vs Events](../integrations/etl-vs-api-vs-events.md) - Integration patterns
- [Data Migration Examples](../code-examples/utilities/data-migration-examples.md) - Complete code examples

