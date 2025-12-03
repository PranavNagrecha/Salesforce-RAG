---
layout: default
title: Record Triggered Examples
description: Code examples for Record Triggered Examples
permalink: /rag/code-examples/flow/record-triggered-examples.html
---

# Record-Triggered Flow Code Examples

> This file contains complete, working examples for Record-Triggered Flow patterns.
> All examples follow Salesforce best practices and can be used as templates.

## Overview

Record-Triggered Flows run automatically when records are created or updated. They can run before save (to modify field values) or after save (to create related records, send notifications, etc.). This document provides practical examples of common Record-Triggered Flow patterns.

**Related Patterns**:
- <a href="{{ '/rag/development/flow-patterns.html' | relative_url }}">Flow Patterns</a> - Complete Flow design patterns
- <a href="{{ '/rag/development/order-of-execution.html' | relative_url }}">Order of Execution</a> - Understanding when Flows execute

## Examples

### Example 1: Before-Save Flow - Field Validation and Default Values

**Pattern**: Before-save flow for field validation and default values
**Use Case**: Setting default values or validating data before save
**Complexity**: Basic
**Related Patterns**: <a href="{{ '/rag/development/flow-patterns.html#record-triggered-flows' | relative_url }}">Flow Patterns</a>

**Problem**:
You need to set default values for fields and validate data before a record is saved.

**Solution**:

**Flow Configuration**:
- **Flow Type**: Record-Triggered Flow
- **Object**: Contact
- **Trigger**: A record is created or updated
- **Entry Conditions**: None (runs for all records)
- **Optimize for**: Actions and Related Records

**Flow Elements**:

1. **Decision Element**: Check if Email is empty
   - **Outcome 1**: Email is empty
     - **Criteria**: `{!$Record.Email}` IS NULL
   - **Outcome 2**: Email is not empty (Default Outcome)

2. **Assignment Element** (in Email is empty outcome):
   - **Variable**: `$Record.Email`
   - **Value**: `{!$Record.FirstName} + '.' + {!$Record.LastName} + '@example.com'`

3. **Decision Element**: Validate Email format
   - **Outcome 1**: Email is valid
     - **Criteria**: `{!$Record.Email}` CONTAINS '@'
   - **Outcome 2**: Email is invalid (Default Outcome)

4. **Formula Element** (in Email is invalid outcome):
   - **Name**: ErrorMessage
   - **Formula**: `'Email must contain @ symbol'`

5. **Fault Element** (in Email is invalid outcome):
   - **Fault Message**: `{!ErrorMessage}`

**Best Practices**:
- Use before-save flows for field modifications
- Validate data early in the process
- Provide clear error messages
- Use formulas for complex default value logic

### Example 2: After-Save Flow - Create Related Records

**Pattern**: After-save flow for creating related records
**Use Case**: Creating child records when parent is created
**Complexity**: Intermediate
**Related Patterns**: <a href="{{ '/rag/development/flow-patterns.html#record-triggered-flows' | relative_url }}">Flow Patterns</a>

**Problem**:
When an Account is created, you need to automatically create a default Contact record.

**Solution**:

**Flow Configuration**:
- **Flow Type**: Record-Triggered Flow
- **Object**: Account
- **Trigger**: A record is created
- **Entry Conditions**: None
- **Optimize for**: Actions and Related Records

**Flow Elements**:

1. **Decision Element**: Check if Account has Contacts
   - **Outcome 1**: No Contacts
     - **Criteria**: `{!$Record.Contacts__r}` IS NULL
   - **Outcome 2**: Has Contacts (Default Outcome)

2. **Create Records Element** (in No Contacts outcome):
   - **Object**: Contact
   - **How Many Records to Create**: One
   - **Field Values**:
     - `AccountId`: `{!$Record.Id}`
     - `FirstName`: `'Default'`
     - `LastName`: `{!$Record.Name}`
     - `Email`: `'contact@' + {!$Record.Name} + '.com'`

