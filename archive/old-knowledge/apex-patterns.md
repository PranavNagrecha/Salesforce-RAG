# Apex Design, Bulkification, and Test Strategy

## What Was Actually Done

Apex is used strategically when Flows are insufficient or need optimization/bulkification. The approach emphasizes proper layering, bulkification, and comprehensive testing.

### When Apex is Chosen

Apex is selected when:
- Flows are insufficient for complex logic or performance requirements
- Heavy reuse is needed by LWCs, external APIs, or other Apex
- Tight control over performance and governor limits is required
- Complex branching or algorithms that are difficult in Flow
- Integration with external APIs needing complex authentication and error handling

### Apex Class Layering

Apex classes are structured in layers:
- **Service Layer**: Business logic and orchestration
- **Domain Layer**: Object-specific logic and validation
- **Selector Layer**: SOQL queries and data access
- **Integration Layer**: External API callouts and transformations

### SOQL Design in Apex

SOQL queries are designed with:
- Selective WHERE clauses using indexed fields
- Bulkification to handle collections efficiently
- Avoidance of SOQL in loops
- Proper use of aggregate queries and subqueries
- Governor limit awareness

### Asynchronous Apex Patterns

Asynchronous patterns are used for:
- **Queueable**: Chaining jobs, callouts after DML, lightweight async processing
- **Batchable**: Large data processing, scheduled batch jobs
- **Scheduled**: Time-based automation, periodic maintenance

### Apex + LWC Patterns

Apex is exposed to LWCs through:
- `@AuraEnabled` methods for imperative calls
- `@wire` adapters for reactive data access
- Service layer pattern with clean method signatures
- DTO-style payloads to abstract SOQL details from components

### Error Handling in Apex

Error handling patterns include:
- Try-catch blocks around DML operations
- Custom exceptions for specific scenarios
- Error logging utility classes
- Meaningful error messages for users
- Graceful degradation when possible

## Rules and Patterns

### Apex Class Structure

- Use layered architecture (Service, Domain, Selector, Integration)
- Keep classes focused on single responsibility
- Use dependency injection where appropriate
- Document public methods with ApexDoc
- Follow naming conventions consistently

### Bulkification

- Always process collections, not single records
- Avoid DML and SOQL in loops
- Use bulk DML operations (insert, update, upsert with collections)
- Handle governor limits proactively
- Test with maximum data volumes

### SOQL Best Practices

- Use selective WHERE clauses with indexed fields
- Avoid querying ID fields unnecessarily
- Use aggregate queries for counts and summaries
- Leverage subqueries for related data
- Monitor query performance and optimize

### Test Strategy

- Aim for 100% code coverage (minimum 90%)
- Test both positive and negative scenarios
- Use test data factories for consistent test data
- Avoid @SeeAllData annotation
- Use Test.startTest() and Test.stopTest() to reset governor limits
- Test with bulk data (200 records minimum)

### Integration Patterns

- Use callout mocks for testing
- Implement retry logic for transient failures
- Handle API authentication securely
- Use named credentials for endpoint configuration
- Log all integration calls for troubleshooting

## Suggested Improvements (From AI)

### Enhanced Test Framework

Build a comprehensive test framework:
- Test data factory patterns for all objects
- Mock framework for external integrations
- Automated test execution in CI/CD
- Test coverage reporting and tracking
- Performance testing for critical paths

### Code Quality Tools

Implement code quality tools:
- PMD for static code analysis
- ESLint for JavaScript/LWC code
- Automated code review processes
- Code quality gates in CI/CD
- Regular code review sessions

### Documentation Standards

Establish documentation standards:
- ApexDoc for all public methods
- Architecture decision records (ADRs)
- API documentation for reusable classes
- Code comments for complex logic
- Change logs for significant modifications

## To Validate

- Specific Apex class naming conventions
- Exact layering structure and dependency patterns
- SOQL optimization techniques used
- Test coverage targets and strategies
- Integration error handling patterns

