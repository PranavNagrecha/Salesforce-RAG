---
layout: default
title: Logging Examples
description: Code examples for Logging Examples
permalink: /rag/code-examples/utilities/logging-examples.html
---

# Logging Code Examples

> This file contains complete, working code examples for structured logging patterns.
> All examples are copy-paste ready and follow Salesforce best practices.

## Overview

Structured logging enables consistent, searchable logging across Salesforce applications. These examples demonstrate custom logging objects, platform event fallbacks, external logging integration, and compliance/audit trail requirements.

**Related Patterns**:
- <a href="{{ '/rag/development/error-handling-and-logging.html' | relative_url }}">Error Handling and Logging</a> - Comprehensive logging framework
- <a href="{{ '/rag/code-examples/utilities/code-examples/utilities/error-handling-examples.html' | relative_url }}">Error Handling Examples</a> - Error handling patterns
- <a href="{{ '/rag/code-examples/utilities/observability/monitoring-alerting.html' | relative_url }}">Observability Patterns</a> - Monitoring patterns

## Examples

### Example 1: Basic Logging Utility

**Pattern**: Custom logging object with utility class
**Use Case**: Structured logging for all operations
**Complexity**: Basic
**Related Patterns**: <a href="{{ '/rag/development/error-handling-and-logging.html' | relative_url }}">Error Handling and Logging</a>

**Problem**:
You need a consistent logging mechanism across your application.

**Solution**:

**Custom Object** (`LOG_LogMessage__c`):
- **API Name**: `LOG_LogMessage__c`
- **Fields**:
  - `Source__c` (Text, 255) - Source class/component
  - `Function__c` (Text, 255) - Function/method name
  - `Level__c` (Picklist) - Log level (INFO, WARNING, ERROR, DEBUG)
  - `Message__c` (Long Text Area) - Log message
  - `Stack_Trace__c` (Long Text Area) - Stack trace for errors
  - `Record_ID__c` (Lookup) - Related record ID
  - `User_ID__c` (Lookup to User) - User who triggered the log
  - `Timestamp__c` (DateTime) - Log timestamp

**Apex** (`LOG_LogMessageUtility.cls`):
```apex
/**
 * Utility class for structured logging
 * Uses custom LOG_LogMessage__c object
 */
public with sharing class LOG_LogMessageUtility {
    
    /**
     * Logs an info message
     * @param source Source class/component
     * @param function Function/method name
     * @param message Log message
     */
    public static void logInfo(String source, String function, String message) {
        createLog('INFO', source, function, message, null, null);
    }
    
    /**
     * Logs a warning message
     * @param source Source class/component
     * @param function Function/method name
     * @param message Log message
     */
    public static void logWarning(String source, String function, String message) {
        createLog('WARNING', source, function, message, null, null);
    }
    
    /**
     * Logs an error message
     * @param source Source class/component
     * @param function Function/method name
     * @param message Log message
     * @param exception Exception object (optional)
     */
    public static void logError(String source, String function, String message, Exception exception) {
        String stackTrace = exception != null ? exception.getStackTraceString() : null;
        createLog('ERROR', source, function, message, stackTrace, null);
    }
    
    /**
     * Logs a debug message
     * @param source Source class/component
     * @param function Function/method name
     * @param message Log message
     */
    public static void logDebug(String source, String function, String message) {
        createLog('DEBUG', source, function, message, null, null);
    }
    
    /**
     * Creates a log record
     * @param level Log level
     * @param source Source class/component
     * @param function Function/method name
     * @param message Log message
     * @param stackTrace Stack trace
     * @param recordId Related record ID
     */
    private static void createLog(String level, String source, String function, String message, String stackTrace, Id recordId) {
        try {
            LOG_LogMessage__c log = new LOG_LogMessage__c();
            log.Level__c = level;
            log.Source__c = source;
            log.Function__c = function;
            log.Message__c = message;
            log.Stack_Trace__c = stackTrace;
            log.Record_ID__c = recordId;
            log.User_ID__c = UserInfo.getUserId();
            log.Timestamp__c = DateTime.now();
            
            insert log;
            
        } catch (Exception e) {
            // Fallback to platform event if DML fails
            publishLogEvent(level, source, function, message, stackTrace, recordId);
        }
    }
    
    /**
     * Publishes log to platform event as fallback
     * @param level Log level
     * @param source Source class/component
     * @param function Function/method name
     * @param message Log message
     * @param stackTrace Stack trace
     * @param recordId Related record ID
     */
    private static void publishLogEvent(String level, String source, String function, String message, String stackTrace, Id recordId) {
        try {
            LOG_LogEvent__e event = new LOG_LogEvent__e();
            event.Level__c = level;
            event.Source__c = source;
            event.Function__c = function;
            event.Message__c = message;
            event.Stack_Trace__c = stackTrace;
            event.Record_ID__c = recordId;
            
            EventBus.publish(new List<LOG_LogEvent__e>{ event });
            
        } catch (Exception e) {
            // Last resort - use System.debug
            System.debug(LoggingLevel.ERROR, 'Logging failed: ' + source + '.' + function + ' - ' + message);
        }
    }
}
```

