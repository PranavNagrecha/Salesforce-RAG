# Salesforce Work – Cursor Concrete History Dump

> **Note**: This document is built ONLY from evidence found in this Cursor workspace and all accessible projects. It does NOT pull content from the GPT Response file. This represents what was actually done, thought through, analyzed, and learned in this workspace environment.

---

## Introduction: The Journey from Code to Knowledge

This document represents a comprehensive synthesis of actual Salesforce implementation work, architectural thinking, problem-solving approaches, and the evolution of understanding that occurred across multiple projects. Unlike theoretical knowledge, this captures the concrete reality of building enterprise-scale Salesforce solutions—the decisions I made, the patterns I established, the problems I solved, and the standards I created through real-world experience.

The work documented here spans:

- **Enterprise-scale public sector portals** I built serving 40,000+ concurrent users
- **Higher education CRM implementations** I developed with complex SIS integrations
- **Multi-tenant identity architectures** I designed supporting diverse user communities
- **Comprehensive code review and quality standards** I established through rigorous analysis
- **Lightning Web Components and Apex classes** I wrote to solve specific business problems
- **Data analysis and cleanup scripts** I created to troubleshoot and optimize systems
- **License management tools** I built to make administration easier

---

## 1. Major Project Contexts (From Workspace Evidence)

### 1.1 Public Sector Benefits Portal – MyServices Project

**Type:** Enterprise-scale public sector portal for citizen self-service and case management

**Scale:** 40,000 concurrent users per day

**Main Salesforce Clouds/Features Used:**

- Experience Cloud (multiple portals: Client Portal, Vendor Portal)
- Service Cloud for internal case management
- OmniStudio (OmniScripts and FlexCards) for guided workflows and reusable UI components
- Platform Events for event-driven integrations
- Custom objects for Notice and Transaction tracking
- Multi-identity provider architecture (OIDC, SAML, business-tenant)

**Main External Systems Involved:**

- MuleSoft integration platform (security boundary, transformation layer)
- External benefits/notice generation systems (hosted on VMs)
- State-wide citizen identity provider (OIDC)
- State internal SSO (SAML)
- Business-tenant identity provider for vendor organizations
- External logging platforms (OpenSearch, Splunk discussions)

**Problems Actually Solved:**

- **Identity & SSO:** Multi-identity provider architecture supporting citizens, vendors, and internal staff in single org
- **Integration Architecture:** MuleSoft as security/transformation boundary for VPN/IP whitelisting requirements
- **Case Management:** Custom Notice and Transaction objects tracking external system outputs
- **Portal Architecture:** Experience Cloud sites with OmniStudio components for complex workflows
- **Security & Compliance:** Government Cloud (GovCloud) compliance, FedRAMP-style controls, permission set-driven security
- **Error Handling & Logging:** Comprehensive logging framework using `LOG_LogMessage__c` object and `LOG_LogMessageUtility` class
- **Data Quality:** Field descriptions, help text, picklist conversions, naming standardization

**Key Architectural Decisions:**

- **Permission Set-Driven Security:** Transition from profile-centric to permission set-based model (profiles minimal, permission sets comprehensive)
- **No Delete Permissions:** Removed all delete permissions for community users (data integrity)
- **Named Credentials Over Hardcoded URLs:** Established standard requiring all API endpoints use Named Credentials
- **Error Handling Standard:** All errors must be logged to `LOG_LogMessage__c` object
- **Configuration Over Hardcoding:** Custom Metadata Types for environment-specific URLs and configuration

**Deep Analysis Work:**

- **Sprint 1 Comprehensive Review:** 18-point detailed feedback document covering error handling, logging, security, data dictionary, component quality
- **Error Handling Analysis:** Detailed review of 56 Integration Procedures identifying 53 with `failOnStepError: false` (silent failures)
- **Permission Restructuring Plan:** Complete migration plan moving 406 field permissions from profiles to permission sets
- **OmniStudio Best Practices Review:** Enterprise-scale component review identifying critical issues (hardcoded URLs, missing error states, inactive components)
- **Data Dictionary Analysis:** Field source analysis, picklist conversion recommendations, description quality standards
- **Component Architectural Deep Dive:** Component-by-component analysis with specific call-outs and suggested solutions

**Standards Established:**

- **Project Rules and Global Standards:** 1,000+ line comprehensive standards document covering:
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

### 1.2 Higher Education CRM Implementation – Excelsior

**Type:** Salesforce Education Cloud (EDA) implementation for higher education institution

**Main Salesforce Clouds/Features Used:**

- Education Cloud (EDA) data model
- Experience Cloud for student/advisor portals
- OmniStudio for application and grant workflows
- Salesforce Scheduler for advising and appointment scheduling
- Platform Events for SIS integration events
- Custom Application objects and Program Enrollment tracking

**Main External Systems Involved:**

- Dell Boomi ETL platform for high-volume batch synchronization
- Oracle-based Student Information System (SIS)
- Institutional identity provider (SAML/OIDC)
- External event bus (Amazon EventBridge reference architecture)

**Problems I Actually Solved:**

- **High-Volume Data Synchronization:** Built integration handling 300,000+ student records (EMPLIDs) synchronized daily from Oracle SIS
- **Composite External ID Strategy:** Designed Account-level external IDs using composite keys (Institution + Program + Effective Date)
- **File-Based Staging Pattern:** Implemented pattern where large ID lists written to disk, then dynamically split into batched SQL IN-clause queries
- **Application Workflow:** Built OmniScripts guiding students through complex application processes
- **Program Selection LWC:** Built `modernProgramSelector` LWC component with `ModernProgramSelectorController` Apex class for program selection with real eligibility rules, filtering by term, area, level, and program offered via options
- **Fraud Score Calculation:** Built `fraudScore` LWC component with `FraudScoreController` Apex class implementing logistic regression model with 16 factors to calculate fraud probability scores on Application records
- **Row Locking Error Handling:** Built `ContactRetryUpdateService` Apex class with configurable retry logic and exponential backoff to handle UNABLE_TO_LOCK_ROW errors in high-concurrency scenarios
- **Contact Update Service:** Built `ContactUpdateService` for handling Contact updates with graceful error handling
- **Data Analysis and Cleanup:** Created data analysis scripts to identify and remove duplicate records, analyze bulk API job failures, troubleshoot integration errors
- **License Management:** Built tools and automation to make license management easier and more efficient
- **Identity Integration:** Implemented SAML/OIDC integration with institutional identity provider

**Key Architectural Decisions I Made:**

- **Contact as Core Student Record:** Contacts serve as primary person record for students and applicants
- **External ID Strategy:** External IDs mirror SIS primary keys (EMPLID) for stable record mapping
- **Derived Fields:** Computed fields like "last three enrolled terms" from SIS data
- **Event-Driven SIS Integration:** Platform Events published for application submissions, status changes, data updates
- **LWC Over Aura:** Migrated from Aura components to Lightning Web Components for better performance and maintainability
- **Service Layer Pattern:** Separated business logic into service classes (e.g., `ContactRetryUpdateService`, `ContactUpdateService`) that can be called from Flows and LWCs

---

## 2. Architecture Patterns Implemented (From Workspace Evidence)

### 2.1 Multi-Tenant Identity Architecture

**Pattern:** Single Salesforce org supporting multiple distinct user communities with different identity providers

**Implementation Evidence:**

- Custom login handlers matching external identity provider GUIDs to existing Contacts
- Multiple identity providers: OIDC (citizens), SAML (internal staff), business-tenant (vendors)
- Record Type-based separation: Client, Vendor, Internal Staff
- Sharing Sets enforcing data visibility rules per user type
- Routing logic directing users to appropriate landing pages based on identity provider type

**Key Decisions:**

- **Pre-create Contacts from Migrations:** Contacts created before users log in for first time
- **Create Users on First Login:** Users created when Contacts exist (attach identity to existing Contact)
- **Avoid Pre-creating All Users:** Conserve licenses by creating users only when they first log in
- **Email + External ID Matching:** Dual matching criteria to prevent duplicate Contact/User creation

**Thought Process:**
The architecture emerged from the constraint of needing to support three distinct user types (citizens, vendors, internal staff) with different security and compliance requirements, all within a single org. The login handler pattern evolved to handle edge cases where external identity exists but Salesforce Contact does not (and vice versa), ensuring no duplicate records while maintaining data integrity.

### 2.2 Event-Driven Integration Architecture

**Pattern:** Platform Events published from Salesforce, routed to external event bus (EventBridge reference), consumed by multiple subscribers

**Implementation Evidence:**

- Platform Events published from Flows (preferred) and Apex
- Event payloads including external IDs, minimal PII, change metadata
- Channel Members within Salesforce subscribing to same events for internal logging/automation
- Reference architecture designed for EventBridge integration

**Key Decisions:**

- **Prefer Flows Over Apex:** Use declarative automation when possible for event publication
- **Self-Contained Payloads:** Include all necessary context in event payloads, avoid requiring subscribers to query Salesforce
- **Minimize PII:** Balance functionality with privacy requirements
- **Idempotent Design:** Design event payloads to be idempotent where possible

**Thought Process:**
The event-driven pattern was chosen to decouple Salesforce from external systems, enabling asynchronous processing and fan-out to multiple subscribers. The decision to prefer Flows over Apex reflects a broader philosophy of declarative-first automation, reserving code for complex logic that cannot be expressed declaratively.

### 2.3 Integration Platform as Security Boundary

**Pattern:** MuleSoft serving as network security layer and transformation boundary between Salesforce and external systems

**Implementation Evidence:**

- MuleSoft handling VPN requirements and IP whitelisting
- X-API-Key header authentication managed at MuleSoft layer
- Data transformation in MuleSoft (DataWeave), not in Salesforce
- Environment-specific endpoint configurations managed in MuleSoft
- XML exports of API specifications when live Swagger access restricted

**Key Decisions:**

- **Centralize Network Security:** Handle all network constraints at integration platform level
- **Abstract Network Complexity:** Salesforce developers don't need to know about VPN/IP whitelisting
- **Transform in Middleware:** Perform data transformation in MuleSoft, not Salesforce
- **Single Point of Control:** One integration platform managing multiple external systems

**Thought Process:**
This pattern emerged from the constraint of strict network security requirements (VPN, IP whitelisting) that couldn't be handled directly in Salesforce. By positioning MuleSoft as the security boundary, Salesforce developers could focus on business logic while the integration platform handled network complexity. This also enabled centralized API authentication and transformation, reducing duplication across multiple integrations.

### 2.4 Permission Set-Driven Security Model

**Pattern:** Profiles contain minimal permissions (UI configuration only), Permission Sets contain all access control

**Implementation Evidence:**

- **Permission Restructuring Plan:** Complete migration plan moving 406 field permissions from profiles to permission sets
- **Profile Structure:** Minimal profiles with only license, tab visibility, record type visibility, layout assignments
- **Permission Set Structure:** Comprehensive permission sets with all object permissions, field permissions, class access, user permissions
- **No Delete Permissions:** All `allowDelete` set to `false` for community users

**Key Decisions:**

- **Profiles = UI Configuration:** Profiles define what users see, not what they can access
- **Permission Sets = Access Control:** All permissions granted through permission sets
- **No Delete Permissions:** Community users cannot delete any records (data integrity)
- **Granular Permission Management:** Easier to manage permissions through permission sets than profiles

**Thought Process:**
The transition from profile-centric to permission set-based security was driven by the need for more granular permission management at scale (40,000 users). Permission sets provide flexibility to grant incremental capabilities without modifying profiles, and they're more efficient for managing permissions across large user populations. The "no delete permissions" decision was made to protect data integrity and prevent accidental data loss.

### 2.5 Comprehensive Logging and Error Handling Framework

**Pattern:** All errors logged to `LOG_LogMessage__c` object using `LOG_LogMessageUtility` class or DataRaptor Load actions

**Implementation Evidence:**

- **LOG_LogMessageUtility Class:** Apex utility class supporting different log levels (Debug, Info, Error, Warning, Fatal)
- **Platform Event Fallback:** Publishes `ErrorLog__e` platform events on DML exceptions
- **Integration Procedure Logging:** DataRaptor Load actions (e.g., `IEECreateLogMessageRec`) for logging API calls
- **Error Handling Analysis:** Detailed review identifying logging gaps and conditional logging needs

**Key Decisions:**

- **All Errors Must Be Logged:** Standard requiring all errors logged to `LOG_LogMessage__c`
- **Conditional Logging Consideration:** Analysis of whether to log all API calls or only errors (storage/performance trade-off)
- **Platform Event Fallback:** If DML fails, publish platform event to ensure error is captured
- **Structured Logging:** Consistent log format with source, source function, message, debug level, payload

**Thought Process:**
The logging framework was established to meet compliance requirements (government cloud, audit trails) while enabling effective troubleshooting. The decision to use a custom logging object rather than System.debug reflects the need for persistent, queryable logs that can be analyzed and reported on. The platform event fallback ensures errors are captured even when DML operations fail.

### 2.6 High-Volume Batch Integration Pattern

**Pattern:** File-based staging for large ID lists, dynamic SQL IN-clause batching, idempotent upserts with external IDs

**Implementation Evidence:**

- **Boomi ETL Processes:** High-volume batch synchronization (300K+ records daily)
- **File-Based Staging:** Large ID lists written to disk, then processed in batches
- **Dynamic SQL Batching:** ID lists split into batched SQL IN-clause queries (1,000 IDs per IN clause)
- **Composite External IDs:** Account-level external IDs using composite keys (Institution + Program + Effective Date)
- **Integration Job Tracking:** Standard fields (`Last_Sync_Timestamp__c`, `Last_Sync_Status__c`, `Last_Sync_Error__c`, `Integration_Job_ID__c`)

**Key Decisions:**

- **Chunking Strategy:** Break large data sets into manageable chunks (1,000-10,000 records per batch)
- **File-Based Staging:** Use file staging for ID lists exceeding 50,000 records
- **Idempotent Upserts:** Always use external IDs for upsert operations
- **Job Tracking Fields:** Standard fields on all integrated objects for correlation and troubleshooting

**Thought Process:**
The high-volume integration pattern evolved from the constraint of processing 300,000+ student records daily. The file-based staging pattern emerged when in-memory processing became impractical. The dynamic SQL batching approach was chosen to work within database query size limits while maintaining performance. The integration job tracking fields were added to enable troubleshooting and correlation with external system logs.

---

## 3. Integrations Actually Built (From Workspace Evidence)

### 3.1 MuleSoft Integration – Public Sector Benefits API

**Source → Salesforce → Target:**

- **Source:** External benefits/notice generation system (hosted on VMs)
- **Salesforce:** Custom Notice and Transaction objects
- **Target:** External system via MuleSoft

**Pattern:** Synchronous and near-synchronous REST API calls

**Tools Used:**

- MuleSoft integration platform
- Named Credentials in Salesforce (when properly configured)
- Custom Metadata Types for interface configuration (`IEE_MS_Interface_Detail__mdt`)

**Orchestration Patterns:**

- **Security Boundary:** MuleSoft handles VPN and IP whitelisting
- **Transformation Layer:** DataWeave transformations in MuleSoft
- **API Authentication:** X-API-Key headers managed at MuleSoft layer
- **Error Handling:** Standardized error responses returned to Salesforce
- **Logging:** Integration logs for troubleshooting connectivity and data issues

**What I Built:**

- **RestIntegrationService:** Built abstract Apex class using Custom Metadata to configure endpoints, methods, headers, timeouts
- **Integration Procedures:** Built multiple Integration Procedures calling MuleSoft APIs for notice lists, document lists, user details, user search
- **Error Handling Analysis:** Analyzed all Integration Procedures identifying hardcoded URLs that should use Named Credentials

**Key Learnings I Discovered:**

- **Hardcoded URLs Are Prohibited:** Established project standard requiring all URLs externalized via Named Credentials or Custom Metadata
- **Error Handling Gaps:** My analysis revealed 53 out of 56 Integration Procedures have `failOnStepError: false` (silent failures)
- **Logging Patterns:** Found that some IPs log unconditionally (every API call), others have no logging at all
- **Configuration Management:** Determined Custom Metadata Types preferred over hardcoded values for environment-specific configuration

### 3.2 Dell Boomi ETL – High-Volume SIS Synchronization

**Source → Salesforce:**

- **Source:** Oracle-based Student Information System (SIS)
- **Salesforce:** Education Cloud data model (Contacts, Program Enrollments, Applications)

**Pattern:** High-volume batch synchronization (300K+ records daily)

**Tools Used:**

- Dell Boomi ETL platform
- File-based staging for large ID lists
- Dynamic SQL IN-clause batching

**Orchestration Patterns:**

- **File-Based Staging:** Large ID lists written to disk, then processed
- **Dynamic SQL Batching:** ID lists split into batched SQL IN-clause queries (1,000 IDs per IN clause)
- **Idempotent Upserts:** External IDs (EMPLID) used for upsert operations
- **Error Handling:** Error capture at each step, retry logic with exponential backoff
- **Job Tracking:** Integration job tracking fields on all integrated objects

**Evidence:**

- Boomi patterns documented in knowledge base
- Composite external ID strategy for Account-level records
- Integration job tracking fields: `Last_Sync_Timestamp__c`, `Last_Sync_Status__c`, `Last_Sync_Error__c`, `Integration_Job_ID__c`

**Key Learnings:**

- **Chunking Is Critical:** Large data sets must be broken into manageable chunks
- **File Staging for Scale:** In-memory processing becomes impractical at very large scales
- **External IDs Enable Idempotency:** Stable external IDs allow safe retry of failed syncs
- **Job Tracking Enables Troubleshooting:** Correlation IDs link Salesforce records to external system job logs

### 3.3 Platform Events – Event-Driven Outbound Integration

**Source → Salesforce → Target:**

- **Source:** Business events in Salesforce (application submissions, status changes, data updates)
- **Salesforce:** Platform Events published from Flows or Apex
- **Target:** External event bus (EventBridge reference architecture), multiple subscribers

**Pattern:** Event-driven, asynchronous

**Tools Used:**

- Salesforce Platform Events
- Event Channels (reference architecture)
- Amazon EventBridge (reference architecture)

**Orchestration Patterns:**

- **Event Publication:** Flows preferred over Apex for declarative event publication
- **Event Routing:** Event Channel routes to external event bus
- **Fan-Out:** EventBridge fans out to multiple subscribers (SIS integration services, analytics pipelines, microservices, notification services)
- **Internal Consumption:** Channel Members in Salesforce subscribe for internal logging/automation

**Evidence:**

- Platform Events and EventBridge patterns documented in knowledge base
- Event-driven architecture documentation

**Key Learnings:**

- **Declarative First:** Prefer Flows over Apex when logic can be expressed declaratively
- **Self-Contained Payloads:** Include all necessary context in event payloads
- **Minimize PII:** Balance functionality with privacy requirements
- **Idempotent Design:** Design event payloads to be idempotent where possible

---

## 4. Identity & SSO Implemented (From Workspace Evidence)

### 4.1 Multi-Identity Provider Architecture

**Implementation:** Single Salesforce org supporting three distinct identity provider types

**Identity Providers:**

1. **External OIDC Provider:** State-wide citizen identity provider for citizens/clients
2. **Internal SAML Provider:** State internal SSO for staff (direct employees)
3. **Business-Tenant Identity Provider:** Separate identity provider for vendor organizations

**Evidence:**

- Identity architecture documentation
- OIDC and SAML flows documentation
- Hybrid identity models documentation
- Login handler patterns

**Key Decisions:**

- **Different Providers for Different User Types:** Security and compliance requirements differ by user type
- **Login Handler Routing:** Custom login handlers route users based on identity provider type
- **Record Type-Based Separation:** Different Record Types for Account (client, vendor, internal) and Contact (citizen, vendor staff, internal staff)
- **Pre-create Contacts:** Contacts created from migrations before users log in for first time
- **Create Users on First Login:** Users created when Contacts exist (attach identity to existing Contact)

**Thought Process:**
The multi-identity provider architecture emerged from the constraint of needing to support three distinct user communities (citizens, vendors, internal staff) with different security and compliance requirements, all within a single org. The login handler pattern evolved to handle edge cases where external identity exists but Salesforce Contact does not (and vice versa), ensuring no duplicate records while maintaining data integrity.

### 4.2 OIDC Implementation for External Users

**Implementation:** OIDC SSO between Salesforce Experience Cloud and state-wide citizen identity provider

**Flow Pattern:**

- OIDC authorization code flow for secure authentication
- External identity provider GUIDs mapped to Salesforce Contacts
- First-time login scenarios where Contacts were pre-created during migration
- Prevention of duplicate Contact/User creation by matching on external GUID and email

**Evidence:**

- OIDC and SAML flows documentation
- Login handler patterns

**Key Decisions:**

- **OIDC for Experience Cloud:** Better user experience than SAML for external users
- **GUID + Email Matching:** Dual matching criteria to prevent duplicates
- **Pre-created Contacts:** Contacts exist before users log in, users attached on first login

### 4.3 SAML Implementation for Internal Staff

**Implementation:** SAML SSO for internal staff using state internal SSO identity provider

**Flow Pattern:**

- SAML 2.0 assertion-based authentication
- Distinction between internal staff (direct employees) and vendor staff (contractors)
- Different SAML attributes/claims for different user types
- SAML attributes mapped to Salesforce User and Contact fields

**Evidence:**

- OIDC and SAML flows documentation
- Login handler patterns

**Key Decisions:**

- **SAML for Enterprise SSO:** Standard for internal enterprise authentication
- **Attribute Mapping:** SAML attributes mapped to Salesforce fields
- **User Type Distinction:** Different handling for internal staff vs. vendor staff

### 4.4 Business-Tenant Identity for Vendors

**Implementation:** Business-tenant identity provider for vendor staff

**Flow Pattern:**

- Vendor staff create business-tenant accounts with same email as legacy ID provider
- Business-tenant identity mapped to pre-created vendor Contact and Vendor Account records
- Multi-org vendor scenarios where staff work across multiple organizations
- Future provider organization onboarding without over-committing licenses upfront

**Evidence:**

- Hybrid identity models documentation
- Login handler patterns

**Key Decisions:**

- **Business-Tenant for Vendors:** Separate identity provider for vendor organizations
- **Email Matching:** Business-tenant accounts use same email as legacy ID provider
- **License Conservation:** Users created on first login, not pre-created

---

## 5. Data Modeling Designed (From Workspace Evidence)

### 5.1 Public Sector Case Management Data Model

**Core Entities:**

- **Client Accounts/Contacts:** Individual citizens/clients (potentially person-style accounts)
- **Vendor (Provider) Accounts:** Organizations providing services on behalf of state
- **Vendor Contacts:** Staff working for provider organizations
- **Staff Contacts and Users:** Internal employees managing cases and services
- **Cases:** Primary records for ongoing service/benefits activity
- **Custom Notice Objects:** Mirroring notices generated by external systems
- **Custom Transaction Objects:** Mirroring transactions logged by external engines

