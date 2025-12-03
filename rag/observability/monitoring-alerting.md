---
title: "Monitoring and Alerting for Salesforce"
level: "Intermediate"
tags:
  - observability
  - monitoring
  - alerting
  - platform-events
last_reviewed: "2025-01-XX"
---

# Monitoring and Alerting for Salesforce

## Overview

This guide covers monitoring and alerting patterns for Salesforce, including Platform Events monitoring, API health monitoring, async job failure detection, and log aggregation patterns. These patterns are essential for maintaining system reliability, detecting issues early, and ensuring operational excellence.

**Related Patterns**:
- [Error Handling and Logging](/rag/development/error-handling-and-logging.html) - Logging framework and error handling
- [Performance Tuning](/rag/observability/performance-tuning.html) - Performance optimization patterns
- [Change Data Capture Patterns](/rag/integrations/change-data-capture-patterns.html) - CDC event processing
- [Event-Driven Architecture](/rag/architecture/event-driven-architecture.html) - Platform Events patterns

## Consensus Best Practices

- **Monitor proactively, not reactively**: Set up monitoring before issues occur
- **Use structured logging**: Implement consistent, structured log formats for better analysis
- **Aggregate logs centrally**: Centralize logs for correlation and analysis
- **Set meaningful alert thresholds**: Avoid alert fatigue with appropriate thresholds
- **Monitor async jobs**: Track Batch, Queueable, and Scheduled job health
- **Track API health**: Monitor external API availability and performance
- **Correlate events**: Use correlation IDs to track related events across systems
- **Automate alerting**: Use automated alerting for critical issues
- **Review and tune alerts**: Regularly review alert effectiveness and adjust thresholds

## Platform Events Monitoring

### Event Processing Metrics

**Key Metrics to Track**:
- **Events Published**: Count of events published per event type
- **Events Processed**: Count of events successfully processed
- **Events Failed**: Count of events that failed processing
- **Processing Time**: Average and p95/p99 processing time
- **Event Lag**: Delay between event publication and processing
- **Retry Count**: Number of retries for failed events

**Monitoring Patterns**:
- Track metrics per event type
- Monitor trends over time
- Set baselines for normal operation
- Alert on anomalies

### Event Lag Monitoring

**Lag Detection**:
- Track time between event publication and processing
- Monitor lag trends over time
- Alert on lag exceeding thresholds
- Identify bottlenecks in event processing

**Lag Analysis**:
- Correlate lag with system load
- Identify peak usage periods
- Analyze lag by event type
- Optimize high-lag event processing

### Event Failure Detection

**Failure Monitoring**:
- Track failed event processing
- Categorize failure types
- Monitor failure rates over time
- Alert on failure rate spikes

**Failure Analysis**:
- Root cause analysis for failures
- Pattern detection in failures
- Correlation with system events
- Failure recovery tracking

**Failure Alerting**:
- Alert on failure rate thresholds
- Alert on critical event failures
- Alert on repeated failures
- Escalate persistent failures

## API Health Monitoring

### API Response Time Tracking

**Response Time Metrics**:
- Track average response time per API endpoint
- Monitor p95 and p99 response times
- Track response time trends
- Alert on response time degradation

**Response Time Analysis**:
- Identify slow endpoints
- Correlate with system load
- Analyze response time patterns
- Optimize slow endpoints

### API Error Rate Monitoring

**Error Rate Metrics**:
- Track error rate per API endpoint
- Monitor error rate trends
- Categorize errors by type
- Alert on error rate spikes

**Error Analysis**:
- Root cause analysis for errors
- Pattern detection in errors
- Correlation with system events
- Error recovery tracking

### API Availability Checks

**Availability Monitoring**:
- Health check endpoints
- Uptime monitoring
- Availability percentage tracking
- Alert on availability drops

**Availability Patterns**:
- Monitor external API availability
- Track Salesforce API availability
- Monitor integration endpoints
- Track service dependencies

## Async Job Failures

### Batch Job Monitoring

**Batch Job Metrics**:
- Job execution count
- Job success/failure rates
- Job execution duration
- Records processed per job
- Job queue depth

