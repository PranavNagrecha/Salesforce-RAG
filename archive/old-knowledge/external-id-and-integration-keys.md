# External ID and Integration Key Strategies

## What Was Actually Done

External ID strategies were designed to support stable record mapping between Salesforce and external systems, enabling idempotent data synchronization and reliable integration patterns.

### Composite External ID Strategy

Composite external IDs were implemented for objects where external systems use multi-column primary keys:

- Account-level external IDs using composite keys (e.g., Institution + Program + Effective Date)
- Concatenation of multiple fields to create unique external IDs
- Stable external IDs that don't change when individual component fields change
- Support for effective-dated records where the same logical record has multiple versions over time

### External ID Field Naming

External ID fields were named consistently:

- Using `External_ID__c` or `External_System_ID__c` naming patterns
- Including system identifier in field name when multiple systems integrate (e.g., `SIS_External_ID__c`)
- Documenting external ID source and format in field help text
- Using Text fields with appropriate length for external system identifiers

### Integration Job Tracking Fields

Standard fields were added to integrated objects for tracking integration job execution:

- `Last_Sync_Timestamp__c` (DateTime) - when record was last synced
- `Last_Sync_Status__c` (Picklist: Success, Error, In Progress) - sync job status
- `Last_Sync_Error__c` (Long Text Area) - error message if sync failed
- `Integration_Job_ID__c` (Text) - correlation ID with external system
- `Record_Source__c` (Picklist: Integration, Manual Entry, Migration) - how record was created

### External ID for Idempotent Upserts

External IDs were used extensively for idempotent upsert operations:

- Enabling ETL processes to insert or update records without duplicates
- Supporting retry logic for failed integration jobs
- Allowing partial syncs without data loss
- Enabling reconciliation between Salesforce and external systems

## Rules and Patterns

### External ID Design Principles

- Always use external IDs for objects that receive data from integrations
- Design external IDs to be stable and unique (mirror external system primary keys)
- Use composite external IDs when external systems use multi-column keys
- Include system identifier in field name when multiple systems integrate
- Document external ID source, format, and uniqueness guarantees

### Composite External ID Construction

- Concatenate component fields with a delimiter (e.g., pipe `|` or dash `-`)
- Ensure delimiter doesn't appear in component field values
- Handle null values in component fields (use empty string or placeholder)
- Consider effective dates when constructing composite keys for time-versioned records
- Validate composite key uniqueness before using as external ID

### Integration Job Tracking

Add these standard fields to all objects that receive data from integrations:
- `Last_Sync_Timestamp__c` (DateTime) - tracks when record was last updated by integration
- `Last_Sync_Status__c` (Picklist: Success, Error, In Progress) - current sync job status
- `Last_Sync_Error__c` (Long Text Area) - detailed error message for troubleshooting
- `Integration_Job_ID__c` (Text) - correlation ID linking to external system job logs
- `Record_Source__c` (Picklist: Integration, Manual Entry, Migration) - record origin

Use these fields to:
- Troubleshoot integration failures
- Identify records that haven't synced recently
- Correlate Salesforce records with external system job logs
- Build dashboards showing integration health
- Audit data changes and integration activity

### External ID Field Configuration

- Mark external ID fields as "External ID" in field definition for upsert support
- Set appropriate field length based on external system identifier format
- Use Text fields (not Number) to preserve leading zeros and special characters
- Add field help text documenting external ID source and format
- Consider making external ID fields required if records always come from integration

### Idempotent Upsert Pattern

- Use external IDs in upsert operations to enable idempotent synchronization
- Handle upsert errors gracefully (duplicate external IDs, validation failures)
- Log upsert results for monitoring and troubleshooting
- Support partial upserts (some records succeed, others fail)
- Implement retry logic for failed upserts

## Suggested Improvements (From AI)

### External ID Validation

Implement external ID validation:
- Validation rules to ensure external IDs match expected format
- Apex triggers to validate external ID uniqueness
- Data quality checks to identify invalid external IDs
- Automated reconciliation processes to find orphaned records

### Enhanced Integration Tracking

Build comprehensive integration tracking:
- Custom object to track all integration job executions with metrics
- Dashboard showing integration health across all integrated systems
- Automated alerts when integration jobs fail or exceed expected duration
- Integration with external monitoring tools for cross-system correlation
- Historical tracking of integration performance trends

### External ID Migration Strategy

When external IDs need to change:
- Create new external ID fields alongside old ones
- Migrate records in batches using Data Loader or ETL tools
- Update all integrations to use new external ID fields
- Validate data integrity after migration
- Deprecate old external ID fields only after all records are migrated

### Multi-System External ID Management

When integrating with multiple systems:
- Use system-specific external ID fields (e.g., `SIS_External_ID__c`, `ERP_External_ID__c`)
- Create a master external ID mapping object if needed
- Document which system is the source of truth for each external ID
- Implement reconciliation processes for external ID conflicts

## To Validate

- Specific external ID field names and composite key structures
- External ID field naming conventions and standards
- Integration job tracking field implementations
- Composite external ID construction logic and delimiter choices
- External ID validation rules and error handling
- Multi-system external ID management approach

