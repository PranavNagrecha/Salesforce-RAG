# Branch Deployment Guide (No GitHub Actions)

This guide explains how to deploy using branch-based deployment instead of GitHub Actions. This is simpler and more reliable.

## Quick Start

### 1. Build and Deploy Script

Run this command to build the site:

```bash
./website/scripts/build-and-deploy.sh
```

This will:
- ✅ Sync RAG index and homepage
- ✅ Update sitemap
- ✅ Build Jekyll site
- ✅ Copy built site to `docs/` folder

### 2. Commit and Push

```bash
git add docs/ rag/rag-index.md rag/rag-library.json website/root/index.md
git commit -m "Deploy: Update website"
git push origin main
```

### 3. Configure GitHub Pages

1. Go to: https://github.com/PranavNagrecha/Salesforce-RAG/settings/pages
2. Under "Source", select: **"Deploy from a branch"**
3. Branch: `main`
4. Folder: `/docs`
5. Click **"Save"**

GitHub Pages will automatically deploy from the `docs/` folder on the `main` branch.

## How It Works

1. **Build locally**: The script builds the Jekyll site locally
2. **Output to `docs/`**: The built site goes into the `docs/` folder
3. **GitHub serves it**: GitHub Pages serves the `docs/` folder automatically
4. **No Actions needed**: No GitHub Actions workflow required!

## Advantages

✅ **Simpler**: No complex workflow files
✅ **More reliable**: No "Cannot find run" errors
✅ **Faster**: Direct deployment, no workflow overhead
✅ **Easier to debug**: Build happens locally, you see errors immediately

## Disadvantages

❌ **Requires local build**: You need Ruby/Jekyll installed locally
❌ **Manual process**: You run the script yourself (but it's one command!)

## Setup (One-Time)

### Install Jekyll

```bash
# Install Ruby (if not installed)
# macOS:
brew install ruby

# Install Bundler
gem install bundler

# Install Jekyll dependencies
cd "/Users/pranavnagrecha/Salesforce for all"
bundle install
```

### Verify Setup

```bash
# Test Jekyll build
bundle exec jekyll build

# Should create _site/ folder
ls _site
```

## Daily Workflow

1. **Update RAG content** (edit markdown files)
2. **Run build script**:
   ```bash
   ./website/scripts/build-and-deploy.sh
   ```
3. **Commit and push**:
   ```bash
   git add docs/ rag/rag-index.md rag/rag-library.json website/root/index.md
   git commit -m "Update: [description]"
   git push origin main
   ```
4. **Wait 1-2 minutes** for GitHub Pages to rebuild
5. **Verify**: https://pranavnagrecha.github.io/Salesforce-RAG/

## Troubleshooting

### Build Fails

```bash
# Make sure dependencies are installed
bundle install

# Check Ruby version (need 3.1+)
ruby --version

# Try building manually
bundle exec jekyll build
```

### Site Not Updating

1. Check GitHub Pages settings: Source = "Deploy from a branch", Folder = "/docs"
2. Wait 2-3 minutes (GitHub needs time to rebuild)
3. Check: https://github.com/PranavNagrecha/Salesforce-RAG/settings/pages (should show "Last deployed")

### `docs/` Folder Not Created

Make sure the build script ran successfully:
```bash
./website/scripts/build-and-deploy.sh
```

Check if `_site/` exists (build output):
```bash
ls _site
```

## Disable GitHub Actions (Optional)

If you want to disable the GitHub Actions workflow:

1. Go to: https://github.com/PranavNagrecha/Salesforce-RAG/settings/actions
2. Under "Workflow permissions", you can disable Actions entirely
3. Or just delete `.github/workflows/deploy-website.yml`

## Summary

**Branch deployment is simpler and more reliable than GitHub Actions for static sites.**

Just run the build script, commit, and push. GitHub Pages handles the rest automatically!

