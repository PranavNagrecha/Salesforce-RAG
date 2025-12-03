/**
 * Client-side search functionality for Salesforce RAG Knowledge Library
 * Supports keyboard shortcuts (Ctrl+K) and accessible search interface
 */

(function() {
  'use strict';

  // Search configuration
  const SEARCH_CONFIG = {
    shortcutKey: 'k',
    minQueryLength: 2,
    maxResults: 20,
    debounceDelay: 300
  };

  // DOM elements
  let searchToggle = null;
  let searchContainer = null;
  let searchInput = null;
  let searchClose = null;
  let searchResults = null;
  let searchData = null;

  // State
  let isOpen = false;
  let debounceTimer = null;

  /**
   * Initialize search functionality
   */
  function init() {
    // Get DOM elements
    searchToggle = document.getElementById('search-toggle');
    searchContainer = document.getElementById('search-container');
    searchInput = document.getElementById('search-input');
    searchClose = document.getElementById('search-close');
    searchResults = document.getElementById('search-results');

    if (!searchToggle || !searchContainer || !searchInput || !searchClose || !searchResults) {
      console.warn('Search elements not found');
      return;
    }

    // Load search data
    loadSearchData();

    // Event listeners
    searchToggle.addEventListener('click', toggleSearch);
    searchClose.addEventListener('click', closeSearch);
    searchInput.addEventListener('input', handleSearch);
    searchInput.addEventListener('keydown', handleKeydown);

    // Keyboard shortcut (Ctrl+K or Cmd+K)
    document.addEventListener('keydown', function(e) {
      if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === SEARCH_CONFIG.shortcutKey) {
        e.preventDefault();
        toggleSearch();
      }
    });

    // Close on Escape
    document.addEventListener('keydown', function(e) {
      if (e.key === 'Escape' && isOpen) {
        closeSearch();
      }
    });

    // Close on click outside
    document.addEventListener('click', function(e) {
      if (isOpen && !searchContainer.contains(e.target) && e.target !== searchToggle) {
        closeSearch();
      }
    });
  }

  /**
   * Load search data from rag-library.json
   */
  async function loadSearchData() {
    try {
      const response = await fetch('/Salesforce-RAG/rag/rag-library.json');
      if (!response.ok) {
        throw new Error('Failed to load search data');
      }
      const data = await response.json();
      searchData = data.files || [];
    } catch (error) {
      console.error('Error loading search data:', error);
      searchData = [];
    }
  }

  /**
   * Toggle search container
   */
  function toggleSearch() {
    if (isOpen) {
      closeSearch();
    } else {
      openSearch();
    }
  }

  /**
   * Open search container
   */
  function openSearch() {
    isOpen = true;
    searchContainer.style.display = 'block';
    searchInput.focus();
    searchToggle.setAttribute('aria-expanded', 'true');
    
    // Update ARIA
    searchContainer.setAttribute('aria-hidden', 'false');
  }

  /**
   * Close search container
   */
  function closeSearch() {
    isOpen = false;
    searchContainer.style.display = 'none';
    searchInput.value = '';
    searchResults.innerHTML = '';
    searchToggle.setAttribute('aria-expanded', 'false');
    
    // Update ARIA
    searchContainer.setAttribute('aria-hidden', 'true');
  }

  /**
   * Handle search input
   */
  function handleSearch() {
    clearTimeout(debounceTimer);
    
    debounceTimer = setTimeout(() => {
      const query = searchInput.value.trim();
      
      if (query.length < SEARCH_CONFIG.minQueryLength) {
        searchResults.innerHTML = '';
        return;
      }

      performSearch(query);
    }, SEARCH_CONFIG.debounceDelay);
  }

  /**
   * Perform search
   */
  function performSearch(query) {
    if (!searchData || searchData.length === 0) {
      searchResults.innerHTML = '<p>Search data not loaded. Please refresh the page.</p>';
      return;
    }

    const lowerQuery = query.toLowerCase();
    const results = searchData
      .filter(file => {
        const title = (file.title || '').toLowerCase();
        const description = (file.description || '').toLowerCase();
        const content = (file.summary || '').toLowerCase();
        const path = (file.path || '').toLowerCase();
        
        return title.includes(lowerQuery) ||
               description.includes(lowerQuery) ||
               content.includes(lowerQuery) ||
               path.includes(lowerQuery);
      })
      .slice(0, SEARCH_CONFIG.maxResults);

    displayResults(results, query);
  }

  /**
   * Display search results
   */
  function displayResults(results, query) {
    if (results.length === 0) {
      searchResults.innerHTML = `<p>No results found for "${query}"</p>`;
      return;
    }

    const html = results.map(file => {
      const title = file.title || file.path || 'Untitled';
      const description = file.description || file.summary || '';
      let url = file.url || file.path || '#';
      
      // Ensure URL has proper base path
      // If URL doesn't start with /, it's relative - prepend /Salesforce-RAG/rag/
      // If URL starts with /rag/, prepend /Salesforce-RAG
      // If URL already starts with /Salesforce-RAG/, use as-is
      if (!url.startsWith('/')) {
        url = '/Salesforce-RAG/rag/' + url;
      } else if (url.startsWith('/rag/')) {
        url = '/Salesforce-RAG' + url;
      } else if (!url.startsWith('/Salesforce-RAG/')) {
        url = '/Salesforce-RAG' + url;
      }
      
      const path = file.path || '';

      return `
        <div class="search-result-item">
          <h4><a href="${url}">${highlightMatch(title, query)}</a></h4>
          <p class="search-result-path">${path}</p>
          <p class="search-result-description">${highlightMatch(description.substring(0, 150), query)}${description.length > 150 ? '...' : ''}</p>
        </div>
      `;
    }).join('');

    searchResults.innerHTML = html;
  }

  /**
   * Highlight matching text in results
   */
  function highlightMatch(text, query) {
    if (!query) return text;
    
    const regex = new RegExp(`(${query})`, 'gi');
    return text.replace(regex, '<mark>$1</mark>');
  }

  /**
   * Handle keyboard navigation in search
   */
  function handleKeydown(e) {
    // Allow Enter to navigate to first result
    if (e.key === 'Enter') {
      const firstResult = searchResults.querySelector('.search-result-item a');
      if (firstResult) {
        firstResult.click();
      }
    }
  }

  // Initialize when DOM is ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();

