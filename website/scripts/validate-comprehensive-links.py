#!/usr/bin/env python3
"""
Comprehensive link validation script.
Validates all discovered links against multiple criteria.
"""

import json
import re
from pathlib import Path
import sys
from collections import defaultdict
from typing import Dict, List, Any, Tuple
import urllib.parse

RAG_DIR = Path("rag")
DISCOVERY_FILE = Path("website/docs/link-discovery.json")
VALIDATION_FILE = Path("website/docs/link-validation.json")

# Files that exist in development/ folder
DEVELOPMENT_FILES = {
    "apex-patterns.md", "soql-query-patterns.md", "governor-limits-and-optimization.md",
    "error-handling-and-logging.md", "flow-patterns.md", "lwc-patterns.md",
    "asynchronous-apex-patterns.md", "custom-settings-metadata-patterns.md",
    "locking-and-concurrency-strategies.md", "order-of-execution.md",
    "large-data-loads.md", "admin-basics.md", "email-management.md",
    "formulas-validation-rules.md", "lightning-app-builder.md", "omnistudio-patterns.md",
}


def build_file_index() -> Dict[str, Path]:
    """Build index of all markdown files by their path."""
    file_index = {}
    for md_file in RAG_DIR.rglob("*.md"):
        if md_file.name == "rag-index.md":
            continue
        try:
            rel_path = md_file.relative_to(RAG_DIR)
            normalized = str(rel_path).replace("\\", "/")
            file_index[normalized] = md_file
            file_index[normalized.lower()] = md_file  # Case-insensitive
        except ValueError:
            continue
    return file_index


def validate_internal_html_link(link: Dict[str, Any], file_index: Dict[str, Path], 
                                source_file: Path) -> List[Dict[str, Any]]:
    """Validate internal HTML link with relative_url filter."""
    issues = []
    url = link["url"]
    
    # Check format
    if not url.startswith("/rag/"):
        issues.append({
            "severity": "error",
            "type": "format",
            "message": f"Path does not start with /rag/: {url}"
        })
        return issues
    
    # Convert .html to .md for file lookup
    if url.endswith(".html"):
        md_path = url[:-5] + ".md"
    elif url.endswith(".md"):
        issues.append({
            "severity": "warning",
            "type": "format",
            "message": f"Link uses .md extension, should use .html: {url}"
        })
        md_path = url
    else:
        md_path = url + ".md"
    
    # Extract relative path from /rag/
    rel_path = md_path.replace("/rag/", "")
    
    # Check for duplicate directory patterns
    parts = rel_path.split("/")
    for i in range(len(parts) - 1):
        if i + 1 < len(parts) and parts[i] == parts[i + 1]:
            issues.append({
                "severity": "error",
                "type": "path",
                "message": f"Duplicate directory pattern: {url}",
                "suggestion": f"/rag/{'/'.join(parts[:i+1] + parts[i+2:])}"
            })
    
    # Check if file exists
    if rel_path in file_index:
        target_file = file_index[rel_path]
        # Check if it's a development file in wrong location
        filename = Path(rel_path).name
        if filename in DEVELOPMENT_FILES:
            expected_path = f"development/{filename}"
            if rel_path != expected_path:
                issues.append({
                    "severity": "error",
                    "type": "path",
                    "message": f"Development file in wrong location: {url}",
                    "suggestion": f"/rag/{expected_path.replace('.md', '.html')}"
                })
    elif rel_path.lower() in file_index:
        issues.append({
            "severity": "warning",
            "type": "case",
            "message": f"Case mismatch: {url} (found: {file_index[rel_path.lower()]})"
        })
    else:
        issues.append({
            "severity": "error",
            "type": "broken",
            "message": f"Target file does not exist: {url}"
        })
    
    return issues


