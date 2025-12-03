---
layout: default
title: Salesforce Lightning Design System (SLDS) Patterns - MCP Knowledge
description: Comprehensive guidelines for using Salesforce Lightning Design System (SLDS) to design enterprise software, covering UX principles, visual design, component usage, interaction patterns, and accessibility
permalink: /rag/mcp-knowledge/design-system-patterns.html
level: Intermediate
tags:
  - mcp
  - slds
  - design
  - accessibility
last_reviewed: 2025-12-03
---

# Salesforce Lightning Design System (SLDS) Patterns - MCP Knowledge

> **Based on Real Implementation Experience**: These patterns align official SLDS guidance with real-world LWC and Experience Cloud implementations.

## Overview

Salesforce Lightning Design System (SLDS) provides **design tokens, component blueprints, and UX guidelines** for building consistent experiences across Salesforce. This document distills key patterns for:

- Choosing and composing SLDS components
- Applying design tokens and utility classes
- Designing responsive layouts
- Ensuring accessibility (WCAG 2)

## Prerequisites

- **Required Knowledge**:
  - Basic HTML/CSS concepts
  - LWC component structure
  - Familiarity with Lightning base components

- **Recommended Reading**:
  - <a href="{{ '/rag/mcp-knowledge/lwc-accessibility.html' | relative_url }}">LWC Accessibility</a> - Accessibility requirements
  - <a href="{{ '/rag/mcp-knowledge/lwc-best-practices.html' | relative_url }}">LWC Best Practices</a> - LWC coding patterns

## When to Use SLDS Patterns

### Use This When

- Building **custom LWCs** for internal users or portals
- Designing **record pages** or **app pages** with Lightning App Builder
- Creating **design systems** or reusable component libraries
- Ensuring **visual and interaction consistency** across teams

### Avoid This When

- Building **public sites** where branding completely replaces SLDS (but still use accessibility guidance)
- Prototyping throwaway UIs (can use simplified layouts, but still respect basic patterns)

## Core Concepts

### Component-First Design

- Prefer **Lightning base components** (`lightning-button`, `lightning-input`) over custom markup
- Extend base components with **small, focused wrappers** only when necessary

### Design Tokens and Utility Classes

- Use design tokens for **colors, spacing, typography** instead of hard-coded values
- Use **utility classes** (`slds-m-around_medium`, `slds-p-horizontal_small`) for layout and spacing

### Responsive Layouts

- Use SLDS **grid system** (`slds-grid`, `slds-col`) for responsive layouts
- Use **media queries** sparingly; rely on grid and utility classes when possible

## Patterns and Examples

### Pattern 1: Page Layout with Grid System

- **Intent**: Create responsive layouts using SLDS grid system
- **Structure**:
  - Use `slds-grid` for row-level layout
  - Use `slds-col` with size classes for columns
  - Use `slds-wrap` for wrapping on small screens

### Pattern 2: Form Layout with SLDS

- **Intent**: Create accessible forms using SLDS form patterns
- **Structure**:
  - Use `lightning-input`, `lightning-combobox` for inputs
  - Group fields using `slds-form-element`
  - Use `slds-form-element__label` and `slds-form-element__control`

## Edge Cases and Limitations

- Overusing custom CSS can break SLDS consistency
- Inconsistent use of tokens can cause theming issues
- Ignoring accessibility guidance can lead to compliance issues

## Related Patterns

- <a href="{{ '/rag/mcp-knowledge/lwc-accessibility.html' | relative_url }}">LWC Accessibility</a> - How SLDS supports accessibility
- <a href="{{ '/rag/development/lwc-patterns.html' | relative_url }}">LWC Patterns</a> - Component architecture

## Q&A

### Q: Why should I use SLDS instead of custom CSS frameworks?

**A**: SLDS ensures **visual consistency**, **accessibility**, and **maintainability** across Salesforce apps. It integrates tightly with Lightning base components and is supported by Salesforce UX updates, reducing design drift.

### Q: How do design tokens help with theming?

**A**: Design tokens abstract colors, spacing, and typography into **semantic values**. Changing a token updates all components that use it, enabling **consistent theming** without touching component code.

