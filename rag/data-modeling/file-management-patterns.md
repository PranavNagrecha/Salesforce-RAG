---
layout: default
title: File Management Patterns
description: Salesforce provides multiple mechanisms for file storage and management, each with different use cases, limitations, and best practices
permalink: /rag/data-modeling/file-management-patterns.html
level: Intermediate
tags:
  - data-modeling
  - files
  - attachments
  - content
  - storage
last_reviewed: 2025-12-03
---

# File Management Patterns

## Overview

Salesforce provides multiple mechanisms for file storage and management: Attachments, Files (ContentVersion), ContentDocument, and Salesforce Files. Each mechanism has different use cases, limitations, and best practices.

**Core Principle**: Choose the file storage mechanism that best matches your requirements for sharing, versioning, storage limits, and access patterns. Different mechanisms serve different needs.

## Prerequisites

**Required Knowledge**:
- Understanding of Salesforce file storage options
- Familiarity with Attachments vs Files
- Knowledge of ContentDocument and ContentVersion
- Understanding of file sharing and permissions
- Knowledge of storage limits

**Recommended Reading**:
- <a href="{{ '/rag/security/sharing-fundamentals.html' | relative_url }}">Sharing Fundamentals</a> - File sharing patterns
- <a href="{{ '/rag/data-modeling/data-storage-planning.html' | relative_url }}">Data Storage Planning</a> - Storage planning patterns

## When to Use Each File Mechanism

### Use Attachments When

- **Legacy compatibility**: Working with legacy systems using Attachments
- **Simple use cases**: Simple file attachment to records
- **No versioning needed**: Don't need file versioning
- **Limited sharing**: Don't need complex sharing

**Limitations**:
- 25MB file size limit
- No versioning
- Limited sharing options
- Deprecated (use Files instead)

### Use Files (ContentVersion) When

- **Modern file storage**: Modern file storage mechanism
- **Versioning needed**: Need file versioning
- **Complex sharing**: Need complex sharing options
- **Large files**: Files up to 2GB (with Large File Upload)
- **Library management**: Need content libraries

**Benefits**:
- Up to 2GB file size (with Large File Upload)
- File versioning
- Rich sharing options
- Content libraries
- Better integration with Experience Cloud

## File Storage Mechanisms

### Mechanism 1: Attachments (Legacy)

**Object**: Attachment

**Use Cases**:
- Legacy system compatibility
- Simple record attachments
- Basic file storage

**Limitations**:
- 25MB file size limit
- No versioning
- Limited sharing
- Deprecated (use Files)

**Migration**: Migrate from Attachments to Files (ContentVersion) for modern file management.

### Mechanism 2: Files (ContentVersion)

**Object**: ContentVersion (file data), ContentDocument (file metadata), ContentDocumentLink (sharing)

**Use Cases**:
- Modern file storage
- File versioning
- Complex sharing
- Content libraries
- Large files (up to 2GB)

**Benefits**:
- Up to 2GB file size
- File versioning
- Rich sharing options
- Content libraries
- Better Experience Cloud integration

**Implementation**:
```apex
// Create file
ContentVersion cv = new ContentVersion(
    Title = 'Document.pdf',
    PathOnClient = 'Document.pdf',
    VersionData = Blob.valueOf('File content'),
    FirstPublishLocationId = recordId
);
insert cv;

// Link file to record
ContentDocumentLink cdl = new ContentDocumentLink(
    LinkedEntityId = recordId,
    ContentDocumentId = cv.ContentDocumentId,
    ShareType = 'V'
);
insert cdl;
```

### Mechanism 3: Salesforce Files

**Purpose**: Native Salesforce file storage with rich features.

**Features**:
- File versioning
- Content libraries
- Sharing sets
- Experience Cloud integration
- Mobile access

**Use Cases**:
- Document management
- Content libraries
- Portal file sharing
- Mobile file access

## File Sharing Patterns

### Pattern 1: Record-Based Sharing

**Purpose**: Share files with users who have access to the related record.

**Implementation**:
- **ContentDocumentLink**: Link files to records
- **ShareType**: 'V' (viewer), 'C' (collaborator), 'I' (inferred)
- **Automatic Sharing**: Files inherit record sharing

**Best Practices**:
- Link files to records
- Use appropriate ShareType
- Leverage record sharing
- Document sharing model

### Pattern 2: User-Based Sharing

**Purpose**: Share files directly with specific users.

**Implementation**:
- **ContentDocumentLink**: Link files to users
- **ShareType**: 'V' (viewer), 'C' (collaborator)
- **Direct Sharing**: Share with specific users

**Best Practices**:
- Share with specific users
- Use appropriate ShareType
- Document sharing
- Review sharing regularly

### Pattern 3: Library-Based Sharing

**Purpose**: Share files via content libraries.

