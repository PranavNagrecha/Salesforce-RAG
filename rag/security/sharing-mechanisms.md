# Salesforce Sharing Mechanisms

## Overview

This document provides a comprehensive guide to all Salesforce sharing mechanisms, including how they work, when to use each type, implementation patterns, and best practices. This covers both internal user sharing and Experience Cloud (Community) sharing patterns.

**Related Patterns**: See `rag/security/permission-set-architecture.md` for permission context, `rag/architecture/portal-architecture.md` for portal sharing patterns, `rag/data-modeling/case-management-data-model.md` for multi-tenant sharing examples, and `rag/identity-sso/multi-tenant-identity-architecture.md` for identity-based sharing.

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

## Sharing Rules

Sharing rules extend access beyond OWD and role hierarchy settings. They provide exceptions to OWD settings by granting additional access to specific users or groups.

### Owner-Based Sharing Rules

#### How Owner-Based Rules Work

Owner-based sharing rules share records owned by specific users or roles with other users, roles, or groups.

**Configuration**:
- **Rule Name**: Descriptive name for the sharing rule
- **Share With**: Users, roles, roles and subordinates, or public groups
- **Based on**: Record owner's role or record owner
- **Access Level**: Read Only or Read/Write

**Example**: Share all Cases owned by users in the "Support Team" role with users in the "Sales Team" role with Read Only access.

#### Use Cases and Examples

- **Team-Based Sharing**: Share records owned by team members with the entire team
- **Cross-Functional Access**: Share records from one department with another
- **Regional Access**: Share records owned by users in a region with regional managers

**Example Pattern**:
```
Rule: Share Support Cases with Sales Team
- Share With: Sales Team Role
- Based on: Cases owned by Support Team Role
- Access Level: Read Only
```

#### Configuration Patterns

- **Role-Based Sharing**: Share records owned by users in a role with another role
- **User-Based Sharing**: Share records owned by specific users with groups
- **Subordinate Sharing**: Share records owned by users and their subordinates

#### Limitations

- **Owner-Based Only**: Cannot share based on record field values
- **Static Configuration**: Cannot use dynamic criteria
- **Access Level**: Can only grant Read Only or Read/Write (not Delete)

### Criteria-Based Sharing Rules

#### How Criteria-Based Rules Work

Criteria-based sharing rules share records that meet specific field value criteria with users, roles, or groups.

**Configuration**:
- **Rule Name**: Descriptive name for the sharing rule
- **Share With**: Users, roles, roles and subordinates, or public groups
- **Criteria**: Field-based criteria (e.g., Region = "West", Status = "Open")
- **Access Level**: Read Only (for most objects) or Read/Write (for limited objects)

**Example**: Share all Cases where Region equals "West" with users in the "West Region Managers" role.

#### Criteria Evaluation and Selectivity

- **Selective Criteria**: Use indexed fields for better performance
- **Criteria Complexity**: Keep criteria simple for better performance
- **Field Types**: Can use text, picklist, number, date, and lookup fields
- **Multiple Criteria**: Can combine multiple criteria with AND logic

**Best Practices**:
- Use indexed fields (e.g., Status, Region, Type)
- Avoid formula fields in criteria
- Keep criteria selective (narrow scope)

#### Use Cases and Examples

- **Regional Access**: Share records in a region with regional teams
- **Status-Based Access**: Share records with specific status with relevant teams
- **Type-Based Access**: Share records of specific types with specialized teams

**Example Pattern**:
```
Rule: Share High Priority Cases with Management
- Share With: Management Role
- Criteria: Priority = "High"
- Access Level: Read Only
```

#### Performance Considerations

- **Selective Criteria**: Use selective criteria to limit record scope
- **Indexed Fields**: Use indexed fields for better query performance
- **Rule Count**: Limit number of criteria-based sharing rules per object
- **Recalculation**: Criteria-based rules recalculate when records change

#### Limitations

- **Read-Only for Most Objects**: Most objects only support Read Only access via criteria-based rules
- **Limited Objects Support Read/Write**: Only certain objects (e.g., Cases, Leads, Custom Objects) support Read/Write access
- **No Formula Fields**: Cannot use formula fields in criteria
- **Static Criteria**: Criteria are evaluated at rule creation time, not dynamically

### Territory-Based Sharing Rules

#### When Territory Management is Used

Territory Management is used when sales organizations need to manage accounts and opportunities based on geographic territories or other business divisions.

**Use Cases**:
- Geographic sales territories
- Product-based territories
- Industry-based territories
- Account-based territories

#### Territory Hierarchy and Sharing

Territory hierarchy allows:
- **Territory Assignment**: Assign accounts and opportunities to territories
- **Territory Sharing**: Users in a territory can access records assigned to that territory
- **Territory Hierarchy**: Users in parent territories can access child territory records

#### Use Cases

- **Geographic Sales**: Sales teams organized by geographic regions
- **Product Sales**: Sales teams organized by product lines
- **Account Management**: Account teams organized by account assignments

