---
title: "LWC Jest Testing - Unit Testing Lightning Web Components"
source: "The Salesforce Master Class wiki"
source_url: "https://github.com/Coding-With-The-Force/The-Salesforce-Master-Class/wiki"
topic: "Topic 3: The Complete Guide To Lightning Web Components"
section: "LWC Jest Testing"
level: "Intermediate"
tags:
  - salesforce
  - lwc
  - testing
  - jest
  - unit-testing
  - best-practices
last_reviewed: "2025-01-XX"
---

# Overview

Jest testing is the standard approach for unit testing Lightning Web Components (LWC). Jest enables developers to test component logic, user interactions, data access, and integration with Apex methods in isolation. Effective Jest testing ensures component quality, prevents regressions, and enables confident refactoring.

Jest testing encompasses setting up Jest testing environment, writing test cases for component behavior, testing events and conditional rendering, testing wire adapters and Apex calls, testing child components, and integrating Jest tests into CI/CD pipelines. Understanding Jest testing patterns enables developers to write comprehensive, maintainable tests.

Most LWC development should include Jest tests. Tests should cover component logic, user interactions, data access patterns, and error handling. Well-written Jest tests serve as documentation and enable safe refactoring.

# Core Concepts

## What Is Jest Testing?

**What it is**: Jest is a JavaScript testing framework used for unit testing Lightning Web Components.

**Key characteristics**:
- Runs in Node.js environment (not browser)
- Mocks Salesforce platform APIs
- Tests component logic and behavior
- Fast execution
- Integrated with Salesforce DX

**What Jest tests**:
- Component initialization and rendering
- Property and method behavior
- Event handling and dispatching
- Conditional rendering logic
- Wire adapter behavior
- Apex method calls
- Child component interactions

**What Jest doesn't test**:
- Actual Salesforce data (uses mocks)
- Browser-specific behavior (runs in Node.js)
- Visual appearance (tests logic, not UI)
- Integration with other components (unit tests, not integration tests)

## Setting Up Jest Testing

**What it is**: Configuring development environment and project for Jest testing.

**Prerequisites**:
- Salesforce DX project setup
- Node.js and npm installed
- Jest and @salesforce/sfdx-lwc-jest installed

**Setup steps**:
1. Install Jest dependencies: `npm install --save-dev jest @salesforce/sfdx-lwc-jest @salesforce/lwc-jest-utils`
2. Configure Jest in `package.json` or `jest.config.js`
3. Create test files alongside component files
4. Run tests: `npm test` or `sfdx-lwc-jest`

**Configuration**:
- Jest configuration for LWC
- Mock setup for Salesforce APIs
- Test file patterns
- Coverage reporting

## Basic Jest Test Structure

**What it is**: Standard structure for Jest test files.

**Test file structure**:
```javascript
import { createElement } from 'lwc';
import MyComponent from 'c/myComponent';

describe('c-my-component', () => {
    afterEach(() => {
        while (document.body.firstChild) {
            document.body.removeChild(document.body.firstChild);
        }
    });

    it('renders component', () => {
        const element = createElement('c-my-component', {
            is: MyComponent
        });
        document.body.appendChild(element);
        
        // Assertions
        expect(element).toBeTruthy();
    });
});
```

**Key elements**:
- **describe**: Test suite for component
- **it/test**: Individual test case
- **beforeEach/afterEach**: Setup and cleanup
- **createElement**: Create component instance
- **Assertions**: Verify expected behavior

## Testing Component Properties

**What it is**: Testing how components respond to property changes.

**Testing approach**:
- Set properties when creating element
- Change properties after creation
- Verify component updates reactively
- Test property validation and defaults

**Example**:
```javascript
it('updates when property changes', () => {
    const element = createElement('c-my-component', {
        is: MyComponent
    });
    element.recordId = '001xx000003DGbQAAW';
    document.body.appendChild(element);
    
    return Promise.resolve().then(() => {
        // Assert property value
        expect(element.recordId).toBe('001xx000003DGbQAAW');
    });
});
```

## Testing Events

**What it is**: Testing component event handling and dispatching.

**Testing approach**:
- Simulate user interactions
- Verify events are dispatched
- Test event listeners
- Verify event payload

