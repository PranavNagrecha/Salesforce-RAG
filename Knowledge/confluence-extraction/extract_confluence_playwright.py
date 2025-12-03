#!/usr/bin/env python3
"""
Advanced Confluence content extractor using Playwright for JavaScript-rendered pages.
Extracts content from The Detail Department Confluence space.
"""

import asyncio
from playwright.async_api import async_playwright
import re
import os
from pathlib import Path

BASE_URL = "https://tddprojects.atlassian.net/wiki/spaces/SF"

# Known page IDs and titles - using direct page URLs
PAGES = [
    {"title": "Rules for Fields", "page_id": "58818628", "url": f"{BASE_URL}/pages/58818628/Rules+for+Fields"},
    {"title": "Objects", "page_id": "58819722", "url": f"{BASE_URL}/pages/58819722/Objects"},
    {"title": "Contacts", "page_id": "58819722", "url": f"{BASE_URL}/pages/58819722/Contacts"},
    {"title": "DevOps Center", "page_id": "2441740432", "url": f"{BASE_URL}/pages/2441740432/DevOps+Center"},
    {"title": "Help", "page_id": "58819597", "url": f"{BASE_URL}/pages/58819597/Help"},
    {"title": "Salesforce API", "page_id": "58819638", "url": f"{BASE_URL}/pages/58819638/Salesforce+API"},
    {"title": "The Fancy Contact Page", "page_id": "2494824467", "url": f"{BASE_URL}/pages/2494824467/The+Fancy+Contact+Page"},
    {"title": "Salesforce Anywhere", "page_id": "1129513037", "url": f"{BASE_URL}/pages/1129513037/Salesforce+Anywhere"},
]

async def extract_page_content(page, url, title):
    """Extract content from a Confluence page using Playwright."""
    try:
        print(f"Loading: {title}...")
        await page.goto(url, wait_until="domcontentloaded", timeout=60000)
        
        # Wait a bit for JavaScript to render
        await page.wait_for_timeout(5000)
        
        # Try multiple strategies to find content
        content_text = None
        
        # Strategy 1: Try Confluence-specific selectors
        confluence_selectors = [
            'div[data-testid="content"]',
            'div.wiki-content',
            'div#content',
            'article',
            'main',
            '[role="main"]',
            '.ak-renderer-document',
            '.ak-renderer-page',
        ]
        
        for selector in confluence_selectors:
            try:
                element = await page.query_selector(selector)
                if element:
                    content_text = await element.inner_text()
                    if content_text and len(content_text) > 200:  # Ensure we got substantial content
                        print(f"  ✓ Found content using selector: {selector}")
                        break
            except Exception as e:
                continue
        
        # Strategy 2: Get all text from body and filter
        if not content_text or len(content_text) < 200:
            try:
                body = await page.query_selector('body')
                if body:
                    full_text = await body.inner_text()
                    # Debug: print first 500 chars to see what we're getting
                    print(f"  Debug: First 500 chars of body text: {full_text[:500]}")
                    
                    # Try to extract just the main content area
                    # Look for common patterns in Confluence pages
                    lines = full_text.split('\n')
                    # Filter out navigation, headers, footers
                    content_lines = []
                    skip_patterns = ['Skip to', 'Log in', 'Sign up', 'Search', 'Menu', 'Settings', 'Accept all cookies']
                    for line in lines:
                        line = line.strip()
                        if line and len(line) > 10 and not any(skip.lower() in line.lower() for skip in skip_patterns):
                            content_lines.append(line)
                    content_text = '\n'.join(content_lines)
                    
                    # If we still have substantial content, use it
                    if content_text and len(content_text) > 200:
                        print(f"  ✓ Extracted {len(content_text)} characters from body")
            except Exception as e:
                print(f"  Debug: Error in fallback extraction: {e}")
        
        # Final check - if we have any reasonable content, return it
        if content_text and len(content_text) > 100:
            return clean_text(content_text)
        else:
            print(f"  ✗ Content too short: {len(content_text) if content_text else 0} characters")
            return None
        
    except Exception as e:
        print(f"  ✗ Error: {str(e)}")
        return None

def clean_text(text):
    """Clean extracted text."""
    if not text:
        return ""
    # Remove extra whitespace but preserve line breaks
    lines = [line.strip() for line in text.split('\n')]
    lines = [line for line in lines if line]  # Remove empty lines
    return '\n\n'.join(lines)

def save_to_markdown(title, content, output_dir="../../Knowledge"):
    """Save extracted content to a markdown file."""
    if not content:
        return None
    
    # Create safe filename
    filename = re.sub(r'[^\w\s-]', '', title)
    filename = re.sub(r'[-\s]+', '-', filename)
    filename = f"TDD-{filename}.md"
    
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)
    
    filepath = output_path / filename
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(f"# {title}\n\n")
        f.write(f"**Source**: The Detail Department Confluence\n")
        f.write(f"**URL**: https://tddprojects.atlassian.net/wiki/spaces/SF\n\n")
        f.write("---\n\n")
        f.write(content)
    
    print(f"✅ Saved: {filepath}")
    return str(filepath)

async def main():
    """Main extraction function."""
    print("Starting Confluence content extraction with Playwright...")
    print("Note: This requires Playwright to be installed: pip install playwright && playwright install")
    
    async with async_playwright() as p:
        # Launch browser with realistic settings to avoid bot detection
        browser = await p.chromium.launch(
            headless=True,  # Keep headless but make it stealthy
            args=[
                '--disable-blink-features=AutomationControlled',
                '--disable-dev-shm-usage',
                '--no-sandbox',
            ]
        )
        context = await browser.new_context(
            user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            viewport={'width': 1920, 'height': 1080},
            locale='en-US',
            timezone_id='America/Los_Angeles',
        )
        # Remove webdriver property
        await context.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            });
        """)
        page = await context.new_page()
        
        extracted_count = 0
        
        for page_info in PAGES:
            title = page_info["title"]
            url = page_info["url"]
            
            print(f"\n{'='*60}")
            print(f"Extracting: {title}")
            print(f"URL: {url}")
            
            content = await extract_page_content(page, url, title)
            
            if content:
                save_to_markdown(title, content)
                extracted_count += 1
            else:
                print(f"⚠️  Failed to extract content for: {title}")
            
            # Be polite - wait between requests
            await asyncio.sleep(3)
        
        await browser.close()
        
        print(f"\n{'='*60}")
        print(f"Extraction complete! Extracted {extracted_count}/{len(PAGES)} pages.")

if __name__ == "__main__":
    asyncio.run(main())

