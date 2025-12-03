---
title: "Lead Management and Conversion Data Model"
level: "Intermediate"
tags:
  - data-modeling
  - lead-management
  - lead-conversion
  - duplicate-prevention
  - marketing-attribution
last_reviewed: "2025-01-XX"
---

# Lead Management and Conversion Data Model

## Overview

A comprehensive data model and process guide for Salesforce lead management, supporting lead capture, qualification, routing, conversion, and duplicate management. The model handles leads from multiple sources, automated assignment, scoring, conversion to Contacts/Accounts/Opportunities, and data quality management within a single Salesforce org.

## Prerequisites

**Required Knowledge**:
- Understanding of Salesforce Lead object and lead conversion process
- Knowledge of duplicate management and matching rules
- Familiarity with assignment rules and lead routing
- Understanding of Campaigns and marketing attribution
- Knowledge of Record Types and their use in lead management

**Recommended Reading**:
- `rag/data-modeling/external-ids-and-integration-keys.md` - External ID patterns
- `rag/data-governance/data-quality-stewardship.md` - Duplicate prevention
- `rag/data-modeling/object-setup-and-configuration.md` - Object configuration
- `rag/development/flow-patterns.md` - Automation patterns

## Core Entity Model

### Lead Object

**Representation**: Potential customers who have shown interest but haven't been qualified or converted

**Implementation**:
- Leads as primary records for unqualified prospects
- Support multiple lead sources (Web, Phone, Email, Trade Show, Partner, etc.)
- Link leads to Campaigns for marketing attribution
- Include external system IDs for correlation with marketing automation platforms
- Support multiple lead types through Record Types
- Track lead status and qualification stages explicitly

**Key Standard Fields**:
- `FirstName`, `LastName` - Contact name information
- `Company` - Company name (required field)
- `Email` - Email address
- `Phone` - Phone number
- `MobilePhone` - Mobile phone number
- `Title` - Job title
- `LeadSource` - Source of the lead (picklist)
- `Status` - Lead status (picklist: Open - Not Contacted, Working - Contacted, Qualified, Nurturing, Unqualified)
- `Rating` - Lead rating (Hot, Warm, Cold)
- `Industry` - Industry classification
- `AnnualRevenue` - Company annual revenue
- `NumberOfEmployees` - Company size
- `Street`, `City`, `State`, `PostalCode`, `Country` - Address information
- `Website` - Company website
- `Description` - Lead description/notes
- `OwnerId` - Assigned owner (User or Queue)
- `IsConverted` - Boolean indicating if lead has been converted
- `ConvertedDate` - Date when lead was converted
- `ConvertedAccountId` - Account created from conversion
- `ConvertedContactId` - Contact created from conversion
- `ConvertedOpportunityId` - Opportunity created from conversion

### Account Object (Post-Conversion)

**Representation**: Business accounts created from lead conversion

**Implementation**:
- Accounts created automatically or matched during lead conversion
- Account name typically comes from Lead.Company field
- Support person accounts vs business accounts based on org configuration
- Link to converted Contact through AccountContactRelationship
- Support multiple account types through Record Types

### Contact Object (Post-Conversion)

**Representation**: Individual contacts created from lead conversion

**Implementation**:
- Contacts created automatically during lead conversion
- Contact name comes from Lead.FirstName and Lead.LastName
- Email, phone, and other fields mapped from Lead fields
- Link to Account through AccountContactRelationship
- Support multiple contact types through Record Types

### Opportunity Object (Post-Conversion)

**Representation**: Sales opportunities created from qualified lead conversion

**Implementation**:
- Opportunities created when qualified leads are converted
- Opportunity name typically includes Account name and close date
- Link to Account and Contact
- Support multiple opportunity types through Record Types
- Track opportunity stage, amount, close date, and probability

## Lead Conversion Model

### Conversion Process Overview

**Process Flow**:
1. Lead is created and assigned
2. Lead is qualified (status changes to "Qualified")
3. Lead is converted (creates Account, Contact, and optionally Opportunity)
4. Lead record becomes read-only (IsConverted = true)
5. Related records (Account, Contact, Opportunity) become active

### Field Mapping During Conversion

