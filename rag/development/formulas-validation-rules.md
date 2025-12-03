---
layout: default
title: Formulas and Validation Rules
description: Comprehensive guide to Salesforce Validation Rules and Formula Fields, including syntax, operations, patterns, use cases, and best practices
permalink: /rag/development/formulas-validation-rules.html
---

# Formulas and Validation Rules

> **Declarative Data Quality**: Validation Rules are the primary declarative mechanism for ensuring data quality in Salesforce. They execute during the before-save phase and prevent invalid data from being saved to the database.

## Overview

Validation Rules enforce data quality by preventing records from being saved when they don't meet specified criteria. They use formula expressions to evaluate field values and related data, providing immediate feedback to users when validation fails.

**Key Characteristics**:
- Execute during before-save phase (after before-save flows and triggers)
- Cannot be bypassed by standard users (unlike workflow field updates)
- Provide immediate user feedback with error messages
- Support complex formula expressions with cross-object references
- Impact user save time (run synchronously)

**Execution Context**: Custom validation rules execute during step 4 of the order of execution, after system validation rules (step 3) and before-save flows/triggers have run. This allows validation rules to reference field values that may have been modified by before-save automation.

**Relationship to Other Validation Methods**:
- **System Validation Rules**: Execute first (step 3), enforce required fields, data types, and field-level security
- **Custom Validation Rules**: Execute after before-save automation (step 4), can reference modified field values
- **Before-Save Flows**: Can perform simple validations, but validation rules are preferred for data quality enforcement
- **Apex Validation**: Used for complex validations requiring queries, callouts, or complex business logic

## Prerequisites

**Required Knowledge**:
- Understanding of Salesforce data model and field types
- Familiarity with formula syntax and operators
- Knowledge of order of execution in Salesforce
- Understanding of when validation rules execute vs other automation
- Experience with field-level and object-level security

**Recommended Reading**:
- <a href="{{ '/rag/development/order-of-execution.html' | relative_url }}">Order of Execution</a> - Understanding when validation rules execute
- <a href="{{ '/rag/development/flow-patterns.html' | relative_url }}">Flow Patterns</a> - When to use Flows vs Validation Rules
- <a href="{{ '/rag/code-examples/utilities/validation-examples.html' | relative_url }}">Validation Examples</a> - Apex validation patterns for complex scenarios

## When to Use Validation Rules

### Use Validation Rules When:
- Need to enforce data quality at the point of entry
- Validation logic can be expressed in a formula (no queries required)
- Need immediate user feedback on save
- Validation applies to all users (cannot be bypassed)
- Simple to moderate complexity validation logic
- Cross-field validation within the same record
- Conditional required fields based on other field values
- Format validation (email, phone, URL, etc.)
- Range validation (numbers, dates)
- Status transition validation

### Use Before-Save Flows When:
- Need to modify field values based on validation
- Validation requires simple decision logic that's easier to visualize
- Need to set default values when validation fails
- Business users need to maintain the logic visually

### Use Apex Validation When:
- Validation requires SOQL queries to check related records
- Need to validate against external data (callouts)
- Complex business logic that formulas cannot express efficiently
- Need to validate across multiple records in bulk
- Validation requires complex calculations or transformations
- Need dynamic error messages based on multiple conditions
- Performance is critical and formula complexity would impact save time

### Decision Matrix

| Scenario | Validation Rules | Before-Save Flow | Apex |
|----------|-----------------|------------------|------|
| Email format validation | ✅ | ⚠️ (overkill) | ❌ |
| Required field when Status = "Closed" | ✅ | ✅ | ❌ |
| Amount must be > 0 | ✅ | ⚠️ (overkill) | ❌ |
| Check if related Account has specific field value | ❌ | ❌ | ✅ |
| Validate against external system | ❌ | ❌ | ✅ |
| Complex multi-record validation | ❌ | ❌ | ✅ |
| Set default value if validation fails | ⚠️ | ✅ | ✅ |

## Formula Syntax and Operations

### Text Operations

**CONTAINS**: Check if text contains a substring
```
CONTAINS(Email, "@")
```

**BEGINS**: Check if text begins with a substring
```
BEGINS(AccountNumber, "ACC-")
```

**ENDS**: Check if text ends with a substring
```
ENDS(Website, ".com")
```

**LEN**: Get length of text
```
LEN(Description) > 1000
```

