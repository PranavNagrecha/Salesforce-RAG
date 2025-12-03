---
layout: default
title: Overview
description: Documentation for Overview
permalink: /rag/best-practices/reports-dashboards.html
---

# Overview

Salesforce Reports and Dashboards provide powerful analytics and visualization capabilities for understanding business performance, tracking key metrics, and making data-driven decisions. Reports retrieve and organize data from Salesforce objects, while Dashboards visualize report data through charts and metrics.

Effective reporting requires understanding report types, report formats, filtering, grouping, and summarization. Dashboards combine multiple report components into visual overviews that provide at-a-glance insights. Both reports and dashboards can be scheduled, shared, and customized for different user needs.

Understanding reports and dashboards enables administrators to provide business users with the insights they need while managing report performance, sharing, and maintenance. The decision between standard reports, CRM Analytics, and Tableau depends on complexity, data volume, and analytical needs.

# Core Concepts

## Report Types

**What it is**: Report types define which objects and relationships are available in a report, determining what data can be included.

**Standard report types**:
- **Tabular**: Simple list of records, no grouping or summarization
- **Summary**: Records grouped by fields with subtotals and grand totals
- **Matrix**: Records grouped by rows and columns with intersection summaries
- **Joined**: Reports combining data from multiple objects through relationships

**Custom report types**:
- Created for custom objects or specific object relationships
- Define which objects and relationships are available
- Enable reporting on custom data models

**Best practice**: Use standard report types when possible. Create custom report types for custom objects or specific relationship reporting needs. Understand report type limitations and capabilities.

## Report Formats

**Tabular reports**:
- Simple list format
- No grouping or summarization
- Suitable for data exports and simple lists
- Fastest report format

**Summary reports**:
- Records grouped by fields
- Subtotals and grand totals
- Suitable for grouped analysis
- Most common report format

**Matrix reports**:
- Records grouped by rows and columns
- Intersection summaries
- Suitable for cross-tab analysis
- More complex but powerful

**Joined reports**:
- Multiple report blocks from different objects
- Side-by-side comparison
- Suitable for comparing different object data
- Limited relationship capabilities

**Best practice**: Choose report format based on analysis needs. Use summary reports for most business reporting. Use matrix reports for cross-tab analysis. Use tabular reports for simple lists.

## Report Components

**Filters**:
- Filter records included in report
- Support multiple filter conditions
- Support date ranges and relative dates
- Support field value filters

**Grouping**:
- Group records by field values
- Multiple grouping levels
- Subtotals and grand totals
- Suitable for hierarchical analysis

**Summarization**:
- Summarize numeric fields (SUM, AVG, MIN, MAX, COUNT)
- Calculate percentages
- Show totals and subtotals
- Suitable for metric calculation

**Formulas**:
- Calculate custom values in reports
- Reference other report fields
- Support conditional logic
- Suitable for custom metrics

**Best practice**: Use filters to focus reports on relevant data. Use grouping for hierarchical analysis. Use summarization for metric calculation. Use formulas for custom calculations.

## Dashboards

**What it is**: Visual overviews combining multiple report components (charts, metrics, tables) into single views.

**Key characteristics**:
- Combine multiple report components
- Visual charts and graphs
- Key metrics and KPIs
- Real-time or scheduled data
- Shareable and customizable

**Dashboard components**:
- **Charts**: Visual representations of report data
- **Metrics**: Key performance indicators
- **Tables**: Tabular data displays
- **Gauges**: Progress indicators
- **Visualforce**: Custom Visualforce components

**Best practice**: Design dashboards for specific audiences and use cases. Focus on key metrics and insights. Keep dashboards simple and actionable. Test dashboards with end users.

# Deep-Dive Patterns & Best Practices

## Report Design Patterns

**Pattern 1 - Operational Reports**:
Reports for day-to-day operations, tracking current status and activities.

**Components**:
- Current records and status
- Recent activities
- Assigned tasks
- Open items

**Pattern 2 - Analytical Reports**:
Reports for analysis and insights, understanding trends and patterns.

