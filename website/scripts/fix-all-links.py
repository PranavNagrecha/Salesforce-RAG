#!/usr/bin/env python3
"""
Fix all internal links in markdown files to use HTML links with Jekyll's relative_url filter.
This ensures all links work correctly with Jekyll's baseurl.
Jekyll's kramdown doesn't apply baseurl to markdown links, so we use HTML links instead.
"""

import re
from pathlib import Path
import sys

RAG_DIR = Path("rag")

def fix_links_in_file(file_path: Path):
    """Fix all internal links in a markdown file to use absolute paths."""
    try:
        content = file_path.read_text(encoding='utf-8')
    except Exception as e:
        print(f"Warning: Could not read {file_path}: {e}", file=sys.stderr)
        return False
    
    # Get relative path from rag/ directory
    try:
        rel_path = file_path.relative_to(RAG_DIR)
    except ValueError:
        return False
    
    # Get the directory containing this file (relative to rag/)
    file_dir = rel_path.parent
    
    modified = False
    new_content = content
    
    # Pattern to match markdown links: [text](url)
    link_pattern = r'\[([^\]]+)\]\(([^\)]+)\)'
    
    def replace_link(match):
        nonlocal modified
        link_text = match.group(1)
        link_url = match.group(2)
        
        # Skip external links
        if link_url.startswith(("http://", "https://", "mailto:")):
            return match.group(0)
        
        # Skip anchor links
        if link_url.startswith("#"):
            return match.group(0)
        
        # Skip Jekyll template syntax
        if "{{" in link_url or "|" in link_url:
            return match.group(0)
        
        # Convert all internal links to HTML links with Jekyll relative_url filter
        if link_url.endswith(".html") or link_url.endswith(".md"):
            # Build absolute path for Jekyll
            if link_url.startswith("/rag/"):
                # Already absolute path
                absolute_path = link_url
            elif link_url.startswith("../"):
                # Relative path with parent directory - resolve correctly
                parts = link_url.split("/")
                up_count = sum(1 for p in parts if p == "..")
                remaining = "/".join([p for p in parts if p != ".." and p])
                # Go up from file_dir
                target_dir = file_dir
                for _ in range(up_count):
                    if target_dir == Path("."):
                        # Can't go up from rag/ root
                        break
                    target_dir = target_dir.parent
                if target_dir == Path("."):
                    absolute_path = f"/rag/{remaining}"
                else:
                    # Build path correctly
                    target_str = str(target_dir).replace("\\", "/")
                    absolute_path = f"/rag/{target_str}/{remaining}" if target_str else f"/rag/{remaining}"
            elif link_url.startswith("./"):
                # Same directory
                remaining = link_url[2:]
                if file_dir == Path("."):
                    absolute_path = f"/rag/{remaining}"
                else:
                    absolute_path = f"/rag/{file_dir}/{remaining}"
            else:
                # Same directory or subdirectory (no ../ or ./ prefix)
                if file_dir == Path("."):
                    # File is in rag/ root
                    absolute_path = f"/rag/{link_url}"
                else:
                    # File is in a subdirectory - link is relative to that directory
                    # If link_url doesn't contain /, it's in same directory
                    if "/" not in link_url:
                        # Same directory
                        file_dir_str = str(file_dir).replace("\\", "/")
                        absolute_path = f"/rag/{file_dir_str}/{link_url}"
                    else:
                        # Subdirectory - resolve relative to file_dir
                        file_dir_str = str(file_dir).replace("\\", "/")
                        absolute_path = f"/rag/{file_dir_str}/{link_url}"
            
            # Convert .md to .html if needed
            if absolute_path.endswith(".md"):
                absolute_path = absolute_path[:-3] + ".html"
            
            # Normalize path
            absolute_path = absolute_path.replace("//", "/")
            
            # Convert to HTML link with Jekyll filter
            modified = True
            return f"<a href=\"{{{{ '{absolute_path}' | relative_url }}}}\">{link_text}</a>"
            # Handle relative paths
            if not link_url.startswith("/"):
                # This is a relative path - convert to absolute
                # Handle ../ paths
                if link_url.startswith("../"):
                    # Count how many ../ we have
                    parts = link_url.split("/")
                    up_count = sum(1 for p in parts if p == "..")
                    # Build path from rag/ root
                    remaining = "/".join([p for p in parts if p != ".." and p])
                    # Go up from file_dir
                    target_dir = file_dir
                    for _ in range(up_count):
                        target_dir = target_dir.parent
                    if target_dir == Path("."):
                        new_url = f"/rag/{remaining}"
                    else:
                        new_url = f"/rag/{target_dir}/{remaining}"
                elif link_url.startswith("./"):
                    # Same directory
                    remaining = link_url[2:]
                    if file_dir == Path("."):
                        new_url = f"/rag/{remaining}"
                    else:
                        new_url = f"/rag/{file_dir}/{remaining}"
                else:
                    # Same directory or subdirectory
                    if file_dir == Path("."):
                        new_url = f"/rag/{link_url}"
                    else:
                        new_url = f"/rag/{file_dir}/{link_url}"
                
                # Convert .md to .html if needed
                if new_url.endswith(".md"):
                    new_url = new_url[:-3] + ".html"
                
                # Normalize path (remove //, handle .)
                new_url = new_url.replace("//", "/")
                
                modified = True
                return f"[{link_text}]({new_url})"
        
        return match.group(0)
    
    # Replace all links
    new_content = re.sub(link_pattern, replace_link, content)
    
    if modified:
        file_path.write_text(new_content, encoding='utf-8')
        print(f"Fixed links in: {file_path}")
        return True
    
    return False

def main():
    """Fix all links in all markdown files."""
    if not RAG_DIR.exists():
        print(f"Error: {RAG_DIR} directory not found", file=sys.stderr)
        sys.exit(1)
    
    fixed_count = 0
    total_files = 0
    
    for file_path in RAG_DIR.rglob("*.md"):
        # Skip rag-index.md (it's generated by sync-homepage.py)
        if file_path.name == "rag-index.md":
            continue
        
        total_files += 1
        if fix_links_in_file(file_path):
            fixed_count += 1
    
    print(f"\n✅ Fixed links in {fixed_count} out of {total_files} files")

if __name__ == "__main__":
    main()

