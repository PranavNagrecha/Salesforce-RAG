# Project Delivery Framework

## Overview

Sprint-based delivery approach for managing complex multi-stakeholder Salesforce projects. Emphasizes clear scope definition, stakeholder coordination, iterative delivery, and comprehensive quality standards.

**Related Patterns**:
- [Testing Strategy](rag/project-methods/testing-strategy.md) - Comprehensive testing strategies
- [Deployment Patterns](rag/project-methods/deployment-patterns.md) - Deployment and CI/CD patterns
- [Salesforce DX Patterns](rag/project-methods/sfdx-patterns.md) - SFDX-specific patterns
- [Release Governance](rag/operations/release-governance.md) - Release approval and risk management

## Sprint-Based Delivery

### Sprint Structure

**Pattern**: Clear sprint definitions with defined scope

**Implementation**:
- Sprint 1, Sprint 2, etc. with defined scope
- Tracking of Salesforce configuration work within each sprint
- Integration testing milestones aligned with sprint deliverables
- Portal functionality delivered incrementally across sprints
- Clear scope definition and tracking to avoid scope creep

### Sprint Planning

**Practices**:
- Define clear scope for each sprint with specific deliverables
- Track Salesforce configuration work, integration milestones, and portal functionality separately
- Align sprint deliverables with testing windows and stakeholder availability
- Communicate sprint scope clearly to all stakeholders
- Review and adjust sprint scope based on velocity and dependencies

### Sprint Review Process

**Comprehensive Analysis**:
- Detailed feedback documents covering multiple areas
- Example: 18-point detailed feedback document covering:
  1. Logging pattern for HTTP callouts vs DataRaptor-only IPs
  2. NULL checks and error messages
  3. Silent failures and blank screens
  4. Hardcoded URLs - removal and configuration approach
  5. DataRaptor caching
  6. Test components
  7. Missing component descriptions
  8. Hardcoded test data and record IDs
  9. Naming convention - inconsistent naming
  10. Missing timeout settings for HTTP actions
  11. Apex classes used by Sprint 1 components
  12. Apex test classes
  13. Apex code quality - System.debug statements, hardcoded values, error logging
  14. Profile and Permission Set - security and configuration
  15. Feedback survey named flow not found in UI
  16. Data Dictionary - field type conversions, descriptions, naming standards
  17. Guest User Profile configuration
  18. SurveyResponse CreatedBy field - not reflecting actual submitter

## Stakeholder Coordination

### Stakeholder Groups

**Groups**:
- State IT teams for infrastructure and security requirements
- External integrators for integration platform work (MuleSoft, Boomi)
- Analyst partners for business analysis and requirements
- Internal teams for Salesforce configuration and development

### Coordination Practices

**Maintain**:
- Regular communication with all stakeholder groups
- Keep everyone aligned on sprint scope and deliverables
- Coordinate testing windows across multiple systems and teams
- Document decisions and open items from stakeholder meetings
- Escalate blockers and dependencies promptly

## Testing Window Coordination

### Testing Milestones

**Coordination**:
- Reserved testing periods (e.g., December testing periods) for integration validation
- Coordination of testing schedules across multiple systems
- Alignment of testing milestones with sprint deliverables
- User acceptance testing (UAT) coordination with business stakeholders

### Integration Milestone Tracking

**Tracking**:
- Track integration testing milestones separately from Salesforce configuration
- Coordinate integration testing with external integrators and external system teams
- Reserve testing windows for integration validation
- Document integration test results and issues
- Align integration milestones with sprint deliverables

## Change Management

### Documentation Alignment

**Pattern**: Keep technical design documents aligned with implementation

**Practices**:
- Discussions about when/how new objects and automations need to be reflected in technical design docs (TDD)
- Keeping diagrams and documentation aligned with actual implemented flows
- Version control for design documents and technical specifications
- Communication of changes to all stakeholders
- Review documentation regularly for accuracy

### Change Communication

**Practices**:
- Communicate changes to all stakeholders
- Update TDD when implementations change
- Keep diagrams aligned with actual flows
- Version control all documentation
- Regular documentation reviews

## Quality Standards

### Comprehensive Code Review

