---
title: "OmniStudio Patterns"
level: "Intermediate"
tags:
  - omnistudio
  - development
  - patterns
  - omniscripts
  - flexcards
last_reviewed: "2025-01-XX"
---

# OmniStudio Patterns

## Overview

OmniStudio (OmniScripts and FlexCards) provides guided workflows and reusable UI components for complex business processes. Used in higher education and public sector contexts to guide users through applications, grant workflows, and other multi-step processes.

## Prerequisites

**Required Knowledge**:
- Understanding of Salesforce declarative automation
- Knowledge of Flow concepts (⚠️ **Note**: Process Builder is deprecated, use Record-Triggered Flows instead)
- Understanding of data transformation and validation
- Familiarity with Experience Cloud (for portal implementations)

**Recommended Reading**:
- <a href="{{ '/rag/development/development/flow-patterns.html' | relative_url }}">Flow Patterns</a> - Flow automation patterns
- <a href="{{ '/rag/development/architecture/portal-architecture.html' | relative_url }}">Portal Architecture</a> - Experience Cloud patterns
- <a href="{{ '/rag/development/development/lwc-patterns.html' | relative_url }}">LWC Patterns</a> - Lightning Web Component patterns

## OmniScripts for Guided Processes

### Purpose

OmniScripts guide users through complex processes:

- Application submission workflows
- Grant application and approval processes
- Multi-step data collection
- Guided forms with business rule enforcement
- Step-by-step workflows for both internal staff and portal users

### Design Patterns

**Clear Step Progression**:
- Design OmniScripts with clear step progression
- Each step has a specific purpose
- Guide users through complex processes
- Provide clear navigation and progress indicators

**Data Raptors for Transformation**:
- Use data raptors for data transformation
- Transform data between steps
- Validate data at each step
- Support complex data mappings

**Validation at Each Step**:
- Implement validation at each step
- Provide immediate feedback
- Prevent invalid data entry
- Guide users to correct errors

**Error Handling**:
- Provide clear error messages and recovery paths
- Handle validation failures gracefully
- Support user correction workflows
- Log errors for troubleshooting

**User Experience**:
- Support both internal and portal user experiences
- Responsive design for mobile and desktop
- Clear guidance and help text
- Progress indicators and navigation

## FlexCards for Reusable UI Components

### Purpose

FlexCards provide structured, reusable UI components:

- Display aggregated data from multiple sources
- Show at-a-glance information for records
- Support responsive design for mobile and desktop
- Integrate with OmniScripts for complete user experiences

### Design Patterns

**Reusability**:
- Design FlexCards for reusability across multiple contexts
- Use data raptors to aggregate data from multiple sources
- Support configuration-driven display
- Enable reuse across different record types

**Data Aggregation**:
- Use data raptors to aggregate data from multiple sources
- Combine data from related records
- Support complex data relationships
- Enable efficient data loading

**Responsive Design**:
- Support responsive design for different screen sizes
- Mobile-first approach
- Flexible layouts
- Touch-friendly interfaces

**Integration**:
- Integrate with OmniScripts for complete workflows
- Support standalone display
- Enable interaction with Salesforce data
- Support real-time updates

## Grant Management Workflows

### Application Workflows

**Guided Grant Applications**:
- Step-by-step grant application processes
- Data collection and validation for grant requirements
- Integration with Salesforce data model for grant tracking
- Support for complex grant eligibility rules

### Approval Workflows

**Grant Approval Processes**:
- Step-by-step grant approval processes
- Workflow routing based on grant type and amount
- Approval tracking and history
- Integration with notification systems

### Data Integration

**Salesforce Integration**:
- Integration with Salesforce data model for grant tracking
- Link grants to students, programs, and accounts
- Support grant history and reporting
- Enable grant management workflows

## Integration Patterns

### Salesforce Data Model Integration

**Pattern**: Integrate OmniStudio with Salesforce data model

**Implementation**:
- Use data raptors for complex data transformations
- Support both real-time and batch data updates
- Handle errors gracefully with user-friendly messages
- Log OmniStudio actions for audit purposes

### Data Raptor Usage

**Pattern**: Use data raptors for data transformation

**Implementation**:
- Transform data between OmniScript steps
- Aggregate data from multiple sources for FlexCards
- Support complex data mappings
- Enable efficient data loading

### Error Handling

**Pattern**: Handle errors gracefully

**Implementation**:
- Provide user-friendly error messages
- Support error recovery workflows
- Log errors for troubleshooting
- Handle integration failures gracefully

