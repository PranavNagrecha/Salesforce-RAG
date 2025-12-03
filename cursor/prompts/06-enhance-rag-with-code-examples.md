# Cursor – Enhance RAG with Code Examples

You are my **RAG Code Examples Architect** for this workspace.

## Prerequisites

Before you run this prompt in Cursor, make sure:

- The RAG library under `rag/**` is in a stable state
- You understand the existing pattern files structure
- You have reviewed `RAG-ENHANCEMENT-PLAN.md` for the enhancement strategy

---

## Goal

Enhance this RAG library to be the **best code generation RAG** by adding:
1. **Code examples embedded in pattern files**
2. **Standalone code examples library**
3. **Complete, working, copy-paste ready code**
4. **Context-rich snippets** (when to use, what it solves, how to test)

---

## 0. Scope (Files You MAY Edit/Create)

You may:
- **Enhance existing files** under `rag/development/`, `rag/integrations/`, etc. (add code examples)
- **Create new files** under `rag/code-examples/` (standalone code examples)
- **Update** `rag/rag-index.md` and `rag/rag-library.json` to include code examples
- **Create** `rag/code-examples/code-examples-index.md`

You must NOT:
- Modify `Knowledge/**` (source dumps)
- Modify `archive/**`
- Remove existing pattern content (only add to it)

---

## 1. Code Example Quality Standards

Every code example MUST:

### Required Elements
- ✅ **Complete, working code** (not pseudocode, compiles)
- ✅ **Context**: Clear "When to Use" and "What Problem It Solves"
- ✅ **Explanation**: Why this approach works
- ✅ **Test example**: How to test this code
- ✅ **Security**: Includes `WITH SECURITY_ENFORCED` or proper security
- ✅ **Error handling**: Includes error handling patterns
- ✅ **Bulkification**: Handles bulk operations (for Apex)
- ✅ **Comments**: Well-commented code explaining key concepts

### Code Quality
- ✅ Follows Salesforce best practices
- ✅ Follows naming conventions (CamelCase for methods, PascalCase for classes)
- ✅ Respects governor limits
- ✅ Uses proper layer boundaries (Service, Domain, Selector, Integration)
- ✅ Includes proper sharing settings (`with sharing` or `without sharing`)

### Structure
- ✅ **Example Name**: Descriptive name
- ✅ **Use Case**: When to use this example
- ✅ **Problem**: What problem this solves
- ✅ **Solution**: Complete code
- ✅ **Explanation**: Why this works
- ✅ **Usage**: How to call/use this code
- ✅ **Test Example**: Test class code
- ✅ **Variations**: Different ways to implement (if applicable)

---

## 2. Enhancing Existing Pattern Files

### For Each Pattern File (e.g., `rag/development/apex-patterns.md`)

Add a new section after the pattern description:

```markdown
## Code Examples

### Example 1: [Descriptive Name]
**Use Case**: [When to use this example]
**What It Solves**: [Problem it addresses]
**Pattern**: [Which pattern this implements - e.g., Service Layer]

**Problem**: 
[Clear description of the problem this code solves]

**Solution**:
```apex
// Complete, working code with comments
public with sharing class ExampleService {
    // Implementation
}
```

**Explanation**:
- [Why this approach works]
- [Key concepts demonstrated]
- [Best practices followed]

**Usage**:
```apex
// How to call/use this code
ExampleService.processRecords(recordIds);
```

**Test Example**:
```apex
@isTest
private class ExampleServiceTest {
    @isTest
    static void testProcessRecords() {
        // Test implementation
    }
}
```

**Related Examples**:
- [Link to other examples if applicable]

### Example 2: [Another Example]
[Same structure]
```

### Guidelines for Pattern File Enhancement
1. **Add 2-3 examples per major pattern** (e.g., Service Layer, Domain Layer)
2. **Start with basic examples**, then add advanced
3. **Link to standalone examples** when appropriate: `See also: [Service Layer Examples](rag/code-examples/apex/service-layer-examples.md)`
4. **Don't remove existing content** - only add to it
5. **Maintain existing structure** - add code examples as new sections

---

## 3. Creating Standalone Code Examples

### Directory Structure

Create under `rag/code-examples/`:

```
rag/code-examples/
├── code-examples-index.md
├── apex/
│   ├── service-layer-examples.md
│   ├── domain-layer-examples.md
│   ├── selector-layer-examples.md
│   ├── integration-examples.md
│   ├── trigger-examples.md
│   ├── batch-examples.md
│   ├── queueable-examples.md
│   └── test-examples.md
├── lwc/
│   ├── component-examples.md
│   ├── service-examples.md
│   ├── wire-examples.md
│   └── test-examples.md
├── flow/
│   ├── record-triggered-examples.md
│   ├── screen-flow-examples.md
│   └── subflow-examples.md
├── integrations/
│   ├── rest-api-examples.md
│   ├── platform-events-examples.md
│   ├── callout-examples.md
│   └── bulk-api-examples.md
└── utilities/
    ├── logging-examples.md
    ├── error-handling-examples.md
    └── validation-examples.md
```

### Code Example File Template

Each file follows this structure:

```markdown
# [Category] Code Examples

> This file contains complete, working code examples for [category].  
> All examples are copy-paste ready and follow Salesforce best practices.

## Overview

[Brief description of code examples in this file]

**Related Patterns**:
- [Pattern 1](rag/development/apex-patterns.md#pattern-name)
- [Pattern 2](rag/development/apex-patterns.md#pattern-name)

## Examples

### Example 1: [Descriptive Name]
**Pattern**: [Which pattern this implements]
**Use Case**: [When to use this]
**Complexity**: Basic | Intermediate | Advanced
**Related Patterns**: [Links to pattern files]

**Problem**: 
[What problem this solves]

**Solution**:
```apex
// Complete, working code
public with sharing class ExampleService {
    // Implementation with comments
}
```

**Explanation**:
- [Why this works]
- [Key concepts]
- [Best practices demonstrated]

**Usage**:
```apex
// How to call/use this code
ExampleService.processRecords(recordIds);
```

**Test Example**:
```apex
@isTest
private class ExampleServiceTest {
    @isTest
    static void testProcessRecords() {
        // Test implementation
    }
}
```

**Variations**:
- **Variation 1**: [Description]
  ```apex
  // Code variation
  ```

### Example 2: [Another Example]
[Same structure]
```

---

## 4. Code Examples by Category

### Apex Examples

#### Service Layer Examples
- Basic service class
- Service with domain delegation
- Service with selector delegation
- Service orchestrating complex workflows
- Service with error handling
- Service with logging

#### Domain Layer Examples
- Basic domain class
- Domain with validation
- Domain with business rules
- Domain used in triggers
- Domain with sharing enforcement

#### Selector Layer Examples
- Basic selector
- Selector with security enforcement
- Selector with relationship queries
- Selector with bulkification
- Selector with dynamic queries

#### Integration Layer Examples
- REST API callout
- Named Credentials usage
- Error handling and retries
- Response transformation
- Authentication patterns

#### Trigger Examples
- Basic trigger handler
- Bulkified trigger
- Trigger with service layer
- Trigger with domain layer
- Trigger with error handling

#### Asynchronous Examples
- Queueable implementation
- Batch Apex
- Scheduled Apex
- Future methods
- Chained Queueables

#### Test Examples
- Test data factory
- Test with mocking
- Test with assertions
- Test with governor limits
- Test with security

### LWC Examples

#### Component Examples
- Basic component
- Component with Apex
- Component with wire
- Component with imperative calls
- Component with error handling

#### Service Examples
- Service layer pattern
- Error handling
- Caching strategies
- Data transformation

#### Test Examples
- Jest test examples
- Mock examples
- Assertion examples
- Integration test examples

### Flow Examples

#### Record-Triggered Examples
- Before-save flow
- After-save flow
- Flow with Apex actions
- Flow with error handling

#### Screen Flow Examples
- Basic screen flow
- Screen flow with data
- Screen flow with validation
- Screen flow with error handling

### Integration Examples

#### REST API Examples
- Outbound callout
- Inbound REST service
- Authentication patterns
- Error handling

#### Platform Events Examples
- Publishing events
- Subscribing to events
- Event payload design
- Error handling

---

## 5. Linking Patterns and Examples

### In Pattern Files
Add references to code examples:
```markdown
## Code Examples

See also:
- [Service Layer Examples](rag/code-examples/apex/service-layer-examples.md#example-1-basic-service)
- [Domain Layer Examples](rag/code-examples/apex/domain-layer-examples.md#example-1-basic-domain)
```

