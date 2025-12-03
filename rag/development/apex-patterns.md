---
title: "Apex Design Patterns and Best Practices"
level: "Intermediate"
tags:
  - apex
  - development
  - patterns
  - service-layer
  - domain-layer
  - selector-layer
last_reviewed: "2025-01-XX"
---

# Apex Design Patterns and Best Practices

## Overview

Apex is used strategically when Flows are insufficient or need optimization/bulkification. The approach emphasizes proper layering, bulkification, comprehensive testing, and integration with declarative automation.

Apex is Salesforce's proprietary programming language, similar to Java, that enables developers to build custom business logic, integrations, and complex automation. Understanding Apex fundamentals, language features, and design patterns enables developers to build robust, maintainable, and performant solutions.

## Prerequisites

**Required Knowledge**:
- Basic understanding of object-oriented programming concepts
- Familiarity with Salesforce data model (objects, fields, relationships)
- Understanding of Salesforce security model (profiles, permission sets, sharing)
- Knowledge of SOQL (Salesforce Object Query Language)

**Recommended Reading**:
- <a href="{{ '/rag/development/flow-patterns.html' | relative_url }}">Flow Patterns</a> - Understanding when to use Flow vs Apex
- <a href="{{ '/rag/development/soql-query-patterns.html' | relative_url }}">SOQL Query Patterns</a> - SOQL query best practices
- <a href="{{ '/rag/development/governor-limits-and-optimization.html' | relative_url }}">Governor Limits and Optimization</a> - Understanding platform limits
- <a href="{{ '/rag/development/error-handling-and-logging.html' | relative_url }}">Error Handling and Logging</a> - Error handling patterns

## Apex Language Fundamentals

### Data Types and Variables

**Primitive types**:
- Integer, Long, Double, Decimal for numbers
- String for text
- Boolean for true/false
- Date, DateTime, Time for dates and times
- ID for Salesforce record IDs
- Blob for binary data

**Collections**:
- **List**: Ordered collection with index access
- **Set**: Unordered collection of unique values
- **Map**: Key-value pairs for lookup

**Best practice**: Use appropriate data types for variables. Prefer `List<Type>` over `Type[]` for clarity. Use Sets for uniqueness, Maps for key-value lookups.

### Control Structures

**Conditionals**:
- `if-else` for conditional logic
- `switch` for multiple value comparisons
- Ternary operator for simple conditionals

**Loops**:
- `for` loops for iteration with index
- `for-each` loops for collection iteration
- `while` loops for conditional iteration
- `do-while` loops for post-condition iteration

**Best practice**: Use for-each loops for collection iteration. Avoid loops with DML or SOQL inside. Use early returns to reduce nesting.

### Exception Handling

**Try-catch-finally**:
- `try` block for code that may throw exceptions
- `catch` block for exception handling
- `finally` block for cleanup code

**Exception types**:
- Standard exceptions (DmlException, QueryException, etc.)
- Custom exceptions for business logic errors
- Exception messages and stack traces

**Best practice**: Wrap DML operations in try-catch blocks. Use custom exceptions for business logic errors. Log exceptions for troubleshooting. Handle exceptions gracefully.

### Access Modifiers

**Public**: Accessible from any Apex class or external contexts (Flows, LWCs).

**Private**: Accessible only within the same class.

**Global**: Accessible from external systems (web services, managed packages).

**Best practice**: Use `public` for service methods called from Flows or LWCs. Use `private` for internal helper methods. Use `global` only when required (web services, managed packages).

## When to Choose Apex

Apex is selected when:

- **Flows are insufficient** for complex logic or performance requirements
- **Heavy reuse** is needed by LWCs, external APIs, or other Apex
- **Tight control** over performance and governor limits is required
- **Complex branching or algorithms** that are difficult in Flow
- **Integration with external APIs** needing complex authentication and error handling

## Apex Class Layering

Apex classes are structured in layers:

### Service Layer

Business logic and orchestration:

