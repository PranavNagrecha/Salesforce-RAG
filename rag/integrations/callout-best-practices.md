---
title: "Callout Best Practices"
level: "Intermediate"
tags:
  - integrations
  - apex
  - callouts
  - http
  - best-practices
  - error-handling
last_reviewed: "2025-01-XX"
---

# Callout Best Practices

## Overview

This guide provides comprehensive best practices for implementing HTTP callouts in Salesforce, covering limitations, authentication, error handling, asynchronous patterns, circuit breakers, response optimization, testing, and monitoring. Following these patterns ensures robust, maintainable, and efficient callout implementations.

## Prerequisites

**Required Knowledge**:
- Understanding of HTTP callouts and REST APIs
- Basic understanding of Apex programming
- Familiarity with Salesforce governor limits
- Knowledge of error handling patterns

**Recommended Reading**:
- <a href="{{ '/rag/integrations/development/apex-patterns.html' | relative_url }}">Apex Patterns</a> - Apex development patterns
- <a href="{{ '/rag/integrations/development/asynchronous-apex-patterns.html' | relative_url }}">Asynchronous Apex Patterns</a> - Queueable and @future patterns
- <a href="{{ '/rag/integrations/development/error-handling-and-logging.html' | relative_url }}">Error Handling and Logging</a> - Error handling patterns
- <a href="{{ '/rag/integrations/etl-vs-api-vs-events.html' | relative_url }}">ETL vs API vs Events</a> - Integration pattern selection
- <a href="{{ '/rag/integrations/code-examples/apex/integration-examples.html' | relative_url }}">Integration Examples</a> - Complete callout code examples

## Callout Limitations

Understanding Salesforce callout limitations is critical for designing robust integrations:

### Synchronous Callout Limitations

- **10-second timeout**: Synchronous callouts must complete within 10 seconds
- **100 callouts per transaction**: Maximum 100 HTTP callouts allowed per transaction
- **6MB heap size limit**: Total response processing must not exceed 6MB heap size
- **Named Credentials count**: Each Named Credential callout counts toward the 100 callout limit

### Asynchronous Callout Limitations

- **120-second timeout**: Asynchronous callouts (Queueable, @future, Batch) can run up to 120 seconds
- **Higher callout limits**: Asynchronous contexts have higher governor limits
- **Separate transaction**: Each async job runs in a separate transaction with fresh limits

### Impact on Design

These limitations shape callout architecture:

- **Use async patterns** for long-running or multiple callouts
- **Optimize response processing** to avoid heap size limits
- **Implement circuit breakers** for high-volume integrations
- **Monitor callout counts** to avoid hitting limits
- **Design for failure** with proper error handling and retries

## Use Named Credentials for Authentication

Named Credentials are the gold standard for managing external system authentication in Salesforce.

### Benefits of Named Credentials

- **Centralized credential management**: Single source of truth for endpoints and credentials
- **Automatic authentication handling**: OAuth, basic auth, and certificate-based auth handled automatically
- **Environment-specific configurations**: Different endpoints per org (dev, staging, production)
- **Enhanced security**: Credentials encrypted and stored securely
- **Simplified deployment**: No hardcoded URLs or credentials in code

### Implementation Pattern

```apex
// Good: Use Named Credential
req.setEndpoint('callout:MyNamedCredential/api/endpoint');

// Bad: Hardcoded URL
req.setEndpoint('https://api.example.com/endpoint');
```

### Named Credential Configuration

- **Endpoint**: Base URL for the external system
- **Identity Type**: OAuth 2.0, Named Principal, Anonymous
- **Authentication Protocol**: OAuth 2.0, Basic Auth, Certificate
- **Per-User Callout**: Enable if user-specific authentication required

