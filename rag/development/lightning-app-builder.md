---
layout: default
title: Overview
description: Documentation for Overview
permalink: /rag/development/lightning-app-builder.html
---

# Overview

Lightning App Builder is a drag-and-drop tool for creating custom Lightning pages without code. It enables administrators to build responsive, component-based pages for record detail views, app home pages, and object home pages, providing flexible user experiences tailored to business needs.

Lightning App Builder uses Lightning components (both standard and custom) that can be arranged on pages with responsive layouts. Dynamic Forms and Dynamic Actions extend page layout capabilities by enabling field-level and action-level visibility rules, reducing the need for multiple page layouts.

Understanding Lightning App Builder enables administrators to create modern, responsive user interfaces that improve user experience and productivity. Combined with Dynamic Forms and Dynamic Actions, it provides powerful declarative UI customization capabilities.

# Core Concepts

## Lightning App Builder

**What it is**: Visual, drag-and-drop tool for building Lightning pages using Lightning components.

**Key characteristics**:
- No code required
- Component-based architecture
- Responsive layouts
- Supports record pages, app pages, and home pages
- Real-time preview
- Mobile-responsive design

**Page types**:
- **Record Pages**: Custom detail pages for specific objects
- **App Pages**: Custom pages for Lightning apps
- **Home Pages**: Custom home pages for apps or objects

**Best practice**: Use Lightning App Builder to create modern, responsive user interfaces. Leverage standard Lightning components before building custom components. Test pages with different user profiles and devices.

## Lightning Components

**What it is**: Reusable UI elements that can be added to Lightning pages.

**Component types**:
- **Standard Components**: Built-in Salesforce components (fields, related lists, charts, etc.)
- **Custom Components**: Custom Lightning Web Components or Aura components
- **AppExchange Components**: Third-party components from AppExchange

**Common standard components**:
- Fields (individual fields or field sets)
- Related Lists
- Charts and Reports
- Chatter Feed
- Files and Notes
- Record Detail
- Utility Bar

**Best practice**: Use standard components when possible. Build custom components only when standard components are insufficient. Test components with different data scenarios.

## Dynamic Forms

**What it is**: Feature that enables field-level visibility rules on record pages, reducing the need for multiple page layouts.

**Key characteristics**:
- Field-level visibility rules
- Conditional field display
- Reduces page layout complexity
- Works with Lightning App Builder
- Supports complex visibility logic

**Benefits**:
- Single page layout for multiple scenarios
- Field-level control without multiple layouts
- Easier maintenance and updates
- Better user experience with conditional fields

**Best practice**: Use Dynamic Forms to reduce page layout complexity. Create field visibility rules based on record type, field values, or user profile. Test visibility rules with different scenarios.

## Dynamic Actions

**What it is**: Feature that enables action-level visibility rules on record pages, controlling which actions (buttons, quick actions) are visible.

**Key characteristics**:
- Action-level visibility rules
- Conditional action display
- Reduces action configuration complexity
- Works with Lightning App Builder
- Supports complex visibility logic

**Benefits**:
- Single action configuration for multiple scenarios
- Action-level control without multiple configurations
- Easier maintenance and updates
- Better user experience with conditional actions

**Best practice**: Use Dynamic Actions to control action visibility based on record type, field values, or user profile. Test action visibility with different scenarios.

# Deep-Dive Patterns & Best Practices

## Lightning Page Design Patterns

**Pattern 1 - Record Detail Pages**:
Create custom record detail pages with relevant components, fields, and related lists organized for user workflows.

**Components to include**:
- Record detail component with key fields
- Related lists for important relationships
- Chatter feed for collaboration
- Charts for data visualization
- Custom components for specialized functionality

**Pattern 2 - App Home Pages**:
Create custom home pages for Lightning apps with dashboards, reports, and key metrics.

**Components to include**:
- Dashboard components
- Report components
- Key metric components
- Navigation components
- Custom components for app-specific functionality

**Pattern 3 - Object Home Pages**:
Create custom home pages for objects with list views, filters, and quick actions.

**Components to include**:
- List view components
- Filter components
- Quick action components
- Chart components
- Custom components for object-specific functionality

**Best practice**: Design pages based on user workflows. Organize components logically. Test pages with end users. Iterate based on feedback.

## Dynamic Forms Patterns

**Pattern 1 - Record Type-Based Visibility**:
Show different fields based on record type.

**Example**: Show "Student ID" field only for "Student" record type, "Employee ID" field only for "Employee" record type.

