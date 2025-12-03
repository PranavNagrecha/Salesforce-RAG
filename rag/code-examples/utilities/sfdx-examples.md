---
layout: default
title: Salesforce DX Code Examples
description: Salesforce DX provides command-line tools and workflows for modern Salesforce development
permalink: /rag/code-examples/utilities/sfdx-examples.html
---

# Salesforce DX Code Examples

> Complete, working code examples for Salesforce DX patterns.
> All examples are copy-paste ready and follow Salesforce best practices.

## Overview

Salesforce DX provides command-line tools and workflows for modern Salesforce development. These examples show common SFDX patterns and scripts.

**Related Patterns**:
- <a href="{{ '/rag/project-methods/sfdx-patterns.html' | relative_url }}">Salesforce DX Patterns</a>
- <a href="{{ '/rag/project-methods/deployment-patterns.html' | relative_url }}">Deployment Patterns</a>

## Examples

### Example 1: SFDX Project Setup

**Pattern**: Initialize SFDX project
**Use Case**: Starting new Salesforce project
**Complexity**: Basic

**Solution**:

```bash
# Initialize SFDX project
sf project generate --name my-project

# Create scratch org
sf org create scratch --definition-file config/project-scratch-def.json --alias dev

# Push source to scratch org
sf project deploy start --source-dir force-app --target-org dev

# Open scratch org
sf org open --target-org dev
```

---

### Example 2: SFDX Deployment Script

**Pattern**: Automated deployment script
**Use Case**: CI/CD pipeline deployment
**Complexity**: Intermediate

**Solution**:

```bash
#!/bin/bash
# Deploy to target org with validation

# Set variables
TARGET_ORG=$1
VALIDATE_ONLY=${2:-false}

# Validate deployment
if [ "$VALIDATE_ONLY" = "true" ]; then
    sf project deploy start \
        --source-dir force-app \
        --target-org $TARGET_ORG \
        --dry-run \
        --wait 10
else
    # Deploy
    sf project deploy start \
        --source-dir force-app \
        --target-org $TARGET_ORG \
        --wait 10
    
    # Run tests
    sf apex run test \
        --target-org $TARGET_ORG \
        --code-coverage \
        --result-format human \
        --wait 10
fi
```

---

## Related Patterns

- <a href="{{ '/rag/project-methods/sfdx-patterns.html' | relative_url }}">Salesforce DX Patterns</a> - Complete SFDX guide
- <a href="{{ '/rag/project-methods/deployment-patterns.html' | relative_url }}">Deployment Patterns</a> - Deployment patterns