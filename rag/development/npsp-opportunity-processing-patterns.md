---
layout: default
title: NPSP Opportunity Processing Patterns
description: Comprehensive process patterns for nonprofit and education fundraising opportunity processing, covering gift entry, pledge management, recurring donations, stage automation, and donor stewardship workflows
permalink: /rag/development/npsp-opportunity-processing-patterns.html
level: Intermediate
tags:
  - npsp
  - opportunity
  - fundraising
  - flow
  - automation
  - nonprofit
last_reviewed: 2025-01-03
---

# NPSP Opportunity Processing Patterns

> **Based on Real Implementation Experience**: These patterns reflect real-world nonprofit and education fundraising implementations, covering gift entry workflows, pledge fulfillment, recurring donation management, and donor stewardship automation.

## Overview

Opportunity processing is central to nonprofit and education fundraising operations, encompassing gift entry, pledge management, recurring donation processing, stage automation, and donor stewardship workflows. Unlike traditional B2B sales processes, NPSP Opportunity processing focuses on revenue recognition, donor relationships, grant compliance, and stewardship activities that build long-term donor engagement.

Effective Opportunity processing requires understanding how gifts flow from initial commitment through payment receipt, how recurring donations create child Opportunities automatically, how stage changes trigger acknowledgment and receipt workflows, and how batch gift entry processes handle high-volume donation processing. These patterns enable organizations to process gifts efficiently while maintaining data quality and donor relationships.

## Prerequisites

- **Required Knowledge**:
  - Understanding of NPSP Opportunity and Gift data model (Payments, Recurring Donations, Allocations)
  - Knowledge of Record-Triggered Flows and automation patterns
  - Familiarity with Opportunity stages and stage progression
  - Understanding of Account/Contact relationship models (Households, Organizations)

- **Recommended Reading**:
  - <a href="{{ '/rag/data-modeling/npsp-opportunity-gift-model.html' | relative_url }}">NPSP Opportunity and Gift Data Model</a> - Data model for gifts, payments, and allocations
  - <a href="{{ '/rag/development/flow-patterns.html' | relative_url }}">Flow Design and Orchestration Patterns</a> - Flow automation patterns
  - <a href="{{ '/rag/development/locking-and-concurrency-strategies.html' | relative_url }}">Locking and Concurrency Strategies</a> - Handling concurrent updates and locking errors
  - <a href="{{ '/rag/best-practices/sales-cloud-features.html' | relative_url }}">Sales Cloud Features</a> - Core Sales Cloud features used by NPSP

## When to Use

### Use This When

- Implementing gift entry and donation processing workflows
- Automating stage progression based on payment status
- Managing recurring donation creation and payment processing
- Building pledge fulfillment and payment reminder workflows
- Implementing donor stewardship and acknowledgment automation
- Processing batch gift entry from online giving platforms or imports
- Handling major gift and grant review and approval workflows

### Avoid This When

- Pure B2B sales opportunity processing without fundraising context
- Simple revenue tracking that doesn't require payment schedules or stewardship
- Systems that don't need to differentiate between gift types or donor relationships
- Revenue models that don't align with gift/donation terminology

## Core Concepts

### Stage Design for Fundraising Pipelines

**What it is**: Opportunity stages in NPSP represent gift status progression from commitment through payment receipt and acknowledgment.

**Common stage progression**:
- **Prospecting**: Initial donor interest or cultivation
- **Cultivation**: Ongoing relationship building and engagement
- **Solicitation**: Ask made, awaiting response
- **Pledged**: Commitment received, payments scheduled
- **Posted**: Payment received, gift posted to accounting
- **Closed Won**: Gift fully processed and acknowledged
- **Closed Lost**: Commitment not fulfilled or gift declined

**Stage-specific automation**:
- Pledged → Create Payment records with scheduled dates
- Posted → Trigger acknowledgment and receipt workflows
- Closed Won → Complete stewardship activities and update donor records

**Best practice**: Design stages to match organizational fundraising workflow. Use Record Types to support different stage progressions for different gift types (Donation, Grant, Major Gift). Configure stage-specific fields and automation.

### Donor Stewardship Tasks

**What it is**: Stewardship tasks track follow-up activities, acknowledgments, and relationship-building activities with donors.

**Key stewardship activities**:
- Thank-you calls and emails
- Acknowledgment letter generation and mailing
- Receipt generation and delivery
- Follow-up reminders for pledges
- Donor recognition and engagement activities

