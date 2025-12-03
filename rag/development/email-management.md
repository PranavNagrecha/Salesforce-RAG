---
layout: default
title: Overview
description: Documentation for Overview
permalink: /rag/development/email-management.html
---

# Overview

Salesforce provides comprehensive email capabilities for sending individual emails, mass emails, and automated emails through workflows and Flows. Understanding email management enables administrators to configure email functionality, templates, deliverability, and limits to support business communication needs.

Email in Salesforce includes individual email (from records), mass email (to multiple recipients), automated email (through automation), and email templates. Effective email management requires understanding email limits, deliverability configuration, template design, and automation integration.

Configuring email effectively requires understanding business communication needs, email volume, deliverability requirements, and platform limits. Administrators must balance email functionality with deliverability, compliance, and user experience.

# Core Concepts

## Email Types

**Individual Email**: Email sent from a record (Account, Contact, Case, etc.) to a single recipient.

**Key characteristics**:
- Sent from record detail page
- Links email to record (EmailMessage object)
- Supports email templates
- Tracks email in activity history

**Mass Email**: Email sent to multiple recipients from list views or reports.

**Key characteristics**:
- Sent to multiple recipients at once
- Supports email templates
- Subject to mass email limits
- Tracks emails in activity history

**Automated Email**: Email sent automatically through workflows, Flows, or Apex.

**Key characteristics**:
- Triggered by automation
- Supports email templates
- Can be sent in bulk
- Tracks emails in activity history

**Best practice**: Use individual email for personal communication. Use mass email for marketing or announcements. Use automated email for notifications and alerts.

## Email Templates

**What it is**: Pre-formatted email content that can be reused for consistent messaging.

**Template types**:
- **Text Templates**: Plain text email templates
- **HTML Templates**: Rich HTML email templates with formatting
- **Visualforce Templates**: Advanced templates with Visualforce markup
- **Letterhead Templates**: Templates with letterhead branding

**Template features**:
- Merge fields for personalization
- Rich text formatting (HTML templates)
- Letterhead branding
- Conditional content (Visualforce templates)

**Best practice**: Create email templates for common communications. Use merge fields for personalization. Test templates with sample data. Maintain templates regularly.

## Email Deliverability

**What it is**: Configuration and practices that ensure emails are delivered successfully and not marked as spam.

**Key factors**:
- SPF (Sender Policy Framework) records
- DKIM (DomainKeys Identified Mail) records
- Email authentication configuration
- Sender reputation
- Email content and formatting

**Deliverability configuration**:
- Configure SPF records for sending domain
- Configure DKIM records for email authentication
- Set up email authentication in Salesforce
- Monitor email deliverability and bounce rates

**Best practice**: Configure email authentication (SPF, DKIM) for better deliverability. Monitor bounce rates and spam complaints. Follow email best practices (clear subject lines, opt-out options, etc.).

## Email Limits

**Daily email limits**:
- Single email: 5,000 recipients per day (Enterprise/Performance/Unlimited)
- Mass email: 500 recipients per mass email (Enterprise/Performance/Unlimited)
- Automated email: Subject to daily limits based on edition

**Limit considerations**:
- Limits vary by Salesforce edition
- Limits apply per user, not per org
- Limits reset daily
- Exceeding limits prevents email sending

**Best practice**: Understand email limits for your edition. Plan email campaigns within limits. Use Marketing Cloud for high-volume email needs. Monitor email usage.

# Deep-Dive Patterns & Best Practices

## Email Template Design Patterns

**Pattern 1 - Personalization**:
Use merge fields to personalize email content.

**Example**: "Dear {!Contact.FirstName}, Thank you for your inquiry about {!Case.Subject}."

**Pattern 2 - Branding**:
Use letterhead templates for consistent branding.

**Example**: Include company logo, colors, and branding in email templates.

**Pattern 3 - Conditional Content**:
Use Visualforce templates for conditional content.

**Example**: Show different content based on record type, status, or other field values.

**Best practice**: Design templates for readability and branding. Use merge fields for personalization. Test templates with sample data. Maintain templates regularly.

## Email Automation Patterns

**Pattern 1 - Case Notifications**:
Send automated emails when cases are created or updated.

**Configuration**:
- Use Flows to send emails (⚠️ **Note**: Process Builder is deprecated - use Record-Triggered Flows instead)
- Use email templates for consistent messaging
- Include case details and next steps
- Send to case contacts or account contacts

**Pattern 2 - Opportunity Alerts**:
Send automated emails for opportunity milestones.

**Configuration**:
- Use Flows to send emails at opportunity stages
- Notify sales team of important opportunities
- Include opportunity details and action items

**Pattern 3 - Task Reminders**:
Send automated email reminders for overdue tasks.

**Configuration**:
- Use Scheduled Flows to check overdue tasks
- Send reminder emails to task assignees
- Include task details and links

**Best practice**: Automate email notifications for important events. Use email templates for consistency. Test automation thoroughly. Monitor email volume and limits.

## Mass Email Patterns

**Pattern 1 - Marketing Campaigns**:
Send mass emails for marketing campaigns.

