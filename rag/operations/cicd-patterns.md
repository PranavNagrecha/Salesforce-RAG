---
layout: default
title: CI/CD Patterns for Salesforce
description: This guide covers comprehensive CI/CD patterns for Salesforce, including metadata vs
permalink: /rag/operations/cicd-patterns.html
---

# CI/CD Patterns for Salesforce

## Overview

This guide covers comprehensive CI/CD patterns for Salesforce, including metadata vs. source-tracked orgs, unlocked packages, sandbox seeding, deployment validation strategies, and rollback patterns. These patterns are essential for managing complex Salesforce development lifecycles with multiple teams and environments.

**Related Patterns**:
- <a href="{{ '/rag/project-methods/deployment-patterns.html' | relative_url }}">Deployment Patterns</a> - Deployment methods and best practices
- <a href="{{ '/rag/project-methods/sfdx-patterns.html' | relative_url }}">Salesforce DX Patterns</a> - SFDX-specific patterns
- <a href="{{ '/rag/operations/environment-strategy.html' | relative_url }}">Environment Strategy</a> - Org topology and environment management
- <a href="{{ '/rag/operations/release-governance.html' | relative_url }}">Release Governance</a> - Release approval and risk management

## Prerequisites

**Required Knowledge**:
- Understanding of Salesforce metadata and deployment concepts
- Familiarity with version control systems (Git)
- Knowledge of Salesforce CLI and deployment tools
- Understanding of sandbox types and their purposes
- Basic knowledge of CI/CD concepts and pipelines

**Recommended Reading**:
- `rag/project-methods/deployment-patterns.md` - Deployment methods and patterns
- `rag/project-methods/sfdx-patterns.md` - Salesforce DX patterns
- `rag/operations/environment-strategy.md` - Environment management
- `rag/operations/release-governance.md` - Release approval processes

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

## Q&A

### Q: What is the difference between metadata orgs and source-tracked orgs?

**A**: **Metadata orgs** use Change Sets or Metadata API for deployments and require manual tracking of changes. **Source-tracked orgs** automatically track changes and integrate with Git and CI/CD pipelines. Use source-tracked orgs for new projects or when modernizing existing projects. Metadata orgs are for legacy projects not yet converted.

### Q: When should I use unlocked packages?

**A**: Use **unlocked packages** when: (1) **Breaking down large codebases** into manageable modules, (2) **Enabling modular development** across teams, (3) **Versioning components** independently, (4) **Sharing components** across projects, (5) **Managing dependencies** between components. Unlocked packages provide better organization and versioning than monolithic deployments.

### Q: How do I automate sandbox seeding?

**A**: Automate sandbox seeding by: (1) **Creating seed data scripts** (Apex, Data Loader, ETL tools), (2) **Using test data factories** for consistent data, (3) **Automating seed execution** in CI/CD pipelines, (4) **Scheduling regular refreshes** of seed data, (5) **Versioning seed data** in source control, (6) **Documenting seed data requirements**. Ensure consistent test data across environments.

### Q: What validation should I perform before deployments?

**A**: Validate before deployments by: (1) **Running Apex tests** (minimum 75% coverage), (2) **Validating metadata** (check for errors, dependencies), (3) **Checking governor limits** (ensure no limit violations), (4) **Reviewing security** (profiles, permission sets), (5) **Testing in sandbox** first, (6) **Running smoke tests** after deployment. Never skip validation before production deployments.

### Q: How do I implement rollback strategies for Salesforce deployments?

**A**: Implement rollback by: (1) **Backing up metadata** before deployment, (2) **Using version control** to track changes, (3) **Creating rollback scripts** (reverse deployment steps), (4) **Testing rollback procedures** in sandbox, (5) **Documenting rollback steps**, (6) **Using feature flags** for quick rollbacks without code changes. Always have a rollback plan before production deployments.

### Q: What are feature flags and how do I use them in Salesforce?

**A**: **Feature flags** are configuration settings that enable/disable features without code changes. Use them for: (1) **Gradual rollouts** (enable for subset of users first), (2) **Quick rollbacks** (disable feature without deployment), (3) **A/B testing** (test different feature versions), (4) **Environment-specific behavior** (different behavior per environment). Implement using Custom Metadata Types or Custom Settings.

### Q: How do I set up CI/CD pipelines for Salesforce?

**A**: Set up CI/CD pipelines by: (1) **Using source control** (Git) for metadata, (2) **Automating deployments** (Salesforce CLI, Metadata API), (3) **Running tests** on every commit, (4) **Validating deployments** before production, (5) **Automating sandbox seeding**, (6) **Using CI/CD tools** (Jenkins, GitHub Actions, GitLab CI), (7) **Monitoring deployments** and test results.

### Q: What is the difference between validation and deployment?

**A**: **Validation** runs tests and checks without deploying to the org (dry run). **Deployment** actually applies changes to the org. Always validate before deploying to production. Validation catches errors without affecting the org, while deployment makes changes permanent. Use validation in CI/CD pipelines to catch issues early.