#### Configuration Patterns

- **Territory Assignment Rules**: Automatically assign records to territories based on criteria
- **Territory Sharing**: Share records with users in assigned territories
- **Territory Hierarchy**: Grant access through territory hierarchy

## Manual Sharing

### When Manual Sharing is Used

Manual sharing allows record owners or users with full access to share individual records with other users or groups on a case-by-case basis.

**Use Cases**:
- One-off access requirements
- Temporary access needs
- Exceptions not covered by sharing rules
- Collaborative access for specific records

### How Manual Sharing Works

- **Record Owner**: Can share records they own
- **Full Access Users**: Users with full access (e.g., View All, Modify All) can share records
- **Share Button**: Available on record detail pages
- **Access Level**: Can grant Read Only or Read/Write access
- **Expiration**: Can set expiration date for manual shares (if enabled)

### Limitations and Considerations

- **Not Scalable**: Manual sharing is not scalable for large numbers of records
- **Maintenance Overhead**: Requires manual maintenance for each record
- **No Automation**: Cannot automate manual sharing
- **Audit Trail**: Manual shares are tracked but require manual management

### Best Practices

- **Use Sparingly**: Use manual sharing only for exceptions
- **Document Exceptions**: Document why manual sharing was used
- **Review Regularly**: Review manual shares and remove when no longer needed
- **Set Expiration**: Use expiration dates for temporary access
- **Consider Alternatives**: Consider sharing rules or Apex managed sharing for recurring patterns

## Apex Managed Sharing

### When to Use Apex Managed Sharing

Apex managed sharing is used for complex sharing requirements that cannot be met through declarative sharing rules.

**Use Cases**:
- Dynamic sharing based on complex business logic
- Sharing based on custom relationships
- Sharing that changes based on record field values
- Sharing for Experience Cloud users (when sharing sets are insufficient)
- Sharing based on external system data

### Apex Sharing Reasons

Apex Sharing Reasons define why a record is shared programmatically. Each custom object can have up to 10 Apex Sharing Reasons.

**Configuration**:
- **Sharing Reason Label**: User-friendly label
- **Sharing Reason API Name**: API name for Apex code
- **Description**: Description of when this sharing reason is used

**Example**: "Project Team Member" sharing reason for sharing project records with team members.

### Implementation Patterns

#### Creating Shares

```apex
// Share a Case record with a user
CaseShare caseShare = new CaseShare();
caseShare.CaseId = caseRecord.Id;
caseShare.UserOrGroupId = userId;
caseShare.CaseAccessLevel = 'Read';
caseShare.RowCause = Schema.CaseShare.RowCause.Manual; // or custom Apex Sharing Reason
insert caseShare;
```

#### Bulk Sharing Pattern

```apex
public with sharing class CaseSharingService {
    public static void shareCasesWithUsers(Map<Id, Set<Id>> caseIdToUserIds) {
        List<CaseShare> sharesToInsert = new List<CaseShare>();
        
        for (Id caseId : caseIdToUserIds.keySet()) {
            for (Id userId : caseIdToUserIds.get(caseId)) {
                CaseShare share = new CaseShare();
                share.CaseId = caseId;
                share.UserOrGroupId = userId;
                share.CaseAccessLevel = 'Read';
                share.RowCause = Schema.CaseShare.RowCause.Manual;
                sharesToInsert.add(share);
            }
        }
        
        if (!sharesToInsert.isEmpty()) {
            Database.insert(sharesToInsert, false); // Allow partial success
        }
    }
}
```

#### Using Custom Apex Sharing Reasons

```apex
// Define custom sharing reason in Apex Sharing Reasons
// Then use in code:
CaseShare caseShare = new CaseShare();
caseShare.CaseId = caseRecord.Id;
caseShare.UserOrGroupId = userId;
caseShare.CaseAccessLevel = 'Read';
caseShare.RowCause = Schema.CaseShare.RowCause.Project_Team_Member__c; // Custom reason
insert caseShare;
```

#### Updating Shares

```apex
// Update existing share to change access level
CaseShare existingShare = [SELECT Id, CaseAccessLevel 
                            FROM CaseShare 
                            WHERE CaseId = :caseId 
                            AND UserOrGroupId = :userId 
                            AND RowCause = 'Manual'
                            LIMIT 1];
                            
if (existingShare != null) {
    existingShare.CaseAccessLevel = 'Read/Write';
    update existingShare;
}
```

#### Deleting Shares

```apex
// Delete shares based on criteria
List<CaseShare> sharesToDelete = [
    SELECT Id 
    FROM CaseShare 
    WHERE CaseId = :caseId 
    AND RowCause = 'Manual'
    AND UserOrGroupId IN :userIdsToRemove
];

if (!sharesToDelete.isEmpty()) {
    delete sharesToDelete;
}
```

### Best Practices and Bulkification

