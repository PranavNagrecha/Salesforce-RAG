# Lightning Web Component (LWC) Patterns

## Overview

LWCs are built for complex business logic that standard page layouts cannot handle. Components are designed to make complex processes usable for non-technical users and hide integration complexity behind simple interfaces.

## When to Use LWCs

LWCs are surgical tools for complex UI needs when:

- Need to combine data from multiple objects/systems
- Need complex client-side decisions and filtering
- Need responsive, interactive experiences
- Need to work cleanly in Experience Cloud portals
- Standard layouts or Flows cannot handle the requirement

## Component Patterns

### Console-Style LWCs

**Purpose**: Agent consoles for case workers, advisors, internal staff

**Features**:
- Aggregate data from multiple related records (Cases, Contacts, external system results)
- Show "at-a-glance" status, flags, and next actions
- Use `@wire` adapters to fetch data via Apex or LDS
- Implement local state + imperative Apex calls for actions (e.g., re-run external check, update status)
- Avoid heavy logic in components by pushing orchestration into Apex/services

### Fraud/Risk Scoring LWC

**Purpose**: Display fraud or risk scores for clients/cases

**Features**:
- Shows fraud or risk score based on rules and/or external scoring engine
- Displays score with clear visual indicators (color, icons, messaging)
- Pulls scores from either custom object populated by integration, or Apex making callout to integration layer
- Handles no-score scenarios (e.g., new client)
- Supports multiple rulesets or sources (system score vs manual overrides)
- LWC is mostly presentation + lightweight orchestration
- Apex service layer encapsulates callout details, error handling, and mapping from external payload → internal score model

