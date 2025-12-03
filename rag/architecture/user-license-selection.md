---
title: "Salesforce User License Selection"
source: "The Salesforce Master Class wiki"
source_url: "https://github.com/Coding-With-The-Force/The-Salesforce-Master-Class/wiki"
topic: "Topic 1: How to evaluate Salesforce for your business"
section: "Understanding Salesforce, its products, and its licenses"
level: "Beginner"
tags:
  - salesforce
  - user-licenses
  - licensing
  - evaluation
  - best-practices
last_reviewed: "2025-01-XX"
---

# Overview

Salesforce user licenses determine what functionality users can access, what data they can see, and what actions they can perform in the org. Selecting the right user license types is critical for providing appropriate access while controlling licensing costs.

User licenses come in different types (Salesforce, Platform, Service Cloud, Experience Cloud, etc.) that provide different levels of access to standard objects, custom objects, and platform features. Each license type has specific capabilities and limitations that must align with user roles and responsibilities.

Understanding license types requires evaluating user needs, access requirements, and cost optimization opportunities. The decision impacts both user experience and total cost of ownership, making license selection a key component of Salesforce planning.

# Core Concepts

## Salesforce License

**What it is**: Full-featured license providing access to standard Salesforce objects (Accounts, Contacts, Opportunities, Cases, etc.) and all platform capabilities.

**Key characteristics**:
- Access to standard Sales and Service Cloud objects
- Full platform capabilities (custom objects, automation, etc.)
- Can be assigned to Sales Cloud or Service Cloud users
- Suitable for users who need standard CRM functionality

**When to use**: Users who need access to standard Salesforce objects (Accounts, Contacts, Opportunities, Cases, Leads, etc.) and standard CRM functionality.

**Common use cases**: Sales representatives, account managers, service agents, case workers, managers who need full CRM access.

## Platform License

**What it is**: Limited license providing access to custom objects and limited standard objects, but not full Sales or Service Cloud functionality.

**Key characteristics**:
- Access to custom objects and custom applications
- Limited access to standard objects (typically Accounts, Contacts, and custom objects only)
- No access to Opportunities, Cases, Leads, or other standard Sales/Service Cloud objects
- Full platform capabilities (automation, development, etc.)
- Typically less expensive than full Salesforce licenses

**When to use**: Users who only need access to custom objects and don't need standard Sales or Service Cloud functionality.

**Common use cases**: Users of custom applications, users who only need Accounts/Contacts access, users who don't need Opportunities or Cases.

## Service Cloud License

**What it is**: License providing access to Service Cloud functionality (Cases, Knowledge, etc.) but not Sales Cloud functionality (Opportunities, Leads, etc.).

**Key characteristics**:
- Access to Service Cloud objects (Cases, Knowledge, etc.)
- Access to Accounts and Contacts
- No access to Sales Cloud objects (Opportunities, Leads, etc.)
- Full platform capabilities for custom objects
- Suitable for service-focused users

**When to use**: Users who need Service Cloud functionality but don't need Sales Cloud functionality.

**Common use cases**: Customer service agents, support staff, knowledge managers, users focused on case management.

## Experience Cloud License

**What it is**: License for external users accessing Experience Cloud sites (customer portals, partner portals, etc.).

**Key characteristics**:
- Access to Experience Cloud sites
- Controlled access to Salesforce data based on sharing rules and profiles
- Typically less expensive than internal user licenses
- Can be guest users (no license) or member users (licensed)

**When to use**: External users (customers, partners, citizens) who need portal access to Salesforce data.

**Common use cases**: Customer self-service portals, partner portals, citizen portals, external stakeholder access.

## Integration User License

**What it is**: Free API-only license for system-to-system integrations, included with Enterprise, Performance, and Unlimited editions.

**Key characteristics**:
- API access only (no UI access)
- Free license (included with certain editions)
- Suitable for integration users only
- Cannot be used for human users

**When to use**: System-to-system integrations that need API access to Salesforce.

**Common use cases**: Integration users for MuleSoft, Dell Boomi, or other integration platforms, API-only access for external systems.

## License Type Comparison

