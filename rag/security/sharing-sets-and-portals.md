---
title: "Salesforce Sharing Sets and Portal Sharing"
level: "Intermediate"
tags:
  - salesforce
  - security
  - sharing
  - experience-cloud
  - sharing-sets
  - portals
last_reviewed: "2025-01-XX"
---

# Salesforce Sharing Sets and Portal Sharing

## Overview

This document covers Experience Cloud (Community) sharing patterns, Sharing Sets, field-level sharing considerations, performance optimization, best practices, common patterns, troubleshooting, and code examples.

**Related Patterns**: 
- See `rag/security/sharing-fundamentals.md` for OWD, Role Hierarchy, and View All permissions
- See `rag/security/sharing-rules-and-manual-sharing.md` for sharing rules and Apex managed sharing
- See `rag/architecture/portal-architecture.md` for portal architecture patterns

## Prerequisites

- Understanding of Org-Wide Defaults (OWD) and Role Hierarchy
- Basic knowledge of Experience Cloud (Communities)
- Understanding of record ownership and user roles

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

## Q&A

### Q: What are Sharing Sets and when do I use them?

**A**: Sharing Sets are Experience Cloud (Community) mechanisms for enforcing data visibility rules per user type. They replace traditional sharing rules for portal/community users, as Customer Community licenses do not support sharing rules. Use Sharing Sets when community users need record access based on user, account, or owner relationships.

### Q: What is the difference between Sharing Sets and Sharing Rules?

**A**: **Sharing Rules** are for internal users and support owner-based, criteria-based, and territory-based sharing. **Sharing Sets** are for Experience Cloud (Community) users and support user-based, account-based, and owner-based sharing. Customer Community licenses do not support sharing rules, so Sharing Sets are required for community user access.

### Q: How do I implement multi-tenant data isolation in Experience Cloud?

**A**: Use multiple Sharing Sets for different profiles, combine with Record Type-based separation, and use Apex managed sharing for complex patterns. Ensure Sharing Sets only grant access to the user's tenant records. Use restrictive OWD (Private) and validation rules to prevent cross-tenant data access.

### Q: How does Field-Level Security (FLS) interact with sharing?

**A**: FLS and sharing are evaluated independently. Sharing determines if a user can see the record; FLS determines if the user can see specific fields on the record. A user must have both record-level access (sharing) and field-level access (FLS) to see a field value. Sharing rules do not override FLS.

### Q: What are the performance considerations for sharing?

**A**: Limit the number of sharing rules per object (recommended: < 50 per object). Use selective, indexed criteria for criteria-based sharing rules. Use public groups to simplify sharing rule management. Limit role hierarchy depth. Monitor sharing calculation performance. Consider View All for reporting users instead of many sharing rules.

### Q: How do I troubleshoot sharing access issues?

**A**: Use sharing reasons to understand why users have access. Check OWD settings, verify role hierarchy structure, check sharing rule criteria and configuration, check for manual shares, verify View All/Modify All permissions, and use sharing debug tools and SOQL queries to analyze sharing.

### Q: When should I use Apex managed sharing for Experience Cloud users?

**A**: Use Apex managed sharing for Experience Cloud users when sharing requirements are complex and not met by Sharing Sets, when sharing is based on custom relationships, when sharing changes dynamically based on record field values, or when sharing is based on external system data.

### Q: How do I optimize sharing for large data volumes?

**A**: Use highly selective sharing rules with indexed criteria. Use public groups instead of individual user sharing. Consider Apex managed sharing for complex patterns. Optimize sharing rules for performance. Monitor sharing calculation performance. Consider View All/Modify All for reporting users instead of many sharing rules.

## Related Patterns

