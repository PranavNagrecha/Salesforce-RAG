/**
 * Simple client-side search for Jekyll site
 * Searches through page titles and descriptions
 */

(function() {
    'use strict';
    
    // Search index - will be populated from page data
    let searchIndex = [];
    let searchInput = null;
    let searchResults = null;
    let isIndexed = false;
    
    /**
     * Initialize search functionality
     */
    function initSearch() {
        // Get existing search container (created in layout) or create it
        let searchContainer = document.getElementById('search-container');
        if (!searchContainer) {
            searchContainer = document.createElement('div');
            searchContainer.id = 'search-container';
            searchContainer.className = 'search-container';
            searchContainer.style.display = 'none';
            searchContainer.innerHTML = `
                <div class="search-box">
                    <input type="text" id="search-input" placeholder="Search knowledge base... (Ctrl+K)" autocomplete="off">
                    <button id="search-close" class="search-close" aria-label="Close search">×</button>
                </div>
                <div id="search-results" class="search-results"></div>
            `;
            
            // Add to page (after header)
            const header = document.querySelector('.site-header');
            if (header) {
                header.parentNode.insertBefore(searchContainer, header.nextSibling);
            }
        }
        
        searchInput = document.getElementById('search-input');
        searchResults = document.getElementById('search-results');
        const searchClose = document.getElementById('search-close');
        const searchToggle = document.getElementById('search-toggle');
        
        if (!searchInput || !searchResults) {
            console.warn('Search elements not found');
            return;
        }
        
        // Build search index from current page
        buildSearchIndex();
        
        // Event listeners
        searchInput.addEventListener('input', handleSearch);
        searchInput.addEventListener('focus', showResults);
        if (searchClose) {
            searchClose.addEventListener('click', closeSearch);
        }
        if (searchToggle) {
            searchToggle.addEventListener('click', function() {
                searchContainer.style.display = searchContainer.style.display === 'none' ? 'block' : 'none';
                if (searchContainer.style.display === 'block') {
                    searchInput.focus();
                }
            });
        }
        
        document.addEventListener('click', function(e) {
            if (!searchContainer.contains(e.target) && 
                e.target !== searchInput && 
                e.target !== searchToggle) {
                closeSearch();
            }
        });
        
        // Keyboard shortcuts
        document.addEventListener('keydown', function(e) {
            // Ctrl/Cmd + K to toggle search
            if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
                e.preventDefault();
                const isVisible = searchContainer.style.display !== 'none';
                searchContainer.style.display = isVisible ? 'none' : 'block';
                if (!isVisible) {
                    searchInput.focus();
                }
            }
            // Escape to close
            if (e.key === 'Escape') {
                closeSearch();
            }
        });
    }
    
    /**
     * Build search index from page content
     */
    function buildSearchIndex() {
        if (isIndexed) return;
        
        // Get all links to RAG pages
        const links = document.querySelectorAll('a[href*="/rag/"]');
        links.forEach(link => {
            const href = link.getAttribute('href');
            const text = link.textContent.trim();
            const parent = link.closest('.domain-card, li, p');
            let description = '';
            
            if (parent) {
                const descElement = parent.querySelector('p');
                if (descElement) {
                    description = descElement.textContent.trim();
                }
            }
            
            // Only index actual content pages (not index pages)
            if (href && href.includes('.html') && !href.includes('rag-index.html')) {
                searchIndex.push({
                    title: text,
                    url: href,
                    description: description || text,
                    keywords: (text + ' ' + description).toLowerCase()
                });
            }
        });
        
        // Also index homepage cards
        const cards = document.querySelectorAll('.domain-card');
        cards.forEach(card => {
            const link = card.querySelector('a');
            const desc = card.querySelector('p');
            if (link && desc) {
                const title = link.textContent.trim();
                const url = link.getAttribute('href');
                const description = desc.textContent.trim();
                
                searchIndex.push({
                    title: title,
                    url: url,
                    description: description,
                    keywords: (title + ' ' + description).toLowerCase(),
                    isCategory: true
                });
            }
        });
        
        isIndexed = true;
    }
    
    /**
     * Handle search input
     */
    function handleSearch(e) {
        const query = e.target.value.trim().toLowerCase();
        
        if (query.length < 2) {
            searchResults.innerHTML = '';
            searchResults.style.display = 'none';
            return;
        }
        
        const results = searchIndex.filter(item => {
            return item.keywords.includes(query);
        }).slice(0, 10); // Limit to 10 results
        
        displayResults(results, query);
    }
    
    /**
     * Display search results
     */
    function displayResults(results, query) {
        if (results.length === 0) {
            searchResults.innerHTML = '<div class="search-no-results">No results found. Try different keywords.</div>';
            searchResults.style.display = 'block';
            return;
        }
        
        const html = results.map(item => {
            const title = highlightMatch(item.title, query);
            const desc = item.description ? highlightMatch(item.description.substring(0, 120), query) : '';
            const badge = item.isCategory ? '<span class="search-badge">Category</span>' : '';
            
            return `
                <a href="${item.url}" class="search-result-item">
                    <div class="search-result-title">${title} ${badge}</div>
                    ${desc ? `<div class="search-result-desc">${desc}${item.description.length > 120 ? '...' : ''}</div>` : ''}
                </a>
            `;
        }).join('');
        
        searchResults.innerHTML = html;
        searchResults.style.display = 'block';
    }
    
    /**
     * Highlight matching text
     */
    function highlightMatch(text, query) {
        if (!query) return text;
        const regex = new RegExp(`(${query})`, 'gi');
        return text.replace(regex, '<mark>$1</mark>');
    }
    
    /**
     * Show search results (if they exist)
     */
    function showResults() {
        if (searchResults && searchResults.innerHTML) {
            searchResults.style.display = 'block';
        }
    }
    
    /**
     * Close search
     */
    function closeSearch() {
        const searchContainer = document.getElementById('search-container');
        if (searchContainer) {
            searchContainer.style.display = 'none';
        }
        if (searchResults) {
            searchResults.style.display = 'none';
        }
        if (searchInput) {
            searchInput.value = '';
        }
    }
    
    /**
     * Show search
     */
    function showSearch() {
        const searchContainer = document.getElementById('search-container');
        if (searchContainer) {
            searchContainer.style.display = 'block';
            if (searchInput) {
                searchInput.focus();
            }
        }
    }
    
    // Initialize when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initSearch);
    } else {
        initSearch();
    }
})();

