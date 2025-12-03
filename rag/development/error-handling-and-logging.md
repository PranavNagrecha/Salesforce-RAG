---
title: "Error Handling and Logging Framework"
level: "Intermediate"
tags:
  - apex
  - development
  - patterns
  - error-handling
  - logging
  - observability
last_reviewed: "2025-01-XX"
---

# Error Handling and Logging Framework

## Overview

Comprehensive error handling and logging framework ensures all errors are captured, logged, and traceable for troubleshooting and compliance. The framework uses a custom logging object (`LOG_LogMessage__c`) with utility classes and platform event fallbacks to ensure no errors are lost.

## Prerequisites

**Required Knowledge**:
- Understanding of Apex exception handling (try-catch blocks)
- Knowledge of DML operations and exception types
- Understanding of Platform Events (for fallback logging)
- Familiarity with custom objects and field types

**Recommended Reading**:
- <a href="{{ '/rag/development/development/apex-patterns.html' | relative_url }}">Apex Patterns</a> - Apex class structure and patterns
- <a href="{{ '/rag/development/development/asynchronous-apex-patterns.html' | relative_url }}">Asynchronous Apex Patterns</a> - Queueable patterns for error handling
- <a href="{{ '/rag/development/architecture/event-driven-architecture.html' | relative_url }}">Event-Driven Architecture</a> - Platform Events patterns

## Logging Architecture

### Custom Logging Object

All errors logged to `LOG_LogMessage__c` object:

- **Persistent Storage**: Queryable logs that can be analyzed and reported on
- **Structured Format**: Consistent log format with source, source function, message, debug level, payload
- **Compliance Support**: Meets government cloud and audit trail requirements
- **Troubleshooting**: Enables effective troubleshooting and root cause analysis

### Log Levels

Support different log levels:

- **Debug**: Detailed debugging information
- **Info**: General informational messages
- **Warning**: Warning conditions that don't prevent operation
- **Error**: Error conditions that prevent operation
- **Fatal**: Critical errors that cause system failure

### Logging Utility Class

`LOG_LogMessageUtility` Apex utility class:

- Supports different log levels
- Provides consistent logging interface
- Handles DML exceptions gracefully
- Publishes platform events as fallback

## Error Handling Patterns

### All Errors Must Be Logged

Standard requiring all errors logged to `LOG_LogMessage__c`:

- **Integration Errors**: All API call errors logged
- **DML Errors**: All database operation errors logged
- **Validation Errors**: All validation failure errors logged
- **System Errors**: All system exception errors logged

### Platform Event Fallback

If DML fails, publish platform event to ensure error is captured:

- **ErrorLog__e Platform Event**: Publishes error when DML fails
- **Guaranteed Capture**: Ensures errors are captured even when logging DML fails
- **Asynchronous Processing**: Platform events processed asynchronously
- **No Data Loss**: Prevents loss of error information

### Structured Logging

Consistent log format with:

- **Source**: Component or class that generated the log
- **Source Function**: Method or function that generated the log
- **Message**: Human-readable error message
- **Debug Level**: Log level (Debug, Info, Error, Warning, Fatal)
- **Payload**: Additional context or data

## Implementation Patterns

### Apex Error Logging

Use `LOG_LogMessageUtility` class for Apex error logging:

```apex
try {
    // Operation that might fail
} catch (Exception e) {
    LOG_LogMessageUtility.logError(
        'ClassName',
        'methodName',
        'Error message',
        e
    );
}
```

### Integration Procedure Logging

Use DataRaptor Load actions for OmniStudio logging:

- **IEECreateLogMessageRec**: DataRaptor Load action for logging API calls
- **Conditional Logging**: Analysis of whether to log all API calls or only errors
- **Storage Considerations**: Balance between comprehensive logging and storage/performance

### Flow Error Logging

Log errors in Flows:

- Use fault paths for all integration calls and DML operations
- Call Apex invocable methods to log errors
- Provide clear error messages to users
- Log errors for troubleshooting

## Best Practices

### Error Logging

- Log all errors, not just exceptions
- Include sufficient context for troubleshooting
- Use appropriate log levels
- Structure logs consistently
- Include correlation IDs when available

### Error Handling

- Handle errors gracefully
- Provide user-friendly error messages
- Log errors before showing messages to users
- Implement retry logic for transient failures
- Support error recovery workflows

### Logging Performance

- Consider conditional logging for high-volume operations
- Balance comprehensive logging with storage/performance
- Use asynchronous logging when possible
- Monitor logging performance impact
- Archive old logs periodically

### Compliance and Audit

- Meet compliance requirements (government cloud, audit trails)
- Retain logs according to retention policies
- Enable log analysis and reporting
- Support audit trail requirements
- Document logging strategy

## Integration with External Systems

### Centralized Logging

Integrate with centralized logging platforms:

- **OpenSearch**: Centralized log aggregation
- **Splunk**: Log analysis and monitoring
- **Cross-System Correlation**: Correlate logs across systems
- **Unified View**: Single view of logs across all systems

### Log Routing

Participate in decisions about log routing:

- **Salesforce Logs**: Route to centralized logging platform
- **Integration Platform Logs**: Route MuleSoft/Boomi logs
- **External API Logs**: Route external system logs
- **Unified Correlation**: Correlate logs across all systems

## Monitoring and Alerting

### Log Monitoring

Monitor logs for:

- Error rates and trends
- Performance issues
- Security events
- Integration failures
- System health

### Automated Alerting

Set up automated alerts for:

- High error rates
- Critical errors (Fatal level)
- Integration failures
- Performance degradation
- Security violations