- Coordinates between domain, selector, and integration layers
- Exposes clean method signatures for Flows and LWCs
- Handles business rules and workflow orchestration
- Orchestrates complex workflows (queries → validation → DML → notifications)
- Delegates object-specific logic to Domain layer
- Delegates data access to Selector layer
- Delegates external calls to Integration layer
- Should NOT contain SOQL queries (delegate to Selector)
- Should NOT contain object-specific validation (delegate to Domain)
- Should NOT contain external API callouts (delegate to Integration)
- Example: `ContactRetryUpdateService`, `ContactUpdateService`, `RestIntegrationService`

### Domain Layer

Object-specific logic and validation:

- Object-specific business rules
- Validation logic
- Helper methods for specific objects
- Encapsulates business rules for a specific Salesforce object
- Can be called from triggers OR from Service layer
- Should NOT contain SOQL queries (delegate to Selector layer)
- Should NOT contain external callouts (delegate to Integration layer)
- Use directly in triggers for simple validation; use through Service layer for complex workflows
- Example: Account helper classes, `ContactDomain`, `AccountDomain`

### Selector Layer

SOQL queries and data access:

- Centralized SOQL queries
- Data access abstraction
- Query optimization
- Governor limit awareness
- Provide reusable query methods (e.g., `selectById(Set<Id> ids)`, `selectByExternalId(Set<String> externalIds)`)
- Use specific method names rather than abstract criteria methods
- Enforce security using `WITH SECURITY_ENFORCED` or `WITH USER_MODE` in all queries
- Should NOT contain business logic (delegate to Domain layer)
- Should NOT contain external callouts (delegate to Integration layer)

### Integration Layer

External API callouts and transformations:

- External API integration
- Data transformation
- Authentication handling
- Error handling for external systems
- Use Named Credentials for endpoints (NO hardcoded URLs)
- Centralize error handling and retry logic for external systems
- Should NOT contain business logic (delegate to Service layer)
- Should NOT contain SOQL queries (delegate to Selector layer)
- Example: `RestIntegrationService`

### Utility Classes

Reusable functionality:

- Cross-cutting concerns
- Logging utilities
- Common helper methods
- Example: `LOG_LogMessageUtility`

## SOQL Design in Apex

### Selective WHERE Clauses

- Use indexed fields in WHERE clauses
- Avoid querying ID fields unnecessarily
- Use selective filters to reduce query scope
- Monitor query performance

### Bulkification

- Always process collections, not single records
- Avoid DML and SOQL in loops
- Use bulk DML operations (insert, update, upsert with collections)
- Handle governor limits proactively
- Test with maximum data volumes (200+ records minimum)

### Query Optimization

- Combine queries where possible using relationship syntax
- Use aggregate queries for counts and summaries
- Leverage subqueries for related data
- Avoid unnecessary field queries
- Use `WITH SECURITY_ENFORCED` or `WITH USER_MODE` for security

### Security Enforcement

- ALL SOQL queries MUST use `WITH SECURITY_ENFORCED` or `WITH USER_MODE`
- Respect field-level and object-level security
- Document security decisions when using `without sharing`

## Asynchronous Apex Patterns

For comprehensive asynchronous Apex patterns, see <a href="{{ '/rag/development/asynchronous-apex-patterns.html' | relative_url }}">Asynchronous Apex Patterns</a>.

### Queueable

Use for:

- Chaining jobs
- Callouts after DML
- Lightweight async processing
- Jobs that need to be chained together

**Related**: <a href="{{ '/rag/development/code-examples/apex/queueable-examples.html' | relative_url }}">Queueable Examples</a>, <a href="{{ '/rag/development/code-examples/templates/apex-queueable-template.html' | relative_url }}">Queueable Template</a>

### Batchable

Use for:

- Large data processing
- Scheduled batch jobs
- Processing thousands of records
- Operations that exceed synchronous limits

**Related**: <a href="{{ '/rag/development/code-examples/apex/batch-examples.html' | relative_url }}">Batch Examples</a>, <a href="{{ '/rag/development/code-examples/templates/apex-batch-template.html' | relative_url }}">Batch Template</a>

### Scheduled

Use for:

- Time-based automation
- Periodic maintenance
- Scheduled data processing
- Recurring tasks

