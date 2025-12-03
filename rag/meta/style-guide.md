---
layout: default
title: RAG Knowledge Style Guide
description: Standards for structure, voice, formatting, and metadata across the Salesforce RAG knowledge library
permalink: /rag/meta/style-guide.html
---

# RAG Knowledge Style Guide

## Purpose

This document defines the **canonical structure and style** for all knowledge, pattern, and code-example files in the RAG library. New content should follow this guide by default.

## Frontmatter Standard

All content files **must** start with YAML frontmatter:

```yaml
---
layout: default
title: Human-readable Title
description: One-sentence summary in plain English
permalink: /rag/<folder>/<file>.html
level: Beginner | Intermediate | Advanced
tags:
  - primary-domain
  - secondary-domain
last_reviewed: 2025-01-01
---
```

- **layout**: Always `default`.
- **title**: Clear, descriptive, user-facing title.
- **description**: One sentence, present tense, declarative.
- **permalink**: `/rag/<folder>/<filename>.html`.
- **level**: Overall difficulty.
- **tags**: Lowercase, kebab-case domain tags (e.g., `apex`, `flow`, `lwc`, `integration`, `security`).
- **last_reviewed**: Date in `YYYY-MM-DD` format when content was last validated.

## Standard Section Order (Knowledge / Pattern Files)

All non-index knowledge and pattern files should use this section order:

1. `# Title` (matches frontmatter `title`)
2. `> **Based on Real Implementation Experience**` (optional but recommended)
3. `## Overview`
4. `## Prerequisites`
5. `## When to Use`
6. `## Core Concepts`
7. `## Patterns and Examples` (or domain-appropriate main section)
8. `## Edge Cases and Limitations`
9. `## Related Patterns`
10. `## Q&A`

### Overview

- 1–3 short paragraphs.
- Explain **what** this topic is and **why it matters**.

### Prerequisites

Use bullets grouped as:

- **Required Knowledge**:
  - Short bullets
- **Recommended Reading**:
  - `<a href="{{ '/rag/...' | relative_url }}">Title</a> - short reason`

### When to Use

Clearly distinguish **when to choose this pattern/approach** vs. alternatives. Use:

- `### Use This When`
- `### Avoid This When`

### Core Concepts

Define key ideas and vocabulary. Prefer:

- Short subsections with `###` headings.
- Concise paragraphs and bullets.

### Patterns and Examples

Organize by:

- `### Pattern Name`
- **Intent**: One sentence.
- **Structure**: Short description or pseudo-flow.
- **Example**: Inline explanation, with code samples referencing code-example files when appropriate.

### Edge Cases and Limitations

Explicitly list:

- Platform limits.
- Gotchas from real projects.
- Scenarios where this pattern fails or needs adjustment.

### Related Patterns

Use a consistent bullet style:

- `- <a href="{{ '/rag/path/file.html' | relative_url }}">File Title</a> - short relation note`

Ensure **bidirectional links** where it makes sense.

### Q&A

Use the standard format:

```markdown
## Q&A

### Q: Question?

**A**: Clear, direct answer in 2–5 sentences, using bold for key terms and patterns.
```

Target **8–10 questions** for primary pattern files, **5–8** for smaller topics.

## Code Example Files Structure

Code-example files should follow this order:

1. Frontmatter (as above, with `tags` including `code-examples` and language)
2. `# Title`
3. `## Overview`
4. `## When to Use`
5. `## Example 1: Name`
6. `## Example 2: Name` (etc.)
7. `## Testing Considerations`
8. `## Related Patterns`

Within each example:

- Start with **Use Case** paragraph.
- Provide a **full code block** with comments.
- Reference any required test classes or setup.

## Voice and Tone

- Prefer **third-person, declarative** voice:
  - “Use Flow when …”
  - “Apex is used when …”
- Avoid casual language; be **direct and instructional**.
- Use **bold** for key ideas and pattern names, not for entire paragraphs.

## Terminology

- Use a central terminology mapping (to be defined in `terminology-mapping.md`).
- Be consistent with:
  - “Record-Triggered Flow” (not “RTF” unless already defined).
  - “Integration user” vs. “API-only user”.
  - “Experience Cloud” instead of “Community Cloud”.

## Formatting Rules

- Max line width: ~120 characters where practical.
- Use `##` for major sections, `###` for subsections.
- Use `- ` for bullets, never numbered lists for unordered items.
- Use inline code backticks for:
  - Apex types and keywords (e.g., `Queueable`, `Database.Batchable`).
  - SOQL snippets (short ones).


