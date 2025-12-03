---
title: "Salesforce Sharing Rules and Manual Sharing"
level: "Intermediate"
tags:
  - salesforce
  - security
  - sharing
  - sharing-rules
  - apex-managed-sharing
last_reviewed: "2025-01-XX"
---

# Salesforce Sharing Rules and Manual Sharing

## Overview

This document covers sharing rules (owner-based, criteria-based, territory-based), manual sharing, and Apex managed sharing. These mechanisms extend access beyond Org-Wide Defaults and Role Hierarchy.

**Related Patterns**: 
- See `rag/security/sharing-fundamentals.md` for OWD, Role Hierarchy, and View All permissions
- See `rag/security/sharing-sets-and-portals.md` for Experience Cloud sharing patterns
- See `rag/security/permission-set-architecture.md` for permission context

## Prerequisites

- Understanding of Org-Wide Defaults (OWD) and Role Hierarchy
- Basic knowledge of Salesforce security model
- Understanding of record ownership and user roles

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

## Decision Frameworks

### Sharing Rule vs. Role Hierarchy Decision

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

### Apex Managed Sharing vs. Declarative Sharing

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

## Edge Cases and Limitations

### Sharing Rule Limitations

- **Criteria-Based Rules**: Most objects only support Read Only access
- **Formula Fields**: Cannot use formula fields in criteria-based rules
- **Performance**: Large numbers of sharing rules can impact performance
- **Recalculation**: Criteria-based rules recalculate when records change

### Apex Managed Sharing Limitations

- **Governor Limits**: Share creation counts against DML limits
- **Complexity**: Requires code maintenance and testing
- **Performance**: Large-scale sharing operations can be slow
- **Error Handling**: Must handle share creation failures gracefully

## Q&A

### Q: What is the difference between Owner-based and Criteria-based sharing rules?

**A**: **Owner-based** sharing rules share records owned by specific users or roles with other users, roles, or groups. **Criteria-based** sharing rules share records that meet specific field value criteria (e.g., Region = "West") with users, roles, or groups. Owner-based rules are simpler but limited to ownership; criteria-based rules are more flexible but have performance considerations.

### Q: When should I use sharing rules vs Apex managed sharing?

**A**: Use **sharing rules** when sharing patterns are static, criteria can be defined declaratively, and standard sharing rules meet requirements. Use **Apex managed sharing** when sharing is dynamic based on complex logic, based on custom relationships, changes based on record field values, or when sharing sets are insufficient for Experience Cloud users.

### Q: What are the limitations of criteria-based sharing rules?

**A**: Most objects only support Read Only access via criteria-based rules (limited objects support Read/Write). You cannot use formula fields in criteria. Large numbers of criteria-based rules can impact performance. Rules recalculate when records change, which can cause performance issues with large data volumes.

### Q: How do I bulkify Apex managed sharing operations?

**A**: Always bulkify share creation, updates, and deletions. Collect all shares to create/update/delete in lists, then perform DML operations on the entire list. Use `Database.insert/update/delete` with `allOrNone=false` for partial success. Never perform DML operations inside loops.

### Q: What are Apex Sharing Reasons and why do I need them?

**A**: Apex Sharing Reasons define why a record is shared programmatically. Each custom object can have up to 10 Apex Sharing Reasons. They provide a way to categorize and track programmatic shares, making it easier to understand why records are shared and to clean up shares when they're no longer needed.

### Q: When should I use manual sharing?

**A**: Use manual sharing **sparingly** and only for exceptions - one-off access requirements, temporary access needs, or exceptions not covered by sharing rules. Manual sharing is not scalable and requires manual maintenance. Consider sharing rules or Apex managed sharing for recurring patterns.

### Q: How do I test Apex managed sharing?

**A**: Create test users with appropriate roles, create test records, execute sharing logic within `Test.startTest()` and `Test.stopTest()`, then verify shares were created by querying Share objects. Test with different user roles and record scenarios, including edge cases like record owner changes and role changes.