**Lead to Contact Mapping**:
- `Lead.FirstName` → `Contact.FirstName`
- `Lead.LastName` → `Contact.LastName`
- `Lead.Email` → `Contact.Email`
- `Lead.Phone` → `Contact.Phone`
- `Lead.MobilePhone` → `Contact.MobilePhone`
- `Lead.Title` → `Contact.Title`
- `Lead.Description` → `Contact.Description`
- `Lead.Street` → `Contact.MailingStreet`
- `Lead.City` → `Contact.MailingCity`
- `Lead.State` → `Contact.MailingState`
- `Lead.PostalCode` → `Contact.MailingPostalCode`
- `Lead.Country` → `Contact.MailingCountry`
- Custom fields can be mapped through conversion settings or automation

**Lead to Account Mapping**:
- `Lead.Company` → `Account.Name`
- `Lead.Industry` → `Account.Industry`
- `Lead.AnnualRevenue` → `Account.AnnualRevenue`
- `Lead.NumberOfEmployees` → `Account.NumberOfEmployees`
- `Lead.Website` → `Account.Website`
- `Lead.Street` → `Account.BillingStreet`
- `Lead.City` → `Account.BillingCity`
- `Lead.State` → `Account.BillingState`
- `Lead.PostalCode` → `Account.BillingPostalCode`
- `Lead.Country` → `Account.BillingCountry`
- Custom fields can be mapped through conversion settings

**Lead to Opportunity Mapping**:
- Opportunity name typically auto-generated (e.g., "Account Name - Close Date")
- `Lead.Amount` (if custom field exists) → `Opportunity.Amount`
- `Lead.CloseDate` (if custom field exists) → `Opportunity.CloseDate`
- Custom fields can be mapped through automation

### Account Matching During Conversion

**Matching Logic**:
- Salesforce attempts to match Lead.Company to existing Account.Name
- Matching is case-insensitive and trims whitespace
- If match found, uses existing Account instead of creating new one
- If no match, creates new Account
- Matching can be enhanced with custom logic in Apex or Flow

**Person Account Considerations**:
- If Person Accounts are enabled, conversion behavior differs
- Person Account combines Account and Contact into single record
- Lead conversion creates Person Account instead of separate Account/Contact
- Address fields map to Person Account address fields

### Conversion Settings and Automation

**Standard Conversion Settings**:
- Configure which fields map to Contact, Account, Opportunity
- Set default values for created records
- Configure whether to create Opportunity during conversion
- Set default Opportunity record type and stage

**Automated Conversion Patterns**:
- Use Flow to automate conversion when lead status = "Qualified"
- Use Apex to handle complex conversion logic (duplicate detection, custom matching)
- Use Record-Triggered Flows for simple conversion triggers (⚠️ **Note**: Process Builder and Workflow Rules are deprecated - use Record-Triggered Flows instead)
- Handle conversion errors gracefully with try-catch blocks

**Conversion Error Handling**:
- Validation rules on Account/Contact/Opportunity can block conversion
- Required fields on target objects must be populated
- Duplicate rules can prevent conversion if duplicates exist
- Handle conversion failures with error messages and logging

## Duplicate Rules and Matching Rules

### Duplicate Rule Configuration

**Purpose**: Prevent duplicate leads from being created or identify duplicates during lead creation/update

**Implementation**:
- Create Duplicate Rules in Setup → Duplicate Management
- Configure matching criteria (email, phone, company name, etc.)
- Set action (Block, Allow, Alert)
- Define matching logic (exact match, fuzzy match, etc.)

**Lead Duplicate Rule Patterns**:
- **Email-based matching**: Match on Email field (exact match)
- **Phone-based matching**: Match on Phone or MobilePhone (normalized)
- **Company + Email matching**: Match on Company AND Email (composite key)
- **Name + Company matching**: Match on FirstName + LastName + Company
- **Fuzzy matching**: Use matching rules with similarity thresholds

**Matching Rule Configuration**:
- Create Matching Rules to define how duplicates are identified
- Configure match criteria with field-level matching logic
- Set matching method (Exact, Fuzzy, Phonetic, etc.)
- Define match threshold (percentage or count)
- Test matching rules with sample data

