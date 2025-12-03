#!/usr/bin/env python3
"""
Automatically rebuild rag-index.md from rag/ folder and sync homepage

This script:
1. Scans rag/ folder structure for all .md files
2. Reads each file to extract metadata (title, description, etc.)
3. Rebuilds rag-index.md with all files organized by domain
4. Rebuilds rag-library.json with all file metadata and statistics
5. Auto-generates homepage (website/root/index.md) with category cards
6. Ensures all links work correctly

Just run: python website/scripts/sync-homepage.py

IMPORTANT: See website/docs/LESSONS-LEARNED.md for critical lessons and best practices
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
}

# Files to exclude
EXCLUDE_FILES = {
    "README.md",
    "CONTRIBUTING.md",
    "MAINTENANCE.md",
    "rag-index.md",
    "rag-library.json",
    "index.md",
}

# Get project root (script is in website/scripts/, so parent.parent.parent = repo root)
BASE_DIR = Path(__file__).parent.parent.parent
RAG_DIR = BASE_DIR / "rag"
INDEX_PATH = RAG_DIR / "rag-index.md"
LIBRARY_PATH = RAG_DIR / "rag-library.json"
HOMEPAGE_PATH = BASE_DIR / "website" / "root" / "index.md"


def extract_frontmatter(content):
    """Extract YAML frontmatter from markdown file."""
    frontmatter = {}
    if content.startswith("---"):
        try:
            parts = content.split("---", 2)
            if len(parts) >= 3:
                frontmatter = yaml.safe_load(parts[1]) or {}
        except Exception:
            pass
    return frontmatter


def extract_title(content, filename):
    """Extract title from frontmatter or first heading."""
    frontmatter = extract_frontmatter(content)
    if frontmatter.get("title"):
        return frontmatter["title"]
    
    # Try first H1 or H2
    h1_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
    if h1_match:
        return h1_match.group(1).strip()
    
    h2_match = re.search(r'^##\s+(.+)$', content, re.MULTILINE)
    if h2_match:
        return h2_match.group(1).strip()
    
    # Fallback to filename
    return filename.replace(".md", "").replace("-", " ").replace("_", " ").title()


def extract_description(content, title):
    """Extract description from frontmatter, Overview section, or first paragraph."""
    frontmatter = extract_frontmatter(content)
    if frontmatter.get("description"):
        return frontmatter["description"]
    
    # Try Overview section
    overview_match = re.search(
        r'(?:^##\s+Overview\s*$|^###\s+Overview\s*$)(.*?)(?=^##|\Z)',
        content,
        re.MULTILINE | re.DOTALL
    )
    if overview_match:
        overview_text = overview_match.group(1).strip()
        # Get first paragraph
        first_para = re.split(r'\n\n+', overview_text)[0].strip()
        if first_para and len(first_para) > 20:
            return first_para[:300]  # Limit length
    
    # Try first paragraph after title
    content_after_title = re.sub(r'^#+\s+.*?\n', '', content, count=1)
    first_para = re.search(r'^([^\n]+(?:\n[^\n]+)*)', content_after_title, re.MULTILINE)
    if first_para:
        para = first_para.group(1).strip()
        if para and len(para) > 20 and not para.startswith("#"):
            return para[:300]
    
    # Fallback
    return f"Documentation for {title}"


def find_markdown_files():
    """Find all markdown files in rag/ directory, organized by folder."""
    files_by_folder = defaultdict(list)
    
    for file_path in RAG_DIR.rglob("*.md"):
        # Skip excluded files
        if file_path.name in EXCLUDE_FILES:
            continue
        
        # Get relative path from rag/
        try:
            rel_path = file_path.relative_to(RAG_DIR)
        except ValueError:
            continue
        
        # Get folder (first part of path)
        parts = rel_path.parts
        if len(parts) > 1:
            folder = parts[0]
        else:
            folder = "root"
        
        # Read file content
        try:
            content = file_path.read_text(encoding='utf-8')
        except Exception as e:
            print(f"Warning: Could not read {file_path}: {e}", file=sys.stderr)
            continue
        
        # Extract metadata
        title = extract_title(content, file_path.name)
        description = extract_description(content, title)
        frontmatter = extract_frontmatter(content)
        
        # Get permalink from frontmatter if available, otherwise construct from path
        if frontmatter and "permalink" in frontmatter:
            # Use permalink from frontmatter (e.g., "/rag/code-examples/flow/record-triggered-examples.html")
            # Keep absolute path starting with /rag/ for search.js compatibility
            # search.js will prepend /Salesforce-RAG to /rag/ paths, resulting in /Salesforce-RAG/rag/...
            url = frontmatter["permalink"]
            # Ensure it starts with /rag/ (absolute path)
            if not url.startswith("/rag/"):
                # If permalink doesn't start with /rag/, construct it
                url_path = str(rel_path).replace("\\", "/").replace(".md", ".html")
                url = f"/rag/{url_path}"
        else:
            # Build URL path (convert .md to .html, use forward slashes)
            url_path = str(rel_path).replace("\\", "/").replace(".md", ".html")
            
            # Use absolute path starting with /rag/ for search.js compatibility
            # search.js will prepend /Salesforce-RAG to /rag/ paths
            url = f"/rag/{url_path}"
        
        file_info = {
            "path": str(rel_path),
            "filename": file_path.name,
            "folder": folder,
            "title": title,
            "description": description,
            "url": url,  # Use permalink from frontmatter if available, otherwise relative path
            "modified": datetime.fromtimestamp(file_path.stat().st_mtime).isoformat(),
            "size": file_path.stat().st_size,
        }
        
        files_by_folder[folder].append(file_info)
    
    return files_by_folder


def build_rag_index(files_by_folder):
    """Build rag-index.md content."""
    lines = [
        "---\n",
        "layout: default\n",
        "title: RAG Knowledge Library Index\n",
        "description: Complete index of all knowledge files organized by domain.\n",
        "permalink: /rag/rag-index.html\n",
        "---\n\n",
        "# RAG Knowledge Library Index\n"
    ]
    
    # Sort folders by section name
    sorted_folders = sorted(
        files_by_folder.keys(),
        key=lambda f: FOLDER_TO_SECTION.get(f, f).lower()
    )
    
    for folder in sorted_folders:
        if folder == "root":
            continue
        
        section_name = FOLDER_TO_SECTION.get(folder, folder.replace("-", " ").title())
        files = sorted(files_by_folder[folder], key=lambda f: f["filename"].lower())
        
        if not files:
            continue
        
        # Section header
        lines.append(f"## {section_name}\n\n")
        
        # Section description - always use the predefined descriptions
        desc_map = {
            "API Reference": "Quick reference for common APIs, methods, and patterns.",
            "Adoption": "Adoption and change management patterns for user readiness and org health.",
            "Architecture Patterns": "Architecture patterns for designing system structure, integration patterns, multi-tenant solutions, and portal architecture.",
            "Best Practices": "Best practices for Salesforce product evaluation, org edition selection, user license selection, pricing negotiation, org staffing, reporting, and cloud features.",
            "Code Examples": "Complete, working code examples organized by category. All examples are copy-paste ready and include tests.",
            "Data Governance": "Data governance and compliance patterns for data residency, compliance, and data quality.",
            "Data Modeling": "Data modeling patterns for designing external IDs, integration keys, student lifecycle models, and case management models.",
            "Development": "Development patterns and practices for implementing Apex, Flow, LWC, OmniStudio, error handling, logging, troubleshooting patterns, concurrency control, and performance optimization.",
            "Glossary": "Terminology and definitions for clarifying what terms mean and understanding core concepts.",
            "Identity and SSO": "Identity and SSO patterns for implementing SSO, multi-identity provider architectures, and login handlers.",
            "Integration Patterns": "Integration patterns and platforms for ETL, API, and event-driven integrations, SIS synchronization, integration platforms like MuleSoft and Dell Boomi, and Salesforce to LLM data pipelines.",
            "MCP Knowledge": "Knowledge extracted from Salesforce MCP Service tools, providing official guidance and best practices.",
            "Observability": "Observability and resilience patterns for monitoring, performance tuning, and high availability.",
            "Operations": "Delivery and operations patterns for CI/CD, environment strategy, and release governance.",
            "Patterns": "Reusable design patterns that span multiple domains, including governor limit management, bulkification, and cross-cutting design patterns.",
            "Project Methods": "Project delivery and methodology for sprint-based delivery, testing strategies, and quality standards.",
            "Quick Start Guides": "Step-by-step guides for getting started with Salesforce development.",
            "Security": "Security and access control patterns for implementing permission set-driven security, managing access control, securing Salesforce data for LLM systems, and implementing comprehensive sharing mechanisms.",
            "Testing": "Testing patterns and examples for Apex, LWC, and integration testing.",
            "Troubleshooting": "Debugging and troubleshooting approaches for integration debugging, data reconciliation, common errors, and root cause analysis.",
        }
        desc = desc_map.get(section_name, f"{section_name} documentation and patterns.")
        
        lines.append(f"{desc}\n\n")
        
        # File summaries with links
        for file_info in files:
            filename = file_info["filename"]
            url = file_info["url"]
            description = file_info["description"]
            # Build absolute path for Jekyll relative_url filter
            # url is already an absolute path starting with /rag/ (from find_markdown_files)
            # Just use it directly, ensuring it starts with /rag/
            if url.startswith("/rag/"):
                absolute_path = url
            elif url.startswith("/"):
                # Already absolute but wrong prefix, fix it
                absolute_path = f"/rag{url}"
            else:
                # Relative path, prepend /rag/
                absolute_path = f"/rag/{url}"
            
            # Use HTML link with Jekyll relative_url filter in the header
            lines.append(f"### {filename}\n\n")
            lines.append(f"<a href=\"{{{{ '{absolute_path}' | relative_url }}}}\">View {filename}</a>\n\n")
            lines.append(f"**Summary**: {description}\n\n")
        
        lines.append("\n")
    
    return "".join(lines)


def build_rag_library(files_by_folder):
    """Build rag-library.json content."""
    all_files = []
    for folder, files in files_by_folder.items():
        all_files.extend(files)
    
    # Calculate statistics
    stats = {
        "total_files": len(all_files),
        "total_folders": len([f for f in files_by_folder.keys() if f != "root"]),
        "last_updated": datetime.now().isoformat(),
    }
    
    # Group by folder for statistics
    folder_stats = {}
    for folder, files in files_by_folder.items():
        if folder != "root":
            folder_stats[folder] = len(files)
    
    return {
        "metadata": {
            "title": "Salesforce RAG Knowledge Library",
            "description": "A comprehensive knowledge library containing implementation patterns, best practices, and architectural guidance.",
            "version": "1.0",
            "last_updated": stats["last_updated"],
        },
        "statistics": stats,
        "folder_statistics": folder_stats,
        "files": sorted(all_files, key=lambda f: f["path"]),
    }


def build_homepage(files_by_folder):
    """Build homepage with category cards."""
    lines = [
        "---\n",
        "layout: default\n",
        "title: Salesforce RAG Knowledge Library\n",
        "description: A comprehensive knowledge library containing implementation patterns, best practices, and architectural guidance derived from real Salesforce implementation experience. Organized for efficient retrieval by AI systems and human developers.\n",
        "permalink: /\n",
        "---\n\n",
        "# Salesforce RAG Knowledge Library\n\n",
        '<div class="intro">\n',
        '  <p class="lead">A comprehensive knowledge library of Salesforce implementation patterns, best practices, and architectural guidance. All content derived from real implementation experience.</p>\n',
        "</div>\n\n",
        "## Browse by Category\n\n",
        '<div class="domain-grid">\n',
    ]
    
    # Sort folders by section name, only include folders with files
    sorted_folders = sorted(
        [f for f in files_by_folder.keys() if f != "root" and files_by_folder[f]],
        key=lambda f: FOLDER_TO_SECTION.get(f, f).lower()
    )
    
    # Section descriptions (must match rag-index.md)
    section_descriptions = {
        "API Reference": "Quick reference for common APIs, methods, and patterns.",
        "Adoption": "Adoption and change management patterns for user readiness and org health.",
        "Architecture Patterns": "Architecture patterns for designing system structure, integration patterns, multi-tenant solutions, and portal architecture.",
        "Best Practices": "Best practices for Salesforce product evaluation, org edition selection, user license selection, pricing negotiation, org staffing, reporting, and cloud features.",
        "Code Examples": "Complete, working code examples organized by category. All examples are copy-paste ready and include tests.",
        "Data Governance": "Data governance and compliance patterns for data residency, compliance, and data quality.",
        "Data Modeling": "Data modeling patterns for designing external IDs, integration keys, student lifecycle models, and case management models.",
        "Development": "Development patterns and practices for implementing Apex, Flow, LWC, OmniStudio, error handling, logging, troubleshooting patterns, concurrency control, and performance optimization.",
        "Glossary": "Terminology and definitions for clarifying what terms mean and understanding core concepts.",
        "Identity and SSO": "Identity and SSO patterns for implementing SSO, multi-identity provider architectures, and login handlers.",
        "Integration Patterns": "Integration patterns and platforms for ETL, API, and event-driven integrations, SIS synchronization, integration platforms like MuleSoft and Dell Boomi, and Salesforce to LLM data pipelines.",
        "MCP Knowledge": "Knowledge extracted from Salesforce MCP Service tools, providing official guidance and best practices.",
        "Observability": "Observability and resilience patterns for monitoring, performance tuning, and high availability.",
        "Operations": "Delivery and operations patterns for CI/CD, environment strategy, and release governance.",
        "Patterns": "Reusable design patterns that span multiple domains, including governor limit management, bulkification, and cross-cutting design patterns.",
        "Project Methods": "Project delivery and methodology for sprint-based delivery, testing strategies, and quality standards.",
        "Quick Start Guides": "Step-by-step guides for getting started with Salesforce development.",
        "Security": "Security and access control patterns for implementing permission set-driven security, managing access control, securing Salesforce data for LLM systems, and implementing comprehensive sharing mechanisms.",
        "Testing": "Testing patterns and examples for Apex, LWC, and integration testing.",
        "Troubleshooting": "Debugging and troubleshooting approaches for integration debugging, data reconciliation, common errors, and root cause analysis.",
    }
    
    for folder in sorted_folders:
        section_name = FOLDER_TO_SECTION.get(folder, folder.replace("-", " ").title())
        emoji = EMOJI_MAP.get(section_name, "📄")
        description = section_descriptions.get(section_name, f"{section_name} documentation and patterns.")
        anchor = section_name.lower().replace(" ", "-")
        
        lines.append('  <div class="domain-card">\n')
        lines.append(f'    <h3><a href="{{{{ \'/rag/rag-index.html\' | relative_url }}}}#{anchor}">{emoji} {section_name}</a></h3>\n')
        lines.append(f'    <p>{description}</p>\n')
        lines.append('  </div>\n')
        lines.append('\n')
    
    lines.append("</div>\n\n\n")
    
    # Quick Links section
    lines.append("## Quick Links\n\n")
    lines.append("- 📖 **[Complete Index]({{ '/rag/rag-index.html' | relative_url }})** - Browse all knowledge files by domain\n")
    lines.append("- 📋 **[JSON Metadata]({{ '/rag/rag-library.json' | relative_url }})** - Machine-readable metadata for RAG systems\n")
    lines.append("- 💡 **[Code Examples]({{ '/rag/code-examples/code-examples-index.html' | relative_url }})** - Complete, working code examples ready to copy and use\n")
    lines.append("- 🔍 **[Search the Knowledge Base]({{ '/rag/rag-index.html' | relative_url }})** - Find specific patterns and best practices\n\n")
    
    # About section
    total_files = sum(len(files) for files in files_by_folder.values())
    lines.append("## About This Library\n\n")
    lines.append(f"This knowledge library contains **{total_files}+ files** covering:\n\n")
    lines.append("- ✅ **Implementation patterns** from real Salesforce projects\n")
    lines.append("- ✅ **Best practices** for development, architecture, and operations\n")
    lines.append("- ✅ **Code examples** ready to copy and use\n")
    lines.append("- ✅ **Decision frameworks** for common scenarios\n")
    lines.append("- ✅ **Troubleshooting guides** for common issues\n\n")
    lines.append("All content is **sanitized** (no identifying information) and **pattern-focused** for reuse across implementations.\n\n")
    lines.append("---\n\n")
    lines.append('<div class="footer-note">\n')
    lines.append('  <p><strong>Last Updated:</strong> {{ site.time | date: "%B %Y" }}</p>\n')
    lines.append('  <p>This knowledge library is continuously updated with new patterns and best practices from real Salesforce implementations.</p>\n')
    lines.append("</div>\n")
    
    return "".join(lines)


def main():
    """Main function."""
    print("Scanning rag/ folder for markdown files...")
    files_by_folder = find_markdown_files()
    
    print(f"Found {sum(len(files) for files in files_by_folder.values())} files in {len(files_by_folder)} folders")
    
    print("Building rag-index.md...")
    index_content = build_rag_index(files_by_folder)
    # Ensure directory exists before writing
    INDEX_PATH.parent.mkdir(parents=True, exist_ok=True)
    INDEX_PATH.write_text(index_content, encoding='utf-8')
    print(f"✓ Wrote {INDEX_PATH}")
    
    print("Building rag-library.json...")
    library_data = build_rag_library(files_by_folder)
    # Ensure directory exists before writing
    LIBRARY_PATH.parent.mkdir(parents=True, exist_ok=True)
    LIBRARY_PATH.write_text(json.dumps(library_data, indent=2, ensure_ascii=False), encoding='utf-8')
    print(f"✓ Wrote {LIBRARY_PATH}")
    
    print("Building homepage...")
    homepage_content = build_homepage(files_by_folder)
    # Ensure directory exists before writing
    HOMEPAGE_PATH.parent.mkdir(parents=True, exist_ok=True)
    HOMEPAGE_PATH.write_text(homepage_content, encoding='utf-8')
    print(f"✓ Wrote {HOMEPAGE_PATH}")
    
    print("\n✅ Sync complete!")
    print(f"  - {INDEX_PATH.name}: {len(index_content)} characters")
    print(f"  - {LIBRARY_PATH.name}: {library_data['statistics']['total_files']} files")
    print(f"  - {HOMEPAGE_PATH.name}: {len(homepage_content)} characters")


if __name__ == "__main__":
    main()

