# Core Terminology and Definitions

## Overview

This glossary defines core terms used throughout the RAG knowledge library. Terms are defined in the context of this architecture, integrations, and data models. All definitions are generic and avoid client- or org-specific names.

## Integration Terms

### ETL (Extract, Transform, Load)

**Definition**: Batch data synchronization pattern for high-volume data transfer between systems.

**Context**: Used for scheduled or on-demand synchronization of large data sets (hundreds of thousands of records). Typically implemented using integration platforms (Dell Boomi, MuleSoft) or Salesforce Bulk API.

**Related Patterns**: See `rag/integrations/etl-vs-api-vs-events.md` for when to use ETL vs. other patterns.

### API (Application Programming Interface)

**Definition**: Synchronous request/response integration pattern for real-time or near-real-time data exchange.

**Context**: Used when immediate feedback is required, lower volume per transaction, or user-initiated actions. Implemented using REST APIs, SOAP APIs, Named Credentials, or Custom Metadata Types.

**Related Patterns**: See `rag/integrations/etl-vs-api-vs-events.md` for API pattern selection.

### Platform Events

**Definition**: Salesforce event-driven integration mechanism for asynchronous, publish-subscribe patterns.

**Context**: Used for decoupled systems, multiple subscribers, asynchronous processing, and cross-system orchestration. Events are published from Flows and Apex, consumed internally via Channel Members, or forwarded to external event buses.

**Related Patterns**: See `rag/architecture/event-driven-architecture.md` for Platform Events implementation.

### External ID

**Definition**: Salesforce field marked as external ID, enabling idempotent upsert operations and stable record mapping.

**Context**: Used to map records between Salesforce and external systems. External IDs mirror external system primary keys and support retry logic, reconciliation, and partial syncs.

**Related Patterns**: See `rag/data-modeling/external-ids-and-integration-keys.md` for external ID design.

### Integration Key

**Definition**: Composite field or combination of fields used to uniquely identify records across systems.

**Context**: Used when external systems use multi-column primary keys. Composite external IDs concatenate multiple fields to create unique identifiers.

**Related Patterns**: See `rag/data-modeling/external-ids-and-integration-keys.md` for composite external ID patterns.

## Identity and SSO Terms

### OIDC (OpenID Connect)

**Definition**: Identity provider protocol for external users, typically used for citizen/client portals.

**Context**: Used for external user authentication in Experience Cloud portals. Supports state-wide citizen identity providers and external authentication systems.

**Related Patterns**: See `rag/identity-sso/multi-tenant-identity-architecture.md` for OIDC implementation.

### SAML (Security Assertion Markup Language)

**Definition**: Identity provider protocol for enterprise SSO, typically used for internal staff authentication.

**Context**: Used for internal staff authentication, institutional identity providers, and enterprise SSO scenarios.

**Related Patterns**: See `rag/identity-sso/multi-tenant-identity-architecture.md` for SAML implementation.

### Organization Tenant Identity

**Definition**: Identity provider pattern for external partner/provider authentication, supporting organization tenant relationships.

**Context**: Used for external partner/provider portals where users are associated with business organizations. Supports multi-tenant identity where external partners see only their associated organization's records.

**Related Patterns**: See `rag/identity-sso/multi-tenant-identity-architecture.md` for organization tenant identity patterns.

### Login Handler

**Definition**: Apex class that intercepts login events and routes users based on identity provider type.

**Context**: Used to detect login type (citizen vs. external partner vs. staff), route to appropriate landing pages, and tie authenticated identity back to the right Contact and Account records.

**Related Patterns**: See `rag/identity-sso/multi-tenant-identity-architecture.md` for login handler patterns.

## Data Model Terms

### SIS (Student Information System)

**Definition**: External system for student data, typically a legacy ERP or student management system.

**Context**: Used in higher education implementations. SIS systems typically provide student records, enrollments, courses, and academic data via batch synchronization.

**Related Patterns**: See `rag/integrations/sis-sync-patterns.md` for SIS synchronization patterns.

### EDA (Education Data Architecture)

**Definition**: Salesforce Education Cloud data model supporting higher education institutions.

**Context**: Uses Contact as core student record, Program Enrollment objects, Application objects, and Course Enrollment objects. Designed for SIS integration and student lifecycle management.

**Related Patterns**: See `rag/data-modeling/student-lifecycle-data-model.md` for EDA data model.

### Record Type

**Definition**: Salesforce mechanism for differentiating record types within the same object.

**Context**: Used to separate different user communities (citizen, external partner staff, internal staff), different account types (client, external partner, internal), and different case types. Enables Record Type-based routing and sharing rules.

**Related Patterns**: See `rag/identity-sso/multi-tenant-identity-architecture.md` for Record Type-based separation.

## Security Terms

### Permission Set

**Definition**: Salesforce mechanism for granting incremental permissions beyond profile settings.

**Context**: Used for permission set-driven security architecture. Profiles contain only UI configuration, while permission sets contain all access control. Supports role-based assignment via Permission Set Groups.

**Related Patterns**: See `rag/security/permission-set-architecture.md` for permission set patterns.

### Permission Set Group

**Definition**: Collection of permission sets grouped together for role-based assignment.

**Context**: Used to assign multiple permission sets to users based on their role. Simplifies permission management at scale.

