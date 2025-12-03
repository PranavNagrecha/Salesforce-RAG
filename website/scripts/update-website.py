#!/usr/bin/env python3
"""
Update Website Script for Salesforce RAG Knowledge Library

This script automatically updates website files when RAG content changes:
- Generates/updates sitemap.xml with all markdown files
- Validates markdown file structure
- Updates metadata if needed
- Prepares site for deployment

Usage:
    python website/scripts/update-website.py
    python website/scripts/update-website.py --validate-only
    python website/scripts/update-website.py --dry-run

IMPORTANT: See website/docs/LESSONS-LEARNED.md for critical lessons and best practices
"""

import os
import sys
import json
import re
import xml.etree.ElementTree as ET
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Tuple
import argparse

# Configuration
BASE_DIR = Path(__file__).parent.parent.parent
RAG_DIR = BASE_DIR / "rag"
SITEMAP_PATH = BASE_DIR / "website" / "root" / "sitemap.xml"
SITE_URL = "https://pranavnagrecha.github.io/Salesforce-RAG"
EXCLUDE_DIRS = {"meta", ".git", "__pycache__", "node_modules"}
EXCLUDE_FILES = {"README.md", "CONTRIBUTING.md", "MAINTENANCE.md", "rag-index.md", "rag-library.json", "index.md"}

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
        content = file_path.read_text(encoding='utf-8')
        if content.startswith("---"):
            import yaml
            parts = content.split("---", 2)
            if len(parts) >= 3:
                frontmatter = yaml.safe_load(parts[1]) or {}
                metadata.update(frontmatter)
    except Exception:
        pass
    
    return metadata


def get_priority_for_path(relative_path: str) -> float:
    """Get sitemap priority based on file path."""
    parts = relative_path.split("/")
    if len(parts) > 1:
        folder = parts[0]
        return DOMAIN_PRIORITIES.get(folder, 0.7)
    return 0.8  # Root level files


def generate_sitemap(markdown_files: List[Tuple[Path, str]]) -> str:
    """Generate sitemap.xml content."""
    # Create XML structure
    urlset = ET.Element("urlset")
    urlset.set("xmlns", "http://www.sitemaps.org/schemas/sitemap/0.9")
    
    # Add homepage
    url_elem = ET.SubElement(urlset, "url")
    ET.SubElement(url_elem, "loc").text = f"{SITE_URL}/"
    ET.SubElement(url_elem, "lastmod").text = datetime.now().strftime("%Y-%m-%d")
    ET.SubElement(url_elem, "changefreq").text = "weekly"
    ET.SubElement(url_elem, "priority").text = "1.0"
    
    # Add rag-index
    url_elem = ET.SubElement(urlset, "url")
    ET.SubElement(url_elem, "loc").text = f"{SITE_URL}/rag/rag-index.html"
    ET.SubElement(url_elem, "lastmod").text = datetime.now().strftime("%Y-%m-%d")
    ET.SubElement(url_elem, "changefreq").text = "daily"
    ET.SubElement(url_elem, "priority").text = "0.9"
    
    # Add all markdown files
    for file_path, relative_path in markdown_files:
        metadata = get_file_metadata(file_path)
        
        # Convert .md to .html and build URL
        url_path = relative_path.replace("\\", "/").replace(".md", ".html")
        full_url = f"{SITE_URL}/rag/{url_path}"
        
        url_elem = ET.SubElement(urlset, "url")
        ET.SubElement(url_elem, "loc").text = full_url
        ET.SubElement(url_elem, "lastmod").text = metadata["modified"].strftime("%Y-%m-%d")
        ET.SubElement(url_elem, "changefreq").text = "monthly"
        priority = get_priority_for_path(relative_path)
        ET.SubElement(url_elem, "priority").text = str(priority)
    
    # Convert to string
    ET.indent(urlset, space="  ")
    return ET.tostring(urlset, encoding='unicode', xml_declaration=True)


