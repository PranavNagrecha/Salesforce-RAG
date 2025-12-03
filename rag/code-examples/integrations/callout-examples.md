# HTTP Callout Code Examples

> This file contains complete, working code examples for HTTP callout patterns in Salesforce.
> All examples follow Salesforce callout best practices.

## Overview

HTTP callouts enable Salesforce to communicate with external systems via REST or SOAP APIs. These examples demonstrate authentication, error handling, retry logic, and response processing.

**Related Patterns**:
- [Callout Best Practices](../integrations/callout-best-practices.md) - Complete callout best practices
- [Asynchronous Apex Patterns](../development/asynchronous-apex-patterns.md) - Async patterns for callouts

## Examples

### Example 1: Basic REST Callout

**Pattern**: Simple REST API callout with Named Credential
**Use Case**: Calling external REST APIs
**Complexity**: Basic
**Related Patterns**: [Callout Best Practices](../integrations/callout-best-practices.md)

**Problem**:
You need to make a simple REST API call to an external system.

**Solution**:

**Apex** (`ExternalApiService.cls`):
```apex
public with sharing class ExternalApiService {
    
    /**
     * Makes REST callout to external API
     * @param endpoint Endpoint path (relative to Named Credential)
     * @param method HTTP method (GET, POST, etc.)
     * @param body Request body (optional)
     * @return HttpResponse response
     */
    public static HttpResponse makeCallout(String endpoint, String method, String body) {
        HttpRequest req = new HttpRequest();
        req.setEndpoint('callout:ExternalApi/' + endpoint);
        req.setMethod(method);
        req.setHeader('Content-Type', 'application/json');
        req.setTimeout(12000);
        
        if (String.isNotBlank(body)) {
            req.setBody(body);
        }
        
        Http http = new Http();
        HttpResponse res = http.send(req);
        
        return res;
    }
}
```

**Best Practices**:
- Use Named Credentials for endpoint and authentication
- Set appropriate timeout (default 10s, max 120s)
- Set Content-Type header
- Handle response status codes

### Example 2: Callout with Error Handling and Retry

**Pattern**: Callout with retry logic for transient failures
**Use Case**: Handling network errors and retries
**Complexity**: Intermediate
**Related Patterns**: [Callout Best Practices](../integrations/callout-best-practices.md), [Error Handling](../development/error-handling-and-logging.md)

**Problem**:
You need to make a callout with retry logic for transient failures.

**Solution**:

**Apex** (`RetryableCalloutService.cls`):
```apex
public with sharing class RetryableCalloutService {
    
    private static final Integer MAX_RETRIES = 3;
    private static final Integer RETRY_DELAY_MS = 1000;
    
    /**
     * Makes callout with retry logic
     * @param endpoint Endpoint path
     * @param method HTTP method
     * @param body Request body
     * @return HttpResponse response
     */
    public static HttpResponse makeCalloutWithRetry(String endpoint, String method, String body) {
        Integer attempt = 0;
        Exception lastException;
        
        while (attempt < MAX_RETRIES) {
            try {
                HttpRequest req = new HttpRequest();
                req.setEndpoint('callout:ExternalApi/' + endpoint);
                req.setMethod(method);
                req.setHeader('Content-Type', 'application/json');
                req.setTimeout(12000);
                
                if (String.isNotBlank(body)) {
                    req.setBody(body);
                }
                
                Http http = new Http();
                HttpResponse res = http.send(req);
                
                // Retry on 5xx errors
                if (res.getStatusCode() >= 500 && res.getStatusCode() < 600 && attempt < MAX_RETRIES - 1) {
                    attempt++;
                    Long delay = RETRY_DELAY_MS * attempt; // Exponential backoff
                    System.debug('Retrying callout after ' + delay + 'ms. Attempt: ' + attempt);
                    continue;
                }
                
                return res;
                
            } catch (CalloutException e) {
                lastException = e;
                attempt++;
                
                if (attempt < MAX_RETRIES) {
                    Long delay = RETRY_DELAY_MS * attempt;
                    System.debug('Callout exception, retrying after ' + delay + 'ms. Attempt: ' + attempt);
                }
            }
        }
        
        // All retries failed
        throw new CalloutException('Callout failed after ' + MAX_RETRIES + ' attempts: ' + 
            (lastException != null ? lastException.getMessage() : 'Unknown error'));
    }
}
```

**Best Practices**:
- Implement retry logic for transient failures (5xx errors, network timeouts)
- Use exponential backoff for retry delays
- Limit retry attempts to avoid governor limits
- Log retry attempts for troubleshooting

### Example 3: Async Callout with Queueable

**Pattern**: Making callouts asynchronously to avoid timeout issues
**Use Case**: Long-running callouts or high-volume scenarios
**Complexity**: Advanced
**Related Patterns**: [Asynchronous Apex Patterns](../development/asynchronous-apex-patterns.md), [Callout Best Practices](../integrations/callout-best-practices.md)

**Problem**:
You need to make callouts asynchronously to avoid timeout issues or governor limits.

**Solution**:

**Apex** (`AsyncCalloutQueueable.cls`):
```apex
public class AsyncCalloutQueueable implements Queueable, Database.AllowsCallouts {
    
    private String endpoint;
    private String method;
    private String body;
    
    public AsyncCalloutQueueable(String endpoint, String method, String body) {
        this.endpoint = endpoint;
        this.method = method;
        this.body = body;
    }
    
    public void execute(QueueableContext context) {
        try {
            HttpRequest req = new HttpRequest();
            req.setEndpoint('callout:ExternalApi/' + endpoint);
            req.setMethod(method);
            req.setHeader('Content-Type', 'application/json');
            req.setTimeout(120000); // 120 seconds in async context
            
            if (String.isNotBlank(body)) {
                req.setBody(body);
            }
            
            Http http = new Http();
            HttpResponse res = http.send(req);
            
            // Process response
            if (res.getStatusCode() == 200) {
                System.debug('Callout successful: ' + res.getBody());
                // Update records, log success, etc.
            } else {
                System.debug('Callout failed with status: ' + res.getStatusCode());
                // Log error, handle failure
            }
            
        } catch (Exception e) {
            System.debug('Callout exception: ' + e.getMessage());
            // Log error
        }
    }
}
```

**Usage**:
```apex
// Enqueue async callout
AsyncCalloutQueueable job = new AsyncCalloutQueueable('/api/data', 'POST', jsonBody);
System.enqueueJob(job);
```

**Best Practices**:
- Use `Database.AllowsCallouts` interface for async callouts
- Longer timeout available in async context (120s)
- Handle errors gracefully
- Consider chaining Queueable jobs for multiple callouts

## Related Examples

- [Platform Events Examples](integrations/platform-events-examples.md) - Event-driven integration patterns
- [Bulk API Examples](integrations/bulk-api-examples.md) - Bulk data operations

## See Also

- [Callout Best Practices](../integrations/callout-best-practices.md) - Complete callout best practices
- [Asynchronous Apex Patterns](../development/asynchronous-apex-patterns.md) - Async patterns for callouts
- [Error Handling and Logging](../development/error-handling-and-logging.md) - Error handling patterns