**Related Patterns**: See `rag/security/permission-set-architecture.md` for permission set group patterns.

### Sharing Set

**Definition**: Experience Cloud mechanism for enforcing data visibility rules per user type.

**Context**: Used in portal implementations to ensure users see only their own records or records for their associated organizations. Replaces traditional sharing rules for portal users.

**Related Patterns**: See `rag/architecture/portal-architecture.md` for sharing set patterns.

## Platform Terms

### Experience Cloud

**Definition**: Salesforce portal/community platform for external user access.

**Context**: Used for student/applicant portals, external partner/provider portals, and citizen/client portals. Supports multiple user types with different identity providers, security requirements, and access patterns.

**Related Patterns**: See `rag/architecture/portal-architecture.md` for Experience Cloud patterns.

### GovCloud (Government Cloud)

**Definition**: Compliant cloud environment meeting government security and compliance requirements.

**Context**: Used for public sector implementations requiring specific compliance standards. Supports government cloud security requirements and audit trail needs.

**Related Patterns**: See `rag/development/error-handling-and-logging.md` for compliance logging requirements.

## Development Terms

### LWC (Lightning Web Component)

**Definition**: Modern Salesforce UI component framework for building reusable, performant user interfaces.

**Context**: Used for complex business logic components, console-style interfaces, fraud/risk scoring components, and program-selection components. Integrates with Apex via `@AuraEnabled` methods and `@wire` adapters.

**Related Patterns**: See `rag/development/lwc-patterns.md` for LWC patterns.

### OmniStudio

**Definition**: Salesforce OmniStudio for guided workflows (OmniScripts) and reusable UI components (FlexCards).

**Context**: Used for grant management workflows, guided processes, and reusable UI components. Integrates with Salesforce data model and supports complex business logic.

**Related Patterns**: See `rag/development/omnistudio-patterns.md` for OmniStudio patterns.

### Flow

**Definition**: Salesforce declarative automation tool for building business processes without code.

**Context**: Used for Record-Triggered Flows, Screen Flows, Subflows, Scheduled Flows, and Auto-Launched Flows. Preferred over Apex when possible, with Apex used for complex logic or performance requirements.

**Related Patterns**: See `rag/development/flow-patterns.md` for Flow patterns.

### Apex

**Definition**: Salesforce programming language for building custom business logic and integrations.

**Context**: Used when Flows are insufficient, heavy reuse is needed, tight control over performance is required, or complex algorithms are needed. Structured in layers: Service, Domain, Selector, Integration.

**Related Patterns**: See `rag/development/apex-patterns.md` for Apex patterns.

## Integration Platform Terms

### MuleSoft

**Definition**: Integration platform used as security boundary and transformation layer.

**Context**: Used for VPN/IP whitelisting, DataWeave transformations, and secure integration boundaries. Acts as intermediary between external systems and Salesforce.

**Related Patterns**: See `rag/integrations/integration-platform-patterns.md` for MuleSoft patterns.

### Dell Boomi

**Definition**: Integration platform used for high-volume ETL operations and batch processing.

**Context**: Used for file-based staging, dynamic SQL batching, and large-scale data synchronization. Optimized for high-volume batch operations.

**Related Patterns**: See `rag/integrations/integration-platform-patterns.md` for Boomi patterns.

## Data Quality Terms

### Idempotent Operation

**Definition**: Operation that can be safely repeated without changing the result beyond the initial application.

**Context**: Used in integration patterns to support retry logic. Upsert operations using external IDs are idempotent, allowing safe retries of failed integration jobs.

**Related Patterns**: See `rag/integrations/sis-sync-patterns.md` for idempotent upsert patterns.

### Reconciliation

**Definition**: Process of comparing data between Salesforce and external systems to identify discrepancies.

**Context**: Used to ensure data consistency across systems. Based on external IDs, integration job tracking, and field-level comparison.

**Related Patterns**: See `rag/troubleshooting/data-reconciliation.md` for reconciliation patterns.

## Project Method Terms

### Sprint-Based Delivery

**Definition**: Agile delivery approach using time-boxed sprints for managing complex multi-stakeholder projects.

**Context**: Used for coordinating stakeholder work, testing windows, change management, and quality standards. Supports iterative delivery with regular stakeholder coordination.

**Related Patterns**: See `rag/project-methods/delivery-framework.md` for sprint-based delivery patterns.

### UAT (User Acceptance Testing)

**Definition**: Testing phase where end users validate that the system meets business requirements.

**Context**: Used to validate Salesforce configurations, integrations, and portal functionality across multiple environments. Includes integration testing, data quality testing, and user migration testing.

**Related Patterns**: See `rag/project-methods/testing-strategy.md` for testing strategies.

## Related Documentation

For domain-specific terminology and definitions, see:

- **Integration Terms**: `rag/integrations/etl-vs-api-vs-events.md`
- **Identity Terms**: `rag/identity-sso/multi-tenant-identity-architecture.md`
- **Data Model Terms**: `rag/data-modeling/student-lifecycle-data-model.md`
- **Security Terms**: `rag/security/permission-set-architecture.md`
- **Development Terms**: `rag/development/apex-patterns.md`, `rag/development/flow-patterns.md`, `rag/development/lwc-patterns.md`