**Access to standard objects**:
- Salesforce License: Full access to all standard objects
- Platform License: Limited access (typically Accounts, Contacts, custom objects only)
- Service Cloud License: Service Cloud objects + Accounts/Contacts, no Sales Cloud objects
- Experience Cloud License: Controlled access based on sharing and profiles

**Cost considerations**:
- Salesforce License: Typically highest cost
- Platform License: Typically lower cost than full Salesforce license
- Service Cloud License: Typically similar to Salesforce license
- Experience Cloud License: Typically lower cost than internal licenses
- Integration User License: Free (with qualifying editions)

**Use case alignment**:
- Salesforce License: Users needing full CRM functionality
- Platform License: Users needing only custom functionality
- Service Cloud License: Service-focused users
- Experience Cloud License: External portal users
- Integration User License: System integrations only

# Deep-Dive Patterns & Best Practices

## License Selection Framework

**Step 1 - Assess user needs**:
- What objects does the user need to access?
- What functionality does the user need?
- Is the user internal or external?
- What is the user's primary role?

**Step 2 - Map needs to license types**:
- Full CRM needs → Salesforce License
- Custom app only → Platform License
- Service only → Service Cloud License
- External portal → Experience Cloud License
- System integration → Integration User License

**Step 3 - Evaluate cost optimization**:
- Can Platform licenses be used instead of full Salesforce licenses?
- Are Experience Cloud licenses appropriate for external users?
- Can Integration User licenses be used for system integrations?

**Decision pattern**: Match license type to user needs. Use Platform licenses for users who don't need standard CRM objects. Use Experience Cloud licenses for external users. Use Integration User licenses for system integrations.

## Common License Selection Patterns

**Pattern 1 - Platform License for Custom Apps**:
Use Platform licenses for users who only need access to custom objects and don't need standard Sales or Service Cloud functionality. This reduces licensing costs while providing necessary access.

**Pattern 2 - Service Cloud License for Service Teams**:
Use Service Cloud licenses for users focused on case management and service delivery who don't need Sales Cloud functionality (Opportunities, Leads, etc.).

**Pattern 3 - Experience Cloud License for External Users**:
Use Experience Cloud licenses (or guest access) for external users accessing portals rather than full internal user licenses. This provides appropriate access at lower cost.

**Pattern 4 - Integration User License for System Integrations**:
Use free Integration User licenses for system-to-system integrations rather than full user licenses. Integration User licenses provide API access without UI access.

## License Cost Optimization

**Platform license optimization**:
- Identify users who don't need Opportunities, Cases, or Leads
- Use Platform licenses for custom application users
- Use Platform licenses for users who only need Accounts/Contacts access
- Can significantly reduce licensing costs

**Experience Cloud optimization**:
- Use Experience Cloud licenses for external users instead of internal licenses
- Consider guest user access where appropriate (no license cost)
- Configure sharing appropriately for external user access

**Integration user optimization**:
- Use free Integration User licenses for all system-to-system integrations
- Don't use full user licenses for integration purposes
- Integration User licenses are included with Enterprise, Performance, and Unlimited editions

**Best practice**: Regularly review license assignments to ensure users have appropriate licenses. Optimize license types to reduce costs while maintaining necessary functionality.

## License and Profile/Permission Set Relationship

**License determines available objects**:
- License type determines which standard objects are available
- Profiles and Permission Sets control access within license capabilities
- Cannot grant access to objects not included in license type

**Profile and Permission Set control access**:
- Profiles control object and field access within license capabilities
- Permission Sets extend access within license capabilities
- Field-level security and sharing rules further control access

**Best practice**: License type provides the foundation for access. Profiles and Permission Sets control detailed access within license capabilities. Ensure license type aligns with user needs before configuring profiles and permission sets.

# Implementation Guide

## License Selection Process

1. **User role analysis**: Document what each user role needs to accomplish
2. **Object access requirements**: Identify which objects each role needs to access
3. **License type mapping**: Map user roles to appropriate license types
4. **Cost analysis**: Evaluate licensing costs for different license type combinations
5. **Access validation**: Confirm license types provide necessary access
6. **Optimization review**: Identify opportunities to use lower-cost license types

