---
layout: default
title: NPSP Opportunity and Gift Data Model
description: A comprehensive data model for nonprofit and education fundraising, covering how NPSP uses the standard Opportunity object to represent gifts, grants, and donations, along with related NPSP objects like Payments, Recurring Donations, and Allocations
permalink: /rag/data-modeling/npsp-opportunity-gift-model.html
level: Intermediate
tags:
  - npsp
  - opportunity
  - fundraising
  - data-modeling
  - nonprofit
last_reviewed: 2025-01-03
---

# NPSP Opportunity and Gift Data Model

> **Based on Real Implementation Experience**: This model reflects patterns from multiple nonprofit and education cloud implementations using Salesforce Nonprofit Success Pack (NPSP) and Education Cloud, covering donation processing, grant management, and fundraising workflows.

## Overview

The Salesforce Nonprofit Success Pack (NPSP) repurposes the standard **Opportunity** object to represent gifts, grants, and donations in nonprofit and education fundraising contexts. Unlike traditional B2B sales opportunities, NPSP Opportunities track revenue from donors, foundations, and sponsors, with specialized objects like **Payments**, **Recurring Donations**, **Allocations**, and **Soft Credits** supporting complex fundraising workflows.

This data model is essential for organizations that need to track individual donations, multi-payment pledges, recurring gifts, grant awards, and donor stewardship activities. Understanding how NPSP extends the standard Opportunity object enables architects and administrators to design effective fundraising systems that support both one-time and recurring revenue streams.

## Prerequisites

- **Required Knowledge**:
  - Understanding of standard Salesforce Opportunity object and its relationships
  - Knowledge of NPSP core objects (Payments, Recurring Donations, Allocations)
  - Familiarity with Account/Contact relationship models (Households, Organizations)
  - Understanding of Record Types and their use in differentiating gift types

- **Recommended Reading**:
  - <a href="{{ '/rag/data-modeling/lead-management-patterns.html' | relative_url }}">Lead Management and Conversion Data Model</a> - How prospects become donors
  - <a href="{{ '/rag/data-modeling/standard-object-oddities.html' | relative_url }}">Standard Object Oddities</a> - Standard object quirks that impact Opportunities
  - <a href="{{ '/rag/best-practices/sales-cloud-features.html' | relative_url }}">Sales Cloud Features</a> - Core Sales Cloud features used by NPSP
  - <a href="{{ '/rag/development/npsp-opportunity-processing-patterns.html' | relative_url }}">NPSP Opportunity Processing Patterns</a> - Process patterns for gift processing

## When to Use

### Use This When

- Implementing NPSP or Education Cloud fundraising functionality
- Designing data models for donation tracking, grant management, or sponsorship programs
- Need to support multi-payment pledges, recurring donations, or soft credits
- Requiring allocation tracking to General Accounting Units (GAUs) or funds
- Building systems that track both individual and organizational donors
- Need to differentiate between one-time gifts, pledges, and recurring donations

### Avoid This When

- Pure B2B sales opportunities without nonprofit/fundraising context
- Simple revenue tracking that doesn't require payment schedules or allocations
- Systems that don't need to track donor relationships or stewardship
- Revenue models that don't align with gift/donation terminology

## Core Concepts

### Opportunity as Gift Record

**What it is**: In NPSP, the standard Opportunity object represents a gift, grant, or donation rather than a sales opportunity.

**Key characteristics**:
- Opportunity Amount represents the total gift amount (not revenue until paid)
- Close Date represents the expected or actual gift date
- Stage represents gift status (Pledged, Posted, Closed Won, Closed Lost)
- Account represents the donor (Household, Organization, or Individual)
- Contact represents the primary donor contact

**NPSP-specific fields**:
- `npe01__OppPayment__c` (Payment object relationship)
- `npsp__Primary_Contact__c` (Primary donor contact)
- `npsp__Recurring_Donation__c` (Link to Recurring Donation if applicable)
- Custom fields for gift type, designation, acknowledgment status

**Best practice**: Use Record Types to differentiate between Donation, Grant, Major Gift, and other gift types. Configure page layouts and fields based on gift type requirements.

### Payment Object (npe01__OppPayment__c)

**What it is**: NPSP Payment object tracks individual payment transactions against an Opportunity, enabling multi-payment pledges and payment schedules.

**Key characteristics**:
- Links to Opportunity via `npe01__Opportunity__c`
- Tracks payment amount, date, and method
- Supports partial payments and payment schedules
- Enables payment reminders and follow-up workflows
- Payment status (Paid, Pending, Failed, Written Off)