**LEFT**: Get leftmost characters
```
LEFT(Phone, 3) = "415"
```

**RIGHT**: Get rightmost characters
```
RIGHT(Email, 4) = ".com"
```

**MID**: Get substring from middle
```
MID(AccountNumber, 5, 3) = "123"
```

**SUBSTITUTE**: Replace text
```
SUBSTITUTE(Phone, " ", "") = Phone
```

**TRIM**: Remove leading/trailing spaces
```
TRIM(LastName) <> LastName
```

**UPPER**: Convert to uppercase
```
UPPER(Status) = "CLOSED"
```

**LOWER**: Convert to lowercase
```
LOWER(Email) <> Email
```

**TEXT**: Convert number/date to text
```
TEXT(Amount) = "1000"
```

### Number Operations

**Arithmetic Operators**: +, -, *, /
```
Amount > (Quantity * UnitPrice)
```

**MOD**: Modulo (remainder)
```
MOD(AccountNumber, 10) = 0
```

**ABS**: Absolute value
```
ABS(Amount) = Amount
```

**CEILING**: Round up
```
CEILING(Amount) = Amount
```

**FLOOR**: Round down
```
FLOOR(Amount) = Amount
```

**MAX**: Maximum value
```
MAX(Amount, 0) <> Amount
```

**MIN**: Minimum value
```
MIN(Amount, 1000) <> Amount
```

**ROUND**: Round to nearest integer
```
ROUND(Amount) <> Amount
```

### Date/Time Operations

**TODAY**: Current date
```
CloseDate < TODAY()
```

**NOW**: Current date/time
```
CreatedDate > NOW()
```

**DATEVALUE**: Convert text/date-time to date
```
DATEVALUE(CreatedDate) = TODAY()
```

**DATETIMEVALUE**: Convert text to date-time
```
DATETIMEVALUE("2024-01-01 12:00:00")
```

**YEAR**: Extract year
```
YEAR(CloseDate) < YEAR(TODAY())
```

**MONTH**: Extract month
```
MONTH(CloseDate) = 12
```

**DAY**: Extract day
```
DAY(CloseDate) > 28
```

**WEEKDAY**: Day of week (1=Sunday, 7=Saturday)
```
WEEKDAY(CloseDate) = 1
```

**ADDMONTHS**: Add months to date
```
CloseDate < ADDMONTHS(TODAY(), 1)
```

**DATE**: Create date from year, month, day
```
CloseDate < DATE(2024, 12, 31)
```

### Logical Operations

**AND**: Logical AND
```
AND(Status = "Closed", Amount > 0)
```

**OR**: Logical OR
```
OR(ISBLANK(Email), ISBLANK(Phone))
```

**NOT**: Logical NOT
```
NOT(ISBLANK(Email))
```

**IF**: Conditional expression
```
IF(Amount > 1000, "High", "Low")
```

**CASE**: Multiple conditions
```
CASE(Status, "New", 1, "In Progress", 2, 3)
```

**ISBLANK**: Check if field is blank
```
ISBLANK(Email)
```

**ISNULL**: Check if field is null
```
ISNULL(Amount)
```

**ISCHANGED**: Check if field changed
```
ISCHANGED(Status)
```

**ISNEW**: Check if record is new
```
ISNEW()
```

**PRIORVALUE**: Get previous field value
```
Status <> PRIORVALUE(Status)
```

### Relationship Operations

**Cross-Object Field References**: Access related object fields
```
Account.Industry = "Technology"
```

**$Record**: Reference current record context
```
$Record.Status = "Closed"
```

**$User**: Reference current user fields
```
$User.Department = "Sales"
```

**$Profile**: Reference current user profile
```
$Profile.Name = "System Administrator"
```

### Type Conversion

**TEXT**: Convert to text
```
TEXT(Amount) = "1000"
```

**VALUE**: Convert text to number
```
VALUE(AccountNumber) > 1000
```

**DATEVALUE**: Convert to date
```
DATEVALUE(TextDate__c)
```

**DATETIMEVALUE**: Convert to date-time
```
DATETIMEVALUE(TextDateTime__c)
```

## Common Validation Patterns

### 1. Required Field Validation

**Pattern**: Ensure a field has a value
```
ISBLANK(Email)
```

**Use Case**: Email is required on Contact records
```
ISBLANK(Email)
```

### 2. Conditional Required Fields

**Pattern**: Field required based on another field value
```
AND(Status = "Closed", ISBLANK(CloseReason__c))
```

