---
layout: default
title: Apex Batch Template
description: Code examples for Apex Batch Template
permalink: /rag/code-examples/templates/apex-batch-template.html
---

# Batch Apex Template

**Use Case**: Basic stateless Batch Apex for bulk processing

**Template**:
```apex
/**
 * Batch class for [description]
 * Processes records in batches of 200
 */
global class [ClassName]Batch implements Database.Batchable<SObject> {
    
    // Add instance variables for parameters if needed
    // private String parameter;
    
    /**
     * Constructor (optional)
     * @param parameter Description
     */
    public [ClassName]Batch() {
        // Initialize parameters
    }
    
    /**
     * Start method - returns QueryLocator for batch processing
     * @param bc BatchableContext
     * @return Database.QueryLocator
     */
    global Database.QueryLocator start(Database.BatchableContext bc) {
        return Database.getQueryLocator([
            SELECT Id, [Field1], [Field2]
            FROM [ObjectName]
            WHERE [Conditions]
            WITH SECURITY_ENFORCED
        ]);
    }
    
    /**
     * Execute method - processes each batch of records
     * @param bc BatchableContext
     * @param scope List of records in current batch
     */
    global void execute(Database.BatchableContext bc, List<[ObjectName]> scope) {
        List<[ObjectName]> recordsToUpdate = new List<[ObjectName]>();
        
        for ([ObjectName] record : scope) {
            // Process each record
            // record.Field1 = newValue;
            recordsToUpdate.add(record);
        }
        
        if (!recordsToUpdate.isEmpty()) {
            update recordsToUpdate;
        }
    }
    
    /**
     * Finish method - called after all batches complete
     * @param bc BatchableContext
     */
    global void finish(Database.BatchableContext bc) {
        // Query job status
        AsyncApexJob job = [
            SELECT Id, Status, NumberOfErrors, JobItemsProcessed, TotalJobItems
            FROM AsyncApexJob
            WHERE Id = :bc.getJobId()
        ];
        
        // Log completion
        System.debug('Batch job completed: ' + job.Status);
        System.debug('Records processed: ' + job.JobItemsProcessed);
        System.debug('Errors: ' + job.NumberOfErrors);
    }
}
```

**Usage**:
```apex
// Execute batch job
[ClassName]Batch batch = new [ClassName]Batch();
Id jobId = Database.executeBatch(batch, 200);
```

**For Stateful Batch**:
- Add `implements Database.Batchable<SObject>, Database.Stateful`
- Add instance variables to maintain state
- Update state in `execute()` method
- Use state in `finish()` method

**For Batch Chaining**:
- Call `Database.executeBatch()` from `finish()` method
- Pass parameters to next batch via constructor

