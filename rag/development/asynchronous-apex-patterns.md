---
title: "Asynchronous Apex Patterns"
level: "Advanced"
tags:
  - apex
  - development
  - patterns
  - batch
  - queueable
  - scheduled
  - asynchronous
last_reviewed: "2025-01-XX"
---

# Asynchronous Apex Patterns

## Overview

This guide provides comprehensive patterns for asynchronous Apex processing, covering Batch Apex, Queueable Apex, Scheduled Apex, and @future methods. Asynchronous Apex is essential for processing large data volumes, performing long-running operations, and avoiding governor limit exceptions in synchronous contexts.

**Related Patterns**:
- [Apex Patterns](development/apex-patterns.html) - General Apex patterns and class layering
- [Governor Limits and Optimization](development/governor-limits-and-optimization.html) - Governor limit management
- [Error Handling and Logging](development/error-handling-and-logging.html) - Error handling patterns

## Prerequisites

**Required Knowledge**:
- Understanding of Apex programming fundamentals
- Knowledge of governor limits and when they apply
- Understanding of Salesforce transaction model
- Familiarity with DML operations and SOQL queries

**Recommended Reading**:
- [Apex Patterns](development/apex-patterns.html) - Apex class structure and patterns
- [Governor Limits and Optimization](development/governor-limits-and-optimization.html) - Limit management
- [Order of Execution](development/order-of-execution.html) - Transaction execution order
- [Error Handling and Logging](development/error-handling-and-logging.html) - Error handling patterns

## Consensus Best Practices

- **Use Batch Apex for large data volumes**: Process thousands or millions of records in batches
- **Use Queueable for chaining and callouts**: Chain jobs together or perform callouts after DML
- **Use Scheduled Apex for time-based operations**: Run periodic maintenance and scheduled tasks
- **Migrate from @future to Queueable**: Queueable provides better error handling and chaining capabilities
- **Always implement error handling**: Handle exceptions gracefully and log errors
- **Monitor job status**: Track job execution and handle failures appropriately
- **Use stateful batches when needed**: Maintain state across batch executions when required
- **Test with realistic data volumes**: Test async jobs with production-like data volumes

## Decision Framework: When to Use Each Type

### Use Batch Apex When:
- Processing **thousands or millions of records**
- Need to process records in **batches of 200**
- Operations exceed **synchronous governor limits**
- Need **separate transaction contexts** for each batch
- Processing **large data migrations** or **bulk updates**

### Use Queueable Apex When:
- Need to **chain jobs together** (job A → job B → job C)
- Performing **callouts after DML** operations
- Need **lightweight async processing** (smaller than batch)
- Need **better error handling** than @future methods
- Processing **up to 50,000 records** (less than batch scale)

### Use Scheduled Apex When:
- Need **time-based automation** (daily, weekly, monthly)
- Running **periodic maintenance** tasks
- Need **recurring scheduled tasks**
- Scheduling **batch jobs** to run on a schedule
- Need **cron-based execution**

### Use @future Methods When:
- **Legacy code** that hasn't been migrated yet
- Simple **fire-and-forget** async operations
- **Migrating to Queueable** is not immediately feasible
- **Note**: Prefer Queueable for new development

## Batch Apex Patterns

### Pattern 1: Basic Stateless Batch Apex

**When to use**: Processing large datasets without maintaining state between batches.

**Implementation approach**:
- Implement `Database.Batchable<SObject>` interface
- Use `Database.QueryLocator` for SOQL-based batches
- Process records in `execute()` method
- Handle errors in `finish()` method

**Why it's recommended**: Stateless batches are simpler and more efficient when state isn't needed. They're ideal for bulk updates, data transformations, and large-scale processing.

**Example scenario**: Updating 100,000 Contact records with a new field value. Each batch of 200 records processes independently without maintaining state.

**Key Points**:
- Stateless batches are faster and use less memory
- Each batch executes in a separate transaction
- No state is maintained between batches
- Ideal for simple bulk operations

### Pattern 2: Stateful Batch Apex

**When to use**: Need to maintain state across batch executions (counters, aggregations, processed IDs).

**Implementation approach**:
- Implement `Database.Batchable<SObject>` interface
- Use instance variables to maintain state
- Update state in `execute()` method
- Use state in `finish()` method

