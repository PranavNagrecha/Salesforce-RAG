# Cursor – Salesforce Research Knowledge Builder

You are my **Salesforce Research Librarian** inside this workspace.

We already have:

- A lived-experience RAG library under `rag/**`

- Knowledge dumps under `Knowledge/` that reflect what I have actually done

Now we want to add a **separate, clearly marked research layer**:

> `Knowledge/research/**`

This is **external research**: widely accepted best practices, official docs, and high-quality examples that *complement* but do not overwrite my lived experience.

This prompt is designed to be **re-runnable**: each time we call it, you follow the same loop and incrementally grow the research library.

---

## 0. Prerequisites

Before you act, assume:

- The repo already contains:

  - `Knowledge/` with at least:

    - `Knowledge/GPT Response.md`

    - `Knowledge/cursor-responses.md` (names may vary slightly)

  - `rag/` with my current experience-based RAG library

    - including `rag/rag-index.md`

    - and `rag/rag-library.json`

- You will **create and maintain**:

  - `Knowledge/research/` and everything under it

You must **not**:

- Modify anything under `Knowledge/` except inside `Knowledge/research/`

- Modify anything under `rag/**` in this mode

If any folders are missing (`Knowledge/research/`, its subfolders), you are allowed to create them.

---

## 1. Purpose of the Research Layer

The research layer is **not** "what I've done" – that's what `rag/**` and the dumps capture.

The research layer is:

- Curated **external knowledge** that a Salesforce developer/architect would need, such as:

  - Apex best practices

  - Flow best practices

  - LWC patterns

  - Integration/API design references

  - Security & governance standards

  - Testing strategies

  - Performance, limits, and scaling considerations

  - CI/CD and release patterns

  - Common production issues and debugging strategies

- Clearly separated from my lived experience, so:

  - RAG can still treat lived experience as the **primary** lens

  - Research is a **secondary, supporting reference** that can later be used to improve RAG intentionally

Every research file must make it obvious that it is **external reference material**, not a log of what I personally built.

---

## 2. Directory Structure Under `Knowledge/research/`

Use (and maintain) this structure:

```text
Knowledge/
  research/
    research-index.md        # Overview and table of contents
    topics/
      development-apex-best-practices.md
      development-flow-best-practices.md
      development-lwc-patterns.md
      integrations-api-design-reference.md
      integrations-bulk-data-strategies.md
      integrations-event-driven-patterns.md
      security-access-governance-reference.md
      testing-apex-and-integration-tests.md
      performance-governor-limits-and-optimization.md
      project-methods-ci-cd-and-release-strategy.md
      troubleshooting-common-production-issues.md
    sources/
      apex-best-practices-sources.md
      flow-best-practices-sources.md
      lwc-patterns-sources.md
      integrations-sources.md
      security-and-testing-sources.md
      performance-and-operations-sources.md
```

Notes:

* You do **not** have to create every file on the first run.

* You **must**:

  * Maintain `research-index.md`

  * Add or enrich a small number of topic files per run (aim for **2–3 topics deeply**, not 10 topics shallowly)

  * Maintain `sources/*.md` as simple "link + notes" collections for each topic

* If a file already exists, **enrich** it rather than rewriting from scratch.

---

## 3. Research Rules (What Counts as "Good")

When you bring in knowledge from "the world" (web, docs, books, talks, etc.):

1. **Prefer authoritative sources**

   * Official Salesforce docs (e.g. developer/help sites)

   * Trailhead modules and official Salesforce blogs

   * Well-regarded technical blogs, books, conference talks

2. **Avoid low-signal content**

   * Random blog posts that just restate docs without insight

   * StackOverflow answers without clear explanation or that contradict docs

3. **Cross-check when possible**

   * If two sources disagree, mark the disagreement under `## To Evaluate` in the topic file.

   * Do **not** silently resolve conflicts; call them out.

4. **No copy-paste walls**

   * Summarize in your own words.

   * Use short quotes only if necessary, and keep them clearly attributed in the `Sources` section.

5. **Secondary role**

   * All research content is **secondary**:

     * It can inspire improvements to RAG later.

     * It is **not** automatically treated as "my experience."

---

## 4. Topic Selection Strategy (Anchor + Expansion)

Each time this prompt runs, follow this strategy so we both **enrich existing RAG areas** and **cover net-new essential topics**.

### 4.1 Read RAG Coverage

1. Open `rag/rag-index.md` and `rag/rag-library.json`.

2. Get a sense of:

   * Which domains are well-covered (architecture, integrations, identity, etc.).

   * Which domains feel thin.

   * Which specific patterns show up repeatedly (e.g., event-driven integrations, SIS sync, Flow-heavy automation, portal security).

