---
title: "File Management Patterns"
level: "Intermediate"
tags:
  - data-modeling
  - file-management
  - contentversion
  - attachments
  - documents
last_reviewed: "2025-01-XX"
---

# File Management Patterns

## Overview

Salesforce provides multiple mechanisms for file storage and management. Understanding when to use ContentVersion (Files), Attachments, Documents, and the Library system is critical for effective data management and user experience.

## File Storage Mechanisms

### ContentVersion (Files)

**Modern file storage mechanism** - recommended for new implementations.

**Characteristics**:
- Stored in ContentVersion and ContentDocument objects
- Linked to records via ContentDocumentLink
- Supports versioning (multiple versions per document)
- Supports sharing and collaboration
- Integrated with Salesforce Files
- Available in Lightning Experience and mobile
- Supports file preview and inline viewing

**Use Cases**:
- User-uploaded files attached to records
- Document management and collaboration
- Files that need versioning
- Files that need sharing across records
- Modern Salesforce implementations

**Best Practices**:
- Use ContentVersion for all new file storage needs
- Leverage versioning for document management
- Use ContentDocumentLink for record associations
- Consider file sharing requirements
- Monitor storage usage

### Attachments

**Legacy file storage mechanism** - still supported but not recommended for new implementations.

**Characteristics**:
- Stored in Attachment object
- Direct relationship to parent record
- No versioning support
- Limited sharing capabilities
- Not fully integrated with Lightning Experience
- Simpler structure than ContentVersion

**Use Cases**:
- Legacy implementations
- Simple file attachments without versioning needs
- Migration from older systems

**Best Practices**:
- Avoid for new implementations
- Consider migrating to ContentVersion
- Use only for simple attachment needs
- Be aware of Lightning Experience limitations

### Documents

**Library-style document storage** - for organizational documents.

**Characteristics**:
- Stored in Document object
- Organizational-level storage
- Not linked to specific records
- Used for templates and shared documents
- Available in Classic and Lightning

**Use Cases**:
- Email templates
- Document templates
- Organizational documents
- Shared resources

**Best Practices**:
- Use for organizational documents
- Not for record-specific attachments
- Consider for template storage

### Library System

**Organized file storage** - for structured document management.

**Characteristics**:
- Organized file storage system
- Folder-based organization
- Supports categorization
- Integrated with ContentVersion
- Available in Lightning Experience

**Use Cases**:
- Organized document libraries
- Categorized file storage
- Department or project-based file organization
- Structured document management

**Best Practices**:
- Use for organized file storage
- Leverage folder structure
- Consider for project-based organization
- Integrate with ContentVersion

## Decision Framework

### When to Use ContentVersion (Files)

**Use ContentVersion when**:
- Building new implementations
- Need versioning support
- Need file sharing across records
- Want Lightning Experience integration
- Need collaboration features
- Want modern file management

**Example Use Cases**:
- Case attachments
- Account documents
- Application supporting documents
- Contract attachments
- Collaboration documents

### When to Use Attachments

**Use Attachments when**:
- Maintaining legacy implementations
- Simple attachment needs
- No versioning required
- Classic-only implementations
- Migration from older systems

**Example Use Cases**:
- Legacy system integrations
- Simple file attachments
- Temporary file storage

### When to Use Documents

**Use Documents when**:
- Organizational templates
- Shared resources
- Email templates
- Document templates
- Not record-specific

**Example Use Cases**:
- Email templates
- Document templates
- Organizational policies
- Shared resources

### When to Use Library System

**Use Library System when**:
- Need organized file storage
- Want folder-based organization
- Need categorization
- Project-based file management
- Department-based organization

**Example Use Cases**:
- Project document libraries
- Department file storage
- Categorized document management
- Structured file organization

## Implementation Patterns

### ContentVersion Implementation

**Pattern**: Use ContentVersion for record attachments

**Implementation**:
1. Create ContentVersion record for file upload
2. Create ContentDocumentLink to associate with record
3. Use ContentDocument for file metadata
4. Leverage versioning for document management

**Example**:
- User uploads file to Case record
- ContentVersion created with file data
- ContentDocumentLink created linking file to Case
- File appears in Case's Files related list