**Why it's recommended**: Stateful batches allow maintaining state across all batch executions, enabling complex processing logic that requires aggregation or tracking.

**Example scenario**: Calculating total revenue across all Opportunities. Each batch adds to a running total, and the final total is calculated in `finish()`.

**Key Points**:
- State is maintained across all batch executions
- Instance variables persist between batches
- More memory intensive than stateless
- Use when aggregation or tracking is needed

### Pattern 3: Batch Chaining

**When to use**: Need to run multiple batch jobs sequentially (Job A completes → Job B starts).

**Implementation approach**:
- Call `Database.executeBatch()` from `finish()` method
- Pass necessary parameters to next batch
- Handle chaining errors appropriately
- Monitor chain execution

**Why it's recommended**: Batch chaining allows breaking large operations into sequential steps, each with fresh governor limits. This is essential for multi-step data processing.

**Example scenario**: Data migration with three steps: (1) Import accounts, (2) Import contacts, (3) Link contacts to accounts. Each step runs as a separate batch job.

**Key Points**:
- Each chained batch has fresh governor limits
- Can chain multiple batches sequentially
- Monitor chain execution to detect failures
- Use for multi-step data processing

### Pattern 4: Batch Error Handling and Retry

**When to use**: Need to handle errors gracefully and retry failed batches.

**Implementation approach**:
- Implement `Database.BatchableContext` for job tracking
- Use try-catch blocks in `execute()` method
- Log errors to custom logging object
- Implement retry logic for failed batches
- Use `Database.executeBatch()` with retry count

**Why it's recommended**: Proper error handling ensures batch jobs don't fail silently and allows retrying failed operations. This is critical for production reliability.

**Example scenario**: Processing 50,000 records where some may fail validation. Errors are logged, and failed records are retried in a separate batch job.

**Key Points**:
- Always implement error handling in batches
- Log errors for debugging and monitoring
- Retry failed batches with exponential backoff
- Monitor batch job status

### Pattern 5: Batch Monitoring and Job Status

**When to use**: Need to monitor batch job execution and track status.

**Implementation approach**:
- Query `AsyncApexJob` object for job status
- Track job progress and completion
- Monitor job failures and errors
- Implement job status notifications

**Why it's recommended**: Monitoring batch jobs allows detecting failures early and tracking long-running operations. This is essential for production operations.

**Example scenario**: Nightly batch job processes 1 million records. Monitoring tracks progress, sends notifications on completion, and alerts on failures.

**Key Points**:
- Query `AsyncApexJob` for job status
- Track `Status`, `NumberOfErrors`, `JobItemsProcessed`
- Implement notifications for job completion
- Monitor job execution time

## Queueable Apex Patterns

### Pattern 1: Basic Queueable

**When to use**: Simple async processing that doesn't require batching.

**Implementation approach**:
- Implement `Queueable` interface
- Implement `execute(QueueableContext)` method
- Enqueue job using `System.enqueueJob()`
- Handle errors appropriately

**Why it's recommended**: Queueable provides a simple way to perform async operations with better error handling than @future methods. It's ideal for lightweight async processing.

**Example scenario**: Sending email notifications after record updates. The Queueable job sends emails asynchronously without blocking the main transaction.

**Key Points**:
- Simpler than Batch Apex for smaller operations
- Better error handling than @future methods
- Can process up to 50,000 records
- Executes in separate transaction context

### Pattern 2: Chained Queueable Jobs

**When to use**: Need to chain multiple async operations sequentially.

**Implementation approach**:
- Enqueue next job from `execute()` method
- Pass data between chained jobs via constructor
- Handle chaining errors appropriately
- Monitor chain execution

**Why it's recommended**: Queueable chaining allows breaking complex operations into sequential steps, each with fresh governor limits. This is more flexible than batch chaining.

**Example scenario**: Multi-step integration: (1) Query external API, (2) Transform data, (3) Update Salesforce records. Each step runs as a chained Queueable job.

**Key Points**:
- Can chain up to 50 Queueable jobs
- Each job has fresh governor limits
- Pass data via constructor parameters
- Monitor chain execution

### Pattern 3: Queueable with Callouts

**When to use**: Need to perform HTTP callouts after DML operations.

**Implementation approach**:
- Implement `Queueable` interface
- Perform callouts in `execute()` method
- Handle callout errors appropriately
- Implement retry logic for failed callouts

