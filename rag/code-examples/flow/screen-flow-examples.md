---
title: "Screen Flow Code Examples"
level: "Intermediate"
tags:
  - flow
  - code-examples
  - screen-flow
  - user-interaction
last_reviewed: "2025-01-XX"
---

# Screen Flow Code Examples

> This file contains complete, working examples for Screen Flow patterns.
> All examples follow Salesforce best practices and can be used as templates.

## Overview

Screen Flows provide guided user interactions for multi-step processes. They are ideal for internal apps, portal UX, guided data capture, and step-by-step case/application handling. This document provides practical examples of common Screen Flow patterns.

**Related Patterns**:
- <a href="{{ '/rag/development/flow-patterns.html' | relative_url }}">Flow Patterns</a> - Complete Flow design patterns
- <a href="{{ '/rag/code-examples/flow/code-examples/flow/record-triggered-examples.html' | relative_url }}">Record-Triggered Examples</a> - Automated flow patterns

## Examples

### Example 1: Basic Multi-Step Form

**Pattern**: Multi-step form for data collection
**Use Case**: Collecting user information across multiple screens
**Complexity**: Basic
**Related Patterns**: <a href="{{ '/rag/development/flow-patterns.html#screen-flows.html' | relative_url }}">Flow Patterns</a>

**Problem**:
You need to collect contact information across multiple screens with validation and navigation.

**Solution**:

**Flow Configuration**:
- **Flow Type**: Screen Flow
- **Start Element**: Screen
- **Navigation**: Next/Previous buttons

**Flow Structure**:

1. **Screen 1**: Personal Information
   - **Fields**:
     - First Name (Text Input, Required)
     - Last Name (Text Input, Required)
     - Email (Email Input, Required)
   - **Navigation**: Next button → Screen 2

2. **Screen 2**: Contact Details
   - **Fields**:
     - Phone (Phone Input)
     - Mailing Address (Address Input)
   - **Navigation**: 
     - Previous button → Screen 1
     - Next button → Screen 3

3. **Screen 3**: Review and Submit
   - **Display**: Summary of all entered information
   - **Actions**:
     - Submit button → Create Contact record
     - Back button → Screen 2

4. **Create Records Element**: Create Contact
   - **Object**: Contact
   - **Field Values**:
     - `FirstName`: `{!First_Name}`
     - `LastName`: `{!Last_Name}`
     - `Email`: `{!Email}`
     - `Phone`: `{!Phone}`
     - `MailingStreet`: `{!Mailing_Address_Street}`
     - `MailingCity`: `{!Mailing_Address_City}`
     - `MailingState`: `{!Mailing_Address_State}`
     - `MailingPostalCode`: `{!Mailing_Address_PostalCode}`

5. **Screen 4**: Success
   - **Display**: Confirmation message with Contact ID
   - **Navigation**: Finish button

**Best Practices**:
- Break long forms into logical steps
- Provide clear navigation (Next/Previous)
- Show summary screen before submission
- Validate required fields on each screen

### Example 2: Conditional Navigation Based on User Input

**Pattern**: Dynamic flow navigation based on user selections
**Use Case**: Different paths based on user choices
**Complexity**: Intermediate
**Related Patterns**: <a href="{{ '/rag/development/flow-patterns.html#screen-flows.html' | relative_url }}">Flow Patterns</a>

**Problem**:
You need to show different screens based on user selections (e.g., different application types).

**Solution**:

**Flow Structure**:

1. **Screen 1**: Application Type Selection
   - **Fields**:
     - Application Type (Picklist, Required)
       - Options: Student, Staff, Partner
   - **Navigation**: Next button → Decision

2. **Decision Element**: Route by Application Type
   - **Outcome 1**: Student Application
     - **Criteria**: `{!Application_Type}` EQUALS `Student`
   - **Outcome 2**: Staff Application
     - **Criteria**: `{!Application_Type}` EQUALS `Staff`
   - **Outcome 3**: Partner Application
     - **Criteria**: `{!Application_Type}` EQUALS `Partner`

3. **Screen 2A**: Student Information (Student path)
   - **Fields**:
     - Student ID (Text Input)
     - Program (Picklist)
     - Enrollment Date (Date Input)
   - **Navigation**: Next button → Screen 3

4. **Screen 2B**: Staff Information (Staff path)
   - **Fields**:
     - Employee ID (Text Input)
     - Department (Picklist)
     - Hire Date (Date Input)
   - **Navigation**: Next button → Screen 3

