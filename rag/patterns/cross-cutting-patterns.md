# Cross-Cutting Design Patterns

## Overview

This document summarizes reusable patterns that appear across multiple domains in the architecture. These patterns are fundamental to how the system operates and should be considered when implementing features in any domain.

**Note**: This file links to detailed domain-specific documentation. It does not duplicate full content but provides a "pattern table of contents" showing how different pieces of the architecture fit together.

## Governor Limit Management

### Pattern Summary

Governor limits are a fundamental constraint in Salesforce. All code and automation must be designed to handle bulk operations and respect platform limits.

### Where This Pattern Appears

- **Apex Development**: See `rag/development/apex-patterns.md` for SOQL optimization, bulkification, and asynchronous patterns
- **Flow Development**: See `rag/development/flow-patterns.md` for bulk Flow patterns and collection processing
- **Integration Patterns**: See `rag/integrations/etl-vs-api-vs-events.md` for batch processing patterns
- **Troubleshooting**: See `rag/troubleshooting/integration-debugging.md` for limit-related debugging

### Key Principles

- Always process collections, never single records in loops
- Use selective WHERE clauses with indexed fields
- Leverage asynchronous processing (Queueable, Batchable, Scheduled) for large operations
- Test with maximum data volumes (200+ records minimum)
- Monitor and log limit usage for optimization

### Common Anti-Patterns

- SOQL or DML inside loops
- Processing records one at a time
- Not testing with bulk data
- Ignoring query selectivity warnings

## Bulkification Patterns

### Pattern Summary

All automation must handle bulk operations efficiently, processing collections rather than individual records.

### Where This Pattern Appears

- **Apex Development**: See `rag/development/apex-patterns.md` for Apex bulkification patterns
- **Flow Development**: See `rag/development/flow-patterns.md` for Record-Triggered Flow bulk patterns
- **Integration Patterns**: See `rag/integrations/sis-sync-patterns.md` for batch synchronization patterns

### Key Principles

- Design all triggers, Flows, and Apex to handle 200+ records
- Use bulk DML operations (insert, update, upsert with collections)
- Process related records in batches
- Avoid nested loops when possible

### Implementation Checklist

- [ ] All triggers process `Trigger.new` or `Trigger.old` collections
- [ ] All Flows use collection variables and loops
- [ ] All Apex methods accept and process collections
- [ ] All integration jobs handle batch processing

## External ID and Integration Key Patterns

### Pattern Summary

External IDs provide stable record mapping between Salesforce and external systems, enabling idempotent operations and reliable integrations.

### Where This Pattern Appears

- **Data Modeling**: See `rag/data-modeling/external-ids-and-integration-keys.md` for comprehensive external ID design
- **Integration Patterns**: See `rag/integrations/sis-sync-patterns.md` for external ID usage in batch sync
- **Troubleshooting**: See `rag/troubleshooting/data-reconciliation.md` for external ID-based reconciliation

### Key Principles

- Use external IDs for all objects receiving integration data
- Mirror external system primary keys
- Support composite external IDs for multi-column keys
- Enable idempotent upsert operations
- Track integration job metadata (timestamps, status)

### Common Use Cases

- SIS synchronization with stable student record mapping
- Multi-system integration with different external ID sources
- Reconciliation between Salesforce and external systems
- Retry logic for failed integration jobs

## Error Handling and Logging Patterns

### Pattern Summary

Comprehensive error handling and logging ensures all errors are captured, logged, and traceable for troubleshooting and compliance.

### Where This Pattern Appears

- **Development**: See `rag/development/error-handling-and-logging.md` for complete logging framework
- **Integration Patterns**: See `rag/integrations/integration-platform-patterns.md` for integration error handling
- **Troubleshooting**: See `rag/troubleshooting/integration-debugging.md` for error investigation patterns

### Key Principles

- All errors must be logged to `LOG_LogMessage__c` object
- Use platform event fallback if DML fails
- Include structured context (source, function, payload)
- Support different log levels (Debug, Info, Warning, Error, Fatal)
- Integrate with centralized logging platforms (OpenSearch, Splunk)

### Implementation Checklist

- [ ] All DML operations wrapped in try-catch blocks
- [ ] All integration errors logged with context
- [ ] Platform event fallback configured for logging failures
- [ ] Logs queryable for troubleshooting and reporting

## Data Quality and Deduplication Patterns

### Pattern Summary

Data quality patterns ensure clean, deduplicated data across the system, supporting reliable matching and reconciliation.

### Where This Pattern Appears

- **Data Modeling**: See `rag/data-modeling/external-ids-and-integration-keys.md` for external ID-based matching
- **Integration Patterns**: See `rag/integrations/sis-sync-patterns.md` for idempotent upsert patterns
- **Troubleshooting**: See `rag/troubleshooting/data-reconciliation.md` for data quality validation
- **Project Methods**: See `rag/project-methods/testing-strategy.md` for data quality testing

### Key Principles

