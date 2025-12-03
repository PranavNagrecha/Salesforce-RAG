# Website Setup Guide

This guide explains how to set up your Salesforce RAG Knowledge Library as an SEO-optimized website on GitHub Pages.

## What Was Added

### 1. Jekyll Configuration (`_config.yml`)
- Configured for GitHub Pages
- Enabled SEO plugins (jekyll-seo-tag, jekyll-sitemap, jekyll-feed)
- Set up proper URL structure
- Configured collections for RAG content

### 2. SEO Optimizations

#### Meta Tags
- Open Graph tags for social media sharing
- Twitter Card tags
- Proper meta descriptions and keywords
- Author information

#### Structured Data (JSON-LD)
- WebSite schema for better search engine understanding
- TechArticle schema for content pages
- SearchAction schema for search functionality

#### Sitemap & Robots
- `sitemap.xml` for search engine indexing
- `robots.txt` to guide crawlers
- Auto-generated sitemap via jekyll-sitemap plugin

### 3. Website Structure
- `index.md` - SEO-optimized homepage with navigation
- `_layouts/default.html` - Responsive layout template
- `assets/css/main.css` - Custom styling
- Navigation header and footer

## Setup Steps

### 1. Enable GitHub Pages

1. Go to your repository on GitHub
2. Navigate to **Settings** → **Pages**
3. Under **Source**, select **Deploy from a branch**
4. Choose **main** branch and **/ (root)** folder
5. Click **Save**

GitHub Pages will automatically build your site using Jekyll.

### 2. Verify Repository Name

Make sure your repository is named exactly `Salesforce-RAG` (case-sensitive). If it's different, update the `baseurl` in `_config.yml`:

```yaml
baseurl: /Your-Repository-Name
```

### 3. Wait for Build

GitHub Pages typically takes 1-2 minutes to build. You can check the build status in:
- **Settings** → **Pages** → **Build and deployment**
- Or check the Actions tab for build logs

### 4. Access Your Site

Once built, your site will be available at:
```
https://pranavnagrecha.github.io/Salesforce-RAG/
```

## SEO Best Practices Implemented

### ✅ On-Page SEO
- Semantic HTML structure
- Proper heading hierarchy (H1, H2, H3)
- Meta descriptions for all pages
- Alt text placeholders for images
- Internal linking structure

### ✅ Technical SEO
- Mobile-responsive design
- Fast loading (static site)
- Clean URL structure
- XML sitemap
- Robots.txt configuration

### ✅ Content SEO
- Keyword-rich content
- Structured data markup
- Social media optimization
- Breadcrumb navigation (can be added)

## Additional SEO Improvements You Can Make

### 1. Add Google Analytics

Add your Google Analytics tracking code to `_layouts/default.html`:

```html
<!-- Google Analytics -->
<script async src="https://www.googletagmanager.com/gtag/js?id=GA_MEASUREMENT_ID"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'GA_MEASUREMENT_ID');
</script>
```

### 2. Submit to Google Search Console

1. Go to [Google Search Console](https://search.google.com/search-console)
2. Add your property: `https://pranavnagrecha.github.io/Salesforce-RAG/`
3. Verify ownership (GitHub Pages provides verification)
4. Submit your sitemap: `https://pranavnagrecha.github.io/Salesforce-RAG/sitemap.xml`

### 3. Add More Structured Data

Consider adding:
- **BreadcrumbList** schema for navigation
- **Article** schema for individual knowledge files
- **CollectionPage** schema for category pages

### 4. Optimize Images

- Add images with descriptive filenames
- Include alt text for all images
- Use WebP format for better compression
- Add image sitemap if you have many images

### 5. Improve Internal Linking

- Add "Related Articles" sections
- Create topic hub pages
- Add breadcrumb navigation
- Link related content within articles

### 6. Add Social Sharing Buttons

Consider adding share buttons for:
- Twitter
- LinkedIn
- Reddit
- Hacker News

### 7. Create a Blog/News Section

Regularly updated content helps with SEO:
- Add a "What's New" section
- Create release notes
- Write about new patterns discovered

## Testing Your SEO

### Tools to Use

1. **Google PageSpeed Insights**
   - Test mobile and desktop performance
   - Get optimization suggestions

2. **Google Rich Results Test**
   - Validate structured data
   - Check if rich snippets will appear

3. **Schema Markup Validator**
   - Validate JSON-LD structured data

4. **Mobile-Friendly Test**
   - Ensure mobile responsiveness

5. **Lighthouse (Chrome DevTools)**
   - Performance audit
   - SEO audit
   - Accessibility audit

## Monitoring

### Track Your Rankings

1. Set up Google Search Console
2. Monitor search performance
3. Track which keywords bring traffic
4. Monitor click-through rates

### Analytics

Track:
- Page views
- Bounce rate
- Time on page
- Popular content
- Traffic sources

## Troubleshooting

### Site Not Building

1. Check GitHub Actions for build errors
2. Verify `_config.yml` syntax
3. Check for Jekyll plugin compatibility
4. Review build logs in Settings → Pages

### Pages Not Indexing

1. Verify sitemap is accessible
2. Submit sitemap to Google Search Console
3. Check robots.txt isn't blocking pages
4. Ensure pages have proper meta tags

### SEO Issues

1. Run Lighthouse audit
2. Check structured data validity
3. Verify mobile responsiveness
4. Test page load speed

## Next Steps

1. **Commit and Push** all the new files
2. **Wait for GitHub Pages** to build (1-2 minutes)
3. **Test the site** at your GitHub Pages URL
4. **Submit to Google Search Console**
5. **Share on social media** to get initial traffic
6. **Monitor and optimize** based on analytics

## Resources

- [GitHub Pages Documentation](https://docs.github.com/en/pages)
- [Jekyll Documentation](https://jekyllrb.com/docs/)
- [Google Search Central](https://developers.google.com/search)
- [Schema.org Documentation](https://schema.org/)

---

**Note**: It may take a few days to weeks for Google to fully index your site. Be patient and continue creating quality content!