**Use Case**: Close Reason required when Status is Closed
```
AND(Status = "Closed", ISBLANK(CloseReason__c))
```

### 3. Field Format Validation

**Pattern**: Validate field format (email, phone, URL, etc.)
```
AND(
  NOT(ISBLANK(Email)),
  NOT(CONTAINS(Email, "@"))
)
```

**Use Case**: Email must contain @ symbol
```
AND(
  NOT(ISBLANK(Email)),
  NOT(CONTAINS(Email, "@"))
)
```

### 4. Range Validation

**Pattern**: Validate number or date is within range
```
OR(Amount < 0, Amount > 1000000)
```

**Use Case**: Amount must be between 0 and 1,000,000
```
OR(Amount < 0, Amount > 1000000)
```

### 5. Date Comparison Validation

**Pattern**: Validate date relationships
```
CloseDate < TODAY()
```

**Use Case**: Close Date cannot be in the past
```
CloseDate < TODAY()
```

### 6. Cross-Field Validation

**Pattern**: Validate relationship between multiple fields
```
AND(
  NOT(ISBLANK(StartDate__c)),
  NOT(ISBLANK(EndDate__c)),
  EndDate__c < StartDate__c
)
```

**Use Case**: End Date must be after Start Date
```
AND(
  NOT(ISBLANK(StartDate__c)),
  NOT(ISBLANK(EndDate__c)),
  EndDate__c < StartDate__c
)
```

### 7. Record Type Specific Validation

**Pattern**: Apply validation only to specific record types
```
AND(
  RecordType.Name = "Student",
  ISBLANK(StudentID__c)
)
```

**Use Case**: Student ID required for Student record type
```
AND(
  RecordType.Name = "Student",
  ISBLANK(StudentID__c)
)
```

### 8. Status Transition Validation

**Pattern**: Prevent invalid status transitions
```
AND(
  ISCHANGED(Status),
  PRIORVALUE(Status) = "Closed",
  Status <> "Closed"
)
```

**Use Case**: Cannot change status from Closed
```
AND(
  ISCHANGED(Status),
  PRIORVALUE(Status) = "Closed",
  Status <> "Closed"
)
```

### 9. Text Length Validation

**Pattern**: Validate text field length
```
LEN(Description) > 5000
```

**Use Case**: Description cannot exceed 5000 characters
```
LEN(Description) > 5000
```

### 10. Duplicate Prevention Patterns

**Pattern**: Prevent duplicate values (basic check)
```
AND(
  ISNEW(),
  AccountId IN $CustomObject__c.AccountId
)
```

**Note**: For robust duplicate prevention, use Duplicate Rules instead of validation rules.

## Use Cases by Domain

### Account/Contact Validation

**Email Format Validation**:
```
AND(
  NOT(ISBLANK(Email)),
  OR(
    NOT(CONTAINS(Email, "@")),
    NOT(CONTAINS(Email, ".")),
    LEN(Email) < 5
  )
)
```

**Phone Format Validation**:
```
AND(
  NOT(ISBLANK(Phone)),
  LEN(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(Phone, " ", ""), "-", ""), "(", ""), ")", "")) < 10
)
```

**Address Validation**:
```
AND(
  RecordType.Name = "Business",
  ISBLANK(BillingStreet)
)
```

### Opportunity Validation

**Amount Validation**:
```
Amount <= 0
```

**Close Date Validation**:
```
CloseDate < TODAY()
```

**Stage Transition Validation**:
```
AND(
  ISCHANGED(StageName),
  PRIORVALUE(StageName) = "Closed Won",
  StageName <> "Closed Won"
)
```

**Required Fields for Closed Opportunities**:
```
AND(
  StageName = "Closed Won",
  ISBLANK(CloseReason__c)
)
```

### Case Validation

**Status Transition Validation**:
```
AND(
  ISCHANGED(Status),
  PRIORVALUE(Status) = "Closed",
  Status <> "Closed"
)
```

**Priority Rules**:
```
AND(
  Priority = "High",
  ISBLANK(Description)
)
```

**SLA Validation**:
```
AND(
  Status = "New",
  CreatedDate < NOW() - (2/24)
)
```

### Custom Object Examples

**Education Cloud - Student Validation**:
```
AND(
  RecordType.Name = "Student",
  OR(
    ISBLANK(StudentID__c),
    ISBLANK(EnrollmentDate__c)
  )
)
```

