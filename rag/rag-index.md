# RAG Knowledge Library Index

## Overview

This RAG (Retrieval-Augmented Generation) knowledge library contains structured knowledge derived from real Salesforce implementation experience. All content has been sanitized to remove identifying information and organized for efficient retrieval by AI systems.

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

### event-driven-architecture.md

**When to Retrieve**: Questions about event-driven integration, Platform Events, asynchronous processing, event bus patterns, or decoupling Salesforce from external systems.

**Summary**: Comprehensive guide to event-driven architecture using Platform Events. Covers event publication patterns, external event bus integration (EventBridge reference), payload design, error handling, and best practices. Includes when to use events vs. APIs vs. ETL.

**Key Topics**:
- Platform Events publication from Flows and Apex
- External event bus patterns (EventBridge)
- Event payload design (self-contained, minimal PII, idempotent)
- Internal event consumption via Channel Members
- Error handling and monitoring patterns

### portal-architecture.md

**When to Retrieve**: Questions about Experience Cloud portal architecture, multi-tenant portal implementations, portal user experience design, or identity-aware portal routing.

**Summary**: Experience Cloud portal architecture patterns for supporting multiple user types (students/applicants, external partners/providers, citizens/clients) with different identity providers, security requirements, and access patterns.

**Key Topics**:
- Student/applicant portal patterns
- External partner/provider portal patterns
- Citizen/client portal patterns
- Identity-aware behavior and routing
- Sharing and security for portals

## Integration Patterns

### etl-vs-api-vs-events.md

**When to Retrieve**: Questions about choosing between ETL, API, or Events integration patterns, or understanding tradeoffs between integration approaches.

**Summary**: Decision framework for selecting integration patterns. Covers when to use ETL (batch), API (synchronous), or Events (asynchronous), with implementation patterns, best practices, and tradeoffs for each approach.

**Key Topics**:
- ETL pattern for high-volume batch synchronization
- API pattern for real-time request/response
- Events pattern for asynchronous processing
- Hybrid pattern combinations
- Decision framework and selection criteria

### integration-platform-patterns.md

**When to Retrieve**: Questions about MuleSoft or Dell Boomi integration platforms, security boundaries for integrations, transformation layers, or high-volume ETL operations.

**Summary**: Patterns for using integration platforms (MuleSoft and Dell Boomi). Covers MuleSoft as security boundary and transformation layer, Boomi for high-volume ETL, file-based staging, dynamic SQL batching, and best practices for both platforms.

**Key Topics**:
- MuleSoft as security boundary (VPN, IP whitelisting)
- MuleSoft transformation layer (DataWeave)
- Boomi high-volume batch processing
- File-based staging for large data sets
- Integration job tracking patterns

### sis-sync-patterns.md

**When to Retrieve**: Questions about SIS synchronization, high-volume batch integration patterns, file-based staging for large data sets, or student data synchronization.

**Summary**: High-volume batch synchronization patterns for integrating Salesforce Education Cloud with legacy Student Information Systems (SIS). Covers file-based staging, dynamic SQL batching, and idempotent upserts.

**Key Topics**:
- File-based staging for large ID lists
- Dynamic SQL IN-clause batching
- Idempotent upserts with external IDs
- Integration job tracking
- Error handling and retry logic

## Identity and SSO

### multi-tenant-identity-architecture.md

**When to Retrieve**: Questions about multi-tenant identity, multiple identity providers (OIDC, SAML, organization tenant), login handlers, or supporting different user types in a single org.

**Summary**: Comprehensive guide to multi-tenant identity architecture supporting multiple user communities (citizens, external partner organizations, internal staff) with different identity providers. Covers OIDC, SAML, organization tenant identity, login handler patterns, Record Type-based separation, and sharing models.

**Key Topics**:
- OIDC for external users (citizens/clients)
- SAML for internal staff
- Organization tenant identity for external partners
- Login handler patterns and matching strategies
- Record Type-based user separation
- Sharing and security by identity type

## Data Modeling

### external-ids-and-integration-keys.md

**When to Retrieve**: Questions about external IDs, integration keys, composite external IDs, idempotent upserts, or integration job tracking.

