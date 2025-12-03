---
layout: default
title: Record-Triggered Flow Code Examples
description: Record-Triggered Flows run automatically when records are created or updated, providing declarative automation for common business processes
permalink: /rag/code-examples/flow/record-triggered-examples.html
level: Intermediate
tags:
  - code-examples
  - flow
  - record-triggered
  - automation
last_reviewed: 2025-12-03
---

# Record-Triggered Flow Code Examples

## Overview

Record-Triggered Flows are the primary automation tool in Salesforce for declarative automation. These examples demonstrate common patterns for:

- **Before-Save Flows**: Fast field updates and defaulting (runs before record save)
- **After-Save Flows**: Creating related records, publishing events, sending notifications (runs after record save)
- **Bulkification**: Handling multiple records efficiently
- **Error Handling**: Graceful error management with fault paths
- **Routing Logic**: Decision nodes for conditional processing

## When to Use

### Use Record-Triggered Flows When

- Need to automate record creation/updates based on field changes
- Need to create related records when parent records are created
- Need to publish Platform Events for integrations
- Need to send notifications based on record changes
- Need to set default values or calculate fields
- Need declarative automation that business users can maintain

### Avoid Record-Triggered Flows When

- Need complex logic that requires Apex
- Need to make callouts from before-save (not supported)
- Need tight control over governor limits for very large datasets
- Need complex nested loops or advanced data transformations

## Example 1: Before-Save Flow - Field Defaulting

**Use Case**: Set default values on Case creation based on record type and other criteria.

**Flow Name**: `Case_BeforeSave_Defaulting`

**Entry Criteria**:
```
Record Type = 'Support Case' AND Status = 'New'
```

**Flow Structure**:
1. **Start Element**: Record-Triggered Flow (Before Save)
   - Object: Case
   - Entry Criteria: `RecordType.DeveloperName = 'Support_Case' AND Status = 'New'`
   - Trigger: Create and Update

2. **Decision Node**: Check Priority
   - Outcome 1: `Priority = null` → Set Priority to 'Medium'
   - Outcome 2: `Priority != null` → Continue

3. **Assignment Element**: Set Default Values
   - `Priority` = `'Medium'` (if null)
   - `OwnerId` = `{!$Record.OwnerId}` (if null, assign to Queue)
   - `Due_Date__c` = `TODAY() + 3` (calculate based on SLA)

4. **End Element**: Save the record

**Key Points**:
- Before-save flows can only update fields on the triggering record
- No DML operations on other records allowed
- Keep logic fast (impacts user save time)
- Use strict entry criteria to avoid unnecessary executions

## Example 2: After-Save Flow - Create Related Records

**Use Case**: Create a Task when a Case is created with Priority = 'High'.

**Flow Name**: `Case_AfterSave_CreateHighPriorityTask`

**Entry Criteria**:
```
Priority = 'High' AND ISNEW() = true
```

**Flow Structure**:
1. **Start Element**: Record-Triggered Flow (After Save)
   - Object: Case
   - Entry Criteria: `Priority = 'High' AND ISNEW() = true`
   - Trigger: Create

2. **Create Records Element**: Create Follow-up Task
   - Object: Task
   - How Many: One
   - Fields:
     - `Subject` = `'Follow up on High Priority Case ' & {!$Record.CaseNumber}`
     - `WhatId` = `{!$Record.Id}`
     - `Status` = `'Not Started'`
     - `Priority` = `'High'`
     - `ActivityDate` = `TODAY() + 1`
   - Store In: `NewTask` (single record variable)
   - Fault Path: Log error and continue

3. **End Element**: End the flow

**Key Points**:
- After-save flows can create/update/delete related records
- Use bulk operations (create multiple records at once when possible)
- Always configure fault paths for error handling
- Store created record IDs in variables for later use

## Example 3: After-Save Flow - Route by Record State

**Use Case**: Orchestrate application status changes with different logic for new vs updated records.

**Flow Name**: `App_AfterSave_ApplicationStatusOrchestration`

