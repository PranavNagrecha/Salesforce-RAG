# Locking and Concurrency Strategies (Research Layer)

> This file is **external research**, not a log of personal project history.  
> It summarizes widely accepted guidance, examples, and references for this topic.

## 1. What This Covers

This topic covers Salesforce row locking, concurrency control patterns, UNABLE_TO_LOCK_ROW error handling, retry strategies, deadlock prevention, and high-concurrency scenario management. This is a **net-new expansion topic** that doesn't directly correspond to existing RAG content, though it relates conceptually to `rag/development/apex-patterns.md`, which briefly mentions row locking error handling in the retry logic section.

This research provides comprehensive guidance on row locking mechanisms, concurrency control patterns, retry strategies with exponential backoff, deadlock prevention, and high-concurrency optimization that are widely used in the Salesforce ecosystem but may not be explicitly documented in lived experience. These patterns are especially relevant for integration-heavy systems with large data volumes and high concurrency, as seen in `rag/integrations/...`, where multiple processes may attempt to update the same records simultaneously.

This relates to the **development** domain in `rag/**`, specifically error handling, retry logic, and high-concurrency scenario management.

## 2. Consensus Best Practices

- **Implement retry logic for row locking errors**: When encountering `UNABLE_TO_LOCK_ROW` exceptions, implement retry logic with exponential backoff to handle transient locking conflicts gracefully. This prevents data loss and improves system reliability under high concurrency.

- **Use exponential backoff for retries**: Increase delay between retry attempts exponentially (e.g., 1 second, 2 seconds, 4 seconds) to reduce contention and allow locks to clear. This prevents retry storms and improves success rates.

- **Limit retry attempts**: Set maximum retry attempts (typically 3-5) to prevent infinite retry loops and ensure failed operations are logged for manual intervention. Configurable retry counts via Custom Metadata enable environment-specific tuning.

- **Design for lock-free operations when possible**: Minimize lock contention by designing operations to avoid updating the same records simultaneously. Use record-level locking only when necessary, and consider alternative patterns (event-driven, queue-based) for high-concurrency scenarios.

- **Handle partial success scenarios**: When processing collections, handle cases where some records succeed and others fail due to locking. Implement idempotent operations to allow safe retries of failed records without duplicating successful operations.

- **Use NOWAIT locking for read operations**: When reading records that may be locked, use `FOR UPDATE NOWAIT` in SOQL to fail immediately rather than waiting, enabling faster failure handling and retry logic.

- **Implement deadlock detection and prevention**: Design operations to acquire locks in consistent order to prevent deadlocks. When deadlocks occur, implement detection and retry mechanisms to resolve them automatically.

- **Monitor and log locking conflicts**: Track row locking errors, retry attempts, and lock contention patterns to identify optimization opportunities. Use logging to understand concurrency patterns and adjust retry strategies.

- **Use Queueable for retry operations**: When retries are needed, use Queueable Apex to defer retry attempts to a separate transaction context, avoiding additional governor limit consumption in the original transaction.

- **Optimize transaction scope**: Minimize the duration of transactions that hold locks by performing expensive operations (callouts, complex calculations) before acquiring locks, and releasing locks as soon as possible.

## 3. Key Patterns and Examples

### Pattern 1: Retry Logic with Exponential Backoff

**When to use**: When operations may encounter `UNABLE_TO_LOCK_ROW` exceptions due to concurrent updates, and you need to handle transient locking conflicts gracefully.

**Implementation approach**:
- Catch `DmlException` and check for `UNABLE_TO_LOCK_ROW` status code
- Implement retry loop with configurable maximum attempts
- Use exponential backoff: delay = baseDelay * (2 ^ attemptNumber)
- Add jitter (random variation) to prevent retry storms
- Log retry attempts for monitoring
- After max attempts, log failure and escalate

**Why it's recommended**: Exponential backoff reduces lock contention by spacing out retry attempts, allowing locks to clear. It prevents retry storms where multiple processes retry simultaneously, making the problem worse. This pattern is essential for high-concurrency scenarios where multiple processes update the same records.

**Example scenario**: A Contact update service encounters `UNABLE_TO_LOCK_ROW`. It retries with delays of 100ms, 200ms, 400ms (exponential backoff). If still failing after 3 attempts, it logs the error and defers to a Queueable job for later retry.

