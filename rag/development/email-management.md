---
layout: default
title: Email Management Patterns
description: Patterns for sending, receiving, and tracking email in Salesforce using standard features and Apex
permalink: /rag/development/email-management.html
level: Intermediate
tags:
  - email
  - communication
last_reviewed: 2025-12-03
---

# Email Management Patterns

> **Based on Real Implementation Experience**: Email is often the **primary communication channel** with customers, students, and citizens, and poorly designed email patterns quickly become a support burden.

## Overview

Salesforce supports multiple email mechanisms:

- **Standard email actions** (Send Email, Email Alerts in Flows).
- **Email-to-Case** and **On-Demand Email-to-Case**.
- **Apex email** (`Messaging.SingleEmailMessage`, `Messaging.MassEmailMessage`).

This document focuses on **when to use which mechanism**, how to manage **templates and branding**, and how to design email flows that are **reliable, traceable, and secure**.

## Prerequisites

- **Required Knowledge**:
  - Basic object model for leads, contacts, cases, and custom objects.
  - Familiarity with Flows and email templates.

- **Recommended Reading**:
  - <a href="{{ '/rag/development/flow-patterns.html' | relative_url }}">Flow Patterns</a>
  - <a href="{{ '/rag/development/error-handling-and-logging.html' | relative_url }}">Error Handling and Logging</a>

## When to Use Which Email Mechanism

### Use Standard Email Alerts and Actions When

- The email logic is **simple** (single template per scenario).
- You can express send conditions declaratively in **Flows** or **approval processes**.
- You want **admins** to be able to maintain templates and logic.

### Use Apex Email When

- The recipient list is **complex** (dynamic stakeholders, CC/BCC logic).
- You need **fine-grained control** over headers, attachments, or reply-to addresses.
- You require **advanced error handling** or logging beyond standard capabilities.

## Core Concepts

### Templates and Personalization

- Prefer **Lightning Email Templates** with merge fields.
- Keep **branding and layout** in templates, not in Apex.
- Use **letterheads** and shared layouts for consistency.

### Deliverability and Limits

- Be aware of **daily send limits** and **per-org restrictions**.
- Use **Organization-Wide Addresses** where appropriate.
- Work with security and compliance teams for **DKIM**, **SPF**, and **DMARC**.

## Patterns and Examples

### Pattern 1: Flow-Driven Notifications

- Triggered by **record changes** (status updates, ownership changes, SLA breaches).
- Use **Record-Triggered Flows** with **Email Alerts** referencing templates.
- Keep **entry criteria strict** to avoid spam.

### Pattern 2: Apex-Driven Bulk Notifications

- Use **Batch Apex or Queueable** to send emails in bulk while respecting limits.
- Use `SingleEmailMessage` and careful **batch sizing**.
- Log failures to a **logging object** or Platform Event.

## Edge Cases and Limitations

- High-volume email sending may require **Marketing Cloud** or **MFA/transactional** email providers.
- Some email clients **strip HTML** or modify layouts; test with major clients.
- Email-to-Case can create **duplicate cases** without good routing and deduplication rules.

## Related Patterns

- <a href="{{ '/rag/integrations/integration-platform-patterns.html' | relative_url }}">Integration Platform Patterns</a> - For external email systems.
- <a href="{{ '/rag/data-governance/data-residency-compliance.html' | relative_url }}">Data Residency and Compliance</a> - For email content and PII.

## Q&A

### Q: When should we move from standard email alerts to Apex email?

**A**: Move when you need **dynamic recipient logic**, **complex personalization**, **bulk sending with batching**, or **centralized logging** that is difficult to achieve using only declarative tools.

### Q: How do we avoid over-notifying users?

**A**: Define **clear notification rules**, add **rate limiting** where appropriate (e.g., only one email per case per hour), and test with real users. Avoid sending multiple near-identical notifications triggered by the same change.