**Evidence:**

- Public sector case modeling documentation
- Data dictionary analysis
- Custom object metadata for Notice and Transaction tracking

**Key Design Decisions:**

- **Cases as Primary Records:** Cases represent ongoing service/benefits activity
- **Notice Objects Track External Outputs:** Custom Notice objects mirror notices from external system
- **Transaction Objects Track External Engines:** Custom Transaction objects mirror transactions from external engine
- **Record Type Strategy:** Different Record Types for Account (client, vendor, internal) and Contact (citizen, vendor staff, internal staff)
- **External System IDs:** Fields for correlation with legacy systems

**Field Design Patterns:**

- **Source System Fields:** Source system field (HIX, MA21, MMIS) - should be picklist
- **Role Fields:** Role field (Client, Vendor Eligibility Worker, Staff) - should be picklist
- **Language Code Fields:** Language code field (ENG, etc.) - should be picklist
- **Status Fields:** Status field (Printed, Hold, Release) - picklist
- **Action Fields:** Action field (Hold, Release) - picklist

**Data Quality Analysis:**

- **Field Description Quality:** Analysis identifying poor descriptions (just repeat label) vs. good descriptions (source, purpose, population, business rules)
- **Help Text Missing:** Zero custom fields have help text - recommendation to add for user-facing fields
- **Picklist Conversions:** Three fields identified for conversion from Text to Picklist (SourceSystem, Role, LanguageCode)
- **Formula Field Discrepancy:** `IEE_MS_DetailPageURL__c` has static text in repository but URL formula in data dictionary

### 5.2 Education Cloud Data Model

**Core Entities:**

- **Contact as Core Student/Applicant Record:** Contacts serve as primary person record
- **Program Enrollment Objects:** Education Cloud Program Enrollment and Course Enrollment objects
- **Application Objects:** Custom or standard Application objects (one or multiple applications per student)
- **Account for Programs:** Accounts represent academic programs or institutions

**Evidence:**

- Education Cloud modeling documentation
- External ID and integration keys documentation

**Key Design Decisions:**

- **Contact as Primary Person Record:** Contacts used across all Education Cloud implementations
- **External IDs Mirror SIS Keys:** External IDs (EMPLID) mirror SIS primary keys
- **Composite External IDs:** Account-level external IDs using composite keys (Institution + Program + Effective Date)
- **Derived Fields:** Computed fields like "last three enrolled terms" from SIS data
- **Program Modalities:** Fields or Record Types for online, hybrid, in-person
- **Program Levels:** Fields for undergraduate, graduate, non-degree

**Integration Tracking Fields:**

- `Last_Sync_Timestamp__c` (DateTime)
- `Last_Sync_Status__c` (Picklist: Success, Error, In Progress)
- `Last_Sync_Error__c` (Long Text Area)
- `Integration_Job_ID__c` (Text)
- `Record_Source__c` (Picklist: Integration, Manual Entry, Migration)

### 5.3 External ID and Integration Key Strategies

**Pattern:** External IDs designed to support stable record mapping between Salesforce and external systems

**Implementation Evidence:**

- External ID and integration keys documentation
- Composite external ID strategy for Account-level records
- Integration job tracking fields on all integrated objects

**Key Design Decisions:**

- **External IDs for All Integrated Objects:** Always use external IDs for objects receiving data from integrations
- **Stable and Unique:** External IDs mirror external system primary keys
- **Composite External IDs:** When external systems use multi-column keys, concatenate with delimiter
- **Integration Job Tracking:** Standard fields on all integrated objects for correlation and troubleshooting

**Composite External ID Construction:**

- Concatenate component fields with delimiter (pipe `|` or dash `-`)
- Ensure delimiter doesn't appear in component field values
- Handle null values in component fields (use empty string or placeholder)
- Consider effective dates when constructing composite keys for time-versioned records

---

## 6. Security & Compliance Work (From Workspace Evidence)

### 6.1 Government Cloud Compliance

**Environment:** High-compliance government cloud environment with FedRAMP-style controls

**Compliance Considerations:**

- Data residency requirements ensuring data remains within approved geographic boundaries
- Enhanced logging and monitoring to meet audit requirements
- Email security with DKIM/SPF configuration for outbound communications
- Network security with VPN requirements and IP whitelisting for integrations
- Access control aligned with required control families (user provisioning, least privilege)

**Evidence:**

- Government cloud and compliance documentation
- Security overview documentation
- Logging, monitoring, and audit documentation

**Key Decisions:**

- **Data Residency:** All data processing within approved geographic boundaries
- **Comprehensive Logging:** All user actions and data access logged for audit
- **Permission Set-Driven Security:** More granular access control than profiles
- **Network Security:** Integration platforms (MuleSoft) as security boundaries

### 6.2 Permission Set-Driven Security Model

**Pattern:** Profiles minimal (UI configuration only), Permission Sets comprehensive (all access control)

**Implementation Evidence:**

- **Permission Restructuring Plan:** Complete migration plan moving 406 field permissions from profiles to permission sets
- **Profile Structure:** Minimal profiles with only license, tab visibility, record type visibility, layout assignments
- **Permission Set Structure:** Comprehensive permission sets with all object permissions, field permissions, class access, user permissions
- **No Delete Permissions:** All `allowDelete` set to `false` for community users

**Key Decisions:**

- **Profiles = UI Configuration:** Profiles define what users see, not what they can access
- **Permission Sets = Access Control:** All permissions granted through permission sets
- **No Delete Permissions:** Community users cannot delete any records (data integrity)
- **Test Classes Removed:** Test classes (`CommunitiesLandingControllerTest`, `CommunitiesLoginControllerTest`) removed from permission sets

**Security Review Findings I Identified:**

- **Two Similar Profiles:** Client profile with underscore and Client Profile with space with different permissions - confusion risk
- **Test Classes in Permission Set:** Test classes should never be accessible to end users (security risk)
- **Over-Privileged Access:** Users can create/delete records on Notice and Transaction objects - should be restricted
- **Sensitive Field Access:** SSN field editable - should be read-only for security/compliance
- **View All Fields Permission:** `viewAllFields: true` on OmniStudio objects - question why community users need this

### 6.3 Comprehensive Logging and Monitoring

**Pattern:** All errors logged to `LOG_LogMessage__c` object using `LOG_LogMessageUtility` class or DataRaptor Load actions

**Implementation Evidence:**

- **LOG_LogMessageUtility Class:** Apex utility class supporting different log levels (Debug, Info, Error, Warning, Fatal)
- **Platform Event Fallback:** Publishes `ErrorLog__e` platform events on DML exceptions
- **Integration Procedure Logging:** DataRaptor Load actions for logging API calls
- **Error Handling Analysis:** Detailed review identifying logging gaps

**Key Decisions:**

- **All Errors Must Be Logged:** Standard requiring all errors logged to `LOG_LogMessage__c`
- **Conditional Logging Consideration:** Analysis of whether to log all API calls or only errors (storage/performance trade-off)
- **Platform Event Fallback:** If DML fails, publish platform event to ensure error is captured
- **Structured Logging:** Consistent log format with source, source function, message, debug level, payload

**Logging Analysis Findings:**

- **Unconditional Logging:** Integration Procedures that have logging steps write to custom log object EVERY TIME (success or failure) because `executionConditionalFormula` is empty
- **Storage Impact:** At 40K scale, if each user makes 5 API calls = 200,000 log records per day
- **Performance Impact:** Every IP execution triggers DataRaptor Load action, additional DML for every API call
- **Recommendation:** Consider conditional logging (log only errors) for production environments

---

## 7. Project / Process Patterns (From Workspace Evidence)

### 7.1 Sprint-Based Delivery Approach

**Pattern:** Sprint-based delivery with clear scope definition, stakeholder coordination, and iterative delivery

**Implementation Evidence:**

- Delivery approach documentation
- Sprint 1 comprehensive review (18-point feedback document)
- Analysis documents organized by sprint

**Key Practices:**

- **Clear Sprint Definitions:** Sprint 1, Sprint 2, etc. with defined scope
- **Stakeholder Coordination:** State IT teams, vendor integrators, analyst partners, internal teams
- **Testing Window Coordination:** Reserved testing periods for integration validation
- **Change Management:** Discussions about when/how new objects and automations need to be reflected in TDD

**Sprint 1 Review Process:**

- **Comprehensive Analysis:** 18-point detailed feedback document covering:
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
  14. IEE Client Profile and Permission Set - security and configuration
  15. Feedback survey named flow not found in UI
  16. Data Dictionary - field type conversions, descriptions, naming standards
  17. ClientPortal Profile (Guest User)
  18. SurveyResponse CreatedBy field - not reflecting actual submitter

### 7.2 Comprehensive Code Review and Quality Standards

**Pattern:** Rigorous code review process establishing comprehensive quality standards

**Implementation Evidence:**

- **Project Rules and Global Standards:** 1,000+ line comprehensive standards document
- **Error Handling Analysis:** Detailed review of Integration Procedures
- **Permission Security Review:** Comprehensive security analysis
- **OmniStudio Best Practices Review:** Enterprise-scale component review
- **Data Dictionary Analysis:** Field source analysis, quality standards
- **Component Architectural Deep Dive:** Component-by-component analysis

**Standards Established:**

**Error Logging Standards I Established:**

- ALL exceptions MUST be logged to custom log object using logging utility class
- NO System.debug statements in production code
- Use proper logging instead of System.debug

**Error Handling Standards I Established:**

- Integration Procedures must show error messages to users when APIs fail
- Set `failOnStepError: true` for critical steps
- Add error states to Flex Cards
- Return error data in response

**Configuration Management Standards I Established:**

- NO hardcoded values (IDs, counts, URLs, etc.)
- Use Custom Metadata or Custom Settings
- All URLs must use Named Credentials or Custom Metadata

**Apex Code Standards I Established:**

- ALL Apex classes MUST have proper ApexDoc documentation
- ALL SOQL queries MUST use `WITH SECURITY_ENFORCED` or `WITH USER_MODE`
- ALL SOQL queries MUST be optimized (combine queries where possible)
- NO SOQL queries in loops
- ALL test classes MUST create their own test data (no `@IsTest(SeeAllData=true)`)
- ALL test classes MUST achieve minimum 90% code coverage

**Component Standards I Established:**

- ALL components MUST have meaningful descriptions
- NO test/dummy components in production
- Follow PascalCase naming convention
- Add timeout settings to HTTP actions
- Remove hardcoded test data

**Data Dictionary Standards I Established:**

- Field descriptions must be meaningful (not just repeat label)
- Include: source, purpose, population, business rules
- Add help text for user-facing fields
- Convert Text fields with limited values to Picklists
- Standardize field naming patterns

### 7.3 Testing and QA Strategy

**Pattern:** Comprehensive testing strategies covering integration, data quality, user migration, and UAT

**Implementation Evidence:**

- Testing and QA strategy documentation
- Integration testing for Salesforce → MuleSoft → external APIs
- Data quality testing for lead-to-contact conversion errors
- User migration and login handler testing
- UAT test instructions

**Key Practices:**

- **Integration Testing:** Connectivity testing, data transformation validation, error handling validation
- **Data Quality Testing:** Real-time matching and deduplication, error capture and troubleshooting
- **User Migration Testing:** User migration flows, login handler flows, identity mapping validation
- **UAT:** Step-by-step test instructions for business users

### 7.4 Release and Deployment Practices

**Pattern:** Source control and CI/CD pipelines for promoting metadata and integration changes

**Implementation Evidence:**

- Release and deployment practices documentation
- Environment management (DEV, QA, PERF, UAT, PROD)
- Source control (GitHub) for metadata changes
- CI/CD pipelines for promoting changes

**Key Practices:**

- **Environment Promotion:** Systematic promotion through environments (DEV → QA → UAT → PROD)
- **Source Control:** All metadata changes in source control
- **CI/CD Pipelines:** Automated deployment where possible
- **Change Management:** Update TDD when implementations change, keep diagrams aligned

---

## 8. Other Confirmed Work

### 8.1 OmniStudio Implementation Patterns

**Implementation Evidence:**

- OmniStudio patterns documentation
- Component analysis: 56 Integration Procedures, 200+ Flex Cards
- Best practices review identifying critical issues

**Key Patterns:**

- **OmniScripts for Guided Processes:** Application workflows, grant workflows, step-by-step guidance
- **FlexCards for Reusable UI Components:** Structured, reusable components, aggregated data display
- **Integration Procedures:** Orchestrate data retrieval and transformation
- **DataRaptors:** Extract, Transform, Load actions for data manipulation

**Critical Issues I Identified:**

- **53 out of 56 Integration Procedures** have `failOnStepError: false` (silent failures)
- **5 Integration Procedures** contain hardcoded URLs (should use Named Credentials)
- **29 Integration Procedures** missing Named Credentials
- **44 Integration Procedures** marked inactive (technical debt)
- **168 Flex Cards** marked inactive
- **27 Integration Procedures** have empty descriptions
- **5 test/dummy components** found in production metadata

### 8.2 Apex Implementation Patterns

**What I Built:**

**1. Logging Utility Class (`LOG_LogMessageUtility`):**

I built this class to solve a critical problem: we needed comprehensive error logging for compliance and troubleshooting, but System.debug wasn't sufficient. Here's how I approached it:

**The Problem:**

- System.debug statements don't persist - can't troubleshoot production issues
- No structured logging for compliance/audit requirements
- Need different log levels (Debug, Info, Error, Warning, Fatal)
- Need to handle large payloads (truncation)
- Need to handle DML failures gracefully (publish Platform Events as fallback)

**The Solution I Built:**

- Created `LOG_LogMessageUtility` class implementing `Callable` interface (can be called from Flows)
- Implemented different log levels as enum: `LOG_LogLevel {Debug, Info, Error, Warning}`
- Built `logMessage()` methods that:
  - Accept log level, source, source function, message, payload
  - Check log settings (can filter by level)
  - Truncate payloads if too large
  - Can queue DML requests or execute immediately
  - On DML exception, publish `ErrorLog__e` Platform Event as fallback
- Used Custom Settings (`LOG_LogMessageSettings__c`) to control logging behavior

**Why I Built It This Way:**

- **Callable Interface:** Needed to be callable from Flows and Apex - Callable interface provides both
- **Platform Event Fallback:** If DML fails (governor limits, validation rules), Platform Event ensures error is still captured
- **Truncation:** Large payloads can exceed field limits - truncation prevents DML errors
- **Log Settings:** At 40K scale, logging everything would create massive storage - settings allow filtering
- **Queue DML Option:** For high-volume scenarios, can queue logs and batch insert

**What I Learned:**

- Always have a fallback mechanism for critical logging
- Consider storage implications at scale
- Make utilities flexible (queue vs immediate, filtering options)

**2. Integration Service (`RestIntegrationService`):**

I built this to solve the problem of hardcoded URLs and inconsistent integration patterns:

**The Problem:**

- Multiple Apex classes making HTTP callouts with hardcoded URLs
- Different error handling patterns in each class
- Environment-specific URLs (dev vs prod) hardcoded
- No centralized configuration management

**The Solution I Built:**

- Created abstract `RestIntegrationService` class implementing `IIntegrationService` interface
- Uses Custom Metadata Type (`IEE_MS_Interface_Detail__mdt`) to configure:
  - Endpoint URLs (via Named Credentials)
  - HTTP methods (GET, POST, etc.)
  - Headers
  - Timeouts
  - Request/response transformations
- `generateRequest()` method reads Custom Metadata and builds HttpRequest
- `sendRequest()` method executes the request and returns HttpResponse

**Why I Built It This Way:**

- **Custom Metadata:** Can have different records per environment (dev, staging, prod) - no code changes needed
- **Named Credentials:** URLs externalized, credentials managed by Salesforce
- **Abstract Class:** Can extend for specific integrations while reusing common logic
- **Interface Pattern:** Other classes can implement same interface for consistency

**What I Learned:**

- Externalize all configuration - never hardcode environment-specific values
- Use Named Credentials for all external URLs
- Centralize integration patterns - easier to maintain and audit

**3. Contact Retry Update Service (`ContactRetryUpdateService`):**

I built this to solve row locking errors in high-concurrency scenarios:

**The Problem:**

- Users getting `UNABLE_TO_LOCK_ROW` errors when updating Contact records
- High-traffic periods causing failures
- No retry mechanism
- Errors causing user frustration

**The Solution I Built:**

- Created `ContactRetryUpdateService` with `@InvocableMethod` (callable from Flows)
- Implemented configurable retry logic:
  - Default: 3 retries with 100ms wait period
  - Configurable via invocable variables
- Row locking error detection:
  - Checks error status code (`UNABLE_TO_LOCK_ROW`)
  - Checks error message (string matching for "unable to obtain exclusive access")
  - Only retries on row locking errors, not other errors
- Governor limit awareness:
  - Checks CPU time before retry
  - Fails fast if approaching limits
  - Uses busy-wait (noted as future improvement - could use Platform Events/Queueable)

**Why I Built It This Way:**

- **Invocable Method:** Needed to be callable from Flows (where the updates were happening)
- **Configurable Retries:** Different scenarios need different retry counts
- **Error Detection:** Only retry on retryable errors (row locking), not validation errors
- **CPU Time Awareness:** Prevents governor limit exceptions
- **Busy-Wait Limitation:** Noted in code comments - for high-volume, should use async alternatives

**What I Learned:**

- Retry logic must be intelligent (only retry retryable errors)
- Always consider governor limits in retry logic
- Document trade-offs and future improvements in code
- Busy-wait works but isn't ideal for high-volume scenarios

**4. Fraud/Risk Score Calculation Pattern:**

I built a fraud probability scoring system for application review:

**The Problem:**

- Need to calculate fraud probability scores on application records
- Model uses logistic regression with 16 demographic and academic factors
- Need to display detailed score breakdown for transparency
- Business rules override model (military status, nursing programs, completed courses)
- Users need to provide feedback on scores for model improvement

**My Solution:**

- **Calculation Service:**
  - Data fetch method retrieves application, contact, educational history, and course completion data
  - Calculation method implements logistic regression model with 16 factors
  - Update method persists calculated score to application record
  - Feedback method sends structured email with complete score breakdown
- Override conditions checked first:
  - Active Duty Military → fraud score = 0
  - Nursing Programs → fraud score = 0
  - Completed Courses (with valid grades) → fraud score = 0
- If no overrides, calculates score using:
  - Age coefficient (0.041 × age)
  - Gender coefficient (-0.348 for female)
  - Race coefficients (various values)
  - Ethnicity coefficient (-1.474 for Hispanic)
  - International student coefficient (-2.234)
  - Income coefficients (various brackets)
  - Education coefficients (high school, highest degree, parent education)
  - Budget group coefficients (Academic Partner, Military, etc.)
  - Division coefficients (Health Sciences, Liberal Arts, etc.)
  - Degree level coefficients (Bachelors, Graduate Certificate, Masters)
  - Zero credit flag (4.257 if no educational history)
  - Submission date flag (3.691 if has submission date)
  - Inquiry days coefficient (-0.00127 × days)
  - Constant (-7.577)
- Converts total odds to probability using logistic function: `e^(odds) / (1 + e^(odds)) × 100`
- Returns detailed breakdown with field values and scores for display

**Why I Built It This Way:**

- **Override Conditions First:** Business rule - certain conditions override the model
- **Detailed Breakdown:** Users need to understand why score is what it is
- **Cacheable Methods:** `getFraudInputs()` and `calculateFraudScore()` are cacheable for performance
- **Feedback Mechanism:** Users can provide feedback on scores - valuable for model improvement
- **Structured Email:** Feedback emails include complete score breakdown for analysis

**Performance Optimizations I Implemented:**

1. **Page Load Time Improvements:**
   - **No Auto-Calculation on Load:** The component doesn't automatically calculate on page load. User must click "Calculate" button. This prevents unnecessary Apex calls when users just view the record.
   - **Cacheable Methods:** Both `getFraudInputs()` and `calculateFraudScore()` use `@AuraEnabled(cacheable=true)`, allowing Salesforce to cache results and reduce server round trips.
   - **Cache Busting with Random Parameter:** The `getFraudInputs()` method accepts a `random` parameter (using `System.currentTimeMillis()`) to ensure fresh data when needed, while still benefiting from caching when the same data is requested.
   - **Single Apex Call for Calculation:** The calculation method fetches all required data in one call rather than multiple separate queries, reducing network latency.
   - **Efficient Query Structure:** Queries use `LIMIT 1` where appropriate and only fetch necessary fields, reducing data transfer.

2. **Query Optimizations:**
   - **Relationship Queries:** Uses relationship queries (`hed__Applying_To__r.Area__c`) to fetch related data in single query instead of separate queries.
   - **Conditional Queries:** Only queries for Educational History and Completed Courses when Contact exists, avoiding unnecessary queries.
   - **Selective WHERE Clauses:** All queries use indexed fields (Id fields) for optimal performance.
   - **Minimal Field Selection:** Only selects fields actually needed for calculation, not entire objects.

3. **UI/UX Optimizations:**
   - **Lazy Loading:** Score breakdown is hidden in tabs, only loaded when user expands "Score Breakdown" tab.
   - **Loading States:** Clear loading spinner during calculation prevents user confusion.
   - **Error Handling:** Graceful error messages with specific error details help users understand issues.
   - **Tabbed Interface:** Organized display with Summary and Score Breakdown tabs reduces cognitive load.

**What I Learned:**

- Business rules (overrides) should be checked before model calculation
- Users need transparency in scoring models
- Feedback mechanisms are valuable for model improvement
- Detailed breakdowns help users understand and trust the system
- **Performance:** Not auto-calculating on load significantly improves page load times
- **Caching:** Cacheable methods with cache busting provide best of both worlds (performance + fresh data)
- **User Control:** Giving users control over when to calculate improves perceived performance

**5. Program Selection Service Pattern:**

I built a program selection service to replace an older component with modern patterns:

**The Problem:**

- Legacy component had issues:
  - Hardcoded values making maintenance difficult
  - Missing error handling causing poor user experience
  - Performance issues from too many API calls
  - Inconsistent state management
  - Built in Aura (harder to maintain than LWC)

**My Solution:**

- **Cacheable Reference Data Methods:**
  - Terms method returns list of open terms (cached)
  - Areas method returns picklist values from metadata (cached)
  - Levels method returns picklist values from metadata (cached)
  - Programs method returns filtered programs based on selections (cached)
  - Delivery options method returns options for specific program (cached)