**Relationship model**:
- One Opportunity can have multiple Payments
- Payment total should equal Opportunity Amount when fully paid
- Payments can be scheduled for future dates (pledge fulfillment)

**Best practice**: Create Payments when gifts are received, not just when Opportunities are created. Use Payment records to track pledge fulfillment over time.

### Recurring Donation Object (npe03__Recurring_Donation__c)

**What it is**: NPSP Recurring Donation object manages ongoing donation commitments that create child Opportunities and Payments on a schedule.

**Key characteristics**:
- Links to Account (donor) and Contact (primary donor)
- Defines donation amount, frequency (Monthly, Quarterly, Annual), and start date
- Automatically creates child Opportunities and Payments based on schedule
- Tracks active status and next payment date
- Supports installment tracking and payment reminders

**Relationship model**:
- One Recurring Donation creates multiple child Opportunities
- Each child Opportunity links back to parent Recurring Donation
- Payments are created for each installment

**Best practice**: Use Recurring Donations for monthly, quarterly, or annual giving programs. Configure automation to create child Opportunities and Payments automatically.

### Allocation and GAU Objects

**What it is**: NPSP Allocation objects track how gift amounts are distributed across General Accounting Units (GAUs), funds, or designations.

**Key characteristics**:
- Allocations link Opportunities to GAUs (funds, programs, campaigns)
- Support partial allocations (e.g., 50% to Program A, 50% to Program B)
- Enable reporting by fund, program, or designation
- Support multi-year grant allocations across fiscal periods

**Relationship model**:
- One Opportunity can have multiple Allocations
- Allocation amounts should sum to Opportunity Amount
- GAUs represent funds, programs, or designations

**Best practice**: Use Allocations when gifts need to be split across multiple funds or programs. Configure GAUs to match organizational chart of accounts or fund structure.

### Soft Credits

**What it is**: Soft Credits attribute gift influence to Contacts who aren't the primary donor but influenced the gift (board members, volunteers, event hosts).

**Key characteristics**:
- Track influence relationships separate from primary donor
- Enable reporting on influencer networks and engagement
- Support multiple soft credits per Opportunity
- Differentiate between hard credits (primary donor) and soft credits (influencers)

**Relationship model**:
- Soft Credits link Opportunities to Contacts (influencers)
- One Opportunity can have multiple Soft Credits
- Soft Credits don't affect Opportunity Amount or Payment totals

**Best practice**: Use Soft Credits to track board member influence, volunteer fundraising, and event host contributions. Enable soft credit reporting for donor engagement analysis.

## Patterns and Examples

### Pattern 1: Single One-Time Gift

**Intent**: Model a simple one-time donation with immediate payment.

**Structure**:
- Create Opportunity with Amount = gift amount
- Set Stage = "Posted" or "Closed Won" (depending on org configuration)
- Set Close Date = gift date
- Create single Payment record with Payment Date = gift date, Status = "Paid"
- Link Opportunity to Account (donor) and Contact (primary donor)

**Example**:
- Donor gives $500 one-time gift on 2025-01-15
- Opportunity: Amount = $500, Stage = "Posted", Close Date = 2025-01-15
- Payment: Amount = $500, Payment Date = 2025-01-15, Status = "Paid"
- Account = Donor Household, Contact = Primary Donor

**Considerations**:
- Ensure Payment Amount equals Opportunity Amount for one-time gifts
- Set appropriate Record Type for gift type (Donation, Grant, etc.)
- Configure acknowledgment and receipt workflows

### Pattern 2: Multi-Payment Pledge

**Intent**: Model a pledge commitment with scheduled payments over time.

**Structure**:
- Create Opportunity with Amount = total pledge amount
- Set Stage = "Pledged" (initial stage for commitments)
- Set Close Date = final payment date or pledge commitment date
- Create multiple Payment records with future Payment Dates
- Update Opportunity Stage to "Posted" when all Payments are received

**Example**:
- Donor pledges $1,200 to be paid in 12 monthly installments of $100
- Opportunity: Amount = $1,200, Stage = "Pledged", Close Date = 2025-12-31
- Payments: 12 Payment records, each $100, Payment Dates = 2025-01-15, 2025-02-15, ..., 2025-12-15, Status = "Pending"
- As payments are received, update Payment Status = "Paid" and Payment Date = actual payment date
- When all Payments are "Paid", update Opportunity Stage = "Posted"

