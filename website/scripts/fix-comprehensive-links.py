#!/usr/bin/env python3
"""
Comprehensive link fix script.
Automatically fixes common link issues with safety checks.
"""

import json
import re
from pathlib import Path
import sys
from typing import Dict, List, Any
import shutil
from datetime import datetime

RAG_DIR = Path("rag")
VALIDATION_FILE = Path("website/docs/link-validation.json")
BACKUP_DIR = Path("website/docs/link-fix-backups")

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


def fix_duplicate_directory_pattern(content: str, file_path: Path) -> tuple[str, bool]:
    """Fix duplicate directory patterns in links."""
    modified = False
    new_content = content
    
    # First, fix the specific /rag/rag/ pattern (most common issue)
    # Pattern: /rag/rag/... should be /rag/...
    rag_duplicate_pattern = r'/rag/rag/'
    if re.search(rag_duplicate_pattern, new_content):
        new_content = re.sub(rag_duplicate_pattern, '/rag/', new_content)
        modified = True
    
    # Pattern: /rag/folder/folder/file.html (for other duplicate subdirectories)
    pattern = r'/rag/([^/]+)/\1/'
    
    def replace_duplicate(match):
        nonlocal modified
        folder = match.group(1)
        modified = True
        return f'/rag/{folder}/'
    
    new_content = re.sub(pattern, replace_duplicate, new_content)
    
    return new_content, modified


def fix_development_file_paths(content: str, file_path: Path) -> tuple[str, bool]:
    """Fix incorrect paths to development/ files."""
    modified = False
    new_content = content
    
    # First, fix any paths with wrong subdirectories (e.g., /rag/code-examples/development/ -> /rag/development/)
    wrong_pattern = re.compile(r'/rag/([^/]+/)+development/')
    def fix_wrong_subdir(match):
        nonlocal modified
        modified = True
        # Extract just the filename part
        full_match = match.group(0)
        # Replace with correct path
        return '/rag/development/'
    
    new_content = wrong_pattern.sub(fix_wrong_subdir, new_content)
    
    # Pattern: <a href="{{ '/rag/.../development/file.html' | relative_url }}">
    html_pattern = re.compile(
        r'<a\s+href=["\']\{\{\s*["\']([^"\']+)["\']\s*\|\s*relative_url\s*\}\}["\']\s*>',
        re.IGNORECASE
    )
    
    def replace_path(match):
        nonlocal modified
        url = match.group(1)
        
        # Check if this is a development file in wrong location
        if not url.startswith("/rag/"):
            return match.group(0)
        
        # Fix any remaining wrong paths (e.g., code-examples/development/)
        if "/code-examples/development/" in url or "/flow/development/" in url or "/lwc/development/" in url:
            modified = True
            url = url.replace("/code-examples/development/", "/development/")
            url = url.replace("/flow/development/", "/development/")
            url = url.replace("/lwc/development/", "/development/")
            return match.group(0).replace(match.group(1), url)
        
        # Extract filename
        parts = url.replace("/rag/", "").split("/")
        filename = parts[-1].replace(".html", ".md").split("#")[0]  # Remove anchor
        
        if filename in DEVELOPMENT_FILES:
            correct_path = DEVELOPMENT_FILES[filename]
            # Preserve anchor if present
            if "#" in url:
                anchor = "#" + url.split("#", 1)[1]
                correct_path = correct_path.replace(".html", anchor)
            if url != correct_path:
                modified = True
                return match.group(0).replace(url, correct_path)
        
        return match.group(0)
    
    new_content = html_pattern.sub(replace_path, new_content)
    
    # Fix anchor links with .html extension
    anchor_pattern = re.compile(r'(#[\w-]+)\.html')
    def fix_anchor(match):
        nonlocal modified
        modified = True
        return match.group(1)
    
    new_content = anchor_pattern.sub(fix_anchor, new_content)
    
    return new_content, modified


def convert_markdown_to_html_link(content: str, file_path: Path) -> tuple[str, bool]:
    """Convert remaining markdown links to HTML format with relative_url filter."""
    modified = False
    new_content = content
    
    # Remove code blocks to avoid false positives
    code_blocks = []
    code_block_pattern = r'```[^`]*```'
    
    def replace_code_block(match):
        placeholder = f"__CODE_BLOCK_{len(code_blocks)}__"
        code_blocks.append(match.group(0))
        return placeholder
    
    new_content = re.sub(code_block_pattern, replace_code_block, new_content, flags=re.DOTALL)
    
    # Pattern: [text](url)
    markdown_link_pattern = re.compile(r'\[([^\]]+)\]\(([^\)]+)\)')
    
    def replace_markdown_link(match):
        nonlocal modified
        link_text = match.group(1)
        link_url = match.group(2)
        
        # Skip external links
        if link_url.startswith(("http://", "https://", "mailto:")):
            return match.group(0)
        
        # Skip anchor links
        if link_url.startswith("#"):
            return match.group(0)
        
        # Skip if already has Jekyll syntax
        if "{{" in link_url or "|" in link_url:
            return match.group(0)
        
        # Convert to absolute path from /rag/
        source_dir = file_path.parent
        try:
            rel_path = file_path.relative_to(RAG_DIR)
            file_dir = rel_path.parent
        except ValueError:
            return match.group(0)
        
        # Resolve relative path
        if link_url.startswith("../"):
            parts = link_url.split("/")
            up_count = sum(1 for p in parts if p == "..")
            remaining = "/".join([p for p in parts if p != ".." and p])
            
            target_dir = file_dir
            for _ in range(up_count):
                if target_dir == Path("."):
                    break
                target_dir = target_dir.parent
            
            if target_dir == Path("."):
                absolute_path = f"/rag/{remaining}"
            else:
                target_str = str(target_dir).replace("\\", "/")
                absolute_path = f"/rag/{target_str}/{remaining}" if target_str else f"/rag/{remaining}"
        elif link_url.startswith("./"):
            remaining = link_url[2:]
            if file_dir == Path("."):
                absolute_path = f"/rag/{remaining}"
            else:
                file_dir_str = str(file_dir).replace("\\", "/")
                absolute_path = f"/rag/{file_dir_str}/{remaining}"
        else:
            # Same directory or subdirectory
            if file_dir == Path("."):
                absolute_path = f"/rag/{link_url}"
            else:
                file_dir_str = str(file_dir).replace("\\", "/")
                absolute_path = f"/rag/{file_dir_str}/{link_url}"
        
        # Ensure .html extension
        if absolute_path.endswith(".md"):
            absolute_path = absolute_path[:-3] + ".html"
        elif not absolute_path.endswith(".html"):
            absolute_path = absolute_path + ".html"
        
        # Normalize path
        absolute_path = absolute_path.replace("//", "/")
        
        modified = True
        return f'<a href="{{{{ \'{absolute_path}\' | relative_url }}}}">{link_text}</a>'
    
    new_content = markdown_link_pattern.sub(replace_markdown_link, new_content)
    
    # Restore code blocks
    for i, code_block in enumerate(code_blocks):
        new_content = new_content.replace(f"__CODE_BLOCK_{i}__", code_block)
    
    return new_content, modified


