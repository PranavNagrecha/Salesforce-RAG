---
title: "Standard Object Oddities and Constraints in Salesforce"
source: "The Salesforce Master Class wiki"
source_url: "https://github.com/Coding-With-The-Force/The-Salesforce-Master-Class/wiki"
topic: "Topic 4: The Complete Guide To Salesforce Architecture"
section: "Standard Object Oddities to Remember"
level: "Intermediate"
tags:
  - salesforce
  - architecture
  - standard-objects
  - constraints
  - best-practices
last_reviewed: "2025-01-XX"
---

# Overview

Standard Salesforce objects have various oddities, constraints, and special behaviors that architects and developers must understand. These differences impact data modeling, security configuration, automation design, and user experience. Knowing these oddities prevents design mistakes and enables effective solutions.

Standard object oddities encompass objects where quick actions aren't available, objects that can have queues own them, objects with restricted CRUD permissions, objects that can't be used in lookup relationships, and objects that support dynamic forms. Understanding these differences is critical for architecture and design.

Most standard objects follow consistent patterns, but exceptions exist. Architects must be aware of these exceptions to design effective solutions and avoid configuration errors.

# Core Concepts

## Standard Objects Where Quick Actions Are Not Available

**What it is**: Some standard objects don't support quick actions, limiting automation and user experience options.

**Objects without quick actions**:
- **Campaign Member**: Cannot create quick actions
- **Case Comment**: Cannot create quick actions
- **Email Message**: Cannot create quick actions
- **Event**: Cannot create quick actions (Task supports quick actions)
- **Note**: Cannot create quick actions
- **Solution**: Cannot create quick actions

**Impact**:
- Cannot create object-specific quick actions for these objects
- Limited automation options for these objects
- May need to use other mechanisms (buttons, links, flows) for actions

**Workarounds**:
- Use global quick actions if appropriate
- Use custom buttons or links
- Use Flow for custom actions
- Use Apex for programmatic actions

## Standard Objects That Can Have Queues Own Them

**What it is**: Some standard objects support queue ownership, enabling queue-based routing and assignment.

**Objects that support queues**:
- **Case**: Queues can own cases
- **Lead**: Queues can own leads
- **Service Contract**: Queues can own service contracts
- **Contract**: Queues can own contracts
- **Order**: Queues can own orders

**Objects that don't support queues**:
- **Account**: Cannot assign to queues
- **Contact**: Cannot assign to queues
- **Opportunity**: Cannot assign to queues
- **Campaign**: Cannot assign to queues

**Use cases**:
- **Queue-based routing**: Assign records to queues for team-based work
- **Work distribution**: Distribute work across team members
- **Assignment rules**: Use queues in assignment rules

**Best practices**:
- Use queues for objects that support them when queue-based routing is needed
- Understand queue ownership implications for sharing and visibility
- Design assignment rules with queue support in mind

## Standard Objects That Can't Have Object CRUD Updated in Profiles or Permission Sets

**What it is**: Some standard objects have fixed CRUD permissions that cannot be modified in profiles or permission sets.

**Objects with fixed CRUD**:
- **User**: Cannot modify CRUD permissions (all users have read access to other users)
- **Profile**: Cannot modify CRUD permissions
- **Permission Set**: Cannot modify CRUD permissions
- **Role**: Cannot modify CRUD permissions

**Impact**:
- Cannot restrict access to these objects through profiles or permission sets
- Must use other mechanisms (sharing rules, field-level security) for access control
- May need to use custom objects if restricted access is required

**Workarounds**:
- Use field-level security to restrict field access
- Use sharing rules for record-level access (where applicable)
- Use custom objects if restricted object-level access is required

## Standard Objects That Can't Be Used in Lookup Relationship Fields

**What it is**: Some standard objects cannot be used as parent objects in lookup or master-detail relationships.

**Objects that can't be lookup parents**:
- **User**: Cannot create lookup to User (use Owner field instead)
- **Profile**: Cannot create lookup to Profile
- **Permission Set**: Cannot create lookup to Permission Set
- **Role**: Cannot create lookup to Role
- **Group**: Cannot create lookup to Group (use sharing instead)