**Considerations**:
- Payment Amounts should sum to Opportunity Amount
- Use automation to send payment reminders before scheduled Payment Dates
- Handle partial payments and payment schedule adjustments
- Track pledge fulfillment percentage for reporting

### Pattern 3: Recurring Donation

**Intent**: Model ongoing monthly, quarterly, or annual giving commitments.

**Structure**:
- Create Recurring Donation record with Amount, Frequency, Start Date
- NPSP automation creates child Opportunities and Payments automatically
- Each installment creates new Opportunity and Payment
- Link all child Opportunities to parent Recurring Donation

**Example**:
- Donor commits to $50/month recurring donation starting 2025-01-15
- Recurring Donation: Amount = $50, Frequency = "Monthly", Start Date = 2025-01-15, Status = "Active"
- NPSP creates Opportunity #1: Amount = $50, Close Date = 2025-01-15, Stage = "Posted"
- NPSP creates Payment #1: Amount = $50, Payment Date = 2025-01-15, Status = "Paid"
- NPSP automatically creates subsequent Opportunities and Payments each month
- All child Opportunities link to parent Recurring Donation

**Considerations**:
- Configure Recurring Donation automation settings in NPSP
- Handle payment failures and update Recurring Donation status
- Support Recurring Donation modifications (amount, frequency changes)
- Track Recurring Donation lifetime value and retention

### Pattern 4: Grant with Allocations

**Intent**: Model a grant award with allocations across multiple funds or programs.

**Structure**:
- Create Opportunity (Grant) with Amount = total grant amount
- Set Record Type = "Grant" to differentiate from donations
- Create multiple Allocation records linking to different GAUs
- Allocation Amounts sum to Opportunity Amount
- Track grant reporting requirements and milestones

**Example**:
- Foundation awards $50,000 grant: $30,000 to Program A, $20,000 to Program B
- Opportunity: Amount = $50,000, Record Type = "Grant", Stage = "Awarded", Close Date = 2025-01-01
- Allocation #1: Amount = $30,000, GAU = "Program A Fund"
- Allocation #2: Amount = $20,000, GAU = "Program B Fund"
- Payments created as grant installments are received
- Track grant reporting milestones and compliance requirements

**Considerations**:
- Allocation Amounts must sum to Opportunity Amount
- Use GAUs to represent funds, programs, or designations
- Support multi-year grant allocations across fiscal periods
- Track grant reporting and compliance requirements

### Pattern 5: Soft Credits for Influencers

**Intent**: Attribute gift influence to Contacts who influenced the donation but aren't the primary donor.

**Structure**:
- Create Opportunity with primary donor (Account/Contact)
- Create Soft Credit records linking Opportunity to influencer Contacts
- Soft Credits don't affect Opportunity Amount or Payment totals
- Enable soft credit reporting for engagement analysis

**Example**:
- Organization gives $10,000 gift (primary donor: Organization Account)
- Board Member (Contact) influenced the gift decision
- Opportunity: Amount = $10,000, Account = Organization, Contact = Primary Contact
- Soft Credit: Opportunity = Gift, Contact = Board Member, Role = "Influencer"
- Reporting shows both Organization (hard credit) and Board Member (soft credit) in donor reports

**Considerations**:
- Soft Credits are separate from primary donor relationship
- Use Soft Credits for board members, volunteers, event hosts
- Enable soft credit reporting for donor engagement and influence analysis
- Track soft credit lifetime value for influencer recognition

## Edge Cases and Limitations

### Edge Case 1: Anonymous Gifts

**Scenario**: Donor requests anonymity, requiring special handling of donor information.

**Consideration**:
- Use generic Account/Contact records for anonymous gifts (e.g., "Anonymous Donor")
- Mark Opportunity with custom field indicating anonymous status
- Configure sharing rules to restrict access to anonymous gift details
- Ensure acknowledgment and receipt processes respect anonymity
- Support reporting that aggregates anonymous gifts without exposing donor identity

### Edge Case 2: In-Kind Gifts

**Scenario**: Donor provides goods or services instead of cash, requiring valuation and tracking.

**Consideration**:
- Use custom Record Type or field to mark in-kind gifts
- Track in-kind gift description, valuation, and valuation date
- Create Opportunity with Amount = estimated value (if applicable)
- Use custom fields to track in-kind gift details (description, category, valuation method)
- Support reporting that differentiates cash vs. in-kind gifts
- Consider separate object for in-kind gift details if complex tracking needed

### Edge Case 3: Pass-Through Grants

**Scenario**: Organization receives grant to pass through to another organization, requiring special accounting.

