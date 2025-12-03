---
layout: default
title: Integration User License Guide
description: The Salesforce Integration User License is a free API-only license designed for system-to-system integrations
permalink: /rag/integrations/integration-user-license-guide.html
---

## License Details

### License Availability

**Included Licenses**:
- Enterprise Edition: 5 free Integration User Licenses
- Performance Edition: 5 free Integration User Licenses
- Unlimited Edition: 5 free Integration User Licenses
- Professional Edition: Not included (requires upgrade)

**Additional Licenses**:
- Additional licenses available for purchase at approximately $10 per user per month
- Purchase through Salesforce Account Executive or Partner

### Checking License Availability

**Company Information Page**:
- Navigate to Setup → Company Information
- Review "Integration User Licenses" section
- View available, used, and total licenses
- Monitor license utilization for planning

**License Allocation Strategy**:
- Plan for one Integration User License per external system
- Reserve licenses for future integrations
- Monitor usage trends to anticipate additional license needs
- Consider license costs when planning integration architecture

### Edition Requirements

**Supported Editions**:
- Enterprise Edition and above
- Performance Edition
- Unlimited Edition

**Not Supported**:
- Professional Edition
- Developer Edition (limited support)
- Trial orgs (varies by trial type)

## Setup and Configuration

### Step 1: Create Integration User

**User Creation Process**:
- Navigate to Setup → Users → Users
- Click "New User" button
- Complete required user fields:
  - First Name: Descriptive name (e.g., "MuleSoft", "Boomi", "SIS Sync")
  - Last Name: "Integration" or system identifier
  - Alias: Short identifier for the integration
  - Email: Use a monitored email address for notifications
  - Username: Unique username following naming convention
  - User License: Select "Salesforce Integration"

**Naming Conventions**:
- Use descriptive names indicating the integration purpose
- Include system name or identifier in username
- Follow organizational naming standards
- Document naming conventions for consistency

### Step 2: Assign Profile

**Minimum Access Profile**:
- Assign "Minimum Access – API Only Integrations" profile
- This profile cannot be modified to allow UI access
- Provides base API access without object permissions
- All object and field access granted through Permission Sets

**Profile Limitations**:
- Cannot access Salesforce UI (Login attempts will fail)
- Cannot be modified to enable UI access
- Designed exclusively for API interactions
- Base profile provides minimal permissions

### Step 3: Assign Permission Set License

**Permission Set License Assignment**:
- Navigate to user record → Permission Set License Assignments
- Assign "Salesforce API Integration" Permission Set License (PSL)
- Required for Permission Sets that extend beyond base profile
- Enables assignment of custom Permission Sets

**When PSL is Required**:
- Using Permission Sets beyond default profile permissions
- Custom Permission Sets requiring PSL
- Extended object or field access requirements

### Step 4: Configure Permission Sets

**Permission Set Design**:
- Create dedicated Permission Set for each integration
- Name Permission Set to reflect integration purpose
- Grant only necessary object and field permissions
- Follow principle of least privilege

**Object Permissions**:
- Grant Read, Create, Edit, Delete as needed
- Consider object-level security requirements
- Review sharing rules and role hierarchy impact
- Document permission rationale

**Field Permissions**:
- Grant field-level access for required fields
- Respect field-level security (FLS) settings
- Consider sensitive data fields
- Document field access requirements

**System Permissions**:
- Grant API access (included in profile)
- Consider additional system permissions if needed
- Review Apex class access if using custom Apex
- Document system permission requirements

**Permission Set Assignment**:
- Assign Permission Set to Integration User
- Verify permissions are correctly applied
- Test API access with minimal permissions first
- Document Permission Set assignments

## Authentication Patterns

### OAuth 2.0 Client Credentials Flow

**Server-to-Server Authentication**:
- OAuth 2.0 Client Credentials Flow is the recommended authentication method
- Designed for system-to-system authentication without user interaction
- Provides secure token-based authentication
- Tokens can be cached and reused until expiration

**When to Use Client Credentials Flow**:
- System-to-system integrations
- Scheduled jobs and batch processes
- Server-side applications
- Integration platforms (MuleSoft, Dell Boomi)

**When NOT to Use Client Credentials Flow**:
- User-initiated actions requiring user context
- Delegated authentication scenarios
- Mobile applications requiring user authentication

