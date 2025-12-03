# Code Examples Index

Complete, working code examples organized by category. All examples are copy-paste ready and follow Salesforce best practices.

## Overview

This directory contains standalone code examples that complement the pattern documentation in `rag/development/`, `rag/integrations/`, etc. Each example includes:

- Complete, working code
- Context (when to use, what problem it solves)
- Explanation (why this approach works)
- Test examples
- Variations (different ways to implement)

## Apex Examples

### Service Layer
- <a href="{{ '/rag/code-examples/code-examples/apex/service-layer-examples.html' | relative_url }}">Service Layer Examples</a> - Service class implementations with domain and selector delegation

### Domain Layer
- <a href="{{ '/rag/code-examples/code-examples/apex/domain-layer-examples.html' | relative_url }}">Domain Layer Examples</a> - Object-specific business logic and validation

### Selector Layer
- <a href="{{ '/rag/code-examples/code-examples/apex/selector-layer-examples.html' | relative_url }}">Selector Layer Examples</a> - SOQL queries and data access patterns

### Integration Layer
- <a href="{{ '/rag/code-examples/code-examples/apex/integration-examples.html' | relative_url }}">Integration Examples</a> - External API callouts and transformations

### Triggers
- <a href="{{ '/rag/code-examples/code-examples/apex/trigger-examples.html' | relative_url }}">Trigger Examples</a> - Trigger handler patterns with bulkification

### Asynchronous Processing
- <a href="{{ '/rag/code-examples/code-examples/apex/batch-examples.html' | relative_url }}">Batch Examples</a> - Batch Apex implementations: stateless, stateful, chaining, error handling, monitoring
- <a href="{{ '/rag/code-examples/code-examples/apex/queueable-examples.html' | relative_url }}">Queueable Examples</a> - Queueable patterns: basic, chaining, callouts, retry logic, monitoring
- <a href="{{ '/rag/code-examples/code-examples/apex/scheduled-examples.html' | relative_url }}">Scheduled Examples</a> - Scheduled Apex patterns: cron expressions, scheduled batch jobs, error handling, monitoring

### Testing
- <a href="{{ '/rag/code-examples/code-examples/apex/test-examples.html' | relative_url }}">Test Examples</a> - Test class patterns, factories, and mocking

## LWC Examples

### Components
- <a href="{{ '/rag/code-examples/code-examples/lwc/component-examples.html' | relative_url }}">Component Examples</a> - Lightning Web Component implementations

### Services
- <a href="{{ '/rag/code-examples/code-examples/lwc/service-examples.html' | relative_url }}">Service Examples</a> - LWC service layer patterns

### Wire and Data
- <a href="{{ '/rag/code-examples/code-examples/lwc/wire-examples.html' | relative_url }}">Wire Examples</a> - Wire service and imperative call patterns

### Accessibility
- <a href="{{ '/rag/code-examples/code-examples/lwc/accessibility-examples.html' | relative_url }}">Accessibility Examples</a> - Complete accessibility code examples: forms, keyboard navigation, ARIA, images, semantic HTML, dynamic content, color/contrast

### Testing
- <a href="{{ '/rag/code-examples/code-examples/lwc/test-examples.html' | relative_url }}">Test Examples</a> - Jest test examples for LWC

## Flow Examples

### Record-Triggered
- <a href="{{ '/rag/code-examples/code-examples/flow/record-triggered-examples.html' | relative_url }}">Record-Triggered Examples</a> - Before-save and after-save flow patterns

### Screen Flows
- <a href="{{ '/rag/code-examples/code-examples/flow/screen-flow-examples.html' | relative_url }}">Screen Flow Examples</a> - User interaction flow patterns

### Subflows
- <a href="{{ '/rag/code-examples/code-examples/flow/subflow-examples.html' | relative_url }}">Subflow Examples</a> - Reusable subflow patterns

## Integration Examples

