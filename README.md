# Salesforce RAG Knowledge Library

A structured knowledge library containing implementation patterns, best practices, and architectural guidance derived from real Salesforce implementation experience. All content has been sanitized to remove identifying information and organized for efficient retrieval by AI systems and human developers.

## Overview

This repository provides a Retrieval-Augmented Generation (RAG) knowledge base for Salesforce implementations, covering:

- **Architecture Patterns**: Event-driven architecture, portal architecture, multi-tenant solutions
- **Integration Patterns**: ETL, API, and event-driven integrations, integration platforms (MuleSoft, Dell Boomi), SIS synchronization
- **Identity & SSO**: Multi-tenant identity architecture, multiple identity providers (OIDC, SAML)
- **Data Modeling**: External IDs, integration keys, student lifecycle models, case management models
- **Security**: Permission set-driven security architecture
- **Development**: Apex, Flow, Lightning Web Components (LWC), OmniStudio patterns, error handling, logging
- **Troubleshooting**: Integration debugging, data reconciliation, root cause analysis
- **Project Methods**: Sprint-based delivery, testing strategies, quality standards
- **Patterns**: Cross-cutting patterns that span multiple domains
- **Glossary**: Core terminology and definitions

## Repository Structure

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

## License

[Add your license information here]

## Support

For questions or issues related to this knowledge library, please [add your support channel information here].

