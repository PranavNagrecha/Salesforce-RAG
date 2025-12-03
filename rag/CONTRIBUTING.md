# Contributing to Salesforce RAG Repository

Thank you for your interest in contributing to the Salesforce RAG knowledge repository. This document provides guidelines for contributing content, ensuring consistency and quality.

## Contribution Process

1. **Review Existing Content**: Check if similar content already exists
2. **Follow Structure Standards**: Use templates in `meta/templates/`
3. **Maintain Consistency**: Follow style guide and terminology standards
4. **Add Cross-References**: Link to related patterns
5. **Include Q&A**: Add Q&A section for RAG retrieval
6. **Test Examples**: Ensure code examples work and follow best practices

## File Structure Requirements

All new files must include:

1. **YAML Frontmatter**:
   ```yaml
   ---
   title: "File Title"
   level: "Beginner|Intermediate|Advanced"
   tags:
     - tag1
     - tag2
   last_reviewed: "YYYY-MM-DD"
   ---
   ```

2. **Standard Sections**:
   - Overview
   - When to Use (for pattern files)
   - Prerequisites
   - Core Concepts
   - Implementation (or Patterns)
   - Best Practices
   - Common Pitfalls
   - Q&A (10+ questions)
   - Related Patterns
   - Edge Cases and Limitations (when applicable)

## Content Standards

### Voice and Tone

- Use third-person, declarative voice: "X is used when Y" or "Use X when Y"
- Avoid first-person ("we", "I") unless in examples
- Be clear and concise
- Assume audience is Salesforce architects, developers, or advanced admins

### Terminology

- Follow `meta/terminology-mapping.md` for standard terms
- Use "Experience Cloud" not "Communities"
- Use "Permission Set" not "Perm Set"
- Use "Record-Triggered Flow" not "RTF"
- Include deprecation warnings for deprecated features

### Code Examples

- All code must follow user's coding standards (see user_rules)
- Include ApexDoc comments for Apex code
- Test all code examples before including
- Explain code examples with context
- Include error handling patterns

### Q&A Sections

- Include 8-10 common questions
- Questions should be natural language queries
- Answers should be comprehensive but concise
- Use format: "### Q: [Question]?" followed by "**A**: [Answer]"

## Quality Checklist

Before submitting:

- [ ] File follows template structure
- [ ] Frontmatter includes all required fields
- [ ] Terminology matches standard mapping
- [ ] Code examples tested and documented
- [ ] Q&A section included (8+ questions)
- [ ] Related Patterns section included
- [ ] Cross-references updated in related files
- [ ] No broken links
- [ ] Spelling and grammar checked
- [ ] Deprecation warnings included where applicable

## Adding New Files

1. **Choose Location**: Place file in appropriate domain folder
2. **Use Template**: Start with `meta/templates/knowledge-file-template.md`
3. **Update Index**: Add entry to `rag-index.md`
4. **Update Metadata**: Add entry to `rag-library.json`
5. **Add Cross-References**: Link from related files

## Updating Existing Files

1. **Maintain Structure**: Keep existing structure unless improving it
2. **Update Last Reviewed**: Update `last_reviewed` in frontmatter
3. **Preserve Q&A**: Don't remove existing Q&A, enhance it
4. **Update Cross-References**: Update links in related files if needed
5. **Document Changes**: Note significant changes in commit message

## Code Example Guidelines

### Apex Code

- Use `with sharing` or `without sharing` explicitly
- Include error handling
- Follow bulkification patterns
- Include ApexDoc comments
- Use descriptive variable names

### LWC Code

- Include error handling
- Use `@wire` appropriately
- Handle loading states
- Include accessibility attributes
- Follow LWC best practices

### Flow Examples

- Document entry criteria
- Explain decision logic
- Include error handling
- Note bulk considerations

## Review Process

1. **Self-Review**: Check against quality checklist
2. **Terminology Check**: Verify against terminology mapping
3. **Link Validation**: Check all internal links work
4. **Code Testing**: Test all code examples
5. **Structure Validation**: Verify follows template

## Questions?

- Review `meta/style-guide.md` for detailed style guidelines
- Check `meta/terminology-mapping.md` for terminology standards
- Look at existing files for examples of good structure
- Review `MAINTENANCE.md` for maintenance procedures

## Thank You

Your contributions help make this repository a valuable resource for the Salesforce community. Thank you for taking the time to contribute!

