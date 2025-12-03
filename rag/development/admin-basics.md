---
title: "Salesforce Administration Basics"
source: "The Salesforce Master Class wiki"
source_url: "https://github.com/Coding-With-The-Force/The-Salesforce-Master-Class/wiki"
topic: "Topic 2: The Complete Guide To Salesforce Administration"
section: "The Basics of Salesforce Administration"
level: "Beginner"
tags:
  - salesforce
  - administration
  - org-setup
  - navigation
  - best-practices
last_reviewed: "2025-01-XX"
---

# Overview

Salesforce administration encompasses the foundational activities required to configure, maintain, and optimize a Salesforce org for business use. Administrators are responsible for org setup, user management, data model configuration, security configuration, automation, and ongoing maintenance.

Effective administration requires understanding the Salesforce platform architecture, declarative configuration capabilities, security model, and how different configuration elements work together. Administrators must balance business requirements with platform capabilities, ensuring the org supports business processes while maintaining security, performance, and usability.

The role of a Salesforce administrator has evolved from basic configuration to strategic platform management, requiring knowledge of both declarative tools and when to involve developers for programmatic solutions. Modern administrators work closely with business stakeholders, developers, and architects to deliver solutions.

# Core Concepts

## Salesforce Administrator Role

**What it is**: Primary role responsible for configuring, maintaining, and optimizing Salesforce orgs to support business processes.

**Key responsibilities**:
- Org setup and configuration
- User and license management
- Data model configuration (objects, fields, relationships)
- Security configuration (profiles, permission sets, sharing)
- Automation configuration (Flows - ⚠️ **Note**: Process Builder and Workflow Rules are deprecated, use Record-Triggered Flows instead)
- Reports and dashboards
- Data management and quality
- User training and support
- Change management and deployment

**Skill requirements**:
- Salesforce Administrator certification recommended
- Understanding of declarative configuration
- Understanding of security and sharing model
- Data management and quality skills
- Business process analysis skills
- Communication and training skills

## Lightning Experience vs. Classic

**Lightning Experience**: Modern Salesforce user interface providing enhanced functionality, improved mobile experience, and advanced features.

**Key features**:
- Modern, responsive interface
- Enhanced reporting and dashboards
- Lightning App Builder for custom pages
- Advanced automation with Flows
- Improved mobile experience
- Better collaboration features

**When to use**: Default for most users. Use Lightning Experience for modern functionality and improved user experience.

**Salesforce Classic**: Legacy user interface still available for specific use cases or when Lightning Experience doesn't support required functionality.

**When to use**: Use Classic only when specific functionality isn't available in Lightning Experience or for specific administrative tasks that require Classic.

**Best practice**: Use Lightning Experience as default. Use Classic only when necessary for specific functionality.

## Sandboxes and Scratch Orgs

**Sandboxes**: Copies of production orgs used for development, testing, and training.

**Types of sandboxes**:
- Developer Sandbox: Basic sandbox for development and testing
- Developer Pro Sandbox: Enhanced sandbox with more data and features
- Partial Copy Sandbox: Sandbox with subset of production data
- Full Sandbox: Complete copy of production org with all data

**When to use**: Use sandboxes for development, testing, user acceptance testing, and training. Never develop directly in production.

**Scratch Orgs**: Temporary, source-driven orgs for development and testing, typically used with Salesforce DX.

**When to use**: Use scratch orgs for modern development workflows, source-driven development, and CI/CD pipelines.

**Best practice**: Always develop and test in sandboxes or scratch orgs before deploying to production. Use appropriate sandbox type for your needs.

## Company Information and Org Settings

**Company Information**: Basic org configuration including company name, address, fiscal year, and organizational details.

**Key settings**:
- Company name and details
- Fiscal year settings
- Default currency and multi-currency
- Language and locale settings
- Time zone settings

**Org Settings**: Organization-wide settings that affect all users and functionality.

**Key settings**:
- UI settings (Lightning Experience, Classic)
- Security settings (password policies, session settings)
- Data management settings
- Email settings
- Feature toggles and preferences

**Best practice**: Configure company information and org settings early in org setup. Review and update settings periodically as needs evolve.

# Deep-Dive Patterns & Best Practices

## Org Setup Best Practices

