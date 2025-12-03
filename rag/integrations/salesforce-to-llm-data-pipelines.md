---
title: "Salesforce to LLM Data Pipelines"
level: "Advanced"
tags:
  - integrations
  - llm
  - rag
  - data-pipelines
  - ai
last_reviewed: "2025-01-XX"
---

# Salesforce → LLM Data Pipelines

## Overview

This document covers high-level pipeline patterns for extracting, transforming, and loading Salesforce data and metadata into LLM-powered systems (RAG, tools, agents). It addresses how to move Salesforce data into RAG/LLM systems, common architectural variants and their tradeoffs, extraction strategies, transformation and chunking approaches, and interaction with manifest-style descriptions.

## Prerequisites

**Required Knowledge**:
- Understanding of RAG (Retrieval-Augmented Generation) systems and vector databases
- Knowledge of Salesforce APIs (REST, Bulk, Metadata, CDC)
- Familiarity with data extraction and transformation patterns
- Understanding of LLM embeddings and vector similarity search
- Knowledge of chunking strategies for document retrieval
- Experience with data pipeline architectures (ETL, event-driven)

**Recommended Reading**:
- `rag/integrations/change-data-capture-patterns.md` - CDC event processing
- `rag/integrations/etl-vs-api-vs-events.md` - Integration pattern selection
- `rag/security/salesforce-llm-data-governance.md` - Data governance for LLM systems
- `rag/data-modeling/data-migration-patterns.md` - Data migration strategies

## Conceptual Architecture

### Core Stages: Extract → Transform → Index → Retrieve

The fundamental pipeline consists of four stages:

1. **Extract**: Pull data and metadata from Salesforce via APIs
2. **Transform**: Normalize, enrich, and structure data for LLM consumption
3. **Index**: Generate embeddings and store in vector database for RAG
4. **Retrieve**: Query vector store to retrieve relevant context for LLM

### Common Architectural Variants

#### Batch Export (Nightly/Periodic)

**Pattern**: Scheduled full or incremental data extraction on a fixed schedule.

**Characteristics**:
- Scheduled execution (nightly, weekly, hourly)
- Full data dumps or incremental updates
- Bulk API for high-volume extraction
- File-based staging for very large datasets

**Pros**:
- Predictable resource usage
- Efficient for large volumes
- Can run during off-peak hours
- Simpler error recovery (retry entire batch)

**Cons**:
- Not real-time (data may be stale)
- Requires job scheduling infrastructure
- May miss rapid changes between runs
- Full refreshes can be resource-intensive

**Use Cases**:
- Initial RAG index population
- Periodic knowledge base refresh
- Large-scale data migration to LLM systems
- Non-time-sensitive use cases

#### Event-Driven (Change Data Capture or Events)

**Pattern**: Real-time or near-real-time updates triggered by Salesforce change events.

**Characteristics**:
- Change Data Capture (CDC) events or Platform Events
- Event-driven architecture with publish-subscribe pattern
- Real-time or near-real-time processing
- Event stream processing

**Related**: [Change Data Capture Patterns](integrations/change-data-capture-patterns.html) - Complete CDC patterns guide

**Pros**:
- Real-time data freshness
- Efficient incremental updates
- Event-driven decoupling
- Scales with event volume

**Cons**:
- Requires event subscription infrastructure
- May generate high event volume
- Event retention limits (24 hours for standard events)
- More complex error handling and retry logic

**Use Cases**:
- Real-time RAG updates for frequently changing data
- Event-driven LLM knowledge base refresh
- Maintaining LLM system in sync with Salesforce
- Time-sensitive use cases

#### On-Demand Query (Tool-Style Calls)

**Pattern**: LLM agent queries Salesforce directly during conversation via API calls.

**Characteristics**:
- Direct API calls from LLM agent to Salesforce
- Query generation from natural language
- Real-time data retrieval
- Tool/function calling pattern

**Pros**:
- Always current data (no stale data)
- No extraction pipeline needed
- Flexible query patterns
- Direct integration with LLM agents

**Cons**:
- API rate limits and governor limits
- Requires query generation logic
- Network latency per query
- Security model evaluation per query

**Use Cases**:
- LLM agents that need real-time data
- Ad-hoc queries during conversations
- Tool-style function calling
- When data freshness is critical

