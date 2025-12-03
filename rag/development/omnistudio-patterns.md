---
layout: default
title: OmniStudio Patterns
description: Patterns for designing OmniScripts and FlexCards for guided, multi-step business processes
permalink: /rag/development/omnistudio-patterns.html
level: Intermediate
tags:
  - omnistudio
  - ui
last_reviewed: 2025-12-03
---

# OmniStudio Patterns

> **Based on Real Implementation Experience**: These patterns come from public sector and education implementations using OmniStudio for complex intake and case processes.

## Overview

OmniStudio provides:

- **OmniScripts** for guided, multi-step workflows.
- **FlexCards** for configurable UI cards that surface data from multiple sources.

This document focuses on **when to choose OmniStudio vs LWC or Flow**, and on structural patterns for maintainable OmniScripts and FlexCards.

## Prerequisites

- **Required Knowledge**:
  - Basic Lightning Experience navigation.
  - Understanding of the **underlying data model** used in the process.

- **Recommended Reading**:
  - <a href="{{ '/rag/development/flow-patterns.html' | relative_url }}">Flow Patterns</a>
  - <a href="{{ '/rag/development/lwc-patterns.html' | relative_url }}">LWC Patterns</a>

## When to Use OmniStudio

### Use OmniStudio When

- You need **highly guided** user journeys with multiple steps and branching.
- Requirements are **heavily configuration-driven** and likely to change frequently.
- You are integrating data from **multiple systems** in a single UI.

### Prefer LWC or Flow When

- You need **lightweight components** embedded in record pages.
- Logic is primarily **record-triggered** and back-end oriented.
- You require **fine-grained control** over UX and performance beyond OmniStudio’s abstraction.

## Core Concepts

### OmniScript Design

- Break complex scripts into **modular sub-scripts** where possible.
- Use **DataRaptors and Integration Procedures** to abstract data access and transformations.

### FlexCard Design

- Keep FlexCards **focused** (single purpose per card).
- Avoid overloading cards with too many states or actions.

## Patterns and Examples

### Pattern 1: Guided Intake OmniScript

- Multi-step form capturing data across several related objects.
- Uses **DataRaptors** to prefill and save data.
- Includes **draft-save** and **resume later** when supported.

### Pattern 2: Summary FlexCard

- Combines data from **multiple related records**.
- Provides **quick actions** (launch OmniScript, open record, start Flow).

## Edge Cases and Limitations

- OmniStudio components can have **heavier page load** than simple LWCs.
- Some advanced behaviors may still require **custom LWCs** embedded inside OmniStudio.

## Related Patterns

- <a href="{{ '/rag/integrations/integration-platform-patterns.html' | relative_url }}">Integration Platform Patterns</a>

## Q&A

### Q: When should I embed a Flow or LWC inside OmniStudio?

**A**: Embed when you need capabilities not easily modeled in OmniStudio alone (e.g., complex custom validation, performance-optimized UI). Keep OmniStudio responsible for **orchestration**, while LWC/Flow handle **specialized tasks**.

