---
layout: default
title: Custom Settings and Custom Metadata Patterns
description: Patterns for using Custom Settings and Custom Metadata Types for configuration management in Salesforce
permalink: /rag/development/custom-settings-metadata-patterns.html
level: Intermediate
tags:
  - configuration
  - custom-metadata
  - custom-settings
last_reviewed: 2025-12-03
---

# Custom Settings and Custom Metadata Patterns

> **Pattern Intent**: Centralize configuration so that logic and data can change at different speeds without code rewrites or risky production edits.

## Overview

Custom Settings and Custom Metadata Types provide **declarative configuration storage**:

- **Custom Settings**: Row-level configuration cached in memory, good for org-wide and user-level flags.
- **Custom Metadata Types (CMDT)**: Metadata that can be **deployed** between orgs and packaged; preferred for most configuration in modern architectures.

This document explains how to choose between them and how to structure configuration for **Flows, Apex, and integrations**.

## Prerequisites

- **Required Knowledge**:
  - Basic understanding of objects and records in Salesforce.
  - Ability to create fields and records in Setup.

- **Recommended Reading**:
  - <a href="{{ '/rag/code-examples/utilities/custom-settings-examples.html' | relative_url }}">Custom Settings Code Examples</a>
  - <a href="{{ '/rag/code-examples/utilities/custom-metadata-examples.html' | relative_url }}">Custom Metadata Code Examples</a>
  - <a href="{{ '/rag/development/apex-patterns.html' | relative_url }}">Apex Patterns</a>

## When to Use

### Use Custom Metadata When

- Configuration must be **deployed** between environments (Git → CI/CD → orgs).
- You need **version control** and change tracking for configuration.
- Configuration is **referenced by Apex, Flows, and validation rules**.
- You work on **managed packages** or multi-org solutions.

### Use Custom Settings When

- Values are **org-specific** and not usually deployed (e.g., per-sandbox toggles).
- You need **user- or profile-level overrides** (`Hierarchy` type).
- You require **very fast, cached access** to simple flags and limits.

### Avoid Both When

- The data is **transactional** (belongs in objects, not configuration).
- You need **highly dynamic user-entered data** that changes frequently.

## Core Concepts

### Configuration as Data

Treat configuration as data:

- Keep **business rules** in CMDT where possible.
- Keep **operational flags** (e.g., “maintenance mode”) in Custom Settings.

### Lookup by External Keys

Use **stable keys** (e.g., `DeveloperName`, external Id-style fields) to look up CMDT or settings:

- Avoid hardcoding record Ids in Apex or Flow.
- Use **enums or constants** in Apex to reference configuration keys.

## Patterns and Examples

### Pattern 1: Feature Flag via Hierarchy Custom Setting

- Create a `Hierarchy` Custom Setting with a Boolean field such as `Enable_Feature_X__c`.
- Read it in Apex via `MySetting__c.getInstance().Enable_Feature_X__c`.
- Allow **per-user** or **per-profile** overrides for pilots.

### Pattern 2: CMDT-Driven Routing Rules

- Use a CMDT like `Routing_Rule__mdt` with fields:
  - `Channel__c`
  - `RecordType__c`
  - `Target_Queue__c`
- Query CMDT in Apex or Flow to determine routing without changing code.

### Pattern 3: Decision Framework: Custom Object vs CMDT vs Custom Setting

Use the decision frameworks described in the **Decision Frameworks** section of the repo (to be expanded) to select the right storage based on:

- **Who** maintains the data.
- **How often** it changes.
- Whether it must be **deployed** between orgs.

## Edge Cases and Limitations

- CMDT records cannot be modified by end users in production without **deployments** (good for control, bad for rapid changes).
- Custom Settings can be changed in production UI, which can be **risky** if not controlled.
- Both CMDT and Custom Settings count toward **limits** (number of records and total configuration).

## Related Patterns

- <a href="{{ '/rag/code-examples/utilities/custom-settings-examples.html' | relative_url }}">Custom Settings Examples</a>
- <a href="{{ '/rag/code-examples/utilities/custom-metadata-examples.html' | relative_url }}">Custom Metadata Examples</a>
- <a href="{{ '/rag/data-modeling/object-setup-and-configuration.html' | relative_url }}">Object Setup and Configuration</a>

## Q&A

### Q: When should I migrate from Custom Settings to Custom Metadata?

**A**: Migrate when you need **deployment control**, **versioning**, or **packaging** for configuration. CMDT is preferred for long-lived configuration, while Custom Settings are better for environment-specific toggles and hierarchy overrides.

### Q: Can I use CMDT in Flows?

**A**: Yes. Modern Flows can **reference CMDT** via Get Records and decision elements. This enables **configuration-driven Flows** where business rules are stored outside the Flow definition.

