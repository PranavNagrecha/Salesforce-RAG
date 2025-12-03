# Website Rules and Guidelines

## 🚀 Quick Start: Auto-Sync Everything

**Just run this command:**
```bash
python website/scripts/sync-homepage.py
```

That's it. The script will:
- ✅ **Scan `rag/` folder** for all .md files
- ✅ **Rebuild `rag-index.md`** from actual files (not just reference it)
- ✅ **Rebuild `rag-library.json`** with all file metadata and statistics
- ✅ **Find all categories** automatically
- ✅ **Add missing categories** to homepage
- ✅ **Update all descriptions** to match exactly
- ✅ **Ensure all links** work correctly

**Or use the complete update script:**
```bash
website/scripts/update-rag-and-website.sh
```

This script orchestrates the complete workflow:
1. Runs `sync-homepage.py` (rebuilds `rag-index.md`, `rag-library.json`, and updates homepage)
2. Runs `update-website.py` (generates sitemap, fixes links)
3. Validates all changes
4. Optionally commits changes

**Then commit:**
```bash
git add rag/rag-index.md rag/rag-library.json website/root/index.md website/root/sitemap.xml
git commit -m "Auto-sync RAG index, library JSON, and homepage"
git push
```

---

## General Principles

1. **Automation First**: Use `sync-homepage.py` - don't manually edit homepage categories
2. **Consistency**: All content must match between homepage and `rag-index.md`
3. **User Experience**: Navigation should be intuitive and all links must work
4. **SEO Optimization**: All pages must have proper meta tags, descriptions, and structured data
5. **Accessibility**: Follow WCAG 2.1 AA standards for accessibility
6. **Mobile Responsive**: All layouts must work on mobile, tablet, and desktop

## Homepage Rules

### Category Cards

**CRITICAL RULE**: **Homepage cards are created DYNAMICALLY based on actual folder contents.**

1. **Auto-Sync Only**: Use `sync-homepage.py` to update homepage - don't manually edit
2. **Must Match Index**: Homepage card descriptions MUST exactly match `rag-index.md` section descriptions
3. **Card Creation Rule**: 
   - **Empty folder = NO card** (folder exists but has zero .md files)
   - **Folder with files = YES card** (folder has at least ONE .md file)
   - Cards are created automatically for ALL folders that have files
4. **Dynamic Coverage**: The script scans `rag/` folder structure and creates cards for:
   - Every main folder that contains at least one .md file
   - Currently: API Reference, Adoption, Architecture Patterns, Best Practices, Code Examples, Data Governance, Data Modeling, Development, Glossary, Identity and SSO, Integration Patterns, MCP Knowledge, Observability, Operations, Patterns, Project Methods, Quick Start Guides, Security, Testing, Troubleshooting
5. **No Duplicates**: Each category appears exactly once on the homepage
6. **Consistent Formatting**: All cards follow the same structure (script handles this)
7. **Automatic Updates**: When you add a file to an empty folder, the next sync will create its card

### When Adding New Files to rag/

1. **Add your .md file** to the appropriate folder in `rag/`
2. **CRITICAL: Add Jekyll frontmatter** to your new file:
   ```yaml
   ---
   layout: default
   title: Your Page Title
   description: Brief description of the page content
   permalink: /rag/your-folder/your-file.html
   ---
   ```
   - **Without frontmatter, the file will NOT generate an HTML page and links will return 404**
3. **Run**: `python website/scripts/sync-homepage.py` (or `website/scripts/update-rag-and-website.sh`)
4. The script will:
   - Find your new file automatically
   - Add it to `rag-index.md`
   - Add it to `rag-library.json` with metadata
   - **If this is the FIRST file in a folder**: Create a new homepage card for that folder
   - **If folder already had files**: Update existing card
   - Update statistics and coverage counts
5. Commit changes:
   ```bash
   git add rag/your-folder/your-file.md rag/rag-index.md rag/rag-library.json website/root/index.md
   git commit -m "Add new RAG file: [filename]"
   git push
   ```
6. Done!

**Remember: Frontmatter is REQUIRED - files without it will not work!**

**Note**: Empty folders (with zero .md files) will NOT get homepage cards. As soon as you add the first file, the card will appear.

### Link Rules

1. **Use Jekyll Filters**: Always use `{{ '/path' | relative_url }}` for internal links in HTML/templates
2. **Relative Paths in Markdown**: In markdown files (like rag-index.md and all content files), use **relative paths** (e.g., `adoption/org-health-checks.html`)
   - **CRITICAL**: Jekyll's kramdown markdown processor does NOT apply baseurl to absolute paths in markdown links
   - Relative paths work correctly: `adoption/org-health-checks.html` resolves to `/Salesforce-RAG/rag/adoption/org-health-checks.html`
   - Absolute paths like `/rag/...` will NOT work - they become `/rag/...` without baseurl