## Prerequisites

- Understanding of user roles and responsibilities
- Object access requirements for each role
- Internal vs. external user identification
- Integration requirements
- Budget constraints

## Key Configuration Decisions

**License type decisions**:
- Which license type provides necessary object access?
- Can Platform licenses be used instead of full Salesforce licenses?
- Are Experience Cloud licenses appropriate for external users?
- Can Integration User licenses be used for system integrations?

**Cost optimization decisions**:
- Which users can use Platform licenses?
- Which external users can use Experience Cloud licenses?
- Are all system integrations using Integration User licenses?

## Validation & Testing

**License selection validation**:
- Confirm license types provide necessary object access
- Verify users can accomplish required tasks with selected license types
- Test access with different license types in sandbox
- Validate cost estimates against budget constraints
- Assess upgrade path if license types need to change

**Tools to use**:
- Salesforce license type documentation
- Sandbox orgs for testing license types
- Salesforce account executives for licensing guidance
- User access testing with different license types

# Common Pitfalls & Anti-Patterns

## Over-Licensing Users

**Bad pattern**: Assigning full Salesforce licenses to users who only need Platform license capabilities (custom objects only, no standard CRM objects).

**Why it's bad**: Increases licensing costs without providing necessary value. Users don't benefit from additional capabilities, and org pays for unused functionality.

**Better approach**: Evaluate user needs carefully. Use Platform licenses for users who don't need standard CRM objects. Use Service Cloud licenses for service-focused users who don't need Sales Cloud functionality.

## Q&A

### Q: What is the difference between Standard User and Platform User licenses?

**A**: **Standard User** licenses provide access to standard Sales and Service Cloud objects (Accounts, Contacts, Opportunities, Cases, etc.) plus custom objects. **Platform User** licenses provide access only to custom objects and limited standard objects (Contacts, custom objects). Use Standard User for users who need CRM functionality; use Platform User for users who only need custom applications.

### Q: When should I use Experience Cloud licenses vs Standard User licenses?

**A**: Use **Experience Cloud licenses** for external users (customers, partners, citizens) who need portal access. Use **Standard User licenses** for internal employees who need full Salesforce access. Experience Cloud licenses are typically less expensive and designed for external user scenarios.

### Q: What is an Integration User License and when should I use it?

**A**: **Integration User License** is a free API-only license included with Enterprise, Performance, and Unlimited editions. Use it for system-to-system integrations that require API access but don't need UI access. Each org gets 5 free Integration User Licenses. Use Integration User Licenses instead of full user licenses for integration scenarios.

### Q: Can I mix different license types in the same org?

**A**: Yes, you can mix different license types in the same org. Users with different license types can work together, but each user's access is determined by their license type and assigned permissions. Mix license types strategically to optimize costs while meeting access requirements.

### Q: How do I determine which license type a user needs?

**A**: Determine license type by evaluating: (1) **Object access needs** (standard CRM objects vs custom objects only), (2) **User type** (internal employee vs external user), (3) **Access pattern** (UI access vs API-only), (4) **Feature requirements** (Sales Cloud, Service Cloud, custom apps). Match license type to user needs and responsibilities.

### Q: What happens if I assign the wrong license type to a user?

**A**: Users with insufficient license types may not be able to access required objects or features. Users with excessive license types increase costs without providing value. Test license types in sandbox before assigning in production. Monitor user access issues and adjust license assignments as needed.

### Q: How do I optimize license costs?

**A**: Optimize license costs by: (1) **Use Platform licenses** for users who don't need standard CRM objects, (2) **Use Experience Cloud licenses** for external users, (3) **Use Integration User licenses** for system integrations, (4) **Review license assignments regularly** to identify unused or over-licensed users, (5) **Right-size licenses** to user needs, (6) **Consider license consolidation** when appropriate.

### Q: Can I change a user's license type after assignment?

**A**: Yes, you can change a user's license type, but this may affect their access to objects and features. Test license type changes in sandbox first. Communicate changes to users. Update permission sets if needed. Monitor for access issues after license type changes.