**Initial setup checklist**:
1. Configure company information and org details
2. Set up fiscal year and currency settings
3. Configure language and time zone settings
4. Set up UI preferences (Lightning Experience default)
5. Configure security settings (password policies, session settings)
6. Set up email settings and deliverability
7. Configure data management settings
8. Review and configure feature toggles

**Ongoing maintenance**:
- Regularly review org settings and preferences
- Monitor storage usage and limits
- Review and update company information as needed
- Monitor feature adoption and usage
- Review security settings and compliance requirements

## Navigation and User Experience

**Lightning Experience navigation**:
- App Launcher for accessing apps and objects
- Navigation bar for quick access to common items
- Object tabs for accessing specific objects
- Recent items for quick access to recently viewed records

**Customization opportunities**:
- Customize navigation items in apps
- Configure app-specific navigation
- Set up custom Lightning pages
- Configure mobile navigation

**Best practice**: Customize navigation to match user workflows. Simplify navigation for better user experience. Test navigation with end users.

## Storage and Limits Management

**Storage types**:
- Data storage (records)
- File storage (ContentVersion, Attachments)
- Big Object storage (archived data)

**Monitoring storage**:
- Regularly monitor storage usage
- Plan for storage growth
- Archive old data when appropriate
- Clean up unused files and attachments

**Best practice**: Monitor storage usage proactively. Plan for storage growth. Implement data archiving strategies for large data volumes.

## Multi-Language and Multi-Currency Setup

**Multi-language setup**:
- Configure supported languages
- Translate field labels and values
- Translate picklist values
- Translate email templates and communications

**Multi-currency setup**:
- Enable multi-currency
- Configure currencies and conversion rates
- Set default currency
- Configure currency for users and records

**Best practice**: Configure multi-language and multi-currency early if needed. Plan for translation and currency management. Consider ongoing maintenance requirements.

# Implementation Guide

## Org Setup Process

1. **Company information**: Configure company name, address, and organizational details
2. **Fiscal year**: Set up fiscal year settings if different from calendar year
3. **Currency**: Configure default currency and multi-currency if needed
4. **Language and locale**: Configure supported languages and locale settings
5. **Time zone**: Set default time zone and user time zone preferences
6. **UI settings**: Configure Lightning Experience as default, set UI preferences
7. **Security settings**: Configure password policies, session settings, security preferences
8. **Email settings**: Configure email deliverability, email templates, email limits
9. **Feature toggles**: Review and enable/disable features as needed
10. **Storage monitoring**: Set up storage monitoring and alerts

## Prerequisites

- System Administrator access
- Understanding of business requirements
- Company information and organizational details
- Security and compliance requirements
- Email and communication requirements

## Key Configuration Decisions

**UI preferences**:
- Lightning Experience vs. Classic default
- Mobile app preferences
- Navigation customization
- App and tab configuration

**Security decisions**:
- Password policy requirements
- Session timeout settings
- IP restrictions if needed
- Two-factor authentication requirements

**Data management decisions**:
- Multi-currency requirements
- Multi-language requirements
- Data archiving strategy
- Storage management approach

## Validation & Testing

**Org setup validation**:
- Verify company information is correct
- Test UI preferences and navigation
- Validate security settings
- Test email functionality
- Verify multi-currency and multi-language if configured
- Test storage monitoring and alerts

**Tools to use**:
- Setup menu for org configuration
- Company Information page
- Security Settings
- Email Administration
- Storage usage reports

# Common Pitfalls & Anti-Patterns

## Not Configuring Org Settings Early

**Bad pattern**: Delaying org setup configuration, leading to rework and user confusion.

**Why it's bad**: Org settings affect all users and functionality. Changing settings later may require data migration, user retraining, or rework.

**Better approach**: Configure org settings early in implementation. Review settings with stakeholders. Document configuration decisions.

## Ignoring Storage Limits

**Bad pattern**: Not monitoring storage usage, leading to storage limit issues and org constraints.

**Why it's bad**: Storage limits can prevent data creation, file uploads, or other operations. Resolving storage issues can be disruptive.

**Better approach**: Monitor storage usage proactively. Plan for storage growth. Implement data archiving strategies. Set up storage alerts.

## Not Using Sandboxes for Development

