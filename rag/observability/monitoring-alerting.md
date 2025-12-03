---
layout: default
title: Monitoring and Alerting for Salesforce
description: This guide covers monitoring and alerting patterns for Salesforce, including Platform Events monitoring, API health monitoring, async job failure detection, and log aggregation patterns
permalink: /rag/observability/monitoring-alerting.html
level: Intermediate
tags:
  - observability
  - monitoring
  - alerting
  - platform-events
  - api-health
last_reviewed: 2025-12-03
---

# Monitoring and Alerting for Salesforce

## Overview

Monitoring and alerting patterns enable proactive detection of issues, performance problems, and system health degradation. This guide covers Platform Events monitoring, API health monitoring, async job failure detection, and log aggregation patterns.

**Core Principle**: Monitor system health proactively, alert on issues before they impact users, and aggregate logs for centralized analysis. Visibility enables rapid issue detection and resolution.

## Prerequisites

**Required Knowledge**:
- Understanding of Salesforce platform capabilities
- Familiarity with Platform Events and async processing
- Knowledge of API patterns and callouts
- Understanding of logging and error handling
- Knowledge of monitoring tools and dashboards

**Recommended Reading**:
- <a href="{{ '/rag/observability/performance-tuning.html' | relative_url }}">Performance Tuning</a> - Performance optimization and monitoring
- <a href="{{ '/rag/integrations/change-data-capture-patterns.html' | relative_url }}">Change Data Capture Patterns</a> - CDC monitoring patterns
- <a href="{{ '/rag/architecture/event-driven-architecture.html' | relative_url }}">Event-Driven Architecture</a> - Platform Events patterns
- <a href="{{ '/rag/development/error-handling-and-logging.html' | relative_url }}">Error Handling and Logging</a> - Logging patterns

## When to Use Monitoring and Alerting

### Use Monitoring and Alerting When

- **Production systems**: Need visibility into production system health
- **Critical integrations**: Integrations require monitoring
- **Async job processing**: Async jobs need failure detection
- **Performance issues**: Need to detect performance degradation
- **Compliance requirements**: Regulatory requirements mandate monitoring
- **Proactive issue detection**: Need to detect issues before user impact

### Avoid Monitoring and Alerting When

- **Development environments**: Basic logging sufficient
- **Non-critical systems**: System failures have minimal impact
- **Limited resources**: Don't have resources for monitoring setup
- **Simple use cases**: Basic error handling sufficient

## Platform Events Monitoring

### Pattern 1: Event Publication Monitoring

**Purpose**: Monitor Platform Event publication success and failure rates.

**Implementation**:
- **Custom Logging Object**: Log event publication attempts
- **Success/Failure Tracking**: Track publication success and failures
- **Metrics Dashboard**: Dashboard showing event publication metrics
- **Alerting**: Alert on high failure rates

**Example**:
```apex
public class EventPublicationLogger {
    public static void logEventPublication(String eventType, Boolean success, String errorMessage) {
        Event_Publication_Log__c log = new Event_Publication_Log__c(
            Event_Type__c = eventType,
            Success__c = success,
            Error_Message__c = errorMessage,
            Timestamp__c = Datetime.now()
        );
        insert log;
    }
}
```

**Best Practices**:
- Log all event publications
- Track success/failure rates
- Monitor event volume
- Alert on failures
- Create dashboards

### Pattern 2: Event Processing Monitoring

**Purpose**: Monitor event processing by subscribers.

**Implementation**:
- **Subscriber Logging**: Log event processing by subscribers
- **Processing Time**: Track event processing duration
- **Failure Tracking**: Track processing failures
- **Lag Monitoring**: Monitor event processing lag

**Best Practices**:
- Log event processing
- Track processing time
- Monitor processing lag
- Alert on failures
- Create processing dashboards

## API Health Monitoring

### Pattern 1: Callout Health Monitoring

**Purpose**: Monitor API callout health and performance.

**Implementation**:
- **Callout Metrics**: Track callout duration, status codes, response sizes
- **Failure Rate Monitoring**: Monitor callout failure rates
- **Circuit Breaker Monitoring**: Monitor circuit breaker state
- **Health Dashboards**: Dashboards showing API health

**Example**:
```apex
public class CalloutHealthMonitor {
    public static void trackCallout(String integrationName, String endpoint, 
                                   Integer statusCode, Long duration) {
        Callout_Metric__c metric = new Callout_Metric__c(
            Integration_Name__c = integrationName,
            Endpoint__c = endpoint,
            Status_Code__c = statusCode,
            Duration_ms__c = duration,
            Timestamp__c = Datetime.now()
        );
        insert metric;
    }
    
    public static void checkHealth(String integrationName) {
        Integer failureCount = [
            SELECT COUNT() 
            FROM Callout_Metric__c 
            WHERE Integration_Name__c = :integrationName
            AND Status_Code__c >= 500
            AND Timestamp__c >= :Datetime.now().addHours(-1)
        ];
        
        if (failureCount > 10) {
            sendAlert('High failure rate: ' + integrationName);
        }
    }
}
```

