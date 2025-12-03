---
layout: default
title: Cross-Cutting Design Patterns
description: This document summarizes reusable patterns that appear across multiple domains in the architecture
permalink: /rag/patterns/cross-cutting-patterns.html
---
- **Troubleshooting**: See `rag/troubleshooting/integration-debugging.md` for testing-related debugging

### Key Principles

- Test with bulk data (200+ records minimum)
- Include both positive and negative test cases
- Test integration connectivity, transformation, and error handling
- Validate data quality (matching, deduplication, error capture)
- Test user migration and login handlers
- Coordinate testing windows across stakeholders
- Test classes should never be accessible to end users (security risk)
- Design for testability from the start (dependency injection, interfaces)
- Test integration error scenarios (network failures, timeouts, invalid responses)

### Testing Checklist

- [ ] Unit tests with bulk data (200+ records)
- [ ] Integration tests for all integration points
- [ ] Data quality tests for matching and deduplication
- [ ] User migration tests for identity providers
- [ ] Portal functionality tests for all user types
- [ ] Test classes removed from permission sets (security review)
- [ ] Test classes create their own test data (no @SeeAllData)
- [ ] Test both positive and negative scenarios
- [ ] Test integration error scenarios with callout mocks

## Related Patterns

These patterns often work together:

- **External IDs + Bulkification**: External IDs enable efficient bulk upsert operations
- **Error Handling + Logging**: Comprehensive logging supports error investigation
- **Security + Portal Design**: Security patterns enable multi-tenant portal implementations
- **Integration Patterns + Data Quality**: Integration patterns must support data quality requirements
- **Testing + All Patterns**: Testing validates that all patterns work correctly together

## Q&A

### Q: What are cross-cutting patterns in Salesforce?

**A**: **Cross-cutting patterns** are reusable patterns that appear across multiple domains in the architecture. They include: (1) **Governor limit management** (handling platform limits), (2) **Bulkification** (processing records in bulk), (3) **External IDs** (stable record mapping), (4) **Error handling** (consistent error management), (5) **Security patterns** (access control, sharing). These patterns are fundamental to how the system operates.

### Q: Why are cross-cutting patterns important?

**A**: Cross-cutting patterns are important because: (1) **Consistency** (same patterns across domains), (2) **Reusability** (patterns can be reused), (3) **Maintainability** (easier to maintain consistent patterns), (4) **Quality** (proven patterns reduce errors), (5) **Scalability** (patterns designed for scale). Understanding cross-cutting patterns enables effective architecture design.

### Q: How do I apply governor limit management patterns?

**A**: Apply by: (1) **Bulkifying all code** (no DML/SOQL in loops), (2) **Using async processing** (Batch, Queueable, @future) for long-running operations, (3) **Optimizing queries** (reduce query count, improve selectivity), (4) **Using Platform Cache** to reduce query load, (5) **Monitoring limit usage** proactively, (6) **Breaking work into chunks** for large datasets. Governor limit management is critical for all Salesforce development.

### Q: What is bulkification and why is it important?

**A**: **Bulkification** is designing code to handle multiple records efficiently (bulk operations). It's important because: (1) **Salesforce processes records in bulk** (triggers, flows receive collections), (2) **Prevents governor limit violations** (efficient processing), (3) **Better performance** (bulk operations are faster), (4) **Required for production** (code must handle bulk). All code should be bulkified.

### Q: How do I use external IDs for stable record mapping?

**A**: Use external IDs by: (1) **Mirroring external system primary keys** (e.g., EMPLID, external system IDs), (2) **Designing stable external IDs** (don't change over time), (3) **Using composite external IDs** when external systems use multi-column keys, (4) **Using external IDs for record matching** (upsert operations), (5) **Including timestamp fields** to track last sync time. External IDs enable stable record mapping and idempotent operations.

### Q: How do I implement consistent error handling?

**A**: Implement by: (1) **Using structured logging** (consistent log format), (2) **Creating custom exceptions** for specific scenarios, (3) **Wrapping DML operations** in try-catch blocks, (4) **Logging errors** with context (user, record, operation), (5) **Providing user-friendly error messages**, (6) **Handling errors gracefully** (retry logic, fallback). Consistent error handling improves debugging and user experience.

### Q: How do cross-cutting patterns relate to domain-specific patterns?

**A**: Cross-cutting patterns **apply across all domains** (development, integrations, security, data modeling). Domain-specific patterns are **specific to a domain** (Apex patterns, integration patterns, security patterns). Cross-cutting patterns provide foundation, domain-specific patterns provide domain expertise. Use both together for comprehensive architecture.

### Q: What are best practices for cross-cutting patterns?

**A**: Best practices include: (1) **Apply consistently** (use same patterns across domains), (2) **Document patterns** (clear pattern documentation), (3) **Train teams** (ensure team understands patterns), (4) **Review code** (verify patterns are followed), (5) **Iterate and improve** (refine patterns based on experience), (6) **Share knowledge** (document learnings, best practices).

## To Validate

- Advanced governor limit optimization techniques
- Change Data Capture (CDC) patterns for real-time synchronization
- Marketing Cloud integration patterns
- Contact center integration patterns
- ITSM/Incident Management integration patterns

