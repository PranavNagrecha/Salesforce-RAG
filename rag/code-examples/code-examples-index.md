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
- [Service Layer Examples](code-examples/apex/service-layer-examples.html) - Service class implementations with domain and selector delegation

### Domain Layer
- [Domain Layer Examples](code-examples/apex/domain-layer-examples.html) - Object-specific business logic and validation

### Selector Layer
- [Selector Layer Examples](code-examples/apex/selector-layer-examples.html) - SOQL queries and data access patterns

### Integration Layer
- [Integration Examples](code-examples/apex/integration-examples.html) - External API callouts and transformations

### Triggers
- [Trigger Examples](code-examples/apex/trigger-examples.html) - Trigger handler patterns with bulkification

### Asynchronous Processing
- [Batch Examples](code-examples/apex/batch-examples.html) - Batch Apex implementations: stateless, stateful, chaining, error handling, monitoring
- [Queueable Examples](code-examples/apex/queueable-examples.html) - Queueable patterns: basic, chaining, callouts, retry logic, monitoring
- [Scheduled Examples](code-examples/apex/scheduled-examples.html) - Scheduled Apex patterns: cron expressions, scheduled batch jobs, error handling, monitoring

### Testing
- [Test Examples](code-examples/apex/test-examples.html) - Test class patterns, factories, and mocking

## LWC Examples

### Components
- [Component Examples](code-examples/lwc/component-examples.html) - Lightning Web Component implementations

### Services
- [Service Examples](code-examples/lwc/service-examples.html) - LWC service layer patterns

### Wire and Data
- [Wire Examples](code-examples/lwc/wire-examples.html) - Wire service and imperative call patterns

### Accessibility
- [Accessibility Examples](code-examples/lwc/accessibility-examples.html) - Complete accessibility code examples: forms, keyboard navigation, ARIA, images, semantic HTML, dynamic content, color/contrast

### Testing
- [Test Examples](code-examples/lwc/test-examples.html) - Jest test examples for LWC

## Flow Examples

### Record-Triggered
- [Record-Triggered Examples](code-examples/flow/record-triggered-examples.html) - Before-save and after-save flow patterns

### Screen Flows
- [Screen Flow Examples](code-examples/flow/screen-flow-examples.html) - User interaction flow patterns

### Subflows
- [Subflow Examples](code-examples/flow/subflow-examples.html) - Reusable subflow patterns

## Integration Examples

### REST API
- [REST API Examples](code-examples/integrations/rest-api-examples.html) - Outbound and inbound REST API patterns

### Platform Events
- [Platform Events Examples](code-examples/integrations/platform-events-examples.html) - Event publishing and subscription patterns

### Callouts
- [Callout Examples](code-examples/integrations/callout-examples.html) - HTTP callout patterns with error handling

### Bulk API
- [Bulk API Examples](code-examples/integrations/bulk-api-examples.html) - Bulk data operations

## Utility Examples

### Logging
- [Logging Examples](code-examples/utilities/logging-examples.html) - Structured logging patterns

### Error Handling
- [Error Handling Examples](code-examples/utilities/error-handling-examples.html) - Error handling and retry patterns

### Validation
- [Validation Examples](code-examples/utilities/validation-examples.html) - Data validation patterns

## Templates

### Apex Templates
- [Service Template](code-examples/templates/apex-service-template.html) - Service class template
- [Domain Template](code-examples/templates/apex-domain-template.html) - Domain class template
- [Selector Template](code-examples/templates/apex-selector-template.html) - Selector class template
- [Trigger Template](code-examples/templates/apex-trigger-template.html) - Trigger handler template
- [Batch Template](code-examples/templates/apex-batch-template.html) - Batch Apex template
- [Queueable Template](code-examples/templates/apex-queueable-template.html) - Queueable Apex template
- [Scheduled Template](code-examples/templates/apex-scheduled-template.html) - Scheduled Apex template
- [Test Class Template](code-examples/templates/test-class-template.html) - Test class template

### LWC Templates
- [Accessible Component Template](code-examples/templates/lwc-accessible-component-template.html) - Accessible LWC component template with all accessibility best practices

### Deployment Templates
- [SFDX Project Template](code-examples/templates/sfdx-project-template.html) - SFDX project setup template
- [CI/CD Template](code-examples/templates/ci-cd-template.html) - CI/CD pipeline template

## How to Use

1. **Find a pattern** in `rag/development/` or `rag/integrations/`
2. **See code examples** linked from pattern files
3. **Browse standalone examples** in this directory
4. **Copy and adapt** code examples for your use case
5. **Use templates** as starting points for new components

## Related Documentation

- [RAG Index](rag-index.html) - Complete RAG library index
- [Apex Patterns](development/apex-patterns.html) - Apex design patterns
- [LWC Patterns](development/lwc-patterns.html) - Lightning Web Component patterns
- [Flow Patterns](development/flow-patterns.html) - Flow design patterns
- [Integration Patterns](../integrations/) - Integration patterns

