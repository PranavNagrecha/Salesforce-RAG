---
title: "Choosing a Mobile Strategy for Salesforce"
source: "The Salesforce Master Class wiki"
source_url: "https://github.com/Coding-With-The-Force/The-Salesforce-Master-Class/wiki"
topic: "Topic 4: The Complete Guide To Salesforce Architecture"
section: "Choosing a Mobile Strategy for your Salesforce Org"
level: "Intermediate"
tags:
  - salesforce
  - architecture
  - mobile
  - strategy
  - best-practices
last_reviewed: "2025-01-XX"
---

# Overview

Mobile strategy is a critical architectural decision that impacts user experience, development approach, maintenance, and cost. Salesforce provides multiple mobile options, each with different capabilities, use cases, and tradeoffs. Choosing the right mobile strategy requires understanding user needs, use cases, and platform capabilities.

Mobile strategy encompasses evaluating different mobile options (Salesforce Mobile App, Experience Cloud mobile, custom mobile apps), understanding when to use each, and making informed decisions based on requirements. The decision impacts development effort, user experience, offline capabilities, and long-term maintenance.

Most organizations start with the Salesforce Mobile App, which provides good coverage for standard CRM use cases. Custom mobile apps or Experience Cloud mobile are appropriate when there are specific requirements that standard mobile app can't meet, such as custom user experiences, offline requirements, or specialized workflows.

# Core Concepts

## Salesforce Mobile App

**What it is**: Native mobile application provided by Salesforce for iOS and Android that provides access to Salesforce data and functionality.

**Key characteristics**:
- Pre-built mobile app (no custom development required)
- Access to standard and custom objects
- Offline capabilities (sync data for offline access)
- Mobile-optimized UI for standard Salesforce features
- Push notifications
- Mobile-specific features (barcode scanning, location services)

**Advantages**:
- **No development required**: Use out-of-the-box
- **Regular updates**: Salesforce maintains and updates app
- **Offline support**: Sync data for offline access
- **Security**: Built-in security and authentication
- **Cost**: Included with Salesforce licenses

**Disadvantages**:
- **Limited customization**: Can't fully customize UI/UX
- **Standard workflows**: Optimized for standard Salesforce processes
- **Branding limitations**: Limited ability to customize branding
- **Feature limitations**: Some features may not be available on mobile

**When to use**:
- Standard CRM use cases (accounts, contacts, opportunities, cases)
- Users need mobile access to Salesforce data
- Offline access is needed
- Quick deployment without custom development
- Standard Salesforce workflows are sufficient

## Experience Cloud Mobile

**What it is**: Mobile-optimized Experience Cloud sites that provide custom user experiences for external users (customers, partners, community members).

**Key characteristics**:
- Mobile-responsive web experience
- Custom branding and UI
- Access to Experience Cloud data and functionality
- Works in mobile browsers
- Can be "installed" as web app (add to home screen)

**Advantages**:
- **Custom branding**: Full control over look and feel
- **Custom user experience**: Design specific workflows and interfaces
- **No app store**: Deploy as web app, no app store approval needed
- **Easier updates**: Update web app without app store approval
- **Cross-platform**: Works on iOS and Android (and desktop)

**Disadvantages**:
- **Limited offline**: Web-based, limited offline capabilities
- **Performance**: May be slower than native app
- **Device features**: Limited access to device features (camera, GPS, etc.)
- **User experience**: May not feel as native as mobile app

**When to use**:
- External users (customers, partners) need mobile access
- Custom user experience is required
- Custom branding is important
- Web-based deployment is preferred
- Offline requirements are minimal

## Custom Mobile Apps

**What it is**: Custom-built native or hybrid mobile applications built using Salesforce Mobile SDK or other frameworks.

**Key characteristics**:
- Fully custom UI/UX
- Native or hybrid app development
- Full access to device features
- Custom offline capabilities
- App store distribution

**Advantages**:
- **Full customization**: Complete control over UI/UX
- **Native experience**: Can feel more native and performant
- **Device features**: Full access to device capabilities
- **Custom offline**: Can implement custom offline strategies
- **Branding**: Complete branding control

**Disadvantages**:
- **Development cost**: Requires custom development
- **Maintenance**: Must maintain and update app
- **App store**: Requires app store approval and distribution
- **Complexity**: More complex to build and maintain
- **Cost**: Higher development and maintenance costs

**When to use**:
- Standard mobile app doesn't meet requirements
- Custom user experience is critical
- Specialized workflows or features needed
- Full offline capabilities required
- Budget and resources available for custom development

## Hybrid Approaches

**What it is**: Combination of mobile options, using different approaches for different user types or use cases.

**Key characteristics**:
- Salesforce Mobile App for internal users
- Experience Cloud mobile for external users
- Custom apps for specialized use cases
- Different strategies for different user groups

**Advantages**:
- **Right tool for right job**: Use best option for each use case
- **Flexibility**: Can optimize for different user needs
- **Cost optimization**: Use standard options where possible, custom where needed

**Disadvantages**:
- **Complexity**: Managing multiple mobile approaches
- **Consistency**: Different experiences for different users
- **Maintenance**: Multiple systems to maintain

