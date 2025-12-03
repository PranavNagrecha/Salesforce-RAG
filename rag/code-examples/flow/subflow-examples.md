---
layout: default
title: Subflow Code Examples
description: Subflows are reusable flow components that can be called from other Flows or Apex, enabling code reuse and easier maintenance
permalink: /rag/code-examples/flow/subflow-examples.html
level: Intermediate
tags:
  - code-examples
  - flow
  - subflow
  - reusable-components
last_reviewed: 2025-12-03
---

# Subflow Code Examples

## Overview

Subflows extract logical chunks into reusable components that can be called from multiple Flows or Apex. These examples demonstrate common patterns for:

- **Reusable logic**: Common validation, transformation, and calculation logic
- **Task creation**: Standardized task creation patterns
- **Notification logic**: Reusable email and notification patterns
- **Data transformation**: Common data transformation utilities
- **Assignment rules**: Reusable assignment logic

## When to Use

### Use Subflows When

- Same logic is used in multiple Flows
- Need to extract complex logic for clarity
- Want to test logic independently
- Need consistent logic across multiple contexts
- Want easier maintenance (update once, affects all callers)
- Need reusable utility functions

### Avoid Subflows When

- Logic is only used once (keep it in the main flow)
- Logic is very simple (not worth the abstraction)
- Need to break governor limits (Subflows share limits with caller)
- Need different error handling per context (consider separate flows)

## Example 1: Reusable Task Creation

**Use Case**: Create a standardized follow-up task that can be reused across multiple Flows.

**Subflow Name**: `Subflow_Create_Follow_Up_Task`

**Input Variables**:
- `RelatedRecordId` (Text, required): ID of the record to relate the task to
- `TaskSubject` (Text, required): Subject of the task
- `TaskPriority` (Picklist, optional): Priority of the task (default: "Medium")
- `DaysUntilDue` (Number, optional): Days until task is due (default: 7)
- `AssignedToUserId` (Text, optional): User ID to assign task to (default: record owner)

**Output Variables**:
- `CreatedTaskId` (Text): ID of the created task
- `IsSuccess` (Checkbox): Whether task creation succeeded
- `ErrorMessage` (Text): Error message if creation failed

**Subflow Structure**:
1. **Start Element**: Subflow
   - Input Variables: All listed above
   - Output Variables: All listed above

2. **Assignment Element**: Set Default Values
   - `TaskPriority` = `IF(ISBLANK(TaskPriority), 'Medium', TaskPriority)`
   - `DaysUntilDue` = `IF(ISBLANK(DaysUntilDue), 7, DaysUntilDue)`

3. **Get Records Element**: Get Record Owner (if not assigned)
   - Object: Record (dynamic based on RelatedRecordId)
   - Filter: `Id = {!RelatedRecordId}`
   - Store In: `RelatedRecord` (single record variable)
   - Get Fields: `OwnerId`

4. **Decision Node**: Check Assignment
   - Outcome 1: `ISBLANK(AssignedToUserId)` → Use Record Owner
   - Outcome 2: `NOT(ISBLANK(AssignedToUserId))` → Use Assigned User

5. **Assignment Element**: Set Assignment
   - `FinalOwnerId` = `IF(ISBLANK(AssignedToUserId), RelatedRecord.OwnerId, AssignedToUserId)`

6. **Create Records Element**: Create Task
   - Object: Task
   - How Many: One
   - Fields:
     - `Subject` = `{!TaskSubject}`
     - `WhatId` = `{!RelatedRecordId}`
     - `Status` = `'Not Started'`
     - `Priority` = `{!TaskPriority}`
     - `OwnerId` = `{!FinalOwnerId}`
     - `ActivityDate` = `TODAY() + {!DaysUntilDue}`
   - Store In: `NewTask` (single record variable)
   - Fault Path: Set error and continue

7. **Decision Node**: Check Success
   - Outcome 1: `NewTask.Id != null` → Success Path
   - Outcome 2: Default → Error Path

8. **Assignment Element**: Set Success Output
   - `CreatedTaskId` = `{!NewTask.Id}`
   - `IsSuccess` = `true`
   - `ErrorMessage` = `''`

9. **Assignment Element**: Set Error Output
   - `CreatedTaskId` = `''`
   - `IsSuccess` = `false`
   - `ErrorMessage` = `'Failed to create task: ' & {!$Flow.FaultMessage}`

