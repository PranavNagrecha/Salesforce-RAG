# Salesforce Data Scope & Security for LLMs

## Overview

This document covers how to choose *what* data to expose from Salesforce to LLMs and how to do that safely. It addresses scoping strategy (which objects, fields, and records to include), security considerations (how to reflect Salesforce access controls in LLM data extraction), data masking and redaction strategies, and governance and lifecycle management.

## Data Scoping Principles

### Criteria for Including/Excluding Data

#### Relevance to RAG/LLM Use Cases

**Include When**:
- Data provides context for answering questions
- Data enables relationship understanding
- Data supports temporal reasoning
- Data enables status and state understanding

**Exclude When**:
- Data doesn't contribute to LLM understanding
- Data is redundant or derivable
- Data increases token usage without value
- Data is operational/technical only

#### Sensitivity and PII/PHI

**Include When**:
- Data is necessary for LLM use case
- Data can be safely masked or redacted
- Data classification allows inclusion
- Compliance requirements are met

**Exclude When**:
- Data contains sensitive PII/PHI that cannot be masked
- Data classification prohibits inclusion
- Compliance requirements cannot be met
- Data exposure risk outweighs utility

#### Data Volume and Performance Constraints

**Include When**:
- Data volume is manageable
- Extraction performance is acceptable
- Storage costs are reasonable
- Processing costs are acceptable

**Exclude When**:
- Data volume is too large for efficient processing
- Extraction performance is unacceptable
- Storage costs are prohibitive
- Processing costs outweigh benefits

### Approaches to Selecting

#### Core Business Data

**What**: Primary business entities and their key attributes.

**Examples**:
- Accounts (Name, Industry, Annual Revenue)
- Contacts (Name, Email, Role)
- Cases (Subject, Description, Status, Priority)
- Opportunities (Name, Amount, Stage, Close Date)

**Rationale**: Core business data provides essential context for most LLM use cases.

#### Supporting Context

**What**: Related records and metadata that provide additional context.

**Examples**:
- Related Contacts for Accounts
- Case Comments and Activities
- Opportunity Products
- Account Hierarchy

**Rationale**: Supporting context enriches understanding but may not be essential for all use cases.

#### Excluded/Sanitized Fields

**What**: Fields that are excluded entirely or sanitized before inclusion.

**Examples**:
- SSN, Credit Card Numbers (excluded or fully masked)
- Passwords, API Keys (excluded)
- Internal Notes (may be sanitized)
- Audit Fields (excluded unless relevant)

**Rationale**: Sensitive data must be excluded or sanitized to meet security and compliance requirements.

## Mapping Salesforce Security to LLM Access

### How to Interpret

#### Field-Level Security (FLS)

**What It Means**: Users may not have read access to certain fields.

**For LLM Extraction**:
- Evaluate FLS for extraction user context
- Only extract fields the user can access
- Handle FLS-restricted fields gracefully
- Document FLS restrictions

**Implementation**: Query FLS metadata and filter fields based on accessibility.

#### Object Permissions

**What It Means**: Users may not have read access to certain objects.

**For LLM Extraction**:
- Evaluate object permissions for extraction user
- Skip objects the user cannot access
- Handle object access errors gracefully
- Document object permission requirements

**Implementation**: Query object permissions and skip inaccessible objects.

#### Sharing Rules and Org-Wide Defaults

**What It Means**: Record visibility is determined by sharing rules, not just object permissions.

**For LLM Extraction**:
- Understand that SOQL queries automatically respect sharing rules (in user context)
- Use appropriate user context for extraction
- Document sharing rules that affect extraction scope
- Recognize that sharing rules may limit data completeness

**Implementation**: Use user context (not system context) to respect sharing rules automatically.

### Strategies for

#### Extracting Data Under a Constrained Service Account

**Pattern**: Use dedicated service account with minimal required permissions.

**Benefits**:
- Consistent permission model
- Clear audit trail
- Easier permission management
- Security isolation

**Considerations**:
- Service account needs appropriate permissions for extraction scope
- May not respect user-specific sharing rules
- May extract more data than individual users can see

**Use When**: Extracting data for general-purpose RAG system, not user-specific.

#### User-Context Extraction

**Pattern**: Extract data in context of specific user to respect their permissions.

