# Website Files Organization

All website-related files are now organized under the `website/` folder.

## Structure

```
website/
├── _layouts/          # Jekyll layout templates
│   └── default.html
├── assets/            # CSS, JS, images
│   └── css/
│       └── main.css
├── root/              # Files that must be in repo root during build
│   ├── _config.yml   # Jekyll configuration
│   ├── index.md      # Homepage
│   ├── Gemfile       # Ruby dependencies
│   ├── robots.txt    # SEO crawler instructions
│   ├── sitemap.xml   # SEO sitemap (auto-generated)
│   └── README.md     # Documentation for root files
└── docs/              # Website documentation
    ├── WEBSITE-SETUP.md
    ├── QUICK-START-WEBSITE.md
    └── DEPLOYMENT.md
```

## Root Files

Files in `website/root/` are automatically copied to the repository root during GitHub Actions build. This is because Jekyll requires these files in the actual root directory.

**Note:** For local Jekyll development, you may need to copy these files to root manually, or they will be copied automatically during the GitHub Actions build.

## How It Works

1. **Development**: Edit files in `website/` folder
2. **Build**: GitHub Actions copies:
   - `website/_layouts/` → `_layouts/`
   - `website/assets/` → `assets/`
   - `website/root/*` → repository root
3. **Deploy**: Jekyll builds using root directories
4. **Result**: Clean organization + working Jekyll site

## Benefits

✅ **Better Organization**: All website files in one place  
✅ **Clean Root**: No website files in repository root  
✅ **Jekyll Compatible**: Build process handles copying automatically  
✅ **Easy Updates**: Edit in `website/` folder  

## Quick Reference

- **Edit layouts**: `website/_layouts/default.html`
- **Edit styles**: `website/assets/css/main.css`
- **Edit homepage**: `website/root/index.md`
- **Edit config**: `website/root/_config.yml`
- **Read docs**: `website/docs/`
- **Update site**: Run `./scripts/update-rag-and-website.sh`