**Why it's recommended**: Queueable allows performing callouts after DML, which isn't possible in the same transaction. This is essential for integration scenarios.

**Example scenario**: Creating a record in Salesforce, then calling an external API to sync the data. The Queueable job performs the callout after the DML completes.

**Key Points**:
- Callouts can be performed after DML
- Not possible in same transaction as DML
- Implement retry logic for failed callouts
- Handle callout errors gracefully

### Pattern 4: Queueable Retry Pattern

**When to use**: Need to retry failed operations with exponential backoff.

**Implementation approach**:
- Track retry count in Queueable class
- Implement exponential backoff delays
- Retry failed operations up to maximum attempts
- Log errors after max retries

**Why it's recommended**: Retry logic with exponential backoff handles transient errors gracefully and improves reliability for integration scenarios.

**Example scenario**: Calling external API that may be temporarily unavailable. The Queueable job retries with increasing delays (1s, 2s, 4s) up to 3 attempts.

**Key Points**:
- Implement exponential backoff (1s, 2s, 4s, 8s)
- Set maximum retry attempts (typically 3-5)
- Log errors after max retries
- Use for transient error handling

### Pattern 5: Queueable Monitoring

**When to use**: Need to monitor Queueable job execution and track status.

**Implementation approach**:
- Query `AsyncApexJob` for job status
- Track job execution time and errors
- Implement job status notifications
- Monitor queue depth and processing time

**Why it's recommended**: Monitoring Queueable jobs allows detecting failures and tracking async operation performance. This is essential for production reliability.

**Example scenario**: Queueable job processes integration data. Monitoring tracks execution time, detects failures, and sends alerts on errors.

**Key Points**:
- Query `AsyncApexJob` for job status
- Track `Status`, `NumberOfErrors`, `JobItemsProcessed`
- Monitor queue depth
- Implement error notifications

## Scheduled Apex Patterns

### Pattern 1: Basic Scheduled Apex

**When to use**: Need to run code on a schedule (daily, weekly, monthly).

**Implementation approach**:
- Implement `Schedulable` interface
- Implement `execute(SchedulableContext)` method
- Schedule job using `System.schedule()`
- Use cron expressions for scheduling

**Why it's recommended**: Scheduled Apex provides time-based automation for periodic tasks. It's essential for maintenance, reporting, and scheduled data processing.

**Example scenario**: Daily cleanup job that deletes old records. The Scheduled Apex job runs every day at 2 AM to perform cleanup.

**Key Points**:
- Use cron expressions for scheduling
- Can schedule up to 100 jobs per org
- Jobs run in system context
- Handle errors appropriately

### Pattern 2: Cron Expression Patterns

**When to use**: Need to schedule jobs at specific times or intervals.

**Common cron expressions**:
- `0 0 * * * ?` - Every day at midnight
- `0 0 2 * * ?` - Every day at 2 AM
- `0 0 0 ? * MON` - Every Monday at midnight
- `0 0 0 1 * ?` - First day of every month at midnight
- `0 0 * * * ?` - Every hour
- `0 */15 * * * ?` - Every 15 minutes

**Why it's recommended**: Cron expressions provide flexible scheduling for various time-based requirements. Understanding cron syntax is essential for scheduled automation.

**Key Points**:
- Format: `Seconds Minutes Hours Day_of_month Month Day_of_week Year`
- Use `?` for day_of_month or day_of_week (not both)
- Test cron expressions before scheduling
- Use Salesforce's Schedule Apex UI to validate

### Pattern 3: Scheduled Batch Job

**When to use**: Need to run batch jobs on a schedule.

**Implementation approach**:
- Create Schedulable class that calls `Database.executeBatch()`
- Schedule the Schedulable class
- Pass batch size and parameters
- Monitor scheduled batch execution

**Why it's recommended**: Scheduling batch jobs allows running large data processing operations on a schedule. This is essential for nightly syncs and periodic maintenance.

**Example scenario**: Nightly sync of 500,000 records from external system. Scheduled Apex triggers Batch Apex job every night at 1 AM.

**Key Points**:
- Schedule the Schedulable class, not the Batch class
- Pass batch size and parameters
- Monitor scheduled batch execution
- Handle scheduling errors

### Pattern 4: Scheduled Error Handling

