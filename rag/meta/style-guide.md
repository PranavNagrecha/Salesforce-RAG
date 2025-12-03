# RAG Knowledge Library Style Guide

This style guide establishes standards for voice, tone, terminology, formatting, and structure across all files in the RAG knowledge library.

## Voice and Tone

### Standard Voice: Third-Person Declarative

**Use**: Third-person, declarative voice throughout all documentation.

**Correct Examples**:
- "Apex is used when Flows are insufficient for complex logic."
- "Permission Sets are assigned to users to grant incremental access."
- "External IDs enable idempotent upsert operations."

**Incorrect Examples**:
- "We use Apex when Flows are insufficient." (first-person)
- "You should assign Permission Sets to users." (second-person imperative)
- "Use External IDs for idempotent upserts." (imperative without context)

### Tone Guidelines

- **Professional**: Maintain a professional, authoritative tone
- **Clear**: Use clear, direct language
- **Concise**: Be concise but comprehensive
- **Consistent**: Maintain consistency across all files

## Terminology Standards

### Standardized Terms

Use these exact terms consistently throughout all documentation:

#### Platform Terms
- ✅ **Experience Cloud** (not "Community", not "Portal", not "Communities")
- ✅ **Lightning Web Component** or **LWC** (in code contexts, LWC is acceptable)
- ✅ **Record-Triggered Flow** (not "RTF", not "Record Trigger Flow")
- ✅ **Platform Events** (not "PE")
- ✅ **Custom Metadata Type** (not "CMT")
- ✅ **Custom Setting** (not "CS")

#### Security Terms
- ✅ **Permission Set** (not "Perm Set", not "PS")
- ✅ **Permission Set Group** (not "PSG")
- ✅ **Field-Level Security** or **FLS** (FLS acceptable in technical contexts)
- ✅ **Object-Level Security** or **OLS** (OLS acceptable in technical contexts)
- ✅ **Org-Wide Defaults** or **OWD** (OWD acceptable in technical contexts)

#### Integration Terms
- ✅ **External ID** (not "Ext ID", not "External Identifier")
- ✅ **Integration User License** (not "Integration License")
- ✅ **Named Credential** (not "Named Cred")

#### Data Terms
- ✅ **Student Information System** or **SIS** (SIS acceptable after first use)
- ✅ **Education Data Architecture** or **EDA** (EDA acceptable after first use)

### Terminology Usage Rules

1. **First Use**: Always spell out acronyms on first use with acronym in parentheses
   - Example: "Lightning Web Component (LWC) is used for..."
   - After first use, acronym is acceptable: "LWC components can..."

2. **Consistency**: Once a term is established, use it consistently throughout the document

3. **Context Matters**: In code examples and technical contexts, abbreviations may be acceptable if they're standard in that context

## Heading Hierarchy

### Standard Structure

```
# H1: Document Title (only one per file)
## H2: Major Sections (Overview, Core Concepts, Patterns, etc.)
### H3: Subsections within major sections
#### H4: Sub-subsections (use sparingly)
```

### Heading Guidelines

- **H1**: Only for document title (matches frontmatter title)
- **H2**: Major sections (Overview, When to Use, Core Concepts, Patterns, Implementation, Pitfalls, Edge Cases, Q&A, Related Patterns)
- **H3**: Subsections, individual patterns, concepts
- **H4**: Use sparingly for detailed breakdowns

### Heading Format

- Use title case for all headings
- Be descriptive and specific
- Avoid generic headings like "Introduction" or "Details"

## Code Example Formatting

### Structure

All code examples should follow this structure:

1. **Brief Description** (1-2 sentences)
2. **Pattern/Use Case** (what it demonstrates)
3. **Complexity Level** (Basic/Intermediate/Advanced)
4. **Related Patterns** (links)
5. **Problem Statement** (what problem it solves)
6. **Solution Code** (with comments)
7. **Explanation** (why it works)
8. **Best Practices** (do's and don'ts)

### Code Commenting Standards

- Use ApexDoc format for classes and methods
- Explain **why**, not just **what**
- Use clear, descriptive variable names
- Include parameter and return value descriptions

### Example Format

```apex
/**
 * Service class for processing Contact updates
 * Orchestrates workflow: query → validate → update → log
 */
public with sharing class ContactUpdateService {
    
    /**
     * Updates contacts with validation and business logic
     * @param contactIds Set of Contact IDs to update
     * @return List of processed Contact IDs
     */
    public static List<Id> processContacts(Set<Id> contactIds) {
        // Implementation with clear comments
    }
}
```

## Cross-Linking Format

### Related Patterns Section

Standard format for "Related Patterns" section:

```markdown
## Related Patterns

**See Also**:
- [Pattern Name](/Salesforce-RAG/rag/path/to/pattern-file.html) - Brief description of relationship
- [Another Pattern](/Salesforce-RAG/rag/path/to/another-pattern.html) - Brief description

**Related Domains**:
- [Domain File](/Salesforce-RAG/rag/path/to/domain-file.html) - Brief description
```

### Internal Link Format

- Use relative paths with `rag/` prefix: `rag/development/apex-patterns.md`
- Always include brief description after link
- Ensure bidirectional linking when appropriate (if A links to B, B should link to A when relevant)

## File Structure Standards

### Required Sections

All knowledge files must include these sections in order:

1. **Overview** - Brief introduction (2-4 paragraphs)
2. **When to Use** - Decision criteria and use cases
3. **Prerequisites** - Required knowledge and recommended reading
4. **Core Concepts** - Fundamental concepts and terminology
5. **Patterns** - Main content (patterns, practices, approaches)
6. **Implementation** - Step-by-step guidance
7. **Pitfalls** - Common mistakes and anti-patterns
8. **Edge Cases and Limitations** - Important considerations
9. **Q&A** - Common questions and answers (5-10 questions)
10. **Related Patterns** - Links to related content

### Optional Sections

- **Variations** - Different approaches to the same pattern
- **Migration Considerations** - Guidance for migrating from other approaches
- **Examples** - Additional examples beyond code examples

## Frontmatter Standards

### Required Fields

```yaml
---
title: "Document Title"
level: "Beginner|Intermediate|Advanced"
tags:
  - tag1
  - tag2
last_reviewed: "YYYY-MM-DD"
---
```

### Optional Fields

```yaml
source: "Source name"
source_url: "Source URL"
topic: "Topic category"
section: "Section name"
```

### Tag Guidelines

- Use lowercase, hyphenated tags: `apex-patterns`, `integration-platforms`
- Include domain tag: `development`, `architecture`, `integrations`
- Include technology tag: `apex`, `lwc`, `flow`, `mulesoft`
- Include concept tag: `security`, `testing`, `performance`

## Level Indicators

### File Level

Set in frontmatter: `level: "Beginner|Intermediate|Advanced"`

### Section Level

When content level changes within a file, add level indicator:

```markdown
### Advanced: Complex Pattern Name

[Advanced content here]
```

### Level Definitions

- **Beginner**: Assumes basic Salesforce knowledge, explains fundamentals
- **Intermediate**: Assumes understanding of Salesforce basics, covers patterns and practices
- **Advanced**: Assumes deep Salesforce knowledge, covers complex scenarios and optimizations

## Q&A Section Standards

### Format

```markdown
## Q&A

### Q: [Clear, specific question]?

**A**: [Comprehensive answer with examples if needed]

### Q: [Another question]?

**A**: [Answer]
```

### Guidelines

- Include 5-10 questions per file
- Questions should be common, real-world scenarios
- Answers should be comprehensive but concise
- Use examples in answers when helpful
- Cover both "how" and "why" questions

## Checklist Format

When using checklists:

```markdown
### Implementation Checklist

- [ ] Step 1: Description
- [ ] Step 2: Description
- [ ] Step 3: Description
```

## Best Practices Format

### Do's and Don'ts

```markdown
**Do**:
- ✅ Best practice 1
- ✅ Best practice 2

**Don't**:
- ❌ Anti-pattern 1
- ❌ Anti-pattern 2
```

## Deprecation Warnings

When documenting deprecated features:

```markdown
> **⚠️ Deprecated**: [Feature name] is deprecated as of [Release]. Use [replacement] instead. See [migration guide link] for migration guidance.
```

## Examples of Correct Formatting

### Pattern Section

```markdown
### Pattern 1: Service Layer Pattern

**When to use**: Orchestrating complex workflows that involve multiple objects or systems.

**Implementation**:
1. Create service class with `public static` methods
2. Delegate to Domain layer for validation
3. Delegate to Selector layer for data access
4. Handle errors and logging

**Example**:
```apex
// Code example
```

**Best Practices**:
- Use `with sharing` or `without sharing` explicitly
- Process collections, not single records
- Delegate to appropriate layers
```

## Review Checklist

Before finalizing any file, ensure:

- [ ] Voice is third-person declarative
- [ ] Terminology matches style guide standards
- [ ] All required sections are present
- [ ] Headings follow hierarchy standards
- [ ] Code examples follow formatting standards
- [ ] Cross-links use standard format
- [ ] Frontmatter includes required fields
- [ ] Q&A section has 5-10 questions
- [ ] Related Patterns section is complete
- [ ] Level indicator is set appropriately

## Updates to This Guide

This style guide should be updated as standards evolve. When making changes:

1. Document the change and rationale
2. Update affected files
3. Communicate changes to contributors
4. Update this document with the change date

**Last Updated**: 2025-01-XX