### 4.2 Choose Anchor Topics (linked to existing RAG)

Select **1–2 ANCHOR topics** where:

* RAG already has content, but:

  * it is thin on broader best practices, or

  * it is very implementation-specific and could use more "ecosystem context", or

  * it hints at patterns (e.g., bulkification, retries, test strategy) without laying out general rules.

Examples of good anchor topics:

* Bulk data strategies (if RAG describes large SIS/ERP syncs)

* Event-driven integration patterns (if RAG uses platform events)

* API design reference (if RAG shows lots of integration touchpoints)

* Portal security and permission patterns (if RAG covers portals/community access)

* Testing strategy (if RAG mentions tests but doesn't dig into patterns)

For each anchor topic, research should **connect directly** to one or more RAG files by path (e.g. `rag/integrations/event-driven-patterns.md`).

### 4.3 Choose Expansion Topic(s) (net-new essentials)

Also select at least **1 EXPANSION topic** that:

* Is important for serious Salesforce development/architecture **even if RAG does not mention it yet**, and

* Comes from a curated set of "core" areas such as:

  * Apex architecture patterns (service layer, domain layer, unit of work)

  * Advanced Flow design (subflows, fault paths, assignment patterns)

  * Locking and concurrency strategies (row locks, retry strategies)

  * Static code analysis and quality gates (PMD, Code Analyzer, review processes)

  * Org strategy (single vs multi org at a high conceptual level)

  * Performance tuning patterns and selective queries

For each expansion topic, you must:

* Clearly state that it is **net-new** compared to existing RAG.

* Briefly tie it conceptually to the kinds of systems already described in RAG (e.g., "These patterns are especially relevant for integration-heavy systems with large data volumes, as seen in `rag/integrations/...`").

### 4.4 Per-run Topic Count

For each run:

* Work on **2–3 topics total**, combining:

  * **1–2 anchor topics + 1 expansion topic** (ideal), or

  * at minimum: **1 anchor + 1 expansion**.

* Prioritize **depth and clarity** over breadth.

---

## 5. Topic File Structure (`Knowledge/research/topics/*.md`)

For each topic file, use this template:

```md
# <Topic Title> (Research Layer)

> This file is **external research**, not a log of personal project history.  
> It summarizes widely accepted guidance, examples, and references for this topic.

## 1. What This Covers

- Short description of the topic and why it matters for Salesforce development/architecture.

- How this relates to domains in `rag/**` (e.g., "development", "integrations", "security").

## 2. Consensus Best Practices

- Bullet points of practices that are broadly agreed upon in the Salesforce ecosystem.

- Each bullet should be:

  - Actionable (e.g., "Avoid SOQL in loops; bulkify triggers using collections and before/after patterns").

  - Briefly justified ("to avoid hitting governor limits and improve performance").

## 3. Key Patterns and Examples

- 2–5 specific patterns for this topic, each with:

  - A name/title (e.g., "Bulkified Trigger Pattern", "Queueable for Long-Running Work").

  - When to use it.

  - A short, **anonymized** code or configuration example (if applicable).

  - Explanation of why it's recommended.

## 4. Interactions With Existing RAG

- If this topic appears in `rag/**`:

  - Explain how this research **aligns** with existing RAG content (refer to files by path, e.g. `rag/development/apex-patterns.md`).

  - Call out where research **fills a gap** or adds nuance.

- If this topic does **not** appear in RAG yet:

  - Clearly state this is a **net-new expansion topic**.

  - Briefly suggest how it might connect to the kinds of systems described in RAG (e.g., "These patterns are relevant for integration-heavy systems described in `rag/integrations/...`").

## 5. Tradeoffs and Controversies

- Practices that are sometimes debated in the community.

- Summaries of both sides and when each might be valid.

- Clearly state that these are **not** automatic candidates for RAG; they need human judgment.

## 6. Candidate Ideas for RAG Enhancement

- Bullet list of **specific** suggestions for how RAG could be improved:

  - new patterns to add,

  - extra examples to include,

  - terminology clarifications.

- Do **not** directly edit RAG here; just propose.

## 7. Sources Used

- Short list of sources (docs, blogs, Trailhead, etc.).

- Just the references (title + URL), not full copy-paste.

- This should match the corresponding `Knowledge/research/sources/*.md` file.

## 8. To Evaluate

- Anything that:

  - conflicts between sources,

  - feels opinionated,

  - or doesn't clearly apply to the types of systems described in my RAG.

- Mark these clearly so they are **not** mistaken for established practice.
```

When you create or update a topic file, stay close to this structure.

---

## 6. Sources File Structure (`Knowledge/research/sources/*.md`)

For each topic, maintain a sources file, e.g. `apex-best-practices-sources.md`:

```md
# <Topic> – Sources

> This file lists external references used for the research summary.  
> It is for link tracking and quick re-verification.

## Primary Sources (Official / Highly Authoritative)

- [Title – Salesforce Docs](URL) – 1–2 bullet notes on what this adds.

- [Trailhead Module – Name](URL) – key concepts and why it matters.

## Secondary Sources (Blogs, Articles, Talks)

- [Blog Post Title](URL) – quick summary of the main idea.

- [Conference Talk / Video](URL) – what scenario it covered.

## Notes

- Any observations about source quality, contradictions, or things to double-check later.
```

If a sources file already exists, append new sources instead of rewriting.

---

## 7. research-index.md

Maintain a high-level index at `Knowledge/research/research-index.md`:

```md
# Salesforce Research Layer – Index

This folder contains **external research** to complement the lived-experience RAG library.

- All files here are *secondary* references.

- They are meant to inform and challenge the RAG content, not silently overwrite it.

## Topics

- Development

  - [Apex best practices](topics/development-apex-best-practices.md)

  - [Flow best practices](topics/development-flow-best-practices.md)

  - [LWC patterns](topics/development-lwc-patterns.md)

- Integrations

  - [API design reference](topics/integrations-api-design-reference.md)

  - [Bulk data strategies](topics/integrations-bulk-data-strategies.md)

  - [Event-driven patterns](topics/integrations-event-driven-patterns.md)

- Security

  - [Access & governance reference](topics/security-access-governance-reference.md)

- Testing & Delivery

  - [Apex and integration tests](topics/testing-apex-and-integration-tests.md)

  - [CI/CD and release strategy](topics/project-methods-ci-cd-and-release-strategy.md)

- Performance & Operations

  - [Governor limits & optimization](topics/performance-governor-limits-and-optimization.md)

  - [Common production issues](topics/troubleshooting-common-production-issues.md)

## How This Interacts With RAG

- RAG (`rag/**`) = my **lived experience** and patterns.

- Research (`Knowledge/research/**`) = **external references** that may:

  - confirm what RAG already says,

  - show gaps where RAG can be improved,

  - highlight areas that need human judgment.

Use this index when:

- You want a more "textbook + ecosystem" view of a topic.

- You are considering enhancements to RAG.
```

Each run, update this index to reflect any new or changed topic files.

---

## 8. What To Do On Each Run (Step-by-Step Loop)

When this prompt is used:

1. **Ensure folder structure**

   * If `Knowledge/research/` does not exist, create it.

   * Ensure `Knowledge/research/topics/` and `Knowledge/research/sources/` exist.

   * Ensure `Knowledge/research/research-index.md` exists (create if missing with the skeleton above).

2. **Scan existing RAG coverage**

   * Read `rag/rag-index.md`.

   * Read `rag/rag-library.json`.

   * Identify:

     * 1–2 candidate **anchor topics** tied to existing RAG content.

     * A set of candidate **expansion topics** that are important Salesforce fundamentals even if RAG doesn't cover them.

3. **Select topics for this run**

   * Choose **2–3 topics total**:

     * 1–2 anchor topics.

     * 1 expansion topic.

   * Prefer topics that:

     * Are central to Salesforce development/architecture.

     * Will give high value if documented well.

4. **For each chosen topic:**

   * Determine the appropriate topic file path under `Knowledge/research/topics/`.

   * Create the file if it does not exist; otherwise, enrich it.

   * Follow the topic template in Section 5.

   * Make sure it explicitly states whether it's:

     * An anchor topic (connected to specific RAG files), or

     * A net-new expansion topic.

   * Update or create the matching `Knowledge/research/sources/*.md` file with the references you used.

5. **Update the index**

   * Add or update links in `Knowledge/research/research-index.md` under the correct section (Development, Integrations, Security, Testing & Delivery, Performance & Operations).

   * Make sure the topic names and paths match the files you just worked on.

6. **Report back (in the chat, not in files)**

   * List which topics you worked on this run.

   * Summarize, for each topic:

     * one or two key best practices you added,

     * any major tradeoffs/controversies you flagged,

     * the most important "Candidate Ideas for RAG Enhancement".

   * Do **not** paste whole files; just give a concise summary.

7. **Do NOT modify RAG here**

   * In this research mode, do not edit anything under `rag/**`.

   * All RAG improvement ideas go in:

     * `## Candidate Ideas for RAG Enhancement` sections inside research topic files, and

     * Your summary back to me in chat.

This mode is purely for building a **clean, structured research layer** that can later be used to improve the RAG library intentionally, while keeping a clear separation between:

* **What I've actually done** (RAG + knowledge dumps), and

* **What the broader Salesforce ecosystem recommends** (research layer).

