# Terminology Mapping and Standardization

This document defines the standard terminology to be used consistently across the RAG repository. All files should use these terms to ensure consistency and improve RAG retrieval quality.

## Standard Terms

### Experience Cloud / Communities / Portals

**Standard Term**: **Experience Cloud**

**Variations to Replace**:
- "Communities" → "Experience Cloud"
- "Community" → "Experience Cloud site" or "Experience Cloud"
- "Portal" → "Experience Cloud" (when referring to Salesforce Experience Cloud)
- "Customer Portal" → "Experience Cloud site"
- "Partner Portal" → "Experience Cloud site"

**Usage Notes**: Always use "Experience Cloud" as the primary term. When referring to a specific site, use "Experience Cloud site" or "Experience Cloud portal" for clarity.

### Permission Sets

**Standard Term**: **Permission Set**

**Variations to Replace**:
- "Perm Set" → "Permission Set"
- "PS" → "Permission Set" (avoid abbreviations)
- "Permission Set Group" → "Permission Set Group" (keep full term)

**Usage Notes**: Always use the full term "Permission Set" in documentation. Abbreviations may be used in code comments or technical contexts only.

### Record-Triggered Flows

**Standard Term**: **Record-Triggered Flow**

**Variations to Replace**:
- "RTF" → "Record-Triggered Flow"
- "Record Trigger Flow" → "Record-Triggered Flow"
- "Auto-Launched Flow" → "Record-Triggered Flow" (when triggered by record changes)

**Usage Notes**: Use "Record-Triggered Flow" for flows triggered by record changes. Use "Auto-Launched Flow" only when referring to flows called programmatically.

### Platform Events

**Standard Term**: **Platform Events**

**Variations to Replace**:
- "PE" → "Platform Events" (avoid abbreviations)
- "Event" → "Platform Event" (when referring to Salesforce Platform Events specifically)

**Usage Notes**: Use "Platform Events" for Salesforce Platform Events. Use "event" generically when referring to events in general.

### Change Data Capture

**Standard Term**: **Change Data Capture (CDC)**

**Variations to Replace**:
- "CDC Events" → "Change Data Capture events"
- "Change Events" → "Change Data Capture events"

**Usage Notes**: First reference should be "Change Data Capture (CDC)", subsequent references can use "CDC".

### Lightning Web Components

**Standard Term**: **Lightning Web Component (LWC)**

**Variations to Replace**:
- "LWC Component" → "Lightning Web Component" (redundant)
- "Lightning Component" → "Lightning Web Component" (when referring to LWC specifically)

**Usage Notes**: First reference should be "Lightning Web Component (LWC)", subsequent references can use "LWC".

### Apex

**Standard Term**: **Apex**

**Variations to Replace**:
- "Apex Code" → "Apex" (redundant)
- "Salesforce Apex" → "Apex" (context is clear)

**Usage Notes**: Use "Apex" as the standard term. Specify "Apex class", "Apex trigger", "Apex method" when needed for clarity.

### SOQL

**Standard Term**: **SOQL**

**Variations to Replace**:
- "SOQL Query" → "SOQL query" (SOQL already implies query)
- "Salesforce Object Query Language" → "SOQL" (use abbreviation after first reference)

**Usage Notes**: First reference can be "SOQL (Salesforce Object Query Language)", subsequent references use "SOQL".

### External ID

**Standard Term**: **External ID**

**Variations to Replace**:
- "External ID Field" → "External ID" (field is implied)
- "Ext ID" → "External ID" (avoid abbreviations)

**Usage Notes**: Use "External ID" as the standard term. Specify "External ID field" when needed for clarity.

### Integration User License

**Standard Term**: **Integration User License**

**Variations to Replace**:
- "Integration License" → "Integration User License"
- "API-Only License" → "Integration User License" (when referring to Integration User License specifically)

**Usage Notes**: Use "Integration User License" as the standard term. Can use "API-only license" when explaining the concept.

### Named Credential

**Standard Term**: **Named Credential**

**Variations to Replace**:
- "Named Credentials" → "Named Credential" (when referring to the feature)
- "Credential" → "Named Credential" (when referring to Salesforce Named Credentials)

**Usage Notes**: Use "Named Credential" as the standard term. Plural "Named Credentials" when referring to multiple instances.

