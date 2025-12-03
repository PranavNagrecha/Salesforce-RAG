---
title: "Flow Design and Orchestration Patterns"
level: "Intermediate"
tags:
  - flow
  - development
  - patterns
  - automation
  - declarative
last_reviewed: "2025-01-XX"
---

# Flow Design and Orchestration Patterns

## Overview

Flow is used as the primary automation engine across projects, with Apex reserved for complex logic, integrations, and performance-critical scenarios. The approach emphasizes declarative automation where possible, with clear patterns for when to use different Flow types.

## Prerequisites

**Required Knowledge**:
- Understanding of Salesforce data model (objects, fields, relationships)
- Basic understanding of Salesforce automation concepts
- Familiarity with Salesforce security model (profiles, permission sets)

**Recommended Reading**:
- [Apex Patterns](development/apex-patterns.html) - Understanding when to use Apex vs Flow
- [Order of Execution](development/order-of-execution.html) - Understanding when Flows execute
- [Admin Basics](development/admin-basics.html) - Foundation Salesforce administration knowledge

## Flow Type Selection

### Record-Triggered Flows (RTF)

**Primary workhorse** for:

- Creating/updating related records
- Status transitions
- Notifications
- Simple cross-object logic

**When to use**: Most object automation needs

### Subflows

**Reusable logic chunks** for:

- Assignment rules
- Task creation
- Status updates
- Integration call wrappers

**When to use**: Logic that appears in multiple Flows

### Screen Flows

**Guided user interactions** for:

- Internal apps (advisors/staff)
- Portal UX (where standard layouts aren't enough)
- Guided data capture
- Step-by-step case/application handling

**When to use**: Multi-step user interactions requiring guidance

### Scheduled Flows

**Periodic operations** for:

- Periodic cleanup
- Data maintenance
- Batch operations
- Scheduled tasks

**When to use**: Time-based automation needs

### Auto-Launched Flows

**Reusable logic** for:

- Called from other Flows
- Called from Apex
- Reusable automation sequences

**When to use**: Logic that needs to be called from multiple contexts

## Record-Triggered Flow Structure

### Strict Entry Criteria

**Pattern**: Set entry conditions so only relevant records enter the Flow

- Avoid "run on every change, then decide inside the Flow"
- Use specific conditions (e.g., `Status` in ('X', 'Y') AND key fields not null)
- Reduces unnecessary Flow execution
- Improves performance

**Example**: Entry criteria like `Status` in ('Submitted', 'Under Review') AND `Application_Type__c` != null

### Separation of Concerns with Decision Nodes

**Pattern**: First node after start is usually a Decision that routes:

- "New vs Update" behavior
- "Channel or Source" variations (portal vs internal vs integration)
- "Person type" (student vs external partner vs staff) when needed
- Each branch focused on one coherent business path

**Benefits**: Clear separation, easier maintenance, better performance

### Subflows for Complex Tasks

**Pattern**: Extract logical chunks into Subflows such as:

- "Create Advisor Tasks"
- "Sync Application Status to Child Objects"
- "Build Notification Payload"

**Benefits**: 
- Easier testing
- Reuse across multiple triggers
- Smaller main Flow
- Better maintainability

### Minimal DML and Queries

**Pattern**: 

- Use fast field updates (before-save) when just updating the triggering record
- Aggregate logic to avoid multiple unnecessary updates
- Ask "Should this be in Apex instead?" if too complex

**Performance**: Reduces DML operations and improves execution time

## Screen Flow Design Patterns

### Step Structure

Clear stages:

- **Step 1**: Identify/lookup
- **Step 2**: Collect core information
- **Step 3**: Optional/extras
- **Step 4**: Confirmation/review

### Context Handling

- Prefer not asking users for IDs explicitly
- Use lookups or context from previous steps
- Pass context between steps using variables
- Reduce user input errors

### Validation

- Validate at each step before proceeding
- Provide clear error messages
- Enable users to correct errors
- Prevent invalid data entry

### Error Handling

- Clear error messages and recovery paths
- Handle validation failures gracefully
- Support user correction workflows
- Log errors for troubleshooting

## Flow + Apex Integration

### Flow Responsibilities

Flow handles:

- Straightforward decision trees
- Updates to related records
- Simple calculations
- UI orchestration (Screen Flows)
- Triggering Platform Events via standard actions

### Invocable Apex Responsibilities

Invocable Apex handles:

- Complex branching or state machines
- Heavy calculations
- Integration with external APIs needing complex authentication/error handling
- Multi-step operations requiring code reuse

### Flow → Apex → Flow Pattern

**Pattern**: 

1. Flow gathers context and calls Apex with clean request object
2. Apex does heavy lifting
3. Flow interprets result and handles user messages/logging/routing

**Benefits**: Best of both worlds - declarative orchestration with code power

## Flow Naming and Documentation

### Flow Naming Conventions

**Pattern**: Reflect object, trigger, and business purpose

- Examples: `App_AfterSave_ApplicationStatusOrchestration`, `Case_BeforeSave_Defaulting`
- Format: `Object_TriggerPoint_BusinessPurpose`
- Use PascalCase for clarity

### Element Naming

**Pattern**: Decision/Assignment/Update elements named by condition or action

- Good: `Decide_AdvisorAssignmentNeeded`, `Update_Application_ReadyForSIS`
- Bad: "Assignment 1/2/3"
- Use descriptive names that indicate purpose

### Descriptions and Annotations

- Flows and key elements include descriptions explaining purpose and business context
- Document business rules and logic
- Explain why decisions are made
- Help future maintainers understand intent

## Error Handling in Flows

### Fault Paths

- Implement fault paths for all integration calls and DML operations
- Provide clear error messages to users
- Log errors for troubleshooting
- Handle partial failures gracefully

### Error Messages

- User-friendly error messages
- Actionable guidance for users
- Clear indication of what went wrong
- Recovery suggestions when possible

### Error Logging

- Log all errors to custom logging object
- Include context about what failed
- Support troubleshooting workflows
- Enable error analysis and reporting

## Flow Performance

### Execution Time

- Monitor Flow execution time
- Identify slow elements
- Optimize queries and DML operations
- Consider Apex for performance-critical paths

### Element Count

- Monitor total element count
- Break complex Flows into Subflows
- Reduce unnecessary elements
- Optimize decision trees

### Query Optimization

- Avoid nested loops and excessive queries
- Use collection variables efficiently
- Consider bulkification when processing multiple records
- Profile Flows to identify performance bottlenecks

## Flow Change Management

### Version Control

- Version control Flows through source control
- Track changes over time
- Enable rollback if needed
- Document modifications

### Testing

- Test Flows thoroughly before deployment
- Test with realistic data volumes
- Test error scenarios
- User acceptance testing for Screen Flows

### Documentation

- Document Flow purpose and business logic
- Maintain change logs
- Document dependencies
- Create user guides for Screen Flows

### Coordination

- Review Flows regularly for optimization opportunities
- Coordinate Flow changes with related Apex and automation
- Update documentation when Flows change
- Communicate changes to stakeholders

## Flow User Permission Deprecation (Winter '26)

### Overview

The "Flow User" user permission is being deprecated in Winter '26 (2025). This affects how Flows execute and which users can run Flows.

### Migration Considerations

**Before Winter '26**:
- Users with Flow User permission could run Flows without object permissions
- This created security risks and bypassed proper access control

**After Winter '26**:
- Users must have appropriate object and field permissions to run Flows
- Flow User permission will no longer grant access to run Flows
- Flows will respect object-level and field-level security

**Migration Steps**:
1. Identify all users with Flow User permission
2. Review which Flows these users need to run
3. Grant appropriate object and field permissions via Permission Sets
4. Test Flows with new permissions before Winter '26
5. Remove Flow User permission after migration is complete
6. Document permission changes for audit purposes

**Best Practices**:
- Migrate before Winter '26 to avoid disruption
- Grant minimal permissions needed (principle of least privilege)
- Use Permission Sets (not Profiles) for access control
- Test thoroughly with different user types
- Document permission requirements for each Flow

### Deprecation Timeline

- **Winter '26 (2025)**: Flow User permission deprecated
- **Migration Required**: All orgs must migrate before Winter '26
- **Impact**: Flows will execute based on object and field permissions instead

### Migration Requirements

**Before Winter '26**:
1. Review all users with Flow User permission
2. Ensure users have appropriate object and field permissions
3. Test Flows with users who will lose Flow User permission
4. Update permission sets and profiles as needed
5. Document any changes required

**After Migration**:
- Flows execute based on object/field permissions
- Users need Read/Edit permissions on objects and fields used in Flows
- Flow execution context determines permissions

### Best Practices

1. **Audit Current Usage**: Identify all users with Flow User permission
2. **Review Flow Permissions**: Ensure Flows use appropriate object/field permissions
3. **Test Migration**: Test Flows with users who will lose Flow User permission
4. **Update Documentation**: Document permission requirements for Flows
5. **Plan Migration**: Create migration plan before Winter '26

### Permission Requirements

**For Flow Execution**:
- Users need Read/Edit permissions on objects used in Flows
- Users need Read/Edit permissions on fields used in Flows
- Flow execution context determines effective permissions
- System context may be required for certain operations

**For Screen Flows**:
- Users need appropriate object and field permissions
- Screen Flow visibility controlled by object permissions
- Field-level security applies to Flow fields


## Best Practices Summary

### Flow Type Selection

- Use Record-Triggered Flows for object automation
- Use Subflows for reusable logic
- Use Screen Flows for guided user interactions
- Use Scheduled Flows for periodic operations
- Use Auto-Launched Flows when called from other contexts

### Flow Design

- Set strict entry criteria
- Use Decision nodes early for routing
- Extract complex logic into Subflows
- Minimize DML operations
- Consider Apex if Flow becomes too complex

### Error Handling

- Implement fault paths for all operations
- Provide clear error messages
- Log errors for troubleshooting
- Handle partial failures gracefully

### Performance

- Monitor execution time and element count
- Optimize queries and DML
- Use collection variables efficiently
- Profile Flows to identify bottlenecks

## Q&A

### Q: When should I use Flow vs Apex for automation?

**A**: Use Flow as the default choice for most automation. Flow is declarative, easier to maintain, and sufficient for most business logic. Use Apex when you need complex logic Flow cannot handle, require tight control over governor limits, need heavy reuse across multiple contexts, or need to integrate with external APIs requiring complex authentication.

### Q: What is the difference between Record-Triggered Flow and Process Builder?

**A**: Record-Triggered Flows are the modern replacement for Process Builder. Process Builder is deprecated. Record-Triggered Flows run before or after save, support more complex logic, and provide better error handling. Migrate from Process Builder to Record-Triggered Flows.

### Q: Should I use before-save or after-save Record-Triggered Flows?

**A**: Use before-save flows when you need to modify field values on the same record, validate data, or prevent save operations. Use after-save flows when you need to create or update related records, send notifications, or perform operations that require the record to be saved first.

### Q: How do I handle errors in Flows?

**A**: Implement fault paths for all operations (DML, Apex calls, subflows). Provide clear, user-friendly error messages. Log errors to a logging service for troubleshooting. Handle partial failures gracefully by using decision elements to check operation results. Use try-catch patterns with fault connectors.

### Q: Can I call Apex from Flows?

**A**: Yes, use Invocable Apex methods (methods annotated with `@InvocableMethod`) to call Apex from Flows. This allows you to use complex Apex logic within Flow automation. Parameters must be lists (even for single values), and return values should also be lists.

### Q: How do I optimize Flow performance?

**A**: Set strict entry criteria to avoid unnecessary Flow execution. Use Decision nodes early for routing to reduce unnecessary element execution. Extract complex logic into Subflows for reuse and testing. Minimize DML operations by batching updates. Monitor execution time and element count. Profile Flows to identify bottlenecks.

### Q: What is the Flow User permission and why is it being deprecated?

**A**: The Flow User permission allowed users to run Flows without object permissions. It's being deprecated in Winter '26 because it created security risks. Users must now have appropriate object and field permissions to run Flows. Migrate users from Flow User permission to proper object permissions before Winter '26.

### Q: How do I test Flows?

**A**: Test Flows with bulk data (200+ records) to ensure bulkification works. Test both positive and negative scenarios. Test error handling by triggering fault paths. Use debug mode to step through Flow execution. Test with different user profiles to ensure proper permissions. Document test scenarios and results.

### Q: When should I use Screen Flows vs Record-Triggered Flows?

**A**: Use Screen Flows for guided user interactions, multi-step data capture, or when you need user input during a process. Use Record-Triggered Flows for automated processes that run when records are created or updated. Screen Flows are user-initiated; Record-Triggered Flows are system-initiated.

### Q: How do I handle bulk operations in Record-Triggered Flows?

**A**: Record-Triggered Flows automatically bulkify - they process all records in the trigger context. Use collection variables to store related records. Use loops to process collections. Avoid DML or SOQL inside loops. Design Flows to handle 200+ records efficiently.

## Related Patterns

**See Also**:
- [Apex Patterns](development/apex-patterns.html) - Understanding when to use Apex vs Flow
- [Order of Execution](development/order-of-execution.html) - Understanding when Flows execute in the save sequence
- [Error Handling and Logging](development/error-handling-and-logging.html) - Error handling patterns for Flow integration
- [Admin Basics](development/admin-basics.html) - Foundation Salesforce administration knowledge

**Related Domains**:
- [Testing Strategy](project-methods/testing-strategy.html) - Testing Flow automation
- [Code Examples](../code-examples/flow/) - Flow pattern examples (coming soon)

### Change Management

- Version control all Flows
- Test thoroughly before deployment
- Document purpose and business logic
- Coordinate changes with related automation