**Implementation**:
- **ContentWorkspace**: Create content libraries
- **Library Sharing**: Share libraries with users/groups
- **File Organization**: Organize files in libraries

**Best Practices**:
- Create content libraries
- Share libraries appropriately
- Organize files logically
- Document library structure

## File Management Best Practices

### File Organization

- **Naming Conventions**: Use consistent file naming
- **Folder Structure**: Organize files logically
- **Content Libraries**: Use libraries for organization
- **Tagging**: Tag files for searchability

### File Versioning

- **Version Control**: Use ContentVersion for versioning
- **Version History**: Track file version history
- **Version Naming**: Name versions descriptively
- **Version Cleanup**: Clean up old versions

### File Storage Optimization

- **Storage Limits**: Monitor storage usage
- **File Compression**: Compress files when possible
- **File Archiving**: Archive old files
- **Storage Cleanup**: Remove unused files

### File Security

- **Sharing Controls**: Control file sharing
- **Field-Level Security**: Control field access
- **Encryption**: Encrypt sensitive files
- **Access Auditing**: Audit file access

## Migration Patterns

### Pattern 1: Attachments to Files Migration

**Purpose**: Migrate from Attachments to Files (ContentVersion).

**Implementation**:
- **Export Attachments**: Export Attachment records
- **Create ContentVersion**: Create ContentVersion from Attachment
- **Link to Records**: Link ContentVersion to original records
- **Verify Migration**: Verify files migrated correctly
- **Archive Attachments**: Archive original Attachments

**Best Practices**:
- Export before migration
- Create ContentVersion
- Link to records
- Verify migration
- Archive originals

### Pattern 2: External File Migration

**Purpose**: Migrate files from external systems to Salesforce.

**Implementation**:
- **Export from External**: Export files from external system
- **Import to Salesforce**: Import files to Salesforce
- **Link to Records**: Link files to Salesforce records
- **Verify Migration**: Verify files migrated correctly

**Best Practices**:
- Export from external
- Import to Salesforce
- Link to records
- Verify migration
- Document process

## Related Patterns

- <a href="{{ '/rag/security/sharing-fundamentals.html' | relative_url }}">Sharing Fundamentals</a> - File sharing patterns
- <a href="{{ '/rag/data-modeling/data-storage-planning.html' | relative_url }}">Data Storage Planning</a> - Storage planning patterns
- <a href="{{ '/rag/data-modeling/data-migration-patterns.html' | relative_url }}">Data Migration Patterns</a> - File migration patterns

## Q&A

### Q: What are the different file storage mechanisms in Salesforce?

**A**: Salesforce provides: (1) **Attachments** (legacy, 25MB limit, deprecated), (2) **Files (ContentVersion)** (modern, up to 2GB, versioning, rich sharing), (3) **Salesforce Files** (native file storage with libraries). Use Files (ContentVersion) for modern file management, migrate from Attachments.

### Q: When should I use Attachments vs Files?

**A**: Use **Files (ContentVersion)** for: (1) **Modern file storage** (recommended), (2) **Large files** (up to 2GB), (3) **Versioning** (file versioning), (4) **Complex sharing** (rich sharing options). Use **Attachments** only for: (1) **Legacy compatibility** (existing systems), (2) **Simple use cases** (basic attachments). Migrate from Attachments to Files.

### Q: How do I share files in Salesforce?

**A**: Share files by: (1) **Record-based sharing** (link files to records, inherit record sharing), (2) **User-based sharing** (share directly with users via ContentDocumentLink), (3) **Library-based sharing** (share via content libraries). Use ContentDocumentLink to control file sharing.

### Q: How do I migrate from Attachments to Files?

**A**: Migrate by: (1) **Export Attachments** (export Attachment records), (2) **Create ContentVersion** (create ContentVersion from Attachment), (3) **Link to records** (link ContentVersion to original records), (4) **Verify migration** (verify files migrated correctly), (5) **Archive Attachments** (archive original Attachments). Migration enables modern file management.

### Q: What are file storage limits in Salesforce?

**A**: Storage limits: (1) **Attachments** (25MB per file), (2) **Files** (2GB per file with Large File Upload), (3) **Org storage** (varies by edition, can purchase additional). Monitor storage usage and optimize file storage.

### Q: How do I organize files in Salesforce?

**A**: Organize by: (1) **Content libraries** (organize files in libraries), (2) **Naming conventions** (consistent file naming), (3) **Tagging** (tag files for searchability), (4) **Folder structure** (logical organization), (5) **Versioning** (use ContentVersion for versioning). Good organization improves file management.

### Q: How do I optimize file storage?

**A**: Optimize by: (1) **Monitor storage** (track storage usage), (2) **Compress files** (compress when possible), (3) **Archive old files** (archive unused files), (4) **Clean up** (remove unused files), (5) **Use appropriate mechanism** (choose right mechanism for use case). Storage optimization reduces costs and improves performance.
