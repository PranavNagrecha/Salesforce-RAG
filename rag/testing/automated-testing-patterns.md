# Automated Testing Patterns for Salesforce

## Overview

This guide covers automated testing patterns for Salesforce at scale, including Apex test data factories, UI test automation for LWC and Experience Cloud, contract tests for integrations, and load testing patterns. These patterns are essential for ensuring code quality, preventing regressions, and maintaining system reliability at enterprise scale.

**Related Patterns**:
- [Apex Testing Patterns](apex-testing-patterns.md) - Apex test class patterns
- [Test Data Factories](test-data-factories.md) - Test data factory patterns
- [Testing Strategy](../project-methods/testing-strategy.md) - Comprehensive testing strategies
- [Non-Functional Requirements](non-functional-requirements.md) - Security, accessibility, and performance testing

## Consensus Best Practices

- **Automate all repetitive tests**: Automate tests that run frequently or are critical
- **Use test data factories**: Create reusable test data factories for consistent test data
- **Test at multiple levels**: Unit tests, integration tests, UI tests, and end-to-end tests
- **Maintain test coverage**: Aim for high code coverage with meaningful tests
- **Test with realistic data**: Use production-like data volumes and scenarios
- **Automate test execution**: Integrate tests into CI/CD pipelines
- **Monitor test results**: Track test execution and failure rates
- **Maintain test code quality**: Treat test code with same quality standards as production code

## Apex Test Data Factories

### Factory Pattern Enhancements

**Advanced Factory Patterns**:
- **Builder pattern**: Fluent API for building test data
- **Template pattern**: Reusable templates for common scenarios
- **Strategy pattern**: Different strategies for different test scenarios
- **Factory registry**: Central registry of factories for easy access

**Factory Best Practices**:
- Create factories per object type
- Support customization of factory output
- Make factories idempotent (safe to call multiple times)
- Document factory usage and parameters
- Version factories for breaking changes

### Bulk Factory Patterns

**Bulk Data Creation**:
- Create large datasets efficiently
- Use Bulk API patterns for very large datasets
- Optimize for governor limits
- Support batch creation for performance

**Bulk Factory Implementation**:
- Create records in collections
- Use Database.insert with allOrNothing=false for partial success
- Process in batches to avoid governor limits
- Track creation progress for large datasets

**Bulk Factory Examples**:
- Create 200+ records for bulk testing
- Create related records in bulk
- Create complex object hierarchies in bulk
- Support bulk creation with relationships

### Relationship Factories

**Relationship Factory Patterns**:
- **Parent-child factories**: Create parent and child records together
- **Many-to-many factories**: Create junction object records
- **Hierarchical factories**: Create multi-level hierarchies
- **Cross-object factories**: Create related records across objects

**Relationship Factory Implementation**:
- Create parent records first
- Use parent IDs for child record creation
- Support relationship traversal
- Handle circular dependencies

**Relationship Factory Best Practices**:
- Document relationship requirements
- Support optional relationships
- Handle relationship cardinality
- Test relationship factories independently

## UI Test Automation

### LWC Test Automation (Jest)

**Jest Testing Framework**:
- Use Jest for LWC unit testing
- Test component logic and rendering
- Mock Apex methods and wire adapters
- Test user interactions and events

**Jest Test Patterns**:
- **Component rendering tests**: Test component initialization
- **Property tests**: Test property updates
- **Event tests**: Test event handling
- **Wire adapter tests**: Test data loading
- **Imperative call tests**: Test Apex method calls

**Jest Best Practices**:
- Test component behavior, not implementation
- Use meaningful test descriptions
- Mock external dependencies
- Test error scenarios
- Maintain test coverage

### Experience Cloud UI Testing

**Experience Cloud Testing Challenges**:
- Multiple user types and profiles
- Portal-specific functionality
- Identity provider integration
- Sharing and security models

**Experience Cloud Test Patterns**:
- **User type testing**: Test with different user types
- **Portal page testing**: Test portal-specific pages
- **Authentication testing**: Test login and authentication flows
- **Sharing testing**: Test record sharing in portals

**Experience Cloud Test Tools**:
- Selenium for browser automation
- Playwright for modern browser testing
- Salesforce Test Automation Framework
- Custom test utilities

### Selenium/Playwright Patterns

**Selenium Test Patterns**:
- **Page Object Model**: Encapsulate page elements and actions
- **Test data management**: Manage test data for UI tests
- **Wait strategies**: Handle asynchronous page loads
- **Cross-browser testing**: Test across different browsers

**Playwright Advantages**:
- Modern browser automation
- Better async handling
- Auto-waiting for elements
- Cross-browser support