**Consideration**:
- Create Opportunity for grant received (Organization as donor)
- Create related Opportunity or custom object for grant passed through (sub-grantee)
- Track pass-through relationship and reporting requirements
- Use Allocations to track pass-through amounts
- Support reporting that shows both grant received and grant passed through
- Ensure compliance with pass-through grant reporting requirements

### Edge Case 4: Matching Gifts

**Scenario**: Corporate donor matches employee donations, requiring coordination between employee gift and corporate match.

**Consideration**:
- Create Opportunity for employee gift (Employee as donor)
- Create related Opportunity for corporate match (Corporation as donor)
- Link matching gifts through custom relationship field or junction object
- Track matching gift status and corporate match program details
- Support reporting that shows both employee gift and corporate match
- Handle matching gift verification and processing workflows

### Edge Case 5: Multi-Currency Fundraising

**Scenario**: Organization receives gifts in multiple currencies, requiring currency conversion and reporting.

**Consideration**:
- Enable multi-currency in Salesforce org
- Set Opportunity Currency to gift currency
- Use Salesforce currency conversion for reporting in base currency
- Track exchange rates and conversion dates for accurate reporting
- Support reporting in both gift currency and base currency
- Handle currency conversion for Payments and Allocations

### Edge Case 6: Fiscal Year vs. Calendar Year

**Scenario**: Organization uses fiscal year (e.g., July-June) for reporting, but gifts are received on calendar dates.

**Consideration**:
- Use custom Fiscal Year field or formula to calculate fiscal year from Close Date
- Configure reporting to group by fiscal year instead of calendar year
- Support both calendar year and fiscal year reporting
- Handle fiscal year transitions and gift attribution
- Ensure Payments and Allocations align with fiscal year reporting

### Edge Case 7: Partial Write-Offs

**Scenario**: Pledge payment fails or donor cancels commitment, requiring partial write-off of Opportunity Amount.

**Consideration**:
- Create Payment records for received payments (Status = "Paid")
- Create Payment record for write-off amount (Status = "Written Off")
- Update Opportunity Amount if pledge is reduced
- Track write-off reason and date for reporting
- Support reporting that shows both paid and written-off amounts
- Handle write-off workflows and approval processes

### Limitations

- **Payment Limits**: NPSP Payments have relationship limits; very high-volume payment processing may require batch processing
- **Recurring Donation Automation**: Recurring Donation automation runs on schedule; immediate processing requires manual or custom automation
- **Allocation Complexity**: Complex allocation scenarios (multi-year, multi-GAU) may require custom objects or automation
- **Soft Credit Performance**: High-volume soft credit creation can impact reporting performance
- **Currency Conversion**: Multi-currency reporting requires careful configuration and testing
- **Fiscal Year Reporting**: Fiscal year calculations require custom fields or formulas; standard reporting uses calendar year

## Related Patterns

