# Apex and Test Class Lessons Learned (Research Layer)

> This file is **external research**, not a log of personal project history.  
> It summarizes widely accepted guidance, examples, and references for this topic, derived from concrete implementation experience.

## 1. What This Covers

This topic covers concrete lessons learned from Apex class and test class implementations across multiple enterprise Salesforce projects. This is an **anchor topic** that connects directly to existing RAG content in `rag/development/apex-patterns.md` and `rag/project-methods/testing-strategy.md`, which provide general best practices but don't capture specific lessons learned from real-world implementations, common pitfalls, and practical patterns that emerged from solving actual problems.

This research provides concrete examples, anti-patterns, and lessons learned from building production Apex classes and test classes, including logging utilities, integration services, retry mechanisms, fraud scoring systems, and program selection services. These patterns are especially relevant for developers building enterprise-scale Salesforce solutions where code quality, testability, and maintainability are critical.

This relates to the **development** domain in `rag/**`, specifically Apex patterns, testing strategies, and code quality standards.

## 2. Consensus Best Practices (From Real Implementation Experience)

### Apex Class Design Lessons

- **Always implement fallback mechanisms for critical operations**: When building logging utilities or error handling, always have a fallback (e.g., Platform Events) if primary mechanism fails. This prevents loss of critical information when DML fails due to governor limits or validation rules.

- **Externalize all configuration**: Never hardcode environment-specific values (URLs, IDs, counts). Use Custom Metadata Types or Custom Settings for configuration that varies by environment. This enables environment-specific configuration without code changes.

- **Use Named Credentials for all external URLs**: All HTTP callouts should use Named Credentials, not hardcoded URLs. This centralizes credential management and enables environment-specific endpoints.

- **Design for testability from the start**: Use dependency injection patterns, define interfaces for dependencies (e.g., `IContactSelector`, `IExternalApiService`), and inject dependencies through constructors or setter methods. This enables mocking in test classes.

- **Document trade-offs and future improvements in code**: When implementing a solution that has known limitations (e.g., busy-wait retry logic), document these in code comments. This helps future developers understand why decisions were made and what improvements could be made.

- **Check business rules before complex calculations**: When implementing scoring models or complex calculations, check override conditions first (e.g., business rules that override the model). This prevents unnecessary computation and ensures business rules are respected.

- **Provide transparency in automated decisions**: When implementing scoring models or automated decision-making, provide detailed breakdowns showing how decisions were made. This builds user trust and enables feedback for model improvement.

### Test Class Design Lessons

- **ALL test classes MUST create their own test data**: Never use `@IsTest(SeeAllData=true)`. Test classes must be self-contained and create all necessary test data. This ensures tests are reliable and don't depend on org-specific data.

- **Test classes should never be accessible to end users**: Test classes should never be included in permission sets or profiles accessible to end users. This is a security risk and can expose test logic to unauthorized users.

- **Test with realistic data volumes**: Always test with bulk data (200+ records minimum) to ensure code handles governor limits correctly. Single-record tests don't catch bulkification issues.

- **Test both positive and negative scenarios**: Include test cases for both successful operations and error scenarios. Test error handling, edge cases, and boundary conditions.

- **Minimize logic within Test.startTest() and Test.stopTest() blocks**: These blocks reset governor limits, but complex logic within them can mask limit issues. Keep logic minimal and focused on the operation being tested.

- **Use test data factories for consistent test data**: Create test data factories that generate consistent, realistic test data. This reduces duplication and makes tests more maintainable.

- **Test integration error scenarios**: When testing integrations, use callout mocks to test error scenarios (network failures, timeouts, invalid responses). Don't just test successful scenarios.

### Code Quality Lessons

- **Remove System.debug statements before deployment**: System.debug statements don't persist and can't be used for production troubleshooting. Use proper logging utilities instead.

- **Remove unused code promptly**: Unused code creates confusion and maintenance burden. Remove it promptly to keep codebase clean.

