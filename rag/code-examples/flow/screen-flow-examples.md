# Screen Flow Code Examples

> This file contains complete, working examples for Screen Flow patterns.
> All examples demonstrate user interaction patterns in Screen Flows.

## Overview

Screen Flows provide guided user interactions for multi-step processes. These examples demonstrate common patterns for data collection, decision-making, and record creation.

**Related Patterns**:
- [Flow Patterns](../development/flow-patterns.md) - Complete Flow development patterns

## Examples

### Example 1: Multi-Step Data Collection

**Pattern**: Collecting data across multiple screens
**Use Case**: Guided data entry for complex processes
**Complexity**: Basic
**Related Patterns**: [Flow Patterns](../development/flow-patterns.md#screen-flow-design-patterns)

**Problem**:
You need to guide users through a multi-step data collection process.

**Solution**:

**Flow Structure**:
1. **Screen 1**: Collect Contact Information
   - First Name (Text Input)
   - Last Name (Text Input)
   - Email (Email Input)
   - Next Button

2. **Screen 2**: Collect Additional Information
   - Phone (Phone Input)
   - Company (Text Input)
   - Industry (Picklist)
   - Previous Button, Next Button

3. **Screen 3**: Review and Confirm
   - Display all collected values
   - Back Button, Submit Button

4. **Create Records**: Create Contact with collected data

**Best Practices**:
- Break complex forms into logical steps
- Provide navigation (Previous/Next buttons)
- Validate input at each step
- Show progress indicator
- Provide review screen before submission

### Example 2: Conditional Screen Navigation

**Pattern**: Showing different screens based on user input
**Use Case**: Dynamic flow paths based on decisions
**Complexity**: Intermediate
**Related Patterns**: [Flow Patterns](../development/flow-patterns.md)

**Problem**:
You need to show different screens based on user selections.

**Solution**:

**Flow Structure**:
1. **Screen 1**: Select Record Type
   - Record Type (Picklist: 'Student', 'Applicant', 'Alumni')
   - Next Button

2. **Decision**: Route based on Record Type
   - Outcome 1: 'Student' → Screen 2A (Student Information)
   - Outcome 2: 'Applicant' → Screen 2B (Application Information)
   - Outcome 3: 'Alumni' → Screen 2C (Alumni Information)

3. **Screen 2A/2B/2C**: Collect type-specific information

4. **Create Records**: Create Contact with appropriate Record Type

**Best Practices**:
- Use Decision elements to route users
- Keep screen count manageable (3-7 screens typically)
- Provide clear navigation options
- Validate required fields before proceeding

## Related Examples

- [Record-Triggered Examples](flow/record-triggered-examples.md) - Automated flow patterns
- [Subflow Examples](flow/subflow-examples.md) - Reusable subflow patterns

## See Also

- [Flow Patterns](../development/flow-patterns.md) - Complete Flow development patterns