3. **Baseurl Handling**: All internal links must work with `baseurl: /Salesforce-RAG`
4. **File Extensions**: Convert `.md` to `.html` in all links
5. **Anchor Format**: Section anchors use lowercase with hyphens (e.g., `#architecture-patterns`, `#adoption`, `#api-reference`)
   - Anchors are generated from section names: "Architecture Patterns" → `#architecture-patterns`
   - All section headings in rag-index.md automatically get anchor IDs
   - Homepage category cards link to these anchors (e.g., `{{ '/rag/rag-index.html' | relative_url }}#adoption`)

## Content Rules

### Jekyll Frontmatter Requirement

**CRITICAL RULE**: **ALL markdown files in `rag/` MUST have Jekyll frontmatter or Jekyll will NOT generate HTML pages.**

1. **Required Frontmatter**: Every `.md` file in `rag/` must start with frontmatter:
   ```yaml
   ---
   layout: default
   title: Page Title
   description: Page description for SEO
   permalink: /rag/path/to/page.html
   ---
   ```

2. **Why It's Required**: 
   - Without frontmatter, Jekyll treats the file as plain markdown and does NOT convert it to HTML
   - Links to files without frontmatter will return 404 errors
   - Frontmatter tells Jekyll to process the file and where to generate the HTML

3. **Permalink Format**: 
   - Must match the file path: `rag/development/lwc-patterns.md` → `permalink: /rag/development/lwc-patterns.html`
   - Always use `.html` extension (Jekyll converts `.md` to `.html`)

4. **When Adding New Files**:
   - **ALWAYS** add frontmatter immediately when creating a new `.md` file
   - Use this template:
     ```yaml
     ---
     layout: default
     title: Your Page Title
     description: Brief description of the page content
     permalink: /rag/your-folder/your-file.html
     ---
     ```

5. **Validation**: 
   - **ALWAYS run before deploying**: `python website/scripts/validate-frontmatter.py`
   - This checks ALL markdown files in `rag/` for proper frontmatter
   - Files without frontmatter will cause 404 errors when linked
   - The validation script will list all files missing frontmatter

6. **Automated Checking**:
   - The `update-rag-and-website.sh` script should validate frontmatter
   - CI/CD pipeline should fail if files are missing frontmatter
   - **Never deploy without validating frontmatter first**

**This is a hard requirement - files without frontmatter will NOT work on the website.**

### Descriptions

1. **Exact Match**: Homepage descriptions must exactly match `rag-index.md` section descriptions
2. **Auto-Sync**: Use `sync-homepage.py` to ensure they match
3. **No Manual Edits**: Don't manually edit homepage descriptions - they'll be overwritten

### Navigation

1. **Complete Index**: The `rag-index.md` must include ALL domains
2. **All Domains Visible**: Homepage must show cards for ALL major domains (script ensures this)
3. **No Hidden Content**: If it's in the index, it should be accessible from homepage

## File Organization Rules

### Website Files

1. **All in `website/` folder**: All website-related files must be in `website/` folder
2. **Root Files**: Files that must be in repo root go in `website/root/`
3. **Scripts**: All scripts go in `website/scripts/`
4. **Documentation**: All website docs go in `website/docs/`

### Git Tracking

1. **Only `rag/` and `website/`**: Only these two directories are tracked
2. **No Exceptions**: All other directories are excluded via `.gitignore`

## Link Structure Rules

### In rag-index.md

1. **Bullet List Items**: These are the clickable links
   - Format: `- <a href="{{ '/rag/path/file.html' | relative_url }}">filename.md</a> — Description`
   - These MUST be clickable and work
   - Generated automatically by `sync-homepage.py`
2. **Subsection Headers**: These are metadata (not links)
   - Format: `### filename.md`
   - These provide additional information about the file

### Internal Links