## Performance Optimization

### Data Raptor Optimization

**Pattern**: Optimize data raptor queries for performance

**Implementation**:
- Minimize data raptor queries
- Use selective queries with proper filters
- Cache data when appropriate
- Monitor data raptor performance

### Server Round Trips

**Pattern**: Minimize server round trips

**Implementation**:
- Batch operations when possible
- Use data raptors efficiently
- Cache data in component state
- Reduce unnecessary API calls

### Async Processing

**Pattern**: Use async processing for heavy operations

**Implementation**:
- Defer heavy calculations to async jobs
- Use background processing for large data sets
- Support progress indicators for long operations
- Enable cancellation of long-running operations

### Performance Monitoring

**Pattern**: Monitor OmniStudio performance metrics

**Implementation**:
- Track OmniScript execution time
- Monitor FlexCard load times
- Identify performance bottlenecks
- Optimize based on performance data

## Best Practices

### OmniScript Design

- Design OmniScripts with clear step progression
- Use data raptors for data transformation
- Implement validation at each step
- Provide clear error messages and recovery paths
- Support both internal and portal user experiences

### FlexCard Design

- Design FlexCards for reusability across multiple contexts
- Use data raptors to aggregate data from multiple sources
- Support responsive design for different screen sizes
- Integrate with OmniScripts for complete workflows
- Follow design system guidelines for consistency

### Integration Patterns

- Integrate OmniStudio with Salesforce data model
- Use data raptors for complex data transformations
- Support both real-time and batch data updates
- Handle errors gracefully with user-friendly messages
- Log OmniStudio actions for audit purposes

### Performance Optimization

- Optimize data raptor queries for performance
- Minimize server round trips
- Cache data when appropriate
- Use async processing for heavy operations
- Monitor OmniStudio performance metrics

## Configuration Management

### Hardcoded Values

**Standard**: NO hardcoded values (IDs, counts, URLs, etc.)

**Implementation**:
- Use Custom Metadata or Custom Settings
- All URLs must use Named Credentials or Custom Metadata
- Environment-specific configuration
- Runtime configuration changes

### Component Status

**Standard**: ALL components MUST have meaningful descriptions

**Implementation**:
- NO test/dummy components in production
- Follow PascalCase naming convention
- Add timeout settings to HTTP actions
- Remove hardcoded test data

## Error Handling Standards

### Error States

**Standard**: Add error states to Flex Cards

**Implementation**:
- Return error data in response
- Display error messages to users
- Support error recovery workflows
- Log errors for troubleshooting

### Integration Procedure Errors

**Standard**: Integration Procedures must show error messages to users when APIs fail

**Implementation**:
- Set `failOnStepError: true` for critical steps
- Provide user-friendly error messages
- Log errors for troubleshooting
- Support error recovery

## Best Practices Summary

### OmniScript Design

- Clear step progression
- Data raptors for transformation
- Validation at each step
- Error handling and recovery
- User experience optimization

### FlexCard Design

- Reusability across contexts
- Data aggregation from multiple sources
- Responsive design
- Integration with OmniScripts
- Design system consistency

### Integration

- Salesforce data model integration
- Data raptor usage for transformations
- Error handling
- Performance optimization
- Monitoring and observability

### Configuration

- No hardcoded values
- Custom Metadata for configuration
- Environment-specific settings
- Component status management
- Error handling standards

## Tradeoffs

### Advantages

- Guided workflows improve user experience
- Reusable components reduce development time
- Declarative configuration enables business user changes
- Responsive design supports multiple devices
- Integration with Salesforce data model

### Challenges

- Complex data raptor transformations
- Performance optimization required
- Error handling complexity
- Configuration management
- Testing and debugging

## When to Use OmniStudio

Use OmniStudio when:

- Need guided multi-step workflows
- Require reusable UI components
- Complex business processes need step-by-step guidance
- Both internal and portal users need guided experiences
- Grant management or application workflows required

## When Not to Use OmniStudio

Avoid OmniStudio when:

- Simple single-step processes
- Standard Salesforce functionality sufficient
- No guided workflow requirements
- Different UI framework preferred
- Performance-critical real-time operations

## Q&A

### Q: What is OmniStudio and when should I use it?

**A**: **OmniStudio** (OmniScripts and FlexCards) provides guided workflows and reusable UI components for complex business processes. Use OmniStudio when: (1) **Guided multi-step processes** (application workflows, grant processes), (2) **Complex data collection** (multi-step forms with business rules), (3) **Reusable UI components** (FlexCards for dashboards), (4) **Both internal and portal users** (works in Experience Cloud), (5) **Business rule enforcement** (validation and conditional logic).

