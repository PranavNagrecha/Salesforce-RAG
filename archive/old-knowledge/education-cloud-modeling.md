# Education Cloud Data Modeling

## What Was Actually Done

The Salesforce Education Cloud (EDA) data model was customized to support higher education institutions, with particular focus on online and adult-learning programs. The model integrates with legacy student information systems (SIS) while supporting CRM workflows for admissions and student engagement.

### Core Data Model Decisions

- **Contact as Core Student/Applicant Record**: Contacts serve as the primary person record for students and applicants
- **Program Enrollment Objects**: Education Cloud Program Enrollment and Course Enrollment objects represent academic participation
- **Application Objects**: Custom or standard Application objects represent one or multiple applications per student
- **Account for Programs**: Accounts may represent academic programs or institutions depending on the data model approach

### Program and Enrollment Modeling

Program enrollments were modeled to support:

- Program modalities (online, hybrid, in-person) as fields or Record Types
- Program levels (undergraduate, graduate, non-degree) for categorization
- Special program types (accelerated, cohort-based) as flags or fields
- Enrollment status and history tracking
- Term and section data mapping from SIS

### Application Tracking

Application objects were designed to support:

- Multiple applications per student (different programs, different terms)
- Application status tracking (submitted, under review, admitted, enrolled, withdrawn)
- Program-specific metadata (program type, modality, term)
- Application checklists and required documents
- Automated advisor task generation based on application status

### SIS Integration Data Model

The data model was designed to align with SIS structures:

- External IDs mirroring SIS primary keys (e.g., EMPLID for students)
- Composite external IDs on Account for SIS program-based records (Institution + Program + Effective Date)
- Timestamp and job-tracking fields for ETL runs
- Derived fields like "last three enrolled terms" computed from SIS data

### Custom Fields and Structures

Custom fields were added to support:

- Non-degree application types
- Application types for specific program groupings (e.g., "hybrid program" logic)
- Derived fields computed from SIS data
- Integration tracking fields (last sync timestamp, sync status, job ID)

## Rules and Patterns

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
- Use composite external IDs on Account when SIS uses multi-column keys (Institution + Program + Effective Date)
- Include timestamp fields to track last sync time
- Implement job tracking fields to correlate Salesforce records with SIS sync jobs
- Document external ID strategy for each integrated object

### Derived Field Patterns

- Compute derived fields from related records (e.g., "last three enrolled terms" from Program Enrollment records)
- Use formula fields for simple calculations
- Use Apex or Flow for complex derived fields that require aggregation
- Cache derived fields in custom fields if computation is expensive
- Update derived fields when source data changes

## Suggested Improvements (From AI)

### Enhanced Enrollment Modeling

Consider more sophisticated enrollment modeling:
- Support enrollment history with effective dates
- Track enrollment changes over time (status changes, program transfers)
- Model prerequisite and co-requisite relationships
- Support waitlist and enrollment capacity management

### Application Workflow Modeling

Enhance application workflow modeling:
- Model application stages and transitions explicitly
- Support parallel application processes (multiple programs simultaneously)
- Track application milestones and deadlines
- Automate application routing and assignment

### Academic Structure Modeling

Model academic structures more comprehensively:
- Represent course catalogs and course prerequisites
- Model term and academic calendar structures
- Support program requirements and degree plans
- Track academic progress and completion status

### Integration Data Quality

Enhance integration data quality:
- Validate SIS data before importing to Salesforce
- Handle data inconsistencies and missing data gracefully
- Implement data quality checks for critical fields
- Create data quality reports for review

## To Validate

- Specific Education Cloud object customizations and field additions
- External ID field names and composite key structures
- Derived field calculation logic and update triggers
- Application object structure and status workflow
- Program Enrollment customizations and related objects
- SIS integration field mappings and transformation rules

