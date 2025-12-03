---
layout: default
title: Integration Layer Code Examples
description: The Integration Layer handles external API callouts, data transformation, authentication, and error handling
permalink: /rag/code-examples/apex/integration-examples.html
---

# Integration Layer Code Examples

> This file contains complete, working code examples for Apex Integration Layer patterns.  
> All examples are copy-paste ready and follow Salesforce best practices.

## Overview

The Integration Layer handles external API callouts, data transformation, authentication, and error handling. It should NOT contain business logic or SOQL queries.

**Related Patterns**:
- <a href="{{ '/rag/code-examples/apex/Salesforce-RAG/rag/development/apex-patterns.html#apex-class-layering.html' | relative_url }}">Apex Class Layering</a>
- <a href="{{ '/rag/code-examples/apex/Salesforce-RAG/rag/development/apex-patterns.html#integration-layer.html' | relative_url }}">Integration Layer Pattern</a>

## Examples

### Example 1: REST API Callout with Named Credentials
**Pattern**: Integration Layer with Named Credentials  
**Use Case**: Outbound REST API callout  
**Complexity**: Basic  
**Related Patterns**: <a href="{{ '/rag/code-examples/apex/Salesforce-RAG/rag/development/apex-patterns.html#integration-layer.html' | relative_url }}">Integration Layer</a>

**Problem**: 
You need to make HTTP callouts to external systems using Named Credentials for authentication.

**Solution**:
```apex
/**
 * Integration service for REST API callouts
 * Uses Named Credentials for authentication
 */
public with sharing class RestIntegrationService {
    
    /**
     * Makes HTTP callout to external system
     * @param endpoint Endpoint path (relative to Named Credential)
     * @param method HTTP method (GET, POST, PUT, DELETE)
     * @param payload Request payload (null for GET)
     * @return HttpResponse from external system
     */
    public static HttpResponse makeCallout(String endpoint, String method, Map<String, Object> payload) {
        HttpRequest req = new HttpRequest();
        
        // Use Named Credential (NO hardcoded URLs)
        req.setEndpoint('callout:MyNamedCredential' + endpoint);
        req.setMethod(method);
        req.setHeader('Content-Type', 'application/json');
        req.setTimeout(30000); // 30 seconds
        
        // Add payload for POST/PUT
        if (payload != null && (method == 'POST' || method == 'PUT')) {
            req.setBody(JSON.serialize(payload));
        }
        
        Http http = new Http();
        HttpResponse res;
        
        try {
            res = http.send(req);
            
            // Log success
            LOG_LogMessageUtility.logInfo(
                'RestIntegrationService',
                'makeCallout',
                'Callout successful: ' + method + ' ' + endpoint + ' - Status: ' + res.getStatusCode()
            );
            
        } catch (Exception e) {
            // Log error
            LOG_LogMessageUtility.logError(
                'RestIntegrationService',
                'makeCallout',
                'Callout failed: ' + method + ' ' + endpoint + ' - ' + e.getMessage(),
                e
            );
            throw new IntegrationException('Callout failed: ' + e.getMessage(), e);
        }
        
        return res;
    }
    
    /**
     * Makes GET callout
     * @param endpoint Endpoint path
     * @return HttpResponse
     */
    public static HttpResponse get(String endpoint) {
        return makeCallout(endpoint, 'GET', null);
    }
    
    /**
     * Makes POST callout
     * @param endpoint Endpoint path
     * @param payload Request payload
     * @return HttpResponse
     */
    public static HttpResponse post(String endpoint, Map<String, Object> payload) {
        return makeCallout(endpoint, 'POST', payload);
    }
    
    /**
     * Custom exception for integration errors
     */
    public class IntegrationException extends Exception {}
}
```

**Explanation**:
- **Named Credentials**: Uses `callout:MyNamedCredential` (no hardcoded URLs)
- **Error Handling**: Wraps callout in try-catch with logging
- **Timeout**: Sets appropriate timeout (30 seconds)
- **Logging**: Logs both success and errors
- **Reusability**: Provides GET, POST methods

**Usage**:
```apex
// GET request
HttpResponse response = RestIntegrationService.get('/api/contacts');

// POST request
Map<String, Object> payload = new Map<String, Object>{
    'name' => 'Test',
    'email' => 'test@example.com'
};
HttpResponse response = RestIntegrationService.post('/api/contacts', payload);
```

**Test Example**:
```apex
@isTest
private class RestIntegrationServiceTest {
    
    @isTest
    static void testMakeCallout_Success() {
        Test.setMock(HttpCalloutMock.class, new MockHttpResponseGenerator());
        
        Test.startTest();
        HttpResponse response = RestIntegrationService.get('/api/test');
        Test.stopTest();
        
        System.assertEquals(200, response.getStatusCode(), 'Should return 200');
    }
    
    @isTest
    static void testMakeCallout_Error() {
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
            res.setBody('{"success": true}');
            return res;
        }
    }
    
    private class MockHttpErrorGenerator implements HttpCalloutMock {
        public HTTPResponse respond(HTTPRequest req) {
            throw new CalloutException('Connection timeout');
        }
    }
}
```

---

### Example 2: Integration with Retry Logic
**Pattern**: Integration Layer with Retry and Error Handling  
**Use Case**: Resilient external API integration  
**Complexity**: Intermediate

**Problem**: 
You need to handle transient failures in external API callouts with retry logic.

