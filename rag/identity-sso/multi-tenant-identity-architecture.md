# Multi-Tenant Identity Architecture

## Overview

Multi-tenant identity architecture enables a single Salesforce org to support multiple distinct user communities with different identity providers, security requirements, and access patterns. This pattern is essential for public sector and higher education implementations where citizens, external partner organizations, and internal staff must coexist in the same org.

## Architecture Pattern

### Single-Org Multi-Tenant Model

A single Salesforce org serves multiple distinct user communities:

- **External Users (Citizens/Clients)**: Accessing public sector portals via OIDC identity provider
- **External Partner Staff**: Service provider organization staff accessing via organization tenant identity provider
- **Internal Staff**: Direct employees accessing via internal SAML SSO

Each user type has different:
- Identity providers (OIDC vs. SAML vs. organization tenant)
- Account/Contact Record Types (client vs. external partner vs. internal)
- Sharing rules and data visibility
- Portal experiences (Experience Cloud vs. internal Service Cloud)

## Identity Provider Implementation

### OIDC for External Users

OIDC SSO implementation for external users (citizens/clients):

- **Use Case**: State-wide citizen identity provider for personal tenant users
- **Flow**: OIDC authorization code flow for secure authentication
- **Mapping**: External identity provider GUIDs mapped to Salesforce Contacts
- **First-Time Login**: Handles scenarios where Contacts were pre-created during migration
- **Duplicate Prevention**: Matches on external GUID and email to prevent duplicate Contact/User creation

### SAML for Internal Staff

SAML SSO implementation for internal staff:

- **Use Case**: State internal SSO identity provider for direct employees
- **Flow**: SAML 2.0 assertion-based authentication
- **User Types**: Distinguishes between internal staff (direct employees) and external partner staff (contractors)
- **Attributes**: Supports different SAML attributes/claims for different user types
- **Mapping**: Maps SAML attributes to Salesforce User and Contact fields

### Organization Tenant Identity for External Partners

Organization tenant identity provider for external partner staff:

- **Use Case**: External partner organizations doing work on behalf of the state
- **Account Creation**: External partner staff must create organization tenant accounts with the same email as their legacy ID provider
- **Mapping**: Maps organization tenant identity to pre-created external partner Contact and External Partner Account records
- **Multi-Org Support**: Handles multi-org external partner scenarios where staff work across multiple organizations
- **License Management**: Supports future provider organization onboarding without over-committing licenses upfront

## Login Handler Patterns

### Custom Login Handler Implementation

Custom login handlers manage identity flows:

- **Identity Detection**: Detect identity provider type from login context
- **Contact Matching**: Match external identity to existing Contacts using GUID and email
- **User Creation**: Create Users on first login when Contacts exist (attach identity to existing Contact)
- **Routing**: Route users to appropriate landing pages based on identity provider type
- **Error Handling**: Handle edge cases and error scenarios gracefully

### Matching Strategy

Dual matching criteria to prevent duplicate Contact/User creation:

- **Primary**: External identity provider GUID
- **Secondary**: Email address
- **Fallback**: Use email when external ID is not available
- **Logging**: Log all login handler operations for troubleshooting

## Record Type-Based Separation

### Account and Contact Record Types

Distinct Record Types for different user types:

- **Client Record Type**: For citizens/clients accessing public sector portals
- **External Partner Record Type**: For external partner staff and service providers
- **Internal Staff Record Type**: For direct employees

### Record Type Usage

- Apply Record Type-specific sharing rules and field-level security
- Route users to Record Type-appropriate landing pages based on identity provider
- Use Record Types in login handler logic to determine user type
- Maintain separation of person-level data from organization-level data

## Sharing and Security Model

### Sharing Sets

Sharing Sets enforce data visibility rules per user type:

- **Client Users**: See only their own cases/records
- **External Partner Users**: See only records for their associated organizations
- **Internal Staff**: Can see cross-agency as needed according to policy

### Role Hierarchy