### OAuth Client Credentials Configuration

**Connected App Setup**:
- Create Connected App in Salesforce Setup
- Enable OAuth Settings
- Select OAuth Scopes: "Access and manage your data (api)"
- Configure callback URL (not used for Client Credentials, but required)
- Enable "Require Secret for Web Server Flow"

**Client Credentials Flow Process**:
- External system requests access token using client ID and secret
- Salesforce validates credentials and returns access token
- External system uses access token for API calls
- Token expires after configured time (default 2 hours)

**Token Management**:
- Cache tokens to reduce authentication calls
- Implement token refresh before expiration
- Handle token expiration gracefully
- Monitor token usage for security

### Named Credentials Configuration

**Named Credentials for Integration Users**:
- Configure Named Credentials pointing to Salesforce APIs
- Use OAuth 2.0 Client Credentials authentication
- Store Connected App credentials securely
- Enable automatic token refresh

**Benefits of Named Credentials**:
- Centralized credential management
- Automatic token refresh
- No hardcoded credentials in code
- Environment-specific configurations

**Named Credentials Setup**:
- Create Named Credential in Setup
- Select Authentication Protocol: OAuth 2.0
- Select Identity Type: Named Principal
- Configure Connected App reference
- Set callback URL and scope

### Alternative Authentication Methods

**Username-Password Flow** (Not Recommended):
- Basic authentication using username and password
- Less secure than OAuth flows
- Requires storing passwords
- Not recommended for production integrations

**JWT Bearer Token Flow**:
- Uses digital signatures for authentication
- Requires certificate management
- More complex setup
- Suitable for enterprise integrations with certificate infrastructure

## Permission Management

### Principle of Least Privilege

**Permission Strategy**:
- Grant only permissions necessary for integration functionality
- Start with minimal permissions and expand as needed
- Document permission requirements for each integration
- Regularly audit permissions for unused access

**Permission Review Process**:
- Review integration functionality requirements
- Identify minimum necessary object and field access
- Grant permissions through Permission Sets
- Document permission rationale
- Regularly audit and remove unused permissions

### Permission Set Design Patterns

**Dedicated Permission Set per Integration**:
- Create one Permission Set per integration system
- Name clearly to indicate integration purpose
- Document all permissions and rationale
- Version control Permission Set metadata

**Permission Set Structure**:
- Object Permissions: Read, Create, Edit, Delete as needed
- Field Permissions: Field-level access for required fields
- System Permissions: Additional system-level permissions if needed
- Apex Class Access: If integration uses custom Apex classes

**Permission Set Naming Convention**:
- Use descriptive names: "Integration - [System Name] - [Purpose]"
- Include integration identifier
- Follow organizational naming standards
- Document naming conventions

### Object-Level Security

**Object Access Considerations**:
- Review object-level security settings
- Consider sharing rules and role hierarchy
- Integration users may need elevated access
- Document object access requirements

**Sharing Model Impact**:
- Integration users may bypass sharing rules with elevated permissions
- Consider Private sharing model implications
- Document sharing rule exceptions
- Review audit logs for access patterns

### Field-Level Security

**Field Access Considerations**:
- Respect field-level security (FLS) settings
- Grant field access through Permission Sets
- Consider sensitive data fields
- Document field access requirements

**Sensitive Data Handling**:
- Limit access to sensitive fields (SSN, financial data)
- Document sensitive field access
- Implement additional monitoring for sensitive data access
- Review compliance requirements

### Profile Limitations

**API-Only Restriction**:
- "Minimum Access – API Only Integrations" profile cannot be modified
- Cannot enable UI access through profile modifications
- All access must be granted through Permission Sets
- Profile provides base API access only

**Profile Customization**:
- Profile settings are locked for Integration User License
- Cannot modify profile to enable UI features
- Permission Sets are the only way to grant additional access
- Document profile limitations for stakeholders

## Best Practices

### Dedicated User per Integration

**One User per External System**:
- Assign one Integration User License per external system
- Enables clear audit trails per integration
- Simplifies permission management
- Improves security isolation

**Benefits**:
- Clear audit trail showing which system performed actions
- Simplified permission management per integration
- Security isolation between integrations
- Easier troubleshooting and monitoring

