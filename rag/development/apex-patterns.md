---
layout: default
title: Apex Design Patterns and Best Practices
description: Apex is used strategically when Flows are insufficient or need optimization/bulkification
permalink: /rag/development/apex-patterns.html
---
- <a href="{{ '/rag/testing/apex-testing-patterns.html' | relative_url }}">Testing Patterns</a> - Apex testing best practices
- <a href="{{ '/rag/code-examples/apex/' | relative_url }}">Code Examples</a> - Complete working code examples

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
