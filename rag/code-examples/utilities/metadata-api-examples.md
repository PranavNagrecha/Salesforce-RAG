---
layout: default
title: Metadata API Code Examples
description: The Metadata API allows programmatic deployment and retrieval of Salesforce metadata
permalink: /rag/code-examples/utilities/metadata-api-examples.html
---

# Metadata API Code Examples

> Complete, working code examples for Metadata API patterns.
> All examples are copy-paste ready and follow Salesforce best practices.

## Overview

The Metadata API allows programmatic deployment and retrieval of Salesforce metadata. It's used for automated deployments, CI/CD pipelines, and bulk metadata operations.

**Related Patterns**:
- <a href="{{ '/rag/project-methods/deployment-patterns.html' | relative_url }}">Deployment Patterns</a>
- <a href="{{ '/rag/project-methods/sfdx-patterns.html' | relative_url }}">Salesforce DX Patterns</a>

## Examples

### Example 1: Metadata API Deployment

**Pattern**: Deploy metadata using Metadata API
**Use Case**: Automated metadata deployment
**Complexity**: Advanced

**Solution**:

```apex
/**
 * Utility class for Metadata API deployment
 */
public class MetadataApiDeployment {
    
    /**
     * Deploy metadata from zip file
     * @param zipFile Base64 encoded zip file
     * @return AsyncResult with deployment ID
     */
    public static MetadataService.AsyncResult deployMetadata(Blob zipFile) {
        MetadataService.MetadataPort service = createService();
        MetadataService.DeployOptions deployOptions = new MetadataService.DeployOptions();
        deployOptions.allowMissingFiles = false;
        deployOptions.autoUpdatePackage = false;
        deployOptions.checkOnly = false;
        deployOptions.ignoreWarnings = false;
        deployOptions.performRetrieve = false;
        deployOptions.purgeOnDelete = false;
        deployOptions.rollbackOnError = true;
        deployOptions.runAllTests = false;
        deployOptions.singlePackage = true;
        
        MetadataService.AsyncResult result = service.deploy(zipFile, deployOptions);
        return result;
    }
    
    /**
     * Check deployment status
     * @param deploymentId Deployment ID
     * @return DeployResult with deployment status
     */
    public static MetadataService.DeployResult checkDeploymentStatus(String deploymentId) {
        MetadataService.MetadataPort service = createService();
        MetadataService.DeployResult result = service.checkDeployStatus(deploymentId, false);
        return result;
    }
    
    private static MetadataService.MetadataPort createService() {
        MetadataService.MetadataPort service = new MetadataService.MetadataPort();
        service.SessionHeader = new MetadataService.SessionHeader_element();
        service.SessionHeader.sessionId = UserInfo.getSessionId();
        return service;
    }
}
```

**Note**: This example uses a MetadataService wrapper class. In practice, you would use the Metadata API WSDL or Salesforce CLI.

---

## Related Patterns

- <a href="{{ '/rag/project-methods/deployment-patterns.html' | relative_url }}">Deployment Patterns</a> - Complete deployment guide
- <a href="{{ '/rag/project-methods/sfdx-patterns.html' | relative_url }}">Salesforce DX Patterns</a> - SFDX patterns