1. **HTML Links with Jekyll Filters Required**: Use **HTML links with `relative_url` filter** in markdown files
   - **CRITICAL**: Jekyll's kramdown does NOT apply baseurl to markdown links (neither absolute nor relative)
   - ✅ Correct: `<a href="{{ '/rag/adoption/org-health-checks.html' | relative_url }}">text</a>` (HTML with filter)
   - ❌ Wrong: `[text](adoption/org-health-checks.html)` (markdown link - won't work with baseurl)
   - ❌ Wrong: `[text](/rag/adoption/org-health-checks.html)` (markdown absolute - won't work)
   - **Solution**: All internal links must use HTML format with Jekyll's `relative_url` filter
2. **Correct Path Resolution**: When converting relative paths to absolute paths, ensure correct resolution:
   - ✅ Correct: `user-readiness.html` (same dir) → `/rag/adoption/user-readiness.html`
   - ✅ Correct: `../development/governor-limits-and-optimization.html` → `/rag/development/governor-limits-and-optimization.html`
   - ✅ Correct: `../observability/performance-tuning.html` → `/rag/observability/performance-tuning.html`
   - ❌ Wrong: `/rag/adoption/adoption/user-readiness.html` (duplicate directory)
   - ❌ Wrong: `/rag/adoption/observability/performance-tuning.html` (wrong - should be `/rag/observability/`)
   - ❌ Wrong: `/rag/adoption/development/governor-limits-and-optimization.html` (wrong - should be `/rag/development/`)
   - **Path Resolution Rules**:
     - Same directory: `file.html` → `/rag/{current_dir}/file.html`
     - Parent directory: `../other-dir/file.html` → `/rag/other-dir/file.html` (go up from current_dir first)
     - Subdirectory: `subdir/file.html` → `/rag/{current_dir}/subdir/file.html`
3. **HTML Extension**: Always use `.html` extension (not `.md`)
4. **Baseurl Handling**: Jekyll's `relative_url` filter automatically applies baseurl to absolute paths starting with `/`
5. **Anchor Links**: Use lowercase with hyphens for section anchors (e.g., `#adoption`, `#architecture-patterns`)
   - Section "Architecture Patterns" → anchor `#architecture-patterns`
   - Section "API Reference" → anchor `#api-reference`
   - Section "Code Examples" → anchor `#code-examples`

## Link Formatting Rules

### In rag-index.md

1. **HTML Links with Jekyll Filters Required**: All links must use **HTML format with `relative_url` filter**
   - ✅ Correct: `<a href="{{ '/rag/adoption/org-health-checks.html' | relative_url }}">org-health-checks.md</a>`
   - ✅ Correct: `<a href="{{ '/rag/api-reference/apex-api-reference.html' | relative_url }}">apex-api-reference.md</a>`
   - ❌ Wrong: `[text](adoption/org-health-checks.html)` (markdown link - baseurl not applied)
   - ❌ Wrong: `[text](/rag/adoption/org-health-checks.html)` (markdown absolute - baseurl not applied)
   - **Why**: Jekyll's kramdown markdown processor does NOT apply baseurl to any markdown links
2. **HTML Extension**: Always use `.html` extension (Jekyll converts `.md` to `.html`)
3. **Anchor Links**: Section headings automatically get anchor IDs
   - Format: Section name → lowercase with hyphens
   - Example: "Architecture Patterns" → `#architecture-patterns`
   - Example: "API Reference" → `#api-reference`
   - Example: "Code Examples" → `#code-examples`

### In Homepage (index.md)

1. **Jekyll Filters**: Use `{{ '/path' | relative_url }}` for all links
2. **Anchor Links**: Link to sections using format: `{{ '/rag/rag-index.html' | relative_url }}#section-name`
   - Example: `{{ '/rag/rag-index.html' | relative_url }}#adoption`
   - Example: `{{ '/rag/rag-index.html' | relative_url }}#architecture-patterns`

### In Navigation (default.html layout)

1. **Jekyll Filters**: Use `{{ '/path' | relative_url }}` for all links
2. **Consistent Navigation**: All pages use the same navigation from the default layout

## Deployment Rules

### GitHub Actions

1. **Automatic Deployment**: Changes to `rag/` or `website/` trigger deployment
2. **Build Process**: 
   - Copy `website/root/*` to repo root
   - Copy `website/_layouts/` and `website/assets/` to root
   - Run Jekyll build
   - Deploy to GitHub Pages
3. **Link Resolution**: 
   - Absolute paths starting with `/` are automatically resolved with baseurl via `relative_url` filter
   - Example: `{{ '/rag/adoption/org-health-checks.html' | relative_url }}` → `/Salesforce-RAG/rag/adoption/org-health-checks.html`
   - **Path Validation**: Use `fix-incorrect-paths.py` to find and fix incorrect paths:
     - Duplicate directories: `/rag/adoption/adoption/` → `/rag/adoption/`
     - Wrong parent paths: `/rag/adoption/observability/` → `/rag/observability/`
     - Wrong parent paths: `/rag/adoption/development/` → `/rag/development/`

### Testing Before Deploy

1. **Validate Frontmatter**: `python website/scripts/validate-frontmatter.py`
   - **CRITICAL**: This must pass before deploying
   - All markdown files must have proper Jekyll frontmatter
   - Files without frontmatter will cause 404 errors
2. **Run Sync Script**: `python website/scripts/sync-homepage.py`
3. **Link Validation**: `python website/scripts/validate-comprehensive-links.py`
   - Verify all links work
   - Check for broken links
4. **Description Match**: Verify homepage matches index (script does this)
5. **All Categories**: Verify all domains have homepage cards (script does this)
6. **Mobile Check**: Verify mobile responsiveness

## Link Path Resolution Rules

### Common Path Errors to Avoid

1. **Duplicate Directories**: 
   - ❌ Wrong: `/rag/adoption/adoption/user-readiness.html`
   - ✅ Correct: `/rag/adoption/user-readiness.html`
   - **Cause**: Script incorrectly resolved same-directory links

2. **Wrong Parent Directory Resolution**:
   - ❌ Wrong: `/rag/adoption/observability/performance-tuning.html` (from `adoption/` folder)
   - ✅ Correct: `/rag/observability/performance-tuning.html`
   - **Cause**: Script didn't properly go up directories with `../`

3. **Incorrect Relative Path Handling**:
   - From `rag/adoption/org-health-checks.md`:
     - `user-readiness.html` → `/rag/adoption/user-readiness.html` ✅
     - `../development/governor-limits-and-optimization.html` → `/rag/development/governor-limits-and-optimization.html` ✅
     - `../observability/performance-tuning.html` → `/rag/observability/performance-tuning.html` ✅

### Fixing Incorrect Paths

1. **Run fix-incorrect-paths.py**: Automatically fixes common path errors
   ```bash
   python website/scripts/fix-incorrect-paths.py
   ```

2. **Manual Verification**: Check for patterns:
   - `/rag/([^/]+)/\1/` - duplicate directories
   - `/rag/adoption/observability/` - wrong parent path
   - `/rag/adoption/development/` - wrong parent path

3. **Path Resolution Logic**:
   - Same directory: `file.html` → `/rag/{current_dir}/file.html`
   - Parent directory (`../`): Go up from current_dir, then append remaining path
   - Subdirectory: Append to current_dir path

## Comprehensive Link Validation

### Overview

The comprehensive link validation system reviews **ALL links** across the entire codebase, including:
- Internal HTML links (with relative_url filter)
- Internal markdown links (legacy)
- External links (http/https)
- Anchor links
- Mailto links

### Link Validation Workflow

1. **Discover All Links**:
   ```bash
   python website/scripts/discover-all-links.py
   ```
   - Scans all markdown files
   - Categorizes links by type
   - Outputs: `website/docs/link-discovery.json`

2. **Validate All Links**:
   ```bash
   python website/scripts/validate-comprehensive-links.py
   ```
   - Validates file existence
   - Checks format correctness
   - Verifies path accuracy
   - Outputs: `website/docs/link-validation.json`

3. **Generate Reports**:
   ```bash
   python website/scripts/generate-link-report.py
   ```
   - Generates Markdown report: `website/docs/link-validation-report.md`
   - Generates JSON report: `website/docs/link-validation-report.json`
   - Generates CSV report: `website/docs/link-validation-report.csv`

4. **Fix Issues** (optional):
   ```bash
   python website/scripts/fix-comprehensive-links.py --dry-run  # Preview fixes
   python website/scripts/fix-comprehensive-links.py --apply    # Apply fixes
   ```

### Validation Checks

The comprehensive validator checks:

1. **Internal HTML Links**:
   - Path starts with `/rag/`
   - Target file exists (converts `.html` to `.md`)
   - Path correctness (not in wrong subdirectory)
   - Format: `{{ '/rag/path/file.html' | relative_url }}`
   - No duplicate directory patterns

2. **Internal Markdown Links**:
   - Target file exists
   - Extension warnings (.md should be .html)
   - Relative path resolution
   - Flagged for conversion to HTML format

3. **External Links**:
   - Suspicious patterns (localhost, test domains)
   - Note: Actual URL checking is optional (can be slow)

4. **Anchor Links**:
   - Target file exists
   - Anchor ID exists in target file
   - Format validation (lowercase with hyphens)

5. **File Existence**:
   - All internal links verified
   - Relative paths resolved correctly
   - Case sensitivity checked

6. **Path Correctness**:
   - Files in correct directories
   - No duplicate directory paths
   - Correct parent directory resolution

7. **Duplicate Links**:
   - Same URL with different text
   - Multiple links to same file from same source

### CI/CD Integration

Link validation runs automatically on:
- Every push to `main` branch
- Every pull request
- Manual trigger via `workflow_dispatch`

The workflow:
1. Discovers all links
2. Validates all links
3. Generates reports
4. Uploads reports as artifacts
5. Comments on PRs with validation results
6. Fails build on critical errors

### Troubleshooting Common Link Issues

**Issue: Links not working on a page**
- **Cause**: Missing Jekyll frontmatter
- **Fix**: Add frontmatter to markdown file:
  ```yaml
  ---
  layout: default
  title: Page Title
  permalink: /rag/path/to/page.html
  ---
  ```

**Issue: Links resolve to wrong path (missing baseurl)**
- **Cause**: Using markdown links instead of HTML with relative_url filter
- **Fix**: Convert to HTML format: `<a href="{{ '/rag/path/file.html' | relative_url }}">text</a>`

**Issue: Links point to wrong directory**
- **Cause**: Incorrect relative path resolution
- **Fix**: Use absolute paths starting with `/rag/` in HTML links

**Issue: Duplicate directory in path**
- **Cause**: Script incorrectly resolved relative paths
- **Fix**: Run `fix-comprehensive-links.py` to auto-fix

## Maintenance Rules

### When Adding New Domain

1. **Create the folder** in `rag/` (e.g., `rag/my-new-domain/`)
2. **Add at least ONE .md file** to the folder (empty folders don't get cards)
3. **Add folder mapping** to `FOLDER_TO_SECTION` in `website/scripts/sync-homepage.py`:
   ```python
   "my-new-domain": "My New Domain",
   ```
4. **Add emoji** to `EMOJI_MAP` in the same file:
   ```python
   "My New Domain": "🎯",
   ```
5. **Run**: `python website/scripts/sync-homepage.py` (or `website/scripts/update-rag-and-website.sh`)
6. The script will:
   - Automatically detect the new domain (because it has files)
   - Add it to `rag-index.md`
   - Add it to `rag-library.json`
   - **Create a new homepage card** (because folder has files)
7. Commit changes:
   ```bash
   git add rag/rag-index.md rag/rag-library.json website/root/index.md website/scripts/sync-homepage.py
   git commit -m "Add new domain: [domain-name]"
   git push
   ```
8. Done!

**Important**: The folder MUST have at least one .md file to get a homepage card. Empty folders are ignored.

### When Updating Descriptions

1. Update descriptions in your RAG files
2. **Run**: `python website/scripts/sync-homepage.py`
3. The script will:
   - Extract updated descriptions from files
   - Update `rag-index.md` with new descriptions
   - Update `rag-library.json` with new summaries
   - Update homepage to match
4. Commit changes:
   ```bash
   git add rag/rag-index.md rag/rag-library.json website/root/index.md
   git commit -m "Update descriptions"
   git push
   ```
5. Done!

**Never manually edit homepage categories - always use the sync script!**

## Quality Checklist

Before every deployment:

- [ ] **CRITICAL: Validate Frontmatter**: `python website/scripts/validate-frontmatter.py`
  - All markdown files must have proper Jekyll frontmatter
  - This MUST pass before deploying
  - Files without frontmatter will cause 404 errors
- [ ] Run `python website/scripts/sync-homepage.py` (or `website/scripts/update-rag-and-website.sh`)
- [ ] **Validate Links**: `python website/scripts/validate-comprehensive-links.py`
  - Check for broken links
  - Verify all internal links work
- [ ] Verify `rag-index.md` is up to date
- [ ] Verify `rag-library.json` is up to date with correct file counts
- [ ] Verify homepage categories match `rag-index.md`
- [ ] All links use `relative_url` filter
- [ ] All links work (test anchor links)
- [ ] Mobile responsive layout works
- [ ] No broken links
- [ ] SEO meta tags present
- [ ] Sitemap updated

## Violations

If you find:
- Homepage descriptions that don't match index → **Run sync script**
- Missing homepage cards for domains → **Run sync script**
- Broken links → Fix immediately
- Inconsistent formatting → **Run sync script**

## Questions?

**Just run the script:**
```bash
python website/scripts/sync-homepage.py
```

That's it. No manual work needed.

---

## Critical Reference: Lessons Learned

**⚠️ IMPORTANT:** Before making any changes to the website infrastructure, **always read**:

📚 **[LESSONS-LEARNED.md](LESSONS-LEARNED.md)** - Critical lessons from the website rebuild, including:
- Directory creation before file writing
- Gemfile placement in GitHub Actions
- GitHub Pages gem conflicts
- Link validation best practices
- Workflow structure and ordering
- Common pitfalls to avoid

This document contains hard-won knowledge from debugging deployment issues. **Reference it first** when encountering problems or making infrastructure changes.