10. **End Element**: End Subflow
    - Return: Output variables

**Usage in Parent Flow**:
```
Call Subflow: Create Follow-Up Task
  Input:
    RelatedRecordId = {!$Record.Id}
    TaskSubject = 'Follow up on Case ' & {!$Record.CaseNumber}
    TaskPriority = {!$Record.Priority}
    DaysUntilDue = 3
  Output:
    CreatedTaskId → TaskId variable
    IsSuccess → TaskCreatedSuccessfully variable
```

**Key Points**:
- Use input variables for flexibility
- Provide default values for optional inputs
- Return success/failure status to caller
- Handle errors gracefully and return error information
- Document input/output requirements clearly

## Example 2: Reusable Status Update

**Use Case**: Update related records' status when parent record status changes.

**Subflow Name**: `Subflow_Update_Related_Records_Status`

**Input Variables**:
- `ParentRecordId` (Text, required): ID of the parent record
- `ParentObjectName` (Text, required): API name of parent object (e.g., "Account")
- `ChildObjectName` (Text, required): API name of child object (e.g., "Case")
- `RelationshipFieldName` (Text, required): API name of lookup field (e.g., "AccountId")
- `NewStatus` (Text, required): New status value to set
- `StatusFieldName` (Text, required): API name of status field (e.g., "Status")
- `FilterCriteria` (Text, optional): Additional filter criteria (e.g., "Status != 'Closed'")

**Output Variables**:
- `RecordsUpdated` (Number): Number of records updated
- `IsSuccess` (Checkbox): Whether update succeeded
- `ErrorMessage` (Text): Error message if update failed

**Subflow Structure**:
1. **Start Element**: Subflow
   - Input Variables: All listed above
   - Output Variables: All listed above

2. **Get Records Element**: Get Related Records
   - Object: Dynamic (based on ChildObjectName)
   - Filter: `{RelationshipFieldName} = {!ParentRecordId} AND {StatusFieldName} != {!NewStatus} {FilterCriteria}`
   - Store In: `RelatedRecords` (collection variable)

3. **Decision Node**: Check if Records Exist
   - Outcome 1: `RelatedRecords` is not empty → Update Records
   - Outcome 2: `RelatedRecords` is empty → No Records to Update

4. **Assignment Element**: Prepare Records for Update
   - Loop through `RelatedRecords`
   - Set `{StatusFieldName}` = `{!NewStatus}` for each record

5. **Update Records Element**: Update Related Records
   - Records: `RelatedRecords`
   - How Many: Multiple
   - Fields: Update status field
   - Fault Path: Set error and continue

6. **Assignment Element**: Set Success Output
   - `RecordsUpdated` = `COUNT(RelatedRecords)`
   - `IsSuccess` = `true`
   - `ErrorMessage` = `''`

7. **Assignment Element**: Set Error Output
   - `RecordsUpdated` = `0`
   - `IsSuccess` = `false`
   - `ErrorMessage` = `'Failed to update records: ' & {!$Flow.FaultMessage}`

8. **End Element**: End Subflow

**Key Points**:
- Use dynamic object and field names for reusability
- Query related records before updating
- Only update records that need updating (avoid unnecessary DML)
- Return count of updated records to caller
- Handle empty collections gracefully

## Example 3: Reusable Email Notification

**Use Case**: Send standardized email notifications that can be reused across multiple Flows.

**Subflow Name**: `Subflow_Send_Email_Notification`

**Input Variables**:
- `ToEmailAddresses` (Text, required): Comma-separated email addresses
- `EmailSubject` (Text, required): Email subject
- `EmailBody` (Text, required): Email body (plain text or HTML)
- `RelatedRecordId` (Text, optional): ID of related record for email template
- `TemplateId` (Text, optional): Email template ID (if using template)
- `UseTemplate` (Checkbox, optional): Whether to use email template (default: false)

**Output Variables**:
- `EmailSent` (Checkbox): Whether email was sent successfully
- `ErrorMessage` (Text): Error message if send failed

**Subflow Structure**:
1. **Start Element**: Subflow
   - Input Variables: All listed above
   - Output Variables: All listed above