## Salesforce Data Sources for LLMs

### Types of Data

#### Structured Objects/Fields

**What**: Standard and custom object records with field values.

**When Useful**:
- Core business data (Accounts, Contacts, Cases, Opportunities)
- Status and state information
- Descriptive fields (Name, Description, Notes)
- Relationship data (lookup and master-detail relationships)

**Typical Use in RAG**:
- Record-level chunks for entity understanding
- Relationship-aware chunks for context assembly
- Status and state information for reasoning

#### Metadata (Schema and Labels)

**What**: Object definitions, field metadata, validation rules, relationship definitions.

**When Useful**:
- LLM needs to understand Salesforce schema
- Query generation from natural language
- Schema-aware reasoning
- Validation of LLM-generated queries

**Typical Use in RAG**:
- Schema metadata for LLM understanding
- Field labels and help text for context
- Validation rules for constraint understanding
- Relationship definitions for traversal

#### Documents/Content (Files, Articles, Attachments)

**What**: Files, Knowledge articles, ContentVersion records, attachments.

**When Useful**:
- Document-based RAG systems
- Knowledge base articles
- File attachments with relevant content
- Rich text fields with formatted content

**Typical Use in RAG**:
- Document chunks for document retrieval
- Knowledge article chunks
- File content extraction and chunking
- Rich text field content

#### Logs/Events (If Relevant)

**What**: Platform Events, Change Data Capture events, audit logs.

**When Useful**:
- Event-driven RAG updates
- Temporal reasoning about changes
- Audit trail understanding
- Change history analysis

**Typical Use in RAG**:
- Event-driven incremental updates
- Change history chunks
- Temporal context for reasoning

### Typical Combinations Used in Real RAG Systems

**Pattern 1: Schema + Records**
- Schema metadata for understanding
- Record data for content
- Common for general-purpose RAG systems

**Pattern 2: Records + Relationships**
- Record data with relationship traversal
- Contextual chunks with related records
- Common for entity-centric RAG systems

**Pattern 3: Schema + Records + Documents**
- Comprehensive RAG with all data types
- Schema for understanding, records for content, documents for additional context
- Common for knowledge base RAG systems

## Extraction Patterns

### Overview of Extraction APIs

#### REST/Composite APIs

**Characteristics**:
- Synchronous request/response
- Real-time or near-real-time extraction
- Direct query of objects, fields, and relationships
- Supports SOQL and SOSL queries

**Use Cases**:
- Real-time RAG updates
- Targeted extraction of specific objects
- Custom extraction logic for complex data models
- On-demand query patterns

**Limitations**:
- API rate limits (24-hour rolling window, concurrent request limits)
- Requires careful query optimization to avoid governor limits
- May not capture all metadata dependencies automatically

#### Bulk API

**Characteristics**:
- Asynchronous job-based processing
- High-volume data extraction (millions of records)
- Efficient for full data dumps or large incremental syncs
- Supports CSV, JSON, or XML output formats

**Use Cases**:
- Initial RAG index population
- Periodic full refresh of LLM knowledge base
- Large-scale data migration to LLM systems

**Limitations**:
- Not real-time (jobs run asynchronously)
- Requires job status polling
- May need chunking for very large datasets

#### Metadata/Tooling APIs (For Schema)

**Characteristics**:
- Extracts object definitions, field metadata, relationships
- Captures validation rules, workflows, process builders
- Includes custom settings and custom metadata types
- Provides structural understanding of data model

**Use Cases**:
- Building LLM understanding of Salesforce schema
- Generating documentation for RAG systems
- Creating manifest files for connector tools

**Limitations**:
- Does not include actual record data
- May not capture all runtime behaviors
- Requires separate extraction for record data

#### Change Data Capture / Event-Based Updates

**Characteristics**:
- Real-time or near-real-time data change notifications
- Event-driven architecture with publish-subscribe pattern
- Captures create, update, delete, and undelete operations
- Supports filtering by object type and field changes

**Use Cases**:
- Incremental RAG updates for real-time systems
- Event-driven LLM knowledge base refresh
- Maintaining LLM system in sync with Salesforce

**Limitations**:
- Requires event subscription infrastructure
- May generate high event volume
- Event retention limits (24 hours for standard events)