- <a href="{{ '/rag/data-modeling/lead-management-patterns.html' | relative_url }}">Lead Management and Conversion Data Model</a> - How prospects become donors through lead conversion
- <a href="{{ '/rag/data-modeling/standard-object-oddities.html' | relative_url }}">Standard Object Oddities</a> - Standard object quirks that impact Opportunities (e.g., Opportunities don't support queues)
- <a href="{{ '/rag/best-practices/sales-cloud-features.html' | relative_url }}">Sales Cloud Features</a> - Core Sales Cloud features used by NPSP (stages, products, forecasting)
- <a href="{{ '/rag/development/npsp-opportunity-processing-patterns.html' | relative_url }}">NPSP Opportunity Processing Patterns</a> - Process patterns for gift processing, automation, and workflows
- <a href="{{ '/rag/best-practices/reports-dashboards.html' | relative_url }}">Reports and Dashboards</a> - Fundraising pipeline and giving history reporting patterns

## Q&A

### Q: How does NPSP use the standard Opportunity object for gifts?

**A**: NPSP repurposes the standard **Opportunity** object to represent gifts, grants, and donations. The Opportunity Amount represents the total gift amount, Close Date represents the gift date, and Stage represents gift status (Pledged, Posted, Closed Won). NPSP adds custom fields and related objects (Payments, Recurring Donations, Allocations) to support fundraising workflows. The Account represents the donor (Household, Organization, or Individual), and the Contact represents the primary donor contact.

### Q: What's the difference between a Payment and an Opportunity in NPSP?

**A**: The **Opportunity** represents the total gift commitment or amount, while **Payments** represent individual payment transactions against that Opportunity. For one-time gifts, there's typically one Payment equal to the Opportunity Amount. For multi-payment pledges, there are multiple Payments that sum to the Opportunity Amount. Payments track payment dates, methods, and status (Paid, Pending, Failed, Written Off), enabling pledge fulfillment tracking and payment reminders.

### Q: How do Recurring Donations work in NPSP?

**A**: **Recurring Donations** manage ongoing donation commitments (monthly, quarterly, annual) that automatically create child Opportunities and Payments on a schedule. The Recurring Donation defines the amount, frequency, and start date. NPSP automation creates child Opportunities and Payments automatically based on the schedule. Each installment creates a new Opportunity and Payment, all linked to the parent Recurring Donation. Recurring Donations track active status, next payment date, and lifetime value.

### Q: What are Allocations and GAUs in NPSP?

**A**: **Allocations** track how gift amounts are distributed across General Accounting Units (GAUs), funds, or designations. Allocations link Opportunities to GAUs (funds, programs, campaigns) and support partial allocations (e.g., 50% to Program A, 50% to Program B). Allocation amounts should sum to the Opportunity Amount. GAUs represent funds, programs, or designations and enable reporting by fund, program, or designation. Use Allocations when gifts need to be split across multiple funds or programs.

### Q: What are Soft Credits and when should I use them?

**A**: **Soft Credits** attribute gift influence to Contacts who aren't the primary donor but influenced the gift (board members, volunteers, event hosts). Soft Credits link Opportunities to influencer Contacts and enable reporting on influencer networks and engagement. Soft Credits don't affect Opportunity Amount or Payment totals. Use Soft Credits to track board member influence, volunteer fundraising, and event host contributions. Enable soft credit reporting for donor engagement analysis.

### Q: How do I model a multi-payment pledge?

**A**: Model a multi-payment pledge by: (1) **Create Opportunity** with Amount = total pledge amount, Stage = "Pledged", Close Date = final payment date, (2) **Create multiple Payment records** with future Payment Dates and Status = "Pending", (3) **Payment Amounts sum to Opportunity Amount**, (4) **As payments are received**, update Payment Status = "Paid" and Payment Date = actual payment date, (5) **When all Payments are "Paid"**, update Opportunity Stage = "Posted". Use automation to send payment reminders before scheduled Payment Dates.

### Q: How do I handle anonymous gifts in NPSP?

**A**: Handle anonymous gifts by: (1) **Use generic Account/Contact records** for anonymous gifts (e.g., "Anonymous Donor"), (2) **Mark Opportunity** with custom field indicating anonymous status, (3) **Configure sharing rules** to restrict access to anonymous gift details, (4) **Ensure acknowledgment and receipt processes** respect anonymity, (5) **Support reporting** that aggregates anonymous gifts without exposing donor identity. Anonymous gifts require special handling to protect donor privacy while maintaining accurate reporting.

### Q: What's the difference between a hard credit and a soft credit?

**A**: A **hard credit** is attributed to the primary donor (Account/Contact on the Opportunity) and affects Opportunity Amount and Payment totals. A **soft credit** is attributed to an influencer Contact who influenced the gift but isn't the primary donor. Soft Credits don't affect Opportunity Amount or Payment totals but enable reporting on influencer networks and engagement. Use hard credits for primary donors, soft credits for board members, volunteers, and event hosts who influenced gifts.

### Q: How do I track grant allocations across multiple funds or programs?

**A**: Track grant allocations by: (1) **Create Opportunity** (Grant) with Amount = total grant amount, Record Type = "Grant", (2) **Create multiple Allocation records** linking to different GAUs (funds, programs), (3) **Allocation Amounts sum to Opportunity Amount**, (4) **Use GAUs** to represent funds, programs, or designations, (5) **Support reporting** by fund, program, or designation. Allocations enable organizations to track how grant amounts are distributed across multiple funds or programs for accurate financial reporting.

### Q: What are best practices for NPSP Opportunity data modeling?

**A**: Best practices include: (1) **Use Record Types** to differentiate between Donation, Grant, Major Gift, and other gift types, (2) **Create Payments when gifts are received**, not just when Opportunities are created, (3) **Use Recurring Donations** for monthly, quarterly, or annual giving programs, (4) **Use Allocations** when gifts need to be split across multiple funds or programs, (5) **Use Soft Credits** to track influencer relationships and engagement, (6) **Ensure Payment Amounts sum to Opportunity Amount** for accurate financial reporting, (7) **Configure acknowledgment and receipt workflows** based on gift type and donor preferences.