**Configuration**:
- Use mass email from Campaigns or list views
- Use email templates for consistent messaging
- Include opt-out options
- Track email opens and clicks (if enabled)

**Pattern 2 - Announcements**:
Send mass emails for organizational announcements.

**Configuration**:
- Use mass email from list views or reports
- Use email templates for formatting
- Send to appropriate user groups
- Monitor delivery and responses

**Best practice**: Use mass email for marketing or announcements. Include opt-out options. Monitor email limits. Consider Marketing Cloud for high-volume needs.

# Implementation Guide

## Email Configuration Process

1. **Configure email settings**: Set up email deliverability, authentication, and preferences
2. **Create email templates**: Create templates for common communications
3. **Configure email automation**: Set up Flows or workflows for automated emails
4. **Test email functionality**: Test individual, mass, and automated emails
5. **Monitor email deliverability**: Monitor bounce rates and spam complaints
6. **Train users**: Train users on email functionality and best practices

## Prerequisites

- System Administrator or appropriate permissions
- Understanding of email requirements and volume
- Understanding of email deliverability and authentication
- Email domain access for SPF/DKIM configuration
- Understanding of email limits

## Key Configuration Decisions

**Email deliverability decisions**:
- SPF and DKIM configuration?
- Email authentication setup?
- Sender reputation management?
- Bounce and spam monitoring?

**Email template decisions**:
- Which templates are needed?
- What merge fields are required?
- What branding and formatting?
- What template types (text, HTML, Visualforce)?

**Email automation decisions**:
- Which events trigger emails?
- Which templates are used?
- Who receives automated emails?
- What email volume is expected?

## Validation & Testing

**Email testing**:
- Test individual email sending
- Test mass email functionality
- Test automated email triggers
- Test email templates with sample data
- Test email deliverability
- Monitor email limits and usage

**Tools to use**:
- Email Administration in Setup
- Email Templates management
- Email Logs for delivery tracking
- Deliverability monitoring
- Email usage reports

# Common Pitfalls & Anti-Patterns

## Not Configuring Email Authentication

**Bad pattern**: Not configuring SPF and DKIM records, leading to poor deliverability.

**Why it's bad**: Emails may be marked as spam, reducing deliverability and trust.

**Better approach**: Configure SPF and DKIM records for email authentication. Set up email authentication in Salesforce. Monitor deliverability and bounce rates.

## Exceeding Email Limits

**Bad pattern**: Sending emails without monitoring limits, causing email failures.

**Why it's bad**: Exceeding limits prevents email sending, disrupting communication.

**Better approach**: Understand email limits for your edition. Monitor email usage. Plan email campaigns within limits. Use Marketing Cloud for high-volume needs.

## Poor Email Template Design

**Bad pattern**: Creating email templates without proper formatting, personalization, or branding.

**Why it's bad**: Reduces email effectiveness, poor user experience, and inconsistent messaging.

**Better approach**: Design templates with proper formatting and branding. Use merge fields for personalization. Test templates with sample data. Maintain templates regularly.

## Not Testing Automated Emails

**Bad pattern**: Deploying email automation without thorough testing.

**Why it's bad**: May send incorrect emails, cause user confusion, or trigger unintended emails.

**Better approach**: Test automated emails thoroughly before deployment. Test with sample data and scenarios. Monitor automated email volume and content.

## Ignoring Email Deliverability

**Bad pattern**: Not monitoring email deliverability, bounce rates, or spam complaints.

**Why it's bad**: Poor deliverability reduces email effectiveness and may damage sender reputation.

**Better approach**: Monitor email deliverability regularly. Track bounce rates and spam complaints. Configure email authentication. Follow email best practices.

# Real-World Scenarios

## Scenario 1 - Case Notification Emails

**Problem**: Service team needs to send automated emails to customers when cases are created or updated.

**Context**: High case volume, need consistent customer communication, email templates required.

**Solution**:
- Create email templates for case notifications
- Configure Flow to send emails on case creation/update
- Use merge fields for personalization
- Include case details and next steps
- Send to case contacts
- Monitor email delivery

**Key decisions**: Use email templates for consistency. Automate email sending through Flows. Include case details for context. Monitor email deliverability.

## Scenario 2 - Marketing Campaign Emails

**Problem**: Marketing team needs to send mass emails to campaign members for product announcements.

**Context**: Marketing campaigns, need mass email capability, email templates required.

**Solution**:
- Create email templates for marketing communications
- Use mass email from Campaigns
- Include opt-out options
- Track email opens and clicks
- Monitor email limits
- Consider Marketing Cloud for high volume

**Key decisions**: Use mass email for campaigns. Include opt-out options. Monitor email limits. Consider Marketing Cloud for high-volume needs.

## Scenario 3 - Email Deliverability Configuration

**Problem**: Organization needs to improve email deliverability and reduce spam marking.

**Context**: Poor email deliverability, emails marked as spam, need authentication configuration.

**Solution**:
- Configure SPF records for sending domain
- Configure DKIM records for email authentication
- Set up email authentication in Salesforce
- Monitor bounce rates and spam complaints
- Follow email best practices
- Improve sender reputation