**Entry Criteria**:
```
Record Type = 'Application' AND ISCHANGED(Status)
```

**Flow Structure**:
1. **Start Element**: Record-Triggered Flow (After Save)
   - Object: Application__c (custom object)
   - Entry Criteria: `RecordType.DeveloperName = 'Application' AND ISCHANGED(Status__c)`
   - Trigger: Create and Update

2. **Decision Node**: Route by Record State
   - Outcome 1: `ISNEW() = true` → New Application Path
   - Outcome 2: `ISNEW() = false` → Updated Application Path

3. **New Application Path**:
   - **Subflow**: `Subflow_Create_Advisor_Tasks`
     - Input: `ApplicationId` = `{!$Record.Id}`
   - **Create Records**: Create Application History record
   - **Publish Platform Event**: `ApplicationCreated__e`
     - Fields: `ApplicationId__c` = `{!$Record.Id}`, `Status__c` = `{!$Record.Status__c}`

4. **Updated Application Path**:
   - **Decision Node**: Route by Status
     - Outcome 1: `Status__c = 'Approved'` → Approved Path
     - Outcome 2: `Status__c = 'Rejected'` → Rejected Path
     - Outcome 3: `Status__c = 'Pending'` → Pending Path
   - **Subflow**: `Subflow_Sync_Application_Status_to_Child_Objects`
   - **Send Email**: Notify applicant of status change

5. **End Element**: End the flow

**Key Points**:
- Route by record state early (New vs Update, Status, Channel)
- Use Subflows for complex tasks to keep main flow readable
- Publish Platform Events for event-driven integrations
- Aggregate DML operations to minimize governor limit usage

## Example 4: After-Save Flow - Bulk Create Related Records

**Use Case**: Create tasks for multiple Contacts when Account is updated.

**Flow Name**: `Account_AfterSave_CreateContactTasks`

**Entry Criteria**:
```
ISCHANGED(Status__c) AND Status__c = 'Active'
```

**Flow Structure**:
1. **Start Element**: Record-Triggered Flow (After Save)
   - Object: Account
   - Entry Criteria: `ISCHANGED(Status__c) AND Status__c = 'Active'`
   - Trigger: Update

2. **Get Records Element**: Get Related Contacts
   - Object: Contact
   - Filter: `AccountId = {!$Record.Id} AND Active__c = true`
   - Store In: `RelatedContacts` (collection variable)
   - Sort: None

3. **Loop Element**: Prepare Tasks
   - Loop Through: `RelatedContacts`
   - Current Item: `CurrentContact`
   - **Assignment Element**: Add Task to Collection
     - Variable: `TasksToCreate` (collection variable, initialized empty)
     - Add Items:
       - `Subject` = `'Follow up with ' & {!CurrentContact.Name}`
       - `WhoId` = `{!CurrentContact.Id}`
       - `WhatId` = `{!$Record.Id}`
       - `Status` = `'Not Started'`
       - `Priority` = `'Medium'`
       - `ActivityDate` = `TODAY() + 7`

4. **Create Records Element**: Create Tasks in Bulk
   - Object: Task
   - How Many: Multiple
   - Records: `TasksToCreate`
   - Store In: `CreatedTasks` (collection variable)
   - Fault Path: Log errors and continue

5. **End Element**: End the flow

**Key Points**:
- Prepare records in collections before creating (bulk operation)
- Use Loop elements to build collections
- Create multiple records at once (not one at a time)
- Each Create Records element counts as 1 DML operation (limit: 150 per transaction)

## Example 5: After-Save Flow - Update Related Records

**Use Case**: Update all related Cases when Account status changes to 'Closed'.

**Flow Name**: `Account_AfterSave_CloseRelatedCases`

**Entry Criteria**:
```
ISCHANGED(Status__c) AND Status__c = 'Closed'
```

**Flow Structure**:
1. **Start Element**: Record-Triggered Flow (After Save)
   - Object: Account
   - Entry Criteria: `ISCHANGED(Status__c) AND Status__c = 'Closed'`
   - Trigger: Update