Design role hierarchies that support:

- Cross-agency visibility for authorized staff
- Restricted access for portal users
- Organization-based access for external partner users

### Field-Level Security

Use field-level security to:

- Protect sensitive PII at the field level
- Apply different field access based on user type
- Support compliance requirements

## User Creation Strategy

### Pre-Create Contacts from Migrations

- Contacts created before users log in for the first time
- Enables identity attachment to existing records
- Prevents duplicate record creation

### Create Users on First Login

- Users created when Contacts exist (attach identity to existing Contact)
- Conserves licenses by creating users only when they first log in
- Avoids pre-creating all users upfront

### License Management

- Handle license utilization carefully, especially for external partner staff
- Use "create user on first login" pattern for external partner staff while keeping Contact records pre-migrated
- Monitor license consumption and plan for growth

## Identity Mapping Strategy

### External ID Mapping

- Map external identity provider GUIDs to Salesforce Contact external ID fields
- Use email addresses as fallback matching criteria
- Store identity provider identifiers in custom fields for correlation
- Maintain mapping between external identity and Salesforce User records

### Claims/JWT Attribute Mapping

- Map OIDC claims to Salesforce Contact and User fields for external users
- Map SAML attributes to Salesforce User and Contact fields for internal staff
- Use identity provider claims to determine Record Type assignments
- Support different claim mappings for different user types

### Edge Case Handling

Handle cases where:

- External identity exists but Salesforce Contact does not
- Salesforce Contact exists but external identity does not
- Multiple identity providers for the same user
- Identity provider changes or updates

## Routing and Landing Pages

### Identity Provider-Based Routing

- Detect identity provider type from login context (OIDC vs. SAML vs. organization tenant)
- Route users to appropriate landing pages based on identity provider type
- Apply different user experiences for different identity provider types
- Document routing logic for operations teams

### Landing Page Assignment

- **Portal Users**: Experience Cloud site landing pages
- **Internal Staff**: Service Cloud or internal app landing pages
- **External Partner Users**: External partner portal landing pages

## Best Practices

### OIDC Flow Implementation

- Use OIDC authorization code flow for Experience Cloud portals
- Configure OIDC provider with correct endpoints (authorization, token, userinfo)
- Map OIDC claims to Salesforce Contact and User fields
- Store external identity provider GUID in custom fields for correlation
- Handle token refresh and expiration scenarios
- Implement logout flows that clear both Salesforce and identity provider sessions

### SAML Flow Implementation

- Use SAML 2.0 for enterprise SSO scenarios
- Configure SAML identity provider with correct metadata
- Map SAML attributes to Salesforce User and Contact fields
- Handle SAML assertion validation and signature verification
- Support different SAML attribute mappings for different user types
- Implement single logout (SLO) where supported by identity provider

### Login Handler Best Practices

- Always check for existing Contacts by external ID before creating new records
- Use email as a secondary matching criterion when external ID is not available
- Log all login handler operations for troubleshooting
- Handle identity provider errors gracefully (network failures, invalid tokens)
- Route users to Record Type-appropriate landing pages
- Maintain Account/Contact ownership consistency during identity attachment

## Tradeoffs and Considerations

### Advantages

- Single org reduces data silos and enables unified reporting
- Shared infrastructure reduces costs
- Consistent data model across user types
- Centralized administration

### Challenges

- Complex identity provider management
- Careful sharing rule design required
- License management across user types
- Identity mapping complexity
- Testing across multiple identity providers

## When to Use This Pattern

Use multi-tenant identity architecture when:

- Multiple distinct user communities need access to the same org
- Different identity providers are required for security/compliance
- Shared data model benefits outweigh complexity
- License costs need to be optimized
- Unified reporting is important

## When Not to Use This Pattern

Avoid multi-tenant identity architecture when:

- User communities have completely separate data requirements
- Identity provider complexity outweighs benefits
- Security requirements cannot be met with sharing rules
- License costs are not a concern
- Separate orgs provide better isolation