**Summary**: Comprehensive guide to external ID strategies for stable record mapping between Salesforce and external systems. Covers external ID design principles, composite external IDs, integration job tracking fields, idempotent upsert patterns, and best practices.

**Key Topics**:
- External ID design principles (stable, unique, mirror external keys)
- Composite external IDs for multi-column keys
- Integration job tracking fields (Last_Sync_Timestamp, Last_Sync_Status, etc.)
- Idempotent upsert patterns
- Multi-system external ID management

### student-lifecycle-data-model.md

**When to Retrieve**: Questions about Education Cloud data modeling, student and applicant data models, program enrollment modeling, or SIS integration data models.

**Summary**: Salesforce Education Cloud (EDA) data model supporting higher education institutions. Covers Contact as core student record, Program Enrollment objects, Application objects, and SIS integration patterns.

**Key Topics**:
- Contact as core student/applicant record
- Program Enrollment and Course Enrollment objects
- Application object design
- SIS integration data model
- Derived fields from SIS data

### case-management-data-model.md

**When to Retrieve**: Questions about public sector case management, multi-tenant case data models, notice and transaction objects, or client-external partner relationship modeling.

**Summary**: Comprehensive data model for public sector case management, supporting multi-agency public benefits and services portals. Covers clients, external partner organizations, staff, cases, notices, and transactions within a single Salesforce org.

**Key Topics**:
- Client Accounts/Contacts modeling
- External Partner (Provider) Accounts
- Case management model
- Notice and Transaction objects
- Multi-tenant data isolation

## Security

### permission-set-architecture.md

**When to Retrieve**: Questions about permission set-driven security, transitioning from profile-centric to permission set-based access control, or managing permissions at scale.

**Summary**: Guide to permission set-driven security architecture. Covers profile structure (minimal UI configuration), permission set structure (comprehensive access control), permission set groups, migration strategy, and best practices for managing permissions at scale.

**Key Topics**:
- Profiles = UI configuration only
- Permission Sets = Access control
- Permission Set Groups for role-based assignment
- No delete permissions for community users
- Migration strategy from profile-centric model

## Development

### error-handling-and-logging.md

**When to Retrieve**: Questions about error handling, logging frameworks, compliance logging, troubleshooting, or audit trails.

**Summary**: Comprehensive error handling and logging framework using custom LOG_LogMessage__c object. Covers logging utility classes, platform event fallbacks, structured logging, integration with external logging platforms, and compliance requirements.

**Key Topics**:
- Custom logging object (LOG_LogMessage__c)
- LOG_LogMessageUtility class
- Platform event fallback for DML failures
- Structured logging format
- Integration with centralized logging (OpenSearch, Splunk)
- Compliance and audit trail requirements

### apex-patterns.md

**When to Retrieve**: Questions about Apex design patterns, when to choose Apex over Flow, Apex class layering, SOQL optimization, or Apex testing strategies.

**Summary**: Apex design patterns and best practices. Covers when to choose Apex, class layering (Service, Domain, Selector, Integration), SOQL design, asynchronous patterns, Apex+LWC integration, error handling, and testing strategies.

**Key Topics**:
- When to choose Apex over Flow
- Apex class layering (Service, Domain, Selector, Integration)
- SOQL design and optimization
- Asynchronous Apex patterns (Queueable, Batchable, Scheduled)
- Apex + LWC integration patterns
- Error handling and testing strategies

### flow-patterns.md

**When to Retrieve**: Questions about Flow design, Record-triggered Flow patterns, Screen Flow design, Flow + Apex integration, or Flow performance optimization.

**Summary**: Flow design and orchestration patterns. Covers Flow type selection, Record-Triggered Flow structure, Screen Flow design, Flow+Apex integration, naming conventions, error handling, and performance optimization.

**Key Topics**:
- Flow type selection (Record-Triggered, Subflows, Screen, Scheduled, Auto-Launched)
- Record-Triggered Flow structure patterns
- Screen Flow design patterns
- Flow + Apex integration patterns
- Flow naming and documentation
- Error handling and performance

### lwc-patterns.md

