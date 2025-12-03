#!/usr/bin/env python3
"""
Automatically rebuild rag-index.md from rag/ folder and sync homepage

This script:
1. Scans rag/ folder structure for all .md files
2. Reads each file to extract metadata (title, description, etc.)
3. Rebuilds rag-index.md with all files organized by domain
4. Syncs homepage categories with rag-index.md
5. Ensures all links work correctly

Just run: python website/scripts/sync-homepage.py

LESSONS LEARNED (Don't repeat these mistakes):
1. Finding closing </div> tag: Must count nested divs, not just find first </div>
   - domain-grid contains domain-card divs, so need to track depth
   - Use depth counter: +1 for <div, -1 for </div>, stop when depth == 0
2. File organization: Always scan actual rag/ folder, don't just reference rag-index.md
   - This ensures new files are automatically included
   - Extracts metadata from actual files, not stale index
3. Homepage sync: Must replace entire domain-grid section, not just append
   - Find grid_start and grid_end correctly
   - Replace everything between, including all cards
4. Metadata extraction: Handle missing frontmatter gracefully
   - Fall back to filename if no title
   - Extract from Overview section if no description
   - Don't fail if metadata is missing
5. Domain mapping: Map folder names to section names consistently
   - Use FOLDER_TO_SECTION dict for all mappings
   - Handle edge cases (quick-start vs Quick Start Guides)
6. Verification: Always verify output structure
   - Check that correct number of cards are generated
   - Ensure closing tags are correct
   - Validate HTML structure
7. Dependencies: Script requires PyYAML for YAML frontmatter parsing
   - GitHub Actions needs: pip install pyyaml
   - Local development: pip install pyyaml or pip install -r requirements.txt
   - Don't assume dependencies are installed
"""

import re
import sys
import json
import yaml
from pathlib import Path
from collections import defaultdict
from datetime import datetime

# Folder to section name mapping
FOLDER_TO_SECTION = {
    "architecture": "Architecture Patterns",
    "integrations": "Integration Patterns",
    "identity-sso": "Identity and SSO",
    "data-modeling": "Data Modeling",
    "security": "Security",
    "best-practices": "Best Practices",
    "development": "Development",
    "troubleshooting": "Troubleshooting",
    "patterns": "Patterns",
    "glossary": "Glossary",
    "project-methods": "Project Methods",
    "operations": "Operations",
    "observability": "Observability",
    "data-governance": "Data Governance",
    "adoption": "Adoption",
    "testing": "Testing",
    "quick-start": "Quick Start Guides",
    "api-reference": "API Reference",
    "mcp-knowledge": "MCP Knowledge",
    "code-examples": "Code Examples",
}

# Emoji mapping for categories
EMOJI_MAP = {
    "Architecture Patterns": "🏗️",
    "Integration Patterns": "🔌",
    "Identity and SSO": "🔐",
    "Data Modeling": "📊",
    "Security": "🔒",
    "Best Practices": "⭐",
    "Development": "💻",
    "Troubleshooting": "🔧",
    "Patterns": "🔀",
    "Glossary": "📖",
    "Project Methods": "📋",
    "Operations": "🚀",
    "Observability": "📊",
    "Data Governance": "🛡️",
    "Adoption": "👥",
    "Testing": "✅",
    "Quick Start Guides": "⚡",
    "API Reference": "📚",
    "MCP Knowledge": "🔧",
    "Code Examples": "📝",
}

# Sections to exclude (meta/documentation sections)
EXCLUDE_SECTIONS = {
    "Overview",
    "How to use this index",
    "Directory Structure",
    "Retrieval Guidelines",
    "Terminology",
    "File Status",
    "Maintenance",
}

# Files to exclude
EXCLUDE_FILES = {
    "rag-index.md",
    "README.md",
    "CONTRIBUTING.md",
    "MAINTENANCE.md",
}


def get_anchor_id(section_name):
    """Convert section name to anchor ID (lowercase, hyphens)"""
    return section_name.lower().replace(" ", "-").replace("&", "and")


def extract_frontmatter(content):
    """Extract YAML frontmatter from markdown file
    
    LESSON LEARNED: Handle missing frontmatter gracefully
    - Not all files have frontmatter
    - Return empty dict if missing, don't fail
    """
    if not content.startswith('---'):
        return {}
    
    try:
        end = content.find('---', 3)
        if end == -1:
            return {}
        
        frontmatter_text = content[3:end].strip()
        return yaml.safe_load(frontmatter_text) or {}
    except:
        return {}