**Related**: <a href="{{ '/rag/development/code-examples/apex/scheduled-examples.html' | relative_url }}">Scheduled Examples</a>, <a href="{{ '/rag/development/code-examples/templates/apex-scheduled-template.html' | relative_url }}">Scheduled Template</a>

## Apex + LWC Integration

### @AuraEnabled Methods

- Use for imperative calls from LWCs
- Support both cacheable and non-cacheable methods
- Use `@AuraEnabled(cacheable=true)` for read-only operations
- Provide clean method signatures with DTO-style payloads

### @wire Adapters

- Use for reactive data access
- Support automatic data refresh
- Handle loading and error states
- Abstract SOQL details from components

### Service Layer Pattern

- Apex classes expose clean methods for LWCs
- Methods like `getXXXViewModel(Id recordId)` and `performAction(...)`
- LWCs don't "know" SOQL details; they deal with DTO-style payloads
- Encapsulates business logic and data access

## Error Handling in Apex

### Try-Catch Blocks

- Wrap DML operations in try-catch blocks
- Handle specific exception types when possible
- Provide meaningful error messages
- Log all errors to custom logging object

### Custom Exceptions

- Create custom exceptions for specific scenarios
- Provide context in exception messages
- Support error recovery workflows
- Enable better error handling in calling code

### Error Logging

- ALL exceptions MUST be logged to custom log object using logging utility class
- NO System.debug statements in production code
- Use proper logging instead of System.debug
- Log errors before showing messages to users

### Graceful Degradation

- Handle errors gracefully when possible
- Provide fallback mechanisms
- Support partial success scenarios
- Enable error recovery workflows

## Code Quality Standards

### Documentation

- ALL Apex classes MUST have proper ApexDoc documentation
- Document public methods with purpose, parameters, and return values
- Include file headers specifying purpose and ownership
- Write self-documenting code; avoid relying solely on comments

### Code Cleanliness

- Remove unused code promptly
- Avoid hardcoding IDs; use schema methods or constants
- Replace repeated strings with constants (repeated strings are error-prone and hard to maintain)
- Remove System.debug statements before deployment
- Clean up commented code (commented code creates confusion - remove it or convert to proper documentation)

### Security

- ALL SOQL queries MUST use `WITH SECURITY_ENFORCED` or `WITH USER_MODE`
- Use `without sharing` only when necessary and document why
- Handle field-level security appropriately
- Validate input data before processing

### Performance

- Optimize SOQL queries (combine queries where possible)
- NO SOQL queries in loops
- Use bulk DML operations
- Monitor governor limit usage
- Profile code to identify bottlenecks

## Testing Strategy

### Test Coverage

- Aim for 100% code coverage (minimum 90%)
- Test both positive and negative scenarios
- Test with bulk data (200 records minimum)
- Use `Test.startTest()` and `Test.stopTest()` to reset governor limits

### Test Data

- Use test data factories for consistent test data
- Avoid `@SeeAllData` annotation
- ALL test classes MUST create their own test data
- Create realistic test scenarios

### Test Structure

- Test classes should be private
- Minimize logic within `Test.startTest()` and `Test.stopTest()` blocks
- Include both positive and negative test cases
- Test error handling and edge cases

### Mocking

- Use callout mocks for testing integrations
- Mock external dependencies when possible
- Use dependency injection for testability
- Define interfaces for dependencies (e.g., `IContactSelector`, `IExternalApiService`)
- Inject dependencies through constructors or setter methods
- Provide mock implementations for testing
- Test integration error scenarios

### Test Class Security

- **Test classes should NEVER be accessible to end users**: Test classes should never be included in permission sets or profiles accessible to end users. This is a security risk and can expose test logic to unauthorized users.
- Always review permission sets for test classes during security reviews
- Remove test classes from permission sets if found

## Invocable Methods

### Flow Integration

- Build invocable methods for Flow integration
- Use clean request/response objects
- Handle errors gracefully
- Support both single and bulk operations

### Examples

- `SendSMSMagic` - SMS sending functionality
- `ContactRetryUpdateService` - Contact update with retry logic
- Methods that can be called from Flows and LWCs

