# Salesforce RAG Knowledge Library

A structured knowledge library containing implementation patterns, best practices, and architectural guidance derived from real Salesforce implementation experience. All content has been sanitized to remove identifying information and organized for efficient retrieval by AI systems and human developers.

## Overview

This repository provides a Retrieval-Augmented Generation (RAG) knowledge base for Salesforce implementations, covering the full spectrum from development to operations, governance, and adoption. All content is derived from real implementation experience and organized for efficient retrieval by AI systems and human developers.

### Core Domains

- **Architecture Patterns**: Event-driven architecture with Platform Events, Experience Cloud portal architecture for multiple user communities, multi-tenant solutions, and system design patterns

- **Integration Patterns**: ETL vs. API vs. Events decision frameworks, integration platforms (MuleSoft, Dell Boomi), Student Information System (SIS) synchronization, Change Data Capture (CDC), and Salesforce-to-LLM data pipelines

- **Identity & SSO**: Multi-tenant identity architecture supporting multiple user communities, multiple identity providers (OIDC, SAML, organization tenant), login handlers, and identity-aware routing

- **Data Modeling**: External IDs and integration keys, student lifecycle models (Education Cloud/EDA), case management models, lead management and conversion, object setup and configuration, file management patterns, and data migration strategies

- **Security**: Permission set-driven security architecture, field-level security, Salesforce-to-LLM data governance, access control patterns, and security best practices

### Development & Quality

- **Development**: Apex patterns (Service, Domain, Selector, Integration layers), Flow design and orchestration, Lightning Web Components (LWC), OmniStudio patterns, error handling and logging frameworks, order of execution, locking and concurrency, governor limits and optimization, SOQL query patterns, asynchronous Apex (Batch, Queueable, Scheduled), and Custom Settings/Metadata patterns

- **Testing**: Apex testing patterns, test data factories, automated testing at scale (UI automation, contract tests, load testing), non-functional requirements (security testing, accessibility, performance benchmarks), and comprehensive testing strategies

### Operations & Observability

- **Operations**: CI/CD patterns (metadata vs. source-tracked orgs, unlocked packages, sandbox seeding, deployment validation, rollback strategies), environment strategy (org topologies for multi-team programs, data masking, refresh cadences), and release governance (Change Advisory Boards, approval workflows, risk-based checklists)

- **Observability**: Monitoring and alerting (Platform Events monitoring, API health, async job failures, log aggregation), performance tuning (query/selectivity optimization, Large Data Volume handling, governor limit mitigation, caching strategies), and high availability & disaster recovery (backup/restore, failover patterns, business continuity drills)

### Governance & Adoption

- **Data Governance**: Data residency and compliance (PII/PHI handling, GDPR/CCPA/SOC2 controls, field-level encryption, Shield best practices), data quality and stewardship (duplicate prevention beyond leads, survivorship rules, master data governance)

- **Adoption**: User readiness (training plans, support models, feature adoption telemetry), org health checks (technical debt triage, baseline audits, remediation playbooks), and change management patterns

### Supporting Domains

- **Troubleshooting**: Integration debugging, data reconciliation, common Apex/LWC errors, governor limit errors, and root cause analysis techniques

- **Project Methods**: Sprint-based delivery frameworks, comprehensive testing strategies, deployment patterns, and Salesforce DX (SFDX) patterns

- **Patterns**: Cross-cutting patterns that span multiple domains (governor limit management, bulkification, external IDs, error handling, security)

- **Code Examples**: Complete, working code examples organized by category (Apex, LWC, Flow, integrations, utilities, templates) - all copy-paste ready with tests

- **Quick Start Guides**: Step-by-step guides for getting started with Apex, LWC, and other Salesforce technologies

- **API Reference**: Quick reference for common APIs, methods, and patterns (Apex, LWC, LDS, SOQL, Platform Events)

- **MCP Knowledge**: Official Salesforce guidance and best practices extracted from Salesforce MCP Service tools

- **Glossary**: Core terminology and definitions for integration, identity, data modeling, security, platform, development, and project method terms

## Repository Structure