**Pattern 2 - Status-Based Visibility**:
Show fields based on record status or stage.

**Example**: Show "Closed Date" field only when Status is "Closed". Show "Approval Comments" field only when Status is "Pending Approval".

**Pattern 3 - User Profile-Based Visibility**:
Show fields based on user profile or permission sets.

**Example**: Show "Internal Notes" field only for internal staff profiles. Show "Public Information" fields for all users.

**Best practice**: Use Dynamic Forms to reduce page layout complexity. Create visibility rules based on business logic. Test visibility rules with different record types, statuses, and user profiles.

## Dynamic Actions Patterns

**Pattern 1 - Record Type-Based Actions**:
Show different actions based on record type.

**Example**: Show "Convert to Opportunity" action only for "Lead" record type. Show "Close Case" action only for "Case" record type.

**Pattern 2 - Status-Based Actions**:
Show actions based on record status.

**Example**: Show "Submit for Approval" action only when Status is "Draft". Show "Reopen" action only when Status is "Closed".

**Pattern 3 - User Role-Based Actions**:
Show actions based on user role or profile.

**Example**: Show "Approve" action only for managers. Show "Edit" action only for record owners.

**Best practice**: Use Dynamic Actions to control action visibility based on business logic. Test action visibility with different scenarios. Ensure users have appropriate actions for their workflows.

## Component Selection and Configuration

**Standard component selection**:
- Use standard components when possible
- Evaluate component capabilities before building custom
- Test components with different data scenarios
- Configure components appropriately

**Custom component development**:
- Build custom components only when standard components are insufficient
- Follow Lightning Web Component best practices
- Test custom components thoroughly
- Document component purpose and usage

**Best practice**: Prefer standard components. Build custom components only when necessary. Test all components with different scenarios and user profiles.

# Implementation Guide

## Lightning Page Creation Process

1. **Identify page need**: Determine what type of page is needed (record, app, home)
2. **Design page layout**: Design component layout and organization
3. **Create Lightning page**: Create page in Lightning App Builder
4. **Add components**: Add and configure Lightning components
5. **Configure responsive behavior**: Configure mobile and tablet layouts
6. **Set visibility rules**: Configure Dynamic Forms and Dynamic Actions if needed
7. **Test page**: Test with different user profiles and data scenarios
8. **Activate and assign**: Activate page and assign to appropriate users/apps

## Dynamic Forms Configuration Process

1. **Identify field visibility needs**: Determine which fields should be conditionally visible
2. **Design visibility rules**: Design rules based on record type, field values, or user profile
3. **Enable Dynamic Forms**: Enable Dynamic Forms on record page
4. **Configure field visibility**: Configure visibility rules for each field
5. **Test visibility**: Test with different record types, field values, and user profiles
6. **Deploy and verify**: Deploy to production and verify field visibility

## Dynamic Actions Configuration Process

1. **Identify action visibility needs**: Determine which actions should be conditionally visible
2. **Design visibility rules**: Design rules based on record type, field values, or user profile
3. **Enable Dynamic Actions**: Enable Dynamic Actions on record page
4. **Configure action visibility**: Configure visibility rules for each action
5. **Test visibility**: Test with different record types, field values, and user profiles
6. **Deploy and verify**: Deploy to production and verify action visibility

## Prerequisites

- System Administrator or appropriate permissions
- Understanding of user workflows and page requirements
- Understanding of Lightning components
- Understanding of Dynamic Forms and Dynamic Actions
- Access to Lightning App Builder

## Key Configuration Decisions

**Page design decisions**:
- What type of page is needed (record, app, home)?
- Which components should be included?
- How should components be organized?
- What responsive behavior is needed?

**Dynamic Forms decisions**:
- Which fields should be conditionally visible?
- What visibility rules are needed?
- Should visibility be based on record type, field values, or user profile?

**Dynamic Actions decisions**:
- Which actions should be conditionally visible?
- What visibility rules are needed?
- Should visibility be based on record type, field values, or user profile?

## Validation & Testing

**Page testing**:
- Test with different user profiles
- Test with different record types
- Test with different data scenarios
- Test responsive behavior on mobile and tablet
- Test component functionality
- Test page performance

**Dynamic Forms testing**:
- Test field visibility with different record types
- Test field visibility with different field values
- Test field visibility with different user profiles
- Verify fields appear/disappear correctly
- Test form submission and validation

**Dynamic Actions testing**:
- Test action visibility with different record types
- Test action visibility with different field values
- Test action visibility with different user profiles
- Verify actions appear/disappear correctly
- Test action functionality

