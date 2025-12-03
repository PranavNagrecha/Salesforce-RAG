#!/usr/bin/env python3
"""
Validate all internal links in markdown files and find incorrect paths.
This script finds links that point to wrong directories (e.g., /rag/api-reference/development/ when file is in /rag/development/).
"""

import re
from pathlib import Path
import sys
from collections import defaultdict

RAG_DIR = Path("rag")

# Files that exist in development/ folder
DEVELOPMENT_FILES = {
    "apex-patterns.md",
    "soql-query-patterns.md",
    "governor-limits-and-optimization.md",
    "error-handling-and-logging.md",
    "flow-patterns.md",
    "lwc-patterns.md",
    "asynchronous-apex-patterns.md",
    "custom-settings-metadata-patterns.md",
    "locking-and-concurrency-strategies.md",
    "order-of-execution.md",
    "large-data-loads.md",
    "admin-basics.md",
    "email-management.md",
    "formulas-validation-rules.md",
    "lightning-app-builder.md",
    "omnistudio-patterns.md",
}

def find_all_links():
    """Find all internal links in markdown files."""
    issues = defaultdict(list)
    
    # Pattern to match HTML links with relative_url filter
    link_pattern = re.compile(r'<a href="\{\{\s*[\'"](\S+)[\'"]\s*\|\s*relative_url\s*\}\}">')
    
    for md_file in RAG_DIR.rglob("*.md"):
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
        
        # Find all links
        for match in link_pattern.finditer(content):
            link_url = match.group(1)
            
            # Skip external links
            if link_url.startswith(("http://", "https://", "mailto:")):
                continue
            
            # Only check /rag/ paths
            if not link_url.startswith("/rag/"):
                continue
            
            # Extract the file path from the link
            # Format: /rag/folder/file.html
            path_parts = link_url.replace("/rag/", "").split("/")
            
            # Check if this is a development file that's being referenced from wrong location
            filename = path_parts[-1].replace(".html", ".md")
            
            if filename in DEVELOPMENT_FILES:
                # Check if path is wrong (should be /rag/development/filename.html)
                if len(path_parts) > 2 or (len(path_parts) == 2 and path_parts[0] != "development"):
                    correct_path = f"/rag/development/{filename.replace('.md', '.html')}"
                    if link_url != correct_path:
                        issues[md_file].append({
                            "incorrect": link_url,
                            "correct": correct_path,
                            "line": content[:match.start()].count('\n') + 1
                        })
    
    return issues

def main():
    """Main function."""
    print("Scanning all markdown files for incorrect links...")
    issues = find_all_links()
    
    if not issues:
        print("\n✅ No incorrect links found!")
        return 0
    
    print(f"\n❌ Found incorrect links in {len(issues)} files:\n")
    
    total_issues = 0
    for file_path, file_issues in issues.items():
        print(f"  {file_path}:")
        for issue in file_issues:
            total_issues += 1
            print(f"    Line {issue['line']}:")
            print(f"      ❌ {issue['incorrect']}")
            print(f"      ✅ {issue['correct']}")
        print()
    
    print(f"\nTotal: {total_issues} incorrect links found")
    return 1

if __name__ == "__main__":
    sys.exit(main())

