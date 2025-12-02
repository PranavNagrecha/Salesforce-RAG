# Salesforce DX (SFDX) Patterns

## Overview

Salesforce DX provides a modern, source-driven development workflow for Salesforce. This guide covers SFDX project structure, commands, scratch org patterns, source tracking, and CI/CD integration.

**Related Patterns**:
- [Deployment Patterns](deployment-patterns.md) - General deployment patterns
- [Delivery Framework](delivery-framework.md) - Project delivery methodology

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

## Related Patterns

- [Deployment Patterns](deployment-patterns.md) - General deployment patterns
- [Delivery Framework](delivery-framework.md) - Project delivery methodology