**Bad pattern**: Developing or testing directly in production org.

**Why it's bad**: Risks data corruption, user disruption, and production issues. Makes it difficult to test changes safely.

**Better approach**: Always use sandboxes or scratch orgs for development and testing. Deploy to production only after thorough testing.

## Over-Customizing Navigation

**Bad pattern**: Creating complex navigation structures that confuse users or don't match workflows.

**Why it's bad**: Poor navigation reduces user adoption and productivity. Complex navigation is difficult to maintain.

**Better approach**: Keep navigation simple and aligned with user workflows. Test navigation with end users. Iterate based on feedback.

## Not Documenting Configuration Decisions

**Bad pattern**: Making configuration decisions without documentation, leading to confusion and rework.

**Why it's bad**: Undocumented decisions are difficult to understand, maintain, or change. New team members struggle to understand org configuration.

**Better approach**: Document all configuration decisions. Maintain org documentation. Review and update documentation regularly.

# Real-World Scenarios

## Scenario 1 - New Org Setup

**Problem**: Setting up a new Salesforce org for a mid-size organization with 100 users, multi-currency requirements, and multiple languages.

**Context**: New org, 100 users, operations in 5 countries with different currencies, need to support 3 languages.

**Solution**:
- Configure company information with headquarters details
- Enable multi-currency with 5 currencies
- Configure 3 supported languages
- Set Lightning Experience as default
- Configure security settings per compliance requirements
- Set up storage monitoring

**Key decisions**: Configure multi-currency and multi-language early. Set Lightning Experience as default. Configure security settings per compliance requirements.

## Scenario 2 - Org Migration from Classic to Lightning

**Problem**: Migrating existing org from Classic to Lightning Experience with 200 users and custom Classic functionality.

**Context**: Existing org using Classic, need to migrate to Lightning, some custom Classic functionality may not be available in Lightning.

**Solution**:
- Assess Lightning Experience compatibility
- Identify Classic-only functionality
- Plan migration for Classic-only features
- Configure Lightning Experience preferences
- Train users on Lightning Experience
- Phase migration by user group

**Key decisions**: Assess compatibility before migration. Plan for Classic-only functionality. Phase migration to reduce risk.

## Scenario 3 - Multi-Org Environment Setup

**Problem**: Setting up multiple orgs (production, sandboxes, development) with consistent configuration and data management.

**Context**: Large organization with production org, multiple sandboxes, need consistent configuration across orgs.

**Solution**:
- Document org configuration standards
- Use change sets or DevOps for configuration deployment
- Maintain configuration consistency across orgs
- Set up sandbox refresh schedules
- Implement configuration management processes

**Key decisions**: Standardize configuration across orgs. Use deployment tools for consistency. Maintain configuration documentation.

# Checklist / Mental Model

## Org Setup Checklist

When setting up a Salesforce org, always configure:

1. **Company information**: Company name, address, organizational details
2. **Fiscal year**: Fiscal year settings if different from calendar year
3. **Currency**: Default currency and multi-currency if needed
4. **Language and locale**: Supported languages and locale settings
5. **Time zone**: Default time zone and user preferences
6. **UI settings**: Lightning Experience default, UI preferences
7. **Security settings**: Password policies, session settings, security preferences
8. **Email settings**: Email deliverability, templates, limits
9. **Feature toggles**: Review and enable/disable features
10. **Storage monitoring**: Set up monitoring and alerts

## Administration Mental Model

**Start with fundamentals**: Configure org settings, company information, and basic preferences early. These settings affect all users and functionality.

**Use sandboxes**: Always develop and test in sandboxes or scratch orgs. Never develop directly in production.

**Monitor proactively**: Monitor storage, limits, and org health proactively. Set up alerts and regular reviews.

**Document decisions**: Document all configuration decisions. Maintain org documentation for team knowledge.

**Iterate based on feedback**: Gather user feedback and iterate on configuration. Administration is an ongoing process, not a one-time setup.

## User Management

User management in Salesforce encompasses creating, configuring, and maintaining user accounts, assigning licenses, configuring access through profiles and permission sets, and managing user lifecycle. Effective user management ensures users have appropriate access while controlling licensing costs and maintaining security.

### User Accounts

