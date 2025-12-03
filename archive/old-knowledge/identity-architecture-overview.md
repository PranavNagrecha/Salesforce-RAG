# Identity Architecture Overview

## What Was Actually Done

Multiple identity providers were integrated across different implementations to support various user types within single Salesforce orgs. The identity architecture supports citizens/clients, vendor staff, and internal staff, each with different identity provider requirements.

### Multi-Identity Provider Design

A single Salesforce org was designed to support three distinct identity provider types:

- **External OIDC Provider**: State-wide citizen identity provider for citizens and clients accessing public sector portals
- **Internal SAML Provider**: State internal SSO for staff (direct employees)
- **Business-Tenant Identity Provider**: Separate identity provider for vendor organizations providing services on behalf of the state

### Login Handler Implementation

Custom login handlers were implemented to manage user creation and identity mapping:

- Match external identity provider GUIDs to existing Contacts using email and external ID fields
- Prevent duplicate Contact/User creation when users first log in after migration
- Route users to appropriate landing pages based on their identity provider type
- Maintain consistent Account/Contact ownership relationships during identity attachment
- Handle edge cases where external identity exists but Salesforce Contact does not (and vice versa)

### Experience Cloud vs Internal Users

A mixed model was implemented where:

- Experience Cloud users (citizens, vendors) and internal users coexist in the same org
- Different identity providers for different user types
- Different JWT/claims mapping to Salesforce fields based on identity provider
- Sharing and security flows that restrict portal users while allowing internal users broader access

### Higher Education SSO Patterns

In higher education contexts, Salesforce login options were aligned with institutional SSO strategy:

- SAML or OIDC integration with institutional identity provider for staff
- Potential student SSO integration (less common, typically handled through Experience Cloud)
- Identity mapping between institutional IDs and Salesforce contacts/users
- Alignment with SIS IDs and external IDs used for integration

## Rules and Patterns

### Multi-Identity Provider Strategy

- Use different identity providers for different user types when security and compliance requirements differ
- Implement login handlers to route users based on identity provider type
- Design identity mapping to support pre-created Contacts from migrations
- Avoid creating duplicate Contacts/Users when external identity is attached
- Document identity provider decision criteria for future onboarding

### Login Handler Design

- Always check for existing Contacts by external ID before creating new records
- Use email as a secondary matching criterion when external ID is not available
- Log all login handler operations for troubleshooting identity mapping issues
- Handle edge cases where external identity exists but Salesforce Contact does not (and vice versa)
- Route users to Record Type-appropriate landing pages based on identity provider type
- Maintain Account/Contact ownership consistency during identity attachment

### Identity Mapping

- Map external identity provider GUIDs to Salesforce Contact external ID fields
- Use email addresses as fallback matching criteria
- Store identity provider identifiers in custom fields for correlation
- Maintain mapping between external identity and Salesforce User records
- Support identity provider claims/JWT attributes mapping to Salesforce fields

### User Creation Strategy

- Pre-create Contacts from migrations before users log in for the first time
- Create Users on first login when Contacts already exist (attach identity to existing Contact)
- Avoid pre-creating Users for every potential user to conserve licenses
- Use "create user on first login" pattern for vendor staff while keeping Contact records pre-migrated
- Handle license utilization carefully, especially for vendor staff

### Experience Cloud Identity

- Use OIDC for external users (citizens, clients) when possible for better user experience
- Implement login handlers that detect Experience Cloud vs. internal user login
- Route Experience Cloud users to portal-specific landing pages
- Restrict Experience Cloud user access through sharing rules and field-level security
- Support guest user access for unauthenticated portal features where appropriate

## Suggested Improvements (From AI)

### Centralized Identity Management

Consider implementing a centralized identity management approach:
- Single identity provider with role-based access control instead of multiple providers
- Use Salesforce Identity for unified identity management
- Implement role-based routing instead of identity provider-based routing
- Reduce complexity by standardizing on fewer identity providers

### Enhanced Identity Mapping

Improve identity mapping capabilities:
- Create custom objects to track identity provider mappings
- Implement identity reconciliation processes for orphaned records
- Build dashboards to monitor identity mapping success rates
- Automate identity mapping for bulk migrations

### Identity Provider Standardization

Standardize identity provider configurations:
- Create reusable login handler patterns for common identity provider types
- Document identity provider configuration templates
- Establish identity provider testing procedures
- Create runbooks for identity provider troubleshooting

### User Provisioning Automation

Automate user provisioning processes:
- Implement automated user creation workflows based on identity provider attributes
- Use permission set assignments based on identity provider roles
- Automate user deprovisioning when users are removed from identity provider
- Create user lifecycle management processes

## To Validate

- Specific identity provider configurations (OIDC endpoints, SAML metadata)
- Login handler code patterns and error handling approaches
- Exact identity mapping logic (how GUIDs map to Contacts)
- User creation patterns and license utilization strategies
- Identity provider claims/JWT attribute mappings to Salesforce fields
- Experience Cloud identity configuration details

