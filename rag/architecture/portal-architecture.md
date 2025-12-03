---
layout: default
title: Portal Architecture Patterns
description: Experience Cloud portal architecture patterns for supporting multiple user types with different identity providers, security requirements, and access patterns
permalink: /rag/architecture/portal-architecture.html
level: Advanced
tags:
  - architecture
  - experience-cloud
  - portals
  - multi-tenant
  - identity
last_reviewed: 2025-12-03
---

# Portal Architecture Patterns

## Overview

Experience Cloud (formerly Community Cloud) portal architecture patterns support multiple user types (students/applicants, external partners/providers, citizens/clients) with different identity providers, security requirements, and access patterns. This document covers architectural patterns for designing and implementing multi-tenant portals.

**Core Principle**: Design portals to support multiple distinct user communities with different identity providers, security requirements, and access patterns. Use sharing sets, permission sets, and identity providers to isolate and secure each community.

## Prerequisites

**Required Knowledge**:
- Understanding of Experience Cloud (Community Cloud)
- Familiarity with sharing and security models
- Knowledge of identity providers (SAML, OAuth, etc.)
- Understanding of multi-tenant architecture
- Knowledge of portal user management

**Recommended Reading**:
- <a href="{{ '/rag/identity-sso/multi-tenant-identity-architecture.html' | relative_url }}">Multi-Tenant Identity Architecture</a> - Identity provider patterns for portals
- <a href="{{ '/rag/security/sharing-sets-and-portals.html' | relative_url }}">Sharing Sets and Portal Sharing</a> - Portal sharing patterns
- <a href="{{ '/rag/security/permission-set-architecture.html' | relative_url }}">Permission Set Architecture</a> - Permission set patterns for portals

## When to Use Portal Architecture

### Use Portal Architecture When

- **External user access**: Need to provide access to external users (customers, partners, citizens)
- **Multiple user communities**: Different user types with different access requirements
- **Self-service**: Users need self-service capabilities
- **Branded experience**: Need branded, customized user experience
- **Identity integration**: Need to integrate with external identity providers
- **Public access**: Need public-facing portals (with or without authentication)

### Avoid Portal Architecture When

- **Internal-only access**: All users are internal employees
- **Simple use case**: Standard Salesforce UI meets requirements
- **Limited resources**: Don't have resources to build and maintain portals
- **Complex requirements**: Requirements too complex for Experience Cloud

## Portal Architecture Patterns

### Pattern 1: Single Portal, Multiple User Types

**Architecture**: One Experience Cloud site with multiple user types managed via profiles and permission sets.

**Use Case**: Portal serves multiple user types (students, applicants, partners) with different access levels.

**Implementation**:
- **Single Experience Site**: One Experience Cloud site
- **Multiple Profiles**: Different profiles for each user type
- **Permission Sets**: Feature-based permission sets for different access levels
- **Sharing Sets**: Sharing sets to control record access
- **Page Variations**: Different page layouts for different user types

**Benefits**:
- Simpler architecture (one site to manage)
- Shared components and pages
- Easier maintenance

**Challenges**:
- Complex sharing rules
- Multiple user types in one site
- More complex permission management

### Pattern 2: Multiple Portals, Separate Communities

**Architecture**: Multiple Experience Cloud sites, one per user community.

**Use Case**: Distinct user communities (students, partners, citizens) with completely different access patterns.

**Implementation**:
- **Multiple Experience Sites**: One site per user community
- **Separate Profiles**: Different profiles per site
- **Isolated Sharing**: Separate sharing sets per site
- **Separate Identity Providers**: Different identity providers per site (if needed)
- **Branded Experiences**: Different branding per site

**Benefits**:
- Complete isolation between communities
- Simpler sharing rules per site
- Independent branding and customization
- Easier to scale individual communities

**Challenges**:
- More sites to manage
- Duplicate components (if needed)
- More complex overall architecture

### Pattern 3: Hub-and-Spoke Portal Architecture

**Architecture**: Central hub portal with spoke portals for specific functions.

