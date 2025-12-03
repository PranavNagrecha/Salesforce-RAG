---
layout: default
title: SFDX Project Template
description: Documentation for SFDX Project Template
permalink: /rag/code-examples/templates/sfdx-project-template.html
---

# SFDX Project Template

**Use Case**: Initialize new SFDX project

**Template**:

**sfdx-project.json**:
```json
{
  "packageDirectories": [
    {
      "path": "force-app",
      "default": true
    }
  ],
  "name": "My Project",
  "namespace": "",
  "sfdcLoginUrl": "https://login.salesforce.com",
  "sourceApiVersion": "60.0"
}
```

**config/project-scratch-def.json**:
```json
{
  "orgName": "My Company",
  "edition": "Enterprise",
  "features": [],
  "settings": {
    "lightningExperienceSettings": {
      "enableS1DesktopEnabled": true
    }
  }
}
```

**Usage**:
```bash
# Initialize project
sf project generate --name my-project

# Create scratch org
sf org create scratch --definition-file config/project-scratch-def.json
```