def extract_summary_from_content(content):
    """Extract summary/description from file content"""
    # Look for Overview section
    overview_match = re.search(r'^## Overview\s*\n\n(.*?)(?=\n##|\n#|$)', content, re.MULTILINE | re.DOTALL)
    if overview_match:
        overview = overview_match.group(1).strip()
        # Get first paragraph
        first_para = overview.split('\n\n')[0].strip()
        if first_para:
            return first_para
    
    # Look for first paragraph after frontmatter
    content_after_fm = re.sub(r'^---.*?---\s*', '', content, flags=re.DOTALL)
    first_para = content_after_fm.strip().split('\n\n')[0] if content_after_fm.strip() else ""
    if first_para and not first_para.startswith('#'):
        return first_para[:200]  # Limit length
    
    return ""


def extract_when_to_retrieve(content):
    """Extract 'When to Retrieve' section"""
    match = re.search(r'\*\*When to Retrieve\*\*:\s*(.*?)(?=\n\*\*|\n##|\n#|$)', content, re.MULTILINE | re.DOTALL)
    if match:
        return match.group(1).strip()
    return ""


def extract_key_topics(content):
    """Extract Key Topics list"""
    match = re.search(r'\*\*Key Topics\*\*:\s*\n((?:- .*\n?)+)', content, re.MULTILINE)
    if match:
        topics = []
        for line in match.group(1).split('\n'):
            if line.strip().startswith('-'):
                topics.append(line.strip()[2:].strip())
        return topics
    return []


def scan_rag_folder(rag_path):
    """Scan rag/ folder and organize files by domain
    
    CRITICAL: This function MUST ensure ALL main folders get cards, even if empty.
    - Scans actual folder structure to find ALL main folders
    - Creates entries for ALL folders in FOLDER_TO_SECTION
    - Ensures every main folder has a card on homepage
    """
    files_by_domain = defaultdict(list)
    
    print("📂 Scanning rag/ folder structure...")
    
    # FIRST: Find ALL main folders that exist (even if empty)
    existing_folders = set()
    for item in rag_path.iterdir():
        if item.is_dir() and not item.name.startswith('.'):
            # Skip meta and other non-content folders
            if item.name not in {'meta', '.git', '__pycache__', 'node_modules'}:
                existing_folders.add(item.name)
    
    # SECOND: Scan for files in each folder
    for md_file in rag_path.rglob('*.md'):
        # Skip excluded files
        if md_file.name in EXCLUDE_FILES:
            continue
        
        # Skip files in meta/ folder (templates, etc.)
        if 'meta/' in str(md_file.relative_to(rag_path)):
            continue
        
        # Get domain from folder structure
        relative_path = md_file.relative_to(rag_path)
        parts = relative_path.parts
        
        if len(parts) == 1:
            # Root level file - skip for now
            continue
        
        domain_folder = parts[0]
        filename = parts[-1]
        
        # Map folder to section
        section_name = FOLDER_TO_SECTION.get(domain_folder)
        if not section_name:
            # Unknown folder - still track it but warn
            if domain_folder not in {'examples', 'meta'}:
                print(f"   ⚠️  Unknown domain folder: {domain_folder} (will not get homepage card)")
            continue
        
        # Read file content
        try:
            content = md_file.read_text(encoding='utf-8')
        except:
            print(f"   ⚠️  Could not read: {relative_path}")
            continue
        
        # Extract metadata
        frontmatter = extract_frontmatter(content)
        title = frontmatter.get('title', filename.replace('.md', '').replace('-', ' ').title())
        summary = extract_summary_from_content(content) or frontmatter.get('description', '')
        when_to_retrieve = extract_when_to_retrieve(content)
        key_topics = extract_key_topics(content)
        
        # Build relative path for link
        link_path = str(relative_path).replace('.md', '.html')
        
        files_by_domain[section_name].append({
            'filename': filename,
            'title': title,
            'link_path': link_path,
            'summary': summary,
            'when_to_retrieve': when_to_retrieve,
            'key_topics': key_topics,
            'full_path': relative_path,
        })
    
    # THIRD: Only include folders that have at least ONE file
    # Rule: Empty folder = NO card. Folder with files = YES card.
    total_files = sum(len(files) for files in files_by_domain.values())
    total_domains = len(files_by_domain)
    
    # Check for folders that exist but have no files
    empty_folders = []
    for folder_name, section_name in FOLDER_TO_SECTION.items():
        if folder_name in existing_folders and section_name not in files_by_domain:
            empty_folders.append(folder_name)
    
    if empty_folders:
        print(f"   ℹ️  Folders with no files (will NOT get homepage cards): {', '.join(empty_folders)}")
    
    print(f"   Found {total_files} files in {total_domains} domains")
    print(f"   ✅ Creating homepage cards for {total_domains} folders with files (empty folders excluded)")
    
    return files_by_domain


