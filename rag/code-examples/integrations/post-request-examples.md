---
layout: default
title: REST POST Request Code Examples
description: Examples for performing REST POST callouts from Apex using Named Credentials
permalink: /rag/code-examples/integrations/post-request-examples.html
---

## Example: Basic POST Request

```apex
public with sharing class RestPostService {
    @AuraEnabled
    public static void sendPayload(String payloadJson) {
        HttpRequest req = new HttpRequest();
        req.setEndpoint('callout:MyNamedCredential/api/resource');
        req.setMethod('POST');
        req.setHeader('Content-Type', 'application/json');
        req.setBody(payloadJson);

        Http http = new Http();
        HTTPResponse res = http.send(req);

        if (res.getStatusCode() >= 400) {
            // Handle error
        }
    }
}
```

## To Validate

- Confirm the Named Credential is configured with the correct base URL and authentication.
- Ensure timeouts and error handling follow callout best practices.


