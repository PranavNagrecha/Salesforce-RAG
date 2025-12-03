# OIDC and SAML Identity Flows

## What Was Actually Done

Both OIDC and SAML identity providers were implemented to support different user types within the same Salesforce org. OIDC was used for external users (citizens/clients), while SAML was used for internal staff.

### OIDC Implementation for External Users

OIDC SSO was implemented between Salesforce Experience Cloud and a state-wide citizen identity provider for personal tenant users. The implementation:

- Enables citizens and clients to log in to Experience Cloud portals using their state-wide digital identity
- Uses OIDC authorization code flow for secure authentication
- Maps external identity provider GUIDs to Salesforce Contacts
- Handles first-time login scenarios where Contacts were pre-created during migration
- Prevents duplicate Contact/User creation by matching on external GUID and email

### SAML Implementation for Internal Staff

SAML SSO was implemented for internal staff using a state internal SSO identity provider. The implementation:

- Enables staff to log in using their internal enterprise credentials
- Uses SAML 2.0 assertion-based authentication
- Distinguishes between internal staff (direct employees) and vendor staff (contractors)
- Supports different SAML attributes/claims for different user types
- Maps SAML attributes to Salesforce User and Contact fields

### Business-Tenant Identity for Vendors

A business-tenant identity provider was implemented for vendor staff. The implementation:

- Requires vendor staff to create business-tenant accounts with the same email as their legacy ID provider
- Maps business-tenant identity to pre-created vendor Contact and Vendor Account records
- Handles multi-org vendor scenarios where staff work across multiple organizations
- Supports future provider organization onboarding without over-committing licenses upfront

### Login Handler Patterns

Custom login handlers were implemented to manage the identity flows:

- Detect identity provider type from login context
- Match external identity to existing Contacts using GUID and email
- Create Users on first login when Contacts exist (attach identity to existing Contact)
- Route users to appropriate landing pages based on identity provider type
- Handle edge cases and error scenarios gracefully

## Rules and Patterns

### OIDC Flow Implementation

- Use OIDC authorization code flow for Experience Cloud portals
- Configure OIDC provider with correct endpoints (authorization, token, userinfo)
- Map OIDC claims to Salesforce Contact and User fields
- Store external identity provider GUID in custom fields for correlation
- Handle token refresh and expiration scenarios
- Implement logout flows that clear both Salesforce and identity provider sessions

### SAML Flow Implementation

- Use SAML 2.0 for enterprise SSO scenarios
- Configure SAML identity provider with correct metadata (or provide Salesforce metadata to identity provider)
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

### Identity Mapping Strategy

- Map external identity provider GUIDs to Salesforce Contact external ID fields
- Use email addresses as fallback matching criteria
- Store identity provider identifiers in custom fields for correlation
- Maintain mapping between external identity and Salesforce User records
- Support identity provider claims/JWT attributes mapping to Salesforce fields
- Handle cases where external identity exists but Salesforce Contact does not

### User Creation on First Login

- Pre-create Contacts from migrations before users log in for the first time
- Create Users on first login when Contacts already exist (attach identity to existing Contact)
- Avoid pre-creating Users for every potential user to conserve licenses
- Use "create user on first login" pattern for vendor staff while keeping Contact records pre-migrated
- Handle license utilization carefully, especially for vendor staff

### Multi-Identity Provider Routing

- Detect identity provider type from login context (OIDC vs. SAML)
- Route users to appropriate landing pages based on identity provider type
- Apply different sharing rules and field-level security based on identity provider
- Support different user experiences for different identity provider types
- Document routing logic for operations teams

## Suggested Improvements (From AI)

### Unified Identity Provider

Consider standardizing on a single identity provider where possible:
- Use Salesforce Identity for unified identity management
- Implement role-based access control instead of identity provider-based routing
- Reduce complexity by standardizing on fewer identity providers
- Use custom attributes/claims to differentiate user types instead of separate providers

### Enhanced Identity Mapping

Improve identity mapping capabilities:
- Create custom objects to track identity provider mappings
- Implement identity reconciliation processes for orphaned records
- Build dashboards to monitor identity mapping success rates
- Automate identity mapping for bulk migrations
- Create identity mapping audit reports

### Identity Provider Testing

Build comprehensive testing for identity providers:
- Test identity provider configurations in sandbox environments
- Validate identity mapping logic with test users
- Test error scenarios (network failures, invalid tokens)
- Perform user acceptance testing for login flows
- Create test procedures for identity provider changes

### User Lifecycle Management

Automate user lifecycle management:
- Implement automated user creation workflows based on identity provider attributes
- Use permission set assignments based on identity provider roles
- Automate user deprovisioning when users are removed from identity provider
- Create user lifecycle management processes
- Monitor user creation and deprovisioning for compliance

## To Validate

- Specific OIDC provider configuration (endpoints, client ID, client secret)
- SAML identity provider metadata and attribute mappings
- Login handler code implementation details
- Identity mapping logic (exact field mappings and matching criteria)
- User creation patterns and license utilization strategies
- Error handling scenarios and recovery procedures
- Logout flow implementation details