**Best Practices**:
- Track all callouts
- Monitor failure rates
- Alert on high failure rates
- Monitor response times
- Create health dashboards

### Pattern 2: API Rate Limit Monitoring

**Purpose**: Monitor API rate limit usage and approaching limits.

**Implementation**:
- **Rate Limit Tracking**: Track API call counts
- **Limit Monitoring**: Monitor approaching rate limits
- **Alerting**: Alert when approaching limits
- **Throttling**: Implement throttling when approaching limits

**Best Practices**:
- Track API usage
- Monitor rate limits
- Alert on high usage
- Implement throttling
- Create usage dashboards

## Async Job Failure Detection

### Pattern 1: Batch Job Monitoring

**Purpose**: Monitor Batch Apex job failures and performance.

**Implementation**:
- **Job Status Monitoring**: Query AsyncApexJob for job status
- **Failure Detection**: Detect failed batch jobs
- **Error Logging**: Log batch job errors
- **Alerting**: Alert on batch job failures

**Example**:
```apex
public class BatchJobMonitor {
    public static void monitorBatchJobs() {
        List<AsyncApexJob> failedJobs = [
            SELECT Id, ApexClass.Name, Status, NumberOfErrors, 
                   JobItemsProcessed, TotalJobItems
            FROM AsyncApexJob
            WHERE Status = 'Failed'
            AND CreatedDate >= :Datetime.now().addHours(-24)
        ];
        
        if (!failedJobs.isEmpty()) {
            sendAlert('Failed batch jobs detected: ' + failedJobs.size());
        }
    }
}
```

**Best Practices**:
- Monitor job status
- Detect failures
- Log errors
- Alert on failures
- Create job dashboards

### Pattern 2: Queueable Job Monitoring

**Purpose**: Monitor Queueable Apex job failures.

**Implementation**:
- **Job Status Tracking**: Track Queueable job status
- **Failure Detection**: Detect failed Queueable jobs
- **Chain Monitoring**: Monitor Queueable job chains
- **Alerting**: Alert on Queueable failures

**Best Practices**:
- Track job status
- Detect failures
- Monitor job chains
- Alert on failures
- Create monitoring dashboards

### Pattern 3: Scheduled Job Monitoring

**Purpose**: Monitor Scheduled Apex job execution and failures.

**Implementation**:
- **Execution Tracking**: Track scheduled job execution
- **Failure Detection**: Detect failed scheduled jobs
- **Execution Time Monitoring**: Monitor job execution time
- **Alerting**: Alert on scheduled job failures

**Best Practices**:
- Track execution
- Detect failures
- Monitor execution time
- Alert on failures
- Create execution dashboards

## Log Aggregation Patterns

### Pattern 1: Centralized Logging

**Purpose**: Aggregate logs from multiple sources for centralized analysis.

**Implementation**:
- **Custom Logging Object**: Centralized logging object
- **Log Collection**: Collect logs from multiple sources
- **Log Analysis**: Analyze logs for patterns
- **Log Retention**: Implement log retention policies

**Best Practices**:
- Centralize logs
- Collect from all sources
- Analyze for patterns
- Implement retention
- Create log dashboards

### Pattern 2: Error Log Aggregation

**Purpose**: Aggregate error logs for analysis and alerting.

**Implementation**:
- **Error Logging**: Log all errors to custom object
- **Error Aggregation**: Aggregate errors by type, source, frequency
- **Error Analysis**: Analyze error patterns
- **Alerting**: Alert on error spikes

**Best Practices**:
- Log all errors
- Aggregate by type
- Analyze patterns
- Alert on spikes
- Create error dashboards

### Pattern 3: Performance Log Aggregation

**Purpose**: Aggregate performance logs for analysis.

**Implementation**:
- **Performance Logging**: Log performance metrics
- **Performance Aggregation**: Aggregate performance data
- **Performance Analysis**: Analyze performance trends
- **Alerting**: Alert on performance degradation

**Best Practices**:
- Log performance metrics
- Aggregate data
- Analyze trends
- Alert on degradation
- Create performance dashboards

## Alerting Patterns

### Pattern 1: Threshold-Based Alerting

**Purpose**: Alert when metrics exceed thresholds.

**Implementation**:
- **Define Thresholds**: Set thresholds for metrics
- **Monitor Metrics**: Monitor metrics continuously
- **Alert on Threshold**: Alert when threshold exceeded
- **Escalation**: Escalate if alert not acknowledged

