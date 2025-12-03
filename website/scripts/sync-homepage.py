#!/usr/bin/env python3
"""
Automatically sync homepage categories with rag-index.md

This script:
1. Scans rag-index.md for all section headings
2. Checks homepage for matching categories
3. Adds missing categories automatically
4. Updates descriptions to match rag-index.md exactly
5. Ensures all links work correctly

Just run: python website/scripts/sync-homepage.py
"""

import re
import sys
from pathlib import Path

# Emoji mapping for categories
EMOJI_MAP = {
    "Architecture Patterns": "🏗️",
    "Integration Patterns": "🔌",
    "Identity and SSO": "🔐",
    "Data Modeling": "📊",
    "Security": "🔒",
    "Best Practices": "⭐",
    "Development": "💻",
    "Troubleshooting": "🔧",
    "Patterns": "🔀",
    "Glossary": "📖",
    "Project Methods": "📋",
    "Operations": "🚀",
    "Observability": "📊",
    "Data Governance": "🛡️",
    "Adoption": "👥",
    "Testing": "✅",
    "Quick Start Guides": "⚡",
    "API Reference": "📚",
    "MCP Knowledge": "🔧",
    "Code Examples": "📝",
}

# Sections to exclude (meta/documentation sections)
EXCLUDE_SECTIONS = {
    "Overview",
    "How to use this index",
    "Directory Structure",
    "Retrieval Guidelines",
    "Terminology",
    "File Status",
    "Maintenance",
}


def get_anchor_id(section_name):
    """Convert section name to anchor ID (lowercase, hyphens)"""
    return section_name.lower().replace(" ", "-").replace("&", "and")


def extract_sections_from_index(rag_index_path):
    """Extract all sections from rag-index.md"""
    sections = []
    
    with open(rag_index_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find all ## headings
    pattern = r'^## (.+)$'
    for match in re.finditer(pattern, content, re.MULTILINE):
        section_name = match.group(1).strip()
        
        if section_name in EXCLUDE_SECTIONS:
            continue
        
        # Get description (next line after heading)
        lines = content[match.end():].split('\n')
        description = ""
        for line in lines[1:3]:  # Check next 2 lines
            line = line.strip()
            if line and not line.startswith('-') and not line.startswith('#'):
                description = line
                break
        
        sections.append({
            'name': section_name,
            'description': description,
            'anchor': get_anchor_id(section_name)
        })
    
    return sections


def extract_categories_from_homepage(homepage_path):
    """Extract existing categories from homepage"""
    categories = {}
    
    with open(homepage_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find all domain-card entries
    pattern = r'<h3><a href="[^"]*#([^"]+)">[^<]*([^<]+)</a></h3>\s*<p>([^<]+)</p>'
    for match in re.finditer(pattern, content, re.DOTALL):
        anchor = match.group(1)
        name = match.group(2).strip()
        # Remove emoji if present
        name = re.sub(r'^[^\w\s]*\s*', '', name)
        description = match.group(3).strip()
        
        categories[anchor] = {
            'name': name,
            'description': description
        }
    
    return categories


def generate_card_html(section):
    """Generate HTML for a domain card"""
    emoji = EMOJI_MAP.get(section['name'], "📄")
    display_name = section['name']
    
    # Handle "Quick Start Guides" -> "Quick Start" for display
    if section['name'] == "Quick Start Guides":
        display_name = "Quick Start"
    
    return f'''  <div class="domain-card">
    <h3><a href="{{{{ '/rag/rag-index.html' | relative_url }}}}#{section['anchor']}">{emoji} {display_name}</a></h3>
    <p>{section['description']}</p>
  </div>'''


def update_homepage(rag_index_path, homepage_path):
    """Update homepage with all categories from rag-index.md"""
    
    print("📖 Scanning rag-index.md...")
    sections = extract_sections_from_index(rag_index_path)
    print(f"   Found {len(sections)} categories")
    
    print("🏠 Checking current homepage...")
    existing_categories = extract_categories_from_homepage(homepage_path)
    print(f"   Found {len(existing_categories)} existing categories")
    
    # Read homepage
    with open(homepage_path, 'r', encoding='utf-8') as f:
        homepage_content = f.read()
    
    # Find the domain-grid section
    grid_start = homepage_content.find('<div class="domain-grid">')
    grid_end = homepage_content.find('</div>', grid_start) + 6
    
    if grid_start == -1:
        print("❌ ERROR: Could not find domain-grid section!")
        return False
    
    # Generate all cards
    print("🔄 Generating cards...")
    cards = []
    for section in sections:
        cards.append(generate_card_html(section))
    
    # Replace the grid content
    new_grid = '<div class="domain-grid">\n' + '\n  \n'.join(cards) + '\n</div>'
    new_homepage = homepage_content[:grid_start] + new_grid + homepage_content[grid_end:]
    
    # Write updated homepage
    with open(homepage_path, 'w', encoding='utf-8') as f:
        f.write(new_homepage)
    
    print(f"✅ Updated homepage with {len(sections)} categories")
    print(f"   Added: {len(sections) - len(existing_categories)} new categories")
    print(f"   Updated: {len(existing_categories)} existing categories")
    
    return True


def main():
    """Main function"""
    repo_root = Path(__file__).parent.parent.parent
    rag_index_path = repo_root / 'rag' / 'rag-index.md'
    homepage_path = repo_root / 'website' / 'root' / 'index.md'
    
    if not rag_index_path.exists():
        print(f"❌ ERROR: {rag_index_path} not found!")
        sys.exit(1)
    
    if not homepage_path.exists():
        print(f"❌ ERROR: {homepage_path} not found!")
        sys.exit(1)
    
    print("🚀 Syncing homepage with rag-index.md...\n")
    
    success = update_homepage(rag_index_path, homepage_path)
    
    if success:
        print("\n✅ Done! Homepage is now in sync with rag-index.md")
        print("   Run: git add website/root/index.md && git commit -m 'Auto-sync homepage categories'")
    else:
        print("\n❌ Failed to update homepage")
        sys.exit(1)


if __name__ == '__main__':
    main()