**When to use**:
- Different user types have different needs
- Some users need standard mobile app, others need custom experience
- Cost optimization (use standard where possible, custom where needed)

# Deep-Dive Patterns & Best Practices

## Decision Framework

### User Type

**Question**: Who are the mobile users?

**Internal users (employees)**: Salesforce Mobile App is typically best fit.

**External users (customers, partners)**: Experience Cloud mobile or custom app may be better.

**Decision factor**: User type determines which options are available and appropriate.

### Use Case

**Question**: What do users need to do on mobile?

**Standard CRM tasks**: Salesforce Mobile App handles well.

**Custom workflows**: May need Experience Cloud mobile or custom app.

**Specialized features**: May require custom app.

**Decision factor**: Use case complexity and customization needs.

### Offline Requirements

**Question**: Do users need to work offline?

**Salesforce Mobile App**: Good offline support with data sync.

**Experience Cloud mobile**: Limited offline (web-based).

**Custom app**: Can implement custom offline strategies.

**Decision factor**: Offline requirements determine viable options.

### Branding Requirements

**Question**: How important is custom branding?

**Salesforce Mobile App**: Limited branding customization.

**Experience Cloud mobile**: Full branding control.

**Custom app**: Complete branding control.

**Decision factor**: Branding requirements may drive choice.

### Budget and Resources

**Question**: What budget and resources are available?

**Salesforce Mobile App**: No additional cost (included).

**Experience Cloud mobile**: Experience Cloud license costs.

**Custom app**: Development and maintenance costs.

**Decision factor**: Budget constraints may limit options.

## Mobile-Optimized LWC Patterns

**What it is**: Building Lightning Web Components that work well on mobile devices.

**Key considerations**:
- **Responsive design**: Components adapt to screen size
- **Touch-friendly**: Large touch targets, appropriate spacing
- **Performance**: Optimize for mobile performance
- **Offline considerations**: Handle offline scenarios gracefully
- **Mobile-specific features**: Use mobile APIs (location, camera, barcode scanner)

**Best practices**:
- Use responsive CSS and SLDS mobile utilities
- Design for touch (larger buttons, appropriate spacing)
- Optimize data loading (lazy load, pagination)
- Handle offline scenarios
- Test on actual mobile devices

# Implementation Guide

## Prerequisites

- Understanding of user needs and use cases
- Knowledge of mobile options and capabilities
- Understanding of offline requirements
- Budget and resource assessment

## High-Level Steps

1. **Identify mobile users**: Who needs mobile access?
2. **Understand use cases**: What do users need to do on mobile?
3. **Assess requirements**: Offline, branding, customization, device features
4. **Evaluate options**: Salesforce Mobile App, Experience Cloud mobile, custom app
5. **Make decision**: Choose strategy based on requirements and tradeoffs
6. **Plan implementation**: Design mobile experience, configure mobile app or build custom app
7. **Test on devices**: Test on actual mobile devices, not just simulators

## Key Configuration Decisions

**Mobile option**: Which mobile approach? Depends on user type, use case, and requirements.

**Offline strategy**: How to handle offline? Depends on mobile option and offline requirements.

**Branding approach**: How much branding customization? Depends on mobile option and branding requirements.

# Common Pitfalls & Anti-Patterns

## Bad Pattern: Choosing Custom App When Standard Mobile App Would Work

**Why it's bad**: Unnecessary development cost and maintenance when standard mobile app meets requirements.

**Better approach**: Start with Salesforce Mobile App. Only use custom app when there are specific requirements that standard app can't meet.

## Bad Pattern: Not Considering Offline Requirements

**Why it's bad**: Users may need to work offline, but chosen mobile option doesn't support it well, leading to poor user experience.

**Better approach**: Understand offline requirements early. Choose mobile option that supports offline needs. Design offline experience.

## Bad Pattern: Not Testing on Actual Mobile Devices

**Why it's bad**: Mobile experience may differ from desktop or simulator. Issues only appear on actual devices.

**Better approach**: Test on actual iOS and Android devices. Test different screen sizes and OS versions. Test offline scenarios.

## Bad Pattern: Ignoring Mobile Performance

**Why it's bad**: Mobile devices have limited resources. Poor performance leads to poor user experience.

**Better approach**: Optimize for mobile performance. Lazy load data, paginate results, minimize API calls, optimize images.

# Real-World Scenarios

## Scenario 1: Sales Team Needs Mobile Access

**Problem**: Sales team needs to access accounts, contacts, and opportunities while in field.

**Context**: Standard CRM use case, users are employees, need offline access for areas with poor connectivity.

**Solution**: Salesforce Mobile App. Configure mobile layouts, enable offline sync for key objects, train users on mobile features. Benefits: No development, good offline support, quick deployment.

## Scenario 2: Customers Need Mobile Portal Access

**Problem**: Customers need to access their account information, submit cases, and view knowledge articles on mobile.

**Context**: External users, need custom branding, web-based deployment preferred.

**Solution**: Experience Cloud mobile. Create mobile-responsive Experience Cloud site, customize branding, optimize for mobile. Benefits: Custom branding, web-based, no app store.