- **Dynamic SOQL Pattern:**
  - Builds SOQL query dynamically based on selected filters
  - Uses proper escaping to prevent SOQL injection
  - Limits results to prevent large result sets
- **Smart Option Handling:**
  - If program has only one delivery option, auto-selects it
  - If multiple options, returns all for user selection
  - Maps picklist API names to user-friendly labels using metadata
  - Falls back to API name if metadata unavailable

**Why I Built It This Way:**

- **Cacheable Methods:** Terms, areas, levels don't change often - caching improves performance
- **Dynamic SOQL:** Need to filter by different combinations - dynamic query allows flexibility
- **Proper Escaping:** Security best practice - prevent SOQL injection
- **Auto-Selection:** Better UX - if only one option, don't make user select it
- **Label Mapping:** Users see friendly labels, not API names

**Responsiveness Improvements I Implemented:**

1. **Mobile-First Responsive Design:**
   - **Media Queries at 768px Breakpoint:** All major UI elements adapt at 768px width for tablet and mobile devices.
   - **Flexible Layout:** Uses flexbox with `flex-direction: column` for vertical stacking on mobile.
   - **Compact Padding:** Reduced padding on mobile (0.5rem vs 0.75rem) to maximize screen space.
   - **Font Size Adjustments:** Smaller font sizes on mobile (0.8rem vs 0.875rem) for better fit.
   - **Touch-Friendly Targets:** Buttons and interactive elements sized appropriately for touch (minimum 44px touch targets).

2. **Responsive Components:**
   - **Field Cards:** Adapt padding and spacing on mobile.
   - **Compact Selections:** Font size reduces from 0.875rem to 0.8rem on mobile.
   - **Help Text:** Responsive padding and font size adjustments.
   - **Delivery Option Cards:** Gap and padding adjustments for mobile.
   - **Radio Groups:** Enhanced radio group styling adapts to smaller screens.

**Query Optimizations I Implemented:**

1. **Efficient Data Loading:**
   - **Cascading Load Pattern:** Terms load first, then areas (after term selection), then levels (after area selection), then programs (after level selection). This reduces initial load time and only loads what's needed.
   - **Cacheable Methods:** All getter methods (`getTerms()`, `getAreas()`, `getLevels()`, `getPrograms()`) are cacheable, reducing server calls.
   - **Dynamic SOQL with Filters:** The `getPrograms()` method builds SOQL dynamically with WHERE clauses only for selected filters, ensuring selective queries.
   - **LIMIT 100:** Programs query limits to 100 results to prevent large result sets.
   - **ORDER BY Optimization:** Uses `ORDER BY Formatted_Name__c ASC` for consistent, sorted results.
   - **Picklist Metadata Caching:** `getAreas()` and `getLevels()` use picklist metadata which is cached by Salesforce, avoiding queries.

2. **Selective Field Queries:**
   - **Minimal Field Selection:** Only selects `Id`, `Formatted_Name__c`, `Name` for programs, not entire Account object.
   - **Relationship Queries:** Uses `Starting_Term__r.Name` relationship query instead of separate query.

**Color Structure and Implementation:**

1. **Brand Color System:**
   - **Primary Color (Excelsior Purple):** `#59005A` - Used throughout for:
     - Header titles
     - Border colors on hover
     - Button backgrounds (gradient)
     - Icons
     - Focus states
     - Selected states
   - **Gradient Backgrounds:** Uses linear gradients for visual depth:
     - Compact selections: `linear-gradient(135deg, #59005A, #7a1a7b)`
     - Apply button: `linear-gradient(135deg, #59005A, #4a004a)`
     - Hover states: `linear-gradient(135deg, #7a1a7b, #59005A)`
   - **Secondary Colors:**
     - White (`#ffffff`) for text on dark backgrounds
     - Gray scale (`#333`, `#666`, `#e5e5e5`) for text and borders
     - Warning yellow (`#fff3cd`, `#ffeaa7`, `#856404`) for no programs message

2. **Color Usage Patterns:**
   - **Interactive Elements:** Purple borders on hover, purple backgrounds when selected
   - **Text Hierarchy:** Dark gray (`#333`) for primary text, lighter gray (`#666`) for secondary text
   - **Backgrounds:** White for cards, light gray (`#f8f9fa`) for help text and option cards
   - **States:**
     - Default: White background, gray border
     - Hover: Purple border, light gray background
     - Selected: Purple gradient background, white text
     - Focus: Purple outline for accessibility

3. **CSS Implementation:**
   - **CSS Custom Properties:** Uses CSS variables where possible for maintainability
   - **Consistent Color Application:** All purple elements use the same hex value for consistency
   - **Transitions:** Smooth color transitions on hover (0.2s ease, 0.3s cubic-bezier)
   - **Box Shadows:** Purple-tinted shadows (`rgba(89, 0, 90, 0.15)`) for depth

**Compact View Pattern I Implemented:**

1. **State Management:**
   - **Selection States:** Each step has a boolean flag (`isTermSelected`, `isAreaSelected`, etc.) to track if selection is made
   - **Compact Display:** Once selected, shows compact view with icon, label, value, and edit icon
   - **Edit Capability:** Clicking compact view allows editing by resetting the selection state

2. **UX Benefits:**
   - **Progressive Disclosure:** Only shows relevant fields based on previous selections
   - **Visual Feedback:** Clear indication of what's selected with purple gradient background
   - **Space Efficiency:** Compact view saves vertical space, allowing more content on screen
   - **Edit Flow:** Easy to edit selections without losing context

**What I Learned:**

- Always escape user input in dynamic SOQL
- Cache static/reference data
- Auto-select when only one option exists
- Map API names to user-friendly labels
- **Responsive Design:** Mobile-first approach with breakpoints improves usability across devices
- **Color Consistency:** Using a single brand color throughout creates cohesive visual identity
- **Progressive Disclosure:** Showing only relevant fields reduces cognitive load
- **State Management:** Clear state flags make UI behavior predictable and maintainable
- **Performance:** Cascading loads reduce initial page load time significantly

**Key Patterns I Established:**

- **Service Layer:** Business logic and orchestration (e.g., `RestIntegrationService`)
- **Domain Layer:** Object-specific logic (e.g., Account helper classes)
- **Selector Layer:** SOQL queries and data access
- **Integration Layer:** External API callouts (e.g., `RestIntegrationService`)
- **Utility Classes:** Reusable functionality (e.g., `LOG_LogMessageUtility`)
- **Invocable Methods:** Built invocable methods for Flow integration (e.g., `SendSMSMagicEU`, `ContactRetryUpdateService`)
- **Cacheable Methods:** Use `@AuraEnabled(cacheable=true)` for read-only operations
- **Error Handling:** Always log errors, provide user-friendly messages, have fallback mechanisms

**Code Quality Issues I Found and Fixed:**

- **System.debug Statements:** Found in production classes, removed and replaced with proper logging
- **Hardcoded Values:** Contact ID and retry count hardcoded, moved to Custom Metadata
- **Exception Handling:** Exceptions caught but only logged to System.debug, updated to log to custom log object
- **SOQL Optimization:** Two separate queries that could be combined using relationship syntax, optimized
- **Unused Variables:** Found in production code, removed
- **Commented Code:** Found in production code, cleaned up
- **SOQL Injection Risk:** Dynamic SOQL without escaping, added `String.escapeSingleQuotes()`
- **Missing Null Checks:** Direct field access without null checks, added proper null handling

### 8.3 Flow Design Patterns

**Implementation Evidence:**

- Flow design patterns documentation
- Flow naming conventions: `App_AfterSave_ApplicationStatusOrchestration`, `Case_BeforeSave_Defaulting`

**Key Patterns:**

- **Record-Triggered Flows:** Primary workhorse for creating/updating related records, status transitions, notifications
- **Subflows:** Reusable logic chunks for assignment rules, task creation, status updates
- **Screen Flows:** Guided data capture, step-by-step case/application handling
- **Scheduled Flows:** Periodic cleanup, data maintenance, batch operations
- **Auto-Launched Flows:** Called from other Flows or Apex for reusable logic

**Flow Structure Patterns:**

- **Strict Entry Criteria:** Avoid "run on every change, then decide inside"
- **Separation of Concerns:** Decision nodes routing by record state (New vs Update, channel, person type)
- **Subflows for Complex Tasks:** Extract logical chunks into Subflows
- **Minimal DML:** Use fast field updates when possible, aggregate logic

### 8.4 LWC Implementation Patterns

**How I Think About LWCs:**

LWCs are surgical tools for complex UI needs that standard layouts or Flows can't handle well. I use them when:
- Need to combine data from multiple objects/systems
- Need complex client-side decisions and filtering
- Need responsive, interactive experiences
- Need to work cleanly in Experience Cloud portals

**Program Selection Pattern:**

I built a program selection component for higher-education admissions contexts:

**The Problem:**
- Applicants need to select academic programs with complex eligibility rules
- Programs filtered by term, area of study, degree level, delivery mode
- Need to handle single vs multiple delivery options
- Must enforce business rules (e.g., "This program only available in term X")
- Need responsive design for mobile users
- Must provide clear guidance and help text

**My Solution:**
- **Cascading Dropdown Pattern:**
  - Step-by-step selection: Term → Area → Level → Program → Delivery Mode
  - Each step filters next step's options
  - Only loads data when previous step selected (reduces initial load time)
  - Resets downstream selections when upstream selection changes
- **Compact View Pattern:**
  - Once selected, shows compact view with icon, label, value
  - Click to edit (resets that step and downstream)
  - Saves vertical space, shows progress clearly
- **Auto-Selection Logic:**
  - If program has only one delivery option, auto-selects it
  - If multiple options, shows radio buttons with help text
  - Reduces unnecessary clicks
- **Responsive Design:**
  - Mobile-first with 768px breakpoint
  - Flexible layouts, touch-friendly targets
  - Brand color system with gradients for visual depth
- **Performance Optimizations:**
  - Cacheable Apex methods for reference data (terms, areas, levels)
  - Dynamic SOQL with proper escaping for program queries
  - Cascading loads reduce initial page load time
  - LIMIT 100 on program queries

**Why I Built It This Way:**
- **Progressive Disclosure:** Only show relevant options, reduces cognitive load
- **State Management:** Clear boolean flags for each step's selection state
- **Performance:** Cascading loads and caching reduce server calls
- **User Experience:** Auto-selection and compact view improve usability
- **Responsive:** Mobile-first ensures works on all devices

**Fraud/Risk Score Display Pattern:**

I built a fraud probability score component for application review:

**The Problem:**
- Staff need single-glance view of risk score
- Score calculated from 16 demographic and academic factors
- Need detailed breakdown to understand why score is what it is
- Business rules override model (military, nursing, completed courses)
- Users need to provide feedback on scores
- Must not slow down page load

**My Solution:**
- **On-Demand Calculation:**
  - Doesn't auto-calculate on page load
  - User clicks "Calculate" button when needed
  - Prevents unnecessary Apex calls when just viewing record
- **Cacheable Methods:**
  - Both data fetch and calculation methods are cacheable
  - Cache busting with random parameter when fresh data needed
  - Reduces server round trips
- **Detailed Breakdown:**
  - Shows all 16 factors with values and coefficients
  - Tabbed interface (Summary and Score Breakdown)
  - Lazy loading of breakdown (only loads when tab expanded)
- **Override Conditions:**
  - Checks business rules first (military, nursing, completed courses)
  - If override applies, sets score to 0 with reason
  - Model calculation only if no overrides
- **Feedback Mechanism:**
  - Modal for user feedback
  - Sends structured email with complete score breakdown
  - Helps improve model over time

**Why I Built It This Way:**
- **Performance:** On-demand calculation and caching improve page load times
- **Transparency:** Detailed breakdown builds user trust
- **Business Rules:** Overrides checked first, as business requires
- **Feedback Loop:** User feedback valuable for model improvement
- **User Control:** Giving users control over when to calculate improves perceived performance

**Advisor Management Pattern:**

I built an advisor management component for staff to manage advisor information:

**The Problem:**
- Need to view and edit advisor-specific fields (availability days, times, nickname)
- Hundreds of advisors, need pagination
- Need search functionality
- Need inline editing without full page refresh
- Must work with field-level security

**My Solution:**
- **Pagination Pattern:**
  - 15 advisors per page
  - Server-side pagination (Apex handles offset/limit)
  - Cache busting with random parameter
- **Search Functionality:**
  - Search by name or email across all pages
  - Server-side search (Apex handles filtering)
  - Resets to page 1 on search
- **Inline Editing:**
  - Lightning Data Table with editable columns
  - Draft values tracked locally
  - Batch update on save (all edited rows in one DML)
- **System Mode Updates:**
  - Apex uses `without sharing` to bypass FLS for updates
  - Allows staff to edit fields they might not have FLS access to
  - Still respects object-level security

**Why I Built It This Way:**
- **Pagination:** Server-side more efficient than loading all records
- **Search:** Server-side allows searching across all data, not just loaded page
- **Inline Editing:** Better UX than separate edit pages
- **Batch Updates:** More efficient than updating one at a time
- **System Mode:** Needed for staff to manage advisor fields

**Key Patterns I Established:**

- **Console-Style LWCs:** Aggregate data from multiple related records, show "at-a-glance" status
- **Service-Layer Pattern:** Apex classes expose clean methods, LWCs deal with DTO-style payloads
- **Config-Driven UI:** Custom metadata/custom settings drive field visibility, thresholds, text/labels
- **Performance-Aware:** Batch reads into single wired Apex method, use `refreshApex` carefully
- **Cascading Dropdowns:** Reusable pattern for dependent dropdowns with proper state management
- **Error Handling:** Comprehensive error handling with toast notifications and user-friendly messages
- **Feedback Mechanisms:** Feedback modals and email functionality for user input and improvement tracking
- **On-Demand Loading:** Don't auto-load heavy data, let users trigger when needed
- **Compact View Pattern:** Show selected values in compact form, allow editing without losing context
- **Responsive Design:** Mobile-first with breakpoints, flexible layouts, touch-friendly targets

### 8.5 SOQL Debugging Patterns

**Implementation Evidence:**

- SOQL debugging patterns documentation
- Advanced SOQL queries for troubleshooting

**Key Patterns:**

- **History Object Queries:** Use ContactHistory, AccountHistory, CaseHistory to track changes
- **Root Cause Analysis:** Query multiple objects to find relationships, use aggregate queries to identify patterns
- **Metadata Analysis:** Use VS Code + Salesforce Extensions to retrieve and inspect metadata
- **Error Investigation:** Query error fields on records, correlate errors with record types and sources

---

### 8.6 Batch Processing Patterns for Large-Scale Operations

**How I Think About Batch Processing:**

When I need to process large volumes of records (emails, calculations, updates), I use Batch Apex with specific patterns:

**Batch Email Processing Pattern:**

I built a batch email processing system to handle large-scale email campaigns while respecting governor limits:

**The Problem:**
- Need to send emails to thousands of contacts
- Must use email templates with merge fields
- Need to handle attachments, CC/BCC, org-wide email addresses
- Must respect single email limits (5,000 per day per org, 1,000 per transaction)
- Need to track success/failure across batches
- Must handle errors gracefully without stopping entire job

**My Solution:**
- **Batch Apex Class:** Implements `Database.Batchable<SObject>` and `Database.Stateful` to:
  - Process contacts in batches (default 200 per batch)
  - Track state across batches (total processed, successful, failed, error messages)
  - Query contacts with fields needed for email template merge fields
- **Flexible Email Configuration:**
  - Supports email templates OR custom subject/body
  - Optional related record ID for merge fields (Account, Opportunity, etc.)
  - Optional org-wide email address
  - Optional CC/BCC addresses
  - Optional attachments (ContentVersion or Attachment IDs)
  - Configurable whether to save email as activity on Contact
- **Error Handling:**
  - Validates contact has email address before processing
  - Catches and logs errors per contact without stopping batch
  - Collects all error messages for reporting in finish method
  - Uses `Messaging.sendEmail()` with `allOrNone=false` to allow partial success
- **Stateful Tracking:**
  - Maintains counters across all batches
  - Logs summary in finish method
  - Can optionally send completion notification or create log records

**Why I Built It This Way:**
- **Batch Processing:** Handles large volumes without hitting transaction limits
- **Stateful:** Need to track progress across all batches, not just current batch
- **Flexible Configuration:** Different campaigns need different email settings
- **Error Resilience:** One bad contact shouldn't stop entire campaign
- **Partial Success:** `allOrNone=false` allows successful emails even if some fail

**Batch Fraud Score Calculation Pattern:**

I built a batch job to recalculate fraud scores for large numbers of applications:

**The Problem:**
- Need to recalculate fraud scores for thousands of applications
- Same calculation logic as interactive component
- Must handle override conditions (military, nursing, completed courses)
- Need to process efficiently with bulk queries
- Must track progress and errors

**My Solution:**
- **Bulk Query Pattern:** 
  - Queries all applications in start method
  - Collects all contact IDs and application IDs in execute method
  - Queries all related data in bulk (Contacts, Educational History, Registered Courses)
  - Builds maps for O(1) lookup during processing
- **Shared Calculation Logic:**
  - Reuses same calculation method as interactive component
  - Ensures consistency between batch and interactive calculations
- **Efficient Processing:**
  - Processes all applications in batch together
  - Single DML update for all applications in batch
  - Avoids SOQL in loops
- **Stateful Tracking:**
  - Tracks total processed, updated, errors across all batches
  - Logs summary in finish method

**Why I Built It This Way:**
- **Bulk Queries:** Avoids N+1 query problem by querying all related data upfront
- **Map-Based Lookups:** O(1) access to related records during processing
- **Shared Logic:** Ensures batch and interactive calculations match exactly
- **Single DML:** More efficient than updating records one at a time

**Key Patterns I Established:**

- **Batch Apex for Large Volumes:** Use when processing thousands of records
- **Stateful for Tracking:** Use `Database.Stateful` when need to track progress across batches
- **Bulk Query Pattern:** Query all related data upfront, use maps for lookups
- **Error Resilience:** Catch errors per record, don't stop entire batch
- **Flexible Configuration:** Pass configuration through constructor, not hardcoded
- **Shared Business Logic:** Reuse calculation/processing logic between batch and interactive

### 8.7 Data Analysis and Cleanup Work

**What I Built:**

- **Bulk API Job Analysis:** Created Python scripts to analyze bulk API job failures, identify patterns in failed records, generate reports on job status and error rates
- **Integration Error Analysis:** Created analysis documents and scripts to troubleshoot integration errors, identify root causes, track error patterns across different integration points
- **Data Cleanup Scripts:** Built scripts to identify and remove duplicate records, analyze data quality issues, generate cleanup reports
- **CSV Export Analysis:** Created scripts to process CSV exports of failed and successful records, compare results, identify discrepancies
- **SOQL Debugging Queries:** Wrote advanced SOQL queries to troubleshoot data issues, find root causes of errors, track record changes over time

**Problems I Solved:**

- **Bulk API Job Failures:** Analyzed bulk API job failures to identify patterns, root causes, and data quality issues
- **Integration Errors:** Troubleshot integration errors by analyzing error logs, identifying common failure points, and creating remediation strategies
- **Data Quality Issues:** Identified and fixed data quality issues through systematic analysis and cleanup scripts
- **Record Deduplication:** Built processes to identify and remove duplicate records while preserving data integrity

---

### 9.1 How I Analyze Problems

**Pattern:** Comprehensive, evidence-based analysis with specific call-outs and suggested solutions

**Example - Error Handling Analysis:**

1. **Question Formulation:** "Do Integration Procedures show error messages to users when APIs fail? Are errors logged?"
2. **Evidence Gathering:** Review all Integration Procedures, identify `failOnStepError` settings, check for logging steps
3. **Finding Documentation:** Create detailed analysis document with evidence, impact assessment, recommendations
4. **Solution Proposing:** Provide specific implementation patterns with code examples

**Example - Permission Security Review:**

1. **Comprehensive Review:** Review Profile and Permission Set metadata
2. **Issue Identification:** Test classes in permission set, over-privileged access, sensitive field access
3. **Impact Assessment:** Security risks, compliance violations, data integrity issues
4. **Migration Planning:** Detailed step-by-step migration plan with XML examples

### 9.2 How I Establish Standards

**Pattern:** Standards emerge from real-world problems and are codified through comprehensive documentation

**Example - Project Rules and Global Standards:**

1. **Problem Identification:** Issues found during Sprint 1 review (hardcoded URLs, missing error handling, System.debug statements)
2. **Standard Formulation:** Create rule prohibiting the problem (e.g., "NO hardcoded URLs")
3. **Documentation:** Comprehensive standards document with examples, required implementations, current behavior, target behavior
4. **Enforcement:** Standards become part of code review process

**Example - Error Handling Standard:**

1. **Problem:** Silent failures in Integration Procedures, no error visibility
2. **Analysis:** Review all Integration Procedures, identify patterns
3. **Standard:** "ALL errors MUST be logged to `LOG_LogMessage__c`"
4. **Implementation Pattern:** Provide specific code examples and configuration patterns

### 9.3 How I Make Architecture Decisions

**Pattern:** Architecture decisions emerge from constraints and requirements, then are refined through analysis

**Example - Permission Set-Driven Security:**

1. **Constraint:** 40,000 users, need granular permission management
2. **Requirement:** Easier permission management, better scalability
3. **Decision:** Transition from profile-centric to permission set-based model
4. **Implementation:** Detailed migration plan moving 406 field permissions
5. **Refinement:** Analysis identifying test classes, delete permissions, over-privileged access

**Example - MuleSoft as Security Boundary:**

1. **Constraint:** VPN and IP whitelisting requirements
2. **Requirement:** Salesforce developers shouldn't need to know about network complexity
3. **Decision:** Use MuleSoft as security boundary
4. **Implementation:** All external API calls go through MuleSoft
5. **Refinement:** Analysis identifying hardcoded URLs that should use Named Credentials

### 9.4 How I Ensure Quality

**Pattern:** Rigorous code review process with comprehensive analysis and specific recommendations

**Example - Sprint 1 Review:**

1. **Comprehensive Analysis:** 18-point detailed feedback document
2. **Evidence-Based Findings:** Specific code examples, line numbers, file paths
3. **Impact Assessment:** Scale considerations (40K users), security risks, compliance issues
4. **Specific Recommendations:** Code examples, configuration patterns, implementation steps
5. **Follow-Up:** Analysis documents for each area (error handling, security, components, data dictionary)

**Example - Component Architectural Deep Dive:**

1. **Component-by-Component Analysis:** Review each component individually
2. **Specific Call-Outs:** Identify critical issues, high priority issues, moderate issues
3. **Suggested Solutions:** Provide specific implementation patterns with code examples
4. **References:** Link to official Salesforce documentation
5. **Priority Actions:** Immediate actions, short-term actions, medium-term actions

