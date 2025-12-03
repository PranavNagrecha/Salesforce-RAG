---
layout: default
title: Permission Set-Driven Security Architecture
description: Permission set-driven security architecture transitions from profile-centric to permission set-based access control, enabling flexible, modular security management
permalink: /rag/security/permission-set-architecture.html
level: Intermediate
tags:
  - security
  - permission-sets
  - access-control
  - architecture
last_reviewed: 2025-12-03
---

# Permission Set-Driven Security Architecture

## Overview

Permission set-driven security architecture transitions from profile-centric to permission set-based access control. This approach enables flexible, modular security management where profiles provide base permissions and permission sets grant additional capabilities.

**Core Principle**: Profiles provide base permissions for user roles. Permission sets grant additional capabilities for specific functions, features, or temporary access. This separation enables flexible, modular security management.

## Prerequisites

**Required Knowledge**:
- Understanding of Salesforce security model
- Familiarity with profiles and permission sets
- Knowledge of field-level security and object permissions
- Understanding of sharing and access control
- Knowledge of user management patterns

**Recommended Reading**:
- <a href="{{ '/rag/security/sharing-fundamentals.html' | relative_url }}">Sharing Fundamentals</a> - Fundamental sharing concepts
- <a href="{{ '/rag/development/admin-basics.html' | relative_url }}">Admin Basics</a> - User management and security basics
- <a href="{{ '/rag/integrations/integration-user-license-guide.html' | relative_url }}">Integration User License Guide</a> - Permission management for integration users

## When to Use Permission Set-Driven Architecture

### Use Permission Set-Driven Architecture When

- **Multiple user types**: Different user types need different combinations of permissions
- **Feature-based access**: Need to grant access to specific features or functions
- **Temporary access**: Need to grant temporary permissions (projects, training)
- **Complex permission combinations**: Many different permission combinations needed
- **Modular security**: Want to manage security in modular, reusable components
- **Reduced profile count**: Want to reduce number of profiles (easier management)
- **Flexible access control**: Need flexible, granular access control

### Avoid Permission Set-Driven Architecture When

- **Simple org**: Small org with few user types and simple permission needs
- **Legacy system**: Existing profile-centric system that works well
- **Migration cost**: Migration cost outweighs benefits
- **Limited admin resources**: Don't have resources to manage permission sets

## Architecture Pattern

### Profile Strategy

**Minimal Profiles**: Create minimal profiles that provide base permissions for user roles.

**Profile Structure**:
- **Base Permissions**: Object-level access (Read, Create, Edit, Delete)
- **Standard App Access**: Access to standard Salesforce apps
- **Login Hours**: Restrict login hours if needed
- **IP Restrictions**: Restrict IP ranges if needed

**Profile Naming**:
- `System Administrator` - Full access (one profile)
- `Standard User` - Base user permissions
- `Read Only User` - Read-only access
- `Integration User` - API-only access (if using Integration User License)

### Permission Set Strategy

**Feature-Based Permission Sets**: Create permission sets for specific features or functions.

**Permission Set Categories**:
1. **Feature Permission Sets**: Grant access to specific features
   - `Case Management Access`
   - `Opportunity Management Access`
   - `Report Builder Access`
   - `Data Export Access`

2. **Object Permission Sets**: Grant access to specific objects
   - `Custom Object A Access`
   - `Custom Object B Access`
   - `External Object Access`

3. **Field Permission Sets**: Grant access to specific fields
   - `Sensitive Field Access`
   - `Financial Field Access`
   - `PII Field Access`

4. **Function Permission Sets**: Grant access for specific job functions
   - `Sales Manager Access`
   - `Support Agent Access`
   - `Data Analyst Access`

5. **Temporary Permission Sets**: Grant temporary access
   - `Project Alpha Access` (with expiration)
   - `Training Access` (temporary)

**Permission Set Naming Convention**:
- Format: `{Feature/Function} - {Access Type}`
- Examples:
  - `Case Management - Full Access`
  - `Financial Data - Read Only`
  - `Report Builder - Create Access`

## Implementation Pattern

