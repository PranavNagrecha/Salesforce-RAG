---
layout: default
title: REST API Code Examples
description: REST API integrations enable real-time, synchronous communication between Salesforce and external systems
permalink: /rag/code-examples/integrations/rest-api-examples.html
---

# REST API Code Examples

> This file contains complete, working code examples for REST API integration patterns.
> All examples are copy-paste ready and follow Salesforce best practices.

## Overview

REST API integrations enable real-time, synchronous communication between Salesforce and external systems. These examples demonstrate common REST API patterns including outbound callouts, inbound REST services, authentication, error handling, and response processing.

**Related Patterns**:
- <a href="{{ '/rag/integrations/callout-best-practices.html' | relative_url }}">Callout Best Practices</a> - Comprehensive callout best practices
- <a href="{{ '/rag/integrations/integration-platform-patterns.html' | relative_url }}">Integration Platform Patterns</a> - Integration platform patterns
- <a href="{{ '/rag/code-examples/integrations/code-examples/apex/integration-examples.html' | relative_url }}">Integration Examples</a> - Apex integration layer examples

## Examples

### Example 1: Outbound REST API Callout with Named Credentials

**Pattern**: REST API callout using Named Credentials
**Use Case**: Calling external REST APIs from Salesforce
**Complexity**: Basic
**Related Patterns**: <a href="{{ '/rag/integrations/callout-best-practices.html' | relative_url }}">Callout Best Practices</a>

**Problem**:
You need to make HTTP callouts to an external REST API using Named Credentials for authentication.

**Solution**:

**Apex** (`RestApiService.cls`):
```apex
/**
 * Service for making REST API callouts to external systems
 * Uses Named Credentials for authentication
 */
public with sharing class RestApiService {
    
    /**
     * Makes HTTP GET callout
     * @param endpoint Endpoint path (relative to Named Credential)
     * @return Response data as Map
     */
    public static Map<String, Object> get(String endpoint) {
        HttpRequest req = new HttpRequest();
        req.setEndpoint('callout:ExternalApi' + endpoint);
        req.setMethod('GET');
        req.setHeader('Content-Type', 'application/json');
        req.setTimeout(30000); // 30 seconds
        
        Http http = new Http();
        HttpResponse res = http.send(req);
        
        return handleResponse(res, 'GET', endpoint);
    }
    
    /**
     * Makes HTTP POST callout
     * @param endpoint Endpoint path
     * @param payload Request payload
     * @return Response data as Map
     */
    public static Map<String, Object> post(String endpoint, Map<String, Object> payload) {
        HttpRequest req = new HttpRequest();
        req.setEndpoint('callout:ExternalApi' + endpoint);
        req.setMethod('POST');
        req.setHeader('Content-Type', 'application/json');
        req.setBody(JSON.serialize(payload));
        req.setTimeout(30000);
        
        Http http = new Http();
        HttpResponse res = http.send(req);
        
        return handleResponse(res, 'POST', endpoint);
    }
    
    /**
     * Makes HTTP PUT callout
     * @param endpoint Endpoint path
     * @param payload Request payload
     * @return Response data as Map
     */
    public static Map<String, Object> put(String endpoint, Map<String, Object> payload) {
        HttpRequest req = new HttpRequest();
        req.setEndpoint('callout:ExternalApi' + endpoint);
        req.setMethod('PUT');
        req.setHeader('Content-Type', 'application/json');
        req.setBody(JSON.serialize(payload));
        req.setTimeout(30000);
        
        Http http = new Http();
        HttpResponse res = http.send(req);
        
        return handleResponse(res, 'PUT', endpoint);
    }
    
    /**
     * Makes HTTP DELETE callout
     * @param endpoint Endpoint path
     * @return Response data as Map
     */
    public static Map<String, Object> delete(String endpoint) {
        HttpRequest req = new HttpRequest();
        req.setEndpoint('callout:ExternalApi' + endpoint);
        req.setMethod('DELETE');
        req.setHeader('Content-Type', 'application/json');
        req.setTimeout(30000);
        
        Http http = new Http();
        HttpResponse res = http.send(req);
        
        return handleResponse(res, 'DELETE', endpoint);
    }
    
    /**
     * Handles HTTP response with error checking
     * @param res HttpResponse
     * @param method HTTP method
     * @param endpoint Endpoint path
     * @return Response data as Map
     */
    private static Map<String, Object> handleResponse(HttpResponse res, String method, String endpoint) {
        Integer statusCode = res.getStatusCode();
        
        if (statusCode >= 200 && statusCode < 300) {
            // Success
            LOG_LogMessageUtility.logInfo(
                'RestApiService',
                method,
                'Callout successful: ' + method + ' ' + endpoint + ' - Status: ' + statusCode
            );
            
            if (String.isNotBlank(res.getBody())) {
                return (Map<String, Object>) JSON.deserializeUntyped(res.getBody());
            }
            return new Map<String, Object>();
            
        } else if (statusCode >= 400 && statusCode < 500) {
            // Client error - don't retry
            String errorMsg = 'Client error: ' + statusCode + ' - ' + res.getStatus();
            LOG_LogMessageUtility.logError(
                'RestApiService',
                method,
                errorMsg + ' - Endpoint: ' + endpoint,
                null
            );
            throw new RestApiException(errorMsg);
            
        } else if (statusCode >= 500) {
            // Server error - may retry
            String errorMsg = 'Server error: ' + statusCode + ' - ' + res.getStatus();
            LOG_LogMessageUtility.logError(
                'RestApiService',
                method,
                errorMsg + ' - Endpoint: ' + endpoint,
                null
            );
            throw new RestApiException(errorMsg);
        }
        
        throw new RestApiException('Unexpected status code: ' + statusCode);
    }
    
    /**
     * Custom exception for REST API errors
     */
    public class RestApiException extends Exception {}
}
```

