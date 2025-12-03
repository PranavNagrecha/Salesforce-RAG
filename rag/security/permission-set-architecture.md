---
title: "Permission Set-Driven Security Architecture"
level: "Advanced"
tags:
  - security
  - permission-sets
  - access-control
  - architecture
last_reviewed: "2025-01-XX"
---

# Permission Set-Driven Security Architecture

## Overview

Permission set-driven security architecture transitions from profile-centric to permission set-based access control. This pattern provides more granular permission management, especially at scale, and enables flexible role-based access control without creating multiple profiles.

## Prerequisites

**Required Knowledge**:
- Understanding of Salesforce security model (Profiles, Permission Sets, Sharing)
- Knowledge of object-level and field-level security
- Understanding of user management and license types
- Familiarity with role hierarchy and sharing rules

**Recommended Reading**:
- [Sharing Fundamentals](/rag/security/sharing-fundamentals.html) - Organization-wide defaults and role hierarchy
- [Admin Basics](/rag/development/admin-basics.html) - User management and basic administration
- [Integration User License Guide](/rag/integrations/integration-user-license-guide.html) - Permission management for integration users

## Architecture Pattern

### Profile Structure

Profiles contain minimal permissions focused on UI configuration:

- **License Assignment**: User license type (Salesforce, Experience Cloud, etc.)
- **Tab Visibility**: Which tabs users can see
- **Record Type Visibility**: Which record types are available
- **Layout Assignments**: Which page layouts are used
- **Minimal Object Permissions**: Only base object access required for license

### Permission Set Structure

Permission Sets contain comprehensive access control:

- **Object Permissions**: Read, Create, Edit, Delete permissions for all objects
- **Field Permissions**: Field-level security for all fields
- **Class Access**: Apex class access for custom code
- **User Permissions**: System permissions and feature access
- **App Access**: Application access assignments

### Permission Set Groups

Permission Set Groups organize related permission sets:

- Group related permission sets for role-based assignment
- Define roles through permission set groups (advisor, admissions officer, case worker, external partner staff)
- Enable incremental capability assignment
- Support role-based access control without multiple profiles

## Key Architectural Decisions

### Profiles = UI Configuration

Profiles define what users see, not what they can access. This separation enables:

- Consistent UI experience across user types
- Flexible permission management without profile changes
- Easier permission updates through permission sets
- Reduced profile proliferation

### Permission Sets = Access Control

All permissions granted through permission sets. This enables:

- Granular permission management at scale
- Incremental capability assignment
- Role-based access control without profile changes
- Easier permission auditing and reporting

### No Delete Permissions for Community Users

All `allowDelete` set to `false` for community users. This provides:

- Data integrity protection
- Prevention of accidental data loss
- Compliance with data retention requirements
- Reduced risk of data corruption

## Implementation Pattern

### Permission Restructuring

Complete migration from profile-centric to permission set-based model:

- **Migration Plan**: Move 406 field permissions from profiles to permission sets
- **Profile Cleanup**: Remove object and field permissions from profiles
- **Permission Set Creation**: Create permission sets for each role and capability
- **Permission Set Groups**: Organize permission sets into groups for role assignment

### Permission Set Design

Design permission sets for specific roles and capabilities:

- **Role-Based Permission Sets**: Permission sets for specific roles (advisor, case worker, external partner staff)
- **Capability Permission Sets**: Permission sets for specific capabilities (special object access, sensitive fields)
- **Incremental Assignment**: Grant incremental capabilities through additional permission sets
- **Documentation**: Document permission set purpose and usage

### Permission Set Assignment

Assign permission sets based on user roles and needs:

- **Automatic Assignment**: Use permission set groups for automatic assignment
- **Manual Assignment**: Assign individual permission sets for special cases
- **Audit Trail**: Track permission set assignments for compliance
- **Regular Review**: Review and update permission set assignments periodically

## Best Practices

### Permission Set Naming

Use consistent naming conventions:

- Include role or capability in permission set name
- Use descriptive names that indicate purpose
- Follow organizational naming standards
- Document naming conventions for team

### Permission Set Organization

Organize permission sets logically:

- Group related permission sets into permission set groups
- Create permission sets for specific roles
- Create capability permission sets for special access
- Document permission set relationships

### Permission Management

Manage permissions systematically:

- Document all permission set assignments
- Review permission sets regularly for unused permissions
- Remove permissions when no longer needed
- Audit permission set usage periodically

### Security Review

Conduct regular security reviews:

- Review permission set assignments for all users
- Identify over-privileged users
- Remove unnecessary permissions
- Document security review findings

## Migration Strategy

### Assessment Phase

Assess current permission model:

- Inventory all profile permissions
- Identify permission set opportunities
- Document current permission structure
- Plan migration approach

