---
layout: default
title: HTTP Callout Code Examples
description: HTTP callouts enable Salesforce to communicate with external systems via REST or SOAP APIs
permalink: /rag/development/asynchronous-apex-patterns.html' | relative_url }}">Asynchronous Apex Patterns</a> - Async patterns

## Examples

### Example 1: Basic HTTP Callout with Named Credentials

**Pattern**: HTTP callout using Named Credentials
**Use Case**: Making authenticated HTTP requests to external APIs
**Complexity**: Basic
**Related Patterns**: <a href="{{ '/rag/integrations/callout-best-practices.html' | relative_url }}">Callout Best Practices</a>

**Problem**:
You need to make HTTP callouts to an external API using Named Credentials for authentication.

**Solution**:

**Apex** (`HttpCalloutService.cls`):
```apex
/**
 * Service for making HTTP callouts to external systems
 * Uses Named Credentials for authentication
 */
public with sharing class HttpCalloutService {
    
    /**
     * Makes HTTP GET callout
     * @param endpoint Endpoint path (relative to Named Credential)
     * @return HttpResponse
     */
    public static HttpResponse get(String endpoint) {
        return makeCallout(endpoint, 'GET', null, null);
    }
    
    /**
     * Makes HTTP POST callout
     * @param endpoint Endpoint path
     * @param payload Request body
     * @return HttpResponse
     */
    public static HttpResponse post(String endpoint, String payload) {
        return makeCallout(endpoint, 'POST', payload, null);
    }
    
    /**
     * Makes HTTP callout with full control
     * @param endpoint Endpoint path
     * @param method HTTP method
     * @param body Request body (null for GET)
     * @param headers Additional headers (null for default)
     * @return HttpResponse
     */
    public static HttpResponse makeCallout(String endpoint, String method, String body, Map<String, String> headers) {
        HttpRequest req = new HttpRequest();
        
        // Use Named Credential (NO hardcoded URLs)
        req.setEndpoint('callout:ExternalApi' + endpoint);
        req.setMethod(method);
        req.setTimeout(30000); // 30 seconds for sync
        
        // Set default headers
        req.setHeader('Content-Type', 'application/json');
        req.setHeader('Accept', 'application/json');
        
        // Add custom headers if provided
        if (headers != null) {
            for (String key : headers.keySet()) {
                req.setHeader(key, headers.get(key));
            }
        }
        
        // Set body for POST/PUT
        if (String.isNotBlank(body) && (method == 'POST' || method == 'PUT')) {
            req.setBody(body);
        }
        
        Http http = new Http();
        HttpResponse res;
        
        try {
            res = http.send(req);
            
            // Log callout
            LOG_LogMessageUtility.logInfo(
                'HttpCalloutService',
                'makeCallout',
                method + ' ' + endpoint + ' - Status: ' + res.getStatusCode()
            );
            
        } catch (Exception e) {
            LOG_LogMessageUtility.logError(
                'HttpCalloutService',
                'makeCallout',
                'Callout failed: ' + method + ' ' + endpoint + ' - ' + e.getMessage(),
                e
            );
            throw new CalloutException('Callout failed: ' + e.getMessage(), e);
        }
        
        return res;
    }
    
    /**
     * Custom exception for callout errors
     */
    public class CalloutException extends Exception {}
}
```

**Best Practices**:
- Always use Named Credentials for endpoints
- Set appropriate timeouts (30s sync, 120s async)
- Include default headers (Content-Type, Accept)
- Log all callouts for troubleshooting
- Handle exceptions gracefully

### Example 2: Callout with Comprehensive Error Handling

**Pattern**: Comprehensive error handling for HTTP callouts
**Use Case**: Handling various error scenarios gracefully
**Complexity**: Intermediate
**Related Patterns**: <a href="{{ '/rag/integrations/callout-best-practices.html' | relative_url }}">Callout Best Practices</a>

**Problem**:
You need to handle different types of errors (network, timeout, HTTP status codes) appropriately.

**Solution**:

**Apex** (`RobustCalloutService.cls`):
```apex
/**
 * Robust HTTP callout service with comprehensive error handling
 */
public with sharing class RobustCalloutService {
    
    /**
     * Makes HTTP callout with comprehensive error handling
     * @param endpoint Endpoint path
     * @param method HTTP method
     * @param payload Request payload
     * @return CalloutResult with response and status
     */
    public static CalloutResult makeCallout(String endpoint, String method, Map<String, Object> payload) {
        CalloutResult result = new CalloutResult();
        
        try {
            HttpRequest req = buildRequest(endpoint, method, payload);
            Http http = new Http();
            HttpResponse res = http.send(req);
            
            result.statusCode = res.getStatusCode();
            result.responseBody = res.getBody();
            result.isSuccess = false; // Will be set based on status code
            
            // Handle different status codes
            if (result.statusCode >= 200 && result.statusCode < 300) {
                // Success
                result.isSuccess = true;
                result.message = 'Callout successful';
                
            } else if (result.statusCode >= 400 && result.statusCode < 500) {
                // Client error - don't retry
                result.isSuccess = false;
                result.isRetryable = false;
                result.message = 'Client error: ' + result.statusCode + ' - ' + res.getStatus();
                result.errorType = 'CLIENT_ERROR';
                
                LOG_LogMessageUtility.logError(
                    'RobustCalloutService',
                    'makeCallout',
                    result.message + ' - Endpoint: ' + endpoint,
                    null
                );
                
            } else if (result.statusCode >= 500) {
                // Server error - may retry
                result.isSuccess = false;
                result.isRetryable = true;
                result.message = 'Server error: ' + result.statusCode + ' - ' + res.getStatus();
                result.errorType = 'SERVER_ERROR';
                
                LOG_LogMessageUtility.logError(
                    'RobustCalloutService',
                    'makeCallout',
                    result.message + ' - Endpoint: ' + endpoint,
                    null
                );
            }
            
        } catch (CalloutException e) {
            // Network/timeout error - may retry
            result.isSuccess = false;
            result.isRetryable = true;
            result.message = 'Network error: ' + e.getMessage();
            result.errorType = 'NETWORK_ERROR';
            
            LOG_LogMessageUtility.logError(
                'RobustCalloutService',
                'makeCallout',
                result.message + ' - Endpoint: ' + endpoint,
                e
            );
            
        } catch (Exception e) {
            // Unexpected error
            result.isSuccess = false;
            result.isRetryable = false;
            result.message = 'Unexpected error: ' + e.getMessage();
            result.errorType = 'UNEXPECTED_ERROR';
            
            LOG_LogMessageUtility.logError(
                'RobustCalloutService',
                'makeCallout',
                result.message + ' - Endpoint: ' + endpoint,
                e
            );
        }
        
        return result;
    }
    
    /**
     * Builds HTTP request
     * @param endpoint Endpoint path
     * @param method HTTP method
     * @param payload Request payload
     * @return HttpRequest
     */
    private static HttpRequest buildRequest(String endpoint, String method, Map<String, Object> payload) {
        HttpRequest req = new HttpRequest();
        req.setEndpoint('callout:ExternalApi' + endpoint);
        req.setMethod(method);
        req.setHeader('Content-Type', 'application/json');
        req.setTimeout(30000);
        
        if (payload != null && (method == 'POST' || method == 'PUT')) {
            req.setBody(JSON.serialize(payload));
        }
        
        return req;
    }
    
    /**
     * Result class for callout operations
     */
    public class CalloutResult {
        public Boolean isSuccess { get; set; }
        public Boolean isRetryable { get; set; }
        public Integer statusCode { get; set; }
        public String responseBody { get; set; }
        public String message { get; set; }
        public String errorType { get; set; }
        
        public CalloutResult() {
            this.isRetryable = false;
        }
    }
}
```

**Best Practices**:
- Check status codes and handle appropriately
- Distinguish between retryable and non-retryable errors
- Log all errors with context
- Return structured results for callers

### Example 3: Asynchronous Callout with Queueable

**Pattern**: Making callouts asynchronously using Queueable
**Use Case**: Long-running or high-volume callouts
**Complexity**: Intermediate
**Related Patterns**: <a href="{{ '/rag/development/asynchronous-apex-patterns.html' | relative_url }}">Asynchronous Apex Patterns</a>