```
rag/
├── architecture/          # System architecture patterns
│   ├── event-driven-architecture.md
│   └── portal-architecture.md
│
├── integrations/          # Integration patterns and platforms
│   ├── etl-vs-api-vs-events.md
│   ├── integration-platform-patterns.md
│   ├── sis-sync-patterns.md
│   ├── salesforce-to-llm-data-pipelines.md
│   └── change-data-capture-patterns.md
│
├── identity-sso/         # Identity and SSO patterns
│   └── multi-tenant-identity-architecture.md
│
├── data-modeling/        # Data modeling patterns
│   ├── external-ids-and-integration-keys.md
│   ├── student-lifecycle-data-model.md
│   ├── case-management-data-model.md
│   ├── lead-management-patterns.md
│   ├── object-setup-and-configuration.md
│   ├── file-management-patterns.md
│   └── data-migration-patterns.md
│
├── security/             # Security and access control patterns
│   ├── permission-set-architecture.md
│   └── salesforce-llm-data-governance.md
│
├── operations/            # Delivery & operations patterns
│   ├── cicd-patterns.md              # CI/CD, packages, sandbox seeding, rollback
│   ├── environment-strategy.md       # Org topologies, data masking, refresh cadences
│   └── release-governance.md         # CAB, approval workflows, risk-based checklists
│
├── observability/         # Observability & resilience patterns
│   ├── monitoring-alerting.md        # Platform Events, API health, async jobs, logs
│   ├── performance-tuning.md         # Query optimization, LDV, governor limits, caching
│   └── ha-dr-patterns.md             # Backup/restore, failover, business continuity
│
├── data-governance/      # Data governance & compliance patterns
│   ├── data-residency-compliance.md  # PII/PHI, GDPR/CCPA/SOC2, encryption, Shield
│   └── data-quality-stewardship.md   # Duplicate prevention, survivorship, MDM
│
├── adoption/              # Adoption & change management patterns
│   ├── user-readiness.md             # Training plans, support models, adoption telemetry
│   └── org-health-checks.md          # Technical debt, baseline audits, remediation
│
├── project-methods/      # Project delivery and methodology
│   ├── delivery-framework.md
│   ├── testing-strategy.md
│   ├── deployment-patterns.md
│   └── sfdx-patterns.md
│
├── development/          # Development patterns and practices
│   ├── error-handling-and-logging.md
│   ├── apex-patterns.md
│   ├── flow-patterns.md
│   ├── order-of-execution.md
│   ├── lwc-patterns.md
│   ├── omnistudio-patterns.md
│   ├── locking-and-concurrency-strategies.md
│   ├── governor-limits-and-optimization.md
│   ├── soql-query-patterns.md
│   ├── asynchronous-apex-patterns.md
│   └── custom-settings-metadata-patterns.md
│
├── testing/              # Testing patterns and examples
│   ├── apex-testing-patterns.md
│   ├── test-data-factories.md
│   ├── automated-testing-patterns.md    # UI automation, contract tests, load testing
│   └── non-functional-requirements.md   # Security, accessibility, performance testing
│
├── troubleshooting/      # Debugging and troubleshooting
│   ├── integration-debugging.md
│   ├── data-reconciliation.md
│   ├── common-apex-errors.md
│   ├── common-lwc-errors.md
│   └── governor-limit-errors.md
│
├── patterns/             # Reusable design patterns
│   └── cross-cutting-patterns.md
│
├── code-examples/        # Complete, working code examples
│   ├── apex/             # Service, Domain, Selector, Integration, Trigger, Batch, Queueable, Scheduled
│   ├── lwc/              # Component examples
│   ├── flow/             # Flow examples
│   ├── integrations/     # REST API, Platform Events, CDC, Bulk API
│   ├── utilities/        # Logging, error handling, validation, Custom Settings/Metadata, SFDX
│   └── templates/        # Copy-paste ready templates for all patterns
│
├── quick-start/          # Quick-start guides
│   ├── apex-quick-start.md
│   └── lwc-quick-start.md
│
├── api-reference/        # API references and method signatures
│   ├── apex-api-reference.md
│   ├── lwc-api-reference.md
│   ├── lds-api-reference.md
│   ├── soql-reference.md
│   └── platform-events-api.md
│
├── mcp-knowledge/        # MCP-extracted knowledge
│   ├── lwc-development-guide.md
│   ├── lwc-best-practices.md
│   ├── lwc-accessibility.md
│   ├── lds-patterns.md
│   └── design-system-patterns.md
│
├── glossary/             # Terminology and definitions
│   └── core-terminology.md
│
├── rag-index.md          # Human-readable index of all knowledge files
└── rag-library.json      # Machine-readable metadata for RAG systems
```

## Quick Start

### For Humans

1. **Browse the index**: Start with [`rag/rag-index.md`](rag/rag-index.md) to find relevant knowledge files
2. **Read domain overviews**: Each domain section in the index provides a brief overview
3. **Find specific topics**: Use the "When to Retrieve" guidance to locate relevant files
4. **Read the files**: Each markdown file contains detailed patterns and best practices

### For AI Systems / RAG Tools

1. **Use the JSON metadata**: [`rag/rag-library.json`](rag/rag-library.json) contains structured metadata for each knowledge file
2. **Query by domain**: Filter files by `domain` field (architecture, integrations, development, etc.)
3. **Match questions to files**: Use `whenToRetrieve` arrays to find relevant files for a given question
4. **Retrieve summaries**: Use `summary` and `keyTopics` fields for quick context

## Usage Examples

See the [`examples/`](examples/) directory for detailed usage examples:

- **[Cursor IDE Usage](examples/cursor-usage.md)**: Step-by-step guide for using this library with Cursor's RAG features, including prompt patterns and workflows
- **[Generic RAG Integration](examples/generic-rag-usage.md)**: Integration examples for LangChain, LlamaIndex, and other RAG frameworks with complete code samples

## Content Characteristics

All content in this library:

- ✅ **Evidence-Based**: Derived from real implementation experience
- ✅ **Sanitized**: All identifying information removed (company names, client names, project codenames)
- ✅ **Pattern-Focused**: Emphasizes reusable patterns and best practices
- ✅ **Decision-Oriented**: Includes architectural decisions and tradeoffs
- ✅ **Implementation-Ready**: Provides actionable guidance for implementation

## Key Files

- **`rag/rag-index.md`**: Human-readable index with domain overviews and file descriptions
- **`rag/rag-library.json`**: Machine-readable metadata with structured information for each knowledge file
- **`examples/`**: Usage examples for different RAG frameworks and tools
- **`QUALITY.md`**: Quality assurance checklist and verification guidelines for ensuring best-practice coverage

## Terminology

Common terms used throughout the library:

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

For complete terminology definitions, see [`rag/glossary/core-terminology.md`](rag/glossary/core-terminology.md).

## Contributing

This library is derived from immutable source documents and implementation experience. Content is organized by domain and follows consistent patterns:

1. Each knowledge file focuses on a specific topic or pattern
2. Files include practical examples and implementation guidance
3. All identifying information is removed (anonymized)
4. Patterns are reusable and applicable across different implementations