**What it is**: Individual user accounts representing people who access the Salesforce org.

**Key characteristics**:
- Each user requires a license
- Users have profiles and permission sets for access control
- Users can be assigned roles for hierarchy and sharing
- Users have personal settings and preferences
- Users can be active or inactive

**User information**:
- Name and contact information
- Username (unique identifier)
- Email address
- License assignment
- Profile assignment
- Role assignment
- Permission set assignments

### User Licenses

**What it is**: License types that determine which standard objects and features users can access.

**Key license types**:
- Salesforce License: Full access to standard objects (Accounts, Contacts, Opportunities, Cases, etc.)
- Platform License: Access to custom objects and limited standard objects (typically Accounts, Contacts only)
- Service Cloud License: Access to Service Cloud objects (Cases, Knowledge) but not Sales Cloud objects
- Experience Cloud License: For external users accessing Experience Cloud sites
- Integration User License: Free API-only license for system integrations

**License impact**:
- Determines which standard objects are available
- Affects feature availability
- Impacts licensing costs
- Cannot be changed without license reassignment

**Best practice**: Assign licenses that match user needs. Use Platform licenses for users who don't need standard CRM objects. Use Integration User licenses for system integrations.

### Profiles

**What it is**: Collection of settings and permissions that control what users can see and do.

**Key characteristics**:
- Assigned to users (one profile per user)
- Contains object permissions, field permissions, and system permissions
- Contains UI configuration (tab visibility, record type visibility, page layout assignments)
- Contains license assignment (determines available objects)

**Profile components**:
- Object permissions (Read, Create, Edit, Delete)
- Field-level security (Read, Edit)
- System permissions (View All Data, Modify All Data, etc.)
- Tab visibility
- Record type visibility
- Page layout assignments
- App assignments

**Best practice**: Use profiles for UI configuration and base permissions. Use permission sets for incremental access. Minimize profile count by using permission sets for variations.

### Permission Sets

**What it is**: Collections of settings and permissions that extend user access beyond their profile.

**Key characteristics**:
- Assigned to users (multiple permission sets per user)
- Extends access granted by profile
- Provides incremental capability assignment
- Enables flexible access management without profile changes

**Permission set components**:
- Object permissions (additional access)
- Field-level security (additional access)
- System permissions (additional capabilities)
- App access
- Apex class access

**Best practice**: Use permission sets for incremental access. Grant additional capabilities through permission sets rather than creating multiple profiles. Use permission set groups for role-based assignment.

### Roles and Role Hierarchy

**What it is**: Hierarchical structure that determines data access through sharing and record visibility.

**Key characteristics**:
- Users assigned to roles in hierarchy
- Higher roles can see records owned by lower roles
- Used for sharing and record visibility
- Separate from permissions (profiles/permission sets)

**Role hierarchy impact**:
- Determines record visibility through hierarchy
- Affects sharing rule evaluation
- Used for reporting and data access
- Does not grant object or field permissions

**Best practice**: Design role hierarchy to match organizational structure. Use roles for sharing, not for permissions. Keep hierarchy manageable and aligned with business structure.

### User Lifecycle Management

**User creation**:
- Create user accounts with appropriate license and profile
- Assign roles and permission sets
- Configure user settings and preferences
- Set up user authentication (password, SSO)

**User maintenance**:
- Update user information as needed
- Modify profile and permission set assignments
- Update role assignments
- Manage user access changes

**User deactivation**:
- Deactivate users who no longer need access
- Transfer ownership of records
- Maintain user data for historical purposes
- Free up licenses for reassignment

**Best practice**: Establish user lifecycle management processes. Document user creation, maintenance, and deactivation procedures. Regularly review user access and license usage.

### User Creation Best Practices

**Creation checklist**:
1. Verify license availability
2. Assign appropriate license type
3. Assign profile matching user needs
4. Assign role in hierarchy
5. Assign permission sets for additional access
6. Configure user settings and preferences
7. Set up authentication (password or SSO)
8. Send welcome email with login instructions

**License optimization**:
- Use Platform licenses for users who don't need standard CRM objects
- Use Service Cloud licenses for service-focused users
- Use Experience Cloud licenses for external users
- Use Integration User licenses for system integrations