**Example**:
```javascript
it('dispatches custom event', () => {
    const element = createElement('c-my-component', {
        is: MyComponent
    });
    document.body.appendChild(element);
    
    const handler = jest.fn();
    element.addEventListener('custom', handler);
    
    // Trigger event
    const button = element.shadowRoot.querySelector('lightning-button');
    button.click();
    
    return Promise.resolve().then(() => {
        expect(handler).toHaveBeenCalled();
    });
});
```

## Testing Wire Adapters

**What it is**: Testing components that use @wire to access Salesforce data.

**Testing approach**:
- Mock wire adapter responses
- Test reactive wire behavior
- Test error handling
- Verify data rendering

**Example**:
```javascript
import { registerApexTestWireAdapter } from '@salesforce/sfdx-lwc-jest';
import getRecord from '@salesforce/apex/MyController.getRecord';

const getRecordAdapter = registerApexTestWireAdapter(getRecord);

it('renders data from wire adapter', () => {
    const element = createElement('c-my-component', {
        is: MyComponent
    });
    element.recordId = '001xx000003DGbQAAW';
    document.body.appendChild(element);
    
    // Emit mock data
    getRecordAdapter.emit({ Name: 'Test Account' });
    
    return Promise.resolve().then(() => {
        const name = element.shadowRoot.querySelector('.name');
        expect(name.textContent).toBe('Test Account');
    });
});
```

## Testing Apex Method Calls

**What it is**: Testing components that call Apex methods imperatively.

**Testing approach**:
- Mock Apex method responses
- Test method calls
- Test error handling
- Verify UI updates

**Example**:
```javascript
import { registerApexTestWireAdapter } from '@salesforce/sfdx-lwc-jest';
import saveRecord from '@salesforce/apex/MyController.saveRecord';

const saveRecordAdapter = registerApexTestWireAdapter(saveRecord);

it('calls Apex method and handles response', () => {
    const element = createElement('c-my-component', {
        is: MyComponent
    });
    document.body.appendChild(element);
    
    // Mock successful response
    saveRecordAdapter.emit({ success: true });
    
    const button = element.shadowRoot.querySelector('lightning-button');
    button.click();
    
    return Promise.resolve().then(() => {
        expect(saveRecordAdapter.getLastConfig()).toBeTruthy();
    });
});
```

## Testing Child Components

**What it is**: Testing components that contain or interact with child components.

**Testing approach**:
- Test child component rendering
- Test parent-child communication
- Mock child component behavior
- Test slot content

**Example**:
```javascript
it('renders child component', () => {
    const element = createElement('c-parent-component', {
        is: ParentComponent
    });
    document.body.appendChild(element);
    
    return Promise.resolve().then(() => {
        const child = element.shadowRoot.querySelector('c-child-component');
        expect(child).toBeTruthy();
    });
});
```

# Deep-Dive Patterns & Best Practices

## Test Organization

### Test File Structure

**Pattern**: Organize tests logically within test file.

**Structure**:
- Group related tests in describe blocks
- Use descriptive test names
- Order tests logically (setup, basic, advanced, edge cases)
- Keep tests independent (no dependencies between tests)

**Best practices**:
- One describe block per component
- Nested describe blocks for logical groupings
- Clear, descriptive test names
- Independent tests (can run in any order)

### Test Data Management

**Pattern**: Use consistent test data patterns.

**Approaches**:
- **Constants**: Define test data as constants
- **Factories**: Create test data factories for complex data
- **Mocks**: Use mocks for external dependencies
- **Fixtures**: Use fixtures for complex test scenarios

**Best practices**:
- Reuse test data where appropriate
- Keep test data realistic
- Use factories for complex data
- Mock external dependencies

## Testing Patterns

### Async Testing Pattern

**Pattern**: Handle asynchronous operations in tests.

**Approach**:
- Use `Promise.resolve()` for async operations
- Use `flushPromises()` for wire adapter updates
- Use `await` for async/await code
- Return promises from tests

**Example**:
```javascript
it('handles async operation', () => {
    const element = createElement('c-my-component', {
        is: MyComponent
    });
    document.body.appendChild(element);
    
    // Trigger async operation
    const button = element.shadowRoot.querySelector('lightning-button');
    button.click();
    
    return Promise.resolve().then(() => {
        // Assert after async completes
        expect(element.isLoading).toBe(false);
    });
});
```

### Mock Pattern

**Pattern**: Mock external dependencies for isolated testing.

**Approaches**:
- Mock Apex methods
- Mock wire adapters
- Mock platform APIs
- Mock child components

**Best practices**:
- Mock external dependencies
- Keep mocks simple and focused
- Use realistic mock data
- Verify mock interactions