**Use Case**: Central portal (main experience) with specialized portals for specific functions (support, partner portal, etc.).

**Implementation**:
- **Hub Portal**: Main Experience Cloud site (central access point)
- **Spoke Portals**: Specialized Experience Cloud sites (support, partners, etc.)
- **Cross-Portal Navigation**: Navigation between portals
- **Shared Identity**: Shared identity provider across portals
- **Centralized Management**: Centralized user management

**Benefits**:
- Specialized portals for specific functions
- Centralized access point
- Flexible architecture

**Challenges**:
- Cross-portal navigation complexity
- Multiple sites to manage
- Identity provider coordination

## Identity Provider Patterns

### Pattern 1: Salesforce Authentication

**Use Case**: Simple authentication using Salesforce user accounts.

**Implementation**:
- **Salesforce Authentication**: Standard Salesforce login
- **Portal User Licenses**: Experience Cloud user licenses
- **User Management**: Manage users in Salesforce

**Benefits**:
- Simple implementation
- No external dependencies
- Built-in user management

**Limitations**:
- Users must have Salesforce accounts
- Limited customization of login experience

### Pattern 2: External Identity Provider (SAML/OAuth)

**Use Case**: Integrate with external identity providers (Azure AD, Okta, etc.).

**Implementation**:
- **SAML/OAuth Integration**: Configure external identity provider
- **Just-In-Time (JIT) Provisioning**: Auto-create users on first login
- **Attribute Mapping**: Map identity provider attributes to Salesforce
- **Single Sign-On (SSO)**: SSO across portals and external systems

**Benefits**:
- Integration with existing identity systems
- SSO capabilities
- Centralized identity management

**Challenges**:
- More complex setup
- Identity provider dependencies
- Attribute mapping complexity

### Pattern 3: Multi-Identity Provider Architecture

**Use Case**: Different identity providers for different user communities.

**Implementation**:
- **Multiple Identity Providers**: Different providers per portal/user type
- **Login Handlers**: Custom login handlers to route users
- **Attribute Mapping**: Different attribute mapping per provider
- **User Matching**: Match users across identity providers

**Benefits**:
- Support different identity systems
- Flexible identity management
- Support legacy systems

**Challenges**:
- Complex identity management
- User matching complexity
- Multiple identity provider dependencies

## Sharing Patterns

### Sharing Set Pattern

**Purpose**: Control record access for portal users.

**Implementation**:
- **Sharing Sets**: Define sharing sets for portal users
- **Record Access**: Grant access to records based on criteria
- **Field-Level Sharing**: Control field-level access
- **Object-Level Sharing**: Control object-level access

**Best Practices**:
- Use sharing sets for portal-specific sharing
- Combine with org-wide defaults
- Test sharing with different user types
- Document sharing set purposes

### Manual Sharing Pattern

**Purpose**: Grant access to specific records for specific users.

**Implementation**:
- **Manual Sharing**: Share records manually with portal users
- **Apex Managed Sharing**: Programmatically share records
- **Sharing Reasons**: Document sharing reasons

**Use Cases**:
- Grant access to specific cases
- Share records with specific partners
- Temporary access grants

## Security Patterns

### Permission Set Pattern

**Purpose**: Grant feature-specific access to portal users.

**Implementation**:
- **Feature Permission Sets**: Permission sets for specific features
- **User Assignment**: Assign permission sets to portal users
- **Permission Set Groups**: Group related permission sets

**Best Practices**:
- Use permission sets for feature access
- Document permission set purposes
- Regular permission set reviews

### Field-Level Security Pattern

**Purpose**: Control field-level access for portal users.

**Implementation**:
- **Field-Level Security**: Set FLS on fields
- **Profile FLS**: Set FLS in profiles
- **Permission Set FLS**: Set FLS in permission sets

**Best Practices**:
- Restrict sensitive fields
- Use permission sets for field access
- Test field-level security

## Performance Patterns

### Caching Pattern

**Purpose**: Improve portal performance with caching.

**Implementation**:
- **Platform Cache**: Use Platform Cache for frequently accessed data
- **CDN**: Use CDN for static assets
- **Lazy Loading**: Lazy load components and data