def validate_internal_markdown_link(link: Dict[str, Any], file_index: Dict[str, Path],
                                    source_file: Path) -> List[Dict[str, Any]]:
    """Validate internal markdown link."""
    issues = []
    url = link["url"]
    
    # Skip anchor-only links
    if url.startswith("#"):
        return issues
    
    # Skip external links
    if url.startswith(("http://", "https://", "mailto:")):
        return issues
    
    # Check extension
    if url.endswith(".md"):
        issues.append({
            "severity": "warning",
            "type": "format",
            "message": f"Markdown link uses .md extension, should use .html: {url}",
            "suggestion": "Convert to HTML format with relative_url filter"
        })
    
    # Resolve relative path
    source_dir = source_file.parent
    if url.startswith("../"):
        # Relative path with parent directory
        parts = url.split("/")
        up_count = sum(1 for p in parts if p == "..")
        remaining = "/".join([p for p in parts if p != ".." and p])
        
        target_dir = source_dir
        for _ in range(up_count):
            if target_dir == RAG_DIR:
                break
            target_dir = target_dir.parent
        
        if target_dir == RAG_DIR:
            rel_path = remaining
        else:
            rel_path = str(target_dir.relative_to(RAG_DIR)).replace("\\", "/") + "/" + remaining
    elif url.startswith("./"):
        rel_path = str(source_dir.relative_to(RAG_DIR)).replace("\\", "/") + "/" + url[2:]
    else:
        rel_path = str(source_dir.relative_to(RAG_DIR)).replace("\\", "/") + "/" + url
    
    # Convert .html to .md for lookup
    if rel_path.endswith(".html"):
        rel_path = rel_path[:-5] + ".md"
    elif not rel_path.endswith(".md"):
        rel_path = rel_path + ".md"
    
    # Check if file exists
    if rel_path not in file_index and rel_path.lower() not in file_index:
        issues.append({
            "severity": "error",
            "type": "broken",
            "message": f"Target file does not exist: {url}",
            "resolved_path": rel_path
        })
    
    return issues