**Public Sector - Compliance Validation**:
```
AND(
  RecordType.Name = "Public Record",
  ISBLANK(ComplianceDate__c),
  Status = "Active"
)
```

## Examples

### Example 1: Email Format Validation

**Use Case**: Ensure email addresses contain @ symbol and valid domain
**Formula**:
```
AND(
  NOT(ISBLANK(Email)),
  OR(
    NOT(CONTAINS(Email, "@")),
    LEN(LEFT(Email, FIND("@", Email) - 1)) < 1,
    LEN(RIGHT(Email, LEN(Email) - FIND("@", Email))) < 4
  )
)
```
**Error Message**: "Email address must be in a valid format (e.g., user@example.com)"
**When It Fires**: Insert, Update
**Explanation**: Checks that email contains @, has text before @, and has at least 4 characters after @ (domain + extension)

### Example 2: Phone Number Validation

**Use Case**: Validate phone number format (10-15 digits)
**Formula**:
```
AND(
  NOT(ISBLANK(Phone)),
  OR(
    LEN(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(Phone, " ", ""), "-", ""), "(", ""), ")", ""), ".", "")) < 10,
    LEN(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(Phone, " ", ""), "-", ""), "(", ""), ")", ""), ".", "")) > 15
  )
)
```
**Error Message**: "Phone number must contain 10-15 digits"
**When It Fires**: Insert, Update
**Explanation**: Removes common formatting characters and validates length

### Example 3: Conditional Required Field

**Use Case**: Close Reason required when Opportunity is Closed Won
**Formula**:
```
AND(
  StageName = "Closed Won",
  ISBLANK(CloseReason__c)
)
```
**Error Message**: "Close Reason is required when Opportunity is Closed Won"
**When It Fires**: Insert, Update
**Explanation**: Simple conditional check using AND

### Example 4: NPSP Donation Opportunity Validation

**Use Case**: Enforce Close Date and Amount when Opportunity Stage is "Posted" or "Closed Won" for donation Opportunities
**Formula**:
```
AND(
  RecordType.DeveloperName = "Donation",
  OR(
    StageName = "Posted",
    StageName = "Closed Won"
  ),
  OR(
    ISBLANK(CloseDate),
    Amount <= 0
  )
)
```
**Error Message**: "Close Date and Amount are required when Donation Opportunity is Posted or Closed Won"
**When It Fires**: Insert, Update
**Explanation**: Ensures donation Opportunities have required fields when moved to Posted or Closed Won stages

### Example 5: Date Range Validation

**Use Case**: Close Date must be within current fiscal year
**Formula**:
```
OR(
  CloseDate < DATE(YEAR(TODAY()), 1, 1),
  CloseDate > DATE(YEAR(TODAY()), 12, 31)
)
```
**Error Message**: "Close Date must be within the current calendar year"
**When It Fires**: Insert, Update
**Explanation**: Uses DATE function to create year boundaries

### Example 5: Number Range Validation

**Use Case**: Amount must be between $100 and $1,000,000
**Formula**:
```
OR(
  ISBLANK(Amount),
  Amount < 100,
  Amount > 1000000
)
```
**Error Message**: "Amount must be between $100 and $1,000,000"
**When It Fires**: Insert, Update
**Explanation**: Simple range check with OR condition

### Example 6: Status Transition Validation

**Use Case**: Cannot move from Closed Won to any other stage
**Formula**:
```
AND(
  ISCHANGED(StageName),
  PRIORVALUE(StageName) = "Closed Won",
  StageName <> "Closed Won"
)
```
**Error Message**: "Cannot change stage from Closed Won"
**When It Fires**: Update
**Explanation**: Uses ISCHANGED and PRIORVALUE to detect invalid transitions

### Example 7: Cross-Field Date Validation

**Use Case**: End Date must be after Start Date
**Formula**:
```
AND(
  NOT(ISBLANK(StartDate__c)),
  NOT(ISBLANK(EndDate__c)),
  EndDate__c <= StartDate__c
)
```
**Error Message**: "End Date must be after Start Date"
**When It Fires**: Insert, Update
**Explanation**: Validates relationship between two date fields

### Example 8: Record Type Specific Validation

**Use Case**: Student ID required for Student record type
**Formula**:
```
AND(
  RecordType.Name = "Student",
  ISBLANK(StudentID__c)
)
```
**Error Message**: "Student ID is required for Student records"
**When It Fires**: Insert, Update
**Explanation**: Combines record type check with required field validation

