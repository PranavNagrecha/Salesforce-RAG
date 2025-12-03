---
title: "Automated Testing Patterns for Salesforce"
level: "Advanced"
tags:
  - testing
  - automation
  - ui-testing
  - contract-testing
  - load-testing
last_reviewed: "2025-01-XX"
---

# Automated Testing Patterns for Salesforce

## Overview

This guide covers automated testing patterns for Salesforce at scale, including Apex test data factories, UI test automation for LWC and Experience Cloud, contract tests for integrations, and load testing patterns. These patterns are essential for ensuring code quality, preventing regressions, and maintaining system reliability at enterprise scale.

**Related Patterns**:
- [Apex Testing Patterns](testing/apex-testing-patterns.html) - Apex test class patterns
- [Test Data Factories](testing/test-data-factories.html) - Test data factory patterns
- [Testing Strategy](project-methods/testing-strategy.html) - Comprehensive testing strategies
- [Non-Functional Requirements](testing/non-functional-requirements.html) - Security, accessibility, and performance testing

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

## Q&A

### Q: What types of automated testing should I implement for Salesforce?

**A**: Implement testing at multiple levels: (1) **Unit tests** (Apex test classes) for code logic, (2) **Integration tests** for API and data synchronization, (3) **UI tests** for LWC components and Experience Cloud, (4) **Contract tests** for integrations, (5) **Load tests** for performance. Each level serves different purposes and catches different types of issues.

### Q: How do I automate UI testing for Lightning Web Components?

**A**: Automate LWC UI testing by: (1) **Using Jest** for unit testing LWC components, (2) **Using Playwright or Selenium** for end-to-end UI testing, (3) **Using Salesforce Test Automation Framework** for Salesforce-specific UI testing, (4) **Creating page object models** for maintainable test code, (5) **Testing accessibility** with automated accessibility testing tools.

### Q: What are contract tests and why are they important for integrations?

**A**: **Contract tests** verify that integration interfaces (APIs, events) match expected contracts. They're important because they: (1) **Prevent breaking changes** in integrations, (2) **Enable independent development** of integrated systems, (3) **Document integration contracts**, (4) **Catch integration issues early**. Use tools like Pact for contract testing.

### Q: How do I implement load testing for Salesforce?

**A**: Implement load testing by: (1) **Defining load test scenarios** (expected load, stress points), (2) **Using load testing tools** (JMeter, Gatling, k6), (3) **Testing in sandbox environments**, (4) **Monitoring system metrics** during tests, (5) **Analyzing results** to identify bottlenecks. Test under expected load, beyond expected load (stress), and with sudden spikes.

### Q: Should I run all tests in CI/CD pipelines?

**A**: **Run different tests at different stages**: (1) **Unit tests on every commit** for fast feedback, (2) **Integration tests on pull requests** to catch integration issues, (3) **Full test suite before deployment** to ensure quality, (4) **Smoke tests after deployment** to verify deployment success. Balance test coverage with execution time.

### Q: How do I manage test data for automated tests?

**A**: Manage test data by: (1) **Using test data factories** to generate data programmatically, (2) **Maintaining reusable test data sets** in version control, (3) **Isolating test data per test** to prevent interference, (4) **Cleaning up test data after tests** to maintain test environment, (5) **Documenting test data requirements** for each test.

### Q: What is the difference between load testing, stress testing, and spike testing?

**A**: **Load testing** tests under expected load to verify system handles normal usage. **Stress testing** tests beyond expected load to find breaking points. **Spike testing** tests sudden load increases to verify system handles traffic spikes. Each type reveals different performance characteristics and failure modes.

### Q: How do I test integrations with external systems?

**A**: Test integrations by: (1) **Mocking external systems** when possible to isolate tests, (2) **Using test environments** for integration testing, (3) **Testing both success and failure scenarios**, (4) **Testing batch and real-time integrations** separately, (5) **Monitoring integration test execution** for reliability. Use contract tests to verify integration interfaces.

### Q: What metrics should I track for automated testing?

**A**: Track metrics including: (1) **Test coverage** (code coverage percentage), (2) **Test execution time** (how long tests take to run), (3) **Test failure rate** (percentage of failing tests), (4) **Test flakiness** (tests that fail intermittently), (5) **Time to detect issues** (how quickly tests catch bugs). These metrics help improve test quality and effectiveness.

### Q: How do I make automated tests maintainable?

**A**: Make tests maintainable by: (1) **Using page object models** for UI tests, (2) **Creating reusable test data factories**, (3) **Following DRY principles** (Don't Repeat Yourself), (4) **Documenting test purpose and setup**, (5) **Treating test code with same quality standards** as production code, (6) **Refactoring tests** as requirements change.

## Related Patterns

- [Apex Testing Patterns](testing/apex-testing-patterns.html) - Apex test class patterns
- [Test Data Factories](testing/test-data-factories.html) - Test data factory patterns
- [Testing Strategy](project-methods/testing-strategy.html) - Comprehensive testing strategies
- [Non-Functional Requirements](testing/non-functional-requirements.html) - Security, accessibility, and performance testing
- [Performance Tuning](observability/performance-tuning.html) - Performance optimization patterns