## Common Patterns

### Retry Logic

- Implement retry logic for transient failures
- Use exponential backoff
- Configurable retry counts via Custom Metadata
- Handle row locking errors (UNABLE_TO_LOCK_ROW)

### Row Locking Error Handling

- Built `ContactRetryUpdateService` with configurable retry logic
- Exponential backoff for high-concurrency scenarios
- Handles UNABLE_TO_LOCK_ROW errors gracefully
- Supports configurable retry attempts

**Lessons Learned from Real Implementations:**

- **Retry logic must be intelligent**: Only retry errors that are likely to succeed on retry (e.g., row locking errors). Don't retry validation errors - they won't succeed on retry.
- **Always consider governor limits in retry logic**: Check CPU time and other limits before retrying. Fail fast if approaching limits.
- **Document trade-offs and future improvements**: When implementing a solution with known limitations (e.g., busy-wait retry logic), document these in code comments. This helps future developers understand why decisions were made.
- **Consider async alternatives for high-volume scenarios**: Busy-wait retry logic works but isn't ideal for high-volume scenarios. Consider Queueable or Platform Events for async retries.

### Configuration Management

- Use Custom Metadata Types for configuration
- Avoid hardcoded values (IDs, counts, URLs, etc.)
- Support environment-specific configuration
- Enable runtime configuration changes

**Lessons Learned from Real Implementations:**

- **Externalize all configuration**: Never hardcode environment-specific values (URLs, IDs, counts). Use Custom Metadata Types or Custom Settings for configuration that varies by environment. This enables environment-specific configuration without code changes.

**Related**: <a href="{{ '/rag/development/custom-settings-metadata-patterns.html' | relative_url }}">Custom Settings and Custom Metadata Patterns</a>, <a href="{{ '/rag/development/code-examples/utilities/custom-settings-examples.html' | relative_url }}">Custom Settings Examples</a>, <a href="{{ '/rag/development/code-examples/utilities/custom-metadata-examples.html' | relative_url }}">Custom Metadata Examples</a>
- **Use Named Credentials for all external URLs**: All HTTP callouts should use Named Credentials, not hardcoded URLs. This centralizes credential management and enables environment-specific endpoints.
- **Centralize integration patterns**: When multiple classes make HTTP callouts, centralize the pattern in an abstract service class. This makes maintenance and auditing easier.


## Detailed Pattern Implementations

### Pattern 1: Logging Utility with Fallback Mechanism

**When to use**: When you need comprehensive error logging for compliance and troubleshooting, but System.debug isn't sufficient.

**Implementation approach**:
- Create utility class implementing `Callable` interface (enables calling from Flows)
- Implement different log levels (Debug, Info, Error, Warning, Fatal)
- Build methods that accept log level, source, source function, message, payload
- Check log settings (can filter by level)
- Truncate payloads if too large (prevents DML errors)
- Can queue DML requests or execute immediately
- On DML exception, publish Platform Event as fallback

**Why it's recommended**: System.debug statements don't persist and can't be used for production troubleshooting. A logging utility with fallback ensures critical errors are captured even when DML fails. The Callable interface enables use from both Flows and Apex.

**Real example**: `LOG_LogMessageUtility` class built for enterprise-scale public sector portal serving 40,000+ concurrent users. Implemented `Callable` interface, different log levels, truncation for large payloads, and Platform Event fallback when DML fails.

**Lessons learned**:
- Always have a fallback mechanism for critical logging
- Consider storage implications at scale (use log settings to filter)
- Make utilities flexible (queue vs immediate, filtering options)
- Truncation prevents DML errors from large payloads

### Pattern 2: Integration Service with Configuration Management

**When to use**: When you have multiple Apex classes making HTTP callouts with hardcoded URLs and inconsistent error handling patterns.

**Implementation approach**:
- Create abstract class implementing interface
- Use Custom Metadata Type to configure endpoints, methods, headers, timeouts
- Use Named Credentials for URLs (externalized, credentials managed by Salesforce)
- Centralize request generation and execution
- Standardize error handling patterns