### Example 9: Text Length Validation

**Use Case**: Description cannot exceed 5000 characters
**Formula**:
```
LEN(Description) > 5000
```
**Error Message**: "Description cannot exceed 5000 characters"
**When It Fires**: Insert, Update
**Explanation**: Uses LEN function to check text length

### Example 10: URL Format Validation

**Use Case**: Website must start with http:// or https://
**Formula**:
```
AND(
  NOT(ISBLANK(Website)),
  AND(
    NOT(BEGINS(UPPER(Website), "HTTP://")),
    NOT(BEGINS(UPPER(Website), "HTTPS://"))
  )
)
```
**Error Message**: "Website must start with http:// or https://"
**When It Fires**: Insert, Update
**Explanation**: Uses BEGINS and UPPER to check URL format

### Example 11: Postal Code Validation (US)

**Use Case**: US Postal Code must be 5 digits or 5+4 format
**Formula**:
```
AND(
  BillingCountry = "United States",
  NOT(ISBLANK(BillingPostalCode)),
  OR(
    AND(
      LEN(BillingPostalCode) <> 5,
      LEN(BillingPostalCode) <> 10
    ),
    AND(
      LEN(BillingPostalCode) = 10,
      MID(BillingPostalCode, 6, 1) <> "-"
    )
  )
)
```
**Error Message**: "US Postal Code must be 5 digits or 5+4 format (12345-6789)"
**When It Fires**: Insert, Update
**Explanation**: Validates US postal code format with country check

### Example 12: Percentage Validation

**Use Case**: Percentage field must be between 0 and 100
**Formula**:
```
OR(
  ISBLANK(PercentComplete__c),
  PercentComplete__c < 0,
  PercentComplete__c > 100
)
```
**Error Message**: "Percentage must be between 0 and 100"
**When It Fires**: Insert, Update
**Explanation**: Simple range validation for percentage fields

### Example 13: Multi-Condition Validation

**Use Case**: Either Email or Phone required, but not both blank
**Formula**:
```
AND(
  ISBLANK(Email),
  ISBLANK(Phone)
)
```
**Error Message**: "Either Email or Phone is required"
**When It Fires**: Insert, Update
**Explanation**: Validates that at least one contact method is provided

### Example 14: Case-Insensitive Validation

**Use Case**: Status must be "Active" or "Inactive" (case-insensitive)
**Formula**:
```
AND(
  NOT(ISBLANK(Status__c)),
  AND(
    UPPER(Status__c) <> "ACTIVE",
    UPPER(Status__c) <> "INACTIVE"
  )
)
```
**Error Message**: "Status must be Active or Inactive"
**When It Fires**: Insert, Update
**Explanation**: Uses UPPER to make comparison case-insensitive

### Example 15: Cross-Object Validation

**Use Case**: Contact Email must match Account Domain
**Formula**:
```
AND(
  NOT(ISBLANK(Email)),
  NOT(ISBLANK(Account.Domain__c)),
  NOT(CONTAINS(Email, Account.Domain__c))
)
```
**Error Message**: "Contact email domain must match account domain"
**When It Fires**: Insert, Update
**Explanation**: Validates relationship between Contact and Account fields

### Example 16: Business Hours Validation

**Use Case**: Close Date cannot be on weekend
**Formula**:
```
OR(
  WEEKDAY(CloseDate) = 1,
  WEEKDAY(CloseDate) = 7
)
```
**Error Message**: "Close Date cannot be on a weekend"
**When It Fires**: Insert, Update
**Explanation**: Uses WEEKDAY function to check for Saturday (7) or Sunday (1)

### Example 17: Future Date Validation

**Use Case**: Start Date cannot be more than 1 year in the future
**Formula**:
```
StartDate__c > ADDMONTHS(TODAY(), 12)
```
**Error Message**: "Start Date cannot be more than 1 year in the future"
**When It Fires**: Insert, Update
**Explanation**: Uses ADDMONTHS to calculate future date boundary

## Best Practices

### Formula Design

**Keep Formulas Simple and Readable**:
- Break complex logic into multiple validation rules when possible
- Use formula fields to simplify validation rule expressions
- Add comments in formula field descriptions to document complex logic
- Avoid deeply nested IF statements (use CASE instead when possible)