- **Bulkify Operations**: Always bulkify share creation, updates, and deletions
- **Error Handling**: Use Database.insert/update/delete with allOrNone=false for partial success
- **Avoid DML in Loops**: Never perform DML operations inside loops
- **Use Custom Sharing Reasons**: Use custom Apex Sharing Reasons for programmatic shares
- **Clean Up Old Shares**: Remove shares when they are no longer needed
- **Test Sharing Logic**: Test sharing logic thoroughly, including edge cases

### Testing Apex Managed Sharing

```apex
@isTest
private class CaseSharingServiceTest {
    @isTest
    static void testShareCasesWithUsers() {
        // Create test data
        User testUser = TestDataFactory.createUser('Standard User');
        Case testCase = TestDataFactory.createCase();
        
        Test.startTest();
        // Test sharing
        Map<Id, Set<Id>> caseIdToUserIds = new Map<Id, Set<Id>>{
            testCase.Id => new Set<Id>{ testUser.Id }
        };
        CaseSharingService.shareCasesWithUsers(caseIdToUserIds);
        Test.stopTest();
        
        // Verify share was created
        CaseShare share = [
            SELECT Id, CaseAccessLevel, RowCause 
            FROM CaseShare 
            WHERE CaseId = :testCase.Id 
            AND UserOrGroupId = :testUser.Id
            LIMIT 1
        ];
        
        System.assertNotEquals(null, share, 'Share should be created');
        System.assertEquals('Read', share.CaseAccessLevel, 'Access level should be Read');
    }
}
```

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

## Experience Cloud (Community) Sharing

### Sharing Sets

#### What Sharing Sets Are

Sharing Sets are Experience Cloud (Community) mechanisms for enforcing data visibility rules per user type. They replace traditional sharing rules for portal/community users, as Customer Community licenses do not support sharing rules.

#### How Sharing Sets Work

Sharing Sets grant community users access to records based on:
- **User-Based**: Records associated with the user's contact
- **Account-Based**: Records associated with the user's account
- **Owner-Based**: Records owned by the user

**Configuration**:
- **Sharing Set Name**: Descriptive name
- **User Profile**: Community user profile
- **Object Access**: Objects to share
- **Sharing Rule**: Based on user, account, or record owner
- **Access Level**: Read Only or Read/Write

#### Configuration Patterns

**Pattern 1: Users See Only Their Own Records**
```
Sharing Set: Customer Self-Service
- Profile: Customer Community User
- Object: Case
- Rule: Cases where Contact equals User's Contact
- Access Level: Read/Write
```

**Pattern 2: Users See Records for Their Account**
```
Sharing Set: Partner Portal Access
- Profile: Partner Community User
- Object: Opportunity
- Rule: Opportunities where Account equals User's Account
- Access Level: Read Only
```

**Pattern 3: Users See Records They Own**
```
Sharing Set: Community User Owned Records
- Profile: Customer Community User
- Object: Custom_Project__c
- Rule: Projects where Owner equals User
- Access Level: Read/Write
```

#### Sharing Set Rules

- **Based on User**: Records where a lookup field equals the user's contact
- **Based on Account**: Records where Account equals the user's account
- **Based on Owner**: Records owned by the user

#### Use Cases for Portal/Community Users

- **Customer Self-Service**: Customers see only their own cases and records
- **Partner Portals**: Partners see records for their associated account
- **Employee Communities**: Employees see records based on their contact or account
- **Multi-Tenant Portals**: Different user types see different record sets

#### Limitations and Considerations

- **Community Users Only**: Sharing Sets only apply to Experience Cloud users
- **No Criteria-Based**: Cannot use field criteria (unlike sharing rules)
- **Limited Objects**: Some objects may not support sharing sets
- **One Rule Per Object**: One sharing set rule per object per profile
- **No Territory Support**: Territory management not supported for community users

### Community Sharing Patterns

#### Users See Only Their Own Records

**Pattern**: Community users see only records where they are the contact or owner.

**Implementation**:
- Sharing Set based on User's Contact
- Or Sharing Set based on Owner equals User

**Use Cases**:
- Customer self-service portals
- Individual user portals
- Personal record management

#### Users See Records for Their Associated Account

**Pattern**: Community users see records associated with their account.

**Implementation**:
- Sharing Set based on Account equals User's Account
- Requires Account lookup on the object

**Use Cases**:
- Partner portals
- Account-based collaboration
- Multi-user account access

#### Users See Records Based on Custom Relationships

**Pattern**: Community users see records based on custom lookup relationships.

**Implementation**:
- Sharing Set based on custom lookup field equals User's Contact
- Requires custom lookup field on the object

**Use Cases**:
- Project-based access
- Team-based access
- Custom relationship access

#### Multi-Tenant Portal Patterns

**Pattern**: Different user types in the same portal see different record sets.

**Implementation**:
- Multiple Sharing Sets for different profiles
- Record Type-based separation
- Sharing Set rules based on user type

**Use Cases**:
- Student/applicant portals with different access
- Client/partner portals with different access
- Multi-organization portals

**Related Patterns**: See `rag/architecture/portal-architecture.md` for portal architecture patterns and `rag/data-modeling/case-management-data-model.md` for multi-tenant data isolation patterns.