### Step 1: Audit Current Profiles

**Actions**:
1. List all existing profiles
2. Document permissions for each profile
3. Identify permission combinations
4. Identify redundant profiles
5. Document user assignments

**Output**: Profile audit document with permission matrix

### Step 2: Design Minimal Profiles

**Actions**:
1. Identify base user roles (e.g., Standard User, Read Only User)
2. Define base permissions for each role
3. Create minimal profiles with base permissions only
4. Remove feature-specific permissions from profiles

**Output**: Minimal profile structure

### Step 3: Create Feature Permission Sets

**Actions**:
1. Identify features and functions requiring permissions
2. Create permission sets for each feature/function
3. Grant appropriate object, field, and system permissions
4. Document permission set purpose and usage

**Output**: Feature permission sets

### Step 4: Migrate Users

**Actions**:
1. Assign users to minimal profiles
2. Assign feature permission sets to users
3. Test user access
4. Verify permissions work correctly
5. Document user-to-permission-set assignments

**Output**: Migrated user assignments

### Step 5: Maintain and Iterate

**Actions**:
1. Create new permission sets for new features
2. Update permission sets as features evolve
3. Remove unused permission sets
4. Document permission set changes
5. Review and audit regularly

**Output**: Ongoing maintenance process

## Best Practices

### Permission Set Design

- **Single Purpose**: Each permission set should have a single, clear purpose
- **Granular**: Create granular permission sets (easier to combine)
- **Documented**: Document purpose, usage, and assignments
- **Named Clearly**: Use clear, descriptive names
- **Grouped**: Group related permissions together

### Assignment Strategy

- **User Assignment**: Assign permission sets to users based on job function
- **Group Assignment**: Use permission set groups for common combinations
- **Temporary Access**: Use permission sets for temporary access (with expiration)
- **Audit Trail**: Track permission set assignments for compliance

### Maintenance

- **Regular Review**: Review permission sets quarterly
- **Remove Unused**: Remove unused permission sets
- **Update Documentation**: Keep documentation current
- **Test Changes**: Test permission set changes before deployment
- **Version Control**: Track permission set changes in version control

## Permission Set Groups

**Purpose**: Group related permission sets for easier assignment.

**Use Cases**:
- Common permission combinations
- Role-based access (e.g., "Sales Manager" group)
- Feature bundles (e.g., "Case Management Suite")

**Example**:
- Permission Set Group: `Sales Manager Access`
  - Permission Set: `Opportunity Management - Full Access`
  - Permission Set: `Report Builder - Create Access`
  - Permission Set: `Forecast Management - View Access`

## Migration Considerations

### From Profile-Centric to Permission Set-Driven

**Migration Steps**:
1. **Audit**: Audit current profiles and permissions
2. **Design**: Design minimal profiles and permission sets
3. **Create**: Create new profiles and permission sets in sandbox
4. **Test**: Test with sample users
5. **Migrate**: Migrate users in phases
6. **Verify**: Verify permissions work correctly
7. **Deprecate**: Deprecate old profiles (after migration complete)

**Challenges**:
- **User Impact**: Users may need multiple permission sets
- **Assignment Management**: More permission sets to manage
- **Testing**: More complex testing (profile + permission set combinations)
- **Documentation**: More documentation needed

**Benefits**:
- **Flexibility**: More flexible permission management
- **Modularity**: Modular, reusable permission components
- **Reduced Profiles**: Fewer profiles to manage
- **Easier Updates**: Update permissions without changing profiles

## Edge Cases and Limitations

### Limitations

- **Profile Limits**: Still need profiles (cannot eliminate profiles)
- **Permission Set Limits**: 1000 permission sets per org
- **Assignment Limits**: Users can have up to 1000 permission set assignments
- **Complexity**: More complex than profile-centric approach
- **Testing**: More complex testing scenarios

### Edge Cases

- **Conflicting Permissions**: Permission sets can conflict (last assigned wins)
- **Profile Override**: Profiles can override permission set permissions in some cases
- **Sharing**: Permission sets don't grant sharing access (use sharing rules)
- **License Limits**: Permission sets respect user license limits