---

## 10. Evolution of Understanding

### 10.1 From Generic to Specific

**Pattern:** Understanding evolves from generic patterns to specific, evidence-based implementations

**Example - Error Handling:**

- **Initial Understanding:** "Errors should be handled"
- **Evolved Understanding:** "53 out of 56 Integration Procedures have `failOnStepError: false`, causing silent failures. Need conditional logging with `executionConditionalFormula` checking for errors. Flex Cards need error states. Integration Procedures need `failureResponse` objects with user-friendly messages."

**Example - Security:**

- **Initial Understanding:** "Use permission sets"
- **Evolved Understanding:** "Profiles should contain zero permissions (minimal base configuration only). Permission Sets should contain ALL permissions (all access control). NO delete permissions anywhere. Test classes must be removed from permission sets. SSN fields should be read-only."

### 10.2 From Symptoms to Root Causes

**Pattern:** Analysis digs deeper to find root causes, not just fix symptoms

**Example - SOQL Debugging:**

- **Symptom:** "Users can't log in"
- **Root Cause Analysis:** Query User object with status conditions, cross-reference with login history, identify users who are active but frozen, correlate with permission set assignments and profile changes

**Example - Data Quality Errors:**

- **Symptom:** "Lead conversion failing"
- **Root Cause Analysis:** Query ContactHistory to track field changes, identify creation sources, track ownership changes, correlate with Lead conversion history, create test cases to replicate errors around default record types

### 10.3 From Individual to Systematic

**Pattern:** Individual findings lead to systematic standards and patterns

**Example - Hardcoded URLs:**

- **Individual Finding:** "This Integration Procedure has a hardcoded URL"
- **Systematic Analysis:** Review all Integration Procedures and Flex Cards, identify all hardcoded URLs
- **Standard Establishment:** "NO hardcoded URLs permitted. All URLs must use Named Credentials or Custom Metadata."
- **Configuration Approach:** Analysis document comparing Custom Labels vs Custom Metadata Types, recommending hybrid approach

**Example - Error Handling:**

- **Individual Finding:** "This Integration Procedure doesn't show errors to users"
- **Systematic Analysis:** Review all 56 Integration Procedures, identify patterns
- **Standard Establishment:** "ALL errors MUST be logged. Integration Procedures MUST show error messages to users."
- **Implementation Pattern:** Provide complete error handling pattern with code examples

---

## 11. How I Develop, Troubleshoot, and Review Code Using Cursor as My Tool

### 11.1 My Development Workflow

**When I'm building something new, here's my process:**

**1. Starting a New Component or Class:**

- I search my codebase for similar patterns I've built before
- I look for existing LWC components or Apex service classes to understand the patterns I've established
- I review actual examples from my previous work to ensure consistency
- This ensures I'm reusing proven approaches, not reinventing patterns

**2. Building with Context:**

- I open multiple related files (the component, the Apex controller, related utilities)
- I review the Project Rules and Global Standards document to ensure my code follows established patterns
- I check existing implementations to understand how similar features were built
- This prevents me from writing code that violates established standards

**3. Iterative Refinement:**

- I write a first draft, then review it against:
  - Project Rules and Global Standards
  - Existing patterns in the codebase
  - Best practices from analysis documents
- I iterate based on what I find, refining error handling, logging patterns, and other aspects
- I check similar implementations to see how they handle edge cases

**4. Learning from Past Work:**

- When I'm stuck, I search through my analysis documents, code reviews, and implementation notes
- I review what I did before and WHY I did it that way - the constraints, the decisions, the trade-offs
- I learn from my own experience, not just generic documentation

**Example: Building the Modern Program Selector LWC**

When I built the `modernProgramSelector` LWC for Excelsior, here's my process:

1. **Pattern Discovery:** I searched my codebase for existing program selector components. I found `programSelector`, `programSelectorV2`, and related Apex controllers.
2. **Understanding the Problem:** I reviewed analysis documents I'd created earlier that showed problems with previous implementations:

   - Hardcoded values
   - Missing error handling
   - Performance issues with too many API calls
   - Inconsistent state management
3. **Design Decisions:** Based on my LWC patterns document and the issues I'd identified, I structured the component to:

   - Use `@wire` for initial data loading (cacheable)
   - Use imperative calls for user actions
   - Implement proper error handling with toast notifications
   - Follow the cascading dropdown pattern I'd established
4. **Implementation:** As I wrote code, I reviewed each section against my standards:

   - Does this error handling follow our standards?
   - Is this SOQL query optimized?
   - Does this match our naming conventions?
5. **Testing:** I reviewed similar components to identify edge cases to test:

   - Empty result sets
   - API failures
   - Network timeouts
   - Invalid user selections

**Why This Approach Works:**

- **Consistency:** I'm building on established patterns, not creating new ones each time
- **Quality:** I catch violations of standards before code review
- **Speed:** I can quickly reference patterns I've established
- **Learning:** I understand WHY patterns exist, not just WHAT they are

### 11.2 My Troubleshooting Methodology

**When something breaks, here's how I investigate:**

**1. Understanding the Symptom:**

- I start by identifying the problem: "Users are seeing blank screens when they try to view notices"
- I search my codebase for:
  - Similar issues I've seen before
  - Error handling patterns in notice-related components
  - Analysis documents I've created about blank screens or error handling

**2. Root Cause Analysis:**

- I review my Error Handling Analysis document which I created earlier, which identified:
  - `failOnStepError: false` causing silent failures
  - Empty `failureResponse: {}` meaning no error data returned
  - Missing error states in Flex Cards
- This gives me a checklist of things to investigate

**3. Evidence Gathering:**

- I search for all Integration Procedures that call notice APIs
- I find: `IEE_NoticeListAPICalloutIp`, `IEEDocumentListAPICallout`, etc.
- I review the error handling configuration in these IPs
- I examine the actual JSON configuration and identify:
  - `failOnStepError: false` (the problem)
  - Empty `failureResponse: {}` (no error messages)
  - Missing logging steps

**4. Solution Design:**

- I review my Error Handling Analysis document for the correct pattern
- I reference the detailed implementation pattern I documented:
  - Set `failOnStepError: true`
  - Configure `failureResponse` with user-friendly messages
  - Add error logging steps
  - Add error states to Flex Cards
- I use the JSON structure examples I created in the analysis document

**5. Validation:**

- After implementing the fix, I review it against Project Rules and Global Standards
- I check for any gaps or inconsistencies

**Example: Troubleshooting Row Locking Errors**

When I encountered `UNABLE_TO_LOCK_ROW` errors in high-concurrency scenarios:

1. **Problem Identification:** Users were getting errors when updating Contact records during high-traffic periods
2. **Investigation:**

   - I searched my codebase for previous row locking solutions - found nothing, this was a new problem
   - I reviewed my codebase for DML error handling patterns
   - I found `LOG_LogMessageUtility` and error handling patterns I'd established
3. **Solution Research:**

   - I researched best practices for handling row locking errors in Salesforce
   - I learned about retry logic, exponential backoff, governor limits
   - I designed a solution that follows my logging standards
   - I decided to use `Database.update()` with `allOrNone=false`, implementing retry with CPU time awareness
4. **Implementation:**

   - I built `ContactRetryUpdateService`
   - As I wrote each method, I reviewed it against my standards:
     - Is this retry logic correct?
     - Does this handle governor limits properly?
     - Does this follow our error logging standard?
   - I identified issues like:
     - Busy-wait consuming CPU time (noted as future improvement)
     - Missing CPU time checks before retries
     - Error detection using string matching (noted as potential future issue)
5. **Documentation:**

   - I documented the solution including:
     - The problem (row locking errors)
     - The solution (retry with exponential backoff)
     - The trade-offs (CPU time vs. async alternatives)
     - Future improvements (Platform Events, Queueable)

**Why This Approach Works:**

- **Systematic:** I follow a consistent investigation process
- **Evidence-Based:** I find actual evidence from my codebase, not guess
- **Comprehensive:** I review related issues and patterns I've documented
- **Documented:** Solutions are captured for future reference

### 11.3 My Code Review Process

**Code reviews are where I provide comprehensive, actionable feedback:**

**1. Preparation:**

- Before starting a review, I review:
  - Project Rules and Global Standards
  - Previous code review findings
  - Analysis documents with specific examples
- This gives me a checklist of things to look for

**2. Systematic Review:**

- I review code against specific standards:
  - Does this Apex class follow our error logging standard?
  - Are there any hardcoded values that should use Custom Metadata?
  - Does this SOQL query follow our optimization patterns?
- I check against:
  - Project standards
  - Existing patterns in the codebase
  - Analysis documents with specific examples

**3. Finding Patterns:**

- When I find one issue, I search across all projects for:
  - Similar issues in other files
  - Patterns of violations
  - Related analysis documents
- This helps me provide comprehensive feedback, not just point out one instance

**4. Providing Solutions:**

- Instead of just saying "this is wrong," I reference:
  - Implementation patterns from analysis documents
  - Examples from existing code
  - Standards documents with specific requirements
- I provide specific, actionable recommendations with examples

**5. Impact Assessment:**

- I review analysis documents that discuss:
  - Performance implications
  - Storage impacts
  - Security risks
  - Compliance violations
- This helps prioritize fixes

**Example: Sprint 1 Comprehensive Code Review**

When I did the Sprint 1 review, here's my process:

1. **Scope Definition:**

   - I identified all components in Sprint 1: Integration Procedures, Flex Cards, Apex classes, and related metadata
   - I compiled a comprehensive checklist from Project Rules and Global Standards
2. **Systematic Analysis:**

   - For each category, I analyzed:
     - **Error Handling:** I reviewed all Integration Procedures for error handling patterns
     - I found 56 Integration Procedures, identified 53 with `failOnStepError: false`
     - **Hardcoded URLs:** I searched for all hardcoded URLs in Integration Procedures and Flex Cards
     - I found 5 Integration Procedures and multiple Flex Cards with hardcoded URLs
     - **Logging:** I checked if all Integration Procedures have error logging
     - I found most IPs missing logging, some logging unconditionally
3. **Deep Dive Analysis:**

   - For critical issues, I created detailed analysis documents:
     - I created a detailed analysis of error handling in Integration Procedures
     - I structured the analysis document with:
       - Current state assessment
       - Evidence from each IP
       - Impact analysis
       - Required fixes with examples
       - Implementation patterns
     - This became the Error Handling Analysis document
4. **Solution Documentation:**

   - Based on the issues found, I created:
     - Complete error handling pattern with JSON examples
     - URL externalization approach (Custom Labels vs Custom Metadata analysis)
     - Logging pattern with DataRaptor examples
   - These patterns were added to Project Rules and Global Standards
5. **Feedback Compilation:**

   - I organized all findings into a comprehensive 18-point feedback document with:
     - Clear problem statements
     - Evidence
     - Questions for clarification
     - Action items
     - References to analysis documents

**Why This Approach Gets Excellent Results:**

- **Comprehensive:** I check everything systematically
- **Evidence-Based:** Every finding is backed by actual code or configuration
- **Actionable:** Solutions are specific with examples, not vague suggestions
- **Prioritized:** Impact assessment helps focus on what matters most
- **Educational:** Developers understand WHY something is wrong, not just that it is

### 11.4 How I Use Cursor for Org Management

**My Org Management Workflow with Cursor:**

Managing Salesforce orgs at scale requires systematic approaches - Cursor helps me be methodical:

**1. Understanding Current State:**

- When I need to understand the org structure, I ask Cursor: "Analyze the permission model in this org"
- Cursor reads profile and permission set metadata, identifies:
  - What permissions are in profiles vs permission sets
  - Inconsistencies
  - Security issues
  - Opportunities for improvement

**2. Planning Changes:**

- Before making changes, I ask Cursor: "What's the impact of moving permissions from profiles to permission sets?"
- Cursor references:
  - Permission Restructuring Plan document
  - Analysis of current permission distribution
  - Best practices for permission management
- This helps me create a detailed migration plan

**3. Systematic Execution:**

- I ask Cursor to help create step-by-step plans:
  - "Create a migration plan for moving 406 field permissions from profiles to permission sets"
  - Cursor structures the plan with:
    - Current state analysis
    - Target state definition
    - Step-by-step migration process
    - Validation checklist
    - Rollback procedures

**4. Validation:**

- After changes, I ask Cursor: "Verify that the permission model matches our target state"
- Cursor checks:
  - Profiles have minimal permissions
  - Permission sets have all required permissions
  - No security issues (delete permissions, test classes, etc.)
  - Consistency across similar profiles/permission sets

**Example: Converting Profiles to Permission Sets**

When I restructured permissions for the public sector portal:

1. **Current State Analysis:**

   - I asked Cursor: "Analyze the IEE_Client Profile and Permission Set - what permissions are where?"
   - Cursor read the metadata files and identified:
     - Profile had 406 field permissions
     - Profile had 10 object permissions
     - Permission Set had 156 field permissions
     - Permission Set had 9 object permissions
     - Permission Set had 2 DELETE permissions (security issue)
   - I asked: "What's the target state based on our standards?"
   - Cursor referenced the Permission Restructuring Plan which defined:
     - Profiles = minimal (license, tabs, record types, layouts only)
     - Permission Sets = all permissions
     - NO delete permissions anywhere
2. **Migration Planning:**

   - I asked Cursor: "Create a detailed migration plan for this restructuring"
   - Cursor helped structure the Permission Restructuring Plan with:
     - Current state analysis (what's in profiles, what's in permission sets)
     - Target state definition (minimal profiles, comprehensive permission sets)
     - Step-by-step migration process:
       - Phase 1: Remove delete permissions
       - Phase 2: Migrate object permissions
       - Phase 3: Migrate field permissions (406 fields!)
       - Phase 4: Migrate class access
       - Phase 5: Migrate user permissions
       - Phase 6: Create minimal profiles
       - Phase 7: Test and validate
     - Detailed field-by-field migration checklist
     - XML examples showing before/after
     - Validation checklist
3. **Execution:**

   - As I migrated permissions, I asked Cursor:
     - "Does this field permission belong in the permission set?"
     - "Is this the correct permission level (read vs edit)?"
     - "Have I missed any fields?"
   - Cursor cross-referenced:
     - Original profile permissions
     - Existing permission set permissions
     - Business requirements from analysis documents
4. **Validation:**

   - After migration, I asked Cursor: "Verify the migration is complete and correct"
   - Cursor checked:
     - All 406 field permissions moved to permission set
     - All object permissions moved to permission set
     - Profiles have zero permissions (only UI configuration)
     - No delete permissions exist
     - Test classes removed from permission set
   - Cursor identified any gaps or issues

**Why This Approach Works:**

- **Systematic:** I follow a methodical process, not ad-hoc changes
- **Documented:** Every change is planned and validated
- **Safe:** Validation ensures nothing breaks
- **Scalable:** Patterns can be applied to other profiles/permission sets

### 11.5 How I Use Cursor for Deep Analysis

**My Analysis Methodology with Cursor:**

When I need to understand how something works or identify problems, Cursor helps me do deep, comprehensive analysis:

**1. Question Formulation:**

- I start with a clear question: "Do Integration Procedures show error messages to users when APIs fail?"
- I ask Cursor: "Help me investigate this question systematically"
- Cursor suggests:
  - What to look for (error handling configuration)
  - Where to look (Integration Procedure metadata)
  - What patterns to check (failOnStepError, failureResponse, error states)

**2. Evidence Gathering:**

- I ask Cursor: "Find all Integration Procedures that call external APIs"
- Cursor searches and finds: `IEE_NoticeListAPICalloutIp`, `IEEDocumentListAPICallout`, `IEEUserDetail_IP`, `IEEUserSearch_IP`
- I ask: "What's the error handling configuration in each of these?"
- Cursor reads the metadata and extracts:
  - `failOnStepError` settings
  - `failureResponse` configuration
  - Logging steps
  - Error state handling

**3. Pattern Identification:**

- I ask Cursor: "What patterns do you see across these Integration Procedures?"
- Cursor identifies:
  - 100% have `failOnStepError: false` (silent failures)
  - 0% have proper `failureResponse` configuration
  - 25% have logging (but unconditional)
  - 0% have error states in Flex Cards
- This gives me quantitative findings, not just observations

**4. Impact Assessment:**

- I ask Cursor: "What's the impact of these issues at 40K user scale?"
- Cursor calculates:
  - If each user makes 5 API calls = 200,000 calls per day
  - If 1% fail = 2,000 failures per day with no error messages
  - Storage impact of unconditional logging
  - Performance impact of missing error handling
- This helps prioritize fixes

**5. Solution Design:**

- I ask Cursor: "Based on our standards and best practices, what's the correct pattern?"
- Cursor references:
  - Project Rules and Global Standards
  - Salesforce best practices
  - Implementation patterns from analysis documents
- I ask: "Create a complete implementation pattern with examples"
- Cursor structures the pattern with:
  - Step-by-step configuration
  - JSON examples
  - Flex Card error state examples
  - Testing checklist

**6. Documentation:**

- I ask Cursor: "Help me document this analysis comprehensively"
- Cursor helps structure the analysis document with:
  - Executive summary
  - Current state assessment
  - Detailed findings per component
  - Impact analysis
  - Required fixes
  - Implementation patterns
  - Priority actions
  - Testing checklist

**Example: Error Handling Analysis**

When I created the Error Handling Analysis document:

1. **Question:** "Do Integration Procedures show error messages to users when APIs fail? Are errors logged?"
2. **Investigation with Cursor:**

   - I asked: "Find all Integration Procedures that call MuleSoft APIs"
   - Cursor found 4 main IPs
   - I asked: "What's the error handling configuration in each?"
   - Cursor extracted the relevant JSON configuration for each
3. **Analysis:**

   - I asked Cursor: "What patterns do you see? What's missing?"
   - Cursor identified:
     - All have `failOnStepError: false`
     - All have empty `failureResponse: {}`
     - Most have no logging
     - None have error states in Flex Cards
   - I asked: "What's the impact?"
   - Cursor calculated:
     - Users see blank screens (0% show errors)
     - No audit trail (75% have no error logging)
     - Cannot debug issues
     - Compliance violations
4. **Solution Design:**

   - I asked Cursor: "What's the correct pattern based on our standards?"
   - Cursor referenced Project Rules and Global Standards
   - I asked: "Create a complete implementation pattern"
   - Cursor structured the pattern with:
     - HTTP Action configuration
     - Error logging step
     - Response Action with error data
     - Flex Card error state
   - Each with complete JSON examples
5. **Documentation:**

   - I asked Cursor: "Help me structure this as a comprehensive analysis document"
   - Cursor helped create the document with:
     - Executive summary (answers to questions)
     - Detailed analysis per IP (evidence, impact)
     - Required fixes (with examples)
     - Implementation pattern (complete pattern)
     - Priority actions (critical vs high)
     - Testing checklist

**Why This Approach Works:**

- **Thorough:** I don't miss anything - Cursor helps me be systematic
- **Evidence-Based:** Every finding is backed by actual configuration
- **Actionable:** Solutions are specific with examples
- **Prioritized:** Impact assessment helps focus efforts
- **Documented:** Analysis becomes reusable knowledge

### 11.6 How I Use Cursor to Make Myself Better

**My Continuous Improvement Process with Cursor:**

I use Cursor not just to build things, but to learn and improve:

**1. Reflecting on Past Work:**

- After completing a task, I ask Cursor: "What did I learn from this? What would I do differently?"
- Cursor reviews:
  - What I built
  - What issues I encountered
  - How I solved them
  - What patterns I established
- I ask: "What are the key takeaways I should remember?"
- Cursor helps me extract lessons learned and add them to my knowledge base

**2. Identifying Knowledge Gaps:**

- I ask Cursor: "What areas of Salesforce development am I less experienced in?"
- Cursor analyzes my codebase and identifies:
  - Technologies I've used extensively (LWC, Apex, OmniStudio)
  - Technologies I've used less (Platform Events, Change Data Capture)
  - Patterns I understand well
  - Patterns I'm still learning
- I ask: "What should I learn next based on my projects?"
- Cursor suggests learning paths based on:
  - What I'm building
  - What I'm struggling with
  - What's coming up in projects

**3. Building on Experience:**

- When I encounter a new problem, I ask Cursor: "Have I solved something similar before?"
- Cursor finds:
  - Similar problems I've solved
  - How I solved them
  - What worked and what didn't
  - What I learned
- I ask: "How can I apply that experience to this new problem?"
- Cursor helps me adapt past solutions to new contexts

**4. Establishing Best Practices:**

- When I solve a problem, I ask Cursor: "Is this a pattern I should reuse? How should I document it?"
- Cursor helps me:
  - Identify reusable patterns
  - Document them in standards documents
  - Create examples for future reference
  - Add to knowledge base

**5. Code Review as Learning:**

- When I review code, I ask Cursor: "What can I learn from the issues I'm finding?"
- Cursor helps me identify:
  - Common mistakes I should avoid
  - Patterns that work well
  - Areas where I need better standards
  - Opportunities to improve my own code

**Example: Learning from the Sprint 1 Review**

After completing the Sprint 1 review:

1. **Reflection:**

   - I asked Cursor: "What did I learn from this comprehensive review?"
   - Cursor identified:
     - The importance of systematic analysis (18 points covered everything)
     - The value of evidence-based findings (not just opinions)
     - How detailed analysis documents become reusable knowledge
     - The impact of comprehensive standards (caught issues before they spread)
2. **Pattern Extraction:**

   - I asked Cursor: "What patterns should I establish based on these findings?"
   - Cursor helped me create:
     - Error handling standard (from error handling analysis)
     - Logging standard (from logging analysis)
     - URL externalization standard (from hardcoded URL analysis)
     - Permission management standard (from permission review)
   - These became part of Project Rules and Global Standards
3. **Process Improvement:**

   - I asked Cursor: "How can I do code reviews more effectively in the future?"
   - Cursor suggested:
     - Use systematic checklists (like the 18-point review)
     - Create analysis documents for complex issues
     - Reference standards documents during review
     - Provide specific examples, not just feedback
   - I incorporated these into my review process
4. **Knowledge Base Building:**

   - I asked Cursor: "How should I document this review process for future use?"
   - Cursor helped structure:
     - Code review methodology
     - Analysis document templates
     - Standards documentation approach
   - This became part of my knowledge base

**Why This Approach Works:**

- **Continuous Learning:** I'm always improving, not just repeating
- **Pattern Recognition:** I identify reusable patterns and document them
- **Knowledge Accumulation:** Everything I learn becomes part of my knowledge base
- **Efficiency:** I get better over time, solving problems faster

### 11.7 My Development Process: Questions I Asked Myself and What I Built

**This section captures my actual development process - the questions I asked, the research I did, and what I built:**