def rebuild_rag_library_json(rag_path, files_by_domain):
    """Rebuild rag-library.json from scanned files"""
    print("📝 Rebuilding rag-library.json...")
    
    json_path = rag_path / 'rag-library.json'
    
    # Build directory structure mapping
    directory_structure = {}
    for folder, section in FOLDER_TO_SECTION.items():
        directory_structure[folder] = generate_section_description(section, []).replace(f"{section} patterns and practices.", "").strip()
        if not directory_structure[folder]:
            # Fallback descriptions
            descriptions = {
                "architecture": "System architecture patterns",
                "integrations": "Integration patterns and platforms",
                "identity-sso": "Identity and SSO patterns",
                "data-modeling": "Data modeling patterns",
                "security": "Security and access control patterns",
                "operations": "Delivery & operations patterns",
                "observability": "Observability & resilience patterns",
                "data-governance": "Data governance & compliance patterns",
                "adoption": "Adoption & change management patterns",
                "project-methods": "Project delivery and methodology",
                "development": "Development patterns and practices",
                "troubleshooting": "Debugging and troubleshooting",
                "patterns": "Reusable design patterns",
                "glossary": "Terminology and definitions",
                "code-examples": "Complete, working code examples",
                "testing": "Testing patterns and examples",
                "quick-start": "Quick-start guides",
                "api-reference": "API references and method signatures",
                "mcp-knowledge": "MCP-extracted knowledge",
                "best-practices": "Best practices for Salesforce product evaluation, org edition selection, user license selection, pricing negotiation, org staffing, reporting, and cloud features",
            }
            directory_structure[folder] = descriptions.get(folder, f"{section} patterns and practices")
    
    # Build files array
    files_array = []
    for section_name in sorted(files_by_domain.keys()):
        files = sorted(files_by_domain[section_name], key=lambda x: x['filename'])
        
        # Find folder name for this section
        folder_name = None
        for folder, section in FOLDER_TO_SECTION.items():
            if section == section_name:
                folder_name = folder
                break
        
        if not folder_name:
            continue
        
        for file_info in files:
            # Build whenToRetrieve array
            when_to_retrieve = []
            if file_info['when_to_retrieve']:
                # Split by common delimiters or use as single item
                when_text = file_info['when_to_retrieve']
                # Try to split by newlines or bullets
                if '\n' in when_text or '- ' in when_text:
                    lines = when_text.replace('- ', '').split('\n')
                    when_to_retrieve = [line.strip() for line in lines if line.strip()]
                else:
                    when_to_retrieve = [when_text] if when_text else []
            
            file_entry = {
                "domain": folder_name,
                "file": file_info['filename'],
                "path": f"rag/{file_info['full_path']}",
                "whenToRetrieve": when_to_retrieve,
                "summary": file_info['summary'] or file_info['title'],
                "keyTopics": file_info['key_topics'] or [],
                "status": "completed"
            }
            
            # Add optional fields if they exist
            if file_info.get('title') and file_info['title'] != file_info['filename'].replace('.md', '').replace('-', ' ').title():
                file_entry["title"] = file_info['title']
            
            files_array.append(file_entry)
    
    # Calculate statistics
    total_files = len(files_array)
    completed_files = total_files  # All files are completed
    domains = len(files_by_domain)
    domains_with_files = domains
    
    # Calculate coverage (files per domain)
    coverage = {}
    for folder, section in FOLDER_TO_SECTION.items():
        if section in files_by_domain:
            coverage[folder] = len(files_by_domain[section])
    
    # Build JSON structure
    library_json = {
        "version": "2.0",
        "lastUpdated": datetime.now().strftime("%Y-%m-%d"),
        "description": "RAG Knowledge Library - Structured knowledge derived from real Salesforce implementation experience. All content sanitized and organized for efficient AI retrieval.",
        "directoryStructure": directory_structure,
        "files": files_array,
        "retrievalGuidelines": {
            "whenToUse": [
                "Architecture Questions: Designing system architecture, integration patterns, multi-tenant solutions, or portal architecture",
                "Integration Questions: Implementing ETL, API, or event-driven integrations, SIS synchronization, integration platforms, or Change Data Capture (CDC) patterns",
                "Identity Questions: Implementing SSO, multi-identity provider architectures, or login handlers",
                "Data Modeling Questions: Designing external IDs, integration keys, student lifecycle models, case management models, lead management and conversion patterns, setting up custom objects with fields, layouts, and permissions, choosing file storage mechanisms (ContentVersion, Attachments, Documents), or planning data migrations",
                "Security Questions: Implementing permission set-driven security, managing access control, or securing Salesforce data for LLM systems",
                "Development Questions: Implementing Apex, Flow, LWC, OmniStudio, error handling, logging, troubleshooting patterns, understanding order of execution, choosing between before-save and after-save automation, handling row locking and concurrency, optimizing governor limits and performance, building dynamic SOQL queries, implementing relationship queries, performing org maintenance, implementing asynchronous Apex (Batch, Queueable, Scheduled), or using Custom Settings and Custom Metadata",
                "Operations Questions: Implementing CI/CD, choosing between metadata and source-tracked orgs, using unlocked packages, automating sandbox seeding, implementing deployment validation, planning rollback strategies, designing org topologies, implementing data masking, planning refresh cadences, establishing release governance, or managing Change Advisory Boards",
                "Observability Questions: Implementing monitoring and alerting, monitoring Platform Events, tracking API health, detecting async job failures, implementing log aggregation, optimizing query performance, handling Large Data Volumes, mitigating governor limits, implementing caching, planning backup/restore, implementing failover patterns, or conducting business continuity drills",
                "Data Governance Questions: Handling PII/PHI data, implementing GDPR/CCPA/SOC2 compliance, configuring field-level encryption, implementing Shield best practices, preventing duplicates, configuring survivorship rules, or establishing master data governance",
                "Adoption Questions: Creating training plans, establishing support models, implementing feature adoption telemetry, conducting technical debt triage, performing baseline audits, or creating remediation playbooks",
                "Project Methods Questions: Sprint-based delivery, testing strategies, quality standards, deployment patterns, or Salesforce DX workflows",
                "Troubleshooting Questions: Integration debugging, data reconciliation, common errors, or root cause analysis",
                "Pattern Questions: Looking for reusable patterns or best practices",
                "Code Generation Questions: Need complete, working code examples, implementing specific patterns, or looking for copy-paste ready code",
                "Testing Questions: Writing test classes, creating test data factories, testing patterns, or test coverage strategies",
                "Quick Start Questions: Getting started with Apex, LWC, or other Salesforce technologies",
                "API Reference Questions: Looking up method signatures, API usage, or quick reference for common patterns",
                "MCP Knowledge Questions: Official Salesforce guidance, best practices, or MCP-validated patterns"
            ],
            "howToUse": [
                "Identify Domain: Determine which domain folder contains relevant knowledge",
                "Review Index: Check rag-index.md for file summaries and retrieval guidance",
                "Read Relevant Files: Read files that match the question domain",
                "Cross-Reference: Check related files in other domains when needed",
                "Apply Patterns: Use patterns and best practices from the library"
            ]
        },
        "contentCharacteristics": {
            "evidenceBased": "Derived from real implementation experience",
            "sanitized": "All identifying information removed (company names, client names, project codenames)",
            "patternFocused": "Emphasizes reusable patterns and best practices",
            "decisionOriented": "Includes architectural decisions and tradeoffs",
            "implementationReady": "Provides actionable guidance for implementation"
        },
        "terminology": {
            "ETL": "Extract, Transform, Load - batch data synchronization",
            "SIS": "Student Information System - external system for student data",
            "OIDC": "OpenID Connect - identity provider protocol for external users",
            "SAML": "Security Assertion Markup Language - identity provider protocol for enterprise SSO",
            "Platform Events": "Salesforce event-driven integration mechanism",
            "External ID": "Field marked as external ID for upsert operations",
            "Permission Set": "Salesforce mechanism for granting incremental permissions",
            "Record Type": "Salesforce mechanism for differentiating record types",
            "Experience Cloud": "Salesforce portal/community platform",
            "GovCloud": "Government Cloud - compliant cloud environment",
            "OmniStudio": "Salesforce OmniStudio for guided workflows and reusable UI components",
            "LWC": "Lightning Web Component - modern Salesforce UI component framework",
            "EDA": "Education Data Architecture - Salesforce Education Cloud data model"
        },
        "plannedFiles": [],
        "statistics": {
            "totalFiles": total_files,
            "completedFiles": completed_files,
            "plannedFiles": 0,
            "domains": domains,
            "domainsWithFiles": domains_with_files
        },
        "coverage": coverage
    }
    
    # Write JSON file
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(library_json, f, indent=2, ensure_ascii=False)
    
    print(f"   ✅ Rebuilt rag-library.json with {total_files} files in {domains} domains")