### Community vs. Internal Sharing

#### Differences in Sharing Behavior

- **Sharing Rules**: Internal users can use sharing rules; Customer Community users cannot
- **Sharing Sets**: Community users use sharing sets; internal users do not
- **Role Hierarchy**: Community users typically don't have role hierarchy
- **Manual Sharing**: Community users may have limited manual sharing capabilities

#### Portal User Restrictions

- **No Sharing Rules**: Customer Community licenses do not support sharing rules
- **Sharing Sets Required**: Must use sharing sets for record access
- **Limited Manual Sharing**: Limited manual sharing capabilities
- **No Role Hierarchy**: Typically no role hierarchy for community users

#### Best Practices for Community Sharing

- **Use Sharing Sets**: Use sharing sets for all community user access
- **Document Patterns**: Document sharing set patterns and configurations
- **Test Thoroughly**: Test sharing sets with different user types
- **Consider Apex Managed Sharing**: Use Apex managed sharing for complex community sharing requirements
- **Review Regularly**: Review sharing set configurations regularly

## Field-Level Sharing Considerations

### How FLS Interacts with Sharing

Field-Level Security (FLS) and sharing are evaluated independently:

1. **Sharing**: Determines if user can see the record
2. **FLS**: Determines if user can see specific fields on the record

**Key Principle**: A user must have both record-level access (sharing) and field-level access (FLS) to see a field value.

### Field-Level Security vs. Record-Level Sharing

- **Sharing**: Controls record-level access (which records)
- **FLS**: Controls field-level access (which fields)

**Example**: A user may have access to a Case record (through sharing) but not see the SSN field (restricted by FLS).

### Sharing Rules Don't Override FLS

Sharing rules grant record-level access but do not override field-level security. If a field is restricted by FLS, sharing rules cannot grant access to that field.

**Exception**: View All Fields and Modify All Fields permissions bypass FLS.

### Best Practices

- **Configure FLS First**: Configure field-level security before sharing rules
- **Document FLS Restrictions**: Document which fields are restricted and why
- **Test FLS and Sharing Together**: Test both FLS and sharing together
- **Consider View All Fields**: Use View All Fields sparingly for users who need comprehensive access
- **Compliance Alignment**: Ensure FLS aligns with compliance requirements

## Sharing Calculation and Performance

### How Sharing is Calculated

Salesforce calculates sharing in real-time when users access records. The sharing calculation:

1. Evaluates OWD settings
2. Checks role hierarchy
3. Evaluates sharing rules (owner-based, criteria-based, territory-based)
4. Checks manual shares
5. Evaluates Apex managed shares
6. Checks View All / Modify All permissions
7. Checks View All Data / Modify All Data permissions

**Result**: User has access if any mechanism grants access.

### Sharing Recalculation

Sharing is recalculated when:
- **Record Changes**: Record field values change (for criteria-based rules)
- **Owner Changes**: Record owner changes
- **Role Changes**: User's role changes
- **Sharing Rule Changes**: Sharing rules are added, modified, or deleted
- **Manual Sharing**: Manual shares are added or removed
- **Apex Sharing**: Apex managed shares are created, updated, or deleted

**Automatic Recalculation**: Salesforce automatically recalculates sharing when relevant changes occur.

### Performance Considerations

- **Sharing Rule Count**: Limit number of sharing rules per object (recommended: < 50 per object)
- **Criteria Selectivity**: Use selective criteria for criteria-based sharing rules
- **Indexed Fields**: Use indexed fields in criteria-based sharing rules
- **Public Groups**: Use public groups to simplify sharing rule management
- **Role Hierarchy Depth**: Limit role hierarchy depth for performance

### Large Data Volume (LDV) Sharing Patterns

For orgs with large data volumes:

- **Selective Sharing Rules**: Use highly selective sharing rules
- **Indexed Criteria**: Use indexed fields in criteria-based rules
- **Public Groups**: Use public groups instead of individual user sharing
- **Apex Managed Sharing**: Consider Apex managed sharing for complex patterns
- **Sharing Rule Optimization**: Optimize sharing rules for performance

### Optimization Strategies

- **Minimize Sharing Rules**: Use minimum number of sharing rules necessary
- **Use Public Groups**: Group users into public groups for sharing
- **Optimize Criteria**: Use selective, indexed criteria
- **Monitor Performance**: Monitor sharing calculation performance
- **Consider Alternatives**: Consider View All / Modify All for reporting users instead of sharing rules

## Decision Frameworks

### When to Use Each Sharing Mechanism

#### Decision Tree for Selecting Sharing Approach

1. **Start with OWD**: Set OWD to most restrictive setting that meets requirements
2. **Role Hierarchy**: Use role hierarchy if organizational structure matches access needs
3. **Sharing Rules**: Use sharing rules for cross-functional or criteria-based access
4. **Manual Sharing**: Use manual sharing only for exceptions
5. **Apex Managed Sharing**: Use Apex managed sharing for complex, dynamic requirements
6. **View All / Modify All**: Use sparingly for administrative or reporting needs