#### Example 1: Building the Error Handling Analysis Document

**My Process:**

1. I searched for all Integration Procedures that call MuleSoft APIs
2. I reviewed the error handling configuration in each of these Integration Procedures
3. I analyzed the patterns I saw and identified what was missing
4. I assessed the impact of these issues at 40K user scale
5. Based on my standards, I designed the correct pattern for fixing this
6. I created a complete implementation pattern with examples
7. I structured this as a comprehensive analysis document

**What I Found:**

- 4 main Integration Procedures calling MuleSoft APIs
- All had `failOnStepError: false` (silent failures)
- All had empty `failureResponse: {}` (no error messages)
- Most had no logging steps
- None had error states in Flex Cards

**What I Built:**

- Created comprehensive Error Handling Analysis document with:
  - Executive summary answering the questions
  - Detailed analysis per Integration Procedure (evidence, impact)
  - Required fixes with JSON examples
  - Complete implementation pattern (HTTP Action → Error Logging → Response Action → Flex Card error state)
  - Priority actions (critical vs high)
  - Testing checklist

**The Document Structure I Created:**

```
# Error Handling Analysis
## Executive Summary
- Question 1: Error Messages to Users - CURRENTLY NO
- Question 2: Error Logging - PARTIALLY IMPLEMENTED
## Detailed Analysis
- For each IP: Evidence, Impact, Required Fixes
## Implementation Pattern
- Step-by-step configuration with JSON examples
## Priority Actions
- Critical vs High priority
## Testing Checklist
```

#### Example 2: Permission Restructuring Plan

**My Process:**

1. I analyzed the IEE_Client Profile and Permission Set - identified what permissions were where
2. I reviewed my standards to determine the target state
3. I created a detailed migration plan for this restructuring
4. I reviewed each field permission to determine if it belonged in the permission set
5. I verified the correct permission level (read vs edit) for each field
6. I cross-checked to ensure I didn't miss any fields
7. I validated the migration was complete and correct

**What I Found:**

- Profile had 406 field permissions that needed to move
- Profile had 10 object permissions that needed to move
- Permission Set had 156 field permissions (keep and merge)
- Permission Set had 2 DELETE permissions (security issue - must remove)
- Permission Set had test classes (must remove)

**What I Built:**

- Created comprehensive Permission Restructuring Plan with:
  - Current state analysis (what's in profiles, what's in permission sets)
  - Target state definition (minimal profiles, comprehensive permission sets)
  - Step-by-step migration process (7 phases)
  - Detailed field-by-field migration checklist
  - XML examples showing before/after
  - Validation checklist
  - Benefits of the new structure

**The Migration Plan I Created:**

```
# Permission Restructuring Plan
## Current State Analysis
- What's in Profiles (406 field permissions, 10 object permissions)
- What's in Permission Sets (156 field permissions, 9 object permissions, 2 DELETE permissions)
## Target State
- Profiles = minimal (license, tabs, record types, layouts only)
- Permission Sets = all permissions
- NO delete permissions anywhere
## Migration Steps
- Phase 1: Remove delete permissions
- Phase 2: Migrate object permissions
- Phase 3: Migrate field permissions (406 fields!)
- Phase 4: Migrate class access
- Phase 5: Migrate user permissions
- Phase 6: Create minimal profiles
- Phase 7: Test and validate
## Detailed Field Permission Migration
- Complete list of 406 fields with permission levels
## Validation Checklist
```

#### Example 3: Sprint 1 Comprehensive Code Review

**My Process:**

1. I identified all components in Sprint 1
2. I compiled the standards I should check these against
3. I reviewed all Integration Procedures for error handling patterns
4. I searched for all hardcoded URLs in Integration Procedures and Flex Cards
5. I checked if all Integration Procedures have error logging
6. I created a detailed analysis of error handling in Integration Procedures
7. Based on the issues found, I designed the implementation patterns needed
8. I organized all findings into a comprehensive feedback document

**What I Found:**

- 56 Integration Procedures total
- 53 with `failOnStepError: false` (silent failures)
- 5 Integration Procedures with hardcoded URLs
- Multiple Flex Cards with hardcoded URLs
- Most Integration Procedures missing error logging
- System.debug statements in Apex classes
- Hardcoded values in Apex classes
- Missing component descriptions
- Test components in production
- Missing timeout settings
- Permission issues (test classes, delete permissions)

**What I Built:**

- Created 18-point comprehensive feedback document covering:

  1. Logging pattern for HTTP callouts vs DataRaptor-only IPs
  2. NULL checks and error messages
  3. Silent failures and blank screens
  4. Hardcoded URLs - removal and configuration approach
  5. DataRaptor caching
  6. Test components in production
  7. Missing component descriptions
  8. Hardcoded test data and record IDs
  9. Naming convention inconsistencies
  10. Missing timeout settings
  11. Apex classes used by Sprint 1 components
  12. Apex test classes
  13. Apex code quality (System.debug, hardcoded values, error logging)
  14. Profile and Permission Set security
  15. Feedback survey named flow
  16. Data Dictionary field conversions and descriptions
  17. Field naming inconsistencies
  18. Guest user profile permissions
- Created detailed analysis documents for each area:

  - Error Handling Analysis
  - Permission Restructuring Plan
  - Components Architectural Deep Dive
  - Data Dictionary Comprehensive Analysis
  - URL Storage Recommendation (Custom Labels vs Custom Metadata)

**My Review Process:**

1. **Systematic Analysis:** I checked every component against every standard
2. **Pattern Finding:** When I found one issue, I searched for all similar issues
3. **Impact Assessment:** I calculated impact at 40K user scale
4. **Solution Design:** I created specific implementation patterns with examples
5. **Documentation:** I structured comprehensive feedback document

#### Example 4: Building the Modern Program Selector LWC

**My Process:**

1. I searched for all existing program selector components in the codebase
2. I reviewed analysis documents to identify issues with previous implementations
3. Based on my LWC patterns document and the issues I found, I designed the component structure
4. I reviewed the error handling against my standards
5. I verified the SOQL query was optimized
6. I checked that it matched my naming conventions
7. I reviewed similar components to identify edge cases to test

**What I Found:**

- Existing components: `programSelector`, `programSelectorV2`
- Issues with previous implementations:
  - Hardcoded values
  - Missing error handling
  - Performance issues (too many API calls)
  - Inconsistent state management

**What I Built:**

- Built `modernProgramSelector` LWC with:

  - Cascading dropdowns (Term → Area → Level → Program → Program Offered Via)
  - Proper error handling with toast notifications
  - `@wire` for initial data loading (cacheable)
  - Imperative calls for user actions
  - Compact view with edit capability
  - Single vs multiple offering options handling
  - Help text and icons for delivery options
  - Navigation to application page with selected program details
- Built `ModernProgramSelectorController` Apex class with:

  - Cacheable methods for terms, areas, levels
  - Dynamic SOQL with proper escaping
  - Program filtering by term, area, level
  - Dynamic label mapping (API names to friendly labels)
  - Auto-selection for single offering options

**My Iterative Process:**

1. **Pattern Discovery:** I found existing components and their issues
2. **Design:** I designed structure based on patterns and issues
3. **Implementation:** As I wrote code, I reviewed each section against my standards
4. **Refinement:** I identified issues and made improvements
5. **Testing:** I identified edge cases to test based on similar components

#### Example 5: Troubleshooting Row Locking Errors

**My Process:**

1. I searched my codebase for previous row locking solutions
2. I reviewed patterns for handling DML errors in my codebase
3. I researched best practices for handling row locking errors in Salesforce
4. I designed retry logic that follows my logging standards
5. I reviewed the retry logic for correctness
6. I verified it handles governor limits properly
7. I checked that it follows my error logging standard
8. I documented the solution for future reference

**What I Found:**

- No previous row locking solutions in codebase (new problem)
- Found `LOG_LogMessageUtility` for error logging
- Found error handling patterns in other classes

**What I Built:**

- Built `ContactRetryUpdateService` with:
  - `@InvocableMethod` for Flow integration
  - Configurable retry logic (default: 3 retries, 100ms wait)
  - Row locking error detection (status code and message checking)
  - Governor limit awareness (CPU time checks before retries)
  - Proper error logging using `LOG_LogMessageUtility`
  - Busy-wait implementation (noted as future improvement)

**My Problem-Solving Process:**

1. **Investigation:** I searched for similar problems (none found)
2. **Research:** I researched best practices for row locking
3. **Design:** I designed retry logic with logging standards
4. **Implementation:** I reviewed each method as I wrote it
5. **Documentation:** I documented the problem, solution, trade-offs, and future improvements

#### Example 6: Creating the Project Rules and Global Standards Document

**My Process:**

1. I compiled all issues found during Sprint 1 review
2. I identified patterns to establish based on these findings
3. I designed how to document these standards
4. I created examples to include
5. I structured this document for future reference

**What I Found:**

- 18 major issues from Sprint 1 review
- Patterns emerging from individual findings
- Need for comprehensive standards document

**What I Built:**

- Created 1,000+ line Project Rules and Global Standards document covering:
  - Error Logging Standard
  - Error Handling Standard
  - Error Message Display Standard
  - Named Credentials Standard
  - Hardcoded URLs Standard
  - Configuration Management Standard
  - Component Status Standard
  - Naming Conventions Standard
  - Version Management Standard
  - Performance Optimization Standard
  - Security Standards
  - Documentation Requirements
  - Testing Component Standards
  - Integration Procedure Structure Standards
  - DataRaptor Standards
  - Apex Code Standards
  - Profile and Permission Set Standards
  - Data Dictionary/Field Standards

**My Standards Creation Process:**

1. **Problem Identification:** I compiled all issues from Sprint 1 review
2. **Pattern Recognition:** I identified patterns across issues
3. **Standard Formulation:** I created rules prohibiting problems
4. **Documentation:** I structured comprehensive standards with examples
5. **Enforcement:** Standards became part of code review process

**Why This Process Works:**

- **Systematic:** I ask myself specific questions and find specific answers
- **Evidence-Based:** I find actual evidence from my codebase, not guesses
- **Actionable:** I create specific implementation patterns, not vague suggestions
- **Comprehensive:** I check everything systematically, not just obvious issues
- **Documented:** Everything becomes part of my knowledge base for future reference

---

## 12. More Patterns from Other Cursor Projects

### 12.1 Email Automation and Analysis Work

**What I Built:**

I conducted a comprehensive analysis of 219,290 emails sent from a higher education Salesforce org over 12 months. This analysis identified automation sources, email templates, and manual email patterns.

**The Problem:**
- Need to understand email usage patterns across the org
- Identify which emails are automated vs manual
- Find opportunities to automate manual emails
- Understand email template usage
- Identify automation sources (Flows, Macros, Apex)

**My Process:**
1. I queried all EmailMessage records from the last 12 months
2. I analyzed email subjects, from addresses, and recipients
3. I matched emails to EmailTemplate records
4. I identified automation sources by matching email patterns to Flow/Macro configurations
5. I categorized emails as: Automated (Flow/Macro), Macro-Sent, Manual (Template-Based), Manual (Unique)
6. I created comprehensive analysis reports with breakdowns by automation source

**What I Found:**
- **34,561 automated emails (15.8%)** - sent through Flows and Apex
- **28,770 macro-sent emails (13.1%)** - sent by staff using macros
- **155,959 manual emails (71.1%)** - sent directly by staff
  - 98,944 template-based (staff using EmailTemplates)
  - 57,015 unique (staff writing custom emails)
- **32 distinct automation sources** identified (7 flows, 25 macros)
- **717 email templates** identified

**Top Automation Sources:**
- Flow: Mid_Point_Evaluation_Screen_Flow - 29,004 emails (83.9% of automated)
- Flow: RT_U_AS_Send_Advisor_Change_Email - 3,635 emails (10.5% of automated)
- Flow: TRAA_Community_Login_Flow - 1,359 emails (3.9% of automated)
- Macro: Initial Cornerstone - 3,976 emails
- Macro: Course Registration Outreach - 3,747 emails

**What I Built:**
- Created comprehensive email analysis reports with:
  - Executive summary with key metrics
  - Automation source breakdown
  - Email template catalog
  - Manual email analysis
  - Automation analysis
  - Data quality fixes documentation
  - Categorization rules documentation
- Built Python scripts to query and analyze email data
- Created documentation for running queries and monitoring progress

**Why This Analysis Was Valuable:**
- Identified opportunities to automate manual emails
- Found email templates that could be reused
- Identified automation sources that were sending high volumes
- Provided data for email optimization decisions
- Created baseline for measuring automation improvements

### 12.2 Application Template Migration Work

**What I Built:**

I created a complete process for migrating Application Templates with all related records (Items and Conditions) between Salesforce environments. This involved complex hierarchical data migration with relationship mapping.

**The Problem:**
- Need to migrate Application Templates from one org to another
- Templates have child Items, Items have child Conditions
- RecordTypeIds are org-specific and must be mapped
- Relationships must be preserved (Template → Items → Conditions)
- All field values must be preserved exactly

**My Solution:**
1. **Export Process:**
   - Created Python script that uses Apex to dynamically discover ALL fields for each object
   - Falls back to comprehensive field list if Apex fails (with warning)
   - Exports Template, Items, and Conditions to JSON files
   - Creates plan file for import

2. **Prepare Process:**
   - Maps RecordTypeIds from source org to target org (by RecordType Name)
   - Updates Template lookup in Items to use referenceId format
   - Maps Item IDs to Names, then Names to referenceIds for Conditions
   - Updates Item lookup in Conditions to use referenceId format
   - Ensures ALL data fields are present (adds null for missing)
   - Removes system fields (Id, CreatedDate, etc.)

3. **Import Process:**
   - Uses `sf data import tree` with combined plan file
   - Ensures correct import order (Template → Items → Conditions)

4. **Verification Process:**
   - Field-by-field comparison between source and target
   - Verifies RecordType matches
   - Verifies item/condition counts match
   - Verifies order numbers match
   - Verifies condition values match

**Critical Lessons I Learned:**
- **Always Export ALL Fields:** Use Apex to dynamically discover fields, have comprehensive fallback
- **RecordTypeId Mapping is Required:** RecordTypeIds are org-specific, must map by Name
- **Relationship Mapping is Critical:** Must query source org to map old IDs → Names → referenceIds
- **Verify Everything:** Don't assume it worked, always do field-by-field comparison
- **System Fields Must Be Removed:** Id, Name (on Conditions), CreatedDate cannot be imported
- **All Fields Must Be Present:** Even if null, fields must be in JSON (sf data export omits nulls)

**What I Built:**
- Python script (`migrate_template_complete.py`) for complete migration process
- Comprehensive migration process documentation
- Error handling for common issues
- Verification checklists
- Usage examples and troubleshooting guide

**Why This Was Complex:**
- Three-level hierarchy (Template → Items → Conditions)
- RecordType mapping between orgs
- Relationship preservation across orgs
- Field discovery and validation
- Order preservation (Screen Number, Screen Order)

### 12.3 Bulk API Job Analysis and Troubleshooting

**What I Built:**

I created Python scripts and analysis documents to troubleshoot Bulk API job failures and identify patterns in failed records.

**The Problem:**
- Bulk API jobs failing with unclear error messages
- Need to identify patterns in failed records
- Need to generate reports on job status and error rates
- Need to correlate job IDs with external system logs

**My Solution:**
1. **Bulk API Job Checker Script:**
   - Queries Bulk API 2.0 jobs using REST API
   - Filters jobs by object, date range, status
   - Identifies failed jobs and extracts error details
   - Generates reports on job status and error rates

2. **Query Bulk API Jobs Script:**
   - Queries specific job details
   - Retrieves failed records for analysis
   - Exports failed records to CSV for analysis
   - Identifies patterns in failed records

3. **Analysis Documents:**
   - Created analysis documents for specific job failures
   - Documented error types and root causes
   - Created troubleshooting guides
   - Documented Workbench step-by-step instructions

**What I Found:**
- Connection timeout errors from integration platform (not Bulk API errors)
- Socket timeout exceptions during Salesforce login
- Need to correlate integration platform execution IDs with Salesforce job IDs
- Pattern identification in failed records (data quality issues, validation errors)

**What I Built:**
- Python scripts for querying and analyzing Bulk API jobs
- Analysis documents for specific job failures
- Troubleshooting guides with step-by-step instructions
- Workbench instructions for manual job analysis
- CSV export scripts for failed records

**Why This Was Valuable:**
- Enabled root cause analysis of integration failures
- Identified data quality issues causing job failures
- Created correlation between external system logs and Salesforce jobs
- Provided methodology for troubleshooting future failures

### 12.4 Integration Error Analysis and Troubleshooting

**What I Built:**

I created analysis documents and methodologies for troubleshooting integration errors between Salesforce and external systems via integration platforms.

**The Problem:**
- Integration platform (ETL tool) errors with unclear root causes
- Need to correlate integration platform execution IDs with Salesforce records
- Need to identify whether errors are from Salesforce, network, or external system
- Need to track error patterns across different integration points

**My Solution:**
1. **Error Analysis Process:**
   - Identified error type (connection timeout, socket timeout, SOAP operation error)
   - Determined error source (Salesforce, network, integration platform)
   - Correlated execution IDs with Salesforce job IDs
   - Analyzed error patterns across different integration points

2. **Root Cause Identification:**
   - Network connectivity issues between integration platform and Salesforce
   - Salesforce API timeout (request took too long)
   - Salesforce service degradation
   - Integration platform timeout settings too short
   - Large data volume causing slow response

3. **Troubleshooting Methodology:**
   - Check Salesforce API status for specific dates
   - Review integration platform logs for retry attempts
   - Verify if job eventually succeeded
   - Check Salesforce org health at time of error
   - Check for scheduled maintenance

**What I Built:**
- Integration error analysis documents
- Root cause identification methodology
- Troubleshooting checklists
- Correlation between integration platform and Salesforce logs

**Why This Was Valuable:**
- Enabled systematic troubleshooting of integration failures
- Identified whether errors were transient or systemic
- Created methodology for future troubleshooting
- Provided correlation between external system logs and Salesforce

### 12.5 Batch Email Processing at Scale

**What I Built:**

I built a Batch Apex class for sending emails to large volumes of contacts while respecting Salesforce governor limits.

**The Problem:**
- Need to send emails to thousands of contacts
- Single email send operations hit governor limits
- Need to support email templates, custom subject/body, attachments
- Need to track success/failure across batches
- Need to log emails as activities on contacts

**My Solution:**
- Created `EmailSenderBatch` class implementing `Database.Batchable<SObject>` and `Database.Stateful`
- Constructor accepts:
  - Email template ID (optional)
  - List of Contact IDs
  - Related record ID for merge fields
  - Org-wide email address ID
  - CC/BCC addresses
  - Attachment IDs
  - Custom subject/body/htmlBody
- Stateful variables track:
  - Total processed
  - Total successful
  - Total failed
  - Error messages
- Start method queries contacts with fields needed for email templates
- Execute method:
  - Processes contacts in batches
  - Queries email template if provided
  - Builds email messages with merge fields
  - Sends emails using `Messaging.sendEmail()`
  - Logs emails as activities if configured
- Finish method provides summary of results

**Why I Built It This Way:**
- **Batchable Interface:** Handles large volumes within governor limits
- **Stateful:** Tracks progress across batches
- **Flexible:** Supports templates or custom content
- **Activity Logging:** Can log emails as activities on contacts
- **Error Tracking:** Captures and reports errors

**What I Learned:**
- Batch processing is essential for large email volumes
- Stateful batches enable progress tracking
- Need to query template separately to get merge field values
- Activity logging should be optional (performance consideration)
- Error tracking helps identify problematic contacts

### 12.6 Batch Fraud Score Calculation

**What I Built:**

I built a Batch Apex class to calculate fraud scores for multiple applications, processing them in chunks while respecting governor limits.

**The Problem:**
- Need to calculate fraud scores for thousands of applications
- Single calculation operations hit governor limits
- Need to process in batches
- Need to track progress and errors
- Need to use same logic as real-time calculation

**My Solution:**
- Created `FraudScoreBatch` class implementing `Database.Batchable<sObject>` and `Database.Stateful`
- Default query selects all applications with applicants
- Custom query constructor allows filtering
- Stateful variables track:
  - Total processed
  - Total updated
  - Total errors
  - Error messages
- Execute method:
  - Collects contact and application IDs
  - Queries all related data in bulk (Contacts, Educational History, Registered Courses)
  - Processes each application using same logic as `FraudScoreController`
  - Checks override conditions first (Military, Nursing, Completed Courses)
  - Calculates fraud score using logistic regression model if no overrides
  - Updates application records with calculated scores
  - Tracks errors for applications that fail
- Finish method provides summary of results

**Why I Built It This Way:**
- **Batchable Interface:** Handles large volumes within governor limits
- **Stateful:** Tracks progress across batches
- **Bulk Data Queries:** Queries all related data once, not per application
- **Same Logic:** Uses same calculation logic as real-time component
- **Error Tracking:** Captures and reports errors without failing entire batch

