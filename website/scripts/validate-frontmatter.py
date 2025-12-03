#!/usr/bin/env python3
"""
Validate that all markdown files in rag/ have proper Jekyll frontmatter.

This script checks:
1. All .md files have frontmatter starting with ---
2. Frontmatter contains required fields: layout, title, permalink
3. Permalink matches file path

Usage:
    python website/scripts/validate-frontmatter.py
    python website/scripts/validate-frontmatter.py --fix  # Auto-fix missing frontmatter
"""

import re
import sys
from pathlib import Path

def has_proper_frontmatter(file_path):
    """Check if file has proper Jekyll frontmatter with layout and permalink."""
    try:
        content = file_path.read_text(encoding='utf-8')
        stripped = content.strip()
        if not stripped.startswith('---'):
            return False, "Missing frontmatter (doesn't start with ---)"
        
        lines = stripped.split('\n')
        if len(lines) < 2:
            return False, "Invalid frontmatter format (too short)"
        
        # First line should be ---
        if lines[0].strip() != '---':
            return False, "Invalid frontmatter format (first line not ---)"
        
        # Find closing ---
        closing_idx = None
        for i in range(1, len(lines)):
            if lines[i].strip() == '---':
                closing_idx = i
                break
        
        if closing_idx is None:
            return False, "Invalid frontmatter format (no closing ---)"
        
        # Find where frontmatter ends
        end_idx = 1
        for i in range(2, len(lines)):
            if lines[i].strip() == '---':
                end_idx = i
                break
        
        frontmatter_text = '\n'.join(lines[:end_idx+1])
        
        # Check for required fields
        missing = []
        if 'layout:' not in frontmatter_text:
            missing.append('layout')
        if 'permalink:' not in frontmatter_text:
            missing.append('permalink')
        if 'title:' not in frontmatter_text:
            missing.append('title')
        
        if missing:
            return False, f"Missing required fields: {', '.join(missing)}"
        
        # Verify permalink matches file path
        permalink_match = re.search(r'permalink:\s*(.+)', frontmatter_text)
        if permalink_match:
            permalink = permalink_match.group(1).strip().strip('"\'')
            rel_path = str(file_path.relative_to(Path('rag')))
            expected_permalink = f"/rag/{rel_path.replace('.md', '.html')}"
            if permalink != expected_permalink:
                return False, f"Permalink mismatch: {permalink} != {expected_permalink}"
        
        return True, None
    except Exception as e:
        return False, f"Error reading file: {str(e)}"

def main():
    """Main validation function."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Validate Jekyll frontmatter in all markdown files')
    parser.add_argument('--fix', action='store_true', help='Auto-fix missing frontmatter')
    parser.add_argument('--verbose', action='store_true', help='Verbose output')
    args = parser.parse_args()
    
    # Find all markdown files in rag/
    rag_dir = Path('rag')
    if not rag_dir.exists():
        print(f"Error: {rag_dir} directory not found")
        sys.exit(1)
    
    all_md_files = list(rag_dir.rglob('*.md'))
    
    # Exclude index files and special files
    excluded = {'rag-index.md', 'README.md', 'CONTRIBUTING.md', 'MAINTENANCE.md', 'code-examples-index.md'}
    all_md_files = [f for f in all_md_files if f.name not in excluded]
    
    issues = []
    for file_path in sorted(all_md_files):
        is_valid, error_msg = has_proper_frontmatter(file_path)
        if not is_valid:
            issues.append((file_path, error_msg))
            if args.verbose:
                print(f"✗ {file_path}: {error_msg}")
    
    if issues:
        print(f"\n❌ Found {len(issues)} files with frontmatter issues:")
        for file_path, error_msg in issues:
            print(f"  ✗ {file_path}: {error_msg}")
        
        if args.fix:
            print("\n🔧 Auto-fixing files...")
            # Import the fix function (would need to be implemented)
            print("  (Auto-fix not yet implemented - use the comprehensive fix script)")
        
        print(f"\n💡 To fix, run:")
        print(f"   python website/scripts/validate-frontmatter.py --fix")
        print(f"   Or manually add frontmatter to each file")
        sys.exit(1)
    else:
        print(f"✅ All {len(all_md_files)} files have proper Jekyll frontmatter!")
        sys.exit(0)

if __name__ == '__main__':
    main()

