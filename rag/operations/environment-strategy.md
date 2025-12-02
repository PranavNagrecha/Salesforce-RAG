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

## Related Patterns

- [CI/CD Patterns](cicd-patterns.md) - CI/CD and deployment automation
- [Release Governance](release-governance.md) - Release approval and risk management
- [Data Residency & Compliance](../data-governance/data-residency-compliance.md) - Data protection and compliance
- [Sandbox Seeding](rag/operations/cicd-patterns.md#sandbox-seeding) - Test data management patterns

