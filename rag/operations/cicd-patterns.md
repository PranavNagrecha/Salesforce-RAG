# CI/CD Patterns for Salesforce

## Overview

This guide covers comprehensive CI/CD patterns for Salesforce, including metadata vs. source-tracked orgs, unlocked packages, sandbox seeding, deployment validation strategies, and rollback patterns. These patterns are essential for managing complex Salesforce development lifecycles with multiple teams and environments.

**Related Patterns**:
- [Deployment Patterns](rag/project-methods/deployment-patterns.md) - Deployment methods and best practices
- [Salesforce DX Patterns](rag/project-methods/sfdx-patterns.md) - SFDX-specific patterns
- [Environment Strategy](rag/operations/environment-strategy.md) - Org topology and environment management
- [Release Governance](rag/operations/release-governance.md) - Release approval and risk management

## Consensus Best Practices

- **Use source-tracked orgs for new projects**: Source-tracked orgs provide better integration with modern CI/CD tooling and source control
- **Migrate metadata orgs to source-tracked when possible**: Modernize existing projects to leverage source-tracked capabilities
- **Use unlocked packages for modular development**: Break down large codebases into manageable, versioned packages
- **Automate sandbox seeding**: Ensure consistent test data across environments through automated seeding pipelines
- **Validate before every deployment**: Run comprehensive validation checks before production deployments
- **Plan rollback strategies**: Always have a rollback plan before deploying to production
- **Use feature flags for gradual rollouts**: Enable gradual feature releases and quick rollbacks without code changes
- **Automate CI/CD pipelines**: Reduce manual errors and ensure consistent deployment processes

## Metadata vs. Source-Tracked Orgs

### Decision Framework

**Use Source-Tracked Orgs When**:
- Starting new projects or greenfield implementations
- Need tight integration with Git and CI/CD pipelines
- Want automatic source tracking of changes
- Require modern development workflow with scratch orgs
- Need better support for package development

**Use Metadata Orgs When**:
- Working with existing legacy projects
- Team is not ready to adopt SFDX workflow
- Need to work with orgs that cannot be converted to source-tracked
- Using Change Sets for simple deployments

### Source-Tracked Org Patterns

**Source Tracking**:
- Salesforce automatically tracks changes made directly in the org
- Changes can be pulled into local source control
- Supports both org-to-source and source-to-org workflows
- Enables conflict resolution between org and source changes

**Benefits**:
- Better integration with Git workflows
- Automatic change detection
- Support for modern CI/CD tooling
- Scratch org support for isolated development

**Migration Strategy**:
1. Initialize SFDX project structure
2. Retrieve all metadata from org
3. Convert to source-tracked org
4. Set up source control and CI/CD pipelines
5. Train team on new workflow

### Metadata Org Patterns

**Traditional Metadata API**:
- Manual retrieval and deployment of metadata
- Change Sets for connected org deployments
- Metadata API for automated deployments
- Requires explicit metadata management

**When to Maintain Metadata Orgs**:
- Legacy systems with complex dependencies
- Teams not ready for SFDX adoption
- Org limitations preventing source-tracked conversion
- Simple deployment requirements

## Unlocked Packages

### Package Development Patterns

**Package Structure**:
- Organize related metadata into logical packages
- Define clear package boundaries and dependencies
- Version packages using semantic versioning (major.minor.patch)
- Document package contents and dependencies

**Dependency Management**:
- Define package dependencies explicitly
- Use dependency version ranges carefully
- Avoid circular dependencies between packages
- Document dependency upgrade paths

**Versioning Strategy**:
- **Major version**: Breaking changes requiring manual intervention
- **Minor version**: New features, backward compatible
- **Patch version**: Bug fixes, backward compatible
- Tag versions in source control
- Maintain changelog for each package

### Package Promotion Patterns

**Promotion Workflow**:
1. Develop in dev org or scratch org
2. Create package version in dev environment
3. Install in integration/testing environment
4. Validate package in staging environment
5. Promote to production after approval

**Package Installation**:
- Use `sf project deploy start --source-dir` for package installation
- Validate package dependencies before installation
- Test package installation in non-production first
- Monitor installation logs for errors

**Package Upgrade Patterns**:
- Test upgrades in sandbox environments
- Document breaking changes in upgrade notes
- Provide migration scripts for data transformations
- Support rollback to previous package version