**When to use**: Need to handle errors in scheduled jobs gracefully.

**Implementation approach**:
- Use try-catch blocks in `execute()` method
- Log errors to custom logging object
- Send error notifications
- Implement retry logic for failed schedules

**Why it's recommended**: Proper error handling ensures scheduled jobs don't fail silently and allows detecting issues early. This is critical for production reliability.

**Example scenario**: Scheduled job processes daily reports. Errors are logged and notifications sent to administrators for manual intervention.

**Key Points**:
- Always implement error handling
- Log errors for debugging
- Send error notifications
- Monitor scheduled job failures

### Pattern 5: Scheduled Job Monitoring

**When to use**: Need to monitor scheduled job execution and track status.

**Implementation approach**:
- Query `CronTrigger` and `CronJobDetail` for job status
- Track job execution time and next run time
- Monitor job failures and errors
- Implement job status notifications

**Why it's recommended**: Monitoring scheduled jobs allows detecting failures and tracking scheduled automation performance. This is essential for production operations.

**Example scenario**: Scheduled job runs daily maintenance. Monitoring tracks execution time, detects failures, and sends alerts on errors.

**Key Points**:
- Query `CronTrigger` for job status
- Track `NextFireTime`, `PreviousFireTime`, `State`
- Monitor job execution time
- Implement failure notifications

## @future Methods

### When to Use @future

**Use @future when**:
- **Legacy code** that hasn't been migrated to Queueable
- Simple **fire-and-forget** async operations
- **Migrating to Queueable** is not immediately feasible
- Need **simple async processing** without chaining

**Note**: For new development, prefer Queueable over @future methods.

### Limitations of @future Methods

- **Cannot chain jobs**: Cannot call another @future method from @future
- **Limited error handling**: Less flexible error handling than Queueable
- **No return values**: Cannot return values from @future methods
- **Parameter limitations**: Can only pass primitive types, collections of primitives, or IDs
- **No callouts after DML**: Cannot perform callouts in same transaction as DML

### Best Practices for @future Methods

- **Keep methods simple**: Avoid complex logic in @future methods
- **Handle errors appropriately**: Use try-catch blocks and log errors
- **Test thoroughly**: Test @future methods with realistic scenarios
- **Plan migration to Queueable**: Plan to migrate @future methods to Queueable

### Migration from @future to Queueable

**Migration steps**:
1. Create Queueable class with same logic
2. Replace `@future` annotation with `Queueable` interface
3. Change method signature to `execute(QueueableContext)`
4. Update callers to use `System.enqueueJob()`
5. Test thoroughly before deploying

**Benefits of migration**:
- Better error handling
- Ability to chain jobs
- More flexible parameter passing
- Better monitoring capabilities

## Tradeoffs and Implementation Decisions

### Batch Apex vs Queueable

**Use Batch Apex when**:
- Processing thousands or millions of records
- Need to process in batches of 200
- Operations exceed synchronous limits significantly

**Use Queueable when**:
- Processing smaller volumes (up to 50,000 records)
- Need to chain jobs together
- Performing callouts after DML
- Need better error handling than @future

**Tradeoff**: Batch Apex is more efficient for large volumes but less flexible. Queueable is more flexible but limited to smaller volumes.

### Stateful vs Stateless Batch

**Use Stateful when**:
- Need to maintain state across batches
- Aggregating data across batches
- Tracking processed records

**Use Stateless when**:
- No state needed between batches
- Simple bulk operations
- Performance is critical

**Tradeoff**: Stateful batches are more flexible but use more memory. Stateless batches are faster and more efficient.

### Scheduled vs Manual Execution

**Use Scheduled when**:
- Need time-based automation
- Periodic maintenance tasks
- Recurring operations

**Use Manual when**:
- One-time operations
- On-demand processing
- Testing and debugging

**Tradeoff**: Scheduled provides automation but less control. Manual execution provides control but requires manual intervention.

## Edge Cases and Limitations

### Batch Apex Job Failures

**Scenario**: Batch Apex jobs may fail due to governor limits, data issues, or system errors.

**Consideration**:
- Implement error handling in `execute()` and `finish()` methods
- Use Database methods with `allOrNone=false` for partial success
- Log failures for troubleshooting and retry
- Monitor job status and implement retry mechanisms

### Queueable Chaining Limits