**Common Matching Rule Patterns**:
- **Email Exact Match**: Email field, Exact match, Required
- **Phone Normalized Match**: Phone field, Normalized (strips formatting), Required
- **Company Fuzzy Match**: Company field, Fuzzy match, 80% similarity threshold
- **Name Phonetic Match**: FirstName + LastName, Phonetic match, for name variations

### Duplicate Rule Actions

**Block Action**:
- Prevents duplicate record creation
- Shows error message to user
- Requires user to review and merge duplicates
- Best for high-confidence duplicate scenarios

**Allow Action**:
- Allows duplicate creation but alerts user
- User can choose to continue or review duplicates
- Best for potential duplicates that need review

**Alert Action**:
- Creates duplicate record but shows alert
- User can review and merge later
- Best for low-confidence duplicates

### Duplicate Management Best Practices

**Data Quality**:
- Standardize data formats before duplicate checking (phone numbers, emails, company names)
- Use data cleansing tools to normalize data
- Implement validation rules to enforce data quality

**Matching Strategy**:
- Start with high-confidence matches (email, phone)
- Add composite matching for better accuracy (email + company)
- Use fuzzy matching for company names to catch variations
- Test matching rules with real data before production

**Performance Considerations**:
- Duplicate rules execute during save, impacting performance
- Limit number of matching criteria to essential fields
- Use indexed fields in matching rules for better performance
- Consider batch duplicate detection for large data imports

## Lead Assignment Rules

### Assignment Rule Configuration

**Purpose**: Automatically assign leads to sales representatives or queues based on criteria

**Implementation**:
- Create Lead Assignment Rules in Setup → Lead Assignment Rules
- Define rule entries with criteria and assignments
- Set rule order (more specific rules first)
- Activate assignment rules
- Configure when rules trigger (on create, on manual assignment, or both)

### Assignment Criteria Patterns

**Geographic Assignment**:
- Assign based on Country, State, Postal Code, or custom territory fields
- Example: Country = "United States" AND State = "California" → Assign to West Coast Queue

**Industry-Based Assignment**:
- Assign based on Industry field
- Example: Industry = "Technology" → Assign to Technology Sales Team

**Company Size Assignment**:
- Assign based on AnnualRevenue or NumberOfEmployees
- Example: AnnualRevenue > 10000000 → Assign to Enterprise Sales Queue

**Lead Source Assignment**:
- Assign based on LeadSource field
- Example: LeadSource = "Partner" → Assign to Partner Sales Team

**Product Interest Assignment**:
- Assign based on custom Product Interest fields
- Example: Product_Interest__c = "Product A" → Assign to Product A Sales Team

**Composite Criteria**:
- Combine multiple criteria for precise assignment
- Example: Country = "United States" AND Industry = "Healthcare" AND AnnualRevenue > 5000000 → Assign to Healthcare Enterprise Queue

### Round-Robin Assignment

**Purpose**: Distribute leads evenly across sales representatives

**Implementation**:
- Use Assignment Rules with Round-Robin option
- Configure round-robin queue with multiple users
- System automatically rotates assignment among queue members
- Ensures fair distribution and prevents lead hoarding

**Round-Robin Best Practices**:
- Group users by territory or product expertise
- Monitor assignment distribution to ensure fairness
- Adjust queue membership based on capacity
- Use separate round-robin queues for different lead types

### Assignment Rule Order

**Rule Evaluation**:
- Rules are evaluated in order (top to bottom)
- First matching rule wins
- More specific rules should be higher in order
- General rules should be lower in order

**Example Rule Order**:
1. Enterprise Healthcare (Country = "US" AND Industry = "Healthcare" AND AnnualRevenue > 10000000)
2. Healthcare (Industry = "Healthcare")
3. Enterprise (AnnualRevenue > 10000000)
4. Default (all other leads)

### Assignment Rule Triggers

**On Create**:
- Rules trigger automatically when lead is created
- Applies to API-created leads, web-to-lead, manual creation
- Ensures immediate assignment

**On Manual Assignment**:
- Rules trigger when lead owner is manually changed
- Re-evaluates assignment based on current field values
- Useful for reassignment scenarios