## Related Patterns

**See Also**:
- <a href="{{ '/rag/architecture/architecture/org-edition-selection.html' | relative_url }}">Org Edition Selection</a> - Edition selection and license availability
- <a href="{{ '/rag/architecture/architecture/salesforce-pricing-negotiation.html' | relative_url }}">Salesforce Pricing Negotiation</a> - License cost optimization

**Related Domains**:
- <a href="{{ '/rag/architecture/integrations/integration-user-license-guide.html' | relative_url }}">Integration User License Guide</a> - Integration User License setup and configuration
- <a href="{{ '/rag/architecture/security/permission-set-architecture.html' | relative_url }}">Permission Set Architecture</a> - Permission management for different license types

## Under-Licensing Users

**Bad pattern**: Assigning Platform licenses to users who need access to Opportunities, Cases, or other standard objects not included in Platform licenses.

**Why it's bad**: Users cannot access required objects, preventing them from accomplishing their work. Requires license upgrade and may cause user frustration.

**Better approach**: Ensure license types provide necessary object access. Don't optimize costs at the expense of user functionality.

## Using Full Licenses for Integration Users

**Bad pattern**: Assigning full Salesforce licenses to integration users (system-to-system integrations) instead of using free Integration User licenses.

**Why it's bad**: Wastes expensive user licenses on system integrations. Integration User licenses are free and provide necessary API access.

**Better approach**: Use free Integration User licenses for all system-to-system integrations. Integration User licenses are included with Enterprise, Performance, and Unlimited editions.

## Not Optimizing External User Licenses

**Bad pattern**: Assigning internal user licenses to external users accessing Experience Cloud sites instead of using Experience Cloud licenses.

**Why it's bad**: Increases licensing costs. Experience Cloud licenses are typically less expensive and provide appropriate access for external users.

**Better approach**: Use Experience Cloud licenses for external portal users. Consider guest user access where appropriate (no license cost for read-only access).

# Real-World Scenarios

## Scenario 1 - Sales Organization with Custom App Users

**Problem**: A sales organization has 50 sales representatives who need full CRM access, and 20 custom app users who only need access to custom objects for a specialized application.

**Context**: Sales reps need Opportunities, Accounts, Contacts. Custom app users only need custom objects, no standard CRM objects.

**Solution**: 
- 50 Salesforce licenses for sales representatives
- 20 Platform licenses for custom app users

**Key decisions**: Use Platform licenses for custom app users to reduce costs while maintaining necessary access. Sales representatives need full Salesforce licenses for Opportunities and standard CRM functionality.

## Scenario 2 - Service Organization with External Portal

**Problem**: A service organization has 30 service agents who need case management, and 500 customers who need self-service portal access.

**Context**: Service agents need Cases, Knowledge, Accounts, Contacts. Customers need portal access to view their cases and update information.

**Solution**:
- 30 Service Cloud licenses for service agents
- 500 Experience Cloud licenses for customer portal users

**Key decisions**: Use Service Cloud licenses for service-focused internal users. Use Experience Cloud licenses for external customers rather than internal licenses. Configure sharing appropriately for customer access.

## Scenario 3 - Organization with System Integrations

**Problem**: An organization needs to integrate Salesforce with 3 external systems (ERP, marketing automation, billing system) requiring API access.

**Context**: Integrations need API access only, no UI access required. Organization has Enterprise edition.

**Solution**: 
- 3 Integration User licenses (free) for system integrations

**Key decisions**: Use free Integration User licenses for all system integrations. Integration User licenses provide API access without requiring expensive user licenses.

# Checklist / Mental Model

## License Selection Checklist

When selecting user license types, always ask:

1. **User needs**: What objects does the user need to access? What functionality is required?
2. **License capabilities**: Which license type provides necessary object access?
3. **Cost optimization**: Can a lower-cost license type meet user needs?
4. **External users**: Are Experience Cloud licenses appropriate for external users?
5. **Integration users**: Are Integration User licenses being used for system integrations?
6. **Access validation**: Do selected license types provide all necessary access?
7. **Future planning**: How will user needs evolve, and what license flexibility is needed?

