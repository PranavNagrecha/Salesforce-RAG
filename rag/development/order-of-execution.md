---
title: "Order of Execution"
level: "Intermediate"
tags:
  - apex
  - flow
  - development
  - order-of-execution
  - triggers
last_reviewed: "2025-01-XX"
---

# Order of Execution

## Overview

Understanding the order of execution in Salesforce is critical for architects and developers. The execution order determines when triggers, flows, validation rules, and other automation run, which directly impacts system behavior, data integrity, and debugging capabilities.

## Prerequisites

**Required Knowledge**:
- Understanding of Salesforce automation (Triggers, Flows, Process Builder, Workflow Rules)
- Knowledge of validation rules and data validation
- Understanding of Apex triggers and execution context
- Familiarity with record save operations

**Recommended Reading**:
- [Apex Patterns](development/apex-patterns.html) - Apex trigger patterns
- [Flow Patterns](development/flow-patterns.html) - Flow automation patterns
- [Error Handling and Logging](development/error-handling-and-logging.html) - Error handling in automation

## Complete Order of Execution

### Save Operation Sequence

When a record is saved (insert, update, upsert, or undelete), Salesforce executes automation in a specific order:

#### 1. Load Original Record from Database
- System loads the original record data from the database
- For new records, original values are null
- For updates, original values reflect the state before the current transaction

#### 2. Load New Record Values
- System loads new field values from the request
- Combines original and new values to create the "before" and "after" record states

#### 3. System Validation Rules
- **System-level validation rules** execute first
- These include:
  - Required field validation
  - Field format validation (e.g., email format)
  - Maximum field length validation
- If validation fails, the transaction stops and an error is returned

#### 4. Before-Save Automation (Before Save)

**Execution Order**:
1. **Before-Save Record-Triggered Flows** (entry criteria evaluated)
2. **Apex Before Triggers** (`before insert`, `before update`, `before delete`)
3. **Duplicate Rules** (if enabled)
4. **Custom Validation Rules** (if not already evaluated)

**Key Characteristics**:
- Execute before the record is committed to the database
- Can modify field values before save
- Cannot perform DML operations on other records
- Cannot perform SOQL queries (with exceptions for certain scenarios)
- Field changes made here are included in the final save

**Best Practices**:
- Use before-save automation for field value modifications
- Use before-save for data validation that needs to prevent save
- Keep before-save logic fast and efficient
- Avoid complex logic that could impact performance

#### 5. Save to Database (No Rollback Point)
- Record is saved to the database
- This is a point of no return - record exists in database
- If subsequent steps fail, the record remains saved

#### 6. After-Save Automation (After Save)

**Execution Order**:
1. **After-Save Record-Triggered Flows** (entry criteria evaluated)
2. **Apex After Triggers** (`after insert`, `after update`, `after delete`, `after undelete`)
3. **Assignment Rules** (if enabled)
4. **Auto-Response Rules** (if enabled)
5. **Workflow Rules** (if still in use - ⚠️ **Deprecated**: Use Record-Triggered Flows instead)
6. **Process Builder** (if still in use - ⚠️ **Deprecated**: Use Record-Triggered Flows instead)
7. **Escalation Rules** (if enabled)

**Key Characteristics**:
- Execute after the record is committed to the database
- Cannot modify the triggering record's field values (record is read-only)
- Can perform DML operations on other records
- Can perform SOQL queries
- Can publish Platform Events
- Can make callouts (with proper async handling)

**Best Practices**:
- Use after-save automation for related record operations
- Use after-save for notifications and integrations
- Use after-save for complex business logic requiring queries
- Keep after-save logic bulkified

#### 7. Post-Commit Automation

**Execution Order**:
1. **Platform Events** (published in after-save automation)
2. **Email Alerts** (from workflow rules or Process Builder - ⚠️ **Deprecated**: Use Flows instead)
3. **Outbound Messages** (from workflow rules - ⚠️ **Deprecated**: Use Flows instead)
4. **Flow Orchestration** (if triggered)
5. **Apex Queueable Jobs** (if enqueued)
6. **Apex Future Methods** (if called)

**Key Characteristics**:
- Execute asynchronously or after transaction commits
- Cannot modify the triggering record
- Can perform DML on other records
- Can make callouts
- Execute outside the main transaction context

### Delete Operation Sequence

When a record is deleted:

1. **Before Delete Triggers** execute
2. **Validation Rules** check for deletion restrictions
3. **Record is deleted** from database
4. **After Delete Triggers** execute
5. **Cascade Delete** operations execute (for Master-Detail relationships)
6. **Post-Delete Automation** executes (similar to post-commit)

### Undelete Operation Sequence

