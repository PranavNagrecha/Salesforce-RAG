# Hybrid Identity Models

## What Was Actually Done

Hybrid identity models were implemented to support multiple user types within a single Salesforce org, each with different identity provider requirements and access patterns. The models support citizens/clients, vendor staff, and internal staff coexisting in the same org.

### Single-Org Multi-Tenant Identity Model

A single Salesforce org was designed to serve three distinct user communities:

- **Citizens/Clients**: External users accessing public sector portals via OIDC identity provider
- **Vendor Staff**: Service provider organization staff accessing via business-tenant identity provider
- **Internal Staff**: Direct employees accessing via internal SAML SSO

Each user type has different:
- Identity providers (OIDC vs. SAML vs. business-tenant)
- Account/Contact Record Types (client vs. vendor vs. internal)
- Sharing rules and data visibility
- Portal experiences (Experience Cloud vs. internal Service Cloud)

### Experience Cloud and Internal User Coexistence

The implementation supports Experience Cloud users and internal users in the same org:

- Different identity providers for different user types
- Different JWT/claims mapping to Salesforce fields based on identity provider
- Sharing and security flows that restrict portal users while allowing internal users broader access
- Portal users see a restricted slice of the same underlying objects that internal users can access fully

### Identity Provider Routing

Login handlers were implemented to route users based on identity provider type:

- Detect identity provider from login context
- Route to appropriate landing pages (portal vs. internal)
- Apply appropriate Record Types and sharing rules
- Tie authenticated identity back to the right Contact and Account

### Vendor Organization Identity

Business-tenant identity was implemented for vendor organizations:

- Vendor staff must create business-tenant accounts with the same email as their legacy ID provider
- Login handler maps business-tenant identity to pre-created vendor Contact and Vendor Account
- Handles multi-org vendor scenarios where staff work across multiple organizations
- Supports future provider organization onboarding without over-committing licenses upfront

## Rules and Patterns

### Multi-Tenant Identity Design

- Use different identity providers for different user types when security and compliance requirements differ
- Implement login handlers to route users based on identity provider type
- Design identity mapping to support pre-created Contacts from migrations
- Avoid creating duplicate Contacts/Users when external identity is attached
- Document identity provider decision criteria for future onboarding

### Record Type-Based Identity Separation

- Use distinct Record Types for Account and Contact to differentiate between client, vendor, and internal staff
- Apply Record Type-specific sharing rules and field-level security
- Route users to Record Type-appropriate landing pages based on identity provider
- Use Record Types in login handler logic to determine user type

### Sharing and Security by Identity Type

- Implement Sharing Sets to enforce data visibility rules per user type
- Design role hierarchies that support cross-agency visibility for authorized staff
- Use field-level security to protect sensitive PII at the field level
- Portal users see only their own records; internal users see broader data sets
- Vendor users see only records for their associated organizations

### Identity Provider Claims Mapping

- Map OIDC claims to Salesforce Contact and User fields for external users
- Map SAML attributes to Salesforce User and Contact fields for internal staff
- Use identity provider claims to determine Record Type assignments
- Store identity provider identifiers in custom fields for correlation
- Support different claim mappings for different user types

### User Creation Strategy

- Pre-create Contacts from migrations before users log in for the first time
- Create Users on first login when Contacts already exist (attach identity to existing Contact)
- Avoid pre-creating Users for every potential user to conserve licenses
- Use "create user on first login" pattern for vendor staff while keeping Contact records pre-migrated
- Handle license utilization carefully, especially for vendor staff

## Suggested Improvements (From AI)

### Unified Identity Management

Consider implementing a unified identity management approach:
- Single identity provider with role-based access control instead of multiple providers
- Use Salesforce Identity for unified identity management
- Implement role-based routing instead of identity provider-based routing
- Reduce complexity by standardizing on fewer identity providers
- Use custom attributes/claims to differentiate user types instead of separate providers

### Enhanced Identity Mapping

Improve identity mapping capabilities:
- Create custom objects to track identity provider mappings
- Implement identity reconciliation processes for orphaned records
- Build dashboards to monitor identity mapping success rates
- Automate identity mapping for bulk migrations
- Create identity mapping audit reports

### Identity Provider Standardization

Standardize identity provider configurations:
- Create reusable login handler patterns for common identity provider types
- Document identity provider configuration templates
- Establish identity provider testing procedures
- Create runbooks for identity provider troubleshooting
- Implement identity provider health monitoring

### User Lifecycle Management

Automate user lifecycle management:
- Implement automated user creation workflows based on identity provider attributes
- Use permission set assignments based on identity provider roles
- Automate user deprovisioning when users are removed from identity provider
- Create user lifecycle management processes
- Monitor user creation and deprovisioning for compliance

## To Validate

- Specific identity provider configurations for each user type
- Login handler routing logic and landing page assignments
- Record Type assignments based on identity provider type
- Sharing rule configurations for each user type
- Identity provider claims/JWT attribute mappings to Salesforce fields
- User creation patterns and license utilization strategies
- Vendor organization onboarding process details

