# Locking and Concurrency Strategies – Sources

> This file lists external references used for the research summary.  
> It is for link tracking and quick re-verification.

## Primary Sources (Official / Highly Authoritative)

- Salesforce Developer Documentation: Apex Exception Handling
  - https://developer.salesforce.com/docs/atlas.en-us.apexcode.meta/apexcode/apex_exception_handling.htm
  - Exception handling patterns including DmlException and status codes

- Salesforce Developer Documentation: DML Statements
  - https://developer.salesforce.com/docs/atlas.en-us.apexcode.meta/apexcode/apex_dml.htm
  - DML operations, error handling, and partial success scenarios

- Salesforce Developer Documentation: SOQL FOR UPDATE
  - https://developer.salesforce.com/docs/atlas.en-us.soql_sosl.meta/soql_sosl/sforce_api_calls_soql_select_for_update.htm
  - Row locking mechanisms and FOR UPDATE clauses

- Trailhead: Apex Basics & Database
  - https://trailhead.salesforce.com/content/learn/modules/apex_database
  - DML operations, error handling, and transaction management

- Trailhead: Asynchronous Apex
  - https://trailhead.salesforce.com/content/learn/modules/asynchronous_apex
  - Queueable Apex for retry operations and separate transaction contexts

- Official Salesforce Blog: Error Handling Best Practices
  - https://developer.salesforce.com/blogs
  - Retry patterns, error handling, and concurrency management

## Secondary Sources (Blogs, Articles, Talks)

- Salesforce Stack Exchange: Row Locking Discussions
  - https://salesforce.stackexchange.com/questions/tagged/row-locking
  - Community discussions on UNABLE_TO_LOCK_ROW handling and retry strategies

- Salesforce Stack Exchange: Concurrency
  - https://salesforce.stackexchange.com/questions/tagged/concurrency
  - Concurrency control patterns and high-concurrency scenarios

## Notes

- UNABLE_TO_LOCK_ROW error handling is well-documented
- Retry patterns with exponential backoff are widely recommended
- Deadlock prevention strategies are less documented but follow standard database concurrency principles