#### OWD Selection Framework

**Choose Private When**:
- Data is sensitive
- Need maximum control
- Compliance requires restrictive access
- Most records should be private

**Choose Public Read Only When**:
- Data should be visible to all
- Edit access should be restricted
- Need transparency
- Collaboration requires visibility

**Choose Public Read/Write When**:
- Data is non-sensitive
- Maximum collaboration needed
- Reference data that all users maintain
- No security concerns

#### Sharing Rule vs. Role Hierarchy Decision

**Use Role Hierarchy When**:
- Organizational structure matches access needs
- Managers need to see subordinate records
- Simple hierarchical access patterns
- Access follows reporting structure

**Use Sharing Rules When**:
- Cross-functional access needed
- Criteria-based access required
- Team-based access patterns
- Access doesn't follow organizational hierarchy

#### Apex Managed Sharing vs. Declarative Sharing

**Use Declarative Sharing (Sharing Rules) When**:
- Static sharing patterns
- Criteria can be defined declaratively
- Standard sharing rules meet requirements
- No complex business logic needed

**Use Apex Managed Sharing When**:
- Dynamic sharing based on complex logic
- Sharing based on custom relationships
- Sharing changes based on record field values
- Experience Cloud sharing when sharing sets insufficient
- External system integration requirements

### Community Sharing Decision Framework

#### When to Use Sharing Sets

**Use Sharing Sets When**:
- Community users need record access
- Simple relationship-based access (user, account, owner)
- Standard sharing set patterns meet requirements
- Customer Community or Partner Community licenses

#### When to Use Apex Managed Sharing for Communities

**Use Apex Managed Sharing When**:
- Complex sharing requirements not met by sharing sets
- Custom relationship-based sharing
- Dynamic sharing based on record field values
- Sharing based on external system data
- Multi-tenant portal patterns with complex requirements

#### Portal Sharing Patterns Selection

**Users See Only Their Own Records**:
- Use Sharing Set based on User's Contact or Owner
- Simple self-service portals
- Individual user portals

**Users See Records for Their Account**:
- Use Sharing Set based on Account
- Partner portals
- Account-based collaboration

**Users See Records Based on Custom Relationships**:
- Use Sharing Set based on custom lookup field
- Or use Apex managed sharing for complex relationships
- Project-based or team-based access

**Multi-Tenant Portals**:
- Use multiple Sharing Sets for different profiles
- Combine with Record Type-based separation
- Use Apex managed sharing for complex patterns

## Best Practices

### Security Best Practices

- **Principle of Least Privilege**: Grant minimum access necessary
- **Start Restrictive**: Begin with restrictive OWD and open access as needed
- **Document Decisions**: Document all sharing configuration decisions
- **Regular Reviews**: Review sharing configurations regularly (quarterly minimum)
- **Audit Access**: Audit who has access to what records
- **Monitor Changes**: Monitor sharing rule and permission changes
- **Compliance Alignment**: Ensure sharing aligns with compliance requirements

### Performance Best Practices

- **Limit Sharing Rules**: Keep sharing rule count reasonable (< 50 per object)
- **Use Selective Criteria**: Use selective, indexed criteria for criteria-based rules
- **Use Public Groups**: Group users into public groups for sharing
- **Optimize Role Hierarchy**: Keep role hierarchy depth reasonable
- **Monitor Performance**: Monitor sharing calculation performance
- **Consider Alternatives**: Consider View All for reporting users instead of many sharing rules

### Maintenance and Governance

- **Documentation**: Document all sharing rules, sharing sets, and permissions
- **Naming Conventions**: Use consistent naming conventions
- **Regular Reviews**: Review sharing configurations regularly
- **Change Management**: Use change management process for sharing changes
- **Version Control**: Track sharing configuration changes
- **Training**: Train administrators on sharing best practices

### Documentation Requirements

- **Sharing Rule Documentation**: Document purpose, criteria, and access level for each sharing rule
- **Sharing Set Documentation**: Document sharing set patterns and configurations
- **Permission Documentation**: Document View All / Modify All assignments and justifications
- **Decision Documentation**: Document OWD selection decisions
- **Pattern Documentation**: Document common sharing patterns used in the org

### Testing Sharing Rules

- **Test Scenarios**: Test sharing rules with different user roles and record scenarios
- **Edge Cases**: Test edge cases (record owner changes, role changes, criteria changes)
- **Performance Testing**: Test sharing rule performance with large data volumes
- **User Acceptance Testing**: Include sharing in user acceptance testing
- **Regression Testing**: Test sharing rules after configuration changes

### Troubleshooting Sharing Issues

- **Use Sharing Reasons**: Use sharing reasons to understand why users have access
- **Check OWD**: Verify OWD settings
- **Check Role Hierarchy**: Verify role hierarchy structure
- **Check Sharing Rules**: Verify sharing rule criteria and configuration
- **Check Manual Shares**: Check for manual shares
- **Check Permissions**: Verify View All / Modify All permissions
- **Use Debug Tools**: Use sharing debug tools and SOQL queries