### Flow

**Standard Term**: **Flow**

**Variations to Replace**:
- "Salesforce Flow" → "Flow" (context is clear)
- "Flow Builder" → "Flow" (when referring to the automation, not the tool)

**Usage Notes**: Use "Flow" as the standard term. Specify "Record-Triggered Flow", "Screen Flow", "Autolaunched Flow" when needed.

### Process Builder

**Standard Term**: **Process Builder** (with deprecation note)

**Variations to Replace**: None (but always include deprecation warning)

**Usage Notes**: Always include deprecation warning: "Process Builder (deprecated - use Record-Triggered Flows instead)".

### Workflow Rules

**Standard Term**: **Workflow Rules** (with deprecation note)

**Variations to Replace**: None (but always include deprecation warning)

**Usage Notes**: Always include deprecation warning: "Workflow Rules (deprecated - use Record-Triggered Flows instead)".

### Profile

**Standard Term**: **Profile**

**Variations to Replace**: None

**Usage Notes**: Use "Profile" as the standard term. In permission set-driven architecture, clarify that profiles are for UI configuration only.

### Sandbox

**Standard Term**: **Sandbox**

**Variations to Replace**:
- "Sandbox Org" → "Sandbox" (redundant)
- "SB" → "Sandbox" (avoid abbreviations)

**Usage Notes**: Use "Sandbox" as the standard term. Specify "Developer Sandbox", "Partial Copy Sandbox", etc. when needed.

### Scratch Org

**Standard Term**: **Scratch Org**

**Variations to Replace**:
- "Scratch Organization" → "Scratch Org"
- "SO" → "Scratch Org" (avoid abbreviations)

**Usage Notes**: Use "Scratch Org" as the standard term.

## Terminology by Domain

### Development Terms

- **Apex** (not "Apex Code")
- **Lightning Web Component (LWC)** (not "LWC Component")
- **Flow** (not "Salesforce Flow")
- **Record-Triggered Flow** (not "RTF")
- **SOQL** (not "SOQL Query" redundantly)
- **SOSL** (Salesforce Object Search Language)

### Integration Terms

- **Platform Events** (not "PE")
- **Change Data Capture (CDC)** (first reference, then "CDC")
- **Named Credential** (not "Credential" generically)
- **Integration User License** (not "Integration License")
- **ETL** (Extract, Transform, Load)
- **REST API** (not "REST" alone)
- **SOAP API** (not "SOAP" alone)
- **Bulk API** (not "Bulk" alone)

### Security Terms

- **Permission Set** (not "Perm Set" or "PS")
- **Permission Set Group** (full term)
- **Profile** (standard term)
- **Experience Cloud** (not "Communities" or "Portal")
- **Organization-Wide Defaults (OWD)** (first reference, then "OWD")

### Data Modeling Terms

- **External ID** (not "Ext ID")
- **Custom Object** (not "Custom Objects" when singular)
- **Custom Field** (not "Custom Fields" when singular)
- **Lookup Field** (not "Lookup" alone)
- **Master-Detail Field** (not "Master-Detail" alone)

### Architecture Terms

- **Experience Cloud** (not "Communities")
- **Sandbox** (not "Sandbox Org")
- **Scratch Org** (not "Scratch Organization")
- **Production Org** (or just "Production")
- **Multi-Org** (acceptable abbreviation)
- **Single-Org** (acceptable abbreviation)

## Deprecated Terms

### Always Include Deprecation Warnings

- **Workflow Rules**: Always note "(deprecated - use Record-Triggered Flows instead)"
- **Process Builder**: Always note "(deprecated - use Record-Triggered Flows instead)"
- **Flow User Permission**: Always note "(deprecated in Winter '26 - use Flow permissions in Permission Sets instead)"

## Implementation Guidelines

1. **First Reference**: Use full term with abbreviation in parentheses: "Lightning Web Component (LWC)"
2. **Subsequent References**: Use abbreviation: "LWC"
3. **Consistency**: Use the same term throughout a file
4. **Context**: Ensure term is clear in context
5. **Deprecation**: Always include deprecation warnings for deprecated features

## Cross-Reference

- See [Core Terminology](../glossary/core-terminology.md) for complete definitions
- See [Style Guide](style-guide.md) for voice and tone standards