**Automation patterns**:
- Create Tasks when Opportunities reach specific stages
- Trigger acknowledgment workflows when Payments are received
- Schedule follow-up reminders for pending pledges
- Generate receipts and acknowledgment letters automatically

**Best practice**: Automate stewardship task creation based on Opportunity stage and payment status. Use Task assignment rules to route stewardship activities to appropriate staff. Track stewardship completion for donor relationship management.

### Ownership and Teams

**What it is**: Opportunity ownership determines who manages the gift relationship, while teams enable collaboration and visibility.

**Ownership patterns**:
- **Opportunity Owner**: Primary gift officer or fundraiser responsible for relationship
- **Account Owner**: Organization or household owner (may differ from Opportunity Owner)
- **Contact Roles**: Additional contacts involved in gift (board members, influencers)

**Team patterns**:
- Add gift officers to Opportunity Team for collaboration
- Use Public Groups for department-level visibility
- Configure sharing rules for cross-department access

**Best practice**: Assign Opportunity Owner based on gift size, donor relationship, or territory. Use Opportunity Teams for major gifts requiring multiple staff collaboration. Configure sharing rules to ensure appropriate visibility.

## Patterns and Examples

### Pattern 1: Automated Donation Opportunity Creation from Online Forms

**Intent**: Automatically create donation Opportunities from online giving forms or web-to-lead conversions.

**Structure**:
- Online form submission creates Lead or Contact record
- Record-Triggered Flow detects new Lead/Contact with donation intent
- Flow creates Opportunity with Amount, Close Date, and Record Type
- Flow creates Payment record if payment information provided
- Flow assigns Opportunity Owner based on gift amount or territory

**Example Flow Logic**:
1. **Trigger**: Lead created with LeadSource = "Online Giving" OR Contact created with custom field "Donation_Intent__c" = true
2. **Get Records**: Retrieve Account (Household) for Contact, or create new Account if needed
3. **Create Records**: Create Opportunity with:
   - Amount = Lead/Contact custom field "Donation_Amount__c"
   - Close Date = TODAY()
   - Stage = "Posted" (if payment received) or "Pledged" (if commitment only)
   - Record Type = "Donation"
   - Account = Household Account
   - Contact = Primary Contact
4. **Create Payment** (if payment received): Create Payment with:
   - Amount = Opportunity Amount
   - Payment Date = TODAY()
   - Status = "Paid"
5. **Assignment**: Assign Opportunity Owner based on gift amount (major gifts to major gift officer, others to general fundraising queue)

**Considerations**:
- Handle duplicate detection before creating Opportunities
- Validate payment information before creating Payment records
- Configure error handling for failed Opportunity creation
- Support both one-time and recurring donation form submissions
- Integrate with payment processing platforms (Stripe, PayPal, etc.)

### Pattern 2: Flow-Based Stage Automation for Payment Status

**Intent**: Automatically progress Opportunity stage when payment status changes (e.g., when last payment is posted, auto-progress to Closed Won).

**Structure**:
- Record-Triggered Flow on Payment object (after create/update)
- Flow queries related Opportunity and all Payments
- Flow calculates payment totals and compares to Opportunity Amount
- Flow updates Opportunity Stage based on payment status

**Example Flow Logic**:
1. **Trigger**: Payment created or updated (Status changed to "Paid")
2. **Get Records**: Get Opportunity and all related Payments
3. **Loop Through Payments**: Calculate total paid amount (SUM of Payments where Status = "Paid")
4. **Decision**: 
   - If total paid = Opportunity Amount AND all Payments are "Paid" → Update Stage = "Closed Won"
   - If total paid > 0 AND total paid < Opportunity Amount → Update Stage = "Posted" (partial payment)
   - If total paid = 0 → Keep Stage = "Pledged"
5. **Update Records**: Update Opportunity Stage and custom field "Payment_Status__c"

**Considerations**:
- Handle concurrent payment updates to avoid race conditions
- Use Platform Events or Queueable for high-volume payment processing
- Support partial payments and payment schedule adjustments
- Configure stage progression rules based on organizational requirements
- Log stage changes for audit trail

### Pattern 3: Handling Pledges with Future-Dated Payments and Reminders

**Intent**: Manage multi-payment pledges with scheduled payment dates and automated reminder workflows.

**Structure**:
- Create Opportunity with Stage = "Pledged" and total Amount
- Create multiple Payment records with future Payment Dates and Status = "Pending"
- Scheduled Flow or Process Builder checks for upcoming payment dates
- Send payment reminders before scheduled Payment Dates
- Update Payment Status when payments are received