**Why it's recommended**: Hardcoded URLs make environment management difficult and create security risks. Centralizing integration patterns makes maintenance and auditing easier. Custom Metadata enables environment-specific configuration without code changes.

**Real example**: `RestIntegrationService` abstract class built to solve problem of multiple Apex classes with hardcoded URLs. Uses Custom Metadata Type (`IEE_MS_Interface_Detail__mdt`) to configure endpoints, methods, headers, timeouts. Named Credentials externalize URLs and credentials.

**Lessons learned**:
- Externalize all configuration - never hardcode environment-specific values
- Use Named Credentials for all external URLs
- Centralize integration patterns - easier to maintain and audit
- Abstract classes enable reuse while allowing specific implementations

### Pattern 3: Retry Logic with Intelligent Error Detection

**When to use**: When operations may encounter transient errors (e.g., row locking errors) that should be retried, but permanent errors (e.g., validation errors) should not be retried.

**Implementation approach**:
- Create service class with `@InvocableMethod` (callable from Flows)
- Implement configurable retry logic (default: 3 retries with exponential backoff)
- Detect retryable errors (check error status code AND error message)
- Only retry on retryable errors (e.g., `UNABLE_TO_LOCK_ROW`), not validation errors
- Check governor limits before retry (fail fast if approaching limits)
- Document trade-offs (e.g., busy-wait limitation, future async improvements)

**Why it's recommended**: Retry logic must be intelligent - only retry errors that are likely to succeed on retry. Retrying validation errors wastes resources and doesn't solve the problem. Governor limit awareness prevents retry logic from causing limit exceptions.

**Real example**: `ContactRetryUpdateService` built to solve row locking errors in high-concurrency scenarios. Implements configurable retry logic with exponential backoff, intelligent error detection (only retries row locking errors), and governor limit awareness.

**Lessons learned**:
- Retry logic must be intelligent (only retry retryable errors)
- Always consider governor limits in retry logic
- Document trade-offs and future improvements in code
- Busy-wait works but isn't ideal for high-volume scenarios (consider async alternatives)

### Pattern 4: Scoring Model with Business Rule Overrides

**When to use**: When implementing automated scoring or decision-making systems where business rules can override model calculations.

**Implementation approach**:
- Check override conditions first (before model calculation)
- If override conditions met, return override result immediately
- If no overrides, perform model calculation
- Return detailed breakdown showing how decision was made
- Provide feedback mechanism for model improvement

**Why it's recommended**: Business rules should always take precedence over model calculations. Checking overrides first prevents unnecessary computation and ensures business rules are respected. Detailed breakdowns build user trust and enable feedback for model improvement.

**Real example**: Fraud score calculation system for application review. Checks override conditions first (Active Duty Military, Nursing Programs, Completed Courses → fraud score = 0). If no overrides, calculates score using logistic regression model with 16 factors. Returns detailed breakdown with field values and scores for display.

**Lessons learned**:
- Business rules (overrides) should be checked before model calculation
- Users need transparency in scoring models
- Feedback mechanisms are valuable for model improvement
- Detailed breakdowns help users understand and trust the system

## Lessons Learned from Real Implementations

### Logging Utilities

- **Always implement fallback mechanisms**: When building logging utilities, always have a fallback (e.g., Platform Events) if primary mechanism fails. This prevents loss of critical information when DML fails due to governor limits or validation rules.
- **Consider storage implications at scale**: At enterprise scale (40K+ concurrent users), logging everything creates massive storage. Use log settings to filter by level.
- **Make utilities flexible**: Support both queue and immediate execution, filtering options, and different log levels.

### Integration Services

- **Externalize all configuration**: Never hardcode environment-specific values. Use Custom Metadata Types for configuration that varies by environment.
- **Use Named Credentials for all external URLs**: Centralizes credential management and enables environment-specific endpoints.
- **Centralize integration patterns**: When multiple classes make HTTP callouts, centralize the pattern in an abstract service class. This makes maintenance and auditing easier.

### Performance Optimization