## Common Patterns

### Multi-Tenant Data Isolation

#### Record Type-Based Separation

**Pattern**: Use Record Types to distinguish between different tenant data, then apply Record Type-specific sharing.

**Implementation**:
- Different Record Types for different tenants
- Sharing rules or sharing sets based on Record Type
- Field-level security based on Record Type

**Use Cases**:
- Multi-organization portals
- Client/partner data separation
- Student/applicant data separation

**Related Patterns**: See `rag/data-modeling/case-management-data-model.md` for multi-tenant data isolation patterns.

#### Sharing Set Patterns for Portals

**Pattern**: Use Sharing Sets to ensure portal users see only their tenant's records.

**Implementation**:
- Sharing Set based on Account (for account-based tenants)
- Sharing Set based on Contact (for contact-based tenants)
- Multiple Sharing Sets for different tenant types

**Use Cases**:
- Multi-tenant Experience Cloud portals
- Partner portals with multiple organizations
- Client portals with data isolation

#### Cross-Tenant Access Prevention

**Pattern**: Ensure users cannot access records from other tenants.

**Implementation**:
- Restrictive OWD (Private)
- Sharing Sets that only grant access to user's tenant
- Apex managed sharing that enforces tenant boundaries
- Validation rules to prevent cross-tenant data access

**Use Cases**:
- Multi-tenant SaaS applications
- Government multi-agency portals
- Education multi-institution portals

### Hierarchical Access Patterns

#### Manager Sees Subordinate Records

**Pattern**: Managers can see all records owned by their subordinates.

**Implementation**:
- Role hierarchy with managers above subordinates
- OWD set to Private
- Role hierarchy automatically grants access

**Use Cases**:
- Sales management
- Support management
- Project management

#### Territory-Based Access

**Pattern**: Users see records assigned to their territory.

**Implementation**:
- Territory Management enabled
- Territory assignment rules
- Territory-based sharing rules

**Use Cases**:
- Geographic sales territories
- Product-based territories
- Industry-based territories

#### Account-Based Access

**Pattern**: Users see records associated with their account.

**Implementation**:
- Sharing rules based on Account
- Or Sharing Sets based on Account (for community users)

**Use Cases**:
- Partner portals
- Account-based collaboration
- Customer account access

### Collaborative Access Patterns

#### Team-Based Sharing

**Pattern**: Team members share records with each other.

**Implementation**:
- Owner-based sharing rules sharing team records with team role
- Or public group containing team members
- Or Apex managed sharing for dynamic team membership

**Use Cases**:
- Project teams
- Sales teams
- Support teams

#### Project-Based Sharing

**Pattern**: Users see records associated with projects they're assigned to.

**Implementation**:
- Custom lookup field from record to Project
- Sharing Set or Apex managed sharing based on project assignment
- Custom relationship between User and Project

**Use Cases**:
- Project management
- Collaborative project work
- Project-based reporting

#### Cross-Functional Access

**Pattern**: Users from different departments see each other's records.

**Implementation**:
- Criteria-based sharing rules (e.g., Region, Status)
- Owner-based sharing rules across departments
- Apex managed sharing for complex cross-functional logic

**Use Cases**:
- Sales and support collaboration
- Marketing and sales collaboration
- Cross-departmental projects

## Troubleshooting

### Common Sharing Issues

#### Users Cannot See Records They Should See

**Possible Causes**:
- OWD too restrictive
- Role hierarchy not configured correctly
- Sharing rules not configured or criteria not met
- User lacks object permissions
- Manual share not created
- Apex managed share not created

**Solutions**:
- Check OWD settings
- Verify role hierarchy
- Check sharing rule criteria
- Verify object permissions
- Check for manual shares
- Verify Apex managed shares

#### Users Can See Records They Shouldn't See

**Possible Causes**:
- OWD too permissive
- Sharing rules too broad
- View All / Modify All permissions granted
- View All Data / Modify All Data permissions granted
- Role hierarchy grants unintended access

**Solutions**:
- Review OWD settings
- Review sharing rule criteria
- Review View All / Modify All permissions
- Review View All Data / Modify All Data permissions
- Review role hierarchy

#### Sharing Rules Not Working

**Possible Causes**:
- Criteria not selective enough
- Criteria fields not indexed
- Sharing rules not activated
- Public groups not configured correctly
- Role hierarchy conflicts

**Solutions**:
- Use selective, indexed criteria
- Activate sharing rules
- Verify public group membership
- Review role hierarchy

### How to Debug Sharing Problems

#### Use Sharing Reasons

Salesforce provides sharing reasons that explain why a user has access to a record:

```apex
// Query sharing reasons for a record
List<CaseShare> shares = [
    SELECT Id, UserOrGroupId, CaseAccessLevel, RowCause
    FROM CaseShare
    WHERE CaseId = :caseId
];

// RowCause values:
// - 'Owner' - User owns the record
// - 'Manual' - Manually shared
// - 'Rule' - Sharing rule
// - 'Territory' - Territory sharing
// - Custom Apex Sharing Reason API names
```

#### Check Sharing Settings

Use Setup → Sharing Settings to review:
- OWD settings for each object
- Sharing rules configuration
- Role hierarchy structure
- Public groups

#### SOQL Queries for Sharing Analysis

**Query Shares for a Record**:
```sql
SELECT Id, UserOrGroupId, CaseAccessLevel, RowCause, UserOrGroup.Name
FROM CaseShare
WHERE CaseId = '001XX000004XXXXXXX'
```

**Query Shares for a User**:
```sql
SELECT Id, CaseId, CaseAccessLevel, RowCause, Case.Subject
FROM CaseShare
WHERE UserOrGroupId = '005XX000004XXXXXXX'
```

**Query Manual Shares**:
```sql
SELECT Id, CaseId, UserOrGroupId, CaseAccessLevel
FROM CaseShare
WHERE RowCause = 'Manual'
```

**Query Sharing Rules**:
```sql
SELECT Id, Name, SobjectType, AccessLevel, SharingRuleType
FROM SharingRules
WHERE SobjectType = 'Case'
```

### Tools for Analyzing Sharing

- **Sharing Settings UI**: Setup → Sharing Settings
- **Sharing Reasons**: View sharing reasons on record detail pages
- **Sharing Debug Tools**: Use Developer Console or Workbench
- **SOQL Queries**: Query Share objects to analyze sharing
- **Sharing Reports**: Create reports on Share objects

## Code Examples

### Apex Managed Sharing Examples

#### Basic Share Creation

```apex
public with sharing class CaseSharingService {
    /**
     * Share a Case record with a user
     * @param caseId Case record ID
     * @param userId User ID to share with
     * @param accessLevel Read or Read/Write
     */
    public static void shareCaseWithUser(Id caseId, Id userId, String accessLevel) {
        CaseShare caseShare = new CaseShare();
        caseShare.CaseId = caseId;
        caseShare.UserOrGroupId = userId;
        caseShare.CaseAccessLevel = accessLevel;
        caseShare.RowCause = Schema.CaseShare.RowCause.Manual;
        
        try {
            insert caseShare;
        } catch (DmlException e) {
            if (e.getDmlType(0) == StatusCode.INVALID_FIELD) {
                // Share already exists or invalid
                System.debug('Share creation failed: ' + e.getMessage());
            }
            throw e;
        }
    }
}
```

#### Bulk Share Creation

```apex
public with sharing class CaseSharingService {
    /**
     * Share multiple Cases with multiple users
     * @param caseIdToUserIds Map of Case ID to Set of User IDs
     * @param accessLevel Read or Read/Write
     */
    public static void shareCasesWithUsers(
        Map<Id, Set<Id>> caseIdToUserIds, 
        String accessLevel
    ) {
        List<CaseShare> sharesToInsert = new List<CaseShare>();
        
        for (Id caseId : caseIdToUserIds.keySet()) {
            for (Id userId : caseIdToUserIds.get(caseId)) {
                CaseShare share = new CaseShare();
                share.CaseId = caseId;
                share.UserOrGroupId = userId;
                share.CaseAccessLevel = accessLevel;
                share.RowCause = Schema.CaseShare.RowCause.Manual;
                sharesToInsert.add(share);
            }
        }
        
        if (!sharesToInsert.isEmpty()) {
            Database.insert(sharesToInsert, false); // Allow partial success
        }
    }
}
```

#### Share with Custom Apex Sharing Reason

```apex
public with sharing class ProjectSharingService {
    /**
     * Share Project records with team members using custom sharing reason
     * @param projectId Project record ID
     * @param teamMemberIds Set of team member User IDs
     */
    public static void shareProjectWithTeam(Id projectId, Set<Id> teamMemberIds) {
        List<Custom_Project__Share> sharesToInsert = new List<Custom_Project__Share>();
        
        for (Id userId : teamMemberIds) {
            Custom_Project__Share share = new Custom_Project__Share();
            share.ParentId = projectId;
            share.UserOrGroupId = userId;
            share.AccessLevel = 'Read';
            share.RowCause = Schema.Custom_Project__Share.RowCause.Project_Team_Member__c;
            sharesToInsert.add(share);
        }
        
        if (!sharesToInsert.isEmpty()) {
            Database.insert(sharesToInsert, false);
        }
    }
}
```

#### Update Existing Shares

```apex
public with sharing class CaseSharingService {
    /**
     * Update access level for existing shares
     * @param caseId Case record ID
     * @param userId User ID
     * @param newAccessLevel New access level (Read or Read/Write)
     */
    public static void updateCaseShareAccess(
        Id caseId, 
        Id userId, 
        String newAccessLevel
    ) {
        List<CaseShare> existingShares = [
            SELECT Id, CaseAccessLevel 
            FROM CaseShare 
            WHERE CaseId = :caseId 
            AND UserOrGroupId = :userId 
            AND RowCause = 'Manual'
        ];
        
        if (!existingShares.isEmpty()) {
            for (CaseShare share : existingShares) {
                share.CaseAccessLevel = newAccessLevel;
            }
            update existingShares;
        }
    }
}
```

