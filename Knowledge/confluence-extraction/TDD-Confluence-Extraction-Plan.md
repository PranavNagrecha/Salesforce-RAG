# The Detail Department Confluence - Extraction Plan

## Current Status

✅ **Index Created**: `TDD-Confluence-Index.md` - Complete catalog of all topics and pages  
✅ **Objects Page Extracted**: Already in Knowledge folder as `SF-Objects-301125-090542.pdf`  
✅ **RAG Integration**: Objects content integrated into `rag/data-modeling/object-setup-and-configuration.md`

## Extraction Challenge

The Confluence space uses JavaScript-rendered content, making simple HTML scraping ineffective. The content loads dynamically, requiring:

1. **Browser automation** (Selenium/Playwright)
2. **Confluence REST API** access (if available)
3. **Manual export** from Confluence
4. **Confluence export tools**

## High-Priority Pages for Extraction

### 1. Rules for Fields
- **Page ID**: 58818628
- **URL**: https://tddprojects.atlassian.net/wiki/spaces/SF/pages/58818628/Rules+for+Fields
- **Priority**: HIGH - Field configuration best practices
- **Status**: ⏳ Pending extraction

### 2. New Salesforce Org
- **Priority**: HIGH - Initial org setup checklist
- **Status**: ⏳ Pending extraction

### 3. Flow Triggers (Before-Save and After-Save)
- **Priority**: HIGH - Flow automation patterns
- **Status**: ⏳ Pending extraction

### 4. Dynamic Forms and Dynamic Actions
- **Priority**: HIGH - Lightning form implementation
- **Status**: ⏳ Pending extraction

### 5. Clicks Or Code
- **Priority**: HIGH - Decision framework for declarative vs programmatic
- **Status**: ⏳ Pending extraction

### 6. Data Storage
- **Priority**: MEDIUM - Data storage best practices
- **Status**: ⏳ Pending extraction

### 7. Building a "Simple" Case Management Process
- **Priority**: MEDIUM - Case management patterns
- **Status**: ⏳ Pending extraction

### 8. Using Platform Events in Flows
- **Priority**: MEDIUM - Event-driven patterns
- **Status**: ⏳ Pending extraction

### 9. Salesforce Security
- **Priority**: HIGH - Security best practices
- **Status**: ⏳ Pending extraction

### 10. Lightning Web Components
- **Priority**: MEDIUM - LWC development patterns
- **Status**: ⏳ Pending extraction

## Recommended Extraction Methods

### Method 1: Browser Automation (Recommended)
```python
# Use Playwright or Selenium to render JavaScript
# Extract content after page fully loads
```

### Method 2: Confluence REST API
```python
# If API access is available
# Use Confluence REST API to get page content
```

### Method 3: Manual Export
1. Visit each page in browser
2. Use browser's "Print to PDF" or "Save Page As"
3. Convert PDFs to markdown if needed

### Method 4: Confluence Export Feature
1. Use Confluence's built-in export (if available)
2. Export space as HTML or PDF
3. Parse exported files

## Next Steps

1. **Immediate**: Create placeholder markdown files for high-priority pages
2. **Short-term**: Set up browser automation script for extraction
3. **Long-term**: Establish periodic sync process to keep content updated

## File Structure

Once extracted, organize files as:
```
Knowledge/
├── TDD-Confluence-Index.md (✅ Complete)
├── TDD-Confluence-Extraction-Plan.md (✅ This file)
├── SF-Objects-301125-090542.pdf (✅ Extracted)
├── TDD-Rules-for-Fields.md (⏳ Pending)
├── TDD-New-Salesforce-Org.md (⏳ Pending)
├── TDD-Flow-Triggers.md (⏳ Pending)
├── TDD-Dynamic-Forms.md (⏳ Pending)
├── TDD-Clicks-Or-Code.md (⏳ Pending)
└── [Additional pages as extracted]
```

## Integration with RAG

After extraction, evaluate each page for RAG integration:
- Extract patterns and best practices
- Create structured RAG files
- Update `rag-library.json` and `rag-index.md`
- Cross-reference with existing RAG content

