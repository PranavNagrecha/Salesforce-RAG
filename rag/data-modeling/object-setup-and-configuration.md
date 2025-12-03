---
layout: default
title: Object Setup and Configuration
description: Comprehensive checklist and best practices for setting up custom and standard objects in Salesforce
permalink: /rag/data-modeling/object-setup-and-configuration.html
---

# Object Setup and Configuration

## Overview

Comprehensive checklist and best practices for setting up custom and standard objects in Salesforce. This guide covers the complete object configuration process from initial creation through Lightning Experience optimization, ensuring objects are properly configured for production use.

## Prerequisites

**Required Knowledge**:
- Understanding of Salesforce object model and custom object creation
- Familiarity with field types, relationships, and validation rules
- Knowledge of Lightning Experience and page layouts
- Understanding of profiles, permission sets, and object-level security
- Basic knowledge of record types and their use cases

**Recommended Reading**:
- `rag/data-modeling/standard-object-oddities.md` - Standard object considerations
- `rag/security/permission-set-architecture.md` - Permission set patterns
- `rag/development/formulas-validation-rules.md` - Validation rule patterns
- `rag/development/lightning-app-builder.md` - Lightning page configuration

## Object Setup Checklist

### Initial Object Creation

**Steps**:
1. Create the Object and name it
2. Set the Name field on the object (e.g., Auto Number)
3. Configure object details:
   - Allow Reports
   - Allow Activities (optional)
   - Track Field History
   - Set Deployed status
   - Allow Search

### Tab Configuration

**Steps**:
1. Create the Tab for the object
2. Decide who should access the Tab
3. Decide which App the Tab should be in (not all apps)
4. Consider tab visibility for different user types

### Record Types (Optional)

**What they are**: Record Types enable different business processes, picklist values, and page layouts for the same object. They allow the same object to support multiple workflows or use cases.

**When to use**:
- Different business processes for the same object
- Different picklist values needed for different record categories
- Different page layouts needed for different user groups or workflows
- Different validation rules or automation needed based on record category

**When NOT to use**:
- Simple variations that can be handled with fields or picklists
- Variations that would be better served by separate objects
- When record types add unnecessary complexity

**Steps**:
1. Create Record Types if needed for different record workflows
2. Configure Record Type-specific page layouts
3. Set Record Type defaults for profiles
4. Configure Record Type visibility in profiles/permission sets
5. Configure Record Type-specific picklist values
6. Set up Record Type-specific automation if needed

**Best Practices**:
- Use Record Types when you need different business processes for the same object
- Keep Record Type count manageable (typically 2-5 Record Types per object)
- Consider whether separate objects would be better than Record Types
- Document Record Type purpose and usage
- Test Record Type assignment and visibility

### Field Configuration

**Steps**:
1. Add fields to the object
2. Include Help Text for user-facing fields
3. Set correct Field-Level Security (FLS) permissions as you create fields
4. Include Lookup or Master-Detail fields to other objects
5. Remember to set Lookup Filters if required
6. Configure field visibility and required settings

**Best Practices**:
- See all fields in alphabetical order (custom and standard)
- Be aware of standard fields that are not visible by default (e.g., Contacts)
- Field-level security is critical: https://help.salesforce.com/HTViewHelpDoc?id=admin_fls.htm

### Page Layout Configuration

**What they are**: Page Layouts control which fields appear on record detail pages, field order and organization, related lists, and actions available to users. They provide the user interface structure for viewing and editing records.

**Key components**:
- Field organization in sections
- Field visibility and required settings
- Related lists and their visibility
- Actions (buttons, links, quick actions)
- Field read-only settings
- Mobile layout configuration

**Layout assignment**:
- Page layouts are assigned to profiles and record types
- Different profiles can have different layouts for the same record type
- Different record types can have different layouts
- Layouts can be shared across profiles when appropriate

**Steps**:
1. Edit the Page Layout to ensure all fields are visible and in the right location
2. Organize fields into logical sections
3. Make the Section header visible for System Fields
4. Ensure required fields are marked as required
5. Configure field read-only settings where appropriate
6. Add Related Lists:
   - Files and Notes related list (if using them)
   - Object History related list
   - Other related object lists