**Naming Convention**:
- Use descriptive usernames indicating integration purpose
- Include system name or identifier
- Follow organizational naming standards
- Document user assignments

### Security and Audit Trail

**Audit Trail Benefits**:
- All API calls logged with Integration User identity
- Clear attribution of actions to specific integrations
- Enhanced security monitoring and compliance
- Simplified troubleshooting

**Monitoring Integration Users**:
- Review API usage logs regularly
- Monitor for unusual access patterns
- Track permission changes
- Review audit logs for compliance

**Event Monitoring**:
- Enable Event Monitoring for Integration Users
- Track API calls and data access
- Monitor for security anomalies
- Generate compliance reports

### Permission Management Strategies

**Regular Permission Audits**:
- Review permissions quarterly or semi-annually
- Remove unused permissions
- Document permission changes
- Verify permissions match integration requirements

**Permission Documentation**:
- Document all Permission Set assignments
- Record permission rationale
- Maintain permission change log
- Include permissions in integration documentation

**Permission Testing**:
- Test integrations with minimal permissions first
- Verify permissions meet integration requirements
- Test permission changes in sandbox before production
- Document permission testing procedures

### Regular Audit and Monitoring

**Audit Schedule**:
- Review Integration User activities monthly
- Audit permissions quarterly
- Review license utilization quarterly
- Annual comprehensive security review

**Monitoring Activities**:
- Review API usage logs
- Monitor for failed authentication attempts
- Track permission changes
- Review compliance with security policies

**Compliance Considerations**:
- Document audit procedures
- Maintain audit logs
- Generate compliance reports
- Address security findings promptly

### Integration Naming Conventions

**User Naming**:
- Format: "[System Name] Integration" or "[Purpose] Integration"
- Examples: "MuleSoft Integration", "SIS Sync Integration"
- Include system identifier in username
- Follow organizational standards

**Permission Set Naming**:
- Format: "Integration - [System Name] - [Purpose]"
- Examples: "Integration - MuleSoft - Student Sync"
- Include integration identifier
- Document naming conventions

**Connected App Naming**:
- Format: "[System Name] Integration" or "[Purpose] Integration"
- Include system identifier
- Follow organizational standards
- Document Connected App assignments

## Security Considerations

### API-Only Access Restrictions

**UI Access Prevention**:
- Integration Users cannot access Salesforce UI
- Login attempts to UI will fail
- All access must be through APIs
- Profile cannot be modified to enable UI access

**API Access Methods**:
- REST API
- SOAP API
- Bulk API
- Streaming API
- Metadata API

**Access Limitations**:
- No access to Salesforce mobile apps
- No access to Experience Cloud sites
- No access to Lightning Experience or Classic
- API access only

### Network Security Considerations

**IP Restrictions**:
- Consider IP whitelisting for Integration Users
- Use Trusted IP Ranges in Salesforce
- Configure at Connected App level if supported
- Document IP restrictions

**VPN and Network Security**:
- Integration platforms (MuleSoft, Boomi) may handle network security
- Document network paths and security controls
- Consider VPN requirements for external systems
- Review network security architecture

**Firewall and Network Controls**:
- Document firewall rules for API access
- Review network security policies
- Consider DMZ architecture for integration servers
- Document network security controls

### Credential Rotation Practices

**Credential Rotation Schedule**:
- Rotate Connected App secrets annually or as required by policy
- Document rotation procedures
- Test rotation in sandbox before production
- Coordinate with integration teams

**Rotation Process**:
- Generate new Connected App secret
- Update external systems with new credentials
- Verify integration functionality
- Retire old credentials after verification
- Document rotation completion

**Credential Storage**:
- Store credentials securely (secrets management system)
- Never hardcode credentials in code
- Use Named Credentials when possible
- Document credential storage locations

### Event Monitoring and API Usage Tracking

**Event Monitoring Setup**:
- Enable Event Monitoring for Integration Users
- Configure event types to monitor
- Set up dashboards for API usage
- Configure alerts for anomalies

**API Usage Tracking**:
- Monitor API call volumes per Integration User
- Track API response times
- Identify API limit usage
- Generate usage reports

**Security Monitoring**:
- Monitor for failed authentication attempts
- Track unusual access patterns
- Review API calls for sensitive data access
- Generate security reports