**Example - Complex Logic Simplified**:
Instead of:
```
IF(Status = "A", IF(Amount > 100, IF(Type = "X", true, false), false), false)
```

Use:
```
AND(Status = "A", Amount > 100, Type = "X")
```

### Error Messages

**Use Clear, Actionable Error Messages**:
- Explain what's wrong and how to fix it
- Include field names and expected values
- Avoid technical jargon
- Provide examples when format is required

**Good Error Messages**:
- "Email address must be in a valid format (e.g., user@example.com)"
- "Close Date must be within the current calendar year"
- "Amount must be between $100 and $1,000,000"

**Poor Error Messages**:
- "Validation failed"
- "Invalid data"
- "Error"

### Performance

**Optimize Formula Complexity**:
- Avoid unnecessary cross-object references
- Use indexed fields in validation conditions when possible
- Test validation rules with bulk data operations
- Consider performance impact on save time

**Performance Considerations**:
- Cross-object references require additional queries
- Complex formulas with many functions can slow down save time
- Validation rules execute for every record in bulk operations
- Consider moving complex validations to Apex if performance is critical

### Testing

**Test Thoroughly**:
- Test with single record operations
- Test with bulk data operations (200+ records)
- Test edge cases (null values, empty strings, boundary values)
- Test with different user profiles and record types
- Test status transitions and field changes

**Test Scenarios**:
- Valid data should pass
- Invalid data should fail with clear error message
- Edge cases (null, empty, boundary values)
- Bulk operations (200+ records)
- Different record types
- Different user profiles

### Documentation

**Document Complex Formulas**:
- Add descriptions to validation rules explaining the business logic
- Use formula fields with descriptions to document complex calculations
- Maintain a validation rules inventory with business justifications
- Document any workarounds or limitations

### User Experience

**Consider User Experience**:
- Validate early (on field change when possible)
- Provide immediate feedback
- Use clear, actionable error messages
- Consider validation rule order (most common failures first)
- Test error message display in different contexts (UI, API, bulk)

### Maintainability

**Design for Maintainability**:
- Use consistent naming conventions
- Group related validation rules
- Document business rules and requirements
- Review and update validation rules regularly
- Remove obsolete validation rules

## Common Pitfalls

### Overly Complex Formulas

**Problem**: Formulas that are difficult to understand and maintain
**Solution**: Break complex logic into multiple validation rules or use formula fields to simplify expressions

**Example - Too Complex**:
```
IF(AND(Status = "A", Amount > 100), IF(OR(Type = "X", Type = "Y"), IF(NOT(ISBLANK(Description)), true, false), false), false)
```

**Better Approach**:
Create formula field `IsValidForProcessing__c`:
```
AND(Status = "A", Amount > 100, OR(Type = "X", Type = "Y"), NOT(ISBLANK(Description)))
```

Then validation rule:
```
NOT(IsValidForProcessing__c)
```

### Performance Issues with Cross-Object References

**Problem**: Excessive cross-object references slow down save operations
**Solution**: Minimize cross-object references, use formula fields to cache values, or move to Apex for complex validations

**Performance Impact**:
- Each cross-object reference requires a query
- Multiple cross-object references multiply query overhead
- Consider formula fields on the record to cache related values

### Not Handling Null Values

**Problem**: Formulas fail or behave unexpectedly with null values
**Solution**: Always use ISBLANK or ISNULL to check for null values before operations

**Example - Problematic**:
```
LEN(Description) > 100
```
This fails if Description is null.

**Fixed**:
```
AND(
  NOT(ISBLANK(Description)),
  LEN(Description) > 100
)
```

### Confusing Error Messages

**Problem**: Error messages don't clearly explain what's wrong or how to fix it
**Solution**: Write clear, actionable error messages with examples

**Poor Error Message**:
"Validation failed"

**Better Error Message**:
"Email address must be in a valid format (e.g., user@example.com)"

### Validation Rules That Block Legitimate Data

**Problem**: Overly restrictive validation rules prevent valid data entry
**Solution**: Test thoroughly with real-world scenarios, review validation rules regularly, provide bypass mechanisms for edge cases

**Common Issues**:
- Validation rules that are too strict
- Not accounting for all valid scenarios
- Blocking data migration or integration scenarios

### Not Testing with Bulk Operations

**Problem**: Validation rules work for single records but fail or perform poorly in bulk
**Solution**: Always test validation rules with bulk data operations (200+ records)

