# Fix GitHub Pages Deployment 404 Error

## Error Message
```
Error: Failed to create deployment (status: 404)
Error: Cannot find any run with github.run_id
```

## Root Cause
GitHub Pages is configured to deploy from a branch instead of GitHub Actions.

## Solution

### Step 1: Go to Repository Settings
1. Navigate to: https://github.com/PranavNagrecha/Salesforce-RAG/settings/pages
2. Or: Repository → Settings → Pages

### Step 2: Change Deployment Source
1. Under "Source", you'll see it's set to "Deploy from a branch"
2. **Change it to "GitHub Actions"**
3. Click "Save"

### Step 3: Re-run Workflow
1. Go to: https://github.com/PranavNagrecha/Salesforce-RAG/actions
2. Find the failed workflow run
3. Click "Re-run jobs" → "Re-run all jobs"

## Why This Happens

- GitHub Pages can deploy from:
  - **Branch**: Uses a branch (like `gh-pages` or `/docs` folder)
  - **GitHub Actions**: Uses the custom workflow we created

- Our workflow uses `actions/deploy-pages@v3` which requires:
  - Pages source set to "GitHub Actions"
  - `pages: write` permission (already in workflow)
  - `environment: github-pages` (already in workflow)

## Verification

After changing the source:
1. Workflow should complete successfully
2. Site will be deployed to: https://pranavnagrecha.github.io/Salesforce-RAG/
3. Deployment will show in repository Settings → Pages

## If Still Failing

1. Check repository permissions:
   - Settings → Actions → General
   - Ensure "Workflow permissions" allows "Read and write permissions"

2. Check Pages settings:
   - Ensure "GitHub Actions" is selected as source
   - No branch is selected

3. Re-run the workflow after making changes

