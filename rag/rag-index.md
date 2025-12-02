# RAG Knowledge Library Index

## Overview

This RAG (Retrieval-Augmented Generation) knowledge library contains structured knowledge derived from real Salesforce implementation experience. All content has been sanitized to remove identifying information and organized for efficient retrieval by AI systems.

## How to use this index

- **LLMs or tools** can use this file to decide which `rag/**` docs to retrieve for a given question.
- **Humans** can skim domains to understand what knowledge is available.
- **See the README** and `examples/` folder for details on using this repository with Cursor and other RAG frameworks.

## Directory Structure

```
rag/
├── architecture/          # System architecture patterns
├── integrations/          # Integration patterns and platforms
├── identity-sso/         # Identity and SSO patterns
├── data-modeling/        # Data modeling patterns
├── security/             # Security and access control patterns
├── operations/            # Delivery & operations patterns
├── observability/         # Observability & resilience patterns
├── data-governance/      # Data governance & compliance patterns
├── adoption/              # Adoption & change management patterns
├── project-methods/      # Project delivery and methodology
├── development/          # Development patterns and practices
├── testing/              # Testing patterns and examples
├── troubleshooting/      # Debugging and troubleshooting
├── patterns/             # Reusable design patterns
├── glossary/             # Terminology and definitions
├── code-examples/        # Complete, working code examples
├── quick-start/          # Quick-start guides
├── api-reference/        # API references and method signatures
├── mcp-knowledge/        # MCP-extracted knowledge
└── rag-index.md          # This file
```

## Architecture Patterns

Architecture patterns for designing system structure, integration patterns, multi-tenant solutions, and portal architecture.

- [event-driven-architecture.md](architecture/event-driven-architecture.md) — Guide to implementing event-driven architecture with Platform Events, including event publication, payload design, and integration with external event buses
- [portal-architecture.md](architecture/portal-architecture.md) — Experience Cloud portal architecture patterns for multiple user communities with different identity providers and security requirements

### event-driven-architecture.md

**When to Retrieve**: How to implement Platform Events for asynchronous integration, designing event-driven architecture to decouple systems, publishing events from Flows or Apex, integrating with external event buses, or designing event payloads.

**Summary**: Guide to implementing event-driven architecture with Platform Events. Teaches how to publish events from Flows and Apex, design self-contained event payloads, integrate with external event buses, consume events internally, and handle errors. Includes decision framework for when to use events vs. APIs vs. ETL.

**Key Topics**:
- Platform Events publication from Flows and Apex
- External event bus patterns (EventBridge)
- Event payload design (self-contained, minimal PII, idempotent)
- Internal event consumption via Channel Members
- Error handling and monitoring patterns

### portal-architecture.md

**When to Retrieve**: Designing Experience Cloud portals for multiple user communities, supporting different user types in one portal, implementing identity-aware routing, or designing portal security and sharing models.

**Summary**: Architecture patterns for Experience Cloud portals that support multiple user communities (students/applicants, external partners/providers, citizens/clients) with different identity providers, security requirements, and access patterns. Covers identity-aware routing, sharing models, and portal design patterns.

**Key Topics**:
- Student/applicant portal patterns
- External partner/provider portal patterns
- Citizen/client portal patterns
- Identity-aware behavior and routing
- Sharing and security for portals

## Integration Patterns

Integration patterns and platforms for ETL, API, and event-driven integrations, SIS synchronization, integration platforms like MuleSoft and Dell Boomi, and Salesforce to LLM data pipelines.

- [etl-vs-api-vs-events.md](integrations/etl-vs-api-vs-events.md) — Decision framework for choosing between ETL (batch), API (synchronous), or Events (asynchronous) integration patterns
- [integration-platform-patterns.md](integrations/integration-platform-patterns.md) — Patterns for implementing integrations using MuleSoft and Dell Boomi platforms as security boundaries and transformation layers
- [sis-sync-patterns.md](integrations/sis-sync-patterns.md) — High-volume batch synchronization patterns for integrating with Student Information Systems using file-based staging and idempotent upserts
- [salesforce-to-llm-data-pipelines.md](integrations/salesforce-to-llm-data-pipelines.md) — Pipeline patterns for extracting, transforming, and loading Salesforce data and metadata into LLM-powered systems (RAG, tools, agents)
- [change-data-capture-patterns.md](integrations/change-data-capture-patterns.md) — Change Data Capture patterns: CDC event processing, Platform Event integration, error handling, replay strategies, and real-time integration patterns
- [integration-user-license-guide.md](integrations/integration-user-license-guide.md) — Comprehensive guide to Salesforce Integration User Licenses (free API-only license): setup, authentication, permissions, security, and best practices

### etl-vs-api-vs-events.md

**When to Retrieve**: Deciding whether to use ETL, API, or Events for an integration, understanding tradeoffs between batch/synchronous/asynchronous patterns, or selecting the right integration pattern for a use case.

**Summary**: Decision framework for choosing integration patterns. Explains when to use ETL (high-volume batch), API (real-time request/response), or Events (asynchronous publish-subscribe), with implementation patterns, best practices, and tradeoffs for each approach.

**Key Topics**:
- ETL pattern for high-volume batch synchronization
- API pattern for real-time request/response
- Events pattern for asynchronous processing
- Hybrid pattern combinations
- Decision framework and selection criteria

### integration-platform-patterns.md

**When to Retrieve**: Implementing integrations with MuleSoft or Dell Boomi, using integration platforms as security boundaries, designing transformation layers, or handling high-volume ETL operations.

**Summary**: Patterns for implementing integrations using MuleSoft and Dell Boomi platforms. Covers using MuleSoft as a security boundary (VPN, IP whitelisting) and transformation layer (DataWeave), using Boomi for high-volume batch processing, file-based staging patterns, and best practices for both platforms.

**Key Topics**:
- MuleSoft as security boundary (VPN, IP whitelisting)
- MuleSoft transformation layer (DataWeave)
- Boomi high-volume batch processing
- File-based staging for large data sets
- Integration job tracking patterns

### sis-sync-patterns.md

**When to Retrieve**: Synchronizing large volumes of data from Student Information Systems (SIS), implementing high-volume batch integrations, using file-based staging for very large data sets, or designing idempotent batch synchronization patterns.

**Summary**: High-volume batch synchronization patterns for integrating Salesforce Education Cloud with legacy Student Information Systems. Teaches file-based staging for large ID lists, dynamic SQL IN-clause batching, idempotent upserts using external IDs, integration job tracking, and error handling with retry logic.

**Key Topics**:
- File-based staging for large ID lists
- Dynamic SQL IN-clause batching
- Idempotent upserts with external IDs
- Integration job tracking
- Error handling and retry logic

### salesforce-to-llm-data-pipelines.md

**When to Retrieve**: Moving Salesforce data into LLM/RAG systems, designing data extraction pipelines for LLM systems, implementing transformation and chunking strategies for Salesforce data, or understanding architectural variants for Salesforce to LLM data pipelines.

**Summary**: High-level pipeline patterns for extracting, transforming, and loading Salesforce data and metadata into LLM-powered systems. Covers batch export, event-driven, and on-demand query patterns, extraction APIs (REST, Bulk, Metadata, CDC), transformation and chunking strategies, and interaction with manifest-style descriptions.

**Key Topics**:
- Batch export vs event-driven vs on-demand query patterns
- REST API, Bulk API, Metadata API, and CDC extraction patterns
- Per-record vs aggregated chunking strategies
- Field selection and redaction patterns
- Relationship context preservation in chunks

### integration-user-license-guide.md

**When to Retrieve**: Setting up Integration User Licenses for system-to-system integrations, configuring API-only authentication for external systems, understanding how to use the free Integration User License, implementing OAuth Client Credentials Flow, managing permissions for integration users, or planning integration authentication strategy.

**Summary**: Comprehensive guide to Salesforce Integration User Licenses - the free API-only license included with Enterprise, Performance, and Unlimited editions. Covers license details and allocation, step-by-step setup and configuration, OAuth 2.0 Client Credentials Flow authentication, Permission Set design and management, security best practices, operational monitoring, and integration patterns with MuleSoft and Dell Boomi.