7. Configure Related List visibility and order
8. Configure actions (buttons, links, quick actions)
9. Test layout with different profiles and record types

**Best Practices**:
- Organize fields logically in sections
- Group related fields together
- Make system fields visible with section headers
- Configure related lists for easy navigation
- Test layouts with end users
- Keep layouts consistent across similar objects

### Actions Configuration

**Steps**:
1. Override the Salesforce Mobile and Lightning Experience Actions
2. Set the exact Actions you want to appear on the Object
3. Optional - Create other Page Layouts if required for other Record Types
4. Optional - Create a Create Record Action from a related Object
   - Ensure the Layout is correct with all required fields for Creating the record
5. Optional - Create an Update Record Action for bulk updates from list view

### Compact Layout

**Steps**:
1. Create the Compact Layout
2. Assign it to the Page Layout
3. Configure which fields appear in the compact layout

### Search Layouts

**Steps**:
1. Set the Search Layouts (IMPORTANT!)
2. Configure which fields appear in search results
3. Ensure search layout is optimized for user needs

### List View Configuration

**Steps**:
1. Go to the Tab
2. Edit the All View
3. If there are any Record Types, create a View for each Record Type
4. If there are any buttons to add to the List View, then add them
5. Ensure you go back to Classic if this will be in Communities to ensure Communities users can't see inappropriate Views

### Validation Rules (Optional)

**Steps**:
1. Add any Validation Rules needed
2. Test validation rules with different scenarios
3. Ensure error messages are clear and actionable

### Permissions Configuration

**Steps**:
1. Set permissions on Object (Object-Level Security)
2. Configure Field-Level Security for all fields
3. Set Record Type defaults if applicable
4. Configure sharing settings if needed

### Feed Tracking

**Steps**:
1. Enable Feed Tracking for the Object
2. Configure which fields to track in feeds
3. Consider feed tracking impact on storage

### Lightning Record Page Configuration

**Steps**:
1. Look at the Object, create a Test Record
2. Edit the Lightning Record Page
3. Configure page components:
   - Chatter first
   - Delete Related (if applicable)
   - Add Related List Quick Links IF there are related lists
   - Add Files as a Related List under Chatter
4. Activate Page - Assign as Org Default

## Field Configuration Best Practices

### Field Visibility

**Challenge**: Not seeing ALL fields in alphabetical order

**Solution**: Have a good understanding of what are the custom and standard fields in your org

**Note**: Be aware of standard fields that are not set as visible by default (e.g., Contacts)

### Field-Level Security

**Critical**: Field-level security is the most important aspect of field configuration

**Reference**: https://help.salesforce.com/HTViewHelpDoc?id=admin_fls.htm

**Best Practices**:
- Set FLS permissions as you create fields
- Review FLS for all fields before deployment
- Test field visibility with different user profiles
- Consider field visibility for community users

### Help Text

**Best Practice**: Include Help Text for all user-facing fields

**Purpose**: Provides guidance to users on field purpose and expected values

**Implementation**:
- Add help text to all custom fields
- Add help text to standard fields when necessary
- Provide clear, concise guidance
- Explain field purpose and expected values
- Include examples when helpful

### Field Descriptions

**Best Practice**: Add descriptions to fields created for specific purposes

**Use Cases**:
- Formula fields created for reporting
- Fields added for integration purposes
- Fields with specific business rules
- Fields that require explanation

**Implementation**:
- Document field purpose in description
- Explain why field exists
- Note any special considerations
- Include business rules if applicable

## Field Naming Conventions

### API Name Best Practices

**General Guidelines**:
- Use descriptive, clear names
- Follow consistent naming conventions
- Consider API name stability
- Avoid abbreviations unless standard
- Use CamelCase for API names

**API Name Stability**:
- API names should remain stable even if labels change
- Use standard object API names in custom field API names when renaming standard objects
- Example: If Case is renamed to Complaint, use `CaseFileNo__c` not `ComplaintFileNo__c`
- This allows object name changes without API name changes