### REST API
- <a href="{{ '/rag/code-examples/code-examples/integrations/rest-api-examples.html' | relative_url }}">REST API Examples</a> - Outbound and inbound REST API patterns

### Platform Events
- <a href="{{ '/rag/code-examples/code-examples/integrations/platform-events-examples.html' | relative_url }}">Platform Events Examples</a> - Event publishing and subscription patterns

### Callouts
- <a href="{{ '/rag/code-examples/code-examples/integrations/callout-examples.html' | relative_url }}">Callout Examples</a> - HTTP callout patterns with error handling

### Bulk API
- <a href="{{ '/rag/code-examples/code-examples/integrations/bulk-api-examples.html' | relative_url }}">Bulk API Examples</a> - Bulk data operations

## Utility Examples

### Logging
- <a href="{{ '/rag/code-examples/code-examples/utilities/logging-examples.html' | relative_url }}">Logging Examples</a> - Structured logging patterns

### Error Handling
- <a href="{{ '/rag/code-examples/code-examples/utilities/error-handling-examples.html' | relative_url }}">Error Handling Examples</a> - Error handling and retry patterns

### Validation
- <a href="{{ '/rag/code-examples/code-examples/utilities/validation-examples.html' | relative_url }}">Validation Examples</a> - Data validation patterns

## Templates

### Apex Templates
- <a href="{{ '/rag/code-examples/code-examples/templates/apex-service-template.html' | relative_url }}">Service Template</a> - Service class template
- <a href="{{ '/rag/code-examples/code-examples/templates/apex-domain-template.html' | relative_url }}">Domain Template</a> - Domain class template
- <a href="{{ '/rag/code-examples/code-examples/templates/apex-selector-template.html' | relative_url }}">Selector Template</a> - Selector class template
- <a href="{{ '/rag/code-examples/code-examples/templates/apex-trigger-template.html' | relative_url }}">Trigger Template</a> - Trigger handler template
- <a href="{{ '/rag/code-examples/code-examples/templates/apex-batch-template.html' | relative_url }}">Batch Template</a> - Batch Apex template
- <a href="{{ '/rag/code-examples/code-examples/templates/apex-queueable-template.html' | relative_url }}">Queueable Template</a> - Queueable Apex template
- <a href="{{ '/rag/code-examples/code-examples/templates/apex-scheduled-template.html' | relative_url }}">Scheduled Template</a> - Scheduled Apex template
- <a href="{{ '/rag/code-examples/code-examples/templates/test-class-template.html' | relative_url }}">Test Class Template</a> - Test class template

### LWC Templates
- <a href="{{ '/rag/code-examples/code-examples/templates/lwc-accessible-component-template.html' | relative_url }}">Accessible Component Template</a> - Accessible LWC component template with all accessibility best practices

### Deployment Templates
- <a href="{{ '/rag/code-examples/code-examples/templates/sfdx-project-template.html' | relative_url }}">SFDX Project Template</a> - SFDX project setup template
- <a href="{{ '/rag/code-examples/code-examples/templates/ci-cd-template.html' | relative_url }}">CI/CD Template</a> - CI/CD pipeline template

## How to Use

1. **Find a pattern** in `rag/development/` or `rag/integrations/`
2. **See code examples** linked from pattern files
3. **Browse standalone examples** in this directory
4. **Copy and adapt** code examples for your use case
5. **Use templates** as starting points for new components

## Related Documentation

- <a href="{{ '/rag/code-examples/rag-index.html' | relative_url }}">RAG Index</a> - Complete RAG library index
- <a href="{{ '/rag/code-examples/development/apex-patterns.html' | relative_url }}">Apex Patterns</a> - Apex design patterns
- <a href="{{ '/rag/code-examples/development/lwc-patterns.html' | relative_url }}">LWC Patterns</a> - Lightning Web Component patterns
- <a href="{{ '/rag/code-examples/development/flow-patterns.html' | relative_url }}">Flow Patterns</a> - Flow design patterns
- [Integration Patterns](../integrations/) - Integration patterns