### Pattern 2: Idempotent Operations with External IDs

**When to use**: When retrying operations that may have partially succeeded, or when you need to ensure operations can be safely retried without side effects.

**Implementation approach**:
- Use External IDs for upsert operations
- Design operations to be idempotent (same input produces same result)
- Track operation status to prevent duplicate processing
- Use upsert instead of separate insert/update logic
- Handle partial success scenarios gracefully

**Why it's recommended**: Idempotent operations enable safe retries without creating duplicates or causing side effects. External IDs ensure stable record identification across retry attempts. This pattern is critical for integration scenarios where network issues or locking conflicts may cause partial failures.

**Example scenario**: An integration syncs 1,000 records. 800 succeed, 200 fail due to locking. The retry logic uses External IDs to upsert only the 200 failed records, avoiding duplicate processing of the 800 successful records.

### Pattern 3: Queueable-Based Retry Pattern

**When to use**: When you need to retry operations in a separate transaction context, avoiding additional governor limit consumption in the original transaction.

**Implementation approach**:
- Catch `UNABLE_TO_LOCK_ROW` exceptions
- Enqueue failed records to a Queueable job
- Queueable job retries the operation in a fresh transaction context
- Implement retry logic within the Queueable job
- Track retry attempts and escalate persistent failures

**Why it's recommended**: Queueable jobs execute in separate transaction contexts with fresh governor limits, allowing retries without consuming additional resources in the original transaction. This pattern is especially useful when the original transaction is near limit thresholds.

**Example scenario**: A trigger processes 200 records, and 10 fail due to locking. Instead of retrying in the trigger (consuming more limits), the trigger enqueues the 10 failed records to a Queueable job that retries them in a separate transaction.

### Pattern 4: Lock-Free Design Patterns

**When to use**: When you can design operations to avoid lock contention by using alternative patterns that don't require row-level locking.

**Implementation approach**:
- Use Platform Events for asynchronous updates instead of direct DML
- Implement queue-based processing to serialize updates
- Use custom objects for staging updates, then batch process
- Design workflows to minimize simultaneous updates to the same records
- Use record-level flags to coordinate updates without locking

**Why it's recommended**: Lock-free designs eliminate locking conflicts entirely, improving performance and reliability. While not always possible, this pattern should be considered for high-concurrency scenarios where locking becomes a bottleneck.

**Example scenario**: Instead of multiple processes directly updating Account records simultaneously, they publish Platform Events. A single subscriber processes events sequentially, eliminating lock contention.

### Pattern 5: Deadlock Prevention and Detection

**When to use**: When multiple operations may acquire locks on multiple records in different orders, creating potential deadlock scenarios.

**Implementation approach**:
- Always acquire locks in consistent order (e.g., sort by record Id before locking)
- Use `FOR UPDATE` clauses consistently across all queries
- Implement timeout mechanisms for lock acquisition
- Detect deadlocks through timeout exceptions
- Retry deadlocked operations with lock order enforcement

**Why it's recommended**: Deadlocks cause operations to hang indefinitely, degrading system performance. Consistent lock ordering prevents deadlocks, and timeout mechanisms detect and resolve them when they occur. This pattern is essential for complex workflows involving multiple record updates.

**Example scenario**: Two processes need to update Account and Contact records. Process A locks Account then Contact. Process B locks Contact then Account. This creates a deadlock. Solution: Both processes sort records by Id and lock in Id order, preventing deadlocks.

## 4. Interactions With Existing RAG

This research topic is a **net-new expansion topic** that doesn't directly correspond to existing RAG content:

**Conceptual relationship to `rag/development/apex-patterns.md`**:
- The RAG file mentions row locking error handling in the retry logic section ("Handle row locking errors (UNABLE_TO_LOCK_ROW)") and describes `ContactRetryUpdateService` with configurable retry logic. This research adds comprehensive guidance on locking mechanisms, concurrency control patterns, deadlock prevention, and advanced retry strategies that are widely accepted in the Salesforce community but not explicitly documented in lived experience.

**How this connects to RAG systems**:
- These patterns are especially relevant for integration-heavy systems described in `rag/integrations/...`, where high-concurrency scenarios and row locking conflicts are common. The retry patterns relate to error handling patterns in `rag/development/error-handling-and-logging.md`.

