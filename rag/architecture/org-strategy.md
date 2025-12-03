---
layout: default
title: Overview
description: Documentation for Overview
permalink: /rag/architecture/org-strategy.html
---

# Overview

Org strategy is one of the most critical architectural decisions in Salesforce implementations. The choice between a single org and multiple orgs impacts data isolation, security, customization, integration complexity, cost, and long-term maintainability. This decision has far-reaching implications and is difficult to reverse.

Org strategy encompasses understanding when to use a single org versus multiple orgs, evaluating factors like data isolation, security requirements, business unit independence, integration needs, and cost. The decision requires balancing competing concerns: simplicity vs. isolation, cost vs. complexity, flexibility vs. standardization.

Most organizations start with a single org, which is appropriate for most scenarios. Multiple orgs are justified when there are strong requirements for data isolation, independent business units, or regulatory separation. Understanding the tradeoffs enables informed decision-making.

# Core Concepts

## Single Org Strategy

**What it is**: All business units, departments, or entities operate within one Salesforce org.

**Key characteristics**:
- Shared data model and configuration
- Centralized administration and governance
- Single integration point
- Shared security model
- Unified reporting and analytics

**Advantages**:
- **Simplicity**: One org to manage, one set of configurations
- **Cost efficiency**: Lower licensing and administration costs
- **Data visibility**: Cross-business unit reporting and analytics
- **Integration simplicity**: Single integration point
- **Shared resources**: Reuse of components, patterns, and expertise

**Disadvantages**:
- **Data isolation challenges**: Harder to isolate data between business units
- **Security complexity**: More complex sharing rules and security model
- **Customization conflicts**: Different business units may need conflicting customizations
- **Governance complexity**: More stakeholders, more coordination needed
- **Risk concentration**: Issues affect entire organization

**When to use**:
- Single business entity or closely related business units
- Need for cross-business unit reporting and data sharing
- Limited data isolation requirements
- Cost-sensitive implementations
- Standardized processes across business units

## Multiple Org Strategy

**What it is**: Separate Salesforce orgs for different business units, departments, or entities.

**Key characteristics**:
- Independent data models and configurations
- Separate administration and governance
- Multiple integration points
- Independent security models
- Separate reporting and analytics

**Advantages**:
- **Data isolation**: Complete separation between business units
- **Security simplicity**: Simpler security model per org
- **Customization freedom**: Each org can customize independently
- **Governance independence**: Independent change management
- **Risk isolation**: Issues in one org don't affect others

**Disadvantages**:
- **Complexity**: Multiple orgs to manage and coordinate
- **Cost**: Higher licensing and administration costs
- **Data silos**: Harder to share data and report across orgs
- **Integration complexity**: Multiple integration points to manage
- **Resource duplication**: Duplicate components and expertise

**When to use**:
- Strong data isolation requirements (regulatory, competitive, security)
- Independent business units with different processes
- Mergers and acquisitions with existing orgs
- Regulatory requirements for data separation
- Different business models requiring different configurations

## Hybrid Strategy

**What it is**: Combination of single org and multiple orgs, typically with a central org and satellite orgs.

**Key characteristics**:
- Central org for shared functions
- Satellite orgs for specific business units or functions
- Integration between orgs for data sharing
- Centralized governance for some functions, decentralized for others

**Advantages**:
- **Balanced approach**: Isolation where needed, sharing where beneficial
- **Flexibility**: Can adapt to different business unit needs
- **Selective integration**: Share data where it makes sense

**Disadvantages**:
- **Complexity**: Most complex to manage and coordinate
- **Cost**: Higher than single org, may be lower than full multi-org
- **Integration overhead**: Requires integration between orgs

**When to use**:
- Some business units need isolation, others can share
- Central functions (HR, Finance) with separate business units
- Gradual migration from multiple orgs to single org (or vice versa)

# Deep-Dive Patterns & Best Practices

## Decision Framework

### Data Isolation Requirements

**Question**: Do business units need complete data isolation?

**Single org**: Data isolation through sharing rules, record types, and profiles. Not complete isolation.

**Multiple orgs**: Complete data isolation. No way for one business unit to access another's data.

**Decision factor**: Regulatory requirements, competitive separation, security requirements.

### Business Unit Independence

**Question**: Do business units operate independently with different processes?

**Single org**: Can support different processes through record types, profiles, and automation, but within shared data model.

**Multiple orgs**: Complete independence. Each org can have different data models, processes, and configurations.

**Decision factor**: How different are business unit processes? Can they be accommodated in shared model?

### Integration Requirements

**Question**: Do business units need to share data or integrate with each other?

**Single org**: Native data sharing. No integration needed.

**Multiple orgs**: Requires integration (APIs, ETL) to share data. More complex.

**Decision factor**: How much data sharing is needed? Is integration complexity acceptable?

### Cost Considerations