**Benefits**:
- Respects user's FLS/OLS permissions
- Respects user's sharing rules
- Enables personalized RAG systems
- Matches user's actual data visibility

**Considerations**:
- May require per-user extraction
- More complex extraction logic
- May impact performance with many users

**Use When**: Extracting data for user-specific RAG systems or personalized experiences.

#### Maintaining Consistent Access Rules in the RAG/LLM Layer

**Challenge**: RAG/LLM layer doesn't automatically inherit Salesforce security.

**Strategies**:
- **Separate Indexes**: Create separate indexes per audience/role
- **Attribute-Based Filtering**: Filter at query time based on user attributes
- **Metadata Filtering**: Use metadata to filter chunks based on access rules
- **Post-Retrieval Filtering**: Filter retrieved chunks based on access rules

**Tradeoffs**:
- Separate indexes: More storage, better performance, clearer security
- Attribute-based filtering: Less storage, more complex queries, runtime filtering
- Metadata filtering: Moderate storage, query-time filtering, requires metadata design
- Post-retrieval filtering: Simple, but may retrieve irrelevant chunks

## Approaches to Enforcing Security in RAG

### Index Design

#### Separate Indexes Per Audience/Role

**Pattern**: Create separate vector indexes for different user roles or audiences.

**Implementation**:
- Extract data separately for each role
- Create separate indexes per role
- Route queries to appropriate index based on user role

**Pros**:
- Clear security boundaries
- No runtime filtering needed
- Better performance (smaller indexes)
- Easier to audit and manage

**Cons**:
- More storage (multiple indexes)
- More complex extraction (per-role extraction)
- Index maintenance overhead

**Use When**: Clear role-based access patterns, sufficient storage, performance critical.

#### Attribute-Based Filtering at Query Time

**Pattern**: Include access attributes in chunks and filter at query time.

**Implementation**:
- Include access attributes (role, department, etc.) in chunk metadata
- Filter chunks at query time based on user attributes
- Use metadata filters in vector database queries

**Pros**:
- Single index for all users
- Flexible access control
- Less storage than separate indexes
- Easier to update access rules

**Cons**:
- More complex query logic
- Runtime filtering overhead
- Requires careful metadata design
- May retrieve irrelevant chunks

**Use When**: Flexible access patterns, limited storage, access rules change frequently.

### Pros/Cons of Each Approach

**Separate Indexes**:
- ✅ Clear security boundaries
- ✅ Better performance
- ✅ Easier audit
- ❌ More storage
- ❌ More complex extraction

**Attribute-Based Filtering**:
- ✅ Single index
- ✅ Flexible access
- ✅ Less storage
- ❌ Complex queries
- ❌ Runtime overhead

### Potential Pitfalls

#### Over-Sharing Via a Single Global Index

**Risk**: All users query same index, may retrieve chunks they shouldn't see.

**Mitigation**:
- Implement post-retrieval filtering
- Use metadata filtering at query time
- Create separate indexes for sensitive data
- Document and audit access patterns

#### Treating LLM as If It "Inherits" Salesforce Security Automatically

**Risk**: Assuming LLM automatically respects Salesforce security without implementation.

**Reality**: LLM/RAG layer doesn't automatically inherit Salesforce security. Must be implemented explicitly.

**Mitigation**:
- Explicitly implement security in extraction
- Explicitly implement security in indexing
- Explicitly implement security in retrieval
- Document security implementation
- Audit security compliance

## Governance and Lifecycle

### Refresh Cadence

**Strategies**:
- **Real-Time**: Event-driven updates for critical data
- **Near-Real-Time**: Frequent scheduled updates (hourly, every 15 minutes)
- **Batch**: Periodic full refresh (daily, weekly)
- **On-Demand**: Manual or triggered refresh for specific use cases

**Decision Factors**:
- Data change frequency
- LLM use case requirements (real-time vs batch)
- API call costs and system load
- Accuracy requirements (how fresh data needs to be)

### Handling Updates, Corrections, and Deletions

**Updates**:
- Incremental extraction of changed records
- Update existing chunks in vector store
- Handle field-level updates efficiently

**Corrections**:
- Re-extract corrected records
- Update chunks with corrected data
- Maintain correction history if needed