5. **Screen 2C**: Partner Information (Partner path)
   - **Fields**:
     - Organization Name (Text Input)
     - Partner Type (Picklist)
     - Contract Number (Text Input)
   - **Navigation**: Next button → Screen 3

6. **Screen 3**: Review and Submit
   - **Display**: Summary based on selected path
   - **Actions**: Submit button → Create record

**Best Practices**:
- Use Decision elements to route users
- Show relevant fields based on selections
- Maintain context across screens
- Provide clear navigation paths

### Example 3: Lookup and Related Record Creation

**Pattern**: Finding existing records and creating related records
**Use Case**: Looking up accounts and creating contacts
**Complexity**: Intermediate
**Related Patterns**: <a href="{{ '/rag/development/flow-patterns.html#screen-flows.html' | relative_url }}">Flow Patterns</a>

**Problem**:
You need to allow users to search for an Account and then create a Contact for that Account.

**Solution**:

**Flow Structure**:

1. **Screen 1**: Account Lookup
   - **Fields**:
     - Account Search (Lookup Field, Required)
   - **Navigation**: Next button → Get Records

2. **Get Records Element**: Get Account Details
   - **Object**: Account
   - **Filter**: `Id` EQUALS `{!Account_Search}`
   - **Store**: `SelectedAccount`

3. **Decision Element**: Check if Account Found
   - **Outcome 1**: Account found
     - **Criteria**: `{!SelectedAccount.Id}` IS NOT NULL
   - **Outcome 2**: Account not found (Default Outcome)

4. **Screen 2A**: Account Not Found (Account not found path)
   - **Display**: Error message
   - **Actions**: Back button → Screen 1

5. **Screen 2B**: Contact Information (Account found path)
   - **Display**: Account Name: `{!SelectedAccount.Name}`
   - **Fields**:
     - First Name (Text Input, Required)
     - Last Name (Text Input, Required)
     - Email (Email Input, Required)
     - Phone (Phone Input)
   - **Navigation**: Next button → Screen 3

6. **Screen 3**: Review
   - **Display**: 
     - Account: `{!SelectedAccount.Name}`
     - Contact: `{!First_Name} {!Last_Name}`
   - **Actions**: Submit button → Create Contact

7. **Create Records Element**: Create Contact
   - **Object**: Contact
   - **Field Values**:
     - `AccountId`: `{!SelectedAccount.Id}`
     - `FirstName`: `{!First_Name}`
     - `LastName`: `{!Last_Name}`
     - `Email`: `{!Email}`
     - `Phone`: `{!Phone}`

8. **Screen 4**: Success
   - **Display**: Contact created successfully
   - **Navigation**: Finish button

**Best Practices**:
- Use Lookup fields for record selection
- Validate that records are found
- Show selected record information
- Create related records with proper relationships

### Example 4: Data Collection with Validation

**Pattern**: Collecting and validating data before submission
**Use Case**: Ensuring data quality before record creation
**Complexity**: Intermediate
**Related Patterns**: <a href="{{ '/rag/development/flow-patterns.html#screen-flows.html' | relative_url }}">Flow Patterns</a>

**Problem**:
You need to collect case information with validation before creating the case.

**Solution**:

**Flow Structure**:

1. **Screen 1**: Case Information
   - **Fields**:
     - Subject (Text Input, Required)
     - Description (Long Text Area, Required)
     - Priority (Picklist, Required)
     - Category (Picklist, Required)
   - **Navigation**: Next button → Validation

2. **Decision Element**: Validate Required Fields
   - **Outcome 1**: Valid
     - **Criteria**: 
       - `{!Subject}` IS NOT NULL AND
       - `{!Description}` IS NOT NULL AND
       - `{!Priority}` IS NOT NULL AND
       - `{!Category}` IS NOT NULL
   - **Outcome 2**: Invalid (Default Outcome)

3. **Screen 2A**: Validation Error (Invalid path)
   - **Display**: Error message listing missing fields
   - **Actions**: Back button → Screen 1

4. **Screen 2B**: Additional Information (Valid path)
   - **Fields**:
     - Contact Email (Email Input)
     - Contact Phone (Phone Input)
   - **Navigation**: Next button → Screen 3

5. **Screen 3**: Review
   - **Display**: Summary of all information
   - **Actions**: Submit button → Create Case

6. **Create Records Element**: Create Case
   - **Object**: Case
   - **Field Values**:
     - `Subject`: `{!Subject}`
     - `Description`: `{!Description}`
     - `Priority`: `{!Priority}`
     - `Category__c`: `{!Category}`
     - `ContactEmail`: `{!Contact_Email}`
     - `ContactPhone`: `{!Contact_Phone}`

