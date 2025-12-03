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
- [Service Layer Examples](/rag/code-examples/apex/service-layer-examples.html) - Service class implementations with domain and selector delegation

### Domain Layer
- [Domain Layer Examples](/rag/code-examples/apex/domain-layer-examples.html) - Object-specific business logic and validation

### Selector Layer
- [Selector Layer Examples](/rag/code-examples/apex/selector-layer-examples.html) - SOQL queries and data access patterns

### Integration Layer
- [Integration Examples](/rag/code-examples/apex/integration-examples.html) - External API callouts and transformations

### Triggers
- [Trigger Examples](/rag/code-examples/apex/trigger-examples.html) - Trigger handler patterns with bulkification

### Asynchronous Processing
- [Batch Examples](/rag/code-examples/apex/batch-examples.html) - Batch Apex implementations: stateless, stateful, chaining, error handling, monitoring
- [Queueable Examples](/rag/code-examples/apex/queueable-examples.html) - Queueable patterns: basic, chaining, callouts, retry logic, monitoring
- [Scheduled Examples](/rag/code-examples/apex/scheduled-examples.html) - Scheduled Apex patterns: cron expressions, scheduled batch jobs, error handling, monitoring

### Testing
- [Test Examples](/rag/code-examples/apex/test-examples.html) - Test class patterns, factories, and mocking

## LWC Examples

### Components
- [Component Examples](/rag/code-examples/lwc/component-examples.html) - Lightning Web Component implementations

### Services
- [Service Examples](/rag/code-examples/lwc/service-examples.html) - LWC service layer patterns

### Wire and Data
- [Wire Examples](/rag/code-examples/lwc/wire-examples.html) - Wire service and imperative call patterns

### Accessibility
- [Accessibility Examples](/rag/code-examples/lwc/accessibility-examples.html) - Complete accessibility code examples: forms, keyboard navigation, ARIA, images, semantic HTML, dynamic content, color/contrast

### Testing
- [Test Examples](/rag/code-examples/lwc/test-examples.html) - Jest test examples for LWC

## Flow Examples

### Record-Triggered
- [Record-Triggered Examples](/rag/code-examples/flow/record-triggered-examples.html) - Before-save and after-save flow patterns

### Screen Flows
- [Screen Flow Examples](/rag/code-examples/flow/screen-flow-examples.html) - User interaction flow patterns

### Subflows
- [Subflow Examples](/rag/code-examples/flow/subflow-examples.html) - Reusable subflow patterns

## Integration Examples

### REST API
- [REST API Examples](/rag/code-examples/integrations/rest-api-examples.html) - Outbound and inbound REST API patterns

### Platform Events
- [Platform Events Examples](/rag/code-examples/integrations/platform-events-examples.html) - Event publishing and subscription patterns

### Callouts
- [Callout Examples](/rag/code-examples/integrations/callout-examples.html) - HTTP callout patterns with error handling

### Bulk API
- [Bulk API Examples](/rag/code-examples/integrations/bulk-api-examples.html) - Bulk data operations

## Utility Examples

### Logging
- [Logging Examples](/rag/code-examples/utilities/logging-examples.html) - Structured logging patterns

### Error Handling
- [Error Handling Examples](/rag/code-examples/utilities/error-handling-examples.html) - Error handling and retry patterns

### Validation
- [Validation Examples](/rag/code-examples/utilities/validation-examples.html) - Data validation patterns

## Templates

### Apex Templates
- [Service Template](/rag/code-examples/templates/apex-service-template.html) - Service class template
- [Domain Template](/rag/code-examples/templates/apex-domain-template.html) - Domain class template
- [Selector Template](/rag/code-examples/templates/apex-selector-template.html) - Selector class template
- [Trigger Template](/rag/code-examples/templates/apex-trigger-template.html) - Trigger handler template
- [Batch Template](/rag/code-examples/templates/apex-batch-template.html) - Batch Apex template
- [Queueable Template](/rag/code-examples/templates/apex-queueable-template.html) - Queueable Apex template
- [Scheduled Template](/rag/code-examples/templates/apex-scheduled-template.html) - Scheduled Apex template
- [Test Class Template](/rag/code-examples/templates/test-class-template.html) - Test class template

### LWC Templates
- [Accessible Component Template](/rag/code-examples/templates/lwc-accessible-component-template.html) - Accessible LWC component template with all accessibility best practices

### Deployment Templates
- [SFDX Project Template](/rag/code-examples/templates/sfdx-project-template.html) - SFDX project setup template
- [CI/CD Template](/rag/code-examples/templates/ci-cd-template.html) - CI/CD pipeline template

## How to Use

1. **Find a pattern** in `rag/development/` or `rag/integrations/`
2. **See code examples** linked from pattern files
3. **Browse standalone examples** in this directory
4. **Copy and adapt** code examples for your use case
5. **Use templates** as starting points for new components

## Related Documentation

- [RAG Index](/rag/rag-index.html) - Complete RAG library index
- [Apex Patterns](/rag/development/apex-patterns.html) - Apex design patterns
- [LWC Patterns](/rag/development/lwc-patterns.html) - Lightning Web Component patterns
- [Flow Patterns](/rag/development/flow-patterns.html) - Flow design patterns
- [Integration Patterns](../integrations/) - Integration patterns

