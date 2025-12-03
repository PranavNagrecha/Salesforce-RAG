---
layout: default
title: Code Examples Index
description: Complete, working code examples organized by category. All examples are copy-paste ready and follow Salesforce best practices.
permalink: /rag/code-examples/code-examples-index.html
---

# Code Examples Index

Complete, working code examples organized by category. All examples are copy-paste ready and follow Salesforce best practices.

## Overview

This index provides access to all code examples in the repository, organized by domain and type. Each example includes:
- Complete, working code
- Context and use cases
- Explanation of patterns
- Test examples
- Related pattern references

## Apex Examples

Apex code examples demonstrating service layer, domain layer, selector layer, triggers, and asynchronous patterns.

### Service Layer
- <a href="{{ '/rag/code-examples/apex/service-layer-examples.html' | relative_url }}">Service Layer Examples</a> - Service layer pattern implementations with orchestration and delegation

### Domain Layer
- <a href="{{ '/rag/code-examples/apex/domain-layer-examples.html' | relative_url }}">Domain Layer Examples</a> - Domain layer pattern implementations with business logic and validation

### Selector Layer
- <a href="{{ '/rag/code-examples/apex/selector-layer-examples.html' | relative_url }}">Selector Layer Examples</a> - Selector layer pattern implementations with SOQL queries and security enforcement

### Triggers
- <a href="{{ '/rag/code-examples/apex/trigger-examples.html' | relative_url }}">Trigger Examples</a> - Trigger handler patterns with bulkification and error handling

### Asynchronous Patterns
- <a href="{{ '/rag/code-examples/apex/queueable-examples.html' | relative_url }}">Queueable Examples</a> - Queueable Apex implementations for asynchronous processing
- <a href="{{ '/rag/code-examples/apex/batch-examples.html' | relative_url }}">Batch Examples</a> - Batch Apex implementations for large data processing
- <a href="{{ '/rag/code-examples/apex/scheduled-examples.html' | relative_url }}">Scheduled Examples</a> - Scheduled Apex implementations for time-based automation

### Integration Layer
- <a href="{{ '/rag/code-examples/apex/integration-examples.html' | relative_url }}">Integration Examples</a> - Apex integration layer patterns with callouts and error handling

**Related Patterns**:
- <a href="{{ '/rag/development/apex-patterns.html' | relative_url }}">Apex Patterns</a> - Apex design patterns and best practices
- <a href="{{ '/rag/development/asynchronous-apex-patterns.html' | relative_url }}">Asynchronous Apex Patterns</a> - Asynchronous processing patterns

## Lightning Web Component (LWC) Examples

Lightning Web Component examples demonstrating component patterns, wire services, and testing.

### Components
- <a href="{{ '/rag/code-examples/lwc/component-examples.html' | relative_url }}">Component Examples</a> - LWC component implementations with data binding and event handling

### Wire Services
- <a href="{{ '/rag/code-examples/lwc/wire-examples.html' | relative_url }}">Wire Examples</a> - LWC wire service patterns with Lightning Data Service

### Services
- <a href="{{ '/rag/code-examples/lwc/service-examples.html' | relative_url }}">Service Examples</a> - LWC service layer patterns for data access and business logic

### Testing
- <a href="{{ '/rag/code-examples/lwc/test-examples.html' | relative_url }}">Test Examples</a> - Jest test examples for LWC components

### Accessibility
- <a href="{{ '/rag/code-examples/lwc/accessibility-examples.html' | relative_url }}">Accessibility Examples</a> - Accessible LWC component patterns

**Related Patterns**:
- <a href="{{ '/rag/development/lwc-patterns.html' | relative_url }}">LWC Patterns</a> - Lightning Web Component patterns and best practices
- <a href="{{ '/rag/mcp-knowledge/lwc-best-practices.html' | relative_url }}">LWC Best Practices</a> - Official LWC best practices

## Flow Examples

Flow examples demonstrating record-triggered flows, screen flows, and subflows.

### Record-Triggered Flows
- <a href="{{ '/rag/code-examples/flow/record-triggered-examples.html' | relative_url }}">Record-Triggered Flow Examples</a> - Record-triggered flow patterns for automation

### Screen Flows
- <a href="{{ '/rag/code-examples/flow/screen-flow-examples.html' | relative_url }}">Screen Flow Examples</a> - Screen flow patterns for user interactions

### Subflows
- <a href="{{ '/rag/code-examples/flow/subflow-examples.html' | relative_url }}">Subflow Examples</a> - Subflow patterns for reusable automation logic

**Related Patterns**:
- <a href="{{ '/rag/development/flow-patterns.html' | relative_url }}">Flow Patterns</a> - Flow design and orchestration patterns

## Integration Examples

Integration examples demonstrating REST APIs, Platform Events, callouts, CDC, and Bulk API patterns.

### REST API
- <a href="{{ '/rag/code-examples/integrations/rest-api-examples.html' | relative_url }}">REST API Examples</a> - REST API integration patterns with outbound and inbound services

### Platform Events
- <a href="{{ '/rag/code-examples/integrations/platform-events-examples.html' | relative_url }}">Platform Events Examples</a> - Platform Events patterns for event-driven architecture

### Callouts
- <a href="{{ '/rag/code-examples/integrations/callout-examples.html' | relative_url }}">Callout Examples</a> - HTTP callout patterns with error handling and retries

### Change Data Capture (CDC)
- <a href="{{ '/rag/code-examples/integrations/cdc-examples.html' | relative_url }}">CDC Examples</a> - Change Data Capture patterns for real-time data synchronization

### Bulk API
- <a href="{{ '/rag/code-examples/integrations/bulk-api-examples.html' | relative_url }}">Bulk API Examples</a> - Bulk API patterns for large data operations