**Example Flow Logic**:
1. **Pledge Creation**: Opportunity created with Stage = "Pledged", Amount = total pledge amount
2. **Payment Schedule Creation**: Create Payment records with:
   - Amount = installment amount (e.g., $100/month for 12 months)
   - Payment Date = future date (e.g., 2025-01-15, 2025-02-15, ...)
   - Status = "Pending"
3. **Scheduled Reminder Flow** (runs daily):
   - Query Payments where Payment Date = TODAY() + 7 days AND Status = "Pending"
   - Create Tasks for Opportunity Owner: "Send payment reminder for [Opportunity Name]"
   - Send email reminder to donor Contact (if configured)
4. **Payment Receipt**: When payment received, update Payment:
   - Status = "Paid"
   - Payment Date = actual payment date
   - Trigger acknowledgment workflow

**Considerations**:
- Configure reminder timing (7 days before, 3 days before, day of)
- Handle payment schedule adjustments (donor changes payment date)
- Support payment method updates (credit card, check, wire transfer)
- Track pledge fulfillment percentage for reporting
- Handle payment failures and update Payment Status = "Failed"

### Pattern 4: Major Gift and Grant Review and Approval Workflows

**Intent**: Implement approval workflows for major gifts and grants requiring review before acceptance.

**Structure**:
- Create Opportunity with Stage = "Solicitation" or "Under Review"
- Record-Triggered Flow detects major gift threshold or Grant Record Type
- Flow creates Approval Process or custom approval record
- Flow assigns approval tasks to appropriate reviewers
- Flow updates Opportunity Stage based on approval decision

**Example Flow Logic**:
1. **Trigger**: Opportunity created or updated with Amount >= $10,000 OR Record Type = "Grant"
2. **Decision**: 
   - If Amount >= $50,000 → Requires Executive Director approval
   - If Amount >= $10,000 AND Amount < $50,000 → Requires Development Director approval
   - If Record Type = "Grant" → Requires Grant Review Committee approval
3. **Create Approval Record**: Create custom Approval__c record with:
   - Opportunity = Opportunity Id
   - Approver = assigned approver (based on amount or type)
   - Status = "Pending"
   - Due Date = TODAY() + 5 days
4. **Create Task**: Create Task for approver: "Review [Opportunity Name] - $[Amount]"
5. **Approval Decision Flow** (triggered when Approval Status changes):
   - If Approved → Update Opportunity Stage = "Pledged" or "Awarded"
   - If Rejected → Update Opportunity Stage = "Closed Lost", add rejection reason
   - If Requires Changes → Update Opportunity Stage = "Solicitation", add feedback

**Considerations**:
- Configure approval thresholds based on organizational policies
- Support multi-level approvals for very large gifts
- Track approval history and decision rationale
- Handle approval timeouts and escalation
- Integrate with document management for grant proposals and agreements

### Pattern 5: Batch Gift Entry Flows and Data Quality Checks

**Intent**: Process high-volume gift entry from imports, online giving platforms, or batch data loads with data quality validation.

**Structure**:
- Batch import creates Opportunities and Payments via API or Data Loader
- Record-Triggered Flow validates data quality on create/update
- Flow checks for required fields, valid amounts, and duplicate detection
- Flow creates error records or updates Opportunity with validation status
- Flow triggers acknowledgment workflows for valid gifts

**Example Flow Logic**:
1. **Trigger**: Opportunity created (from batch import or API)
2. **Data Quality Checks**:
   - **Required Fields**: Check Account, Contact, Amount, Close Date are populated
   - **Amount Validation**: Check Amount > 0 and Amount <= maximum gift threshold
   - **Date Validation**: Check Close Date is not in future (unless Pledged)
   - **Duplicate Detection**: Check for existing Opportunities with same Account, Amount, Close Date (within 30 days)
3. **Decision**:
   - If validation fails → Create Error_Log__c record, mark Opportunity with custom field "Data_Quality_Status__c" = "Failed"
   - If validation passes → Mark Opportunity with "Data_Quality_Status__c" = "Valid", trigger acknowledgment workflow
4. **Error Handling**: Send notification to data quality team for failed validations
5. **Bulk Processing**: Use Batch Apex or Queueable for high-volume processing to avoid governor limits