### File Upload Patterns

**Pattern**: Handle file uploads in Flows or Apex

**Flow Implementation**:
- Use File Upload component in Screen Flows
- Store file in ContentVersion
- Create ContentDocumentLink
- Associate with record

**Apex Implementation**:
- Use ContentVersion for file storage
- Create ContentDocumentLink for associations
- Handle file metadata
- Support versioning

### File Sharing Patterns

**Pattern**: Share files across multiple records

**Implementation**:
- Create ContentDocumentLink for each record
- Support sharing across related records
- Manage sharing permissions
- Control file visibility

**Use Cases**:
- Share file across multiple Cases
- Share document with related Accounts
- Collaborative document management

### File Versioning Patterns

**Pattern**: Manage multiple versions of documents

**Implementation**:
- Use ContentVersion for versioning
- Track version history
- Support version comparison
- Manage current version

**Use Cases**:
- Contract version management
- Document revision tracking
- Version-controlled documents

## Storage Management

### Storage Limits

**Considerations**:
- File storage counts against org storage limits
- Monitor storage usage regularly
- Implement file retention policies
- Archive old files when appropriate

**Best Practices**:
- Monitor storage usage
- Implement retention policies
- Archive old files
- Consider external storage for large files
- Compress files when possible

### File Cleanup Patterns

**Pattern**: Regular cleanup of old or unused files

**Implementation**:
- Scheduled Flow or Apex job for cleanup
- Identify files based on age or usage
- Archive or delete old files
- Maintain file metadata

**Best Practices**:
- Regular cleanup schedules
- Archive before deletion
- Maintain audit trails
- Notify users before deletion

## Security and Access Control

### File-Level Security

**Pattern**: Control file access based on record permissions

**Implementation**:
- Files inherit record permissions
- ContentDocumentLink controls access
- Field-level security applies
- Sharing rules affect file visibility

**Best Practices**:
- Align file permissions with record permissions
- Use ContentDocumentLink for access control
- Consider file sharing requirements
- Review file access regularly

### File Sharing Patterns

**Pattern**: Share files with specific users or groups

**Implementation**:
- Use ContentDocumentLink for user sharing
- Support group sharing
- Manage sharing permissions
- Control file visibility

**Best Practices**:
- Use sharing for collaboration
- Review sharing regularly
- Align with business requirements
- Document sharing policies

## Integration Patterns

### External File Storage

**Pattern**: Store files externally and reference in Salesforce

**Implementation**:
- Store files in external system (e.g., AWS S3, SharePoint)
- Store file URL or reference in Salesforce
- Access files via external links
- Manage file lifecycle externally

**Use Cases**:
- Large file storage
- Compliance requirements
- External file management systems
- Cost optimization

**Best Practices**:
- Use for large files
- Maintain file references
- Consider access patterns
- Document external storage

### File Migration Patterns

**Pattern**: Migrate from Attachments to ContentVersion

**Implementation**:
- Identify Attachment records
- Create ContentVersion records
- Create ContentDocumentLink records
- Archive or delete Attachment records
- Update integrations and references

**Best Practices**:
- Plan migration carefully
- Test migration process
- Maintain data integrity
- Update integrations
- Document migration

## Best Practices Summary

### File Storage Selection

- **Use ContentVersion** for new implementations
- **Use Attachments** only for legacy systems
- **Use Documents** for organizational templates
- **Use Library System** for organized storage

### Implementation

- **Leverage versioning** for document management
- **Use ContentDocumentLink** for record associations
- **Implement file sharing** when needed
- **Monitor storage usage** regularly

### Security

- **Align file permissions** with record permissions
- **Use ContentDocumentLink** for access control
- **Review file access** regularly
- **Document sharing policies**

### Maintenance

- **Implement retention policies**
- **Archive old files** regularly
- **Monitor storage usage**
- **Clean up unused files**

## Related Patterns

- See `rag/data-modeling/object-setup-and-configuration.md` for object setup patterns
- See `rag/development/flow-patterns.md` for Flow file upload patterns
- See `rag/development/apex-patterns.md` for Apex file management patterns

## Q&A

### Q: What is the difference between ContentVersion (Files) and Attachments?