**When to Retrieve**: Questions about Lightning Web Component patterns, console-style LWCs, program selection components, fraud/risk scoring components, or LWC performance optimization.

**Summary**: Lightning Web Component (LWC) patterns for complex business logic. Covers console-style LWCs, fraud/risk scoring components, program-selection components, service-layer patterns, config-driven UI, and performance optimization.

**Key Topics**:
- Console-style LWC patterns
- Fraud/risk scoring LWC implementation
- Program-selection LWC patterns
- Service-layer pattern for LWCs
- Config-driven UI patterns
- Performance optimization and accessibility

### omnistudio-patterns.md

**When to Retrieve**: Questions about OmniStudio, OmniScript design patterns, FlexCard patterns, grant management workflows, or OmniStudio performance optimization.

**Summary**: OmniStudio (OmniScripts and FlexCards) patterns for guided workflows and reusable UI components. Covers OmniScript design, FlexCard design, grant management workflows, integration patterns, and performance optimization.

**Key Topics**:
- OmniScripts for guided processes
- FlexCards for reusable UI components
- Grant management workflows
- Integration with Salesforce data model
- Performance optimization and error handling

## Troubleshooting

### integration-debugging.md

**When to Retrieve**: Questions about integration troubleshooting, SOQL debugging patterns, root cause analysis, integration error analysis, or data quality debugging.

**Summary**: Systematic approaches to troubleshooting integration failures, identifying root causes, and resolving data synchronization issues. Covers SOQL debugging, history object queries, error investigation, and metadata analysis.

**Key Topics**:
- SOQL debugging patterns
- History object queries for change tracking
- Root cause analysis techniques
- Integration error analysis
- Data quality debugging methods

### data-reconciliation.md

**When to Retrieve**: Questions about data reconciliation, external ID-based reconciliation, field-level reconciliation, discrepancy identification, or reconciliation reporting.

**Summary**: Systematic approaches to reconciling data between Salesforce and external systems, identifying discrepancies, and ensuring data consistency. Covers external ID-based reconciliation, integration job tracking, and reconciliation workflows.

**Key Topics**:
- External ID-based reconciliation
- Integration job tracking reconciliation
- Field-level reconciliation
- Discrepancy identification
- Reconciliation reporting and alerting

## Patterns

### cross-cutting-patterns.md

**When to Retrieve**: Questions about reusable patterns across domains, governor limit management, bulkification patterns, cross-cutting design patterns, or patterns that span multiple domains.

**Summary**: Summary of cross-cutting patterns that appear across multiple domains. Covers governor limit management, bulkification, external ID patterns, error handling, data quality, security patterns, integration pattern selection, portal design, and testing patterns. Links to detailed domain-specific documentation.

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

### core-terminology.md

**When to Retrieve**: Questions about terminology definitions, clarifying what a term means, understanding acronyms and abbreviations, or core concepts and definitions.

**Summary**: Core terminology and definitions used throughout the RAG knowledge library. Covers integration terms (ETL, API, Platform Events, External ID), identity terms (OIDC, SAML, Login Handler), data model terms (SIS, EDA, Record Type), security terms (Permission Set, Sharing Set), platform terms (Experience Cloud, GovCloud), development terms (LWC, OmniStudio, Flow, Apex), and project method terms.

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

### delivery-framework.md

**When to Retrieve**: Questions about sprint-based delivery, stakeholder coordination, quality standards, change management, or project delivery methodology.

**Summary**: Sprint-based delivery approach for managing complex multi-stakeholder Salesforce projects. Covers sprint structure, stakeholder coordination, testing window coordination, change management, and comprehensive quality standards.

**Key Topics**:
- Sprint-based delivery structure
- Stakeholder coordination practices
- Testing window coordination
- Change management and documentation alignment
- Comprehensive quality standards

### testing-strategy.md

**When to Retrieve**: Questions about testing strategies, integration testing, data quality testing, user migration testing, or user acceptance testing.

**Summary**: Comprehensive testing strategies covering integration testing, data quality testing, user migration testing, and user acceptance testing. Validates Salesforce configurations, integrations, and portal functionality across multiple environments.

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
