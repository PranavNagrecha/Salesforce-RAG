---
title: "Salesforce Sharing Fundamentals"
level: "Intermediate"
tags:
  - salesforce
  - security
  - sharing
  - org-wide-defaults
  - role-hierarchy
last_reviewed: "2025-01-XX"
---

# Salesforce Sharing Fundamentals

## Overview

This document covers the fundamental concepts of Salesforce sharing, including Org-Wide Defaults (OWD), Role Hierarchy, and View All/Modify All permissions. These are the foundational mechanisms that control record-level access in Salesforce.

**Related Patterns**: 
- See `rag/security/sharing-rules-and-manual-sharing.md` for sharing rules and manual sharing
- See `rag/security/sharing-sets-and-portals.md` for Experience Cloud sharing patterns
- See `rag/security/permission-set-architecture.md` for permission context

## Prerequisites

**Required Knowledge**:
- Understanding of Salesforce security model (Profiles, Permission Sets)
- Knowledge of object-level and field-level security
- Understanding of user management and roles
- Familiarity with record ownership concepts

**Recommended Reading**:
- [Permission Set Architecture](permission-set-architecture.md) - Permission management patterns
- [Admin Basics](../development/admin-basics.md) - User management and basic administration
- [Sharing Rules and Manual Sharing](sharing-rules-and-manual-sharing.md) - Advanced sharing patterns

## Sharing Model Fundamentals

### How Salesforce Sharing Works

Salesforce uses a layered security model where sharing determines **record-level access** after object and field permissions are evaluated:

1. **Object Permissions**: User must have Read permission on the object
2. **Field-Level Security (FLS)**: User must have Read permission on the field
3. **Sharing**: User must have record-level access through sharing mechanisms

**Key Principle**: Sharing rules determine **which records** a user can see, not **which fields** they can see. Field-level security is separate and evaluated independently.

### Order of Evaluation

Salesforce evaluates sharing in this order:

1. **Org-Wide Defaults (OWD)**: Baseline access level
2. **Role Hierarchy**: Users above record owner in hierarchy
3. **Sharing Rules**: Owner-based, criteria-based, territory-based
4. **Manual Sharing**: Individual record sharing
5. **Apex Managed Sharing**: Programmatic sharing
6. **View All / Modify All**: Object-level permissions that bypass sharing
7. **View All Data / Modify All Data**: System-level permissions that bypass all sharing

**Important**: The most permissive access wins. If any mechanism grants access, the user can see the record.

### Sharing vs. Permissions Distinction

- **Permissions**: Control what objects and fields users can access (object-level and field-level)
- **Sharing**: Controls which specific records users can access (record-level)

A user can have Read permission on the Account object but still not see specific Account records if sharing rules don't grant access.

## Org-Wide Defaults (OWD)

### What OWD Controls

Org-Wide Defaults establish the baseline level of access to records for all users within the organization. OWD settings determine the default access level for each object before any sharing rules are applied.

### OWD Settings

#### Private

**What It Means**: Only record owners and users above them in the role hierarchy can access records.

**Use When**:
- Data is sensitive and should be restricted by default
- Need maximum control over record access
- Compliance requires restrictive default access

**Impact**: Requires sharing rules to grant access beyond owners and role hierarchy.

**Example**: Cases are Private by default. Only the case owner and their manager can see the case unless sharing rules grant additional access.

#### Public Read Only

**What It Means**: All users can view records, but only owners and users above them in the role hierarchy can edit.

**Use When**:
- Data should be visible to all users but editable only by owners
- Need transparency across the organization
- Collaboration requires visibility but not edit access

**Impact**: Sharing rules can grant edit access, but read access is already granted to all users.

**Example**: Products are Public Read Only. All users can see product information, but only product managers can edit.

#### Public Read/Write

**What It Means**: All users can view and edit all records.

**Use When**:
- Data is non-sensitive and collaborative
- Need maximum collaboration and transparency
- Data is reference data that all users should maintain

**Impact**: No sharing rules needed for basic access. All users can see and edit all records.

**Example**: Knowledge articles might be Public Read/Write for collaborative editing.

### OWD for Standard vs. Custom Objects

- **Standard Objects**: Some standard objects have fixed OWD (e.g., User object is always Private)
- **Custom Objects**: Can be set to Private, Public Read Only, or Public Read/Write
- **Restrictions**: Some objects cannot be set to Public Read/Write (e.g., Cases, Leads)

### Impact on Sharing Rule Requirements

- **Private OWD**: Requires sharing rules for any access beyond owners and role hierarchy
- **Public Read Only**: Sharing rules needed only for edit access (read is already granted)
- **Public Read/Write**: Sharing rules not needed for basic access (all users already have access)

### Best Practices for OWD Selection

- **Start Restrictive**: Begin with Private OWD and open access through sharing rules as needed
- **Security First**: Choose the most restrictive OWD that meets business requirements
- **Document Decisions**: Document why each object has its OWD setting
- **Review Regularly**: Review OWD settings as business requirements change
- **Consider Compliance**: More restrictive OWD supports compliance requirements