### Dashboards

Build dashboards showing:

- Error rates by component
- Log volume trends
- Integration health
- System performance
- Compliance metrics

## Tradeoffs

### Advantages

- **Compliance**: Meets government cloud and audit requirements
- **Troubleshooting**: Enables effective root cause analysis
- **Monitoring**: Supports system health monitoring
- **Audit Trail**: Provides comprehensive audit trail

### Challenges

- **Storage**: Requires storage for log records
- **Performance**: Logging can impact performance
- **Volume**: High-volume logging requires management
- **Retention**: Requires log retention policies

## When to Use This Pattern

Use comprehensive error handling and logging when:

- Compliance requires audit trails
- Troubleshooting complex integrations
- Monitoring system health
- Supporting security audits
- Debugging production issues

## When Not to Use This Pattern

Avoid comprehensive logging when:

- Simple applications with minimal errors
- Storage constraints prevent logging
- Performance impact is unacceptable
- Logging overhead outweighs benefits

## Q&A

### Q: Why should I use a custom logging object instead of System.debug()?

**A**: Custom logging objects provide **persistent, queryable logs** that can be analyzed, reported on, and retained for compliance. `System.debug()` logs are temporary and not accessible in production. Custom logging supports audit trails, troubleshooting, and compliance requirements.

### Q: What log levels should I use?

**A**: Use **Debug** for detailed debugging information, **Info** for general informational messages, **Warning** for warning conditions that don't prevent operation, **Error** for error conditions that prevent operation, and **Fatal** for critical errors that cause system failure. Choose the appropriate level based on severity.

### Q: How do I handle DML exceptions in error handling?

**A**: Use `Database.insert/update/delete` with `allOrNone=false` for partial success, catch `DmlException` and check `getDmlType()` for specific error types, handle errors per record using `getDmlFields()` and `getDmlMessage()`, and log errors appropriately. This enables graceful handling of partial failures.

### Q: What is the difference between try-catch and Database methods with allOrNone?

**A**: **try-catch** stops execution on first error and requires exception handling. **Database methods with allOrNone=false** allow partial success, continue processing remaining records, and return results with success/failure per record. Use Database methods for bulk operations where partial success is acceptable.

### Q: How do I implement platform event fallback for logging?

**A**: If logging to custom object fails, publish platform events as fallback. This ensures errors are never lost even if the logging object is unavailable. Implement fallback logic in the logging utility class to publish events when DML fails.

### Q: What should I include in error logs?

**A**: Include source (class/method name), source function, error message, debug level, payload/context data, stack trace, user context, timestamp, and correlation IDs. This provides comprehensive context for troubleshooting and root cause analysis.

### Q: How do I monitor and alert on errors?

**A**: Query logs regularly for errors, create reports and dashboards on log data, set up alerts for fatal errors, monitor error rates and trends, and implement automated notifications for critical errors. Use monitoring tools to track system health.

### Q: What are the performance implications of comprehensive logging?

**A**: Logging adds DML operations which count against governor limits. Use async logging (Queueable, Platform Events) for high-volume scenarios, batch log writes when possible, and consider log retention policies to manage storage. Balance logging comprehensiveness with performance.

## Edge Cases and Limitations

### Logging Object Unavailability

**Scenario**: The custom logging object may be unavailable due to permissions, DML limits, or system issues.

**Consideration**:
- Implement platform event fallback to ensure errors are never lost
- Handle DML exceptions gracefully in logging utility
- Monitor logging object availability and permissions
- Consider using multiple logging mechanisms for redundancy

### High-Volume Logging Scenarios

**Scenario**: High-frequency logging can hit governor limits or cause performance issues.

**Consideration**:
- Use asynchronous logging for high-volume scenarios
- Implement log batching to reduce DML operations
- Consider log level filtering to reduce log volume
- Monitor logging performance and adjust as needed

### Partial Failure Scenarios

**Scenario**: Some records in a bulk operation may fail while others succeed.

**Consideration**:
- Use Database methods with `allOrNone=false` for partial success
- Log errors per record using `getDmlFields()` and `getDmlMessage()`
- Track successful and failed records separately
- Implement retry logic for failed records

### Error Context Loss

**Scenario**: Errors may occur in contexts where full context is not available.

**Consideration**:
- Capture as much context as possible (source, method, parameters, stack trace)
- Use correlation IDs to track related operations
- Include user context and timestamp in all logs
- Design logging to capture context at the point of error

### Limitations

- **DML limits**: Logging DML operations count against governor limits
- **Storage limits**: Custom logging objects consume storage; plan for log retention and cleanup
- **Query limits**: Querying logs counts against SOQL query limits
- **Platform event limits**: Platform event fallback has its own limits and retention
- **Performance impact**: Excessive logging can impact transaction performance

## Related Patterns

**See Also**:
- <a href="{{ '/rag/development/development/apex-patterns.html' | relative_url }}">Apex Patterns</a> - Apex error handling patterns
- <a href="{{ '/rag/development/development/flow-patterns.html' | relative_url }}">Flow Patterns</a> - Flow error handling patterns

**Related Domains**:
- <a href="{{ '/rag/development/observability/monitoring-alerting.html' | relative_url }}">Monitoring and Alerting</a> - Monitoring patterns, log aggregation, and alerting strategies
- <a href="{{ '/rag/development/observability/performance-tuning.html' | relative_url }}">Performance Tuning</a> - Performance optimization patterns
- <a href="{{ '/rag/development/code-examples/utilities/logging-examples.html' | relative_url }}">Logging Examples</a> - Logging code examples

