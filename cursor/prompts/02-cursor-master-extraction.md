# Cursor – Salesforce Concrete History Extraction Prompt

You are my **Cursor Concrete History Extractor**.

## Prerequisites

Before you run this prompt in Cursor:

- Open the Salesforce knowledge repo as a **workspace** in Cursor.
- Ensure the workspace contains a `Knowledge/` folder (it can be empty for the first run).
- Make sure all of your relevant Salesforce code, metadata, and docs are part of this workspace
  (this prompt will scan the whole workspace, not just one project folder).
- Confirm that this prompt file itself is saved somewhere in the repo (e.g. `cursor/prompts/02-cursor-master-extraction.md`).

---

## Goal

Scan my real work in this Cursor workspace and produce a single, anonymized, article-style document:

> `Knowledge/cursor-responses.md`

that describes what I’ve actually built, based on code + docs, **not** on GPT text.  
This will later be combined with `Knowledge/GPT Response.md` and turned into a RAG library.

---

## 0. Hard Rules

1. **Evidence only**
   - Base statements on:
     - files in this workspace (code, metadata, markdown, specs, notes), and/or
     - any content I explicitly paste into this chat.
   - If something is only loosely implied, put it under `## To Validate` instead of asserting it as fact.

2. **Strong anonymization**
   - Do **not** output real:
     - company / client / agency names
     - universities / schools
     - internal project or app names
     - URLs / domains, ticket numbers, IDs, emails
   - Use generic roles, for example:
     - “public sector benefits portal on Salesforce”
     - “public sector case management org in a compliant cloud”
     - “higher-education CRM integrated with a student information system (SIS)”
     - “community college implementation”
     - “external OIDC identity provider”
     - “internal SAML identity provider”
     - “ETL integration layer”
     - “event bus platform”

3. **No raw identifiers in the final prose**
   - You MAY read:
     - object/field API names
     - Apex/LWC/Flow names
   - But in the output, describe them conceptually, for example:
     - “object for student term enrollments”
     - “batch job that syncs student records to a student information system”
     - “case-related object capturing outbound notices and related transactions”

4. **No invented history**
   - Do not invent projects or tools that are not supported by the workspace.
   - If you cannot clearly support something from files or explicit instructions, either omit it or mark under `## To Validate`.

---

## 1. Where to Look

Search across the full workspace:

- Salesforce project folders
- Integration configs (Boomi, MuleSoft, ETL, scripts)
- Docs (`*.md`, `*.txt`, specs, READMEs)
- Metadata exports, mapping docs, config files

You may glance at any existing knowledge files **only as hints**, but do not treat them as authoritative truth.

---

## 2. Output File & Structure

Create or overwrite:

> `Knowledge/cursor-responses.md`

with a Markdown document of this form:

```md
# Salesforce Work – Cursor Concrete History Dump

## 1. Major Project Contexts (From Workspace Evidence)

- Bullet each distinct context you can see from the files, e.g.:
  - “public sector benefits and case management org in a compliant cloud”
  - “higher-education CRM integrated with a student information system via an ETL tool”
  - “community college implementation using Salesforce Education Cloud and portals”
- For each context:
  - main Salesforce clouds/features
  - main external system roles (SIS, ERP, IdPs, ETL, event bus)
  - main categories of problems solved

## 2. Architecture Patterns (From Real Files)

- Event-driven vs batch vs API integrations
- Portal vs internal user separation
- Multi-system flows (CRM ↔ SIS ↔ ERP, etc.)
- Any compliant-cloud / security patterns visible

For each pattern:
- describe systems involved (generic roles)
- explain how data moves
- capture why this pattern seems to have been chosen (volume, latency, constraints).

## 3. Integrations Implemented

- For each clear integration pattern:
  - Source → Salesforce → Target (roles only, not names)
  - Real-time vs batch vs hybrid
  - Tools used (ETL platform, middleware, platform events, direct APIs)
  - Error handling, retries, idempotency, logging/monitoring patterns visible in code/config.

## 4. Identity & SSO

- Identity/SSO work visible in configs/docs:
  - external OIDC provider flows
  - internal SAML flows
  - portal vs internal user SSO
  - user-creation / linking strategies

## 5. Data Modeling

- Conceptual models from objects/fields:
  - student / program / enrollment / term
  - case / notice / transaction
  - account/contact/relationship models
  - external ID & key design for sync with SIS/ERP
- Focus on **relationships and roles**, not raw object names.

## 6. Security, Permissions, and Compliance

- Permission-set / sharing patterns you can infer.
- Portal vs internal access patterns.
- Logging/audit patterns connected to compliance.

## 7. Development & Delivery Practices

- Patterns in:
  - project layout / repos
  - Apex test usage
  - Flow/Omni/LWC design
  - CI/CD or deployment hints (if visible)
  - design-doc conventions (if present)

## 8. Troubleshooting & Operational Patterns

- How errors are logged, surfaced, and triaged.
- Any reconciliation / backfill patterns.
- Common operational flows (e.g., replaying events, running backfills, bulk corrections).

## 9. To Validate

- Bullets for anything:
  - partially supported,
  - inferred but not rock-solid,
  - or that might mix details from multiple projects.
- Briefly note which files or folders you used as evidence.
```

Write in concise, article-style prose. This file is the **Cursor brain dump** that will live next to `Knowledge/GPT Response.md`.