**Testing Checklist**:
- Test with Data Loader (200+ records)
- Test with API bulk operations
- Monitor performance and governor limits
- Verify error handling in bulk scenarios

### Circular Dependencies with Formula Fields

**Problem**: Validation rules reference formula fields that reference the same fields, causing circular logic
**Solution**: Avoid circular dependencies, use direct field references in validation rules when possible

**Example - Circular Dependency**:
- Validation rule checks `CalculatedField__c`
- `CalculatedField__c` is a formula that references `Amount`
- Validation rule also references `Amount`
- This can cause unexpected behavior

### Case Sensitivity Issues

**Problem**: Text comparisons fail due to case sensitivity
**Solution**: Use UPPER or LOWER functions for case-insensitive comparisons

**Example - Case Sensitive**:
```
Status = "closed"
```
This fails if Status is "Closed".

**Fixed**:
```
UPPER(Status) = "CLOSED"
```

## Performance Considerations

### Impact on Save Time

Validation rules execute synchronously during the save operation, directly impacting user experience. Complex formulas or multiple validation rules can significantly increase save time.

**Optimization Strategies**:
- Minimize formula complexity
- Reduce cross-object references
- Use indexed fields in conditions
- Test with realistic data volumes
- Consider moving complex validations to Apex

### Bulk Operation Performance

Validation rules execute for every record in bulk operations. With 200 records, each validation rule runs 200 times, multiplying the performance impact.

**Best Practices for Bulk Operations**:
- Test validation rules with bulk data (200+ records)
- Monitor performance in bulk scenarios
- Consider async validation for non-critical rules
- Use Apex for complex bulk validations

### Cross-Object Reference Performance

Each cross-object reference in a validation rule requires a query to the related object. Multiple cross-object references multiply the query overhead.

**Performance Impact**:
- Single cross-object reference: 1 additional query per record
- Multiple cross-object references: N additional queries per record
- In bulk operations: N queries × number of records

**Optimization**:
- Minimize cross-object references
- Use formula fields to cache related values
- Consider Apex for validations requiring multiple related records

### Formula Complexity Impact

Complex formulas with many functions, nested conditions, or calculations can slow down validation rule evaluation.

**Complexity Factors**:
- Number of functions used
- Nesting depth of conditions
- Number of field references
- Type of operations (text manipulation is slower than simple comparisons)

**When to Move to Apex**:
- Formulas exceed 5,000 characters
- More than 5 cross-object references
- Complex calculations or transformations
- Performance issues in production

## Troubleshooting

### Common Formula Errors

**Syntax Errors**:
- Missing parentheses
- Incorrect function names
- Wrong number of parameters
- Type mismatches

**Debugging Tips**:
- Use formula fields to test individual parts of complex formulas
- Check formula syntax in Setup → Object Manager → Fields
- Use the formula editor's syntax checker
- Test with sample data

### Testing Strategies

**Single Record Testing**:
- Test with valid data (should pass)
- Test with invalid data (should fail)
- Test edge cases (null, empty, boundary values)
- Test with different record types
- Test with different user profiles

**Bulk Testing**:
- Test with Data Loader (200+ records)
- Monitor performance metrics
- Verify error handling
- Check governor limit usage

### Debugging Techniques

**Formula Field Testing**:
Create a formula field with the same logic as your validation rule to test and debug:
1. Create formula field with validation logic
2. Test with sample data
3. Verify formula results
4. Copy formula to validation rule

**Incremental Testing**:
Break complex formulas into parts:
1. Test each part individually
2. Combine parts incrementally
3. Verify final result

**Error Message Testing**:
- Verify error messages display correctly
- Test in different contexts (UI, API, bulk)
- Check error message formatting
- Ensure error messages are actionable

### Bulk Operation Issues

**Common Issues**:
- Validation rules fail unexpectedly in bulk
- Performance degradation with large datasets
- Governor limit exceptions
- Inconsistent error reporting

**Solutions**:
- Test thoroughly with bulk data
- Optimize formula complexity
- Consider Apex for bulk validations
- Monitor performance metrics

## Q&A

### Q: When do validation rules execute in the order of execution?

**A**: **Custom validation rules** execute during step 4 of the order of execution, after system validation rules (step 3) and before-save flows/triggers have run. This allows validation rules to reference field values that may have been modified by before-save automation. **System validation rules** execute first (step 3), before any automation.

### Q: Can validation rules reference fields modified by before-save flows?