**Usage**:
```apex
// Log info
LOG_LogMessageUtility.logInfo('ContactService', 'processContacts', 'Processing 10 contacts');

// Log error
try {
    // Some operation
} catch (Exception e) {
    LOG_LogMessageUtility.logError('ContactService', 'processContacts', 'Error processing contacts', e);
}
```

**Best Practices**:
- Use structured logging consistently
- Include source, function, and message
- Use appropriate log levels
- Implement fallback mechanism for DML failures

### Example 2: Logging with Platform Event Fallback

**Pattern**: Platform event fallback when DML fails
**Use Case**: Ensuring logs are captured even when DML fails
**Complexity**: Intermediate
**Related Patterns**: <a href="{{ '/rag/development/error-handling-and-logging.html' | relative_url }}">Error Handling and Logging</a>

**Problem**:
You need to ensure logs are captured even when DML operations fail (e.g., during trigger failures).

**Solution**:

**Platform Event** (`LOG_LogEvent__e`):
- **Label**: Log Event
- **Fields**:
  - `Level__c` (Text, 255) - Log level
  - `Source__c` (Text, 255) - Source class/component
  - `Function__c` (Text, 255) - Function/method name
  - `Message__c` (Long Text Area) - Log message
  - `Stack_Trace__c` (Long Text Area) - Stack trace
  - `Record_ID__c` (Text, 255) - Related record ID

**Apex** (`LOG_LogMessageUtility.cls` - Enhanced):
```apex
/**
 * Enhanced logging utility with platform event fallback
 */
public with sharing class LOG_LogMessageUtility {
    
    /**
     * Creates log with automatic fallback
     * @param level Log level
     * @param source Source class/component
     * @param function Function/method name
     * @param message Log message
     * @param stackTrace Stack trace
     * @param recordId Related record ID
     */
    public static void createLog(String level, String source, String function, String message, String stackTrace, Id recordId) {
        // Try DML first
        try {
            LOG_LogMessage__c log = new LOG_LogMessage__c();
            log.Level__c = level;
            log.Source__c = source;
            log.Function__c = function;
            log.Message__c = message;
            log.Stack_Trace__c = stackTrace;
            log.Record_ID__c = recordId;
            log.User_ID__c = UserInfo.getUserId();
            log.Timestamp__c = DateTime.now();
            
            insert log;
            return; // Success - exit
            
        } catch (DmlException e) {
            // DML failed - use platform event fallback
            publishLogEvent(level, source, function, message, stackTrace, recordId);
            
        } catch (Exception e) {
            // Unexpected error - use platform event fallback
            publishLogEvent(level, source, function, message, stackTrace, recordId);
        }
    }
    
    /**
     * Publishes log to platform event
     * @param level Log level
     * @param source Source class/component
     * @param function Function/method name
     * @param message Log message
     * @param stackTrace Stack trace
     * @param recordId Related record ID
     */
    private static void publishLogEvent(String level, String source, String function, String message, String stackTrace, Id recordId) {
        try {
            LOG_LogEvent__e event = new LOG_LogEvent__e();
            event.Level__c = level;
            event.Source__c = source;
            event.Function__c = function;
            event.Message__c = message;
            event.Stack_Trace__c = stackTrace;
            event.Record_ID__c = recordId != null ? String.valueOf(recordId) : null;
            
            List<Database.SaveResult> results = EventBus.publish(new List<LOG_LogEvent__e>{ event });
            
            // Check for publish errors
            for (Database.SaveResult result : results) {
                if (!result.isSuccess()) {
                    // Last resort - System.debug
                    System.debug(LoggingLevel.ERROR, 'Log event publish failed: ' + source + '.' + function);
                }
            }
            
        } catch (Exception e) {
            // Last resort - System.debug
            System.debug(LoggingLevel.ERROR, 'Logging completely failed: ' + source + '.' + function + ' - ' + message);
        }
    }
}
```