**Related Patterns**: [Integration Examples](../../code-examples/apex/integration-examples.html#example-1-rest-api-callout-with-named-credentials)

## Implement Proper Error Handling

Robust error handling is essential for production callouts. Always plan for various failure scenarios.

### Error Handling Patterns

#### Pattern 1: Status Code Checking

```apex
HttpResponse response = http.send(req);

if (response.getStatusCode() >= 200 && response.getStatusCode() < 300) {
    // Success - process response
    return parseResponse(response);
} else if (response.getStatusCode() >= 400 && response.getStatusCode() < 500) {
    // Client error - don't retry
    throw new IntegrationException('Client error: ' + response.getStatusCode());
} else if (response.getStatusCode() >= 500) {
    // Server error - retryable
    throw new RetryableIntegrationException('Server error: ' + response.getStatusCode());
}
```

#### Pattern 2: Exception Handling

```apex
try {
    HttpResponse response = http.send(req);
    return processResponse(response);
} catch (CalloutException e) {
    // Network/connection errors - retryable
    LOG_LogMessageUtility.logError('IntegrationService', 'makeCallout', 
        'Callout exception: ' + e.getMessage(), e);
    throw new RetryableIntegrationException('Callout failed: ' + e.getMessage(), e);
} catch (Exception e) {
    // Unexpected errors
    LOG_LogMessageUtility.logError('IntegrationService', 'makeCallout', 
        'Unexpected error: ' + e.getMessage(), e);
    throw new IntegrationException('Unexpected error: ' + e.getMessage(), e);
}
```

#### Pattern 3: Retryable vs Non-Retryable Errors

```apex
private static Boolean isRetryableError(Integer statusCode, Exception e) {
    // Retry on server errors (5xx) and timeouts
    if (statusCode != null && statusCode >= 500) {
        return true;
    }
    
    // Retry on connection/timeout errors
    String message = e.getMessage();
    return message.contains('timeout') || 
           message.contains('Connection') ||
           message.contains('Read timed out');
}
```

### Error Handling Best Practices

- **Check HTTP status codes**: Always validate status codes before processing responses
- **Distinguish retryable vs non-retryable errors**: Don't retry client errors (4xx)
- **Log all errors**: Comprehensive logging for troubleshooting
- **Provide user-friendly messages**: Transform technical errors into actionable messages
- **Handle timeout scenarios**: Explicitly handle timeout exceptions

**Related Patterns**: <a href="{{ '/rag/integrations/development/error-handling-and-logging.html' | relative_url }}">Error Handling and Logging</a>

## Leverage Asynchronous Patterns

For non-critical callouts or when dealing with multiple external systems, use asynchronous patterns to improve user experience and avoid governor limits.

### When to Use Asynchronous Callouts

- **After DML operations**: Cannot make callouts after DML in same transaction
- **Non-critical operations**: Operations that don't require immediate user feedback
- **Multiple callouts**: When making multiple callouts that exceed synchronous limits
- **Long-running operations**: Operations that may exceed 10-second timeout

### Pattern 1: Queueable for Callouts After DML

```apex
public class CalloutQueueable implements Queueable, Database.AllowsCallouts {
    
    private Id recordId;
    private String endpoint;
    private Map<String, Object> payload;
    
    public CalloutQueueable(Id recordId, String endpoint, Map<String, Object> payload) {
        this.recordId = recordId;
        this.endpoint = endpoint;
        this.payload = payload;
    }
    
    public void execute(QueueableContext context) {
        // Make callout in separate transaction
        HttpResponse response = RestIntegrationService.post(endpoint, payload);
        
        // Update record with response
        // Note: This is a new transaction, so DML is allowed
        updateRecordWithResponse(recordId, response);
    }
}

// Usage: After DML, enqueue callout
insert contact;
System.enqueueJob(new CalloutQueueable(contact.Id, '/api/sync', payload));
```

### Pattern 2: Queueable for Multiple Callouts

```apex
public class MultiCalloutQueueable implements Queueable, Database.AllowsCallouts {
    
    private List<CalloutRequest> requests;
    
    public void execute(QueueableContext context) {
        for (CalloutRequest req : requests) {
            try {
                HttpResponse response = RestIntegrationService.makeCallout(
                    req.endpoint, req.method, req.payload
                );
                req.handleResponse(response);
            } catch (Exception e) {
                req.handleError(e);
            }
        }
    }
}
```

### Pattern 3: @future for Simple Async Callouts

```apex
@future(callout=true)
public static void makeAsyncCallout(String endpoint, String payloadJson) {
    Map<String, Object> payload = (Map<String, Object>)JSON.deserializeUntyped(payloadJson);
    RestIntegrationService.post(endpoint, payload);
}
```

**Note**: Prefer Queueable over @future for new development due to better error handling and chaining capabilities.

**Related Patterns**: <a href="{{ '/rag/integrations/development/asynchronous-apex-patterns.html' | relative_url }}">Asynchronous Apex Patterns</a>, <a href="{{ '/rag/integrations/code-examples/apex/queueable-examples.html' | relative_url }}">Queueable Examples</a>

## Implement Circuit Breaker Pattern

For high-volume integrations, implement a circuit breaker pattern to prevent cascading failures and protect external systems from overload.

### Circuit Breaker States

- **Closed**: Normal operation, callouts proceed
- **Open**: Circuit is open, callouts fail fast without attempting
- **Half-Open**: Testing if external system has recovered

### Implementation Pattern

```apex
public class CircuitBreaker {
    
    private static final Integer FAILURE_THRESHOLD = 5;
    private static final Integer TIMEOUT_SECONDS = 60;
    
    private static Map<String, CircuitState> circuitStates = new Map<String, CircuitState>();
    
    public class CircuitState {
        public Integer failureCount = 0;
        public Datetime lastFailureTime;
        public Boolean isOpen = false;
    }
    
    public static Boolean isCircuitOpen(String circuitName) {
        CircuitState state = getCircuitState(circuitName);
        
        if (!state.isOpen) {
            return false;
        }
        
        // Check if timeout has elapsed (half-open state)
        if (state.lastFailureTime != null && 
            Datetime.now().getTime() - state.lastFailureTime.getTime() > TIMEOUT_SECONDS * 1000) {
            state.isOpen = false; // Move to half-open
            return false;
        }
        
        return true;
    }
    
    public static void recordSuccess(String circuitName) {
        CircuitState state = getCircuitState(circuitName);
        state.failureCount = 0;
        state.isOpen = false;
    }
    
    public static void recordFailure(String circuitName) {
        CircuitState state = getCircuitState(circuitName);
        state.failureCount++;
        state.lastFailureTime = Datetime.now();
        
        if (state.failureCount >= FAILURE_THRESHOLD) {
            state.isOpen = true;
            LOG_LogMessageUtility.logError('CircuitBreaker', 'recordFailure', 
                'Circuit opened for: ' + circuitName);
        }
    }
    
    private static CircuitState getCircuitState(String circuitName) {
        if (!circuitStates.containsKey(circuitName)) {
            circuitStates.put(circuitName, new CircuitState());
        }
        return circuitStates.get(circuitName);
    }
}

// Usage in integration service
public static HttpResponse makeCalloutWithCircuitBreaker(String endpoint, String method, Map<String, Object> payload) {
    String circuitName = 'ExternalAPI';
    
    if (CircuitBreaker.isCircuitOpen(circuitName)) {
        throw new IntegrationException('Circuit breaker is open. External system unavailable.');
    }
    
    try {
        HttpResponse response = RestIntegrationService.makeCallout(endpoint, method, payload);
        CircuitBreaker.recordSuccess(circuitName);
        return response;
    } catch (Exception e) {
        CircuitBreaker.recordFailure(circuitName);
        throw e;
    }
}
```

### Circuit Breaker Best Practices

- **Use Custom Metadata** to configure thresholds per integration
- **Monitor circuit state** in logging and monitoring systems
- **Alert on circuit open** to notify operations team
- **Test half-open state** to ensure recovery detection
- **Use separate circuits** for different external systems

## Use Queueable Apex for Complex Callout Chains

When you need to make multiple related callouts or handle complex processing, Queueable Apex provides more flexibility than @future methods.

### Pattern 1: Chained Callouts

```apex
public class ChainedCalloutQueueable implements Queueable, Database.AllowsCallouts {
    
    private List<CalloutStep> steps;
    private Integer currentStep = 0;
    
    public void execute(QueueableContext context) {
        if (currentStep >= steps.size()) {
            return; // All steps complete
        }
        
        CalloutStep step = steps[currentStep];
        HttpResponse response = RestIntegrationService.makeCallout(
            step.endpoint, step.method, step.payload
        );
        
        // Process response and prepare next step
        step.processResponse(response);
        currentStep++;
        
        // Chain next step if more steps remain
        if (currentStep < steps.size()) {
            System.enqueueJob(this);
        }
    }
}
```

### Pattern 2: Callout with Post-Processing

```apex
public class CalloutWithProcessingQueueable implements Queueable, Database.AllowsCallouts {
    
    private Id recordId;
    private String endpoint;
    
    public void execute(QueueableContext context) {
        // Make callout
        HttpResponse response = RestIntegrationService.get(endpoint);
        
        // Process response and update records
        Map<String, Object> data = parseResponse(response);
        updateRelatedRecords(recordId, data);
        
        // Trigger downstream processing if needed
        if (needsDownstreamProcessing(data)) {
            System.enqueueJob(new DownstreamProcessingQueueable(recordId, data));
        }
    }
}
```

**Related Patterns**: <a href="{{ '/rag/integrations/code-examples/apex/queueable-examples.html' | relative_url }}">Queueable Examples</a>, <a href="{{ '/rag/integrations/development/asynchronous-apex-patterns.html' | relative_url }}">Asynchronous Apex Patterns</a>

## Optimize Response Processing

When dealing with large responses, optimize memory usage and processing to avoid heap size limits.

### Pattern 1: Stream Processing for Large Responses

```apex
public static void processLargeResponse(HttpResponse response) {
    // For very large responses, process in chunks
    String body = response.getBody();
    
    // Use JSON parser with streaming for large payloads
    JSONParser parser = JSON.createParser(body);
    
    while (parser.nextToken() != null) {
        if (parser.getCurrentToken() == JSONToken.START_OBJECT) {
            Map<String, Object> record = (Map<String, Object>)parser.readValueAs(Map.class);
            processRecord(record);
            
            // Clear processed data to free memory
            record.clear();
        }
    }
}
```

### Pattern 2: Selective Field Processing

```apex
public static List<Map<String, Object>> extractRelevantFields(String responseBody) {
    Map<String, Object> fullResponse = (Map<String, Object>)JSON.deserializeUntyped(responseBody);
    
    // Extract only needed fields to reduce memory usage
    List<String> relevantFields = new List<String>{'id', 'name', 'status'};
    List<Map<String, Object>> extracted = new List<Map<String, Object>>();
    
    for (Object recordObj : (List<Object>)fullResponse.get('records')) {
        Map<String, Object> record = (Map<String, Object>)recordObj;
        Map<String, Object> extractedRecord = new Map<String, Object>();
        
        for (String field : relevantFields) {
            if (record.containsKey(field)) {
                extractedRecord.put(field, record.get(field));
            }
        }
        
        extracted.add(extractedRecord);
    }
    
    return extracted;
}
```

### Pattern 3: Batch Processing Large Responses

```apex
public static void processResponseInBatches(HttpResponse response) {
    List<Map<String, Object>> allRecords = parseResponse(response);
    
    // Process in batches to avoid heap size limits
    Integer batchSize = 100;
    for (Integer i = 0; i < allRecords.size(); i += batchSize) {
        Integer endIndex = Math.min(i + batchSize, allRecords.size());
        List<Map<String, Object>> batch = new List<Map<String, Object>>();
        
        for (Integer j = i; j < endIndex; j++) {
            batch.add(allRecords[j]);
        }
        
        processBatch(batch);
        batch.clear(); // Free memory
    }
}
```

### Response Processing Best Practices

- **Monitor heap size**: Check `Limits.getHeapSize()` before and after processing
- **Process incrementally**: Don't load entire response into memory at once
- **Clear processed data**: Explicitly clear variables to free memory
- **Use streaming parsers**: For very large JSON responses
- **Extract only needed fields**: Reduce memory footprint

**Related Patterns**: <a href="{{ '/rag/integrations/development/governor-limits-and-optimization.html' | relative_url }}">Governor Limits and Optimization</a>

## Monitor and Log Callout Performance

Implement comprehensive monitoring and logging to track callout performance and troubleshoot issues.

### Pattern 1: Performance Logging

```apex
public static HttpResponse makeCalloutWithLogging(String endpoint, String method, Map<String, Object> payload) {
    Long startTime = System.now().getTime();
    String requestId = generateRequestId();
    
    try {
        HttpResponse response = RestIntegrationService.makeCallout(endpoint, method, payload);
        
        Long duration = System.now().getTime() - startTime;
        
        // Log performance metrics
        LOG_LogMessageUtility.logInfo('IntegrationService', 'makeCallout', 
            'Callout completed: ' + method + ' ' + endpoint + 
            ' - Status: ' + response.getStatusCode() + 
            ' - Duration: ' + duration + 'ms' +
            ' - RequestId: ' + requestId);
        
        return response;
        
    } catch (Exception e) {
        Long duration = System.now().getTime() - startTime;
        
        LOG_LogMessageUtility.logError('IntegrationService', 'makeCallout', 
            'Callout failed: ' + method + ' ' + endpoint + 
            ' - Duration: ' + duration + 'ms' +
            ' - RequestId: ' + requestId, e);
        
        throw e;
    }
}
```

### Pattern 2: Callout Metrics Tracking

```apex
public class CalloutMetrics {
    
    public static void trackCallout(String integrationName, String endpoint, Integer statusCode, Long duration) {
        // Store metrics in custom object or Platform Event
        Callout_Metric__c metric = new Callout_Metric__c(
            Integration_Name__c = integrationName,
            Endpoint__c = endpoint,
            Status_Code__c = statusCode,
            Duration_ms__c = duration,
            Timestamp__c = Datetime.now()
        );
        
        insert metric;
    }
}
```

### Pattern 3: Alerting on Failures

```apex
public static void checkCalloutHealth(String integrationName) {
    // Query recent failures
    Integer failureCount = [
        SELECT COUNT() 
        FROM Callout_Metric__c 
        WHERE Integration_Name__c = :integrationName
        AND Status_Code__c >= 500
        AND Timestamp__c >= :Datetime.now().addHours(-1)
    ];
    
    if (failureCount > 10) {
        // Send alert via Platform Event or notification
        sendAlert('High failure rate detected for: ' + integrationName);
    }
}
```

### Monitoring Best Practices

- **Log all callouts**: Success and failure cases
- **Track performance metrics**: Duration, status codes, response sizes
- **Monitor failure rates**: Alert on high failure rates
- **Track circuit breaker state**: Monitor when circuits open/close
- **Correlate requests**: Use request IDs for tracing
- **Set up dashboards**: Visualize callout health and performance

**Related Patterns**: <a href="{{ '/rag/integrations/observability/monitoring-alerting.html' | relative_url }}">Monitoring and Alerting</a>

## Avoid DML Before Callout

Salesforce does not allow DML operations before callouts in the same transaction. Use asynchronous patterns to separate DML and callouts.

### The Restriction

```apex
// This will FAIL
insert contact;
HttpResponse response = RestIntegrationService.post('/api/sync', payload);
// Error: You have uncommitted work pending. Please commit or rollback before calling out
```

### Solution 1: Use Queueable

```apex
// DML in synchronous context
insert contact;

// Enqueue callout in separate transaction
System.enqueueJob(new CalloutQueueable(contact.Id, '/api/sync', payload));
```

### Solution 2: Use @future

```apex
// DML in synchronous context
insert contact;

// Callout in separate transaction
makeAsyncCallout('/api/sync', JSON.serialize(payload));
```

### Solution 3: Reverse Order (Callout First)

```apex
// Make callout first
HttpResponse response = RestIntegrationService.post('/api/sync', payload);

// Then perform DML
insert contact;
```

### Best Practice

**Always use Queueable or @future** when you need both DML and callouts. This ensures:
- Separate transaction contexts
- Fresh governor limits
- Proper error handling
- Better user experience (non-blocking)

**Related Patterns**: <a href="{{ '/rag/integrations/development/asynchronous-apex-patterns.html' | relative_url }}">Asynchronous Apex Patterns</a>

## Testing Callout Best Practices

Always implement comprehensive test coverage for your callouts with proper mocking.

### Pattern 1: HTTP Callout Mock

```apex
@isTest
private class IntegrationServiceTest {
    
    @isTest
    static void testSuccessfulCallout() {
        Test.setMock(HttpCalloutMock.class, new MockHttpResponseGenerator());
        
        Test.startTest();
        HttpResponse response = RestIntegrationService.get('/api/test');
        Test.stopTest();
        
        System.assertEquals(200, response.getStatusCode(), 'Should return 200');
        System.assert(response.getBody().contains('success'), 'Should contain success');
    }
    
    @isTest
    static void testErrorCallout() {
        Test.setMock(HttpCalloutMock.class, new MockHttpErrorGenerator());
        
        Test.startTest();
        try {
            RestIntegrationService.get('/api/test');
            System.assert(false, 'Should throw exception');
        } catch (RestIntegrationService.IntegrationException e) {
            System.assert(e.getMessage().contains('Callout failed'), 'Should throw integration error');
        }
        Test.stopTest();
    }
    
    // Mock HTTP response generator
    private class MockHttpResponseGenerator implements HttpCalloutMock {
        public HTTPResponse respond(HTTPRequest req) {
            HttpResponse res = new HttpResponse();
            res.setStatusCode(200);
            res.setBody('{"success": true, "data": {"id": "123"}}');
            res.setHeader('Content-Type', 'application/json');
            return res;
        }
    }
    
    private class MockHttpErrorGenerator implements HttpCalloutMock {
        public HTTPResponse respond(HTTPRequest req) {
            HttpResponse res = new HttpResponse();
            res.setStatusCode(500);
            res.setBody('{"error": "Internal server error"}');
            return res;
        }
    }
}
```

### Pattern 2: Test Multiple Scenarios

```apex
@isTest
private class ComprehensiveCalloutTest {
    
    @isTest
    static void testTimeoutScenario() {
        Test.setMock(HttpCalloutMock.class, new MockTimeoutGenerator());
        
        Test.startTest();
        try {
            RestIntegrationService.get('/api/slow');
            System.assert(false, 'Should throw timeout exception');
        } catch (Exception e) {
            System.assert(e.getMessage().contains('timeout'), 'Should handle timeout');
        }
        Test.stopTest();
    }
    
    @isTest
    static void testRetryLogic() {
        Test.setMock(HttpCalloutMock.class, new MockRetryGenerator());
        
        Test.startTest();
        HttpResponse response = ResilientIntegrationService.makeCalloutWithRetry(
            '/api/unstable', 'GET', null
        );
        Test.stopTest();
        
        System.assertEquals(200, response.getStatusCode(), 'Should succeed after retry');
    }
    
    @isTest
    static void testCircuitBreaker() {
        // Test circuit opening after threshold
        for (Integer i = 0; i < 5; i++) {
            Test.setMock(HttpCalloutMock.class, new MockErrorGenerator());
            try {
                RestIntegrationService.makeCallout('/api/failing', 'GET', null);
            } catch (Exception e) {
                // Expected
            }
        }
        
        // Circuit should now be open
        Test.startTest();
        try {
            RestIntegrationService.makeCallout('/api/failing', 'GET', null);
            System.assert(false, 'Should fail fast when circuit is open');
        } catch (IntegrationException e) {
            System.assert(e.getMessage().contains('Circuit breaker'), 'Should indicate circuit open');
        }
        Test.stopTest();
    }
}
```

### Testing Best Practices

- **Mock all callouts**: Never make real callouts in tests
- **Test success scenarios**: Verify successful callout handling
- **Test error scenarios**: Test timeout, 4xx, 5xx errors
- **Test retry logic**: Verify retry behavior for transient failures
- **Test circuit breaker**: Verify circuit opens/closes correctly
- **Test async patterns**: Test Queueable and @future callouts
- **Achieve 100% coverage**: Cover all code paths

**Related Patterns**: <a href="{{ '/rag/integrations/testing/apex-testing-patterns.html' | relative_url }}">Apex Testing Patterns</a>

## Key Takeaways

Following these best practices will help you build robust, maintainable, and efficient callout solutions:

1. **Always use Named Credentials** for authentication and endpoint management
2. **Understand callout limitations** (10s sync timeout, 100 callouts, 6MB heap, 120s async timeout)
3. **Implement comprehensive error handling** with proper status code checking
4. **Use asynchronous patterns** for non-critical operations and callouts after DML
5. **Consider circuit breaker patterns** for high-volume integrations
6. **Optimize response processing** to avoid heap size limits
7. **Monitor and log** callout performance for troubleshooting
8. **Avoid DML before callout** - use Queueable or @future
9. **Write comprehensive tests** with proper mocking

Remember that callouts are often the most fragile part of your Salesforce integrations. Investing time in proper error handling, monitoring, and testing will save you significant troubleshooting time in production.

## Q&A

### Q: What are the callout timeout limits in Salesforce?

**A**: **Synchronous callouts** have a 10-second timeout and must complete within this window. **Asynchronous callouts** (Queueable, @future, Batch) have a 120-second timeout. Use async patterns for long-running callouts or when you need more time.

### Q: Why should I use Named Credentials for callouts?

**A**: Named Credentials provide **centralized endpoint and authentication management**, support OAuth 2.0 and certificate-based authentication, simplify callout code (no hardcoded URLs), enable credential rotation without code changes, and improve security by avoiding hardcoded credentials.

### Q: Can I perform DML operations before a callout?

**A**: **No, Salesforce does not allow DML operations before callouts** in the same transaction. You'll get an error: "You have uncommitted work pending." Use Queueable or @future to separate DML and callouts into different transactions, or make the callout first, then perform DML.

### Q: How do I handle callout failures and retries?

**A**: Implement retry logic with exponential backoff for transient failures (5xx errors, timeouts), use circuit breaker patterns for high-volume integrations, log all failures for troubleshooting, implement idempotent operations to allow safe retries, and monitor failure rates to detect issues early.

### Q: What is a circuit breaker pattern and when should I use it?

**A**: A **circuit breaker** prevents cascading failures by "opening" the circuit after a threshold of failures, failing fast without attempting callouts. Use for high-volume integrations to protect external systems from overload and prevent retry storms. Implement separate circuits for different external systems.

### Q: How do I test callouts in Apex?

**A**: Use `Test.setMock(HttpCalloutMock.class, mockInstance)` to mock HTTP callouts, create mock classes implementing `HttpCalloutMock`, test success and error scenarios, test retry logic and circuit breakers, and never make real callouts in tests. Achieve 100% code coverage.

### Q: What are the governor limits for callouts?

**A**: **Synchronous**: 100 callouts per transaction, 10-second timeout, 6MB heap size. **Asynchronous**: 120-second timeout, higher limits, separate transaction context. Monitor callout counts using `Limits.getCallouts()` to avoid hitting limits.

### Q: How do I optimize callout response processing?

**A**: Process responses incrementally (don't load entire response into memory), use streaming parsers for large JSON responses, extract only needed fields to reduce memory footprint, clear processed data to free memory, and monitor heap size with `Limits.getHeapSize()`. Batch process large responses.

## Edge Cases and Limitations

### Edge Case 1: Callout Timeout with Critical Operations

**Scenario**: Critical operation requiring callout that may timeout, causing business impact.

**Consideration**:
- Use async patterns for non-critical operations
- Implement timeout handling with fallback logic
- Consider circuit breaker pattern for unreliable systems
- Monitor callout success rates
- Plan for timeout scenarios
- Document timeout handling procedures

### Edge Case 2: Large Response Processing

**Scenario**: External system returning very large responses causing heap size exceptions.

**Consideration**:
- Process responses incrementally
- Use streaming parsers for large JSON
- Extract only needed fields
- Clear processed data to free memory
- Consider pagination if external system supports it
- Monitor heap size usage

### Edge Case 3: Callout Retry with Idempotency

**Scenario**: Retrying failed callouts causing duplicate operations in external system.

**Consideration**:
- Design external APIs to be idempotent
- Use idempotency keys in callout requests
- Implement idempotent retry logic
- Track callout attempts to prevent duplicates
- Test retry scenarios thoroughly
- Document idempotency requirements

### Edge Case 4: Callout Authentication Failures

**Scenario**: OAuth token expiration or authentication failures during long-running operations.

**Consideration**:
- Implement token refresh logic
- Handle authentication errors gracefully
- Monitor token expiration times
- Use Named Credentials for automatic token management
- Implement fallback authentication mechanisms
- Test authentication failure scenarios

### Edge Case 5: Callout Rate Limiting

**Scenario**: External system rate-limiting callouts causing integration failures.

**Consideration**:
- Implement rate limiting and throttling
- Use exponential backoff for retries
- Monitor callout rate limit usage
- Coordinate callouts across integrations
- Consider async processing to spread load
- Document rate limit handling

### Limitations

- **Timeout Limits**: Synchronous callouts have 10-second timeout (120s async)
- **Callout Count Limits**: 100 callouts per synchronous transaction
- **Heap Size Limits**: Response processing limited by 6MB heap size (sync)
- **Authentication Complexity**: OAuth token management adds complexity
- **Error Handling**: External system errors may not be easily handled
- **Rate Limiting**: External systems may rate-limit callouts
- **Network Reliability**: Network issues may cause callout failures

## Related Patterns

**See Also**:
- <a href="{{ '/rag/integrations/etl-vs-api-vs-events.html' | relative_url }}">ETL vs API vs Events</a> - Integration pattern selection
- <a href="{{ '/rag/integrations/development/asynchronous-apex-patterns.html' | relative_url }}">Asynchronous Apex Patterns</a> - Queueable and @future patterns

**Related Domains**:
- <a href="{{ '/rag/integrations/code-examples/apex/integration-examples.html' | relative_url }}">Integration Examples</a> - Complete callout code examples
- <a href="{{ '/rag/integrations/development/error-handling-and-logging.html' | relative_url }}">Error Handling and Logging</a> - Error handling patterns
- <a href="{{ '/rag/integrations/development/governor-limits-and-optimization.html' | relative_url }}">Governor Limits and Optimization</a> - Performance optimization
- <a href="{{ '/rag/integrations/observability/monitoring-alerting.html' | relative_url }}">Monitoring and Alerting</a> - Monitoring patterns

- <a href="{{ '/rag/integrations/code-examples/apex/integration-examples.html' | relative_url }}">Integration Examples</a> - Complete callout code examples
- <a href="{{ '/rag/integrations/development/asynchronous-apex-patterns.html' | relative_url }}">Asynchronous Apex Patterns</a> - Queueable and @future patterns
- <a href="{{ '/rag/integrations/development/error-handling-and-logging.html' | relative_url }}">Error Handling and Logging</a> - Error handling patterns
- <a href="{{ '/rag/integrations/etl-vs-api-vs-events.html' | relative_url }}">ETL vs API vs Events</a> - Integration pattern selection
- <a href="{{ '/rag/integrations/development/governor-limits-and-optimization.html' | relative_url }}">Governor Limits and Optimization</a> - Performance optimization
- <a href="{{ '/rag/integrations/observability/monitoring-alerting.html' | relative_url }}">Monitoring and Alerting</a> - Monitoring patterns