**Best Practices**:
- Cache frequently accessed data
- Use CDN for static assets
- Implement lazy loading

### Data Volume Pattern

**Purpose**: Handle large data volumes in portals.

**Implementation**:
- **Pagination**: Implement pagination for large datasets
- **Filtering**: Provide filtering capabilities
- **Search**: Implement search functionality
- **Data Archiving**: Archive old data

**Best Practices**:
- Paginate large datasets
- Provide filtering and search
- Archive old data

## Related Patterns

- <a href="{{ '/rag/identity-sso/multi-tenant-identity-architecture.html' | relative_url }}">Multi-Tenant Identity Architecture</a> - Identity provider patterns for portals
- <a href="{{ '/rag/security/sharing-sets-and-portals.html' | relative_url }}">Sharing Sets and Portal Sharing</a> - Portal sharing patterns and best practices
- <a href="{{ '/rag/security/permission-set-architecture.html' | relative_url }}">Permission Set Architecture</a> - Permission set patterns for portals
- <a href="{{ '/rag/development/lwc-patterns.html' | relative_url }}">LWC Patterns</a> - LWC patterns for portal components

## Q&A

### Q: What is portal architecture in Salesforce?

**A**: **Portal architecture** refers to Experience Cloud (Community Cloud) architecture patterns for: (1) **Multiple user communities** (students, partners, citizens), (2) **Different identity providers** (Salesforce, SAML, OAuth), (3) **Different security requirements** (sharing sets, permission sets), (4) **Different access patterns** (self-service, partner access, public access). Portal architecture enables multi-tenant portal implementations.

### Q: When should I use a single portal vs multiple portals?

**A**: Use **single portal** when: (1) **Similar user types** (similar access requirements), (2) **Shared components** (can share pages and components), (3) **Simpler management** (one site to manage). Use **multiple portals** when: (1) **Distinct communities** (completely different access patterns), (2) **Complete isolation** (need complete separation), (3) **Different branding** (different branding per community), (4) **Independent scaling** (need to scale communities independently).

### Q: How do I implement multi-identity provider architecture?

**A**: Implement by: (1) **Configure identity providers** (SAML, OAuth for each provider), (2) **Login handlers** (custom login handlers to route users), (3) **Attribute mapping** (map attributes per provider), (4) **User matching** (match users across providers), (5) **JIT provisioning** (auto-create users on first login). Multi-identity provider architecture supports different identity systems for different user communities.

### Q: How do sharing sets work in portals?

**A**: **Sharing sets** control record access for portal users: (1) **Define sharing sets** (specify which records portal users can access), (2) **Record criteria** (criteria for record access), (3) **Field-level sharing** (control field-level access), (4) **Object-level sharing** (control object-level access). Sharing sets provide portal-specific sharing control beyond org-wide defaults.

### Q: What are best practices for portal security?

**A**: Best practices: (1) **Use sharing sets** (portal-specific sharing), (2) **Permission sets** (feature-based access), (3) **Field-level security** (restrict sensitive fields), (4) **Regular audits** (review access regularly), (5) **Test with different user types** (test security with different users), (6) **Document security model** (clear documentation). Portal security requires careful design and regular review.

### Q: How do I handle performance in portals?

**A**: Handle performance by: (1) **Platform Cache** (cache frequently accessed data), (2) **CDN** (use CDN for static assets), (3) **Pagination** (paginate large datasets), (4) **Filtering and search** (provide filtering capabilities), (5) **Lazy loading** (lazy load components), (6) **Data archiving** (archive old data). Portal performance requires optimization at multiple levels.

### Q: What are common portal architecture challenges?

**A**: Common challenges: (1) **Complex sharing rules** (multiple user types, complex sharing), (2) **Identity provider integration** (multiple identity providers), (3) **Performance** (large data volumes, many users), (4) **User management** (managing many portal users), (5) **Customization** (balancing customization with maintainability), (6) **Testing** (testing with different user types). Address challenges through careful architecture design and regular review.