**Solution**:
```apex
/**
 * Integration service with retry logic
 */
public with sharing class ResilientIntegrationService {
    
    private static final Integer MAX_RETRIES = 3;
    private static final Integer RETRY_DELAY_MS = 1000;
    
    /**
     * Makes callout with retry logic
     * @param endpoint Endpoint path
     * @param method HTTP method
     * @param payload Request payload
     * @return HttpResponse
     */
    public static HttpResponse makeCalloutWithRetry(
        String endpoint, 
        String method, 
        Map<String, Object> payload
    ) {
        Integer retryCount = 0;
        Exception lastException;
        
        while (retryCount < MAX_RETRIES) {
            try {
                return RestIntegrationService.makeCallout(endpoint, method, payload);
                
            } catch (RestIntegrationService.IntegrationException e) {
                lastException = e;
                retryCount++;
                
                // Check if error is retryable (e.g., timeout, 5xx errors)
                if (isRetryableError(e) && retryCount < MAX_RETRIES) {
                    LOG_LogMessageUtility.logInfo(
                        'ResilientIntegrationService',
                        'makeCalloutWithRetry',
                        'Retry attempt ' + retryCount + ' for ' + endpoint
                    );
                    // Note: Cannot use Thread.sleep in Apex, use Queueable for delays
                    continue;
                } else {
                    throw e;
                }
            }
        }
        
        // All retries exhausted
        throw new IntegrationException(
            'Callout failed after ' + MAX_RETRIES + ' retries: ' + lastException.getMessage(),
            lastException
        );
    }
    
    /**
     * Determines if error is retryable
     * @param e Exception to check
     * @return true if error is retryable
     */
    private static Boolean isRetryableError(Exception e) {
        String message = e.getMessage();
        // Retry on timeouts, connection errors, 5xx server errors
        return message.contains('timeout') || 
               message.contains('Connection') ||
               message.contains('500') ||
               message.contains('502') ||
               message.contains('503');
    }
    
    public class IntegrationException extends Exception {}
}
```

**Best Practices**:
- Retry only on transient errors (timeouts, 5xx)
- Don't retry on 4xx errors (client errors)
- Use Queueable for retry delays (can't use Thread.sleep)
- Log retry attempts for monitoring

---

### Example 3: Response Transformation
**Pattern**: Integration Layer with Data Transformation  
**Use Case**: Transforming external API responses  
**Complexity**: Intermediate

**Problem**: 
You need to transform external API responses into Salesforce-friendly format.

**Solution**:
```apex
/**
 * Integration service with response transformation
 */
public with sharing class TransformationIntegrationService {
    
    /**
     * Syncs Contact to external system and transforms response
     * @param contact Contact record to sync
     * @return Transformed response data
     */
    public static Map<String, Object> syncContact(Contact contact) {
        // Prepare payload
        Map<String, Object> payload = new Map<String, Object>{
            'firstName' => contact.FirstName,
            'lastName' => contact.LastName,
            'email' => contact.Email,
            'phone' => contact.Phone
        };
        
        // Make callout
        HttpResponse response = RestIntegrationService.post('/api/contacts', payload);
        
        // Transform response
        if (response.getStatusCode() == 200 || response.getStatusCode() == 201) {
            Map<String, Object> responseData = (Map<String, Object>)JSON.deserializeUntyped(response.getBody());
            return transformResponse(responseData);
        } else {
            throw new IntegrationException('Sync failed with status: ' + response.getStatusCode());
        }
    }
    
    /**
     * Transforms external API response to Salesforce format
     * @param responseData External API response
     * @return Transformed data
     */
    private static Map<String, Object> transformResponse(Map<String, Object> responseData) {
        Map<String, Object> transformed = new Map<String, Object>();
        
        // Map external fields to Salesforce fields
        transformed.put('externalId', responseData.get('id'));
        transformed.put('syncStatus', 'Success');
        transformed.put('syncTimestamp', Datetime.now());
        
        return transformed;
    }
    
    public class IntegrationException extends Exception {}
}
```

---

## Common Patterns

### Pattern 1: Named Credentials
```apex
req.setEndpoint('callout:MyNamedCredential' + endpoint);
// NO hardcoded URLs
```

### Pattern 2: Error Handling
```apex
try {
    res = http.send(req);
} catch (Exception e) {
    LOG_LogMessageUtility.logError(...);
    throw new IntegrationException(...);
}
```

### Pattern 3: Response Parsing
```apex
Map<String, Object> responseData = (Map<String, Object>)JSON.deserializeUntyped(response.getBody());
```

---

## Best Practices

1. **Use Named Credentials** for endpoints (NO hardcoded URLs)
2. **Centralize error handling** and retry logic
3. **Log all callouts** (success and errors)
4. **Set appropriate timeouts** (30 seconds default)
5. **Transform responses** to Salesforce-friendly format
6. **Handle HTTP status codes** appropriately
7. **Should NOT contain business logic** (delegate to Service layer)
8. **Should NOT contain SOQL queries** (delegate to Selector layer)
9. **Use @future or Queueable** for callouts after DML
10. **Implement retry logic** for transient failures

---

## Related Patterns

- <a href="{{ '/rag/code-examples/apex/code-examples/apex/service-layer-examples.html' | relative_url }}">Service Layer Examples</a> - Service layer patterns
- <a href="{{ '/rag/integrations.html' | relative_url }}">Integration Patterns</a> - Integration architecture patterns
- <a href="{{ '/rag/development/error-handling-and-logging.html' | relative_url }}">Error Handling</a> - Error handling patterns