**Access configuration**:
- Start with base profile matching user role
- Add permission sets for incremental access
- Assign role in hierarchy for sharing
- Configure user settings and preferences

### Profile and Permission Set Strategy

**Profile strategy**:
- Minimize profile count (3-5 profiles typically sufficient)
- Use profiles for UI configuration and base permissions
- Use permission sets for access variations
- Keep profiles simple and focused

**Permission set strategy**:
- Create permission sets for specific roles or capabilities
- Use permission set groups for role-based assignment
- Grant incremental access through permission sets
- Document permission set purpose and usage

**Best practice**: Use permission set-driven architecture. Profiles provide base access; permission sets provide incremental capabilities. This approach reduces profile proliferation and enables flexible access management.

### Role Hierarchy Design

**Design principles**:
- Align hierarchy with organizational structure
- Keep hierarchy manageable (typically 5-10 levels)
- Use roles for sharing, not for permissions
- Design for data visibility needs

**Common patterns**:
- Executive → Management → Individual Contributors
- Department-based hierarchy
- Geographic hierarchy
- Functional hierarchy

**Best practice**: Design role hierarchy to match business structure. Use roles for record visibility and sharing. Don't use roles as substitute for permissions.

### User Access Management

**Access review process**:
- Regularly review user access and permissions
- Verify users have appropriate access for their roles
- Remove unnecessary access
- Document access changes

**Access audit**:
- Review profile and permission set assignments
- Review role assignments
- Review license usage
- Identify optimization opportunities

**Best practice**: Establish regular access review process. Audit user access periodically. Remove unnecessary access. Optimize license usage.

### User Management Common Pitfalls

**Over-Licensing Users**: Assigning full Salesforce licenses to users who only need Platform license capabilities increases costs without providing value. Evaluate user needs carefully and use Platform licenses strategically.

**Profile Proliferation**: Creating many profiles (20+) for different user access variations is difficult to maintain and increases complexity. Minimize profile count and use permission sets for access variations.

**Not Using Permission Sets**: Creating profiles for every access variation instead of using permission sets leads to profile proliferation and inflexible access management. Use permission sets for incremental access.

**Ignoring Role Hierarchy**: Not assigning users to roles or using roles incorrectly for permissions prevents proper record visibility. Assign all users to appropriate roles and design hierarchy for sharing.

**Not Managing User Lifecycle**: Creating users without processes for maintenance and deactivation leads to orphaned accounts and unnecessary license usage. Establish user lifecycle management processes.

# Key Terms & Definitions

- **Salesforce Administrator**: Primary role responsible for configuring, maintaining, and optimizing Salesforce orgs
- **Lightning Experience**: Modern Salesforce user interface with enhanced functionality
- **Salesforce Classic**: Legacy user interface still available for specific use cases
- **Sandbox**: Copy of production org used for development, testing, and training
- **Scratch Org**: Temporary, source-driven org for development, typically used with Salesforce DX
- **Company Information**: Basic org configuration including company name, address, and organizational details
- **Org Settings**: Organization-wide settings that affect all users and functionality
- **Multi-Currency**: Feature enabling multiple currencies in a single org
- **Multi-Language**: Feature enabling multiple languages in a single org
- **Storage Limits**: Platform limits on data storage, file storage, and Big Object storage
- **User Account**: Individual user account representing a person who accesses the Salesforce org
- **User License**: License type determining which standard objects and features users can access
- **Profile**: Collection of settings and permissions controlling what users can see and do
- **Permission Set**: Collection of settings and permissions extending user access beyond profile
- **Role**: Position in hierarchical structure determining data access through sharing
- **Role Hierarchy**: Hierarchical structure determining record visibility and sharing
- **User Lifecycle**: Process of user creation, maintenance, and deactivation

# RAG-Friendly Q&A Seeds

**Q:** What's the difference between Lightning Experience and Classic?

**A:** Lightning Experience is the modern Salesforce user interface with enhanced functionality, improved mobile experience, and advanced features. Classic is the legacy interface still available for specific use cases. Lightning Experience is the default and recommended interface for most users. Use Classic only when specific functionality isn't available in Lightning Experience.

**Q:** When should I use sandboxes vs. scratch orgs?

