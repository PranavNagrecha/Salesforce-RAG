# Data Residency and Compliance for Salesforce

## Overview

This guide covers data residency and compliance patterns for Salesforce, including PII/PHI handling, GDPR/CCPA/SOC2 controls, field-level encryption, and Shield best practices. These patterns are essential for ensuring data protection, regulatory compliance, and maintaining customer trust.

**Related Patterns**:
- [Salesforce LLM Data Governance](../security/salesforce-llm-data-governance.md) - Data governance for LLM systems
- [Permission Set Architecture](../security/permission-set-architecture.md) - Access control patterns
- [Environment Strategy](../operations/environment-strategy.md) - Data masking patterns

## Consensus Best Practices

- **Classify data by sensitivity**: Identify and classify all PII/PHI data
- **Encrypt sensitive data at rest**: Use Shield Encryption for sensitive fields
- **Implement field-level security**: Control access to sensitive fields
- **Maintain audit trails**: Track access to and changes to sensitive data
- **Document compliance controls**: Document all compliance measures
- **Regular compliance reviews**: Conduct regular compliance audits
- **Train teams on compliance**: Ensure teams understand compliance requirements
- **Monitor compliance continuously**: Monitor and alert on compliance violations

## PII/PHI Handling

### PII Identification Patterns

**PII Categories**:
- **Direct identifiers**: Name, SSN, email, phone number
- **Indirect identifiers**: Date of birth, zip code, IP address
- **Biometric data**: Fingerprints, facial recognition data
- **Location data**: GPS coordinates, address history

**PHI Categories**:
- **Health information**: Medical records, diagnoses, treatments
- **Health identifiers**: Medical record numbers, health plan numbers
- **Payment information**: Insurance information, billing records
- **Research data**: De-identified health data

**PII/PHI Identification Process**:
1. Inventory all data fields in org
2. Classify fields by sensitivity level
3. Document PII/PHI fields
4. Review and update classification regularly

### PHI Protection Strategies

**HIPAA Compliance**:
- Implement administrative safeguards
- Implement physical safeguards
- Implement technical safeguards
- Conduct risk assessments
- Maintain Business Associate Agreements (BAAs)

**PHI Protection Measures**:
- Encrypt PHI at rest and in transit
- Implement access controls
- Maintain audit logs
- Train staff on HIPAA requirements
- Document PHI handling procedures

**PHI Access Controls**:
- Role-based access to PHI
- Field-level security for PHI fields
- Audit trail for PHI access
- Regular access reviews

### Data Classification

**Classification Levels**:
- **Public**: No restrictions, can be shared freely
- **Internal**: Restricted to organization, not public
- **Confidential**: Restricted to authorized personnel
- **Restricted**: Highest sensitivity, strictest controls

**Classification Process**:
- Classify all data fields
- Document classification rationale
- Review classifications regularly
- Update classifications as needed

**Classification Implementation**:
- Use field-level security
- Implement sharing rules
- Use encryption for sensitive data
- Monitor data access

## GDPR/CCPA/SOC2 Controls

### GDPR Compliance Framework

**GDPR Principles**:
- **Lawfulness, fairness, transparency**: Process data lawfully and transparently
- **Purpose limitation**: Collect data for specified purposes only
- **Data minimization**: Collect only necessary data
- **Accuracy**: Keep data accurate and up to date
- **Storage limitation**: Retain data only as long as necessary
- **Integrity and confidentiality**: Protect data security
- **Accountability**: Demonstrate compliance

**Data Subject Rights**:
- **Right to access**: Provide data subjects access to their data
- **Right to rectification**: Correct inaccurate data
- **Right to erasure**: Delete data upon request (right to be forgotten)
- **Right to restrict processing**: Restrict data processing
- **Right to data portability**: Export data in portable format
- **Right to object**: Object to data processing

**GDPR Implementation**:
- Implement data subject request processes
- Maintain consent management
- Document data processing activities
- Conduct Data Protection Impact Assessments (DPIAs)
- Appoint Data Protection Officer (DPO) if required

### CCPA Compliance Framework

**CCPA Requirements**:
- **Right to know**: Consumers can request data disclosure
- **Right to delete**: Consumers can request data deletion
- **Right to opt-out**: Consumers can opt-out of data sales
- **Non-discrimination**: Cannot discriminate for exercising rights

**CCPA Implementation**:
- Implement consumer request processes
- Maintain opt-out mechanisms
- Document data sharing and sales
- Train staff on CCPA requirements
- Update privacy policies

### SOC2 Controls

