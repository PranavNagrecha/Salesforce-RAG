# Integration Platform Patterns

## Overview

Integration platforms serve as middleware between Salesforce and external systems, handling security, transformation, and orchestration. Two primary platforms are used: MuleSoft (for security boundaries and transformation) and Dell Boomi (for high-volume ETL operations).

## MuleSoft Integration Platform

### Use Case: Security and Transformation Boundary

MuleSoft serves as a security and transformation boundary between Salesforce and external systems, particularly in public sector implementations with strict network and compliance requirements.

### Architecture Pattern

**Security Boundary**:
- Handles VPN requirements for accessing external systems
- Manages IP whitelisting at the integration platform level
- Provides a single point of network control for multiple external systems
- Abstracts network complexity from Salesforce developers

**Transformation Layer**:
- Performs data transformation in MuleSoft (DataWeave), not in Salesforce
- Maps external system data models to Salesforce-friendly formats
- Handles environment-specific quirks and endpoint variations
- Centralizes transformation logic for maintainability

**API Management**:
- Manages API authentication (X-API-Key headers, OAuth)
- Handles environment-specific endpoint configurations
- Provides API versioning and routing
- Manages API specifications (XML exports when live Swagger access restricted)

### Implementation Patterns

**Synchronous REST API Calls**:
- Salesforce → MuleSoft → External System
- MuleSoft handles network security (VPN, IP whitelisting)
- DataWeave transformations in MuleSoft
- Standardized error responses returned to Salesforce

**Configuration Management**:
- Environment-specific endpoints managed in MuleSoft
- API keys stored securely in MuleSoft's secure properties
- Custom Metadata Types in Salesforce for interface configuration
- Named Credentials in Salesforce pointing to MuleSoft endpoints

**Error Handling**:
- Comprehensive error handling in MuleSoft flows
- Standardized error responses to Salesforce
- Retry logic for transient failures
- Logging for troubleshooting connectivity and data issues

### Best Practices

**Network Security**:
- Centralize all network security requirements at MuleSoft layer
- Abstract network complexity from Salesforce
- Document all network paths and security controls for compliance

**Data Transformation**:
- Perform transformation in MuleSoft, not Salesforce
- Use DataWeave for complex mappings
- Handle environment-specific variations in MuleSoft

**API Management**:
- Store API keys securely in MuleSoft's secure properties
- Use X-API-Key headers as required by external systems
- Rotate API keys regularly
- Document API key usage and access requirements

**Error Handling**:
- Implement comprehensive error handling in MuleSoft flows
- Return standardized error responses to Salesforce
- Log all integration errors for troubleshooting
- Use MuleSoft's error handling framework (on-error-continue, on-error-propagate)

## Dell Boomi Integration Platform

### Use Case: High-Volume ETL Operations

Dell Boomi serves as the primary ETL platform for high-volume batch integrations, particularly for synchronizing large data sets between legacy systems and Salesforce.

### Architecture Pattern

**High-Volume Batch Processing**:
- Handles hundreds of thousands of records per run
- File-based staging for very large ID lists
- Dynamic SQL IN-clause batching for database queries
- Idempotent upserts using External IDs

**File-Based Staging**:
- Large ID lists written to disk as files
- Files read back and dynamically split into batched SQL IN-clause queries
- Database processes queries in manageable chunks (1,000 IDs per IN clause)
- Results returned in structured payloads

**Reusable Components**:
- Standardized processes for logging, error handling, notifications
- Reusable connector configurations for common systems
- Consistent naming conventions and folder structure
- Template processes for common patterns

### Implementation Patterns

**Oracle Database Integration**:
- Dynamically split large ID lists into SQL IN-clause batches
- Use parameterized queries to prevent SQL injection
- Handle Oracle-specific data types and formats
- Implement connection pooling for efficiency

**Salesforce Integration via Boomi**:
- Use upsert operations with External IDs for idempotent synchronization
- Respect Salesforce API limits (typically 2,000 records per call)
- Implement retry logic for API limit exceptions
- Use bulk API when processing large volumes

**Job Tracking**:
- Integration job tracking fields on all integrated objects
- Correlation IDs linking Salesforce records to external system job logs
- Status fields: `Last_Sync_Timestamp__c`, `Last_Sync_Status__c`, `Last_Sync_Error__c`, `Integration_Job_ID__c`

### Best Practices

**Process Design**:
- Break large data sets into manageable chunks (1,000-10,000 records per batch)
- Use file-based staging for ID lists exceeding 50,000 records
- Implement error handling at every step
- Log all operations for troubleshooting and audit

**Data Transformation**:
- Map external system field names to Salesforce API names consistently
- Handle data type conversions (dates, numbers, text) explicitly
- Apply data validation rules before sending to Salesforce
- Transform null values appropriately

**Error Handling**:
- Capture error details at each step
- Send notifications (email, Slack) when critical errors occur
- Log errors to centralized logging system
- Implement dead-letter queues for unprocessable records

**Reusability**:
- Create standardized process templates
- Establish consistent naming conventions
- Organize processes in logical folder structures
- Document reusable components

## Platform Selection Criteria

### Use MuleSoft When

- **Security Requirements**: VPN, IP whitelisting, network security boundaries required
- **Transformation Complexity**: Complex data transformations needed
- **API Management**: API versioning, routing, and management required
- **Network Constraints**: Strict network security requirements
- **Multiple External Systems**: Single integration platform managing multiple systems

### Use Dell Boomi When

- **High Volume**: Processing hundreds of thousands or millions of records
- **ETL Operations**: Batch synchronization and data migration
- **Legacy Systems**: Integration with legacy systems (Oracle, mainframe)
- **File-Based Processing**: Large file-based data exchanges
- **Scheduled Jobs**: Periodic batch synchronization

## Common Patterns Across Platforms

### Error Handling

Both platforms should implement:
- Comprehensive error handling at every step
- Retry logic for transient failures
- Dead-letter queues for unprocessable records
- Standardized error logging
- Notification mechanisms for critical failures

### Logging and Monitoring

Both platforms should provide:
- Comprehensive logging for troubleshooting
- Integration with centralized logging platforms
- Dashboards showing execution metrics
- Automated alerts for failures
- Performance monitoring and trend analysis

### Configuration Management

Both platforms should support:
- Environment-specific configurations
- Secure storage of credentials and API keys
- Version management for processes and configurations
- Documentation of configurations and changes

## Integration with Salesforce

### Named Credentials

- All Salesforce-to-platform endpoints use Named Credentials
- No hardcoded URLs in Salesforce code
- Environment-specific endpoint configurations
- Centralized authentication management

### Custom Metadata Types

- Interface configuration stored in Custom Metadata Types

**Related**: [Custom Settings and Custom Metadata Patterns](rag/development/custom-settings-metadata-patterns.md) - Complete guide to Custom Settings and Custom Metadata
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