**Best Practices**:
- Set appropriate thresholds
- Monitor continuously
- Alert promptly
- Implement escalation
- Review thresholds regularly

### Pattern 2: Anomaly Detection

**Purpose**: Detect anomalies in metrics (unusual patterns).

**Implementation**:
- **Baseline Metrics**: Establish baseline metrics
- **Anomaly Detection**: Detect deviations from baseline
- **Alert on Anomalies**: Alert when anomalies detected
- **Pattern Analysis**: Analyze anomaly patterns

**Best Practices**:
- Establish baselines
- Detect anomalies
- Alert on anomalies
- Analyze patterns
- Refine detection

### Pattern 3: Composite Alerting

**Purpose**: Alert based on multiple conditions.

**Implementation**:
- **Multiple Conditions**: Define multiple alert conditions
- **Composite Logic**: Combine conditions (AND, OR)
- **Alert on Composite**: Alert when composite condition met
- **Context**: Include context in alerts

**Best Practices**:
- Define conditions
- Combine logically
- Alert appropriately
- Include context
- Review conditions

## Related Patterns

- <a href="{{ '/rag/observability/performance-tuning.html' | relative_url }}">Performance Tuning</a> - Performance optimization and monitoring
- <a href="{{ '/rag/integrations/change-data-capture-patterns.html' | relative_url }}">Change Data Capture Patterns</a> - CDC monitoring patterns
- <a href="{{ '/rag/architecture/event-driven-architecture.html' | relative_url }}">Event-Driven Architecture</a> - Platform Events patterns
- <a href="{{ '/rag/development/error-handling-and-logging.html' | relative_url }}">Error Handling and Logging</a> - Logging patterns
- <a href="{{ '/rag/integrations/callout-best-practices.html' | relative_url }}">Callout Best Practices</a> - API callout monitoring

## Q&A

### Q: What are monitoring and alerting patterns for Salesforce?

**A**: **Monitoring and alerting patterns** enable: (1) **Proactive issue detection** (detect issues before user impact), (2) **System health visibility** (dashboards showing system health), (3) **Performance monitoring** (track performance metrics), (4) **Error tracking** (track and analyze errors), (5) **Automated alerting** (alert on issues automatically). Monitoring and alerting provide visibility into system health and enable rapid issue resolution.

### Q: How do I monitor Platform Events?

**A**: Monitor by: (1) **Log event publications** (log all event publication attempts), (2) **Track success/failure rates** (monitor publication success), (3) **Monitor event volume** (track event counts), (4) **Alert on failures** (alert when failures detected), (5) **Create dashboards** (visualize event metrics). Platform Events monitoring ensures event-driven integrations are working correctly.

### Q: How do I monitor API callout health?

**A**: Monitor by: (1) **Track callout metrics** (duration, status codes, response sizes), (2) **Monitor failure rates** (track callout failures), (3) **Circuit breaker monitoring** (monitor circuit breaker state), (4) **Alert on failures** (alert on high failure rates), (5) **Create health dashboards** (visualize API health). API health monitoring ensures integrations are functioning correctly.

### Q: How do I detect async job failures?

**A**: Detect by: (1) **Query AsyncApexJob** (query job status), (2) **Monitor job status** (track job execution), (3) **Detect failures** (identify failed jobs), (4) **Log errors** (log job errors), (5) **Alert on failures** (alert when jobs fail). Async job failure detection ensures background processing is working correctly.

### Q: How do I aggregate logs for analysis?

**A**: Aggregate by: (1) **Centralized logging** (log to custom object), (2) **Collect from all sources** (collect logs from all components), (3) **Aggregate by type** (group logs by type), (4) **Analyze patterns** (identify patterns in logs), (5) **Create dashboards** (visualize log data). Log aggregation enables centralized analysis and pattern detection.

### Q: What are best practices for alerting?

**A**: Best practices: (1) **Set appropriate thresholds** (not too sensitive, not too lenient), (2) **Monitor continuously** (real-time or near-real-time), (3) **Alert promptly** (alert quickly on issues), (4) **Include context** (provide context in alerts), (5) **Implement escalation** (escalate if not acknowledged), (6) **Review regularly** (review and adjust thresholds). Effective alerting enables rapid issue response.

### Q: How do I create monitoring dashboards?

**A**: Create by: (1) **Identify key metrics** (determine what to monitor), (2) **Create custom objects** (store metrics in custom objects), (3) **Build reports** (create reports on metrics), (4) **Create dashboards** (build dashboards from reports), (5) **Share dashboards** (share with stakeholders). Monitoring dashboards provide visibility into system health.