**Tools to use**:
- Lightning App Builder for page creation
- Dynamic Forms configuration in page editor
- Dynamic Actions configuration in page editor
- Preview mode for testing
- Different user profiles for access testing

# Common Pitfalls & Anti-Patterns

## Over-Complex Page Designs

**Bad pattern**: Creating pages with too many components, complex layouts, or poor organization.

**Why it's bad**: Confuses users, reduces performance, and is difficult to maintain. Users may not find needed information or functionality.

**Better approach**: Keep pages simple and focused. Organize components logically. Test pages with end users. Iterate based on feedback.

## Not Using Dynamic Forms

**Bad pattern**: Creating multiple page layouts for different scenarios instead of using Dynamic Forms.

**Why it's bad**: Increases maintenance complexity, requires multiple layout assignments, and makes updates difficult.

**Better approach**: Use Dynamic Forms to reduce page layout complexity. Create field visibility rules based on business logic. Single page layout with conditional fields is easier to maintain.

## Not Testing Responsive Behavior

**Bad pattern**: Creating pages without testing mobile and tablet layouts.

**Why it's bad**: Pages may not work well on mobile devices, reducing user experience and adoption.

**Better approach**: Always test responsive behavior. Configure mobile and tablet layouts. Test on actual devices when possible.

## Not Using Standard Components

**Bad pattern**: Building custom components when standard components would suffice.

**Why it's bad**: Increases development time and maintenance burden. Standard components are tested and maintained by Salesforce.

**Better approach**: Use standard components when possible. Build custom components only when standard components are insufficient. Evaluate component capabilities before building custom.

## Ignoring User Feedback

**Bad pattern**: Creating pages without gathering user feedback or testing with end users.

**Why it's bad**: Pages may not match user workflows or needs, reducing adoption and productivity.

**Better approach**: Test pages with end users. Gather feedback and iterate. Design pages based on user workflows and needs.

# Real-World Scenarios

## Scenario 1 - Custom Case Detail Page

**Problem**: Need custom Case detail page with case information, related contacts, case history, and knowledge articles organized for service agents.

**Context**: Service Cloud implementation, service agents need efficient case management interface.

**Solution**: 
- Create Lightning record page for Case object
- Add record detail component with key case fields
- Add related list for case contacts
- Add case history component
- Add knowledge article component
- Add Chatter feed for collaboration
- Configure Dynamic Forms for field visibility by case type
- Configure Dynamic Actions for action visibility by case status

**Key decisions**: Use Lightning App Builder for modern interface. Use Dynamic Forms to reduce layout complexity. Organize components for service agent workflow.

## Scenario 2 - App Home Page with Metrics

**Problem**: Need custom home page for Sales app with key metrics, recent opportunities, and quick actions.

**Context**: Sales Cloud implementation, sales team needs dashboard-style home page.

**Solution**:
- Create Lightning app page for Sales app
- Add dashboard component with key sales metrics
- Add report component for recent opportunities
- Add quick action components
- Add navigation components
- Configure responsive layouts

**Key decisions**: Use app page for home page. Include key metrics and quick actions. Test responsive behavior.

## Scenario 3 - Dynamic Forms for Record Types

**Problem**: Need single page layout for Account object supporting multiple record types with different field requirements.

**Context**: Account object with "Customer" and "Partner" record types, different fields needed for each type.

**Solution**:
- Enable Dynamic Forms on Account record page
- Configure field visibility rules based on record type
- Show "Customer ID" field only for "Customer" record type
- Show "Partner Agreement" field only for "Partner" record type
- Show common fields for all record types
- Single page layout with conditional fields

**Key decisions**: Use Dynamic Forms to reduce layout complexity. Single layout with conditional fields is easier to maintain than multiple layouts.

# Checklist / Mental Model

## Lightning Page Creation Checklist

When creating Lightning pages:

1. **Identify page type**: Record page, app page, or home page?
2. **Design layout**: How should components be organized?
3. **Select components**: Which standard or custom components are needed?
4. **Configure components**: Configure each component appropriately
5. **Set visibility rules**: Configure Dynamic Forms and Dynamic Actions if needed
6. **Test thoroughly**: Test with different user profiles, record types, and data scenarios
7. **Test responsive**: Test mobile and tablet layouts
8. **Activate and assign**: Activate page and assign to appropriate users/apps

## Lightning App Builder Mental Model

**Use Lightning App Builder for modern UI**: Use Lightning App Builder to create modern, responsive user interfaces. Leverage standard components before building custom.