### Patterns to Feed RAG

#### Full Loads vs Incremental Loads

**Full Loads**:
- Extract all records from selected objects
- Use for initial index population
- Periodic full refresh to ensure consistency
- Pros: Complete data, simpler logic
- Cons: Resource-intensive, slower

**Incremental Loads**:
- Extract only changed records since last extraction
- Use timestamp-based or event-based change tracking
- Pros: Efficient, faster, less resource-intensive
- Cons: More complex logic, requires change tracking

#### Snapshots vs CDC-Based Approaches

**Snapshots**:
- Periodic full data snapshots
- Point-in-time data representation
- Pros: Simple, consistent state
- Cons: May miss rapid changes, resource-intensive

**CDC-Based Approaches**:
- Change event-driven incremental updates
- Real-time or near-real-time updates
- Pros: Always current, efficient
- Cons: Complex event handling, event retention limits

### Tradeoffs

**Performance and Limits**:
- API rate limits constrain extraction frequency
- Governor limits constrain query complexity
- Bulk API more efficient for large volumes
- REST API more flexible for targeted extraction

**Complexity**:
- Full loads simpler but resource-intensive
- Incremental loads more complex but efficient
- Event-driven more complex but real-time
- On-demand simplest but limited by rate limits

**Data Freshness**:
- Batch: Stale data between runs
- Event-driven: Real-time freshness
- On-demand: Always current

**Operational Risk**:
- Lock contention with high-volume extraction
- API limit exhaustion
- Error recovery complexity
- Data consistency challenges

## Transformation & Chunking for RAG

### Strategies for Modeling Salesforce Data as RAG "Documents"

#### Per-Record Chunks vs Aggregated "Logical Documents"

**Per-Record Chunks**:
- One chunk per Salesforce record
- Simple and straightforward
- Pros: Easy to implement, clear boundaries
- Cons: May lose relationship context

**Aggregated Logical Documents**:
- Multiple related records in one chunk (e.g., Account + Contacts)
- Preserves relationship context
- Pros: Richer context, relationship-aware
- Cons: Larger chunks, more complex logic

#### Per-Object vs Cross-Object Chunks

**Per-Object Chunks**:
- Chunks organized by object type
- Simple organization
- Pros: Easy to filter and retrieve
- Cons: May miss cross-object relationships

**Cross-Object Chunks**:
- Chunks include related records from multiple objects
- Preserves cross-object context
- Pros: Richer context, relationship-aware
- Cons: More complex chunking logic

### Chunking Strategies

#### Field Selection and Redaction

**What to Include**:
- Descriptive fields (Name, Description, Notes, Comments)
- Status fields (Status, Stage, State)
- Relationship context (related record names)
- Temporal fields (Created Date, Last Modified Date)

**What to Exclude**:
- System fields (unless relevant)
- Audit fields (unless user context needed)
- Technical fields (encryption keys, configuration)
- Large binary data (unless specifically needed)

#### Flattening Relationships into Text

**Pattern**: Include related record information as text in chunks.

**Example**:
```
Account: Acme Corp
Industry: Technology
Related Contacts: John Doe (Primary), Jane Smith (Billing)
Related Cases: Case #12345 (Open), Case #12346 (Closed)
```

**Pros**: Preserves relationship context in text
**Cons**: May create large chunks, relationship structure lost

#### Using Natural-Language Labels and Metadata

**Pattern**: Include field labels, help text, and metadata for better retrieval.

**Example**:
```
Object: Account
Field: AnnualRevenue
Label: Annual Revenue
Help Text: The company's annual revenue in USD
Value: $1,000,000
```

**Pros**: Better semantic understanding, improved retrieval
**Cons**: Increases chunk size, more metadata to manage

### Example Patterns

#### "Case-Centric Document" Pattern

**Structure**: Case record with related Account, Contact, and Case Comments.

**Chunk Content**:
- Case fields (Subject, Description, Status, Priority)
- Related Account information (Name, Industry)
- Related Contact information (Name, Email)
- Case Comments (recent comments as text)

**Use Case**: Support agent RAG system for case understanding

#### "Student Lifecycle" Pattern (Conceptual, Anonymized)

