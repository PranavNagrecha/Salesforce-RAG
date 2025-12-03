#!/usr/bin/env python3
"""
Fix all incorrect internal links in markdown files.
This script automatically fixes links that point to wrong directories.
"""

import re
from pathlib import Path
import sys

RAG_DIR = Path("rag")

# Files that exist in development/ folder - map to correct path
DEVELOPMENT_FILES = {
    "apex-patterns.md": "/rag/development/apex-patterns.html",
    "soql-query-patterns.md": "/rag/development/soql-query-patterns.html",
    "governor-limits-and-optimization.md": "/rag/development/governor-limits-and-optimization.html",
    "error-handling-and-logging.md": "/rag/development/error-handling-and-logging.html",
    "flow-patterns.md": "/rag/development/flow-patterns.html",
    "lwc-patterns.md": "/rag/development/lwc-patterns.html",
    "asynchronous-apex-patterns.md": "/rag/development/asynchronous-apex-patterns.html",
    "custom-settings-metadata-patterns.md": "/rag/development/custom-settings-metadata-patterns.html",
    "locking-and-concurrency-strategies.md": "/rag/development/locking-and-concurrency-strategies.html",
    "order-of-execution.md": "/rag/development/order-of-execution.html",
    "large-data-loads.md": "/rag/development/large-data-loads.html",
    "admin-basics.md": "/rag/development/admin-basics.html",
    "email-management.md": "/rag/development/email-management.html",
    "formulas-validation-rules.md": "/rag/development/formulas-validation-rules.html",
    "lightning-app-builder.md": "/rag/development/lightning-app-builder.html",
    "omnistudio-patterns.md": "/rag/development/omnistudio-patterns.html",
}

def fix_file(file_path: Path):
    """Fix incorrect links in a file."""
    try:
        content = file_path.read_text(encoding='utf-8')
    except Exception as e:
        print(f"Warning: Could not read {file_path}: {e}", file=sys.stderr)
        return False
    
    modified = False
    new_content = content
    
    # Pattern to match HTML links with relative_url filter
    def replace_link(match):
        nonlocal modified
        full_match = match.group(0)
        link_url = match.group(1)
        
        # Skip external links
        if link_url.startswith(("http://", "https://", "mailto:")):
            return full_match
        
        # Only check /rag/ paths
        if not link_url.startswith("/rag/"):
            return full_match
        
        # Extract the file path from the link
        path_parts = link_url.replace("/rag/", "").split("/")
        filename = path_parts[-1].replace(".html", ".md")
        
        # Check if this is a development file that's being referenced from wrong location
        if filename in DEVELOPMENT_FILES:
            correct_path = DEVELOPMENT_FILES[filename]
            if link_url != correct_path:
                modified = True
                # Replace the incorrect URL with the correct one
                return full_match.replace(link_url, correct_path)
        
        return full_match
    
    # Pattern: <a href="{{ '/rag/path/file.html' | relative_url }}">
    link_pattern = re.compile(r'<a href="\{\{\s*[\'"](\S+)[\'"]\s*\|\s*relative_url\s*\}\}">')
    new_content = link_pattern.sub(replace_link, new_content)
    
    if modified:
        file_path.write_text(new_content, encoding='utf-8')
        print(f"Fixed links in: {file_path}")
        return True
    
    return False

def main():
    """Main function."""
    if not RAG_DIR.exists():
        print(f"Error: {RAG_DIR} directory not found", file=sys.stderr)
        sys.exit(1)
    
    print("Fixing incorrect links in all markdown files...")
    
    fixed_count = 0
    total_files = 0
    
    for file_path in RAG_DIR.rglob("*.md"):
        # Skip rag-index.md (it's generated)
        if file_path.name == "rag-index.md":
            continue
        
        total_files += 1
        if fix_file(file_path):
            fixed_count += 1
    
    print(f"\n✅ Fixed links in {fixed_count} out of {total_files} files")

if __name__ == "__main__":
    main()