**Best Practices**:
- Use after-save flows for creating related records
- Check for existing records to avoid duplicates
- Use formulas for dynamic field values
- Handle bulk operations (flows automatically bulkify)

### Example 3: After-Save Flow - Send Email Notification

**Pattern**: After-save flow for sending notifications
**Use Case**: Sending email notifications when records are created or updated
**Complexity**: Intermediate
**Related Patterns**: <a href="{{ '/rag/development/flow-patterns.html#record-triggered-flows' | relative_url }}">Flow Patterns</a>

**Problem**:
When a Case is created with high priority, you need to send an email notification to the account owner.

**Solution**:

**Flow Configuration**:
- **Flow Type**: Record-Triggered Flow
- **Object**: Case
- **Trigger**: A record is created or updated
- **Entry Conditions**: 
  - `{!$Record.Priority}` EQUALS `High`
- **Optimize for**: Actions and Related Records

**Flow Elements**:

1. **Get Records Element**: Get Account Owner
   - **Object**: User
   - **Filter**: `Id` EQUALS `{!$Record.Account.OwnerId}`
   - **Store**: `AccountOwner`

2. **Decision Element**: Check if Account Owner exists
   - **Outcome 1**: Owner exists
     - **Criteria**: `{!AccountOwner.Id}` IS NOT NULL
   - **Outcome 2**: Owner does not exist (Default Outcome)

3. **Email Alerts Element** (in Owner exists outcome):
   - **Email Alert**: High Priority Case Alert
   - **Recipients**: `{!AccountOwner.Email}`
   - **Related To**: `{!$Record.Id}`

**Email Alert Configuration** (created separately):
- **Name**: High Priority Case Alert
- **Object**: Case
- **Email Template**: High Priority Case Notification
- **Recipients**: User (Account Owner)

**Best Practices**:
- Use entry conditions to limit flow execution
- Get related records before using their fields
- Use Email Alerts for reusable email templates
- Handle cases where related records don't exist

### Example 4: Before-Save Flow - Calculate Field Values

**Pattern**: Before-save flow for calculated fields
**Use Case**: Calculating field values based on other fields
**Complexity**: Intermediate
**Related Patterns**: <a href="{{ '/rag/development/flow-patterns.html#record-triggered-flows' | relative_url }}">Flow Patterns</a>

**Problem**:
You need to calculate a Contact's full name and set it in a custom field when FirstName or LastName changes.

**Solution**:

**Flow Configuration**:
- **Flow Type**: Record-Triggered Flow
- **Object**: Contact
- **Trigger**: A record is created or updated
- **Entry Conditions**: 
  - `{!$Record.FirstName}` IS CHANGED OR
  - `{!$Record.LastName}` IS CHANGED
- **Optimize for**: Actions and Related Records

**Flow Elements**:

1. **Formula Element**: Calculate Full Name
   - **Name**: FullName
   - **Formula**: `TRIM({!$Record.FirstName} + ' ' + {!$Record.LastName})`

2. **Assignment Element**: Set Full Name Field
   - **Variable**: `$Record.Full_Name__c`
   - **Value**: `{!FullName}`

**Best Practices**:
- Use before-save flows for field calculations
- Use entry conditions to run only when needed
- Use TRIM() to remove extra spaces
- Handle null values in formulas

### Example 5: After-Save Flow - Update Related Records

**Pattern**: After-save flow for updating related records
**Use Case**: Updating child records when parent changes
**Complexity**: Intermediate
**Related Patterns**: <a href="{{ '/rag/development/flow-patterns.html#record-triggered-flows' | relative_url }}">Flow Patterns</a>

**Problem**:
When an Account's Industry changes, you need to update all related Contacts' Industry field.

**Solution**:

**Flow Configuration**:
- **Flow Type**: Record-Triggered Flow
- **Object**: Account
- **Trigger**: A record is updated
- **Entry Conditions**: 
  - `{!$Record.Industry}` IS CHANGED