**Gaps filled by this research**:
- The RAG file mentions row locking error handling but doesn't cover locking mechanisms, deadlock prevention, lock-free design patterns, or comprehensive concurrency control strategies. This research adds detailed guidance on these topics that are essential for high-concurrency systems.

**Nuances added**:
- This research emphasizes exponential backoff patterns, idempotent operation design, Queueable-based retries, and deadlock prevention that complement the RAG file's focus on retry logic. It provides deeper guidance on concurrency control that is widely used in the community.

## 5. Tradeoffs and Controversies

**Retry attempt limits**: Some teams prefer aggressive retries (5-10 attempts) to maximize success rates, while others prefer conservative retries (2-3 attempts) to fail fast and escalate. The tradeoff is between success rate (more retries) and responsiveness (fewer retries). The consensus leans toward 3-5 attempts with exponential backoff.

**Synchronous vs asynchronous retries**: Some patterns retry synchronously in the same transaction, while others defer to Queueable jobs. The tradeoff is between simplicity (synchronous) and resource efficiency (asynchronous). The consensus is to use synchronous for quick retries (1-2 attempts) and asynchronous for longer retries.

**Lock-free vs locking patterns**: Lock-free designs are more complex but eliminate contention. Locking patterns are simpler but may cause conflicts. The tradeoff is between complexity (lock-free) and simplicity (locking). The consensus is to use lock-free when possible, but locking is acceptable when necessary.

**Deadlock prevention complexity**: Consistent lock ordering prevents deadlocks but adds complexity. Detecting and retrying deadlocks is simpler but may not prevent all deadlocks. The tradeoff is between prevention (complex) and detection (simple). The consensus is to implement consistent lock ordering for critical paths.

**Retry delay strategies**: Fixed delays are simpler but may not adapt to system load. Exponential backoff adapts but is more complex. The tradeoff is between simplicity (fixed) and adaptability (exponential). The consensus strongly favors exponential backoff for better performance.

These tradeoffs are **not** automatic candidates for RAG changes; they require human judgment based on system load, concurrency patterns, and business requirements.

## 6. Candidate Ideas for RAG Enhancement

- **Expand retry logic guidance in `rag/development/apex-patterns.md`**: The RAG file mentions retry logic and row locking errors but could include detailed guidance on exponential backoff patterns, retry attempt limits, and Queueable-based retry strategies.

- **Add concurrency control patterns**: Consider adding guidance on lock-free design patterns, deadlock prevention, and concurrency optimization strategies that complement existing retry logic.

- **Add idempotent operation patterns**: Consider adding guidance on designing idempotent operations with External IDs to enable safe retries without side effects.

- **Expand error handling patterns**: The RAG file mentions error handling but could include more specific guidance on handling `UNABLE_TO_LOCK_ROW` exceptions, partial success scenarios, and retry escalation patterns.

- **Add high-concurrency optimization patterns**: Consider adding guidance on optimizing operations for high-concurrency scenarios, including lock contention reduction and transaction scope optimization.

## 7. Sources Used

- Salesforce Developer Documentation: Apex Exception Handling
- Salesforce Developer Documentation: DML Statements
- Salesforce Developer Documentation: SOQL FOR UPDATE
- Trailhead: Apex Basics & Database module
- Trailhead: Asynchronous Apex module
- Official Salesforce Blogs: Error Handling Best Practices
- Salesforce Stack Exchange: Row locking and concurrency discussions
- "Advanced Apex Programming" by Dan Appleman (conceptual references on concurrency)

(Detailed sources with URLs are maintained in `Knowledge/research/sources/locking-concurrency-sources.md`)

## 8. To Evaluate

- **Retry attempt limits**: While 3-5 attempts are commonly recommended, optimal limits depend on system load, lock duration, and business requirements. The decision requires evaluation based on monitoring and testing.

- **Exponential backoff parameters**: Base delay and maximum delay values depend on typical lock duration and system load. Optimal parameters require evaluation based on actual concurrency patterns.

- **Lock-free design complexity**: The complexity of implementing lock-free patterns may not be justified for all scenarios. The decision requires evaluation based on concurrency levels and development resources.

- **Deadlock prevention strategies**: Consistent lock ordering is effective but may not be feasible for all scenarios. The decision requires evaluation based on operation complexity and lock acquisition patterns.

