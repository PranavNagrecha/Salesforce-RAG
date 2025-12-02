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

### UNABLE_TO_LOCK_ROW

**Definition**: Salesforce exception status code indicating a row locking conflict when multiple processes attempt to update the same record simultaneously.

**Context**: Occurs in high-concurrency scenarios where multiple processes update the same records. Requires retry logic with exponential backoff to handle transient locking conflicts gracefully.

**Related Patterns**: See `rag/development/locking-and-concurrency-strategies.md` for row locking and retry patterns.

### Exponential Backoff

**Definition**: Retry strategy that increases delay between retry attempts exponentially (e.g., 1 second, 2 seconds, 4 seconds) to reduce contention and allow locks to clear.

**Context**: Used for handling transient errors like `UNABLE_TO_LOCK_ROW`. Prevents retry storms where multiple processes retry simultaneously, making the problem worse.

**Related Patterns**: See `rag/development/locking-and-concurrency-strategies.md` for retry logic patterns.

### Governor Limits

**Definition**: Salesforce runtime limits that constrain resource usage (SOQL queries, DML operations, CPU time, heap size, callouts) to ensure fair resource allocation.

**Context**: Limits apply per transaction context. Synchronous limits are lower than asynchronous limits. Must be monitored and managed to prevent exceptions.

**Related Patterns**: See `rag/development/governor-limits-and-optimization.md` for limit monitoring and optimization patterns.

### Selective Query

**Definition**: SOQL query that uses indexed fields in WHERE clauses and returns less than 10% of records in an object, ensuring efficient index usage.

**Context**: Non-selective queries (returning more than 10%) can cause performance issues and may be blocked in production. Selective queries use indexes efficiently, reducing query time and database load.

**Related Patterns**: See `rag/development/governor-limits-and-optimization.md` for query optimization patterns.

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

### Bulk API

**Definition**: Salesforce API for asynchronous, high-volume data operations (millions of records) using job-based processing.

**Context**: Used for initial RAG index population, periodic full refresh of LLM knowledge bases, and large-scale data migration. Supports CSV, JSON, or XML output formats.

**Related Patterns**: See `rag/integrations/salesforce-to-llm-data-pipelines.md` for Bulk API extraction patterns.

### Change Data Capture (CDC)

**Definition**: Salesforce mechanism for real-time or near-real-time data change notifications via event-driven architecture.

**Context**: Used for incremental RAG updates, event-driven LLM knowledge base refresh, and maintaining LLM systems in sync with Salesforce. Captures create, update, delete, and undelete operations.

**Related Patterns**: See `rag/integrations/salesforce-to-llm-data-pipelines.md` for CDC extraction patterns.

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

## LLM and RAG Terms

### RAG (Retrieval-Augmented Generation)

**Definition**: AI pattern that combines retrieval of relevant context from a knowledge base with LLM generation to produce accurate, context-aware responses.

**Context**: Used for LLM-powered systems that need access to Salesforce data. Involves extracting Salesforce data, transforming it into chunks, indexing in vector databases, and retrieving relevant context for LLM queries.

**Related Patterns**: See `rag/integrations/salesforce-to-llm-data-pipelines.md` for RAG pipeline patterns.

### LLM (Large Language Model)

**Definition**: AI model capable of understanding and generating human-like text, used in conjunction with RAG systems for context-aware responses.

**Context**: Used in Salesforce contexts for support agents, sales assistants, and knowledge base systems. Requires structured data extraction and transformation from Salesforce.

**Related Patterns**: See `rag/integrations/salesforce-to-llm-data-pipelines.md` for LLM integration patterns.

### Chunking

**Definition**: Process of breaking Salesforce data into smaller, manageable pieces (chunks) for indexing in vector databases and retrieval by RAG systems.

**Context**: Can be per-record (one chunk per Salesforce record) or aggregated (multiple related records in one chunk). Includes field selection, redaction, and relationship context preservation.

**Related Patterns**: See `rag/integrations/salesforce-to-llm-data-pipelines.md` for chunking strategies.

### Vector Database

**Definition**: Database optimized for storing and querying vector embeddings generated from text chunks for similarity search in RAG systems.

**Context**: Used to store Salesforce data chunks as embeddings, enabling semantic search and retrieval of relevant context for LLM queries.