**Considerations**:
- Configure data quality rules based on organizational requirements
- Support both API-based and file-based batch imports
- Handle duplicate detection and merge logic
- Log validation errors for troubleshooting and reporting
- Use asynchronous processing for high-volume batch operations
- Integrate with data quality tools and validation services

## Edge Cases and Limitations

### Edge Case 1: Very High-Volume Gift Entry

**Scenario**: Processing thousands of gifts from online giving platforms or batch imports, causing performance issues and locking errors.

**Consideration**:
- Use Batch Apex or Queueable for high-volume Opportunity and Payment creation
- Implement retry logic for UNABLE_TO_LOCK_ROW errors
- Use Platform Events for decoupled processing
- Batch process Payments separately from Opportunities to reduce locking conflicts
- Configure async processing to avoid synchronous governor limits
- Monitor performance and optimize queries for large data volumes

### Edge Case 2: Concurrent Updates from Online Giving Platforms and Staff Users

**Scenario**: Online giving platform creates Opportunity/Payment while staff user is updating same records, causing conflicts.

**Consideration**:
- Use Record-Triggered Flows with "Optimize for Async" to reduce locking conflicts
- Implement retry logic for concurrent update errors
- Use Platform Events to decouple online giving platform updates from staff updates
- Configure field-level security to prevent conflicts on critical fields
- Use custom fields to track update source (Online Platform vs. Staff) for conflict resolution
- Implement conflict resolution workflows for concurrent updates

### Edge Case 3: Recurring Donation Payment Failures

**Scenario**: Recurring Donation payment fails (credit card expired, insufficient funds), requiring failure handling and donor notification.

**Consideration**:
- Configure Recurring Donation automation to handle payment failures
- Create Tasks for Opportunity Owner when payment fails
- Send automated email to donor Contact with payment failure notification
- Update Recurring Donation status to "Failed" or "Paused"
- Support payment method updates and retry logic
- Track payment failure reasons for reporting and donor communication

### Edge Case 4: Pledge Schedule Adjustments

**Scenario**: Donor requests to change pledge payment schedule (amount, frequency, dates), requiring Payment record updates.

**Consideration**:
- Support Payment schedule modifications through Flow or custom UI
- Update Payment Amounts and Payment Dates based on donor request
- Recalculate Opportunity Amount if total pledge amount changes
- Maintain payment history and audit trail for schedule changes
- Send confirmation to donor Contact with updated payment schedule
- Handle partial payments and schedule adjustments mid-pledge

### Limitations

- **Flow Governor Limits**: Record-Triggered Flows have governor limits; high-volume processing may require Batch Apex or Queueable
- **Payment Automation**: NPSP Recurring Donation automation runs on schedule; immediate processing requires custom automation
- **Stage Progression**: Stage progression rules are organization-specific; standard patterns may need customization
- **Approval Processes**: Standard Approval Processes have limitations; complex approvals may require custom objects
- **Batch Processing**: High-volume batch gift entry requires careful governor limit management and async processing
- **Concurrent Updates**: Concurrent updates from multiple sources require conflict resolution and retry logic

## Related Patterns

- <a href="{{ '/rag/data-modeling/npsp-opportunity-gift-model.html' | relative_url }}">NPSP Opportunity and Gift Data Model</a> - Data model for gifts, payments, and allocations
- <a href="{{ '/rag/development/flow-patterns.html' | relative_url }}">Flow Design and Orchestration Patterns</a> - Flow automation patterns and best practices
- <a href="{{ '/rag/development/locking-and-concurrency-strategies.html' | relative_url }}">Locking and Concurrency Strategies</a> - Handling concurrent updates and UNABLE_TO_LOCK_ROW errors
- <a href="{{ '/rag/best-practices/sales-cloud-features.html' | relative_url }}">Sales Cloud Features</a> - Core Sales Cloud features used by NPSP
- <a href="{{ '/rag/best-practices/reports-dashboards.html' | relative_url }}">Reports and Dashboards</a> - Fundraising pipeline and giving history reporting

## Related MCP Knowledge

- <a href="{{ '/rag/mcp-knowledge/lds-patterns.html' | relative_url }}">Lightning Data Service (LDS) Patterns</a> - LDS patterns for Opportunity and Payment data access in LWC
- <a href="{{ '/rag/mcp-knowledge/lwc-development-guide.html' | relative_url }}">LWC Development Guide</a> - LWC patterns for donor-facing and staff-facing Opportunity screens
- <a href="{{ '/rag/mcp-knowledge/lwc-best-practices.html' | relative_url }}">LWC Best Practices</a> - Best practices for building Opportunity management UI components