- **Avoid hardcoding IDs**: Use schema methods or constants instead of hardcoded IDs. This makes code more maintainable and environment-agnostic.

- **Replace repeated strings with constants**: Repeated strings are error-prone and hard to maintain. Extract them to constants.

- **Clean up commented code**: Commented code creates confusion. Remove it or convert to proper documentation.

## 3. Key Patterns and Examples (From Real Implementations)

### Pattern 1: Logging Utility with Fallback Mechanism

**When to use**: When you need comprehensive error logging for compliance and troubleshooting, but System.debug isn't sufficient.

**Implementation approach**:
- Create utility class implementing `Callable` interface (enables calling from Flows)
- Implement different log levels (Debug, Info, Error, Warning, Fatal)
- Build methods that accept log level, source, source function, message, payload
- Check log settings (can filter by level)
- Truncate payloads if too large (prevents DML errors)
- Can queue DML requests or execute immediately
- On DML exception, publish Platform Event as fallback

**Why it's recommended**: System.debug statements don't persist and can't be used for production troubleshooting. A logging utility with fallback ensures critical errors are captured even when DML fails. The Callable interface enables use from both Flows and Apex.

**Real example**: `LOG_LogMessageUtility` class built for enterprise-scale public sector portal serving 40,000+ concurrent users. Implemented `Callable` interface, different log levels, truncation for large payloads, and Platform Event fallback when DML fails.

**Lessons learned**:
- Always have a fallback mechanism for critical logging
- Consider storage implications at scale (use log settings to filter)
- Make utilities flexible (queue vs immediate, filtering options)
- Truncation prevents DML errors from large payloads

### Pattern 2: Integration Service with Configuration Management

**When to use**: When you have multiple Apex classes making HTTP callouts with hardcoded URLs and inconsistent error handling patterns.

**Implementation approach**:
- Create abstract class implementing interface
- Use Custom Metadata Type to configure endpoints, methods, headers, timeouts
- Use Named Credentials for URLs (externalized, credentials managed by Salesforce)
- Centralize request generation and execution
- Standardize error handling patterns

**Why it's recommended**: Hardcoded URLs make environment management difficult and create security risks. Centralizing integration patterns makes maintenance and auditing easier. Custom Metadata enables environment-specific configuration without code changes.

**Real example**: `RestIntegrationService` abstract class built to solve problem of multiple Apex classes with hardcoded URLs. Uses Custom Metadata Type (`IEE_MS_Interface_Detail__mdt`) to configure endpoints, methods, headers, timeouts. Named Credentials externalize URLs and credentials.

**Lessons learned**:
- Externalize all configuration - never hardcode environment-specific values
- Use Named Credentials for all external URLs
- Centralize integration patterns - easier to maintain and audit
- Abstract classes enable reuse while allowing specific implementations

### Pattern 3: Retry Logic with Intelligent Error Detection

**When to use**: When operations may encounter transient errors (e.g., row locking errors) that should be retried, but permanent errors (e.g., validation errors) should not be retried.

**Implementation approach**:
- Create service class with `@InvocableMethod` (callable from Flows)
- Implement configurable retry logic (default: 3 retries with exponential backoff)
- Detect retryable errors (check error status code and error message)
- Only retry on retryable errors (e.g., `UNABLE_TO_LOCK_ROW`), not validation errors
- Check governor limits before retry (fail fast if approaching limits)
- Document trade-offs (e.g., busy-wait limitation, future async improvements)

**Why it's recommended**: Retry logic must be intelligent - only retry errors that are likely to succeed on retry. Retrying validation errors wastes resources and doesn't solve the problem. Governor limit awareness prevents retry logic from causing limit exceptions.

**Real example**: `ContactRetryUpdateService` built to solve row locking errors in high-concurrency scenarios. Implements configurable retry logic with exponential backoff, intelligent error detection (only retries row locking errors), and governor limit awareness.

