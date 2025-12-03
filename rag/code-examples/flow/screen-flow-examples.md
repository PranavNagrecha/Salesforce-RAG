---
layout: default
title: Screen Flow Code Examples
description: Screen Flows provide guided user interactions for multi-step processes, data collection, and complex forms with conditional logic
permalink: /rag/code-examples/flow/screen-flow-examples.html
level: Intermediate
tags:
  - code-examples
  - flow
  - screen-flow
  - user-interaction
last_reviewed: 2025-12-03
---

# Screen Flow Code Examples

## Overview

Screen Flows provide step-by-step user interactions for complex processes that require user input, validation, and guided workflows. These examples demonstrate common patterns for:

- **Multi-step data capture**: Collecting information across multiple screens
- **Conditional navigation**: Showing/hiding steps based on user input
- **Data validation**: Validating user input before proceeding
- **Progress indicators**: Showing users where they are in the process
- **Error handling**: Graceful error messages and recovery

## When to Use

### Use Screen Flows When

- Need multi-step data collection with user input
- Need guided workflows (onboarding, applications, surveys)
- Need conditional logic based on user responses
- Need complex forms that standard page layouts cannot handle
- Need step-by-step processes with validation
- Need user-friendly interfaces for non-technical users

### Avoid Screen Flows When

- Need simple single-field updates (use standard page layouts)
- Need complex business logic (consider Apex + LWC)
- Need highly customized UI (consider LWC)
- Need offline capabilities (not supported)
- Need real-time collaboration (not supported)

## Example 1: Multi-Step Case Creation

**Use Case**: Guide users through creating a detailed Case with conditional fields based on case type.

**Flow Name**: `Screen_Create_Detailed_Case`

**Flow Structure**:
1. **Start Element**: Screen Flow
   - No entry criteria (launched from button or LWC)

2. **Screen 1**: Case Type Selection
   - **Screen Components**:
     - `CaseType` (Picklist): "Select Case Type"
       - Options: "Technical Support", "Billing Inquiry", "Feature Request", "Bug Report"
   - **Navigation**:
     - Next → Screen 2
     - Cancel → End Flow

3. **Decision Node**: Route by Case Type
   - Outcome 1: `CaseType = 'Technical Support'` → Technical Support Path
   - Outcome 2: `CaseType = 'Billing Inquiry'` → Billing Inquiry Path
   - Outcome 3: `CaseType = 'Feature Request'` → Feature Request Path
   - Outcome 4: `CaseType = 'Bug Report'` → Bug Report Path

4. **Screen 2a**: Technical Support Details
   - **Screen Components**:
     - `Subject` (Text): "Subject" (required)
     - `Description` (Long Text): "Description" (required)
     - `Priority` (Picklist): "Priority"
       - Options: "Low", "Medium", "High", "Critical"
     - `Product` (Lookup): "Related Product" (required)
   - **Navigation**:
     - Next → Screen 3
     - Back → Screen 1
     - Cancel → End Flow

5. **Screen 2b**: Billing Inquiry Details
   - **Screen Components**:
     - `Subject` (Text): "Subject" (required)
     - `Description` (Long Text): "Description" (required)
     - `InvoiceNumber` (Text): "Invoice Number" (required)
     - `Amount` (Currency): "Amount in Question"
   - **Navigation**:
     - Next → Screen 3
     - Back → Screen 1
     - Cancel → End Flow

6. **Screen 3**: Review and Submit
   - **Screen Components**:
     - Display Text: "Review your case details:"
     - Display Text: "Case Type: {!CaseType}"
     - Display Text: "Subject: {!Subject}"
     - Display Text: "Description: {!Description}"
     - Display Text: "Priority: {!Priority}"
   - **Navigation**:
     - Submit → Create Case
     - Back → Previous Screen (based on Case Type)
     - Cancel → End Flow

7. **Create Records Element**: Create Case
   - Object: Case
   - How Many: One
   - Fields:
     - `Subject` = `{!Subject}`
     - `Description` = `{!Description}`
     - `Priority` = `{!Priority}`
     - `Type` = `{!CaseType}`
     - `Status` = `'New'`
     - `Origin` = `'Screen Flow'`
   - Store In: `NewCase` (single record variable)
   - Fault Path: Show error screen

