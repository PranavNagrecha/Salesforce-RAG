# RAG Knowledge Library Index

## Overview

This RAG (Retrieval-Augmented Generation) knowledge library contains structured knowledge derived from real Salesforce implementation experience. All content has been sanitized to remove identifying information and organized for efficient retrieval by AI systems.

## How to use this index

- **LLMs or tools** can use this file to decide which `rag/**` docs to retrieve for a given question.
- **Humans** can skim domains to understand what knowledge is available.
- **See the README** for details on using this repository with Cursor or other RAG frameworks.

## Directory Structure

```
rag/
├── architecture/          # System architecture patterns
├── integrations/          # Integration patterns and platforms
├── identity-sso/         # Identity and SSO patterns
├── data-modeling/        # Data modeling patterns
├── security/             # Security and access control patterns
├── project-methods/      # Project delivery and methodology
├── development/          # Development patterns and practices
├── troubleshooting/      # Debugging and troubleshooting
├── patterns/             # Reusable design patterns
├── glossary/             # Terminology and definitions
└── rag-index.md          # This file
```

## Architecture Patterns

Architecture patterns for designing system structure, integration patterns, multi-tenant solutions, and portal architecture.

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

Integration patterns and platforms for ETL, API, and event-driven integrations, SIS synchronization, and integration platforms like MuleSoft and Dell Boomi.

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

## Identity and SSO

Identity and SSO patterns for implementing SSO, multi-identity provider architectures, and login handlers.

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

## Security

Security and access control patterns for implementing permission set-driven security and managing access control.

### permission-set-architecture.md

**When to Retrieve**: Implementing permission set-driven security architecture, migrating from profile-centric to permission set-based access control, managing permissions at scale using Permission Set Groups, or designing security models for community users.

**Summary**: Guide to permission set-driven security architecture. Teaches using Profiles for UI configuration only, Permission Sets for comprehensive access control, Permission Set Groups for role-based assignment, migration strategy from profile-centric model, and best practices for managing permissions at scale. Includes restrictions for community users.

**Key Topics**:
- Profiles = UI configuration only
- Permission Sets = Access control
- Permission Set Groups for role-based assignment
- No delete permissions for community users
- Migration strategy from profile-centric model

## Development

Development patterns and practices for implementing Apex, Flow, LWC, OmniStudio, error handling, logging, and troubleshooting patterns.

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

**When to Retrieve**: Deciding when to use Apex vs. Flow, implementing Apex class layering (Service, Domain, Selector, Integration), optimizing SOQL queries and managing governor limits, designing asynchronous Apex (Queueable, Batchable, Scheduled), or integrating Apex with Lightning Web Components.

**Summary**: Apex design patterns and best practices. Covers decision framework for when to choose Apex over Flow, class layering patterns (Service, Domain, Selector, Integration), SOQL design and optimization, asynchronous patterns (Queueable, Batchable, Scheduled), Apex+LWC integration patterns, error handling, and testing strategies.

**Key Topics**:
- When to choose Apex over Flow
- Apex class layering (Service, Domain, Selector, Integration)
- SOQL design and optimization
- Asynchronous Apex patterns (Queueable, Batchable, Scheduled)
- Apex + LWC integration patterns
- Error handling and testing strategies

### flow-patterns.md

**When to Retrieve**: Selecting the right Flow type for automation, designing Record-Triggered Flows with proper structure, building Screen Flows for user interactions, integrating Flows with Apex for complex logic, or optimizing Flow performance and handling errors.

**Summary**: Flow design and orchestration patterns. Covers Flow type selection (Record-Triggered, Subflows, Screen, Scheduled, Auto-Launched), Record-Triggered Flow structure patterns, Screen Flow design patterns, Flow+Apex integration patterns, naming conventions, error handling, and performance optimization.