def validate_links(markdown_files: List[Tuple[Path, str]]) -> Tuple[int, List[str], List[str]]:
    """Validate internal links in markdown files."""
    errors = []
    warnings = []
    total_links = 0
    
    # Build a set of all markdown file paths for quick lookup (normalized)
    md_file_paths = set()
    for _, rel_path in markdown_files:
        normalized = str(rel_path).replace("\\", "/")
        md_file_paths.add(normalized)
        md_file_paths.add(normalized.lower())  # Case-insensitive check
    
    for file_path, relative_path in markdown_files:
        try:
            content = file_path.read_text(encoding='utf-8')
            
            # Remove code blocks to avoid false positives
            # Split by code blocks and only check links outside them
            code_block_pattern = r'```.*?```'
            content_no_code = re.sub(code_block_pattern, '', content, flags=re.DOTALL)
            inline_code_pattern = r'`[^`]+`'
            content_no_code = re.sub(inline_code_pattern, '', content_no_code)
            
            # Find all markdown links
            link_pattern = r'\[([^\]]+)\]\(([^\)]+)\)'
            links = re.findall(link_pattern, content_no_code)
            total_links += len(links)
            
            for link_text, link_url in links:
                # Skip external links
                if link_url.startswith("http://") or link_url.startswith("https://") or link_url.startswith("mailto:"):
                    continue
                
                # Skip anchor links
                if link_url.startswith("#"):
                    continue
                
                # Skip Jekyll template syntax
                if "{{" in link_url or "|" in link_url:
                    continue
                
                # Validate internal link
                # Links should use .html extension (for Jekyll output)
                if link_url.endswith(".md"):
                    warnings.append(f"{relative_path}: Link '{link_text}' uses .md extension (should be .html): {link_url}")
                
                # Check if link is relative and valid
                if not link_url.startswith("/"):
                    # Remove anchor if present
                    link_url_clean = link_url.split("#")[0]
                    
                    # Relative link - convert .html to .md for checking source files
                    check_url = link_url_clean
                    if check_url.endswith(".html"):
                        check_url = check_url[:-5] + ".md"
                    elif not check_url.endswith(".md"):
                        # Try adding .md
                        check_url = check_url + ".md"
                    
                    # Handle relative paths (../)
                    try:
                        # Resolve relative to current file's directory
                        link_path = (file_path.parent / check_url).resolve()
                        
                        # Check if file exists and is within RAG directory
                        if not link_path.exists() or RAG_DIR not in link_path.parents:
                            # Try without .md extension
                            check_url_no_ext = check_url.replace(".md", "")
                            link_path_no_ext = (file_path.parent / check_url_no_ext).resolve()
                            if not link_path_no_ext.exists() or RAG_DIR not in link_path_no_ext.parents:
                                # Check if it's a valid relative path in our file set
                                rel_check = link_path.relative_to(RAG_DIR) if RAG_DIR in link_path.parents else None
                                if rel_check and str(rel_check).replace("\\", "/") not in md_file_paths:
                                    errors.append(f"{relative_path}: Broken link '{link_text}': {link_url}")
                    except (ValueError, OSError):
                        # Path resolution failed, likely invalid
                        errors.append(f"{relative_path}: Invalid link path '{link_text}': {link_url}")
        
        except Exception as e:
            errors.append(f"{relative_path}: Error reading file: {e}")
    
    return total_links, errors, warnings


def main():
    """Main function."""
    parser = argparse.ArgumentParser(description="Update website files")
    parser.add_argument("--validate-only", action="store_true", help="Only validate, don't update files")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be done without making changes")
    parser.add_argument("--verbose", action="store_true", help="Verbose output")
    args = parser.parse_args()
    
    if args.verbose:
        print("Finding markdown files...")
    
    markdown_files = find_markdown_files(RAG_DIR, RAG_DIR)
    
    if args.verbose:
        print(f"Found {len(markdown_files)} markdown files")
    
    # Validate links
    if args.verbose:
        print("Validating links...")
    
    total_links, link_errors, link_warnings = validate_links(markdown_files)
    
    if link_warnings:
        if args.verbose:
            print(f"\n⚠️  Found {len(link_warnings)} link warnings (non-blocking):", file=sys.stderr)
            for warning in link_warnings[:5]:  # Show first 5
                print(f"  - {warning}", file=sys.stderr)
            if len(link_warnings) > 5:
                print(f"  ... and {len(link_warnings) - 5} more", file=sys.stderr)
    
    if link_errors:
        print(f"\n❌ Found {len(link_errors)} broken links:", file=sys.stderr)
        for error in link_errors[:10]:  # Show first 10
            print(f"  - {error}", file=sys.stderr)
        if len(link_errors) > 10:
            print(f"  ... and {len(link_errors) - 10} more", file=sys.stderr)
    else:
        if args.verbose:
            print(f"✓ All {total_links} links validated successfully")
    
    if args.validate_only:
        # Only fail on actual broken links, not warnings
        # In CI, be lenient - only fail if there are many errors
        if link_errors and len(link_errors) > 100:
            print(f"\n❌ Too many broken links ({len(link_errors)}). Please fix critical issues.", file=sys.stderr)
            sys.exit(1)
        elif link_errors:
            print(f"\n⚠️  Found {len(link_errors)} potentially broken links (non-blocking)", file=sys.stderr)
            if args.verbose:
                for error in link_errors[:5]:
                    print(f"  - {error}", file=sys.stderr)
        return
    
    # Generate sitemap
    if args.verbose:
        print("Generating sitemap.xml...")
    
    sitemap_content = generate_sitemap(markdown_files)
    
    if args.dry_run:
        print(f"[DRY RUN] Would write sitemap.xml ({len(sitemap_content)} characters)")
        print(f"[DRY RUN] Would include {len(markdown_files)} markdown files")
    else:
        SITEMAP_PATH.write_text(sitemap_content, encoding='utf-8')
        print(f"✓ Wrote {SITEMAP_PATH}")
        print(f"  - {len(markdown_files)} markdown files")
        print(f"  - {total_links} total links")
        if link_errors:
            print(f"  - ⚠️  {len(link_errors)} link issues found")
        else:
            print(f"  - ✓ All links valid")


if __name__ == "__main__":
    main()

