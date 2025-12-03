# Flow Design and Orchestration Patterns

## What Was Actually Done

Flow is used as the primary automation engine across projects, with Apex reserved for complex logic, integrations, and performance-critical scenarios. The approach emphasizes declarative automation where possible, with clear patterns for when to use different Flow types.

### Flow Type Selection

Different Flow types are chosen based on specific use cases:

- **Record-Triggered Flows (RTF)**: Primary workhorse for creating/updating related records, status transitions, notifications, and simple cross-object logic
- **Subflows**: Reusable logic chunks for assignment rules, task creation, status updates, and integration call wrappers
- **Screen Flows**: Used in internal apps (advisors/staff) and occasionally in portal UX for guided data capture and step-by-step case/application handling
- **Scheduled Flows**: Periodic cleanup, data maintenance, and batch operations
- **Auto-Launched Flows**: Called from other Flows or Apex for reusable logic

### Record-Triggered Flow Structure

Record-triggered flows follow a consistent internal pattern:

1. **Strict entry criteria**: Avoid "run on every change, then decide inside the Flow." Set entry conditions so only relevant records enter the Flow (e.g., `Status` in ('X', 'Y') AND key fields not null)

2. **Separation of concerns with decision nodes**: First node after start is usually a Decision that routes:
   - "New vs Update" behavior
   - "Channel or Source" variations (portal vs internal vs integration)
   - "Person type" (student vs vendor vs staff) when needed
   - Each branch focused on one coherent business path

3. **Subflows for complex tasks**: Extract logical chunks into Subflows such as:
   - "Create Advisor Tasks"
   - "Sync Application Status to Child Objects"
   - "Build Notification Payload"
   - Benefits: easier testing, reuse across multiple triggers, smaller main Flow

4. **Minimal DML and queries**: Use fast field updates (before-save) when just updating the triggering record. Aggregate logic to avoid multiple unnecessary updates. Ask "Should this be in Apex instead?" if too complex

### Screen Flow Design Patterns

Screen flows are designed with clear stage structure:

- **Step structure**: Clear stages (Step 1: Identify/lookup, Step 2: Collect core information, Step 3: Optional/extras, Step 4: Confirmation/review)
- **Context handling**: Prefer not asking users for IDs explicitly; use lookups or context from previous steps
- **Validation**: Validate at each step before proceeding
- **Error handling**: Clear error messages and recovery paths

### Flow + Apex Integration

Flows and Apex are combined strategically:

- **Flow does**: Straightforward decision trees, updates to related records, simple calculations, UI orchestration (Screen Flows), triggering Platform Events via standard actions
- **Invocable Apex does**: Complex branching or state machines, heavy calculations, integration with external APIs needing complex authentication/error handling, multi-step operations requiring code reuse
- **Pattern: Flow → Apex → Flow**: Flow gathers context and calls Apex with clean request object; Apex does heavy lifting; Flow interprets result and handles user messages/logging/routing

### Flow Naming and Documentation

Consistent naming patterns are used:

- **Flow names**: Reflect object, trigger, and business purpose (e.g., `App_AfterSave_ApplicationStatusOrchestration`, `Case_BeforeSave_Defaulting`)
- **Element names**: Decision/Assignment/Update elements named by condition or action, not "Assignment 1/2/3" (e.g., `Decide_AdvisorAssignmentNeeded`, `Update_Application_ReadyForSIS`)
- **Descriptions and annotations**: Flows and key elements include descriptions explaining purpose and business context

## Rules and Patterns

### Flow Type Selection

- Use Record-Triggered Flows for object automation (create/update related records, status transitions, notifications)
- Use Subflows for reusable logic that appears in multiple Flows
- Use Screen Flows for guided user interactions in internal apps or portals
- Use Scheduled Flows for periodic batch operations and cleanup
- Use Auto-Launched Flows when called from other Flows or Apex

### Record-Triggered Flow Design

- Set strict entry criteria to avoid unnecessary Flow execution
- Use Decision nodes early to route by record state (New vs Update, channel, person type)
- Extract complex logic into Subflows for reuse and testability
- Minimize DML operations; use fast field updates when possible
- Consider Apex if Flow becomes too complex or performance-critical

### Error Handling in Flows

- Implement fault paths for all integration calls and DML operations
- Provide clear error messages to users
- Log errors for troubleshooting
- Handle partial failures gracefully
- Use try-catch patterns where appropriate

### Flow Performance

- Monitor Flow execution time and element count
- Avoid nested loops and excessive queries
- Use collection variables efficiently
- Consider bulkification when processing multiple records
- Profile Flows to identify performance bottlenecks

### Flow Change Management

- Version control Flows through source control
- Test Flows thoroughly before deployment
- Document Flow purpose and business logic
- Review Flows regularly for optimization opportunities
- Coordinate Flow changes with related Apex and automation

## Suggested Improvements (From AI)

### Flow Testing Framework

Implement comprehensive Flow testing:
- Unit tests for Subflows
- Integration tests for Record-Triggered Flows
- User acceptance testing for Screen Flows
- Automated regression testing
- Performance testing for high-volume scenarios

### Flow Monitoring and Observability

Enhance Flow observability:
- Custom objects to track Flow execution metrics
- Dashboard showing Flow performance and error rates
- Automated alerts for Flow failures
- Flow execution logs for troubleshooting
- Business metrics tracking through Flows

### Flow Documentation Standards

Establish Flow documentation standards:
- Template for Flow documentation
- Business logic documentation requirements
- Change log for Flow modifications
- Flow dependency mapping
- User guides for Screen Flows

## To Validate

- Specific Flow naming conventions and templates
- Exact entry criteria patterns used in Record-Triggered Flows
- Subflow structure and reuse patterns
- Flow performance benchmarks and optimization strategies
- Flow change management procedures

