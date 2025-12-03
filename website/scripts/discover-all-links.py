#!/usr/bin/env python3
"""
Comprehensive link discovery script.
Scans all markdown files and discovers every link, categorizing by type.
"""

import re
import json
from pathlib import Path
import sys
from collections import defaultdict
from typing import List, Dict, Any

RAG_DIR = Path("rag")
OUTPUT_FILE = Path("website/docs/link-discovery.json")

# Link patterns
HTML_LINK_PATTERN = re.compile(
    r'<a\s+href=["\']\{\{\s*["\']([^"\']+)["\']\s*\|\s*relative_url\s*\}\}["\']\s*>([^<]*)</a>',
    re.IGNORECASE
)

MARKDOWN_LINK_PATTERN = re.compile(
    r'\[([^\]]+)\]\(([^\)]+)\)'
)

EXTERNAL_LINK_PATTERN = re.compile(
    r'(https?://[^\s\)]+)',
    re.IGNORECASE
)

ANCHOR_LINK_PATTERN = re.compile(
    r'#([a-z0-9-]+)',
    re.IGNORECASE
)

MAILTO_PATTERN = re.compile(
    r'mailto:([^\s\)]+)',
    re.IGNORECASE
)


def extract_html_links(content: str, file_path: Path, line_offset: int = 0) -> List[Dict[str, Any]]:
    """Extract HTML links with Jekyll relative_url filter."""
    links = []
    for match in HTML_LINK_PATTERN.finditer(content):
        url = match.group(1)
        text = match.group(2).strip()
        line_num = content[:match.start()].count('\n') + 1 + line_offset
        
        link_type = "internal_html"
        if url.startswith(("http://", "https://")):
            link_type = "external"
        elif url.startswith("mailto:"):
            link_type = "mailto"
        elif url.startswith("#"):
            link_type = "anchor"
        
        links.append({
            "type": link_type,
            "url": url,
            "text": text,
            "line": line_num,
            "format": "html_jekyll"
        })
    
    return links


def extract_markdown_links(content: str, file_path: Path, line_offset: int = 0) -> List[Dict[str, Any]]:
    """Extract markdown links [text](url)."""
    links = []
    # Remove code blocks to avoid false positives
    code_block_pattern = r'```.*?```'
    content_no_code = re.sub(code_block_pattern, '', content, flags=re.DOTALL)
    inline_code_pattern = r'`[^`]+`'
    content_no_code = re.sub(inline_code_pattern, '', content_no_code)
    
    for match in MARKDOWN_LINK_PATTERN.finditer(content_no_code):
        text = match.group(1)
        url = match.group(2)
        line_num = content[:match.start()].count('\n') + 1 + line_offset
        
        # Skip if already captured as HTML link
        if "{{" in url or "|" in url:
            continue
        
        link_type = "internal_markdown"
        if url.startswith(("http://", "https://")):
            link_type = "external"
        elif url.startswith("mailto:"):
            link_type = "mailto"
        elif url.startswith("#"):
            link_type = "anchor"
        
        links.append({
            "type": link_type,
            "url": url,
            "text": text,
            "line": line_num,
            "format": "markdown"
        })
    
    return links


def extract_external_links(content: str, file_path: Path, line_offset: int = 0) -> List[Dict[str, Any]]:
    """Extract standalone external links (not in markdown or HTML format)."""
    links = []
    # Remove code blocks and existing links
    code_block_pattern = r'```.*?```'
    content_no_code = re.sub(code_block_pattern, '', content, flags=re.DOTALL)
    
    # Remove markdown and HTML links already captured
    content_no_code = re.sub(r'\[([^\]]+)\]\([^\)]+\)', '', content_no_code)
    content_no_code = re.sub(r'<a[^>]*>.*?</a>', '', content_no_code, flags=re.DOTALL)
    
    for match in EXTERNAL_LINK_PATTERN.finditer(content_no_code):
        url = match.group(1)
        line_num = content[:match.start()].count('\n') + 1 + line_offset
        
        links.append({
            "type": "external",
            "url": url,
            "text": url,
            "line": line_num,
            "format": "standalone"
        })
    
    return links


def discover_all_links() -> Dict[str, Any]:
    """Discover all links in all markdown files."""
    all_links = []
    files_processed = 0
    links_by_type = defaultdict(int)
    
    if not RAG_DIR.exists():
        print(f"Error: {RAG_DIR} directory not found", file=sys.stderr)
        sys.exit(1)
    
    print("Scanning all markdown files for links...")
    
    for md_file in RAG_DIR.rglob("*.md"):
        # Skip rag-index.md (it's auto-generated)
        if md_file.name == "rag-index.md":
            continue
        
        try:
            content = md_file.read_text(encoding='utf-8')
        except Exception as e:
            print(f"Warning: Could not read {md_file}: {e}", file=sys.stderr)
            continue
        
        # Get relative path from rag/
        try:
            rel_path = md_file.relative_to(RAG_DIR)
        except ValueError:
            continue
        
        files_processed += 1
        
        # Extract all link types
        html_links = extract_html_links(content, md_file)
        markdown_links = extract_markdown_links(content, md_file)
        external_links = extract_external_links(content, md_file)
        
        # Combine all links
        file_links = html_links + markdown_links + external_links
        
        for link in file_links:
            link["source_file"] = str(rel_path).replace("\\", "/")
            link["source_path"] = str(md_file)
            all_links.append(link)
            links_by_type[link["type"]] += 1
    
    # Build summary
    summary = {
        "total_files": files_processed,
        "total_links": len(all_links),
        "links_by_type": dict(links_by_type),
        "links_by_format": defaultdict(int)
    }
    
    for link in all_links:
        summary["links_by_format"][link["format"]] += 1
    
    summary["links_by_format"] = dict(summary["links_by_format"])
    
    return {
        "summary": summary,
        "links": all_links
    }


def main():
    """Main function."""
    print("=" * 60)
    print("Comprehensive Link Discovery")
    print("=" * 60)
    
    result = discover_all_links()
    
    # Print summary
    print(f"\nSummary:")
    print(f"  Files processed: {result['summary']['total_files']}")
    print(f"  Total links found: {result['summary']['total_links']}")
    print(f"\nLinks by type:")
    for link_type, count in sorted(result['summary']['links_by_type'].items()):
        print(f"  {link_type}: {count}")
    print(f"\nLinks by format:")
    for format_type, count in sorted(result['summary']['links_by_format'].items()):
        print(f"  {format_type}: {count}")
    
    # Save to JSON
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_FILE.write_text(
        json.dumps(result, indent=2, ensure_ascii=False),
        encoding='utf-8'
    )
    print(f"\n✓ Saved link discovery results to: {OUTPUT_FILE}")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())

