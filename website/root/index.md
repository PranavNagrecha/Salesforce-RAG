---
layout: default
title: Salesforce RAG Knowledge Library
description: A comprehensive knowledge library containing implementation patterns, best practices, and architectural guidance derived from real Salesforce implementation experience. Organized for efficient retrieval by AI systems and human developers.
permalink: /
---

# Salesforce RAG Knowledge Library

<div class="intro">
  <p class="lead">A comprehensive knowledge library of Salesforce implementation patterns, best practices, and architectural guidance. All content derived from real implementation experience.</p>
</div>

## Browse by Category

<div class="domain-grid">
  <div class="domain-card">
    <h3><a href="{{ '/rag/rag-index.html' | relative_url }}#architecture-patterns">🏗️ Architecture Patterns</a></h3>
    <p>Event-driven architecture, portal architecture, multi-tenant solutions, and system design patterns</p>
  </div>
  
  <div class="domain-card">
    <h3><a href="{{ '/rag/rag-index.html' | relative_url }}#integration-patterns">🔌 Integration Patterns</a></h3>
    <p>ETL vs. API vs. Events decision frameworks, MuleSoft, Dell Boomi, SIS synchronization, CDC, and Salesforce-to-LLM pipelines</p>
  </div>
  
  <div class="domain-card">
    <h3><a href="{{ '/rag/rag-index.html' | relative_url }}#development">💻 Development</a></h3>
    <p>Apex patterns, Flow design, Lightning Web Components (LWC), OmniStudio, error handling, and performance optimization</p>
  </div>
  
  <div class="domain-card">
    <h3><a href="{{ '/rag/rag-index.html' | relative_url }}#data-modeling">📊 Data Modeling</a></h3>
    <p>External IDs, integration keys, student lifecycle models, case management, lead management, and data migration</p>
  </div>
  
  <div class="domain-card">
    <h3><a href="{{ '/rag/rag-index.html' | relative_url }}#security">🔒 Security</a></h3>
    <p>Permission set-driven security, field-level security, sharing patterns, and Salesforce-to-LLM data governance</p>
  </div>
  
  <div class="domain-card">
    <h3><a href="{{ '/rag/rag-index.html' | relative_url }}#testing">✅ Testing</a></h3>
    <p>Apex testing patterns, test data factories, automated testing, Jest testing, and non-functional requirements</p>
  </div>
  
  <div class="domain-card">
    <h3><a href="{{ '/rag/rag-index.html' | relative_url }}#operations">🚀 Operations</a></h3>
    <p>CI/CD patterns, environment strategy, release governance, monitoring, performance tuning, and high availability</p>
  </div>
  
  <div class="domain-card">
    <h3><a href="{{ '/rag/rag-index.html' | relative_url }}#code-examples">📝 Code Examples</a></h3>
    <p>Complete, working code examples for Apex, LWC, Flow, integrations, utilities, and templates - all copy-paste ready</p>
  </div>
  
  <div class="domain-card">
    <h3><a href="{{ '/rag/rag-index.html' | relative_url }}#troubleshooting">🔧 Troubleshooting</a></h3>
    <p>Integration debugging, data reconciliation, common Apex/LWC errors, governor limit errors, and root cause analysis</p>
  </div>
  
  <div class="domain-card">
    <h3><a href="{{ '/rag/rag-index.html' | relative_url }}#quick-start-guides">⚡ Quick Start</a></h3>
    <p>Step-by-step guides for getting started with Apex, LWC, and other Salesforce technologies</p>
  </div>
  
  <div class="domain-card">
    <h3><a href="{{ '/rag/rag-index.html' | relative_url }}#api-reference">📚 API Reference</a></h3>
    <p>Quick reference for common APIs, methods, and patterns (Apex, LWC, LDS, SOQL, Platform Events)</p>
  </div>
  
  <div class="domain-card">
    <h3><a href="{{ '/rag/rag-index.html' | relative_url }}#glossary">📖 Glossary</a></h3>
    <p>Core terminology and definitions for integration, identity, data modeling, security, platform, and development terms</p>
  </div>
</div>

## Quick Links

- 📖 **[Complete Index]({{ '/rag/rag-index.html' | relative_url }})** - Browse all knowledge files by domain
- 📋 **[JSON Metadata]({{ '/rag/rag-library.json' | relative_url }})** - Machine-readable metadata for RAG systems
- 💡 **[Usage Examples]({{ '/examples/' | relative_url }})** - Integration guides for Cursor, LangChain, and more
- 🔍 **[Search the Knowledge Base]({{ '/rag/rag-index.html' | relative_url }})** - Find specific patterns and best practices

## About This Library

This knowledge library contains **140+ files** covering:

- ✅ **Implementation patterns** from real Salesforce projects
- ✅ **Best practices** for development, architecture, and operations  
- ✅ **Code examples** ready to copy and use
- ✅ **Decision frameworks** for common scenarios
- ✅ **Troubleshooting guides** for common issues

All content is **sanitized** (no identifying information) and **pattern-focused** for reuse across implementations.

---

<div class="footer-note">
  <p><strong>Last Updated:</strong> {{ site.time | date: "%B %Y" }}</p>
  <p>This knowledge library is continuously updated with new patterns and best practices from real Salesforce implementations.</p>
</div>

<style>
.intro {
  margin: 1rem 0 2rem 0;
  padding: 1rem 1.5rem;
  background: #f8f9fa;
  border-left: 4px solid #0176d3;
  border-radius: 4px;
}

.lead {
  font-size: 1rem;
  line-height: 1.6;
  color: #333;
  margin: 0;
}

.domain-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 1.25rem;
  margin: 1.5rem 0 3rem 0;
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

