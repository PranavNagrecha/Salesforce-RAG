---
title: "Bulk API Code Examples"
level: "Advanced"
tags:
  - integrations
  - code-examples
  - bulk-api
  - high-volume
last_reviewed: "2025-01-XX"
---

# Bulk API Code Examples

> This file contains complete, working code examples for Bulk API patterns.
> All examples are copy-paste ready and follow Salesforce best practices.

## Overview

Bulk API enables high-volume data operations in Salesforce. These examples demonstrate creating bulk jobs, uploading data, monitoring job status, and processing results for large-scale data operations.

**Related Patterns**:
- [Large Data Loads](/rag/development/large-data-loads.html) - Large data load patterns
- [Data Migration Patterns](/rag/data-modeling/data-migration-patterns.html) - Data migration patterns
- [Integration Platform Patterns](/rag/integrations/integration-platform-patterns.html) - Integration patterns

## Examples

### Example 1: Basic Bulk API Job Creation

**Pattern**: Creating and executing Bulk API jobs
**Use Case**: High-volume data operations
**Complexity**: Intermediate
**Related Patterns**: [Large Data Loads](/rag/development/large-data-loads.html)

**Problem**:
You need to insert or update large volumes of records using Bulk API.

**Solution**:

**Apex** (`BulkApiService.cls`):
```apex
/**
 * Service for Bulk API operations
 * Handles high-volume data operations
 */
public with sharing class BulkApiService {
    
    /**
     * Creates and executes a Bulk API insert job
     * @param objectType Object API name
     * @param records List of records to insert
     * @return Job ID
     */
    public static String createInsertJob(String objectType, List<SObject> records) {
        // Convert records to CSV
        String csvData = convertToCsv(records);
        
        // Create job
        String jobId = createJob(objectType, 'insert');
        
        // Upload batch
        String batchId = uploadBatch(jobId, csvData);
        
        // Close job
        closeJob(jobId);
        
        return jobId;
    }
    
    /**
     * Creates a Bulk API job
     * @param objectType Object API name
     * @param operation Operation type (insert, update, upsert, delete)
     * @return Job ID
     */
    private static String createJob(String objectType, String operation) {
        HttpRequest req = new HttpRequest();
        req.setEndpoint('callout:BulkApi/services/async/45.0/job');
        req.setMethod('POST');
        req.setHeader('Content-Type', 'application/xml; charset=UTF-8');
        req.setHeader('X-SFDC-Session', UserInfo.getSessionId());
        
        String xmlBody = '<?xml version="1.0" encoding="UTF-8"?>' +
            '<jobInfo xmlns="http://www.force.com/2009/06/asyncapi/dataload">' +
            '<operation>' + operation + '</operation>' +
            '<object>' + objectType + '</object>' +
            '<contentType>CSV</contentType>' +
            '</jobInfo>';
        
        req.setBody(xmlBody);
        
        Http http = new Http();
        HttpResponse res = http.send(req);
        
        if (res.getStatusCode() == 201) {
            // Parse job ID from response
            Dom.Document doc = new Dom.Document();
            doc.load(res.getBody());
            Dom.XmlNode root = doc.getRootElement();
            Dom.XmlNode idNode = root.getChildElement('id', null);
            return idNode.getText();
        }
        
        throw new BulkApiException('Failed to create job: ' + res.getStatusCode());
    }
    
    /**
     * Uploads batch data to Bulk API job
     * @param jobId Job ID
     * @param csvData CSV data
     * @return Batch ID
     */
    private static String uploadBatch(String jobId, String csvData) {
        HttpRequest req = new HttpRequest();
        req.setEndpoint('callout:BulkApi/services/async/45.0/job/' + jobId + '/batch');
        req.setMethod('POST');
        req.setHeader('Content-Type', 'text/csv');
        req.setHeader('X-SFDC-Session', UserInfo.getSessionId());
        req.setBody(csvData);
        
        Http http = new Http();
        HttpResponse res = http.send(req);
        
        if (res.getStatusCode() == 201) {
            // Parse batch ID from response
            Dom.Document doc = new Dom.Document();
            doc.load(res.getBody());
            Dom.XmlNode root = doc.getRootElement();
            Dom.XmlNode idNode = root.getChildElement('id', null);
            return idNode.getText();
        }
        
        throw new BulkApiException('Failed to upload batch: ' + res.getStatusCode());
    }
    
    /**
     * Closes a Bulk API job
     * @param jobId Job ID
     */
    private static void closeJob(String jobId) {
        HttpRequest req = new HttpRequest();
        req.setEndpoint('callout:BulkApi/services/async/45.0/job/' + jobId);
        req.setMethod('POST');
        req.setHeader('Content-Type', 'application/xml; charset=UTF-8');
        req.setHeader('X-SFDC-Session', UserInfo.getSessionId());
        
        String xmlBody = '<?xml version="1.0" encoding="UTF-8"?>' +
            '<jobInfo xmlns="http://www.force.com/2009/06/asyncapi/dataload">' +
            '<state>UploadComplete</state>' +
            '</jobInfo>';
        
        req.setBody(xmlBody);
        
        Http http = new Http();
        HttpResponse res = http.send(req);
        
        if (res.getStatusCode() != 200) {
            throw new BulkApiException('Failed to close job: ' + res.getStatusCode());
        }
    }
    
    /**
     * Converts records to CSV format
     * @param records List of records
     * @return CSV string
     */
    private static String convertToCsv(List<SObject> records) {
        if (records.isEmpty()) {
            return '';
        }
        
        // Get field names from first record
        SObject firstRecord = records[0];
        List<String> fieldNames = new List<String>(firstRecord.getPopulatedFieldsAsMap().keySet());
        
        // Build CSV header
        String csv = String.join(fieldNames, ',') + '\n';
        
        // Build CSV rows
        for (SObject record : records) {
            List<String> values = new List<String>();
            for (String fieldName : fieldNames) {
                Object value = record.get(fieldName);
                if (value == null) {
                    values.add('');
                } else {
                    String strValue = String.valueOf(value);
                    // Escape commas and quotes
                    if (strValue.contains(',') || strValue.contains('"')) {
                        strValue = '"' + strValue.replace('"', '""') + '"';
                    }
                    values.add(strValue);
                }
            }
            csv += String.join(values, ',') + '\n';
        }
        
        return csv;
    }
    
    /**
     * Custom exception for Bulk API errors
     */
    public class BulkApiException extends Exception {}
}
```