**Related Patterns**: See `rag/integrations/salesforce-to-llm-data-pipelines.md` for indexing strategies.

## Operations Terms

### CI/CD (Continuous Integration/Continuous Deployment)

**Definition**: Automated software delivery process that integrates code changes and deploys them to environments automatically.

**Context**: Used for Salesforce deployments to ensure consistent, reliable deployments. Includes metadata vs. source-tracked orgs, unlocked packages, sandbox seeding, deployment validation, and rollback strategies.

**Related Patterns**: See `rag/operations/cicd-patterns.md` for CI/CD patterns.

### Source-Tracked Org

**Definition**: Salesforce org that automatically tracks changes made directly in the org, enabling bidirectional sync between org and source control.

**Context**: Used for modern development workflows with SFDX. Supports automatic change detection, better Git integration, and modern CI/CD tooling.

**Related Patterns**: See `rag/operations/cicd-patterns.md` for source-tracked org patterns.

### Unlocked Package

**Definition**: Salesforce package type for modular development, allowing versioned, reusable components that can be installed and upgraded independently.

**Context**: Used for breaking down large codebases into manageable, versioned packages. Supports dependency management, versioning, and package promotion workflows.

**Related Patterns**: See `rag/operations/cicd-patterns.md` for unlocked package patterns.

### CAB (Change Advisory Board)

**Definition**: Governance body that reviews and approves changes before deployment to production.

**Context**: Used for managing release governance, assessing change risk, coordinating release scheduling, and ensuring proper approval workflows.

**Related Patterns**: See `rag/operations/release-governance.md` for CAB patterns.

## Observability Terms

### LDV (Large Data Volume)

**Definition**: Salesforce org with 1 million+ records per object, requiring specialized data handling and query optimization strategies.

**Context**: Used to describe orgs with very large datasets. Requires indexed field usage, data archiving strategies, and LDV-specific query optimization.

**Related Patterns**: See `rag/observability/performance-tuning.md` for LDV handling patterns.

### RTO (Recovery Time Objective)

**Definition**: Maximum acceptable downtime, defining the time to restore system functionality after a disaster.

**Context**: Used in disaster recovery planning. Varies by system criticality (minutes to hours for critical systems, days to weeks for standard systems).

**Related Patterns**: See `rag/observability/ha-dr-patterns.md` for RTO planning.

### RPO (Recovery Point Objective)

**Definition**: Maximum acceptable data loss, defining the point in time to recover to after a disaster.

**Context**: Used in backup and disaster recovery planning. Determines backup frequency requirements (real-time replication for zero data loss, hours to days for acceptable data loss).

**Related Patterns**: See `rag/observability/ha-dr-patterns.md` for RPO planning.

### Circuit Breaker

**Definition**: Design pattern that prevents cascading failures by failing fast when a system is down, allowing time for recovery.

**Context**: Used in integration failover patterns. Has three states: Closed (normal operation), Open (fail fast), Half-Open (testing recovery).

**Related Patterns**: See `rag/observability/ha-dr-patterns.md` for circuit breaker patterns.

## Data Governance Terms

### PII (Personally Identifiable Information)

**Definition**: Data that can identify a specific individual, such as name, SSN, email, phone number, or biometric data.

**Context**: Used in data classification and protection strategies. Requires encryption, access controls, and compliance with regulations like GDPR and CCPA.

**Related Patterns**: See `rag/data-governance/data-residency-compliance.md` for PII handling patterns.

### PHI (Protected Health Information)

**Definition**: Health information that can identify an individual, including medical records, diagnoses, treatments, and health identifiers.

**Context**: Used in healthcare implementations. Requires HIPAA compliance, encryption, audit trails, and strict access controls.

**Related Patterns**: See `rag/data-governance/data-residency-compliance.md` for PHI protection patterns.

### GDPR (General Data Protection Regulation)

**Definition**: European Union regulation governing data protection and privacy for individuals within the EU.

**Context**: Used for implementations serving EU residents. Requires data subject rights (access, rectification, erasure, portability), consent management, and data processing documentation.

**Related Patterns**: See `rag/data-governance/data-residency-compliance.md` for GDPR compliance patterns.