### Q: What is the difference between OmniScripts and FlexCards?

**A**: **OmniScripts** are guided workflows that walk users through multi-step processes (application submission, grant workflows). **FlexCards** are reusable UI components for displaying data (dashboards, cards, lists). OmniScripts guide users through processes, FlexCards display information. Both are part of OmniStudio and can be used together.

### Q: How do I implement OmniScripts for guided processes?

**A**: Implement by: (1) **Designing workflow steps** (define process steps), (2) **Creating OmniScript** (configure steps, fields, validation), (3) **Adding business rules** (conditional logic, validation), (4) **Configuring data actions** (save data, call Apex, integrate), (5) **Testing workflow** (test all paths), (6) **Deploying to users** (assign to profiles, permission sets). OmniScripts provide step-by-step guidance.

### Q: How do I use FlexCards for reusable UI components?

**A**: Use FlexCards by: (1) **Designing card layout** (define data to display), (2) **Creating FlexCard** (configure layout, fields, styling), (3) **Adding data sources** (SOQL queries, Apex methods), (4) **Configuring interactions** (click actions, navigation), (5) **Embedding in pages** (add to Lightning pages, Experience Cloud), (6) **Reusing across pages** (same card, different contexts). FlexCards provide reusable UI components.

### Q: Can OmniStudio be used in Experience Cloud (portals)?

**A**: Yes, OmniStudio works in Experience Cloud. OmniScripts can be embedded in Experience Cloud pages for external users (customers, partners, citizens). FlexCards can be used in Experience Cloud dashboards and pages. OmniStudio supports both internal users (Salesforce org) and external users (Experience Cloud), making it suitable for multi-user-type scenarios.

### Q: How do I handle data in OmniScripts?

**A**: Handle data by: (1) **Collecting data** in OmniScript steps (form fields, user input), (2) **Validating data** (business rules, required fields), (3) **Saving data** (DataRaptor, Apex methods), (4) **Loading existing data** (pre-populate fields from records), (5) **Transforming data** (DataRaptor for transformation), (6) **Integrating with external systems** (callouts, integrations). OmniScripts provide data collection and processing capabilities.

### Q: What are DataRaptors in OmniStudio?

**A**: **DataRaptors** are data transformation components in OmniStudio. They: (1) **Extract data** from Salesforce (SOQL queries), (2) **Transform data** (field mapping, calculations), (3) **Load data** to Salesforce (DML operations), (4) **Integrate with external systems** (callouts, APIs). DataRaptors enable data transformation and integration within OmniScripts and FlexCards.

### Q: How do I test OmniStudio components?

**A**: Test by: (1) **Testing OmniScripts** (walk through all steps, test all paths), (2) **Testing FlexCards** (verify data display, interactions), (3) **Testing data actions** (verify data saves correctly), (4) **Testing business rules** (test conditional logic, validation), (5) **Testing in different contexts** (internal users, portal users), (6) **Testing error handling** (test error scenarios). Comprehensive testing ensures OmniStudio components work correctly.

### Q: What are best practices for OmniStudio?

**A**: Best practices include: (1) **Design workflows clearly** (define steps, data flow), (2) **Use business rules** for validation and conditional logic, (3) **Test thoroughly** (all paths, error scenarios), (4) **Optimize data actions** (efficient queries, bulk operations), (5) **Reuse FlexCards** (create reusable components), (6) **Document workflows** (document process, data flow), (7) **Monitor performance** (track execution time, errors).

### Q: When should I use OmniStudio vs. Flows vs. custom LWC?

**A**: Use **OmniStudio** for: guided multi-step workflows, reusable UI components, complex business processes. Use **Flows** for: declarative automation, simple workflows, standard Salesforce processes. Use **custom LWC** for: custom UI requirements, complex interactions, specialized functionality. Choose based on requirements: OmniStudio for guided workflows, Flows for automation, LWC for custom UI.

## Related Patterns

**See Also**:
- <a href="{{ '/rag/development/development/flow-patterns.html' | relative_url }}">Flow Patterns</a> - Flow automation patterns
- <a href="{{ '/rag/development/development/lwc-patterns.html' | relative_url }}">LWC Patterns</a> - Lightning Web Component patterns

**Related Domains**:
- <a href="{{ '/rag/development/architecture/portal-architecture.html' | relative_url }}">Portal Architecture</a> - Experience Cloud patterns

