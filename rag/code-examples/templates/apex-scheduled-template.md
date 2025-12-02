# Scheduled Apex Template

**Use Case**: Basic Scheduled Apex for time-based automation

**Template**:
```apex
/**
 * Scheduled class for [description]
 * Runs [frequency] at [time]
 */
global class [ClassName]Scheduled implements Schedulable {
    
    /**
     * Execute method - performs scheduled work
     * @param sc SchedulableContext
     */
    global void execute(SchedulableContext sc) {
        try {
            // Perform scheduled work
            // Example: Query records, process data, run batch jobs
            
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
            
            // Or trigger batch job
            // [BatchClassName] batch = new [BatchClassName]();
            // Id batchJobId = Database.executeBatch(batch, 200);
            
        } catch (Exception e) {
            // Log error
            System.debug('ERROR: Scheduled job failed: ' + e.getMessage());
            
            // Send error notification if needed
            // sendErrorNotification(sc.getTriggerId(), e);
            
            throw e;
        }
    }
}
```

**Usage**:
```apex
// Schedule job
[ClassName]Scheduled scheduledJob = new [ClassName]Scheduled();
String cronExpression = '0 0 2 * * ?'; // Daily at 2 AM
Id jobId = System.schedule('Job Name', cronExpression, scheduledJob);
```

**Common Cron Expressions**:
- `'0 0 0 * * ?'` - Every day at midnight
- `'0 0 2 * * ?'` - Every day at 2 AM
- `'0 0 0 ? * MON'` - Every Monday at midnight
- `'0 0 0 1 * ?'` - First day of every month at midnight
- `'0 0 * * * ?'` - Every hour
- `'0 */15 * * * ?'` - Every 15 minutes

**For Scheduled Batch**:
- Call `Database.executeBatch()` from `execute()` method
- Pass batch size and parameters

**For Error Handling**:
- Wrap execution in try-catch block
- Log errors with context
- Send error notifications
- Re-throw exceptions to mark job as failed

