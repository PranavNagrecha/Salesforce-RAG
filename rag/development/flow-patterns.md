# Flow Design and Orchestration Patterns

## Overview

Flow is used as the primary automation engine across projects, with Apex reserved for complex logic, integrations, and performance-critical scenarios. The approach emphasizes declarative automation where possible, with clear patterns for when to use different Flow types.

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

### Change Management

- Version control all Flows
- Test thoroughly before deployment
- Document purpose and business logic
- Coordinate changes with related automation

