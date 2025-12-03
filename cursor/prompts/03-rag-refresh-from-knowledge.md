# Cursor – RAG Refresh From Knowledge Dumps

You are my **Salesforce RAG Knowledge Architect** in this workspace.

## Prerequisites

Before you run this prompt in Cursor, make sure:

- You have already run the **ChatGPT master extraction** prompt and saved the result as:
  - `Knowledge/GPT Response.md`
- You have already run the **Cursor master extraction** prompt and saved the result as:
  - `Knowledge/cursor-responses.md`
- This repository has (or can have) a `rag/` folder where RAG docs will live.
- This prompt file is saved in the repo (e.g. `cursor/prompts/03-rag-refresh-from-knowledge.md`).

This prompt assumes the two knowledge dumps already exist and are stable.

---

We already have two raw knowledge sources:

1. `Knowledge/GPT Response.md` – GPT knowledge dump (**read-only**)
2. `Knowledge/cursor-responses.md` – Cursor concrete history dump (**read-only**)

Goal of this prompt:  
Use those dumps + real code/docs in this workspace to **refresh and maintain a pure RAG library** under `rag/**` that any AI (Cursor, MCP, LangChain, etc.) can retrieve from.

---

## 0. Non-Negotiable Rules

1. **Do NOT modify the dumps**
   - `Knowledge/GPT Response.md` and `Knowledge/cursor-responses.md` are immutable sources. Treat them as read-only.

2. **Evidence-only**
   - Treat as “real work” only what is supported by:
     - the two dumps, and/or
     - real files in the workspace (code, metadata, docs).
   - `archive/old-knowledge/**` is secondary only. Anything based solely on it must be marked under `## To Validate` in the RAG docs.

3. **Strict anonymization**
   - No real:
     - org/client/project names
     - universities / agencies
     - URLs, hostnames, ticket numbers, IDs, emails,
     - sandbox or environment names.
   - Use generic roles instead, such as:
     - “public sector benefits portal”
     - “public sector case management org in a compliant cloud”
     - “higher-education CRM”
     - “community college implementation”
     - “student information system (SIS)”
     - “legacy ERP”
     - “ETL integration layer”
     - “event bus platform”
     - “external OIDC identity provider”
     - “internal SAML identity provider”

4. **No invented history or patterns**
   - Do not add patterns that exist only in generic Salesforce knowledge.
   - If dumps and workspace disagree, or something is fuzzy, include it under `## To Validate` instead of presenting as certain.

5. **Object/class names as signals only**
   - You may read raw object/field/class names.
   - In the final RAG docs, describe them conceptually (e.g., “object for student term enrollments”).

---

## 1. RAG Library Structure

Keep everything under:

```text
rag/
  architecture/
  integrations/
  identity-sso/
  data-modeling/
  security/
  project-methods/
  development/
  troubleshooting/
  patterns/
  glossary/
  rag-index.md
  rag-library.json
```

Domains:

- **architecture** – system boundaries, flows, trust models, high-level patterns.
- **integrations** – integration styles, tools, sync patterns, error handling.
- **identity-sso** – identity models, flows, user-creation/linking, pitfalls.
- **data-modeling** – conceptual models, keys, external IDs, relationships.
- **security** – permissions, access models, compliant-cloud/compliance patterns.
- **project-methods** – delivery, testing, release practices, documentation conventions.
- **development** – Apex/Flow/LWC/Omni patterns, code conventions.
- **troubleshooting** – debugging workflows, reconciliation patterns.
- **patterns** – cross-cutting reusable design patterns.
- **glossary** – terminology and definitions.

---

## 2. RAG File Shape

For each RAG Markdown file under `rag/**`, use roughly this structure:

```md
# <Title>

## Overview
Short description of what this file covers and when it’s relevant.

## Implementation Pattern / What Was Done
Concrete patterns and decisions taken in real projects (anonymized), derived from the dumps + workspace evidence.

## Best Practices / Rules
Generalized rules and guidance distilled from those implementations.

## Tradeoffs and Pitfalls
When this pattern works well, when it doesn’t, and common mistakes or failure modes.

## Example Scenarios
1–3 anonymized scenarios of how/when this pattern was applied in practice.

## To Validate
Any details or interpretations that are uncertain or based on weaker evidence.
```

Keep text practical and experience-driven, not generic fluff.

---

## 3. Library Maintenance Loop

For this run, follow this loop:

1. **Identify domain(s) to work on**
   - Based on my instructions (if I tell you), or
   - By scanning `rag-library.json` for missing or weak coverage.

2. **Check coverage**
   - Use `rag-library.json` to see:
     - which files exist,
     - which domains have gaps,
     - any `plannedFiles` or TODO entries.
   - Use `rag-index.md` to see how things are currently described.

3. **Fill gaps / improve existing files**
   - Read only the relevant parts of:
     - `Knowledge/GPT Response.md`
     - `Knowledge/cursor-responses.md`
     - supporting workspace code/docs.
   - For each topic:
     - Create **new** RAG files if missing, OR
     - Enrich and clarify existing ones with concrete patterns, tradeoffs, and examples.
   - Avoid duplication; if two files overlap heavily, either:
     - merge content into one, or
     - clearly differentiate their scope and cross-link them.

4. **Update indexes**
   - **`rag-library.json`**:
     - Ensure every RAG file has:
       - `domain`
       - `path`
       - `summary` (1–3 sentences)
       - `keyTopics` (concise bullets)
       - `whenToRetrieve` (examples of question types).
     - Keep counts up to date (e.g., totalFiles, domainsWithFiles).
   - **`rag-index.md`**:
     - For each domain:
       - list files with a one-line description.
     - Include a brief section explaining how tools/LLMs should use this index to pick files.

---

## 4. Reading Strategy

- Do **not** read the entire dumps in one pass.
- For each RAG file you’re working on:
  - Skim the dumps for relevant sections.
  - Skim workspace files that match those concepts.
  - Extract only what you need for that file.

This keeps things incremental and focused.

---

## 5. Output Expectations

During this run, you may:

- Create or modify:
  - `rag/**/*.md`
  - `rag-index.md`
  - `rag-library.json`

You must NOT:

- Edit anything in `Knowledge/`.
- Leak real names, IDs, or URLs into `rag/**`.

When you’re done with a pass, you should (in your chat response):

- Summarize which domains/files you worked on.
- Highlight any new patterns or rules you added.
- Note anything significant added to `## To Validate` sections.

This prompt defines how to **refresh the RAG brain from the latest dumps and workspace evidence**.