**Components**:
- Historical data and trends
- Grouped and summarized data
- Comparative analysis
- Performance metrics

**Pattern 3 - Management Reports**:
Reports for management and executives, high-level metrics and summaries.

**Components**:
- Key performance indicators
- Summarized data
- Trends and comparisons
- Executive summaries

**Best practice**: Design reports for specific audiences and use cases. Operational reports for daily work, analytical reports for insights, management reports for high-level metrics.

## Dashboard Design Patterns

**Pattern 1 - Executive Dashboard**:
High-level metrics and KPIs for executives and management.

**Components**:
- Key performance indicators
- Trend charts
- Comparative metrics
- Summary tables

**Pattern 2 - Operational Dashboard**:
Day-to-day metrics and activities for operational teams.

**Components**:
- Current status metrics
- Activity charts
- Task lists
- Performance indicators

**Pattern 3 - Functional Dashboard**:
Function-specific metrics and insights for specific teams.

**Components**:
- Team-specific metrics
- Function-specific charts
- Performance indicators
- Action items

**Best practice**: Design dashboards for specific audiences. Focus on key metrics and actionable insights. Keep dashboards simple and focused. Test with end users.

## Report Performance Optimization

**Filter optimization**:
- Use indexed fields in filters
- Use selective filters (reduce record count)
- Avoid complex filter conditions
- Use date filters to limit data range

**Field selection**:
- Include only needed fields
- Avoid unnecessary formula fields
- Minimize cross-object fields
- Optimize field selection

**Grouping and summarization**:
- Limit grouping levels
- Use efficient grouping fields
- Optimize summarization calculations
- Consider report format impact

**Best practice**: Optimize reports for performance. Use selective filters. Include only needed fields. Test report performance with realistic data volumes.

## Report Sharing and Security

**Sharing models**:
- **Private**: Only report creator can access
- **Public**: All users can access
- **Shared with specific users/roles**: Controlled sharing

**Security considerations**:
- Reports respect object and field permissions
- Users see only data they have access to
- Sharing rules affect report data
- Role hierarchy affects data visibility

**Best practice**: Share reports appropriately. Use public reports for common needs. Use controlled sharing for sensitive reports. Test report access with different user profiles.

# Implementation Guide

## Report Creation Process

1. **Identify reporting need**: Determine what data and insights are needed
2. **Select report type**: Choose appropriate report type (standard or custom)
3. **Select report format**: Choose format (tabular, summary, matrix, joined)
4. **Configure filters**: Set filters to focus on relevant data
5. **Configure grouping**: Group records if needed for analysis
6. **Configure summarization**: Summarize numeric fields if needed
7. **Add formulas**: Add custom formulas if needed
8. **Test report**: Test with realistic data and user profiles
9. **Share report**: Share with appropriate users or make public
10. **Schedule if needed**: Schedule report for automatic generation

## Dashboard Creation Process

1. **Identify dashboard need**: Determine what metrics and insights are needed
2. **Select reports**: Choose reports to include in dashboard
3. **Design dashboard layout**: Design component layout and organization
4. **Add components**: Add charts, metrics, and tables
5. **Configure components**: Configure each component appropriately
6. **Set refresh schedule**: Configure dashboard refresh (real-time or scheduled)
7. **Test dashboard**: Test with different user profiles
8. **Share dashboard**: Share with appropriate users or make public

## Prerequisites

- Report Builder or Dashboard Builder access
- Understanding of data model and relationships
- Understanding of business reporting needs
- Understanding of report types and formats
- Understanding of sharing and security

## Key Configuration Decisions

**Report decisions**:
- Which report type provides needed data?
- Which format supports analysis needs?
- What filters focus on relevant data?
- What grouping and summarization are needed?

**Dashboard decisions**:
- Which reports provide needed insights?
- Which components visualize data effectively?
- What layout organizes components logically?
- What refresh schedule provides timely data?

## Validation & Testing

**Report testing**:
- Test with realistic data volumes
- Test with different user profiles
- Verify data accuracy
- Test report performance
- Verify filters and grouping work correctly

