---
layout: default
title: Deployment and CI/CD Patterns
description: This guide covers Salesforce deployment strategies, source control patterns, deployment best practices, Metadata API usage, and package development patterns
permalink: /rag/project-methods/deployment-patterns.html
---

# Deployment and CI/CD Patterns

## Overview

This guide covers Salesforce deployment strategies, source control patterns, deployment best practices, Metadata API usage, and package development patterns. These patterns are essential for managing Salesforce development lifecycle and ensuring reliable deployments.

**Related Patterns**:
- <a href="{{ '/rag/project-methods/delivery-framework.html' | relative_url }}">Delivery Framework</a> - Project delivery methodology
- <a href="{{ '/rag/project-methods/sfdx-patterns.html' | relative_url }}">Salesforce DX Patterns</a> - SFDX-specific patterns

## Consensus Best Practices

- **Use source control**: All metadata should be version controlled
- **Use Salesforce DX for new projects**: SFDX provides modern development workflow
- **Validate before deploying**: Always run validation before production deployment
- **Use deployment checklists**: Follow comprehensive checklists before deployment
- **Implement rollback strategies**: Plan for rollback in case of deployment failures
- **Use packages for reusable components**: Unlocked packages for modular development
- **Automate deployments**: Use CI/CD pipelines for consistent deployments
- **Test thoroughly**: Run all tests before production deployment

## Deployment Methods

### Change Sets

**When to use**:
- Small, ad-hoc deployments
- Deploying between connected orgs
- Quick fixes and hotfixes
- Non-technical users performing deployments

**Limitations**:
- Only works between connected orgs
- No source control integration
- Manual process
- Limited rollback capabilities

### Metadata API

**When to use**:
- Automated deployments
- CI/CD pipelines
- Deploying to multiple orgs
- Integration with external tools

**Advantages**:
- Programmatic deployment
- Source control integration
- Automated workflows
- Better rollback capabilities

### Salesforce DX (SFDX)

**When to use**:
- New projects and development
- Modern development workflow
- Package development
- CI/CD integration

**Advantages**:
- Source-driven development
- Scratch org support
- Package development
- Modern tooling

## Source Control Strategies

### Git Workflow Patterns

**Branching Strategy**:
- `main` branch: Production-ready code
- `develop` branch: Integration branch
- Feature branches: `feature/feature-name`
- Release branches: `release/version`
- Hotfix branches: `hotfix/issue-name`

