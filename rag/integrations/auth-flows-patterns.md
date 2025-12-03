---
layout: default
title: Authentication Flow Patterns
description: Patterns for implementing OAuth and related authentication flows for Salesforce integrations
permalink: /rag/integrations/auth-flows-patterns.html
---

## What Was Actually Done

- Implemented OAuth 2.0 client credentials flow for server-to-server integrations.
- Used Named Credentials and Connected Apps to manage tokens and endpoints.
- Designed flows where external systems call Salesforce APIs and where Salesforce calls external APIs.

## Patterns

### Pattern 1: Client Credentials for External System → Salesforce

- External system authenticates to Salesforce using a Connected App with OAuth 2.0 client credentials.
- Scoped to an Integration User with the Integration User License where possible.

### Pattern 2: Client Credentials for Salesforce → External System

- Salesforce uses Named Credentials configured with OAuth 2.0 client credentials.
- Apex callouts reference the Named Credential endpoint rather than hardcoded URLs.

## To Validate

- Confirm chosen flow per integration is documented and least-privilege scopes are used.
- Ensure token lifetimes and rotation are handled by platform features where possible.


