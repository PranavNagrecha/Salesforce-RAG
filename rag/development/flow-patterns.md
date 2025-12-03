---
layout: default
title: Flow Design and Orchestration Patterns
description: Comprehensive Flow patterns and best practices based on real implementation experience across enterprise-scale Salesforce projects
permalink: /rag/development/flow-patterns.html
---

# Flow Design and Orchestration Patterns

> **Based on Real Implementation Experience**: This document captures Flow patterns and practices derived from actual implementation experience across multiple enterprise-scale Salesforce projects, including public sector portals serving 40,000+ concurrent users and higher education CRM implementations with complex integrations.

## Overview

Flow is the primary automation engine across projects, with Apex reserved for complex logic, integrations, and performance-critical scenarios. This declarative-first approach enables faster development, easier maintenance, and better collaboration between admins and developers.

**Core Philosophy**: Prefer Flows over Apex when logic can be expressed declaratively. Use Apex for complex logic that Flow cannot handle efficiently, tight control over governor limits, heavy reuse across multiple contexts, or integrations requiring complex authentication and error handling.

## Prerequisites

**Required Knowledge**:
- Understanding of Salesforce automation concepts
- Familiarity with declarative automation tools
- Knowledge of Salesforce data model and relationships
- Understanding of governor limits and performance considerations
- Experience with error handling patterns

**Recommended Reading**:
- <a href="{{ '/rag/development/order-of-execution.html' | relative_url }}">Order of Execution</a> - Understanding when Flows execute in the transaction
- <a href="{{ '/rag/development/apex-patterns.html' | relative_url }}">Apex Patterns</a> - When to use Apex vs Flow
- <a href="{{ '/rag/development/error-handling-and-logging.html' | relative_url }}">Error Handling and Logging</a> - Error handling patterns for Flows
- <a href="{{ '/rag/development/governor-limits-and-optimization.html' | relative_url }}">Governor Limits and Optimization</a> - Performance considerations

## When to Use Flow vs Apex

### Use Flow When:
- Logic can be expressed declaratively
- Need to create/update related records based on record changes
- Need to orchestrate simple workflows with decision logic
- Need guided user interactions (Screen Flows)
- Need to publish Platform Events (preferred over Apex for declarative event publication)
- Need periodic batch operations (Scheduled Flows)
- Need reusable logic chunks (Subflows)
- Business users need to maintain the logic
- Need faster development and easier maintenance

### Use Apex When:
- Complex logic that Flow cannot handle efficiently
- Tight control over governor limits required
- Heavy reuse across multiple contexts (LWCs, external APIs, other Apex)
- Integrations requiring complex authentication and error handling
- Complex data transformations or calculations
- Performance-critical scenarios requiring optimization
- Complex loop logic or nested iterations
- Advanced error handling with custom exceptions
- Need to make callouts from triggers (before-save Flows cannot make callouts)

## Flow Types and Detailed Use Cases

### Record-Triggered Flows

**Primary Workhorse**: Record-Triggered Flows are the primary automation tool for creating/updating related records, status transitions, and notifications.

#### Before-Save Flows

**Execution Context**: Run before the record is saved to the database, during the before-save phase of the order of execution.

**Capabilities**:
- Can modify field values on the triggering record
- Cannot perform DML operations on other records
- Cannot make callouts
- Cannot publish Platform Events
- Run synchronously and impact user save time

**Use Cases**:
- Field defaulting and value setting
- Simple field calculations
- Field value transformations
- Simple validations (though validation rules are preferred)
- Field value normalization

**Best Practices**:
- Keep logic fast and simple (impacts user save time)
- Use strict entry criteria to avoid unnecessary executions
- Only update fields on the triggering record
- Avoid complex calculations that could slow down save time
- Use fast field updates when possible

**Real Example**: `Case_BeforeSave_Defaulting` - Sets default values on Case creation based on record type and other criteria.

**Example Pattern**:
```
Entry Criteria: Record Type = 'Support Case' AND Status = 'New'
Logic:
  - Set Priority = 'Medium' if Priority is null
  - Set Owner = Queue if Owner is null
  - Calculate Due Date based on SLA rules
```

#### After-Save Flows

**Execution Context**: Run after the record is saved to the database, during the after-save phase of the order of execution.

**Capabilities**:
- Record is read-only (cannot modify triggering record fields)
- Can perform DML operations on other records
- Can make callouts (via Apex actions)
- Can publish Platform Events
- Can query related data
- Can create/update/delete related records

**Use Cases**:
- Creating related records
- Updating related records
- Publishing Platform Events for integrations
- Sending email notifications
- Creating tasks and activities
- Complex validations requiring queries
- Rollup calculations
- Integration orchestration

**Best Practices**:
- Use strict entry criteria
- Route by record state early (New vs Update, channel, person type)
- Use Subflows for complex tasks
- Aggregate DML operations to minimize governor limit usage
- Move heavy operations to async processing when possible

**Real Example**: `App_AfterSave_ApplicationStatusOrchestration` - Orchestrates application status changes, creates related records, publishes Platform Events, and sends notifications.

**Example Pattern**:
```
Entry Criteria: Record Type = 'Application' AND Status changed
First Decision Node:
  - Route by IsNew (New vs Update)
  - Route by Channel (Portal vs Internal vs Integration)
  - Route by Person Type (Student vs Vendor vs Staff)
Subflows:
  - "Create Advisor Tasks"
  - "Sync Application Status to Child Objects"
  - "Build Notification Payload"
Actions:
  - Create related records
  - Publish Platform Event
  - Send email notification
```

#### Record-Triggered Flow Structure Pattern

**Consistent Structure**: All Record-Triggered Flows follow a consistent structure pattern.

**Before-Save Flow Structure**:
1. **Entry Criteria**: Strict criteria matching specific conditions
2. **Fast Field Updates**: Update triggering record fields only
3. **Simple Calculations**: Basic field calculations and defaulting
4. **No DML**: No DML operations on other objects
5. **No Callouts**: No callouts or Platform Events

**After-Save Flow Structure**:
1. **Entry Criteria**: Strict criteria matching specific conditions
2. **First Decision Node**: Route by context (New vs Update, Channel, Person Type)
3. **Subflows**: Extract complex tasks into Subflows
4. **Related Record Operations**: Create/update/delete related records
5. **Integration Calls**: Call Apex actions for integrations
6. **Platform Event Publishing**: Publish events for event-driven architecture
7. **Error Handling**: Fault paths for all operations

### Screen Flows

**Guided Data Capture**: Screen Flows provide step-by-step user interactions for complex processes.

**Use Cases**:
- Multi-step case/application handling
- Guided data capture with validation
- User onboarding workflows
- Feedback surveys
- Step-by-step processes requiring user input
- Complex forms with conditional logic
- Approval workflows with user input
- Data collection workflows

**Best Practices**:
- Break complex processes into logical steps
- Use decision nodes to show/hide steps based on user input
- Validate data at each step
- Provide clear navigation (Next, Back, Cancel)
- Show progress indicators
- Handle errors gracefully with user-friendly messages
- Use Subflows for reusable screen logic

**Real Example**: `Mid_Point_Evaluation_Screen_Flow` - Guided evaluation process sending 29,004 emails (83.9% of automated emails in one org).

**Screen Flow Structure Pattern**:
1. **Introduction Screen**: Welcome message and instructions
2. **Data Collection Screens**: Step-by-step data input with validation
3. **Decision Nodes**: Route based on user input
4. **Review Screen**: Summary of collected data
5. **Confirmation Screen**: Success message and next steps
6. **Error Handling**: User-friendly error messages

### Scheduled Flows

**Periodic Operations**: Scheduled Flows run on a schedule for batch operations.

**Use Cases**:
- Periodic cleanup (archiving old records)
- Data maintenance (updating calculated fields)
- Batch record updates
- Scheduled notifications
- Data synchronization tasks
- Report generation and distribution
- Compliance and audit tasks

**Best Practices**:
- Use entry criteria to filter records efficiently
- Process records in batches to avoid governor limits
- Log all operations for troubleshooting
- Handle errors gracefully with retry logic
- Monitor execution time and optimize as needed
- Use Subflows for reusable batch logic

**Scheduled Flow Structure Pattern**:
1. **Entry Criteria**: Filter records to process
2. **Decision Node**: Route by record state or criteria
3. **Batch Processing**: Process records in collections
4. **Error Handling**: Log errors and continue processing
5. **Completion Logic**: Update status and send notifications

### Auto-Launched Flows

**Reusable Logic**: Auto-Launched Flows are called from other Flows or Apex for reusable logic.

**Use Cases**:
- Common validation logic
- Reusable transformation logic
- Shared decision logic
- Integration with Apex via `@InvocableMethod`
- Utility functions callable from multiple contexts
- Data transformation utilities

**Best Practices**:
- Design for reusability
- Use input/output variables for flexibility
- Document input/output requirements
- Handle errors gracefully
- Keep logic focused and single-purpose

**Auto-Launched Flow Structure Pattern**:
1. **Input Variables**: Define required and optional inputs
2. **Logic**: Reusable business logic
3. **Output Variables**: Return results to caller
4. **Error Handling**: Return error information to caller

### Subflows

**Reusable Logic Chunks**: Subflows extract logical chunks into reusable components.

**Use Cases**:
- Assignment rules
- Task creation
- Status updates
- Common validation logic
- Reusable decision logic
- Notification logic
- Data transformation logic
- Common calculations

**Benefits**:
- Easier testing (test subflow once, reuse everywhere)
- Easier maintenance (update logic in one place)
- Clearer flow structure (main flow shows high-level logic)
- Reduced duplication
- Consistent logic across multiple flows

**Best Practices**:
- Identify repeated logic patterns
- Extract into Subflows for reuse
- Use input/output variables for flexibility
- Document Subflow purpose and usage
- Test Subflows independently
- Version Subflows carefully (breaking changes affect all callers)

**Subflow Structure Pattern**:
1. **Input Variables**: Define inputs needed by Subflow
2. **Reusable Logic**: Common logic used by multiple flows
3. **Output Variables**: Return results to caller
4. **Error Handling**: Handle errors and return status

## Flow Naming Conventions

**Real Naming Pattern**: Based on actual implementation experience across enterprise projects.

**Format**: `{Type}_{Object}_{Trigger}_{Description}`

**Components**:
- **Type Prefix**: 
  - `RT_` = Record-Triggered
  - `Screen_` = Screen Flow
  - `Scheduled_` = Scheduled Flow
  - `Auto_` = Auto-Launched Flow
  - `Subflow_` = Subflow
- **Object Abbreviation**: 
  - `C_` = Case
  - `App_` = Application
  - `Contact_` = Contact
  - `Account_` = Account
