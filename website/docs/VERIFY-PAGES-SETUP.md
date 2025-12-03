# How to Verify GitHub Pages is Set Up Correctly

## Quick Check

1. **Go to**: https://github.com/PranavNagrecha/Salesforce-RAG/settings/pages

2. **Look at "Build and deployment" section**

3. **Check the "Source" dropdown**:
   - ✅ **CORRECT**: Shows "GitHub Actions" 
   - ❌ **WRONG**: Shows "Deploy from a branch" with a branch name (like `main` or `gh-pages`)

## If It's Wrong

1. Click the "Source" dropdown
2. Select **"GitHub Actions"**
3. Click **"Save"**
4. Wait 10-20 seconds for GitHub to update
5. Go to Actions tab and re-run the failed workflow

## Visual Guide

**CORRECT Setup:**
```
Build and deployment
Source: [GitHub Actions ▼]
```

**WRONG Setup:**
```
Build and deployment  
Source: [Deploy from a branch ▼]
Branch: [main / (root) ▼]
```

## Still Not Working?

### Check 1: Environment Exists
1. Go to: https://github.com/PranavNagrecha/Salesforce-RAG/settings/environments
2. You should see "github-pages" environment listed
3. If not, the first workflow run should create it (but it needs Pages source = GitHub Actions first)

### Check 2: Workflow Permissions
1. Go to: https://github.com/PranavNagrecha/Salesforce-RAG/settings/actions
2. Scroll to "Workflow permissions"
3. Should be: **"Read and write permissions"**
4. If not, change it and save

### Check 3: Repository Visibility
- Public repos: GitHub Pages works automatically
- Private repos: Need GitHub Pro/Team/Enterprise plan

## Test After Fixing

1. Make a small change (or empty commit):
   ```bash
   git commit --allow-empty -m "Test Pages deployment"
   git push origin main
   ```

2. Watch the workflow: https://github.com/PranavNagrecha/Salesforce-RAG/actions

3. Should complete successfully now!

## Common Mistakes

❌ **Mistake 1**: Setting source to a branch (like `main`) instead of "GitHub Actions"
❌ **Mistake 2**: Not clicking "Save" after changing the source
❌ **Mistake 3**: Re-running workflow before GitHub finishes updating the settings (wait 10-20 seconds)

✅ **Correct**: Source = "GitHub Actions", then wait, then re-run workflow

