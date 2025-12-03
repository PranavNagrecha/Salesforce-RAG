# Website Root Files

This folder contains Jekyll configuration files that must be in the repository root during build.

## Files

- `_config.yml` - Jekyll configuration
- `index.md` - Homepage
- `Gemfile` - Ruby dependencies
- `robots.txt` - SEO crawler instructions
- `sitemap.xml` - SEO sitemap (auto-generated)

## How It Works

During GitHub Actions build:
1. Files from `website/root/` are copied to repository root
2. Jekyll builds using root files
3. Site deploys to GitHub Pages

## Editing

Edit files in this folder. They will be automatically copied to root during deployment.

## Note

These files are kept in `website/root/` for organization, but Jekyll requires them in the actual repository root during build. The GitHub Actions workflow handles the copying automatically.

