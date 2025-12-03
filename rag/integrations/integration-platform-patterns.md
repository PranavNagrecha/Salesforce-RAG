---
layout: default
title: Integration Platform Patterns
description: Integration platforms serve as middleware between Salesforce and external systems, handling security, transformation, and orchestration
permalink: /rag/integrations/integration-platform-patterns.html
---
- Environment-specific settings (endpoints, timeouts, headers)
- Reusable across multiple integrations
- Version-controlled configuration

### Error Logging

- All errors logged to `LOG_LogMessage__c` object
- Correlation IDs linking Salesforce records to platform job logs
- Comprehensive error details for troubleshooting
- Integration with centralized logging platforms

## Best Practices Summary

### MuleSoft Best Practices

- Use as security boundary for network constraints
- Perform data transformation in MuleSoft, not Salesforce
- Centralize API authentication at MuleSoft layer
- Abstract network complexity from Salesforce
- Implement comprehensive error handling

### Boomi Best Practices

- Break large data sets into manageable chunks
- Use file-based staging for very large ID lists
- Implement comprehensive error handling and logging
- Create reusable process templates
- Track integration jobs with correlation IDs

### Common Best Practices

- Use Named Credentials for all endpoints
- Store configuration in Custom Metadata Types
- Log all operations for troubleshooting
- Implement retry logic for transient failures
- Monitor integration health and performance

## Edge Cases and Limitations

### Edge Case 1: High-Volume ETL with Network Failures

**Scenario**: Large ETL job fails mid-process due to network timeout or connection issues, requiring partial retry.

**Consideration**:
- Implement checkpoint/resume functionality in ETL processes
- Use idempotent operations with External IDs for safe retries
- Track processed records to avoid duplicate processing
- Implement exponential backoff for retry logic
- Log job progress for troubleshooting and recovery

### Edge Case 2: MuleSoft Transformation with Complex Data Structures

**Scenario**: Complex nested data structures causing DataWeave transformation failures or performance issues.

**Consideration**:
- Validate data structure before transformation
- Handle null values and missing fields gracefully
- Optimize DataWeave transformations for performance
- Test transformations with edge case data
- Implement error handling for transformation failures

### Edge Case 3: Boomi Batch Processing with Very Large Files

**Scenario**: Processing files with millions of records causing memory or timeout issues in Boomi.

**Consideration**:
- Break large files into smaller chunks for processing
- Use file-based staging for very large datasets
- Implement streaming processing for large files
- Monitor Boomi process memory usage
- Optimize batch sizes based on record complexity

### Edge Case 4: Integration Platform Authentication Failures

**Scenario**: OAuth token expiration or authentication failures during long-running integration jobs.

**Consideration**:
- Implement token refresh logic for long-running jobs
- Handle authentication errors gracefully with retry logic
- Monitor token expiration times
- Use service accounts with appropriate token lifetimes
- Implement fallback authentication mechanisms

### Edge Case 5: Multi-System Integration Coordination

**Scenario**: Coordinating integrations across multiple external systems with different response times and error handling.

**Consideration**:
- Implement circuit breakers for unreliable systems
- Use async patterns for long-running integrations
- Handle partial failures gracefully
- Implement correlation IDs for tracking across systems
- Monitor integration health across all systems

### Limitations

- **MuleSoft Performance**: DataWeave transformations have performance limits with very large datasets
- **Boomi Batch Size**: Optimal batch sizes depend on record complexity and system resources
- **Network Timeouts**: Integration platforms subject to network timeout constraints
- **API Rate Limits**: External systems may have rate limits affecting integration throughput
- **Token Expiration**: OAuth tokens expire and require refresh logic
- **File Size Limits**: File-based staging has practical size limits
- **Concurrent Job Limits**: Integration platforms have limits on concurrent jobs
- **Transformation Complexity**: Complex transformations may hit platform limits

## Q&A

### Q: When should I use MuleSoft vs Dell Boomi for integrations?

**A**: Use MuleSoft when you need a security boundary (VPN, IP whitelisting), complex data transformations (DataWeave), API management, or network security requirements. Use Dell Boomi when you need high-volume ETL operations (hundreds of thousands of records), batch synchronization, file-based processing, or integration with legacy systems (Oracle, mainframe).