def validate_external_link(link: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Validate external link."""
    issues = []
    url = link["url"]
    
    # Check for suspicious patterns
    if "localhost" in url or "127.0.0.1" in url:
        issues.append({
            "severity": "warning",
            "type": "suspicious",
            "message": f"Localhost URL found: {url}"
        })
    
    # Check for test domains
    if any(domain in url for domain in ["test.com", "example.com", "placeholder"]):
        issues.append({
            "severity": "warning",
            "type": "suspicious",
            "message": f"Test/placeholder URL: {url}"
        })
    
    # Note: Actual URL checking (HTTP requests) would be done separately
    # to avoid blocking the validation process
    
    return issues


def validate_anchor_link(link: Dict[str, Any], file_index: Dict[str, Path],
                         source_file: Path) -> List[Dict[str, Any]]:
    """Validate anchor link."""
    issues = []
    url = link["url"]
    
    # Extract anchor
    if "#" in url:
        parts = url.split("#", 1)
        file_url = parts[0]
        anchor = parts[1]
    else:
        anchor = url.lstrip("#")
        file_url = None
    
    # If file URL is specified, validate it
    if file_url:
        if file_url.startswith("/rag/"):
            rel_path = file_url.replace("/rag/", "").replace(".html", ".md")
            if rel_path not in file_index:
                issues.append({
                    "severity": "error",
                    "type": "broken",
                    "message": f"Anchor target file does not exist: {file_url}"
                })
                return issues
            target_file = file_index.get(rel_path) or file_index.get(rel_path.lower())
        else:
            # Relative path - resolve from source
            source_dir = source_file.parent
            if file_url.startswith("../"):
                # Handle relative paths
                parts = file_url.split("/")
                up_count = sum(1 for p in parts if p == "..")
                remaining = "/".join([p for p in parts if p != ".." and p])
                target_dir = source_dir
                for _ in range(up_count):
                    if target_dir == RAG_DIR:
                        break
                    target_dir = target_dir.parent
                rel_path = str(target_dir.relative_to(RAG_DIR)).replace("\\", "/") + "/" + remaining
            else:
                rel_path = str(source_dir.relative_to(RAG_DIR)).replace("\\", "/") + "/" + file_url
            
            rel_path = rel_path.replace(".html", ".md")
            if rel_path not in file_index:
                issues.append({
                    "severity": "error",
                    "type": "broken",
                    "message": f"Anchor target file does not exist: {file_url}"
                })
                return issues
            target_file = file_index.get(rel_path) or file_index.get(rel_path.lower())
    else:
        # Anchor in same file
        target_file = source_file
    
    # Check if anchor exists in target file
    if target_file:
        try:
            content = target_file.read_text(encoding='utf-8')
            # Check for heading with matching anchor ID
            # Jekyll generates anchors from headings: "Section Name" -> "section-name"
            anchor_pattern = re.compile(r'^#{1,6}\s+.*', re.MULTILINE)
            headings = anchor_pattern.findall(content)
            
            # Generate expected anchor IDs from headings
            expected_anchors = set()
            for heading in headings:
                # Remove # and extract text
                text = re.sub(r'^#+\s+', '', heading).strip()
                # Convert to anchor format (lowercase, hyphens)
                anchor_id = re.sub(r'[^\w\s-]', '', text.lower())
                anchor_id = re.sub(r'[-\s]+', '-', anchor_id)
                expected_anchors.add(anchor_id)
            
            if anchor not in expected_anchors:
                issues.append({
                    "severity": "warning",
                    "type": "anchor",
                    "message": f"Anchor '{anchor}' may not exist in target file"
                })
        except Exception as e:
            issues.append({
                "severity": "warning",
                "type": "anchor",
                "message": f"Could not validate anchor: {e}"
            })
    
    return issues


def validate_all_links(discovery_data: Dict[str, Any]) -> Dict[str, Any]:
    """Validate all discovered links."""
    file_index = build_file_index()
    
    all_issues = []
    links_validated = 0
    issues_by_type = defaultdict(int)
    issues_by_severity = defaultdict(int)
    
    print("Validating all links...")
    
    for link in discovery_data["links"]:
        link_issues = []
        source_file = Path(link["source_path"])
        
        if link["type"] == "internal_html":
            link_issues = validate_internal_html_link(link, file_index, source_file)
        elif link["type"] == "internal_markdown":
            link_issues = validate_internal_markdown_link(link, file_index, source_file)
        elif link["type"] == "external":
            link_issues = validate_external_link(link)
        elif link["type"] == "anchor":
            link_issues = validate_anchor_link(link, file_index, source_file)
        elif link["type"] == "mailto":
            # Mailto links are generally valid
            pass
        
        if link_issues:
            for issue in link_issues:
                issue["link"] = link
                all_issues.append(issue)
                issues_by_type[issue["type"]] += 1
                issues_by_severity[issue["severity"]] += 1
        
        links_validated += 1
    
    # Find duplicate links
    duplicate_links = find_duplicate_links(discovery_data["links"])
    
    return {
        "summary": {
            "total_links": links_validated,
            "total_issues": len(all_issues),
            "issues_by_type": dict(issues_by_type),
            "issues_by_severity": dict(issues_by_severity),
            "duplicate_links_count": len(duplicate_links)
        },
        "issues": all_issues,
        "duplicates": duplicate_links
    }


def find_duplicate_links(links: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Find duplicate and redundant links."""
    duplicates = []
    
    # Group links by URL
    links_by_url = defaultdict(list)
    for link in links:
        if link["type"] in ("internal_html", "internal_markdown"):
            links_by_url[link["url"]].append(link)
    
    # Find URLs with multiple links
    for url, url_links in links_by_url.items():
        if len(url_links) > 1:
            # Group by source file
            by_source = defaultdict(list)
            for link in url_links:
                by_source[link["source_file"]].append(link)
            
            # Check for duplicates in same file
            for source, source_links in by_source.items():
                if len(source_links) > 1:
                    duplicates.append({
                        "type": "duplicate_in_file",
                        "url": url,
                        "source_file": source,
                        "count": len(source_links),
                        "links": source_links
                    })
    
    return duplicates


def main():
    """Main function."""
    if not DISCOVERY_FILE.exists():
        print(f"Error: Discovery file not found: {DISCOVERY_FILE}", file=sys.stderr)
        print("Please run discover-all-links.py first.", file=sys.stderr)
        sys.exit(1)
    
    print("=" * 60)
    print("Comprehensive Link Validation")
    print("=" * 60)
    
    # Load discovery data
    discovery_data = json.loads(DISCOVERY_FILE.read_text(encoding='utf-8'))
    
    # Validate all links
    validation_result = validate_all_links(discovery_data)
    
    # Print summary
    print(f"\nValidation Summary:")
    print(f"  Links validated: {validation_result['summary']['total_links']}")
    print(f"  Total issues: {validation_result['summary']['total_issues']}")
    print(f"  Duplicate links: {validation_result['summary']['duplicate_links_count']}")
    
    print(f"\nIssues by severity:")
    for severity, count in sorted(validation_result['summary']['issues_by_severity'].items()):
        print(f"  {severity}: {count}")
    
    print(f"\nIssues by type:")
    for issue_type, count in sorted(validation_result['summary']['issues_by_type'].items()):
        print(f"  {issue_type}: {count}")
    
    # Save validation results
    VALIDATION_FILE.parent.mkdir(parents=True, exist_ok=True)
    VALIDATION_FILE.write_text(
        json.dumps(validation_result, indent=2, ensure_ascii=False),
        encoding='utf-8'
    )
    print(f"\n✓ Saved validation results to: {VALIDATION_FILE}")
    
    # Return exit code based on errors
    error_count = validation_result['summary']['issues_by_severity'].get('error', 0)
    if error_count > 0:
        print(f"\n❌ Found {error_count} errors. Please review and fix.", file=sys.stderr)
        return 1
    else:
        print(f"\n✅ All links validated successfully!")
        return 0


if __name__ == "__main__":
    sys.exit(main())