**SOC2 Trust Service Criteria**:
- **Security**: System is protected against unauthorized access
- **Availability**: System is available for operation
- **Processing integrity**: System processing is complete and accurate
- **Confidentiality**: Confidential information is protected
- **Privacy**: Personal information is collected and used appropriately

**SOC2 Implementation**:
- Document control objectives
- Implement control activities
- Monitor control effectiveness
- Conduct regular audits
- Maintain audit evidence

**SOC2 Controls for Salesforce**:
- Access controls and authentication
- Data encryption
- Audit logging
- Change management
- Incident response

## Field-Level Encryption

### Shield Encryption Patterns

**Shield Platform Encryption**:
- Encrypt data at rest in database
- Encrypt data in search indexes
- Encrypt data in file storage
- Maintain encryption keys securely

**Encryption Implementation**:
- Identify fields requiring encryption
- Enable Shield Platform Encryption
- Configure encryption for identified fields
- Test encryption functionality
- Document encryption configuration

**Encryption Best Practices**:
- Encrypt all PII/PHI fields
- Use deterministic encryption for searchable fields
- Use probabilistic encryption for maximum security
- Manage encryption keys securely
- Monitor encryption status

### Field-Level Security

**Field-Level Security (FLS)**:
- Control access to individual fields
- Implement role-based field access
- Use permission sets for field access
- Document field access requirements

**FLS Implementation**:
- Review all fields for sensitivity
- Configure FLS per field
- Test FLS configuration
- Monitor FLS effectiveness
- Update FLS as needed

**FLS Best Practices**:
- Principle of least privilege
- Regular access reviews
- Document FLS decisions
- Test FLS in all environments

### Encryption Key Management

**Key Management Patterns**:
- **Salesforce-managed keys**: Salesforce manages encryption keys
- **Customer-managed keys**: Customer manages encryption keys (BYOK)
- **Hybrid approach**: Mix of Salesforce and customer-managed keys

**Key Management Best Practices**:
- Rotate keys regularly
- Secure key storage
- Monitor key usage
- Document key management procedures
- Plan for key recovery

## Shield Best Practices

### Platform Encryption

**Platform Encryption Features**:
- Encrypt standard and custom fields
- Encrypt files and attachments
- Encrypt search indexes
- Support for deterministic and probabilistic encryption

**Platform Encryption Implementation**:
- Enable Platform Encryption
- Identify fields for encryption
- Configure field encryption
- Test encryption functionality
- Monitor encryption performance

**Platform Encryption Considerations**:
- Performance impact of encryption
- Search functionality with encryption
- Integration with external systems
- Backup and restore with encryption

### Event Monitoring

**Event Monitoring Features**:
- Track user activity
- Monitor data access
- Detect security threats
- Audit compliance activities

**Event Monitoring Implementation**:
- Enable Event Monitoring
- Configure event types to monitor
- Set up event monitoring dashboards
- Create alerts for suspicious activity
- Review event logs regularly

**Event Monitoring Best Practices**:
- Monitor critical events
- Set up automated alerts
- Review logs regularly
- Document monitoring procedures
- Respond to security events

### Field Audit Trail

**Field Audit Trail Features**:
- Track field value changes
- Maintain change history
- Support compliance audits
- Enable data lineage tracking

**Field Audit Trail Implementation**:
- Enable Field Audit Trail
- Identify fields for audit tracking
- Configure audit trail per field
- Test audit trail functionality
- Review audit trail data

**Field Audit Trail Best Practices**:
- Audit all sensitive fields
- Maintain audit trail retention
- Review audit trails regularly
- Export audit data for compliance
- Document audit trail configuration

## Compliance Documentation

### Compliance Documentation Requirements

**Documentation Types**:
- Data classification inventory
- Data processing documentation
- Access control documentation
- Encryption configuration documentation
- Audit trail documentation
- Incident response procedures

**Documentation Maintenance**:
- Keep documentation current
- Review documentation regularly
- Update documentation with changes
- Maintain version control
- Store documentation securely

### Compliance Audits

**Audit Preparation**:
- Maintain compliance documentation
- Conduct internal audits
- Prepare audit evidence
- Train staff on audit procedures
- Schedule regular audits

**Audit Execution**:
- Provide audit evidence
- Answer auditor questions
- Document audit findings
- Address audit findings
- Follow up on remediation

## Related Patterns

- [Salesforce LLM Data Governance](../security/salesforce-llm-data-governance.md) - Data governance for LLM systems
- [Permission Set Architecture](../security/permission-set-architecture.md) - Access control patterns
- [Environment Strategy](../operations/environment-strategy.md) - Data masking patterns
- [Data Quality & Stewardship](data-quality-stewardship.md) - Data quality patterns

