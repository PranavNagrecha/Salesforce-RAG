---
title: "Subflow Code Examples"
level: "Intermediate"
tags:
  - flow
  - code-examples
  - subflow
  - reusable-components
last_reviewed: "2025-01-XX"
---

# Subflow Code Examples

> This file contains complete, working examples for Subflow patterns.
> All examples follow Salesforce best practices and can be used as templates.

## Overview

Subflows are reusable flow components that can be called from other Flows or Apex. They enable code reuse, easier maintenance, and consistent business logic across multiple automation contexts. This document provides practical examples of common Subflow patterns.

⚠️ **Note**: Process Builder is deprecated - use Record-Triggered Flows instead. Subflows can be called from Record-Triggered Flows.

**Related Patterns**:
- [Flow Patterns](code-examples/development/flow-patterns.html) - Complete Flow design patterns
- [Record-Triggered Examples](code-examples/flow/record-triggered-examples.html) - Automated flow patterns
- [Screen Flow Examples](code-examples/flow/screen-flow-examples.html) - User interaction flows

## Examples

### Example 1: Reusable Task Creation Subflow

**Pattern**: Subflow for creating tasks consistently
**Use Case**: Creating tasks with standard logic across multiple flows
**Complexity**: Basic
**Related Patterns**: [Flow Patterns](../development/flow-patterns.html#subflows)

**Problem**:
You need to create tasks consistently across multiple Record-Triggered Flows. Instead of duplicating the logic, create a reusable Subflow.

**Solution**:

**Subflow Configuration**:
- **Flow Type**: Autolaunched Flow
- **Flow API Name**: Create_Advisor_Task
- **Input Variables**:
  - `WhatId` (Record ID, Required) - The record the task is related to
  - `Subject` (Text, Required) - Task subject
  - `Priority` (Text, Optional) - Task priority (default: Normal)
  - `DueDate` (Date/Time, Optional) - Task due date
  - `OwnerId` (Record ID, Optional) - Task owner (default: current user)
- **Output Variables**: None

**Subflow Elements**:

1. **Assignment Element**: Set Default Values
   - **Variable**: `Priority`
   - **Value**: `IF(ISBLANK({!Priority}), 'Normal', {!Priority})`
   - **Variable**: `OwnerId`
   - **Value**: `IF(ISBLANK({!OwnerId}), {!$User.Id}, {!OwnerId})`

2. **Create Records Element**: Create Task
   - **Object**: Task
   - **Field Values**:
     - `WhatId`: `{!WhatId}`
     - `Subject`: `{!Subject}`
     - `Priority`: `{!Priority}`
     - `ActivityDate`: `{!DueDate}`
     - `OwnerId`: `{!OwnerId}`
     - `Status`: `Not Started`

**Usage in Parent Flow**:

1. **Subflow Element**: Call Create Advisor Task
   - **Subflow**: Create_Advisor_Task
   - **Input Values**:
     - `WhatId`: `{!$Record.Id}`
     - `Subject`: `'Review Application: ' + {!$Record.Name}`
     - `Priority`: `'High'`
     - `DueDate`: `TODAY() + 3`

**Best Practices**:
- Use input variables for flexibility
- Provide default values for optional inputs
- Document input/output variables
- Keep Subflows focused on single responsibilities

### Example 2: Status Update Subflow

**Pattern**: Subflow for updating record status
**Use Case**: Consistent status updates across multiple flows
**Complexity**: Basic
**Related Patterns**: [Flow Patterns](../development/flow-patterns.html#subflows)

**Problem**:
You need to update record status consistently with logging and notifications.

**Solution**:

**Subflow Configuration**:
- **Flow Type**: Autolaunched Flow
- **Flow API Name**: Update_Record_Status
- **Input Variables**:
  - `RecordId` (Record ID, Required) - Record to update
  - `NewStatus` (Text, Required) - New status value
  - `StatusField` (Text, Required) - API name of status field
  - `SendNotification` (Checkbox, Optional) - Whether to send notification (default: false)
- **Output Variables**:
  - `Success` (Checkbox) - Whether update succeeded

**Subflow Elements**:

1. **Get Records Element**: Get Current Record
   - **Object**: Use `{!RecordId}` to determine object type
   - **Filter**: `Id` EQUALS `{!RecordId}`
   - **Store**: `CurrentRecord`

2. **Decision Element**: Check if Status Changed
   - **Outcome 1**: Status changed
     - **Criteria**: `{!CurrentRecord[StatusField]}` NOT EQUALS `{!NewStatus}`
   - **Outcome 2**: Status unchanged (Default Outcome)

3. **Assignment Element** (in Status changed outcome):
   - **Variable**: `RecordToUpdate`
   - **Value**: `{!CurrentRecord}`
   - **Field Update**: `{!StatusField}` = `{!NewStatus}`

4. **Update Records Element** (in Status changed outcome):
   - **Object**: Same as CurrentRecord
   - **Records**: `{!RecordToUpdate}`

5. **Decision Element** (in Status changed outcome): Check if Send Notification
   - **Outcome 1**: Send notification
     - **Criteria**: `{!SendNotification}` EQUALS `true`
   - **Outcome 2**: Don't send (Default Outcome)

6. **Email Alerts Element** (in Send notification outcome):
   - **Email Alert**: Status Change Notification
   - **Recipients**: Record Owner

7. **Assignment Element**: Set Success Output
   - **Variable**: `Success`
   - **Value**: `true`

**Usage in Parent Flow**:

1. **Subflow Element**: Update Status
   - **Subflow**: Update_Record_Status
   - **Input Values**:
     - `RecordId`: `{!$Record.Id}`
     - `NewStatus`: `'Approved'`
     - `StatusField`: `'Status__c'`
     - `SendNotification`: `true`

2. **Decision Element**: Check if Update Succeeded
   - **Outcome 1**: Success
     - **Criteria**: `{!Update_Record_Status.Success}` EQUALS `true`
   - **Outcome 2**: Failed (Default Outcome)

**Best Practices**:
- Check if update is needed before updating
- Use output variables to communicate results
- Handle errors gracefully
- Make Subflows reusable with input variables

### Example 3: Integration Call Wrapper Subflow

**Pattern**: Subflow for calling Apex methods consistently
**Use Case**: Wrapping Apex calls with error handling and logging
**Complexity**: Intermediate
**Related Patterns**: [Flow Patterns](../development/flow-patterns.html#subflows)

**Problem**:
You need to call Apex methods from multiple flows with consistent error handling.

**Solution**:

**Subflow Configuration**:
- **Flow Type**: Autolaunched Flow
- **Flow API Name**: Call_Integration_Service
- **Input Variables**:
  - `ServiceName` (Text, Required) - Name of Apex service method
  - `InputData` (Text, Optional) - JSON string of input data
  - `RecordId` (Record ID, Optional) - Related record ID
- **Output Variables**:
  - `Success` (Checkbox) - Whether call succeeded
  - `ResponseData` (Text) - Response data from Apex
  - `ErrorMessage` (Text) - Error message if failed

**Subflow Elements**:

1. **Apex Action Element**: Call Integration Service
   - **Apex Action**: `IntegrationService.invoke`
   - **Input Parameters**:
     - `serviceName`: `{!ServiceName}`
     - `inputData`: `{!InputData}`
     - `recordId`: `{!RecordId}`
   - **Store**: `IntegrationResult`

2. **Decision Element**: Check if Call Succeeded
   - **Outcome 1**: Success
     - **Criteria**: `{!IntegrationResult.success}` EQUALS `true`
   - **Outcome 2**: Failed (Default Outcome)

3. **Assignment Element** (in Success outcome):
   - **Variable**: `Success`
   - **Value**: `true`
   - **Variable**: `ResponseData`
   - **Value**: `{!IntegrationResult.responseData}`

4. **Assignment Element** (in Failed outcome):
   - **Variable**: `Success`
   - **Value**: `false`
   - **Variable**: `ErrorMessage`
   - **Value**: `{!IntegrationResult.errorMessage}`

5. **Create Records Element** (in Failed outcome): Log Error
   - **Object**: Log__c
   - **Field Values**:
     - `Service_Name__c`: `{!ServiceName}`
     - `Error_Message__c`: `{!ErrorMessage}`
     - `Record_Id__c`: `{!RecordId}`

**Usage in Parent Flow**:

1. **Subflow Element**: Call Integration
   - **Subflow**: Call_Integration_Service
   - **Input Values**:
     - `ServiceName`: `'SyncToExternalSystem'`
     - `InputData`: `'{ "action": "update", "recordId": "' + {!$Record.Id} + '" }'`
     - `RecordId`: `{!$Record.Id}`

2. **Decision Element**: Check Result
   - **Outcome 1**: Success
     - **Criteria**: `{!Call_Integration_Service.Success}` EQUALS `true`
   - **Outcome 2**: Failed (Default Outcome)

**Best Practices**:
- Wrap Apex calls with error handling
- Log errors for troubleshooting
- Use output variables to communicate results
- Make Subflows flexible with input parameters

### Example 4: Data Validation Subflow

**Pattern**: Subflow for reusable validation logic
**Use Case**: Validating data consistently across multiple flows
**Complexity**: Intermediate
**Related Patterns**: [Flow Patterns](../development/flow-patterns.html#subflows)

**Problem**:
You need to validate email addresses and phone numbers consistently across multiple flows.

**Solution**:

**Subflow Configuration**:
- **Flow Type**: Autolaunched Flow
- **Flow API Name**: Validate_Contact_Data
- **Input Variables**:
  - `Email` (Text, Optional) - Email to validate
  - `Phone` (Text, Optional) - Phone to validate
- **Output Variables**:
  - `IsValid` (Checkbox) - Whether data is valid
  - `ValidationErrors` (Text) - Comma-separated list of errors

**Subflow Elements**:

1. **Formula Element**: Check Email Format
   - **Name**: EmailValid
   - **Formula**: `IF(ISBLANK({!Email}), true, CONTAINS({!Email}, '@'))`

2. **Formula Element**: Check Phone Format
   - **Name**: PhoneValid
   - **Formula**: `IF(ISBLANK({!Phone}), true, LEN(SUBSTITUTE({!Phone}, ' ', '')) >= 10)`

3. **Decision Element**: Determine Validity
   - **Outcome 1**: Valid
     - **Criteria**: `{!EmailValid}` EQUALS `true` AND `{!PhoneValid}` EQUALS `true`
   - **Outcome 2**: Invalid (Default Outcome)

4. **Assignment Element** (in Valid outcome):
   - **Variable**: `IsValid`
   - **Value**: `true`
   - **Variable**: `ValidationErrors`
   - **Value**: `''`

5. **Assignment Element** (in Invalid outcome):
   - **Variable**: `IsValid`
   - **Value**: `false`
   - **Variable**: `ValidationErrors`
   - **Value**: `IF(NOT({!EmailValid}), 'Invalid email format. ', '') + IF(NOT({!PhoneValid}), 'Invalid phone format. ', '')`

**Usage in Parent Flow**:

1. **Subflow Element**: Validate Data
   - **Subflow**: Validate_Contact_Data
   - **Input Values**:
     - `Email`: `{!Contact_Email}`
     - `Phone`: `{!Contact_Phone}`

2. **Decision Element**: Check Validation
   - **Outcome 1**: Valid
     - **Criteria**: `{!Validate_Contact_Data.IsValid}` EQUALS `true`
   - **Outcome 2**: Invalid (Default Outcome)

3. **Screen Element** (in Invalid outcome): Show Errors
   - **Display**: `{!Validate_Contact_Data.ValidationErrors}`

**Best Practices**:
- Create reusable validation logic
- Return clear error messages
- Use output variables for results
- Make validation flexible with optional inputs

### Example 5: Notification Builder Subflow

**Pattern**: Subflow for building notification payloads
**Use Case**: Consistent notification formatting across flows
**Complexity**: Intermediate
**Related Patterns**: [Flow Patterns](../development/flow-patterns.html#subflows)

**Problem**:
You need to build notification payloads consistently for Platform Events or external systems.

**Solution**:

**Subflow Configuration**:
- **Flow Type**: Autolaunched Flow
- **Flow API Name**: Build_Notification_Payload
- **Input Variables**:
  - `RecordId` (Record ID, Required) - Record ID
  - `RecordType` (Text, Required) - Object API name
  - `Action` (Text, Required) - Action type (created, updated, deleted)
  - `Fields` (Text, Optional) - Comma-separated list of fields to include
- **Output Variables**:
  - `Payload` (Text) - JSON payload string

**Subflow Elements**:

1. **Get Records Element**: Get Record Data
   - **Object**: Use `{!RecordType}` to determine object
   - **Filter**: `Id` EQUALS `{!RecordId}`
   - **Store**: `RecordData`

2. **Assignment Element**: Build Payload
   - **Variable**: `Payload`
   - **Value**: `'{ "recordId": "' + {!RecordId} + '", "recordType": "' + {!RecordType} + '", "action": "' + {!Action} + '", "timestamp": "' + NOW() + '" }'`

**Usage in Parent Flow**:

1. **Subflow Element**: Build Payload
   - **Subflow**: Build_Notification_Payload
   - **Input Values**:
     - `RecordId`: `{!$Record.Id}`
     - `RecordType`: `'Contact'`
     - `Action`: `'updated'`
     - `Fields`: `'Name,Email,Phone'`

2. **Apex Action Element**: Publish Platform Event
   - **Apex Action**: `PlatformEventService.publish`
   - **Input Parameter**: `payload` = `{!Build_Notification_Payload.Payload}`

**Best Practices**:
- Build reusable notification logic
- Use consistent payload format
- Include necessary metadata
- Make Subflows flexible with input parameters

## Common Patterns

### Pattern 1: Input/Output Variables

Use input variables for flexibility:
- Required inputs for essential data
- Optional inputs with defaults
- Output variables to communicate results

### Pattern 2: Error Handling

Handle errors consistently:
- Check for errors after operations
- Set output variables to indicate success/failure
- Log errors for troubleshooting

### Pattern 3: Reusability

Design Subflows for reuse:
- Single responsibility
- Flexible input parameters
- Clear documentation
- Consistent naming

## Related Examples

- [Record-Triggered Examples](code-examples/flow/record-triggered-examples.html) - Automated flow patterns
- [Screen Flow Examples](code-examples/flow/screen-flow-examples.html) - User interaction flows

## See Also

- [Flow Patterns](code-examples/development/flow-patterns.html) - Complete Flow design patterns
- [Error Handling and Logging](code-examples/development/error-handling-and-logging.html) - Error handling patterns