2. **Decision Node**: Check if Using Template
   - Outcome 1: `UseTemplate = true` → Use Email Template Path
   - Outcome 2: `UseTemplate = false` → Use Custom Email Path

3. **Send Email Element** (Template Path):
   - Email Template: `{!TemplateId}`
   - Recipients: `{!ToEmailAddresses}`
   - Related Record: `{!RelatedRecordId}`
   - Store In: `EmailResult` (single record variable)
   - Fault Path: Set error and continue

4. **Send Email Element** (Custom Path):
   - To Addresses: `{!ToEmailAddresses}`
   - Subject: `{!EmailSubject}`
   - Body: `{!EmailBody}`
   - Store In: `EmailResult` (single record variable)
   - Fault Path: Set error and continue

5. **Decision Node**: Check Success
   - Outcome 1: `EmailResult.Id != null` → Success Path
   - Outcome 2: Default → Error Path

6. **Assignment Element**: Set Success Output
   - `EmailSent` = `true`
   - `ErrorMessage` = `''`

7. **Assignment Element**: Set Error Output
   - `EmailSent` = `false`
   - `ErrorMessage` = `'Failed to send email: ' & {!$Flow.FaultMessage}`

8. **End Element**: End Subflow

**Key Points**:
- Support both template-based and custom emails
- Handle multiple recipients (comma-separated)
- Return success/failure status to caller
- Handle errors gracefully

## Example 4: Reusable Data Validation

**Use Case**: Validate data format and business rules that can be reused across multiple Flows.

**Subflow Name**: `Subflow_Validate_Contact_Data`

**Input Variables**:
- `Email` (Text, required): Email address to validate
- `Phone` (Text, optional): Phone number to validate
- `DateOfBirth` (Date, optional): Date of birth to validate

**Output Variables**:
- `IsValid` (Checkbox): Whether all validations passed
- `ValidationErrors` (Text): Comma-separated list of validation errors
- `EmailValid` (Checkbox): Whether email is valid
- `PhoneValid` (Checkbox): Whether phone is valid
- `DateOfBirthValid` (Checkbox): Whether date of birth is valid

**Subflow Structure**:
1. **Start Element**: Subflow
   - Input Variables: All listed above
   - Output Variables: All listed above

2. **Assignment Element**: Initialize Outputs
   - `IsValid` = `true`
   - `ValidationErrors` = `''`
   - `EmailValid` = `true`
   - `PhoneValid` = `true`
   - `DateOfBirthValid` = `true`

3. **Decision Node**: Validate Email
   - Outcome 1: `CONTAINS(Email, '@') AND CONTAINS(Email, '.')` → Email Valid
   - Outcome 2: Default → Email Invalid

4. **Assignment Element**: Set Email Invalid
   - `EmailValid` = `false`
   - `IsValid` = `false`
   - `ValidationErrors` = `{!ValidationErrors} & 'Invalid email format; '`

5. **Decision Node**: Validate Phone (if provided)
   - Outcome 1: `ISBLANK(Phone) OR LEN(Phone) >= 10` → Phone Valid
   - Outcome 2: Default → Phone Invalid

6. **Assignment Element**: Set Phone Invalid
   - `PhoneValid` = `false`
   - `IsValid` = `false`
   - `ValidationErrors` = `{!ValidationErrors} & 'Invalid phone format; '`

7. **Decision Node**: Validate Date of Birth (if provided)
   - Outcome 1: `ISBLANK(DateOfBirth) OR DateOfBirth < TODAY()` → Date Valid
   - Outcome 2: Default → Date Invalid

8. **Assignment Element**: Set Date Invalid
   - `DateOfBirthValid` = `false`
   - `IsValid` = `false`
   - `ValidationErrors` = `{!ValidationErrors} & 'Date of birth must be in the past; '`

9. **End Element**: End Subflow

**Usage in Parent Flow**:
```
Call Subflow: Validate Contact Data
  Input:
    Email = {!EmailInput}
    Phone = {!PhoneInput}
    DateOfBirth = {!DateOfBirthInput}
  Output:
    IsValid → ValidationPassed variable
    ValidationErrors → ErrorMessages variable

Decision: Check Validation
  If IsValid = true → Continue
  If IsValid = false → Show Error Screen
```