### Compliance and Audit Requirements

**Audit Requirements**:
- Maintain audit logs for Integration User activities
- Generate compliance reports as required
- Document security controls
- Review audit logs regularly

**Compliance Considerations**:
- Document data access for compliance reviews
- Maintain records of permission changes
- Generate reports for auditors
- Address compliance findings promptly

**Documentation Requirements**:
- Document all Integration User configurations
- Maintain permission documentation
- Record security controls
- Update documentation with changes

## Operational Considerations

### Monitoring Integration User Activities

**API Usage Monitoring**:
- Review API usage logs in Setup → Monitoring → Debug Logs
- Use Event Monitoring for comprehensive tracking
- Monitor API call volumes and patterns
- Track API limit usage

**Activity Monitoring Tools**:
- Setup → Monitoring → Event Monitoring
- Setup → Monitoring → Debug Logs
- Setup → Users → Login History
- Custom dashboards and reports

**Monitoring Best Practices**:
- Set up regular monitoring schedules
- Configure alerts for anomalies
- Review logs for security issues
- Document monitoring procedures

### Troubleshooting Common Issues

**Authentication Failures**:
- Verify Connected App configuration
- Check client ID and secret
- Verify OAuth scopes
- Review token expiration
- Check IP restrictions

**Permission Issues**:
- Verify Permission Set assignments
- Check object and field permissions
- Review Permission Set License assignment
- Verify profile assignment
- Test with minimal permissions first

**API Limit Issues**:
- Monitor API call volumes
- Review API limit usage
- Implement retry logic with backoff
- Consider Bulk API for large operations
- Optimize API call patterns

**Common Troubleshooting Steps**:
- Verify user license assignment
- Check profile assignment
- Review Permission Set assignments
- Verify Connected App configuration
- Review API usage logs
- Check for IP restrictions

### License Management and Planning

**License Utilization Tracking**:
- Monitor license usage in Company Information
- Track license allocation per integration
- Plan for future integration needs
- Document license assignments

**License Planning**:
- Assess integration requirements
- Plan for one license per external system
- Reserve licenses for future integrations
- Budget for additional licenses if needed

**License Optimization**:
- Review unused Integration Users
- Consolidate integrations where appropriate
- Document license usage
- Optimize license allocation

### Migration from Regular User Licenses

**Migration Planning**:
- Identify integrations using regular user licenses
- Assess migration feasibility
- Plan migration timeline
- Coordinate with integration teams

**Migration Process**:
- Create Integration User with same permissions
- Update external systems with new credentials
- Test integration functionality
- Monitor for issues
- Retire old user license

**Migration Considerations**:
- Verify all permissions are migrated
- Test integration thoroughly
- Coordinate downtime if needed
- Document migration process
- Update documentation

## Integration Patterns

### When to Use Integration User Licenses

**Appropriate Use Cases**:
- System-to-system integrations
- Scheduled batch processes
- Integration platforms (MuleSoft, Dell Boomi)
- Custom applications accessing Salesforce APIs
- ETL operations requiring API access

**Decision Criteria**:
- Does the integration require UI access? (No → Use Integration User License)
- Is this a system-to-system integration? (Yes → Use Integration User License)
- Does the integration run on a schedule or server? (Yes → Use Integration User License)
- Is cost optimization important? (Yes → Use Integration User License)

### Integration with MuleSoft

**MuleSoft Integration Pattern**:
- Create dedicated Integration User for MuleSoft
- Configure OAuth Client Credentials in MuleSoft
- Grant permissions for objects accessed by MuleSoft flows
- Use Named Credentials in Salesforce pointing to MuleSoft

**MuleSoft Configuration**:
- Configure OAuth 2.0 Client Credentials in MuleSoft
- Store Salesforce credentials securely in MuleSoft
- Use MuleSoft's Salesforce connector
- Document MuleSoft-Salesforce integration

**Related**: <a href="{{ '/rag/integrations/integration-platform-patterns.html' | relative_url }}">Integration Platform Patterns</a> - Patterns for MuleSoft and Dell Boomi integrations

### Integration with Dell Boomi

