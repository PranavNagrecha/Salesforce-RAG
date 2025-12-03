---
title: "Salesforce DX (SFDX) Patterns"
level: "Intermediate"
tags:
  - project-methods
  - sfdx
  - salesforce-dx
  - source-control
last_reviewed: "2025-01-XX"
---

# Salesforce DX (SFDX) Patterns

## Overview

Salesforce DX provides a modern, source-driven development workflow for Salesforce. This guide covers SFDX project structure, commands, scratch org patterns, source tracking, and CI/CD integration.

**Related Patterns**:
- <a href="{{ '/rag/project-methods/project-methods/deployment-patterns.html' | relative_url }}">Deployment Patterns</a> - General deployment patterns
- <a href="{{ '/rag/project-methods/project-methods/delivery-framework.html' | relative_url }}">Delivery Framework</a> - Project delivery methodology

## Consensus Best Practices

- **Use SFDX for new projects**: Modern development workflow
- **Use scratch orgs for development**: Isolated development environments
- **Track source changes**: Use source tracking for change management
- **Use packages for modularity**: Unlocked packages for reusable components
- **Automate with CI/CD**: Integrate SFDX with CI/CD pipelines
- **Follow project structure**: Use standard SFDX project structure
- **Version control everything**: All metadata in source control

## SFDX Project Structure

### Standard Structure

```
project-root/
├── force-app/
│   └── main/
│       └── default/
│           ├── classes/
│           ├── triggers/
│           ├── lwc/
│           ├── flows/
│           └── objects/
├── force-app-test/
│   └── main/
│       └── default/
│           └── classes/
├── sfdx-project.json
├── .gitignore
└── README.md
```

### Multi-Package Structure

```
project-root/
├── packages/
│   ├── core/
│   ├── integration/
│   └── ui/
├── sfdx-project.json
└── .gitignore
```

## SFDX Commands and Workflows

### Common Commands

**Org Management**:
- `sf org create scratch`: Create scratch org
- `sf org open`: Open org in browser
- `sf org list`: List all orgs
- `sf org delete`: Delete org

**Source Management**:
- `sf project deploy start`: Deploy source to org
- `sf project retrieve start`: Retrieve source from org
- `sf project generate`: Generate metadata

**Package Management**:
- `sf package create`: Create package
- `sf package version create`: Create package version
- `sf package install`: Install package

### Development Workflow

1. **Create scratch org**: `sf org create scratch`
2. **Push source**: `sf project deploy start`
3. **Develop**: Make changes in org or IDE
4. **Pull changes**: `sf project retrieve start`
5. **Commit**: Commit to source control
6. **Deploy**: Deploy to target org

## Scratch Org Patterns

### Scratch Org Configuration

**config/project-scratch-def.json**:
```json
{
  "orgName": "My Company",
  "edition": "Enterprise",
  "features": ["EnableSetPasswordInApi"],
  "settings": {
    "lightningExperienceSettings": {
      "enableS1DesktopEnabled": true
    }
  }
}
```

### Scratch Org Lifecycle

1. **Create**: Create scratch org
2. **Configure**: Set up org configuration
3. **Develop**: Develop and test
4. **Delete**: Delete when done

## Source Tracking

### Source Tracking Patterns

- **Track all changes**: Source tracking monitors all metadata changes
- **Resolve conflicts**: Handle conflicts between org and source
- **Sync regularly**: Keep org and source in sync

### Conflict Resolution

- **Pull changes**: Retrieve changes from org
- **Resolve conflicts**: Manually resolve conflicts
- **Push changes**: Deploy resolved changes

## CI/CD Integration

### CI/CD Patterns

- **Automated testing**: Run tests in CI/CD pipeline
- **Automated deployment**: Deploy on successful tests
- **Environment promotion**: Promote through environments
- **Rollback on failure**: Automatically rollback on failure

### Pipeline Stages

1. **Build**: Build and validate
2. **Test**: Run all tests
3. **Deploy**: Deploy to target org
4. **Verify**: Verify deployment
5. **Notify**: Send notifications

## Q&A

### Q: What is Salesforce DX (SFDX)?

**A**: **Salesforce DX (SFDX)** is a modern, source-driven development workflow for Salesforce. It provides: (1) **Source-driven development** (metadata in source control), (2) **Scratch orgs** (temporary, isolated development environments), (3) **Source tracking** (automatic change tracking), (4) **CLI tools** (command-line interface for development), (5) **Package development** (unlocked packages), (6) **CI/CD integration** (modern development workflow).

### Q: When should I use SFDX vs. traditional development?

