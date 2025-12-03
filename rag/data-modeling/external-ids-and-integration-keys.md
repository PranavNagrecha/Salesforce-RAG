---
title: "External IDs and Integration Keys"
level: "Intermediate"
tags:
  - data-modeling
  - external-ids
  - integration-keys
  - data-sync
last_reviewed: "2025-01-XX"
---

# External IDs and Integration Keys

## Overview

External ID strategies enable stable record mapping between Salesforce and external systems, supporting idempotent data synchronization and reliable integration patterns. External IDs mirror external system primary keys and enable safe retry operations.

## External ID Design Principles

### Always Use External IDs

External IDs should be used for all objects that receive data from integrations:

- Enable idempotent upsert operations
- Support retry logic for failed integration jobs
- Allow partial syncs without data loss
- Enable reconciliation between Salesforce and external systems

### Stable and Unique Design

External IDs should be stable and unique:

- Mirror external system primary keys
- Don't change when individual component fields change
- Remain consistent across integration runs
- Support long-term record correlation

### Composite External IDs

Use composite external IDs when external systems use multi-column primary keys:

- Account-level external IDs using composite keys (e.g., Institution + Program + Effective Date)
- Concatenate multiple fields to create unique external IDs
- Support effective-dated records where the same logical record has multiple versions over time
- Handle null values in component fields appropriately

## External ID Field Configuration

### Field Naming Conventions

Use consistent naming patterns:

- `External_ID__c` or `External_System_ID__c` for single-system integrations
- Include system identifier when multiple systems integrate (e.g., `SIS_External_ID__c`)
- Document external ID source and format in field help text
- Follow organizational naming standards

### Field Type and Configuration

Configure external ID fields appropriately:

- Use Text fields (not Number) to preserve leading zeros and special characters
- Set appropriate field length based on external system identifier format
- Mark external ID fields as "External ID" in field definition for upsert support
- Consider making external ID fields required if records always come from integration

### Field Documentation

Document external ID fields comprehensively:

- Document external ID source (which external system)
- Document external ID format and structure
- Document uniqueness guarantees
- Document any transformation or mapping rules

## Composite External ID Construction

### Delimiter Selection

Choose appropriate delimiter for composite keys:

- Use delimiter that doesn't appear in component field values (e.g., pipe `|` or dash `-`)
- Ensure delimiter is consistent across all composite external IDs
- Document delimiter choice and rationale

### Null Value Handling

Handle null values in component fields:

- Use empty string or placeholder for null values
- Ensure null handling doesn't create duplicate external IDs
- Document null handling approach

### Effective Date Handling

Consider effective dates for time-versioned records:

- Include effective date in composite key when records are time-versioned
- Support multiple versions of the same logical record
- Handle effective date changes appropriately

### Validation

Validate composite key uniqueness:

- Ensure composite keys are unique before using as external ID
- Implement validation rules to prevent duplicate composite keys
- Test composite key construction with sample data

## Integration Job Tracking Fields

### Standard Tracking Fields

Add these standard fields to all objects that receive data from integrations:

- **`Last_Sync_Timestamp__c`** (DateTime): When record was last synced
- **`Last_Sync_Status__c`** (Picklist: Success, Error, In Progress): Sync job status
- **`Last_Sync_Error__c`** (Long Text Area): Error message if sync failed
- **`Integration_Job_ID__c`** (Text): Correlation ID with external system
- **`Record_Source__c`** (Picklist: Integration, Manual Entry, Migration): How record was created

### Usage of Tracking Fields

Use tracking fields for:

- Troubleshooting integration failures
- Identifying records that haven't synced recently
- Correlating Salesforce records with external system job logs
- Building dashboards showing integration health
- Auditing data changes and integration activity

## Idempotent Upsert Pattern

### Upsert Operations

Use external IDs in upsert operations:

- Enable idempotent synchronization
- Support safe retry of failed operations
- Prevent duplicate record creation
- Enable partial syncs without data loss

### Error Handling

Handle upsert errors gracefully:

- Handle duplicate external IDs appropriately
- Handle validation failures
- Log upsert results for monitoring
- Support partial upserts (some records succeed, others fail)

### Retry Logic

Implement retry logic for failed upserts:

- Retry transient failures
- Use exponential backoff for retries
- Track retry attempts
- Escalate persistent failures

## Multi-System External ID Management

### System-Specific External IDs