**Related Patterns**:
- <a href="{{ '/rag/integrations/integration-platform-patterns.html' | relative_url }}">Integration Platform Patterns</a> - Integration platform patterns
- <a href="{{ '/rag/integrations/callout-best-practices.html' | relative_url }}">Callout Best Practices</a> - Callout best practices
- <a href="{{ '/rag/architecture/event-driven-architecture.html' | relative_url }}">Event-Driven Architecture</a> - Event-driven architecture patterns

## Utility Examples

Utility examples demonstrating logging, error handling, validation, custom settings, custom metadata, data migration, metadata API, and SFDX patterns.

### Logging
- <a href="{{ '/rag/code-examples/utilities/logging-examples.html' | relative_url }}">Logging Examples</a> - Logging utility patterns for error tracking and debugging

### Error Handling
- <a href="{{ '/rag/code-examples/utilities/error-handling-examples.html' | relative_url }}">Error Handling Examples</a> - Error handling patterns with custom exceptions and logging

### Validation
- <a href="{{ '/rag/code-examples/utilities/validation-examples.html' | relative_url }}">Validation Examples</a> - Validation utility patterns for data quality

### Custom Settings
- <a href="{{ '/rag/code-examples/utilities/custom-settings-examples.html' | relative_url }}">Custom Settings Examples</a> - Custom Settings patterns for configuration management

### Custom Metadata
- <a href="{{ '/rag/code-examples/utilities/custom-metadata-examples.html' | relative_url }}">Custom Metadata Examples</a> - Custom Metadata patterns for metadata-driven configuration

### Data Migration
- <a href="{{ '/rag/code-examples/utilities/data-migration-examples.html' | relative_url }}">Data Migration Examples</a> - Data migration patterns for bulk data operations

### Metadata API
- <a href="{{ '/rag/code-examples/utilities/metadata-api-examples.html' | relative_url }}">Metadata API Examples</a> - Metadata API patterns for programmatic metadata management

### SFDX
- <a href="{{ '/rag/code-examples/utilities/sfdx-examples.html' | relative_url }}">SFDX Examples</a> - Salesforce CLI (SFDX) patterns for development workflows

**Related Patterns**:
- <a href="{{ '/rag/development/error-handling-and-logging.html' | relative_url }}">Error Handling and Logging</a> - Error handling and logging patterns
- <a href="{{ '/rag/development/custom-settings-metadata-patterns.html' | relative_url }}">Custom Settings and Metadata Patterns</a> - Custom settings and metadata patterns
- <a href="{{ '/rag/project-methods/sfdx-patterns.html' | relative_url }}">SFDX Patterns</a> - Salesforce CLI patterns

## Templates

Code templates for common patterns and structures.

### Apex Templates
- <a href="{{ '/rag/code-examples/templates/apex-service-template.html' | relative_url }}">Service Template</a> - Service layer class template
- <a href="{{ '/rag/code-examples/templates/apex-domain-template.html' | relative_url }}">Domain Template</a> - Domain layer class template
- <a href="{{ '/rag/code-examples/templates/apex-selector-template.html' | relative_url }}">Selector Template</a> - Selector layer class template
- <a href="{{ '/rag/code-examples/templates/apex-trigger-template.html' | relative_url }}">Trigger Template</a> - Trigger handler template
- <a href="{{ '/rag/code-examples/templates/apex-queueable-template.html' | relative_url }}">Queueable Template</a> - Queueable Apex template
- <a href="{{ '/rag/code-examples/templates/apex-batch-template.html' | relative_url }}">Batch Template</a> - Batch Apex template
- <a href="{{ '/rag/code-examples/templates/apex-scheduled-template.html' | relative_url }}">Scheduled Template</a> - Scheduled Apex template

### Testing Templates
- <a href="{{ '/rag/code-examples/templates/test-class-template.html' | relative_url }}">Test Class Template</a> - Apex test class template

### LWC Templates
- <a href="{{ '/rag/code-examples/templates/lwc-accessible-component-template.html' | relative_url }}">Accessible Component Template</a> - Accessible LWC component template

### Project Templates
- <a href="{{ '/rag/code-examples/templates/sfdx-project-template.html' | relative_url }}">SFDX Project Template</a> - Salesforce DX project structure template
- <a href="{{ '/rag/code-examples/templates/ci-cd-template.html' | relative_url }}">CI/CD Template</a> - CI/CD pipeline configuration template

## Usage

### For Developers

1. **Find Examples**: Browse by category to find relevant examples
2. **Copy Code**: All examples are copy-paste ready
3. **Follow Patterns**: Examples demonstrate best practices and patterns
4. **Read Context**: Each example includes use cases and explanations
5. **Run Tests**: Test examples are included for validation

### For RAG Systems

1. **Metadata**: All examples include frontmatter with tags and descriptions
2. **Cross-References**: Examples link to related patterns
3. **Context**: Examples include "when to use" and "what problem it solves"
4. **Complete Code**: Examples are complete and working, not pseudocode

## Related Resources

- <a href="{{ '/rag/rag-index.html' | relative_url }}">RAG Knowledge Library Index</a> - Complete index of all knowledge files
- <a href="{{ '/rag/development/apex-patterns.html' | relative_url }}">Apex Patterns</a> - Apex design patterns
- <a href="{{ '/rag/development/lwc-patterns.html' | relative_url }}">LWC Patterns</a> - Lightning Web Component patterns
- <a href="{{ '/rag/development/flow-patterns.html' | relative_url }}">Flow Patterns</a> - Flow design patterns
- <a href="{{ '/rag/integrations/integration-platform-patterns.html' | relative_url }}">Integration Patterns</a> - Integration platform patterns
