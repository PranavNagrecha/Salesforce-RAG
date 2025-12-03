# Scheduled Apex Code Examples

> Complete, working code examples for Scheduled Apex patterns.
> All examples are copy-paste ready and follow Salesforce best practices.

## Overview

Scheduled Apex provides time-based automation for periodic tasks. It's used for maintenance, reporting, and scheduled data processing using cron expressions.

**Related Patterns**:
- [Asynchronous Apex Patterns](/Salesforce-RAG/rag/development/asynchronous-apex-patterns.html#scheduled-apex-patterns)
- <a href="{{ '/rag/development/error-handling-and-logging.html' | relative_url }}">Error Handling and Logging</a>

## Examples

### Example 1: Basic Scheduled Apex

**Pattern**: Basic Scheduled Apex with cron expression
**Use Case**: Daily cleanup or maintenance tasks
**Complexity**: Basic
**Related Patterns**: [Basic Scheduled Apex](/Salesforce-RAG/rag/development/asynchronous-apex-patterns.html#pattern-1-basic-scheduled-apex)

**Problem**:
You need to run a daily cleanup job that deletes old records. The Scheduled Apex job runs every day at 2 AM to perform cleanup.

**Solution**:

```apex
/**
 * Scheduled class for daily cleanup
 * Runs every day at 2 AM
 */
global class DailyCleanupScheduled implements Schedulable {
    
    /**
     * Execute method - performs cleanup
     * @param sc SchedulableContext
     */
    global void execute(SchedulableContext sc) {
        // Delete old records (older than 90 days)
        Date cutoffDate = Date.today().addDays(-90);
        
        List<Contact> oldContacts = [
            SELECT Id
            FROM Contact
            WHERE CreatedDate < :cutoffDate
            AND Status__c = 'Inactive'
            WITH SECURITY_ENFORCED
        ];
        
        if (!oldContacts.isEmpty()) {
            delete oldContacts;
            System.debug('Deleted ' + oldContacts.size() + ' old contacts');
        }
    }
}
```

**Explanation**:
- Implements `Schedulable` interface
- `execute()` method performs scheduled work
- Runs in system context
- Uses cron expression for scheduling

**Usage**:

```apex
// Schedule job to run daily at 2 AM
// Cron: 0 0 2 * * ? (Seconds Minutes Hours Day Month DayOfWeek Year)
String cronExpression = '0 0 2 * * ?';
String jobName = 'Daily Cleanup';
DailyCleanupScheduled scheduledJob = new DailyCleanupScheduled();
Id jobId = System.schedule(jobName, cronExpression, scheduledJob);
```

**Test Example**:

```apex
@isTest
private class DailyCleanupScheduledTest {
    
    @isTest
    static void testScheduledExecution() {
        // Create old test records
        List<Contact> oldContacts = new List<Contact>();
        for (Integer i = 0; i < 10; i++) {
            oldContacts.add(new Contact(
                LastName = 'Old' + i,
                Status__c = 'Inactive',
                CreatedDate = Date.today().addDays(-100)
            ));
        }
        insert oldContacts;
        
        Test.startTest();
        DailyCleanupScheduled scheduledJob = new DailyCleanupScheduled();
        String cronExpression = '0 0 2 * * ?';
        Id jobId = System.schedule('Test Daily Cleanup', cronExpression, scheduledJob);
        
        // Execute immediately for testing
        scheduledJob.execute(null);
        Test.stopTest();
        
        // Verify old records were deleted
        List<Contact> remainingContacts = [
            SELECT Id
            FROM Contact
            WHERE LastName LIKE 'Old%'
        ];
        System.assertEquals(0, remainingContacts.size());
    }
}
```

---

### Example 2: Cron Expression Examples

**Pattern**: Various cron expressions for different scheduling needs
**Use Case**: Understanding cron syntax for scheduling
**Complexity**: Basic
**Related Patterns**: [Cron Expression Patterns](/Salesforce-RAG/rag/development/asynchronous-apex-patterns.html#pattern-2-cron-expression-patterns)

**Common Cron Expressions**:

```apex
/**
 * Examples of common cron expressions
 */
public class CronExpressionExamples {
    
    // Every day at midnight
    public static final String DAILY_MIDNIGHT = '0 0 0 * * ?';
    
    // Every day at 2 AM
    public static final String DAILY_2AM = '0 0 2 * * ?';
    
    // Every Monday at midnight
    public static final String WEEKLY_MONDAY = '0 0 0 ? * MON';
    
    // First day of every month at midnight
    public static final String MONTHLY_FIRST_DAY = '0 0 0 1 * ?';
    
    // Every hour
    public static final String HOURLY = '0 0 * * * ?';
    
    // Every 15 minutes
    public static final String EVERY_15_MINUTES = '0 */15 * * * ?';
    
    // Every 30 minutes
    public static final String EVERY_30_MINUTES = '0 */30 * * * ?';
    
    // Every weekday at 9 AM
    public static final String WEEKDAY_9AM = '0 0 9 ? * MON-FRI';
    
    // Last day of every month at 11 PM
    public static final String MONTHLY_LAST_DAY = '0 0 23 L * ?';
}
```

**Cron Expression Format**:
```
Seconds Minutes Hours Day_of_month Month Day_of_week Year
```

**Explanation**:
- Use `?` for day_of_month OR day_of_week (not both)
- Use `*` for "every" value
- Use `L` for last day of month
- Use `MON-FRI` for weekday ranges
- Use `/` for intervals (e.g., `*/15` = every 15 minutes)

**Usage**:

```apex
// Schedule with different cron expressions
DailyReportScheduled job = new DailyReportScheduled();

// Daily at 2 AM
Id job1 = System.schedule('Daily Report', CronExpressionExamples.DAILY_2AM, job);

// Weekly on Monday
Id job2 = System.schedule('Weekly Report', CronExpressionExamples.WEEKLY_MONDAY, job);

// Every 15 minutes
Id job3 = System.schedule('Frequent Check', CronExpressionExamples.EVERY_15_MINUTES, job);
```

---

### Example 3: Scheduled Batch Job

**Pattern**: Scheduled Apex that triggers Batch Apex
**Use Case**: Running batch jobs on a schedule
**Complexity**: Intermediate
**Related Patterns**: [Scheduled Batch Job](/Salesforce-RAG/rag/development/asynchronous-apex-patterns.html#pattern-3-scheduled-batch-job)

**Problem**:
You need to run a nightly sync of 500,000 records from an external system. Scheduled Apex triggers Batch Apex job every night at 1 AM.

**Solution**:

```apex
/**
 * Scheduled class that triggers Batch Apex
 */
global class ScheduledBatchTrigger implements Schedulable {
    
    /**
     * Execute method - triggers batch job
     * @param sc SchedulableContext
     */
    global void execute(SchedulableContext sc) {
        // Create and execute batch job
        ExternalSystemSyncBatch batch = new ExternalSystemSyncBatch();
        Id batchJobId = Database.executeBatch(batch, 200);
        
        System.debug('Scheduled batch job started: ' + batchJobId);
    }
}

/**
 * Batch class for syncing external system data
 */
global class ExternalSystemSyncBatch implements Database.Batchable<SObject> {
    
    global Database.QueryLocator start(Database.BatchableContext bc) {
        return Database.getQueryLocator([
            SELECT Id, Name, External_Sync_Status__c
            FROM Contact
            WHERE External_Sync_Status__c != 'Synced'
            WITH SECURITY_ENFORCED
        ]);
    }
    
    global void execute(Database.BatchableContext bc, List<Contact> scope) {
        // Sync logic here
        for (Contact contact : scope) {
            // Perform sync operation
            contact.External_Sync_Status__c = 'Synced';
        }
        update scope;
    }
    
    global void finish(Database.BatchableContext bc) {
        System.debug('Batch sync completed');
    }
}
```

**Explanation**:
- Scheduled class calls `Database.executeBatch()` in `execute()` method
- Batch job processes large data volumes
- Each batch executes with fresh governor limits
- Monitor both scheduled and batch job execution

**Usage**:

```apex
// Schedule the Schedulable class (not the Batch class)
ScheduledBatchTrigger scheduledJob = new ScheduledBatchTrigger();
String cronExpression = '0 0 1 * * ?'; // Daily at 1 AM
Id jobId = System.schedule('Nightly Sync', cronExpression, scheduledJob);
```

---

### Example 4: Scheduled with Error Handling

**Pattern**: Scheduled Apex with comprehensive error handling
**Use Case**: Scheduled jobs that need robust error handling
**Complexity**: Intermediate
**Related Patterns**: [Scheduled Error Handling](/Salesforce-RAG/rag/development/asynchronous-apex-patterns.html#pattern-4-scheduled-error-handling)

**Problem**:
You need to run a scheduled job that processes daily reports. Errors should be logged and notifications sent to administrators for manual intervention.

**Solution**:

```apex
/**
 * Scheduled class with error handling
 */
global class ScheduledReportProcessor implements Schedulable {
    
    global void execute(SchedulableContext sc) {
        try {
            // Process reports
            List<Report> reports = [
                SELECT Id, Name
                FROM Report
                WHERE LastRunDate < TODAY
                WITH SECURITY_ENFORCED
                LIMIT 100
            ];
            
            for (Report report : reports) {
                processReport(report);
            }
            
            // Log success
            System.debug('Successfully processed ' + reports.size() + ' reports');
            
        } catch (Exception e) {
            // Log error
            String errorMsg = 'Scheduled report processing failed: ' + e.getMessage();
            System.debug('ERROR: ' + errorMsg);
            
            // Send error notification
            sendErrorNotification(sc.getTriggerId(), e);
            
            // Re-throw to mark job as failed
            throw e;
        }
    }
    
    private void processReport(Report report) {
        // Report processing logic
        System.debug('Processing report: ' + report.Name);
    }
    
    private void sendErrorNotification(Id triggerId, Exception e) {
        // Query job details
        CronTrigger cronJob = [
            SELECT Id, CronJobDetail.Name, NextFireTime, State
            FROM CronTrigger
            WHERE Id = :triggerId
        ];
        
        String message = 'Scheduled job failed.\n' +
            'Job Name: ' + cronJob.CronJobDetail.Name + '\n' +
            'Next Run: ' + cronJob.NextFireTime + '\n' +
            'State: ' + cronJob.State + '\n' +
            'Error: ' + e.getMessage();
        
        System.debug('ALERT: ' + message);
        // Send email or create notification record
    }
}
```

**Explanation**:
- Wraps execution in try-catch block
- Logs errors with context
- Sends error notifications
- Re-throws exceptions to mark job as failed

**Usage**:

```apex
// Schedule job with error handling
ScheduledReportProcessor scheduledJob = new ScheduledReportProcessor();
String cronExpression = '0 0 3 * * ?'; // Daily at 3 AM
Id jobId = System.schedule('Daily Report Processor', cronExpression, scheduledJob);
```

---

### Example 5: Scheduled Job Monitoring

**Pattern**: Monitoring scheduled job execution and status
**Use Case**: Tracking scheduled automation performance
**Complexity**: Intermediate
**Related Patterns**: [Scheduled Job Monitoring](/Salesforce-RAG/rag/development/asynchronous-apex-patterns.html#pattern-5-scheduled-job-monitoring)

**Problem**:
You need to monitor scheduled job execution, track execution time, detect failures, and send alerts on errors.

**Solution**:

```apex
/**
 * Utility class for monitoring scheduled jobs
 */
public class ScheduledJobMonitor {
    
    /**
     * Get scheduled job status
     * @param jobId CronTrigger ID
     * @return CronTrigger record with job details
     */
    public static CronTrigger getJobStatus(Id jobId) {
        return [
            SELECT Id, CronJobDetail.Name, CronJobDetail.JobType,
                   NextFireTime, PreviousFireTime, State, TimesTriggered
            FROM CronTrigger
            WHERE Id = :jobId
        ];
    }
    
    /**
     * Get all scheduled jobs
     * @return List of CronTrigger records
     */
    public static List<CronTrigger> getAllScheduledJobs() {
        return [
            SELECT Id, CronJobDetail.Name, CronJobDetail.JobType,
                   NextFireTime, PreviousFireTime, State, TimesTriggered
            FROM CronTrigger
            WHERE State IN ('WAITING', 'EXECUTING', 'COMPLETE', 'ERROR', 'PAUSED')
            ORDER BY CronJobDetail.Name
        ];
    }
    
    /**
     * Check if scheduled job is running
     * @param jobId CronTrigger ID
     * @return Boolean indicating if job is running
     */
    public static Boolean isJobRunning(Id jobId) {
        CronTrigger job = getJobStatus(jobId);
        return job.State == 'EXECUTING';
    }
    
    /**
     * Get job execution history
     * @param jobName Job name to search for
     * @return List of AsyncApexJob records
     */
    public static List<AsyncApexJob> getJobExecutionHistory(String jobName) {
        return [
            SELECT Id, Status, NumberOfErrors, JobItemsProcessed,
                   CreatedDate, CompletedDate
            FROM AsyncApexJob
            WHERE ApexClass.Name = :jobName
            ORDER BY CreatedDate DESC
            LIMIT 10
        ];
    }
    
    /**
     * Abort scheduled job
     * @param jobId CronTrigger ID
     */
    public static void abortJob(Id jobId) {
        System.abortJob(jobId);
    }
}

/**
 * Scheduled class with monitoring
 */
global class MonitoredScheduledJob implements Schedulable {
    
    private DateTime startTime;
    
    global void execute(SchedulableContext sc) {
        startTime = DateTime.now();
        
        try {
            // Perform scheduled work
            performScheduledWork();
            
            // Calculate execution time
            Long executionTime = DateTime.now().getTime() - startTime.getTime();
            
            // Log success
            System.debug('Scheduled job completed successfully');
            System.debug('Execution time: ' + (executionTime / 1000) + ' seconds');
            
        } catch (Exception e) {
            // Log error
            System.debug('ERROR: Scheduled job failed: ' + e.getMessage());
            
            // Send error notification
            sendErrorNotification(sc.getTriggerId(), e);
            
            throw e;
        }
    }
    
    private void performScheduledWork() {
        // Scheduled work logic
        System.debug('Performing scheduled work');
    }
    
    private void sendErrorNotification(Id triggerId, Exception e) {
        CronTrigger job = ScheduledJobMonitor.getJobStatus(triggerId);
        
        String message = 'Scheduled job failed.\n' +
            'Job Name: ' + job.CronJobDetail.Name + '\n' +
            'Error: ' + e.getMessage();
        
        System.debug('ALERT: ' + message);
        // Send email or create notification record
    }
}
```

**Explanation**:
- Queries `CronTrigger` and `CronJobDetail` for job status
- Tracks execution time and errors
- Provides utility methods for monitoring
- Sends notifications on failures

**Usage**:

```apex
// Schedule monitored job
MonitoredScheduledJob scheduledJob = new MonitoredScheduledJob();
String cronExpression = '0 0 4 * * ?'; // Daily at 4 AM
Id jobId = System.schedule('Monitored Job', cronExpression, scheduledJob);

// Monitor job status
CronTrigger status = ScheduledJobMonitor.getJobStatus(jobId);
Boolean isRunning = ScheduledJobMonitor.isJobRunning(jobId);
List<CronTrigger> allJobs = ScheduledJobMonitor.getAllScheduledJobs();
```

---

## Related Patterns

- <a href="{{ '/rag/development/asynchronous-apex-patterns.html' | relative_url }}">Asynchronous Apex Patterns</a> - Complete async patterns guide
- <a href="{{ '/rag/development/error-handling-and-logging.html' | relative_url }}">Error Handling and Logging</a> - Error handling patterns
- <a href="{{ '/rag/code-examples/apex/code-examples/templates/apex-scheduled-template.html' | relative_url }}">Scheduled Template</a> - Scheduled Apex template