**Structure**: Student record with related Program Enrollment, Course Enrollment, and Application records.

**Chunk Content**:
- Student information (Name, Email, Status)
- Program Enrollment (Program Name, Status, Start Date)
- Course Enrollment (Course Name, Grade, Status)
- Application information (Application Status, Decision)

**Use Case**: Education RAG system for student information

## Interaction With Manifests

### How Manifest-Style Descriptions Work

Manifest-style descriptions (e.g., tool manifests, connector manifests) typically describe:

- **Tools/Endpoints**: Available API endpoints or tools
- **Parameters**: Input/output parameters for each tool
- **Auth**: Authentication and authorization requirements
- **High-Level Descriptions**: Natural language descriptions of tool capabilities

### Why That Is Not Sufficient

Manifest-style descriptions are **not sufficient** to define:

#### Full Data Pipelines

**Gap**: Manifests describe individual tools/endpoints, not end-to-end pipelines.

**What's Missing**:
- Extraction orchestration (which objects, when, how)
- Transformation logic (chunking, enrichment, normalization)
- Indexing strategy (embedding generation, vector store organization)
- Refresh strategy (incremental vs full, scheduling)

#### Chunking Strategies

**Gap**: Manifests don't define how to chunk Salesforce data for RAG.

**What's Missing**:
- Chunk boundaries (per-record vs aggregated)
- Field selection and redaction rules
- Relationship inclusion strategies
- Metadata embedding approaches

#### Security and Governance Requirements

**Gap**: Manifests don't capture security model evaluation and governance.

**What's Missing**:
- Field-level security (FLS) evaluation
- Object-level security (OLS) evaluation
- Sharing rule understanding
- Data retention policies
- Audit trail requirements

## Sources Used

