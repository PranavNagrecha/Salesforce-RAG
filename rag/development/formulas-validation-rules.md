---
title: "Formulas, Validation Rules, and Custom Labels"
source: "The Salesforce Master Class wiki"
source_url: "https://github.com/Coding-With-The-Force/The-Salesforce-Master-Class/wiki"
topic: "Topic 2: The Complete Guide To Salesforce Administration"
section: "Formulas, Lookup Filters, Custom Labels, and Validation Rules"
level: "Intermediate"
tags:
  - salesforce
  - formulas
  - validation-rules
  - custom-labels
  - administration
last_reviewed: "2025-01-XX"
---

# Overview

Formulas, validation rules, and custom labels are powerful declarative tools for implementing business logic, data validation, and user interface customization in Salesforce. These tools enable administrators to enforce data quality, calculate values, and provide consistent messaging without custom code.

Formulas calculate values dynamically based on field values and expressions. Validation rules prevent invalid data from being saved. Custom labels provide translatable text for user interfaces and error messages. Lookup filters restrict related record selection based on criteria.

Understanding these tools enables administrators to implement complex business logic declaratively, reducing the need for custom development while maintaining data quality and user experience.

# Core Concepts

## Formula Fields

**What it is**: Read-only fields that automatically calculate values based on expressions using other field values, functions, and operators.

**Key characteristics**:
- Calculated automatically when record is saved or viewed
- Read-only (cannot be edited by users)
- Can reference other fields on the same record or related records
- Support various data types (Text, Number, Date, Checkbox, etc.)
- Can use functions, operators, and conditional logic

**Common use cases**:
- Calculate values from other fields (e.g., total amount, days since created)
- Concatenate text from multiple fields
- Format dates or numbers for display
- Conditional logic based on field values
- Cross-object formulas referencing related records

**Best practice**: Use formula fields for calculated values that should always be current and don't need user input. Consider performance impact for complex formulas or large data volumes.

## Validation Rules

**What it is**: Rules that prevent invalid data from being saved by evaluating conditions and displaying error messages when conditions are met.

**Key characteristics**:
- Execute before record is saved
- Prevent save operation when conditions are true
- Display custom error messages to users
- Can reference fields on the same record or related records
- Support complex logical expressions

**Common use cases**:
- Require fields based on other field values
- Enforce data format or range constraints
- Prevent invalid data combinations
- Enforce business rules
- Ensure data quality and consistency

**Best practice**: Use validation rules to enforce data quality and business rules. Keep error messages clear and actionable. Test validation rules thoroughly with different scenarios.

## Custom Labels

**What it is**: Translatable text values that can be referenced in formulas, validation rules, Visualforce, Lightning components, and other places.

**Key characteristics**:
- Stored centrally and referenced by name
- Translatable for multi-language support
- Can be used in formulas, validation rules, code, and UI
- Updated in one place affects all references
- Support text substitution with variables

**Common use cases**:
- Error messages in validation rules
- User-facing text in formulas
- Multi-language support
- Consistent messaging across the org
- Text that may change or need translation

**Best practice**: Use custom labels for user-facing text that may need translation or central management. Reference custom labels in validation rules and formulas for consistent messaging.

## Lookup Filters

**What it is**: Filters applied to lookup and master-detail relationship fields that restrict which related records can be selected.

**Key characteristics**:
- Applied when users select related records
- Filter records based on field values
- Support multiple filter conditions
- Can use AND/OR logic
- Improve data quality by restricting selection

**Common use cases**:
- Restrict related records by status
- Filter by record type
- Restrict based on other field values
- Ensure valid relationships
- Improve user experience by showing only relevant records

**Best practice**: Use lookup filters to improve data quality and user experience. Filter related records to show only valid options. Test lookup filters with different user profiles and record types.

# Deep-Dive Patterns & Best Practices

## Formula Field Patterns

**Pattern 1 - Calculated Values**:
Calculate values from other fields (e.g., total amount, percentage, days difference).

**Example**: `Amount__c * Quantity__c` calculates total from amount and quantity.

**Pattern 2 - Conditional Logic**:
Use IF, CASE, or logical operators for conditional calculations.

**Example**: `IF(Status__c = "Active", "Current", "Inactive")` returns different values based on status.

**Pattern 3 - Text Concatenation**:
Combine text from multiple fields for display.

**Example**: `FirstName__c & " " & LastName__c` combines first and last name.

**Pattern 4 - Cross-Object Formulas**:
Reference fields from related records using relationship names.

