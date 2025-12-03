#!/usr/bin/env python3
"""
Update Website Script for Salesforce RAG Knowledge Library

This script automatically updates website files when RAG content changes:
- Generates/updates sitemap.xml with all markdown files
- Validates markdown file structure
- Updates metadata if needed
- Prepares site for deployment

Usage:
    python scripts/update-website.py
    python scripts/update-website.py --validate-only
    python scripts/update-website.py --dry-run
"""

import os
import sys
import json
import xml.etree.ElementTree as ET
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Tuple
import argparse

# Configuration
BASE_DIR = Path(__file__).parent.parent
RAG_DIR = BASE_DIR / "rag"
SITEMAP_PATH = BASE_DIR / "sitemap.xml"
SITE_URL = "https://pranavnagrecha.github.io/Salesforce-RAG"
EXCLUDE_DIRS = {"meta", ".git", "__pycache__", "node_modules"}
EXCLUDE_FILES = {"README.md", "CONTRIBUTING.md", "MAINTENANCE.md"}

# Domain descriptions for sitemap priorities
DOMAIN_PRIORITIES = {
    "architecture": 0.9,
    "development": 0.9,
    "integrations": 0.9,
    "code-examples": 0.85,
    "testing": 0.85,
    "security": 0.85,
    "data-modeling": 0.85,
    "operations": 0.8,
    "observability": 0.8,
    "troubleshooting": 0.8,
    "project-methods": 0.8,
    "data-governance": 0.75,
    "adoption": 0.75,
    "quick-start": 0.9,
    "api-reference": 0.85,
    "mcp-knowledge": 0.8,
    "patterns": 0.75,
    "glossary": 0.7,
    "best-practices": 0.85,
}


def find_markdown_files(root_dir: Path, relative_to: Path = None) -> List[Tuple[Path, str]]:
    """
    Find all markdown files in the RAG directory.
    
    Returns:
        List of tuples: (absolute_path, relative_path_string)
    """
    if relative_to is None:
        relative_to = root_dir
    
    markdown_files = []
    
    for file_path in root_dir.rglob("*.md"):
        # Skip excluded directories
        if any(excluded in file_path.parts for excluded in EXCLUDE_DIRS):
            continue
        
        # Skip excluded files
        if file_path.name in EXCLUDE_FILES:
            continue
        
        # Get relative path
        try:
            relative_path = file_path.relative_to(relative_to)
            markdown_files.append((file_path, str(relative_path)))
        except ValueError:
            # File is outside the relative directory
            continue
    
    return sorted(markdown_files, key=lambda x: x[1])


def get_file_metadata(file_path: Path) -> Dict:
    """Extract metadata from markdown file (frontmatter, modification date, etc.)."""
    metadata = {
        "path": file_path,
        "modified": datetime.fromtimestamp(file_path.stat().st_mtime),
        "size": file_path.stat().st_size,
    }
    
    # Try to read frontmatter
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
            
            # Check for YAML frontmatter
            if content.startswith("---"):
                lines = content.split("\n")
                if len(lines) > 1:
                    frontmatter_end = None
                    for i, line in enumerate(lines[1:], 1):
                        if line.strip() == "---":
                            frontmatter_end = i
                            break
                    
                    if frontmatter_end:
                        frontmatter = "\n".join(lines[1:frontmatter_end])
                        # Simple YAML parsing (basic)
                        for line in frontmatter.split("\n"):
                            if ":" in line:
                                key, value = line.split(":", 1)
                                key = key.strip().strip('"\'')
                                value = value.strip().strip('"\'')
                                if key == "title":
                                    metadata["title"] = value
    except Exception as e:
        print(f"Warning: Could not read metadata from {file_path}: {e}", file=sys.stderr)
    
    return metadata


def determine_priority(file_path: str) -> float:
    """Determine sitemap priority based on file path."""
    # Check for index files (highest priority)
    if "index" in file_path.lower() or "rag-index" in file_path.lower():
        return 1.0
    
    # Check domain priorities
    for domain, priority in DOMAIN_PRIORITIES.items():
        if f"/{domain}/" in file_path or file_path.startswith(f"{domain}/"):
            return priority
    
    # Default priority
    return 0.7


def determine_changefreq(file_path: str) -> str:
    """Determine change frequency based on file type."""
    if "index" in file_path.lower():
        return "weekly"
    elif "template" in file_path.lower():
        return "monthly"
    elif "example" in file_path.lower():
        return "monthly"
    else:
        return "monthly"