When integrating with multiple systems:

- Use system-specific external ID fields (e.g., `SIS_External_ID__c`, `ERP_External_ID__c`)
- Document which system is the source of truth for each external ID
- Create master external ID mapping object if needed
- Implement reconciliation processes for external ID conflicts

### External ID Mapping

Maintain mapping between external IDs:

- Track external ID relationships across systems
- Document external ID mapping rules
- Implement validation for external ID consistency
- Support external ID migration when needed

## Best Practices

### External ID Design

- Always use external IDs for integrated objects
- Design external IDs to be stable and unique
- Use composite external IDs when needed
- Document external ID strategy for each object

### Integration Tracking

- Add standard tracking fields to all integrated objects
- Use tracking fields for troubleshooting and monitoring
- Build dashboards showing integration health
- Implement alerts for integration failures

### Error Handling

- Handle upsert errors gracefully
- Implement retry logic for transient failures
- Log all integration operations
- Support partial syncs without data loss

### Documentation

- Document external ID source and format
- Document composite key construction logic
- Document integration job tracking field usage
- Document external ID migration procedures

## Migration Strategy

### External ID Migration

When external IDs need to change:

- Create new external ID fields alongside old ones
- Migrate records in batches using Data Loader or ETL tools
- Update all integrations to use new external ID fields
- Validate data integrity after migration
- Deprecate old external ID fields only after all records are migrated

### Validation

Validate external ID migration:

- Verify all records have new external IDs
- Test integration operations with new external IDs
- Monitor integration health after migration
- Document migration results

## Tradeoffs

### Advantages

- **Idempotency**: Safe retry operations
- **Stability**: Consistent record mapping
- **Reconciliation**: Easy to reconcile between systems
- **Error Recovery**: Support for partial syncs

### Challenges

- **Complexity**: Composite keys add complexity
- **Migration**: Changing external IDs requires migration
- **Validation**: Requires validation to ensure uniqueness
- **Documentation**: Requires comprehensive documentation

## When to Use External IDs

Use external IDs when:

- Integrating with external systems
- Need idempotent upsert operations
- Require stable record mapping
- Need to support retry logic
- Require reconciliation between systems

## When Not to Use External IDs

Avoid external IDs when:

- Records are only created in Salesforce
- No external system integration exists
- External system doesn't provide stable identifiers
- Migration effort outweighs benefits

## Q&A

### Q: Why are External IDs important for integrations?

**A**: External IDs enable idempotent upsert operations, support retry logic for failed integration jobs, allow partial syncs without data loss, and enable reconciliation between Salesforce and external systems. They provide stable record mapping that survives integration failures and retries.

### Q: What makes a good External ID?

**A**: A good External ID is **stable** (doesn't change when component fields change), **unique** (uniquely identifies records), **mirrors external system primary keys**, and **remains consistent** across integration runs. It should support long-term record correlation.

### Q: When should I use composite External IDs?

**A**: Use composite External IDs when external systems use multi-column primary keys, when you need account-level external IDs using composite keys (e.g., Institution + Program + Effective Date), or when handling effective-dated records where the same logical record has multiple versions over time.

### Q: How do I handle null values in composite External IDs?

**A**: Handle null values by using default values (e.g., "NULL" or empty string), excluding null fields from the composite key, or using separate External ID fields for different scenarios. Document the null handling strategy in field help text.

### Q: What is the difference between External IDs and Integration Keys?

**A**: **External IDs** are fields marked with the "External ID" attribute that enable upsert operations. **Integration Keys** are the actual values stored in External ID fields that uniquely identify records in external systems. External IDs are the mechanism; Integration Keys are the values.

### Q: How do I migrate existing records to use External IDs?

**A**: Create External ID fields, populate them with values from external systems (or generate stable values), mark fields as External IDs, test upsert operations, and update integration code to use External IDs. Migrate incrementally and test thoroughly.

### Q: Can I have multiple External ID fields on the same object?

**A**: Yes, you can have multiple External ID fields on the same object. This is useful when integrating with multiple external systems (e.g., `SIS_External_ID__c`, `ERP_External_ID__c`). Each External ID field should be clearly named to indicate its source system.

### Q: What happens if an External ID value changes in the external system?

**A**: If External ID values change in the external system, you'll need to update the External ID field values in Salesforce. This can break record correlation. Design External IDs to be stable - they should mirror external system primary keys that don't change.