**Example**: `Account__r.Industry__c` references Industry field from related Account.

**Best practice**: Keep formulas simple and readable. Use formula fields for calculated values that should always be current. Consider performance for complex formulas or large data volumes.

## Validation Rule Patterns

**Pattern 1 - Required Field Validation**:
Require fields based on other field values.

**Example**: `AND(RecordType.DeveloperName = "High_Priority", ISBLANK(Priority_Reason__c))` requires Priority Reason for high priority records.

**Pattern 2 - Data Format Validation**:
Enforce data format or range constraints.

**Example**: `OR(LEN(Phone__c) < 10, LEN(Phone__c) > 15)` ensures phone number length is valid.

**Pattern 3 - Business Rule Validation**:
Enforce business rules and data combinations.

**Example**: `AND(Status__c = "Closed", ISBLANK(Closed_Date__c))` requires Closed Date when status is Closed.

**Pattern 4 - Cross-Object Validation**:
Validate based on related record values.

**Example**: `AND(Account__r.Status__c = "Inactive", Status__c = "Active")` prevents active records for inactive accounts.

**Best practice**: Keep validation rules focused and clear. Use custom labels for error messages. Test validation rules with different scenarios. Document business rules enforced by validation rules.

## Custom Label Patterns

**Pattern 1 - Error Messages**:
Use custom labels for validation rule error messages.

**Example**: Reference `$Label.Validation_Error_Required_Field` in validation rule error message.

**Pattern 2 - User-Facing Text**:
Use custom labels for text displayed to users in formulas or UI.

**Example**: Reference `$Label.Welcome_Message` in formula or component.

**Pattern 3 - Multi-Language Support**:
Use custom labels for translatable text.

**Example**: Create custom labels for each language, reference in formulas or UI.

**Best practice**: Use custom labels for all user-facing text that may need translation or central management. Reference custom labels consistently across the org.

## Lookup Filter Patterns

**Pattern 1 - Status-Based Filtering**:
Filter related records by status.

**Example**: Filter Opportunities to show only "Open" opportunities when selecting from Case.

**Pattern 2 - Record Type Filtering**:
Filter related records by record type.

**Example**: Filter Accounts to show only "Customer" record type accounts.

**Pattern 3 - Multi-Condition Filtering**:
Use multiple filter conditions with AND/OR logic.

**Example**: Filter Contacts where `(Status = "Active" AND Department = "Sales") OR (Status = "Active" AND Department = "Marketing")`.

**Best practice**: Use lookup filters to improve data quality and user experience. Filter to show only valid and relevant records. Test lookup filters with different user profiles.

# Implementation Guide

## Formula Field Creation Process

1. **Identify calculation need**: Determine what value needs to be calculated
2. **Identify source fields**: Identify fields needed for calculation
3. **Design formula expression**: Design formula using functions and operators
4. **Create formula field**: Create field with formula return type
5. **Write formula expression**: Write formula in formula editor
6. **Test formula**: Test with sample data
7. **Deploy and verify**: Deploy to production and verify calculation

## Validation Rule Creation Process

1. **Identify validation need**: Determine what data should be prevented
2. **Design validation condition**: Design condition that identifies invalid data
3. **Create validation rule**: Create rule with condition and error message
4. **Write error message**: Write clear, actionable error message (use custom labels)
5. **Test validation rule**: Test with valid and invalid data scenarios
6. **Deploy and verify**: Deploy to production and verify validation

## Custom Label Creation Process

1. **Identify text need**: Determine text that needs central management or translation
2. **Create custom label**: Create label with name and value
3. **Reference in formulas/rules**: Reference custom label in formulas, validation rules, or code
4. **Translate if needed**: Create translations for multi-language support
5. **Test references**: Test that references work correctly

## Lookup Filter Creation Process

1. **Identify filtering need**: Determine which related records should be available
2. **Design filter conditions**: Design conditions that identify valid records
3. **Create lookup filter**: Create filter on lookup or master-detail field
4. **Configure filter conditions**: Configure filter with field, operator, and value
5. **Test filter**: Test with different scenarios and user profiles
6. **Deploy and verify**: Deploy to production and verify filtering

## Prerequisites

- System Administrator or appropriate permissions
- Understanding of business rules and data requirements
- Understanding of formula syntax and functions
- Understanding of validation rule logic
- Understanding of lookup relationships

## Key Configuration Decisions