### Design Phase

Design permission set structure:

- Create permission sets for each role
- Create capability permission sets
- Organize into permission set groups
- Document permission set design

### Migration Phase

Execute migration:

- Create permission sets with required permissions
- Assign permission sets to users
- Remove permissions from profiles
- Test permission assignments

### Validation Phase

Validate migration:

- Verify all users have required access
- Test permission set assignments
- Audit permission changes
- Document migration results

## Compliance Considerations

### Government Cloud Compliance

Permission set architecture supports compliance:

- Granular access control for audit requirements
- Permission set assignment tracking for compliance
- Regular access reviews for certification
- Documentation for security reviews

### Data Access Controls

Permission sets enable fine-grained data access:

- Field-level security for sensitive data
- Object-level security for data protection
- Record-level security through sharing rules
- Compliance with data access requirements

### Audit Trail

Permission set assignments provide audit trail:

- Track all permission set assignments
- Monitor permission changes
- Report on user access
- Support compliance audits

## Tradeoffs

### Advantages

- **Granular Control**: Fine-grained permission management
- **Flexibility**: Easy to grant incremental capabilities
- **Scalability**: Efficient permission management at scale
- **Maintainability**: Easier to update permissions without profile changes

### Challenges

- **Migration Effort**: Significant effort to migrate from profile-centric model
- **Complexity**: More permission sets to manage
- **Documentation**: Requires comprehensive documentation
- **Training**: Team needs training on permission set management

## When to Use This Pattern

Use permission set-driven security when:

- Managing permissions for large user populations (40,000+ users)
- Need granular permission management
- Require flexible role-based access control
- Need to grant incremental capabilities
- Compliance requires detailed permission tracking

## When Not to Use This Pattern

Avoid permission set-driven security when:

- Small user population with simple permission needs
- Profile-centric model meets all requirements
- Migration effort outweighs benefits
- Team lacks expertise in permission set management

## Q&A

### Q: What is the difference between Profiles and Permission Sets?

**A**: **Profiles** define UI configuration (tab visibility, record type visibility, layout assignments) and assign user licenses. **Permission Sets** contain comprehensive access control (object permissions, field permissions, class access, user permissions). In permission set-driven architecture, profiles = UI configuration, permission sets = access control.

### Q: Why should I use Permission Set Groups?

**A**: Permission Set Groups organize related permission sets for role-based assignment, define roles through permission set groups (e.g., advisor, admissions officer), enable incremental capability assignment, and support role-based access control without creating multiple profiles. They simplify permission management at scale.

### Q: How do I migrate from profile-centric to permission set-driven security?

**A**: Create permission sets for each role, move object and field permissions from profiles to permission sets, organize permission sets into Permission Set Groups, assign Permission Set Groups to users, test thoroughly, and update profiles to contain only UI configuration. Migrate incrementally and document the process.

### Q: Can I still use profiles for permissions?

**A**: Yes, but in permission set-driven architecture, profiles should contain minimal permissions focused on UI configuration. Comprehensive access control should be in Permission Sets. This separation enables flexible permission management without profile changes.

### Q: What are the benefits of permission set-driven security?

**A**: Benefits include granular permission management, flexible role-based access control without multiple profiles, easier permission updates through permission sets, reduced profile proliferation, better compliance tracking, and support for incremental capability assignment.

### Q: How many Permission Sets can a user have?

**A**: A user can have up to **100 Permission Set assignments** (including Permission Set Groups). This is typically more than sufficient for most use cases. Permission Set Groups count as a single assignment but can contain multiple permission sets.

### Q: What is the difference between Permission Sets and Permission Set Groups?

**A**: **Permission Sets** contain individual permissions (object, field, class, user permissions). **Permission Set Groups** organize multiple permission sets together for role-based assignment. Assign Permission Set Groups to users rather than individual permission sets for better organization.

### Q: How do I handle permission changes in permission set-driven architecture?

**A**: Update permission sets (not profiles) to change permissions, assign or unassign permission sets to users as needed, use Permission Set Groups for role-based changes, test permission changes thoroughly, and document permission changes for compliance. Changes take effect immediately upon assignment.

## Related Patterns

- [Sharing Fundamentals](/rag/security/sharing-fundamentals.html) - Organization-wide defaults and role hierarchy
- [Sharing Rules and Manual Sharing](/rag/security/sharing-rules-and-manual-sharing.html) - Sharing rules and manual sharing patterns
- [Sharing Sets and Portals](/rag/security/sharing-sets-and-portals.html) - Experience Cloud sharing patterns
- [Admin Basics](/rag/development/admin-basics.html) - User management and basic administration
- [Integration User License Guide](/rag/integrations/integration-user-license-guide.html) - Permission management for integration users