**Impact**:
- Cannot create direct relationships to these objects
- Must use alternative approaches (Owner fields, sharing, custom objects)

**Workarounds**:
- Use Owner fields for user relationships
- Use sharing for group relationships
- Create custom objects that mirror needed relationships if required

## Standard Objects That Can Use Dynamic Forms

**What it is**: Some standard objects support dynamic forms (field visibility based on record data), while others don't.

**Objects that support dynamic forms**:
- **Account**: Supports dynamic forms
- **Contact**: Supports dynamic forms
- **Opportunity**: Supports dynamic forms
- **Case**: Supports dynamic forms
- **Lead**: Supports dynamic forms
- **Custom objects**: Support dynamic forms

**Objects that don't support dynamic forms**:
- **Campaign**: Does not support dynamic forms
- **Campaign Member**: Does not support dynamic forms
- **Event**: Does not support dynamic forms
- **Task**: Does not support dynamic forms (in some contexts)

**Impact**:
- Can use dynamic forms for conditional field visibility on supported objects
- Must use page layouts or other mechanisms for objects that don't support dynamic forms

**Best practices**:
- Use dynamic forms for supported objects when conditional field visibility is needed
- Use page layouts or other mechanisms for objects that don't support dynamic forms
- Design user experience with dynamic form capabilities in mind

# Deep-Dive Patterns & Best Practices

## Design Patterns for Object Constraints

### Queue-Based Routing Pattern

**Pattern**: Use queues for objects that support them to enable team-based work distribution.

**When to use**: Objects that support queues (Case, Lead) when queue-based routing is needed.

**Approach**:
- Create queues for work distribution
- Use assignment rules to assign records to queues
- Use queue membership for team access
- Design sharing model with queue ownership in mind

**Benefits**: Enables team-based work, flexible assignment, scalable routing.

### Owner Field Pattern

**Pattern**: Use Owner fields for user relationships instead of lookup relationships.

**When to use**: When need to relate records to users, but User object can't be lookup parent.

**Approach**:
- Use standard Owner field when available
- Use custom Owner lookup field if needed
- Design sharing model with ownership in mind

**Benefits**: Leverages standard ownership model, supports sharing rules, enables assignment.

### Dynamic Forms Pattern

**Pattern**: Use dynamic forms for conditional field visibility on supported objects.

**When to use**: Objects that support dynamic forms when conditional field visibility is needed.

**Approach**:
- Use dynamic forms for supported objects
- Configure field visibility rules based on record data
- Use page layouts for objects that don't support dynamic forms

**Benefits**: Better user experience, reduced page layout complexity, conditional visibility.

## Common Design Mistakes

### Trying to Create Quick Actions on Unsupported Objects

**Mistake**: Attempting to create quick actions on objects that don't support them.

**Solution**: Use global quick actions, custom buttons, links, or Flow for actions on these objects.

### Trying to Assign Unsupported Objects to Queues

**Mistake**: Attempting to assign objects to queues when objects don't support queue ownership.

**Solution**: Use other assignment mechanisms (assignment rules with users, custom assignment logic).

### Trying to Modify Fixed CRUD Permissions

**Mistake**: Attempting to modify CRUD permissions for objects with fixed permissions.

**Solution**: Use field-level security, sharing rules, or custom objects if restricted access is needed.

### Trying to Create Lookup to Unsupported Objects

**Mistake**: Attempting to create lookup relationships to objects that can't be lookup parents.

**Solution**: Use Owner fields, sharing, or custom objects for relationships.

# Implementation Guide

## Prerequisites

- Understanding of standard object capabilities and constraints
- Knowledge of Salesforce object model
- Understanding of security and sharing model

## High-Level Steps

1. **Identify object requirements**: What objects are needed? What capabilities are required?
2. **Check object constraints**: Do objects support required capabilities?
3. **Design workarounds**: If constraints exist, design alternative approaches
4. **Implement solution**: Use supported capabilities or workarounds
5. **Test and validate**: Test solution with object constraints in mind