- **Don't auto-calculate on page load**: For LWC controllers, don't auto-calculate on page load. User must click button. This prevents unnecessary Apex calls and significantly improves page load times.
- **Use cacheable methods with cache busting**: Use `@AuraEnabled(cacheable=true)` for read-only operations, but implement cache busting with random parameter when fresh data is needed.
- **Fetch all required data in single Apex call**: Reduce network latency by fetching all required data in one call rather than multiple separate queries.
- **Use lazy loading for detailed breakdowns**: Hide detailed breakdowns in tabs, only load when user expands. This improves perceived performance.

### Scoring Models and Automated Decisions

- **Check business rules before complex calculations**: When implementing scoring models, check override conditions first (e.g., business rules that override the model). This prevents unnecessary computation.
- **Provide transparency in automated decisions**: When implementing scoring models or automated decision-making, provide detailed breakdowns showing how decisions were made. This builds user trust.
- **Enable feedback mechanisms**: Provide feedback mechanisms for model improvement. Users can provide feedback on scores, which is valuable for model refinement.

## Best Practices Summary

### Code Structure

- Use layered architecture (Service, Domain, Selector, Integration)
- Keep classes focused on single responsibility
- Use dependency injection where appropriate
- Follow naming conventions consistently
- Lower layers should NOT depend on higher layers (prevents circular dependencies)

### Performance

- Always bulkify operations
- Optimize SOQL queries
- Monitor governor limits
- Test with maximum data volumes

### Security

- Enforce security in SOQL queries
- Validate input data
- Handle field-level security
- Document security decisions

### Testing

- Achieve minimum 90% code coverage
- Test with bulk data
- Create test data factories
- Test error scenarios
- Design for testability from the start (use dependency injection patterns, define interfaces for dependencies)

### Integration

- Use invocable methods for Flow integration
- Support both cacheable and non-cacheable methods
- Provide clean method signatures
- Abstract SOQL details from callers

## Tradeoffs and Implementation Decisions

### Synchronous vs Asynchronous Retry Logic

**Tradeoff**: Some patterns retry synchronously in the same transaction (e.g., `ContactRetryUpdateService` with busy-wait), while others defer to Queueable jobs.

**Decision guidance**:
- Use synchronous for quick retries (1-2 attempts) - simpler implementation
- Use asynchronous for longer retries or high-volume scenarios - better resource efficiency
- Consider Queueable or Platform Events for async retries when governor limits are a concern

### Auto-Calculation vs User-Initiated Calculation

**Tradeoff**: Some components auto-calculate on page load for convenience, while others require user action.

**Decision guidance**:
- User-initiated calculation significantly improves page load times and perceived performance
- Auto-calculation creates unnecessary Apex calls when users just view records
- Give users control over when to calculate for expensive operations

### Cacheable Methods with Cache Busting

**Tradeoff**: Some implementations use cacheable methods without cache busting (better performance, but stale data risk), while others use cache busting (fresh data, but more server round trips).

**Decision guidance**:
- Use cacheable methods with cache busting when fresh data is needed
- Accept cached data when acceptable for better performance
- Implement cache busting with random parameter (e.g., `System.currentTimeMillis()`) when fresh data required

### Detailed Breakdowns vs Simple Scores

**Tradeoff**: Some scoring systems return only final scores, while others return detailed breakdowns.

**Decision guidance**:
- Detailed breakdowns build user trust and enable feedback for model improvement
- Transparency in automated decisions helps users understand and trust the system
- Balance complexity with user needs and compliance requirements

## Related Patterns

**See Also**:
- <a href="{{ '/rag/development/flow-patterns.html' | relative_url }}">Flow Patterns</a> - Understanding when to use Flow vs Apex
- <a href="{{ '/rag/development/soql-query-patterns.html' | relative_url }}">SOQL Query Patterns</a> - SOQL query best practices and patterns
- <a href="{{ '/rag/development/asynchronous-apex-patterns.html' | relative_url }}">Asynchronous Apex Patterns</a> - Batch, Queueable, and Scheduled Apex patterns
- <a href="{{ '/rag/development/error-handling-and-logging.html' | relative_url }}">Error Handling and Logging</a> - Comprehensive error handling framework
- <a href="{{ '/rag/development/governor-limits-and-optimization.html' | relative_url }}">Governor Limits and Optimization</a> - Performance optimization and limit management
- <a href="{{ '/rag/development/locking-and-concurrency-strategies.html' | relative_url }}">Locking and Concurrency Strategies</a> - Row locking and retry patterns
- <a href="{{ '/rag/development/custom-settings-metadata-patterns.html' | relative_url }}">Custom Settings and Custom Metadata Patterns</a> - Configuration management patterns
- <a href="{{ '/rag/development/order-of-execution.html' | relative_url }}">Order of Execution</a> - Understanding when Apex executes in the save sequence