**Formula decisions**:
- What value needs to be calculated?
- Which fields are needed for calculation?
- What formula expression calculates the value?
- What data type should the formula return?

**Validation decisions**:
- What data should be prevented?
- What condition identifies invalid data?
- What error message should be displayed?
- Should error message use custom labels?

**Lookup filter decisions**:
- Which related records should be available?
- What conditions identify valid records?
- Should filter use AND or OR logic?
- How should filter work with different user profiles?

## Validation & Testing

**Formula testing**:
- Test with various field value combinations
- Test with null/blank values
- Test with related record scenarios
- Verify calculation accuracy
- Test performance with large data volumes

**Validation rule testing**:
- Test with valid data (should save successfully)
- Test with invalid data (should prevent save with error)
- Test with different user profiles
- Test with different record types
- Test edge cases and boundary conditions

**Lookup filter testing**:
- Test with different filter conditions
- Test with different user profiles
- Test with different record types
- Verify only valid records appear
- Test filter performance

**Tools to use**:
- Formula editor for formula creation and testing
- Validation rule editor for rule creation
- Custom label management in Setup
- Lookup filter configuration in field setup
- Test records for validation and testing

# Common Pitfalls & Anti-Patterns

## Over-Complex Formulas

**Bad pattern**: Creating very complex formulas that are difficult to understand, maintain, or debug.

**Why it's bad**: Complex formulas are error-prone, difficult to maintain, and may impact performance. They're hard for other administrators to understand or modify.

**Better approach**: Keep formulas simple and readable. Break complex calculations into multiple formula fields if needed. Consider custom development for very complex logic.

## Validation Rules That Block Valid Data

**Bad pattern**: Creating validation rules that are too restrictive, blocking valid business scenarios.

**Why it's bad**: Prevents users from entering valid data, causing frustration and workarounds. May require frequent exceptions or rule modifications.

**Better approach**: Test validation rules thoroughly with real business scenarios. Ensure rules allow all valid data while preventing invalid data. Review rules with business stakeholders.

## Not Using Custom Labels

**Bad pattern**: Hardcoding text in validation rules, formulas, or UI instead of using custom labels.

**Why it's bad**: Makes translation difficult, requires updates in multiple places, and reduces consistency.

**Better approach**: Use custom labels for all user-facing text. Reference custom labels in validation rules, formulas, and UI. Enables translation and central management.

## Lookup Filters That Are Too Restrictive

**Bad pattern**: Creating lookup filters that are too restrictive, preventing users from selecting valid related records.

**Why it's bad**: Prevents users from creating valid relationships, causing frustration and data quality issues.

**Better approach**: Test lookup filters with real business scenarios. Ensure filters allow all valid relationships while preventing invalid ones. Review filters with users.

## Not Testing Thoroughly

**Bad pattern**: Deploying formulas, validation rules, or lookup filters without thorough testing.

**Why it's bad**: May cause data issues, user frustration, or production problems. Fixing issues in production is more difficult and disruptive.

**Better approach**: Test thoroughly in sandbox before deployment. Test with various scenarios, user profiles, and record types. Involve business users in testing.

# Real-World Scenarios

## Scenario 1 - Calculated Total Field

**Problem**: Need to calculate total amount from quantity and unit price fields, displaying total on record.

**Context**: Custom object with Quantity and Unit Price fields, need Total Amount calculated automatically.

**Solution**: Create formula field `Total_Amount__c` with formula `Quantity__c * Unit_Price__c`. Formula automatically calculates when record is saved or viewed.

**Key decisions**: Use formula field for calculated value. Formula is read-only and always current. Consider rounding or currency formatting if needed.

## Scenario 2 - Required Field Based on Status

**Problem**: Need to require Priority Reason field when Case Status is "High Priority".

**Context**: Case object with Status and Priority Reason fields. Business rule requires Priority Reason for high priority cases.

**Solution**: Create validation rule with condition `AND(Status__c = "High Priority", ISBLANK(Priority_Reason__c))` and error message using custom label.

**Key decisions**: Use validation rule to enforce business rule. Use custom label for error message. Test with different status values.

## Scenario 3 - Filtered Lookup for Related Records

**Problem**: Need to restrict Opportunity selection on Case to only open opportunities for the related account.

**Context**: Case object with lookup to Opportunity. Business rule: Cases should only reference open opportunities for the account.

**Solution**: Create lookup filter on Opportunity lookup field with conditions `Account__c = $Account.Id AND IsClosed = false`.