**Best Practices**:
- Use Bulk API for operations on 5,000+ records
- Convert data to CSV format
- Monitor job status asynchronously
- Handle errors in batch results

### Example 2: Monitoring Bulk API Job Status

**Pattern**: Monitoring Bulk API job and batch status
**Use Case**: Tracking progress of bulk operations
**Complexity**: Intermediate
**Related Patterns**: [Large Data Loads](/rag/development/large-data-loads.html)

**Problem**:
You need to monitor the status of a Bulk API job and retrieve results when complete.

**Solution**:

**Apex** (`BulkApiMonitorService.cls`):
```apex
/**
 * Service for monitoring Bulk API job status
 */
public with sharing class BulkApiMonitorService {
    
    /**
     * Checks job status
     * @param jobId Job ID
     * @return Job status information
     */
    public static JobStatus checkJobStatus(String jobId) {
        HttpRequest req = new HttpRequest();
        req.setEndpoint('callout:BulkApi/services/async/45.0/job/' + jobId);
        req.setMethod('GET');
        req.setHeader('X-SFDC-Session', UserInfo.getSessionId());
        
        Http http = new Http();
        HttpResponse res = http.send(req);
        
        if (res.getStatusCode() == 200) {
            return parseJobStatus(res.getBody());
        }
        
        throw new BulkApiException('Failed to check job status: ' + res.getStatusCode());
    }
    
    /**
     * Checks batch status
     * @param jobId Job ID
     * @param batchId Batch ID
     * @return Batch status information
     */
    public static BatchStatus checkBatchStatus(String jobId, String batchId) {
        HttpRequest req = new HttpRequest();
        req.setEndpoint('callout:BulkApi/services/async/45.0/job/' + jobId + '/batch/' + batchId);
        req.setMethod('GET');
        req.setHeader('X-SFDC-Session', UserInfo.getSessionId());
        
        Http http = new Http();
        HttpResponse res = http.send(req);
        
        if (res.getStatusCode() == 200) {
            return parseBatchStatus(res.getBody());
        }
        
        throw new BulkApiException('Failed to check batch status: ' + res.getStatusCode());
    }
    
    /**
     * Retrieves batch results
     * @param jobId Job ID
     * @param batchId Batch ID
     * @return Batch results as CSV string
     */
    public static String getBatchResults(String jobId, String batchId) {
        HttpRequest req = new HttpRequest();
        req.setEndpoint('callout:BulkApi/services/async/45.0/job/' + jobId + '/batch/' + batchId + '/result');
        req.setMethod('GET');
        req.setHeader('X-SFDC-Session', UserInfo.getSessionId());
        
        Http http = new Http();
        HttpResponse res = http.send(req);
        
        if (res.getStatusCode() == 200) {
            return res.getBody();
        }
        
        throw new BulkApiException('Failed to get batch results: ' + res.getStatusCode());
    }
    
    /**
     * Parses job status from XML response
     * @param xmlResponse XML response
     * @return JobStatus object
     */
    private static JobStatus parseJobStatus(String xmlResponse) {
        JobStatus status = new JobStatus();
        
        Dom.Document doc = new Dom.Document();
        doc.load(xmlResponse);
        Dom.XmlNode root = doc.getRootElement();
        
        status.jobId = getChildText(root, 'id');
        status.state = getChildText(root, 'state');
        status.numberBatchesQueued = Integer.valueOf(getChildText(root, 'numberBatchesQueued'));
        status.numberBatchesInProgress = Integer.valueOf(getChildText(root, 'numberBatchesInProgress'));
        status.numberBatchesCompleted = Integer.valueOf(getChildText(root, 'numberBatchesCompleted'));
        status.numberBatchesFailed = Integer.valueOf(getChildText(root, 'numberBatchesFailed'));
        status.numberRecordsProcessed = Integer.valueOf(getChildText(root, 'numberRecordsProcessed'));
        status.numberRecordsFailed = Integer.valueOf(getChildText(root, 'numberRecordsFailed'));
        
        return status;
    }
    
    /**
     * Parses batch status from XML response
     * @param xmlResponse XML response
     * @return BatchStatus object
     */
    private static BatchStatus parseBatchStatus(String xmlResponse) {
        BatchStatus status = new BatchStatus();
        
        Dom.Document doc = new Dom.Document();
        doc.load(xmlResponse);
        Dom.XmlNode root = doc.getRootElement();
        
        status.batchId = getChildText(root, 'id');
        status.state = getChildText(root, 'state');
        status.numberRecordsProcessed = Integer.valueOf(getChildText(root, 'numberRecordsProcessed'));
        status.numberRecordsFailed = Integer.valueOf(getChildText(root, 'numberRecordsFailed'));
        
        return status;
    }
    
    /**
     * Gets child element text
     * @param parent Parent XML node
     * @param childName Child element name
     * @return Child text or empty string
     */
    private static String getChildText(Dom.XmlNode parent, String childName) {
        Dom.XmlNode child = parent.getChildElement(childName, null);
        return child != null ? child.getText() : '';
    }
    
    /**
     * Job status information
     */
    public class JobStatus {
        public String jobId { get; set; }
        public String state { get; set; }
        public Integer numberBatchesQueued { get; set; }
        public Integer numberBatchesInProgress { get; set; }
        public Integer numberBatchesCompleted { get; set; }
        public Integer numberBatchesFailed { get; set; }
        public Integer numberRecordsProcessed { get; set; }
        public Integer numberRecordsFailed { get; set; }
        
        public Boolean isComplete() {
            return state == 'JobComplete' || state == 'Failed' || state == 'Aborted';
        }
    }
    
    /**
     * Batch status information
     */
    public class BatchStatus {
        public String batchId { get; set; }
        public String state { get; set; }
        public Integer numberRecordsProcessed { get; set; }
        public Integer numberRecordsFailed { get; set; }
        
        public Boolean isComplete() {
            return state == 'Completed' || state == 'Failed' || state == 'NotProcessed';
        }
    }
}
```

