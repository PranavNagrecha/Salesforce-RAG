# Portal Architecture Patterns

## Overview

Experience Cloud portal architecture patterns for supporting multiple user types (students/applicants, external partners/providers, citizens/clients) with different identity providers, security requirements, and access patterns. These patterns enable single-org multi-tenant portal implementations.

## Portal Types

### Student/Applicant Portals

**Purpose**: Experience Cloud site for students and applicants

**Features**:
- Application submission and tracking
- Viewing checklists, tasks, and decisions
- Self-service case creation and knowledge browsing
- Program selection with eligibility rules
- Document submission and tracking

**Identity**: Institutional identity provider (SAML/OIDC)

**Access**: Students see only their own records

### External Partner/Provider Portals

**Purpose**: Experience Cloud site for external partner staff

**Features**:
- Access to assigned clients/cases
- View notices and transactions relevant to their organization
- Case management for assigned clients
- Service delivery tracking

**Identity**: Organization tenant identity provider

**Access**: External partners see only records for their associated organizations

### Citizen/Client Portals

**Purpose**: Experience Cloud site for citizens/clients

**Features**:
- Case submission and tracking
- View notices and transactions
- Self-service case management
- Document submission
- Benefits information access

**Identity**: External OIDC provider (state-wide citizen identity)

**Access**: Clients see only their own cases/records

## Identity-Aware Behavior

### Login Handler Patterns

**Pattern**: Login handlers detect login type and route accordingly

**Implementation**:
- Detect login type (citizen vs external partner vs staff)
- Route to appropriate landing pages
- Tie authenticated identity back to the right Contact and Account
- Handle edge cases (identity exists but Contact doesn't, vice versa)

### Landing Page Routing

**Pattern**: Route users to appropriate landing pages based on identity provider type

**Implementation**:
- Portal users: Experience Cloud site landing pages
- Internal staff: Service Cloud or internal app landing pages
- External partner users: External partner portal landing pages
- Identity provider-based routing logic

### Record Type-Based Routing

**Pattern**: Use Record Types to determine user experience

**Implementation**:
- Different Record Types for Account (client, external partner, internal)
- Different Record Types for Contact (citizen, external partner staff, internal staff)
- Route users to Record Type-appropriate landing pages
- Apply Record Type-specific sharing rules

## Portal Component Patterns

### Program Selection Components

**Pattern**: LWC components for program selection with eligibility rules

**Features**:
- Filterable/searchable list or grid of programs
- Enforces eligibility rules (e.g., "Only show Hybrid programs if X conditions are met")
- Cascading dropdown pattern: Term → Area → Level → Program → Delivery Mode
- Writes final selection back to Application object and Program Enrollment

**Implementation**:
- Uses structured metadata/config (program catalog, flags) rather than hard-coded lists
- Handles edge cases: applicant switching programs mid-process, inactive/retired programs, terms where program is not offered
- Responsive design for mobile users

### Application Tracking Components

**Pattern**: Components for application status and checklist tracking

**Features**:
- Application status display
- Checklist and required documents tracking
- Milestone tracking
- Document submission interface

### Case Management Components

**Pattern**: Components for case submission and tracking

**Features**:
- Case submission forms
- Case status tracking
- Notice and transaction viewing
- Document attachment

## Sharing and Security

### Sharing Sets

**Pattern**: Sharing Sets enforce data visibility rules per user type

**Implementation**:
- Client users: See only their own cases/records
- External partner users: See only records for their associated organizations
- Internal staff: Can see cross-agency as needed according to policy

### Field-Level Security

**Pattern**: Field-level security protects sensitive PII

**Implementation**:
- Portal users have restricted field access
- Internal users have broader field access
- Sensitive fields (SSN, etc.) read-only for portal users
- Field-level security aligned with compliance requirements

### No Delete Permissions

**Pattern**: All `allowDelete` set to `false` for community users

**Rationale**:
- Data integrity protection
- Prevention of accidental data loss
- Compliance with data retention requirements
- Reduced risk of data corruption

## Portal User Experience

### Responsive Design

**Pattern**: Mobile-first approach with responsive layouts

**Implementation**:
- Mobile-first design with breakpoints
- Flexible layouts for different screen sizes
- Touch-friendly interfaces
- Responsive typography and spacing

### Progressive Disclosure

**Pattern**: Show only relevant information to reduce cognitive load

**Implementation**:
- Cascading dropdowns that filter options
- Step-by-step workflows
- Compact views for selected values
- Expandable sections for detailed information

### Error Handling

**Pattern**: User-friendly error messages and recovery paths

**Implementation**:
- Clear error messages
- Actionable guidance for users
- Error recovery workflows
- Support for user correction

## Integration with OmniStudio

### OmniScripts in Portals

**Pattern**: Use OmniScripts for guided workflows in portals

**Implementation**:
- Application submission workflows
- Grant application processes
- Multi-step data collection
- Guided forms with business rule enforcement

### FlexCards in Portals

**Pattern**: Use FlexCards for reusable UI components

**Implementation**:
- Display aggregated data from multiple sources
- Show at-a-glance information
- Support responsive design
- Integrate with OmniScripts

## Best Practices

### Portal Design

- Design portals for specific user types
- Use identity-aware routing
- Implement progressive disclosure
- Support responsive design
- Provide clear navigation

### Security

- Use Sharing Sets for data visibility
- Implement field-level security
- Remove delete permissions for portal users
- Validate user identity
- Log portal user actions

### User Experience

- Provide clear error messages
- Support error recovery
- Use progressive disclosure
- Optimize for mobile devices
- Test with real users

### Integration

- Integrate with OmniStudio for guided workflows
- Use LWCs for complex UI needs
- Support document upload and management
- Integrate with external systems appropriately
- Log integration operations

## Tradeoffs

### Advantages

- Single org supports multiple user types
- Shared infrastructure reduces costs
- Consistent data model
- Centralized administration
- Unified reporting

### Challenges

- Complex sharing rule design
- Identity provider management
- Careful Record Type management
- Testing across multiple user types
- Performance optimization

## When to Use Portal Architecture

Use portal architecture when:

- Multiple user types need portal access
- Different identity providers required
- Shared data model benefits outweigh complexity
- Unified reporting important
- Cost optimization needed

## When Not to Use Portal Architecture

Avoid portal architecture when:

- Single user type only
- Separate portals provide better isolation
- Security requirements cannot be met
- Different data model requirements
- Performance requirements cannot be met