8. **Screen 4**: Success Confirmation
   - **Screen Components**:
     - Display Text: "Case created successfully!"
     - Display Text: "Case Number: {!NewCase.CaseNumber}"
     - Display Text: "You will receive an email confirmation shortly."
   - **Navigation**:
     - Done → End Flow

**Key Points**:
- Use decision nodes to show different screens based on user input
- Validate required fields at each step
- Provide clear navigation (Next, Back, Cancel)
- Show confirmation screen after successful creation
- Handle errors gracefully with error screens

## Example 2: Conditional Step Navigation

**Use Case**: Show/hide steps based on user responses (skip steps that don't apply).

**Flow Name**: `Screen_Conditional_Application_Process`

**Flow Structure**:
1. **Start Element**: Screen Flow

2. **Screen 1**: Basic Information
   - **Screen Components**:
     - `FirstName` (Text): "First Name" (required)
     - `LastName` (Text): "Last Name" (required)
     - `Email` (Email): "Email" (required)
     - `HasPreviousExperience` (Checkbox): "Do you have previous experience?"
   - **Navigation**:
     - Next → Decision Node
     - Cancel → End Flow

3. **Decision Node**: Check Previous Experience
   - Outcome 1: `HasPreviousExperience = true` → Show Experience Screen
   - Outcome 2: `HasPreviousExperience = false` → Skip to Education Screen

4. **Screen 2a**: Previous Experience (conditional)
   - **Screen Components**:
     - `YearsOfExperience` (Number): "Years of Experience" (required)
     - `PreviousCompany` (Text): "Previous Company"
     - `PreviousRole` (Text): "Previous Role"
   - **Navigation**:
     - Next → Screen 3
     - Back → Screen 1
     - Cancel → End Flow

5. **Screen 3**: Education Information
   - **Screen Components**:
     - `EducationLevel` (Picklist): "Education Level" (required)
     - `Institution` (Text): "Institution"
     - `GraduationYear` (Number): "Graduation Year"
   - **Navigation**:
     - Next → Screen 4
     - Back → Previous Screen (conditional)
     - Cancel → End Flow

6. **Screen 4**: Additional Information
   - **Screen Components**:
     - `WillingToRelocate` (Checkbox): "Willing to Relocate?"
     - `AvailableStartDate` (Date): "Available Start Date"
     - `SalaryExpectation` (Currency): "Salary Expectation"
   - **Navigation**:
     - Submit → Create Application
     - Back → Screen 3
     - Cancel → End Flow

7. **Create Records Element**: Create Application
   - Object: Application__c
   - Fields: Map all collected fields
   - Fault Path: Show error screen

**Key Points**:
- Use decision nodes to conditionally show/hide screens
- Skip irrelevant steps to improve user experience
- Maintain navigation context (Back button goes to correct previous screen)
- Validate conditional fields only when screen is shown

## Example 3: Data Validation and Error Handling

**Use Case**: Validate user input and show error messages before proceeding.

**Flow Name**: `Screen_Validated_Data_Entry`

**Flow Structure**:
1. **Start Element**: Screen Flow

2. **Screen 1**: Contact Information
   - **Screen Components**:
     - `Email` (Email): "Email" (required)
     - `Phone` (Phone): "Phone" (required)
     - `DateOfBirth` (Date): "Date of Birth" (required)
   - **Navigation**:
     - Next → Validation Decision
     - Cancel → End Flow

3. **Decision Node**: Validate Email Format
   - Outcome 1: `CONTAINS(Email, '@') AND CONTAINS(Email, '.')` → Valid Email
   - Outcome 2: Default → Invalid Email

4. **Decision Node**: Validate Date of Birth
   - Outcome 1: `DateOfBirth < TODAY()` → Valid Date
   - Outcome 2: Default → Invalid Date

5. **Screen 2**: Error Screen (if validation fails)
   - **Screen Components**:
     - Display Text: "Please correct the following errors:"
     - Display Text: "• Email format is invalid" (if email invalid)
     - Display Text: "• Date of Birth must be in the past" (if date invalid)
   - **Navigation**:
     - Back → Screen 1
     - Cancel → End Flow

6. **Screen 3**: Additional Information (if validation passes)
   - **Screen Components**:
     - `AdditionalInfo` (Long Text): "Additional Information"
   - **Navigation**:
     - Submit → Create Contact
     - Back → Screen 1
     - Cancel → End Flow

7. **Create Records Element**: Create Contact
   - Object: Contact
   - Fields: Map validated fields
   - Fault Path: Show error screen

**Key Points**:
- Validate data before proceeding to next step
- Show clear error messages to users
- Allow users to correct errors and retry
- Use formula expressions for validation logic
- Handle DML errors gracefully with fault paths

## Example 4: Progress Indicator

**Use Case**: Show users their progress through a multi-step process.

**Flow Name**: `Screen_Application_With_Progress`

**Flow Structure**:
1. **Start Element**: Screen Flow
   - Initialize variable: `CurrentStep` = 1
   - Initialize variable: `TotalSteps` = 4

2. **Screen 1**: Step 1 - Personal Information
   - **Screen Components**:
     - Display Text: "Step 1 of 4: Personal Information"
     - Display Text: "Progress: {!CurrentStep} / {!TotalSteps}"
     - `FirstName` (Text): "First Name" (required)
     - `LastName` (Text): "Last Name" (required)
   - **Navigation**:
     - Next → Assignment (increment step) → Screen 2
     - Cancel → End Flow

3. **Assignment Element**: Increment Step
   - `CurrentStep` = `{!CurrentStep} + 1`

4. **Screen 2**: Step 2 - Contact Information
   - **Screen Components**:
     - Display Text: "Step 2 of 4: Contact Information"
     - Display Text: "Progress: {!CurrentStep} / {!TotalSteps}"
     - `Email` (Email): "Email" (required)
     - `Phone` (Phone): "Phone" (required)
   - **Navigation**:
     - Next → Assignment (increment step) → Screen 3
     - Back → Assignment (decrement step) → Screen 1
     - Cancel → End Flow

5. **Screen 3**: Step 3 - Education
   - **Screen Components**:
     - Display Text: "Step 3 of 4: Education"
     - Display Text: "Progress: {!CurrentStep} / {!TotalSteps}"
     - `EducationLevel` (Picklist): "Education Level"
   - **Navigation**:
     - Next → Assignment (increment step) → Screen 4
     - Back → Assignment (decrement step) → Screen 2
     - Cancel → End Flow

6. **Screen 4**: Step 4 - Review and Submit
   - **Screen Components**:
     - Display Text: "Step 4 of 4: Review and Submit"
     - Display Text: "Progress: {!CurrentStep} / {!TotalSteps}"
     - Display Text: "Review your information before submitting"
   - **Navigation**:
     - Submit → Create Application
     - Back → Assignment (decrement step) → Screen 3
     - Cancel → End Flow

**Key Points**:
- Track current step with variables
- Display progress indicator on each screen
- Update step counter when navigating
- Show users where they are in the process

## Testing Considerations

### Test Scenarios

1. **Navigation**:
   - Test Next button on each screen
   - Test Back button (returns to correct previous screen)
   - Test Cancel button (ends flow correctly)
   - Test conditional navigation (decision nodes)

2. **Validation**:
   - Test required field validation
   - Test format validation (email, phone, date)
   - Test business rule validation
   - Test error message display

3. **Data Collection**:
   - Test all field types (text, picklist, lookup, date, etc.)
   - Test conditional fields (show/hide based on input)
   - Test default values
   - Test data persistence across screens

4. **Error Handling**:
   - Test DML errors (duplicate records, validation rules)
   - Test network errors (if applicable)
   - Test user cancellation
   - Test fault paths

### Best Practices

- Test all navigation paths
- Test with different user permissions
- Test with different data scenarios
- Test error scenarios
- Test on mobile devices (if applicable)
- Verify progress indicators work correctly

## Related Patterns

- <a href="{{ '/rag/development/flow-patterns.html' | relative_url }}">Flow Patterns</a> - Comprehensive Flow patterns including Screen Flow best practices
- <a href="{{ '/rag/code-examples/flow/subflow-examples.html' | relative_url }}">Subflow Examples</a> - Reusable Subflow patterns for Screen Flows
- <a href="{{ '/rag/development/lwc-patterns.html' | relative_url }}">LWC Patterns</a> - When to use LWC instead of Screen Flows
- <a href="{{ '/rag/development/error-handling-and-logging.html' | relative_url }}">Error Handling and Logging</a> - Error handling patterns for Flows
