---
layout: default
title: Salesforce RAG Knowledge Library
description: A comprehensive knowledge library containing implementation patterns, best practices, and architectural guidance derived from real Salesforce implementation experience. Organized for efficient retrieval by AI systems and human developers.
permalink: /
---

# Salesforce RAG Knowledge Library

<div class="intro">
  <p class="lead">A structured knowledge library containing implementation patterns, best practices, and architectural guidance derived from real Salesforce implementation experience. All content has been sanitized to remove identifying information and organized for efficient retrieval by AI systems and human developers.</p>
</div>

## Overview

This repository provides a **Retrieval-Augmented Generation (RAG) knowledge base** for Salesforce implementations, covering the full spectrum from development to operations, governance, and adoption. All content is derived from real implementation experience and organized for efficient retrieval by AI systems and human developers.

## Quick Navigation

<div class="domain-grid">
  <div class="domain-card">
    <h3><a href="/rag/architecture/">🏗️ Architecture Patterns</a></h3>
    <p>Event-driven architecture, portal architecture, multi-tenant solutions, and system design patterns</p>
  </div>
  
  <div class="domain-card">
    <h3><a href="/rag/integrations/">🔌 Integration Patterns</a></h3>
    <p>ETL vs. API vs. Events decision frameworks, MuleSoft, Dell Boomi, SIS synchronization, CDC, and Salesforce-to-LLM pipelines</p>
  </div>
  
  <div class="domain-card">
    <h3><a href="/rag/development/">💻 Development</a></h3>
    <p>Apex patterns, Flow design, Lightning Web Components (LWC), OmniStudio, error handling, and performance optimization</p>
  </div>
  
  <div class="domain-card">
    <h3><a href="/rag/data-modeling/">📊 Data Modeling</a></h3>
    <p>External IDs, integration keys, student lifecycle models, case management, lead management, and data migration</p>
  </div>
  
  <div class="domain-card">
    <h3><a href="/rag/security/">🔒 Security</a></h3>
    <p>Permission set-driven security, field-level security, sharing patterns, and Salesforce-to-LLM data governance</p>
  </div>
  
  <div class="domain-card">
    <h3><a href="/rag/testing/">✅ Testing</a></h3>
    <p>Apex testing patterns, test data factories, automated testing, Jest testing, and non-functional requirements</p>
  </div>
  
  <div class="domain-card">
    <h3><a href="/rag/operations/">🚀 Operations</a></h3>
    <p>CI/CD patterns, environment strategy, release governance, monitoring, performance tuning, and high availability</p>
  </div>
  
  <div class="domain-card">
    <h3><a href="/rag/code-examples/">📝 Code Examples</a></h3>
    <p>Complete, working code examples for Apex, LWC, Flow, integrations, utilities, and templates - all copy-paste ready</p>
  </div>
  
  <div class="domain-card">
    <h3><a href="/rag/troubleshooting/">🔧 Troubleshooting</a></h3>
    <p>Integration debugging, data reconciliation, common Apex/LWC errors, governor limit errors, and root cause analysis</p>
  </div>
  
  <div class="domain-card">
    <h3><a href="/rag/quick-start/">⚡ Quick Start</a></h3>
    <p>Step-by-step guides for getting started with Apex, LWC, and other Salesforce technologies</p>
  </div>
  
  <div class="domain-card">
    <h3><a href="/rag/api-reference/">📚 API Reference</a></h3>
    <p>Quick reference for common APIs, methods, and patterns (Apex, LWC, LDS, SOQL, Platform Events)</p>
  </div>
  
  <div class="domain-card">
    <h3><a href="/rag/glossary/">📖 Glossary</a></h3>
    <p>Core terminology and definitions for integration, identity, data modeling, security, platform, and development terms</p>
  </div>
</div>

## Core Domains

### Architecture & Design
- **Architecture Patterns**: Event-driven architecture with Platform Events, Experience Cloud portal architecture for multiple user communities, multi-tenant solutions, and system design patterns
- **Integration Patterns**: ETL vs. API vs. Events decision frameworks, integration platforms (MuleSoft, Dell Boomi), Student Information System (SIS) synchronization, Change Data Capture (CDC), and Salesforce-to-LLM data pipelines
- **Identity & SSO**: Multi-tenant identity architecture supporting multiple user communities, multiple identity providers (OIDC, SAML, organization tenant), login handlers, and identity-aware routing

### Data & Security
- **Data Modeling**: External IDs and integration keys, student lifecycle models (Education Cloud/EDA), case management models, lead management and conversion, object setup and configuration, file management patterns, and data migration strategies
- **Security**: Permission set-driven security architecture, field-level security, Salesforce-to-LLM data governance, access control patterns, and security best practices
- **Data Governance**: Data residency and compliance (PII/PHI handling, GDPR/CCPA/SOC2 controls, field-level encryption, Shield best practices), data quality and stewardship (duplicate prevention beyond leads, survivorship rules, master data governance)