**Batch Job Alerting**:
- Alert on job failures
- Alert on job timeouts
- Alert on low processing rates
- Alert on job queue depth

**Batch Job Analysis**:
- Identify failing job patterns
- Analyze job performance trends
- Optimize slow jobs
- Track job dependencies

### Queueable Job Monitoring

**Queueable Job Metrics**:
- Job execution count
- Job success/failure rates
- Job execution duration
- Job chain depth
- Queue depth

**Queueable Job Alerting**:
- Alert on job failures
- Alert on job timeouts
- Alert on queue depth
- Alert on chain depth limits

**Queueable Job Analysis**:
- Track job chaining patterns
- Identify failure points in chains
- Optimize job execution
- Monitor queue health

### Scheduled Job Monitoring

**Scheduled Job Metrics**:
- Job execution count
- Job success/failure rates
- Job execution duration
- Job schedule adherence
- Missed execution tracking

**Scheduled Job Alerting**:
- Alert on job failures
- Alert on missed executions
- Alert on schedule drift
- Alert on execution timeouts

**Scheduled Job Analysis**:
- Track schedule adherence
- Identify execution patterns
- Optimize job schedules
- Monitor job dependencies

### Retry Monitoring

**Retry Metrics**:
- Retry count per job
- Retry success rates
- Retry patterns
- Retry queue depth

**Retry Alerting**:
- Alert on excessive retries
- Alert on retry failures
- Alert on retry queue depth
- Escalate persistent retries

## Log Aggregation Patterns

### Centralized Logging Strategies

**Log Aggregation Approaches**:
- **Salesforce Event Monitoring**: Native Salesforce log aggregation
- **External Logging Platforms**: Splunk, ELK Stack, Datadog, etc.
- **Hybrid Approach**: Combine Salesforce and external logging

**Log Aggregation Benefits**:
- Centralized log storage
- Cross-system correlation
- Long-term log retention
- Advanced log analysis

### Log Aggregation Tools

**Salesforce Native**:
- Event Monitoring
- Debug Logs
- Transaction Security Policies
- Field Audit Trail

**External Platforms**:
- **Splunk**: Enterprise log aggregation and analysis
- **ELK Stack**: Elasticsearch, Logstash, Kibana
- **Datadog**: Cloud monitoring and logging
- **Sumo Logic**: Cloud-based log management

**Integration Patterns**:
- Platform Events to external systems
- REST API log streaming
- Batch log export
- Real-time log streaming

### Log Retention Policies

**Retention Strategies**:
- **Short-term retention**: Debug logs, transaction logs (7-30 days)
- **Medium-term retention**: Application logs, integration logs (90-180 days)
- **Long-term retention**: Audit logs, compliance logs (1-7 years)
- **Archive retention**: Historical logs for compliance

**Retention Implementation**:
- Configure retention per log type
- Automate log archival
- Compress archived logs
- Maintain retention policies

### Structured Logging Patterns

**Log Structure**:
- Consistent log format across systems
- Include correlation IDs
- Include timestamps and log levels
- Include context information

**Log Levels**:
- **DEBUG**: Detailed diagnostic information
- **INFO**: General informational messages
- **WARN**: Warning messages for potential issues
- **ERROR**: Error messages for failures
- **FATAL**: Critical errors requiring immediate attention

**Log Context**:
- User context (user ID, session ID)
- Request context (request ID, correlation ID)
- System context (org ID, environment)
- Business context (record ID, transaction ID)

## Q&A

### Q: What should I monitor in Salesforce?

**A**: Monitor: (1) **Platform Events** (events published, processed, failed, processing time), (2) **API health** (external API availability, response times, error rates), (3) **Async jobs** (Batch, Queueable, Scheduled job success/failure rates), (4) **System performance** (response times, throughput, error rates), (5) **User activity** (login failures, API usage), (6) **Data quality** (data validation failures, sync issues).

### Q: How do I set up alerting for Salesforce?