**Boomi Integration Pattern**:
- Create dedicated Integration User for Boomi
- Configure OAuth Client Credentials in Boomi
- Grant permissions for objects synchronized by Boomi
- Use Boomi's Salesforce connector

**Boomi Configuration**:
- Configure OAuth 2.0 Client Credentials in Boomi
- Store Salesforce credentials securely in Boomi
- Use Boomi's Salesforce connector for operations
- Document Boomi-Salesforce integration

**Related**: <a href="{{ '/rag/integrations/integration-platform-patterns.html' | relative_url }}">Integration Platform Patterns</a> - Patterns for MuleSoft and Dell Boomi integrations

### REST API Integration Patterns

**REST API Usage**:
- Integration Users can use all REST API endpoints
- Follow REST API best practices
- Implement proper error handling
- Use appropriate API versions

**REST API Best Practices**:
- Use Named Credentials for endpoints
- Implement retry logic for transient failures
- Handle API limits appropriately
- Monitor API usage

**Related**: <a href="{{ '/rag/integrations/etl-vs-api-vs-events.html' | relative_url }}">ETL vs API vs Events</a> - Decision framework for integration patterns

### Bulk API Considerations

**Bulk API Usage**:
- Integration Users can use Bulk API for large operations
- Bulk API is efficient for high-volume operations
- Monitor Bulk API job status
- Handle Bulk API errors appropriately

**Bulk API Best Practices**:
- Use Bulk API for operations exceeding 2,000 records
- Monitor Bulk API job progress
- Implement error handling for failed records
- Use appropriate batch sizes

**Related**: <a href="{{ '/rag/integrations/sis-sync-patterns.html' | relative_url }}">SIS Sync Patterns</a> - High-volume batch synchronization patterns

## Summary

The Salesforce Integration User License provides a cost-effective and secure way to authenticate external systems with Salesforce. By following the setup, configuration, and best practices outlined in this guide, organizations can implement secure system-to-system integrations while optimizing license costs and maintaining strong security controls.

**Key Takeaways**:
- 5 free Integration User Licenses included with Enterprise, Performance, and Unlimited editions
- API-only access provides enhanced security
- One Integration User per external system enables clear audit trails
- OAuth 2.0 Client Credentials Flow is the recommended authentication method
- Permission Sets provide granular access control
- Regular audits and monitoring ensure security and compliance

## Q&A

### Q: What is the Salesforce Integration User License?

**A**: The **Integration User License** is a free API-only license designed for system-to-system integrations. It provides API access without UI access, costs $0 (5 free licenses included with Enterprise/Performance/Unlimited), and enables dedicated users per integration for better security and audit trails.

### Q: When should I use Integration User Licenses vs regular user licenses?

**A**: Use **Integration User Licenses** for system-to-system integrations, scheduled batch processes, integration platforms (MuleSoft, Boomi), and API-only access scenarios. Use **regular user licenses** for users requiring Salesforce UI access, portal users, or mobile app access.

### Q: How many Integration User Licenses do I get?

**A**: **5 free Integration User Licenses** are included with Enterprise, Performance, and Unlimited editions. Professional Edition does not include them (requires upgrade). Additional licenses can be purchased at approximately $10 per user per month.

### Q: What authentication methods can I use with Integration Users?

**A**: Use **OAuth 2.0 Client Credentials Flow** (recommended), **JWT Bearer Token Flow** (for enterprise with certificates), or **Username-Password Flow** (not recommended). OAuth 2.0 Client Credentials is the preferred method for secure, token-based authentication.

### Q: Can Integration Users access the Salesforce UI?

**A**: **No, Integration Users cannot access the Salesforce UI**. They have API-only access. Login attempts to the UI will fail. All access must be through APIs (REST, SOAP, Bulk, Streaming, Metadata). The profile cannot be modified to enable UI access.

### Q: How do I manage permissions for Integration Users?

**A**: Grant permissions through **Permission Sets** (the profile cannot be modified). Create dedicated Permission Sets per integration, grant only necessary object and field permissions, document permission rationale, and regularly audit permissions. Follow the principle of least privilege.

### Q: Should I use one Integration User per system or share users?

**A**: Use **one Integration User per external system**. This enables clear audit trails per integration, simplifies permission management, improves security isolation, and makes troubleshooting easier. Sharing users across systems makes it difficult to track which system performed actions.