### Q: How do I handle authentication in integration platforms?

**A**: Store API keys securely in the integration platform's secure properties (MuleSoft) or secure storage (Boomi). Use OAuth 2.0 Client Credentials Flow for Salesforce authentication. Use Named Credentials in Salesforce pointing to integration platform endpoints. Never hardcode credentials in code or configuration files.

### Q: How do I handle errors in integration platforms?

**A**: Implement comprehensive error handling at every step in integration flows. Use retry logic for transient failures. Implement dead-letter queues for unprocessable records. Return standardized error responses to Salesforce. Log all errors with context for troubleshooting. Send notifications (email, Slack) when critical errors occur.

### Q: How do I optimize high-volume batch integrations?

**A**: Break large data sets into manageable chunks (1,000-10,000 records per batch). Use file-based staging for ID lists exceeding 50,000 records. Implement dynamic SQL IN-clause batching for database queries. Use idempotent upsert operations with External IDs. Track integration jobs with correlation IDs and status fields.

### Q: Should I perform data transformation in Salesforce or the integration platform?

**A**: Perform data transformation in the integration platform (MuleSoft DataWeave, Boomi mapping) rather than in Salesforce. This centralizes transformation logic, handles environment-specific variations, and abstracts complexity from Salesforce developers. Salesforce should receive clean, transformed data ready for upsert.

### Q: How do I manage environment-specific configurations?

**A**: Store environment-specific endpoints and settings in the integration platform's secure properties. Use Custom Metadata Types in Salesforce for interface configuration. Use Named Credentials in Salesforce pointing to integration platform endpoints. Never hardcode environment-specific values in code.

### Q: How do I track integration job status and troubleshoot failures?

**A**: Add integration job tracking fields to all integrated objects: `Last_Sync_Timestamp__c`, `Last_Sync_Status__c`, `Last_Sync_Error__c`, `Integration_Job_ID__c`. Use correlation IDs to link Salesforce records to platform job logs. Query these fields to identify failed records and troubleshoot issues.

### Q: What is the best way to handle large ID lists in integrations?

**A**: For ID lists exceeding 50,000 records, use file-based staging. Write large ID lists to disk as files, then read them back and dynamically split into batched SQL IN-clause queries (1,000 IDs per IN clause). This prevents memory issues and allows processing of very large datasets efficiently.

### Q: How do I ensure idempotent operations in integrations?

**A**: Use External IDs on all objects receiving integration data. Use upsert operations (not insert) with External IDs. Mirror external system primary keys in External ID fields. This ensures that re-running integrations doesn't create duplicates and handles retries safely.

### Q: How do I monitor integration health and performance?

**A**: Implement comprehensive logging in integration platforms. Integrate with centralized logging platforms (OpenSearch, Splunk). Create dashboards showing execution metrics, success rates, and error rates. Set up automated alerts for failures. Monitor API response times and throughput. Track integration job completion rates and identify bottlenecks.

## Related Patterns

**See Also**:
- <a href="{{ '/rag/integrations/etl-vs-api-vs-events.html' | relative_url }}">ETL vs API vs Events</a> - Integration pattern selection framework
- <a href="{{ '/rag/integrations/integration-user-license-guide.html' | relative_url }}">Integration User License Guide</a> - Authentication and licensing for integrations
- <a href="{{ '/rag/integrations/callout-best-practices.html' | relative_url }}">Callout Best Practices</a> - HTTP callout patterns and error handling
- <a href="{{ '/rag/integrations/change-data-capture-patterns.html' | relative_url }}">Change Data Capture Patterns</a> - Real-time change notification patterns

**Related Domains**:
- <a href="{{ '/rag/data-modeling/external-ids-and-integration-keys.html' | relative_url }}">External IDs and Integration Keys</a> - Data mapping and stable record identification
- <a href="{{ '/rag/integrations/sis-sync-patterns.html' | relative_url }}">SIS Sync Patterns</a> - High-volume batch synchronization patterns
- <a href="{{ '/rag/troubleshooting/integration-debugging.html' | relative_url }}">Integration Debugging</a> - Troubleshooting integration failures
- <a href="{{ '/rag/troubleshooting/data-reconciliation.html' | relative_url }}">Data Reconciliation</a> - Reconciling data between systems