When a record is undeleted:

1. **After Undelete Triggers** execute
2. **Validation Rules** execute
3. **Record is restored** to database
4. **After-Save Automation** may execute (depending on configuration)

## Before-Save vs After-Save Decision Framework

### Use Before-Save When:

- **Field Value Modification**: Need to modify field values before save
- **Early Validation**: Need to validate and prevent save early
- **Performance**: Need to avoid unnecessary database operations
- **Data Transformation**: Need to transform data before it's saved
- **Formula-Like Calculations**: Need to calculate values based on other fields

**Examples**:
- Setting default values
- Calculating derived fields
- Normalizing data formats
- Early validation to prevent save

### Use After-Save When:

- **Related Record Operations**: Need to create/update related records
- **SOQL Queries Required**: Need to query other records
- **Complex Business Logic**: Need to perform complex operations
- **Notifications**: Need to send emails or notifications
- **Integrations**: Need to publish events or make callouts
- **Reporting**: Need to update rollup fields or related metrics

**Examples**:
- Creating related records
- Updating parent records
- Sending notifications
- Publishing Platform Events
- Making external API callouts

## Flow Execution Timing

### Record-Triggered Flows

**Before-Save Flows**:
- Execute in step 4 (before save)
- Can modify field values
- Cannot perform DML on other records
- Cannot perform SOQL queries
- Fast execution required

**After-Save Flows**:
- Execute in step 6 (after save)
- Cannot modify triggering record
- Can perform DML on other records
- Can perform SOQL queries
- Can publish Platform Events

**Entry Criteria**:
- Evaluated at the appropriate step
- Must be selective to avoid unnecessary execution
- Use specific conditions to limit execution

### Scheduled Flows

- Execute independently of record operations
- Run on a schedule (hourly, daily, weekly, etc.)
- Can perform DML and SOQL operations
- Execute in their own transaction context

### Screen Flows

- Execute when launched by user or automation
- Can perform DML and SOQL operations
- Execute in user's transaction context

## Validation Rule Timing

### System Validation Rules

- Execute in step 3 (before any automation)
- Cannot be bypassed
- Stop transaction if they fail

### Custom Validation Rules

- Execute in step 4 (during before-save)
- Can reference field values modified by before-save automation
- Stop transaction if they fail
- Can use formulas and cross-object references

**Best Practices**:
- Keep validation rules simple and fast
- Avoid complex formulas that impact performance
- Use validation rules for data quality, not business logic
- Consider before-save flows for complex validation logic

## Trigger Execution Order

### Multiple Triggers

If multiple triggers exist for the same object and event:

1. **No guaranteed order** between triggers
2. Triggers execute in **undefined order**
3. **Best Practice**: Use one trigger per object per event type
4. Use a trigger framework to manage trigger logic

### Trigger Context Variables

- `Trigger.isBefore`: True in before-save triggers
- `Trigger.isAfter`: True in after-save triggers
- `Trigger.isInsert`: True for insert operations
- `Trigger.isUpdate`: True for update operations
- `Trigger.isDelete`: True for delete operations
- `Trigger.isUndelete`: True for undelete operations
- `Trigger.new`: New record values (before-save) or saved record (after-save)
- `Trigger.old`: Original record values (before-save) or previous values (after-save)
- `Trigger.newMap`: Map of new records by ID
- `Trigger.oldMap`: Map of old records by ID

## Common Patterns and Pitfalls

### Pattern: Field Value Modification

**Correct Approach**:
- Use before-save automation (Flow or Apex trigger)
- Modify field values in before-save
- Validation rules see modified values

**Incorrect Approach**:
- Trying to modify field values in after-save
- After-save record is read-only

### Pattern: Related Record Creation

**Correct Approach**:
- Use after-save automation
- Query related records if needed
- Create/update related records

**Incorrect Approach**:
- Trying to create related records in before-save
- Before-save cannot perform DML on other records

### Pattern: Rollup Calculations

**Correct Approach**:
- Use after-save automation
- Query related records
- Update parent or related records

**Incorrect Approach**:
- Trying to update parent in before-save
- Before-save cannot perform DML on other records

### Pattern: Validation with Related Data

**Correct Approach**:
- Use after-save automation for complex validation
- Query related records if needed
- Use Platform Events or custom objects to track validation failures

**Alternative Approach**:
- Use before-save flow with Get Records element (limited scenarios)
- Use validation rules for simple cross-object validation

## Performance Considerations

### Before-Save Performance

- **Fast Execution Required**: Before-save runs synchronously
- **No DML Overhead**: Cannot perform DML, so faster
- **Limited Queries**: Limited SOQL query capabilities
- **Impact on User Experience**: Slow before-save impacts save time