**Lessons learned**:
- Retry logic must be intelligent (only retry retryable errors)
- Always consider governor limits in retry logic
- Document trade-offs and future improvements in code
- Busy-wait works but isn't ideal for high-volume scenarios (consider async alternatives)

### Pattern 4: Scoring Model with Business Rule Overrides

**When to use**: When implementing automated scoring or decision-making systems where business rules can override model calculations.

**Implementation approach**:
- Check override conditions first (before model calculation)
- If override conditions met, return override result immediately
- If no overrides, perform model calculation
- Return detailed breakdown showing how decision was made
- Provide feedback mechanism for model improvement

**Why it's recommended**: Business rules should always take precedence over model calculations. Checking overrides first prevents unnecessary computation and ensures business rules are respected. Detailed breakdowns build user trust and enable feedback for model improvement.

**Real example**: Fraud score calculation system for application review. Checks override conditions first (Active Duty Military, Nursing Programs, Completed Courses → fraud score = 0). If no overrides, calculates score using logistic regression model with 16 factors. Returns detailed breakdown with field values and scores for display.

**Lessons learned**:
- Business rules (overrides) should be checked before model calculation
- Users need transparency in scoring models
- Feedback mechanisms are valuable for model improvement
- Detailed breakdowns help users understand and trust the system

### Pattern 5: Performance-Optimized LWC Controller Pattern

**When to use**: When building Lightning Web Component controllers that need to fetch and process data efficiently.

**Implementation approach**:
- Don't auto-calculate on page load (user must click button) - prevents unnecessary Apex calls
- Use `@AuraEnabled(cacheable=true)` for read-only operations
- Implement cache busting with random parameter when fresh data needed
- Fetch all required data in single Apex call (not multiple separate queries)
- Use relationship queries to combine data in single query
- Only select necessary fields (not entire objects)
- Use lazy loading for detailed breakdowns (hidden in tabs, loaded when expanded)

**Why it's recommended**: Auto-calculating on page load creates unnecessary Apex calls and slows page load times. Cacheable methods with cache busting provide best of both worlds (performance + fresh data). Single Apex calls reduce network latency. Lazy loading improves perceived performance.

**Real example**: Fraud score calculation component. Doesn't auto-calculate on load - user must click "Calculate" button. Uses cacheable methods with cache busting. Fetches all required data in single call. Lazy loads detailed breakdown in tabs.

**Lessons learned**:
- Not auto-calculating on load significantly improves page load times
- Cacheable methods with cache busting provide best of both worlds (performance + fresh data)
- User control over when to calculate improves perceived performance
- Single Apex calls reduce network latency

### Pattern 6: Test Class Security Anti-Pattern

**When NOT to do**: Including test classes in permission sets or profiles accessible to end users.

**Implementation approach**:
- Test classes should never be included in permission sets
- Test classes should never be accessible to end users
- Remove test classes from permission sets if found

**Why it's a problem**: Test classes can expose test logic, data, and potentially sensitive information to unauthorized users. This is a security risk and violates best practices.

**Real example**: Found test classes (`CommunitiesLandingControllerTest`, `CommunitiesLoginControllerTest`) in permission sets during code review. Removed them immediately.

**Lessons learned**:
- Test classes should never be accessible to end users
- Always review permission sets for test classes
- Security reviews should check for test class access

## 4. Interactions With Existing RAG

This research topic is an **anchor topic** that connects directly to existing RAG content:

**Direct relationship to `rag/development/apex-patterns.md`**:
- The RAG file provides general best practices for Apex class layering, SOQL design, error handling, and testing strategies
- This research adds concrete examples, lessons learned, and anti-patterns from real implementations
- The RAG file mentions patterns (e.g., retry logic, logging utilities) but doesn't provide detailed implementation examples or lessons learned

**Direct relationship to `rag/project-methods/testing-strategy.md`**:
- The RAG file provides comprehensive testing strategies covering integration testing, data quality testing, and UAT
- This research adds specific lessons learned about test class design, test data management, and test security
- The RAG file mentions test coverage requirements but doesn't provide concrete examples of test class anti-patterns or lessons learned