- **Permission Set Architecture**: See `rag/security/permission-set-architecture.md` for permission context
- **Portal Architecture**: See `rag/architecture/portal-architecture.md` for portal sharing patterns
- **Case Management Data Model**: See `rag/data-modeling/case-management-data-model.md` for multi-tenant sharing examples
- **Multi-Tenant Identity**: See `rag/identity-sso/multi-tenant-identity-architecture.md` for identity-based sharing
- **Sharing Fundamentals**: See `rag/security/sharing-fundamentals.md` for OWD, Role Hierarchy, and View All permissions
- **Sharing Rules and Manual Sharing**: See `rag/security/sharing-rules-and-manual-sharing.md` for sharing rules and Apex managed sharing

## Edge Cases and Limitations

### Edge Case 1: Sharing Sets with Large Contact/Account Hierarchies

**Scenario**: Sharing Sets processing large numbers of related Contacts or Accounts, causing performance issues.

**Consideration**:
- Limit Sharing Set complexity (avoid deep relationship traversal)
- Use Account-based sharing when possible (more efficient than Contact-based)
- Monitor Sharing Set calculation time with large datasets
- Test Sharing Set performance with production-like data volumes
- Consider Apex managed sharing for very complex sharing requirements

### Edge Case 2: Field-Level Sharing with Many Fields

**Scenario**: Objects with many fields requiring field-level sharing configuration, creating maintenance complexity.

**Consideration**:
- Limit field-level sharing to essential fields (reduces maintenance overhead)
- Use field sets to group related fields for sharing configuration
- Document field-level sharing requirements for maintenance
- Test field-level sharing from community user perspective
- Consider object-level sharing when field-level sharing becomes too complex

### Edge Case 3: Sharing Sets with Complex Relationship Traversal

**Scenario**: Sharing Sets requiring traversal of multiple relationship levels (e.g., Account → Contact → Case → Case Comments).

**Consideration**:
- Limit relationship traversal depth in Sharing Sets (performance impact)
- Use Apex managed sharing for complex relationship traversal
- Test sharing calculation performance with deep relationships
- Document relationship traversal logic for maintenance
- Consider flattening relationships when possible

### Edge Case 4: Multi-Tenant Portal Sharing

**Scenario**: Multiple Experience Cloud sites in same org requiring data isolation between sites.

**Consideration**:
- Use Record Types to separate data by portal/community
- Configure separate Sharing Sets per portal/community
- Test data isolation between portals thoroughly
- Use different Account/Contact Record Types per portal
- Monitor sharing calculation performance with multiple portals

### Edge Case 5: Sharing Sets with High-Volume Data Changes

**Scenario**: High-volume data changes (e.g., bulk updates) triggering Sharing Set recalculations, causing performance issues.

**Consideration**:
- Use bulk API operations to minimize sharing recalculation triggers
- Implement batch processing for high-volume updates
- Monitor sharing calculation performance during bulk operations
- Consider asynchronous sharing calculation for non-critical updates
- Test sharing performance with bulk data operations

### Limitations

- **Sharing Set Limits**: Maximum 50 Sharing Sets per Experience Cloud site (varies by org edition)
- **Customer Community License Restrictions**: Customer Community licenses don't support sharing rules (must use Sharing Sets)
- **Field-Level Sharing Complexity**: Field-level sharing adds maintenance overhead and complexity
- **Sharing Calculation Performance**: Sharing Set calculation may be slow with very large datasets or complex relationships
- **Relationship Traversal Limits**: Deep relationship traversal in Sharing Sets may impact performance
- **Multi-Portal Complexity**: Multiple Experience Cloud sites increase sharing configuration complexity
- **Sharing Set Evaluation Order**: Sharing Sets evaluated in order, most permissive access wins
- **Sharing Set Recalculation**: Sharing Sets recalculated when records change, may cause delays
- **Portal User License Limits**: Different portal user license types have different sharing capabilities

## When to Use This Document

- Designing Experience Cloud sharing with Sharing Sets
- Implementing portal sharing patterns
- Understanding field-level sharing considerations
- Optimizing sharing for large data volumes
- Troubleshooting sharing access issues
- Designing multi-tenant data isolation patterns

