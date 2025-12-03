# Governor Limits and Performance Optimization – Sources

> This file lists external references used for the research summary.  
> It is for link tracking and quick re-verification.

## Primary Sources (Official / Highly Authoritative)

- Salesforce Developer Documentation: Apex Governor Limits
  - https://developer.salesforce.com/docs/atlas.en-us.apexcode.meta/apexcode/apex_gov_limits.htm
  - Comprehensive list of all governor limits with specific values and contexts

- Salesforce Developer Documentation: SOQL and SOSL Reference
  - https://developer.salesforce.com/docs/atlas.en-us.soql_sosl.meta/soql_sosl/
  - Query optimization, selectivity, and performance guidance

- Salesforce Developer Documentation: Query Optimization
  - https://developer.salesforce.com/docs/atlas.en-us.salesforce_large_data_volumes_best_practices.meta/salesforce_large_data_volumes_best_practices/ldv_deploy_query_optimization.htm
  - Query selectivity rules, indexed fields, and performance optimization

- Trailhead: Apex Basics & Database
  - https://trailhead.salesforce.com/content/learn/modules/apex_database
  - Governor limits, SOQL optimization, and bulkification patterns

- Trailhead: Asynchronous Apex
  - https://trailhead.salesforce.com/content/learn/modules/asynchronous_apex
  - Batch Apex, Queueable, and Scheduled Apex for large operations

- Trailhead: Large Data Volumes
  - https://trailhead.salesforce.com/content/learn/modules/large_data_volumes
  - LDV best practices, query optimization, and performance tuning

## Secondary Sources (Blogs, Articles, Talks)

- Official Salesforce Blog: Performance Best Practices
  - https://developer.salesforce.com/blogs
  - Performance optimization techniques and governor limit management

- Salesforce Stack Exchange: Governor Limits Discussions
  - https://salesforce.stackexchange.com/questions/tagged/governor-limits
  - Community discussions on limit management and optimization

- Salesforce Stack Exchange: SOQL Optimization
  - https://salesforce.stackexchange.com/questions/tagged/soql
  - Query optimization patterns and selectivity discussions

## Notes

- Governor limit values are well-documented in official docs
- Query selectivity rules (10% threshold) are widely accepted but may vary by object
- Best practices are consistent across sources with minor variations in implementation details

