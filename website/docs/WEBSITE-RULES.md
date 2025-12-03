# Website Rules and Guidelines

This document defines the rules and standards for maintaining the Salesforce RAG Knowledge Library website.

## General Principles

1. **Consistency First**: All content must be consistent across homepage, index pages, and individual pages
2. **User Experience**: Navigation should be intuitive and all links must work
3. **SEO Optimization**: All pages must have proper meta tags, descriptions, and structured data
4. **Accessibility**: Follow WCAG 2.1 AA standards for accessibility
5. **Mobile Responsive**: All layouts must work on mobile, tablet, and desktop

## Homepage Rules

### Category Cards

1. **Must Match Index**: Homepage card descriptions MUST exactly match the section descriptions in `rag/rag-index.md`
2. **Complete Coverage**: ALL major domains from `rag-index.md` must have homepage cards
3. **Consistent Formatting**: All cards must follow the same structure:
   ```html
   <div class="domain-card">
     <h3><a href="{{ '/rag/rag-index.html' | relative_url }}#section-id">🏗️ Section Name</a></h3>
     <p>Exact description from rag-index.md</p>
   </div>
   ```
4. **Anchor Links**: All cards must link to the corresponding section in `rag-index.html` using proper anchor IDs

### Link Rules

1. **Use Jekyll Filters**: Always use `{{ '/path' | relative_url }}` for internal links
2. **Baseurl Handling**: All internal links must work with `baseurl: /Salesforce-RAG`
3. **File Extensions**: Convert `.md` to `.html` in all links
4. **Anchor Format**: Section anchors use lowercase with hyphens (e.g., `#architecture-patterns`)

## Content Rules

### Descriptions

1. **Exact Match**: Homepage descriptions must exactly match `rag-index.md` section descriptions
2. **No Summaries**: Don't create summaries - use the exact text from the index
3. **Consistency Check**: Before deploying, verify all descriptions match

### Navigation

1. **Complete Index**: The `rag-index.md` must include ALL domains
2. **All Domains Visible**: Homepage must show cards for ALL major domains
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

1. **Link Validation**: Verify all links work
2. **Description Match**: Verify homepage matches index
3. **All Categories**: Verify all domains have homepage cards
4. **Mobile Check**: Verify mobile responsiveness

## Maintenance Rules

### When Adding New Domain

1. Add section to `rag/rag-index.md`
2. Add homepage card to `website/root/index.md`
3. Ensure description matches exactly
4. Test link works
5. Deploy

### When Updating Descriptions

1. Update `rag/rag-index.md` first
2. Then update `website/root/index.md` to match
3. Never update one without the other
4. Always verify they match before committing

## Quality Checklist

Before every deployment, verify:

- [ ] All homepage card descriptions match `rag-index.md` exactly
- [ ] All domains from index have homepage cards
- [ ] All links use `relative_url` filter
- [ ] All links work (test anchor links)
- [ ] Mobile responsive layout works
- [ ] No broken links
- [ ] SEO meta tags present
- [ ] Sitemap updated

## Violations

If you find:
- Homepage descriptions that don't match index → Update homepage to match
- Missing homepage cards for domains → Add cards
- Broken links → Fix immediately
- Inconsistent formatting → Standardize

## Questions?

If unsure about any rule:
1. Check this document first
2. Check `website/docs/` for additional guidance
3. Follow the principle: "Match the index, keep it simple, make it work"