**Usage**:
```apex
// GET request
Map<String, Object> response = RestApiService.get('/api/users/123');

// POST request
Map<String, Object> payload = new Map<String, Object>{
    'name' => 'John Doe',
    'email' => 'john@example.com'
};
Map<String, Object> response = RestApiService.post('/api/users', payload);
```

**Best Practices**:
- Always use Named Credentials for endpoints and authentication
- Check status codes and handle errors appropriately
- Log all callouts for troubleshooting
- Use appropriate timeouts (30 seconds for sync, 120 for async)

### Example 2: Inbound REST API Service

**Pattern**: Exposing REST API endpoints from Salesforce
**Use Case**: Allowing external systems to call Salesforce
**Complexity**: Intermediate
**Related Patterns**: <a href="{{ '/rag/integrations/integration-platform-patterns.html' | relative_url }}">Integration Platform Patterns</a>

**Problem**:
You need to expose a REST API endpoint that external systems can call to create or update records in Salesforce.

**Solution**:

**Apex** (`InboundRestService.cls`):
```apex
/**
 * Inbound REST API service for external systems
 * Exposes endpoints for creating and updating Contact records
 */
@RestResource(urlMapping='/api/contacts/*')
global with sharing class InboundRestService {
    
    /**
     * HTTP GET - Retrieve contact by external ID
     */
    @HttpGet
    global static void getContact() {
        RestRequest req = RestContext.request;
        RestResponse res = RestContext.response;
        
        try {
            // Extract external ID from URL
            String externalId = req.requestURI.substring(req.requestURI.lastIndexOf('/') + 1);
            
            if (String.isBlank(externalId)) {
                res.statusCode = 400;
                res.responseBody = Blob.valueOf(JSON.serialize(new Map<String, String>{
                    'error' => 'External ID is required'
                }));
                return;
            }
            
            // Query contact by external ID
            List<Contact> contacts = [
                SELECT Id, Name, Email, Phone, External_ID__c
                FROM Contact
                WHERE External_ID__c = :externalId
                WITH SECURITY_ENFORCED
                LIMIT 1
            ];
            
            if (contacts.isEmpty()) {
                res.statusCode = 404;
                res.responseBody = Blob.valueOf(JSON.serialize(new Map<String, String>{
                    'error' => 'Contact not found'
                }));
                return;
            }
            
            // Return contact data
            res.statusCode = 200;
            res.responseBody = Blob.valueOf(JSON.serialize(contacts[0]));
            
        } catch (Exception e) {
            res.statusCode = 500;
            res.responseBody = Blob.valueOf(JSON.serialize(new Map<String, String>{
                'error' => 'Internal server error: ' + e.getMessage()
            }));
            
            LOG_LogMessageUtility.logError(
                'InboundRestService',
                'getContact',
                'Error processing GET request: ' + e.getMessage(),
                e
            );
        }
    }
    
    /**
     * HTTP POST - Create contact
     */
    @HttpPost
    global static void createContact() {
        RestRequest req = RestContext.request;
        RestResponse res = RestContext.response;
        
        try {
            // Parse request body
            Map<String, Object> payload = (Map<String, Object>) JSON.deserializeUntyped(
                req.requestBody.toString()
            );
            
            // Validate required fields
            if (!payload.containsKey('externalId') || !payload.containsKey('lastName')) {
                res.statusCode = 400;
                res.responseBody = Blob.valueOf(JSON.serialize(new Map<String, String>{
                    'error' => 'externalId and lastName are required'
                }));
                return;
            }
            
            // Create contact
            Contact contact = new Contact();
            contact.External_ID__c = (String) payload.get('externalId');
            contact.LastName = (String) payload.get('lastName');
            contact.FirstName = (String) payload.get('firstName');
            contact.Email = (String) payload.get('email');
            contact.Phone = (String) payload.get('phone');
            
            insert contact;
            
            // Return created contact
            res.statusCode = 201;
            res.responseBody = Blob.valueOf(JSON.serialize(contact));
            
        } catch (DmlException e) {
            res.statusCode = 400;
            res.responseBody = Blob.valueOf(JSON.serialize(new Map<String, String>{
                'error' => 'Validation error: ' + e.getMessage()
            }));
            
        } catch (Exception e) {
            res.statusCode = 500;
            res.responseBody = Blob.valueOf(JSON.serialize(new Map<String, String>{
                'error' => 'Internal server error: ' + e.getMessage()
            }));
            
            LOG_LogMessageUtility.logError(
                'InboundRestService',
                'createContact',
                'Error processing POST request: ' + e.getMessage(),
                e
            );
        }
    }
    
    /**
     * HTTP PUT - Update contact by external ID
     */
    @HttpPut
    global static void updateContact() {
        RestRequest req = RestContext.request;
        RestResponse res = RestContext.response;
        
        try {
            // Parse request body
            Map<String, Object> payload = (Map<String, Object>) JSON.deserializeUntyped(
                req.requestBody.toString()
            );
            
            if (!payload.containsKey('externalId')) {
                res.statusCode = 400;
                res.responseBody = Blob.valueOf(JSON.serialize(new Map<String, String>{
                    'error' => 'externalId is required'
                }));
                return;
            }
            
            // Find contact by external ID
            String externalId = (String) payload.get('externalId');
            List<Contact> contacts = [
                SELECT Id
                FROM Contact
                WHERE External_ID__c = :externalId
                WITH SECURITY_ENFORCED
                LIMIT 1
            ];
            
            if (contacts.isEmpty()) {
                res.statusCode = 404;
                res.responseBody = Blob.valueOf(JSON.serialize(new Map<String, String>{
                    'error' => 'Contact not found'
                }));
                return;
            }
            
            // Update contact
            Contact contact = contacts[0];
            if (payload.containsKey('firstName')) contact.FirstName = (String) payload.get('firstName');
            if (payload.containsKey('lastName')) contact.LastName = (String) payload.get('lastName');
            if (payload.containsKey('email')) contact.Email = (String) payload.get('email');
            if (payload.containsKey('phone')) contact.Phone = (String) payload.get('phone');
            
            update contact;
            
            // Return updated contact
            res.statusCode = 200;
            res.responseBody = Blob.valueOf(JSON.serialize(contact));
            
        } catch (DmlException e) {
            res.statusCode = 400;
            res.responseBody = Blob.valueOf(JSON.serialize(new Map<String, String>{
                'error' => 'Validation error: ' + e.getMessage()
            }));
            
        } catch (Exception e) {
            res.statusCode = 500;
            res.responseBody = Blob.valueOf(JSON.serialize(new Map<String, String>{
                'error' => 'Internal server error: ' + e.getMessage()
            }));
            
            LOG_LogMessageUtility.logError(
                'InboundRestService',
                'updateContact',
                'Error processing PUT request: ' + e.getMessage(),
                e
            );
        }
    }
}
```