### Error Testing Pattern

**Pattern**: Test error handling and error states.

**Approach**:
- Test error scenarios
- Verify error messages
- Test error recovery
- Verify error UI

**Example**:
```javascript
it('handles Apex method error', () => {
    const element = createElement('c-my-component', {
        is: MyComponent
    });
    document.body.appendChild(element);
    
    // Mock error response
    saveRecordAdapter.emit(new Error('Test error'));
    
    const button = element.shadowRoot.querySelector('lightning-button');
    button.click();
    
    return Promise.resolve().then(() => {
        const error = element.shadowRoot.querySelector('.error');
        expect(error).toBeTruthy();
    });
});
```

# Implementation Guide

## Prerequisites

- Salesforce DX project setup
- Node.js and npm installed
- Understanding of Jest testing framework
- Understanding of LWC component structure

## High-Level Steps

1. **Set up Jest**: Install dependencies, configure Jest
2. **Create test file**: Create test file alongside component
3. **Write basic test**: Test component rendering
4. **Add property tests**: Test property behavior
5. **Add interaction tests**: Test user interactions and events
6. **Add data tests**: Test wire adapters and Apex calls
7. **Add error tests**: Test error handling
8. **Run tests**: Execute tests and verify coverage

## Key Configuration Decisions

**Test coverage target**: What coverage to aim for? Typically 80%+, focus on critical paths.

**Test organization**: How to organize tests? By component, by feature, or by type.

**Mock strategy**: How to mock dependencies? Mock everything, or use real implementations where possible.

# Common Pitfalls & Anti-Patterns

## Bad Pattern: Not Testing Components

**Why it's bad**: Untested components lead to bugs, regressions, and difficult refactoring.

**Better approach**: Write tests for all components. Aim for good coverage. Test critical paths thoroughly.

## Bad Pattern: Testing Implementation Details

**Why it's bad**: Tests that depend on implementation details break when implementation changes, even if behavior is correct.

**Better approach**: Test behavior, not implementation. Test what component does, not how it does it.

## Bad Pattern: Not Testing Error Cases

**Why it's bad**: Error cases are common in production. Not testing them leads to poor error handling.

**Better approach**: Test error scenarios. Verify error messages and recovery. Test error UI.

## Bad Pattern: Over-Mocking

**Why it's bad**: Too many mocks make tests brittle and don't test real behavior.

**Better approach**: Mock external dependencies, but test real component behavior. Balance mocking with realism.

# Real-World Scenarios

## Scenario 1: Testing Component with Wire Adapter

**Problem**: Need to test component that uses @wire to get record data.

**Context**: Component displays account name from wire adapter.

**Solution**: Mock wire adapter, emit test data, verify component renders data correctly. Test error handling. Test reactive updates.

## Scenario 2: Testing Component with Apex Call

**Problem**: Need to test component that calls Apex method on button click.

**Context**: Component saves record when button is clicked.

**Solution**: Mock Apex method, simulate button click, verify method is called with correct parameters, test success and error handling.

## Scenario 3: Testing Component with Events

**Problem**: Need to test component that dispatches custom events.

**Context**: Component dispatches event when form is submitted.

**Solution**: Add event listener, simulate form submission, verify event is dispatched with correct payload.

# Checklist / Mental Model

## Writing Jest Tests

- [ ] Set up Jest testing environment
- [ ] Create test file alongside component
- [ ] Write basic rendering test
- [ ] Test component properties
- [ ] Test user interactions and events
- [ ] Test wire adapters and Apex calls
- [ ] Test error handling
- [ ] Run tests and verify coverage

## Test Quality

- [ ] Tests are independent (no dependencies)
- [ ] Tests are fast (use mocks, avoid real API calls)
- [ ] Tests are reliable (consistent results)
- [ ] Tests are maintainable (clear, well-organized)
- [ ] Tests cover critical paths
- [ ] Tests include error cases

## Mental Model: Test Behavior, Not Implementation

Think of Jest tests as testing what components do (behavior), not how they do it (implementation). Tests should verify expected behavior, handle user interactions, and test error cases. Focus on user-visible behavior and critical paths.

# Key Terms & Definitions

- **Jest**: JavaScript testing framework for unit testing
- **Unit test**: Test that verifies individual component behavior in isolation
- **Mock**: Simulated dependency used in testing
- **Wire adapter**: Reactive service that provides data to components
- **Test coverage**: Percentage of code covered by tests
- **Assertion**: Statement that verifies expected behavior in test