- Use external IDs for stable record matching
- Implement idempotent operations (upsert, not insert)
- Track data quality metrics (matching rates, error rates)
- Support reconciliation workflows for discrepancy identification
- Handle edge cases (null values, format differences)

### Common Scenarios

- Matching Contacts from multiple systems
- Deduplicating Accounts across integration sources
- Reconciling data between Salesforce and external systems
- Validating data quality during testing

## Security and Sharing Patterns

### Pattern Summary

Security patterns ensure proper access control and data isolation across multi-tenant implementations and portal architectures.

### Where This Pattern Appears

- **Security**: See `rag/security/permission-set-architecture.md` for permission set-driven security
- **Identity & SSO**: See `rag/identity-sso/multi-tenant-identity-architecture.md` for identity-based access control
- **Portal Architecture**: See `rag/architecture/portal-architecture.md` for portal sharing patterns

### Key Principles

- Use permission sets for access control (not profiles)
- Separate external and internal permission sets
- Use Record Types for data separation
- Implement sharing sets for portal users
- Enforce field-level and object-level security in SOQL

### Implementation Checklist

- [ ] Profiles contain only UI configuration
- [ ] Permission sets contain all access control
- [ ] Portal users have separate permission sets
- [ ] Sharing sets enforce data visibility rules
- [ ] All SOQL queries use `WITH SECURITY_ENFORCED`

## Integration Pattern Selection

### Pattern Summary

Different integration patterns (ETL, API, Events) serve different use cases. Understanding when to use each pattern is critical for scalable integrations.

### Where This Pattern Appears

- **Integration Patterns**: See `rag/integrations/etl-vs-api-vs-events.md` for comprehensive decision framework
- **Architecture**: See `rag/architecture/event-driven-architecture.md` for event-driven patterns
- **Integration Platforms**: See `rag/integrations/integration-platform-patterns.md` for platform-specific patterns

### Key Principles

- **ETL**: Use for high-volume batch synchronization (hundreds of thousands of records)
- **API**: Use for real-time request/response requiring immediate feedback
- **Events**: Use for asynchronous, decoupled processing with multiple subscribers
- Consider hybrid patterns when appropriate
- Design for idempotency and retry logic

### Decision Framework

1. **Volume**: High volume → ETL, Low volume → API or Events
2. **Timing**: Scheduled → ETL, Real-time → API, Asynchronous → Events
3. **Coupling**: Tight coupling → API, Loose coupling → Events
4. **Subscribers**: Single → API or ETL, Multiple → Events

## Portal Design Patterns

### Pattern Summary

Portal architecture patterns support multiple user types with different identity providers, security requirements, and access patterns.

### Where This Pattern Appears

- **Portal Architecture**: See `rag/architecture/portal-architecture.md` for comprehensive portal patterns
- **Identity & SSO**: See `rag/identity-sso/multi-tenant-identity-architecture.md` for identity-aware routing
- **Security**: See `rag/security/permission-set-architecture.md` for portal security patterns

### Key Principles

- Support multiple user types (students, external partners, citizens, staff) in single org
- Use identity-aware routing based on login type
- Implement Record Type-based separation for different user communities
- Use sharing sets to enforce data visibility per user type
- Separate portal and internal permission sets

### Common Anti-Patterns

- Self-registration with no data model plan
- Relying only on email for identity
- Overly broad sharing sets
- Portal and internal users sharing permission sets
- No logging of portal failures

## Testing and Quality Patterns

### Pattern Summary

Comprehensive testing strategies validate configurations, integrations, and functionality across multiple environments.

### Where This Pattern Appears

- **Project Methods**: See `rag/project-methods/testing-strategy.md` for complete testing framework
- **Development**: See `rag/development/apex-patterns.md` for Apex testing patterns
- **Troubleshooting**: See `rag/troubleshooting/integration-debugging.md` for testing-related debugging

### Key Principles

- Test with bulk data (200+ records minimum)
- Include both positive and negative test cases
- Test integration connectivity, transformation, and error handling
- Validate data quality (matching, deduplication, error capture)
- Test user migration and login handlers
- Coordinate testing windows across stakeholders

### Testing Checklist

- [ ] Unit tests with bulk data (200+ records)
- [ ] Integration tests for all integration points
- [ ] Data quality tests for matching and deduplication
- [ ] User migration tests for identity providers
- [ ] Portal functionality tests for all user types

## Related Patterns

These patterns often work together:

- **External IDs + Bulkification**: External IDs enable efficient bulk upsert operations
- **Error Handling + Logging**: Comprehensive logging supports error investigation
- **Security + Portal Design**: Security patterns enable multi-tenant portal implementations
- **Integration Patterns + Data Quality**: Integration patterns must support data quality requirements
- **Testing + All Patterns**: Testing validates that all patterns work correctly together

## To Validate

- Advanced governor limit optimization techniques
- Change Data Capture (CDC) patterns for real-time synchronization
- Marketing Cloud integration patterns
- Contact center integration patterns
- ITSM/Incident Management integration patterns