**Use Dynamic Forms to reduce complexity**: Use Dynamic Forms to reduce page layout complexity. Single layout with conditional fields is easier to maintain than multiple layouts.

**Design for user workflows**: Design pages based on user workflows and needs. Test with end users and iterate based on feedback.

**Test responsive behavior**: Always test responsive behavior on mobile and tablet. Configure mobile and tablet layouts appropriately.

**Iterate based on feedback**: Gather user feedback and iterate on page design. Pages should evolve based on user needs and feedback.

# Key Terms & Definitions

- **Lightning App Builder**: Visual, drag-and-drop tool for building Lightning pages
- **Lightning Page**: Custom page built with Lightning App Builder (record page, app page, or home page)
- **Lightning Component**: Reusable UI element that can be added to Lightning pages
- **Dynamic Forms**: Feature enabling field-level visibility rules on record pages
- **Dynamic Actions**: Feature enabling action-level visibility rules on record pages
- **Record Page**: Custom detail page for specific objects
- **App Page**: Custom page for Lightning apps
- **Home Page**: Custom home page for apps or objects
- **Visibility Rule**: Condition determining when fields or actions are visible
- **Responsive Layout**: Layout that adapts to different screen sizes (desktop, tablet, mobile)

# RAG-Friendly Q&A Seeds

**Q:** What's the difference between Lightning App Builder and page layouts?

**A:** Lightning App Builder creates Lightning pages (record pages, app pages, home pages) using drag-and-drop components. Page layouts are Classic UI configurations that control field organization on record detail pages. Lightning App Builder provides more flexibility, modern UI, and component-based architecture. Use Lightning App Builder for Lightning Experience, page layouts for Classic (though Lightning pages can replace page layouts in Lightning Experience).

**Q:** When should I use Dynamic Forms?

**A:** Use Dynamic Forms when you need field-level visibility rules on record pages. Dynamic Forms enable conditional field display based on record type, field values, or user profile, reducing the need for multiple page layouts. Use Dynamic Forms to simplify page layout management and provide better user experience with conditional fields.

**Q:** How do I create a custom Lightning page?

**A:** Create custom Lightning page by: (1) Navigate to Lightning App Builder, (2) Click "New" and select page type (Record Page, App Page, or Home Page), (3) Select object or app, (4) Drag and drop components onto page, (5) Configure components, (6) Set visibility rules if needed (Dynamic Forms/Dynamic Actions), (7) Test page, (8) Activate and assign to users/apps.

**Q:** What components can I add to Lightning pages?

**A:** You can add: (1) Standard Salesforce components (fields, related lists, charts, reports, Chatter, etc.), (2) Custom Lightning Web Components or Aura components, (3) AppExchange components from AppExchange. Standard components are recommended when possible. Build custom components only when standard components are insufficient.

**Q:** How do Dynamic Actions work?

**A:** Dynamic Actions enable action-level visibility rules on record pages. You can configure actions (buttons, quick actions) to be visible based on record type, field values, or user profile. This reduces action configuration complexity and provides better user experience with conditional actions. Enable Dynamic Actions on record page, then configure visibility rules for each action.

**Q:** Can I use Lightning App Builder for mobile pages?

**A:** Yes, Lightning App Builder supports responsive layouts for mobile and tablet. Configure mobile and tablet layouts when creating pages. Test responsive behavior on actual devices. Lightning pages automatically adapt to different screen sizes, but you can customize mobile and tablet layouts for optimal experience.

**Q:** How do I test Lightning pages before deploying?

**A:** Test Lightning pages by: (1) Using preview mode in Lightning App Builder, (2) Testing with different user profiles, (3) Testing with different record types, (4) Testing with different data scenarios, (5) Testing responsive behavior on mobile and tablet, (6) Testing component functionality, (7) Testing Dynamic Forms and Dynamic Actions visibility rules. Always test in sandbox before production deployment.

## Related Patterns

**See Also**:
- <a href="{{ '/rag/development/lwc-patterns.html' | relative_url }}">LWC Patterns</a> - Custom Lightning Web Component development
- <a href="{{ '/rag/development/admin-basics.html' | relative_url }}">Admin Basics</a> - Page layout and UI configuration

**Related Domains**:
- <a href="{{ '/rag/development/architecture/portal-architecture.html' | relative_url }}">Portal Architecture</a> - Experience Cloud page patterns
- <a href="{{ '/rag/development/architecture/mobile-strategy.html' | relative_url }}">Mobile Strategy</a> - Mobile page optimization