**Deletions**:
- Handle delete change events
- Remove deleted records from vector store
- Cascade deletions for related records if needed
- Maintain deletion audit trail

### Retention and Compliance Considerations (e.g., Data Minimization)

**Data Minimization**:
- Extract only data needed for LLM use cases
- Exclude unnecessary fields and objects
- Implement data retention policies
- Purge expired data from vector store

**Compliance**:
- GDPR: Right to deletion, data minimization
- CCPA: Consumer privacy rights, data minimization
- HIPAA: Protected health information handling
- FERPA: Educational records privacy

**Retention Policies**:
- Define retention periods per data type
- Implement TTL (time-to-live) for chunks
- Purge expired data automatically
- Document retention policies

### Audit Trails

#### What Was Exported

**Track**:
- Which objects were extracted
- Which fields were extracted
- Which records were extracted
- Extraction filters and criteria

**Purpose**: Understand what data is in LLM system, enable compliance reporting.

#### When

**Track**:
- Extraction timestamps
- Refresh timestamps
- Update timestamps
- Deletion timestamps

**Purpose**: Understand data freshness, enable temporal analysis, support compliance.

#### For Which Purpose

**Track**:
- LLM use case (e.g., "support agent RAG", "sales assistant")
- Extraction purpose (e.g., "initial index", "incremental update")
- User context (if user-specific extraction)

**Purpose**: Enable purpose limitation compliance, support governance.

## Concrete Rules

- Always classify fields before export (public, internal, confidential, restricted)
- Always evaluate FLS/OLS at runtime, not just in manifest
- Always implement data minimization (extract only what's needed)
- Always maintain audit trail (what, when, why)
- Always implement retention policies with TTL
- Always mask or exclude sensitive PII/PHI unless explicitly required and compliant
- Never assume LLM inherits Salesforce security automatically
- Always document security implementation and compliance measures

## Sources Used

- **Field-Level Security Documentation**: [https://help.salesforce.com/s/articleView?id=sf.security_field_level_security.htm](https://help.salesforce.com/s/articleView?id=sf.security_field_level_security.htm)
  - FLS concepts and implementation
  - FLS evaluation and inheritance
  - FLS in API queries

- **Object-Level Security Documentation**: [https://help.salesforce.com/s/articleView?id=sf.security_object_permissions.htm](https://help.salesforce.com/s/articleView?id=sf.security_object_permissions.htm)
  - Object permissions and access control
  - Profile and permission set permissions
  - Object access evaluation

- **Sharing Rules Documentation**: [https://help.salesforce.com/s/articleView?id=sf.security_sharing_rules.htm](https://help.salesforce.com/s/articleView?id=sf.security_sharing_rules.htm)
  - Sharing rule types and evaluation
  - Record visibility and access
  - Sharing rule inheritance

- **Change Data Capture Documentation**: [https://developer.salesforce.com/docs/atlas.en-us.change_data_capture.meta/change_data_capture/](https://developer.salesforce.com/docs/atlas.en-us.change_data_capture.meta/change_data_capture/)
  - Real-time data change events
  - Event subscription and processing
  - Incremental data extraction

- **GDPR Compliance**: General Data Protection Regulation requirements for data minimization, purpose limitation, and data subject rights

- **CCPA Compliance**: California Consumer Privacy Act requirements for consumer privacy rights and data minimization

- **HIPAA Compliance**: Health Insurance Portability and Accountability Act requirements for protected health information handling

- **FERPA Compliance**: Family Educational Rights and Privacy Act requirements for educational records privacy

## To Evaluate

- **Legal/Compliance Advice**: Some patterns may require legal or compliance review, especially for regulated industries (healthcare, education, financial services).

- **Regulatory Environment Suitability**: Patterns suitable for one regulatory environment (e.g., GDPR) may need adjustment for others (e.g., HIPAA, FERPA).

- **Attribute-Based Filtering Performance**: Impact of attribute-based filtering on query performance and whether caching strategies are sufficient.

- **Separate Index Storage Costs**: Whether separate indexes per role are cost-effective at scale, or if attribute-based filtering is preferable.

- **Data Minimization Balance**: Finding the right balance between data minimization and LLM utility - too little data may reduce LLM effectiveness, too much may increase risk.

