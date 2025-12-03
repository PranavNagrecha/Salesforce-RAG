#!/usr/bin/env python3
"""
Script to extract content from The Detail Department Confluence space.
Uses web scraping to extract page content and save as markdown files.
"""

import requests
from bs4 import BeautifulSoup
import re
import os
from urllib.parse import urljoin, urlparse
import time

BASE_URL = "https://tddprojects.atlassian.net/wiki"
SPACE_KEY = "SF"

# List of known page titles/URLs to extract
PAGES_TO_EXTRACT = [
    ("Rules for Fields", "58818628"),
    ("New Salesforce Org", None),  # Will need to find page ID
    ("Flow Triggers", None),
    ("Dynamic Forms", None),
    ("Clicks Or Code", None),
    ("Data Storage", None),
    ("Building a Simple Case Management Process", None),
]

def clean_text(text):
    """Clean extracted text."""
    if not text:
        return ""
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)
    # Remove leading/trailing whitespace
    text = text.strip()
    return text

def extract_page_content(page_id):
    """Extract content from a Confluence page."""
    url = f"{BASE_URL}/spaces/{SPACE_KEY}/pages/{page_id}"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Try to find the main content area
        # Confluence pages have different structures, try multiple selectors
        content_selectors = [
            'div[data-testid="content"]',
            'div.wiki-content',
            'div#content',
            'article',
            'main',
        ]
        
        content = None
        for selector in content_selectors:
            content = soup.select_one(selector)
            if content:
                break
        
        if not content:
            # Fallback: get body text
            content = soup.find('body')
        
        if content:
            # Extract text
            text = content.get_text(separator='\n', strip=True)
            return clean_text(text)
        else:
            return f"Could not extract content from {url}"
            
    except Exception as e:
        return f"Error extracting {url}: {str(e)}"

def save_to_markdown(title, content, output_dir="Knowledge"):
    """Save extracted content to a markdown file."""
    # Create safe filename
    filename = re.sub(r'[^\w\s-]', '', title)
    filename = re.sub(r'[-\s]+', '-', filename)
    filename = f"{filename}.md"
    
    filepath = os.path.join(output_dir, filename)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(f"# {title}\n\n")
        f.write(f"**Source**: The Detail Department Confluence\n")
        f.write(f"**URL**: https://tddprojects.atlassian.net/wiki/spaces/SF\n\n")
        f.write("---\n\n")
        f.write(content)
    
    print(f"Saved: {filepath}")
    return filepath

def main():
    """Main extraction function."""
    print("Starting Confluence content extraction...")
    
    # Extract known pages
    for title, page_id in PAGES_TO_EXTRACT:
        if page_id:
            print(f"\nExtracting: {title} (Page ID: {page_id})")
            content = extract_page_content(page_id)
            if content and not content.startswith("Error"):
                save_to_markdown(title, content)
            time.sleep(2)  # Be polite to the server
    
    print("\nExtraction complete!")

if __name__ == "__main__":
    main()