**Naming Preferences** (Note: These are preferences, not industry standards):
- **Underscores in API Names**: Some prefer no underscores (e.g., `MyFieldName__c`), others use underscores (e.g., `My_Field_Name__c`). Both are valid. Choose based on org standards.
- **Abbreviations**: Use standard abbreviations (e.g., "Num" for Number, "ID" for Identifier)
- **Length**: Keep API names reasonable length for readability

### Object Naming

**Best Practice**: Use singular object names

**Rationale**:
- Aligns with Salesforce standard objects (Account, Contact, Case)
- Consistent with object-oriented design principles
- Clearer in API references

**Examples**:
- Good: `CaseReference__c` (singular)
- Avoid: `CasesReference__c` (plural)

### Field Label vs API Name

**Pattern**: Field labels can be user-friendly, API names should be stable

**Implementation**:
- Use descriptive labels for users
- Use stable API names for code
- Labels can change without affecting API names
- API names should remain constant

**Example**:
- Label: "Complaint File Number"
- API Name: `CaseFileNo__c` (references standard object API name)

## Relationships

### Master-Detail vs Lookup

**Decision Framework**:
- Master-Detail relationships are great for parent-child relationships with cascade delete
- Use Lookup relationships when you need more flexibility
- Remember: You can always use triggers or Rollup Helper to create calculated fields if you don't have a Master-Detail relationship

### Lookup Filters

**Best Practice**: Set Lookup Filters if required to restrict related record selection

**Use Cases**:
- Filter related records by status
- Filter by record type
- Filter by other criteria relevant to business logic

## Standard Objects Reference

### Common Standard Objects

**Files, Content, Attachments, Documents**:
- Different mechanisms for file storage
- Consider which approach fits your use case

**Contacts**:
- Standard fields not visible by default
- Be aware of hidden standard fields

**Accounts**:
- Core organization/person record
- Consider person accounts vs business accounts

**Assets**:
- Track physical or digital assets
- Link to Accounts and Contacts

**Campaigns**:
- Marketing campaign tracking
- Link to Leads and Opportunities

**Cases**:
- Customer service case management
- Link to Accounts and Contacts

**Contracts**:
- Contract management
- Link to Accounts and Opportunities

**Knowledge**:
- Knowledge base articles
- Support self-service and case resolution

**Leads**:
- Lead management
- Convert to Contacts and Opportunities

**Opportunities**:
- Sales opportunity tracking
- Link to Accounts and Contacts

**Tasks**:
- Activity tracking
- Link to various objects

## Implementation Patterns

### Object Setup Workflow

**Recommended Order**:
1. Create object and basic configuration
2. Create fields (with FLS)
3. Create relationships
4. Create tabs and assign to apps
5. Create page layouts
6. Create compact layouts
7. Configure search layouts
8. Set up actions
9. Configure Lightning Record Pages
10. Set permissions
11. Test with test records
12. Configure list views

### Testing Object Configuration

**Steps**:
1. Create a test record
2. Verify all fields are visible and in correct locations
3. Test field-level security with different user profiles
4. Test actions (Create, Edit, Delete)
5. Test related lists
6. Test search functionality
7. Test Lightning Record Page
8. Test list views
9. Test validation rules
10. Test feed tracking

### Community/Portal Considerations

**Important**: If objects will be used in Experience Cloud (Communities):

**Steps**:
1. Ensure you go back to Classic to configure Communities-specific settings
2. Ensure Communities users can't see inappropriate Views
3. Configure sharing settings for community users
4. Test object access from community user perspective
5. Verify field visibility for community users

## Key Architectural Decisions

### Object Configuration Completeness

**Decision**: Complete object setup requires attention to many details

**Rationale**: Incomplete object setup leads to:
- Poor user experience
- Security gaps
- Missing functionality
- Difficult maintenance

**Implementation**: Follow the complete checklist to ensure nothing is missed

### Field-Level Security First