**Question**: What are the cost implications of each strategy?

**Single org**: Lower licensing costs (shared platform features), lower administration costs.

**Multiple orgs**: Higher licensing costs (duplicate platform features), higher administration costs.

**Decision factor**: Budget constraints, cost-benefit analysis.

### Governance and Change Management

**Question**: How do business units want to manage changes and governance?

**Single org**: Centralized governance, coordinated change management.

**Multiple orgs**: Independent governance, independent change management.

**Decision factor**: Governance preferences, change management maturity, coordination capabilities.

## Common Patterns

### Single Org with Record Type Separation

**Pattern**: Use record types to separate different business processes within single org.

**When to use**: Different processes for same object, but can share data model.

**Example**: Different case types (Support, Sales, Partner) using record types on Case object.

### Single Org with Sharing Rule Isolation

**Pattern**: Use sharing rules to isolate data between business units.

**When to use**: Need data isolation but can share org and data model.

**Example**: Different divisions that shouldn't see each other's accounts, but use same Account object.

### Multiple Orgs with Integration

**Pattern**: Separate orgs with integration for data sharing where needed.

**When to use**: Need complete isolation but some data sharing required.

**Example**: Separate orgs for different subsidiaries with integration for consolidated reporting.

### Hub and Spoke

**Pattern**: Central org (hub) with satellite orgs (spokes) for specific functions.

**When to use**: Central functions shared, specific functions isolated.

**Example**: Central org for CRM, separate orgs for field service and partner management.

# Implementation Guide

## Prerequisites

- Understanding of business structure and requirements
- Knowledge of data isolation and security requirements
- Understanding of integration capabilities and complexity
- Cost analysis capabilities

## High-Level Steps

1. **Understand business structure**: Map business units, departments, and entities
2. **Identify requirements**: Data isolation, security, integration, governance
3. **Evaluate options**: Single org, multiple orgs, hybrid
4. **Assess tradeoffs**: Complexity, cost, flexibility, isolation
5. **Make decision**: Choose strategy based on requirements and tradeoffs
6. **Document rationale**: Capture decision and reasoning for future reference
7. **Plan implementation**: Design org structure, data model, security, integration

## Key Configuration Decisions

**Org count**: How many orgs? Depends on business structure and isolation requirements.

**Org purpose**: What does each org do? Define scope and boundaries for each org.

**Integration approach**: How do orgs share data? APIs, ETL, or no sharing.

**Governance model**: How is each org governed? Centralized, decentralized, or hybrid.

# Common Pitfalls & Anti-Patterns

## Bad Pattern: Multiple Orgs for Wrong Reasons

**Why it's bad**: Creating multiple orgs for reasons that don't justify the complexity and cost (e.g., "different departments want different things").

**Better approach**: Evaluate if requirements can be met in single org through configuration (record types, profiles, sharing rules). Only use multiple orgs when there are strong isolation or independence requirements.

## Bad Pattern: Single Org When Isolation Is Required

**Why it's bad**: Using single org when regulatory or security requirements mandate data isolation leads to compliance issues.

**Better approach**: Use multiple orgs when there are strong data isolation requirements that can't be met through sharing rules and security model.

## Bad Pattern: Not Planning for Future Growth

**Why it's bad**: Choosing single org without considering future business unit additions or acquisitions leads to difficult migrations later.

**Better approach**: Consider future growth and business structure changes. Design org strategy with scalability in mind.

## Bad Pattern: Ignoring Integration Complexity

**Why it's bad**: Choosing multiple orgs without understanding integration complexity leads to data silos and reporting challenges.

**Better approach**: Understand integration requirements and complexity. Plan for data sharing and reporting across orgs if needed.

# Real-World Scenarios

## Scenario 1: Multi-Division Company with Shared Customers

**Problem**: Company has multiple divisions (Sales, Service, Marketing) that need to share customer data but have different processes.

**Context**: Divisions are part of same company, share customers, but have different workflows and requirements.

**Solution**: Single org with record types and profiles to support different processes. Sharing rules ensure all divisions can access shared customer data. Benefits: Shared customer view, unified reporting, lower cost.

## Scenario 2: Merged Companies with Existing Orgs

**Problem**: Two companies merge, each has existing Salesforce org with different configurations and data models.

**Context**: Companies operate independently, have different processes, regulatory requirements may differ.

**Solution**: Keep separate orgs initially (multiple org strategy). Integrate for shared reporting. Gradually migrate to single org if business units align. Benefits: Maintains existing operations, allows gradual alignment.

## Scenario 3: Healthcare Organization with PHI Requirements

**Problem**: Healthcare organization needs to isolate patient data between different departments due to HIPAA requirements.

**Context**: Different departments (Clinical, Billing, Research) have different data access requirements and regulatory constraints.

**Solution**: Multiple orgs with strict data isolation. Integration only for aggregated, de-identified reporting. Benefits: Complete data isolation, regulatory compliance, independent governance.

