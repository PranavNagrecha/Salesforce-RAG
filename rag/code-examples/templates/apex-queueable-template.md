---
layout: default
title: Queueable Apex Template
description: Documentation for Queueable Apex Template
permalink: /rag/code-examples/templates/apex-queueable-template.html
---

# Queueable Apex Template

**Use Case**: Basic Queueable for async processing

**Template**:
```apex
/**
 * Queueable class for [description]
 * Processes [what] asynchronously
 */
public class [ClassName]Queueable implements Queueable {
    
    // Add instance variables for parameters
    private [Type] parameter;
    
    /**
     * Constructor to accept parameters
     * @param parameter Description
     */
    public [ClassName]Queueable([Type] parameter) {
        this.parameter = parameter;
    }
    
    /**
     * Execute method - performs async work
     * @param context QueueableContext
     */
    public void execute(QueueableContext context) {
        try {
            // Perform async work
            // Example: Query records, process data, perform callouts
            
            // Query records if needed
            List<[ObjectName]> records = [
                SELECT Id, [Field1], [Field2]
                FROM [ObjectName]
                WHERE [Conditions]
                WITH SECURITY_ENFORCED
            ];
            
            // Process records
            for ([ObjectName] record : records) {
                // Process each record
            }
            
            // Perform DML if needed
            // update records;
            
        } catch (Exception e) {
            // Log error
            System.debug('ERROR: Queueable job failed: ' + e.getMessage());
            throw e;
        }
    }
}
```

**Usage**:
```apex
// Enqueue job
[ClassName]Queueable job = new [ClassName]Queueable(parameter);
Id jobId = System.enqueueJob(job);
```

**For Chained Queueable**:
- Enqueue next job from `execute()` method
- Pass data via constructor parameters
- Can chain up to 50 Queueable jobs

**For Queueable with Callouts**:
- Perform callouts in `execute()` method
- Use Named Credentials for endpoints
- Handle callout errors appropriately

**For Retry Logic**:
- Add retry count parameter to constructor
- Implement exponential backoff
- Retry up to maximum attempts