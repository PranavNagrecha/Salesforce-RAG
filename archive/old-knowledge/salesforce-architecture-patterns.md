# Salesforce Architecture Patterns

## What Was Actually Done

Several core architecture patterns were implemented across different projects to solve common Salesforce design challenges around multi-tenancy, user management, data routing, and integration observability.

### Login Handler and User Creation Patterns

Custom login handlers were implemented to manage user creation and identity mapping across multiple identity providers. The handlers:

- Match external identity provider GUIDs to existing Contacts using email and external ID fields
- Prevent duplicate Contact/User creation when users first log in after migration
- Route users to appropriate landing pages based on their identity provider type
- Maintain consistent Account/Contact ownership relationships during identity attachment

### Record Type and Process Separation

Record Types were used extensively to separate business processes and data models within a single org:

- Different Record Types for Account (client, vendor, internal organization) and Contact (citizen, vendor staff, internal staff)
- Process Builder and Flow logic that branches based on Record Type
- Sharing rules and field-level security that vary by Record Type
- Custom picklist values that are Record Type-specific

### Queue and Routing Patterns

Queue-based routing was implemented for case and service request management:

- Queues organized by function (intake, triage, specialized teams) rather than as catch-all dumping grounds
- Assignment rules that route cases to appropriate queues based on criteria
- Escalation rules tied to queue-specific SLAs
- Reporting dashboards to monitor queue performance and identify bottlenecks

### Soft-Delete and Archival Patterns

Soft-delete patterns were implemented for data retention and compliance:

- Custom "Archived" or "Deleted" status fields instead of hard deletes
- Archival processes that move records to archive objects or mark them as inactive
- Retention policies that determine when records can be permanently deleted
- Reporting that excludes archived records by default but allows historical analysis

### Integration Observability and Job Tracking

Standard fields were added to integrated objects for tracking integration job status:

- Last sync timestamp fields
- Last sync status fields (Success, Error, In Progress)
- Last sync error message fields for troubleshooting
- Integration job ID fields for correlation with external system logs
- Record source fields to identify whether a record came from integration vs. manual entry

## Rules and Patterns

### Login Handler Design

- Always check for existing Contacts by external ID before creating new records
- Use email as a secondary matching criterion when external ID is not available
- Log all login handler operations for troubleshooting identity mapping issues
- Handle edge cases where external identity exists but Salesforce Contact does not (and vice versa)
- Route users to Record Type-appropriate landing pages based on identity provider type

### Record Type Strategy

- Use Record Types to separate business processes, not just to change picklist values
- Design Record Types early; changing them later requires data migration
- Create Record Type-specific Flows and Process Builder logic to avoid complex conditional branches
- Use Record Type in sharing rules and field-level security for data isolation
- Document the business purpose of each Record Type clearly

### Queue Management

- Define clear responsibility per queue (what types of cases belong where)
- Set SLA expectations per queue and configure escalation rules accordingly
- Avoid catch-all queues; if a queue receives everything, it's not serving its purpose
- Use reporting to monitor queue performance and refine routing rules iteratively
- Map contact center queues to Salesforce queues for CTI integrations

### Soft-Delete Implementation

- Use status fields or custom "IsDeleted" flags instead of hard deletes for compliance
- Create archive objects or archive orgs for long-term data retention
- Implement data retention policies that determine archival timing
- Ensure reporting excludes archived records by default
- Document the archival process and retention periods

### Integration Job Tracking

Add these standard fields to all objects that receive data from integrations:
- `Last_Sync_Timestamp__c` (DateTime)
- `Last_Sync_Status__c` (Picklist: Success, Error, In Progress)
- `Last_Sync_Error__c` (Long Text Area)
- `Integration_Job_ID__c` (Text)
- `Record_Source__c` (Picklist: Integration, Manual Entry, Migration)

Use these fields to:
- Troubleshoot integration failures
- Identify records that haven't synced recently
- Correlate Salesforce records with external system job logs
- Build dashboards showing integration health

## Suggested Improvements (From AI)

### Centralized Assignment Engine

Instead of hard-coding queue IDs in Flows and Apex, consider:
- Custom metadata or custom objects to define assignment rules
- A single shared assignment engine (Apex class or Flow) that all automation calls
- Configuration-driven routing that can be updated without code changes
- A/B testing capabilities for routing rule effectiveness

### Enhanced Integration Observability

Build a comprehensive integration monitoring solution:
- Custom object to track all integration job executions with start time, end time, record count, error count
- Dashboard showing integration health across all integrated systems
- Automated alerts when integration jobs fail or exceed expected duration
- Integration with external monitoring tools (e.g., Splunk, DataDog) for cross-system correlation

### Record Type Migration Strategy

When Record Types need to change:
- Create new Record Types alongside old ones
- Migrate records in batches using Data Loader or ETL tools
- Update all automation to handle both old and new Record Types during transition
- Validate data integrity after migration
- Deprecate old Record Types only after all records are migrated

## To Validate

- Specific login handler code patterns and error handling approaches
- Exact Record Type structure used in production (names and purposes)
- Queue naming conventions and how they map to organizational teams
- Soft-delete implementation details and retention policy specifics
- Integration job tracking field names and whether they follow a naming convention