### Q: How do I handle hotfixes in a CI/CD workflow?

**A**: Handle hotfixes by: (1) **Creating hotfix branch** from production, (2) **Fixing issue** in hotfix branch, (3) **Testing thoroughly** before deployment, (4) **Deploying to production** from hotfix branch, (5) **Merging hotfix back** to main branch, (6) **Documenting hotfix** in change log. Ensure hotfixes don't break existing functionality.

### Q: What should I include in a deployment checklist?

**A**: Include in deployment checklist: (1) **Metadata backup** (version control, export), (2) **Test execution** (all tests pass, coverage met), (3) **Validation** (no errors, dependencies resolved), (4) **Security review** (profiles, permission sets), (5) **Rollback plan** (documented, tested), (6) **Communication** (notify stakeholders), (7) **Monitoring** (watch for errors after deployment).

## Edge Cases and Limitations

### Edge Case 1: Deployment Conflicts with Multiple Teams

**Scenario**: Multiple teams deploying to the same org simultaneously, causing metadata conflicts and deployment failures.

**Consideration**:
- Coordinate deployments through release governance
- Use feature flags to isolate team changes
- Implement deployment locks or scheduling
- Test deployment order and dependencies
- Use unlocked packages to isolate team work
- Monitor deployment conflicts and adjust processes

### Edge Case 2: Sandbox Refresh During Active Development

**Scenario**: Sandbox refresh occurs while developers have uncommitted work, causing data loss or metadata conflicts.

**Consideration**:
- Communicate refresh schedules clearly
- Require all work to be committed before refresh
- Use source control to preserve uncommitted changes
- Plan refresh windows during low-activity periods
- Implement refresh approval process
- Document refresh procedures and expectations

### Edge Case 3: Package Dependency Conflicts

**Scenario**: Unlocked packages with conflicting dependencies or version mismatches causing deployment failures.

**Consideration**:
- Document package dependencies clearly
- Test package combinations before deployment
- Use package versioning strategy
- Resolve dependency conflicts early
- Consider package consolidation when appropriate
- Monitor package dependency health

### Edge Case 4: Test Failures in CI/CD Pipeline

**Scenario**: Flaky tests or environment-specific test failures causing CI/CD pipeline failures and deployment delays.

**Consideration**:
- Identify and fix flaky tests
- Use test data factories for consistent test data
- Isolate environment-specific test issues
- Implement retry logic for transient failures
- Monitor test stability and performance
- Document test dependencies and requirements

### Edge Case 5: Rollback Complexity with Data Changes

**Scenario**: Deployment includes data changes that cannot be easily rolled back, causing rollback complexity.

**Consideration**:
- Separate metadata and data deployments when possible
- Document data changes and rollback procedures
- Test rollback procedures in sandbox
- Use feature flags to disable features without rollback
- Plan for data migration during rollback
- Consider data backup before data-changing deployments

### Limitations

- **Deployment Time Limits**: Large deployments may hit timeout limits
- **Test Execution Limits**: Test execution time limits may affect CI/CD pipelines
- **Package Version Limits**: Package versioning has practical limits
- **Sandbox Refresh Limits**: Sandbox refresh frequency and timing constraints
- **Metadata API Limits**: Metadata API has rate limits affecting deployment speed
- **Source-Tracked Org Limits**: Source-tracked orgs have limitations with certain metadata types
- **CI/CD Tool Limits**: CI/CD tools may have execution time and resource limits
- **Rollback Complexity**: Some changes cannot be easily rolled back (data, certain metadata types)

## Related Patterns

**See Also**:
- <a href="{{ '/rag/operations/environment-strategy.html' | relative_url }}">Environment Strategy</a> - Org topology and environment management
- <a href="{{ '/rag/operations/release-governance.html' | relative_url }}">Release Governance</a> - Release approval and risk management

**Related Domains**:
- <a href="{{ '/rag/project-methods/deployment-patterns.html' | relative_url }}">Deployment Patterns</a> - Deployment methods and Metadata API patterns
- <a href="{{ '/rag/project-methods/sfdx-patterns.html' | relative_url }}">Salesforce DX Patterns</a> - SFDX project structure and commands
- <a href="{{ '/rag/project-methods/testing-strategy.html' | relative_url }}">Testing Strategy</a> - Comprehensive testing approaches

- <a href="{{ '/rag/project-methods/deployment-patterns.html' | relative_url }}">Deployment Patterns</a> - Deployment methods and Metadata API patterns
- <a href="{{ '/rag/project-methods/sfdx-patterns.html' | relative_url }}">Salesforce DX Patterns</a> - SFDX project structure and commands
- <a href="{{ '/rag/operations/environment-strategy.html' | relative_url }}">Environment Strategy</a> - Org topology and environment management
- <a href="{{ '/rag/operations/release-governance.html' | relative_url }}">Release Governance</a> - Release approval and risk management
- <a href="{{ '/rag/project-methods/testing-strategy.html' | relative_url }}">Testing Strategy</a> - Comprehensive testing approaches