## Key Configuration Decisions

**Object selection**: Which objects to use? Consider capabilities and constraints.

**Relationship design**: How to relate objects? Consider lookup constraints and alternatives.

**Assignment design**: How to assign records? Consider queue support and alternatives.

**Security design**: How to secure objects? Consider CRUD constraints and alternatives.

# Common Pitfalls & Anti-Patterns

## Bad Pattern: Assuming All Objects Support All Features

**Why it's bad**: Standard objects have different capabilities. Assuming all objects support all features leads to design mistakes.

**Better approach**: Check object capabilities before designing. Understand constraints. Design with constraints in mind.

## Bad Pattern: Not Understanding Queue Support

**Why it's bad**: Queue-based routing is powerful but not all objects support it. Not understanding support leads to design mistakes.

**Better approach**: Understand which objects support queues. Use queues for supported objects. Use alternatives for unsupported objects.

## Bad Pattern: Trying to Override Fixed Permissions

**Why it's bad**: Some objects have fixed CRUD permissions that can't be modified. Trying to override leads to configuration errors.

**Better approach**: Understand fixed permissions. Use field-level security or sharing rules for access control. Use custom objects if restricted access is required.

## Bad Pattern: Not Considering Dynamic Forms Support

**Why it's bad**: Dynamic forms provide better user experience but not all objects support them. Not considering support leads to suboptimal designs.

**Better approach**: Use dynamic forms for supported objects. Use page layouts for unsupported objects. Design with capabilities in mind.

# Real-World Scenarios

## Scenario 1: Need Queue-Based Case Routing

**Problem**: Need to route cases to queues for team-based work distribution.

**Context**: Case object supports queues, need queue-based assignment.

**Solution**: Create queues for case routing. Use assignment rules to assign cases to queues. Design sharing model with queue ownership. Benefits: Team-based work, flexible assignment, scalable routing.

## Scenario 2: Need Quick Action on Campaign Member

**Problem**: Need to create quick action for Campaign Member object.

**Context**: Campaign Member doesn't support quick actions.

**Solution**: Use global quick action if appropriate, or use custom button/link, or use Flow for action. Benefits: Workaround for constraint, maintains functionality.

## Scenario 3: Need Restricted Access to User Object

**Problem**: Need to restrict access to User object for some users.

**Context**: User object has fixed CRUD permissions that can't be modified.

**Solution**: Use field-level security to restrict field access. Use sharing rules for record-level access where applicable. Use custom object if object-level restriction is required. Benefits: Workaround for constraint, maintains security.

# Checklist / Mental Model

## Designing with Object Constraints

- [ ] Identify required objects and capabilities
- [ ] Check object constraints (quick actions, queues, CRUD, lookups, dynamic forms)
- [ ] Design workarounds if constraints exist
- [ ] Test solution with constraints in mind
- [ ] Document constraints and workarounds

## Understanding Object Capabilities

- [ ] Know which objects support quick actions
- [ ] Know which objects support queues
- [ ] Know which objects have fixed CRUD
- [ ] Know which objects can't be lookup parents
- [ ] Know which objects support dynamic forms

## Mental Model: Objects Have Different Capabilities

Think of standard objects as having different capabilities and constraints. Not all objects support all features. Check capabilities before designing. Design with constraints in mind. Use workarounds when needed.

# Key Terms & Definitions

- **Quick actions**: Actions that can be added to page layouts for quick record creation or updates
- **Queue ownership**: Ability for queues to own records for team-based work distribution
- **CRUD permissions**: Create, Read, Update, Delete permissions for objects
- **Lookup relationship**: Relationship between objects using lookup fields
- **Dynamic forms**: Field visibility based on record data, replacing traditional page layouts
- **Fixed permissions**: CRUD permissions that cannot be modified in profiles or permission sets

## Q&A

### Q: Which standard objects don't support quick actions?