**Pattern**: Rigorous code review process establishing comprehensive quality standards

**Standards Established**:

**Error Logging Standards**:
- ALL exceptions MUST be logged to custom log object using logging utility class
- NO System.debug statements in production code
- Use proper logging instead of System.debug

**Error Handling Standards**:
- Integration Procedures must show error messages to users when APIs fail
- Set `failOnStepError: true` for critical steps
- Add error states to Flex Cards
- Return error data in response

**Configuration Management Standards**:
- NO hardcoded values (IDs, counts, URLs, etc.)
- Use Custom Metadata or Custom Settings
- All URLs must use Named Credentials or Custom Metadata

**Apex Code Standards**:
- ALL Apex classes MUST have proper ApexDoc documentation
- ALL SOQL queries MUST use `WITH SECURITY_ENFORCED` or `WITH USER_MODE`
- ALL SOQL queries MUST be optimized (combine queries where possible)
- NO SOQL queries in loops
- ALL test classes MUST create their own test data (no `@IsTest(SeeAllData=true)`)
- ALL test classes MUST achieve minimum 90% code coverage

**Component Standards**:
- ALL components MUST have meaningful descriptions
- NO test/dummy components in production
- Follow PascalCase naming convention
- Add timeout settings to HTTP actions
- Remove hardcoded test data

**Data Dictionary Standards**:
- Field descriptions must be meaningful (not just repeat label)
- Include: source, purpose, population, business rules
- Add help text for user-facing fields
- Convert Text fields with limited values to Picklists
- Standardize field naming patterns

## Standards Documentation

### Project Rules and Global Standards

**Comprehensive Document**: 1,000+ line standards document covering:

- Error logging, error handling, error message display
- Named Credentials usage
- Hardcoded URL prohibition
- Configuration management
- Component status and naming conventions
- Version management
- Performance optimization
- Security standards
- Documentation requirements
- Testing component standards
- Integration Procedure structure
- DataRaptor standards
- Apex code standards
- Profile and Permission Set standards
- Data Dictionary/Field standards

## Best Practices

### Sprint Management

- Define clear scope for each sprint
- Track deliverables separately by type
- Align with testing windows
- Communicate scope clearly
- Review and adjust based on velocity

### Stakeholder Management

- Maintain regular communication
- Keep everyone aligned on scope
- Coordinate testing windows
- Document decisions and action items
- Escalate blockers promptly

### Quality Assurance

- Establish comprehensive standards
- Conduct rigorous code reviews
- Document all standards
- Enforce standards consistently
- Review and update standards regularly

### Documentation

- Keep documentation aligned with implementation
- Version control all documentation
- Update TDD when implementations change
- Communicate changes to stakeholders
- Review documentation regularly

## Tradeoffs

### Advantages

- Clear scope and deliverables
- Systematic quality standards
- Stakeholder alignment
- Iterative delivery
- Comprehensive documentation

### Challenges

- Requires discipline and process
- Documentation overhead
- Coordination complexity
- Standards enforcement
- Change management complexity

## When to Use This Framework

Use this delivery framework when:

- Complex multi-stakeholder projects
- Multiple integration points
- High quality requirements
- Government/compliance projects
- Large-scale implementations

## When Not to Use This Framework

Avoid this framework when:

- Simple projects with single stakeholder
- No integration requirements
- Rapid prototyping needs
- Different methodology preferred
- Minimal quality requirements

## Related Patterns

- [Testing Strategy](rag/project-methods/testing-strategy.md) - Comprehensive testing strategies covering integration testing, data quality testing, user migration testing, and UAT
- [Deployment Patterns](rag/project-methods/deployment-patterns.md) - Deployment and CI/CD patterns, source control strategies, Metadata API patterns
- [Salesforce DX Patterns](rag/project-methods/sfdx-patterns.md) - SFDX project structure, commands, scratch org patterns, source tracking
- [Release Governance](rag/operations/release-governance.md) - Change Advisory Boards, approval workflows, risk-based release checklists
- [CI/CD Patterns](rag/operations/cicd-patterns.md) - CI/CD automation, unlocked packages, sandbox seeding, rollback patterns