### Q: How do I monitor Integration User activities?

**A**: Enable **Event Monitoring** for Integration Users, review API usage logs in Setup → Monitoring, track API call volumes and patterns, monitor for failed authentication attempts, review audit logs regularly, and set up dashboards for API usage. Monitor for security anomalies.

## Edge Cases and Limitations

### Edge Case 1: Integration User License Limits

**Scenario**: Organization requiring more than 5 Integration User Licenses, causing license constraints.

**Consideration**:
- Understand license limits (5 free with qualifying editions)
- Plan for license allocation across integrations
- Consider consolidating integrations when possible
- Document license usage and requirements
- Request additional licenses if needed
- Monitor license usage regularly

### Edge Case 2: Permission Set Management at Scale

**Scenario**: Managing permissions for many Integration Users with different access requirements.

**Consideration**:
- Use Permission Set Groups for role-based assignment
- Document permission requirements per integration
- Review permissions regularly
- Use least-privilege principle
- Test permissions in sandbox
- Monitor permission changes

### Edge Case 3: Integration User Authentication Failures

**Scenario**: OAuth token expiration or authentication failures causing integration disruptions.

**Consideration**:
- Implement token refresh logic
- Monitor authentication success rates
- Handle authentication errors gracefully
- Use Named Credentials for automatic token management
- Document authentication procedures
- Test authentication failure scenarios

### Edge Case 4: Integration User Audit Trail Complexity

**Scenario**: Multiple Integration Users making it difficult to track which integration performed actions.

**Consideration**:
- Use one Integration User per external system
- Enable Event Monitoring for Integration Users
- Review audit logs regularly
- Correlate API calls with integration jobs
- Document integration user assignments
- Monitor for security anomalies

### Edge Case 5: Migration from Connected App to Integration User

**Scenario**: Migrating existing integrations from Connected App authentication to Integration User Licenses.

**Consideration**:
- Plan migration carefully with dual-authentication period
- Test new authentication in sandbox
- Update integration code for new authentication
- Monitor authentication during transition
- Document migration procedures
- Plan for rollback if needed

### Limitations

- **License Limits**: Maximum 5 free Integration User Licenses (with qualifying editions)
- **UI Access**: Integration Users cannot access Salesforce UI
- **Mobile Access**: Integration Users cannot use Salesforce Mobile App
- **Portal Access**: Integration Users cannot access Experience Cloud portals
- **Permission Complexity**: Managing permissions for many Integration Users can be complex
- **Audit Trail**: Multiple Integration Users require careful audit trail management
- **Authentication**: OAuth token management adds complexity

## Related Patterns

**See Also**:
- <a href="{{ '/rag/security/permission-set-architecture.html' | relative_url }}">Permission Set Architecture</a> - Permission management patterns
- <a href="{{ '/rag/integrations/callout-best-practices.html' | relative_url }}">Callout Best Practices</a> - HTTP callout patterns for integration users

**Related Domains**:
- <a href="{{ '/rag/integrations/integration-platform-patterns.html' | relative_url }}">Integration Platform Patterns</a> - MuleSoft and Dell Boomi integration patterns
- <a href="{{ '/rag/integrations/etl-vs-api-vs-events.html' | relative_url }}">ETL vs API vs Events</a> - Integration pattern selection framework
- <a href="{{ '/rag/integrations/sis-sync-patterns.html' | relative_url }}">SIS Sync Patterns</a> - High-volume batch synchronization patterns

- <a href="{{ '/rag/integrations/integration-platform-patterns.html' | relative_url }}">Integration Platform Patterns</a> - MuleSoft and Dell Boomi integration patterns
- <a href="{{ '/rag/integrations/etl-vs-api-vs-events.html' | relative_url }}">ETL vs API vs Events</a> - Integration pattern selection framework
- <a href="{{ '/rag/security/permission-set-architecture.html' | relative_url }}">Permission Set Architecture</a> - Permission management patterns
- <a href="{{ '/rag/integrations/callout-best-practices.html' | relative_url }}">Callout Best Practices</a> - HTTP callout patterns for integration users
- <a href="{{ '/rag/integrations/sis-sync-patterns.html' | relative_url }}">SIS Sync Patterns</a> - High-volume batch synchronization patterns