**A:** Use sandboxes for: (1) Development and testing that needs production-like environment, (2) User acceptance testing with production data subset, (3) Training environments. Use scratch orgs for: (1) Modern source-driven development workflows, (2) CI/CD pipelines, (3) Temporary development environments. Sandboxes are copies of production; scratch orgs are temporary and source-driven.

**Q:** How do I set up multi-currency in Salesforce?

**A:** Set up multi-currency by: (1) Enabling multi-currency in org settings, (2) Configuring currencies and conversion rates, (3) Setting default currency, (4) Configuring currency for users and records. Multi-currency enables different currencies in a single org and automatic currency conversion for reporting and calculations.

**Q:** What org settings should I configure first?

**A:** Configure first: (1) Company information (name, address, organizational details), (2) Fiscal year settings if different from calendar year, (3) Default currency and multi-currency if needed, (4) Language and locale settings, (5) Time zone settings, (6) Lightning Experience as default, (7) Security settings (password policies, session settings). These settings affect all users and functionality.

**Q:** How do I monitor storage usage in Salesforce?

**A:** Monitor storage usage by: (1) Reviewing storage usage in Setup → Company Information, (2) Setting up storage alerts, (3) Regularly reviewing data and file storage, (4) Planning for storage growth, (5) Implementing data archiving strategies for large data volumes. Proactive storage monitoring prevents storage limit issues.

**Q:** Should I develop directly in production?

**A:** No, never develop directly in production. Always use sandboxes or scratch orgs for development and testing. Developing in production risks data corruption, user disruption, and production issues. Deploy to production only after thorough testing in sandboxes.

**Q:** How do I configure multi-language support?

**A:** Configure multi-language by: (1) Enabling supported languages in org settings, (2) Translating field labels and values, (3) Translating picklist values, (4) Translating email templates and communications, (5) Configuring user language preferences. Multi-language enables different languages in a single org for global organizations.

**Q:** What's the difference between a profile and a permission set?

**A:** A profile is assigned to users (one per user) and contains base permissions, UI configuration, and license assignment. A permission set is assigned to users (multiple per user) and extends access granted by profile. Use profiles for base access and UI configuration. Use permission sets for incremental access and additional capabilities.

**Q:** When should I use a Platform license instead of a full Salesforce license?

**A:** Use Platform licenses for users who only need access to custom objects and don't need standard Sales or Service Cloud objects (Opportunities, Cases, Leads, etc.). Platform licenses are typically less expensive and suitable for custom application users or users who only need Accounts/Contacts access.

**Q:** How do I assign roles to users?

**A:** Assign roles to users in the user record. Roles determine record visibility through hierarchy and sharing. Users in higher roles can see records owned by users in lower roles. Use roles for sharing and record visibility, not for permissions.

**Q:** Can I assign multiple permission sets to a user?

**A:** Yes, users can have multiple permission sets assigned. Permission sets extend access granted by profile. Use multiple permission sets to grant incremental capabilities. Permission set groups can organize related permission sets for easier assignment.

**Q:** How do I deactivate a user?

**A:** Deactivate users in the user record by setting status to Inactive. Before deactivating, transfer ownership of records to other users if needed. Deactivated users cannot log in but their data is preserved. Deactivation frees up licenses for reassignment.

**Q:** What permissions do I need to create users?

**A:** You need "Manage Users" permission (typically in System Administrator profile) to create users. Users with this permission can create, edit, and deactivate users, assign licenses, profiles, and permission sets.

**Q:** How do I verify a user's access?

**A:** Verify user access by: (1) Using "Login as User" feature to test access, (2) Reviewing user's profile and permission set assignments, (3) Reviewing user's role in hierarchy, (4) Testing access to objects, fields, and records, (5) Using access reports to audit user permissions.

## Related Patterns

- [Permission Set Architecture](../security/permission-set-architecture.md) - Permission set-driven security patterns
- [Sharing Fundamentals](../security/sharing-fundamentals.md) - Organization-wide defaults and role hierarchy
- [Object Setup and Configuration](../data-modeling/object-setup-and-configuration.md) - Object and field configuration
- [Flow Patterns](flow-patterns.md) - Automation configuration patterns
- [Formulas and Validation Rules](formulas-validation-rules.md) - Declarative business logic