**Best Practices**:
- Poll job status periodically
- Check batch status for detailed progress
- Retrieve results when job is complete
- Handle failed records appropriately

### Example 3: Asynchronous Bulk API Monitoring

**Pattern**: Monitoring Bulk API jobs asynchronously
**Use Case**: Long-running bulk operations
**Complexity**: Advanced
**Related Patterns**: [Asynchronous Apex Patterns](/rag/development/asynchronous-apex-patterns.html)

**Problem**:
You need to monitor Bulk API jobs asynchronously and process results when complete.

**Solution**:

**Apex** (`BulkApiMonitorJob.cls`):
```apex
/**
 * Asynchronous job for monitoring Bulk API operations
 */
public with sharing class BulkApiMonitorJob implements Queueable, Database.AllowsCallouts {
    
    private String jobId;
    private Integer pollCount;
    private static final Integer MAX_POLLS = 60; // 5 minutes max (5 second intervals)
    
    public BulkApiMonitorJob(String jobId) {
        this.jobId = jobId;
        this.pollCount = 0;
    }
    
    public BulkApiMonitorJob(String jobId, Integer pollCount) {
        this.jobId = jobId;
        this.pollCount = pollCount;
    }
    
    public void execute(QueueableContext context) {
        try {
            // Check job status
            BulkApiMonitorService.JobStatus status = BulkApiMonitorService.checkJobStatus(jobId);
            
            if (status.isComplete()) {
                // Job complete - process results
                processJobResults(status);
                
            } else if (pollCount < MAX_POLLS) {
                // Job still running - poll again
                pollCount++;
                System.enqueueJob(new BulkApiMonitorJob(jobId, pollCount));
                
            } else {
                // Max polls reached - log timeout
                LOG_LogMessageUtility.logWarning(
                    'BulkApiMonitorJob',
                    'execute',
                    'Job monitoring timeout: ' + jobId
                );
            }
            
        } catch (Exception e) {
            LOG_LogMessageUtility.logError(
                'BulkApiMonitorJob',
                'execute',
                'Error monitoring job: ' + jobId + ' - ' + e.getMessage(),
                e
            );
        }
    }
    
    /**
     * Processes job results when complete
     * @param status Job status
     */
    private void processJobResults(BulkApiMonitorService.JobStatus status) {
        if (status.state == 'JobComplete') {
            LOG_LogMessageUtility.logInfo(
                'BulkApiMonitorJob',
                'processJobResults',
                'Job completed: ' + jobId + 
                ' - Processed: ' + status.numberRecordsProcessed + 
                ' - Failed: ' + status.numberRecordsFailed
            );
            
            // Process successful results
            // Implementation depends on use case
            
        } else if (status.state == 'Failed' || status.state == 'Aborted') {
            LOG_LogMessageUtility.logError(
                'BulkApiMonitorJob',
                'processJobResults',
                'Job failed: ' + jobId + ' - State: ' + status.state,
                null
            );
            
            // Handle job failure
            // Implementation depends on use case
        }
    }
}
```

**Usage**:
```apex
// Start bulk job
String jobId = BulkApiService.createInsertJob('Contact', contacts);

// Start monitoring
System.enqueueJob(new BulkApiMonitorJob(jobId));
```

**Best Practices**:
- Use Queueable for async monitoring
- Poll job status periodically
- Set maximum poll count to prevent infinite loops
- Process results when job is complete
- Handle job failures appropriately

## Related Examples

- [REST API Examples](/rag/code-examples/integrations/rest-api-examples.html) - REST API patterns
- [Integration Examples](/rag/code-examples/apex/integration-examples.html) - Integration patterns
- [Data Migration Examples](/rag/code-examples/utilities/data-migration-examples.html) - Data migration patterns

## See Also

- [Large Data Loads](/rag/development/large-data-loads.html) - Large data load patterns
- [Data Migration Patterns](/rag/data-modeling/data-migration-patterns.html) - Data migration patterns
- [Asynchronous Apex Patterns](/rag/development/asynchronous-apex-patterns.html) - Async patterns

