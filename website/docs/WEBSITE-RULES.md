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
git add rag/rag-index.md rag/rag-library.json website/root/index.md sitemap.xml
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

1. **Auto-Sync Only**: Use `sync-homepage.py` to update homepage - don't manually edit
2. **Must Match Index**: Homepage card descriptions MUST exactly match `rag-index.md` section descriptions
3. **Complete Coverage**: ALL major domains from `rag-index.md` must have homepage cards (script handles this)
4. **Consistent Formatting**: All cards follow the same structure (script handles this)

### When Adding New Files to rag/

1. Add your .md file to the appropriate folder in `rag/`
2. **Run**: `python website/scripts/sync-homepage.py` (or `website/scripts/update-rag-and-website.sh`)
3. The script will:
   - Find your new file automatically
   - Add it to `rag-index.md`
   - Add it to `rag-library.json` with metadata
   - Update homepage if needed
   - Update statistics and coverage counts
4. Commit changes:
   ```bash
   git add rag/rag-index.md rag/rag-library.json website/root/index.md
   git commit -m "Add new RAG file: [filename]"
   git push
   ```
5. Done!

### Link Rules

1. **Use Jekyll Filters**: Always use `{{ '/path' | relative_url }}` for internal links
2. **Baseurl Handling**: All internal links must work with `baseurl: /Salesforce-RAG`
3. **File Extensions**: Convert `.md` to `.html` in all links
4. **Anchor Format**: Section anchors use lowercase with hyphens (e.g., `#architecture-patterns`)

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

1. **Relative Paths**: Use relative paths within `rag/` directory
2. **HTML Extension**: Always use `.html` extension (not `.md`)
3. **Baseurl Prefix**: Absolute paths starting with `/rag/` need baseurl prefix

## Deployment Rules

### GitHub Actions

1. **Automatic Deployment**: Changes to `rag/` or `website/` trigger deployment
2. **Build Process**: 
   - Copy `website/root/*` to repo root
   - Copy `website/_layouts/` and `website/assets/` to root
   - Run Jekyll build
   - Deploy to GitHub Pages

### Testing Before Deploy

1. **Run Sync Script**: `python website/scripts/sync-homepage.py`
2. **Link Validation**: Verify all links work
3. **Description Match**: Verify homepage matches index (script does this)
4. **All Categories**: Verify all domains have homepage cards (script does this)
5. **Mobile Check**: Verify mobile responsiveness

## Maintenance Rules

### When Adding New Domain

1. Add files to new domain folder in `rag/`
2. **Run**: `python website/scripts/sync-homepage.py` (or `website/scripts/update-rag-and-website.sh`)
3. The script will:
   - Automatically detect the new domain
   - Add it to `rag-index.md`
   - Add it to `rag-library.json`
   - Update homepage with new category card
4. Commit changes:
   ```bash
   git add rag/rag-index.md rag/rag-library.json website/root/index.md
   git commit -m "Add new domain: [domain-name]"
   git push
   ```
5. Done!

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