**Key Topics**:
- Integration User License setup and configuration
- OAuth 2.0 Client Credentials Flow authentication
- Permission Set design for API-only users
- Security best practices and audit trail management
- License management and cost optimization
- Integration patterns with MuleSoft and Dell Boomi
- Operational monitoring and troubleshooting

## Identity and SSO

Identity and SSO patterns for implementing SSO, multi-identity provider architectures, and login handlers.

- [multi-tenant-identity-architecture.md](identity-sso/multi-tenant-identity-architecture.md) — Guide to multi-tenant identity architecture supporting multiple user communities with different identity providers (OIDC, SAML, organization tenant)

### multi-tenant-identity-architecture.md

**When to Retrieve**: Supporting multiple identity providers (OIDC, SAML, organization tenant) in one org, implementing login handlers to route users by identity type, designing multi-tenant identity for different user communities, or separating user types using Record Types and sharing models.

**Summary**: Guide to multi-tenant identity architecture supporting multiple user communities (citizens, external partner organizations, internal staff) with different identity providers. Covers implementing OIDC for external users, SAML for internal staff, organization tenant identity for partners, login handler patterns, Record Type-based separation, and sharing models.

**Key Topics**:
- OIDC for external users (citizens/clients)
- SAML for internal staff
- Organization tenant identity for external partners
- Login handler patterns and matching strategies
- Record Type-based user separation
- Sharing and security by identity type

## Data Modeling

Data modeling patterns for designing external IDs, integration keys, student lifecycle models, and case management models.

- [external-ids-and-integration-keys.md](data-modeling/external-ids-and-integration-keys.md) — Guide to external ID strategies for stable record mapping, composite external IDs, and integration job tracking
- [student-lifecycle-data-model.md](data-modeling/student-lifecycle-data-model.md) — Salesforce Education Cloud (EDA) data model patterns for higher education institutions
- [case-management-data-model.md](data-modeling/case-management-data-model.md) — Data model patterns for public sector case management supporting multi-agency portals
- [lead-management-patterns.md](data-modeling/lead-management-patterns.md) — Comprehensive data model and process guide for Salesforce lead management, conversion, duplicate rules, and assignment patterns
- [object-setup-and-configuration.md](data-modeling/object-setup-and-configuration.md) — Comprehensive checklist and best practices for setting up custom and standard objects in Salesforce
- [file-management-patterns.md](data-modeling/file-management-patterns.md) — File management patterns covering ContentVersion vs Attachments vs Documents, file storage, sharing, versioning, and migration strategies
- [data-migration-patterns.md](data-modeling/data-migration-patterns.md) — Data migration patterns: import strategies, transformation patterns, validation approaches, rollback strategies, and migration best practices

### external-ids-and-integration-keys.md

**When to Retrieve**: Designing external ID fields for stable record mapping, creating composite external IDs for multi-column keys, implementing idempotent upsert operations, or tracking integration job status and timestamps.

**Summary**: Guide to external ID strategies for stable record mapping between Salesforce and external systems. Covers external ID design principles (stable, unique, mirror external keys), composite external IDs for multi-column keys, integration job tracking fields (Last_Sync_Timestamp, Last_Sync_Status), idempotent upsert patterns, and managing external IDs across multiple systems.

**Key Topics**:
- External ID design principles (stable, unique, mirror external keys)
- Composite external IDs for multi-column keys
- Integration job tracking fields (Last_Sync_Timestamp, Last_Sync_Status, etc.)
- Idempotent upsert patterns
- Multi-system external ID management

### student-lifecycle-data-model.md

**When to Retrieve**: Modeling student and applicant data in Education Cloud, designing Program Enrollment and Course Enrollment objects, integrating Education Cloud with Student Information Systems (SIS), or understanding Education Data Architecture (EDA) data model.

**Summary**: Salesforce Education Cloud (EDA) data model patterns for higher education institutions. Covers using Contact as the core student/applicant record, Program Enrollment and Course Enrollment object design, Application object patterns, SIS integration data model, and derived fields from SIS data.

**Key Topics**:
- Contact as core student/applicant record
- Program Enrollment and Course Enrollment objects
- Application object design
- SIS integration data model
- Derived fields from SIS data

### case-management-data-model.md

**When to Retrieve**: Designing case management data models for public sector, modeling multi-tenant case data in a single org, designing Notice and Transaction objects, or modeling relationships between clients and external partner organizations.

**Summary**: Data model patterns for public sector case management supporting multi-agency public benefits and services portals. Covers Client Accounts/Contacts modeling, External Partner (Provider) Accounts, case management model, Notice and Transaction objects, and multi-tenant data isolation patterns.

**Key Topics**:
- Client Accounts/Contacts modeling
- External Partner (Provider) Accounts
- Case management model
- Notice and Transaction objects
- Multi-tenant data isolation

### lead-management-patterns.md

**When to Retrieve**: Implementing lead management and conversion processes, configuring duplicate rules and matching rules for leads, setting up lead assignment rules, designing lead scoring models, or managing lead-to-opportunity conversion workflows.

**Summary**: Comprehensive data model and process guide for Salesforce lead management. Covers lead object structure, conversion field mapping, duplicate rules configuration, lead assignment rules, lead status management, lead scoring, data quality patterns, and integration patterns.

**Key Topics**:
- Lead conversion field mapping (Lead → Contact/Account/Opportunity)
- Duplicate rules and matching rules configuration
- Lead assignment rules and round-robin patterns
- Lead status management and progression
- Lead scoring models and thresholds
- Data quality and standardization patterns
- Web-to-Lead and marketing automation integration

### object-setup-and-configuration.md

**When to Retrieve**: Setting up custom objects in Salesforce, configuring object fields, page layouts, and related lists, setting up tabs, actions, and Lightning Record Pages, configuring field-level security and object permissions, setting up search layouts and compact layouts, or completing object configuration checklist before deployment.

**Summary**: Comprehensive checklist and best practices for setting up custom and standard objects in Salesforce. Covers complete object configuration from initial creation through Lightning Experience optimization, including field setup, page layouts, tabs, actions, search layouts, permissions, field naming conventions, and testing procedures.

**Key Topics**:
- Object creation and basic configuration
- Field configuration with help text and FLS
- Page layout and compact layout setup
- Search layout configuration
- Tab creation and app assignment
- Action configuration (Create, Update)
- Lightning Record Page setup
- Field-level security best practices
- Field naming conventions and API name stability
- Object setup testing procedures
- Community/portal object configuration

### file-management-patterns.md

**When to Retrieve**: Choosing between ContentVersion, Attachments, and Documents, implementing file storage and management in Salesforce, designing file upload and sharing patterns, managing file storage limits and cleanup, migrating from Attachments to ContentVersion, or implementing file versioning and collaboration.

**Summary**: File management patterns for Salesforce implementations. Covers ContentVersion (Files) vs Attachments vs Documents decision framework, file upload patterns, file sharing and versioning, storage management, security and access control, and integration patterns including external file storage and migration strategies.

**Key Topics**:
- ContentVersion (Files) vs Attachments vs Documents
- File upload and storage patterns
- File sharing and versioning
- Storage management and cleanup
- File-level security and access control
- External file storage integration
- File migration patterns

## Security

Security and access control patterns for implementing permission set-driven security, managing access control, securing Salesforce data for LLM systems, and implementing comprehensive sharing mechanisms.

- [permission-set-architecture.md](security/permission-set-architecture.md) — Guide to permission set-driven security architecture with Profiles for UI configuration and Permission Sets for access control
- [salesforce-llm-data-governance.md](security/salesforce-llm-data-governance.md) — Security and governance patterns for choosing what data to expose from Salesforce to LLMs and how to do that safely
- [sharing-mechanisms.md](security/sharing-mechanisms.md) — Comprehensive guide to all Salesforce sharing mechanisms including OWD, Role Hierarchy, Sharing Rules, Apex Managed Sharing, View All/Modify All permissions, Sharing Sets, and community sharing patterns