**A**: Set up alerting by: (1) **Defining alert thresholds** (error rates, response times, failure counts), (2) **Using Platform Events** to publish alert events, (3) **Configuring alert rules** (when to alert, who to notify), (4) **Integrating with external systems** (email, Slack, PagerDuty), (5) **Setting up escalation** (escalate if not acknowledged), (6) **Avoiding alert fatigue** (meaningful thresholds, avoid false positives).

### Q: How do I monitor Platform Events?

**A**: Monitor Platform Events by: (1) **Tracking metrics** (events published, processed, failed, processing time), (2) **Monitoring trends** over time, (3) **Setting up alerts** for high failure rates, (4) **Tracking event lag** (delay between publication and processing), (5) **Monitoring retry counts** for failed events, (6) **Correlating events** using correlation IDs.

### Q: How do I monitor async job health?

**A**: Monitor async jobs by: (1) **Tracking job status** (success, failure, in progress), (2) **Monitoring job completion rates**, (3) **Tracking job execution time**, (4) **Monitoring retry counts** and patterns, (5) **Setting up alerts** for job failures, (6) **Tracking job queue depth** (jobs waiting to execute), (7) **Monitoring governor limit usage** in jobs.

### Q: What is structured logging and why should I use it?

**A**: **Structured logging** uses consistent log formats (JSON, key-value pairs) for better analysis. Benefits: (1) **Easier log parsing** and analysis, (2) **Better correlation** across systems, (3) **Easier filtering** and searching, (4) **Better integration** with log aggregation tools. Include correlation IDs, timestamps, log levels, and context information.

### Q: How do I aggregate logs from Salesforce?

**A**: Aggregate logs by: (1) **Using Salesforce Event Monitoring** for native log aggregation, (2) **Using external platforms** (Splunk, ELK Stack, Datadog), (3) **Publishing log events** via Platform Events, (4) **Streaming logs** via REST API, (5) **Exporting logs** in batches, (6) **Centralizing logs** for correlation and analysis. Choose approach based on retention needs and analysis requirements.

### Q: What log retention policies should I use?

**A**: Use retention policies: (1) **Short-term** (7-30 days) - Debug logs, transaction logs, (2) **Medium-term** (90-180 days) - Application logs, integration logs, (3) **Long-term** (1-7 years) - Audit logs, compliance logs, (4) **Archive** - Historical logs for compliance. Configure retention per log type based on business and compliance requirements.

### Q: How do I avoid alert fatigue?

**A**: Avoid alert fatigue by: (1) **Setting meaningful thresholds** (not too sensitive), (2) **Grouping related alerts** (avoid duplicate alerts), (3) **Using alert severity** (critical, warning, info), (4) **Reviewing and tuning alerts** regularly, (5) **Suppressing known issues** (maintenance windows), (6) **Using alert aggregation** (group similar alerts), (7) **Ensuring alerts are actionable** (clear what to do).

### Q: What correlation IDs should I use for monitoring?

**A**: Use correlation IDs: (1) **Request ID** - unique ID per request/transaction, (2) **User ID** - track user activity, (3) **Session ID** - track user sessions, (4) **Integration Job ID** - track integration operations, (5) **Transaction ID** - track business transactions. Include correlation IDs in all logs and events to enable cross-system correlation.

### Q: How do I monitor API health for external integrations?

**A**: Monitor API health by: (1) **Tracking API availability** (uptime, response times), (2) **Monitoring error rates** (4xx, 5xx errors), (3) **Tracking API usage** (call volume, rate limits), (4) **Setting up health checks** (periodic API calls), (5) **Alerting on API failures** (unavailable, high error rates), (6) **Tracking API performance** (response times, throughput).

## Related Patterns

- [Error Handling and Logging](/rag/development/error-handling-and-logging.html) - Logging framework implementation
- [Performance Tuning](/rag/observability/performance-tuning.html) - Performance optimization and monitoring
- [Change Data Capture Patterns](/rag/integrations/change-data-capture-patterns.html) - CDC monitoring patterns
- [Event-Driven Architecture](/rag/architecture/event-driven-architecture.html) - Platform Events patterns
- [High Availability & DR](/rag/observability/ha-dr-patterns.html) - Disaster recovery and failover patterns