**UI Test Best Practices**:
- Use page object model
- Implement proper waits
- Handle flaky tests
- Maintain test stability
- Test critical user journeys

## Contract Tests for Integrations

### API Contract Testing

**Contract Test Definition**:
- Test API contracts between systems
- Verify request/response formats
- Validate data transformations
- Ensure backward compatibility

**Contract Test Patterns**:
- **Request validation**: Validate request format and required fields
- **Response validation**: Validate response format and data
- **Schema validation**: Validate against JSON/XML schemas
- **Version testing**: Test API version compatibility

**Contract Test Implementation**:
- Use contract testing frameworks (Pact, Spring Cloud Contract)
- Define contracts in code or schema files
- Generate tests from contracts
- Run contract tests in CI/CD

### Event Contract Testing

**Event Contract Patterns**:
- **Event schema validation**: Validate event payload structure
- **Event version testing**: Test event version compatibility
- **Event transformation testing**: Test event transformations
- **Event publishing testing**: Test event publication

**Event Contract Implementation**:
- Define event schemas
- Test event publishing
- Test event consumption
- Validate event transformations
- Test event versioning

### Integration Test Patterns

**Integration Test Types**:
- **API integration tests**: Test API connectivity and data flow
- **Event integration tests**: Test event-driven integrations
- **Batch integration tests**: Test batch data synchronization
- **Real-time integration tests**: Test real-time integrations

**Integration Test Patterns**:
- **Mock external systems**: Mock external APIs for testing
- **Test data setup**: Set up test data for integration tests
- **End-to-end testing**: Test complete integration flows
- **Error scenario testing**: Test error handling and recovery

**Integration Test Best Practices**:
- Isolate integration tests from production
- Use test environments for integration testing
- Mock external systems when possible
- Test both success and failure scenarios
- Monitor integration test execution

## Load Testing Patterns

### Performance Testing Strategies

**Load Testing Types**:
- **Load testing**: Test under expected load
- **Stress testing**: Test beyond expected load
- **Spike testing**: Test sudden load increases
- **Endurance testing**: Test under sustained load

**Load Testing Metrics**:
- **Response time**: API and page response times
- **Throughput**: Requests per second
- **Error rate**: Percentage of failed requests
- **Resource utilization**: CPU, memory, database usage

**Load Testing Tools**:
- **JMeter**: Open-source load testing tool
- **Gatling**: Scala-based load testing tool
- **k6**: Modern load testing tool
- **Salesforce Performance Testing**: Native Salesforce tools

### Load Testing Implementation

**Load Test Planning**:
- Define load test scenarios
- Identify test data requirements
- Plan test execution windows
- Define success criteria

**Load Test Execution**:
- Set up load test environment
- Configure load test tools
- Execute load tests
- Monitor system during tests
- Collect test results

**Load Test Analysis**:
- Analyze response times
- Identify performance bottlenecks
- Review error rates
- Optimize based on findings

### Scalability Testing

**Scalability Test Patterns**:
- **Horizontal scaling**: Test with multiple instances
- **Vertical scaling**: Test with increased resources
- **Data volume scaling**: Test with large data volumes
- **User volume scaling**: Test with large user counts

**Scalability Test Metrics**:
- System capacity limits
- Performance degradation points
- Resource utilization trends
- Scaling effectiveness

**Scalability Test Best Practices**:
- Test with realistic data volumes
- Test with realistic user counts
- Monitor resource utilization
- Identify scaling bottlenecks
- Plan for capacity growth

## Test Automation Infrastructure

### CI/CD Integration

**Test Execution in CI/CD**:
- Run unit tests on every commit
- Run integration tests on pull requests
- Run full test suite before deployment
- Run smoke tests after deployment

**Test Automation Best Practices**:
- Fast feedback loops
- Parallel test execution
- Test result reporting
- Failure notification

### Test Data Management

**Test Data Strategies**:
- **Test data factories**: Generate test data programmatically
- **Test data sets**: Maintain reusable test data sets
- **Test data isolation**: Isolate test data per test
- **Test data cleanup**: Clean up test data after tests

**Test Data Best Practices**:
- Use test data factories
- Maintain test data in version control
- Document test data requirements
- Clean up test data after tests

## Related Patterns

- [Apex Testing Patterns](apex-testing-patterns.md) - Apex test class patterns
- [Test Data Factories](test-data-factories.md) - Test data factory patterns
- [Testing Strategy](../project-methods/testing-strategy.md) - Comprehensive testing strategies
- [Non-Functional Requirements](non-functional-requirements.md) - Security, accessibility, and performance testing
- [Performance Tuning](../observability/performance-tuning.md) - Performance optimization patterns