## Role Hierarchy

### How Role Hierarchy Grants Access

Role hierarchy allows users higher in the hierarchy to access records owned by users below them. This structure mirrors the organization's reporting structure.

**Key Principle**: Role hierarchy grants access **downward** - managers can see subordinate records, but subordinates cannot see manager records (unless sharing rules grant access).

### Role Hierarchy vs. Sharing Rules

- **Role Hierarchy**: Automatic access based on organizational structure
- **Sharing Rules**: Explicit access grants based on criteria or ownership

**When Role Hierarchy is Sufficient**:
- Organizational structure matches access requirements
- Managers need to see all subordinate records
- Simple hierarchical access patterns

**When Sharing Rules are Needed**:
- Cross-functional access requirements
- Team-based access patterns
- Criteria-based access (e.g., region, department)
- Access patterns that don't follow organizational hierarchy

### Limitations of Role Hierarchy

- **One-Way Access**: Only grants access downward, not upward or sideways
- **Organizational Structure Dependency**: Access tied to organizational reporting structure
- **No Criteria-Based Access**: Cannot grant access based on record field values
- **No Cross-Functional Access**: Cannot grant access across different branches of hierarchy

### Best Practices for Role Hierarchy Design

- **Mirror Organization**: Design role hierarchy to mirror actual organizational structure
- **Keep It Simple**: Avoid overly complex hierarchies that are hard to maintain
- **Document Structure**: Document role hierarchy and access patterns
- **Review Regularly**: Review role hierarchy as organization changes
- **Use Public Groups**: Use public groups for non-hierarchical access patterns

## View All / Modify All Permissions

### View All Permission

#### What It Does

View All permission grants users the ability to view all records of a particular object, regardless of sharing settings. It bypasses all sharing rules and org-wide defaults.

**Scope**: Object-level permission that applies to all records of the object.

**Granted Through**: Profiles or Permission Sets.

#### When to Use

- **System Administrators**: Administrators who need to see all records
- **Reporting Users**: Users who need access to all records for reporting
- **Support Teams**: Support teams that need visibility into all cases
- **Audit and Compliance**: Users who need to audit all records

#### Security Implications

- **Bypasses All Sharing**: View All bypasses all sharing mechanisms
- **Broad Access**: Grants access to all records, including sensitive data
- **No Granular Control**: Cannot restrict access to specific records
- **Audit Considerations**: All access is logged, but access is very broad

#### Best Practices

- **Use Sparingly**: Only grant View All when absolutely necessary
- **Document Justification**: Document why View All is needed
- **Regular Review**: Review View All permissions regularly
- **Consider Alternatives**: Consider sharing rules or role hierarchy as alternatives
- **Monitor Usage**: Monitor who has View All and why

### Modify All Permission

#### What It Does

Modify All permission grants users the ability to view, edit, delete, and transfer all records of a particular object, regardless of sharing settings. It bypasses all sharing rules and org-wide defaults.

**Scope**: Object-level permission that applies to all records of the object.

**Granted Through**: Profiles or Permission Sets.

#### When to Use

- **System Administrators**: Administrators who need to manage all records
- **Data Management Teams**: Teams that need to maintain all records
- **Migration and Integration**: Users who need to update all records during migrations

#### Security Implications

- **Bypasses All Sharing**: Modify All bypasses all sharing mechanisms
- **Full Access**: Grants full CRUD access to all records
- **Data Risk**: High risk of accidental data modification or deletion
- **No Granular Control**: Cannot restrict access to specific records

#### Best Practices

- **Extreme Caution**: Use Modify All with extreme caution
- **Limited Assignment**: Assign to very few users
- **Document Justification**: Document why Modify All is needed
- **Regular Review**: Review Modify All permissions regularly
- **Consider Alternatives**: Consider sharing rules with Read/Write access as alternatives
- **Monitor Changes**: Monitor all changes made by users with Modify All

## View All Data / Modify All Data Permissions

### System-Level Permissions

View All Data and Modify All Data are system-level permissions that provide access to all records across all objects in the organization.

### What They Grant

#### View All Data

- **Scope**: All records across all objects
- **Access Level**: Read access to all records
- **Bypasses**: All sharing rules, org-wide defaults, and object permissions

#### Modify All Data

- **Scope**: All records across all objects
- **Access Level**: Full CRUD access to all records
- **Bypasses**: All sharing rules, org-wide defaults, and object permissions

### When to Use

- **System Administrators**: Primary use case for system administrators
- **Integration Users**: Service accounts that need to access all data for integrations
- **Data Migration**: Users performing data migrations
- **Emergency Access**: Emergency access for critical situations

### Security Implications

- **Maximum Access**: Grants maximum possible access to all data
- **Bypasses All Security**: Bypasses all security mechanisms
- **High Risk**: Highest risk permissions in Salesforce
- **Audit Critical**: All access must be audited

### Best Practices and Restrictions