### After-Save Performance

- **Can Be Slower**: After-save can perform complex operations
- **DML Overhead**: Can perform DML on other records
- **Query Capabilities**: Can perform SOQL queries
- **Less Impact on User Experience**: Record is already saved

### Best Practices

- **Keep Before-Save Fast**: Minimize logic in before-save
- **Use After-Save for Complex Logic**: Move complex operations to after-save
- **Bulkify All Automation**: Handle bulk operations efficiently
- **Avoid Nested Triggers**: Prevent trigger recursion
- **Use Platform Events for Async**: Move heavy operations to async

## Debugging Order of Execution Issues

### Common Issues

1. **Field Values Not Updating**: Check if using after-save (read-only)
2. **Validation Rules Failing Unexpectedly**: Check if before-save modified values
3. **Related Records Not Created**: Check if using before-save (cannot perform DML)
4. **Trigger Recursion**: Check trigger logic for update operations
5. **Performance Issues**: Check if complex logic is in before-save

### Debugging Techniques

1. **Use Debug Logs**: Enable debug logs for automation
2. **Check Execution Order**: Review debug logs for execution sequence
3. **Verify Context**: Check trigger context variables
4. **Test Scenarios**: Test with different record states
5. **Review Automation**: Review all automation on the object

## Best Practices Summary

### Design Principles

1. **Understand Execution Order**: Know when each automation type executes
2. **Choose Right Timing**: Use before-save for field modifications, after-save for related operations
3. **Keep Before-Save Fast**: Minimize logic in before-save automation
4. **Bulkify All Automation**: Handle bulk operations efficiently
5. **Avoid Recursion**: Prevent trigger and flow recursion
6. **Use Platform Events**: Move heavy operations to async processing

### Implementation Guidelines

1. **One Trigger Per Object**: Use trigger frameworks to manage logic
2. **Selective Entry Criteria**: Use specific entry criteria in flows
3. **Validation Rules for Data Quality**: Use validation rules for simple validation
4. **Flows for Business Logic**: Use flows for complex business logic
5. **Apex for Complex Logic**: Use Apex for very complex or performance-critical logic

## Related Patterns

**See Also**:
- [Flow Patterns](development/flow-patterns.html) - Flow execution patterns and timing
- [Apex Patterns](development/apex-patterns.html) - Apex trigger patterns and execution

**Related Domains**:
- [Event-Driven Architecture](architecture/event-driven-architecture.html) - Async processing patterns

## Q&A

### Q: What is the difference between before-save and after-save automation?

**A**: **Before-save** automation runs before the record is saved to the database. You can modify field values, but cannot perform DML on other records. **After-save** automation runs after the record is saved. The record is read-only, but you can perform DML on other records and query related data.

### Q: When should I use before-save vs after-save flows?

**A**: Use **before-save** flows for field value modifications, simple validations, and calculations that need to be saved with the record. Use **after-save** flows for related record operations, complex validations requiring queries, rollup calculations, and operations that don't need to modify the current record.

### Q: What is the execution order of validation rules?

**A**: **System validation rules** execute first (step 3), before any automation. **Custom validation rules** execute during before-save (step 4), after before-save flows and triggers have run, so they can reference field values modified by before-save automation.

### Q: Can I modify field values in after-save automation?

**A**: No, records are **read-only** in after-save automation. You cannot modify field values in after-save flows or triggers. To modify field values, use before-save automation (before-save flows or before triggers).

### Q: What happens if multiple triggers exist for the same object?

**A**: If multiple triggers exist for the same object and event, there is **no guaranteed execution order**. Triggers execute in undefined order. Best practice: use one trigger per object per event type and use a trigger framework to manage trigger logic.

### Q: Can I perform DML operations in before-save automation?

**A**: No, **before-save automation cannot perform DML operations** on other records. You can only modify field values on the current record. To perform DML on other records, use after-save automation or async processing (Platform Events, Queueable, etc.).

### Q: How do I prevent trigger recursion?

**A**: Prevent trigger recursion by checking if field values have actually changed before performing updates, using static variables to track execution, implementing guard clauses, and avoiding update operations that would re-trigger the same trigger. Use trigger frameworks that handle recursion prevention.

### Q: What is the performance impact of before-save vs after-save automation?

**A**: **Before-save** runs synchronously and impacts user save time - keep it fast. **After-save** can be slower since the record is already saved, but complex operations in after-save can still impact overall transaction time. Move heavy operations to async processing (Platform Events, Queueable) when possible.

## References

- Salesforce Documentation: Order of Execution
- Trailhead: Apex Triggers and Order of Execution
- Best Practices: Understanding Salesforce Order of Execution