### Development & Quality
- **Development**: Apex patterns (Service, Domain, Selector, Integration layers), Flow design and orchestration, Lightning Web Components (LWC), OmniStudio patterns, error handling and logging frameworks, order of execution, locking and concurrency, governor limits and optimization, SOQL query patterns, asynchronous Apex (Batch, Queueable, Scheduled), and Custom Settings/Metadata patterns
- **Testing**: Apex testing patterns, test data factories, automated testing at scale (UI automation, contract tests, load testing), non-functional requirements (security testing, accessibility, performance benchmarks), and comprehensive testing strategies

### Operations & Observability
- **Operations**: CI/CD patterns (metadata vs. source-tracked orgs, unlocked packages, sandbox seeding, deployment validation, rollback strategies), environment strategy (org topologies for multi-team programs, data masking, refresh cadences), and release governance (Change Advisory Boards, approval workflows, risk-based checklists)
- **Observability**: Monitoring and alerting (Platform Events monitoring, API health, async job failures, log aggregation), performance tuning (query/selectivity optimization, Large Data Volume handling, governor limit mitigation, caching strategies), and high availability & disaster recovery (backup/restore, failover patterns, business continuity drills)

### Adoption & Project Methods
- **Adoption**: User readiness (training plans, support models, feature adoption telemetry), org health checks (technical debt triage, baseline audits, remediation playbooks), and change management patterns
- **Project Methods**: Sprint-based delivery frameworks, comprehensive testing strategies, deployment patterns, and Salesforce DX (SFDX) patterns

## Content Characteristics

All content in this library:

- ✅ **Evidence-Based**: Derived from real implementation experience
- ✅ **Sanitized**: All identifying information removed (company names, client names, project codenames)
- ✅ **Pattern-Focused**: Emphasizes reusable patterns and best practices
- ✅ **Decision-Oriented**: Includes architectural decisions and tradeoffs
- ✅ **Implementation-Ready**: Provides actionable guidance for implementation

## Getting Started

### For Humans

1. **Browse the index**: Start with [rag/rag-index.md](/rag/rag-index.md) to find relevant knowledge files
2. **Read domain overviews**: Each domain section in the index provides a brief overview
3. **Find specific topics**: Use the "When to Retrieve" guidance to locate relevant files
4. **Read the files**: Each markdown file contains detailed patterns and best practices

### For AI Systems / RAG Tools

1. **Use the JSON metadata**: [rag/rag-library.json](/rag/rag-library.json) contains structured metadata for each knowledge file
2. **Query by domain**: Filter files by `domain` field (architecture, integrations, development, etc.)
3. **Match questions to files**: Use `whenToRetrieve` arrays to find relevant files for a given question
4. **Retrieve summaries**: Use `summary` and `keyTopics` fields for quick context

## Usage Examples

See the [examples/](/examples/) directory for detailed usage examples:

- **[Cursor IDE Usage](/examples/cursor-usage.md)**: Step-by-step guide for using this library with Cursor's RAG features, including prompt patterns and workflows
- **[Generic RAG Integration](/examples/generic-rag-usage.md)**: Integration examples for LangChain, LlamaIndex, and other RAG frameworks with complete code samples

## Key Files

- **[rag/rag-index.md](/rag/rag-index.md)**: Human-readable index with domain overviews and file descriptions
- **[rag/rag-library.json](/rag/rag-library.json)**: Machine-readable metadata with structured information for each knowledge file
- **[examples/](/examples/)**: Usage examples for different RAG frameworks and tools

## Contributing

This library is derived from immutable source documents and implementation experience. Content is organized by domain and follows consistent patterns:

1. Each knowledge file focuses on a specific topic or pattern
2. Files include practical examples and implementation guidance
3. All identifying information is removed (anonymized)
4. Patterns are reusable and applicable across different implementations

---

<div class="footer-note">
  <p><strong>Last Updated:</strong> {{ site.time | date: "%B %Y" }}</p>
  <p>This knowledge library is continuously updated with new patterns and best practices from real Salesforce implementations.</p>
</div>

<style>
.intro {
  margin: 2rem 0;
  padding: 1.5rem;
  background: #f8f9fa;
  border-left: 4px solid #0176d3;
  border-radius: 4px;
}

.lead {
  font-size: 1.1rem;
  line-height: 1.6;
  color: #333;
  margin: 0;
}

.domain-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 1.5rem;
  margin: 2rem 0;
}

.domain-card {
  padding: 1.5rem;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  background: #fff;
  transition: transform 0.2s, box-shadow 0.2s;
}

.domain-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}

.domain-card h3 {
  margin-top: 0;
  margin-bottom: 0.75rem;
}

.domain-card h3 a {
  color: #0176d3;
  text-decoration: none;
}

.domain-card h3 a:hover {
  text-decoration: underline;
}

.domain-card p {
  margin: 0;
  color: #666;
  line-height: 1.5;
}

.footer-note {
  margin-top: 3rem;
  padding: 1.5rem;
  background: #f8f9fa;
  border-radius: 4px;
  font-size: 0.9rem;
  color: #666;
}

@media (max-width: 768px) {
  .domain-grid {
    grid-template-columns: 1fr;
  }
}
</style>