### CCPA (California Consumer Privacy Act)

**Definition**: California state law providing consumers rights to know, delete, and opt-out of data sales.

**Context**: Used for implementations serving California residents. Requires consumer request processes, opt-out mechanisms, and privacy policy updates.

**Related Patterns**: See `rag/data-governance/data-residency-compliance.md` for CCPA compliance patterns.

### SOC2 (System and Organization Controls 2)

**Definition**: Security and compliance framework with five trust service criteria: Security, Availability, Processing Integrity, Confidentiality, and Privacy.

**Context**: Used for enterprise implementations requiring security certifications. Requires documented controls, regular audits, and audit evidence maintenance.

**Related Patterns**: See `rag/data-governance/data-residency-compliance.md` for SOC2 controls.

### Shield Platform Encryption

**Definition**: Salesforce encryption solution that encrypts data at rest in the database, search indexes, and file storage.

**Context**: Used for protecting sensitive data (PII/PHI). Supports deterministic encryption (searchable) and probabilistic encryption (maximum security).

**Related Patterns**: See `rag/data-governance/data-residency-compliance.md` for Shield encryption patterns.

### Survivorship Rules

**Definition**: Rules that determine which data values to keep when merging duplicate records.

**Context**: Used in data quality and duplicate management. Defines field-level priority rules (source priority, recency, completeness, quality score) for merge operations.

**Related Patterns**: See `rag/data-governance/data-quality-stewardship.md` for survivorship rule patterns.

### Master Data Governance

**Definition**: Process of managing master data entities (Customer, Product, Reference data) to ensure data quality, consistency, and single source of truth.

**Context**: Used for maintaining data quality at scale. Includes data stewardship workflows, data quality metrics, and automated quality checks.

**Related Patterns**: See `rag/data-governance/data-quality-stewardship.md` for master data governance patterns.

## Adoption Terms

### Feature Adoption Telemetry

**Definition**: Metrics and tracking for measuring how users adopt and use new features in the system.

**Context**: Used for measuring user engagement, identifying adoption barriers, and optimizing feature rollout. Tracks feature usage, frequency, depth, and user satisfaction.

**Related Patterns**: See `rag/adoption/user-readiness.md` for feature adoption patterns.

### Technical Debt

**Definition**: Accumulated shortcuts, workarounds, and suboptimal implementations that require future remediation.

**Context**: Used in org health management. Includes code debt, configuration debt, data debt, security debt, performance debt, and documentation debt.

**Related Patterns**: See `rag/adoption/org-health-checks.md` for technical debt triage patterns.

### Baseline Audit

**Definition**: Comprehensive assessment of org health, including code quality, configuration complexity, data quality, security, and performance.

**Context**: Used for establishing org health baselines, identifying issues, and tracking improvements over time.

**Related Patterns**: See `rag/adoption/org-health-checks.md` for baseline audit patterns.

## Related Documentation

For domain-specific terminology and definitions, see:

- **Integration Terms**: `rag/integrations/etl-vs-api-vs-events.md`, `rag/integrations/salesforce-to-llm-data-pipelines.md`
- **Identity Terms**: `rag/identity-sso/multi-tenant-identity-architecture.md`
- **Data Model Terms**: `rag/data-modeling/student-lifecycle-data-model.md`
- **Security Terms**: `rag/security/permission-set-architecture.md`, `rag/security/salesforce-llm-data-governance.md`
- **Development Terms**: `rag/development/apex-patterns.md`, `rag/development/flow-patterns.md`, `rag/development/lwc-patterns.md`, `rag/development/locking-and-concurrency-strategies.md`, `rag/development/governor-limits-and-optimization.md`
- **Operations Terms**: `rag/operations/cicd-patterns.md`, `rag/operations/environment-strategy.md`, `rag/operations/release-governance.md`
- **Observability Terms**: `rag/observability/monitoring-alerting.md`, `rag/observability/performance-tuning.md`, `rag/observability/ha-dr-patterns.md`
- **Data Governance Terms**: `rag/data-governance/data-residency-compliance.md`, `rag/data-governance/data-quality-stewardship.md`
- **Adoption Terms**: `rag/adoption/user-readiness.md`, `rag/adoption/org-health-checks.md`