- **Optimize for**: Actions and Related Records

**Flow Elements**:

1. **Get Records Element**: Get Related Contacts
   - **Object**: Contact
   - **Filter**: `AccountId` EQUALS `{!$Record.Id}`
   - **Store**: `RelatedContacts`

2. **Decision Element**: Check if Contacts exist
   - **Outcome 1**: Contacts exist
     - **Criteria**: `{!RelatedContacts}` IS NOT NULL
   - **Outcome 2**: No Contacts (Default Outcome)

3. **Update Records Element** (in Contacts exist outcome):
   - **Object**: Contact
   - **Records to Update**: `{!RelatedContacts}`
   - **Field Values**:
     - `Industry__c`: `{!$Record.Industry}`

**Best Practices**:
- Use entry conditions to run only when needed
- Get related records before updating
- Handle bulk operations (flows automatically bulkify)
- Check for null/empty collections before updating

### Example 6: Before-Save Flow - Prevent Save with Validation

**Pattern**: Before-save flow for validation
**Use Case**: Preventing record save when validation fails
**Complexity**: Intermediate
**Related Patterns**: <a href="{{ '/rag/development/flow-patterns.html#record-triggered-flows' | relative_url }}">Flow Patterns</a>

**Problem**:
You need to prevent saving a Contact if the Email domain is not allowed.

**Solution**:

**Flow Configuration**:
- **Flow Type**: Record-Triggered Flow
- **Object**: Contact
- **Trigger**: A record is created or updated
- **Entry Conditions**: 
  - `{!$Record.Email}` IS NOT NULL
- **Optimize for**: Actions and Related Records

**Flow Elements**:

1. **Formula Element**: Extract Email Domain
   - **Name**: EmailDomain
   - **Formula**: `RIGHT({!$Record.Email}, LEN({!$Record.Email}) - FIND('@', {!$Record.Email}))`

2. **Decision Element**: Check if Domain is Allowed
   - **Outcome 1**: Domain not allowed
     - **Criteria**: `{!EmailDomain}` NOT IN `['example.com', 'company.com']`
   - **Outcome 2**: Domain allowed (Default Outcome)

3. **Fault Element** (in Domain not allowed outcome):
   - **Fault Message**: `'Email domain ' + {!EmailDomain} + ' is not allowed. Please use example.com or company.com.'`

**Best Practices**:
- Use before-save flows for validation
- Use formulas for complex validation logic
- Provide clear, actionable error messages
- Use entry conditions to limit flow execution

## Common Patterns

### Pattern 1: Bulkification

Record-Triggered Flows automatically bulkify. When processing multiple records:
- Use collection variables to store related records
- Use loops to process collections
- Avoid DML or SOQL inside loops (flows handle this automatically)

### Pattern 2: Entry Conditions

Use entry conditions to:
- Limit flow execution to specific scenarios
- Improve performance by avoiding unnecessary runs
- Reduce complexity by focusing on specific use cases

### Pattern 3: Error Handling

Handle errors by:
- Using fault paths for all operations
- Providing clear error messages
- Logging errors for troubleshooting
- Handling partial failures gracefully

## Related Examples

- <a href="{{ '/rag/code-examples/flow/screen-flow-examples.html' | relative_url }}">Screen Flow Examples</a> - User interaction flows
- <a href="{{ '/rag/code-examples/flow/subflow-examples.html' | relative_url }}">Subflow Examples</a> - Reusable flow components

## See Also

- <a href="{{ '/rag/development/flow-patterns.html' | relative_url }}">Flow Patterns</a> - Complete Flow design patterns
- <a href="{{ '/rag/development/order-of-execution.html' | relative_url }}">Order of Execution</a> - Understanding when Flows execute
- <a href="{{ '/rag/development/error-handling-and-logging.html' | relative_url }}">Error Handling and Logging</a> - Error handling patterns
