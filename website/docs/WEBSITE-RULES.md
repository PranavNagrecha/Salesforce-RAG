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

1. Add your .md file to the appropriate folder in `rag/`
2. **Run**: `python website/scripts/sync-homepage.py` (or `website/scripts/update-rag-and-website.sh`)
3. The script will:
   - Find your new file automatically
   - Add it to `rag-index.md`
   - Add it to `rag-library.json` with metadata
   - **If this is the FIRST file in a folder**: Create a new homepage card for that folder
   - **If folder already had files**: Update existing card
   - Update statistics and coverage counts
4. Commit changes:
   ```bash
   git add rag/rag-index.md rag/rag-library.json website/root/index.md
   git commit -m "Add new RAG file: [filename]"
   git push
   ```
5. Done!

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
   - Format: `- [filename.md](path/file.html) — Description`
   - These MUST be clickable and work
2. **Subsection Headers**: These are metadata (not links)
   - Format: `### filename.md`
   - These provide additional information about the file

### Internal Links

1. **Relative Paths Required**: Use **relative paths** in markdown files (e.g., `adoption/org-health-checks.html`)
   - **IMPORTANT**: Jekyll's kramdown does NOT apply baseurl to absolute paths in markdown links
   - ✅ Correct: `adoption/org-health-checks.html` (relative path)
   - ✅ Correct: `../project-methods/delivery-framework.html` (relative with parent)
   - ❌ Wrong: `/rag/adoption/org-health-checks.html` (absolute path - won't work with baseurl)
   - ❌ Wrong: `rag/adoption/org-health-checks.html` (absolute path without leading / - still wrong)
2. **HTML Extension**: Always use `.html` extension (not `.md`)
3. **Baseurl Handling**: Jekyll automatically resolves relative paths with baseurl correctly
4. **Anchor Links**: Use lowercase with hyphens for section anchors (e.g., `#adoption`, `#architecture-patterns`)
   - Section "Architecture Patterns" → anchor `#architecture-patterns`
   - Section "API Reference" → anchor `#api-reference`
   - Section "Code Examples" → anchor `#code-examples`

## Link Formatting Rules

### In rag-index.md

1. **Relative Paths Required**: All links must use **relative paths** (rag-index.md is in rag/ folder)
   - ✅ Correct: `adoption/org-health-checks.html` (relative from rag-index.md location)
   - ✅ Correct: `api-reference/apex-api-reference.html` (relative path)
   - ❌ Wrong: `/rag/adoption/org-health-checks.html` (absolute path - kramdown doesn't apply baseurl)
   - ❌ Wrong: `rag/adoption/org-health-checks.html` (absolute path without leading /)
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
   - Absolute paths starting with `/` are automatically resolved with baseurl
   - Example: `/rag/adoption/org-health-checks.html` → `/Salesforce-RAG/rag/adoption/org-health-checks.html`

### Testing Before Deploy

1. **Run Sync Script**: `python website/scripts/sync-homepage.py`
2. **Link Validation**: Verify all links work
3. **Description Match**: Verify homepage matches index (script does this)
4. **All Categories**: Verify all domains have homepage cards (script does this)
5. **Mobile Check**: Verify mobile responsiveness

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

- [ ] Run `python website/scripts/sync-homepage.py` (or `website/scripts/update-rag-and-website.sh`)
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