- **Trigger Type** (for Record-Triggered only):
  - `C_` = Create
  - `U_` = Update
  - `D_` = Delete
  - `BS_` = Before Save
  - `AS_` = After Save
- **Description**: Descriptive name of what the flow does

**Real Examples**:
- `App_AfterSave_ApplicationStatusOrchestration` - After-save flow orchestrating application status changes
- `Case_BeforeSave_Defaulting` - Before-save flow setting default values on Case
- `RT_C_BS_Update_Account_Values_from_Parent_Account_Academic_Programs` - Before-save flow updating Account values from parent Account
- `RT_U_AS_Send_Advisor_Change_Email` - After-save flow sending advisor change emails
- `Screen_Mid_Point_Evaluation` - Screen flow for mid-point evaluation
- `Scheduled_Cleanup_Old_Records` - Scheduled flow for cleaning up old records
- `Auto_Validate_Contact_Data` - Auto-launched flow for contact data validation
- `Subflow_Create_Advisor_Tasks` - Subflow for creating advisor tasks

## Flow Structure Patterns

### Entry Criteria

**Strict Entry Criteria**: Avoid "run on every change, then decide inside" - use entry criteria to filter at the trigger point.

**Best Practice**: Set entry criteria to match the specific conditions where the flow should run, reducing unnecessary executions.

**Benefits**:
- Improved performance (fewer unnecessary executions)
- Reduced governor limit usage
- Clearer intent (entry criteria documents when flow runs)
- Better debugging (easier to understand when flow executes)

**Example**: Instead of running on all Case updates and checking status inside, set entry criteria to `Status = 'New'` if the flow only needs to run when status is New.

**Entry Criteria Patterns**:
- **Status-based**: `Status = 'New'` or `Status IN ('New', 'In Progress')`
- **Record Type-based**: `RecordType.DeveloperName = 'Support_Case'`
- **Field-based**: `Priority != null AND Owner != null`
- **Change-based**: `ISCHANGED(Status)` or `ISCHANGED(Priority)`
- **Combined**: `Status = 'New' AND RecordType.DeveloperName = 'Support_Case' AND Priority != null`

### Decision Logic

**Separation of Concerns**: Use decision nodes to route by record state, channel, person type, or other criteria.

**Pattern**: Route early, handle specific cases in separate branches.

**Decision Node Routing Pattern**:
1. **First Decision**: Route by `IsNew` (New vs Update)
2. **Second Decision**: Route by Record Type or Channel
3. **Third Decision**: Route by Status or Person Type
4. **Specific Branches**: Handle each case in separate branches

**Example**: Route by `IsNew` (New vs Update), then by record type, then by status.

**Decision Node Best Practices**:
- Route by most common criteria first
- Use clear, descriptive outcomes
- Keep decision logic simple and readable
- Document decision criteria in flow description
- Use Subflows for complex decision logic

### Subflows for Complex Tasks

**Extract Logical Chunks**: Extract complex logic into Subflows for reuse and easier testing.

**Pattern**: Identify repeated logic patterns and extract them into Subflows.

**Common Subflow Patterns**:
- Assignment rules: `Subflow_Assign_Case_Owner`
- Task creation: `Subflow_Create_Advisor_Tasks`
- Status updates: `Subflow_Update_Application_Status`
- Notification logic: `Subflow_Send_Notification_Email`
- Validation logic: `Subflow_Validate_Contact_Data`

**When to Extract to Subflow**:
- Logic is used in multiple flows
- Logic is complex and would clutter main flow
- Logic needs to be tested independently
- Logic represents a distinct business function

### DML Operations

**Minimal DML**: Use fast field updates when possible, aggregate logic to reduce DML operations.

**Best Practices**:
- Use fast field updates for simple field changes (before-save only)
- Aggregate related record operations to minimize DML
- Use collections for bulk operations
- Process records in batches to avoid governor limits
- Use `Database.insert/update` with `allOrNothing=false` for partial success handling

**DML Optimization Patterns**:
- **Collection Operations**: Process multiple records in single DML operation
- **Bulk Processing**: Process records in batches (200 records per batch)
- **Fast Field Updates**: Use before-save fast field updates when possible
- **Aggregate Logic**: Combine multiple field updates into single operation

## Order of Execution Context

**Understanding Execution Order**: Flows execute at specific points in the Salesforce order of execution.

### Before-Save Flows Execution

**Execution Point**: Step 4 in order of execution (after system validation, before custom validation rules)

**Execution Order**:
1. System validation rules
2. Before-save triggers
3. Before-save flows
4. Custom validation rules
5. Record save
6. After-save triggers
7. After-save flows

**Key Points**:
- Before-save flows can modify field values before validation rules run
- Custom validation rules can reference field values modified by before-save flows
- Before-save flows run synchronously and impact user save time
- Keep before-save flows fast and simple

### After-Save Flows Execution

**Execution Point**: Step 7 in order of execution (after record save, after after-save triggers)

**Execution Order**:
1. System validation rules
2. Before-save triggers
3. Before-save flows
4. Custom validation rules
5. Record save
6. After-save triggers
7. After-save flows

**Key Points**:
- After-save flows run after record is saved (record is read-only)
- After-save flows can perform DML on other records
- After-save flows can query related data
- After-save flows can publish Platform Events and make callouts

**See Also**: <a href="{{ '/rag/development/order-of-execution.html' | relative_url }}">Order of Execution</a> for complete execution order details.

## Flow Elements Reference

This section provides comprehensive coverage of all Flow elements, including what each element does, when to use it, how to use it, naming conventions, examples, and best practices.

### Get Records Element

**What It Does**: Retrieves records from the database using SOQL queries. Can retrieve single records or collections of records based on criteria.

**When to Use**:
- Need to query related records for processing
- Need to check if records exist before creating/updating
- Need to retrieve parent record data for field updates
- Need to query records for decision logic
- Need to retrieve records for bulk operations

**When NOT to Use**:
- Can use relationship queries instead (more efficient)
- Need to query in loops (use relationship queries or Get Records before loop)
- Need to query the same record multiple times (store in variable)

**How to Use**:
1. Add Get Records element to flow
2. Select object to query
3. Set filter conditions (WHERE clause)
4. Select fields to retrieve
5. Choose how many records to retrieve (First, All, or specific number)
6. Store results in a variable (single record or collection)

**Naming Conventions**:
- Variable: `{ObjectName}Record` for single record (e.g., `AccountRecord`, `ContactRecord`)
- Variable: `{ObjectName}Records` for collection (e.g., `AccountRecords`, `ContactRecords`)
- Element Label: `Get {ObjectName} {Description}` (e.g., `Get Account Parent Account`, `Get Contacts by Account`)

**Examples**:

**Example 1: Get Single Parent Record**
- **Purpose**: Get parent Account for Contact
- **Object**: Account
- **Filter**: `Id = {!$Record.AccountId}`
- **Fields**: `Name`, `Industry`, `BillingCity`
- **How Many**: First
- **Store In**: `AccountRecord` (single record variable)
- **Use Case**: Update Contact fields based on parent Account data

**Example 2: Get Collection of Related Records**
- **Purpose**: Get all Cases for Account
- **Object**: Case
- **Filter**: `AccountId = {!$Record.Id} AND Status != 'Closed'`
- **Fields**: `Id`, `Subject`, `Status`, `Priority`
- **How Many**: All
- **Store In**: `OpenCases` (collection variable)
- **Use Case**: Count open cases or process all open cases

**Example 3: Check if Record Exists**
- **Purpose**: Check if Contact already exists
- **Object**: Contact
- **Filter**: `Email = {!$Record.Email} AND AccountId = {!$Record.AccountId}`
- **Fields**: `Id`
- **How Many**: First
- **Store In**: `ExistingContact` (single record variable)
- **Use Case**: Prevent duplicate Contact creation

