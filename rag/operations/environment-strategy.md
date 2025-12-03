---
title: "Environment Strategy for Salesforce"
level: "Intermediate"
tags:
  - operations
  - environment-strategy
  - sandboxes
  - data-masking
last_reviewed: "2025-01-XX"
---

# Environment Strategy for Salesforce

## Overview

This guide covers environment strategy patterns for Salesforce, including org topologies for multi-team programs, data masking strategies, and sandbox refresh cadences. These patterns are essential for managing complex Salesforce implementations with multiple teams, compliance requirements, and efficient development workflows.

**Related Patterns**:
- [CI/CD Patterns](cicd-patterns.md) - CI/CD and deployment automation
- [Release Governance](release-governance.md) - Release approval and risk management
- [Data Residency & Compliance](../data-governance/data-residency-compliance.md) - Data protection and compliance patterns

## Consensus Best Practices

- **Design org topology early**: Plan org structure before development begins to avoid costly restructuring
- **Isolate teams when possible**: Use separate orgs or clear boundaries for independent team work
- **Mask sensitive data in non-production**: Always mask PII/PHI in sandbox environments
- **Establish refresh cadences**: Define clear refresh schedules based on team needs and data requirements
- **Automate data masking**: Use automated tools and scripts for consistent data masking
- **Document environment purposes**: Clearly document the purpose and usage of each environment
- **Maintain environment parity**: Keep environments as similar as possible to production
- **Plan for environment scaling**: Design topology to support growth and additional teams

## Org Topologies

### Single Org Strategy

**When to Use**:
- Small teams (1-2 development teams)
- Tightly coupled features requiring frequent integration
- Limited budget for multiple orgs
- Simple deployment requirements

**Benefits**:
- Single source of truth
- No cross-org deployment complexity
- Lower cost
- Easier data sharing

**Challenges**:
- Team coordination required
- Potential for conflicts
- Limited isolation
- Shared governor limits

### Multi-Org Strategy

**When to Use**:
- Large programs with multiple independent teams
- Need for complete team isolation
- Different release cadences per team
- Compliance requirements for data isolation

**Benefits**:
- Complete team isolation
- Independent release cycles
- Separate governor limit contexts
- Reduced coordination overhead

**Challenges**:
- Cross-org deployment complexity
- Data synchronization needs
- Higher cost
- Integration complexity

### Hybrid Strategy

**When to Use**:
- Medium to large programs
- Some teams need isolation, others can share
- Phased rollout approach
- Mix of independent and integrated features

**Patterns**:
- Core org for shared functionality
- Feature orgs for independent development
- Integration org for testing cross-org scenarios
- Production org consolidation strategy

### Branching Strategies

**Git Branching for Multi-Team**:
- **Main branch**: Production-ready code
- **Develop branch**: Integration branch for all teams
- **Feature branches**: Team-specific feature branches
- **Release branches**: Coordinated release branches

**Org Branching Patterns**:
- **Dev orgs per team**: Each team has dedicated dev org
- **Shared integration org**: Common org for integration testing
- **Staging org**: Pre-production validation
- **Production org**: Live system

**Coordination Patterns**:
- Regular integration points
- Clear merge procedures
- Conflict resolution processes
- Release coordination

### Org Isolation Patterns

**Metadata Isolation**:
- Use namespaces for package isolation
- Organize metadata by team/feature
- Use unlocked packages for boundaries
- Document metadata ownership

**Data Isolation**:
- Use Record Types for data separation
- Implement sharing rules for data access
- Use custom objects for team-specific data
- Document data ownership and access

**Process Isolation**:
- Separate automation per team/feature
- Independent Flow and Process Builder processes
- Team-specific validation rules
- Document process ownership

## Data Masking

### PII/PHI Masking Strategies

**Data Classification**:
- Identify all PII/PHI fields in org
- Classify data sensitivity levels
- Document masking requirements per field
- Maintain data classification inventory

**Masking Approaches**:
- **Full masking**: Replace with generic values (e.g., "Test User")
- **Partial masking**: Mask portions (e.g., "***-***-1234" for SSN)
- **Scrambling**: Randomize values while maintaining format
- **Hashing**: Use hash functions for consistent masking

**Field-Level Masking**:
- Email: Replace with test email patterns
- Phone: Use test phone number patterns
- SSN: Mask with test SSN patterns
- Address: Use test address data
- Names: Use test name generators

### Test Data Anonymization

**Anonymization Patterns**:
- Generate realistic but fake data
- Maintain data relationships
- Preserve data formats and constraints
- Ensure referential integrity

**Data Generation Tools**:
- Apex data generation scripts
- External data generation tools
- Custom anonymization utilities
- Third-party masking solutions

**Anonymization Best Practices**:
- Maintain data volume and distribution
- Preserve data relationships
- Keep data formats consistent
- Document anonymization rules

### Masking Tools and Patterns

**Apex Masking Scripts**:
- Create utility classes for masking logic
- Support configurable masking rules
- Process data in batches
- Log masking operations

**Data Loader Masking**:
- Export data from production
- Apply masking transformations
- Import masked data to sandbox
- Validate masking results

**Automated Masking Pipelines**:
- Integrate masking into refresh process
- Automate masking after sandbox refresh
- Validate masking completeness
- Document masking procedures

## Refresh Cadences

### Sandbox Refresh Strategies

**Refresh Frequency**:
- **Daily**: For active development orgs
- **Weekly**: For integration testing orgs
- **Monthly**: For UAT and training orgs
- **On-demand**: For special testing scenarios

**Refresh Considerations**:
- Team development needs
- Data freshness requirements
- Refresh time and impact
- Cost of refresh operations