**Key decisions**: Use lookup filter to restrict selection. Filter ensures only valid opportunities can be selected. Test with different account and opportunity scenarios.

# Checklist / Mental Model

## Formula, Validation, and Lookup Filter Checklist

When creating formulas, validation rules, or lookup filters:

1. **Identify need**: What calculation, validation, or filtering is needed?
2. **Design solution**: Design formula expression, validation condition, or filter criteria
3. **Create and configure**: Create field, rule, or filter with appropriate configuration
4. **Test thoroughly**: Test with various scenarios, user profiles, and data combinations
5. **Document purpose**: Document business rule or calculation purpose
6. **Deploy carefully**: Deploy to production after thorough testing
7. **Monitor and maintain**: Monitor usage and maintain as business rules evolve

## Formula and Validation Mental Model

**Use formulas for calculations**: Use formula fields for values that should be calculated automatically and always current. Keep formulas simple and readable.

**Use validation rules for data quality**: Use validation rules to enforce data quality and business rules. Keep error messages clear and actionable.

**Use custom labels for text**: Use custom labels for all user-facing text that may need translation or central management.

**Use lookup filters for data quality**: Use lookup filters to improve data quality and user experience by restricting related record selection.

**Test thoroughly**: Always test formulas, validation rules, and lookup filters thoroughly before deployment. Test with real business scenarios.

# Key Terms & Definitions

- **Formula Field**: Read-only field that automatically calculates values based on expressions
- **Validation Rule**: Rule that prevents invalid data from being saved by evaluating conditions
- **Custom Label**: Translatable text value that can be referenced in formulas, validation rules, and UI
- **Lookup Filter**: Filter applied to lookup fields that restricts which related records can be selected
- **Formula Expression**: Expression using fields, functions, and operators to calculate a value
- **Validation Condition**: Condition that identifies invalid data when true
- **Error Message**: Message displayed to users when validation rule prevents save
- **Cross-Object Formula**: Formula that references fields from related records
- **Cross-Object Validation**: Validation rule that references fields from related records

# RAG-Friendly Q&A Seeds

**Q:** When should I use a formula field vs. a regular field?

**A:** Use formula fields for values that should be calculated automatically and always current (e.g., total amount, days since created, formatted display values). Use regular fields for values that users need to enter or edit. Formula fields are read-only and calculated automatically; regular fields can be edited by users.

**Q:** How do I create a validation rule that requires a field based on another field value?

**A:** Create a validation rule with condition that checks both the trigger field and the required field. Example: `AND(Status__c = "High Priority", ISBLANK(Priority_Reason__c))` requires Priority Reason when Status is High Priority. Use ISBLANK() to check if field is empty. Use AND() to combine conditions.

**Q:** What's the difference between a validation rule and a required field?

**A:** A required field always requires a value regardless of other conditions. A validation rule can require a field conditionally based on other field values. Use required fields for fields that always need values. Use validation rules for conditional requirements or complex business rules.

**Q:** How do I use custom labels in validation rules?

**A:** Reference custom labels in validation rule error messages using `$Label.Custom_Label_Name`. Create custom label first, then reference in validation rule. Custom labels enable translation and central text management.

**Q:** How do lookup filters work?

**A:** Lookup filters restrict which related records can be selected when users choose values for lookup or master-detail fields. Filters evaluate conditions (field values, record types, etc.) and show only records that meet the criteria. Filters improve data quality by preventing invalid relationships.

**Q:** Can I use formulas in validation rules?

**A:** Yes, validation rules use the same formula syntax as formula fields. You can use functions, operators, and field references in validation rule conditions. Validation rules return true/false (prevent save when true), while formula fields return calculated values.

**Q:** How do I test validation rules before deploying?

**A:** Test validation rules by: (1) Creating test records with valid data (should save successfully), (2) Creating test records with invalid data (should prevent save with error), (3) Testing with different user profiles, (4) Testing with different record types, (5) Testing edge cases and boundary conditions. Always test in sandbox before production deployment.

## Related Patterns

**See Also**:
- [Flow Patterns](flow-patterns.html) - Automation patterns for business logic
- [Admin Basics](admin-basics.html) - Declarative configuration patterns
- [Error Handling and Logging](error-handling-and-logging.html) - Error handling in validation rules

**Related Domains**:
- [Object Setup and Configuration](../data-modeling/object-setup-and-configuration.html) - Field and object configuration
- [Validation Examples](../code-examples/utilities/validation-examples.html) - Validation code examples