**A**: **ContentVersion (Files)** is the modern file storage mechanism (recommended for new implementations). It supports versioning, sharing, collaboration, and is integrated with Lightning Experience. **Attachments** is the legacy mechanism (still supported but not recommended). It has no versioning, limited sharing, and is not fully integrated with Lightning. Use ContentVersion for all new file storage needs.

### Q: When should I use ContentVersion vs. Attachments vs. Documents?

**A**: Use **ContentVersion** for: user-uploaded files, document management, files needing versioning, modern implementations. Use **Attachments** for: legacy implementations only, simple attachments without versioning. Use **Documents** for: internal document libraries, template storage, documents not linked to records. Prefer ContentVersion for all new implementations.

### Q: How do I link files to records in Salesforce?

**A**: Link files by: (1) **ContentDocumentLink** - links ContentVersion files to records (many-to-many relationship), (2) **Attachment.ParentId** - links Attachments to parent record (direct relationship), (3) **ContentVersion sharing** - share files across multiple records using ContentDocumentLink. ContentDocumentLink provides flexible file-to-record relationships.

### Q: What is file versioning and how does it work?

**A**: **File versioning** allows multiple versions of the same file. ContentVersion supports versioning (each upload creates a new version), while Attachments do not. Versioning enables: (1) **Track file history** (see all versions), (2) **Revert to previous versions** (if needed), (3) **Collaborative editing** (multiple users can upload versions), (4) **Audit trail** (who uploaded which version). Use ContentVersion when versioning is needed.

### Q: How do I manage file storage in Salesforce?

**A**: Manage storage by: (1) **Monitor file storage usage** (separate from data storage), (2) **Archive old files** to external storage, (3) **Delete unused files** regularly, (4) **Compress files** when possible, (5) **Set file retention policies** (automated cleanup), (6) **Use ContentVersion** (more efficient than Attachments). File storage has separate limits from data storage.

### Q: What is the difference between Files and Documents?

**A**: **Files (ContentVersion)** are user-uploaded files attached to records, support versioning and sharing, integrated with Lightning Experience. **Documents** are internal document libraries, typically templates or reference documents, not linked to records, stored in Documents tab. Use Files for record attachments, Documents for internal libraries.

### Q: How do I share files across multiple records?

**A**: Share files by: (1) **ContentDocumentLink** - create multiple ContentDocumentLink records linking same file to multiple records, (2) **File sharing** - share files with users, groups, or records, (3) **Library sharing** - share document libraries. ContentDocumentLink enables many-to-many file-to-record relationships, allowing files to be shared across multiple records.

### Q: What are file storage limits in Salesforce?

**A**: File storage limits: (1) **Professional** - 1 GB file storage, (2) **Enterprise/Performance/Unlimited** - 10 GB file storage (can purchase additional), (3) **File storage separate from data storage** (different limits), (4) **Big Objects** have separate storage (doesn't count toward file storage). Monitor file storage separately and plan for growth.

### Q: How do I handle file uploads in Flows and Apex?

**A**: Handle uploads by: (1) **Flow** - use File Upload component in Screen Flows, (2) **Apex** - use ContentVersion and ContentDocumentLink APIs, (3) **REST API** - use ContentVersion API endpoints, (4) **Bulk API** - for bulk file uploads. ContentVersion API provides programmatic file management. Always use ContentVersion for new implementations.

### Q: What are best practices for file management?

**A**: Best practices include: (1) **Use ContentVersion** for all new file storage (not Attachments), (2) **Leverage versioning** for document management, (3) **Use ContentDocumentLink** for record associations, (4) **Monitor file storage** usage regularly, (5) **Archive old files** to external storage, (6) **Set retention policies** (automated cleanup), (7) **Compress files** when possible, (8) **Delete unused files** regularly.

## Related Patterns

- [Object Setup and Configuration](object-setup-and-configuration.html) - Object setup patterns
- [Flow Patterns](../development/flow-patterns.html) - Flow file upload patterns
- [Apex Patterns](../development/apex-patterns.html) - Apex file management patterns

## References

- Salesforce Documentation: Files and Attachments
- Trailhead: Files and Content Management
- Best Practices: File Storage in Salesforce

