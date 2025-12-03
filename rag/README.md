# Salesforce RAG Knowledge Repository

This repository contains comprehensive Salesforce knowledge, patterns, and best practices organized for use in Retrieval-Augmented Generation (RAG) systems and as a reference for Salesforce architects, developers, and administrators.

## Repository Structure

### Core Domains

- **`architecture/`** - System architecture patterns, org strategy, portal design, governance
- **`development/`** - Apex, LWC, Flow patterns, error handling, optimization
- **`integrations/`** - Integration patterns, platforms (MuleSoft, Boomi), CDC, callouts
- **`security/`** - Permission sets, sharing mechanisms, LLM data governance
- **`data-modeling/`** - Data models, external IDs, migration patterns, object setup
- **`testing/`** - Testing patterns, test data factories, accessibility testing
- **`troubleshooting/`** - Common errors, debugging patterns, reconciliation
- **`operations/`** - CI/CD, environment strategy, release governance
- **`observability/`** - Monitoring, performance tuning, HA/DR
- **`data-governance/`** - Data quality, compliance, residency
- **`adoption/`** - User readiness, org health checks
- **`project-methods/`** - Delivery framework, testing strategy, deployment

### Supporting Content

- **`code-examples/`** - Working code examples organized by domain
- **`api-reference/`** - API method signatures and references
- **`mcp-knowledge/`** - MCP-extracted knowledge (LWC, LDS, design system)
- **`quick-start/`** - Getting started guides
- **`patterns/`** - Cross-cutting patterns summary
- **`glossary/`** - Core terminology definitions
- **`meta/`** - Templates, style guides, and metadata

## File Structure Standards

All knowledge files follow a consistent structure:

1. **Frontmatter** (YAML) - Metadata including title, level, tags, last_reviewed
2. **Overview** - High-level description and purpose
3. **When to Use** - Decision criteria for using patterns
4. **Prerequisites** - Required knowledge or setup
5. **Core Concepts** - Fundamental concepts and patterns
6. **Implementation** - Step-by-step implementation guidance
7. **Best Practices** - Recommended approaches
8. **Common Pitfalls** - Anti-patterns and how to avoid them
9. **Q&A** - Common questions and answers for RAG retrieval
10. **Related Patterns** - Links to related content
11. **Edge Cases and Limitations** - Known limitations and workarounds

## Content Levels

Files are tagged with levels to indicate target audience:

- **Beginner** - Foundational concepts, basic patterns
- **Intermediate** - Standard patterns, common scenarios
- **Advanced** - Complex patterns, edge cases, optimization

## Key Features

- **RAG-Optimized**: Structured for optimal retrieval and generation
- **Pattern-Focused**: Emphasis on reusable patterns over one-off solutions
- **Cross-Referenced**: Extensive linking between related topics
- **Q&A Sections**: Common questions and answers for better retrieval
- **Code Examples**: Working examples with explanations
- **Best Practices**: Aligned with Salesforce best practices

## Navigation

- **`rag-index.md`** - Comprehensive index of all files
- **`rag-library.json`** - Machine-readable metadata for all files
- **`website/meta/style-guide.md`** - Writing and formatting standards
- **`website/meta/terminology-mapping.md`** - Standard terminology definitions

## Usage

### For RAG Systems

1. Use `rag-library.json` for programmatic access to metadata
2. Files include frontmatter with tags, levels, and metadata
3. Q&A sections provide seed questions for retrieval
4. Related Patterns sections enable graph-based retrieval

### For Human Readers

1. Start with `rag-index.md` to find topics
2. Use Related Patterns sections to discover related content
3. Follow learning paths from beginner to advanced
4. Reference code examples for implementation guidance

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.html) for contribution guidelines.

## Maintenance

See [MAINTENANCE.md](MAINTENANCE.html) for maintenance procedures and schedules.

## License

[Add license information if applicable]

