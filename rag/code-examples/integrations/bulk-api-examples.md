---
layout: default
title: Bulk API Code Examples
description: Bulk API enables high-volume data operations in Salesforce
permalink: /rag/development/large-data-loads.html' | relative_url }}">Large Data Loads</a>

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
**Related Patterns**: <a href="{{ '/rag/development/asynchronous-apex-patterns.html' | relative_url }}">Asynchronous Apex Patterns</a>

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

- <a href="{{ '/rag/development/asynchronous-apex-patterns.html' | relative_url }}">Asynchronous Apex Patterns</a> - Async patterns

