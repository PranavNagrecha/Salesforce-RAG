# Using This RAG Library with Cursor IDE

Cursor IDE supports RAG (Retrieval-Augmented Generation) through its knowledge base features. This guide shows how to use this Salesforce RAG library with Cursor.

## Setup

### Option 1: Add RAG Directory to Cursor

1. Open Cursor Settings (Cmd/Ctrl + ,)
2. Navigate to "Features" → "Knowledge Base" or "RAG"
3. Add the `rag/` directory to your knowledge base paths
4. Cursor will index the markdown files automatically

### Option 2: Reference in Prompts

You can reference specific knowledge files in your Cursor prompts:

```
@rag/development/apex-patterns.md How should I structure my Apex service layer?
```

## Usage Patterns

### 1. Domain-Specific Questions

When asking about a specific domain, reference the relevant knowledge file:

**Example Prompt:**
```
@rag/integrations/etl-vs-api-vs-events.md 
I need to sync 500K records daily from an external system. 
Which integration pattern should I use?
```

**Example Prompt:**
```
@rag/development/flow-patterns.md 
I need to create a Record-Triggered Flow that updates related records. 
What structure should I follow?
```

### 2. Cross-Domain Questions

For questions spanning multiple domains, reference multiple files:

**Example Prompt:**
```
@rag/development/apex-patterns.md @rag/development/error-handling-and-logging.md
I'm building an Apex service class that calls an external API. 
How should I structure it and handle errors?
```

### 3. Using the Index

Reference the index to discover relevant files:

**Example Prompt:**
```
@rag/rag-index.md 
I need to implement multi-tenant identity. 
Which files should I read?
```

### 4. Using JSON Metadata

For programmatic retrieval, use the JSON library:

**Example Prompt:**
```
@rag/rag-library.json 
Find all files related to "integration" and "error handling"
```

## Best Practices

### 1. Start with the Index

When exploring a new topic, start with `rag-index.md`:

```
@rag/rag-index.md What files cover integration patterns?
```

### 2. Use Specific Files for Deep Dives

Once you know which file is relevant, reference it directly:

```
@rag/integrations/integration-platform-patterns.md 
How do I use MuleSoft as a security boundary?
```

### 3. Combine Related Files

For complex questions, combine multiple related files:

```
@rag/development/apex-patterns.md @rag/development/error-handling-and-logging.md @rag/patterns/cross-cutting-patterns.md
How should I structure an Apex service that handles bulk operations, 
logs errors, and respects governor limits?
```

### 4. Reference Terminology

When encountering unfamiliar terms:

```
@rag/glossary/core-terminology.md What is an External ID?
```

## Example Workflows

### Workflow 1: Designing a New Integration

1. **Understand integration patterns:**
   ```
   @rag/integrations/etl-vs-api-vs-events.md 
   When should I use ETL vs API vs Events?
   ```

2. **If using integration platform:**
   ```
   @rag/integrations/integration-platform-patterns.md 
   How do I implement MuleSoft integration patterns?
   ```

3. **Design external IDs:**
   ```
   @rag/data-modeling/external-ids-and-integration-keys.md 
   How should I design external IDs for this integration?
   ```

4. **Handle errors:**
   ```
   @rag/development/error-handling-and-logging.md 
   How should I log integration errors?
   ```

### Workflow 2: Building a Lightning Web Component

1. **Understand LWC patterns:**
   ```
   @rag/development/lwc-patterns.md 
   What patterns should I use for a console-style LWC?
   ```

2. **Integrate with Apex:**
   ```
   @rag/development/apex-patterns.md 
   How should I structure Apex classes for LWC integration?
   ```

3. **Handle errors:**
   ```
   @rag/development/error-handling-and-logging.md 
   How should I handle and log errors in my LWC?
   ```

### Workflow 3: Troubleshooting Integration Issues

1. **Debug the integration:**
   ```
   @rag/troubleshooting/integration-debugging.md 
   How do I troubleshoot integration failures?
   ```

2. **Reconcile data:**
   ```
   @rag/troubleshooting/data-reconciliation.md 
   How do I reconcile data between systems?
   ```

3. **Check external IDs:**
   ```
   @rag/data-modeling/external-ids-and-integration-keys.md 
   Are my external IDs designed correctly?
   ```

## Tips

- **Use semantic search**: Cursor's RAG can find relevant content even if you don't know the exact file name
- **Reference multiple files**: Combine related knowledge files for comprehensive answers
- **Check the glossary**: Use `core-terminology.md` to understand domain-specific terms
- **Follow patterns**: The knowledge files provide proven patterns—adapt them to your use case

## Advanced: Custom RAG Commands

You can create custom Cursor prompts that automatically reference this library. See `cursor/prompts/Public RAG Command.md` (if created) for example prompt templates.