def generate_section_description(section_name, files):
    """Generate section description from files"""
    # Use a generic description based on section name
    descriptions = {
        "Architecture Patterns": "Architecture patterns for designing system structure, integration patterns, multi-tenant solutions, and portal architecture.",
        "Integration Patterns": "Integration patterns and platforms for ETL, API, and event-driven integrations, SIS synchronization, integration platforms like MuleSoft and Dell Boomi, and Salesforce to LLM data pipelines.",
        "Identity and SSO": "Identity and SSO patterns for implementing SSO, multi-identity provider architectures, and login handlers.",
        "Data Modeling": "Data modeling patterns for designing external IDs, integration keys, student lifecycle models, and case management models.",
        "Security": "Security and access control patterns for implementing permission set-driven security, managing access control, securing Salesforce data for LLM systems, and implementing comprehensive sharing mechanisms.",
        "Best Practices": "Best practices for Salesforce product evaluation, org edition selection, user license selection, pricing negotiation, org staffing, reporting, and cloud features.",
        "Development": "Development patterns and practices for implementing Apex, Flow, LWC, OmniStudio, error handling, logging, troubleshooting patterns, concurrency control, and performance optimization.",
        "Troubleshooting": "Debugging and troubleshooting approaches for integration debugging, data reconciliation, common errors, and root cause analysis.",
        "Patterns": "Reusable design patterns that span multiple domains, including governor limit management, bulkification, and cross-cutting design patterns.",
        "Glossary": "Terminology and definitions for clarifying what terms mean and understanding core concepts.",
        "Project Methods": "Project delivery and methodology for sprint-based delivery, testing strategies, and quality standards.",
        "Operations": "Delivery and operations patterns for CI/CD, environment strategy, and release governance.",
        "Observability": "Observability and resilience patterns for monitoring, performance tuning, and high availability.",
        "Data Governance": "Data governance and compliance patterns for data residency, compliance, and data quality.",
        "Adoption": "Adoption and change management patterns for user readiness and org health.",
        "Testing": "Testing patterns and examples for Apex, LWC, and integration testing.",
        "Quick Start Guides": "Step-by-step guides for getting started with Salesforce development.",
        "API Reference": "Quick reference for common APIs, methods, and patterns.",
        "MCP Knowledge": "Knowledge extracted from Salesforce MCP Service tools, providing official guidance and best practices.",
        "Code Examples": "Complete, working code examples organized by category. All examples are copy-paste ready and include tests.",
    }
    return descriptions.get(section_name, f"{section_name} patterns and practices.")