**Both**:
- Rules trigger on both create and manual assignment
- Most common configuration
- Ensures consistent assignment logic

## Lead Status Management

### Standard Lead Status Values

**Common Status Values**:
- **Open - Not Contacted**: New lead, not yet contacted
- **Working - Contacted**: Lead has been contacted, in progress
- **Qualified**: Lead meets qualification criteria, ready for conversion
- **Nurturing**: Lead not ready for sales, in marketing nurture campaign
- **Unqualified**: Lead does not meet qualification criteria
- **Converted**: Lead has been converted (system-managed, read-only)

### Status Progression Patterns

**Linear Progression**:
- Open - Not Contacted → Working - Contacted → Qualified → Converted
- Simple, linear workflow
- Easy to track and report

**Branching Progression**:
- Open - Not Contacted → Working - Contacted → (Qualified OR Nurturing OR Unqualified)
- Supports multiple paths based on qualification
- More complex but flexible

**Status-Based Automation**:
- Use status changes to trigger automation
- Example: Status = "Qualified" → Trigger conversion Flow
- Example: Status = "Nurturing" → Add to marketing campaign

### Status Validation

**Status Transition Rules**:
- Use validation rules to enforce status progression
- Prevent skipping stages (e.g., can't go from "Open" to "Qualified" without "Working")
- Ensure data quality and process compliance

**Status-Based Field Requirements**:
- Require certain fields based on status
- Example: Status = "Qualified" requires Qualification_Score__c > 75
- Use validation rules or Flow to enforce

## Lead Scoring

### Scoring Model Design

**Demographic Scoring**:
- Company size (AnnualRevenue, NumberOfEmployees)
- Industry alignment with target market
- Geographic location
- Job title/role relevance

**Behavioral Scoring**:
- Email engagement (opens, clicks)
- Website visits and page views
- Content downloads
- Form submissions
- Event attendance

**Engagement Scoring**:
- Response to sales outreach
- Meeting scheduled
- Demo requested
- Pricing page visited

### Scoring Implementation

**Manual Scoring**:
- Sales reps assign scores based on conversations
- Simple but subjective
- Requires manual data entry

**Automated Scoring**:
- Use Flow or Apex to calculate scores
- Update score based on activities and field values
- Real-time or batch scoring
- More consistent and scalable

**Einstein Lead Scoring**:
- Use Salesforce Einstein AI for predictive scoring
- Based on historical conversion patterns
- Automatically updates scores
- Requires sufficient historical data

### Score Thresholds

**Qualification Thresholds**:
- Score > 75: Auto-assign to sales
- Score 50-75: Marketing nurture
- Score < 50: General nurture

**Conversion Thresholds**:
- Score > 80: Auto-qualify for conversion
- Score 60-80: Sales review required
- Score < 60: Continue nurturing

## Record Type Strategy

### Lead Record Types

**Types**: Different lead types by source, product, or qualification stage

**Implementation**: Use Record Types to support different lead workflows and processes

### Account Record Types (Post-Conversion)

**Types**: Different account types based on business model

**Implementation**: Use Record Types to distinguish between different account types created from conversion

### Contact Record Types (Post-Conversion)

**Types**: Different contact types based on role or relationship

**Implementation**: Use Record Types to distinguish between different contact types created from conversion

### Opportunity Record Types (Post-Conversion)

**Types**: Different opportunity types by product or sales process

**Implementation**: Use Record Types to support different opportunity workflows and processes

## Field Design Patterns

### Source System Fields

**Pattern**: Lead Source field - should be picklist with controlled values

**Implementation**: Use standard LeadSource picklist or create custom picklist. Standardize source values (Web, Phone, Email, Trade Show, Partner, etc.). Add custom sources as needed (Webinar, Social Media, Referral, etc.). Use for reporting and assignment rules.

### Campaign Tracking Fields

**Pattern**: Campaign fields for marketing attribution

**Implementation**: Use standard Campaign field (lookup to Campaign object). Track first touch and last touch campaigns. Link leads to Campaigns for ROI measurement. Support multi-touch attribution.

### Qualification Fields

**Pattern**: Qualification fields to track BANT or similar criteria

**Implementation**: Budget field (picklist or currency). Authority field (picklist: Decision Maker, Influencer, User). Need field (picklist or text area). Timeline field (date or picklist). Use for qualification scoring and automation.

### Custom Status Fields

**Pattern**: Custom status fields for detailed tracking

**Implementation**: MQL (Marketing Qualified Lead) checkbox. SQL (Sales Qualified Lead) checkbox. Qualification Score (number). Last Contact Date (date). Next Follow-up Date (date).

## Data Quality Patterns

### Field Description Quality

**Standards**:
- Good descriptions include: source, purpose, population method, business rules
- Poor descriptions just repeat label
- Document field purpose and usage
- Include validation rules and automation dependencies

### Help Text

**Pattern**: Add help text for user-facing fields

**Implementation**: Provide guidance to users on field purpose and expected values. Include examples for complex fields. Document business rules and validation criteria. Help users understand data quality requirements.

### Data Standardization

**Pattern**: Standardize data formats for consistency

**Implementation**: Phone numbers: Strip formatting, standardize format. Email addresses: Lowercase, trim whitespace. Company names: Title case, remove extra spaces. Use Flow or Apex to standardize on create/update.

### Data Enrichment

**Pattern**: Enrich lead data with external sources

**Implementation**: Integrate with data enrichment services (ZoomInfo, Clearbit, etc.). Auto-populate missing fields (industry, company size, revenue). Validate and update existing data. Use callouts in Flow or Apex for real-time enrichment.

### Picklist Conversions

**Pattern**: Convert Text fields with limited values to Picklists

**Implementation**: Improve data quality by using picklists for fields with limited valid values. Use for LeadSource, Industry, Rating, and other fields with controlled vocabularies.

## Integration Patterns

### Web-to-Lead Integration

**Pattern**: Capture leads from website forms

**Implementation**:
- Generate web-to-lead HTML form from Salesforce
- Configure field mapping and hidden fields
- Set default values (LeadSource = "Web", Owner, etc.)
- Handle form submissions and create leads automatically

### Marketing Automation Integration

**Pattern**: Sync leads with marketing automation platforms

**Implementation**:
- Integrate with Pardot, Marketo, HubSpot, etc.
- Sync lead data bidirectionally
- Track engagement and update scores
- Handle conversion synchronization

### API-Based Lead Creation

**Pattern**: Create leads via REST/SOAP API

**Implementation**:
- Use Salesforce REST API or SOAP API
- Handle bulk lead creation with Bulk API
- Implement error handling and retry logic
- Support external system ID tracking

## Best Practices

### Lead Object Design

- Use Leads for unqualified prospects
- Link Leads to Campaigns for attribution
- Include external system IDs for integration correlation
- Support multiple lead types through Record Types
- Track lead status and qualification stages explicitly

### Conversion Process Design

- Automate conversion when leads are qualified
- Handle Account matching during conversion
- Map all relevant fields from Lead to Contact/Account/Opportunity
- Create Opportunity only for qualified leads
- Handle conversion errors gracefully

### Duplicate Management

- Implement duplicate rules for high-confidence matches (email, phone)
- Use matching rules with appropriate thresholds
- Standardize data before duplicate checking
- Provide user-friendly duplicate merge interface
- Monitor duplicate creation rates

### Assignment Rules

- Use assignment rules for automatic routing
- Implement round-robin for fair distribution
- Order rules from specific to general
- Test assignment logic with sample data
- Monitor assignment distribution

### Data Quality

- Standardize data formats (phone, email, company name)
- Implement validation rules for required fields
- Use data enrichment for missing information
- Regular data cleansing and deduplication
- Monitor data quality metrics

## Tradeoffs

### Advantages

- Supports complete lead-to-opportunity lifecycle
- Enables marketing attribution and ROI measurement
- Automates lead routing and assignment
- Prevents duplicates with proper configuration
- Integrates with marketing automation platforms

### Challenges

- Complex conversion field mapping
- Duplicate rule performance impact
- Assignment rule maintenance
- Data quality management across sources
- Integration complexity with external systems

## When to Use This Model

Use this lead management model when:

- Implementing sales-driven CRM processes
- Need to track marketing attribution
- Require automated lead routing
- Multiple lead sources (web, phone, email, events)
- Integration with marketing automation platforms
- Need to prevent duplicate leads
- Require lead scoring and qualification

## When Not to Use This Model

Avoid this model when:

- Simple contact management only (no lead qualification needed)
- No marketing attribution requirements
- All prospects are immediately qualified
- Different data model requirements exist
- Person Accounts only (may not need Leads)

## Q&A

### Q: What is the Lead object and when should I use it?

**A**: The **Lead object** represents potential customers who have shown interest but haven't been qualified or converted. Use Leads when: (1) **Tracking unqualified prospects** (before qualification), (2) **Marketing attribution** (tracking lead sources, campaigns), (3) **Lead qualification process** (qualifying leads before conversion), (4) **Multiple lead sources** (web, phone, email, events), (5) **Integration with marketing automation** (marketing platforms create leads).

### Q: How does lead conversion work in Salesforce?

**A**: Lead conversion creates: (1) **Contact** (from Lead name/email), (2) **Account** (from Lead Company, or matched to existing), (3) **Opportunity** (optional, for qualified leads), (4) **Links converted records** (ConvertedAccountId, ConvertedContactId, ConvertedOpportunityId). Conversion can be manual or automated. Once converted, Lead.IsConverted = true and Lead cannot be edited.

### Q: How do I prevent duplicate leads?

**A**: Prevent duplicates by: (1) **Configuring duplicate rules** for Lead object (matching on Email, Name, Company), (2) **Using matching rules** to define match criteria, (3) **Setting blocking vs. alerting rules** (block duplicates or alert users), (4) **Using external IDs** for integration-based leads, (5) **Implementing data quality checks** at entry. Duplicate rules are essential for lead data quality.

### Q: What is lead scoring and how do I implement it?

**A**: **Lead scoring** assigns scores to leads based on criteria (demographics, behavior, engagement). Implement by: (1) **Creating score fields** (Lead Score, Behavioral Score), (2) **Using automation** (Flow, Process Builder) to calculate scores, (3) **Defining scoring criteria** (what increases/decreases score), (4) **Updating scores** based on lead activity, (5) **Using scores for routing** (route high-scoring leads to sales). Lead scoring helps prioritize leads for sales teams.

### Q: How do I route leads to the right sales rep?

**A**: Route leads by: (1) **Assignment rules** (automated routing based on criteria), (2) **Lead source routing** (route by LeadSource), (3) **Territory routing** (route by geography, industry), (4) **Round-robin routing** (distribute leads evenly), (5) **Manual assignment** (users assign leads). Assignment rules can be based on Lead fields (Source, Industry, State, etc.).

### Q: What is the difference between Lead Status and Lead Rating?

**A**: **Lead Status** tracks lead progression (Open - Not Contacted, Working - Contacted, Qualified, Nurturing, Unqualified). **Lead Rating** indicates lead quality (Hot, Warm, Cold). Status tracks process stage, Rating tracks quality. Both are picklist fields on Lead object. Use Status for workflow, Rating for prioritization.

### Q: How do I track marketing attribution for leads?

**A**: Track attribution by: (1) **LeadSource field** (source of lead - Web, Phone, Email, Trade Show), (2) **Campaign association** (link Leads to Campaigns via CampaignMember), (3) **External system IDs** (correlate with marketing automation platforms), (4) **First Touch/Last Touch** (track first and last touchpoints), (5) **Multi-touch attribution** (track all touchpoints). Marketing attribution helps measure marketing effectiveness.

### Q: What happens to converted leads?

**A**: After conversion: (1) **Lead.IsConverted = true** (Lead marked as converted), (2) **Lead becomes read-only** (cannot edit converted leads), (3) **Converted records created** (Contact, Account, Opportunity), (4) **Links maintained** (ConvertedAccountId, ConvertedContactId, ConvertedOpportunityId), (5) **Lead data preserved** (for historical tracking). Converted leads remain in system for reporting and historical tracking.

### Q: How do I handle lead assignment to queues vs. users?

**A**: Assign leads to: (1) **Users** - individual sales reps (direct assignment), (2) **Queues** - team assignment (round-robin, manual assignment from queue). Use queues for: team-based routing, workload distribution, shared lead pools. Use user assignment for: direct ownership, individual accountability. Assignment rules can route to users or queues.

### Q: What are best practices for lead management?

**A**: Best practices include: (1) **Prevent duplicates** (duplicate rules, matching rules), (2) **Implement lead scoring** (prioritize high-quality leads), (3) **Automate routing** (assignment rules for efficiency), (4) **Track marketing attribution** (LeadSource, Campaigns), (5) **Maintain data quality** (validation rules, data quality checks), (6) **Convert qualified leads** (convert when ready), (7) **Monitor lead metrics** (conversion rates, source performance).

## Edge Cases and Limitations

### Edge Case 1: Lead Conversion with Existing Accounts/Contacts

**Scenario**: Converting a lead when Account or Contact already exists, causing duplicate creation or conversion conflicts.

**Consideration**:
- Use duplicate rules to prevent duplicate Account/Contact creation during conversion
- Configure lead conversion settings to use existing Account/Contact when found
- Test lead conversion with existing records to verify behavior
- Handle conversion conflicts gracefully (log conflicts, prevent duplicate creation)
- Use External IDs to match leads to existing Accounts/Contacts

### Edge Case 2: High-Volume Lead Import

**Scenario**: Importing thousands of leads from external systems, causing duplicate creation or assignment rule performance issues.

**Consideration**:
- Use Bulk API for high-volume lead imports
- Implement duplicate prevention before import (pre-validate against existing leads)
- Disable assignment rules during bulk import (assign manually or via batch process)
- Use External IDs for lead matching and idempotent imports
- Test import performance with sample data before full import

### Edge Case 3: Lead Assignment Rule Conflicts

**Scenario**: Multiple assignment rules matching the same lead, causing assignment conflicts or unexpected routing.

**Consideration**:
- Understand assignment rule evaluation order (first matching rule wins)
- Test assignment rules with sample leads to verify routing
- Document assignment rule logic for maintenance
- Use criteria that don't overlap between rules
- Monitor assignment rule performance and adjust as needed

### Edge Case 4: Lead Scoring with Incomplete Data

**Scenario**: Lead scoring formulas failing or producing incorrect scores when required fields are missing.

**Consideration**:
- Use ISBLANK() functions in scoring formulas to handle missing data
- Set default values for scoring fields when data is missing
- Validate lead data before scoring calculation
- Test scoring formulas with incomplete data scenarios
- Document scoring formula logic and field requirements

### Edge Case 5: Lead Conversion with Complex Opportunity Creation

**Scenario**: Converting leads with complex Opportunity creation requirements (multiple products, custom fields, relationships).

**Consideration**:
- Configure lead conversion settings for Opportunity creation
- Use Apex triggers or Flows to handle complex Opportunity creation logic
- Test lead conversion with complex Opportunity requirements
- Handle conversion errors gracefully (log errors, prevent conversion if needed)
- Document Opportunity creation logic for maintenance

### Limitations

- **Lead Conversion Limits**: Lead conversion creates one Account, one Contact, and optionally one Opportunity
- **Converted Lead Editing**: Converted leads become read-only (cannot edit after conversion)
- **Assignment Rule Limits**: Maximum 300 assignment rules per object (varies by org edition)
- **Duplicate Rule Limits**: Maximum 5 duplicate rules per object (varies by org edition)
- **Lead Scoring Complexity**: Lead scoring formulas have complexity limits
- **Campaign Member Limits**: Campaign members have relationship limits
- **External ID Matching**: External IDs must be unique and properly formatted
- **Lead Source Tracking**: Lead Source is a picklist with limited values (may need custom fields)

## Related Patterns

- [External IDs and Integration Keys](external-ids-and-integration-keys.html) - External ID patterns for lead integration
- [Data Quality and Stewardship](../data-governance/data-quality-stewardship.html) - Duplicate prevention patterns
- [Object Setup and Configuration](object-setup-and-configuration.html) - Object configuration patterns