## License Selection Mental Model

**Match license to needs**: Select license type that provides necessary object access without over-licensing. Use Platform licenses for users who don't need standard CRM objects.

**Optimize costs**: Use Platform licenses, Service Cloud licenses, and Experience Cloud licenses strategically to reduce costs while maintaining functionality.

**Use free licenses**: Always use free Integration User licenses for system-to-system integrations. Don't use expensive user licenses for integration purposes.

**Regular review**: Periodically review license assignments to ensure users have appropriate licenses and identify optimization opportunities.

# Key Terms & Definitions

- **Salesforce License**: Full-featured license providing access to standard Salesforce objects and all platform capabilities
- **Platform License**: Limited license providing access to custom objects and limited standard objects, typically less expensive than full Salesforce license
- **Service Cloud License**: License providing access to Service Cloud functionality (Cases, Knowledge) but not Sales Cloud functionality (Opportunities, Leads)
- **Experience Cloud License**: License for external users accessing Experience Cloud sites (portals)
- **Integration User License**: Free API-only license for system-to-system integrations, included with Enterprise, Performance, and Unlimited editions
- **Guest User**: Unlicensed user accessing Experience Cloud sites with read-only access (no license cost)
- **License Type**: Determines which standard objects are available to users
- **Profile**: Controls object and field access within license capabilities
- **Permission Set**: Extends access within license capabilities

# RAG-Friendly Q&A Seeds

**Q:** What's the difference between a Salesforce license and a Platform license?

**A:** A Salesforce license provides access to all standard Salesforce objects (Accounts, Contacts, Opportunities, Cases, Leads, etc.) and full platform capabilities. A Platform license provides access to custom objects and limited standard objects (typically Accounts, Contacts, and custom objects only) but not Opportunities, Cases, Leads, or other standard Sales/Service Cloud objects. Platform licenses are typically less expensive and suitable for users who only need custom functionality.

**Q:** When should I use a Platform license instead of a full Salesforce license?

**A:** Use Platform licenses for users who only need access to custom objects and don't need standard Sales or Service Cloud functionality (Opportunities, Cases, Leads, etc.). Platform licenses are suitable for custom application users, users who only need Accounts/Contacts access, or users who don't need standard CRM objects. Platform licenses can significantly reduce licensing costs.

**Q:** Can I use a Platform license for users who need to access Opportunities or Cases?

**A:** No, Platform licenses don't provide access to Opportunities, Cases, Leads, or other standard Sales/Service Cloud objects. Users who need these objects require full Salesforce licenses or Service Cloud licenses (for Cases). Platform licenses are limited to custom objects and typically Accounts/Contacts only.

**Q:** What's the difference between a Service Cloud license and a Salesforce license?

**A:** A Service Cloud license provides access to Service Cloud objects (Cases, Knowledge, etc.) and Accounts/Contacts, but not Sales Cloud objects (Opportunities, Leads, etc.). A Salesforce license provides access to both Sales and Service Cloud objects. Use Service Cloud licenses for service-focused users who don't need Sales Cloud functionality.

**Q:** When should I use Experience Cloud licenses?

**A:** Use Experience Cloud licenses for external users (customers, partners, citizens) who need portal access to Salesforce data. Experience Cloud licenses are typically less expensive than internal user licenses and provide appropriate access for external users. Consider guest user access (no license) for read-only external access where appropriate.

**Q:** Can I use Integration User licenses for human users?

**A:** No, Integration User licenses are API-only licenses intended for system-to-system integrations. They don't provide UI access and cannot be used for human users. Integration User licenses are free (with qualifying editions) and should be used for all system integrations rather than expensive user licenses.

**Q:** How do I optimize licensing costs?

**A:** Optimize licensing costs by: (1) Using Platform licenses for users who don't need standard CRM objects, (2) Using Service Cloud licenses for service-focused users who don't need Sales Cloud functionality, (3) Using Experience Cloud licenses for external portal users, (4) Using free Integration User licenses for all system integrations, (5) Regularly reviewing license assignments to ensure appropriate license types.