**Key decisions**: Configure email authentication for better deliverability. Monitor deliverability metrics. Follow email best practices. Improve sender reputation over time.

# Checklist / Mental Model

## Email Management Checklist

When configuring email in Salesforce:

1. **Email settings**: Configure email deliverability, authentication, and preferences
2. **Email templates**: Create templates for common communications
3. **Email automation**: Set up automated emails through Flows or workflows
4. **Email testing**: Test individual, mass, and automated emails
5. **Deliverability monitoring**: Monitor bounce rates and spam complaints
6. **Limit monitoring**: Monitor email usage and limits
7. **User training**: Train users on email functionality and best practices

## Email Management Mental Model

**Configure for deliverability**: Set up email authentication (SPF, DKIM) for better deliverability. Monitor deliverability metrics and improve sender reputation.

**Use templates for consistency**: Create email templates for common communications. Use merge fields for personalization. Maintain templates regularly.

**Automate where appropriate**: Automate email notifications for important events. Use email templates for consistency. Test automation thoroughly.

**Monitor limits and usage**: Understand email limits for your edition. Monitor email usage. Plan campaigns within limits. Use Marketing Cloud for high-volume needs.

**Test thoroughly**: Test all email functionality before deployment. Test templates with sample data. Monitor email delivery and effectiveness.

# Key Terms & Definitions

- **Individual Email**: Email sent from a record to a single recipient
- **Mass Email**: Email sent to multiple recipients from list views or reports
- **Automated Email**: Email sent automatically through workflows, Flows, or Apex
- **Email Template**: Pre-formatted email content that can be reused
- **Merge Field**: Field reference in email template that inserts actual field values
- **Email Deliverability**: Configuration and practices ensuring emails are delivered successfully
- **SPF (Sender Policy Framework)**: Email authentication method that verifies sender identity
- **DKIM (DomainKeys Identified Mail)**: Email authentication method that verifies email integrity
- **Email Limits**: Platform limits on number of emails that can be sent per day
- **Email Log**: Record of email sending, delivery, and bounce information

# RAG-Friendly Q&A Seeds

**Q:** What's the difference between individual email and mass email?

**A:** Individual email is sent from a record (Account, Contact, Case) to a single recipient, linking the email to the record. Mass email is sent to multiple recipients from list views or reports, useful for marketing or announcements. Individual email is for personal communication; mass email is for bulk communication. Both support email templates and are subject to email limits.

**Q:** How do I create email templates?

**A:** Create email templates by: (1) Navigate to Email Templates in Setup, (2) Click "New Template", (3) Select template type (Text, HTML, Visualforce, Letterhead), (4) Enter template content with merge fields, (5) Configure template properties, (6) Save template. Use merge fields for personalization. Test templates with sample data.

**Q:** What are email limits in Salesforce?

**A:** Email limits vary by edition: (1) Single email: 5,000 recipients per day (Enterprise/Performance/Unlimited), (2) Mass email: 500 recipients per mass email (Enterprise/Performance/Unlimited), (3) Automated email: Subject to daily limits based on edition. Limits apply per user, reset daily, and prevent sending when exceeded. Use Marketing Cloud for high-volume email needs.

**Q:** How do I configure email deliverability?

**A:** Configure email deliverability by: (1) Set up SPF records for sending domain, (2) Configure DKIM records for email authentication, (3) Set up email authentication in Salesforce, (4) Monitor bounce rates and spam complaints, (5) Follow email best practices (clear subject lines, opt-out options, etc.), (6) Improve sender reputation over time. Email authentication improves deliverability significantly.

**Q:** Can I send automated emails through Flows?

**A:** Yes, you can send automated emails through Flows using the "Send Email" action. Configure email action with template, recipients, and merge fields. Flows can send emails on record creation, updates, or scheduled events. Use email templates for consistency. Test automated emails thoroughly before deployment.

**Q:** How do merge fields work in email templates?

**A:** Merge fields reference Salesforce field values that are inserted into email content when email is sent. Use syntax like `{!Contact.FirstName}` or `{!Case.Subject}` to insert field values. Merge fields enable personalization and dynamic content. Test merge fields with sample data to verify they work correctly.

**Q:** What should I do if emails are being marked as spam?

**A:** If emails are marked as spam: (1) Configure SPF and DKIM records for email authentication, (2) Monitor bounce rates and spam complaints, (3) Follow email best practices (clear subject lines, opt-out options, legitimate content), (4) Improve sender reputation over time, (5) Consider using Marketing Cloud for high-volume email needs. Email authentication is critical for deliverability.

## Related Patterns

**See Also**:
- <a href="{{ '/rag/development/flow-patterns.html' | relative_url }}">Flow Patterns</a> - Automated email sending through Flows
- <a href="{{ '/rag/development/admin-basics.html' | relative_url }}">Admin Basics</a> - Email configuration and settings

**Related Domains**:
- <a href="{{ '/rag/development/integrations/etl-vs-api-vs-events.html' | relative_url }}">Integration Patterns</a> - Email in integration scenarios

