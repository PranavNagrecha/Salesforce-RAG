# Website File Structure

## Organization

All website-related files are organized in the `website/` folder for better project structure.

### Folder Structure

```
website/
├── _layouts/          # Jekyll layout templates
│   └── default.html   # Main layout with SEO
├── assets/            # Static assets
│   └── css/
│       └── main.css   # Stylesheet
└── docs/              # Documentation
    ├── WEBSITE-SETUP.md
    ├── QUICK-START-WEBSITE.md
    └── DEPLOYMENT.md
```

### Root Files (Required by Jekyll/GitHub Pages)

These files **must** remain in the repository root:

- `_config.yml` - Jekyll configuration
- `index.md` - Homepage
- `Gemfile` - Ruby dependencies  
- `robots.txt` - SEO crawler instructions
- `sitemap.xml` - SEO sitemap (auto-generated)

### Build Process

During GitHub Actions build:
1. `website/_layouts/` → copied to `_layouts/` (root)
2. `website/assets/` → copied to `assets/` (root)
3. Jekyll builds using root directories
4. Site deploys to GitHub Pages

This allows us to:
- ✅ Organize files in `website/` folder
- ✅ Keep Jekyll requirements in root during build
- ✅ Maintain clean project structure

## File Locations

| File Type | Source Location | Build Location | Notes |
|-----------|----------------|----------------|-------|
| Layouts | `website/_layouts/` | `_layouts/` (root) | Copied during build |
| Assets | `website/assets/` | `assets/` (root) | Copied during build |
| Config | Root | Root | Must stay in root |
| Homepage | Root | Root | Must stay in root |
| Docs | `website/docs/` | Not built | Documentation only |

## Local Development

When testing locally:

```bash
# Copy layouts and assets to root
cp -r website/_layouts _layouts
cp -r website/assets assets

# Build and serve
bundle exec jekyll serve

# Clean up (optional)
rm -rf _layouts assets
```

Or use the automated workflow which handles this.

## Updating Files

### Update Layouts
Edit files in `website/_layouts/` - they'll be copied during build.

### Update Assets
Edit files in `website/assets/` - they'll be copied during build.

### Update Documentation
Edit files in `website/docs/` - these are for reference only.

## Notes

- The GitHub Actions workflow automatically handles copying
- Local testing may require manual copy (or use the workflow)
- All paths in layouts reference `/assets/` (root path after copy)
- Documentation in `website/docs/` is not part of the built site