**What I Learned:**
- Batch processing requires bulk data queries (not per-record queries)
- Stateful batches enable progress tracking and error accumulation
- Need to handle errors gracefully (don't fail entire batch on one error)
- Same calculation logic should be used in batch and real-time (code reuse)

### 12.7 Application and Opportunity Synchronization

**What I Built:**

I built service classes to synchronize Application records with Opportunity records in a higher education CRM.

**The Problem:**
- Applications need to be linked to Opportunities for enrollment tracking
- Opportunities need to be created when applications are submitted
- Existing Opportunities need to be linked to new Applications
- Opportunity status needs to be updated based on Application status
- Need to handle dual degree programs (multiple programs per student)

**My Solution:**
- Created `traa_OpportunityService` class with `createOpportunity()` method
- Logic:
  1. Collects applicant and program IDs from applications
  2. Queries programs to get Opportunity RecordType and Program Start Date
  3. Queries existing Opportunities for applicants (open opportunities only)
  4. For each application:
     - Checks if Opportunity exists for applicant + program combination
     - If exists: Links application to existing Opportunity, updates Opportunity status
     - If not: Creates new Opportunity with:
       - Name: Contact Name + Program Name (truncated to 120 chars)
       - RecordType from Program configuration
       - Stage: "Applied"
       - Status: "Application Started"
       - Role: "Applicant" (or "Inquiry" if existing)
       - Close Date: Program Start Date (or today + 10 days)
       - Primary Application lookup
  5. Creates OpportunityContactRole records for new Opportunities
  6. Updates Applications with Opportunity lookups

**Why I Built It This Way:**
- **Reuse Existing Opportunities:** Don't create duplicates for same applicant + program
- **Program-Driven Configuration:** RecordType and dates come from Program configuration
- **Status Synchronization:** Opportunity status reflects Application status
- **Dual Degree Support:** Handles multiple programs per student
- **Contact Role Creation:** Ensures proper relationship between Opportunity and Contact

**What I Learned:**
- Need to check for existing Opportunities before creating new ones
- Program configuration should drive Opportunity setup (RecordType, dates)
- Opportunity status should reflect Application lifecycle
- Contact Roles are required for proper Opportunity-Contact relationship

### 12.8 Application Form Controller with Complex Logic

**What I Built:**

I built a comprehensive Apex controller for an application form component that handles complex application workflows.

**The Problem:**
- Need to support multi-step application forms
- Need to handle application template logic
- Need to create applications on-demand when users select programs
- Need to support program offering types (online, hybrid, in-person)
- Need to handle logo display from application templates
- Need to support application status transitions
- Need to handle field mapping and validation

**My Solution:**
- Created controller with multiple `@AuraEnabled` methods:
  - `getProgramApplicationForCurrentUser()` - Gets or creates application for current user
  - `getProgramApplicationForUser()` - Gets or creates application for specific user
  - `getProgramApplication()` - Gets application by ID with access check
  - `getLogoDetails()` - Gets logo URL from application template
  - Methods for saving application data, handling file uploads, status transitions
- Logic:
  - Checks if application exists for user + program combination
  - If exists: Returns existing application
  - If not: Creates new application with:
    - Program lookup
    - Applicant lookup (from User ContactId)
    - Term from Program Starting Term
    - Status: "In Progress"
    - Program offering type if provided
  - Uses `without sharing` to access all application data
  - Validates community user access to applications
  - Handles application template field mapping

**Why I Built It This Way:**
- **On-Demand Creation:** Applications created when users start application process
- **Template-Driven:** Application structure driven by Application Template
- **Access Control:** Validates user access while allowing data access
- **Flexible:** Supports different program offering types
- **Status Management:** Handles application status transitions

**What I Learned:**
- Applications should be created on-demand, not pre-created
- Application Templates drive field structure and validation
- Need to validate user access while allowing necessary data access
- Program offering types need to be captured at application creation

### 12.9 SAML JIT Handler Implementation

**What I Built:**

I built a SAML Just-In-Time (JIT) handler for provisioning users on first login via SAML SSO.

**The Problem:**
- Need to create Users when they first log in via SAML
- Need to link Users to existing Contacts (pre-created from migrations)
- Need to handle user attributes from SAML assertions
- Need to set correct Profile, Locale, Timezone, Email Encoding
- Need to handle Contact and Account creation if they don't exist

**My Solution:**
- Created `IEE_MS_JIT_Handler` class implementing `Auth.SamlJitHandler`
- `handleUser()` method:
  - Sets FederationIdentifier from SAML
  - Maps SAML attributes to User fields (email, firstName, lastName)
  - Generates Alias from firstName + lastName (first char + last name, max 5 chars)
  - Copies Locale, Language, Timezone, EmailEncoding from current user
  - Sets Profile to "IEE Client Profile"
  - Links User to Contact via ContactId
  - Creates or updates User
- `handleContact()` method:
  - Creates or finds Contact by name
  - Maps SAML attributes to Contact fields
  - Links Contact to Account
- `handleAccount()` method:
  - Creates or finds Account by name
  - Updates Account name from SAML attributes

**Why I Built It This Way:**
- **JIT Provisioning:** Users created on first login, not pre-created
- **Contact Linking:** Users linked to pre-created Contacts from migrations
- **Attribute Mapping:** SAML attributes mapped to Salesforce fields
- **Profile Assignment:** All users get same profile (permissions via permission sets)
- **Locale Inheritance:** User settings inherited from current user (or org defaults)

**What I Learned:**
- JIT handlers must handle both create and update scenarios
- Contact pre-creation enables user linking on first login
- FederationIdentifier is critical for SAML user matching
- Profile should be minimal (permissions via permission sets)

### 12.10 Custom Metadata Type Accessor Utility

**What I Built:**

I built a utility class for accessing Custom Metadata Type records dynamically.

**The Problem:**
- Need to access Custom Metadata Type records without hardcoding field names
- Need to support different Custom Metadata Types
- Need to build dynamic SOQL queries
- Need to return records as lists or maps

**My Solution:**
- Created `IEE_MS_CustomMetadataAccessor` class with methods:
  - `getFieldNameList()` - Gets all field names for a Custom Metadata Type using Schema describe
  - `getAllRecords()` - Gets all records for a Custom Metadata Type
  - `getAllRecordsOrderBy()` - Gets all records ordered by specified field
  - `getAllRecordsMap()` - Gets all records as a Map (DeveloperName → sObject)
  - `createQueryString()` - Builds dynamic SOQL query from field list
- Logic:
  - Uses Schema.getGlobalDescribe() to get object metadata
  - Gets all fields using fields.getMap().keyset()
  - Builds SOQL query dynamically
  - Limits to 49,000 records (Custom Metadata limit)
  - Returns records as List or Map

**Why I Built It This Way:**
- **Dynamic Field Discovery:** No need to hardcode field names
- **Reusable:** Works with any Custom Metadata Type
- **Flexible:** Returns List or Map based on use case
- **Safe:** Uses Schema describe (respects field-level security)

**What I Learned:**
- Schema describe enables dynamic field discovery
- Custom Metadata Types have 49,000 record limit
- Dynamic SOQL requires careful field list construction
- Map by DeveloperName is most useful for lookups

### 12.11 Survey Feedback Component

**What I Built:**

I built a Lightning Web Component for displaying survey feedback modals to users.

**The Problem:**
- Need to display survey feedback modal to users
- Need to handle modal open/close
- Need keyboard accessibility (ESC key to close)
- Need to prevent body scroll when modal is open
- Need to navigate to survey URL

**My Solution:**
- Created `ieeSurveyFeedback` LWC component with:
  - `@track showModal` - Controls modal visibility
  - `@track surveyUrl` - Survey URL path
  - `handleCloseModal()` - Closes modal and restores body scroll
  - `connectedCallback()` - Adds keyboard event listener, prevents body scroll
  - `disconnectedCallback()` - Removes event listener, restores body scroll
  - `handleKeyDown()` - Handles ESC key to close modal

**Why I Built It This Way:**
- **Modal Pattern:** Standard modal open/close pattern
- **Accessibility:** ESC key support for keyboard users
- **UX:** Prevents body scroll when modal is open
- **Cleanup:** Removes event listeners on component destruction

**What I Learned:**
- Modal components need keyboard accessibility
- Body scroll prevention improves UX
- Event listeners must be cleaned up on component destruction
- Modal visibility should be controlled by tracked property

### 12.12 Additional Batch Processing Classes

**What I Built:**

I built multiple Batch Apex classes for various data processing tasks:

**1. Merge Cases Batch:**
- Processes Contacts in batches
- Merges duplicate Cases for each Contact
- Handles Case merging logic with conflict resolution

**2. Faculty Contact Manager Batch:**
- Processes Faculty Contacts in batches
- Manages faculty contact relationships
- Handles faculty-specific data updates

**3. Calculate Payments Batch:**
- Processes Course Offerings in batches
- Calculates payment amounts
- Updates payment records

**4. Scheduled Payment Batch:**
- Processes Payment records in batches
- Handles scheduled payment processing
- Updates payment status

**5. Formula Share Helper Batch:**
- Processes records in batches
- Calculates and updates formula-based sharing
- Handles sharing recalculation

**Pattern I Established:**
- All batch classes implement `Database.Batchable<SObject>`
- Stateful batches for progress tracking
- Bulk data queries (not per-record queries)
- Error handling without failing entire batch
- Finish method for summary reporting

### 12.13 Additional LWC Components

**What I Built:**

I built multiple Lightning Web Components for various use cases:

**1. Program Selector V2:**
- Improved version of program selector
- Better filtering and selection logic
- Enhanced user experience

**2. Advisor User Manager:**
- Manages advisor user assignments
- Displays advisor user table
- Handles advisor assignment logic

**3. Benefit Rollups:**
- Displays benefit rollup information
- Aggregates benefit data
- Shows benefit summaries

**4. Generic Header:**
- Reusable header component
- Navigation and branding
- Consistent header across portals

**5. Common Header:**
- Common header for portals
- Shared navigation elements
- Portal-specific customization

**Pattern I Established:**
- Reusable components for common UI elements
- Consistent patterns across components
- Proper error handling and loading states
- Accessibility considerations

### 12.14 Additional Apex Service Classes

**What I Built:**

I built multiple Apex service classes for various business logic:

**1. Opportunity Service:**
- Creates and updates Opportunities from Applications
- Handles Opportunity-Application synchronization
- Manages Opportunity status transitions

**2. PDF Converter Utility:**
- Converts content to PDF format
- Handles PDF generation
- Implements Callable interface for Flow integration

**3. Job Scheduler:**
- Schedules batch jobs
- Manages job scheduling logic
- Handles job trigger events

**4. Context User:**
- Provides user context information
- Implements Callable interface
- Used by OmniStudio components

**5. Notification Controller:**
- Handles notification logic
- Sends notifications to users
- Manages notification preferences

**Pattern I Established:**
- Service classes for business logic
- Callable interface for Flow/OmniStudio integration
- Separation of concerns (service vs controller)
- Reusable utility classes

### 12.15 Trigger Framework Implementation

**What I Built:**

I implemented a comprehensive trigger framework with dispatcher pattern, handler interfaces, and metadata-driven bypass logic.

**The Problem:**
- Need consistent trigger handling across all objects
- Need ability to bypass triggers for specific contexts (before-insert, after-update, etc.)
- Need recursion control to prevent infinite loops
- Need permission set-based bypass for specific users
- Need separation of concerns (dispatcher → handler → helper)

**My Solution:**
- Created `IEETriggerDispatcher` class that:
  - Implements dispatcher pattern routing trigger events to handlers
  - Loads `Trigger_Bypass__mdt` Custom Metadata Type records into cache
  - Implements recursion control using context key (object + before/after + insert/update/delete)
  - Checks bypass configuration per trigger context:
    - Before Insert, Before Update, Before Delete
    - After Insert, After Update, After Delete
  - Supports permission set-based bypass (only bypass if user has required permission set)
  - Supports whole trigger bypass (`Bypass_Execution__c` flag)
  - Routes to appropriate handler method based on trigger context
- Created `IEETriggerInterface` interface with methods:
  - `BeforeInsert(List<SObject> newItems)`
  - `BeforeUpdate(Map<Id, SObject> oldItems, Map<Id, SObject> newItems)`
  - `BeforeDelete(Map<Id, SObject> oldItems)`
  - `AfterInsert(List<SObject> newItems)`
  - `AfterUpdate(Map<Id, SObject> oldItems, Map<Id, SObject> newItems)`
  - `AfterDelete(Map<Id, SObject> oldItems, Map<Id, SObject> oldItemsMap)`
- Created handler classes implementing interface:
  - `IEEAccountTriggerHandler` - Handles Account trigger events
  - `IEEJobSchedulerTriggerHandler` - Handles Job Scheduler trigger events
- Created helper classes for business logic:
  - `IEEAccountHelper` - Contains Account business logic
  - Delegates from handler to helper for separation of concerns

**Why I Built It This Way:**
- **Dispatcher Pattern:** Centralized routing logic, easier to maintain
- **Interface Pattern:** Consistent handler structure across all objects
- **Metadata-Driven Bypass:** Can bypass triggers without code changes
- **Recursion Control:** Prevents infinite loops from trigger chains
- **Permission Set Bypass:** Allows specific users to bypass triggers (e.g., data loads)
- **Separation of Concerns:** Dispatcher → Handler → Helper pattern

**What I Learned:**
- Trigger frameworks need recursion control (context key pattern)
- Metadata-driven bypass is essential for data loads and migrations
- Permission set-based bypass provides fine-grained control
- Interface pattern ensures consistent handler structure
- Helper classes keep business logic separate from trigger logic

### 12.16 Case Deduplication and Merge Work

**What I Built:**

I built a Batch Apex class to identify and merge duplicate Cases for Contacts, specifically for Advising Cases.

**The Problem:**
- Multiple Advising Cases created for same Contact
- Need to merge duplicate Cases into master Case
- Need to update Case Subject with standardized format
- Need to handle Contacts with single Cases (just update subject)
- Need to handle Contacts with multiple Cases (merge duplicates)

**My Solution:**
- Created `MergeCases` Batch Apex class:
  - Start method queries Contacts with their Cases (Advising Case RecordType)
  - Execute method:
    - For Contacts with single Case: Updates Subject to standardized format
    - For Contacts with multiple Cases:
      - Identifies master Case (first by CreatedDate DESC)
      - Updates master Case Subject to standardized format
      - Merges duplicate Cases into master using `Database.merge()`
      - Handles multiple duplicates by merging in pairs
  - Subject format: "Advising - [FirstName] [LastName] - [SIS_ID]" or "MISSINGSIS" if no SIS ID

**Why I Built It This Way:**
- **Batch Processing:** Handles large volumes within governor limits
- **Master Selection:** First Case by CreatedDate becomes master (oldest)
- **Pairwise Merging:** Merges duplicates in pairs to handle multiple duplicates
- **Standardized Subjects:** Ensures consistent Case naming
- **SIS ID Handling:** Includes SIS ID in subject for easy identification

**What I Learned:**
- Case merging must be done in pairs (Database.merge limitation)
- Master Case selection should be consistent (CreatedDate)
- Subject standardization improves Case management
- Batch processing essential for large-scale deduplication

### 12.17 Education Cloud TDTM (Trigger Development Toolkit) Pattern

**What I Built:**

I implemented TDTM (Trigger Development Toolkit) pattern for Education Cloud objects, specifically for Lead conversion to Opportunity synchronization.

**The Problem:**
- Need to sync Campaign Member records when Leads are converted
- Need to populate Opportunity lookup on Campaign Member
- Need to follow Education Cloud TDTM pattern for trigger handling
- Need to handle Lead conversion status changes

**My Solution:**
- Created `traa_LeadConversionOpportunity_TDTM` class extending `hed.TDTM_Runnable`:
  - Implements `run()` method that receives:
    - `newList` - New Lead records
    - `oldList` - Old Lead records
    - `triggerAction` - Trigger action (BeforeUpdate, AfterInsert, etc.)
    - `objResult` - Schema describe for Lead object
  - Returns `DmlWrapper` with objects to update
  - Logic:
    - Detects Lead conversion (Status changed AND IsConverted = true)
    - Queries Campaign Members for converted Leads
    - Populates `traa_Opportunity__c` lookup on Campaign Member with ConvertedOpportunityId
    - Adds Campaign Members to DmlWrapper for update
  - TDTM framework handles the actual DML

**Why I Built It This Way:**
- **TDTM Pattern:** Education Cloud standard for trigger handling
- **DmlWrapper Pattern:** TDTM framework manages DML operations
- **Conversion Detection:** Checks both status change and IsConverted flag
- **Lookup Population:** Links Campaign Members to converted Opportunities

**What I Learned:**
- TDTM is Education Cloud's trigger framework pattern
- DmlWrapper allows TDTM to batch DML operations
- Lead conversion detection requires checking multiple fields
- Campaign Member-Opportunity linking is important for tracking

### 12.18 Record-Triggered Flow Patterns

**What I Built:**

I implemented Record-Triggered Flows following consistent patterns for before-save and after-save logic.

**The Problem:**
- Need consistent Flow structure across all record-triggered flows
- Need to separate before-save (field updates) from after-save (related records)
- Need strict entry criteria to avoid unnecessary executions
- Need subflows for reusable logic

**My Solution:**
- **Before-Save Flows:**
  - Strict entry criteria (e.g., Status in ('X', 'Y') AND key fields not null)
  - Fast field updates only (no DML on other objects)
  - No callouts or Platform Events
  - Simple field calculations and defaulting
- **After-Save Flows:**
  - Strict entry criteria
  - First decision node routes by:
    - New vs Update
    - Channel/Source (portal vs internal vs integration)
    - Person type (student vs vendor vs staff)
  - Subflows for complex tasks:
    - "Create Advisor Tasks"
    - "Sync Application Status to Child Objects"
    - "Build Notification Payload"
  - Related record operations
  - Integration calls
  - Platform Event publishing
- **Flow Naming Convention:**
  - `RT_C_BS_Update_Account_Values_from_Parent_Account_Academic_Programs`
  - `RT_` = Record-Triggered
  - `C_` = Create, `U_` = Update, `D_` = Delete
  - `BS_` = Before Save, `AS_` = After Save
  - Descriptive name of what the flow does

**Example Flow I Built:**
- **Flow:** `RT_C_BS_Update_Account_Values_from_Parent_Account_Academic_Programs`
- **Type:** Record-Triggered Flow (Before Save)
- **Object:** Account (Academic Programs)
- **Entry Criteria:** Record Type = Academic Program AND Parent Account is not null
- **Logic:** Updates Account field values from Parent Account when Academic Program is created

**Why I Built It This Way:**
- **Strict Entry Criteria:** Avoids unnecessary Flow executions
- **Before vs After Separation:** Before-save for field updates, after-save for side effects
- **Decision Node Routing:** First node routes by context (New/Update, Channel, Person Type)
- **Subflows:** Reusable logic chunks, easier testing
- **Naming Convention:** Clear, descriptive names indicating trigger type and purpose

**What I Learned:**
- Before-save flows should only update triggering record fields
- After-save flows handle related records, integrations, events
- Strict entry criteria improves performance
- Subflows enable reuse and easier testing
- Naming conventions make flows easier to understand and maintain

### 12.19 Data Migration and Cleanup Patterns

**What I Built:**

I established comprehensive patterns for data migration, cleanup, and deduplication work across multiple projects.

**Migration Patterns I Established:**

1. **Discovery and Profiling:**
   - Source data profiling (record counts, field distributions, null rates)
   - Target model validation
   - Mapping documentation
   - Data quality assessment

2. **Staging and Validation:**
   - Staging objects for data validation
   - Field-by-field comparison queries
   - Relationship validation (parent-child, cross-object links)
   - Business metric validation

3. **Hierarchical Data Migration:**
   - Application Template migration (Template → Items → Conditions)
   - Relationship mapping using referenceIds
   - RecordType mapping between orgs
   - Order preservation (Screen Number, Screen Order)

4. **Backfill Patterns:**
   - Batch Apex for populating new fields on existing records
   - Idempotent backfill logic (can re-run safely)
   - Progress tracking and error handling

**Cleanup Patterns I Established:**

1. **Deduplication:**
   - Case merging for duplicate Cases per Contact
   - Master selection logic (CreatedDate, most complete record)
   - Pairwise merging for multiple duplicates
   - Standardized naming after merge

2. **Data Quality Fixes:**
   - Field value standardization
   - Missing data population
   - Relationship repair (orphaned records)
   - External ID population

3. **Archive and Delete:**
   - Archive objects for old records
   - Batch deletion with logging
   - Row locking prevention (staggered processing)
   - Backup before destructive operations

**What I Learned:**
- Migration requires discovery before execution
- Hierarchical data needs relationship mapping
- RecordType mapping is critical for functionality
- Deduplication needs master selection logic
- Cleanup requires careful logging and backups

### 12.20 Additional Integration and Utility Patterns

**What I Built:**

I built additional integration utilities and patterns beyond the main integration services.

**1. SMS Integration via SMS Magic EU:**
- Built `SendSMSMagicEU` class with `@InvocableMethod` for Flow integration
- Uses Custom Label for API key (not hardcoded)
- Handles HTTP callouts with error handling
- Returns status code, message ID, and error messages
- Callable from Flows for SMS notifications

**2. PDF Conversion Utility:**
- Built `IEE_MS_PDFConverterUtil` class implementing `Callable` interface
- Converts content to PDF format
- Handles PDF generation for documents
- Callable from Flows and OmniStudio

**3. Custom Metadata Accessor:**
- Built `IEE_MS_CustomMetadataAccessor` utility class
- Dynamically discovers Custom Metadata Type fields using Schema describe
- Builds dynamic SOQL queries
- Returns records as List or Map (by DeveloperName)
- Supports ordering and field discovery

**4. Context User Utility:**
- Built `IEEContextUser` class implementing `Callable` interface
- Provides user context information
- Used by OmniStudio components for user data
- Returns user details, permissions, and context

**Pattern I Established:**
- All integration utilities implement `Callable` or `@InvocableMethod` for Flow/OmniStudio integration
- Configuration externalized (Custom Labels, Custom Metadata)
- Error handling with structured responses
- Reusable utility classes for common operations

### 12.21 Comprehensive Sprint 1 Analysis and Code Review Work

**What I Built:**

I conducted a comprehensive enterprise-scale code review and analysis of 43 OmniStudio components for a public sector portal serving 40,000 concurrent users. This analysis work resulted in 18 detailed analysis documents covering every aspect of the implementation.

**The Problem:**

- Need to review 43 OmniStudio components (Integration Procedures, Flex Cards, DataRaptors) for enterprise-scale deployment
- Need to identify critical issues before production
- Need to establish standards and best practices
- Need to provide actionable feedback with evidence
- Need to ensure components can handle 40K concurrent users

**My Process:**

1. **Systematic Component Review:**
   - Reviewed all 56 Integration Procedures
   - Reviewed all 200+ Flex Cards
   - Reviewed all DataRaptors
   - Analyzed error handling, logging, security, performance, configuration

2. **Deep Dive Analysis Documents:**
   - Created Error Handling Analysis document analyzing all Integration Procedures calling MuleSoft APIs
   - Created Logging Analysis Summary analyzing when and how logs are written
   - Created Permission Restructuring Plan with detailed migration steps
   - Created Client Permission Security Review analyzing access control for 40K users
   - Created Components Architectural Deep Dive with call-outs and solutions
   - Created Components Enterprise Review with critical findings summary
   - Created Components Detailed Analysis with industry best practices
   - Created OmniStudio Best Practices Review identifying critical issues
   - Created Data Dictionary Comprehensive Analysis analyzing field descriptions, help text, duplicates
   - Created Data Dictionary Field Source Analysis analyzing field population sources
   - Created Data Dictionary Repository Comparison comparing data dictionary vs actual metadata
   - Created Hardcoded URLs in Flex Cards inventory
   - Created URL Storage Recommendation analyzing Custom Labels vs Custom Metadata

3. **Evidence-Based Findings:**
   - Found 53 Integration Procedures with `failOnStepError: false` (silent failures)
   - Found 5 Integration Procedures with hardcoded URLs
   - Found 29 Integration Procedures missing Named Credentials
   - Found 168 Flex Cards marked inactive
   - Found 7 Flex Cards with hardcoded URLs in Sprint 1 scope
   - Found test components in production
   - Found missing component descriptions
   - Found duplicate fields in same object
   - Found test fields in production

4. **Solution Documentation:**
   - Created complete error handling pattern with JSON examples
   - Created logging pattern with DataRaptor examples
   - Created URL externalization approach (Custom Labels vs Custom Metadata analysis)
   - Created permission restructuring plan with step-by-step migration
   - Created field description standards and examples
   - Created component naming conventions

5. **Comprehensive Feedback Document:**
   - Created 18-point feedback document with:
     - Clear problem statements
     - Evidence from actual code
     - Questions for clarification
     - Action items
     - References to analysis documents
     - Priority levels (Critical, High, Medium)

**What I Found:**

**Critical Issues:**
- 53 Integration Procedures with silent failures (`failOnStepError: false`)
- 5 Integration Procedures with hardcoded URLs (security risk)
- 29 Integration Procedures missing Named Credentials
- 7 Flex Cards with hardcoded URLs (dev URLs in production)
- Test components in production
- Missing error states in Flex Cards
- Missing loading states in Flex Cards
- No NULL checks in Integration Procedures
- No error messages returned to users

**High Priority Issues:**
- 44 inactive Integration Procedures
- 168 inactive Flex Cards
- Missing component descriptions
- Hardcoded test data in Flex Cards
- Missing execution conditional formulas
- Missing timeout settings for HTTP actions

**Medium Priority Issues:**
- 27 Integration Procedures with empty descriptions
- 325 instances of empty internal notes
- Inconsistent naming conventions
- Missing help text on fields
- Poor quality field descriptions

**What I Built:**

- 18 comprehensive analysis documents organized by category:
  - Error Handling and Logging (2 documents)
  - Security and Permissions (2 documents)
  - Components (4 documents)
  - Data Dictionary (4 documents)
  - Configuration (2 documents)
- Project Rules and Global Standards document with all established standards
- Sprint 1 Feedback document with 18 questions and action items
- Complete implementation patterns with JSON examples
- Troubleshooting guides and best practices

**Why This Approach Was Effective:**

- **Comprehensive:** I checked everything systematically, not just samples
- **Evidence-Based:** Every finding backed by actual code or configuration
- **Actionable:** Solutions specific with examples, not vague suggestions
- **Prioritized:** Impact assessment helps focus on what matters most
- **Educational:** Developers understand WHY something is wrong, not just that it is
- **Structured:** Organized by category for easy reference
- **Referenceable:** Documents serve as ongoing reference for future work

**What I Learned:**

- Enterprise-scale code reviews require systematic approach
- Evidence-based findings are more persuasive than opinions
- Detailed analysis documents serve as institutional knowledge
- Standards emerge from patterns found in actual code
- Comprehensive reviews catch issues that sample reviews miss
- Documentation of analysis process helps future reviews

### 12.22 Comprehensive Email Analysis Project

**What I Built:**

I conducted a comprehensive analysis of 219,290 emails sent from a higher education Salesforce org over 12 months, categorizing them by automation source, identifying email templates, and analyzing manual email patterns.

**The Problem:**

- Need to understand email usage patterns across the org
- Need to identify which emails are automated vs manual
- Need to find opportunities to automate manual emails
- Need to understand email template usage
- Need to identify automation sources (Flows, Macros, Apex)
- Need to analyze 220,651 unique outgoing emails (after deduplication)

**My Solution:**

1. **Data Collection:**
   - Queried all EmailMessage records from last 12 months
   - Handled pagination across 1,460 6-hour chunks
   - Filtered out incoming emails (18,593)
   - Removed duplicates (270,798)
   - Excluded emails sent TO @excelsior.edu recipients (20,693)
   - Final dataset: 199,958 emails for analysis

2. **Data Quality Fixes:**
   - Created deduplication script to remove duplicate emails
   - Fixed collection script to filter incoming emails
   - Verified 100% coverage (220,651 vs 220,600 from Salesforce)
   - Created clean deduplicated dataset

3. **Automation Source Identification:**
   - Extracted Flow metadata to identify email actions
   - Extracted Macro metadata to identify email templates
   - Extracted EmailTemplate records
   - Matched emails to Flows by:
     - EmailTemplate subject match (exact, after normalization)
     - FROM address + Subject match
     - Hardcoded subject match
   - Matched emails to Macros by EmailTemplate subject match
   - Identified 40 flows with 62 email actions
   - Identified 58 macros using 56 unique email templates

4. **Email Categorization:**
   - Automated: 14,668 emails (7.3%) - definitively matched to Flows/Macros
   - Macro-Sent: 1,514 emails (0.8%) - sent via Macros
   - Manual: 183,776 emails (91.9%)
     - Manual (Template-Based): 100,444 emails (54.7% of manual)
     - Manual (Unique): 83,332 emails (45.3% of manual)

5. **Template Catalog:**
   - Identified 717 unique email templates from content patterns
   - Cataloged template usage counts
   - Identified template sources (Flow, Macro, Manual)
   - Documented template subjects and from addresses

6. **Analysis Reports Generated:**
   - Executive Summary with key metrics
   - Automation Analysis with detailed breakdown
   - Template Catalog with 717 templates
   - Manual Email Analysis with top senders
   - Complete Email Analysis Report
   - Email Categorization Rules document
   - Data Quality Fixes document

**What I Found:**

**Automation Sources:**
- 30,363 automated emails (13.8%) from 2 identified flows:
  - Mid_Point_Evaluation_Screen_Flow: 29,004 emails (95.5%)
  - TRAA_Community_Login_Flow: 1,359 emails (4.5%)
- 28,770 macro-sent emails (13.1%) from 58 macros
- Top macro: Initial Cornerstone (3,415 emails)

**Manual Email Patterns:**
- 183,776 manual emails (91.9%)
- Top manual sender: erizzuto@excelsior.edu (8,668 emails)
- 465 unique manual senders
- 100,444 manual emails used EmailTemplates (54.7%)
- 83,332 manual emails were unique (45.3%)

**Template Usage:**
- 799 unique EmailTemplate records used
- 717 pattern-based templates identified
- Top template: "your new academic advisor" (34 emails)

**What I Built:**

- Python scripts for email collection with pagination
- Python scripts for deduplication and data quality fixes
- Python scripts for comprehensive email analysis
- Analysis categorization logic (Flow/Macro/Manual matching)
- Template matching algorithms
- Email exclusion rules (internal-only flows, @excelsior.edu recipients)
- Comprehensive analysis reports in Markdown
- CSV exports for further analysis
- Email categorization rules documentation

**Why This Was Complex:**

- **Scale:** 220,651 unique emails to analyze
- **Data Quality:** 270,798 duplicates, 18,593 incoming emails to filter
- **Categorization Logic:** Complex rules for Flow/Macro/Manual matching
- **Template Matching:** Variable subjects with merge fields cannot be matched exactly
- **Pagination:** Required 1,460 queries in 6-hour chunks
- **Deduplication:** Same emails appeared in multiple collection files

**What I Learned:**

- Email analysis requires careful data quality handling
- Template matching is complex (variable subjects cannot be matched)
- Flow/Macro identification requires metadata analysis
- Manual emails can use templates (template-based vs unique)
- Bulk email analysis requires systematic approach
- Deduplication is critical for accurate analysis
- Comprehensive analysis provides actionable insights

### 12.23 Application Template Migration - Complete Process

**What I Built:**

I built a complete migration process for Application Templates with all related records (Items and Conditions) between Salesforce environments, handling three-level hierarchical data with relationship mapping.

**The Problem:**

- Need to migrate Application Templates between orgs
- Templates have hierarchical structure: Template → Items → Conditions
- RecordTypeIds are org-specific (must be mapped)
- Relationships must be preserved (Items link to Template, Conditions link to Items)
- Order must be preserved (Screen Number, Screen Order)
- All fields must be exported (sf data export omits null fields)

**My Solution:**

1. **Export Process:**
   - Uses Apex to dynamically discover ALL fields for each object
   - Falls back to comprehensive field list if Apex fails (with BIG WARNING)
   - Exports Template, Items, and Conditions to JSON files
   - Creates plan file for import
   - Handles 18 Template fields, 44 Item fields, 7 Condition fields

2. **Prepare Process:**
   - Maps RecordTypeIds from source org to target org (by RecordType Name)
   - Updates Template lookup in Items to use referenceId format (`@traa_Application_Template__cRef1`)
   - Maps Item IDs to Names, then Names to referenceIds for Conditions
   - Updates Item lookup in Conditions to use referenceId format (`@traa_Application_Template_Item__cRefX`)
   - Ensures ALL data fields are present (adds null for missing)
   - Removes system fields (Id, CreatedDate, Name on Conditions, etc.)
   - ABORTS if RecordTypeId missing or mapping fails

3. **Import Process:**
   - Uses `sf data import tree` with combined plan file
   - Ensures correct import order (Template → Items → Conditions)
   - Handles relationship linking via referenceIds

4. **Verification Process:**
   - Field-by-field comparison between source and target
   - Verifies RecordType matches
   - Verifies item/condition counts match
   - Verifies order numbers match (Screen Number, Screen Order)
   - Verifies condition values match

**Critical Lessons I Learned:**

- **Always Export ALL Fields:** Use Apex to dynamically discover fields, have comprehensive fallback
- **RecordTypeId Mapping is Required:** RecordTypeIds are org-specific, must map by Name
- **Relationship Mapping is Critical:** Must query source org to map old IDs → Names → referenceIds
- **Verify Everything:** Don't assume it worked, always do field-by-field comparison
- **System Fields Must Be Removed:** Id, Name (on Conditions), CreatedDate cannot be imported
- **All Fields Must Be Present:** Even if null, fields must be in JSON (sf data export omits nulls)
- **Test with ONE Template First:** Don't create multiple templates, fix ONE completely

**What I Built:**

- Python script (`migrate_template_complete.py`) for complete migration process
- Comprehensive migration process documentation
- Error handling for common issues (RecordType missing, mapping failures)
- Verification checklists
- Usage examples and troubleshooting guide
- Field discovery logic using Apex
- Relationship mapping logic

**Why This Was Complex:**

- Three-level hierarchy (Template → Items → Conditions)
- RecordType mapping between orgs
- Relationship preservation across orgs
- Field discovery and validation
- Order preservation (Screen Number, Screen Order)
- ReferenceId format for relationships
- System field removal
- Null field handling

**What I Learned:**

- Hierarchical data migration requires careful relationship mapping
- RecordType mapping is critical for functionality
- ReferenceIds enable relationship preservation across orgs
- Field discovery prevents missing fields
- Verification is essential - don't assume it worked
- System fields must be explicitly removed
- Null fields must be explicitly added

### 12.24 Bulk API Job Analysis and Troubleshooting

**What I Built:**

I created Python scripts and analysis documents to troubleshoot Bulk API job failures, identify patterns in failed records, and correlate integration platform errors with Salesforce jobs.

**The Problem:**

- Bulk API jobs failing with unclear error messages
- Need to identify patterns in failed records
- Need to generate reports on job status and error rates
- Need to correlate job IDs with external system logs
- Need to troubleshoot connection timeout errors from integration platform

**My Solution:**

1. **Bulk API Job Checker Script:**
   - Queries Bulk API 2.0 jobs using REST API
   - Filters jobs by object, date range, status
   - Identifies failed jobs and extracts error details
   - Generates reports on job status and error rates
   - Handles pagination using `nextRecordsUrl`

2. **Query Bulk API Jobs Script:**
   - Queries specific job details
   - Retrieves failed records for analysis
   - Exports failed records to CSV for analysis
   - Identifies patterns in failed records

3. **Analysis Documents:**
   - Created analysis documents for specific job failures
   - Documented error types and root causes
   - Created troubleshooting guides
   - Documented Workbench step-by-step instructions
   - Created guides for finding specific job IDs by date/time

**What I Found:**

- Connection timeout errors from integration platform (not Bulk API errors)
- Socket timeout exceptions during Salesforce login
- Need to correlate integration platform execution IDs with Salesforce job IDs
- Pattern identification in failed records (data quality issues, validation errors)
- Jobs from different dates appearing in pagination results

**What I Built:**

- Python scripts for querying and analyzing Bulk API jobs
- Analysis documents for specific job failures
- Troubleshooting guides with step-by-step instructions
- Workbench instructions for manual job analysis
- CSV export scripts for failed records
- Job ID lookup guides by date/time

**Why This Was Valuable:**

- Enabled root cause analysis of integration failures
- Identified data quality issues causing job failures
- Created correlation between external system logs and Salesforce jobs
- Provided methodology for troubleshooting future failures
- Documented Workbench process for manual analysis

**What I Learned:**

- Bulk API job errors can be from integration platform, not Salesforce
- Connection timeouts need investigation of network and timeout settings
- Job ID lookup requires pagination through all jobs
- Failed records analysis reveals data quality patterns
- Correlation with external logs requires execution ID tracking

### 12.25 Integration Error Analysis and Troubleshooting

**What I Built:**

I created analysis documents and methodologies for troubleshooting integration errors between Salesforce and external systems via integration platforms.

**The Problem:**

- Integration platform errors (Boomi/MuleSoft) causing data sync failures
- Need to correlate integration platform execution IDs with Salesforce records
- Need to identify root causes of timeout errors
- Need to troubleshoot socket timeout exceptions
- Need to understand error patterns across different integration points

**My Solution:**

1. **Error Analysis Documents:**
   - Documented specific integration errors with execution IDs
   - Identified error types (connection timeout, socket timeout, login timeout)
   - Analyzed root causes (network issues, Salesforce API timeouts, platform timeout settings)
   - Created troubleshooting steps

2. **Error Correlation:**
   - Correlated integration platform execution IDs with Salesforce job IDs
   - Matched error timestamps across systems
   - Identified patterns in error occurrences

3. **Troubleshooting Methodology:**
   - Check Salesforce API status for error time
   - Review integration platform logs for retry attempts
   - Check if job eventually succeeded
   - Verify Salesforce org health at error time
   - Check for scheduled maintenance

**What I Found:**

- Connection timeout errors: Integration platform unable to connect to Salesforce
- Socket timeout exceptions: Read timed out during SOAP operation
- Login timeout: Error during Salesforce login
- Large data volume causing slow responses
- Integration platform timeout settings too short

**What I Built:**

- Integration error analysis documents
- Error correlation methodology
- Troubleshooting guides
- Root cause analysis patterns
- Error pattern identification

**Why This Was Valuable:**

- Enabled understanding of integration failure root causes
- Provided methodology for troubleshooting future errors
- Created correlation between external system logs and Salesforce
- Identified timeout configuration issues
- Documented error patterns for prevention

**What I Learned:**

- Integration errors can be from platform, not Salesforce
- Timeout errors need investigation of both sides
- Error correlation requires execution ID tracking
- Root cause analysis requires logs from both systems
- Timeout settings may need adjustment for large data volumes

### 12.26 Data Dictionary Analysis and Field Quality Review

**What I Built:**

I conducted comprehensive analysis of field descriptions, help text, duplicates, test fields, formulas, and data quality across all custom objects in a public sector portal.

**The Problem:**

- Need to verify field descriptions match actual repository metadata
- Need to identify missing help text
- Need to find duplicate fields
- Need to identify test fields in production
- Need to verify formula fields match data dictionary
- Need to recommend field type conversions (Text to Picklist)

**My Solution:**

1. **Data Dictionary Comprehensive Analysis:**
   - Analyzed all field descriptions for quality
   - Identified poor quality descriptions (just repeat label)
   - Identified missing help text (ZERO custom fields have help text)
   - Found duplicate fields in same object
   - Found test field in production
   - Found formula field discrepancies

2. **Data Dictionary Field Source Analysis:**
   - Analyzed field population sources
   - Identified which API/integration populates each field
   - Identified fields that should be converted to picklists
   - Documented field population timing (first time, on update)

3. **Data Dictionary Repository Comparison:**
   - Compared data dictionary descriptions against actual repository metadata
   - Found 4 description mismatches
   - Found 1 formula field discrepancy
   - Found 1 typo in data dictionary
   - Verified field labels match

**What I Found:**

**Critical Issues:**
- Test field in production: `IEE_MS_Send_Date_Formula__c` with description "Created by Rishav for Testing Notices"
- Duplicate fields: `Log_Code__c` and `Log_Log_Code__c` both labeled "Log Code"
- Formula field discrepancy: Repository has static text, data dictionary shows URL formula
- 4 field description mismatches (data dictionary has wrong descriptions)

**High Priority Issues:**
- ZERO custom fields have Help Text
- Poor quality descriptions (just repeat label)
- Missing business context in descriptions
- Fields that should be picklists (SourceSystem, Role, LanguageCode)

**Medium Priority Issues:**
- Inconsistent field naming patterns
- Missing source/origin information in descriptions
- Missing validation rules documentation

**What I Built:**

- Data Dictionary Comprehensive Analysis document
- Data Dictionary Field Source Analysis document
- Data Dictionary Repository Comparison document
- Field description quality standards
- Help text recommendations
- Picklist conversion recommendations
- Field description format standards

**Why This Was Valuable:**

- Identified data quality issues before production
- Established field documentation standards
- Provided recommendations for field type improvements
- Created verification process for data dictionary accuracy
- Documented field population sources for maintenance

**What I Learned:**

- Field descriptions must include source, purpose, and business rules
- Help text is essential for user-facing fields
- Text fields with limited values should be picklists
- Data dictionary must be verified against actual metadata
- Test fields must be removed from production
- Duplicate fields create confusion and maintenance issues

### 12.27 URL Externalization and Configuration Management Analysis

**What I Built:**

I analyzed hardcoded URLs across Integration Procedures and Flex Cards, and created recommendations for externalization using Custom Labels vs Custom Metadata Types.

**The Problem:**

- Hardcoded URLs in Integration Procedures (5 found)
- Hardcoded URLs in Flex Cards (7 in Sprint 1 scope)
- Dev/sandbox URLs in production components
- Hardcoded record IDs in URLs
- Environment-specific URLs need configuration
- Public URLs need externalization

**My Solution:**

1. **Hardcoded URLs Inventory:**
   - Searched all Integration Procedures for hardcoded URLs
   - Searched all Flex Cards for hardcoded URLs
   - Identified 5 Integration Procedures with hardcoded URLs
   - Identified 7 Flex Cards with hardcoded URLs in Sprint 1 scope
   - Documented all URLs with locations

2. **URL Storage Recommendation:**
   - Analyzed Custom Labels vs Custom Metadata Types
   - Considered environment-specific requirements
   - Considered categorization needs
   - Considered access patterns (Flex Cards vs Integration Procedures)
   - Recommended hybrid approach:
     - Custom Metadata Types for environment-specific URLs
     - Custom Labels for simple, static URLs used in Flex Cards

3. **Implementation Plan:**
   - Created Custom Metadata Type structure recommendation
   - Created Custom Label naming convention
   - Created access patterns for both approaches
   - Created migration plan for existing hardcoded URLs

**What I Found:**

**Integration Procedures:**
- `IEEUserDetail_IP`: Hardcoded dev API URL
- `IEEDocumentListAPICallout`: Hardcoded dev API URL
- `IEEUserSearch_IP`: Hardcoded dev API URL
- All should use Named Credentials

**Flex Cards:**
- `IEEProgramsPage`: 6 hardcoded public URLs
- `IEEMyInformationParent`: 2 hardcoded URLs (1 dev URL)
- `IEENoticeTileViewParentCard`: 2 hardcoded URLs (1 dev URL + hardcoded record ID)
- `ieeCommonFooter`: 5 hardcoded public URLs
- `IEENLDashboardPage`: 1 hardcoded dev URL
- `IEEChangeInfoCard`: 2 hardcoded URLs
- `IEENoticeDetailsTestcard`: 1 hardcoded dev URL + hardcoded record ID

**What I Built:**

- Hardcoded URLs inventory document
- URL Storage Recommendation document analyzing Custom Labels vs Custom Metadata
- Implementation plan with examples
- Custom Metadata Type structure recommendation
- Custom Label naming convention
- Access pattern examples for both approaches

**Why This Was Valuable:**

- Identified security and maintainability risks
- Provided clear recommendation for URL externalization
- Created implementation plan for migration
- Established standards for URL configuration
- Documented all hardcoded URLs for removal

**What I Learned:**

- Hardcoded URLs are security and maintainability risks
- Environment-specific URLs need Custom Metadata Types
- Simple static URLs can use Custom Labels
- Flex Cards need direct access (Custom Labels easier)
- Integration Procedures can use Custom Metadata via Apex
- Hybrid approach provides best of both worlds

### 12.28 Permission Restructuring and Security Review Work

**What I Built:**

I created a comprehensive permission restructuring plan and security review for a public sector portal serving 40,000 users, moving from profile-based to permission set-based security model.

**The Problem:**

- Permissions split between profiles and permission sets
- Need to move to permission set-driven security model
- Need to remove ALL delete permissions for community users
- Need to ensure principle of least privilege
- Need to review security for 40K user scale
- Need to identify over-privileged access

**My Solution:**

1. **Permission Restructuring Plan:**
   - Analyzed current state: Profile has 406 field permissions, 10 object permissions
   - Analyzed current state: Permission Set has 156 field permissions, 9 object permissions
   - Created migration plan:
     - Step 1: Remove ALL delete permissions
     - Step 2: Move ALL permissions from Profile to Permission Set
     - Step 3: Verify no permissions remain in Profile
   - Documented each permission migration with examples
   - Created verification checklist

2. **Client Permission Security Review:**
   - Reviewed IEE_Client Profile and Permission Set
   - Identified critical security issues:
     - Test classes enabled in Permission Set (security risk)
     - Excessive object permissions (create/delete on critical objects)
     - Sensitive field access (SSN editable)
     - Over-privileged access (viewAllFields on OmniStudio objects)
   - Created recommendations for each issue

**What I Found:**

**Critical Security Issues:**
- Test classes enabled in Permission Set (should NEVER be accessible to users)
- Delete permissions on `IEE_MS_Notice__c` and `IEE_MS_Transaction__c` (should be removed)
- SSN field editable (should be read-only)
- Over-privileged access (viewAllFields on OmniStudio objects)

**Migration Requirements:**
- 406 field permissions to move from Profile to Permission Set
- 10 object permissions to move from Profile to Permission Set
- 2 delete permissions to remove from Permission Set
- Test class access to remove from Permission Set

**What I Built:**

- Permission Restructuring Plan with step-by-step migration
- Client Permission Security Review with critical findings
- Migration examples with before/after XML
- Verification checklist
- Security recommendations

**Why This Was Valuable:**

- Established permission set-driven security model
- Identified critical security vulnerabilities
- Created migration plan for safe restructuring
- Documented security best practices
- Ensured principle of least privilege

**What I Learned:**

- Permission set-driven model is more flexible and maintainable
- Test classes should NEVER be accessible to users
- Delete permissions should be removed for community users
- Sensitive fields (SSN) should be read-only
- Over-privileged access creates security risks
- Migration requires careful planning and verification

### 12.29 Workbench and Troubleshooting Guides

**What I Built:**

I created comprehensive troubleshooting guides and step-by-step instructions for using Workbench to analyze Bulk API jobs, find specific job IDs, and troubleshoot integration errors.

**The Problem:**

- Need to find specific Bulk API job IDs by date/time
- Need to troubleshoot Bulk API job failures
- Need to analyze failed records
- Need step-by-step instructions for Workbench
- Need to correlate integration platform errors with Salesforce jobs

**My Solution:**

1. **Workbench Step-by-Step Guides:**
   - Created guide for finding November 11, 2025 job in Workbench
   - Created guide for using Workbench REST Explorer
   - Created guide for pagination through Bulk API jobs
   - Created guide for getting specific job details
   - Created guide for getting failed records

2. **Bulk API Job Analysis Guides:**
   - Created guide for querying all Bulk API jobs
   - Created guide for filtering jobs by date
   - Created guide for analyzing job states
   - Created guide for troubleshooting job failures

3. **Integration Error Troubleshooting:**
   - Created guide for analyzing integration platform errors
   - Created guide for correlating execution IDs with job IDs
   - Created guide for troubleshooting timeout errors

**What I Built:**

- Workbench step-by-step instructions
- Bulk API job analysis guides
- Integration error troubleshooting guides
- Job ID lookup guides by date/time
- Failed records analysis guides

**Why This Was Valuable:**

- Enabled manual troubleshooting when scripts fail
- Provided step-by-step process for non-technical users
- Documented Workbench process for future reference
- Created methodology for troubleshooting integration errors
- Enabled correlation between external logs and Salesforce

**What I Learned:**

- Workbench requires pagination for large result sets
- Job ID lookup requires systematic pagination
- Failed records analysis reveals data quality patterns
- Integration errors need correlation with external logs
- Step-by-step guides are essential for troubleshooting

### 12.30 Data Seeding and Migration Guides

**What I Built:**

I created comprehensive guides for seeding Opportunity data and other objects between Salesforce environments, including data preparation, mapping, and import processes.

**The Problem:**

- Need to seed Opportunity data from higher sandbox to dev sandbox
- Need to handle RecordType mapping between orgs
- Need to handle Account/Contact relationship mapping
- Need to prepare data for import (remove source IDs, map relationships)
- Need to handle required fields and validation rules

**My Solution:**

1. **Opportunity Data Seeding Guide:**
   - Created step-by-step process for exporting Opportunities
   - Created process for exporting related data (Accounts, Contacts)
   - Created data preparation script for import
   - Created RecordType mapping logic
   - Created Account mapping logic (by Name)
   - Created import process using `sf data import tree`

2. **Data Preparation Process:**
   - Maps RecordType DeveloperNames to IDs in target org
   - Maps Account IDs (by Name matching)
   - Removes source org-specific IDs
   - Handles required fields
   - Validates data before import

**What I Built:**

- Opportunity Data Seeding Guide with complete process
- Data preparation scripts
- RecordType mapping logic
- Account mapping logic
- Import process documentation
- Troubleshooting guide

**Why This Was Valuable:**

- Enabled data seeding between environments
- Provided systematic process for data migration
- Handled relationship mapping automatically
- Documented troubleshooting steps
- Created reusable process for future migrations

**What I Learned:**

- RecordType mapping requires DeveloperName matching
- Account mapping by Name is reliable
- Data preparation is critical before import
- Required fields must be validated
- Import process requires careful relationship handling

### 12.31 Email Analysis Methodology and Categorization Rules

**What I Built:**

I developed a comprehensive email categorization system to analyze 219,290 emails sent from a higher education Salesforce org, categorizing them as automated, macro-sent, or manual, and identifying automation sources.

**The Problem:**

- Need to understand email usage patterns across the org
- Need to identify which emails are automated vs manual
- Need to identify automation sources (Flows, Macros, Apex)
- Need to match emails to EmailTemplates
- Need to handle edge cases (org-wide addresses, variable subjects, template reuse)

**My Solution:**

1. **Core Principles I Established:**

   - **Flows Run in User Context:** `CreatedBy` field shows user, not system - cannot use for categorization
   - **Org-Wide Email Addresses Cannot Be Used:** Addresses like `application@excelsior.edu` can be used by both humans and automation
   - **Flow/Macro Template Match Always Wins:** If email matches known Flow/Macro template, it's categorized as automated

2. **Primary Categorization Methods:**

   - **Flow Email Template Match:** Match emails by exact template subject (after normalization) from EmailAlert actions
   - **Flow Composed Email Match:** Match emails by FROM address + Subject for flows that compose emails without templates
   - **Macro Email Template Match:** Match emails by exact template subject from MacroInstruction records
   - **Apex Email Match:** Match emails by FROM address + Subject patterns from Apex classes

3. **Data Quality Fixes I Implemented:**

   - **Deduplication:** Removed 270,798 duplicate emails (53.8% duplicate rate)
   - **Incoming Email Filter:** Filtered out 18,593 incoming emails
   - **Coverage Verification:** Achieved 100.0% coverage (220,651 unique outgoing emails vs 220,600 Salesforce count)

4. **Categorization Rules I Developed:**

   - **Template Matching:** Exact subject match after normalization (remove merge fields, lowercase, trim whitespace)
   - **Pattern Sorting:** Sort patterns by specificity (both subject AND from_address = Priority 1, just subject = Priority 2)
   - **Template Resolution:** Resolve template_id to get template subject when pattern has `subject: null`
   - **Macro Exclusion:** If template is used by macros, DO NOT attribute emails to flows (templates used by macros are commonly used manually)
   - **Hardcoded Subject Matching:** Match emails with hardcoded subjects built in flow formulas

5. **Special Cases I Handled:**

   - **Variable Subjects:** EmailTemplates with merge fields cannot be matched exactly
   - **Multiple Flow Matches:** Flag as PROBLEM when email matches multiple flows (indicates overlapping patterns)
   - **Manual Template Usage:** Humans can send emails using same templates - categorize based on template match but acknowledge limitation
   - **Bulk Sending Detection:** Identify bulk sends (same subject, same from, multiple recipients within time window)

**What I Built:**

- Comprehensive email categorization rules document
- Python scripts for email analysis and categorization
- Data quality fixes (deduplication, incoming email filtering)
- Email collection scripts with proper filtering
- Analysis reports with automation sources, template catalogs, manual email patterns

**Why This Was Complex:**

- 219,290 emails to analyze
- Multiple automation sources (Flows, Macros, Apex, Process Builder)
- Template matching with variable subjects
- Org-wide email addresses used by both humans and automation
- User context vs system context confusion
- Data quality issues (duplicates, incoming emails)

**What I Learned:**

- `CreatedBy` field is not reliable for automation detection (flows run in user context)
- Org-wide email addresses cannot distinguish automated vs manual
- Template matching requires normalization and merge field handling
- Data quality is critical (deduplication, filtering)
- Pattern matching requires specificity sorting
- Multiple matches indicate problems (overlapping patterns)
- Manual template usage must be acknowledged

### 12.32 Flow Logic Documentation and Analysis

**What I Built:**

I created comprehensive flow logic documentation for complex before-save flows, documenting trigger conditions, flow sequences, field assignments, and business purpose.

**The Problem:**

- Need to understand complex flow logic for maintenance
- Need to document trigger conditions and field assignments
- Need to understand business purpose of flows
- Need to troubleshoot flow issues

**My Solution:**

1. **Flow Documentation Structure:**

   - **Flow Type and Status:** Document flow type (Before-Save, Record-Triggered, etc.), trigger object, status, API version
   - **Trigger Conditions:** Document all trigger conditions (object, trigger type, trigger event, field conditions)
   - **Flow Logic Sequence:** Document each step with element type, action, filter conditions, fields retrieved, next step
   - **Decision Points:** Document decision logic, conditions, outcomes, paths
   - **Field Assignments:** Document all field assignments with source and target
   - **Formulas:** Document formula expressions and results
   - **Business Purpose:** Document why the flow exists and what it does

2. **Example Flow I Documented:**

   - **Flow:** Before-Save Auto-Launched Flow on Account
   - **Trigger:** Account Created with RecordType = 'Academic_Program' and Starting_Term__c is NOT BLANK
   - **Logic:**
     - Lookup XREF table using Parent's Program_Comb_ID_SEQ__c
     - If XREF found: Copy Formatted_Name__c from XREF
     - If XREF NOT found: Set Formatted_Name__c to "FORMATTED NAME NOT IN XREF "
     - Update Program Start Date and End Date from Starting Term
     - Copy 17 fields from Parent Account
     - Set Account Name using formula: `{Formatted_Name__c} + ' - ' + {Starting_Term__r.Name}`

**What I Built:**

- Comprehensive flow logic documentation
- Flow sequence diagrams
- Field assignment summaries
- Formula documentation
- Business purpose documentation

**Why This Was Valuable:**

- Enabled maintenance and troubleshooting
- Documented complex logic for future developers
- Provided clear understanding of flow behavior
- Enabled flow optimization and improvement

**What I Learned:**

- Flow documentation is essential for complex flows
- Trigger conditions must be clearly documented
- Field assignments must show source and target
- Formulas must be documented with examples
- Business purpose helps understand flow context

### 12.33 Workbench Troubleshooting and Bulk API Analysis Guides

**What I Built:**

I created comprehensive step-by-step guides for using Workbench to troubleshoot Bulk API jobs, find job IDs by date/time, and analyze failed records.

**The Problem:**

- Need to find specific Bulk API jobs by date/time
- Need to troubleshoot Bulk API job failures
- Need to analyze failed records
- Need step-by-step process for non-technical users

**My Solution:**

1. **Workbench Step-by-Step Guides:**

   - **REST Explorer Access:** Guide for accessing Workbench REST Explorer
   - **Job Query Process:** Guide for querying all Bulk API jobs using `/services/data/v65.0/jobs/ingest`
   - **Pagination Process:** Guide for paginating through large result sets using `nextRecordsUrl`
   - **Date Filtering:** Guide for filtering jobs by `createdDate` field
   - **Job Details:** Guide for getting specific job details using job ID
   - **Failed Records:** Guide for getting failed records using `/services/data/v65.0/jobs/ingest/{jobId}/failedResults`

2. **Bulk API Job Analysis Guides:**

   - **Job ID Lookup:** Guide for finding job IDs by date/time
   - **Job State Analysis:** Guide for understanding job states (JobComplete, Failed, Aborted, UploadComplete, InProgress)
   - **Error Analysis:** Guide for analyzing job errors and failed records
   - **Troubleshooting:** Guide for common issues (job not found, pagination issues, authentication errors)

3. **Integration Error Troubleshooting:**

   - **Correlation Process:** Guide for correlating external execution IDs with Salesforce job IDs
   - **Timeout Error Analysis:** Guide for troubleshooting timeout errors
   - **Failed Record Analysis:** Guide for analyzing patterns in failed records

**What I Built:**

- Workbench step-by-step instructions
- Bulk API job analysis guides
- Job ID lookup guides by date/time
- Failed records analysis guides
- Integration error troubleshooting guides
- Visual guides with example responses

**Why This Was Valuable:**

- Enabled manual troubleshooting when scripts fail
- Provided step-by-step process for non-technical users
- Documented Workbench process for future reference
- Created methodology for troubleshooting integration errors
- Enabled correlation between external logs and Salesforce

**What I Learned:**

- Workbench requires pagination for large result sets
- Job ID lookup requires systematic pagination
- Failed records analysis reveals data quality patterns
- Integration errors need correlation with external logs
- Step-by-step guides are essential for troubleshooting
- Visual guides help users understand the process

### 12.34 Data Dictionary Field Source Analysis and Field Quality Review

**What I Built:**

I conducted comprehensive field source analysis for all Sprint 1 fields, documenting population sources, integration points, picklist recommendations, and field quality issues.

**The Problem:**

- Need to understand where fields are populated from
- Need to identify integration points for each field
- Need to recommend field type conversions (Text to Picklist)
- Need to identify field quality issues (poor descriptions, missing help text)
- Need to document field population timing (first population, update triggers)

**My Solution:**

1. **Field Source Analysis:**

   - **Contact Fields:** Documented 9 fields with population sources (User Search API, User Detail API, MPP Validation)
   - **Notice Fields:** Documented 12 fields with population sources (Notice List API, User Object, Contact Lookup)
   - **Transaction Fields:** Documented 8 fields with population sources (User Detail API, Document List API, System Set)
   - **Log Message Fields:** Documented 12 fields with population sources (LOG_LogMessageUtility Apex Class)

2. **Picklist Conversion Recommendations:**

   - **Critical Conversions:** Identified 3 fields that should be converted from Text to Picklist:
     - `IEE_MS_SourceSystem__c` (Values: HIX, MA21, MMIS)
     - `IEE_MS_Role__c` (Values: Client, Vendor Eligibility Worker, Staff)
     - `IEE_MS_LanguageCode__c` (Values: ENG, etc.)
   - **Review Recommendations:** Identified 3 fields that may need picklist conversion (Status__c, CalloutType__c, InterfaceName__c)

3. **Field Quality Review:**

   - **Poor Quality Descriptions:** Identified fields with descriptions that just repeat the label
   - **Missing Help Text:** Identified ZERO custom fields with Help Text in Sprint 1 objects
   - **Field Description Standards:** Established format: `[What it stores] [from where/source system] [for what purpose]. [Business rules/validation if applicable].`

4. **Critical Issues Identified:**

   - **Formula Field Discrepancy:** `IEE_MS_DetailPageURL__c` - Repository has static text, data dictionary shows URL formula
   - **Missing Source System Documentation:** Need documentation on what HIX, MA21, MMIS represent
   - **Inconsistent Field Naming:** `Log_LogMessage__c` object has inconsistent naming patterns (some fields use `LOG_` prefix, some don't)

**What I Built:**

- Comprehensive field source analysis document
- Picklist conversion recommendations
- Field quality review document
- Field description standards and examples
- Critical issues documentation
- Field population source mapping

**Why This Was Valuable:**

- Enabled understanding of data flow and integration points
- Identified data quality improvements (picklist conversions)
- Established field documentation standards
- Identified critical issues requiring resolution
- Enabled better field maintenance and support

**What I Learned:**

- Field source documentation is essential for maintenance
- Picklist conversions improve data quality
- Field descriptions must be meaningful, not just repeat labels
- Help text is critical for user-facing fields
- Inconsistent naming patterns create maintenance challenges
- Formula field discrepancies indicate configuration issues

### 12.35 URL Externalization and Configuration Management Analysis

**What I Built:**

I conducted comprehensive analysis of hardcoded URLs in Flex Cards and Integration Procedures, and developed recommendations for URL externalization using Custom Labels vs Custom Metadata Types.

**The Problem:**

- Found 7 Flex Cards with hardcoded URLs (dev URLs in production)
- Found 3 Integration Procedures with hardcoded URLs (should use Named Credentials)
- Need environment-specific URLs (dev/staging/prod)
- Need categorization and organization of URLs
- Need direct Flex Card access vs Apex access

**My Solution:**

1. **URL Inventory:**

   - **Flex Cards:** Identified 7 Flex Cards with hardcoded URLs:
     - Public URLs (mass.gov, mahix.org)
     - Dev/sandbox URLs in production components
     - Hardcoded record IDs in URLs
   - **Integration Procedures:** Identified 3 Integration Procedures with hardcoded API endpoints

2. **URL Externalization Recommendation:**

   - **Primary Choice: Custom Metadata Types** for:
     - Environment-specific URLs (dev/staging/prod)
     - Categorized URLs (External Sites, Internal Pages, API Endpoints)
     - URLs with metadata (description, category, active status)
   - **Secondary Choice: Custom Labels** for:
     - Simple, static URLs used directly in Flex Cards
     - Public URLs that never change
     - URLs that need direct Flex Card access without Apex

3. **Proposed Custom Metadata Structure:**

   - **Custom Metadata Type:** `IEE_MS_URL_Configuration__mdt`
   - **Fields:**
     - `Category__c` (Picklist) - External Site | Internal Page | API Endpoint
     - `URL_Type__c` (Picklist) - SSO | Report Changes | Notice Details | Dashboard
     - `Dev_URL__c` (URL) - Development environment URL
     - `Staging_URL__c` (URL) - Staging environment URL
     - `Prod_URL__c` (URL) - Production environment URL
     - `Description__c` (Long Text) - What this URL is used for
     - `Is_Active__c` (Checkbox) - Enable/disable URL

4. **Implementation Approach:**

   - **Hybrid Approach:** Use Custom Metadata for environment-specific URLs, Custom Labels for simple static URLs
   - **Access Pattern:** Custom Metadata via Apex (for IPs), Custom Labels via direct access (for Flex Cards)
   - **Migration Process:** Replace hardcoded URLs with externalized values, remove hardcoded record IDs

**What I Built:**

- Hardcoded URL inventory document
- URL externalization recommendation document
- Custom Metadata vs Custom Labels analysis
- Proposed Custom Metadata structure
- Implementation approach and migration plan

**Why This Was Valuable:**

- Identified security and maintainability risks
- Provided clear recommendation for URL externalization
- Enabled environment-specific URL management
- Created categorization structure for URLs
- Established implementation approach

**What I Learned:**

- Hardcoded URLs are security and maintainability risks
- Environment-specific URLs require Custom Metadata
- Simple static URLs can use Custom Labels
- Hybrid approach provides flexibility
- Direct Flex Card access requires Custom Labels
- Apex access enables Custom Metadata usage

### 12.36 Permission Restructuring and Security Review Work

**What I Built:**

I conducted comprehensive security review of community user profiles and permission sets, and developed detailed plan for restructuring permissions to follow best practices (Profiles minimal, Permission Sets comprehensive, NO delete permissions).

**The Problem:**

- Permissions split between profiles and permission sets (inconsistent)
- Community users have delete permissions (security risk)
- Test class access in permission sets (should not be there)
- Object permissions in profiles (should be in permission sets)
- Missing profile descriptions
- Excessive user permissions for guest users

**My Solution:**

1. **Permission Restructuring Plan:**

   - **Goal:** Profiles = Minimal Permissions, Permission Sets = All Access, NO Delete Permissions
   - **Step 1:** Remove ALL delete permissions from permission sets
   - **Step 2:** Move ALL permissions from profiles to permission sets
   - **Step 3:** Remove test class access from permission sets
   - **Step 4:** Add profile descriptions
   - **Step 5:** Review and remove excessive guest user permissions

2. **Security Review Findings:**

   - **Delete Permissions:** Found 2 delete permissions in permission sets (IEE_MS_Notice__c, IEE_MS_Transaction__c) - MUST REMOVE
   - **Test Class Access:** Found test class access in permission sets (CommunitiesLandingControllerTest, CommunitiesLoginControllerTest) - MUST REMOVE
   - **Object Permissions in Profiles:** Found 10 object permissions in profiles - MUST MOVE to permission sets
   - **Field Permissions:** Found 406 field permissions in profiles - MUST MOVE to permission sets
   - **Guest User Permissions:** Found excessive user permissions for guest users (AllowUniversalSearch, EnableNotifications, ActivitiesAccess) - SHOULD REMOVE

3. **Permission Set Structure:**

   - **Object Permissions:** All object permissions in permission sets (not profiles)
   - **Field Permissions:** All field permissions in permission sets (not profiles)
   - **Class Access:** All class access in permission sets (not profiles)
   - **User Permissions:** All user permissions in permission sets (not profiles)
   - **NO Delete Permissions:** All delete permissions set to false

**What I Built:**

- Permission restructuring plan with step-by-step migration
- Security review document with findings
- Permission set structure documentation
- Guest user permission review
- Profile description recommendations

**Why This Was Valuable:**

- Identified security risks (delete permissions, test class access)
- Established best practice permission model
- Enabled systematic permission migration
- Improved security posture
- Documented permission structure

**What I Learned:**

- Profiles should be minimal (base configuration only)
- Permission sets should contain all access control
- Delete permissions should never be granted to community users
- Test class access should never be in permission sets
- Guest users should have minimal permissions
- Permission structure must be documented

---

## 13. To Validate

### 13.1 Implementation Details

- Specific Apex class naming conventions
- Exact layering structure and dependency patterns
- SOQL optimization techniques used
- Test coverage targets and strategies
- Integration error handling patterns

### 13.2 Configuration Details

- Specific Custom Metadata Type structures
- Named Credential configurations
- Environment-specific URL configurations
- Integration job tracking field naming conventions

### 13.3 Architecture Decisions

- Full implementation status of EventBridge integration (designed vs. production)
- Specific event types actually published in production
- Identity provider configurations and customizations
- Network security architecture details

### 13.4 Standards and Conventions

- Specific Flow naming patterns and templates
- Apex class naming conventions
- Field naming conventions and standards
- Component naming conventions

---

## Conclusion

This document represents a comprehensive synthesis of actual Salesforce implementation work, architectural thinking, problem-solving approaches, and the evolution of understanding that occurred across multiple enterprise-scale projects. It captures not just what was built, but how it was thought about, analyzed, reviewed, and refined.

The work documented here demonstrates:

- **Deep Analysis:** Comprehensive reviews identifying specific issues with evidence and recommendations
- **Systematic Thinking:** Individual findings leading to systematic standards and patterns
- **Evidence-Based Decisions:** Architecture decisions based on real constraints and requirements
- **Quality Focus:** Rigorous code review processes ensuring enterprise-scale quality
- **Knowledge Management:** Methodology for capturing and organizing institutional knowledge

This is the concrete reality of building enterprise-scale Salesforce solutions—the decisions made, the patterns established, the problems solved, and the standards created through real-world experience, all enhanced and accelerated through the strategic use of Cursor AI as a development, troubleshooting, and learning partner.

---

**Document Version:** 6.0
**Last Updated:** Current
**Source:** Cursor workspace evidence only (no GPT Response content)
**Scope:** All accessible Cursor projects and workspace files (`/Users/pranavnagrecha/VS Code`)
**Focus:** Comprehensive brain dump of development, troubleshooting, code review, org management, data analysis, migration, email analysis, comprehensive enterprise-scale analysis work, email categorization methodology, flow documentation, troubleshooting guides, field source analysis, URL externalization, and permission restructuring work using Cursor AI
**Total Sections:** 13 major sections with 36+ detailed subsections covering all aspects of Salesforce implementation work
**Content Sources:** Apex classes, LWC components, OmniStudio metadata, Flow metadata, markdown analysis documents, troubleshooting guides, migration scripts, email analysis scripts, code review documents, security reviews, data dictionary analysis, and comprehensive project documentation
