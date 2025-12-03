# Cursor Knowledge Base Workflow

## What Was Actually Done

A comprehensive knowledge base extraction and compilation workflow was established using Cursor AI to transform raw project knowledge into a structured, domain-organized knowledge repository. The workflow uses multiple prompt files and follows a strict "real work only" philosophy.

### Knowledge Base Structure Created

A domain-structured knowledge base was created under `knowledge/` with the following organization:

- **architecture/**: Salesforce architecture patterns, event-driven architecture, government cloud patterns
- **integrations/**: Integration overview, Boomi patterns, MuleSoft patterns, Platform Events, ETL strategies
- **identity-sso/**: Identity architecture, OIDC/SAML flows, hybrid identity models
- **data-modeling/**: Data modeling overview, Education Cloud modeling, public sector case modeling, external IDs
- **security/**: Security overview, government cloud compliance, logging and monitoring
- **project-methods/**: Delivery approach, testing strategies, release and deployment practices
- **templates/**: (Placeholder for future template files)
- **misc/**: Flow patterns, Apex patterns, LWC patterns, SOQL debugging, OmniStudio, implementation conventions, Cursor workflow

### Prompt Files Created

Two main prompt files were created to guide knowledge extraction:

1. **`cursor/prompts/master-extraction-prompt.md`**: Original comprehensive extraction prompt with domain model, content structure, and extraction workflow
2. **`cursor/prompts/compile-real-knowledge.md`**: Refined prompt emphasizing "real work only" - searches workspace files and ChatGPT dump for evidence

### Extraction Process

The knowledge base was built through a multi-phase process:

1. **Initial Extraction**: Created 22 knowledge files from ChatGPT export covering all major domains
2. **Enhancement Phase**: Added 6 additional files in `misc/` for Flow, Apex, LWC, SOQL, OmniStudio, and implementation conventions
3. **Workspace Integration**: Enhanced existing files with additional patterns found in workspace
4. **Documentation**: Created extraction logs and addition summaries to track all changes

### Content Structure Standard

All knowledge files follow a consistent structure:

```md
# <Title>

## What Was Actually Done
- Concrete descriptions of real implementations
- Based on ChatGPT dump and/or workspace files

## Rules and Patterns
- Generalized rules derived from real experiences

## Suggested Improvements (From AI)
- AI-suggested enhancements (clearly marked, not historical)

## To Validate
- Items requiring user confirmation or clarification
```

### Privacy and Redaction

Strict privacy rules were applied throughout:
- No company names, client names, or specific identifiers
- Generic descriptions used (e.g., "state-wide citizen identity provider", "higher-education institution")
- Technology names allowed (Salesforce, Boomi, MuleSoft, etc.)
- All content safe for potential public GitHub sharing

## Rules and Patterns

### Knowledge Base Organization

- Organize by domain (architecture, integrations, identity-sso, data-modeling, security, project-methods, templates, misc)
- Use consistent file naming conventions within each domain
- Follow the standard content structure for all files
- Cross-reference related topics across domains

### Content Sourcing

- Base all content on:
  - ChatGPT dump of real work history
  - Actual files in workspace (docs, specs, code, configs)
- Never invent projects, tools, or patterns
- Mark uncertain items as "To Validate"
- Document sources when adding from workspace files

### Extraction Workflow

1. Start with ChatGPT dump as index of topics
2. Search workspace for supporting evidence
3. Extract concrete details from workspace files
4. Generalize patterns while preserving accuracy
5. Add to appropriate domain file
6. Mark sources and validation needs

### Quality Checks

Before adding content, verify:
- Is it backed by evidence (dump or workspace)?
- Is it my real work (not generic docs)?
- Is it properly anonymized?
- Is it useful and actionable?

### File Management

- Keep changes focused and reviewable (few files at a time)
- Update extraction log after each session
- Maintain addition summaries for tracking
- Version control all knowledge files
- Document what was added in each update

## Suggested Improvements (From AI)

### Automated Validation

Implement automated validation:
- Scripts to check for privacy violations (company names, etc.)
- Validation of content structure consistency
- Cross-reference checking between files
- Link validation for internal references

### Knowledge Base Search

Build search capabilities:
- Full-text search across all knowledge files
- Domain-specific search filters
- Tag-based organization
- Related topic suggestions

### Continuous Integration

Set up CI/CD for knowledge base:
- Automated structure validation
- Privacy check automation
- Link checking
- Documentation generation

## To Validate

- Specific prompt file usage patterns and when to use which prompt
- Workspace search strategies that were most effective
- File organization decisions and rationale
- Content structure variations that might be needed
- Integration with other documentation systems