## Related Patterns

- <a href="{{ '/rag/security/sharing-fundamentals.html' | relative_url }}">Sharing Fundamentals</a> - Fundamental sharing concepts and patterns
- <a href="{{ '/rag/security/sharing-rules-and-manual-sharing.html' | relative_url }}">Sharing Rules and Manual Sharing</a> - Sharing rules and manual sharing patterns
- <a href="{{ '/rag/development/admin-basics.html' | relative_url }}">Admin Basics</a> - User management and security administration
- <a href="{{ '/rag/integrations/integration-user-license-guide.html' | relative_url }}">Integration User License Guide</a> - Permission management for integration users

## Q&A

### Q: What is permission set-driven security architecture?

**A**: **Permission set-driven security architecture** is an approach where: (1) **Profiles provide base permissions** (minimal, role-based permissions), (2) **Permission sets grant additional capabilities** (feature-specific, function-specific permissions), (3) **Modular security management** (permissions managed in reusable components), (4) **Flexible access control** (combine permission sets for different access levels). This approach enables flexible, modular security management.

### Q: Why use permission set-driven architecture instead of profiles?

**A**: Benefits include: (1) **Flexibility** (combine permission sets for different access levels), (2) **Modularity** (reusable permission components), (3) **Reduced profiles** (fewer profiles to manage), (4) **Easier updates** (update permissions without changing profiles), (5) **Temporary access** (grant temporary permissions via permission sets), (6) **Feature-based access** (grant access to specific features). Permission sets provide more granular, flexible access control.

### Q: How do I design minimal profiles?

**A**: Design minimal profiles by: (1) **Identify base roles** (Standard User, Read Only User, etc.), (2) **Define base permissions** (object-level access, standard app access), (3) **Remove feature-specific permissions** (move to permission sets), (4) **Keep profiles minimal** (only base permissions needed for role), (5) **Document profile purpose** (clear documentation). Minimal profiles provide base permissions, permission sets provide additional capabilities.

### Q: How do I create feature-based permission sets?

**A**: Create feature-based permission sets by: (1) **Identify features** (Case Management, Opportunity Management, etc.), (2) **Define permissions** (object, field, system permissions), (3) **Create permission sets** (one per feature), (4) **Grant appropriate permissions** (object access, field access, system permissions), (5) **Document purpose** (clear naming and documentation). Each permission set should have a single, clear purpose.

### Q: How do I migrate from profile-centric to permission set-driven?

**A**: Migrate by: (1) **Audit current profiles** (document all permissions), (2) **Design minimal profiles** (base permissions only), (3) **Create permission sets** (feature-based permission sets), (4) **Test in sandbox** (test with sample users), (5) **Migrate users in phases** (assign new profiles and permission sets), (6) **Verify permissions** (test user access), (7) **Deprecate old profiles** (after migration complete). Migration should be done in phases with thorough testing.

### Q: What are permission set groups?

**A**: **Permission set groups** group related permission sets for easier assignment. Use for: (1) **Common combinations** (frequently used permission set combinations), (2) **Role-based access** (e.g., "Sales Manager" group), (3) **Feature bundles** (e.g., "Case Management Suite"). Permission set groups simplify assignment of multiple related permission sets.

### Q: What are the limitations of permission set-driven architecture?

**A**: Limitations include: (1) **Profile limits** (still need profiles, cannot eliminate), (2) **Permission set limits** (1000 permission sets per org), (3) **Assignment limits** (users can have up to 1000 permission set assignments), (4) **Complexity** (more complex than profile-centric), (5) **Testing** (more complex testing scenarios). Consider these limitations when designing permission set-driven architecture.

### Q: How do I handle conflicting permissions between permission sets?

**A**: Handle conflicts by: (1) **Last assigned wins** (most recently assigned permission set takes precedence), (2) **Design carefully** (avoid conflicting permissions in permission sets), (3) **Document conflicts** (document known conflicts), (4) **Test combinations** (test permission set combinations), (5) **Use permission set groups** (group compatible permission sets). Avoid conflicting permissions through careful design and testing.