**Decision**: Set FLS permissions as you create fields

**Rationale**: 
- Easier to configure during creation
- Prevents security gaps
- Ensures proper access control from the start

**Implementation**: Configure FLS for each field immediately after creation

### Search Layout Importance

**Decision**: Search Layouts are critical and often overlooked

**Rationale**: 
- Users rely on search to find records
- Poor search layouts reduce productivity
- Search is a primary navigation mechanism

**Implementation**: Always configure Search Layouts as part of object setup

## Best Practices

### Object Setup

- Complete all configuration steps before deployment
- Test object configuration with test records
- Document any custom configurations
- Review object configuration with stakeholders

### Field Configuration

- Set FLS permissions during field creation
- Include help text for all user-facing fields
- Be aware of standard fields not visible by default
- Use appropriate field types for data quality

### Layout Configuration

- Organize fields logically on page layouts
- Make system fields visible with section headers
- Configure related lists appropriately
- Test layouts with different record types

### Action Configuration

- Override default actions to show only needed actions
- Configure Create Record actions with proper layouts
- Enable bulk update actions when needed
- Test actions from different contexts

### Lightning Experience

- Configure Lightning Record Pages for optimal UX
- Place Chatter first for collaboration
- Add Related List Quick Links for navigation
- Test Lightning pages with different user types

## Common Pitfalls

### Incomplete Configuration

**Issue**: Objects deployed without complete configuration

**Impact**: Poor user experience, missing functionality

**Solution**: Follow the complete checklist before deployment

### Missing Field-Level Security

**Issue**: Fields created without FLS configuration

**Impact**: Security gaps, inappropriate data access

**Solution**: Set FLS permissions during field creation

### Overlooked Search Layouts

**Issue**: Search Layouts not configured

**Impact**: Poor search experience, reduced productivity

**Solution**: Always configure Search Layouts as part of setup

### Standard Fields Not Visible

**Issue**: Standard fields not set as visible by default

**Impact**: Missing important fields in layouts

**Solution**: Be aware of standard fields and make them visible when needed

### Community User Access

**Issue**: Objects not properly configured for community users

**Impact**: Community users see inappropriate data or views

**Solution**: Test and configure objects specifically for community access

## Q&A

### Q: What is the recommended order for setting up a new object?

**A**: The recommended order is: (1) Create object and basic configuration, (2) Create fields with FLS, (3) Create relationships, (4) Create tabs and assign to apps, (5) Create page layouts, (6) Create compact layouts, (7) Configure search layouts, (8) Set up actions, (9) Configure Lightning Record Pages, (10) Set permissions, (11) Test with test records, (12) Configure list views.

### Q: When should I use Record Types?

**A**: Use Record Types when you need different business processes, picklist values, or page layouts for the same object. Use them for different workflows or use cases. Avoid Record Types for simple variations that can be handled with fields or picklists, or when separate objects would be better.

### Q: Should I use singular or plural object names?

**A**: Use **singular object names** (e.g., `CaseReference__c` not `CasesReference__c`). This aligns with Salesforce standard objects (Account, Contact, Case), is consistent with object-oriented design principles, and is clearer in API references.

### Q: What is the difference between Field Label and API Name?

**A**: **Field Labels** are user-friendly and can change. **API Names** should be stable and remain constant. Use descriptive labels for users, stable API names for code. Labels can change without affecting API names, but API names should remain constant to avoid breaking integrations and code.

### Q: When should I use Master-Detail vs Lookup relationships?

**A**: Use **Master-Detail** for parent-child relationships with cascade delete requirements. Use **Lookup** relationships when you need more flexibility. Remember: You can always use triggers or Rollup Helper to create calculated fields if you don't have a Master-Detail relationship.

### Q: Why are Search Layouts important?

**A**: **Search Layouts** are critical because users rely on search to find records. Poor search layouts reduce productivity, and search is a primary navigation mechanism. Always configure Search Layouts as part of object setup to ensure users can find records efficiently.

### Q: What should I consider when configuring objects for Experience Cloud (Communities)?