## Q&A

### Q: How do I automate donation Opportunity creation from online giving forms?

**A**: Automate donation Opportunity creation by: (1) **Online form submission** creates Lead or Contact record, (2) **Record-Triggered Flow** detects new Lead/Contact with donation intent, (3) **Flow creates Opportunity** with Amount, Close Date, and Record Type, (4) **Flow creates Payment record** if payment information provided, (5) **Flow assigns Opportunity Owner** based on gift amount or territory. Integrate with payment processing platforms (Stripe, PayPal) for payment information. Handle duplicate detection and data quality validation.

### Q: How do I automatically progress Opportunity stage when payments are received?

**A**: Automatically progress stage by: (1) **Record-Triggered Flow on Payment** object (after create/update), (2) **Flow queries related Opportunity** and all Payments, (3) **Flow calculates payment totals** and compares to Opportunity Amount, (4) **Flow updates Opportunity Stage** based on payment status. If total paid = Opportunity Amount AND all Payments are "Paid" → Update Stage = "Closed Won". If total paid > 0 AND total paid < Opportunity Amount → Update Stage = "Posted" (partial payment). Handle concurrent payment updates to avoid race conditions.

### Q: How do I handle pledges with future-dated payments and reminders?

**A**: Handle pledges by: (1) **Create Opportunity** with Stage = "Pledged" and total Amount, (2) **Create multiple Payment records** with future Payment Dates and Status = "Pending", (3) **Scheduled Flow** checks for upcoming payment dates (runs daily), (4) **Send payment reminders** before scheduled Payment Dates (create Tasks, send emails), (5) **Update Payment Status** when payments are received. Configure reminder timing (7 days before, 3 days before, day of). Handle payment schedule adjustments and payment failures.

### Q: How do I implement approval workflows for major gifts and grants?

**A**: Implement approval workflows by: (1) **Create Opportunity** with Stage = "Solicitation" or "Under Review", (2) **Record-Triggered Flow** detects major gift threshold or Grant Record Type, (3) **Flow creates Approval Process** or custom approval record, (4) **Flow assigns approval tasks** to appropriate reviewers (based on amount or type), (5) **Flow updates Opportunity Stage** based on approval decision. Configure approval thresholds based on organizational policies. Support multi-level approvals for very large gifts. Track approval history and decision rationale.

### Q: How do I process batch gift entry with data quality checks?

**A**: Process batch gift entry by: (1) **Batch import creates Opportunities** and Payments via API or Data Loader, (2) **Record-Triggered Flow validates data quality** on create/update (required fields, valid amounts, duplicate detection), (3) **Flow creates error records** or updates Opportunity with validation status, (4) **Flow triggers acknowledgment workflows** for valid gifts. Use Batch Apex or Queueable for high-volume processing. Handle duplicate detection and merge logic. Log validation errors for troubleshooting. Integrate with data quality tools.

### Q: How do I handle concurrent updates from online giving platforms and staff users?

**A**: Handle concurrent updates by: (1) **Use Record-Triggered Flows** with "Optimize for Async" to reduce locking conflicts, (2) **Implement retry logic** for concurrent update errors, (3) **Use Platform Events** to decouple online giving platform updates from staff updates, (4) **Configure field-level security** to prevent conflicts on critical fields, (5) **Use custom fields** to track update source for conflict resolution. Implement conflict resolution workflows for concurrent updates.

### Q: How do I handle Recurring Donation payment failures?

**A**: Handle payment failures by: (1) **Configure Recurring Donation automation** to handle payment failures, (2) **Create Tasks** for Opportunity Owner when payment fails, (3) **Send automated email** to donor Contact with payment failure notification, (4) **Update Recurring Donation status** to "Failed" or "Paused", (5) **Support payment method updates** and retry logic. Track payment failure reasons for reporting and donor communication. Enable donor self-service payment method updates.

### Q: What are best practices for NPSP Opportunity processing automation?

**A**: Best practices include: (1) **Automate stage progression** based on payment status and gift type, (2) **Create stewardship tasks** automatically when Opportunities reach specific stages, (3) **Send payment reminders** for pending pledges before scheduled dates, (4) **Validate data quality** on Opportunity and Payment creation, (5) **Handle concurrent updates** with retry logic and async processing, (6) **Support batch gift entry** with data quality checks and error handling, (7) **Configure approval workflows** for major gifts and grants, (8) **Track stewardship completion** for donor relationship management.