**Refresh Planning**:
- Schedule refreshes during low-usage periods
- Communicate refresh schedules to teams
- Plan for post-refresh activities
- Document refresh procedures

### Data Refresh Patterns

**Full Data Refresh**:
- Complete sandbox refresh from production
- Includes all data and metadata
- Resets sandbox to production state
- Requires post-refresh configuration

**Partial Data Refresh**:
- Refresh specific objects or data sets
- Use data export/import for selective refresh
- Maintain test data while refreshing production data
- More complex but flexible

**Incremental Data Refresh**:
- Refresh only changed data
- Use change tracking for incremental updates
- Maintain existing test data
- Most complex but least disruptive

### Refresh Automation

**Automated Refresh Workflows**:
- Schedule regular refreshes
- Automate post-refresh configuration
- Automate data seeding after refresh
- Automate data masking after refresh

**Post-Refresh Activities**:
- Configure org settings
- Seed test data
- Apply data masking
- Validate org configuration
- Notify teams of refresh completion

**Refresh Monitoring**:
- Track refresh completion
- Monitor refresh duration
- Log refresh activities
- Alert on refresh failures

## Q&A

### Q: What is environment strategy in Salesforce?

**A**: **Environment strategy** defines how Salesforce orgs are organized and managed across development, testing, and production. It includes: (1) **Org topology** (single org vs. multiple orgs), (2) **Sandbox strategy** (types, refresh cadences), (3) **Data masking** (protecting sensitive data), (4) **Team isolation** (separating team work), (5) **Environment parity** (keeping environments similar).

### Q: When should I use a single org vs. multiple orgs for development?

**A**: Use **single org** for small teams (1-2 teams), tightly coupled features, limited budget, and simple deployments. Use **multiple orgs** for large teams (3+ teams), independent features, complex deployments, and need for team isolation. Design org topology early to avoid costly restructuring later.

### Q: How do I mask sensitive data in sandbox environments?

**A**: Mask sensitive data by: (1) **Identifying sensitive fields** (PII, PHI, financial data), (2) **Using data masking tools** (automated scripts, ETL tools), (3) **Replacing real data** with anonymized data, (4) **Automating masking** in refresh processes, (5) **Validating masking** (ensure no real data remains), (6) **Documenting masking rules**. Always mask PII/PHI in non-production environments.

### Q: What is the recommended sandbox refresh cadence?

**A**: Refresh cadence depends on: (1) **Team needs** (how often fresh data is needed), (2) **Data requirements** (test data freshness), (3) **Refresh costs** (time, resources), (4) **Compliance requirements** (data retention policies). Common cadences: **Weekly** for development sandboxes, **Monthly** for testing sandboxes, **Quarterly** for staging sandboxes. Document refresh schedules clearly.

### Q: How do I maintain environment parity across sandboxes?

**A**: Maintain parity by: (1) **Deploying same metadata** to all environments, (2) **Using same configuration** (profiles, permission sets), (3) **Seeding consistent test data**, (4) **Automating deployments** to ensure consistency, (5) **Documenting differences** when parity isn't possible, (6) **Regular audits** to verify parity. Keep environments as similar as possible to production.

### Q: What sandbox types should I use for different purposes?

**A**: Use sandbox types based on purpose: (1) **Developer** - individual development, (2) **Developer Pro** - individual development with more storage, (3) **Partial Copy** - integration testing with subset of production data, (4) **Full Copy** - full production copy for UAT, (5) **Metadata Only** - configuration testing without data. Choose based on data needs and testing requirements.

### Q: How do I isolate teams in a multi-team environment?

**A**: Isolate teams by: (1) **Using separate orgs** for independent teams, (2) **Using separate sandboxes** per team, (3) **Defining clear boundaries** (objects, features per team), (4) **Using unlocked packages** for modular development, (5) **Coordinating deployments** to avoid conflicts, (6) **Documenting team responsibilities**. Isolate when possible to enable independent work.

### Q: What should I consider when planning org topology?

**A**: Consider: (1) **Team size and structure** (how many teams, how independent), (2) **Feature coupling** (how tightly coupled features are), (3) **Budget constraints** (cost of multiple orgs), (4) **Deployment complexity** (cross-org deployments), (5) **Data sharing needs** (need for unified reporting), (6) **Future growth** (scalability requirements). Design topology early to avoid restructuring.

### Q: How do I handle data requirements across environments?

**A**: Handle data requirements by: (1) **Defining data needs** per environment (what data is needed), (2) **Automating data seeding** (consistent test data), (3) **Masking sensitive data** (PII, PHI), (4) **Refreshing data regularly** (based on cadence), (5) **Documenting data requirements**, (6) **Validating data quality** (ensure data is usable). Balance data freshness with refresh costs.

### Q: What are best practices for environment strategy?

**A**: Best practices include: (1) **Design org topology early** (before development), (2) **Isolate teams when possible** (separate orgs or clear boundaries), (3) **Mask sensitive data** in non-production, (4) **Establish refresh cadences** (documented schedules), (5) **Automate data masking** (consistent processes), (6) **Document environment purposes** (clear usage guidelines), (7) **Maintain environment parity** (keep environments similar), (8) **Plan for scaling** (support future growth).

## Related Patterns

- [CI/CD Patterns](cicd-patterns.md) - CI/CD and deployment automation
- [Release Governance](release-governance.md) - Release approval and risk management
- [Data Residency & Compliance](../data-governance/data-residency-compliance.md) - Data protection and compliance
- [Sandbox Seeding](rag/operations/cicd-patterns.md#sandbox-seeding) - Test data management patterns