**A**: When configuring objects for Experience Cloud: (1) Ensure you go back to Classic to configure Communities-specific settings, (2) Ensure Communities users can't see inappropriate Views, (3) Configure sharing settings for community users, (4) Test object access from community user perspective, (5) Verify field visibility for community users.

### Q: Should I set Field-Level Security (FLS) during field creation or later?

**A**: Set **FLS permissions as you create fields**. This is easier to configure during creation, prevents security gaps, and ensures proper access control from the start. Don't defer FLS configuration - it's a critical security step.

## Edge Cases and Limitations

### Edge Case 1: Objects with Very Large Record Counts

**Scenario**: Objects with millions of records requiring special configuration considerations.

**Consideration**:
- Enable "Allow Search" carefully (may impact search performance)
- Consider deactivating "Track Field History" for high-volume objects (history tracking adds overhead)
- Use indexed fields for frequently queried fields
- Consider data archiving strategies for historical records
- Monitor object performance and adjust configuration as needed

### Edge Case 2: Objects with Complex Relationship Hierarchies

**Scenario**: Objects with many lookup or master-detail relationships creating complex data models.

**Consideration**:
- Limit master-detail relationships (maximum 2 per object)
- Use lookup relationships when cascade delete is not required
- Consider relationship depth when designing data model
- Test relationship traversal performance with large datasets
- Document relationship dependencies for maintenance

### Edge Case 3: Multi-Currency Objects

**Scenario**: Objects requiring multi-currency support with currency conversion.

**Consideration**:
- Enable "Allow Reports" for multi-currency objects (required for currency conversion)
- Configure currency fields appropriately (Currency data type)
- Test currency conversion in reports and formulas
- Understand currency conversion limitations (historical rates, conversion accuracy)
- Consider currency field requirements for international orgs

### Edge Case 4: Objects with Extensive Field History Tracking

**Scenario**: Objects with many fields tracked for history, creating large history tables.

**Consideration**:
- Limit field history tracking to essential fields (history tracking adds storage overhead)
- Monitor history table size and performance impact
- Consider data retention policies for history data
- Use field history tracking strategically (not all fields need tracking)
- Plan for history data archival if needed

### Edge Case 5: Objects Used in Experience Cloud (Communities)

**Scenario**: Objects accessed by community users requiring special configuration.

**Consideration**:
- Configure Communities-specific settings in Classic (not available in Lightning)
- Ensure appropriate sharing settings for community users
- Test object access from community user perspective
- Verify field visibility and FLS for community users
- Configure appropriate page layouts for community users
- Consider Sharing Sets for community user access (Customer Community licenses don't support sharing rules)

### Limitations

- **Master-Detail Relationships**: Maximum 2 master-detail relationships per object
- **Lookup Relationships**: Maximum 40 lookup relationships per object
- **Field History Tracking**: Limited to 20 fields per object (Enterprise and above)
- **Record Types**: Maximum 200 record types per object
- **Page Layouts**: Maximum 1,000 page layouts per object
- **Field Count**: Maximum 800 fields per object (varies by org edition)
- **Object Name Length**: Object API name limited to 40 characters
- **Tab Visibility**: Tab visibility settings affect all users with access to the tab
- **Search Layouts**: Limited customization options for search result layouts
- **Experience Cloud Configuration**: Some object settings must be configured in Classic, not Lightning

## Related Patterns

- See `rag/data-modeling/case-management-data-model.md` for case object modeling patterns
- See `rag/data-modeling/student-lifecycle-data-model.md` for education object modeling
- See `rag/data-modeling/external-ids-and-integration-keys.md` for external ID field configuration
- See `rag/security/permission-set-architecture.md` for permission configuration patterns

## References

- Trailhead: Objects Introduction - https://developer.salesforce.com/trailhead/force_com_introduction/data_modeling/objects_intro
- Trailhead: Object Relationships - https://developer.salesforce.com/trailhead/force_com_introduction/data_modeling/object_relationships
- Field-Level Security: https://help.salesforce.com/HTViewHelpDoc?id=admin_fls.htm

