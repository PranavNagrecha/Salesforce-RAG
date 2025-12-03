# Subflow Code Examples

> This file contains complete, working examples for Subflow patterns.
> All examples demonstrate reusable subflow patterns.

## Overview

Subflows are reusable Flow components that can be called from other Flows. These examples demonstrate common subflow patterns for reusable logic.

**Related Patterns**:
- [Flow Patterns](../development/flow-patterns.md) - Complete Flow development patterns

## Examples

### Example 1: Task Creation Subflow

**Pattern**: Reusable task creation logic
**Use Case**: Creating tasks from multiple parent Flows
**Complexity**: Basic
**Related Patterns**: [Flow Patterns](../development/flow-patterns.md#subflows-for-complex-tasks)

**Problem**:
You need to create tasks from multiple different Flows with consistent logic.

**Solution**:

**Subflow Configuration**:
- **Flow Type**: Subflow
- **Input Variables**:
  - `ParentRecordId` (Text, Required)
  - `TaskSubject` (Text, Required)
  - `TaskPriority` (Text, Default: 'Normal')
  - `TaskOwnerId` (Text, Optional)

**Subflow Elements**:
1. **Start** - Receives input variables
2. **Assignment** - Set Task fields:
   - `WhatId` = `{!ParentRecordId}`
   - `Subject` = `{!TaskSubject}`
   - `Priority` = `{!TaskPriority}`
   - `OwnerId` = `{!TaskOwnerId}` (if provided)
   - `Status` = `'Not Started'`
3. **Create Records** - Create Task
4. **End** - Return Task ID (output variable)

**Usage in Parent Flow**:
- Call Subflow: "Create Task"
- Pass input variables
- Receive Task ID output variable

**Best Practices**:
- Use descriptive input/output variable names
- Document subflow purpose and usage
- Handle optional parameters gracefully
- Return useful output variables

### Example 2: Notification Subflow

**Pattern**: Reusable notification logic
**Use Case**: Sending notifications from multiple Flows
**Complexity**: Intermediate
**Related Patterns**: [Flow Patterns](../development/flow-patterns.md)

**Problem**:
You need to send notifications from multiple Flows with consistent formatting.

**Solution**:

**Subflow Configuration**:
- **Flow Type**: Subflow
- **Input Variables**:
  - `RecipientIds` (Text Collection, Required)
  - `NotificationTitle` (Text, Required)
  - `NotificationBody` (Text, Required)
  - `RelatedRecordId` (Text, Optional)

**Subflow Elements**:
1. **Start** - Receives input variables
2. **Loop** - Loop through `RecipientIds`
3. **Create Records** - Create Custom Notification for each recipient
4. **End** - Return success status

**Best Practices**:
- Process collections in loops
- Handle empty collections gracefully
- Provide meaningful output variables
- Document subflow behavior

## Related Examples

- [Record-Triggered Examples](flow/record-triggered-examples.md) - Automated flow patterns
- [Screen Flow Examples](flow/screen-flow-examples.md) - User interaction flows

## See Also

- [Flow Patterns](../development/flow-patterns.md) - Complete Flow development patterns