**Usage**:
```bash
# GET contact
GET /services/apexrest/api/contacts/EXT123

# POST create contact
POST /services/apexrest/api/contacts
{
  "externalId": "EXT123",
  "firstName": "John",
  "lastName": "Doe",
  "email": "john@example.com"
}

# PUT update contact
PUT /services/apexrest/api/contacts
{
  "externalId": "EXT123",
  "email": "newemail@example.com"
}
```

**Best Practices**:
- Use `@RestResource` and HTTP method annotations
- Validate all input data
- Return appropriate HTTP status codes
- Handle errors gracefully with clear error messages
- Use `WITH SECURITY_ENFORCED` in queries

### Example 3: Asynchronous REST API Callout

**Pattern**: Making REST API callouts asynchronously
**Use Case**: Long-running or high-volume callouts
**Complexity**: Intermediate
**Related Patterns**: <a href="{{ '/rag/development/asynchronous-apex-patterns.html' | relative_url }}">Asynchronous Apex Patterns</a>

**Problem**:
You need to make REST API callouts asynchronously to avoid timeout issues and handle high volumes.

**Solution**:

**Apex** (`AsyncRestApiService.cls`):
```apex
/**
 * Asynchronous REST API callout service
 * Uses Queueable for async execution
 */
public with sharing class AsyncRestApiService implements Queueable, Database.AllowsCallouts {
    
    private String endpoint;
    private String method;
    private Map<String, Object> payload;
    private Id recordId;
    
    public AsyncRestApiService(String endpoint, String method, Map<String, Object> payload, Id recordId) {
        this.endpoint = endpoint;
        this.method = method;
        this.payload = payload;
        this.recordId = recordId;
    }
    
    public void execute(QueueableContext context) {
        try {
            // Make callout
            Map<String, Object> response = makeCallout();
            
            // Update record with response
            updateRecordWithResponse(response);
            
            LOG_LogMessageUtility.logInfo(
                'AsyncRestApiService',
                'execute',
                'Async callout successful: ' + method + ' ' + endpoint
            );
            
        } catch (Exception e) {
            LOG_LogMessageUtility.logError(
                'AsyncRestApiService',
                'execute',
                'Async callout failed: ' + method + ' ' + endpoint + ' - ' + e.getMessage(),
                e
            );
            
            // Mark record as failed
            markRecordAsFailed(e.getMessage());
        }
    }
    
    private Map<String, Object> makeCallout() {
        HttpRequest req = new HttpRequest();
        req.setEndpoint('callout:ExternalApi' + endpoint);
        req.setMethod(method);
        req.setHeader('Content-Type', 'application/json');
        req.setTimeout(120000); // 120 seconds for async
        
        if (payload != null && (method == 'POST' || method == 'PUT')) {
            req.setBody(JSON.serialize(payload));
        }
        
        Http http = new Http();
        HttpResponse res = http.send(req);
        
        if (res.getStatusCode() >= 200 && res.getStatusCode() < 300) {
            if (String.isNotBlank(res.getBody())) {
                return (Map<String, Object>) JSON.deserializeUntyped(res.getBody());
            }
            return new Map<String, Object>();
        }
        
        throw new AsyncRestApiException('Callout failed with status: ' + res.getStatusCode());
    }
    
    private void updateRecordWithResponse(Map<String, Object> response) {
        // Update record based on response
        // Implementation depends on use case
    }
    
    private void markRecordAsFailed(String errorMessage) {
        // Mark record as failed
        // Implementation depends on use case
    }
    
    public class AsyncRestApiException extends Exception {}
}
```

**Usage**:
```apex
// Enqueue async callout
Map<String, Object> payload = new Map<String, Object>{
    'recordId' => contact.Id,
    'action' => 'sync'
};
System.enqueueJob(new AsyncRestApiService('/api/sync', 'POST', payload, contact.Id));
```

**Best Practices**:
- Use Queueable for async callouts
- Implement `Database.AllowsCallouts` interface
- Use longer timeouts (120 seconds) for async
- Handle errors and update records accordingly
- Chain jobs if needed for multiple callouts

## Related Examples

- <a href="{{ '/rag/development/asynchronous-apex-patterns.html' | relative_url }}">Asynchronous Apex Patterns</a> - Async patterns