**A**: Yes, **custom validation rules execute after before-save flows**, so they can reference field values that were modified by before-save automation. System validation rules execute before automation and cannot reference modified values.

### Q: What's the difference between ISBLANK and ISNULL?

**A**: **ISBLANK** returns true for null values, empty strings, and whitespace-only strings. **ISNULL** returns true only for null values. For text fields, use ISBLANK. For number/date fields, both work similarly, but ISBLANK is more commonly used.

### Q: Can validation rules make callouts or query other records?

**A**: No, **validation rules cannot make callouts or perform SOQL queries**. They can only reference fields on the current record and related objects through relationship fields. For validations requiring queries or callouts, use Apex validation.

### Q: How do I validate against related records?

**A**: Validation rules can reference related object fields through relationship fields (e.g., `Account.Industry`), but they cannot query for related records. For complex validations requiring queries, use Apex validation in a trigger or before-save flow.

### Q: Can validation rules be bypassed?

**A**: **Standard users cannot bypass validation rules**. System administrators can temporarily deactivate validation rules, but this should only be done for data migration or maintenance scenarios. Validation rules enforce data quality and should not be bypassed in normal operations.

### Q: How many validation rules can I have per object?

**A**: There is **no hard limit on the number of validation rules per object**, but performance considerations apply. Each validation rule executes during save operations, so having many validation rules can impact save time. Best practice is to consolidate related validations when possible.

### Q: Can validation rules reference formula fields?

**A**: Yes, **validation rules can reference formula fields**, but be careful of circular dependencies. If a formula field references the same fields used in a validation rule, ensure the logic is consistent and doesn't create circular references.

### Q: How do I test validation rules?

**A**: Test validation rules with:
- Single record operations (valid and invalid data)
- Bulk data operations (200+ records)
- Edge cases (null values, empty strings, boundary values)
- Different record types and user profiles
- Status transitions and field changes

### Q: What's the performance impact of validation rules?

**A**: Validation rules execute synchronously and impact save time. Complex formulas, multiple validation rules, and cross-object references can significantly increase save time. Test with realistic data volumes and consider moving complex validations to Apex if performance is critical.

### Q: Can I use validation rules to set field values?

**A**: No, **validation rules cannot set field values**. They can only prevent records from being saved when validation fails. To set field values, use before-save flows, workflow rules (deprecated), or Apex triggers.

### Q: How do I handle validation rules in bulk operations?

**A**: Validation rules execute for every record in bulk operations. Test thoroughly with bulk data (200+ records), optimize formula complexity, and consider Apex for complex bulk validations. Monitor performance and governor limits in bulk scenarios.

### Q: Can validation rules reference $User or $Profile?

**A**: Yes, **validation rules can reference global variables** like `$User`, `$Profile`, `$Organization`, and `$Record`. These are useful for user-specific or profile-specific validations.

### Q: What's the difference between validation rules and duplicate rules?

**A**: **Validation rules** prevent records from being saved when they don't meet criteria. **Duplicate rules** identify and prevent duplicate records based on matching criteria. Use duplicate rules for duplicate prevention, not validation rules.

### Q: How do I debug a validation rule that's not working?

**A**: Debug validation rules by:
- Creating a formula field with the same logic to test
- Testing with sample data (valid and invalid)
- Checking formula syntax
- Verifying field references and types
- Testing with different record types and user profiles
- Using incremental testing for complex formulas

## Related Patterns

- <a href="{{ '/rag/development/order-of-execution.html' | relative_url }}">Order of Execution</a> - Understanding when validation rules execute in the transaction lifecycle
- <a href="{{ '/rag/development/flow-patterns.html' | relative_url }}">Flow Patterns</a> - When to use Flows vs Validation Rules for validation logic
- <a href="{{ '/rag/code-examples/utilities/validation-examples.html' | relative_url }}">Validation Examples</a> - Apex validation patterns for complex scenarios requiring queries or callouts
- <a href="{{ '/rag/data-governance/data-quality-stewardship.html' | relative_url }}">Data Quality Stewardship</a> - Data quality patterns and governance
- <a href="{{ '/rag/development/apex-patterns.html' | relative_url }}">Apex Patterns</a> - Apex validation patterns for complex business logic
- <a href="{{ '/rag/development/error-handling-and-logging.html' | relative_url }}">Error Handling and Logging</a> - Error handling patterns for validation failures
