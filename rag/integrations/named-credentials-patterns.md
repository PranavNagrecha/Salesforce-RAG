---
layout: default
title: Named Credentials Patterns
description: Patterns for using Named Credentials to manage external endpoint URLs and authentication
permalink: /rag/integrations/named-credentials-patterns.html
---

## What Was Actually Done

- Standardized on Named Credentials for all outbound HTTP callouts instead of hardcoded URLs and credentials.
- Used OAuth 2.0 client credentials with Named Credentials for secure token management.
- Pointed Apex integration code to `callout:Named_Credential` endpoints referenced in callout examples.

## Patterns

### Pattern 1: Basic Named Credential Usage

```apex
HttpRequest req = new HttpRequest();
req.setEndpoint('callout:MyNamedCredential/api/resource');
req.setMethod('GET');

Http http = new Http();
HTTPResponse res = http.send(req);
```

### Pattern 2: Environment-Specific Endpoints

- Use one Named Credential per environment and avoid environment flags in code.
- Store environment-specific paths or switches in Custom Metadata where needed.

## To Validate

- Confirm all integration endpoints referenced in Apex use Named Credentials.
- Verify permissions so only integration users can use sensitive Named Credentials.


