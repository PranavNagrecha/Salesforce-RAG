---
layout: default
title: LWC Accessibility - MCP Knowledge
description: Comprehensive accessibility guidelines for Lightning Web Components, based on WCAG 2 and Salesforce MCP guidance
permalink: /rag/mcp-knowledge/lwc-accessibility.html
level: Intermediate
tags:
  - mcp
  - lwc
  - accessibility
  - wcag
last_reviewed: 2025-12-03
---

# LWC Accessibility - MCP Knowledge

> **Based on Real Implementation Experience**: These guidelines combine official MCP accessibility guidance with patterns from real LWC projects.

## Overview

Accessibility ensures **all users**, including those using assistive technologies, can use your LWCs. This document summarizes key patterns for:

- Keyboard navigation
- Screen reader support
- Color contrast
- Focus management

## Prerequisites

- **Required Knowledge**:
  - Basic HTML semantics
  - LWC template syntax
  - Understanding of ARIA attributes

- **Recommended Reading**:
  - <a href="{{ '/rag/mcp-knowledge/design-system-patterns.html' | relative_url }}">Design System Patterns</a> - SLDS accessibility support
  - <a href="{{ '/rag/testing/lwc-accessibility-testing.html' | relative_url }}">LWC Accessibility Testing</a> - Testing patterns

## When to Use

### Use This When

- Building **any** LWC for production
- Designing components used in **public portals** or **regulated industries**
- Implementing **forms**, **tables**, or **interactive controls**

### Avoid This When

- Never. Accessibility patterns should be applied to all production LWCs.

## Core Concepts

### Semantic HTML

- Use semantic elements (`<button>`, `<label>`, `<ul>`, `<li>`) instead of generic `<div>`s
- Use `lightning-*` base components where possible (they implement accessibility patterns)

### ARIA Usage

- Add ARIA attributes **only when semantics are insufficient**
- Use `aria-label`, `aria-labelledby`, `role` carefully and consistently

### Focus Management

- Manage focus on **dialog open/close**
- Ensure focus order follows **visual order**
- Avoid focus traps (user should always be able to exit components)

## Patterns and Examples

### Pattern 1: Accessible Form

- Use `lightning-input` with `label` attributes
- Avoid using placeholders as labels
- Group related fields with `<fieldset>` and `<legend>`

### Pattern 2: Keyboard-Accessible Components

- Implement keyboard handlers (`keydown`) for custom controls
- Support standard keys (Enter/Space for buttons, Arrow keys for lists)

## Edge Cases and Limitations

- Custom rendered HTML requires extra care for ARIA and focus
- Complex components may need dedicated accessibility reviews

## Related Patterns

- <a href="{{ '/rag/testing/lwc-accessibility-testing.html' | relative_url }}">LWC Accessibility Testing</a> - Automated and manual testing
- <a href="{{ '/rag/troubleshooting/lwc-accessibility-errors.html' | relative_url }}">LWC Accessibility Errors</a> - Common issues and fixes

## Q&A

### Q: Do I still need ARIA if I use Lightning base components?

**A**: Lightning base components implement most ARIA and keyboard patterns for you. You generally **don't** need to add ARIA to them, but you still need to ensure **correct labels and structure** around them.

### Q: How do I test LWC accessibility?

**A**: Use a combination of: (1) **Automated tests** (Sa11y, Jest with axe), (2) **Keyboard testing** (tab through UI), (3) **Screen readers** (NVDA, VoiceOver), and (4) **Color contrast tools**. See `lwc-accessibility-testing.md` for detailed patterns.

