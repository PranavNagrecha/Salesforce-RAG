# Website Files

This folder contains all website-related files for the Salesforce RAG Knowledge Library.

## Structure

```
website/
├── _layouts/          # Jekyll layout templates
│   └── default.html    # Main layout with SEO meta tags
├── assets/             # Static assets (CSS, images, etc.)
│   └── css/
│       └── main.css    # Main stylesheet
└── docs/               # Website documentation
    ├── WEBSITE-SETUP.md
    ├── QUICK-START-WEBSITE.md
    └── DEPLOYMENT.md
```

## Important Notes

### Jekyll Requirements

For GitHub Pages to work properly, Jekyll expects certain files in the repository root:

**Must be in root:**
- `_config.yml` - Jekyll configuration
- `index.md` - Homepage
- `Gemfile` - Ruby dependencies
- `robots.txt` - SEO crawler instructions
- `sitemap.xml` - SEO sitemap

**Can be organized:**
- `_layouts/` - Can be in root or website/_layouts (with config)
- `assets/` - Can be in root or website/assets (with config)

### Current Setup

Currently, layouts and assets are in the `website/` folder for organization, but they are referenced with the full path (`/website/assets/...`) in the layout files.

If you encounter build issues, you may need to:
1. Move `_layouts/` and `assets/` to root, OR
2. Use symlinks, OR
3. Update the GitHub Actions workflow to copy them during build

## Files

### Layouts (`_layouts/`)

- **default.html**: Main page layout with:
  - SEO meta tags (Open Graph, Twitter Cards)
  - Structured data (JSON-LD)
  - Navigation header
  - Footer
  - Responsive design

### Assets (`assets/`)

- **css/main.css**: Main stylesheet with:
  - Responsive design
  - Color scheme
  - Typography
  - Component styles

### Documentation (`docs/`)

- **WEBSITE-SETUP.md**: Complete setup guide
- **QUICK-START-WEBSITE.md**: Quick reference for getting started
- **DEPLOYMENT.md**: Deployment and maintenance guide

## Updating the Website

When you update RAG content, run:

```bash
# Update website files (sitemap, etc.)
./scripts/update-rag-and-website.sh

# Or manually
python3 scripts/update-website.py
```

This will:
1. Scan all RAG markdown files
2. Generate/update `sitemap.xml`
3. Validate file structure
4. Prepare for deployment

## Deployment

See `docs/DEPLOYMENT.md` for complete deployment instructions.

The website automatically deploys via GitHub Actions when you push to `main` branch.

## Troubleshooting

If the site doesn't build:

1. **Check GitHub Actions**: Look for build errors
2. **Verify paths**: Ensure asset paths in layouts are correct
3. **Test locally**: Run `bundle exec jekyll serve`
4. **Check _config.yml**: Verify all paths are correct

For more help, see `docs/DEPLOYMENT.md`.