def generate_sitemap(markdown_files: List[Tuple[Path, str]], output_path: Path) -> None:
    """Generate XML sitemap from markdown files."""
    # Create root element
    urlset = ET.Element("urlset")
    urlset.set("xmlns", "http://www.sitemaps.org/schemas/sitemap/0.9")
    urlset.set("xmlns:xsi", "http://www.w3.org/2001/XMLSchema-instance")
    urlset.set("xsi:schemaLocation", 
               "http://www.sitemaps.org/schemas/sitemap/0.9 "
               "http://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd")
    
    # Add homepage
    home_url = ET.SubElement(urlset, "url")
    ET.SubElement(home_url, "loc").text = f"{SITE_URL}/"
    ET.SubElement(home_url, "lastmod").text = datetime.now().strftime("%Y-%m-%d")
    ET.SubElement(home_url, "changefreq").text = "weekly"
    ET.SubElement(home_url, "priority").text = "1.0"
    
    # Add main index
    index_url = ET.SubElement(urlset, "url")
    ET.SubElement(index_url, "loc").text = f"{SITE_URL}/rag/rag-index.html"
    ET.SubElement(index_url, "lastmod").text = datetime.now().strftime("%Y-%m-%d")
    ET.SubElement(index_url, "changefreq").text = "weekly"
    ET.SubElement(index_url, "priority").text = "0.9"
    
    # Add all markdown files
    for file_path, relative_path in markdown_files:
        metadata = get_file_metadata(file_path)
        
        # Convert .md to .html for URL
        url_path = relative_path.replace(".md", ".html")
        # Handle index files
        if url_path.endswith("index.html"):
            url_path = url_path.replace("/index.html", "/")
        
        url = ET.SubElement(urlset, "url")
        ET.SubElement(url, "loc").text = f"{SITE_URL}/{url_path}"
        ET.SubElement(url, "lastmod").text = metadata["modified"].strftime("%Y-%m-%d")
        ET.SubElement(url, "changefreq").text = determine_changefreq(relative_path)
        ET.SubElement(url, "priority").text = str(determine_priority(relative_path))
    
    # Write XML
    tree = ET.ElementTree(urlset)
    ET.indent(tree, space="  ")
    tree.write(output_path, encoding="utf-8", xml_declaration=True)
    
    print(f"✅ Generated sitemap with {len(markdown_files) + 2} URLs")


def validate_markdown_files(markdown_files: List[Tuple[Path, str]]) -> Tuple[int, List[str]]:
    """Validate markdown files for common issues."""
    errors = []
    warnings = []
    
    for file_path, relative_path in markdown_files:
        # Check file is readable
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
        except Exception as e:
            errors.append(f"Cannot read {relative_path}: {e}")
            continue
        
        # Check for basic structure
        if len(content.strip()) < 100:
            warnings.append(f"{relative_path}: File seems very short (< 100 chars)")
        
        # Check for title/heading
        if not content.startswith("#") and "---" not in content[:100]:
            warnings.append(f"{relative_path}: No H1 heading or frontmatter found")
        
        # Check for empty file
        if not content.strip():
            errors.append(f"{relative_path}: File is empty")
    
    return len(errors), errors + warnings


def print_summary(markdown_files: List[Tuple[Path, str]]) -> None:
    """Print summary of files found."""
    print("\n" + "="*60)
    print("RAG Content Summary")
    print("="*60)
    
    # Count by domain
    domain_counts = {}
    for _, relative_path in markdown_files:
        domain = relative_path.split("/")[0] if "/" in relative_path else "root"
        domain_counts[domain] = domain_counts.get(domain, 0) + 1
    
    print(f"\nTotal markdown files: {len(markdown_files)}")
    print("\nFiles by domain:")
    for domain, count in sorted(domain_counts.items()):
        print(f"  {domain:20s}: {count:3d} files")
    
    print("\n" + "="*60)


def main():
    parser = argparse.ArgumentParser(
        description="Update website files for Salesforce RAG Knowledge Library"
    )
    parser.add_argument(
        "--validate-only",
        action="store_true",
        help="Only validate files, don't update sitemap"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be done without making changes"
    )
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Verbose output"
    )
    
    args = parser.parse_args()
    
    print("🔍 Scanning RAG directory...")
    
    # Find all markdown files
    markdown_files = find_markdown_files(RAG_DIR, BASE_DIR)
    
    if not markdown_files:
        print("❌ No markdown files found in rag/ directory!")
        sys.exit(1)
    
    # Print summary
    if args.verbose or not args.validate_only:
        print_summary(markdown_files)
    
    # Validate files
    print("\n🔍 Validating markdown files...")
    error_count, issues = validate_markdown_files(markdown_files)
    
    if issues:
        print(f"\n⚠️  Found {len(issues)} issues:")
        for issue in issues[:10]:  # Show first 10
            print(f"  - {issue}")
        if len(issues) > 10:
            print(f"  ... and {len(issues) - 10} more")
    
    if error_count > 0:
        print(f"\n❌ Found {error_count} errors. Please fix before deploying.")
        if not args.validate_only:
            sys.exit(1)
    
    if args.validate_only:
        print("\n✅ Validation complete!")
        sys.exit(0)
    
    # Generate sitemap
    if not args.dry_run:
        print("\n📝 Generating sitemap.xml...")
        generate_sitemap(markdown_files, SITEMAP_PATH)
        print(f"✅ Sitemap saved to: {SITEMAP_PATH}")
    else:
        print("\n🔍 [DRY RUN] Would generate sitemap with:")
        print(f"  - Homepage")
        print(f"  - Index page")
        print(f"  - {len(markdown_files)} markdown files")
    
    print("\n✅ Website update complete!")
    print("\nNext steps:")
    print("  1. Review the changes")
    print("  2. Commit: git add sitemap.xml")
    print("  3. Push: git push origin main")
    print("  4. GitHub Pages will automatically rebuild")


if __name__ == "__main__":
    main()