def rebuild_rag_index(rag_path, files_by_domain):
    """Rebuild rag-index.md from scanned files"""
    print("📝 Rebuilding rag-index.md...")
    
    # Read existing index to preserve header sections
    index_path = rag_path / 'rag-index.md'
    existing_content = ""
    if index_path.exists():
        existing_content = index_path.read_text(encoding='utf-8')
    
    # Extract header (everything before first ## section)
    header_match = re.search(r'^(.*?)(?=^## [A-Z])', existing_content, re.MULTILINE | re.DOTALL)
    header = header_match.group(1) if header_match else """# RAG Knowledge Library Index

## Overview

This RAG (Retrieval-Augmented Generation) knowledge library contains structured knowledge derived from real Salesforce implementation experience. All content has been sanitized to remove identifying information and organized for efficient retrieval by AI systems.

## How to use this index

- **LLMs or tools** can use this file to decide which `rag/**` docs to retrieve for a given question.
- **Humans** can skim domains to understand what knowledge is available.
- **See the README** and `examples/` folder for details on using this repository with Cursor and other RAG frameworks.

## Directory Structure

```
rag/
├── architecture/          # System architecture patterns
├── integrations/          # Integration patterns and platforms
├── identity-sso/         # Identity and SSO patterns
├── data-modeling/        # Data modeling patterns
├── security/             # Security and access control patterns
├── operations/            # Delivery & operations patterns
├── observability/         # Observability & resilience patterns
├── data-governance/      # Data governance & compliance patterns
├── adoption/              # Adoption & change management patterns
├── project-methods/      # Project delivery and methodology
├── development/          # Development patterns and practices
├── testing/              # Testing patterns and examples
├── troubleshooting/      # Debugging and troubleshooting
├── patterns/             # Reusable design patterns
├── glossary/             # Terminology and definitions
├── code-examples/        # Complete, working code examples
├── quick-start/          # Quick-start guides
├── api-reference/        # API references and method signatures
├── mcp-knowledge/        # MCP-extracted knowledge
└── rag-index.md          # This file
```

"""
    
    # Build sections
    sections = []
    for section_name in sorted(files_by_domain.keys()):
        files = sorted(files_by_domain[section_name], key=lambda x: x['filename'])
        description = generate_section_description(section_name, files)
        anchor = get_anchor_id(section_name)
        
        section_content = f"## {section_name}\n\n{description}\n\n"
        
        # Add file links
        for file_info in files:
            link_path = file_info['link_path']
            title = file_info['title']
            summary = file_info['summary'] or title
            # Truncate summary if too long
            if len(summary) > 150:
                summary = summary[:147] + "..."
            
            section_content += f"- [{file_info['filename']}]({link_path}) — {summary}\n"
        
        section_content += "\n"
        
        # Add detailed info for each file
        for file_info in files:
            section_content += f"### {file_info['filename']}\n\n"
            
            if file_info['when_to_retrieve']:
                section_content += f"**When to Retrieve**: {file_info['when_to_retrieve']}\n\n"
            
            if file_info['summary']:
                section_content += f"**Summary**: {file_info['summary']}\n\n"
            
            if file_info['key_topics']:
                section_content += "**Key Topics**:\n"
                for topic in file_info['key_topics']:
                    section_content += f"- {topic}\n"
                section_content += "\n"
        
        sections.append(section_content)
    
    # Combine header and sections
    new_index = header + "\n".join(sections)
    
    # Write new index
    index_path.write_text(new_index, encoding='utf-8')
    print(f"   ✅ Rebuilt rag-index.md with {len(files_by_domain)} sections")
    
    return files_by_domain


