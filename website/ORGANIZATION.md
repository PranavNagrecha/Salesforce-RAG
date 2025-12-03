# Website Files Organization

All website-related files have been organized into the `website/` folder.

## What Was Moved

### ✅ Moved to `website/` folder:
- `_layouts/` → `website/_layouts/`
- `assets/` → `website/assets/`
- `WEBSITE-SETUP.md` → `website/docs/WEBSITE-SETUP.md`
- `QUICK-START-WEBSITE.md` → `website/docs/QUICK-START-WEBSITE.md`
- `DEPLOYMENT.md` → `website/docs/DEPLOYMENT.md`

### ✅ Stay in Root (Required by Jekyll/GitHub Pages):
- `_config.yml` - Jekyll configuration
- `index.md` - Homepage
- `Gemfile` - Ruby dependencies
- `robots.txt` - SEO crawler instructions
- `sitemap.xml` - SEO sitemap (auto-generated)

## Current Structure

```
.
├── _config.yml          # Jekyll config (must be in root)
├── index.md             # Homepage (must be in root)
├── Gemfile              # Dependencies (must be in root)
├── robots.txt           # SEO (must be in root)
├── sitemap.xml          # SEO (must be in root)
│
└── website/             # All website files organized here
    ├── _layouts/        # Jekyll layouts
    │   └── default.html
    ├── assets/          # Static assets
    │   └── css/
    │       └── main.css
    ├── docs/            # Documentation
    │   ├── WEBSITE-SETUP.md
    │   ├── QUICK-START-WEBSITE.md
    │   └── DEPLOYMENT.md
    ├── README.md        # Website folder documentation
    └── STRUCTURE.md    # File structure explanation
```

## How It Works

1. **Development**: Edit files in `website/` folder
2. **Build**: GitHub Actions copies `website/_layouts/` and `website/assets/` to root
3. **Deploy**: Jekyll builds using root directories
4. **Result**: Clean organization + working Jekyll site

## Benefits

✅ **Better Organization**: All website files in one place  
✅ **Clean Root**: Only essential files in root  
✅ **Jekyll Compatible**: Build process handles copying  
✅ **Easy Updates**: Edit in `website/` folder  

## Quick Reference

- **Edit layouts**: `website/_layouts/default.html`
- **Edit styles**: `website/assets/css/main.css`
- **Read docs**: `website/docs/`
- **Update site**: Run `./scripts/update-rag-and-website.sh`