### permission-set-architecture.md

**When to Retrieve**: Implementing permission set-driven security architecture, migrating from profile-centric to permission set-based access control, managing permissions at scale using Permission Set Groups, or designing security models for community users.

**Summary**: Guide to permission set-driven security architecture. Teaches using Profiles for UI configuration only, Permission Sets for comprehensive access control, Permission Set Groups for role-based assignment, migration strategy from profile-centric model, and best practices for managing permissions at scale. Includes restrictions for community users.

**Key Topics**:
- Profiles = UI configuration only
- Permission Sets = Access control
- Permission Set Groups for role-based assignment
- No delete permissions for community users
- Migration strategy from profile-centric model

### salesforce-llm-data-governance.md

**When to Retrieve**: Choosing what data to expose from Salesforce to LLMs, implementing security model evaluation (FLS, OLS, sharing rules) in LLM data extraction, designing data masking and redaction strategies, or implementing governance and compliance for Salesforce to LLM data pipelines.

**Summary**: Security and governance patterns for Salesforce to LLM data pipelines. Covers data scoping principles, mapping Salesforce security to LLM access, data masking and redaction strategies, RAG security enforcement patterns (separate indexes, attribute-based filtering), and governance lifecycle management (refresh cadence, retention, compliance, audit trails).

**Key Topics**:
- Data scoping principles (relevance, sensitivity, volume constraints)
- FLS/OLS evaluation and sharing rule understanding
- Service account vs user context extraction patterns
- Separate indexes per role vs attribute-based filtering
- Data masking and redaction strategies
- Governance and compliance (GDPR, CCPA, HIPAA, FERPA)

### sharing-mechanisms.md

**When to Retrieve**: Understanding how Salesforce sharing works, implementing sharing rules for internal users, designing Experience Cloud sharing with Sharing Sets, deciding between different sharing mechanisms, troubleshooting sharing access issues, implementing Apex managed sharing, understanding View All/Modify All permissions, designing multi-tenant data isolation patterns, or optimizing sharing for large data volumes.

**Summary**: Comprehensive guide to all Salesforce sharing mechanisms. Covers Org-Wide Defaults (OWD), Role Hierarchy, Sharing Rules (Owner-based, Criteria-based, Territory-based), Manual Sharing, Apex Managed Sharing, View All/Modify All permissions (object and system level), View All Fields/Modify All Fields permissions, Sharing Sets for Experience Cloud, community sharing patterns, sharing calculation and performance, decision frameworks for selecting sharing mechanisms, best practices, common patterns, troubleshooting, and code examples.

**Key Topics**:
- Org-Wide Defaults (Private, Public Read Only, Public Read/Write)
- Role Hierarchy and hierarchical access patterns
- Sharing Rules (Owner-based, Criteria-based, Territory-based)
- Manual Sharing and Apex Managed Sharing
- View All/Modify All permissions (object and system level)
- View All Fields/Modify All Fields permissions
- Sharing Sets for Experience Cloud (Community) users
- Community sharing patterns and multi-tenant data isolation
- Sharing calculation, performance, and optimization
- Decision frameworks for selecting sharing mechanisms
- Best practices, common patterns, and troubleshooting

## Development

Development patterns and practices for implementing Apex, Flow, LWC, OmniStudio, error handling, logging, troubleshooting patterns, concurrency control, and performance optimization.

- [error-handling-and-logging.md](development/error-handling-and-logging.md) — Error handling and logging framework using custom logging objects with platform event fallbacks and external logging integration
- [apex-patterns.md](development/apex-patterns.md) — Apex design patterns including class layering (Service, Domain, Selector, Integration), SOQL optimization, and asynchronous patterns
- [flow-patterns.md](development/flow-patterns.md) — Flow design and orchestration patterns for Record-Triggered, Screen, and other Flow types with Apex integration, including Flow User permission deprecation guidance
- [order-of-execution.md](development/order-of-execution.md) — Complete guide to Salesforce order of execution, covering before-save vs after-save decision framework, trigger and flow execution timing, and debugging techniques
- [lwc-patterns.md](development/lwc-patterns.md) — Lightning Web Component patterns for complex business logic, console-style components, and service-layer patterns
- [omnistudio-patterns.md](development/omnistudio-patterns.md) — OmniStudio patterns for OmniScripts and FlexCards in guided workflows and reusable UI components
- [locking-and-concurrency-strategies.md](development/locking-and-concurrency-strategies.md) — Row locking, concurrency control patterns, UNABLE_TO_LOCK_ROW error handling, retry strategies, and deadlock prevention
- [governor-limits-and-optimization.md](development/governor-limits-and-optimization.md) — Governor limits, performance optimization strategies, SOQL query optimization, selective query patterns, and resource management
- [soql-query-patterns.md](development/soql-query-patterns.md) — Practical SOQL query patterns and examples for common scenarios, including relationship queries, aggregate queries, subqueries, maintenance queries, and cursor-based pagination
- [asynchronous-apex-patterns.md](development/asynchronous-apex-patterns.md) — Comprehensive guide to asynchronous Apex: Batch, Queueable, Scheduled, and @future methods with decision frameworks, patterns, and best practices
- [custom-settings-metadata-patterns.md](development/custom-settings-metadata-patterns.md) — Guide to Custom Settings and Custom Metadata: decision framework, usage patterns, migration strategies, and best practices

### error-handling-and-logging.md

**When to Retrieve**: Implementing error handling and logging frameworks, creating structured logging for compliance and audit trails, integrating with external logging platforms (OpenSearch, Splunk), or handling logging failures with platform event fallbacks.

**Summary**: Error handling and logging framework using custom LOG_LogMessage__c object. Covers implementing logging utility classes, platform event fallback patterns for DML failures, structured logging format, integration with centralized logging platforms (OpenSearch, Splunk), and compliance/audit trail requirements.

**Key Topics**:
- Custom logging object (LOG_LogMessage__c)
- LOG_LogMessageUtility class
- Platform event fallback for DML failures
- Structured logging format
- Integration with centralized logging (OpenSearch, Splunk)
- Compliance and audit trail requirements

### apex-patterns.md

**When to Retrieve**: Deciding when to use Apex vs. Flow, implementing Apex class layering (Service, Domain, Selector, Integration), optimizing SOQL queries and managing governor limits, designing asynchronous Apex (Queueable, Batchable, Scheduled), integrating Apex with Lightning Web Components, implementing logging utilities with fallback mechanisms, building integration services with configuration management, implementing retry logic with intelligent error detection, or building scoring models with business rule overrides.

**Summary**: Apex design patterns and best practices. Covers decision framework for when to choose Apex over Flow, class layering patterns (Service, Domain, Selector, Integration), SOQL design and optimization, asynchronous patterns (Queueable, Batchable, Scheduled), Apex+LWC integration patterns, error handling, and testing strategies. Includes detailed pattern implementations: Logging Utility with Fallback Mechanism, Integration Service with Configuration Management, Retry Logic with Intelligent Error Detection, and Scoring Model with Business Rule Overrides. Also covers tradeoffs and implementation decisions.

**Key Topics**:
- When to choose Apex over Flow
- Apex class layering (Service, Domain, Selector, Integration)
- SOQL design and optimization
- Asynchronous Apex patterns (Queueable, Batchable, Scheduled)
- Apex + LWC integration patterns
- Error handling and testing strategies
- Logging Utility with Fallback Mechanism pattern
- Integration Service with Configuration Management pattern
- Retry Logic with Intelligent Error Detection pattern
- Scoring Model with Business Rule Overrides pattern
- Tradeoffs and implementation decisions

### flow-patterns.md

**When to Retrieve**: Selecting the right Flow type for automation, designing Record-Triggered Flows with proper structure, building Screen Flows for user interactions, integrating Flows with Apex for complex logic, optimizing Flow performance and handling errors, or migrating from Flow User permission before Winter '26.

