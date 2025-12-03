---
layout: default
title: Lightning App Builder Patterns
description: Patterns for composing Lightning pages, using Dynamic Forms, and structuring layouts
permalink: /rag/development/lightning-app-builder.html
level: Beginner
tags:
  - ui
  - lightning-app-builder
last_reviewed: 2025-12-03
---

# Lightning App Builder Patterns

> **Based on Real Implementation Experience**: These patterns reflect what works for maintainable Lightning pages in complex orgs.

## Overview

Lightning App Builder is the **primary tool** for composing record pages, home pages, and app pages:

- Place **standard components**, **custom LWCs**, and **Dynamic Forms sections**.
- Control **visibility** by profile, record type, and filter criteria.

This document focuses on layout and composition patterns, not detailed LWC implementation.

## Prerequisites

- **Required Knowledge**:
  - Basic Lightning Experience navigation.
  - Understanding of page layouts and record types.

- **Recommended Reading**:
  - <a href="{{ '/rag/development/lwc-patterns.html' | relative_url }}">LWC Patterns</a>
  - <a href="{{ '/rag/mcp-knowledge/design-system-patterns.html' | relative_url }}">SLDS Design System Patterns</a>

## When to Use Lightning App Builder

### Use Lightning App Builder When

- You are composing **record pages** or **home pages**.
- You want **admin-maintainable** layouts with conditional visibility.
- You need to surface **custom LWCs** alongside standard components.

### Avoid Over-Complex Pages When

- Pages have too many components and become **slow**.
- There is no clear **information hierarchy** for users.

## Core Concepts

### Templates and Regions

- Use **three-column** or **header plus two-column** templates for most record pages.
- Keep critical information in the **top-left** or **highlight panel**.

### Dynamic Forms and Dynamic Related Lists

- Use **Dynamic Forms** for flexible field-level layout and visibility.
- Use **Dynamic Related Lists** to show different related records based on context (record type, status).

## Patterns and Examples

### Pattern 1: Persona-Based Pages

- Create **different record pages** per profile or app.
- Use **page assignments** to map personas to pages.

### Pattern 2: Progressive Disclosure

- Show only the **most important information** by default.
- Use tabs and accordions for **secondary details**.

## Edge Cases and Limitations

- Very complex pages with many components can impact **performance**, especially on older devices.
- Some managed packages provide components that **cannot be customized** easily; plan layout around them.

## Related Patterns

- <a href="{{ '/rag/quick-start/lwc-quick-start.html' | relative_url }}">LWC Quick Start Guide</a>
- <a href="{{ '/rag/mcp-knowledge/lwc-accessibility.html' | relative_url }}">LWC Accessibility Guidelines</a>

## Q&A

### Q: When should I use a custom LWC instead of standard components?

**A**: Use a custom LWC when the requirement involves **complex interactions**, **custom validation**, or **UI logic** that cannot be achieved with standard components and layouts. Keep layouts in App Builder, and encapsulate complex behavior in LWCs.