**Best Practices**:
- Use relationship queries when possible (more efficient, doesn't count against SOQL limit)
- Select only fields you need (reduces data transfer)
- Use selective filters (indexed fields, <10% of records)
- Store results in variables to reuse
- Use "First" when you only need one record
- Use "All" when you need multiple records
- Avoid Get Records in loops (use before loop or relationship queries)

**Anti-Patterns**:
- ❌ Getting all fields when you only need a few
- ❌ Using Get Records in loops
- ❌ Querying the same record multiple times
- ❌ Not using relationship queries when available
- ❌ Using non-selective filters (returns >10% of records)

**Governor Limit Impact**:
- Each Get Records element counts as 1 SOQL query
- Limit: 100 SOQL queries per transaction
- Use relationship queries to avoid counting against limit

### Assignment Element

**What It Does**: Assigns values to variables, including field values, formulas, and expressions. Can assign multiple values in a single element.

**When to Use**:
- Need to set variable values
- Need to calculate field values
- Need to transform data
- Need to set default values
- Need to build complex expressions
- Need to concatenate strings
- Need to perform calculations

**When NOT to Use**:
- Can use fast field updates instead (before-save only, more efficient)
- Need to update record fields (use Update Records or fast field updates)
- Need to set values in loops (use Loop element with Assignment inside)

**How to Use**:
1. Add Assignment element to flow
2. Select variable or field to assign
3. Set value using formula, expression, or reference
4. Add multiple assignments in single element
5. Use formulas for calculations and transformations

**Naming Conventions**:
- Variable: `{Purpose}Value` (e.g., `FullNameValue`, `TotalAmountValue`)
- Variable: `{Purpose}Text` for text (e.g., `EmailBodyText`, `NotificationText`)
- Variable: `{Purpose}Number` for numbers (e.g., `TotalCountNumber`, `PercentageNumber`)
- Element Label: `Set {VariableName}` (e.g., `Set FullNameValue`, `Set EmailBodyText`)

**Examples**:

**Example 1: Calculate Full Name**
- **Purpose**: Concatenate first and last name
- **Variable**: `FullNameValue` (Text)
- **Value**: `{!$Record.FirstName} & ' ' & {!$Record.LastName}`
- **Use Case**: Display full name in email or notification

**Example 2: Calculate Total Amount**
- **Purpose**: Calculate total from line items
- **Variable**: `TotalAmountValue` (Currency)
- **Value**: `{!OpportunityLineItems.SUM(UnitPrice * Quantity)}`
- **Use Case**: Update Opportunity Total Amount

**Example 3: Build Email Body**
- **Purpose**: Create formatted email body
- **Variable**: `EmailBodyText` (Text)
- **Value**: `'Dear ' & {!$Record.Contact.FirstName} & ',\n\nYour case ' & {!$Record.CaseNumber} & ' has been updated.\n\nStatus: ' & {!$Record.Status}`
- **Use Case**: Send formatted email notification

**Example 4: Set Multiple Values**
- **Purpose**: Set multiple field values at once
- **Assignments**:
  - `PriorityValue` = `'High'`
  - `StatusValue` = `'In Progress'`
  - `DueDateValue` = `TODAY() + 7`
- **Use Case**: Initialize multiple fields with default values

**Best Practices**:
- Use single Assignment element for multiple related assignments
- Use formulas for calculations and transformations
- Store calculated values in variables for reuse
- Use descriptive variable names
- Document complex formulas
- Use Assignment before Update Records to prepare values

**Anti-Patterns**:
- ❌ Using multiple Assignment elements when one would work
- ❌ Not reusing calculated values (recalculating multiple times)
- ❌ Using Assignment for simple field updates (use fast field updates)
- ❌ Not storing intermediate calculations in variables

### Decision Element

**What It Does**: Routes flow execution based on conditions. Evaluates conditions and directs flow to different paths based on outcomes.

**When to Use**:
- Need to route flow based on field values
- Need to route flow based on record state
- Need conditional logic
- Need to handle different scenarios
- Need to route by record type, status, or other criteria
- Need to validate conditions before proceeding

**When NOT to Use**:
- Can use entry criteria instead (more efficient)
- Need simple true/false check (use formula in condition)
- Need complex nested logic (consider Subflow)

**How to Use**:
1. Add Decision element to flow
2. Add outcomes (conditions to evaluate)
3. Set condition for each outcome
4. Set default outcome (when no conditions match)
5. Connect outcomes to next elements

**Naming Conventions**:
- Element Label: `Check {Condition}` (e.g., `Check Status`, `Check Record Type`)
- Outcome: `{Condition}True` / `{Condition}False` (e.g., `IsNewTrue`, `IsNewFalse`)
- Outcome: `{Value}` (e.g., `StatusNew`, `StatusInProgress`, `StatusClosed`)
- Outcome: `{Description}` (e.g., `HighPriority`, `LowPriority`, `MediumPriority`)

**Examples**:

**Example 1: Route by Record State**
- **Purpose**: Route by New vs Update
- **Outcomes**:
  - `IsNew` → `{!$Record.Id} = null`
  - `IsUpdate` → `{!$Record.Id} != null`
- **Default**: `IsUpdate`
- **Use Case**: Different logic for new vs updated records

**Example 2: Route by Status**
- **Purpose**: Route by Case Status
- **Outcomes**:
  - `StatusNew` → `{!$Record.Status} = 'New'`
  - `StatusInProgress` → `{!$Record.Status} = 'In Progress'`
  - `StatusClosed` → `{!$Record.Status} = 'Closed'`
- **Default**: `StatusOther`
- **Use Case**: Different actions based on status

**Example 3: Route by Priority**
- **Purpose**: Route by Priority level
- **Outcomes**:
  - `HighPriority` → `{!$Record.Priority} = 'High'`
  - `MediumPriority` → `{!$Record.Priority} = 'Medium'`
  - `LowPriority` → `{!$Record.Priority} = 'Low'`
- **Default**: `NoPriority`
- **Use Case**: Different assignment rules by priority

**Example 4: Route by Multiple Conditions**
- **Purpose**: Route by Record Type and Status
- **Outcomes**:
  - `SupportCaseNew` → `{!$Record.RecordType.DeveloperName} = 'Support_Case' AND {!$Record.Status} = 'New'`
  - `SupportCaseInProgress` → `{!$Record.RecordType.DeveloperName} = 'Support_Case' AND {!$Record.Status} = 'In Progress'`
  - `SalesCaseNew` → `{!$Record.RecordType.DeveloperName} = 'Sales_Case' AND {!Record.Status} = 'New'`
- **Default**: `OtherCases`
- **Use Case**: Different logic for different record types and statuses

**Best Practices**:
- Route by most common condition first
- Use clear, descriptive outcome names
- Always set a default outcome
- Keep decision logic simple and readable
- Use entry criteria when possible (more efficient)
- Document decision logic in flow description
- Use Subflows for complex decision logic

**Anti-Patterns**:
- ❌ Not setting default outcome
- ❌ Overly complex nested decisions (use Subflows)
- ❌ Duplicating entry criteria logic in decisions
- ❌ Using decisions when entry criteria would work
- ❌ Unclear outcome names

### Loop Element

**What It Does**: Iterates through a collection of records or items, executing elements inside the loop for each item.

**When to Use**:
- Need to process multiple records
- Need to iterate through collection
- Need to perform operations on each item
- Need to aggregate values from collection
- Need to transform collection items

**When NOT to Use**:
- Can use bulk DML operations instead (more efficient)
- Need to query in loop (use Get Records before loop)
- Need to perform DML in loop (use bulk operations)
- Collection is empty or null (check before looping)

**How to Use**:
1. Add Loop element to flow
2. Select collection variable to iterate
3. Set loop variable name (single item from collection)
4. Add elements inside loop to process each item
5. Use loop variable to access current item

**Naming Conventions**:
- Loop Variable: `Current{ObjectName}` (e.g., `CurrentContact`, `CurrentCase`)
- Loop Variable: `{ItemName}Item` (e.g., `LineItem`, `TaskItem`)
- Element Label: `Loop Through {CollectionName}` (e.g., `Loop Through Contacts`, `Loop Through Cases`)

**Examples**:

**Example 1: Process Related Records**
- **Purpose**: Update all related Contacts
- **Collection**: `RelatedContacts` (from Get Records)
- **Loop Variable**: `CurrentContact`
- **Loop Logic**:
  - Assignment: Set `CurrentContact.Department = {!$Record.Department}`
  - Update Records: Update `CurrentContact`
- **Use Case**: Sync department from Account to all Contacts

**Example 2: Aggregate Values**
- **Purpose**: Calculate total amount from line items
- **Collection**: `OpportunityLineItems` (from relationship query)
- **Loop Variable**: `CurrentLineItem`
- **Loop Logic**:
  - Assignment: Add to `TotalAmount = TotalAmount + (CurrentLineItem.UnitPrice * CurrentLineItem.Quantity)`
- **Use Case**: Calculate Opportunity total from line items

**Example 3: Create Related Records**
- **Purpose**: Create tasks for each Contact
- **Collection**: `RelatedContacts` (from Get Records)
- **Loop Variable**: `CurrentContact`
- **Loop Logic**:
  - Assignment: Set `NewTask.Subject = 'Follow up with ' & CurrentContact.Name`
  - Assignment: Set `NewTask.WhoId = CurrentContact.Id`
  - Create Records: Create `NewTask`
- **Use Case**: Create tasks for multiple Contacts

**Best Practices**:
- Check if collection is empty before looping
- Use bulk DML operations when possible (outside loop)
- Avoid SOQL queries inside loops
- Avoid DML operations inside loops (use collections)
- Process items in collections, not individual operations
- Use Loop for transformations, not for DML

**Anti-Patterns**:
- ❌ Performing DML inside loops (use collections)
- ❌ Performing SOQL queries inside loops
- ❌ Not checking if collection is empty
- ❌ Using Loop when bulk operations would work
- ❌ Processing one record at a time instead of bulk

**Governor Limit Impact**:
- Loops can cause governor limit issues if not used carefully
- Avoid SOQL queries inside loops (100 query limit)
- Avoid DML operations inside loops (150 DML limit)
- Use bulk operations outside loops when possible

### Create Records Element

**What It Does**: Creates new records in the database. Can create single records or multiple records in bulk.

**When to Use**:
- Need to create related records
- Need to create child records
- Need to create records based on triggering record
- Need to create records from collections
- Need to create records with field values

**When NOT to Use**:
- Need to update existing records (use Update Records)
- Need to create and update (use Upsert Records)
- Need to create in before-save (use after-save flow)

**How to Use**:
1. Add Create Records element to flow
2. Select object to create
3. Set field values (use Assignment element to prepare values)
4. Choose how many records to create (single or multiple)
5. Store created record IDs in variables
6. Configure fault path for error handling

**Naming Conventions**:
- Variable: `New{ObjectName}` (e.g., `NewTask`, `NewCase`, `NewContact`)
- Variable: `{ObjectName}ToCreate` for collections (e.g., `TasksToCreate`, `CasesToCreate`)
- Element Label: `Create {ObjectName} {Description}` (e.g., `Create Task Follow Up`, `Create Case Support Request`)

**Examples**:

**Example 1: Create Single Related Record**
- **Purpose**: Create Task when Case is created
- **Object**: Task
- **Fields**:
  - `Subject` = `'Follow up on Case ' & {!$Record.CaseNumber}`
  - `WhatId` = `{!$Record.Id}`
  - `Status` = `'Not Started'`
  - `Priority` = `{!$Record.Priority}`
- **Store In**: `NewTask` (single record variable)
- **Use Case**: Auto-create follow-up task for new Cases

**Example 2: Create Multiple Records from Collection**
- **Purpose**: Create tasks for multiple Contacts
- **Object**: Task
- **How Many**: Multiple
- **Collection**: `TasksToCreate` (prepared in Loop)
- **Store In**: `CreatedTasks` (collection variable)
- **Use Case**: Bulk create tasks for multiple Contacts

**Example 3: Create Child Records**
- **Purpose**: Create Opportunity Line Items from Products
- **Object**: OpportunityLineItem
- **Fields**:
  - `OpportunityId` = `{!$Record.Id}`
  - `Product2Id` = `{!CurrentProduct.Id}`
  - `Quantity` = `1`
  - `UnitPrice` = `{!CurrentProduct.Price}`
- **Store In**: `NewLineItem` (single record variable)
- **Use Case**: Create line items from selected products

**Best Practices**:
- Use bulk operations (create multiple records at once)
- Prepare records in collections before creating
- Store created record IDs for later use
- Configure fault paths for error handling
- Use Assignment element to prepare field values
- Validate required fields before creating

**Anti-Patterns**:
- ❌ Creating records one at a time in loops
- ❌ Not configuring fault paths
- ❌ Not storing created record IDs
- ❌ Creating records in before-save flows
- ❌ Not validating required fields

**Governor Limit Impact**:
- Each Create Records element counts as 1 DML operation
- Limit: 150 DML operations per transaction
- Use bulk operations to minimize DML usage

### Update Records Element

**What It Does**: Updates existing records in the database. Can update single records or multiple records in bulk.

**When to Use**:
- Need to update related records
- Need to update child records
- Need to update records based on triggering record
- Need to update records from collections
- Need to update records with calculated values

**When NOT to Use**:
- Need to update triggering record in before-save (use fast field updates)
- Need to update triggering record in after-save (use Update Records on $Record)
- Need to create records (use Create Records)

**How to Use**:
1. Add Update Records element to flow
2. Select records to update (from variable or collection)
3. Set field values to update
4. Choose how many records to update (single or multiple)
5. Configure fault path for error handling

**Naming Conventions**:
- Variable: `{ObjectName}ToUpdate` (e.g., `ContactToUpdate`, `CaseToUpdate`)
- Variable: `{ObjectName}sToUpdate` for collections (e.g., `ContactsToUpdate`, `CasesToUpdate`)
- Element Label: `Update {ObjectName} {Description}` (e.g., `Update Contact Department`, `Update Case Status`)

**Examples**:

**Example 1: Update Single Related Record**
- **Purpose**: Update Contact when Account changes
- **Records**: `RelatedContact` (from Get Records)
- **Fields**:
  - `Department` = `{!$Record.Department}`
  - `MailingCity` = `{!$Record.BillingCity}`
- **Use Case**: Sync Account data to Contact

**Example 2: Update Multiple Records from Collection**
- **Purpose**: Update all related Cases
- **Records**: `RelatedCases` (from Get Records)
- **Fields**:
  - `Status` = `'Closed'`
  - `ClosedDate` = `TODAY()`
- **Use Case**: Close all Cases when Account is closed

**Example 3: Update Triggering Record**
- **Purpose**: Update Case after processing
- **Records**: `$Record` (triggering record)
- **Fields**:
  - `LastProcessedDate` = `NOW()`
  - `ProcessedBy` = `{!$User.Id}`
- **Use Case**: Track processing in after-save flow

**Best Practices**:
- Use bulk operations (update multiple records at once)
- Prepare records in collections before updating
- Only update fields that have changed
- Configure fault paths for error handling
- Use Assignment element to prepare field values
- Check if records exist before updating

**Anti-Patterns**:
- ❌ Updating records one at a time in loops
- ❌ Not configuring fault paths
- ❌ Updating all fields when only some changed
- ❌ Not checking if records exist
- ❌ Updating triggering record unnecessarily

**Governor Limit Impact**:
- Each Update Records element counts as 1 DML operation
- Limit: 150 DML operations per transaction
- Use bulk operations to minimize DML usage

### Delete Records Element

**What It Does**: Deletes records from the database. Can delete single records or multiple records in bulk.

**When to Use**:
- Need to delete related records
- Need to delete child records
- Need to clean up old records
- Need to delete records based on criteria
- Need to delete records from collections

**When NOT to Use**:
- Need to delete triggering record (use delete trigger or process)
- Need to soft delete (use status field instead)
- Need to archive records (use archive object)

**How to Use**:
1. Add Delete Records element to flow
2. Select records to delete (from variable or collection)
3. Choose how many records to delete (single or multiple)
4. Configure fault path for error handling

**Naming Conventions**:
- Variable: `{ObjectName}ToDelete` (e.g., `TaskToDelete`, `CaseToDelete`)
- Variable: `{ObjectName}sToDelete` for collections (e.g., `TasksToDelete`, `CasesToDelete`)
- Element Label: `Delete {ObjectName} {Description}` (e.g., `Delete Old Tasks`, `Delete Duplicate Cases`)

**Examples**:

**Example 1: Delete Single Related Record**
- **Purpose**: Delete old Task when Case is closed
- **Records**: `OldTask` (from Get Records)
- **Use Case**: Clean up old tasks when Case closes

**Example 2: Delete Multiple Records from Collection**
- **Purpose**: Delete all old Tasks
- **Records**: `OldTasks` (from Get Records with date filter)
- **Use Case**: Scheduled cleanup of old records

**Example 3: Delete Child Records**
- **Purpose**: Delete Opportunity Line Items when Opportunity is deleted
- **Records**: `LineItems` (from Get Records)
- **Use Case**: Cascade delete related records

**Best Practices**:
- Use bulk operations (delete multiple records at once)
- Prepare records in collections before deleting
- Configure fault paths for error handling
- Log deletions for audit purposes
- Verify records exist before deleting
- Consider soft delete (status field) instead of hard delete

**Anti-Patterns**:
- ❌ Deleting records one at a time in loops
- ❌ Not configuring fault paths
- ❌ Not logging deletions
- ❌ Deleting without verification
- ❌ Hard deleting when soft delete would work

**Governor Limit Impact**:
- Each Delete Records element counts as 1 DML operation
- Limit: 150 DML operations per transaction
- Use bulk operations to minimize DML usage

### Fast Field Updates (Before-Save Only)

**What It Does**: Updates field values on the triggering record before it is saved. More efficient than Update Records for simple field updates.

**When to Use**:
- Need to update triggering record fields in before-save flow
- Need to set default values
- Need to calculate field values
- Need to normalize field values
- Need simple field updates (no DML required)

**When NOT to Use**:
- Need to update related records (use after-save flow)
- Need complex logic (use Assignment + Update Records)
- Need to update in after-save flow (use Update Records)

**How to Use**:
1. Add Fast Field Update element to flow (before-save only)
2. Select field to update
3. Set field value using formula or reference
4. Add multiple fast field updates as needed

**Naming Conventions**:
- Element Label: `Set {FieldName}` (e.g., `Set Priority`, `Set DueDate`)
- Element Label: `Calculate {FieldName}` (e.g., `Calculate TotalAmount`, `Calculate FullName`)

**Examples**:

**Example 1: Set Default Values**
- **Purpose**: Set default Priority on Case
- **Field**: `Priority`
- **Value**: `IF(ISBLANK({!$Record.Priority}), 'Medium', {!$Record.Priority})`
- **Use Case**: Ensure Priority is always set

**Example 2: Calculate Field Value**
- **Purpose**: Calculate Due Date based on SLA
- **Field**: `DueDate`
- **Value**: `IF({!$Record.Priority} = 'High', TODAY() + 1, TODAY() + 7)`
- **Use Case**: Auto-calculate due dates

**Example 3: Normalize Field Value**
- **Purpose**: Normalize email to lowercase
- **Field**: `Email`
- **Value**: `LOWER({!$Record.Email})`
- **Use Case**: Ensure consistent email format

**Best Practices**:
- Use fast field updates for simple field updates
- Use formulas for calculations
- Set multiple fields in single flow
- Keep logic simple and fast
- Use for default values and calculations

**Anti-Patterns**:
- ❌ Using Update Records for simple field updates
- ❌ Complex logic in fast field updates
- ❌ Not using fast field updates when available

### Apex Action Element

**What It Does**: Calls Apex methods marked with `@InvocableMethod` from Flows. Enables integration between declarative and programmatic automation.

**When to Use**:
- Need complex logic that Flow cannot handle
- Need to call external APIs
- Need complex calculations
- Need retry logic
- Need to reuse Apex logic in Flows
- Need to perform operations Flow cannot do

**When NOT to Use**:
- Logic can be expressed declaratively in Flow
- Simple operations Flow can handle
- Need to avoid code maintenance

**How to Use**:
1. Create Apex class with `@InvocableMethod`
2. Add Apex Action element to flow
3. Select Apex class and method
4. Set input parameters
5. Store output in variables
6. Configure fault path for error handling

**Naming Conventions**:
- Apex Class: `{Purpose}Service` (e.g., `ContactUpdateService`, `SMSNotificationService`)
- Method: `{Action}` (e.g., `updateContacts`, `sendSMS`)
- Element Label: `Call {ClassName}.{MethodName}` (e.g., `Call ContactUpdateService.updateContacts`)

**Examples**:

**Example 1: Retry Logic**
- **Purpose**: Retry Contact update with exponential backoff
- **Apex Class**: `ContactRetryUpdateService`
- **Method**: `retryUpdate`
- **Input**: `ContactIds` (collection)
- **Output**: `Result` (success, error message)
- **Use Case**: Handle row locking errors

**Example 2: External API Call**
- **Purpose**: Send SMS via external API
- **Apex Class**: `SendSMSMagicEU`
- **Method**: `sendSMS`
- **Input**: `PhoneNumber`, `Message`
- **Output**: `Status`, `MessageId`
- **Use Case**: Send SMS notifications

**Example 3: Complex Calculation**
- **Purpose**: Calculate fraud score
- **Apex Class**: `FraudScoreController`
- **Method**: `calculateScore`
- **Input**: `ApplicationId`
- **Output**: `Score`, `Factors`
- **Use Case**: Calculate fraud probability

**Best Practices**:
- Use `@InvocableMethod` for Flow integration
- Accept and return lists (even for single values)
- Use `@InvocableVariable` for complex parameters
- Handle errors gracefully
- Configure fault paths
- Document input/output requirements

**Anti-Patterns**:
- ❌ Not handling errors
- ❌ Not configuring fault paths
- ❌ Not documenting parameters
- ❌ Using Apex when Flow would work

### Subflow Element

**What It Does**: Calls another Flow (Subflow) from the current Flow. Enables reusable logic and modular flow design.

**When to Use**:
- Need reusable logic across multiple flows
- Need to extract complex logic into separate flow
- Need modular flow design
- Need to test logic independently
- Need to maintain logic in one place

**When NOT to Use**:
- Logic is only used in one flow
- Logic is simple and doesn't need separation
- Need to avoid additional flow complexity

**How to Use**:
1. Create Subflow with input/output variables
2. Add Subflow element to flow
3. Select Subflow to call
4. Set input variable values
5. Store output variable values
6. Configure fault path for error handling

**Naming Conventions**:
- Subflow: `Subflow_{Purpose}` (e.g., `Subflow_Create_Advisor_Tasks`, `Subflow_Assign_Case_Owner`)
- Input Variable: `{Purpose}Input` (e.g., `CaseInput`, `ContactInput`)
- Output Variable: `{Purpose}Output` (e.g., `TaskOutput`, `ResultOutput`)
- Element Label: `Call Subflow {SubflowName}` (e.g., `Call Subflow Create Advisor Tasks`)

**Examples**:

**Example 1: Reusable Task Creation**
- **Purpose**: Create advisor tasks (used in multiple flows)
- **Subflow**: `Subflow_Create_Advisor_Tasks`
- **Input**: `ContactId`, `TaskSubject`, `TaskPriority`
- **Output**: `TaskId`, `Success`
- **Use Case**: Create tasks from multiple flows

**Example 2: Reusable Assignment Logic**
- **Purpose**: Assign Case to owner (used in multiple flows)
- **Subflow**: `Subflow_Assign_Case_Owner`
- **Input**: `CaseId`, `AssignmentRule`
- **Output**: `OwnerId`, `Success`
- **Use Case**: Consistent assignment logic

**Example 3: Reusable Validation**
- **Purpose**: Validate Contact data (used in multiple flows)
- **Subflow**: `Subflow_Validate_Contact_Data`
- **Input**: `ContactRecord`
- **Output**: `IsValid`, `ValidationErrors`
- **Use Case**: Consistent validation logic

**Best Practices**:
- Design Subflows for reusability
- Use clear input/output variable names
- Document Subflow purpose and usage
- Test Subflows independently
- Version Subflows carefully (breaking changes affect all callers)
- Keep Subflows focused and single-purpose

**Anti-Patterns**:
- ❌ Subflows that are too complex
- ❌ Subflows that are only used once
- ❌ Not documenting Subflow purpose
- ❌ Breaking changes without versioning

### Platform Event Element

**What It Does**: Publishes Platform Events from Flows. Enables event-driven architecture and decoupling.

**When to Use**:
- Need to publish events for integrations
- Need event-driven architecture
- Need to decouple Salesforce from external systems
- Need to notify multiple subscribers
- Need async processing

**When NOT to Use**:
- Need synchronous processing
- Need immediate response
- Simple automation doesn't need events

**How to Use**:
1. Add Platform Event element to flow
2. Select Platform Event type
3. Set event field values
4. Configure fault path for error handling

**Naming Conventions**:
- Platform Event: `{ObjectName}__e` (e.g., `ApplicationSubmitted__e`, `CaseStatusChanged__e`)
- Element Label: `Publish {EventName}` (e.g., `Publish ApplicationSubmitted`, `Publish CaseStatusChanged`)

**Examples**:

**Example 1: Application Submission Event**
- **Purpose**: Publish event when application is submitted
- **Event**: `ApplicationSubmitted__e`
- **Fields**:
  - `ApplicationId__c` = `{!$Record.Id}`
  - `Status__c` = `{!$Record.Status}`
  - `SubmittedDate__c` = `NOW()`
- **Use Case**: Trigger external system processing

**Example 2: Status Change Event**
- **Purpose**: Publish event when status changes
- **Event**: `CaseStatusChanged__e`
- **Fields**:
  - `CaseId__c` = `{!$Record.Id}`
  - `OldStatus__c` = `{!$Record.PRIORVALUE(Status)}`
  - `NewStatus__c` = `{!$Record.Status}`
- **Use Case**: Notify subscribers of status changes

**Best Practices**:
- Include all necessary context in event payload
- Minimize PII in event payloads
- Design payloads to be idempotent
- Include external IDs for correlation
- Include change metadata
- Configure fault paths

**Anti-Patterns**:
- ❌ Including unnecessary PII
- ❌ Not including correlation IDs
- ❌ Not configuring fault paths
- ❌ Payloads requiring subscribers to query Salesforce

**See Also**: <a href="{{ '/rag/architecture/event-driven-architecture.html' | relative_url }}">Event-Driven Architecture</a> for complete event-driven patterns.

### Email Action Element

**What It Does**: Sends email from Flows. Can send email alerts, email templates, or compose emails.

**When to Use**:
- Need to send notifications
- Need to send email alerts
- Need to send email templates
- Need to compose custom emails
- Need to notify users of changes

**When NOT to Use**:
- Need to send to external email addresses (use Apex)
- Need complex email logic (use Apex)
- Need to send bulk emails (use Apex or Mass Email)

**How to Use**:
1. Add Email Action element to flow
2. Choose email type (Alert, Template, or Compose)
3. Set recipients
4. Set email content
5. Configure fault path for error handling

**Naming Conventions**:
- Element Label: `Send Email {Description}` (e.g., `Send Email Case Notification`, `Send Email Welcome Message`)

**Examples**:

**Example 1: Email Alert**
- **Purpose**: Send email alert when Case is created
- **Type**: Email Alert
- **Alert**: `Case_Created_Alert`
- **Recipients**: Case Owner, Contact Email
- **Use Case**: Notify stakeholders of new Case

**Example 2: Email Template**
- **Purpose**: Send welcome email to new Contact
- **Type**: Email Template
- **Template**: `Welcome_Email_Template`
- **Recipients**: Contact Email
- **Use Case**: Welcome new contacts

**Example 3: Composed Email**
- **Purpose**: Send custom notification email
- **Type**: Compose Email
- **To**: `{!$Record.Contact.Email}`
- **Subject**: `'Case Update: ' & {!$Record.CaseNumber}`
- **Body**: `'Your case has been updated. Status: ' & {!$Record.Status}`
- **Use Case**: Custom email notifications

**Best Practices**:
- Use email templates when possible
- Configure fault paths
- Test email delivery
- Use email alerts for standard notifications
- Compose emails for custom content

**Anti-Patterns**:
- ❌ Not configuring fault paths
- ❌ Sending unnecessary emails
- ❌ Not testing email delivery

### Post to Chatter Element

**What It Does**: Posts messages to Chatter from Flows. Can post to records, users, or groups.

**When to Use**:
- Need to post notifications to Chatter
- Need to notify teams of changes
- Need to post updates to records
- Need to collaborate on records

**When NOT to Use**:
- Need private notifications (use email)
- Need external notifications (use email or Platform Events)

**How to Use**:
1. Add Post to Chatter element to flow
2. Set message content
3. Set target (record, user, or group)
4. Configure fault path for error handling

**Naming Conventions**:
- Element Label: `Post to Chatter {Description}` (e.g., `Post to Chatter Case Update`, `Post to Chatter Team Notification`)

**Examples**:

**Example 1: Post to Record**
- **Purpose**: Post update to Case record
- **Target**: `{!$Record.Id}`
- **Message**: `'Case status updated to ' & {!$Record.Status}`
- **Use Case**: Notify team of Case updates

**Example 2: Post to User**
- **Purpose**: Notify user of assignment
- **Target**: `{!$Record.OwnerId}`
- **Message**: `'You have been assigned Case ' & {!$Record.CaseNumber}`
- **Use Case**: Notify users of assignments

**Best Practices**:
- Use for team collaboration
- Keep messages concise
- Configure fault paths
- Use for internal notifications

### Wait Element

**What It Does**: Pauses flow execution for a specified duration or until a condition is met. Used in scheduled flows and screen flows.

**When to Use**:
- Need to delay execution in scheduled flows
- Need to wait for conditions in screen flows
- Need to pause before retrying operations
- Need to schedule delayed actions

**When NOT to Use**:
- Need immediate execution
- Need to wait in record-triggered flows (not supported)
- Need complex scheduling (use Scheduled Apex)

**How to Use**:
1. Add Wait element to flow
2. Choose wait type (duration or condition)
3. Set wait duration or condition
4. Continue flow after wait

**Naming Conventions**:
- Element Label: `Wait {Duration/Condition}` (e.g., `Wait 5 Minutes`, `Wait for Status Change`)

**Examples**:

**Example 1: Wait Duration**
- **Purpose**: Wait before sending reminder
- **Type**: Duration
- **Duration**: 24 hours
- **Use Case**: Send reminder 24 hours after creation

**Example 2: Wait for Condition**
- **Purpose**: Wait for status change
- **Type**: Condition
- **Condition**: `{!$Record.Status} = 'Closed'`
- **Use Case**: Wait for Case to close before processing

**Best Practices**:
- Use for scheduled flows
- Use for screen flows with delays
- Keep wait durations reasonable
- Document wait conditions

**Anti-Patterns**:
- ❌ Using Wait in record-triggered flows (not supported)
- ❌ Excessive wait durations
- ❌ Unclear wait conditions

### Screen Elements (Screen Flows Only)

Screen Flows include specialized elements for user interaction. These elements are only available in Screen Flows.

#### Screen Element

**What It Does**: Displays a screen to the user with input fields, text, and navigation buttons.

**When to Use**:
- Need to collect user input
- Need to display information to users
- Need to guide users through multi-step processes
- Need to show progress or instructions

**How to Use**:
1. Add Screen element to flow
2. Add components (input fields, text, buttons)
3. Set field labels and help text
4. Configure navigation (Next, Back, Finish)
5. Set screen visibility conditions

**Naming Conventions**:
- Element Label: `Screen {StepNumber} {Description}` (e.g., `Screen 1 Contact Information`, `Screen 2 Review`)
- Element Label: `{Purpose} Screen` (e.g., `Contact Information Screen`, `Review Screen`)

**Screen Components**:
- **Input Fields**: Text, Number, Currency, Date, Picklist, Multi-Select Picklist, Checkbox, Radio Buttons
- **Display Components**: Text, Rich Text, Image, Section
- **Navigation**: Next, Back, Finish, Pause

**Best Practices**:
- Break complex forms into multiple screens
- Use clear field labels and help text
- Show progress indicators
- Validate input at each screen
- Provide clear navigation options
- Use conditional visibility for optional fields

#### Choice (Radio Buttons / Dropdown)

**What It Does**: Displays choices to users as radio buttons or dropdown menus.

**When to Use**:
- Need user to select from options
- Need single selection from multiple options
- Need to guide user choices
- Need to filter next screen based on choice

**How to Use**:
1. Add Choice component to screen
2. Define choice options
3. Set default selection
4. Store selected value in variable
5. Use choice value in decision logic

**Naming Conventions**:
- Variable: `{Purpose}Choice` (e.g., `PriorityChoice`, `StatusChoice`)
- Element Label: `Select {Purpose}` (e.g., `Select Priority`, `Select Status`)

**Examples**:

**Example 1: Priority Selection**
- **Purpose**: Let user select Case priority
- **Choices**: High, Medium, Low
- **Variable**: `PriorityChoice`
- **Use Case**: User selects priority in Screen Flow

**Example 2: Status Selection**
- **Purpose**: Let user select application status
- **Choices**: Submitted, In Review, Approved, Rejected
- **Variable**: `StatusChoice`
- **Use Case**: User updates application status

**Best Practices**:
- Use clear choice labels
- Provide help text for choices
- Set sensible defaults
- Use choice values in decision logic
- Validate choices before proceeding

#### Multi-Select Choice

**What It Does**: Allows users to select multiple options from a list.

**When to Use**:
- Need multiple selections
- Need to select multiple related items
- Need to filter based on multiple selections

**How to Use**:
1. Add Multi-Select Choice component to screen
2. Define choice options
3. Store selected values in collection variable
4. Use collection in decision logic or loops

**Naming Conventions**:
- Variable: `{Purpose}Choices` (e.g., `ProductChoices`, `CategoryChoices`)
- Element Label: `Select {Purpose}` (e.g., `Select Products`, `Select Categories`)

**Best Practices**:
- Use for multiple selections
- Store in collection variables
- Use collection in loops or filters
- Provide clear labels

### Formula Element

**What It Does**: Calculates values using formulas. Can be used in Assignment elements, Decision elements, and field updates.

**When to Use**:
- Need to calculate values
- Need to transform data
- Need to concatenate strings
- Need to perform date calculations
- Need conditional logic in formulas

**How to Use**:
1. Use formula in Assignment, Decision, or field update
2. Reference variables and field values
3. Use formula functions
4. Store calculated value in variable or field

**Naming Conventions**:
- Formula Variable: `{Purpose}Formula` (e.g., `FullNameFormula`, `TotalAmountFormula`)

**Common Formula Patterns**:

**Pattern 1: String Concatenation**
```
{!$Record.FirstName} & ' ' & {!$Record.LastName}
```

**Pattern 2: Conditional Logic**
```
IF({!$Record.Priority} = 'High', TODAY() + 1, TODAY() + 7)
```

**Pattern 3: Date Calculation**
```
TODAY() + 30
NOW() + 1
```

**Pattern 4: Null Handling**
```
IF(ISBLANK({!$Record.CustomField}), 'Default', {!$Record.CustomField})
```

**Pattern 5: Case Logic**
```
CASE({!$Record.Status}, 
  'New', 'New Case',
  'In Progress', 'Active Case',
  'Closed', 'Completed Case',
  'Other'
)
```

**Best Practices**:
- Use formulas for calculations
- Handle null values
- Use clear formula logic
- Document complex formulas
- Test formulas with various inputs

**Anti-Patterns**:
- ❌ Complex nested formulas (use Decision elements)
- ❌ Not handling null values
- ❌ Unclear formula logic

### Collection Operations

**What It Does**: Operations on collections (lists) of records or values.

**When to Use**:
- Need to work with multiple records
- Need to aggregate values
- Need to filter collections
- Need to transform collections

**Collection Functions**:
- **COUNT**: Count items in collection
- **SUM**: Sum numeric values
- **MIN**: Minimum value
- **MAX**: Maximum value
- **FIRST**: First item in collection
- **LAST**: Last item in collection

**Examples**:

**Example 1: Count Related Records**
- **Purpose**: Count open Cases for Account
- **Collection**: `OpenCases`
- **Formula**: `COUNT({!OpenCases})`
- **Use Case**: Display count of open cases

**Example 2: Sum Line Items**
- **Purpose**: Calculate total from line items
- **Collection**: `OpportunityLineItems`
- **Formula**: `SUM({!OpportunityLineItems}, UnitPrice * Quantity)`
- **Use Case**: Calculate Opportunity total

**Example 3: Find Maximum Value**
- **Purpose**: Find highest priority Case
- **Collection**: `RelatedCases`
- **Formula**: `MAX({!RelatedCases}, Priority)`
- **Use Case**: Identify highest priority case

**Best Practices**:
- Use collection functions for aggregations
- Store aggregated values in variables
- Use collections in loops
- Filter collections before aggregating

## Advanced Flow Patterns

### Bulk Processing Pattern

**Pattern**: Process records in bulk to minimize governor limit usage.

**Structure**:
1. Get Records: Retrieve all records to process
2. Loop: Iterate through collection
3. Assignment: Prepare records for bulk operation
4. Create/Update Records: Bulk operation outside loop

**Example**:
```
Get Records: Get all Contacts to update
Loop: For each Contact
  Assignment: Set Department = Account.Department
  Add to collection: ContactsToUpdate
End Loop
Update Records: Update ContactsToUpdate (bulk)
```

**Best Practices**:
- Prepare records in collection
- Perform bulk DML outside loops
- Use collections for bulk operations
- Minimize DML operations

### Relationship Query Pattern

**Pattern**: Use relationship queries to avoid multiple Get Records elements.

**Structure**:
1. Get Records: Query parent record with related records
2. Access related records via relationship
3. Process related records in loop

**Example**:
```
Get Records: Account with Contacts (relationship query)
  Fields: Account fields + Contacts (relationship)
Loop: For each Contact in Account.Contacts
  Process Contact
End Loop
```

**Best Practices**:
- Use relationship queries when possible
- Access related records via relationship
- Avoid multiple Get Records for related data
- Use relationship queries to avoid SOQL limit

### Error Handling Pattern

**Pattern**: Comprehensive error handling with logging and fallback.

**Structure**:
1. Configure fault paths for all operations
2. Log errors to LOG_LogMessage__c
3. Use Platform Event fallback if DML fails
4. Provide user-friendly error messages

**Example**:
```
Create Records: Create Task
  Fault Path:
    Assignment: Set ErrorMessage
    Apex Action: LOG_LogMessageUtility.logError
      Fault Path:
        Platform Event: Publish ErrorLog__e
    Screen: Show Error Message
```

**Best Practices**:
- Always configure fault paths
- Log all errors
- Use Platform Event fallback
- Provide user-friendly messages

### Recursion Prevention Pattern

**Pattern**: Prevent Flow from triggering itself recursively.

**Structure**:
1. Entry Criteria: Use ISCHANGED() to detect specific changes
2. Decision: Check if value actually changed
3. Assignment: Only update if value changed

**Example**:
```
Entry Criteria: ISCHANGED(Status) AND Status = 'Closed'
Decision: Check if Status was already 'Closed'
  If No: Update related records
  If Yes: Skip (prevent recursion)
```

**Best Practices**:
- Use ISCHANGED() in entry criteria
- Check if values actually changed
- Avoid update operations that re-trigger flow
- Use static variables in Apex actions

## Comprehensive Naming Conventions

### Flow Naming Conventions

**Format**: `{Type}_{Object}_{Trigger}_{Description}`

**Type Prefixes**:
- `RT_` = Record-Triggered Flow
- `Screen_` = Screen Flow
- `Scheduled_` = Scheduled Flow
- `Auto_` = Auto-Launched Flow
- `Subflow_` = Subflow

**Object Abbreviations**:
- `C_` = Case
- `App_` = Application
- `Contact_` = Contact
- `Account_` = Account
- `Opp_` = Opportunity
- `Task_` = Task
- `Lead_` = Lead

**Trigger Type** (Record-Triggered only):
- `C_` = Create
- `U_` = Update
- `D_` = Delete
- `BS_` = Before Save
- `AS_` = After Save

**Examples**:
- `RT_C_BS_Update_Account_Values_from_Parent_Account_Academic_Programs`
- `RT_U_AS_Send_Advisor_Change_Email`
- `Screen_Mid_Point_Evaluation`
- `Scheduled_Cleanup_Old_Records`
- `Auto_Validate_Contact_Data`
- `Subflow_Create_Advisor_Tasks`

### Variable Naming Conventions

**Single Record Variables**:
- `{ObjectName}Record` (e.g., `AccountRecord`, `ContactRecord`)
- `Current{ObjectName}` (e.g., `CurrentContact`, `CurrentCase`)

**Collection Variables**:
- `{ObjectName}Records` (e.g., `AccountRecords`, `ContactRecords`)
- `{ObjectName}s` (e.g., `Contacts`, `Cases`)

**Calculated Values**:
- `{Purpose}Value` (e.g., `FullNameValue`, `TotalAmountValue`)
- `{Purpose}Text` (e.g., `EmailBodyText`, `NotificationText`)
- `{Purpose}Number` (e.g., `TotalCountNumber`, `PercentageNumber`)

**Choice Variables**:
- `{Purpose}Choice` (e.g., `PriorityChoice`, `StatusChoice`)
- `{Purpose}Choices` for multi-select (e.g., `ProductChoices`)

**Input/Output Variables**:
- `{Purpose}Input` (e.g., `CaseInput`, `ContactInput`)
- `{Purpose}Output` (e.g., `TaskOutput`, `ResultOutput`)

### Element Naming Conventions

**Get Records**:
- `Get {ObjectName} {Description}` (e.g., `Get Account Parent Account`, `Get Contacts by Account`)

**Assignment**:
- `Set {VariableName}` (e.g., `Set FullNameValue`, `Set EmailBodyText`)

**Decision**:
- `Check {Condition}` (e.g., `Check Status`, `Check Record Type`)

**Loop**:
- `Loop Through {CollectionName}` (e.g., `Loop Through Contacts`, `Loop Through Cases`)

**Create Records**:
- `Create {ObjectName} {Description}` (e.g., `Create Task Follow Up`, `Create Case Support Request`)

**Update Records**:
- `Update {ObjectName} {Description}` (e.g., `Update Contact Department`, `Update Case Status`)

**Delete Records**:
- `Delete {ObjectName} {Description}` (e.g., `Delete Old Tasks`, `Delete Duplicate Cases`)

**Apex Action**:
- `Call {ClassName}.{MethodName}` (e.g., `Call ContactUpdateService.updateContacts`)

**Subflow**:
- `Call Subflow {SubflowName}` (e.g., `Call Subflow Create Advisor Tasks`)

**Platform Event**:
- `Publish {EventName}` (e.g., `Publish ApplicationSubmitted`, `Publish CaseStatusChanged`)

**Email**:
- `Send Email {Description}` (e.g., `Send Email Case Notification`, `Send Email Welcome Message`)

**Screen**:
- `Screen {StepNumber} {Description}` (e.g., `Screen 1 Contact Information`, `Screen 2 Review`)

**Wait**:
- `Wait {Duration/Condition}` (e.g., `Wait 5 Minutes`, `Wait for Status Change`)

## Integration Patterns

### Platform Events from Flows

**Preferred Pattern**: Platform Events published from Flows (preferred over Apex) for declarative event publication.

**Use Cases**:
- Application submissions
- Status changes
- Data updates
- Event-driven integrations
- Decoupling Salesforce from external systems

**Pattern**: Use Flow's "Publish Platform Event" action to publish events declaratively.

**Best Practices**:
- Include all necessary context in event payloads
- Minimize PII in event payloads
- Design payloads to be idempotent where possible
- Include external IDs for correlation
- Include change metadata (who, when, what changed)

**Real Example**: Platform Events published from Flows for SIS integration events, routed to external event bus (EventBridge reference architecture).

**Event Payload Design**:
- Include external IDs for correlation with external system records
- Include minimal necessary PII to balance functionality with privacy
- Include change metadata (who made the change, when it occurred)
- Include business context fields needed by downstream systems
- Design payloads to be self-contained (subscribers shouldn't need to query Salesforce)

**See Also**: <a href="{{ '/rag/architecture/event-driven-architecture.html' | relative_url }}">Event-Driven Architecture</a> for complete event-driven patterns.

### Invocable Methods

**Apex Integration**: Use `@InvocableMethod` to make Apex methods callable from Flows.

**Use Cases**:
- Complex logic that Flow cannot handle
- Reusable Apex logic needed in Flows
- Integration with external systems
- Complex calculations
- Retry logic for DML operations

**Real Examples**:
- `ContactRetryUpdateService` with `@InvocableMethod` for retry logic in Flows
- `SendSMSMagicEU` class with `@InvocableMethod` for SMS notifications from Flows

**Pattern**: Create Apex classes with `@InvocableMethod` for Flow integration, keeping business logic in Apex while enabling declarative orchestration.

**Invocable Method Requirements**:
- Method must be static
- Method must be in a public class
- Parameters must be lists (even for single values)
- Return values must be lists
- Use `@InvocableVariable` for complex input parameters

**Example**:
```apex
public class ContactRetryUpdateService {
    @InvocableMethod(label='Retry Contact Update' description='Retries Contact update with exponential backoff')
    public static List<Result> retryUpdate(List<Request> requests) {
        List<Result> results = new List<Result>();
        for (Request req : requests) {
            // Retry logic with exponential backoff
            Result res = new Result();
            // ... implementation
            results.add(res);
        }
        return results;
    }
    
    public class Request {
        @InvocableVariable(label='Contact IDs' required=true)
        public List<Id> contactIds;
    }
    
    public class Result {
        @InvocableVariable(label='Success')
        public Boolean success;
        @InvocableVariable(label='Error Message')
        public String errorMessage;
    }
}
```

### Callable Interface

**Flexible Integration**: Use `Callable` interface for classes that need to be callable from both Flows and Apex.

**Use Cases**:
- Utility classes used in multiple contexts
- Logging utilities
- Integration utilities
- Common business logic

**Real Examples**:
- `LOG_LogMessageUtility` class implementing `Callable` interface (can be called from Flows and Apex)
- `IEE_MS_PDFConverterUtil` class implementing `Callable` interface for Flow/OmniStudio integration
- `IEEContextUser` class implementing `Callable` interface

**Pattern**: Implement `Callable` interface when class needs to be callable from both Flows and Apex, providing flexibility in how the class is invoked.

**Callable Interface Implementation**:
```apex
public class LOG_LogMessageUtility implements Callable {
    public Object call(String action, Map<String, Object> args) {
        switch on action {
            when 'logError' {
                return logError(args);
            }
            when 'logInfo' {
                return logInfo(args);
            }
            when else {
                throw new IllegalArgumentException('Unknown action: ' + action);
            }
        }
    }
    
    private Object logError(Map<String, Object> args) {
        // Error logging implementation
        return true;
    }
}
```

### Service Layer Pattern

**Separation of Concerns**: Separate business logic into service classes that can be called from Flows and LWCs.

**Pattern**: Create service classes with `@InvocableMethod` or `Callable` interface for Flow integration.

**Real Examples**:
- `ContactRetryUpdateService` - Service class with retry logic callable from Flows
- `ContactUpdateService` - Service class for Contact updates callable from Flows

**Benefits**:
- Reusable business logic
- Easier testing
- Cleaner Flow structure
- Better separation of concerns
- Consistent error handling

## Error Handling Patterns

### Error Handling in Flows

**Comprehensive Error Handling**: All errors must be handled gracefully in Flows.

**Patterns**:
- Use fault paths for all integration calls and DML operations
- Log errors to `LOG_LogMessage__c` object
- Use Platform Event fallback if DML fails
- Provide user-friendly error messages
- Handle errors at appropriate levels (flow level, element level)

**Real Example**: `LOG_LogMessageUtility` class implementing `Callable` interface for error logging from Flows, with Platform Event fallback if DML fails.

**Error Handling Best Practices**:
- Always configure fault paths for DML operations
- Always configure fault paths for Apex actions
- Always configure fault paths for callouts
- Log errors before showing messages to users
- Provide context in error messages
- Use error variables to pass error information

**Fault Path Configuration**:
- Configure fault paths for all elements that can fail
- Use fault path to log errors
- Use fault path to show user-friendly messages
- Use fault path to update error tracking fields
- Use fault path to publish Platform Events for critical errors

### Platform Event Fallback

**DML Failure Handling**: If DML fails (governor limits, validation rules), publish Platform Event as fallback to ensure error is still captured.

**Pattern**: Use Platform Events as fallback mechanism when DML operations fail.

**Real Example**: `LOG_LogMessageUtility` publishes `ErrorLog__e` Platform Event on DML exceptions, ensuring errors are captured even when DML fails.

**Fallback Pattern**:
1. Attempt to log error to `LOG_LogMessage__c` object
2. If DML fails, publish `ErrorLog__e` Platform Event
3. Platform Event subscriber processes error asynchronously
4. Error is captured even when DML fails

**See Also**: <a href="{{ '/rag/development/error-handling-and-logging.html' | relative_url }}">Error Handling and Logging</a> for complete error handling patterns.

## Performance and Governor Limits

### Governor Limits in Flows

**Understanding Limits**: Flows share the same governor limits as Apex within a transaction.

**Key Limits**:
- **SOQL Queries**: 100 queries per transaction
- **DML Operations**: 150 DML statements per transaction
- **CPU Time**: 10,000 milliseconds per transaction
- **Heap Size**: 6 MB synchronous, 12 MB asynchronous
- **Callouts**: 100 callouts per transaction (async only)

**Best Practices**:
- Minimize SOQL queries (use relationship queries when possible)
- Aggregate DML operations (use collections)
- Use fast field updates when possible (before-save only)
- Move heavy operations to async processing
- Monitor governor limit usage

### Performance Optimization

**Optimization Strategies**:
- Use strict entry criteria to reduce unnecessary executions
- Use fast field updates for simple field changes
- Aggregate DML operations to minimize governor limit usage
- Use relationship queries to avoid multiple queries
- Move heavy operations to async processing (Platform Events, Queueable)
- Use Subflows to reduce duplication and improve maintainability

**Performance Monitoring**:
- Monitor Flow execution times
- Track governor limit usage
- Identify performance bottlenecks
- Optimize slow flows
- Use Flow Debug Logs for performance analysis

**See Also**: <a href="{{ '/rag/development/governor-limits-and-optimization.html' | relative_url }}">Governor Limits and Optimization</a> for complete performance patterns.

## Testing Patterns

### Flow Testing Best Practices

**Testing Requirements**:
- Test with various data scenarios
- Test error handling paths
- Test with bulk data (200+ records)
- Test edge cases and boundary conditions
- Test integration points
- Coordinate testing with related automation

**Testing Patterns**:
- **Unit Testing**: Test individual flows in isolation
- **Integration Testing**: Test flows with related automation
- **Bulk Testing**: Test with 200+ records to ensure bulkification
- **Error Testing**: Test error handling and fault paths
- **Edge Case Testing**: Test boundary conditions and edge cases

**Testing Checklist**:
- [ ] Test with various data scenarios
- [ ] Test error handling paths
- [ ] Test with bulk data (200+ records)
- [ ] Test edge cases
- [ ] Test integration points
- [ ] Test with different user contexts
- [ ] Test with different record types
- [ ] Test with different field values

**See Also**: <a href="{{ '/rag/testing/automated-testing-patterns.html' | relative_url }}">Automated Testing Patterns</a> for complete testing strategies.

## Troubleshooting

### Common Flow Issues

**Issue: Flow Not Running**
- **Check Entry Criteria**: Verify entry criteria matches test data
- **Check Flow Status**: Verify flow is active
- **Check Object Permissions**: Verify user has access to object
- **Check Debug Logs**: Review debug logs for flow execution

**Issue: Flow Running Too Often**
- **Tighten Entry Criteria**: Make entry criteria more specific
- **Check Change Detection**: Use `ISCHANGED()` to detect specific field changes
- **Review Flow Logic**: Ensure flow isn't triggering itself recursively

**Issue: Flow Performance Issues**
- **Optimize Entry Criteria**: Use strict entry criteria
- **Reduce SOQL Queries**: Use relationship queries when possible
- **Aggregate DML Operations**: Use collections for bulk operations
- **Move to Async**: Move heavy operations to async processing

**Issue: Flow Errors**
- **Check Fault Paths**: Ensure fault paths are configured
- **Check Error Logs**: Review error logs in `LOG_LogMessage__c`
- **Check Governor Limits**: Verify governor limits aren't exceeded
- **Check Field Access**: Verify user has field-level access

### Debugging Flows

**Debug Tools**:
- **Flow Debug Logs**: Enable debug logs for flow execution
- **Debug Mode**: Use debug mode in Flow Builder
- **System Debug**: Use System.debug in Apex actions
- **Error Logs**: Review error logs in `LOG_LogMessage__c`

**Debug Best Practices**:
- Enable debug logs before testing
- Use debug mode in Flow Builder for step-by-step execution
- Add debug variables to track flow state
- Review debug logs for execution flow
- Check error logs for failure points

## Change Management

### Version Control

**Version Control All Flows**: All Flows must be version controlled and tracked in source control.

**Best Practice**: 
- Use descriptive version comments
- Track Flow changes in version control
- Coordinate Flow changes with related automation
- Document breaking changes
- Maintain version history

### Testing

**Test Thoroughly**: Test Flows thoroughly before deployment, including edge cases and error scenarios.

**Best Practice**:
- Test with various data scenarios
- Test error handling paths
- Test with bulk data (200+ records)
- Coordinate testing with related automation
- Test in sandbox before production

### Documentation

**Document Purpose and Business Logic**: Document Flow purpose, business logic, and entry criteria.

**Best Practice**:
- Add clear descriptions to Flows
- Document entry criteria and decision logic
- Document related Flows and dependencies
- Update documentation when Flows change
- Document error handling patterns

### Coordination

**Coordinate Changes**: Coordinate Flow changes with related automation (other Flows, Apex, Process Builder, Workflow Rules).

**Best Practice**:
- Review related automation before making changes
- Test integration points
- Update related documentation
- Communicate changes to team
- Coordinate deployments

## Real-World Examples

### Example 1: Application Status Orchestration

**Flow**: `App_AfterSave_ApplicationStatusOrchestration`

**Type**: Record-Triggered Flow (After Save)

**Purpose**: Orchestrates application status changes and related record updates

**Entry Criteria**: `Record Type = 'Application' AND ISCHANGED(Status)`

**Pattern**: 
- After-save flow handling related records
- Uses subflows for reusable logic
- Publishes Platform Events for integrations
- Handles status transitions

**Structure**:
1. Entry Criteria: Status changed on Application
2. First Decision: Route by Status value
3. Subflow: "Create Advisor Tasks" for specific statuses
4. Subflow: "Sync Application Status to Child Objects"
5. Action: Publish Platform Event with application data
6. Action: Send email notification

### Example 2: Case Defaulting

**Flow**: `Case_BeforeSave_Defaulting`

**Type**: Record-Triggered Flow (Before Save)

**Purpose**: Sets default values on Case creation

**Entry Criteria**: `Record Type = 'Support Case' AND ISNEW()`

**Pattern**:
- Before-save flow updating triggering record fields
- Uses entry criteria to filter when flow should run
- Minimal DML operations

**Structure**:
1. Entry Criteria: New Case with specific Record Type
2. Fast Field Update: Set Priority = 'Medium' if null
3. Fast Field Update: Set Owner = Queue if null
4. Fast Field Update: Calculate Due Date based on SLA

### Example 3: Account Value Updates

**Flow**: `RT_C_BS_Update_Account_Values_from_Parent_Account_Academic_Programs`

**Type**: Record-Triggered Flow (Before Save)

**Purpose**: Updates Account values from parent Account Academic Programs

**Entry Criteria**: `Record Type = 'Academic Program' AND Parent Account != null AND ISNEW()`

**Pattern**:
- Before-save flow with strict entry criteria
- Updates triggering record fields only
- Uses relationship queries for parent data

**Structure**:
1. Entry Criteria: New Academic Program with Parent Account
2. Get Records: Get Parent Account with related fields
3. Fast Field Update: Update Account fields from Parent Account
4. Fast Field Update: Set derived fields based on Parent Account

### Example 4: Screen Flow - Mid-Point Evaluation

**Flow**: `Screen_Mid_Point_Evaluation`

**Type**: Screen Flow

**Purpose**: Guided evaluation process for student mid-point evaluations

**Real Impact**: Sending 29,004 emails (83.9% of automated emails in one org)

**Structure**:
1. Introduction Screen: Welcome and instructions
2. Data Collection Screens: Step-by-step evaluation input
3. Decision Nodes: Route based on evaluation responses
4. Review Screen: Summary of evaluation data
5. Confirmation Screen: Success message and next steps
6. Email Action: Send evaluation confirmation email

## Edge Cases and Limitations

### Before-Save Flow Limitations

**Limitations**:
- Cannot perform DML on other records
- Cannot make callouts
- Cannot publish Platform Events
- Record is not yet saved (no ID available for related records)
- Limited to fast field updates on triggering record

**Workarounds**:
- Use after-save flows for DML operations
- Use Platform Events for async processing
- Use Queueable Apex for callouts
- Use after-save flows for related record operations

### After-Save Flow Limitations

**Limitations**:
- Record is read-only (cannot modify triggering record fields)
- Must use after-save flow or trigger to modify triggering record
- Can cause recursion if not careful
- Governor limits apply to all operations

**Workarounds**:
- Use before-save flows for field updates
- Use recursion prevention patterns
- Monitor governor limit usage
- Move heavy operations to async processing

### Flow Recursion Prevention

**Prevention Patterns**:
- Check if field values have actually changed before performing updates
- Use static variables to track execution (in Apex actions)
- Use entry criteria with `ISCHANGED()` to detect specific changes
- Avoid update operations that would re-trigger the same flow

**Example Pattern**:
```
Entry Criteria: ISCHANGED(Status) AND Status = 'Closed'
Logic:
  - Check if Status was already 'Closed' (prevent recursion)
  - Only update if Status actually changed
  - Use decision node to prevent unnecessary updates
```

### Governor Limit Considerations

**Common Limit Issues**:
- Too many SOQL queries in loops
- Too many DML operations
- CPU time exceeded
- Heap size exceeded

**Solutions**:
- Use relationship queries to avoid multiple queries
- Aggregate DML operations using collections
- Move heavy operations to async processing
- Optimize flow logic to reduce CPU time
- Use bulk processing patterns

## Best Practices Summary

### Flow Design
- Use strict entry criteria to reduce unnecessary executions
- Separate before-save (field updates) from after-save (related records)
- Use Subflows for reusable logic
- Route by record state early in decision nodes
- Keep before-save flows fast and simple

### Error Handling
- Always configure fault paths for DML operations
- Always configure fault paths for Apex actions
- Log all errors to `LOG_LogMessage__c` object
- Use Platform Event fallback if DML fails
- Provide user-friendly error messages

### Performance
- Minimize SOQL queries (use relationship queries)
- Aggregate DML operations (use collections)
- Use fast field updates when possible
- Move heavy operations to async processing
- Monitor governor limit usage

### Integration
- Prefer Flows over Apex for Platform Event publication
- Use `@InvocableMethod` for complex logic
- Use `Callable` interface for flexible integration
- Separate business logic into service classes
- Design event payloads to be self-contained

### Testing
- Test with various data scenarios
- Test error handling paths
- Test with bulk data (200+ records)
- Test edge cases and boundary conditions
- Coordinate testing with related automation

### Maintenance
- Version control all flows
- Document flow purpose and logic
- Coordinate changes with related automation
- Update documentation when flows change
- Communicate changes to team

## Q&A

### Q: When should I use Flow instead of Apex?

**A**: Use Flow when logic can be expressed declaratively, you need to create/update related records based on record changes, need guided user interactions, or need to publish Platform Events. Flow is preferred for declarative automation; Apex is for complex logic that Flow cannot handle efficiently.

### Q: What is the difference between Before-Save and After-Save Flows?

**A**: Before-Save Flows update triggering record fields only and run before the record is saved. After-Save Flows handle related records, integrations, and events and run after the record is saved. Use Before-Save for field defaulting and validation; use After-Save for related records and integrations.

### Q: Can I modify field values in After-Save Flows?

**A**: No, records are read-only in After-Save Flows. You cannot modify field values in After-Save Flows. To modify field values, use Before-Save Flows or create an After-Save Flow that updates the record (which will trigger another flow execution).

### Q: Can I perform DML operations in Before-Save Flows?

**A**: No, Before-Save Flows cannot perform DML operations on other records. You can only modify field values on the triggering record. To perform DML on other records, use After-Save Flows or async processing (Platform Events, Queueable).

### Q: How do I make Apex methods callable from Flows?

**A**: Use `@InvocableMethod` annotation on static methods in public classes. Methods must accept and return lists (even for single values). Use `@InvocableVariable` for complex input parameters. Alternatively, implement `Callable` interface for classes that need to be callable from both Flows and Apex.

### Q: How do I handle errors in Flows?

**A**: Use fault paths for error handling, log errors to `LOG_LogMessage__c` object using `LOG_LogMessageUtility` class (implements `Callable` interface), use Platform Event fallback if DML fails, and provide user-friendly error messages.

### Q: What is the best naming convention for Flows?

**A**: Use format `{Type}_{Object}_{Trigger}_{Description}` where Type is `RT_` (Record-Triggered), `Screen_`, `Scheduled_`, or `Auto_`; Object is abbreviation like `C_` (Case), `App_` (Application); Trigger is `BS_` (Before Save) or `AS_` (After Save); and Description is what the flow does.

### Q: When should I use Subflows?

**A**: Use Subflows for reusable logic chunks like assignment rules, task creation, status updates, common validation logic, or reusable decision logic. Subflows enable easier testing, easier maintenance, and clearer flow structure.

### Q: How do I publish Platform Events from Flows?

**A**: Use Flow's "Publish Platform Event" action to publish events declaratively. This is preferred over Apex for declarative event publication. Include all necessary context in event payloads, minimize PII, and design payloads to be idempotent where possible.

### Q: What is the Platform Event fallback pattern?

**A**: If DML fails (governor limits, validation rules), publish Platform Event as fallback to ensure error is still captured. This pattern ensures errors are captured even when DML operations fail, using `ErrorLog__e` Platform Event as fallback mechanism.

### Q: How do I prevent Flow recursion?

**A**: Prevent Flow recursion by checking if field values have actually changed before performing updates, using entry criteria with `ISCHANGED()` to detect specific changes, avoiding update operations that would re-trigger the same flow, and using decision nodes to prevent unnecessary updates.

### Q: What are the governor limits for Flows?

**A**: Flows share the same governor limits as Apex: 100 SOQL queries, 150 DML operations, 10,000ms CPU time, 6MB heap (synchronous), 12MB heap (asynchronous), and 100 callouts (async only) per transaction.

### Q: How do I optimize Flow performance?

**A**: Optimize Flow performance by using strict entry criteria, minimizing SOQL queries (use relationship queries), aggregating DML operations (use collections), using fast field updates when possible, moving heavy operations to async processing, and monitoring governor limit usage.

### Q: How do I test Flows?

**A**: Test Flows with various data scenarios, test error handling paths, test with bulk data (200+ records), test edge cases and boundary conditions, test integration points, and coordinate testing with related automation.

### Q: What is the execution order of Flows?

**A**: Before-Save Flows execute at step 4 (after system validation, before custom validation rules). After-Save Flows execute at step 7 (after record save, after after-save triggers). See Order of Execution for complete details.

### Q: Can I make callouts from Before-Save Flows?

**A**: No, Before-Save Flows cannot make callouts. Use After-Save Flows or async processing (Platform Events, Queueable) for callouts.

### Q: How do I handle bulk operations in Flows?

**A**: Handle bulk operations by processing records in collections, aggregating DML operations, using relationship queries to avoid multiple queries, testing with 200+ records, and moving heavy operations to async processing when needed.

## Related Patterns

- <a href="{{ '/rag/development/apex-patterns.html' | relative_url }}">Apex Patterns</a> - Apex design patterns and best practices
- <a href="{{ '/rag/development/order-of-execution.html' | relative_url }}">Order of Execution</a> - Understanding when Flows execute
- <a href="{{ '/rag/architecture/event-driven-architecture.html' | relative_url }}">Event-Driven Architecture</a> - Platform Events and event-driven patterns
- <a href="{{ '/rag/integrations/integration-platform-patterns.html' | relative_url }}">Integration Platform Patterns</a> - Integration patterns with Flows
- <a href="{{ '/rag/development/error-handling-and-logging.html' | relative_url }}">Error Handling and Logging</a> - Error handling patterns for Flows
- <a href="{{ '/rag/development/governor-limits-and-optimization.html' | relative_url }}">Governor Limits and Optimization</a> - Performance considerations
- <a href="{{ '/rag/testing/automated-testing-patterns.html' | relative_url }}">Automated Testing Patterns</a> - Testing strategies for Flows
- <a href="{{ '/rag/code-examples/flow/record-triggered-examples.html' | relative_url }}">Record-Triggered Flow Examples</a> - Record-triggered flow patterns
- <a href="{{ '/rag/code-examples/flow/screen-flow-examples.html' | relative_url }}">Screen Flow Examples</a> - Screen flow patterns
- <a href="{{ '/rag/code-examples/flow/subflow-examples.html' | relative_url }}">Subflow Examples</a> - Subflow patterns