**Related Domains**:
- <a href="{{ '/rag/development/lwc-patterns.html' | relative_url }}">LWC Patterns</a> - Integrating Apex with Lightning Web Components
- <a href="{{ '/rag/development/testing/apex-testing-patterns.html' | relative_url }}">Testing Patterns</a> - Apex testing best practices
- [Code Examples](../code-examples/apex/) - Complete working code examples

## Q&A

### Q: When should I use Apex instead of Flow?

**A**: Use Apex when you need complex logic that Flow cannot handle efficiently, require tight control over governor limits, need heavy reuse across multiple contexts (LWCs, external APIs, other Apex), or need to integrate with external APIs requiring complex authentication and error handling. Flow should be the default choice for most automation; Apex is for cases where Flow is insufficient or needs optimization.

### Q: What is the difference between Service, Domain, and Selector layers?

**A**: The Service layer orchestrates workflows and exposes clean method signatures for Flows and LWCs. The Domain layer contains object-specific business logic and validation. The Selector layer provides centralized SOQL queries with security enforcement. Service delegates to Domain for validation and Selector for data access, keeping concerns separated and code maintainable.

### Q: Should I put SOQL queries in Service classes or Selector classes?

**A**: Always put SOQL queries in Selector classes. Service classes should delegate data access to Selector classes. This centralizes queries, enables security enforcement, and makes queries reusable across different service methods.

### Q: How do I handle bulk operations in Apex?

**A**: Always process collections, never single records in loops. Design all methods to accept and process `List<Type>` or `Set<Id>` parameters. Use bulk DML operations (insert, update, upsert with collections). Test with 200+ records to ensure bulkification works correctly.

### Q: When should I use Queueable vs Batch vs Scheduled Apex?

**A**: Use Queueable for asynchronous processing of small to medium datasets (up to 50,000 records), when you need to chain jobs, or need to make callouts. Use Batch for large datasets (50,000+ records) that need to be processed in chunks. Use Scheduled Apex for time-based automation that runs on a schedule.

### Q: How do I test Apex code that makes callouts?

**A**: Use `Test.setMock()` to set mock HTTP callout responses. Create mock response classes that implement `HttpCalloutMock`. This allows you to test callout logic without making actual HTTP requests during tests.

### Q: What is the best way to handle errors in Apex?

**A**: Wrap DML operations in try-catch blocks. Use custom exceptions for business logic errors. Log all errors to a custom logging object (e.g., `LOG_LogMessage__c`) with platform event fallback if DML fails. Include context information (source, function, payload) in error logs for troubleshooting.

### Q: How do I make Apex methods callable from Flow?

**A**: Use `@InvocableMethod` annotation on static methods. Methods must be in a public class. Parameters should be lists (even for single values). Return values should also be lists. Use `@InvocableVariable` for complex input parameters.

### Q: What is the difference between `with sharing` and `without sharing`?

**A**: `with sharing` enforces sharing rules and respects the user's record-level access. `without sharing` ignores sharing rules and can access all records (subject to field-level security). Use `with sharing` by default; use `without sharing` only when you need to bypass sharing for legitimate reasons (e.g., system operations).

### Q: How do I optimize SOQL queries for performance?

**A**: Use selective WHERE clauses with indexed fields (queries returning <10% of records). Use `WITH SECURITY_ENFORCED` to enforce field-level security. Select only fields you need. Use relationship queries to avoid multiple queries. Test query selectivity using Query Plan in Developer Console.