def fix_file_extensions(content: str, file_path: Path) -> tuple[str, bool]:
    """Fix .md extensions in links to .html."""
    modified = False
    new_content = content
    
    # Pattern: /rag/.../file.md or /rag/.../file.md#anchor
    pattern = r'(/rag/[^"\']+\.md)([#"\']|$)'
    
    def replace_extension(match):
        nonlocal modified
        path = match.group(1)
        suffix = match.group(2)
        modified = True
        return path.replace(".md", ".html") + suffix
    
    new_content = re.sub(pattern, replace_extension, new_content)
    
    return new_content, modified


def fix_file(file_path: Path, dry_run: bool = True) -> Dict[str, Any]:
    """Fix all issues in a file."""
    try:
        content = file_path.read_text(encoding='utf-8')
    except Exception as e:
        return {"error": str(e), "fixed": False}
    
    original_content = content
    fixes_applied = []
    
    # Apply all fixes
    content, fixed1 = fix_duplicate_directory_pattern(content, file_path)
    if fixed1:
        fixes_applied.append("duplicate_directory")
    
    content, fixed2 = fix_development_file_paths(content, file_path)
    if fixed2:
        fixes_applied.append("development_file_paths")
    
    content, fixed3 = convert_markdown_to_html_link(content, file_path)
    if fixed3:
        fixes_applied.append("markdown_to_html")
    
    content, fixed4 = fix_file_extensions(content, file_path)
    if fixed4:
        fixes_applied.append("file_extensions")
    
    if fixes_applied and not dry_run:
        # Create backup
        backup_dir = BACKUP_DIR / datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_dir.mkdir(parents=True, exist_ok=True)
        backup_file = backup_dir / file_path.name
        shutil.copy2(file_path, backup_file)
        
        # Write fixed content
        file_path.write_text(content, encoding='utf-8')
    
    return {
        "fixed": len(fixes_applied) > 0,
        "fixes": fixes_applied,
        "backup": str(backup_dir / file_path.name) if fixes_applied and not dry_run else None
    }


def main():
    """Main function."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Fix comprehensive link issues")
    parser.add_argument("--dry-run", action="store_true", default=True,
                       help="Show what would be fixed without making changes (default)")
    parser.add_argument("--apply", action="store_true",
                       help="Actually apply fixes (creates backups)")
    parser.add_argument("--file", type=str,
                       help="Fix specific file only")
    
    args = parser.parse_args()
    
    dry_run = not args.apply
    
    if dry_run:
        print("=" * 60)
        print("Link Fix (DRY RUN - no changes will be made)")
        print("=" * 60)
    else:
        print("=" * 60)
        print("Link Fix (APPLYING CHANGES)")
        print("=" * 60)
        BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    
    if args.file:
        # Fix specific file
        file_path = Path(args.file)
        if not file_path.exists():
            print(f"Error: File not found: {file_path}", file=sys.stderr)
            sys.exit(1)
        
        result = fix_file(file_path, dry_run)
        if result.get("fixed"):
            print(f"Would fix: {file_path}" if dry_run else f"Fixed: {file_path}")
            print(f"  Fixes: {', '.join(result['fixes'])}")
            if result.get("backup"):
                print(f"  Backup: {result['backup']}")
        else:
            print(f"No fixes needed: {file_path}")
    else:
        # Fix all files
        fixed_count = 0
        total_files = 0
        
        for md_file in RAG_DIR.rglob("*.md"):
            # Include rag-index.md in fixes (it has the most broken links)
            total_files += 1
            result = fix_file(md_file, dry_run)
            
            if result.get("fixed"):
                fixed_count += 1
                if dry_run:
                    print(f"Would fix: {md_file}")
                else:
                    print(f"Fixed: {md_file}")
                print(f"  Fixes: {', '.join(result['fixes'])}")
                if result.get("backup"):
                    print(f"  Backup: {result['backup']}")
        
        print(f"\n{'Would fix' if dry_run else 'Fixed'} {fixed_count} out of {total_files} files")
        
        if dry_run:
            print("\nRun with --apply to actually apply fixes")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())