**A**: Use **SFDX** for: (1) **New projects** (greenfield implementations), (2) **Modern development workflow** (source-driven, Git-based), (3) **Team collaboration** (multiple developers, source control), (4) **CI/CD integration** (automated deployments), (5) **Package development** (unlocked packages). Use **traditional** for: legacy projects not yet migrated, simple deployments, non-technical users.

### Q: What are scratch orgs and how do I use them?

**A**: **Scratch orgs** are temporary, isolated Salesforce orgs for development. Use them by: (1) **Creating scratch orgs** (`sf org create scratch`), (2) **Pushing source** to scratch org (`sf project deploy start`), (3) **Developing in scratch org** (isolated development), (4) **Pulling changes** from scratch org (`sf project deploy retrieve`), (5) **Deleting scratch orgs** when done. Scratch orgs provide clean, isolated environments for development.

### Q: How do I structure an SFDX project?

**A**: Structure SFDX project: (1) **force-app/main/default/** - main source code (classes, triggers, LWC, flows, objects), (2) **force-app-test/main/default/** - test classes, (3) **sfdx-project.json** - project configuration, (4) **config/** - org configuration files, (5) **scripts/** - deployment scripts, (6) **.gitignore** - Git ignore rules. Follow standard SFDX project structure for consistency.

### Q: How do I track source changes in SFDX?

**A**: Track source changes by: (1) **Using source tracking** (SFDX automatically tracks changes in source-tracked orgs), (2) **Pulling changes** from org (`sf project deploy retrieve`), (3) **Pushing changes** to org (`sf project deploy start`), (4) **Using Git** for version control (commit changes to Git), (5) **Reviewing changes** (`sf project deploy report`), (6) **Resolving conflicts** (merge changes properly).

### Q: How do I integrate SFDX with CI/CD?

**A**: Integrate SFDX with CI/CD by: (1) **Installing Salesforce CLI** in CI environment, (2) **Authenticating** to Salesforce orgs (JWT, OAuth), (3) **Running SFDX commands** in CI pipeline (`sf project deploy start`, `sf apex run test`), (4) **Validating deployments** before production, (5) **Running tests** in CI pipeline, (6) **Deploying** after validation passes, (7) **Reporting results** (test results, deployment status).

### Q: What SFDX commands should I know?

**A**: Essential commands: (1) **`sf org create scratch`** - create scratch org, (2) **`sf project deploy start`** - deploy source to org, (3) **`sf project deploy retrieve`** - retrieve changes from org, (4) **`sf apex run test`** - run Apex tests, (5) **`sf org open`** - open org in browser, (6) **`sf org list`** - list orgs, (7) **`sf project generate manifest`** - generate package manifest. Learn these commands for daily SFDX workflow.

### Q: How do I use unlocked packages with SFDX?

**A**: Use unlocked packages by: (1) **Creating package** (`sf package create`), (2) **Adding metadata** to package (`sf package version create`), (3) **Versioning package** (semantic versioning), (4) **Installing package** in orgs (`sf package install`), (5) **Managing dependencies** (package dependencies), (6) **Upgrading packages** (package upgrades). Unlocked packages enable modular, versioned component development.

### Q: What are best practices for SFDX development?

**A**: Best practices include: (1) **Use SFDX for new projects** (modern workflow), (2) **Use scratch orgs** for development (isolated environments), (3) **Track source changes** (use source tracking), (4) **Version control everything** (all metadata in Git), (5) **Use packages** for modularity (unlocked packages), (6) **Automate with CI/CD** (integrate SFDX with CI/CD), (7) **Follow project structure** (standard SFDX structure), (8) **Test thoroughly** (run tests in CI/CD).

### Q: How do I migrate from traditional development to SFDX?

**A**: Migrate to SFDX by: (1) **Setting up SFDX project** (create project structure), (2) **Retrieving metadata** from org (`sf project deploy retrieve`), (3) **Setting up source control** (Git repository), (4) **Converting orgs** to source-tracked (if possible), (5) **Training team** on SFDX workflow, (6) **Gradually adopting SFDX** (start with new features), (7) **Migrating existing code** incrementally. Plan migration carefully and train team on SFDX.

## Related Patterns

- <a href="{{ '/rag/project-methods/project-methods/deployment-patterns.html' | relative_url }}">Deployment Patterns</a> - General deployment patterns
- <a href="{{ '/rag/project-methods/project-methods/delivery-framework.html' | relative_url }}">Delivery Framework</a> - Project delivery methodology
- <a href="{{ '/rag/project-methods/operations/cicd-patterns.html' | relative_url }}">CI/CD Patterns</a> - CI/CD automation patterns

