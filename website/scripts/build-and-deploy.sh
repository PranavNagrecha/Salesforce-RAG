#!/bin/bash
# Build and deploy website to GitHub Pages using branch deployment
# This is simpler and more reliable than GitHub Actions

set -e

echo "🚀 Building and deploying website..."

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Step 1: Update RAG index and homepage
echo -e "${BLUE}📝 Step 1: Syncing RAG index and homepage...${NC}"
python3 website/scripts/sync-homepage.py

# Step 2: Update website files (sitemap)
echo -e "${BLUE}📝 Step 2: Updating website files (sitemap)...${NC}"
python3 website/scripts/update-website.py --verbose

# Step 3: Copy website files to root (Jekyll needs them in root)
echo -e "${BLUE}📝 Step 3: Preparing Jekyll directories...${NC}"
if [ -d "website/_layouts" ]; then
  cp -r website/_layouts _layouts
fi
if [ -d "website/assets" ]; then
  cp -r website/assets assets
fi
if [ -d "website/root" ]; then
  cp website/root/* .
fi

# Step 4: Install Jekyll dependencies
echo -e "${BLUE}📝 Step 4: Installing Jekyll dependencies...${NC}"
bundle install

# Step 5: Build Jekyll site
echo -e "${BLUE}📝 Step 5: Building Jekyll site...${NC}"
JEKYLL_ENV=production bundle exec jekyll build

# Step 6: Copy built site to docs/ folder (for branch deployment)
echo -e "${BLUE}📝 Step 6: Copying built site to docs/ folder...${NC}"
rm -rf docs
cp -r _site docs

# Step 7: Clean up temporary files
echo -e "${BLUE}📝 Step 7: Cleaning up...${NC}"
rm -rf _layouts assets _config.yml Gemfile Gemfile.lock .nojekyll robots.txt sitemap.xml

echo -e "${GREEN}✅ Build complete! Site is in docs/ folder${NC}"
echo -e "${GREEN}📤 Next steps:${NC}"
echo "   1. Review changes: git status"
echo "   2. Commit: git add docs/ rag/rag-index.md rag/rag-library.json website/root/index.md"
echo "   3. Push: git push origin main"
echo "   4. GitHub Pages will automatically deploy from docs/ folder"

