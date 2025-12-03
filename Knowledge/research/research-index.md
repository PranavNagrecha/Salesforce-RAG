# Salesforce Research Layer – Index

This folder contains **external research** to complement the lived-experience RAG library.

- All files here are *secondary* references.

- They are meant to inform and challenge the RAG content, not silently overwrite it.

## Topics

### Development

- [Locking and concurrency strategies](topics/development-locking-and-concurrency-strategies.md)

- [Flow best practices](topics/development-flow-best-practices.md) *(planned)*

- [LWC patterns](topics/development-lwc-patterns.md) *(planned)*

### Integrations

- [API design reference](topics/integrations-api-design-reference.md) *(planned)*

- [Bulk data strategies](topics/integrations-bulk-data-strategies.md) *(planned)*

- [Event-driven patterns](topics/integrations-event-driven-patterns.md) *(planned)*

### Security

- [Access & governance reference](topics/security-access-governance-reference.md) *(planned)*

### Testing & Delivery

- [Apex and test class lessons learned](topics/apex-test-class-lessons-learned.md)

- [Apex and integration tests](topics/testing-apex-and-integration-tests.md) *(planned)*

- [CI/CD and release strategy](topics/project-methods-ci-cd-and-release-strategy.md) *(planned)*

### Performance & Operations

- [Governor limits & optimization](topics/performance-governor-limits-and-optimization.md)

- [Common production issues](topics/troubleshooting-common-production-issues.md) *(planned)*

### LLM Data Pipelines

- [Salesforce → LLM data pipeline patterns](llm/llm-salesforce-data-pipelines.md) — High-level pipeline patterns for extracting, transforming, and loading Salesforce data into LLM/RAG systems, including batch, event-driven, and on-demand approaches

- [Profile/connector manifest gaps](llm/llm-salesforce-profile-manifest-gaps.md) — Explains what manifest-style descriptions cover and what they miss for Salesforce → LLM use cases, including security model, relationships, and business logic gaps

- [Data scope and security for LLM systems](llm/llm-salesforce-data-scope-and-security.md) — How to choose what data to expose from Salesforce to LLMs and how to do that safely, including scoping principles, security mapping, and governance patterns

- [Sources and references](sources/llm-salesforce-to-llm-sources.md) — External sources and references used across all Salesforce → LLM research topics

## How This Interacts With RAG

- RAG (`rag/**`) = my **lived experience** and patterns.

- Research (`Knowledge/research/**`) = **external references** that may:

  - confirm what RAG already says,

  - show gaps where RAG can be improved,

  - highlight areas that need human judgment.

Use this index when:

- You want a more "textbook + ecosystem" view of a topic.

- You are considering enhancements to RAG.