- **Minimal Assignment**: Assign to absolute minimum number of users
- **Service Accounts Only**: Consider service accounts for integrations
- **Time-Limited**: Use time-limited access when possible
- **Document Justification**: Document why these permissions are needed
- **Regular Review**: Review assignments regularly (quarterly minimum)
- **Monitor All Activity**: Monitor all activity by users with these permissions
- **Compliance Considerations**: Ensure compliance with data access requirements
- **Separation of Duties**: Separate View All Data from Modify All Data when possible

## View All Fields / Modify All Fields Permissions

### Field-Level Permissions That Bypass FLS

View All Fields and Modify All Fields are field-level permissions that bypass field-level security (FLS) restrictions.

#### View All Fields

- **What It Does**: Allows users to view all fields of a record, including those restricted by FLS
- **Scope**: All fields across all objects
- **Bypasses**: Field-level security read restrictions

#### Modify All Fields

- **What It Does**: Allows users to edit all fields of a record, including those restricted by FLS
- **Scope**: All fields across all objects
- **Bypasses**: Field-level security edit restrictions

### When to Use

- **System Administrators**: Administrators who need to see/edit all fields
- **Data Management**: Users managing data who need access to all fields
- **Reporting and Analytics**: Users who need access to all fields for reporting
- **Integration Users**: Service accounts that need to read/write all fields

### Security Implications

- **Bypasses FLS**: Bypasses all field-level security restrictions
- **Sensitive Data Access**: May grant access to sensitive fields (SSN, credit card numbers)
- **Compliance Risk**: May violate compliance requirements if sensitive fields are exposed
- **Audit Considerations**: All field access is logged

### Best Practices

- **Use Sparingly**: Only grant when absolutely necessary
- **Document Justification**: Document why these permissions are needed
- **Regular Review**: Review assignments regularly
- **Consider FLS Alternatives**: Consider field-level security as alternative
- **Monitor Usage**: Monitor who has these permissions and why
- **Compliance Review**: Ensure compliance with data protection requirements

## Q&A

### Q: What is the difference between Org-Wide Defaults and Role Hierarchy?

**A**: Org-Wide Defaults (OWD) establish the baseline level of access for all users before any sharing rules are applied. Role Hierarchy grants additional access based on organizational structure - users higher in the hierarchy can access records owned by users below them. OWD sets the foundation; role hierarchy extends access within that foundation.

### Q: When should I use Private OWD vs Public Read Only vs Public Read/Write?

**A**: Use **Private** when data is sensitive and should be restricted by default. Use **Public Read Only** when data should be visible to all users but editable only by owners. Use **Public Read/Write** when data is non-sensitive, collaborative, and all users should be able to maintain it. Start with Private and open access through sharing rules as needed.

### Q: How does Role Hierarchy grant access?

**A**: Role Hierarchy grants access **downward** - managers can see subordinate records, but subordinates cannot see manager records (unless sharing rules grant access). The hierarchy mirrors the organizational reporting structure, automatically granting access based on position in the hierarchy.

### Q: What is the difference between View All and View All Data?

**A**: **View All** is an object-level permission that grants access to all records of a specific object, bypassing sharing for that object only. **View All Data** is a system-level permission that grants read access to all records across all objects in the organization, bypassing all security mechanisms.

### Q: Should I use View All/Modify All permissions?

**A**: Use View All/Modify All **sparingly** and only when absolutely necessary. These permissions bypass all sharing mechanisms and grant broad access. Consider alternatives like sharing rules or role hierarchy first. Document justification and review assignments regularly.

### Q: How do View All Fields and Modify All Fields differ from Field-Level Security?

**A**: Field-Level Security (FLS) restricts access to specific fields based on profiles or permission sets. View All Fields and Modify All Fields are permissions that **bypass** FLS restrictions, allowing users to see/edit all fields regardless of FLS settings. Use these permissions with extreme caution as they may expose sensitive data.

### Q: What is the order of sharing evaluation?

**A**: Salesforce evaluates sharing in this order: 1) Org-Wide Defaults, 2) Role Hierarchy, 3) Sharing Rules, 4) Manual Sharing, 5) Apex Managed Sharing, 6) View All/Modify All, 7) View All Data/Modify All Data. The most permissive access wins - if any mechanism grants access, the user can see the record.

### Q: Can I change OWD settings after records are created?

**A**: Yes, but changing OWD to a more restrictive setting (e.g., from Public Read/Write to Private) may remove access that users previously had. Review sharing rules and role hierarchy to ensure users still have appropriate access after the change. Test thoroughly before making changes in production.

## Related Patterns

- **Sharing Rules and Manual Sharing**: See `rag/security/sharing-rules-and-manual-sharing.md` for sharing rules, manual sharing, and Apex managed sharing
- **Sharing Sets and Portals**: See `rag/security/sharing-sets-and-portals.md` for Experience Cloud sharing patterns
- **Permission Set Architecture**: See `rag/security/permission-set-architecture.md` for permission context

## When to Use This Document

- Understanding the fundamentals of Salesforce sharing
- Setting Org-Wide Defaults for objects
- Designing role hierarchy for access control
- Deciding when to use View All/Modify All permissions
- Understanding the order of sharing evaluation

