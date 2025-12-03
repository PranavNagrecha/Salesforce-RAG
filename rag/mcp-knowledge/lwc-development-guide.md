---
layout: default
title: LWC Development Guide - MCP Knowledge
description: Comprehensive guidance for Lightning Web Components (LWC) development, covering core principles, technical stack, best practices, and development workflows
permalink: /rag/mcp-knowledge/lwc-development-guide.html
level: Intermediate
tags:
  - mcp
  - lwc
  - development
  - workflows
last_reviewed: 2025-12-03
---

# LWC Development Guide - MCP Knowledge

> **Based on Real Implementation Experience**: This guide combines MCP guidance with field-proven project workflows.

## Overview

This guide provides:

- Core principles for LWC development
- Recommended project structure
- Development workflows (local dev, scratch orgs, packaging)
- Quality and testing standards

## Prerequisites

- **Required Knowledge**:
  - JavaScript (ES6+)
  - Salesforce DX basics
  - LWC fundamentals

- **Recommended Reading**:
  - <a href="{{ '/rag/development/lwc-patterns.html' | relative_url }}">LWC Patterns</a> - Architectural patterns
  - <a href="{{ '/rag/testing/lwc-jest-testing.html' | relative_url }}">LWC Jest Testing</a> - Testing patterns

## When to Use

### Use This When

- Setting up new LWC projects
- Standardizing team workflows
- Reviewing development practices

## Core Concepts

### Local Development and DX

- Use **Salesforce DX** and **VS Code**
- Use **scratch orgs** for isolated feature development

### Project Structure

- Group LWCs by **feature** or **domain**
- Use shared **services** and **utils** modules

### Quality Gates

- Enforce **ESLint/Prettier** for code style
- Require **Jest tests** for new components
- Run **Sa11y** tests for accessibility

## Patterns and Examples

### Pattern 1: Feature-Folder Structure

- Organize components by feature:
  - `force-app/main/default/lwc/opportunityConsole/...`
  - `force-app/main/default/lwc/studentIntakeForm/...`

### Pattern 2: Shared Utility Modules

- Create `shared/utils`, `shared/services` for cross-cutting logic
- Keep components lean and focused

## Edge Cases and Limitations

- Monolithic projects without clear structure are hard to maintain
- Lack of testing leads to regressions

## Related Patterns

- <a href="{{ '/rag/mcp-knowledge/lwc-best-practices.html' | relative_url }}">LWC Best Practices</a> - Coding best practices
- <a href="{{ '/rag/mcp-knowledge/lds-patterns.html' | relative_url }}">LDS Patterns</a> - Data access

## Q&A

### Q: How should I structure a large LWC project?

**A**: Use **feature-based folders** (by domain or feature) and shared `services`/`utils` modules. Avoid dumping all components into a single flat directory.

### Q: What quality gates should be enforced for LWCs?

**A**: At minimum: (1) **Linting** (ESLint/Prettier), (2) **Unit tests** (Jest), (3) **Accessibility checks** (Sa11y), and (4) **Code reviews** focusing on patterns from this guide.

