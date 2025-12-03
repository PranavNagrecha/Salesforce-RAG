---
layout: default
title: Mobile Strategy Patterns
description: Patterns for designing Salesforce mobile strategies, including Salesforce mobile app, mobile-optimized LWCs, and offline considerations
permalink: /rag/architecture/mobile-strategy.html
level: Intermediate
tags:
  - architecture
  - mobile
  - lwc
  - offline
last_reviewed: 2025-12-03
---

# Mobile Strategy Patterns

> **Based on Real Implementation Experience**: These patterns come from projects delivering mobile solutions for field teams, advisors, and case workers.

## Overview

Mobile strategy for Salesforce includes:

- Using the **Salesforce mobile app** effectively
- Designing **mobile-optimized LWCs**
- Considering **offline access** and sync
- Aligning with **MCP mobile guidance**

## Prerequisites

- **Required Knowledge**:
  - LWC basics
  - Salesforce mobile app capabilities

- **Recommended Reading**:
  - <a href="{{ '/rag/mcp-knowledge/lwc-development-guide.html' | relative_url }}">LWC Development Guide</a> - Mobile LWC patterns
  - <a href="{{ '/rag/mcp-knowledge/lwc-best-practices.html' | relative_url }}">LWC Best Practices</a>

## When to Use

### Use This When

- Planning **mobile-first** solutions
- Supporting **field workers** or **advisors** on the go
- Evaluating **offline requirements**

## Core Concepts

### Mobile-Friendly Design

- Design for **small screens** first
- Use **responsive layouts** and **SLDS grid**
- Minimize required input where possible

### Offline Considerations

- Identify operations that **must work offline**
- Use **mobile caching patterns** where supported

## Patterns and Examples

### Pattern 1: Mobile-First LWC

- Prioritize content for small screens
- Use `slds-show_small` / `slds-hide_small` utilities

### Pattern 2: Task-Focused Pages

- Create task-focused mobile pages for key workflows
- Avoid overloading mobile layouts with desktop content

## Edge Cases and Limitations

- Not all desktop features are mobile-friendly
- Offline capabilities are limited and require careful design

## Related Patterns

- <a href="{{ '/rag/development/lwc-patterns.html' | relative_url }}">LWC Patterns</a> - Component design
- <a href="{{ '/rag/mcp-knowledge/lwc-development-guide.html' | relative_url }}">LWC Development Guide</a> - Mobile-specific guidance

## Q&A

### Q: When should I build mobile-specific LWCs?

**A**: Build mobile-specific LWCs when the **mobile workflow is significantly different** from desktop, or when you need **highly optimized mobile UX** that can't be achieved with simple responsive tweaks.

### Q: How do I design for offline use?

**A**: Start by identifying **which operations must work offline**, minimize data dependencies, and design flows that can **queue work** and **sync when online**. Follow MCP mobile guidance for supported offline patterns.

