# Fix GitHub Pages 404 Deployment Error

## The Error

```
Error: Failed to create deployment (status: 404)
Error: Cannot find any run with github.run_id
```

## Root Cause

This error occurs when GitHub Pages is **NOT configured to use GitHub Actions** as the deployment source. The workflow is trying to deploy, but GitHub Pages doesn't recognize it because the repository settings are wrong.

## Solution (REQUIRED - Do This Now)

### Step 1: Go to Repository Settings

1. Open: https://github.com/PranavNagrecha/Salesforce-RAG/settings/pages
2. Or navigate: Repository → Settings → Pages

### Step 2: Check the Source Setting

**CRITICAL**: Under "Build and deployment", the "Source" dropdown MUST be set to:

✅ **"GitHub Actions"** ← This is what it should be

❌ **NOT "Deploy from a branch"** ← If it's this, that's the problem!

### Step 3: Change It If Needed

1. If it says "Deploy from a branch", click the dropdown
2. Select **"GitHub Actions"**
3. Click **"Save"**

### Step 4: Verify

After saving, you should see:
- Source: **GitHub Actions** (not a branch name)
- No branch selected
- The workflow will now be able to deploy

### Step 5: Re-run the Workflow

1. Go to: https://github.com/PranavNagrecha/Salesforce-RAG/actions
2. Find the failed workflow run
3. Click **"Re-run jobs"** → **"Re-run all jobs"**

## Why This Happens

- **GitHub Pages** can deploy from two sources:
  1. **Branch**: Uses a branch like `gh-pages` or `/docs` folder
  2. **GitHub Actions**: Uses our custom workflow (`.github/workflows/deploy-website.yml`)

- Our workflow uses `actions/deploy-pages@v3` which **REQUIRES**:
  - Pages source = **"GitHub Actions"**
  - `pages: write` permission (already in workflow ✅)
  - `environment: github-pages` (already in workflow ✅)

- If the source is set to "Deploy from a branch", GitHub Pages API returns 404 because it's looking for a branch deployment, not an Actions deployment.

## Verification Checklist

After fixing:

- [ ] Repository Settings → Pages → Source = **"GitHub Actions"**
- [ ] No branch is selected
- [ ] Workflow has `environment: github-pages` ✅ (already set)
- [ ] Workflow has `pages: write` permission ✅ (already set)
- [ ] Re-run the workflow
- [ ] Deployment succeeds

## If Still Failing

1. **Check repository permissions**:
   - Settings → Actions → General
   - "Workflow permissions" = "Read and write permissions"

2. **Check if environment exists**:
   - Settings → Environments
   - Should see "github-pages" environment
   - If not, the first workflow run should create it

3. **Try manual trigger**:
   - Actions → Deploy Website → "Run workflow" button
   - This sometimes helps initialize the environment

## Quick Test

After changing the source to "GitHub Actions", push any small change to trigger the workflow:

```bash
git commit --allow-empty -m "Test deployment"
git push origin main
```

Then watch: https://github.com/PranavNagrecha/Salesforce-RAG/actions

The deployment should now succeed!

