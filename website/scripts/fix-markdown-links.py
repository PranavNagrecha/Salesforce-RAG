#!/usr/bin/env python3
"""
Fix Markdown Links for Jekyll Website

This script fixes internal markdown links to work with Jekyll's URL structure
and baseurl configuration. It:
1. Converts absolute paths starting with /rag/ to include baseurl
2. Ensures .md extensions are converted to .html for absolute paths
3. Keeps relative paths as-is (Jekyll handles these automatically)
4. Updates links to work with baseurl: /Salesforce-RAG

Usage:
    python scripts/fix-markdown-links.py
    python scripts/fix-markdown-links.py --dry-run
    python scripts/fix-markdown-links.py --validate-only
"""

import os
import re
import sys
from pathlib import Path
from typing import List, Tuple
import argparse

# Configuration
BASE_DIR = Path(__file__).parent.parent
RAG_DIR = BASE_DIR / "rag"
BASEURL = "/Salesforce-RAG"

# Patterns to match markdown links
MARKDOWN_LINK_PATTERN = re.compile(r'\[([^\]]+)\]\(([^)]+)\)')

def is_absolute_path(path: str) -> bool:
    """Check if path is absolute (starts with /)."""
    return path.startswith('/')

def is_relative_path(path: str) -> bool:
    """Check if path is relative (starts with ../ or ./ or no slash)."""
    return path.startswith('../') or path.startswith('./') or (not path.startswith('/') and not path.startswith('http'))

def fix_link_path(link_path: str, file_path: Path, baseurl: str) -> str:
    """
    Fix a link path to work with Jekyll and baseurl.
    
    Rules:
    - Absolute paths starting with /rag/ → /Salesforce-RAG/rag/... and .md → .html
    - Absolute paths starting with /examples/ → /Salesforce-RAG/examples/... and .md → .html
    - Paths starting with rag/ (no leading slash) → Convert to /Salesforce-RAG/rag/... and .md → .html
    - Relative paths → Keep as-is but convert .md → .html (Jekyll handles paths)
    - External URLs → Keep as-is
    - Anchor-only links (#section) → Keep as-is
    """
    # Skip external URLs
    if link_path.startswith('http://') or link_path.startswith('https://') or link_path.startswith('mailto:'):
        return link_path
    
    # Skip anchor-only links
    if link_path.startswith('#'):
        return link_path
    
    # Handle paths starting with rag/ or examples/ (without leading slash) - treat as absolute
    if link_path.startswith('rag/') or link_path.startswith('examples/'):
        # Convert to absolute path with baseurl
        link_path = '/' + link_path  # Add leading slash
        # Convert .md to .html
        if link_path.endswith('.md'):
            link_path = link_path[:-3] + '.html'
        elif link_path.endswith('.md#'):
            link_path = link_path[:-4] + '.html#'
        elif '.md#' in link_path:
            link_path = link_path.replace('.md#', '.html#')
        # Add baseurl
        if not link_path.startswith(baseurl):
            link_path = baseurl + link_path
        return link_path
    
    # Handle absolute paths
    if is_absolute_path(link_path):
        # Convert .md to .html for absolute paths
        if link_path.endswith('.md'):
            link_path = link_path[:-3] + '.html'
        elif link_path.endswith('.md#'):
            link_path = link_path[:-4] + '.html#'
        elif '.md#' in link_path:
            link_path = link_path.replace('.md#', '.html#')
        
        # Add baseurl if it's a site path (starts with /rag/ or /examples/)
        if link_path.startswith('/rag/') or link_path.startswith('/examples/'):
            if not link_path.startswith(baseurl):
                link_path = baseurl + link_path
        
        return link_path
    
    # Handle relative paths - Jekyll handles these automatically
    # But we should convert .md to .html for consistency
    if is_relative_path(link_path):
        # Convert .md to .html in relative paths too
        if link_path.endswith('.md'):
            link_path = link_path[:-3] + '.html'
        elif link_path.endswith('.md#'):
            link_path = link_path[:-4] + '.html#'
        elif '.md#' in link_path:
            link_path = link_path.replace('.md#', '.html#')
        
        return link_path
    
    # Unknown pattern - return as-is
    return link_path

def fix_markdown_file(file_path: Path, baseurl: str, dry_run: bool = False) -> Tuple[int, List[str]]:
    """
    Fix all markdown links in a file.
    
    Returns:
        (number_of_fixes, list_of_changes)
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading {file_path}: {e}", file=sys.stderr)
        return 0, []
    
    original_content = content
    fixes = []
    fix_count = 0
    
    def replace_link(match):
        nonlocal fix_count
        link_text = match.group(1)
        link_path = match.group(2)
        
        fixed_path = fix_link_path(link_path, file_path, baseurl)
        
        if fixed_path != link_path:
            fix_count += 1
            fixes.append(f"  - {link_path} → {fixed_path}")
            return f"[{link_text}]({fixed_path})"
        
        return match.group(0)
    
    # Replace all markdown links
    fixed_content = MARKDOWN_LINK_PATTERN.sub(replace_link, content)
    
    if fix_count > 0 and not dry_run:
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(fixed_content)
        except Exception as e:
            print(f"Error writing {file_path}: {e}", file=sys.stderr)
            return 0, []
    
    return fix_count, fixes

def find_markdown_files(root_dir: Path) -> List[Path]:
    """Find all markdown files in the RAG directory."""
    markdown_files = []
    
    for file_path in root_dir.rglob("*.md"):
        # Skip certain files
        if file_path.name in ["README.md", "CONTRIBUTING.md", "MAINTENANCE.md"]:
            continue
        
        markdown_files.append(file_path)
    
    return sorted(markdown_files)

def main():
    parser = argparse.ArgumentParser(
        description="Fix markdown links for Jekyll website"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be changed without making changes"
    )
    parser.add_argument(
        "--validate-only",
        action="store_true",
        help="Only validate links, don't fix them"
    )
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Verbose output"
    )
    
    args = parser.parse_args()
    
    print("🔍 Scanning for markdown files...")
    
    # Find all markdown files
    markdown_files = find_markdown_files(RAG_DIR)
    
    if not markdown_files:
        print("❌ No markdown files found!")
        sys.exit(1)
    
    print(f"Found {len(markdown_files)} markdown files\n")
    
    total_fixes = 0
    files_changed = 0
    
    for file_path in markdown_files:
        relative_path = file_path.relative_to(BASE_DIR)
        
        fix_count, fixes = fix_markdown_file(
            file_path, 
            BASEURL, 
            dry_run=args.dry_run or args.validate_only
        )
        
        if fix_count > 0:
            files_changed += 1
            total_fixes += fix_count
            
            if args.verbose or args.dry_run:
                print(f"📝 {relative_path}: {fix_count} fix(es)")
                if args.verbose:
                    for fix in fixes:
                        print(fix)
    
    print(f"\n{'='*60}")
    print("Summary")
    print(f"{'='*60}")
    print(f"Files scanned: {len(markdown_files)}")
    print(f"Files with fixes: {files_changed}")
    print(f"Total fixes: {total_fixes}")
    
    if args.dry_run:
        print("\n🔍 [DRY RUN] No changes made. Run without --dry-run to apply fixes.")
    elif args.validate_only:
        print("\n✅ Validation complete!")
    else:
        print("\n✅ All links fixed!")
        print("\nNext steps:")
        print("  1. Review the changes: git diff")
        print("  2. Commit: git add rag/")
        print("  3. Push: git push origin main")

if __name__ == "__main__":
    main()