**Commit Patterns**:
- Atomic commits: One logical change per commit
- Descriptive commit messages
- Reference work items in commits
- Regular commits (don't accumulate changes)

### Metadata Organization

**Directory Structure**:
```
force-app/
├── main/
│   ├── default/
│   │   ├── classes/
│   │   ├── triggers/
│   │   ├── lwc/
│   │   ├── flows/
│   │   └── objects/
│   └── test/
└── metadata/
```

**Best Practices**:
- Organize metadata by type
- Use consistent naming conventions
- Separate test classes
- Document metadata dependencies

## Deployment Best Practices

### Pre-Deployment Validation

**Checklist**:
- Run all tests locally
- Validate metadata dependencies
- Check for breaking changes
- Review deployment plan
- Verify environment configuration

### Deployment Process

**Steps**:
1. **Validate**: Run validation deployment
2. **Review**: Review validation results
3. **Deploy**: Execute deployment
4. **Verify**: Verify deployment success
5. **Test**: Run smoke tests
6. **Monitor**: Monitor for issues

### Rollback Strategies

**Approaches**:
- **Metadata rollback**: Deploy previous version
- **Data rollback**: Restore from backup
- **Feature flags**: Disable features via configuration
- **Quick fixes**: Deploy hotfixes

## Metadata API Patterns

### Metadata API Deployment

**Use Cases**:
- Automated deployments
- CI/CD pipelines
- Bulk metadata operations
- Cross-org deployments

**Patterns**:
- Deploy from source control
- Validate before deploy
- Handle deployment errors
- Track deployment status

### Metadata API Retrieval

**Use Cases**:
- Retrieving metadata from orgs
- Comparing orgs
- Backup metadata
- Migration planning

**Patterns**:
- Retrieve by type
- Retrieve by package
- Compare metadata
- Export metadata

## Package Development Patterns

### Unlocked Packages

**When to use**:
- Modular development
- Reusable components
- Team-based development
- Version management

**Patterns**:
- Package structure
- Dependency management
- Versioning strategy
- Package promotion

### Managed Packages

**When to use**:
- AppExchange apps
- Commercial products
- Protected intellectual property
- Distribution to multiple orgs

**Patterns**:
- Package structure
- Namespace management
- Upgrade handling
- Distribution strategy

## Q&A

### Q: What deployment methods are available in Salesforce?

**A**: Deployment methods: (1) **Change Sets** - for small, ad-hoc deployments between connected orgs, (2) **Metadata API** - for programmatic deployments, CI/CD integration, (3) **Salesforce DX (SFDX)** - modern source-driven workflow, (4) **Unlocked Packages** - for modular, versioned components, (5) **Ant Migration Tool** - command-line deployment tool. Choose based on project needs and workflow preferences.

### Q: When should I use Change Sets vs. Metadata API vs. SFDX?

**A**: Use **Change Sets** for: small deployments, non-technical users, quick fixes. Use **Metadata API** for: programmatic deployments, CI/CD integration, automated deployments. Use **SFDX** for: new projects, modern development workflow, source-driven development, scratch orgs. SFDX is recommended for new projects, Metadata API for automation, Change Sets for simple deployments.

### Q: How do I implement source control for Salesforce?

**A**: Implement source control by: (1) **Using Git** for version control, (2) **Storing all metadata** in source control, (3) **Using SFDX** for source-driven development, (4) **Using branching strategies** (feature branches, main branch), (5) **Committing frequently** (small, logical commits), (6) **Using pull requests** for code review, (7) **Tagging releases** (version tags for deployments).

### Q: What should be included in a deployment checklist?

**A**: Include in checklist: (1) **Metadata backup** (export before deployment), (2) **Test execution** (all tests pass, coverage met), (3) **Validation** (validate deployment, no errors), (4) **Security review** (profiles, permission sets), (5) **Rollback plan** (documented, tested), (6) **Communication** (notify stakeholders), (7) **Monitoring** (watch for errors after deployment), (8) **Documentation** (deployment notes, changes).

### Q: How do I implement rollback strategies?

**A**: Implement rollback by: (1) **Backing up metadata** before deployment (version control, export), (2) **Creating rollback scripts** (reverse deployment steps), (3) **Testing rollback procedures** in sandbox, (4) **Documenting rollback steps** (clear instructions), (5) **Using version control** to track changes, (6) **Planning rollback** before deployment (not after issues), (7) **Automating rollback** where possible.

### Q: What are unlocked packages and when should I use them?

**A**: **Unlocked packages** are versioned, modular components for Salesforce. Use them for: (1) **Modular development** (break down large codebases), (2) **Reusable components** (share across projects), (3) **Version management** (version components independently), (4) **Dependency management** (manage dependencies between components), (5) **Team collaboration** (independent team development). Unlocked packages provide better organization than monolithic deployments.

### Q: How do I use the Metadata API for deployments?

**A**: Use Metadata API by: (1) **Retrieving metadata** from source org, (2) **Deploying metadata** to target org, (3) **Validating deployments** (dry-run validation), (4) **Handling deployment errors** (parse error messages, fix issues), (5) **Automating deployments** (scripts, CI/CD integration), (6) **Tracking deployment status** (monitor deployment progress). Metadata API enables programmatic, automated deployments.

### Q: What are best practices for Salesforce deployments?

**A**: Best practices include: (1) **Use source control** (all metadata version controlled), (2) **Validate before deploying** (always run validation), (3) **Use deployment checklists** (comprehensive checklists), (4) **Implement rollback strategies** (plan for failures), (5) **Test thoroughly** (run all tests before production), (6) **Automate deployments** (CI/CD pipelines), (7) **Document deployments** (deployment notes, changes), (8) **Monitor after deployment** (watch for errors).

### Q: How do I handle deployment conflicts?

**A**: Handle conflicts by: (1) **Identifying conflicts** (metadata conflicts, dependency issues), (2) **Resolving conflicts** (merge changes, update dependencies), (3) **Testing resolution** (verify conflicts resolved), (4) **Coordinating deployments** (avoid simultaneous deployments), (5) **Using source control** (track changes, merge properly), (6) **Communicating changes** (notify team of deployments), (7) **Planning deployments** (coordinate to avoid conflicts).

### Q: What is the difference between validation and deployment?

**A**: **Validation** runs tests and checks without deploying (dry run). **Deployment** actually applies changes to the org. Always validate before deploying to production. Validation catches errors without affecting the org, while deployment makes changes permanent. Use validation in CI/CD pipelines to catch issues early, then deploy after validation passes.

## Related Patterns

- <a href="{{ '/rag/project-methods/sfdx-patterns.html' | relative_url }}">Salesforce DX Patterns</a> - SFDX-specific patterns
- <a href="{{ '/rag/project-methods/delivery-framework.html' | relative_url }}">Delivery Framework</a> - Project delivery methodology
- <a href="{{ '/rag/operations/cicd-patterns.html' | relative_url }}">CI/CD Patterns</a> - CI/CD automation patterns