**Summary**: Flow design and orchestration patterns. Covers Flow type selection (Record-Triggered, Subflows, Screen, Scheduled, Auto-Launched), Record-Triggered Flow structure patterns, Screen Flow design patterns, Flow+Apex integration patterns, naming conventions, error handling, performance optimization, and Flow User permission deprecation migration guidance.

**Key Topics**:
- Flow type selection (Record-Triggered, Subflows, Screen, Scheduled, Auto-Launched)
- Record-Triggered Flow structure patterns
- Screen Flow design patterns
- Flow + Apex integration patterns
- Flow naming and documentation
- Error handling and performance
- Flow User permission deprecation (Winter '26)

### order-of-execution.md

**When to Retrieve**: Understanding when triggers, flows, and validation rules execute, designing automation with execution order in mind, debugging issues related to execution timing, choosing between before-save and after-save automation, understanding trigger execution order and context, or designing field value modifications and related record operations.

**Summary**: Complete guide to Salesforce order of execution. Covers the full execution sequence for save operations, before-save vs after-save decision framework, Flow execution timing, validation rule timing, trigger execution order, common patterns and pitfalls, performance considerations, and debugging techniques.

**Key Topics**:
- Complete order of execution sequence
- Before-save vs after-save decision framework
- Flow execution timing (before-save and after-save)
- Validation rule timing
- Trigger execution order and context
- Common patterns and pitfalls
- Performance considerations
- Debugging execution order issues

### lwc-patterns.md

**When to Retrieve**: Building console-style Lightning Web Components, implementing complex business logic in LWCs, designing service-layer patterns for LWCs, creating config-driven UI components, optimizing LWC performance and accessibility, or implementing performance-optimized LWC controller patterns with cache busting and lazy loading.

**Summary**: Lightning Web Component (LWC) patterns for complex business logic. Covers console-style LWC patterns, fraud/risk scoring component implementation, program-selection component patterns, service-layer patterns for LWCs, config-driven UI patterns, and performance optimization with accessibility considerations. Includes detailed Performance-Optimized LWC Controller Pattern with cache busting, lazy loading, and single Apex call strategies.

**Key Topics**:
- Console-style LWC patterns
- Fraud/risk scoring LWC implementation
- Program-selection LWC patterns
- Service-layer pattern for LWCs
- Config-driven UI patterns
- Performance optimization and accessibility
- Performance-Optimized LWC Controller Pattern
- Cache busting with random parameters
- Lazy loading for detailed breakdowns
- Single Apex call strategies

### omnistudio-patterns.md

**When to Retrieve**: Designing OmniScripts for guided workflows, creating FlexCards for reusable UI components, implementing grant management workflows with OmniStudio, integrating OmniStudio with Salesforce data model, or optimizing OmniStudio performance and error handling.

**Summary**: OmniStudio (OmniScripts and FlexCards) patterns for guided workflows and reusable UI components. Covers OmniScript design patterns for guided processes, FlexCard design for reusable UI, grant management workflow patterns, integration with Salesforce data model, and performance optimization with error handling.

**Key Topics**:
- OmniScripts for guided processes
- FlexCards for reusable UI components
- Grant management workflows
- Integration with Salesforce data model
- Performance optimization and error handling

### locking-and-concurrency-strategies.md

**When to Retrieve**: Handling UNABLE_TO_LOCK_ROW exceptions, implementing retry logic with exponential backoff, designing idempotent operations for safe retries, preventing deadlocks, or optimizing high-concurrency scenarios.

**Summary**: Comprehensive guidance on Salesforce row locking, concurrency control patterns, retry strategies with exponential backoff, deadlock prevention, and high-concurrency optimization. Covers retry logic patterns, idempotent operations with External IDs, Queueable-based retry patterns, lock-free design patterns, and deadlock prevention strategies.

**Key Topics**:
- Retry logic with exponential backoff for UNABLE_TO_LOCK_ROW
- Idempotent operations with External IDs
- Queueable-based retry patterns
- Lock-free design patterns (Platform Events, queue-based processing)
- Deadlock prevention and detection
- Transaction scope optimization

### governor-limits-and-optimization.md

**When to Retrieve**: Monitoring governor limit usage, optimizing SOQL queries for selectivity, implementing query result pagination, using asynchronous processing for large operations, or optimizing heap size usage.

**Summary**: Comprehensive guidance on Salesforce governor limits, performance optimization strategies, SOQL query optimization, selective query patterns, and resource management. Covers governor limits monitoring, selective query optimization (10% threshold, indexed fields), query result pagination, asynchronous processing patterns, and heap size optimization.

**Key Topics**:
- Governor limits monitoring and proactive checking
- Selective query optimization (10% threshold, indexed fields)
- Query result pagination (OFFSET vs cursor-based)
- Asynchronous processing (Batch, Queueable, Scheduled)
- Heap size optimization patterns
- Resource management best practices

### soql-query-patterns.md

**When to Retrieve**: Need practical SOQL query examples for common scenarios, looking for maintenance queries to clean up orgs, need relationship query/aggregate query/subquery examples, want quick reference for query patterns, or building queries for troubleshooting or data analysis.

**Summary**: Practical SOQL query patterns and examples for common Salesforce data retrieval scenarios. Provides concrete, copy-paste-ready query examples including basic SOQL structure, relationship queries, aggregate queries, subqueries, maintenance queries (unused permission sets, roles, profiles, reports, email templates), cursor-based pagination, date/time queries, and common query patterns. Includes quick reference guide for LLMs.

**Key Topics**:
- Basic SOQL syntax and structure
- Relationship queries (parent object fields, child object subqueries)
- Aggregate queries (COUNT, SUM, AVG, GROUP BY)
- Maintenance query patterns (unused components, org cleanup)
- Cursor-based pagination for large datasets
- Date and time query functions
- Selective query patterns with indexed fields
- Security enforcement in Apex queries
- Common query patterns (IN, LIKE, NULL checks, comparisons)

## Troubleshooting

Debugging and troubleshooting approaches for integration debugging, data reconciliation, common errors, and root cause analysis.

- [integration-debugging.md](troubleshooting/integration-debugging.md) — Systematic approaches to troubleshooting integration failures using SOQL debugging, history object queries, and root cause analysis
- [data-reconciliation.md](troubleshooting/data-reconciliation.md) — Approaches to reconciling data between Salesforce and external systems using external IDs and integration job tracking
- [common-apex-errors.md](troubleshooting/common-apex-errors.md) — Common Apex errors with solutions: UNABLE_TO_LOCK_ROW, NULL_POINTER_EXCEPTION, QUERY_EXCEPTION, DML_EXCEPTION, LIMIT_EXCEPTION
- [common-lwc-errors.md](troubleshooting/common-lwc-errors.md) — Common LWC errors with solutions: property access errors, wire adapter errors, event handling errors
- [lwc-accessibility-errors.md](troubleshooting/lwc-accessibility-errors.md) — Common LWC accessibility errors with solutions: missing labels, ARIA issues, keyboard traps, focus indicators, color contrast, WCAG violations
- [governor-limit-errors.md](troubleshooting/governor-limit-errors.md) — Governor limit errors and solutions: too many SOQL queries, too many DML statements, CPU time limits, heap size limits

### integration-debugging.md

**When to Retrieve**: Troubleshooting integration failures and errors, using SOQL debugging patterns to investigate issues, performing root cause analysis for data synchronization problems, querying history objects to track data changes, or analyzing integration errors and data quality issues.

**Summary**: Systematic approaches to troubleshooting integration failures, identifying root causes, and resolving data synchronization issues. Covers SOQL debugging patterns, history object queries for change tracking, root cause analysis techniques, integration error analysis, and data quality debugging methods.

**Key Topics**:
- SOQL debugging patterns
- History object queries for change tracking
- Root cause analysis techniques
- Integration error analysis
- Data quality debugging methods

### data-reconciliation.md

**When to Retrieve**: Reconciling data between Salesforce and external systems, using external IDs to identify and match records, performing field-level reconciliation to find discrepancies, building reconciliation reporting and alerting, or ensuring data consistency across systems.

**Summary**: Systematic approaches to reconciling data between Salesforce and external systems, identifying discrepancies, and ensuring data consistency. Covers external ID-based reconciliation, integration job tracking reconciliation, field-level reconciliation, discrepancy identification, and reconciliation reporting with alerting.

**Key Topics**:
- External ID-based reconciliation
- Integration job tracking reconciliation
- Field-level reconciliation
- Discrepancy identification
- Reconciliation reporting and alerting

## Patterns

Reusable design patterns that span multiple domains, including governor limit management, bulkification, and cross-cutting design patterns.

- [cross-cutting-patterns.md](patterns/cross-cutting-patterns.md) — Summary of cross-cutting patterns including governor limit management, bulkification, external IDs, error handling, and security patterns

### cross-cutting-patterns.md

**When to Retrieve**: Finding reusable patterns that apply across multiple domains, managing governor limits across Apex/Flow/integrations, implementing bulkification patterns, applying cross-cutting design patterns, or understanding patterns that span architecture/development/integration.

**Summary**: Summary of cross-cutting patterns that appear across multiple domains. Covers governor limit management patterns, bulkification across Apex/Flow/integrations, external ID and integration key patterns, error handling and logging patterns, data quality and deduplication patterns, security and sharing patterns, integration pattern selection framework, portal design patterns, and testing/quality patterns. Links to detailed domain-specific documentation.

**Key Topics**:
- Governor limit management patterns
- Bulkification across Apex, Flow, and integrations
- External ID and integration key patterns
- Error handling and logging patterns
- Data quality and deduplication patterns
- Security and sharing patterns
- Integration pattern selection framework
- Portal design patterns
- Testing and quality patterns

## Glossary

Terminology and definitions for clarifying what terms mean and understanding core concepts.

- [core-terminology.md](glossary/core-terminology.md) — Core terminology and definitions for integration, identity, data modeling, security, platform, development, and project method terms

### core-terminology.md

**When to Retrieve**: Looking up definitions of Salesforce and integration terminology, understanding acronyms and abbreviations (ETL, SIS, OIDC, SAML, LWC, etc.), clarifying core concepts used in the knowledge library, or finding domain-specific terminology definitions.

**Summary**: Core terminology and definitions used throughout the RAG knowledge library. Covers integration terms (ETL, API, Platform Events, External ID), identity terms (OIDC, SAML, Login Handler, Organization Tenant Identity), data model terms (SIS, EDA, Record Type), security terms (Permission Set, Permission Set Group, Sharing Set), platform terms (Experience Cloud, GovCloud), development terms (LWC, OmniStudio, Flow, Apex), integration platform terms (MuleSoft, Dell Boomi), data quality terms (Idempotent Operation, Reconciliation), and project method terms (Sprint-Based Delivery, UAT).

**Key Topics**:
- Integration terminology (ETL, API, Platform Events, External ID)
- Identity and SSO terminology (OIDC, SAML, Organization Tenant Identity)
- Data model terminology (SIS, EDA, Record Type)
- Security terminology (Permission Set, Permission Set Group, Sharing Set)
- Platform terminology (Experience Cloud, GovCloud)
- Development terminology (LWC, OmniStudio, Flow, Apex)
- Integration platform terminology (MuleSoft, Dell Boomi)
- Data quality terminology (Idempotent Operation, Reconciliation)
- Project method terminology (Sprint-Based Delivery, UAT)

## Project Methods

Project delivery and methodology for sprint-based delivery, testing strategies, and quality standards.

- [delivery-framework.md](project-methods/delivery-framework.md) — Sprint-based delivery approach for managing complex multi-stakeholder Salesforce projects
- [testing-strategy.md](project-methods/testing-strategy.md) — Comprehensive testing strategies covering integration testing, data quality testing, user migration testing, and UAT
- [deployment-patterns.md](project-methods/deployment-patterns.md) — Deployment and CI/CD patterns: deployment methods, source control strategies, Metadata API patterns, package development, and deployment best practices
- [sfdx-patterns.md](project-methods/sfdx-patterns.md) — Salesforce DX patterns: project structure, commands, scratch org patterns, source tracking, and CI/CD integration

## Operations

Delivery and operations patterns for CI/CD, environment strategy, and release governance.

- [cicd-patterns.md](operations/cicd-patterns.md) — Comprehensive CI/CD patterns: metadata vs. source-tracked orgs, unlocked packages, sandbox seeding, deployment validation, and rollback patterns
- [environment-strategy.md](operations/environment-strategy.md) — Environment strategy: org topologies for multi-team programs, data masking, and refresh cadences
- [release-governance.md](operations/release-governance.md) — Release governance: Change Advisory Boards, approval workflows, and risk-based release checklists

### cicd-patterns.md

**When to Retrieve**: Implementing CI/CD for Salesforce, choosing between metadata and source-tracked orgs, using unlocked packages, automating sandbox seeding, implementing deployment validation, or planning rollback strategies.

**Summary**: Comprehensive CI/CD patterns for Salesforce covering metadata vs. source-tracked org decision framework, unlocked package development and promotion, automated sandbox seeding strategies, deployment validation approaches, and rollback patterns including metadata rollback, data rollback, and feature flag rollbacks.

**Key Topics**:
- Metadata vs. source-tracked orgs decision framework
- Unlocked package development and versioning
- Sandbox seeding automation
- Deployment validation strategies
- Rollback patterns and procedures

### environment-strategy.md

**When to Retrieve**: Designing org topologies for multi-team programs, implementing data masking for PII/PHI, planning sandbox refresh cadences, or managing multiple Salesforce environments.

**Summary**: Environment strategy patterns for Salesforce including org topology patterns (single org, multi-org, hybrid), data masking strategies for PII/PHI, test data anonymization, and sandbox refresh cadence planning.

**Key Topics**:
- Org topology patterns for multi-team programs
- Data masking and anonymization strategies
- Sandbox refresh cadences
- Environment management best practices

### release-governance.md

**When to Retrieve**: Establishing Change Advisory Boards, implementing approval workflows, creating risk-based release checklists, or managing release governance processes.

**Summary**: Release governance patterns including CAB structure and processes, multi-stage approval workflows, automated approval gates, and risk-based release checklists with deployment risk matrices.

**Key Topics**:
- Change Advisory Board (CAB) structure
- Approval workflow patterns
- Risk-based release checklists
- Deployment risk assessment

## Observability

Observability and resilience patterns for monitoring, performance tuning, and high availability.

- [monitoring-alerting.md](observability/monitoring-alerting.md) — Monitoring and alerting: Platform Events monitoring, API health, async job failures, and log aggregation patterns
- [performance-tuning.md](observability/performance-tuning.md) — Performance tuning: Query/selectivity tuning, Large Data Volumes (LDV) handling, governor limit mitigation, and caching strategies
- [ha-dr-patterns.md](observability/ha-dr-patterns.md) — High availability and disaster recovery: Backup/restore approaches, failover patterns for integrations, and business continuity drills

### monitoring-alerting.md

**When to Retrieve**: Implementing monitoring and alerting for Platform Events, monitoring API health, tracking async job failures, implementing log aggregation, or setting up system observability.

**Summary**: Monitoring and alerting patterns for Salesforce including Platform Events monitoring metrics, API health monitoring (response time, error rates, availability), async job failure detection (Batch, Queueable, Scheduled), and log aggregation patterns with centralized logging strategies.

**Key Topics**:
- Platform Events monitoring and metrics
- API health monitoring
- Async job failure detection
- Log aggregation patterns

### performance-tuning.md

**When to Retrieve**: Optimizing query selectivity, handling Large Data Volumes (LDV), mitigating governor limits, implementing caching strategies, or tuning Salesforce performance.

**Summary**: Performance tuning patterns including query/selectivity optimization with indexed fields, LDV handling strategies and data archiving, governor limit mitigation patterns, and caching strategies using Platform Cache.

**Key Topics**:
- Query/selectivity tuning with indexed fields
- Large Data Volume (LDV) handling
- Governor limit mitigation
- Caching strategies

### ha-dr-patterns.md

**When to Retrieve**: Planning backup and restore strategies, implementing failover patterns for integrations, conducting business continuity drills, or designing high availability systems.

**Summary**: High availability and disaster recovery patterns including backup/restore approaches (data and metadata), failover patterns for integrations (circuit breakers, retry logic), and business continuity drills with RTO/RPO planning.

**Key Topics**:
- Backup/restore strategies
- Integration failover patterns
- Business continuity planning
- RTO/RPO objectives

## Data Governance

Data governance and compliance patterns for data residency, compliance, and data quality.

- [data-residency-compliance.md](data-governance/data-residency-compliance.md) — Data residency and compliance: PII/PHI handling, GDPR/CCPA/SOC2 controls, field-level encryption, and Shield best practices
- [data-quality-stewardship.md](data-governance/data-quality-stewardship.md) — Data quality and stewardship: Duplicate prevention beyond leads, survivorship rules, and master data governance

### data-residency-compliance.md

**When to Retrieve**: Handling PII/PHI data, implementing GDPR/CCPA/SOC2 compliance, configuring field-level encryption, or implementing Shield best practices.

**Summary**: Data residency and compliance patterns including PII/PHI identification and protection, GDPR/CCPA/SOC2 compliance frameworks, field-level encryption with Shield Encryption, and Shield best practices (Platform Encryption, Event Monitoring, Field Audit Trail).

**Key Topics**:
- PII/PHI handling and protection
- GDPR/CCPA/SOC2 compliance
- Field-level encryption
- Shield best practices

### data-quality-stewardship.md

**When to Retrieve**: Implementing duplicate prevention for Accounts/Contacts, configuring survivorship rules for data merges, establishing master data governance, or managing data quality at scale.

**Summary**: Data quality and stewardship patterns including duplicate prevention beyond leads (Account/Contact duplicate rules), survivorship rules for data merges, and master data governance with data stewardship workflows and data quality metrics.

**Key Topics**:
- Duplicate prevention for Accounts and Contacts
- Survivorship rules and merge strategies
- Master data governance
- Data quality metrics and stewardship

## Adoption

Adoption and change management patterns for user readiness and org health.

- [user-readiness.md](adoption/user-readiness.md) — User readiness: Training plans, support models, and telemetry for feature adoption
- [org-health-checks.md](adoption/org-health-checks.md) — Org health checks: Technical debt triage, baseline audits, and remediation playbooks

### user-readiness.md

**When to Retrieve**: Creating training plans, establishing support models, implementing feature adoption telemetry, or planning user readiness programs.

**Summary**: User readiness patterns including training curriculum design, role-based training, training delivery methods, help desk patterns, support workflows, and telemetry for feature adoption tracking.

**Key Topics**:
- Training plans and curriculum design
- Support models and workflows
- Feature adoption telemetry
- User engagement patterns

### org-health-checks.md

**When to Retrieve**: Conducting technical debt triage, performing baseline audits, creating remediation playbooks, or maintaining org health.

**Summary**: Org health check patterns including technical debt identification and prioritization, baseline audits (code quality, configuration, data quality), and remediation playbooks for debt remediation, org cleanup, and optimization.

**Key Topics**:
- Technical debt triage
- Baseline audits
- Remediation playbooks
- Org health monitoring

## Testing

Testing patterns and examples for Apex, LWC, and integration testing.

- [apex-testing-patterns.md](testing/apex-testing-patterns.md) — Apex testing patterns: test class structure, test data factories, bulk testing, error scenario testing, mocking
- [test-data-factories.md](testing/test-data-factories.md) — Test data factory patterns: basic factories, relationship factories, customization, bulk data creation
- [automated-testing-patterns.md](testing/automated-testing-patterns.md) — Automated testing at scale: Apex test data factories, UI test automation for LWC/Experience Cloud, contract tests for integrations, and load testing patterns
- [non-functional-requirements.md](testing/non-functional-requirements.md) — Non-functional requirements: Security testing, accessibility for LWCs/portals, and performance benchmarks

### automated-testing-patterns.md

**When to Retrieve**: Implementing automated testing at scale, creating UI test automation, implementing contract tests for integrations, or conducting load testing.

**Summary**: Automated testing patterns for Salesforce at scale including advanced Apex test data factory patterns, UI test automation for LWC (Jest) and Experience Cloud (Selenium/Playwright), contract tests for APIs and events, and load testing patterns with performance testing strategies.

**Key Topics**:
- Advanced test data factory patterns
- UI test automation (Jest, Selenium, Playwright)
- Contract testing for integrations
- Load testing and scalability testing

### non-functional-requirements.md

**When to Retrieve**: Implementing security testing, accessibility testing for LWCs and portals, defining performance benchmarks, or testing non-functional requirements.

**Summary**: Non-functional requirements testing including security testing patterns (vulnerability testing, penetration testing), accessibility testing for LWCs and portals (WCAG compliance), and performance benchmarks with SLA definition and performance testing frameworks.

**Key Topics**:
- Security testing patterns
- Accessibility testing (WCAG compliance)
- Performance benchmarks and SLAs
- NFR test automation

## Quick Start Guides

Step-by-step guides for getting started with Salesforce development.

- [apex-quick-start.md](quick-start/apex-quick-start.md) — Getting started with Apex: create your first service, selector, domain, and test classes
- [lwc-quick-start.md](quick-start/lwc-quick-start.md) — Getting started with LWC: create your first component with data access and interactivity
- [lwc-accessibility-quick-start.md](quick-start/lwc-accessibility-quick-start.md) — Getting started with LWC accessibility: quick checklist, step-by-step guide, essential patterns

## API Reference

Quick reference for common APIs, methods, and patterns.

- [apex-api-reference.md](api-reference/apex-api-reference.md) — Apex API reference: Service, Domain, Selector, Integration, Utility classes with method signatures
- [lwc-api-reference.md](api-reference/lwc-api-reference.md) — LWC API reference: modules, decorators, wire adapters, Lightning Data Service
- [lds-api-reference.md](api-reference/lds-api-reference.md) — Lightning Data Service API reference: getRecord, updateRecord, createRecord, deleteRecord, cache management
- [soql-reference.md](api-reference/soql-reference.md) — SOQL reference: syntax, functions, relationship queries, aggregate queries, date/time functions
- [platform-events-api.md](api-reference/platform-events-api.md) — Platform Events API reference: publishing, subscribing, payload design, error handling

## MCP Knowledge

Knowledge extracted from Salesforce MCP Service tools, providing official guidance and best practices.

- [lwc-development-guide.md](mcp-knowledge/lwc-development-guide.md) — LWC development guidance: core principles, technical stack, best practices, project structure
- [lwc-best-practices.md](mcp-knowledge/lwc-best-practices.md) — LWC best practices: custom events, property naming, decorators, Lightning Message Service, template directives
- [lwc-accessibility.md](mcp-knowledge/lwc-accessibility.md) — LWC accessibility: WCAG 2.2 compliance, images, lists, form labels, keyboard accessibility, link purpose
- [lds-patterns.md](mcp-knowledge/lds-patterns.md) — Lightning Data Service patterns: data consistency, referential integrity, choosing UIAPI vs Apex
- [design-system-patterns.md](mcp-knowledge/design-system-patterns.md) — Salesforce Lightning Design System patterns: UX principles, visual design, component usage, interaction patterns

### delivery-framework.md

**When to Retrieve**: Managing complex multi-stakeholder Salesforce projects, implementing sprint-based delivery structure, coordinating stakeholders and testing windows, establishing quality standards and change management, or planning project delivery methodology.

**Summary**: Sprint-based delivery approach for managing complex multi-stakeholder Salesforce projects. Covers sprint structure, stakeholder coordination practices, testing window coordination, change management and documentation alignment, and comprehensive quality standards.

**Key Topics**:
- Sprint-based delivery structure
- Stakeholder coordination practices
- Testing window coordination
- Change management and documentation alignment
- Comprehensive quality standards

### testing-strategy.md

**When to Retrieve**: Planning comprehensive testing strategies for Salesforce projects, designing integration testing (connectivity, transformation, error handling), implementing data quality testing (matching, deduplication, error capture), testing user migration and login handlers, conducting user acceptance testing (UAT), understanding test class security anti-patterns, or implementing test class design best practices.

**Summary**: Comprehensive testing strategies for Salesforce implementations. Covers integration testing (connectivity, data transformation, error handling), data quality testing (matching, deduplication, error capture), user migration and login handler testing, user acceptance testing (UAT), and test environment management. Includes test class security anti-patterns, test class design anti-patterns, and design for testability best practices.

**Key Topics**:
- Integration testing (connectivity, data transformation, error handling)
- Data quality testing (matching, deduplication, error capture)
- User migration and login handler testing
- User acceptance testing (UAT)
- Test environment management
- Test class security anti-patterns
- Test class design anti-patterns (@SeeAllData, single-record tests, etc.)
- Design for testability best practices

## Code Examples

Complete, working code examples organized by category. All examples are copy-paste ready and include tests.

- [Code Examples Index](code-examples/code-examples-index.md) — Complete index of all code examples

### Apex Examples
- [Service Layer Examples](code-examples/apex/service-layer-examples.md) — Service class implementations with domain and selector delegation
- [Domain Layer Examples](code-examples/apex/domain-layer-examples.md) — Object-specific business logic and validation
- [Selector Layer Examples](code-examples/apex/selector-layer-examples.md) — SOQL queries and data access patterns
- [Integration Examples](code-examples/apex/integration-examples.md) — External API callouts and transformations
- [Trigger Examples](code-examples/apex/trigger-examples.md) — Trigger handler patterns with bulkification
- [Batch Examples](code-examples/apex/batch-examples.md) — Batch Apex implementations: stateless, stateful, chaining, error handling, and monitoring
- [Queueable Examples](code-examples/apex/queueable-examples.md) — Queueable patterns: basic, chaining, callouts, retry logic, and monitoring
- [Scheduled Examples](code-examples/apex/scheduled-examples.md) — Scheduled Apex patterns: cron expressions, scheduled batch jobs, error handling, and monitoring

### Code Templates
- [Service Template](code-examples/templates/apex-service-template.md) — Service class template
- [Domain Template](code-examples/templates/apex-domain-template.md) — Domain class template
- [Selector Template](code-examples/templates/apex-selector-template.md) — Selector class template
- [Trigger Template](code-examples/templates/apex-trigger-template.md) — Trigger handler template
- [Test Template](code-examples/templates/test-class-template.md) — Test class template
- [Batch Template](code-examples/templates/apex-batch-template.md) — Batch Apex template
- [Queueable Template](code-examples/templates/apex-queueable-template.md) — Queueable Apex template
- [Scheduled Template](code-examples/templates/apex-scheduled-template.md) — Scheduled Apex template
- [Accessible Component Template](code-examples/templates/lwc-accessible-component-template.md) — Accessible LWC component template with all accessibility best practices
- [SFDX Project Template](code-examples/templates/sfdx-project-template.md) — SFDX project setup template
- [CI/CD Template](code-examples/templates/ci-cd-template.md) — CI/CD pipeline template

### LWC Examples
- [Component Examples](rag/code-examples/lwc/component-examples.md) — Lightning Web Component implementations (coming soon)
- [Service Examples](rag/code-examples/lwc/service-examples.md) — LWC service layer patterns (coming soon)
- [Wire Examples](rag/code-examples/lwc/wire-examples.md) — Wire service and imperative call patterns (coming soon)
- [Accessibility Examples](code-examples/lwc/accessibility-examples.md) — Complete accessibility code examples: forms, keyboard navigation, ARIA, images, semantic HTML, dynamic content, color/contrast
- [Test Examples](rag/code-examples/lwc/test-examples.md) — Jest test examples for LWC (coming soon)

### Flow Examples
- [Record-Triggered Examples](rag/code-examples/flow/record-triggered-examples.md) — Before-save and after-save flow patterns (coming soon)
- [Screen Flow Examples](rag/code-examples/flow/screen-flow-examples.md) — User interaction flow patterns (coming soon)
- [Subflow Examples](rag/code-examples/flow/subflow-examples.md) — Reusable subflow patterns (coming soon)

### Integration Examples
- [REST API Examples](rag/code-examples/integrations/rest-api-examples.md) — Outbound and inbound REST API patterns (coming soon)
- [Platform Events Examples](rag/code-examples/integrations/platform-events-examples.md) — Event publishing and subscription patterns (coming soon)
- [Callout Examples](rag/code-examples/integrations/callout-examples.md) — HTTP callout patterns with error handling (coming soon)
- [Bulk API Examples](rag/code-examples/integrations/bulk-api-examples.md) — Bulk data operations (coming soon)
- [CDC Examples](code-examples/integrations/cdc-examples.md) — Change Data Capture patterns: trigger handlers, Platform Event integration, error handling, and replay

### Utility Examples
- [Logging Examples](rag/code-examples/utilities/logging-examples.md) — Structured logging patterns (coming soon)
- [Error Handling Examples](rag/code-examples/utilities/error-handling-examples.md) — Error handling and retry patterns (coming soon)
- [Validation Examples](rag/code-examples/utilities/validation-examples.md) — Data validation patterns (coming soon)
- [Custom Settings Examples](code-examples/utilities/custom-settings-examples.md) — Custom Settings usage: hierarchical and list custom settings in Apex and Flows
- [Custom Metadata Examples](code-examples/utilities/custom-metadata-examples.md) — Custom Metadata usage: configuration patterns, Apex queries, Flow integration, and migration from Custom Settings
- [Metadata API Examples](code-examples/utilities/metadata-api-examples.md) — Metadata API patterns: deployment, retrieval, and automation
- [SFDX Examples](code-examples/utilities/sfdx-examples.md) — Salesforce DX patterns: project setup, deployment scripts, and CI/CD integration
- [Data Migration Examples](code-examples/utilities/data-migration-examples.md) — Data migration patterns: import with validation, transformation, error handling, and rollback

**When to Retrieve**: Need complete, working code examples, implementing specific patterns, looking for copy-paste ready code, or need test examples for code patterns.

## Retrieval Guidelines

### When to Use This Library

This RAG library should be retrieved when:

1. **Architecture Questions**: Designing system architecture, integration patterns, multi-tenant solutions, or portal architecture
2. **Integration Questions**: Implementing ETL, API, or event-driven integrations, SIS synchronization, or integration platforms
3. **Identity Questions**: Implementing SSO, multi-identity provider architectures, or login handlers
4. **Data Modeling Questions**: Designing external IDs, integration keys, student lifecycle models, or case management models
5. **Security Questions**: Implementing permission set-driven security or managing access control
6. **Development Questions**: Implementing Apex, Flow, LWC, OmniStudio, error handling, logging, or troubleshooting patterns
7. **Project Methods Questions**: Sprint-based delivery, testing strategies, or quality standards
8. **Troubleshooting Questions**: Integration debugging, data reconciliation, or root cause analysis
9. **Pattern Questions**: Looking for reusable patterns or best practices
10. **Code Generation Questions**: Need complete, working code examples, implementing specific patterns, or looking for copy-paste ready code
11. **Terminology Questions**: Clarifying what a term means or understanding core concepts

### How to Use This Library

1. **Identify Domain**: Determine which domain folder contains relevant knowledge
2. **Review Index**: Check this index for file summaries and retrieval guidance
3. **Read Relevant Files**: Read files that match the question domain
4. **Cross-Reference**: Check related files in other domains when needed
5. **Apply Patterns**: Use patterns and best practices from the library

### Content Characteristics

All content in this library:

- **Evidence-Based**: Derived from real implementation experience
- **Sanitized**: All identifying information removed (company names, client names, project codenames)
- **Pattern-Focused**: Emphasizes reusable patterns and best practices
- **Decision-Oriented**: Includes architectural decisions and tradeoffs
- **Implementation-Ready**: Provides actionable guidance for implementation

## Terminology

### Common Terms

- **ETL**: Extract, Transform, Load - batch data synchronization
- **SIS**: Student Information System - external system for student data
- **OIDC**: OpenID Connect - identity provider protocol for external users
- **SAML**: Security Assertion Markup Language - identity provider protocol for enterprise SSO
- **Platform Events**: Salesforce event-driven integration mechanism
- **External ID**: Field marked as external ID for upsert operations
- **Permission Set**: Salesforce mechanism for granting incremental permissions
- **Record Type**: Salesforce mechanism for differentiating record types
- **Experience Cloud**: Salesforce portal/community platform
- **GovCloud**: Government Cloud - compliant cloud environment
- **OmniStudio**: Salesforce OmniStudio for guided workflows and reusable UI components
- **LWC**: Lightning Web Component - modern Salesforce UI component framework
- **EDA**: Education Data Architecture - Salesforce Education Cloud data model

### Domain-Specific Terms

See individual RAG files for domain-specific terminology and definitions.

## File Status

### Completed Files (68 total)

**Architecture (2 files)**:
- ✅ `architecture/event-driven-architecture.md`
- ✅ `architecture/portal-architecture.md`

**Integrations (5 files)**:
- ✅ `integrations/etl-vs-api-vs-events.md`
- ✅ `integrations/integration-platform-patterns.md`
- ✅ `integrations/sis-sync-patterns.md`
- ✅ `integrations/salesforce-to-llm-data-pipelines.md`
- ✅ `integrations/change-data-capture-patterns.md`

**Identity & SSO (1 file)**:
- ✅ `identity-sso/multi-tenant-identity-architecture.md`

**Data Modeling (7 files)**:
- ✅ `data-modeling/external-ids-and-integration-keys.md`
- ✅ `data-modeling/student-lifecycle-data-model.md`
- ✅ `data-modeling/case-management-data-model.md`
- ✅ `data-modeling/lead-management-patterns.md`
- ✅ `data-modeling/object-setup-and-configuration.md`
- ✅ `data-modeling/file-management-patterns.md`
- ✅ `data-modeling/data-migration-patterns.md`

**Security (3 files)**:
- ✅ `security/permission-set-architecture.md`
- ✅ `security/salesforce-llm-data-governance.md`
- ✅ `security/sharing-mechanisms.md`

**Development (10 files)**:
- ✅ `development/error-handling-and-logging.md`
- ✅ `development/apex-patterns.md`
- ✅ `development/flow-patterns.md`
- ✅ `development/order-of-execution.md`
- ✅ `development/lwc-patterns.md`
- ✅ `development/omnistudio-patterns.md`
- ✅ `development/locking-and-concurrency-strategies.md`
- ✅ `development/governor-limits-and-optimization.md`
- ✅ `development/asynchronous-apex-patterns.md`
- ✅ `development/custom-settings-metadata-patterns.md`

**Troubleshooting (6 files)**:
- ✅ `troubleshooting/integration-debugging.md`
- ✅ `troubleshooting/data-reconciliation.md`
- ✅ `troubleshooting/common-apex-errors.md`
- ✅ `troubleshooting/common-lwc-errors.md`
- ✅ `troubleshooting/governor-limit-errors.md`
- ✅ `troubleshooting/lwc-accessibility-errors.md`

**Testing (3 files)**:
- ✅ `testing/apex-testing-patterns.md`
- ✅ `testing/test-data-factories.md`
- ✅ `testing/automated-testing-patterns.md`
- ✅ `testing/non-functional-requirements.md`
- ✅ `testing/lwc-accessibility-testing.md`

**Quick Start (3 files)**:
- ✅ `quick-start/apex-quick-start.md`
- ✅ `quick-start/lwc-quick-start.md`
- ✅ `quick-start/lwc-accessibility-quick-start.md`

**API Reference (5 files)**:
- ✅ `api-reference/apex-api-reference.md`
- ✅ `api-reference/lwc-api-reference.md`
- ✅ `api-reference/lds-api-reference.md`
- ✅ `api-reference/soql-reference.md`
- ✅ `api-reference/platform-events-api.md`

**MCP Knowledge (5 files)**:
- ✅ `mcp-knowledge/lwc-development-guide.md`
- ✅ `mcp-knowledge/lwc-best-practices.md`
- ✅ `mcp-knowledge/lwc-accessibility.md`
- ✅ `mcp-knowledge/lds-patterns.md`
- ✅ `mcp-knowledge/design-system-patterns.md`

**Code Examples (22 files)**:
- ✅ `code-examples/apex/service-layer-examples.md`
- ✅ `code-examples/apex/domain-layer-examples.md`
- ✅ `code-examples/apex/selector-layer-examples.md`
- ✅ `code-examples/apex/integration-examples.md`
- ✅ `code-examples/apex/trigger-examples.md`
- ✅ `code-examples/apex/batch-examples.md`
- ✅ `code-examples/apex/queueable-examples.md`
- ✅ `code-examples/apex/scheduled-examples.md`
- ✅ `code-examples/integrations/cdc-examples.md`
- ✅ `code-examples/utilities/custom-settings-examples.md`
- ✅ `code-examples/utilities/custom-metadata-examples.md`
- ✅ `code-examples/utilities/metadata-api-examples.md`
- ✅ `code-examples/utilities/sfdx-examples.md`
- ✅ `code-examples/utilities/data-migration-examples.md`
- ✅ `code-examples/templates/apex-service-template.md`
- ✅ `code-examples/templates/apex-domain-template.md`
- ✅ `code-examples/templates/apex-selector-template.md`
- ✅ `code-examples/templates/apex-trigger-template.md`
- ✅ `code-examples/templates/test-class-template.md`
- ✅ `code-examples/templates/apex-batch-template.md`
- ✅ `code-examples/templates/apex-queueable-template.md`
- ✅ `code-examples/templates/apex-scheduled-template.md`
- ✅ `code-examples/templates/lwc-accessible-component-template.md`
- ✅ `code-examples/templates/sfdx-project-template.md`
- ✅ `code-examples/templates/ci-cd-template.md`

**Project Methods (4 files)**:
- ✅ `project-methods/delivery-framework.md`
- ✅ `project-methods/testing-strategy.md`
- ✅ `project-methods/deployment-patterns.md`
- ✅ `project-methods/sfdx-patterns.md`

**Operations (3 files)**:
- ✅ `operations/cicd-patterns.md`
- ✅ `operations/environment-strategy.md`
- ✅ `operations/release-governance.md`

**Observability (3 files)**:
- ✅ `observability/monitoring-alerting.md`
- ✅ `observability/performance-tuning.md`
- ✅ `observability/ha-dr-patterns.md`

**Data Governance (2 files)**:
- ✅ `data-governance/data-residency-compliance.md`
- ✅ `data-governance/data-quality-stewardship.md`

**Adoption (2 files)**:
- ✅ `adoption/user-readiness.md`
- ✅ `adoption/org-health-checks.md`

**Patterns (1 file)**:
- ✅ `patterns/cross-cutting-patterns.md`

**Glossary (1 file)**:
- ✅ `glossary/core-terminology.md`

### Open Gaps / To Validate

Additional topics that may need RAG files based on knowledge source analysis:

- Governor limit scenarios and optimization
- Advanced SOQL patterns and optimization
- Batch Apex patterns for large-scale operations
- Change Data Capture (CDC) patterns
- Marketing Cloud integration patterns
- Contact center integration patterns
- ITSM/Incident Management integration patterns

These topics appear in knowledge sources but may need dedicated RAG files if sufficient evidence exists.

## Maintenance

### Content Updates

This library is derived from immutable source documents:

- **GPT Knowledge Dump**: Read-only source document
- **Cursor Knowledge Dump**: Read-only source document
- **Workspace Evidence**: Code, metadata, and documentation

### Adding New Files

New RAG files should:

1. Be evidence-based (derived from knowledge sources)
2. Be sanitized (no identifying information)
3. Follow existing file structure and format
4. Be added to this index with summary and retrieval guidance
5. Cross-reference related files when appropriate
6. Update `rag-library.json` with new file metadata

### Version Control

This library is version-controlled and should be updated incrementally as new patterns are identified and documented.
