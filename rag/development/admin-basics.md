---
layout: default
title: Salesforce Admin Basics
description: Core responsibilities, skills, and configuration patterns for Salesforce administrators
permalink: /rag/development/admin-basics.html
level: Beginner
tags:
  - admin
  - configuration
  - fundamentals
last_reviewed: 2025-12-03
---

# Salesforce Admin Basics

> **Based on Real Implementation Experience**: This guide captures the practical tasks and patterns that successful admins use on real Salesforce programs, not just what appears on certification blueprints.

## Overview

Salesforce administrators own **day-to-day configuration, data quality, and user enablement**. They translate business requirements into declarative solutions using objects, fields, validation rules, Flows, page layouts, and permissions.

This document focuses on:

- Core admin responsibilities on implementation and BAU teams.
- Safe configuration patterns that scale.
- How admins collaborate with developers and architects.

## Prerequisites

- **Required Knowledge**:
  - Basic CRM concepts (accounts, contacts, leads, opportunities, cases).
  - Comfort with clicking through Setup.

- **Recommended Reading**:
  - <a href="{{ '/rag/data-modeling/object-setup-and-configuration.html' | relative_url }}">Object Setup and Configuration</a> - How to configure objects correctly.
  - <a href="{{ '/rag/development/formulas-validation-rules.html' | relative_url }}">Formulas and Validation Rules</a> - Data quality patterns.
  - <a href="{{ '/rag/security/permission-set-architecture.html' | relative_url }}">Permission Set Architecture</a> - Modern security patterns.

## When to Use Admin-Driven Configuration

### Use Configuration When

- Requirements can be met with **standard features** (fields, validation, workflow via Flow, page layouts, Dynamic Forms).
- Logic is **record-centric** and does not require complex algorithms.
- Business wants the ability to **adjust behavior without a deployment**.
- The change impacts **labels, layouts, picklists, or simple routing**.

### Avoid Configuration Only When

- Logic is **complex, deeply nested, or performance critical**.
- You need **robust error handling** or integrations with external systems.
- You must handle **very high data volumes** or advanced caching.
- You need patterns that are **easier to express in Apex** (see `apex-patterns.md`).

## Core Concepts

### Configuration vs. Customization

- **Configuration**: Changes made through Setup UI (objects, fields, validation rules, Flows, page layouts).
- **Customization**: Changes requiring code (Apex, LWC, Aura), custom middleware, or external services.

Good admins know when to stay declarative and when to pull in a developer.

### Safe Changes in Production

Admin work should be:

- **Repeatable**: Documented and, ideally, scripted via metadata (source control).
- **Reversible**: Changes can be undone if they have unexpected impact.
- **Tested**: High-impact changes should be validated in a sandbox first.

## Patterns and Examples

### Pattern 1: Safe Field Additions

- Add fields in a **sandbox first**.
- Set **field-level security** and **profiles/permission sets** explicitly.
- Add fields to **page layouts and Lightning pages** intentionally; avoid “add to all layouts” by default.
- Coordinate with data migration and integrations when fields are required downstream.

### Pattern 2: Validation Rule Rollout

- Start with **warning reports** or list views to show data that would fail the rule.
- Communicate upcoming changes to users.
- Enable the rule with **clear error messages** referencing help text or documentation.

### Pattern 3: Flow as Primary Automation

- Prefer **record-triggered Flows** for automation over legacy Workflow Rules and Process Builder.
- Keep each Flow **focused** (single responsibility, clear entry criteria).
- Use **subflows** for reusable logic.

See <a href="{{ '/rag/development/flow-patterns.html' | relative_url }}">Flow Patterns</a> for details.

## Edge Cases and Limitations

- Some “simple” configuration (e.g., complex validation rules) can become hard to maintain if overused.
- Changes to **sharing settings, role hierarchy, and OWD** can have wide impact and should be reviewed with an architect.
- Admins should avoid **directly editing managed package objects** without guidance from vendor documentation.

## Related Patterns

- <a href="{{ '/rag/development/flow-patterns.html' | relative_url }}">Flow Design and Orchestration Patterns</a>
- <a href="{{ '/rag/security/permission-set-architecture.html' | relative_url }}">Permission Set-Driven Security Architecture</a>
- <a href="{{ '/rag/data-governance/data-quality-stewardship.html' | relative_url }}">Data Quality and Stewardship</a>

## Q&A

### Q: When should I escalate a requirement from admin configuration to Apex?

**A**: Escalate when the requirement involves **complex logic**, **heavy data volumes**, **advanced error handling**, or **integrations** that are difficult to express in Flow or formulas. Use `apex-patterns.md` to validate that Apex is really needed and to choose the right pattern.

### Q: How can admins work effectively with developers?

**A**: Agree on **clear boundaries**: admins own configuration and simple Flows; developers own Apex, LWCs, and integration code. Use **sandboxes and source control** to share changes, and document requirements as **small, testable stories**.

### Q: What is the biggest risk of admin-only changes in production?

**A**: The biggest risk is **unintended side effects**—for example, a new validation rule breaking integrations, or a Flow causing recursive updates. Always test changes with representative data in a sandbox, and coordinate with developers and architects for high-impact areas like order of execution, sharing, and integrations.