2. **Get Records Element**: Get Open Cases
   - Object: Case
   - Filter: `AccountId = {!$Record.Id} AND Status != 'Closed'`
   - Store In: `OpenCases` (collection variable)

3. **Decision Node**: Check if Cases Exist
   - Outcome 1: `OpenCases` is not empty → Update Cases
   - Outcome 2: `OpenCases` is empty → End flow

4. **Update Records Element**: Close All Cases
   - Records: `OpenCases`
   - How Many: Multiple
   - Fields:
     - `Status` = `'Closed'`
     - `ClosedDate` = `TODAY()`
     - `Reason` = `'Account Closed'`
   - Fault Path: Log errors and continue

5. **End Element**: End the flow

**Key Points**:
- Query related records before updating
- Use bulk update operations (update multiple records at once)
- Only update fields that need to change
- Configure fault paths for error handling

## Example 6: After-Save Flow - Platform Event Publishing

**Use Case**: Publish Platform Event when Application status changes for integration.

**Flow Name**: `App_AfterSave_PublishStatusChangeEvent`

**Entry Criteria**:
```
ISCHANGED(Status__c)
```

**Flow Structure**:
1. **Start Element**: Record-Triggered Flow (After Save)
   - Object: Application__c
   - Entry Criteria: `ISCHANGED(Status__c)`
   - Trigger: Create and Update

2. **Publish Platform Events Element**: Publish Status Change Event
   - Platform Event: `ApplicationStatusChange__e`
   - How Many: One
   - Fields:
     - `ApplicationId__c` = `{!$Record.Id}`
     - `OldStatus__c` = `{!$Record.PRIORVALUE(Status__c)}`
     - `NewStatus__c` = `{!$Record.Status__c}`
     - `ChangedBy__c` = `{!$User.Id}`
     - `ChangedDate__c` = `NOW()`
   - Store In: `PublishedEvent` (single record variable)
   - Fault Path: Log error and continue

3. **End Element**: End the flow

**Key Points**:
- Platform Events enable event-driven architecture
- Events are published asynchronously (don't block transaction)
- Use Platform Events for integrations instead of direct callouts when possible
- Include context fields (old value, new value, user, timestamp)

## Testing Considerations

### Test Scenarios

1. **Before-Save Flows**:
   - Test with null values (defaulting logic)
   - Test with existing values (no overwrite)
   - Test with bulk records (200+ records)
   - Verify save time impact (should be fast)

2. **After-Save Flows**:
   - Test with single record creation
   - Test with bulk record creation (200+ records)
   - Test with related record queries (empty results, multiple results)
   - Test error scenarios (fault paths)
   - Test decision node routing (all paths)

3. **Common Edge Cases**:
   - Empty collections (no related records)
   - Null field values
   - Record type changes
   - Status transitions (all valid transitions)
   - Concurrent updates (UNABLE_TO_LOCK_ROW)

### Best Practices

- Test with bulk data (200+ records minimum)
- Test all decision node paths
- Test fault paths (error scenarios)
- Verify governor limit usage (DML operations, SOQL queries)
- Test with different user permissions
- Test with different record types

## Related Patterns

- <a href="{{ '/rag/development/flow-patterns.html' | relative_url }}">Flow Patterns</a> - Comprehensive Flow patterns and best practices
- <a href="{{ '/rag/development/order-of-execution.html' | relative_url }}">Order of Execution</a> - Understanding when Flows execute in the transaction
- <a href="{{ '/rag/development/governor-limits-and-optimization.html' | relative_url }}">Governor Limits and Optimization</a> - Performance considerations for Flows
- <a href="{{ '/rag/code-examples/flow/subflow-examples.html' | relative_url }}">Subflow Examples</a> - Reusable Subflow patterns
- <a href="{{ '/rag/development/error-handling-and-logging.html' | relative_url }}">Error Handling and Logging</a> - Error handling patterns for Flows
