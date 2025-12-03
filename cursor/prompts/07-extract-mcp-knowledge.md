# Cursor – Extract Salesforce MCP Knowledge to RAG

You are my **MCP Knowledge Extractor** for this workspace.

## Prerequisites

Before you run this prompt in Cursor, make sure:

- You have access to Salesforce MCP tools
- The `rag/mcp-knowledge/` directory exists
- You understand the RAG file structure and format

---

## Goal

Extract knowledge from Salesforce MCP Service tools and format it as static RAG files that complement the existing pattern library.

---

## 0. Scope (Files You MAY Create/Edit)

You may:
- **Create new files** under `rag/mcp-knowledge/`
- **Update** `rag/rag-index.md` to include MCP knowledge section
- **Update** `rag/rag-library.json` to include MCP knowledge files

You must NOT:
- Modify existing pattern files (only create new MCP knowledge files)
- Modify `Knowledge/**` source dumps
- Remove existing content

---

## 1. MCP Tools to Extract From

Extract knowledge from these Salesforce MCP tools:

1. **LWC Development**: `mcp_salesforce_guide_lwc_development`
2. **LWC Best Practices**: `mcp_salesforce_guide_lwc_best_practices`
3. **LWC Accessibility**: `mcp_salesforce_guide_lwc_accessibility`
4. **LWC Security**: `mcp_salesforce_guide_lwc_security`
5. **LDS Development**: `mcp_salesforce_guide_lds_development`
6. **LDS Data Consistency**: `mcp_salesforce_guide_lds_data_consistency`
7. **LDS Referential Integrity**: `mcp_salesforce_guide_lds_referential_integrity`
8. **LDS GraphQL**: `mcp_salesforce_guide_lds_graphql`
9. **Design General**: `mcp_salesforce_guide_design_general`
10. **Mobile LWC Offline**: `mcp_salesforce_get_mobile_lwc_offline_guidance`

---

## 2. File Structure for MCP Knowledge Files

Each MCP knowledge file follows this structure:

```markdown
# [Topic] - MCP Knowledge

> This file contains knowledge extracted from Salesforce MCP Service tools.  
> It complements the lived-experience patterns in `rag/development/` and `rag/patterns/`.

## Overview

[Summary of what this MCP tool provides]

**Source**: Salesforce MCP Service - [Tool Name]

## Key Patterns and Practices

[Extracted patterns and practices from MCP]

### Pattern 1: [Name]
[Description]
[Code examples if available]

### Pattern 2: [Name]
[Description]
[Code examples if available]

## Best Practices

[Best practices from MCP]

## Code Examples

[Code examples from MCP, if available]

## Integration with Existing RAG

**Related Patterns**:
- [Link to related pattern files in rag/development/]
- [Link to related pattern files in rag/patterns/]

**How This Complements Existing RAG**:
- [How MCP knowledge adds to or validates existing patterns]
- [Gaps this fills]

## Additional Resources

[Any additional resources or references from MCP]
```

---

## 3. Files to Create

Create these files in `rag/mcp-knowledge/`:

1. **lwc-development-guide.md**
   - Extract from: `mcp_salesforce_guide_lwc_development`
   - Focus: LWC development patterns, component structure, lifecycle

2. **lwc-best-practices.md**
   - Extract from: `mcp_salesforce_guide_lwc_best_practices`
   - Focus: Best practices for LWC development

3. **lwc-accessibility.md**
   - Extract from: `mcp_salesforce_guide_lwc_accessibility`
   - Focus: Accessibility patterns and requirements

4. **lwc-security.md**
   - Extract from: `mcp_salesforce_guide_lwc_security`
   - Focus: Security patterns for LWC

5. **lds-patterns.md**
   - Extract from: `mcp_salesforce_guide_lds_development`, `mcp_salesforce_guide_lds_data_consistency`, `mcp_salesforce_guide_lds_referential_integrity`
   - Focus: Lightning Data Service patterns

6. **lds-graphql-patterns.md**
   - Extract from: `mcp_salesforce_guide_lds_graphql`
   - Focus: GraphQL patterns for LDS

7. **design-system-patterns.md**
   - Extract from: `mcp_salesforce_guide_design_general`
   - Focus: Salesforce Lightning Design System patterns

8. **mobile-lwc-patterns.md**
   - Extract from: `mcp_salesforce_get_mobile_lwc_offline_guidance`
   - Focus: Mobile LWC and offline patterns

---

## 4. Extraction Process

For each MCP tool:

1. **Call the MCP tool** to get guidance
2. **Extract key information**:
   - Patterns and practices
   - Code examples
   - Best practices
   - Common pitfalls
3. **Format as markdown** following the structure above
4. **Link to existing RAG patterns** where relevant
5. **Sanitize** (remove any identifying information)
6. **Save** to appropriate file in `rag/mcp-knowledge/`

---

## 5. Integration with Existing RAG

### Link MCP Knowledge to Patterns

In each MCP knowledge file, add a section:

```markdown
## Integration with Existing RAG

**Related Patterns**:
- [LWC Patterns](rag/development/lwc-patterns.md) - Complements with MCP-validated practices
- [Apex Patterns](rag/development/apex-patterns.md) - Related backend patterns
- [Security Patterns](rag/security/) - Security considerations

**How This Complements Existing RAG**:
- [Explain how MCP knowledge validates or adds to existing patterns]
- [Note any gaps this fills]
- [Note any differences or additional perspectives]
```

### Update Existing Pattern Files (Optional)

You may add references to MCP knowledge in existing pattern files:

```markdown
## Related MCP Knowledge

See also:
- [LWC Development Guide - MCP](rag/mcp-knowledge/lwc-development-guide.md)
- [LWC Best Practices - MCP](rag/mcp-knowledge/lwc-best-practices.md)
```

---

## 6. Quality Standards

Each MCP knowledge file must:

- ✅ **Be sanitized**: No identifying information
- ✅ **Be structured**: Follow the template above
- ✅ **Link to patterns**: Reference related RAG patterns
- ✅ **Be complete**: Include all key information from MCP
- ✅ **Be readable**: Clear formatting and organization
- ✅ **Include examples**: Code examples when available from MCP

---

## 7. What To Do On Each Run

When this prompt is used:

1. **Select MCP tools to extract** (start with 2-3 tools per run)
2. **Call MCP tools** to get guidance
3. **Extract and format** information as markdown
4. **Create/update** MCP knowledge files
5. **Link to existing patterns** in RAG
6. **Update metadata** (rag-index.md, rag-library.json)
7. **Report back** which files were created/updated

---

## 8. What To Report Back

In your chat response (not in files), list:

- MCP tools called
- Files created/updated
- Key patterns extracted
- Links to existing RAG patterns
- Any gaps or areas needing more detail

Do NOT paste full file contents; I will inspect files directly.

