# Deployment Guide

This guide explains how to deploy your Salesforce RAG Knowledge Library website to GitHub Pages.

## Quick Deploy (Automated)

### Option 1: Use the Update Script (Recommended)

After updating RAG content, run:

```bash
# Update website and commit
./scripts/update-rag-and-website.sh --commit "Update RAG content and website"

# Or just update without committing
./scripts/update-rag-and-website.sh

# Validate only
./scripts/update-rag-and-website.sh --validate-only
```

Then push:
```bash
git push origin main
```

GitHub Actions will automatically:
1. Update the sitemap
2. Build the Jekyll site
3. Deploy to GitHub Pages

### Option 2: Manual Update

```bash
# 1. Update website files
python3 scripts/update-website.py

# 2. Review changes
git status
git diff sitemap.xml

# 3. Commit and push
git add sitemap.xml
git commit -m "Update website files"
git push origin main
```

## Initial Setup (One-Time)

### 1. Enable GitHub Pages

1. Go to your repository: `https://github.com/pranavnagrecha/Salesforce-RAG`
2. Navigate to **Settings** → **Pages**
3. Under **Source**, select:
   - **Source**: `GitHub Actions`
4. Click **Save**

### 2. Enable GitHub Actions

1. Go to **Settings** → **Actions** → **General**
2. Under **Workflow permissions**, select:
   - **Read and write permissions**
   - **Allow GitHub Actions to create and approve pull requests**
3. Click **Save**

### 3. Verify Setup

After pushing, check:
- **Actions** tab: Should show "Deploy Website" workflow running
- **Settings** → **Pages**: Should show deployment status

## Automated Deployment Workflow

The `.github/workflows/deploy-website.yml` workflow automatically:

1. **Triggers on**:
   - Push to `main` branch (when RAG files change)
   - Manual trigger via "Run workflow" button

2. **Runs**:
   - Updates sitemap.xml with all RAG files
   - Validates markdown files
   - Builds Jekyll site
   - Deploys to GitHub Pages

3. **Takes**: ~2-3 minutes

## Manual Deployment

If you need to deploy manually:

```bash
# 1. Update website files
python3 scripts/update-website.py

# 2. Install dependencies (if not already)
bundle install

# 3. Build site locally (optional, for testing)
bundle exec jekyll build

# 4. Commit and push
git add .
git commit -m "Update website"
git push origin main
```

## Testing Locally

Before deploying, test locally:

```bash
# Install dependencies
bundle install

# Build site
bundle exec jekyll build

# Serve locally (optional)
bundle exec jekyll serve

# Visit: http://localhost:4000/Salesforce-RAG/
```

## Troubleshooting

### Site Not Building

1. **Check GitHub Actions**:
   - Go to **Actions** tab
   - Check for failed workflows
   - Review build logs

2. **Common Issues**:
   - **Jekyll errors**: Check `_config.yml` syntax
   - **Missing files**: Ensure all files are committed
   - **Permission errors**: Check GitHub Actions permissions

3. **Fix and Retry**:
   ```bash
   # Fix issues
   python3 scripts/update-website.py --validate-only
   
   # Commit fix
   git add .
   git commit -m "Fix website build"
   git push origin main
   ```

### Sitemap Not Updating

1. **Check script output**:
   ```bash
   python3 scripts/update-website.py --verbose
   ```

2. **Verify files are found**:
   - Check that markdown files are in `rag/` directory
   - Ensure files aren't in excluded directories

3. **Manual update**:
   ```bash
   python3 scripts/update-website.py
   git add sitemap.xml
   git commit -m "Update sitemap"
   git push origin main
   ```

### Pages Not Indexing

1. **Submit to Google Search Console**:
   - Go to [Google Search Console](https://search.google.com/search-console)
   - Add property: `https://pranavnagrecha.github.io/Salesforce-RAG/`
   - Submit sitemap: `https://pranavnagrecha.github.io/Salesforce-RAG/sitemap.xml`

2. **Check robots.txt**:
   - Verify it's not blocking pages
   - Check: `https://pranavnagrecha.github.io/Salesforce-RAG/robots.txt`

3. **Wait**: Google indexing takes 1-2 weeks

## Workflow Summary

### Daily Workflow

```bash
# 1. Update RAG content (edit markdown files)
# 2. Update website
./scripts/update-rag-and-website.sh --commit "Update: [description]"

# 3. Push
git push origin main

# 4. Wait 2-3 minutes for GitHub Pages to rebuild
# 5. Verify at: https://pranavnagrecha.github.io/Salesforce-RAG/
```

### Weekly Workflow

1. Review Google Search Console for indexing status
2. Check Analytics (if configured) for traffic
3. Update sitemap if new content added
4. Review and fix any broken links

## Monitoring

### Check Deployment Status

1. **GitHub Pages**: Settings → Pages → See deployment status
2. **GitHub Actions**: Actions tab → See workflow runs
3. **Site**: Visit your site URL

### Monitor SEO

1. **Google Search Console**: Track indexing and search performance
2. **Google Analytics**: Monitor traffic (if configured)
3. **PageSpeed Insights**: Check performance

## Best Practices

1. **Always validate before committing**:
   ```bash
   ./scripts/update-rag-and-website.sh --validate-only
   ```

2. **Use descriptive commit messages**:
   ```bash
   ./scripts/update-rag-and-website.sh --commit "Add: New Apex pattern for batch processing"
   ```

3. **Test locally before pushing** (optional):
   ```bash
   bundle exec jekyll serve
   ```

4. **Monitor after deployment**:
   - Check GitHub Actions for errors
   - Verify site loads correctly
   - Check sitemap is updated

## Advanced: Custom Domain (Optional)

If you want a custom domain:

1. Add `CNAME` file to root:
   ```
   yourdomain.com
   ```

2. Update `_config.yml`:
   ```yaml
   url: https://yourdomain.com
   baseurl: ""
   ```

3. Configure DNS (see GitHub Pages docs)

## Support

- **GitHub Issues**: Report problems in repository
- **GitHub Pages Docs**: https://docs.github.com/en/pages
- **Jekyll Docs**: https://jekyllrb.com/docs/

---

**Remember**: Every push to `main` automatically triggers a rebuild. Just update your RAG content and push!