**Key Topics**:
- Flow type selection (Record-Triggered, Subflows, Screen, Scheduled, Auto-Launched)
- Record-Triggered Flow structure patterns
- Screen Flow design patterns
- Flow + Apex integration patterns
- Flow naming and documentation
- Error handling and performance

### lwc-patterns.md

**When to Retrieve**: Building console-style Lightning Web Components, implementing complex business logic in LWCs, designing service-layer patterns for LWCs, creating config-driven UI components, or optimizing LWC performance and accessibility.

**Summary**: Lightning Web Component (LWC) patterns for complex business logic. Covers console-style LWC patterns, fraud/risk scoring component implementation, program-selection component patterns, service-layer patterns for LWCs, config-driven UI patterns, and performance optimization with accessibility considerations.

**Key Topics**:
- Console-style LWC patterns
- Fraud/risk scoring LWC implementation
- Program-selection LWC patterns
- Service-layer pattern for LWCs
- Config-driven UI patterns
- Performance optimization and accessibility

### omnistudio-patterns.md

**When to Retrieve**: Designing OmniScripts for guided workflows, creating FlexCards for reusable UI components, implementing grant management workflows with OmniStudio, integrating OmniStudio with Salesforce data model, or optimizing OmniStudio performance and error handling.

**Summary**: OmniStudio (OmniScripts and FlexCards) patterns for guided workflows and reusable UI components. Covers OmniScript design patterns for guided processes, FlexCard design for reusable UI, grant management workflow patterns, integration with Salesforce data model, and performance optimization with error handling.

**Key Topics**:
- OmniScripts for guided processes
- FlexCards for reusable UI components
- Grant management workflows
- Integration with Salesforce data model
- Performance optimization and error handling

## Troubleshooting

Debugging and troubleshooting approaches for integration debugging, data reconciliation, and root cause analysis.

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

**When to Retrieve**: Planning comprehensive testing strategies for Salesforce projects, designing integration testing (connectivity, transformation, error handling), implementing data quality testing (matching, deduplication, error capture), testing user migration and login handlers, or conducting user acceptance testing (UAT).

**Summary**: Comprehensive testing strategies for Salesforce implementations. Covers integration testing (connectivity, data transformation, error handling), data quality testing (matching, deduplication, error capture), user migration and login handler testing, user acceptance testing (UAT), and test environment management.

**Key Topics**:
- Integration testing (connectivity, data transformation, error handling)
- Data quality testing (matching, deduplication, error capture)
- User migration and login handler testing
- User acceptance testing (UAT)
- Test environment management

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
10. **Terminology Questions**: Clarifying what a term means or understanding core concepts

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

### Completed Files (21 total)

**Architecture (2 files)**:
- ✅ `architecture/event-driven-architecture.md`
- ✅ `architecture/portal-architecture.md`

**Integrations (3 files)**:
- ✅ `integrations/etl-vs-api-vs-events.md`
- ✅ `integrations/integration-platform-patterns.md`
- ✅ `integrations/sis-sync-patterns.md`

**Identity & SSO (1 file)**:
- ✅ `identity-sso/multi-tenant-identity-architecture.md`

**Data Modeling (3 files)**:
- ✅ `data-modeling/external-ids-and-integration-keys.md`
- ✅ `data-modeling/student-lifecycle-data-model.md`
- ✅ `data-modeling/case-management-data-model.md`

**Security (1 file)**:
- ✅ `security/permission-set-architecture.md`

**Development (5 files)**:
- ✅ `development/error-handling-and-logging.md`
- ✅ `development/apex-patterns.md`
- ✅ `development/flow-patterns.md`
- ✅ `development/lwc-patterns.md`
- ✅ `development/omnistudio-patterns.md`

**Troubleshooting (2 files)**:
- ✅ `troubleshooting/integration-debugging.md`
- ✅ `troubleshooting/data-reconciliation.md`

**Project Methods (2 files)**:
- ✅ `project-methods/delivery-framework.md`
- ✅ `project-methods/testing-strategy.md`

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