**Best Practices**:
- Always implement fallback mechanism
- Use platform events when DML fails
- Use System.debug as last resort
- Never let logging failures break business logic

### Example 3: External Logging Integration

**Pattern**: Integrating with external logging systems
**Use Case**: Centralized logging across multiple systems
**Complexity**: Advanced
**Related Patterns**: <a href="{{ '/rag/code-examples/utilities/observability/monitoring-alerting.html' | relative_url }}">Observability Patterns</a>

**Problem**:
You need to send logs to an external logging system (e.g., Splunk, OpenSearch).

**Solution**:

**Apex** (`ExternalLoggingService.cls`):
```apex
/**
 * Service for sending logs to external logging systems
 */
public with sharing class ExternalLoggingService implements Queueable, Database.AllowsCallouts {
    
    private List<LOG_LogMessage__c> logs;
    
    public ExternalLoggingService(List<LOG_LogMessage__c> logs) {
        this.logs = logs;
    }
    
    public void execute(QueueableContext context) {
        for (LOG_LogMessage__c log : logs) {
            try {
                sendToExternalSystem(log);
            } catch (Exception e) {
                // Log error but don't fail the job
                System.debug(LoggingLevel.ERROR, 'Failed to send log to external system: ' + e.getMessage());
            }
        }
    }
    
    /**
     * Sends log to external logging system
     * @param log Log message record
     */
    private void sendToExternalSystem(LOG_LogMessage__c log) {
        HttpRequest req = new HttpRequest();
        req.setEndpoint('callout:ExternalLoggingApi/api/logs');
        req.setMethod('POST');
        req.setHeader('Content-Type', 'application/json');
        req.setTimeout(30000);
        
        // Build log payload
        Map<String, Object> payload = new Map<String, Object>{
            'level' => log.Level__c,
            'source' => log.Source__c,
            'function' => log.Function__c,
            'message' => log.Message__c,
            'stackTrace' => log.Stack_Trace__c,
            'recordId' => log.Record_ID__c,
            'userId' => log.User_ID__c,
            'timestamp' => log.Timestamp__c
        };
        
        req.setBody(JSON.serialize(payload));
        
        Http http = new Http();
        HttpResponse res = http.send(req);
        
        if (res.getStatusCode() >= 200 && res.getStatusCode() < 300) {
            // Success
            return;
        }
        
        throw new ExternalLoggingException('Failed to send log: ' + res.getStatusCode());
    }
    
    /**
     * Enqueues logs for external system
     * @param logs List of log records
     */
    public static void enqueueLogs(List<LOG_LogMessage__c> logs) {
        if (logs != null && !logs.isEmpty()) {
            System.enqueueJob(new ExternalLoggingService(logs));
        }
    }
    
    public class ExternalLoggingException extends Exception {}
}
```

**Usage**:
```apex
// After creating logs, send to external system
List<LOG_LogMessage__c> logs = new List<LOG_LogMessage__c>();
// ... create logs ...
insert logs;
ExternalLoggingService.enqueueLogs(logs);
```

**Best Practices**:
- Use async processing for external logging
- Batch logs for efficiency
- Handle failures gracefully
- Don't block business logic for logging

## Related Examples

- <a href="{{ '/rag/code-examples/utilities/code-examples/utilities/error-handling-examples.html' | relative_url }}">Error Handling Examples</a> - Error handling patterns
- <a href="{{ '/rag/code-examples/utilities/code-examples/utilities/validation-examples.html' | relative_url }}">Validation Examples</a> - Validation patterns

## See Also

- <a href="{{ '/rag/development/error-handling-and-logging.html' | relative_url }}">Error Handling and Logging</a> - Comprehensive logging framework
- <a href="{{ '/rag/code-examples/utilities/observability/monitoring-alerting.html' | relative_url }}">Observability Patterns</a> - Monitoring patterns