**Key Points**:
- Validate each field independently
- Return detailed validation results
- Aggregate error messages for user display
- Support optional fields (only validate if provided)
- Return boolean flags for each validation

## Example 5: Reusable Assignment Logic

**Use Case**: Assign records to users or queues based on configurable rules.

**Subflow Name**: `Subflow_Assign_Record_By_Rules`

**Input Variables**:
- `RecordId` (Text, required): ID of record to assign
- `RecordType` (Text, required): Record type of the record
- `Priority` (Text, optional): Priority of the record
- `Region` (Text, optional): Region for assignment

**Output Variables**:
- `AssignedToId` (Text): ID of user or queue assigned
- `AssignmentReason` (Text): Reason for assignment
- `IsSuccess` (Checkbox): Whether assignment succeeded

**Subflow Structure**:
1. **Start Element**: Subflow
   - Input Variables: All listed above
   - Output Variables: All listed above

2. **Get Records Element**: Get Assignment Rules (from Custom Metadata)
   - Object: AssignmentRule__mdt (custom metadata)
   - Filter: `RecordType__c = {!RecordType} AND Active__c = true`
   - Store In: `AssignmentRules` (collection variable)
   - Sort: `Priority__c ASC`

3. **Loop Element**: Evaluate Rules
   - Loop Through: `AssignmentRules`
   - Current Item: `CurrentRule`

4. **Decision Node**: Check Rule Criteria
   - Outcome 1: `Priority = CurrentRule.Priority__c AND Region = CurrentRule.Region__c` → Match
   - Outcome 2: `Priority = CurrentRule.Priority__c` → Match (Region not required)
   - Outcome 3: Default → No Match, Continue Loop

5. **Assignment Element**: Set Assignment
   - `AssignedToId` = `CurrentRule.AssignedToId__c`
   - `AssignmentReason` = `'Assigned by rule: ' & CurrentRule.Label`
   - `IsSuccess` = `true`
   - Exit Loop

6. **Decision Node**: Check if Assigned
   - Outcome 1: `ISBLANK(AssignedToId)` → Use Default Assignment
   - Outcome 2: `NOT(ISBLANK(AssignedToId))` → Assignment Complete

7. **Assignment Element**: Set Default Assignment
   - `AssignedToId` = `DefaultQueueId` (from custom setting)
   - `AssignmentReason` = `'Assigned to default queue'`
   - `IsSuccess` = `true`

8. **End Element**: End Subflow

**Key Points**:
- Use Custom Metadata for configurable assignment rules
- Evaluate rules in priority order
- Support multiple criteria (priority, region, etc.)
- Provide default assignment if no rules match
- Return assignment reason for audit trail

## Testing Considerations

### Test Scenarios

1. **Input Validation**:
   - Test with all required inputs
   - Test with optional inputs (null and provided)
   - Test with invalid inputs
   - Test with edge cases (empty strings, null values)

2. **Logic Execution**:
   - Test all decision node paths
   - Test loop iterations
   - Test conditional logic
   - Test default value assignments

3. **Output Validation**:
   - Verify output variables are set correctly
   - Verify success/failure flags
   - Verify error messages
   - Verify data transformations

4. **Integration**:
   - Test Subflow called from different parent Flows
   - Test Subflow called from Apex (if applicable)
   - Test with different data scenarios
   - Test error propagation to parent

### Best Practices

- Test Subflows independently before using in parent Flows
- Document all input/output requirements clearly
- Use descriptive variable names
- Handle all error scenarios
- Provide default values for optional inputs
- Version Subflows carefully (breaking changes affect all callers)

## Related Patterns

- <a href="{{ '/rag/development/flow-patterns.html' | relative_url }}">Flow Patterns</a> - Comprehensive Flow patterns including Subflow best practices
- <a href="{{ '/rag/code-examples/flow/record-triggered-examples.html' | relative_url }}">Record-Triggered Flow Examples</a> - Examples of using Subflows in Record-Triggered Flows
- <a href="{{ '/rag/code-examples/flow/screen-flow-examples.html' | relative_url }}">Screen Flow Examples</a> - Examples of using Subflows in Screen Flows
- <a href="{{ '/rag/development/custom-settings-metadata-patterns.html' | relative_url }}">Custom Settings and Metadata Patterns</a> - Using Custom Metadata for Subflow configuration