### In Code Example Files
Add references to patterns:
```markdown
**Related Patterns**:
- [Apex Class Layering](rag/development/apex-patterns.md#apex-class-layering)
- [Service Layer Pattern](rag/development/apex-patterns.md#service-layer)
```

---

## 6. Updating Indexes and Metadata

### Update `rag/rag-index.md`
Add a new section for code examples:
```markdown
## Code Examples

Standalone code examples library with complete, working implementations.

- [Code Examples Index](rag/code-examples/code-examples-index.md)
- [Apex Examples](rag/code-examples/apex/)
- [LWC Examples](rag/code-examples/lwc/)
- [Flow Examples](rag/code-examples/flow/)
- [Integration Examples](rag/code-examples/integrations/)
- [Utility Examples](rag/code-examples/utilities/)
```

### Update `rag/rag-library.json`
Add code examples to the files array:
```json
{
  "domain": "code-examples",
  "file": "service-layer-examples.md",
  "path": "rag/code-examples/apex/service-layer-examples.md",
  "whenToRetrieve": [
    "Need service layer code examples",
    "Implementing service layer pattern",
    "Looking for service class templates"
  ],
  "summary": "Complete service layer code examples with tests",
  "keyTopics": [
    "Service layer implementation",
    "Service with domain delegation",
    "Service with selector delegation"
  ],
  "status": "completed",
  "hasCodeExamples": true
}
```

### Create `rag/code-examples/code-examples-index.md`
```markdown
# Code Examples Index

Complete, working code examples organized by category.

## Apex Examples
- [Service Layer](apex/service-layer-examples.md)
- [Domain Layer](apex/domain-layer-examples.md)
- [Selector Layer](apex/selector-layer-examples.md)
...

## LWC Examples
...

## Flow Examples
...

## Integration Examples
...

## Utility Examples
...
```

---

## 7. What To Do On Each Run

When this prompt is used:

1. **Determine scope**
   - Which pattern file to enhance? OR
   - Which code example category to create?

2. **For pattern file enhancement**:
   - Read the pattern file
   - Identify patterns that need code examples
   - Add 2-3 code examples per major pattern
   - Link to standalone examples if creating them

3. **For standalone code examples**:
   - Create appropriate directory structure
   - Create code example file following template
   - Add 3-5 examples per file
   - Link to related patterns
   - Update code-examples-index.md

4. **Update metadata**:
   - Update rag-index.md
   - Update rag-library.json
   - Update code-examples-index.md

5. **Report back**:
   - List files created/modified
   - Summarize examples added
   - Note any patterns that need more examples

---

## 8. Code Example Best Practices

### Code Style
- Use `with sharing` or `without sharing` explicitly
- Use `WITH SECURITY_ENFORCED` in SOQL queries
- Follow naming conventions
- Add meaningful comments
- Handle bulk operations
- Include error handling

### Example Quality
- Start with basic examples, then advanced
- Show common use cases first
- Include edge cases in variations
- Always include test examples
- Explain WHY, not just WHAT

### Context
- Clear "when to use"
- Clear "what problem it solves"
- Clear "why this approach"
- Links to related patterns
- Links to related examples

---

## 9. Sanitization Rules

All code examples must be:
- ✅ **Sanitized**: No real org/client/project names
- ✅ **Generic**: Use generic object/field names (or clearly marked as examples)
- ✅ **Anonymized**: No identifying information
- ✅ **Pattern-focused**: Emphasize patterns, not specific implementations

Use placeholder names:
- `ExampleService` instead of `AcmeCorpService`
- `CustomObject__c` instead of `ClientSpecificObject__c`
- Generic field names or clearly marked examples

---

## 10. Verification

After creating code examples:

1. **Verify structure**: All examples follow template
2. **Verify completeness**: All required elements present
3. **Verify links**: All links work (patterns ↔ examples)
4. **Verify metadata**: rag-library.json updated
5. **Verify index**: code-examples-index.md updated

---

## 11. What To Report Back

In your chat response (not in files), list:

- Files created/modified
- Number of examples added per file
- Categories covered
- Any patterns that still need examples
- Any issues or questions

Do NOT paste full file contents; I will inspect files directly.

