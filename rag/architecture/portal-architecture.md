---
title: "Portal Architecture Patterns"
level: "Advanced"
tags:
  - architecture
  - experience-cloud
  - portals
  - multi-tenant
last_reviewed: "2025-01-XX"
---

# Portal Architecture Patterns

## Overview

Experience Cloud portal architecture patterns for supporting multiple user types (students/applicants, external partners/providers, citizens/clients) with different identity providers, security requirements, and access patterns. These patterns enable single-org multi-tenant portal implementations.

Experience Cloud (formerly Communities) enables organizations to create branded portals for external users (customers, partners, citizens) with controlled access to Salesforce data and functionality. Effective Experience Cloud configuration requires understanding site setup, authentication, branding, security, and user experience design.

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

## Experience Cloud Administration

### Site Setup and Configuration

**Site creation**:
- Create Experience Cloud site with appropriate template
- Configure site URL and domain
- Set up site preferences and settings
- Configure site navigation and pages

**Site templates**:
- Customer Service template for support portals
- Partner Central template for partner portals
- Build Your Own (LWR) template for custom sites
- Choose template based on use case

**Site configuration**:
- Configure site branding and theming
- Set up site navigation and pages
- Configure site preferences and settings
- Set up site search and content management

### Authentication Configuration

**Authentication methods**:
- Salesforce authentication (username/password)
- SAML for enterprise SSO
- OIDC for external identity providers
- Social authentication (if enabled)
- Guest user access (read-only, no authentication)

**Login handler configuration**:
- Configure login handlers for identity routing
- Route users based on identity provider type
- Handle identity matching and user creation
- Configure authentication flows

**Best practice**: Configure authentication based on user type and security requirements. Use SAML for enterprise SSO, OIDC for external users. Configure login handlers for identity-aware routing.

### Branding and Theming

**Branding configuration**:
- Configure site logo and branding
- Set up color schemes and themes
- Customize fonts and typography
- Configure mobile branding

**Theme customization**:
- Use Lightning Design System tokens
- Customize component styling
- Configure responsive design
- Test branding across devices

**Best practice**: Brand sites to match organizational identity. Use Lightning Design System for consistency. Test branding on different devices. Keep branding professional and accessible.

### Security Configuration

**Sharing Sets**:
- Configure Sharing Sets for portal user data access
- Define which records portal users can access
- Set up record-level sharing rules
- Test sharing with different user types

**Field-Level Security**:
- Configure field-level security for portal users
- Restrict sensitive field access
- Align FLS with compliance requirements
- Test field visibility with portal users

**Profile and Permission Sets**:
- Configure Experience Cloud profiles
- Assign permission sets for portal users
- Remove delete permissions for portal users
- Test permissions with portal users

**Best practice**: Configure security carefully for portal users. Use Sharing Sets for record access. Restrict field access appropriately. Remove delete permissions. Test security thoroughly.

### User Experience Configuration

**Page configuration**:
- Configure site pages and navigation
- Set up landing pages for different user types
- Configure page layouts and components
- Test page functionality with portal users

**Component configuration**:
- Add Lightning components to pages
- Configure component visibility and behavior
- Test components with portal users
- Optimize component performance

**Mobile configuration**:
- Configure mobile-responsive layouts
- Test mobile user experience
- Optimize for mobile devices
- Ensure touch-friendly interfaces

**Best practice**: Design user experience for portal users. Keep navigation simple and clear. Test with real portal users. Optimize for mobile devices.

### Content Management

**CMS (Content Management System)**:
- Configure CMS for content management
- Create and manage content items
- Organize content by channels and topics
- Publish content for portal users

**Knowledge base integration**:
- Publish knowledge articles to portal
- Configure article search and browsing
- Organize articles by categories
- Enable article feedback

**Best practice**: Use CMS for content management. Publish knowledge articles for self-service. Organize content for easy discovery. Maintain content regularly.

### Analytics and Moderation

**Site analytics**:
- Configure site analytics and tracking
- Monitor site usage and performance
- Track user engagement and behavior
- Analyze site effectiveness

**Content moderation**:
- Configure content moderation rules
- Set up moderation workflows
- Monitor user-generated content
- Handle moderation actions

**Best practice**: Monitor site analytics for insights. Configure content moderation for user-generated content. Review analytics regularly for optimization opportunities.

## Q&A

### Q: What is the difference between Experience Cloud and Communities?

**A**: **Experience Cloud** is the current name for what was previously called "Communities" or "Community Cloud". They refer to the same platform for creating branded portals for external users. Use "Experience Cloud" in current documentation.

### Q: When should I use a single portal vs multiple portals?

**A**: Use a **single portal** when user types have similar access patterns, security requirements can be met with Sharing Sets and profiles, and you want to simplify administration. Use **multiple portals** when user types need complete isolation, have different security requirements, or require different data models.

### Q: How do I implement multi-tenant data isolation in Experience Cloud?

**A**: Use multiple Sharing Sets for different profiles, combine with Record Type-based separation, use Apex managed sharing for complex patterns, and ensure Sharing Sets only grant access to the user's tenant records. Use restrictive OWD (Private) and validation rules to prevent cross-tenant access.

### Q: What authentication methods are available for Experience Cloud?

**A**: Available methods include Salesforce authentication (username/password), SAML for enterprise SSO, OIDC for external identity providers, social authentication (if enabled), and guest user access (read-only, no authentication). Choose based on user type and security requirements.

### Q: How do Sharing Sets work for Experience Cloud users?

**A**: Sharing Sets grant community users access to records based on user (records associated with user's contact), account (records associated with user's account), or owner (records owned by the user). They replace traditional sharing rules for portal users, as Customer Community licenses do not support sharing rules.

### Q: What are the security considerations for Experience Cloud portals?

**A**: Configure Sharing Sets for record access, configure field-level security appropriately, remove delete permissions for portal users, test security thoroughly with different user types, and align security with compliance requirements. Portal users should have minimal necessary access.

### Q: How do I handle different user types in a single portal?

**A**: Use different Experience Cloud profiles for different user types, configure Sharing Sets per profile, use Record Types to separate data if needed, configure login handlers for identity-aware routing, and set up different landing pages for different user types.

### Q: What are the performance considerations for Experience Cloud portals?

**A**: Optimize Lightning components for performance, configure mobile-responsive layouts, use efficient SOQL queries in components, implement proper caching strategies, monitor site analytics for performance insights, and test portal performance with realistic data volumes.

## Related Patterns

**See Also**:
- [Multi-Tenant Identity Architecture](/rag/identity-sso/multi-tenant-identity-architecture.html) - Identity and SSO patterns for portals
- [Sharing Sets and Portals](/rag/security/sharing-sets-and-portals.html) - Experience Cloud sharing patterns

**Related Domains**:
- [Mobile Strategy](/rag/architecture/mobile-strategy.html) - Mobile portal optimization
- [LWC Patterns](/rag/development/lwc-patterns.html) - Custom component development for portals
- [OmniStudio Patterns](/rag/development/omnistudio-patterns.html) - OmniStudio patterns for portals