def extract_sections_from_index(rag_index_path):
    """Extract all sections from rag-index.md"""
    sections = []
    
    with open(rag_index_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find all ## headings
    pattern = r'^## (.+)$'
    for match in re.finditer(pattern, content, re.MULTILINE):
        section_name = match.group(1).strip()
        
        if section_name in EXCLUDE_SECTIONS:
            continue
        
        # Get description (next line after heading)
        lines = content[match.end():].split('\n')
        description = ""
        for line in lines[1:3]:  # Check next 2 lines
            line = line.strip()
            if line and not line.startswith('-') and not line.startswith('#'):
                description = line
                break
        
        sections.append({
            'name': section_name,
            'description': description,
            'anchor': get_anchor_id(section_name)
        })
    
    return sections


def generate_card_html(section):
    """Generate HTML for a domain card"""
    emoji = EMOJI_MAP.get(section['name'], "📄")
    display_name = section['name']
    
    # Handle "Quick Start Guides" -> "Quick Start" for display
    if section['name'] == "Quick Start Guides":
        display_name = "Quick Start"
    
    return f'''  <div class="domain-card">
    <h3><a href="{{{{ '/rag/rag-index.html' | relative_url }}}}#{section['anchor']}">{emoji} {display_name}</a></h3>
    <p>{section['description']}</p>
  </div>'''


def update_homepage(rag_index_path, homepage_path):
    """Update homepage with all categories from rag-index.md
    
    RULE: Only create cards for folders that have at least ONE file.
    Empty folders = NO card. Folders with files = YES card.
    """
    
    print("🏠 Syncing homepage...")
    sections = extract_sections_from_index(rag_index_path)
    print(f"   Found {len(sections)} categories from rag-index.md (only folders with files)")
    
    # Sort sections alphabetically for consistent ordering
    sections.sort(key=lambda x: x['name'])
    
    print(f"   ✅ Creating {len(sections)} homepage cards (one per folder with files)")
    
    # Read homepage
    with open(homepage_path, 'r', encoding='utf-8') as f:
        homepage_content = f.read()
    
    # Find the domain-grid section
    grid_start = homepage_content.find('<div class="domain-grid">')
    if grid_start == -1:
        print("❌ ERROR: Could not find domain-grid section!")
        return False
    
    # LESSON LEARNED: Must count nested divs to find correct closing tag
    # domain-grid contains domain-card divs, so can't just find first </div>
    # Track depth: +1 for <div, -1 for </div, stop when depth == 0
    pos = grid_start
    depth = 0
    grid_end = -1
    while pos < len(homepage_content):
        if homepage_content[pos:pos+4] == '<div':
            depth += 1
            pos = homepage_content.find('>', pos) + 1
        elif homepage_content[pos:pos+6] == '</div>':
            depth -= 1
            if depth == 0:
                grid_end = pos + 6
                break
            pos += 6
        else:
            pos += 1
    
    if grid_end == -1:
        print("❌ ERROR: Could not find closing tag for domain-grid!")
        return False
    
    # Generate all cards
    cards = []
    for section in sections:
        cards.append(generate_card_html(section))
    
    # Replace the grid content - ensure we get the complete replacement
    new_grid = '<div class="domain-grid">\n' + '\n  \n'.join(cards) + '\n</div>'
    
    # Find the next section after the grid (usually "## Quick Links" or similar)
    # This ensures we don't accidentally include duplicate cards
    next_section = homepage_content.find('\n## ', grid_end)
    if next_section == -1:
        # Try without newline
        next_section = homepage_content.find('## ', grid_end)
    
    if next_section == -1:
        # No next section, replace to end of grid
        new_homepage = homepage_content[:grid_start] + new_grid + homepage_content[grid_end:]
    else:
        # Replace up to next section (skip any duplicate cards)
        new_homepage = homepage_content[:grid_start] + new_grid + '\n\n' + homepage_content[next_section:]
    
    # Write updated homepage
    with open(homepage_path, 'w', encoding='utf-8') as f:
        f.write(new_homepage)
    
    # LESSON LEARNED: Verify output structure
    # Check that correct number of cards are in the grid
    card_count = new_homepage[grid_start:grid_start+5000].count('domain-card')
    if card_count != len(sections):
        print(f"   ⚠️  WARNING: Expected {len(sections)} cards, found {card_count}")
    
    print(f"   ✅ Updated homepage with {len(sections)} categories")
    
    return True


def main():
    """Main function"""
    repo_root = Path(__file__).parent.parent.parent
    rag_path = repo_root / 'rag'
    rag_index_path = rag_path / 'rag-index.md'
    homepage_path = repo_root / 'website' / 'root' / 'index.md'
    
    if not rag_path.exists():
        print(f"❌ ERROR: {rag_path} not found!")
        sys.exit(1)
    
    if not homepage_path.exists():
        print(f"❌ ERROR: {homepage_path} not found!")
        sys.exit(1)
    
    print("🚀 Rebuilding rag-index.md, rag-library.json, and syncing homepage...\n")
    
    # Step 1: Scan rag/ folder and rebuild index
    files_by_domain = scan_rag_folder(rag_path)
    
    # Step 2: Rebuild rag-index.md
    rebuild_rag_index(rag_path, files_by_domain)
    
    # Step 3: Rebuild rag-library.json
    rebuild_rag_library_json(rag_path, files_by_domain)
    
    # Step 4: Sync homepage
    update_homepage(rag_index_path, homepage_path)
    
    print("\n✅ Done! rag-index.md, rag-library.json, and homepage are now in sync")
    print("   Run: git add rag/rag-index.md rag/rag-library.json website/root/index.md && git commit -m 'Auto-sync RAG index, library JSON, and homepage'")


if __name__ == '__main__':
    main()
