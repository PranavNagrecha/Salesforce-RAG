---
layout: default
title: REST Resource Code Examples
description: Examples for implementing REST resources in Apex with @RestResource and HTTP method annotations
permalink: /rag/code-examples/integrations/rest-resource-examples.html
---

## Example: Simple REST Resource

```apex
@RestResource(urlMapping='/example/v1/*')
global with sharing class ExampleRestResource {

    @HttpGet
    global static ExampleResponse getExample() {
        ExampleResponse res = new ExampleResponse();
        res.message = 'OK';
        return res;
    }

    global class ExampleResponse {
        public String message;
    }
}
```

## To Validate

- Confirm URL mappings, authentication, and profiles/permission sets for the REST resource.


