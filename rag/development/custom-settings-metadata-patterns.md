# Custom Settings and Custom Metadata Patterns

## Overview

This guide covers when and how to use Custom Settings and Custom Metadata Types for configuration management in Salesforce. These patterns are essential for externalizing configuration and enabling environment-specific settings.

**Related Patterns**:
- [Apex Patterns](apex-patterns.md) - Apex development patterns
- [Integration Patterns](../integrations/integration-platform-patterns.md) - Integration configuration

## Consensus Best Practices

- **Use Custom Metadata for new development**: Custom Metadata is the modern approach
- **Use Hierarchical Custom Settings for user-specific config**: When you need user-level configuration
- **Use List Custom Settings for simple lookups**: When you need simple key-value lookups
- **Externalize all configuration**: Never hardcode environment-specific values
- **Use Custom Metadata for package configuration**: Custom Metadata deploys with packages
- **Migrate from Custom Settings to Custom Metadata**: Plan migration for better maintainability

## Decision Framework: Custom Settings vs Custom Metadata

### Use Custom Settings When:
- Need **user-specific configuration** (Hierarchical Custom Settings)
- Need **simple key-value lookups** (List Custom Settings)
- **Legacy code** that hasn't been migrated
- Need **runtime configuration changes** without deployment

### Use Custom Metadata When:
- **New development** and configuration
- Need **package-deployable configuration**
- Need **metadata relationships** (lookup relationships)
- Need **longer field names** and more fields
- Need **validation rules** on configuration
- Need **field-level security** on configuration

### Use Other Approaches When:
- **Simple constants**: Use Apex constants or custom labels
- **Environment URLs**: Use Named Credentials
- **User preferences**: Use custom objects or user fields

## Custom Settings Patterns

### Pattern 1: Hierarchical Custom Settings

**When to use**: User-specific or org-wide configuration with hierarchy (User → Profile → Org).

**Implementation approach**:
- Create Hierarchical Custom Setting
- Access via `[SettingName]__c.getInstance()`
- Hierarchy: User → Profile → Org default
- Use for user-specific or org-wide configuration

**Why it's recommended**: Hierarchical Custom Settings provide user-level configuration with fallback to profile and org defaults. This is ideal for user-specific settings.

**Example scenario**: Email notification preferences. Each user can override profile defaults, which override org defaults.

**Key Points**:
- Access via `getInstance()` (user-level) or `getOrgDefaults()` (org-level)
- Hierarchy: User → Profile → Org
- Runtime changes (no deployment needed)
- Not package-deployable

### Pattern 2: List Custom Settings

**When to use**: Simple key-value lookups or configuration tables.

**Implementation approach**:
- Create List Custom Setting
- Access via `[SettingName]__c.getAll()` or `[SettingName]__c.getInstance(key)`
- Use for simple lookups or configuration tables

**Why it's recommended**: List Custom Settings provide simple key-value lookups that are cached and performant. Ideal for configuration tables or lookup data.

**Example scenario**: Country code to country name mapping. List Custom Setting stores country codes as keys with country names as values.

**Key Points**:
- Access via `getAll()` (all records) or `getInstance(key)` (specific record)
- Cached automatically
- Simple key-value lookups
- Not package-deployable

## Custom Metadata Patterns

### Pattern 1: Custom Metadata for Configuration

**When to use**: Environment-specific or package-deployable configuration.

**Implementation approach**:
- Create Custom Metadata Type
- Add fields for configuration values
- Access via SOQL: `SELECT Field1__c, Field2__c FROM CustomMetadataType__mdt`
- Deploy with packages

**Why it's recommended**: Custom Metadata Types are package-deployable and provide better structure than Custom Settings. They're the modern approach for configuration management.

**Example scenario**: Integration endpoint configuration. Custom Metadata stores endpoints, methods, and headers for each integration, deployable with packages.

**Key Points**:
- Access via SOQL queries
- Package-deployable
- Supports relationships and validation
- Metadata (not data) - changes require deployment

### Pattern 2: Custom Metadata in Apex

**When to use**: Accessing Custom Metadata in Apex code.

**Implementation approach**:
- Query Custom Metadata via SOQL
- Cache results in static variables
- Use for configuration lookups

**Why it's recommended**: Custom Metadata queries are performant and cached. Static variables provide efficient access patterns.

**Example scenario**: Integration configuration lookup. Apex queries Custom Metadata once and caches results for subsequent lookups.

**Key Points**:
- Query via SOQL (no DML)
- Cache in static variables
- Access like regular objects
- No governor limits for queries

### Pattern 3: Custom Metadata in Flows

**When to use**: Using Custom Metadata in Flow automation.

**Implementation approach**:
- Use Get Records element to query Custom Metadata
- Use Custom Metadata fields in Flow logic
- Reference Custom Metadata in Flow formulas

**Why it's recommended**: Custom Metadata provides configuration that Flows can access without hardcoding values. This enables configurable Flow logic.

**Example scenario**: Approval threshold configuration. Flow queries Custom Metadata to get approval thresholds based on record type.

**Key Points**:
- Query via Get Records element
- Use in Flow formulas
- No DML operations
- Package-deployable

## Migration Patterns

### Pattern 1: Migrating from Custom Settings to Custom Metadata

**When to use**: Modernizing configuration management.

**Migration steps**:
1. Create Custom Metadata Type with same fields
2. Migrate data from Custom Settings to Custom Metadata
3. Update code to query Custom Metadata instead of Custom Settings
4. Test thoroughly
5. Deploy and remove Custom Settings

**Why it's recommended**: Custom Metadata provides better maintainability, package deployment, and structure. Migration improves long-term maintainability.

**Key Points**:
- Plan migration carefully
- Migrate data first
- Update code incrementally
- Test thoroughly before removing Custom Settings

### Pattern 2: Migrating Hardcoded Values to Custom Metadata

**When to use**: Externalizing hardcoded configuration values.

**Migration steps**:
1. Identify hardcoded values
2. Create Custom Metadata Type
3. Add fields for configuration values
4. Populate Custom Metadata records
5. Update code to query Custom Metadata
6. Test and deploy

**Why it's recommended**: Externalizing hardcoded values enables environment-specific configuration and easier maintenance. This is essential for multi-environment deployments.

**Key Points**:
- Identify all hardcoded values
- Create appropriate Custom Metadata structure
- Update code to use Custom Metadata
- Test in all environments

## Best Practices

### Configuration Management

- **Externalize all configuration**: Never hardcode environment-specific values
- **Use Custom Metadata for new development**: Modern approach
- **Cache configuration values**: Use static variables for performance
- **Validate configuration**: Ensure configuration values are valid

### Security and Access

- **Field-level security**: Use FLS on Custom Metadata fields
- **Sharing rules**: Custom Metadata respects sharing rules
- **Package visibility**: Control Custom Metadata visibility in packages

### Performance

- **Cache queries**: Store Custom Metadata queries in static variables
- **Bulk queries**: Query all needed records in one query
- **Avoid in loops**: Don't query Custom Metadata in loops

## Related Patterns

- [Apex Patterns](apex-patterns.md) - Apex development patterns
- [Integration Patterns](../integrations/integration-platform-patterns.md) - Integration configuration
- [Custom Settings Examples](../code-examples/utilities/custom-settings-examples.md) - Custom Settings code examples
- [Custom Metadata Examples](../code-examples/utilities/custom-metadata-examples.md) - Custom Metadata code examples