7. **Screen 4**: Success
   - **Display**: Case created: `{!Case.Id}`
   - **Navigation**: Finish button

**Best Practices**:
- Validate data before submission
- Show clear error messages
- Allow users to correct errors
- Display summary before final submission

### Example 5: Multi-Object Creation

**Pattern**: Creating multiple related records in one flow
**Use Case**: Creating Account, Contact, and Opportunity together
**Complexity**: Advanced
**Related Patterns**: <a href="{{ '/rag/development/flow-patterns.html#screen-flows.html' | relative_url }}">Flow Patterns</a>

**Problem**:
You need to create an Account, Contact, and Opportunity in a single guided process.

**Solution**:

**Flow Structure**:

1. **Screen 1**: Account Information
   - **Fields**:
     - Account Name (Text Input, Required)
     - Industry (Picklist)
     - Type (Picklist)
   - **Navigation**: Next button → Screen 2

2. **Screen 2**: Contact Information
   - **Fields**:
     - First Name (Text Input, Required)
     - Last Name (Text Input, Required)
     - Email (Email Input, Required)
     - Phone (Phone Input)
     - Title (Text Input)
   - **Navigation**: 
     - Previous button → Screen 1
     - Next button → Screen 3

3. **Screen 3**: Opportunity Information
   - **Fields**:
     - Opportunity Name (Text Input, Required)
     - Stage (Picklist, Required)
     - Amount (Currency Input)
     - Close Date (Date Input, Required)
   - **Navigation**:
     - Previous button → Screen 2
     - Next button → Screen 4

4. **Screen 4**: Review
   - **Display**: Summary of all information
   - **Actions**: Submit button → Create Records

5. **Create Records Element 1**: Create Account
   - **Object**: Account
   - **Field Values**:
     - `Name`: `{!Account_Name}`
     - `Industry`: `{!Industry}`
     - `Type`: `{!Account_Type}`
   - **Store**: `CreatedAccount`

6. **Create Records Element 2**: Create Contact
   - **Object**: Contact
   - **Field Values**:
     - `AccountId`: `{!CreatedAccount.Id}`
     - `FirstName`: `{!First_Name}`
     - `LastName`: `{!Last_Name}`
     - `Email`: `{!Email}`
     - `Phone`: `{!Phone}`
     - `Title`: `{!Title}`
   - **Store**: `CreatedContact`

7. **Create Records Element 3**: Create Opportunity
   - **Object**: Opportunity
   - **Field Values**:
     - `AccountId`: `{!CreatedAccount.Id}`
     - `ContactId`: `{!CreatedContact.Id}`
     - `Name`: `{!Opportunity_Name}`
     - `StageName`: `{!Stage}`
     - `Amount`: `{!Amount}`
     - `CloseDate`: `{!Close_Date}`

8. **Screen 5**: Success
   - **Display**: 
     - Account: `{!CreatedAccount.Name}`
     - Contact: `{!CreatedContact.Name}`
     - Opportunity: `{!Opportunity_Name}`
   - **Navigation**: Finish button

**Best Practices**:
- Create parent records before child records
- Store created records in variables for relationships
- Show progress across multiple steps
- Provide clear summary before submission

## Common Patterns

### Pattern 1: Step Structure

Organize Screen Flows with clear stages:
- **Step 1**: Identify/lookup
- **Step 2**: Collect core information
- **Step 3**: Optional/extras
- **Step 4**: Confirmation/review

### Pattern 2: Context Handling

- Prefer not asking users for IDs explicitly
- Use lookups or context from previous steps
- Pass context between steps using variables

### Pattern 3: Error Handling

- Validate data at each step
- Show clear error messages
- Allow users to correct errors
- Handle missing or invalid data gracefully

## Related Examples

- <a href="{{ '/rag/code-examples/flow/code-examples/flow/record-triggered-examples.html' | relative_url }}">Record-Triggered Examples</a> - Automated flow patterns
- <a href="{{ '/rag/code-examples/flow/code-examples/flow/subflow-examples.html' | relative_url }}">Subflow Examples</a> - Reusable flow components

## See Also

- <a href="{{ '/rag/development/flow-patterns.html' | relative_url }}">Flow Patterns</a> - Complete Flow design patterns
- <a href="{{ '/rag/development/error-handling-and-logging.html' | relative_url }}">Error Handling and Logging</a> - Error handling patterns
