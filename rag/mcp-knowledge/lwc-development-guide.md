# LWC Development Guide - MCP Knowledge

> This file contains knowledge extracted from Salesforce MCP Service tools.  
> It complements the lived-experience patterns in `rag/development/` and `rag/patterns/`.

## Overview

This guide provides comprehensive guidance for Lightning Web Components (LWC) development, covering core principles, technical stack, best practices, and development workflows.

**Source**: Salesforce MCP Service - `mcp_salesforce_guide_lwc_development`

## Core Principles

### Project Understanding
- Analyze user requests thoroughly before implementation
- Ask clarifying questions when requirements are unclear
- Respect Salesforce platform boundaries and governor limits
- Follow systematic error resolution approaches

### Development Workflow
1. **Analyze Requirements** - Understand what needs to be built
2. **Review Existing Code** - Check the codebase for similar patterns
3. **Plan Implementation** - Design component structure before coding
4. **Implement Incrementally** - Build and test in small chunks
5. **Test Thoroughly** - Include Jest tests for LWC and Apex tests for backend

## Technical Stack

### Core Technologies
- **Lightning Web Components (LWC)** - Primary UI framework
- **Lightning Data Service (LDS)** - Client-side data access layer with caching
- **Apex** - Server-side business logic
- **SOQL/SOSL** - Data querying
- **SLDS** - Lightning Design System for styling

### Development Environment
- **SFDX CLI** - Preferred command-line interface for deployment
- **VS Code** - Primary development environment
- **ESLint/Prettier** - Code formatting and linting
- **Jest** - Component testing

## Best Practices

### LWC Development
- Use base Lightning components when available
- Create modular, reusable components
- Implement proper component communication patterns:
  - `@api` properties for parent-to-child
  - Custom events for child-to-parent
  - Lightning Message Service for cross-component

### Data Access using LDS
- Prefer LDS for retrieving data from Salesforce
- Use LDS for standard CRUD operations
- Only use Apex when existing LDS adapters are not sufficient for the data requirements
- Implement proper security checks and field-level security

### Apex Development
- Write bulkified code that respects governor limits
- Use `with sharing` for proper security enforcement
- Avoid SOQL queries or DML in loops
- Include proper error handling

### Performance Optimization
- Minimize server round-trips
- Cache data when appropriate
- Optimize queries with selective filters

## Project Structure
```
force-app/main/default/
├── lwc/               # Lightning Web Components for the "c" namespace
├── aura/              # Aura Components for the "c" namespace
├── classes/           # Apex classes
├── objects/           # Custom objects and fields
├── permissionsets/    # Permission sets
├── layouts/           # Page layouts
├── experiences/       # Experience Cloud sites
└── ...                # Other metadata
```

## Critical Constraints
- Use only Salesforce-approved APIs and libraries
- Respect governor limits and platform boundaries
- Implement proper security controls
- Write test coverage for all custom code
- Use LWC for new development (not Aura, which is now deprecated)

## Debugging & Troubleshooting
- Check debug logs for Apex errors
- Use browser console for LWC errors
- Validate deployment errors with specific attention to metadata dependencies
- Address governor limit issues by refactoring for efficiency

## Quality Standards
- Maintain consistent code formatting using project standards
- Write comprehensive test coverage (minimum 75% for Apex)
- Ensure components are accessible and mobile-friendly
- Follow security best practices for all code

## Integration with Existing RAG

**Related Patterns**:
- [LWC Patterns](rag/development/lwc-patterns.md) - Complements with MCP-validated practices
- [Apex Patterns](rag/development/apex-patterns.md) - Related backend patterns
- [Security Patterns](rag/security/) - Security considerations

**How This Complements Existing RAG**:
- Validates and extends existing LWC patterns with official Salesforce guidance
- Provides development workflow and project structure guidance
- Emphasizes LDS usage over Apex where appropriate
- Adds quality standards and testing requirements