**Dashboard testing**:
- Test with different user profiles
- Verify component data accuracy
- Test dashboard refresh
- Verify sharing and access
- Test on different devices

**Tools to use**:
- Report Builder for report creation
- Dashboard Builder for dashboard creation
- Report and Dashboard folders for organization
- Scheduled reports for automation
- Report and Dashboard sharing for access control

# Common Pitfalls & Anti-Patterns

## Over-Complex Reports

**Bad pattern**: Creating reports with too many fields, complex grouping, or excessive filters.

**Why it's bad**: Reduces performance, confuses users, and is difficult to maintain. Users may not find needed information.

**Better approach**: Keep reports focused and simple. Include only needed fields and grouping. Test report performance. Iterate based on user feedback.

## Not Optimizing Report Performance

**Bad pattern**: Creating reports without considering performance, leading to slow execution or timeouts.

**Why it's bad**: Poor user experience, may cause timeouts, and reduces adoption.

**Better approach**: Optimize reports for performance. Use selective filters. Include only needed fields. Test with realistic data volumes. Consider report format impact.

## Not Sharing Reports Appropriately

**Bad pattern**: Keeping reports private when they should be shared, or sharing sensitive reports inappropriately.

**Why it's bad**: Reduces report value, prevents collaboration, or creates security risks.

**Better approach**: Share reports appropriately. Use public reports for common needs. Use controlled sharing for sensitive reports. Review report sharing regularly.

## Dashboard Information Overload

**Bad pattern**: Creating dashboards with too many components, overwhelming users with information.

**Why it's bad**: Reduces dashboard effectiveness, confuses users, and reduces adoption.

**Better approach**: Keep dashboards focused and simple. Focus on key metrics and insights. Design for specific audiences. Test with end users.

## Not Scheduling Reports

**Bad pattern**: Not scheduling reports that users need regularly, requiring manual generation.

**Why it's bad**: Reduces efficiency, may cause users to miss reports, and increases manual work.

**Better approach**: Schedule reports that users need regularly. Configure appropriate delivery (email, dashboard). Review scheduled reports periodically.

# Real-World Scenarios

## Scenario 1 - Sales Pipeline Report

**Problem**: Sales team needs report showing open opportunities by stage, amount, and owner for pipeline management.

**Context**: Sales Cloud implementation, sales team needs pipeline visibility, managers need team performance metrics.

**Solution**: 
- Create Summary report on Opportunity object
- Group by Stage and Owner
- Summarize Amount field (SUM)
- Filter for open opportunities (IsClosed = false)
- Add formulas for conversion rates if needed
- Share with sales team and managers

**Key decisions**: Use Summary report for grouping. Group by Stage and Owner for pipeline analysis. Summarize Amount for pipeline value. Filter for open opportunities only.

## Scenario 2 - Case Management Dashboard

**Problem**: Service team needs dashboard showing case volume, resolution times, and agent performance.

**Context**: Service Cloud implementation, service managers need operational metrics, agents need their performance data.

**Solution**:
- Create dashboard with multiple report components
- Add chart showing cases by status
- Add metric showing average resolution time
- Add table showing agent performance
- Add chart showing case volume trends
- Configure real-time refresh
- Share with service team

**Key decisions**: Use dashboard for visual overview. Include key metrics and charts. Configure real-time refresh for current data. Share with appropriate users.

## Scenario 3 - Custom Object Reporting

**Problem**: Organization needs reports on custom Application object with related Program and Contact data.

**Context**: Custom Application object with relationships to Program and Contact, need reporting on application status and program enrollment.

**Solution**:
- Create custom report type for Application object
- Include Application, Program, and Contact relationships
- Create Summary report grouping by Program and Status
- Summarize application counts
- Filter for relevant application types
- Share with admissions team

**Key decisions**: Create custom report type for custom object relationships. Use Summary report for grouping. Include related object data for context.

# Checklist / Mental Model

## Report and Dashboard Creation Checklist

When creating reports and dashboards:

1. **Identify need**: What data and insights are needed?
2. **Select type/format**: Which report type and format support needs?
3. **Configure filters**: What filters focus on relevant data?
4. **Configure grouping/summarization**: What grouping and summarization are needed?
5. **Test thoroughly**: Test with realistic data and user profiles
6. **Optimize performance**: Optimize for performance if needed
7. **Share appropriately**: Share with appropriate users
8. **Schedule if needed**: Schedule for automatic generation

## Reporting Mental Model

**Design for audience**: Design reports and dashboards for specific audiences and use cases. Operational reports for daily work, analytical reports for insights, management reports for high-level metrics.

**Keep it simple**: Keep reports and dashboards focused and simple. Include only needed fields and components. Test with end users and iterate.

**Optimize performance**: Optimize reports for performance. Use selective filters, include only needed fields, and test with realistic data volumes.

**Share appropriately**: Share reports and dashboards appropriately. Use public reports for common needs, controlled sharing for sensitive reports.

**Schedule regularly**: Schedule reports that users need regularly. Configure appropriate delivery and review schedules periodically.

# Key Terms & Definitions

- **Report Type**: Defines which objects and relationships are available in a report
- **Tabular Report**: Simple list format with no grouping or summarization
- **Summary Report**: Records grouped by fields with subtotals and grand totals
- **Matrix Report**: Records grouped by rows and columns with intersection summaries
- **Joined Report**: Multiple report blocks from different objects for side-by-side comparison
- **Dashboard**: Visual overview combining multiple report components (charts, metrics, tables)
- **Report Filter**: Condition that determines which records are included in report
- **Report Grouping**: Organizing records by field values with subtotals
- **Report Summarization**: Calculating totals, averages, or other summaries of numeric fields
- **Scheduled Report**: Report automatically generated and delivered on schedule

# RAG-Friendly Q&A Seeds

**Q:** What's the difference between a Summary report and a Matrix report?

**A:** A Summary report groups records by fields in rows with subtotals and grand totals, suitable for hierarchical analysis. A Matrix report groups records by both rows and columns with intersection summaries, suitable for cross-tab analysis. Use Summary reports for most business reporting. Use Matrix reports for cross-tab analysis when you need row and column grouping.

**Q:** How do I create a custom report type?

**A:** Create custom report type by: (1) Navigate to Report Types in Setup, (2) Click "New Custom Report Type", (3) Select primary object, (4) Add related objects if needed, (5) Configure object relationships, (6) Set report type properties, (7) Save and deploy. Custom report types enable reporting on custom objects or specific object relationships.

**Q:** Can I schedule reports to run automatically?

**A:** Yes, you can schedule reports to run automatically and be delivered via email or added to dashboards. Configure schedule (daily, weekly, monthly), delivery method (email, dashboard), and recipients. Scheduled reports are useful for regular reporting needs and reduce manual work.

**Q:** How do dashboards get their data?

**A:** Dashboards get data from reports. Dashboard components (charts, metrics, tables) are based on reports. When dashboard refreshes, it runs underlying reports and displays results. Dashboards can refresh in real-time or on schedule. Users see data based on their permissions and sharing rules.

**Q:** What's the difference between standard reports and CRM Analytics?

**A:** Standard reports provide operational reporting with filtering, grouping, and summarization, suitable for most business needs. CRM Analytics (formerly Tableau CRM) provides advanced analytics with AI-powered insights, data pipelines, and interactive dashboards, suitable for complex analysis and predictive insights. Use standard reports for operational needs, CRM Analytics for advanced analytics.

**Q:** How do I optimize report performance?

**A:** Optimize report performance by: (1) Using indexed fields in filters, (2) Using selective filters to reduce record count, (3) Including only needed fields, (4) Limiting grouping levels, (5) Using date filters to limit data range, (6) Testing with realistic data volumes. Performance optimization is critical for large data volumes.

**Q:** Can I use formulas in reports?

**A:** Yes, you can create formula fields in reports that calculate custom values based on other report fields. Report formulas support functions, operators, and conditional logic. Use formulas for custom metrics, calculations, or conditional display. Formulas are calculated when report runs.