#### Delete Shares

```apex
public with sharing class CaseSharingService {
    /**
     * Remove shares for a Case
     * @param caseId Case record ID
     * @param userIdsToRemove Set of User IDs to remove access for
     */
    public static void removeCaseShares(Id caseId, Set<Id> userIdsToRemove) {
        List<CaseShare> sharesToDelete = [
            SELECT Id 
            FROM CaseShare 
            WHERE CaseId = :caseId 
            AND RowCause = 'Manual'
            AND UserOrGroupId IN :userIdsToRemove
        ];
        
        if (!sharesToDelete.isEmpty()) {
            delete sharesToDelete;
        }
    }
}
```

### Sharing Calculation Queries

#### Query Shares for Analysis

```apex
public with sharing class SharingAnalysisService {
    /**
     * Get all shares for a record with details
     * @param recordId Record ID
     * @return List of Share records with user/group names
     */
    public static List<CaseShare> getRecordShares(Id recordId) {
        return [
            SELECT Id, UserOrGroupId, CaseAccessLevel, RowCause,
                   UserOrGroup.Name, UserOrGroup.Type
            FROM CaseShare
            WHERE CaseId = :recordId
            ORDER BY RowCause, UserOrGroup.Name
        ];
    }
    
    /**
     * Get all records shared with a user
     * @param userId User ID
     * @return List of Share records with record details
     */
    public static List<CaseShare> getUserShares(Id userId) {
        return [
            SELECT Id, CaseId, CaseAccessLevel, RowCause,
                   Case.Subject, Case.Status
            FROM CaseShare
            WHERE UserOrGroupId = :userId
            ORDER BY Case.Subject
        ];
    }
}
```

### Sharing Rule Testing Patterns

#### Test Sharing Rule with Different Users

```apex
@isTest
private class CaseSharingRuleTest {
    @isTest
    static void testSharingRuleGrantsAccess() {
        // Create test users with different roles
        User managerUser = TestDataFactory.createUser('Manager');
        User salesUser = TestDataFactory.createUser('Sales Rep');
        
        // Create test case owned by sales user
        Case testCase = TestDataFactory.createCase();
        testCase.OwnerId = salesUser.Id;
        update testCase;
        
        Test.startTest();
        // Run as manager user
        System.runAs(managerUser) {
            // Query case - should have access via role hierarchy
            List<Case> accessibleCases = [
                SELECT Id, Subject 
                FROM Case 
                WHERE Id = :testCase.Id
            ];
            
            System.assertEquals(1, accessibleCases.size(), 
                'Manager should have access via role hierarchy');
        }
        Test.stopTest();
    }
}
```

### Community Sharing Implementation Examples

#### Apex Managed Sharing for Community Users

```apex
public with sharing class CommunityCaseSharingService {
    /**
     * Share Case with community user based on contact relationship
     * @param caseRecord Case record
     */
    public static void shareCaseWithCommunityUser(Case caseRecord) {
        if (caseRecord.ContactId == null) {
            return;
        }
        
        // Find community user associated with contact
        List<User> communityUsers = [
            SELECT Id 
            FROM User 
            WHERE ContactId = :caseRecord.ContactId
            AND Profile.UserLicense.Name LIKE '%Community%'
            LIMIT 1
        ];
        
        if (!communityUsers.isEmpty()) {
            CaseShare share = new CaseShare();
            share.CaseId = caseRecord.Id;
            share.UserOrGroupId = communityUsers[0].Id;
            share.CaseAccessLevel = 'Read/Write';
            share.RowCause = Schema.CaseShare.RowCause.Manual;
            
            try {
                insert share;
            } catch (DmlException e) {
                // Handle error (e.g., share already exists)
                System.debug('Share creation failed: ' + e.getMessage());
            }
        }
    }
}
```

## Related Patterns

- **Permission Set Architecture**: See `rag/security/permission-set-architecture.md` for permission context
- **Portal Architecture**: See `rag/architecture/portal-architecture.md` for portal sharing patterns
- **Case Management Data Model**: See `rag/data-modeling/case-management-data-model.md` for multi-tenant sharing examples
- **Multi-Tenant Identity**: See `rag/identity-sso/multi-tenant-identity-architecture.md` for identity-based sharing

## When to Use This Document

- Understanding how Salesforce sharing works
- Implementing sharing rules for internal users
- Designing Experience Cloud sharing with Sharing Sets
- Deciding between different sharing mechanisms
- Troubleshooting sharing access issues
- Implementing Apex managed sharing
- Understanding View All/Modify All permissions
- Designing multi-tenant data isolation patterns
- Optimizing sharing for large data volumes