**Implementation Pattern**:
- On-demand calculation (doesn't auto-calculate on page load)
- Cacheable methods for data fetch and calculation
- Detailed breakdown showing all factors with values and coefficients
- Override conditions checked first (business rules before model)
- Feedback mechanism for user input

### Program-Selection LWC

**Purpose**: Let applicants or staff select academic programs with real eligibility rules

**Features**:
- Filterable/searchable list or grid of programs
- Enforces eligibility rules (e.g., "Only show Hybrid programs if X conditions are met")
- Writes final selection back to Application object and Program Enrollment or related record
- Uses structured metadata/config (program catalog, flags) rather than hard-coded lists
- Handles edge cases: applicant switching programs mid-process, inactive/retired programs, terms where program is not offered

**Implementation Pattern**:
- Cascading dropdown pattern: Term → Area → Level → Program → Delivery Mode
- Each step filters next step's options
- Only loads data when previous step selected (reduces initial load time)
- Compact view pattern: shows selected values in compact form, allows editing
- Auto-selection logic: if program has only one delivery option, auto-selects it
- Responsive design: mobile-first with breakpoints, flexible layouts

### Advisor Management LWC

**Purpose**: Staff management of advisor information

**Features**:
- View and edit advisor-specific fields (availability days, times, nickname)
- Pagination for large datasets (15 advisors per page)
- Search functionality (by name or email)
- Inline editing without full page refresh
- Works with field-level security

**Implementation Pattern**:
- Server-side pagination (Apex handles offset/limit)
- Server-side search (Apex handles filtering)
- Lightning Data Table with editable columns
- Draft values tracked locally
- Batch update on save (all edited rows in one DML)
- System mode updates (`without sharing`) to bypass FLS for updates

## Reusable LWC Patterns

### Service-Layer Pattern

**Pattern**: Apex classes expose clean methods for LWCs

- Methods like `getXXXViewModel(Id recordId)` and `performAction(...)`
- LWCs don't "know" SOQL details; they deal with DTO-style payloads
- Encapsulates business logic and data access
- Enables reuse across multiple components

### Config-Driven UI

**Pattern**: Use custom metadata / custom settings to drive:

- Which fields show up
- Thresholds (e.g., risk score color bands)
- Text/labels that might vary by environment or client
- Business rules and configuration

**Benefits**: Environment-specific configuration without code changes

### Performance-Aware Patterns

**Pattern**: Optimize for performance

- Batch reads into a single wired Apex method when possible
- Use `refreshApex` carefully to avoid hammering the org
- Defer heavy recalculation to async jobs if needed
- Cacheable methods for read-only operations
- On-demand loading for heavy data

## Data Access Patterns

### @wire for Reactive Data Access

- Use `@wire` for reactive data access when possible
- Support automatic data refresh
- Handle loading and error states
- Abstract SOQL details from components

### Imperative Apex Calls

- Use imperative Apex calls for actions and updates
- Support user-initiated operations
- Handle loading states appropriately
- Provide immediate feedback

### Batching Data Reads

- Batch data reads into single Apex methods
- Reduce server round trips
- Improve performance
- Simplify component logic

### Caching

- Cache data in component state when appropriate
- Use `@AuraEnabled(cacheable=true)` for read-only operations
- Cache reference data (terms, areas, levels)
- Cache busting with random parameter when fresh data needed

### LDS (Lightning Data Service)

- Use LDS for standard objects when possible
- Leverage platform caching
- Reduce custom Apex code
- Improve performance

## Error Handling

### User-Friendly Messages

- Handle errors gracefully with user-friendly messages
- Provide actionable guidance
- Support error recovery workflows
- Use toast notifications appropriately

### Error Logging

- Log errors for troubleshooting
- Include context about what failed
- Support error analysis
- Enable debugging workflows

### Validation

- Validate input before making server calls
- Provide immediate feedback
- Prevent invalid submissions
- Guide users to correct errors

### Loading States

- Handle loading states appropriately
- Show progress indicators
- Prevent multiple submissions
- Provide feedback during operations

## Performance Optimization

### Minimize Server Round Trips

- Batch operations when possible
- Use cacheable methods for read-only data
- Combine related queries
- Reduce unnecessary calls

### Use refreshApex Carefully

- Don't overuse `refreshApex`
- Only refresh when necessary
- Consider caching strategies
- Monitor performance impact

### Defer Heavy Calculations

- Defer heavy recalculation to async jobs if needed
- On-demand calculation for expensive operations
- Lazy loading for large data sets
- Progressive disclosure of information

### Performance-Optimized LWC Controller Pattern

**When to use**: When building Lightning Web Component controllers that need to fetch and process data efficiently.

**Implementation approach**:
- Don't auto-calculate on page load (user must click button) - prevents unnecessary Apex calls
- Use `@AuraEnabled(cacheable=true)` for read-only operations
- Implement cache busting with random parameter when fresh data needed (e.g., `System.currentTimeMillis()`)
- Fetch all required data in single Apex call (not multiple separate queries)
- Use relationship queries to combine data in single query
- Only select necessary fields (not entire objects)
- Use lazy loading for detailed breakdowns (hidden in tabs, loaded when expanded)

**Why it's recommended**: Auto-calculating on page load creates unnecessary Apex calls and slows page load times. Cacheable methods with cache busting provide best of both worlds (performance + fresh data). Single Apex calls reduce network latency. Lazy loading improves perceived performance.

**Real example**: Fraud score calculation component. Doesn't auto-calculate on load - user must click "Calculate" button. Uses cacheable methods with cache busting. Fetches all required data in single call. Lazy loads detailed breakdown in tabs.

**Lessons learned**:
- Not auto-calculating on load significantly improves page load times
- Cacheable methods with cache busting provide best of both worlds (performance + fresh data)
- User control over when to calculate improves perceived performance
- Single Apex calls reduce network latency

### Optimize Data Queries

- Optimize data queries in Apex
- Use selective WHERE clauses
- Limit result sets appropriately
- Cache frequently accessed data

## Accessibility

### WCAG Guidelines

- Follow WCAG guidelines for accessibility
- Ensure keyboard navigation works
- Support screen readers
- Provide alternative text for images

### Semantic HTML

- Use semantic HTML elements
- Proper heading hierarchy
- Meaningful form labels
- Accessible form controls

### ARIA Labels

- Provide ARIA labels where needed
- Support assistive technologies
- Ensure proper role attributes
- Test with screen readers

## Responsive Design

### Mobile-First Approach

- Mobile-first design with breakpoints
- Flexible layouts for different screen sizes
- Touch-friendly targets
- Responsive typography

### Breakpoints

- Use consistent breakpoints (e.g., 768px)
- Adapt layouts for different screen sizes
- Test on multiple devices
- Ensure usability across devices

## Best Practices Summary

### Component Design

- Break work into focused, reusable components
- Keep components small and single-purpose
- Use composition over complex monolithic components
- Separate presentation from business logic
- Push complex logic to Apex service layer

### Data Access

- Use `@wire` for reactive data access when possible
- Use imperative Apex calls for actions and updates
- Batch data reads into single Apex methods
- Cache data in component state when appropriate
- Use LDS for standard objects when possible

### Error Handling

- Handle errors gracefully with user-friendly messages
- Log errors for troubleshooting
- Provide recovery paths for users
- Validate input before making server calls
- Handle loading states appropriately

### Performance

- Minimize server round trips
- Use `refreshApex` carefully
- Defer heavy calculations to async jobs if needed
- Optimize data queries in Apex
- Use lazy loading for large data sets

### Accessibility

- Follow WCAG guidelines for accessibility
- Use semantic HTML
- Provide ARIA labels where needed
- Ensure keyboard navigation works
- Test with screen readers

