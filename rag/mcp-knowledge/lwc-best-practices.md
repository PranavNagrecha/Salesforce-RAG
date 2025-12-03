---
layout: default
title: LWC Best Practices - MCP Knowledge
description: Comprehensive best practices for Lightning Web Components development, focusing on event handling, property naming, decorator usage, and component structure
permalink: /rag/mcp-knowledge/lwc-best-practices.html
level: Intermediate
tags:
  - mcp
  - lwc
  - best-practices
last_reviewed: 2025-12-03
---

# LWC Best Practices - MCP Knowledge

> **Based on Real Implementation Experience**: These practices are aligned with official MCP guidance and production LWC architectures.

## Overview

This guide summarizes best practices for:

- Component structure and responsibility
- Decorator usage (`@api`, `@wire`)
- Event handling and communication
- State management and error handling

## Prerequisites

- **Required Knowledge**:
  - LWC component model
  - JavaScript classes and modules

- **Recommended Reading**:
  - <a href="{{ '/rag/development/lwc-patterns.html' | relative_url }}">LWC Patterns</a> - Higher-level patterns
  - <a href="{{ '/rag/mcp-knowledge/lwc-development-guide.html' | relative_url }}">LWC Development Guide</a> - Workflows and processes

## When to Use

### Use This When

- Designing new LWCs
- Reviewing existing LWC code
- Creating reusable component libraries

## Core Concepts

### Single Responsibility Components

- Each component should have **one primary responsibility**
- Use child components for reusable UI pieces

### Decorator Usage

- `@api`: Public properties and methods (stable contract)
- `@wire`: Reactive data and services

### Event Handling

- Use **CustomEvent** for parent-child communication
- Use **Lightning Message Service** for cross-hierarchy communication

## Patterns and Examples

### Pattern 1: Container-Presenter

- Container components handle **data fetching and orchestration**
- Presenter components handle **rendering and interaction**

### Pattern 2: Service Modules

- Extract logic into **plain JS service modules** (formatting, mapping)
- Keep components focused on UI concerns

## Edge Cases and Limitations

- Overusing `@track` (not needed in modern LWC)
- Mutating properties directly instead of reassigning

## Related Patterns

- <a href="{{ '/rag/mcp-knowledge/lds-patterns.html' | relative_url }}">LDS Patterns</a> - Data access best practices
- <a href="{{ '/rag/mcp-knowledge/lwc-accessibility.html' | relative_url }}">LWC Accessibility</a> - Accessibility best practices

## Q&A

### Q: How many responsibilities should a single LWC have?

**A**: Ideally **one primary responsibility**. If a component handles data fetching, complex logic, and complex UI, consider splitting it into container and presenter components for maintainability.

### Q: When should I use `@wire` vs imperative Apex?

**A**: Use `@wire` for **reactive data needs** (auto-refresh, record pages). Use imperative Apex for **user-triggered actions** (button clicks) or when you need more control over timing and error handling.