## Sandbox Seeding

### Data Seeding Strategies

**Test Data Management**:
- Create reusable test data sets for common scenarios
- Use data seeding scripts for consistent test data
- Maintain seed data in version control
- Document seed data structure and relationships

**Automated Seeding Pipelines**:
- Use Apex scripts for programmatic data creation
- Leverage Bulk API for large data volumes
- Use Data Loader for complex data relationships
- Automate seeding as part of CI/CD pipeline

**Seed Data Patterns**:
- **Minimal seed data**: Essential records for basic functionality
- **Comprehensive seed data**: Full test data sets for integration testing
- **Role-based seed data**: Data specific to user roles and permissions
- **Scenario-based seed data**: Data for specific test scenarios

### Seeding Implementation

**Apex Seeding Scripts**:
- Create utility classes for common seed data
- Use test data factories for consistent data creation
- Support idempotent seeding (safe to run multiple times)
- Log seeding progress and errors

**Bulk Data Seeding**:
- Use Bulk API 2.0 for large data volumes
- Process data in batches to avoid governor limits
- Validate data before seeding
- Track seeding progress and completion

**Data Refresh Strategies**:
- Seed data after sandbox refresh
- Maintain seed data scripts in source control
- Automate seeding in post-refresh scripts
- Document seed data dependencies

## Deployment Validation

### Pre-Deployment Checklists

**Code Quality Checks**:
- Run all unit tests with minimum coverage thresholds
- Execute static code analysis (PMD, ESLint)
- Review code for security vulnerabilities
- Validate code follows team standards

**Metadata Validation**:
- Validate metadata dependencies
- Check for breaking changes
- Verify configuration consistency
- Validate custom settings and metadata

**Integration Validation**:
- Test integration connectivity
- Validate API credentials and endpoints
- Test integration error handling
- Verify integration data flow

### Automated Validation Pipelines

**CI Pipeline Validation**:
- Run tests on every commit
- Validate metadata on pull requests
- Check code coverage thresholds
- Execute security scans

**Pre-Production Validation**:
- Full test suite execution
- Integration test validation
- Performance testing
- Security validation

**Validation Tools**:
- Salesforce CLI for metadata validation
- Static code analysis tools
- Test automation frameworks
- Security scanning tools

## Rollback Patterns

### Metadata Rollback

**Version Control Rollback**:
- Maintain previous versions in source control
- Tag production deployments
- Deploy previous version from Git tags
- Test rollback in sandbox before production

**Package Rollback**:
- Uninstall current package version
- Install previous package version
- Handle data migration if needed
- Verify rollback success

### Data Rollback

**Backup Strategies**:
- Regular data backups before deployments
- Export critical data before changes
- Use data export tools for backup
- Maintain backup retention policies

**Restore Procedures**:
- Document restore procedures
- Test restore processes regularly
- Maintain restore runbooks
- Verify data integrity after restore

### Feature Flag Rollbacks

**Feature Flag Patterns**:
- Use Custom Metadata or Custom Settings for feature flags
- Implement feature flag checks in code
- Support runtime feature toggling
- Log feature flag usage for analytics

**Rollback via Feature Flags**:
- Disable feature flags to rollback functionality
- No code deployment required
- Instant rollback capability
- Monitor feature flag changes

### Hotfix Strategies

**Hotfix Workflow**:
1. Create hotfix branch from production tag
2. Implement fix in hotfix branch
3. Test fix in sandbox environment
4. Deploy hotfix to production
5. Merge hotfix back to main branch

**Hotfix Best Practices**:
- Minimize hotfix scope
- Test thoroughly before deployment
- Document hotfix in change log
- Plan for proper merge back to main

## Related Patterns

- [Deployment Patterns](rag/project-methods/deployment-patterns.md) - Deployment methods and Metadata API patterns
- [Salesforce DX Patterns](rag/project-methods/sfdx-patterns.md) - SFDX project structure and commands
- [Environment Strategy](rag/operations/environment-strategy.md) - Org topology and environment management
- [Release Governance](rag/operations/release-governance.md) - Release approval and risk management
- [Testing Strategy](rag/project-methods/testing-strategy.md) - Comprehensive testing approaches