### Q: What happens if I create a share that already exists?

**A**: Salesforce will throw a DML exception with `INVALID_FIELD` status code. Handle this gracefully by catching the exception and checking if the share already exists. Alternatively, query for existing shares before creating new ones, or use `Database.insert` with `allOrNone=false` to allow partial success.

## Related Patterns

- **Sharing Fundamentals**: See `rag/security/sharing-fundamentals.md` for OWD, Role Hierarchy, and View All permissions
- **Sharing Sets and Portals**: See `rag/security/sharing-sets-and-portals.md` for Experience Cloud sharing patterns
- **Permission Set Architecture**: See `rag/security/permission-set-architecture.md` for permission context

## Edge Cases and Limitations

### Edge Case 1: Sharing Rules with Large Data Volumes

**Scenario**: Sharing rules processing millions of records, causing performance issues or calculation delays.

**Consideration**:
- Use criteria-based sharing rules with indexed fields for better performance
- Limit sharing rule complexity (avoid complex formula criteria)
- Monitor sharing rule calculation time and adjust as needed
- Consider Apex managed sharing for very large datasets (more control over calculation)
- Test sharing rule performance with production-like data volumes

### Edge Case 2: Sharing Rules with Complex Criteria

**Scenario**: Sharing rules with complex formula criteria or multiple conditions causing calculation issues.

**Consideration**:
- Simplify sharing rule criteria when possible (avoid nested formulas)
- Use indexed fields in criteria for better performance
- Test sharing rule criteria thoroughly before production
- Monitor sharing rule calculation errors and adjust criteria
- Consider Apex managed sharing for very complex criteria

### Edge Case 3: Apex Managed Sharing with High Concurrency

**Scenario**: Apex managed sharing code executing during high-concurrency scenarios, causing lock contention.

**Consideration**:
- Implement bulkification in Apex managed sharing code
- Use asynchronous processing (Queueable, @future) for non-critical sharing
- Avoid sharing calculations in triggers (use async processing)
- Implement retry logic for sharing calculation failures
- Monitor for lock contention and adjust processing strategy

### Edge Case 4: Manual Sharing with Large User Groups

**Scenario**: Manually sharing records with large public groups or role hierarchies, causing performance issues.

**Consideration**:
- Limit manual sharing to small groups when possible
- Use sharing rules instead of manual sharing for large groups
- Consider Apex managed sharing for programmatic sharing with large groups
- Monitor manual sharing performance and adjust approach
- Document manual sharing use cases for maintenance

### Edge Case 5: Sharing Rule Conflicts and Overlaps

**Scenario**: Multiple sharing rules granting different access levels to the same users, causing access conflicts.

**Consideration**:
- Understand sharing rule evaluation order (most permissive access wins)
- Document sharing rule interactions and conflicts
- Test sharing rule combinations to verify access levels
- Use sharing rule groups to organize related rules
- Review sharing rule conflicts during security reviews

### Limitations

- **Sharing Rule Limits**: Maximum 300 sharing rules per object (varies by org edition)
- **Criteria Complexity**: Sharing rule criteria have formula complexity limits
- **Calculation Performance**: Sharing rule calculation may be slow with very large datasets
- **Manual Sharing Limits**: Manual sharing not scalable for large user groups
- **Apex Managed Sharing Complexity**: Apex managed sharing requires code maintenance and testing
- **Sharing Rule Evaluation Order**: Sharing rules evaluated in order, most permissive access wins
- **Sharing Rule Recalculation**: Sharing rules recalculated when records change, may cause delays
- **Public Group Limits**: Public groups have member limits (varies by org edition)

## When to Use This Document

- Implementing sharing rules for internal users
- Deciding between sharing rules and Apex managed sharing
- Implementing Apex managed sharing for complex requirements
- Understanding manual sharing use cases
- Troubleshooting sharing rule issues