## Q&A

### Q: How do I set up Jest testing for Lightning Web Components?

**A**: Set up Jest by: (1) **Installing Jest dependencies** (`jest`, `@salesforce/sfdx-lwc-jest`, `@salesforce/lwc-jest-utils`), (2) **Configuring Jest** in `package.json` or `jest.config.js`, (3) **Creating test files** alongside component files (`.test.js` or `.spec.js`), (4) **Running tests** with `npm test` or `sfdx-lwc-jest`. Follow Salesforce DX Jest setup documentation for complete setup.

### Q: How do I test components that use @wire adapters?

**A**: Test wire adapters by: (1) **Using `registerApexTestWireAdapter`** to register wire adapter, (2) **Creating component** in test, (3) **Emitting mock data** using adapter, (4) **Verifying component renders data** correctly, (5) **Testing reactive updates** (data changes), (6) **Testing error handling** (wire adapter errors). Wire adapters provide reactive data to components.

### Q: How do I test components that call Apex methods?

**A**: Test Apex calls by: (1) **Using `registerApexTestWireAdapter`** to register Apex method, (2) **Creating component** in test, (3) **Simulating user interaction** that triggers method call, (4) **Emitting mock response** using adapter, (5) **Verifying method is called** with correct parameters, (6) **Verifying component handles response** correctly. Mock Apex methods to test component behavior.

### Q: How do I test component events?

**A**: Test events by: (1) **Adding event listener** to component, (2) **Simulating user interaction** that triggers event, (3) **Verifying event is dispatched** using `toHaveBeenCalled()`, (4) **Verifying event payload** if needed, (5) **Testing both custom events and standard events**. Events enable component communication.

### Q: What should I test in LWC components?

**A**: Test: (1) **Component rendering** (renders correctly, displays data), (2) **Property behavior** (properties work correctly), (3) **User interactions** (button clicks, form inputs), (4) **Event handling** (events dispatched/received), (5) **Wire adapter behavior** (data loading, errors), (6) **Apex method calls** (methods called correctly), (7) **Error handling** (errors handled gracefully), (8) **Conditional rendering** (renders based on conditions). Focus on behavior, not implementation details.

### Q: How do I test async operations in Jest?

**A**: Test async by: (1) **Using `Promise.resolve()`** for async operations, (2) **Using `flushPromises()`** for wire adapter updates, (3) **Using `await`** for async/await code, (4) **Returning promises** from tests, (5) **Waiting for async operations** to complete. Handle async operations properly to avoid flaky tests.

### Q: How do I mock dependencies in Jest tests?

**A**: Mock by: (1) **Mocking Apex methods** using `registerApexTestWireAdapter`, (2) **Mocking wire adapters**, (3) **Mocking platform APIs**, (4) **Mocking child components**, (5) **Using realistic mock data**. Keep mocks simple and focused. Mocks enable isolated component testing.

### Q: What's the difference between unit tests and integration tests for LWC?

**A**: **Unit tests (Jest)** test components in isolation with mocks, run fast, test component logic. **Integration tests** test components with real dependencies, run slower, test component interactions. Use both for comprehensive testing. Unit tests catch logic errors, integration tests catch integration issues.

### Q: How do I test error handling in LWC components?

**A**: Test error handling by: (1) **Mocking error responses** from Apex methods or wire adapters, (2) **Simulating error scenarios** (network errors, Apex errors), (3) **Verifying error messages** are displayed, (4) **Testing error recovery** (retry logic, fallback), (5) **Verifying error UI** (error messages, error states). Test both Apex errors and wire adapter errors.

### Q: How do I integrate Jest tests into CI/CD pipeline?

**A**: Integrate by: (1) **Configuring CI/CD** to run Jest tests on code changes, (2) **Setting up test coverage reporting** (track coverage metrics), (3) **Failing builds** on test failures, (4) **Including test results** in build artifacts, (5) **Using Salesforce DX commands** or npm scripts to run tests. Automated testing catches issues early.

## Related Patterns

- [LWC Patterns](../development/lwc-patterns.md) - LWC component patterns
- [LWC Accessibility Testing](lwc-accessibility-testing.md) - Accessibility testing patterns
- [Automated Testing Patterns](automated-testing-patterns.md) - Automated testing approaches
- [Testing Strategy](../project-methods/testing-strategy.md) - Comprehensive testing strategies



