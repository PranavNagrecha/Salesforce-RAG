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
- [Service Layer Examples](apex/service-layer-examples.md) - Service class implementations with domain and selector delegation

### Domain Layer
- [Domain Layer Examples](apex/domain-layer-examples.md) - Object-specific business logic and validation

### Selector Layer
- [Selector Layer Examples](apex/selector-layer-examples.md) - SOQL queries and data access patterns

### Integration Layer
- [Integration Examples](apex/integration-examples.md) - External API callouts and transformations

### Triggers
- [Trigger Examples](apex/trigger-examples.md) - Trigger handler patterns with bulkification

### Asynchronous Processing
- [Batch Examples](apex/batch-examples.md) - Batch Apex implementations: stateless, stateful, chaining, error handling, monitoring
- [Queueable Examples](apex/queueable-examples.md) - Queueable patterns: basic, chaining, callouts, retry logic, monitoring
- [Scheduled Examples](apex/scheduled-examples.md) - Scheduled Apex patterns: cron expressions, scheduled batch jobs, error handling, monitoring

### Testing
- [Test Examples](apex/test-examples.md) - Test class patterns, factories, and mocking

## LWC Examples

### Components
- [Component Examples](lwc/component-examples.md) - Lightning Web Component implementations

### Services
- [Service Examples](lwc/service-examples.md) - LWC service layer patterns

### Wire and Data
- [Wire Examples](lwc/wire-examples.md) - Wire service and imperative call patterns

### Accessibility
- [Accessibility Examples](lwc/accessibility-examples.md) - Complete accessibility code examples: forms, keyboard navigation, ARIA, images, semantic HTML, dynamic content, color/contrast

### Testing
- [Test Examples](lwc/test-examples.md) - Jest test examples for LWC

## Flow Examples

### Record-Triggered
- [Record-Triggered Examples](flow/record-triggered-examples.md) - Before-save and after-save flow patterns

### Screen Flows
- [Screen Flow Examples](flow/screen-flow-examples.md) - User interaction flow patterns

### Subflows
- [Subflow Examples](flow/subflow-examples.md) - Reusable subflow patterns

## Integration Examples

### REST API
- [REST API Examples](integrations/rest-api-examples.md) - Outbound and inbound REST API patterns

### Platform Events
- [Platform Events Examples](integrations/platform-events-examples.md) - Event publishing and subscription patterns

### Callouts
- [Callout Examples](integrations/callout-examples.md) - HTTP callout patterns with error handling

### Bulk API
- [Bulk API Examples](integrations/bulk-api-examples.md) - Bulk data operations

## Utility Examples

### Logging
- [Logging Examples](utilities/logging-examples.md) - Structured logging patterns

### Error Handling
- [Error Handling Examples](utilities/error-handling-examples.md) - Error handling and retry patterns

### Validation
- [Validation Examples](utilities/validation-examples.md) - Data validation patterns

## Templates

### Apex Templates
- [Service Template](templates/apex-service-template.md) - Service class template
- [Domain Template](templates/apex-domain-template.md) - Domain class template
- [Selector Template](templates/apex-selector-template.md) - Selector class template
- [Trigger Template](templates/apex-trigger-template.md) - Trigger handler template
- [Batch Template](templates/apex-batch-template.md) - Batch Apex template
- [Queueable Template](templates/apex-queueable-template.md) - Queueable Apex template
- [Scheduled Template](templates/apex-scheduled-template.md) - Scheduled Apex template
- [Test Class Template](templates/test-class-template.md) - Test class template

### LWC Templates
- [Accessible Component Template](templates/lwc-accessible-component-template.md) - Accessible LWC component template with all accessibility best practices

### Deployment Templates
- [SFDX Project Template](templates/sfdx-project-template.md) - SFDX project setup template
- [CI/CD Template](templates/ci-cd-template.md) - CI/CD pipeline template

## How to Use

1. **Find a pattern** in `rag/development/` or `rag/integrations/`
2. **See code examples** linked from pattern files
3. **Browse standalone examples** in this directory
4. **Copy and adapt** code examples for your use case
5. **Use templates** as starting points for new components

## Related Documentation

- [RAG Index](../rag-index.md) - Complete RAG library index
- [Apex Patterns](../development/apex-patterns.md) - Apex design patterns
- [LWC Patterns](../development/lwc-patterns.md) - Lightning Web Component patterns
- [Flow Patterns](../development/flow-patterns.md) - Flow design patterns
- [Integration Patterns](../integrations/) - Integration patterns