## Scenario 3: Field Service Team Needs Specialized Mobile App

**Problem**: Field service team needs custom mobile app with barcode scanning, GPS tracking, and custom workflows.

**Context**: Specialized use case, standard mobile app doesn't meet requirements, budget available for custom development.

**Solution**: Custom mobile app using Salesforce Mobile SDK. Build native app with custom UI, integrate device features, implement custom offline strategy. Benefits: Full customization, device features, custom workflows.

# Checklist / Mental Model

## Evaluating Mobile Strategy

- [ ] Identify mobile users (internal, external, both)
- [ ] Understand use cases (what do users need to do?)
- [ ] Assess offline requirements
- [ ] Evaluate branding needs
- [ ] Consider budget and resources
- [ ] Evaluate mobile options (Mobile App, Experience Cloud, custom)
- [ ] Make decision based on requirements and tradeoffs

## Implementing Mobile Strategy

- [ ] Configure mobile app or build custom app
- [ ] Design mobile-optimized user experience
- [ ] Implement offline capabilities if needed
- [ ] Test on actual mobile devices
- [ ] Train users on mobile features
- [ ] Monitor mobile usage and performance

## Mental Model: Start Standard, Go Custom Only When Needed

Think of mobile strategy as starting with standard options (Salesforce Mobile App) and going custom only when there are specific requirements that standard options can't meet. Most use cases can be handled by standard mobile app.

# Key Terms & Definitions

- **Salesforce Mobile App**: Native mobile app provided by Salesforce
- **Experience Cloud mobile**: Mobile-optimized Experience Cloud sites
- **Custom mobile app**: Custom-built native or hybrid mobile applications
- **Offline sync**: Synchronizing data for offline access
- **Mobile SDK**: Software development kit for building mobile apps with Salesforce
- **Responsive design**: Design that adapts to different screen sizes

# RAG-Friendly Q&A Seeds

**Q: When should I use Salesforce Mobile App vs. Experience Cloud mobile vs. custom mobile app?**

**A**: Use Salesforce Mobile App for internal users with standard CRM use cases. Use Experience Cloud mobile for external users needing custom branding and web-based deployment. Use custom mobile app only when there are specific requirements (custom workflows, specialized features) that standard options can't meet.

**Q: What offline capabilities does each mobile option provide?**

**A**: Salesforce Mobile App has good offline support with data sync. Experience Cloud mobile has limited offline (web-based). Custom mobile apps can implement custom offline strategies. Assess offline requirements and choose option that supports them.

**Q: How do I build mobile-optimized Lightning Web Components?**

**A**: Use responsive CSS and SLDS mobile utilities, design for touch (larger buttons, appropriate spacing), optimize data loading (lazy load, pagination), handle offline scenarios, and test on actual mobile devices. Follow mobile design best practices.

**Q: What's the cost difference between mobile options?**

**A**: Salesforce Mobile App is included with licenses (no additional cost). Experience Cloud mobile requires Experience Cloud licenses. Custom mobile apps require development and maintenance costs. Consider total cost of ownership, not just initial cost.

**Q: How do I test mobile experiences effectively?**

**A**: Test on actual iOS and Android devices, not just simulators. Test different screen sizes and OS versions. Test offline scenarios. Test performance on actual devices. Get user feedback on mobile experience.

**Q: Can I use multiple mobile strategies for different user types?**

**A**: Yes, hybrid approach is common. Use Salesforce Mobile App for internal users, Experience Cloud mobile for external users, and custom apps for specialized use cases. Use right tool for right job, but manage complexity of multiple approaches.

**Q: What mobile-specific Salesforce APIs are available?**

**A**: Salesforce provides mobile APIs for location services, barcode scanning, document scanning, NFC, biometrics, and other device features. These can be used in custom mobile apps or LWCs designed for mobile.

**Q: How do I handle mobile performance optimization?**

**A**: Optimize for mobile performance by lazy loading data, paginating results, minimizing API calls, optimizing images, and using efficient data access patterns. Test performance on actual devices, not just simulators.

**Q: What's the difference between native and hybrid mobile apps?**

**A**: Native apps are built specifically for iOS or Android using platform-specific languages. Hybrid apps use web technologies (HTML, CSS, JavaScript) wrapped in native container. Native apps typically perform better, hybrid apps are easier to maintain across platforms.

**Q: How do I decide between mobile app and mobile web experience?**

**A**: Mobile app provides better offline capabilities, native feel, and device feature access. Mobile web is easier to deploy and update (no app store), works across platforms, and may be sufficient for many use cases. Consider requirements, user preferences, and maintenance complexity.

## Related Patterns

**See Also**:
- [Portal Architecture](/rag/architecture/portal-architecture.html) - Experience Cloud mobile patterns
- [LWC Patterns](/rag/development/lwc-patterns.html) - Mobile-optimized LWC patterns

**Related Domains**:
- [LWC Accessibility](/rag/development/lwc-patterns.html) - Mobile accessibility patterns
- [Mobile LWC Patterns](/rag/mcp-knowledge/lwc-development-guide.html) - Official mobile LWC guidance