- **Salesforce REST API Developer Guide**: [https://developer.salesforce.com/docs/atlas.en-us.api_rest.meta/api_rest/](https://developer.salesforce.com/docs/atlas.en-us.api_rest.meta/api_rest/)
  - REST API endpoints for data extraction
  - Authentication and rate limiting
  - Query and search capabilities

- **Salesforce Bulk API Developer Guide**: [https://developer.salesforce.com/docs/atlas.en-us.api_asynch.meta/api_asynch/](https://developer.salesforce.com/docs/atlas.en-us.api_asynch.meta/api_asynch/)
  - Bulk data extraction patterns
  - Asynchronous job processing
  - High-volume data operations

- **Salesforce Metadata API Developer Guide**: [https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/](https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/)
  - Schema metadata extraction
  - Object and field definitions
  - Custom metadata types

- **Change Data Capture Developer Guide**: [https://developer.salesforce.com/docs/atlas.en-us.change_data_capture.meta/change_data_capture/](https://developer.salesforce.com/docs/atlas.en-us.change_data_capture.meta/change_data_capture/)
  - Real-time data change events
  - Event subscription and processing
  - Incremental data extraction

- **LangChain Documentation**: [https://python.langchain.com/](https://python.langchain.com/)
  - RAG implementation patterns
  - Vector store integration
  - Document chunking strategies

- **LlamaIndex Documentation**: [https://docs.llamaindex.ai/](https://docs.llamaindex.ai/)
  - Data ingestion patterns
  - Index construction and querying
  - Custom data connectors

## To Evaluate

- **Event Retention Limits**: Standard Change Data Capture events have 24-hour retention. Need to evaluate if this is sufficient for all use cases or if custom events are needed.

- **Chunking Strategy Selection**: Best practices for choosing per-record vs aggregated chunking are not yet standardized. May depend on specific use case and LLM model capabilities.

- **On-Demand Query Performance**: Tradeoffs between on-demand queries and pre-indexed RAG for LLM agents need more real-world validation.

- **Hybrid Pattern Complexity**: Combining multiple extraction patterns (batch + event-driven + on-demand) adds complexity. Need to evaluate when the benefits outweigh the complexity.

- **Metadata Extraction Completeness**: Whether Metadata API captures all necessary schema information for LLM understanding, or if additional sources are needed.

## Q&A

### Q: What is a Salesforce to LLM data pipeline?

**A**: A **Salesforce to LLM data pipeline** extracts, transforms, and loads Salesforce data and metadata into LLM-powered systems (RAG, tools, agents). The pipeline consists of four stages: (1) **Extract** - pull data/metadata from Salesforce via APIs, (2) **Transform** - normalize, enrich, structure data for LLM consumption, (3) **Index** - generate embeddings and store in vector database for RAG, (4) **Retrieve** - query vector store to retrieve relevant context for LLM.

### Q: What extraction APIs should I use for Salesforce to LLM pipelines?

**A**: Use extraction APIs based on requirements: (1) **REST/Composite APIs** - real-time extraction, targeted queries, (2) **Bulk API** - high-volume extraction (millions of records), initial index population, (3) **Metadata/Tooling APIs** - schema extraction (object definitions, field metadata), (4) **Change Data Capture (CDC)** - real-time incremental updates, event-driven refresh. Choose based on volume, freshness requirements, and use case.

### Q: What is the difference between full loads and incremental loads?

**A**: **Full loads** extract all records from selected objects (initial index population, periodic full refresh). **Incremental loads** extract only changed records since last extraction (timestamp-based or event-based). Full loads: complete data, simpler logic, but resource-intensive. Incremental loads: efficient, faster, but more complex logic requiring change tracking.

### Q: How do I chunk Salesforce data for RAG systems?

**A**: Chunk Salesforce data by: (1) **Per-record chunks** - one chunk per record (simple, clear boundaries), (2) **Aggregated logical documents** - multiple related records in one chunk (Account + Contacts, preserves relationships), (3) **Field selection** - include descriptive fields (Name, Description, Status), exclude system/technical fields, (4) **Flattening relationships** - include related record info as text, (5) **Natural-language labels** - include field labels and help text for better retrieval.

### Q: What should I include in RAG chunks from Salesforce?

**A**: Include in chunks: (1) **Descriptive fields** (Name, Description, Notes, Comments), (2) **Status fields** (Status, Stage, State), (3) **Relationship context** (related record names), (4) **Temporal fields** (Created Date, Last Modified Date), (5) **Field labels and help text** (better semantic understanding). Exclude: system fields, audit fields, technical fields, large binary data (unless needed).

### Q: What are the tradeoffs between batch and event-driven extraction?

**A**: **Batch extraction** (nightly/periodic): predictable resource usage, efficient for large volumes, can run off-peak, simpler error recovery, but data may be stale, requires job scheduling. **Event-driven extraction** (CDC-based): real-time freshness, efficient incremental updates, but complex event handling, event retention limits (24 hours), requires event subscription infrastructure.

### Q: How do I handle security and governance in LLM data pipelines?

**A**: Handle security by: (1) **Evaluating Field-Level Security (FLS)** - respect FLS when extracting data, (2) **Evaluating Object-Level Security (OLS)** - respect object access, (3) **Understanding sharing rules** - consider sharing model, (4) **Data retention policies** - comply with retention requirements, (5) **Audit trail requirements** - track data extraction, (6) **Redacting sensitive data** - exclude PII/PHI if not needed. Security evaluation is critical for compliance.

### Q: What is the difference between per-record and aggregated chunking?

**A**: **Per-record chunking** creates one chunk per Salesforce record (simple, clear boundaries, but may lose relationship context). **Aggregated chunking** includes multiple related records in one chunk (Account + Contacts, preserves relationships, richer context, but larger chunks, more complex logic). Choose based on use case - per-record for simple retrieval, aggregated for relationship-aware retrieval.

### Q: How do I choose between REST API, Bulk API, and CDC for extraction?

**A**: Choose based on: (1) **REST API** - real-time, targeted extraction, flexible queries, but rate limits, (2) **Bulk API** - high-volume (millions of records), efficient for full loads, but not real-time, requires job polling, (3) **CDC** - real-time incremental updates, event-driven, but event retention limits, complex event handling. Use REST for on-demand, Bulk for initial/full loads, CDC for real-time incremental.

### Q: What are best practices for Salesforce to LLM pipelines?

**A**: Best practices include: (1) **Choose appropriate extraction API** (REST, Bulk, CDC based on requirements), (2) **Implement chunking strategy** (per-record or aggregated based on use case), (3) **Include relevant fields** (descriptive, status, relationships), (4) **Respect security model** (FLS, OLS, sharing rules), (5) **Handle errors gracefully** (retry logic, error recovery), (6) **Monitor pipeline health** (extraction metrics, indexing status), (7) **Optimize for retrieval** (chunking, metadata, embeddings).

## Edge Cases and Limitations

### Edge Case 1: Large Object Records with Many Relationships

**Scenario**: Records with extensive relationship data (Account with 100+ Contacts, Cases, Opportunities) creating very large chunks.

**Consideration**:
- Limit relationship depth in aggregated chunks (e.g., only include primary Contacts)
- Use separate chunks for different relationship types
- Implement chunk size limits (e.g., max 2,000 tokens per chunk)
- Prioritize most relevant relationships based on use case
- Consider per-record chunks for very large objects

### Edge Case 2: Real-Time Data Freshness Requirements

**Scenario**: LLM system requires real-time data updates, but CDC events have 24-hour retention limits.

**Consideration**:
- Use Platform Events or custom Change Events for longer retention
- Implement hybrid approach (CDC for recent changes, periodic full refresh)
- Use on-demand query pattern for critical real-time data
- Monitor event retention and implement event replay for missed events
- Consider event buffering and replay mechanisms

### Edge Case 3: Field-Level Security (FLS) Evaluation Complexity

**Scenario**: Extracting data while respecting FLS requires per-user security evaluation, complicating extraction.

**Consideration**:
- Extract data with integration user that has appropriate access
- Evaluate FLS during transformation phase (filter fields per user context)
- Use separate extraction pipelines for different user contexts
- Cache FLS evaluation results to improve performance
- Document FLS assumptions in pipeline configuration

### Edge Case 4: Chunking Strategy Selection for Complex Data Models

**Scenario**: Complex data models with many relationships make chunking strategy selection difficult.

**Consideration**:
- Test different chunking strategies (per-record vs aggregated) with sample data
- Measure retrieval quality (precision, recall) for different strategies
- Consider use case requirements (entity-centric vs relationship-aware)
- Use hybrid approach (per-record for simple objects, aggregated for complex)
- Profile chunk sizes and adjust based on embedding model limits

### Edge Case 5: Embedding Model Token Limits

**Scenario**: Chunks exceed embedding model token limits (e.g., 8,192 tokens for some models).

**Consideration**:
- Implement chunk size limits based on embedding model token limits
- Split large chunks into smaller sub-chunks
- Use sliding window approach for very long text fields
- Truncate or summarize very long fields before chunking
- Monitor chunk token counts during transformation

### Edge Case 6: Incremental Update Complexity

**Scenario**: Updating RAG index incrementally requires complex change tracking and partial index updates.

**Consideration**:
- Use CDC events to identify changed records for incremental updates
- Implement change tracking (timestamp-based or event-based)
- Handle record deletions (remove chunks from index)
- Support partial index updates (update specific chunks, not full rebuild)
- Test incremental update logic thoroughly before production

### Limitations

- **API Rate Limits**: REST API has 24-hour rolling window limits and concurrent request limits
- **Bulk API Job Limits**: Bulk API jobs have size limits and require asynchronous processing
- **CDC Event Retention**: Standard CDC events have 24-hour retention limits
- **Embedding Model Limits**: Embedding models have token limits (typically 512-8,192 tokens)
- **Vector Database Capacity**: Vector databases have storage and query performance limits
- **Chunking Strategy Tradeoffs**: Per-record chunks lose relationship context, aggregated chunks may be too large
- **Security Model Complexity**: FLS/OLS evaluation adds complexity to extraction and transformation
- **Data Freshness Tradeoffs**: Real-time extraction requires more complex infrastructure, batch extraction may have stale data
- **On-Demand Query Limits**: Direct API queries are limited by rate limits and governor limits
- **Metadata Extraction Completeness**: Metadata API may not capture all runtime behaviors or custom logic

## Related Patterns

- [Change Data Capture Patterns](integrations/change-data-capture-patterns.html) - CDC event processing
- [ETL vs API vs Events](integrations/etl-vs-api-vs-events.html) - Integration pattern selection
- [Integration Platform Patterns](integrations/integration-platform-patterns.html) - ETL platform patterns
- [Salesforce LLM Data Governance](security/salesforce-llm-data-governance.html) - Data governance for LLM systems