**Scenario**: Queueable jobs can be chained, but there are limits on chain depth.

**Consideration**:
- Maximum chain depth is 2 (Queueable → Queueable → Queueable)
- Plan chain depth carefully to avoid hitting limits
- Consider using Platform Events for deeper chains
- Monitor chain depth and adjust as needed

### Scheduled Job Conflicts

**Scenario**: Multiple scheduled jobs may conflict or overlap.

**Consideration**:
- Use `System.abortJob()` to prevent overlapping executions
- Implement job status checking before scheduling
- Use Custom Metadata to configure job schedules
- Monitor job execution and handle conflicts

### Large Data Volume Processing

**Scenario**: Processing millions of records in Batch Apex may take hours or days.

**Consideration**:
- Break large operations into smaller batches if possible
- Monitor batch progress and implement checkpoints
- Consider using Bulk API for very large operations
- Plan for long-running jobs and user expectations

### Limitations

- **Batch size**: Batch Apex processes 200 records per batch; cannot be changed
- **Queueable depth**: Maximum chain depth of 2 for Queueable jobs
- **Scheduled frequency**: Minimum scheduling interval is 1 hour
- **Job limits**: Limited concurrent jobs (5 Batch, 50 Queueable, 100 Scheduled)
- **Transaction limits**: Each async job has its own governor limits

## Q&A

### Q: When should I use Batch Apex vs Queueable vs Scheduled Apex?

**A**: Use **Batch Apex** for processing thousands or millions of records in batches of 200. Use **Queueable** for chaining jobs, performing callouts after DML, or lightweight async processing. Use **Scheduled Apex** for time-based operations and periodic maintenance tasks.

### Q: What is the difference between stateful and stateless Batch Apex?

**A**: **Stateful** batches maintain state across batch executions using instance variables, useful for aggregating data or tracking processed records. **Stateless** batches don't maintain state between executions, making them faster and more efficient for simple bulk operations.

### Q: Can I chain Queueable jobs?

**A**: Yes, Queueable jobs can chain up to **50 jobs** in a single transaction. Chain jobs by calling `System.enqueueJob()` from within a Queueable's `execute()` method. This enables sequential processing where one job triggers the next.

### Q: Should I use @future methods or Queueable?

**A**: For new development, prefer **Queueable** over @future methods. Queueable provides better error handling, ability to chain jobs, more flexible parameter passing, and better monitoring. Migrate existing @future methods to Queueable when possible.

### Q: What are the governor limits for async Apex?

**A**: **Batch Apex**: 50 concurrent batch jobs, 250,000 batch executions per 24 hours. **Queueable**: 50 chained jobs per transaction, 50,000 Queueable jobs per 24 hours. **Scheduled**: 100 scheduled jobs per org. Each async context has its own governor limits (separate from synchronous limits).

### Q: How do I monitor async job execution?

**A**: Query `AsyncApexJob` for Batch and Queueable jobs, query `CronTrigger` and `CronJobDetail` for Scheduled jobs, monitor job status (Queued, Processing, Completed, Failed), track execution time and errors, and implement notifications for job failures.

### Q: Can I perform callouts in async Apex?

**A**: Yes, async Apex (Batch, Queueable, Scheduled) can perform callouts. Queueable is particularly useful for callouts after DML operations, as it can perform callouts in the same transaction context. Batch and Scheduled can also perform callouts within their execution contexts.

### Q: How do I handle errors in async Apex?

**A**: Implement try-catch blocks in async methods, log errors to custom logging objects, send error notifications, implement retry logic for failed jobs, monitor job failures, and handle partial failures gracefully. Use `Database.executeBatch()` with error handling for Batch Apex.

## Related Patterns

**See Also**:
- [Apex Patterns](development/apex-patterns.html) - General Apex patterns
- [Governor Limits and Optimization](development/governor-limits-and-optimization.html) - Governor limit management
- [Error Handling and Logging](development/error-handling-and-logging.html) - Error handling patterns

**Related Domains**:
- [Batch Examples](code-examples/apex/batch-examples.html) - Complete Batch Apex code examples
- [Queueable Examples](code-examples/apex/queueable-examples.html) - Complete Queueable code examples
- [Scheduled Examples](code-examples/apex/scheduled-examples.html) - Complete Scheduled Apex code examples