# Checklist / Mental Model

## Evaluating Org Strategy

- [ ] Understand business structure (business units, departments, entities)
- [ ] Identify data isolation requirements
- [ ] Assess business unit independence needs
- [ ] Evaluate integration requirements
- [ ] Consider cost implications
- [ ] Assess governance preferences
- [ ] Evaluate tradeoffs (complexity vs. isolation, cost vs. flexibility)

## Making Decision

- [ ] Start with single org assumption (simplest, lowest cost)
- [ ] Evaluate if single org meets requirements
- [ ] Consider multiple orgs only if strong isolation or independence requirements
- [ ] Document decision and rationale
- [ ] Plan for future growth and changes

## Mental Model: Start Simple, Add Complexity Only When Needed

Think of org strategy as starting with simplest approach (single org) and adding complexity (multiple orgs) only when there are strong requirements that justify it. Most organizations can operate effectively in single org. Multiple orgs should be exception, not default.

# Key Terms & Definitions

- **Single org strategy**: All business units operate in one Salesforce org
- **Multiple org strategy**: Separate orgs for different business units
- **Hybrid strategy**: Combination of single and multiple orgs
- **Data isolation**: Separation of data between business units
- **Org governance**: How changes and configurations are managed in org
- **Hub and spoke**: Central org with satellite orgs for specific functions

# RAG-Friendly Q&A Seeds

**Q: When should I use a single org vs. multiple orgs?**

**A**: Start with single org assumption (simplest, lowest cost). Use multiple orgs only when there are strong requirements: complete data isolation (regulatory, security), independent business units with different processes, or regulatory requirements for separation. Most organizations can operate effectively in single org.

**Q: How do I isolate data between business units in a single org?**

**A**: Use sharing rules, record types, and profiles to isolate data. Create separate record types for different business units, use sharing rules to restrict access, and use profiles to control object and field access. Note: This provides isolation but not complete separation like multiple orgs.

**Q: What are the cost implications of single org vs. multiple orgs?**

**A**: Single org has lower licensing costs (shared platform features) and lower administration costs. Multiple orgs have higher licensing costs (duplicate platform features) and higher administration costs. Consider total cost of ownership, not just initial licensing.

**Q: How do I share data between multiple orgs?**

**A**: Use integration (APIs, ETL tools) to share data between orgs. REST/SOAP APIs for real-time sharing, Bulk API for batch sharing, or ETL tools for scheduled synchronization. More complex than native data sharing in single org.

**Q: Can I migrate from multiple orgs to single org (or vice versa)?**

**A**: Yes, but it's complex and time-consuming. Migration requires data migration, configuration consolidation, integration changes, and user training. Plan carefully and consider phased approach. Often better to make right decision initially than migrate later.

**Q: What's a hybrid org strategy?**

**A**: Combination of single and multiple orgs, typically with central org for shared functions and satellite orgs for specific business units or functions. Provides balance between isolation and sharing, but most complex to manage.

**Q: How do I decide org strategy for a merger or acquisition?**

**A**: Evaluate existing orgs, business unit alignment, data isolation requirements, and integration needs. Often start with separate orgs (maintain existing operations), then gradually migrate to single org if business units align. Consider regulatory and compliance requirements.

**Q: What governance considerations affect org strategy?**

**A**: Centralized governance favors single org (easier coordination). Decentralized governance may favor multiple orgs (independent change management). Consider governance preferences, change management maturity, and coordination capabilities when deciding.

**Q: How do I plan org strategy for future growth?**

**A**: Consider future business unit additions, acquisitions, and structural changes. Design org strategy with scalability in mind. Single org is more flexible for growth (easier to add business units). Multiple orgs may require new orgs for new business units.

**Q: What's the hub and spoke org pattern?**

**A**: Central org (hub) for shared functions (CRM, core processes) with satellite orgs (spokes) for specific functions (field service, partner management). Provides isolation for specific functions while sharing core capabilities. More complex than single org but less than full multi-org.

## Related Patterns

**See Also**:
- <a href="{{ '/rag/architecture/org-edition-selection.html' | relative_url }}">Org Edition Selection</a> - Edition selection for org strategy
- <a href="{{ '/rag/architecture/governance-patterns.html' | relative_url }}">Governance Patterns</a> - Governance implications of org strategy

**Related Domains**:
- <a href="{{ '/rag/architecture/integrations/integration-platform-patterns.html' | relative_url }}">Integration Platform Patterns</a> - Multi-org integration patterns
- <a href="{{ '/rag/architecture/operations/environment-strategy.html' | relative_url }}">Environment Strategy</a> - Environment management for multi-org
- <a href="{{ '/rag/architecture/data-modeling/data-migration-patterns.html' | relative_url }}">Data Migration Patterns</a> - Data migration for org strategy