**A**: Objects that don't support quick actions: **Campaign Member, Case Comment, Email Message, Event, Note, and Solution**. Workarounds: (1) **Use global quick actions** if appropriate, (2) **Use custom buttons or links**, (3) **Use Flow** for custom actions, (4) **Use Apex** for programmatic actions. Choose workaround based on use case and requirements.

### Q: Which standard objects can have queues own them?

**A**: Objects that support queue ownership: **Case, Lead, Service Contract, Contract, and Order**. Objects that cannot be assigned to queues: **Account, Contact, Opportunity, and Campaign**. Use queues for supported objects when queue-based routing is needed. Queues enable team-based work distribution.

### Q: Which standard objects have fixed CRUD permissions that can't be modified?

**A**: Objects with fixed CRUD: **User, Profile, Permission Set, and Role**. These objects have CRUD permissions that cannot be modified in profiles or permission sets. Workarounds: (1) **Use field-level security** to restrict field access, (2) **Use sharing rules** for record-level access where applicable, (3) **Use custom objects** if object-level restriction is required.

### Q: Which standard objects can't be used as lookup relationship parents?

**A**: Objects that can't be lookup parents: **User, Profile, Permission Set, Role, and Group**. Workarounds: (1) **Use Owner fields** for user relationships (standard ownership model), (2) **Use sharing** for group relationships, (3) **Use custom objects** if needed. Owner fields leverage standard ownership model and support sharing rules.

### Q: Which standard objects support dynamic forms?

**A**: Objects that support dynamic forms: **Account, Contact, Opportunity, Case, Lead, and custom objects**. Objects that don't support dynamic forms: **Campaign, Campaign Member, Event, and Task** (in some contexts). Use dynamic forms for supported objects, page layouts for unsupported objects. Dynamic forms enable field visibility based on record data.

### Q: How do I work around objects that don't support quick actions?

**A**: Workarounds: (1) **Use global quick actions** if appropriate (available across objects), (2) **Use custom buttons or links** (object-specific actions), (3) **Use Flow** for custom actions (flexible automation), (4) **Use Apex** for programmatic actions (code-based). Choose workaround based on use case and requirements.

### Q: How do I implement queue-based routing for objects that support queues?

**A**: Implement by: (1) **Create queues** for work distribution, (2) **Use assignment rules** to assign records to queues, (3) **Use queue membership** for team access, (4) **Design sharing model** with queue ownership in mind. Works for Case, Lead, and other supported objects. Queues enable team-based routing and workload distribution.

### Q: How do I restrict access to objects with fixed CRUD permissions?

**A**: Restrict access by: (1) **Use field-level security** to restrict field access (control field visibility), (2) **Use sharing rules** for record-level access where applicable (control record visibility), (3) **Use custom objects** if object-level restriction is required. Cannot modify CRUD for User, Profile, Permission Set, or Role - use workarounds.

### Q: How do I relate records to users when User can't be lookup parent?

**A**: Relate by: (1) **Use standard Owner field** when available (leverages ownership model), (2) **Use custom Owner lookup field** if needed (custom ownership), (3) **Design sharing model** with ownership in mind. Owner fields leverage standard ownership model and support sharing rules. Ownership enables sharing and access control.

### Q: What's the impact of object constraints on architecture design?

**A**: Constraints impact: (1) **Data modeling** (relationship design - can't use User as lookup parent), (2) **Security design** (access control - fixed CRUD on some objects), (3) **Automation design** (quick actions, assignment - not all objects support), (4) **User experience** (dynamic forms - not all objects support). Architects must understand constraints to design effective solutions and avoid configuration errors.

## Related Patterns

- <a href="{{ '/rag/data-modeling/object-setup-and-configuration.html' | relative_url }}">Object Setup and Configuration</a> - Object configuration patterns
- <a href="{{ '/rag/data-modeling/security/permission-set-architecture.html' | relative_url }}">Permission Set Architecture</a> - Access control patterns
- <a href="{{ '/rag/data-modeling/security/sharing-fundamentals.html' | relative_url }}">Sharing Fundamentals</a> - Sharing model patterns

