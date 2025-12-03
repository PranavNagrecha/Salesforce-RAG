#!/bin/bash
# Update RAG and Website Script
# 
# This script updates the RAG content and automatically updates the website.
# Run this after making changes to RAG files.
#
# Usage:
#   ./website/scripts/update-rag-and-website.sh
#   ./website/scripts/update-rag-and-website.sh --validate-only
#   ./website/scripts/update-rag-and-website.sh --commit "Your commit message"

set -e  # Exit on error

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Functions
print_header() {
    echo -e "\n${BLUE}========================================${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}========================================${NC}\n"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

# Parse arguments
VALIDATE_ONLY=false
COMMIT_MSG=""
DRY_RUN=false

while [[ $# -gt 0 ]]; do
    case $1 in
        --validate-only)
            VALIDATE_ONLY=true
            shift
            ;;
        --commit)
            COMMIT_MSG="$2"
            shift 2
            ;;
        --dry-run)
            DRY_RUN=true
            shift
            ;;
        --help|-h)
            echo "Usage: $0 [OPTIONS]"
            echo ""
            echo "Options:"
            echo "  --validate-only    Only validate, don't update files"
            echo "  --commit MSG       Commit changes with message"
            echo "  --dry-run          Show what would be done"
            echo "  --help, -h         Show this help message"
            exit 0
            ;;
        *)
            print_error "Unknown option: $1"
            echo "Use --help for usage information"
            exit 1
            ;;
    esac
done

# Change to project root
cd "$PROJECT_ROOT"

print_header "Salesforce RAG → Website Update Script"

# Reference lessons learned document
print_warning "📚 Important: See website/docs/LESSONS-LEARNED.md for critical lessons and best practices"

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    print_error "Python 3 is required but not installed."
    exit 1
fi

# Step 0: Validate Frontmatter (CRITICAL - must pass before proceeding)
print_header "Step 0: Validating Jekyll Frontmatter (CRITICAL)"

if [ "$VALIDATE_ONLY" = true ]; then
    print_warning "Validation mode: Would run: python3 website/scripts/validate-frontmatter.py"
else
    if [ "$DRY_RUN" = true ]; then
        echo "[DRY RUN] Would run: python3 website/scripts/validate-frontmatter.py"
    else
        if ! python3 website/scripts/validate-frontmatter.py; then
            print_error "Frontmatter validation failed! Fix issues before deploying."
            print_error "Run: python3 website/scripts/validate-frontmatter.py --verbose"
            exit 1
        fi
        print_success "All files have proper Jekyll frontmatter!"
    fi
fi

# Step 1: Sync RAG index, library JSON, and homepage
print_header "Step 1: Syncing RAG Index, Library JSON, and Homepage"

if [ "$VALIDATE_ONLY" = true ]; then
    print_warning "Validation mode: Skipping sync (would run: python3 website/scripts/sync-homepage.py)"
else
    if [ "$DRY_RUN" = true ]; then
        echo "[DRY RUN] Would run: python3 website/scripts/sync-homepage.py"
    else
        python3 website/scripts/sync-homepage.py
        print_success "RAG index, library JSON, and homepage synced!"
    fi
fi

# Step 2: Update website files (sitemap, links)
print_header "Step 2: Updating Website Files (Sitemap, Links)"

if [ "$VALIDATE_ONLY" = true ]; then
    python3 website/scripts/update-website.py --validate-only --verbose
    print_success "Validation complete!"
    exit 0
fi

if [ "$DRY_RUN" = true ]; then
    python3 website/scripts/update-website.py --dry-run --verbose
else
    python3 website/scripts/update-website.py --verbose
    print_success "Website files updated!"
fi

# Step 3: Validate changes
print_header "Step 3: Validating Changes"

if [ "$DRY_RUN" = false ] && [ "$VALIDATE_ONLY" = false ]; then
    python3 website/scripts/update-website.py --validate-only
    print_success "Validation complete!"
fi

# Step 4: Check for changes
print_header "Step 4: Checking for Changes"

if git diff --quiet && git diff --cached --quiet; then
    print_warning "No changes detected. Everything is up to date!"
    exit 0
fi

# Show what changed
echo "Changes detected:"
git status --short

# Step 5: Commit if requested
if [ -n "$COMMIT_MSG" ]; then
    print_header "Step 5: Committing Changes"
    
    if [ "$DRY_RUN" = true ]; then
        echo "[DRY RUN] Would commit with message: $COMMIT_MSG"
    else
        git add website/root/sitemap.xml
        git add rag/rag-index.md rag/rag-library.json 2>/dev/null || true
        git add website/root/index.md 2>/dev/null || true
        
        if git diff --cached --quiet; then
            print_warning "No changes to commit"
        else
            git commit -m "$COMMIT_MSG"
            print_success "Changes committed!"
            
            echo ""
            print_warning "Don't forget to push:"
            echo "  git push origin main"
        fi
    fi
else
    echo ""
    print_warning "Changes detected but not committed."
    echo "To commit, run:"
    echo "  $0 --commit 'Your commit message'"
    echo ""
    echo "Or commit manually:"
    echo "  git add rag/rag-index.md rag/rag-library.json website/root/index.md website/root/sitemap.xml"
    echo "  git commit -m 'Update website files'"
    echo "  git push origin main"
fi

# Step 6: Summary
print_header "Summary"

if [ "$DRY_RUN" = false ]; then
    print_success "Website update complete!"
    echo ""
    echo "Next steps:"
    echo "  1. Review changes: git diff"
    echo "  2. Commit: git add rag/rag-index.md rag/rag-library.json website/root/index.md website/root/sitemap.xml && git commit -m 'Update website'"
    echo "  3. Push: git push origin main"
    echo "  4. GitHub Pages will automatically rebuild (1-2 minutes)"
    echo ""
    echo "Your site will be available at:"
    echo "  https://pranavnagrecha.github.io/Salesforce-RAG/"
else
    print_success "Dry run complete! No changes made."
fi

