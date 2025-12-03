# Record-Triggered Flow Code Examples

> This file contains complete, working examples for Record-Triggered Flow patterns.
> All examples follow Salesforce Flow best practices.

## Overview

Record-Triggered Flows run automatically when records are created or updated. These examples demonstrate common patterns for before-save and after-save automation.

**Related Patterns**:
- [Flow Patterns](../development/flow-patterns.md) - Complete Flow development patterns
- [Order of Execution](../development/order-of-execution.md) - Understanding when Flows execute

## Examples

### Example 1: Before-Save Field Update

**Pattern**: Updating field values before record save
**Use Case**: Auto-populating fields or calculating values
**Complexity**: Basic
**Related Patterns**: [Flow Patterns](../development/flow-patterns.md#record-triggered-flow-structure)

**Problem**:
You need to automatically set a field value when a record is created or updated.

**Solution**:

**Flow Configuration**:
- **Trigger**: Record-Triggered Flow
- **Object**: Contact
- **Entry Criteria**: `IsNew = true OR Email != null`
- **Trigger Type**: Before Save

**Flow Elements**:
1. **Start** - Entry criteria: `{!$Record.IsNew} = true OR {!$Record.Email} != null`
2. **Assignment** - Set `{!$Record.Full_Name__c}` = `{!$Record.FirstName} + ' ' + {!$Record.LastName}`
3. **Decision** - Check if Email changed
4. **Assignment** (if Email changed) - Set `{!$Record.Email_Verified__c}` = false

**Best Practices**:
- Use before-save for field updates on the same record
- Set strict entry criteria to avoid unnecessary execution
- Use formulas for simple calculations
- Test with bulk data (200+ records)

### Example 2: After-Save Related Record Creation

**Pattern**: Creating related records after save
**Use Case**: Auto-creating child records or tasks
**Complexity**: Intermediate
**Related Patterns**: [Flow Patterns](../development/flow-patterns.md)

**Problem**:
You need to create a related record when a parent record is saved.

**Solution**:

**Flow Configuration**:
- **Trigger**: Record-Triggered Flow
- **Object**: Case
- **Entry Criteria**: `Status = 'New'`
- **Trigger Type**: After Save

**Flow Elements**:
1. **Start** - Entry criteria: `{!$Record.Status} = 'New'`
2. **Create Records** - Create Task
   - Subject: `'Follow up on Case: ' + {!$Record.CaseNumber}`
   - WhatId: `{!$Record.Id}`
   - Status: `'Not Started'`
   - Priority: `'Normal'`
   - OwnerId: `{!$Record.OwnerId}`

**Best Practices**:
- Use after-save for related record operations
- Set entry criteria to avoid unnecessary execution
- Use collection variables for bulk operations
- Handle errors with fault paths

### Example 3: After-Save Status Update with Decision

**Pattern**: Updating related records based on conditions
**Use Case**: Status synchronization across related records
**Complexity**: Intermediate
**Related Patterns**: [Flow Patterns](../development/flow-patterns.md)

**Problem**:
You need to update related records when a parent record status changes.

**Solution**:

**Flow Configuration**:
- **Trigger**: Record-Triggered Flow
- **Object**: Opportunity
- **Entry Criteria**: `StageName` in ('Closed Won', 'Closed Lost')
- **Trigger Type**: After Save

**Flow Elements**:
1. **Start** - Entry criteria: `{!$Record.StageName} = 'Closed Won' OR {!$Record.StageName} = 'Closed Lost'`
2. **Get Records** - Get related Quotes where `OpportunityId = {!$Record.Id}`
3. **Decision** - Check `{!$Record.StageName}`
   - Outcome 1: `'Closed Won'` → Update Quotes: `Status = 'Approved'`
   - Outcome 2: `'Closed Lost'` → Update Quotes: `Status = 'Rejected'`
4. **Update Records** - Update Quotes collection

**Best Practices**:
- Use Decision elements for routing logic
- Process collections, not single records
- Set entry criteria to reduce execution
- Handle bulk operations efficiently

## Related Examples

- [Screen Flow Examples](flow/screen-flow-examples.md) - User interaction flows
- [Subflow Examples](flow/subflow-examples.md) - Reusable subflow patterns

## See Also

- [Flow Patterns](../development/flow-patterns.md) - Complete Flow development patterns
- [Order of Execution](../development/order-of-execution.md) - Understanding Flow execution timing