**Problem**:
You need to make HTTP callouts asynchronously to avoid timeout issues.

**Solution**:

**Apex** (`AsyncCalloutService.cls`):
```apex
/**
 * Asynchronous HTTP callout service using Queueable
 */
public with sharing class AsyncCalloutService implements Queueable, Database.AllowsCallouts {
    
    private String endpoint;
    private String method;
    private Map<String, Object> payload;
    private Id recordId;
    private Integer retryCount;
    
    public AsyncCalloutService(String endpoint, String method, Map<String, Object> payload, Id recordId) {
        this.endpoint = endpoint;
        this.method = method;
        this.payload = payload;
        this.recordId = recordId;
        this.retryCount = 0;
    }
    
    public void execute(QueueableContext context) {
        try {
            // Make callout
            RobustCalloutService.CalloutResult result = RobustCalloutService.makeCallout(
                endpoint, method, payload
            );
            
            if (result.isSuccess) {
                // Process successful response
                processSuccessResponse(result);
                
            } else if (result.isRetryable && retryCount < 3) {
                // Retry callout
                retryCallout();
                
            } else {
                // Mark as failed after max retries
                markAsFailed(result.message);
            }
            
        } catch (Exception e) {
            LOG_LogMessageUtility.logError(
                'AsyncCalloutService',
                'execute',
                'Async callout failed: ' + endpoint + ' - ' + e.getMessage(),
                e
            );
            markAsFailed(e.getMessage());
        }
    }
    
    /**
     * Retries callout with exponential backoff
     */
    private void retryCallout() {
        retryCount++;
        Integer waitTime = (Integer) Math.pow(2, retryCount) * 1000; // Exponential backoff
        
        // Enqueue new job after wait time
        AsyncCalloutService retryJob = new AsyncCalloutService(endpoint, method, payload, recordId);
        retryJob.retryCount = retryCount;
        
        // Note: Actual wait would require Scheduled Apex or Platform Events
        // This is a simplified example
        System.enqueueJob(retryJob);
    }
    
    /**
     * Processes successful response
     * @param result Callout result
     */
    private void processSuccessResponse(RobustCalloutService.CalloutResult result) {
        // Update record with response
        // Implementation depends on use case
        LOG_LogMessageUtility.logInfo(
            'AsyncCalloutService',
            'processSuccessResponse',
            'Callout successful: ' + endpoint
        );
    }
    
    /**
     * Marks record as failed
     * @param errorMessage Error message
     */
    private void markAsFailed(String errorMessage) {
        // Mark record as failed
        // Implementation depends on use case
        LOG_LogMessageUtility.logError(
            'AsyncCalloutService',
            'markAsFailed',
            'Callout failed after retries: ' + endpoint + ' - ' + errorMessage,
            null
        );
    }
}
```

**Usage**:
```apex
// Enqueue async callout
Map<String, Object> payload = new Map<String, Object>{
    'recordId' => contact.Id,
    'action' => 'sync'
};
System.enqueueJob(new AsyncCalloutService('/api/sync', 'POST', payload, contact.Id));
```

**Best Practices**:
- Use Queueable for async callouts
- Implement retry logic with exponential backoff
- Set longer timeouts (120 seconds) for async
- Handle errors and update records accordingly

### Example 4: Circuit Breaker Pattern

**Pattern**: Circuit breaker for high-volume integrations
**Use Case**: Preventing cascading failures in high-volume scenarios
**Complexity**: Advanced
**Related Patterns**: <a href="{{ '/rag/integrations/callout-best-practices.html' | relative_url }}">Callout Best Practices</a>

**Problem**:
You need to prevent callouts when an external system is down to avoid wasting resources.

**Solution**:

**Apex** (`CircuitBreakerService.cls`):
```apex
/**
 * Circuit breaker service for HTTP callouts
 * Prevents callouts when external system is down
 */
public with sharing class CircuitBreakerService {
    
    private static final String CIRCUIT_BREAKER_SETTING = 'ExternalApi_CircuitBreaker';
    private static final Integer FAILURE_THRESHOLD = 5;
    private static final Integer TIMEOUT_SECONDS = 300; // 5 minutes
    
    /**
     * Checks if circuit is open (system is down)
     * @return True if circuit is open
     */
    public static Boolean isCircuitOpen() {
        CircuitBreakerSetting__c setting = CircuitBreakerSetting__c.getInstance(CIRCUIT_BREAKER_SETTING);
        
        if (setting == null) {
            return false; // Circuit closed by default
        }
        
        // Check if timeout has passed
        if (setting.Last_Failure_Time__c != null) {
            Integer secondsSinceFailure = (Integer) ((DateTime.now().getTime() - setting.Last_Failure_Time__c.getTime()) / 1000);
            
            if (secondsSinceFailure > TIMEOUT_SECONDS) {
                // Timeout passed, reset circuit
                resetCircuit();
                return false;
            }
        }
        
        // Circuit is open if failure count exceeds threshold
        return setting.Failure_Count__c >= FAILURE_THRESHOLD;
    }
    
    /**
     * Records successful callout
     */
    public static void recordSuccess() {
        resetCircuit();
    }
    
    /**
     * Records failed callout
     */
    public static void recordFailure() {
        CircuitBreakerSetting__c setting = CircuitBreakerSetting__c.getInstance(CIRCUIT_BREAKER_SETTING);
        
        if (setting == null) {
            setting = new CircuitBreakerSetting__c();
            setting.Name = CIRCUIT_BREAKER_SETTING;
            setting.Failure_Count__c = 0;
        }
        
        setting.Failure_Count__c = (setting.Failure_Count__c == null ? 0 : setting.Failure_Count__c) + 1;
        setting.Last_Failure_Time__c = DateTime.now();
        
        upsert setting;
        
        LOG_LogMessageUtility.logWarning(
            'CircuitBreakerService',
            'recordFailure',
            'Circuit breaker failure count: ' + setting.Failure_Count__c
        );
    }
    
    /**
     * Resets circuit breaker
     */
    private static void resetCircuit() {
        CircuitBreakerSetting__c setting = CircuitBreakerSetting__c.getInstance(CIRCUIT_BREAKER_SETTING);
        
        if (setting != null) {
            setting.Failure_Count__c = 0;
            setting.Last_Failure_Time__c = null;
            update setting;
        }
    }
    
    /**
     * Makes callout with circuit breaker protection
     * @param endpoint Endpoint path
     * @param method HTTP method
     * @param payload Request payload
     * @return CalloutResult
     */
    public static RobustCalloutService.CalloutResult makeCalloutWithCircuitBreaker(
        String endpoint, String method, Map<String, Object> payload
    ) {
        // Check if circuit is open
        if (isCircuitOpen()) {
            RobustCalloutService.CalloutResult result = new RobustCalloutService.CalloutResult();
            result.isSuccess = false;
            result.isRetryable = false;
            result.message = 'Circuit breaker is open - external system appears to be down';
            result.errorType = 'CIRCUIT_OPEN';
            
            LOG_LogMessageUtility.logWarning(
                'CircuitBreakerService',
                'makeCalloutWithCircuitBreaker',
                'Callout blocked - circuit breaker is open'
            );
            
            return result;
        }
        
        // Make callout
        RobustCalloutService.CalloutResult result = RobustCalloutService.makeCallout(endpoint, method, payload);
        
        // Record result
        if (result.isSuccess) {
            recordSuccess();
        } else {
            recordFailure();
        }
        
        return result;
    }
}
```

**Custom Setting** (`CircuitBreakerSetting__c`):
- **API Name**: `CircuitBreakerSetting__c`
- **Fields**:
  - `Failure_Count__c` (Number) - Count of consecutive failures
  - `Last_Failure_Time__c` (DateTime) - Time of last failure

**Best Practices**:
- Use Custom Settings for circuit breaker state
- Set appropriate failure threshold
- Implement timeout to reset circuit
- Log circuit breaker state changes

## Related Examples

- <a href="{{ '/rag/development/error-handling-and-logging.html' | relative_url }}">Error Handling and Logging</a> - Error handling patterns
