# Student Lifecycle Data Model

## Overview

The Salesforce Education Cloud (EDA) data model supports higher education institutions, with particular focus on online and adult-learning programs. The model integrates with legacy student information systems (SIS) while supporting CRM workflows for admissions and student engagement.

## Core Data Model Decisions

### Contact as Core Student/Applicant Record

**Decision**: Contacts serve as the primary person record for students and applicants

**Rationale**:
- Consistent person record across all Education Cloud implementations
- Supports both applicants and enrolled students
- Enables relationship modeling with programs and institutions
- Aligns with Education Cloud standard model

**Implementation**:
- Store student identifiers (SIS ID, external ID) on Contact
- Link Contacts to Accounts (programs, institutions) through relationships
- Use Record Types to differentiate between applicant, student, alumni if needed
- External IDs mirror SIS primary keys (e.g., EMPLID)

### Program Enrollment Objects

**Decision**: Use Education Cloud Program Enrollment and Course Enrollment objects

**Implementation**:
- Program Enrollment for program-level enrollments
- Course Enrollment for course-level enrollments if needed
- Track enrollment status, start date, end date, and related academic information
- Link enrollments to Contacts (students) and Accounts (programs)
- Support multiple active enrollments per student if institution allows

### Application Objects

**Decision**: Custom or standard Application objects represent one or multiple applications per student

**Implementation**:
- Design Application objects to support multiple applications per student (different programs, different terms)
- Include fields for application status, program, term, and modality
- Link applications to Contacts (applicants) and Accounts (programs)
- Support application checklists and required documents
- Track application submission date and decision date

### Account for Programs

**Decision**: Accounts represent academic programs or institutions depending on the data model approach

**Implementation**:
- Use Accounts to represent programs or institutions
- Support program hierarchies if needed
- Link to Contacts through Program Enrollment relationships
- Use composite external IDs when SIS uses multi-column keys

## Program and Enrollment Modeling

### Program Modalities

**Fields or Record Types** for:

- Online programs
- Hybrid programs
- In-person programs

**Implementation**: Use fields or Record Types to differentiate program delivery modes

### Program Levels

**Fields** for categorization:

- Undergraduate
- Graduate
- Non-degree programs

**Implementation**: Use picklist fields or Record Types to categorize program levels

### Special Program Types

**Flags or fields** for:

- Accelerated programs
- Cohort-based programs
- Special program groupings

**Implementation**: Use boolean flags or picklist fields to identify special program characteristics

### Enrollment Status and History

**Tracking**:

- Enrollment status (active, completed, withdrawn)
- Enrollment history tracking
- Term and section data mapping from SIS
- Effective dates for time-versioned records

## Application Tracking

### Multiple Applications Per Student

**Support**:

- Different programs
- Different terms
- Different application types
- Application history tracking

### Application Status Tracking

**Statuses**:

- Submitted
- Under review
- Admitted
- Enrolled
- Withdrawn

**Implementation**: Use picklist fields or Record Types to track application status

### Program-Specific Metadata

**Fields**:

- Program type
- Modality (online, hybrid, in-person)
- Term
- Application type

### Application Checklists

**Support**:

- Required documents
- Milestone tracking
- Automated advisor task generation based on application status
- Document submission tracking

## SIS Integration Data Model

### External ID Strategy

**Pattern**: External IDs mirror SIS primary keys

- Use SIS primary keys (e.g., EMPLID) as external IDs on Contact
- Use composite external IDs on Account when SIS uses multi-column keys
- Include timestamp fields to track last sync time
- Implement job tracking fields to correlate Salesforce records with SIS sync jobs

### Composite External IDs

**Pattern**: Account-level external IDs using composite keys

- Example: Institution + Program + Effective Date
- Concatenate component fields with delimiter (pipe `|` or dash `-`)
- Ensure delimiter doesn't appear in component field values
- Handle null values in component fields appropriately
- Support effective-dated records where the same logical record has multiple versions over time

### Integration Job Tracking Fields

**Standard fields** on all integrated objects:

- `Last_Sync_Timestamp__c` (DateTime) - when record was last synced
- `Last_Sync_Status__c` (Picklist: Success, Error, In Progress) - sync job status
- `Last_Sync_Error__c` (Long Text Area) - error message if sync failed
- `Integration_Job_ID__c` (Text) - correlation ID with external system
- `Record_Source__c` (Picklist: Integration, Manual Entry, Migration) - how record was created

### Derived Fields

**Pattern**: Computed fields from SIS data

- Example: "last three enrolled terms" computed from Program Enrollment records
- Use formula fields for simple calculations
- Use Apex or Flow for complex derived fields that require aggregation
- Cache derived fields in custom fields if computation is expensive
- Update derived fields when source data changes

## Custom Fields and Structures

### Non-Degree Application Types

**Support**:

- Non-degree program applications
- Certificate programs
- Continuing education

### Application Types for Program Groupings

**Support**:

- Hybrid program logic
- Special program groupings
- Program-specific application workflows

### Derived Fields from SIS Data

**Examples**:

- Last three enrolled terms
- Academic standing
- Credit hours completed
- GPA calculations

## Best Practices

### Contact as Primary Person Record

- Use Contact as the core student/applicant record across all Education Cloud implementations
- Store student identifiers (SIS ID, external ID) on Contact
- Link Contacts to Accounts (programs, institutions) through relationships
- Use Record Types to differentiate between applicant, student, alumni if needed

### Program Enrollment Modeling

- Use Education Cloud Program Enrollment object for program-level enrollments
- Use Course Enrollment for course-level enrollments if needed
- Track enrollment status, start date, end date, and related academic information
- Link enrollments to Contacts (students) and Accounts (programs)
- Support multiple active enrollments per student if institution allows

### Application Object Design

- Design Application objects to support multiple applications per student
- Include fields for application status, program, term, and modality
- Link applications to Contacts (applicants) and Accounts (programs)
- Support application checklists and required documents
- Track application submission date and decision date

### External ID Strategy for SIS Integration

- Use SIS primary keys (e.g., EMPLID) as external IDs on Contact
- Use composite external IDs on Account when SIS uses multi-column keys
- Include timestamp fields to track last sync time
- Implement job tracking fields to correlate Salesforce records with SIS sync jobs
- Document external ID strategy for each integrated object

### Derived Field Patterns

- Compute derived fields from related records (e.g., "last three enrolled terms" from Program Enrollment records)
- Use formula fields for simple calculations
- Use Apex or Flow for complex derived fields that require aggregation
- Cache derived fields in custom fields if computation is expensive
- Update derived fields when source data changes

## Tradeoffs

### Advantages

- Aligns with Education Cloud standard model
- Supports both applicants and enrolled students
- Enables relationship modeling with programs
- Integrates well with SIS systems

### Challenges

- Requires careful external ID management
- Derived fields need maintenance
- Multiple applications per student adds complexity
- Enrollment history tracking can be complex

## When to Use This Model

Use this data model when:

- Implementing Education Cloud for higher education
- Integrating with legacy SIS systems
- Supporting both applicants and enrolled students
- Need to track program enrollments and applications
- Require SIS synchronization

## When Not to Use This Model

Avoid this model when:

- Simple contact management only
- No SIS integration required
- No program enrollment tracking needed
- Different data model requirements exist

