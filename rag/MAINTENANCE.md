# Maintenance Procedures

This document outlines maintenance procedures for the Salesforce RAG repository to ensure content quality, consistency, and currency.

## Regular Maintenance Tasks

### Quarterly Reviews

**Schedule**: Every 3 months

**Tasks**:
1. Update `last_reviewed` dates in frontmatter for reviewed files
2. Review files for outdated patterns or deprecated features
3. Check for broken internal links
4. Validate terminology consistency
5. Review Q&A sections for relevance
6. Update deprecation warnings as needed

**Process**:
- Review 25% of files each quarter (complete rotation annually)
- Focus on high-traffic files first
- Document findings and updates
- Update `rag-library.json` metadata

### Annual Comprehensive Audit

**Schedule**: Once per year

**Tasks**:
1. Review all files for structure consistency
2. Validate all code examples still work
3. Check all cross-references are accurate
4. Review terminology across all files
5. Assess coverage gaps
6. Update style guide if needed
7. Review and update decision frameworks

**Process**:
- Create audit checklist
- Review systematically by domain
- Document findings
- Create improvement plan

## Content Currency

### Salesforce Release Updates

**Schedule**: After each Salesforce release (3x per year)

**Tasks**:
1. Review Salesforce release notes for relevant changes
2. Update files affected by new features
3. Add deprecation warnings for deprecated features
4. Update migration guidance as needed
5. Add new patterns for new features

**Process**:
- Monitor Salesforce release notes
- Identify affected files
- Update content systematically
- Test code examples with new features

### Deprecation Tracking

**Current Deprecations**:
- Workflow Rules (deprecated - use Record-Triggered Flows)
- Process Builder (deprecated - use Record-Triggered Flows)
- Flow User Permission (deprecated Winter '26 - use Permission Sets)

**Process**:
- Track deprecation announcements
- Add warnings to affected files
- Provide migration guidance
- Remove deprecated content after migration period

## Quality Assurance

### Link Validation

**Schedule**: Monthly

**Tasks**:
1. Check all internal links (`rag/` paths)
2. Verify relative paths are correct
3. Check for broken external links
4. Validate cross-references

**Tools**:
- Script to find all markdown links
- Manual review of link targets
- Automated link checker (if available)

### Terminology Consistency

**Schedule**: Quarterly

**Tasks**:
1. Review files against terminology mapping
2. Update inconsistent terminology
3. Add new terms to mapping as needed
4. Document terminology decisions

**Process**:
- Use terminology mapping as reference
- Search for known variations
- Update files systematically
- Document changes

### Code Example Validation

**Schedule**: Before each major update

**Tasks**:
1. Test all code examples in sandbox
2. Verify examples follow coding standards
3. Check for syntax errors
4. Validate error handling patterns
5. Update examples for API changes

**Process**:
- Test in Developer Edition or sandbox
- Verify against current API versions
- Update for deprecated methods
- Document any limitations

## Metadata Maintenance

### Frontmatter Validation

**Schedule**: Quarterly

**Tasks**:
1. Verify all files have frontmatter
2. Check required fields are present
3. Validate tag consistency
4. Update `last_reviewed` dates
5. Ensure level indicators are accurate

### rag-library.json Updates

**Schedule**: After each content update

**Tasks**:
1. Update file entries for new files
2. Update paths for moved files
3. Remove entries for deleted files
4. Update metadata for changed files
5. Validate JSON structure

## Coverage Gaps

### Regular Assessment

**Schedule**: Semi-annually

**Tasks**:
1. Review Salesforce feature releases
2. Identify missing topics
3. Assess coverage by domain
4. Prioritize gaps by importance
5. Create content plan

**Process**:
- Compare against Salesforce documentation
- Review community questions
- Assess usage patterns (if available)
- Prioritize high-impact gaps

## Performance Optimization

### File Size Management

**Schedule**: As needed

**Tasks**:
1. Identify files exceeding 800 lines
2. Assess if splitting is beneficial
3. Split large files into focused modules
4. Update cross-references

**Guidelines**:
- Target 300-800 lines per file
- Split when file covers distinct topics
- Merge tiny files (<100 lines) when appropriate

### Chunking Strategy

**Schedule**: Annually

**Tasks**:
1. Review chunking strategy for RAG systems
2. Assess optimal chunk sizes
3. Update metadata for chunk-level tagging
4. Document retrieval optimization strategies

## Documentation Updates

### README Updates

**Schedule**: As needed

**Tasks**:
1. Update repository structure if changed
2. Add new domains or sections
3. Update usage instructions
4. Reflect current state accurately

### Style Guide Updates

**Schedule**: As needed

**Tasks**:
1. Add new style guidelines as needed
2. Update examples
3. Document new patterns
4. Clarify existing guidelines

## Automation Opportunities

### Scripts to Create

1. **Link Validator**: Check all internal links
2. **Frontmatter Validator**: Verify frontmatter completeness
3. **Terminology Checker**: Find terminology inconsistencies
4. **Metadata Generator**: Generate `rag-library.json` from frontmatter
5. **Structure Validator**: Check file structure against template

### CI/CD Integration

**Potential Automation**:
- Link validation on commits
- Frontmatter validation
- Terminology checking
- Structure validation
- Broken link detection

## Maintenance Schedule Summary

| Task | Frequency | Owner |
|------|-----------|-------|
| Quarterly file reviews | Quarterly | Content team |
| Annual comprehensive audit | Annually | Content team |
| Salesforce release updates | 3x per year | Content team |
| Link validation | Monthly | Automated + manual |
| Terminology consistency | Quarterly | Content team |
| Code example validation | Before updates | Content team |
| Metadata maintenance | After updates | Content team |
| Coverage gap assessment | Semi-annually | Content team |

## Reporting

**Maintenance Reports Should Include**:
- Files reviewed/updated
- Issues found and resolved
- New content added
- Deprecations handled
- Coverage gaps identified
- Performance improvements

## Questions?

For questions about maintenance procedures, refer to:
- <a href="{{ '/rag/website/meta/style-guide.html' | relative_url }}">Style Guide</a>
- <a href="{{ '/rag/website/meta/terminology-mapping.html' | relative_url }}">Terminology Mapping</a>
- <a href="{{ '/rag/CONTRIBUTING.html' | relative_url }}">Contributing Guidelines</a>