**Gaps filled by this research**:
- Concrete implementation examples with real class names and patterns
- Lessons learned from solving actual problems (row locking errors, logging at scale, integration configuration)
- Anti-patterns and security issues (test classes in permission sets)
- Performance optimization lessons (cacheable methods, lazy loading, single Apex calls)

**Nuances added**:
- This research emphasizes practical lessons learned from real implementations, not just theoretical best practices
- It provides concrete examples of how patterns were implemented and why decisions were made
- It captures trade-offs and limitations that were discovered during implementation

## 5. Tradeoffs and Controversies

**Synchronous vs asynchronous retry logic**: Some patterns retry synchronously in the same transaction (e.g., `ContactRetryUpdateService` with busy-wait), while others defer to Queueable jobs. The tradeoff is between simplicity (synchronous) and resource efficiency (asynchronous). The consensus is to use synchronous for quick retries (1-2 attempts) and asynchronous for longer retries or high-volume scenarios.

**Auto-calculation vs user-initiated calculation**: Some components auto-calculate on page load for convenience, while others require user action. The tradeoff is between convenience (auto-calculate) and performance (user-initiated). The consensus from real implementations is that user-initiated calculation significantly improves page load times and perceived performance.

**Cacheable methods with cache busting**: Some implementations use cacheable methods without cache busting (better performance, but stale data risk), while others use cache busting (fresh data, but more server round trips). The tradeoff is between performance (no cache busting) and data freshness (cache busting). The consensus is to use cacheable methods with cache busting when fresh data is needed, but accept cached data when acceptable.

**Detailed breakdowns vs simple scores**: Some scoring systems return only final scores, while others return detailed breakdowns. The tradeoff is between simplicity (simple scores) and transparency (detailed breakdowns). The consensus is that detailed breakdowns build user trust and enable feedback for model improvement, even if they add complexity.

These tradeoffs are **not** automatic candidates for RAG changes; they require human judgment based on system requirements, user needs, and performance constraints.

## 6. Candidate Ideas for RAG Enhancement

- **Add concrete implementation examples to `rag/development/apex-patterns.md`**: The RAG file mentions patterns (e.g., retry logic, logging utilities) but could include concrete examples showing how these patterns were implemented in real projects.

- **Add lessons learned section**: Consider adding a "Lessons Learned" section to the RAG file that captures practical insights from real implementations, not just theoretical best practices.

- **Add anti-patterns section**: Consider adding an "Anti-Patterns" section that documents common mistakes and security issues (e.g., test classes in permission sets).

- **Expand test class guidance**: The RAG file mentions test class best practices but could include more specific guidance on test data factories, test security, and test class anti-patterns.

- **Add performance optimization patterns**: Consider adding more specific guidance on performance optimization patterns (e.g., cacheable methods with cache busting, lazy loading, single Apex calls).

## 7. Sources Used

- Concrete implementation experience from enterprise-scale Salesforce projects
- Code review findings from comprehensive project reviews
- Standards established through rigorous code review processes
- Lessons learned from solving real-world problems (row locking errors, logging at scale, integration configuration)

(Detailed sources with specific project context are maintained in `Knowledge/cursor-responses.md`)

## 8. To Evaluate

- **Retry logic patterns**: While synchronous retry with busy-wait works, optimal patterns depend on system load, concurrency levels, and business requirements. The decision requires evaluation based on monitoring and testing.

- **Cacheable method patterns**: Optimal caching strategies depend on data freshness requirements, user behavior, and system load. The decision requires evaluation based on performance monitoring and user feedback.

- **Scoring model transparency**: The level of detail in scoring breakdowns depends on user needs, compliance requirements, and system complexity. The decision requires evaluation based on user feedback and business requirements.

- **Test class security**: While test classes should never be accessible to end users, the specific security review process depends on project size, team structure, and compliance requirements. The decision requires evaluation based on project context.

