# MeowBox SEO Reference

This document captures the SEO implementation, tooling, and checklist for the MeowBox service.

---

## Live Site

- **Canonical domain**: `https://meowbox.dpdns.org`
- **Redirects**: `*.workers.dev` and `www.meowbox.dpdns.org` → 301 to canonical + `X-Robots-Tag: noindex, nofollow`
- **HTTPS**: Enforced everywhere, 1-year HSTS

---

## Sitemap

- **Location**: `https://meowbox.dpdns.org/sitemap.xml`
- **Format**: XML Sitemap 0.9
- **URLs**: 10 (homepage + 9 subpages)
- **`<lastmod>`**: Updated on every deploy (currently `2026-10-30`)
- **`<priority>`**: Homepage 1.0, landing page 0.9, others 0.8

```xml
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url><loc>https://meowbox.dpdns.org/</loc><lastmod>2026-10-30</lastmod><priority>1.0</priority></url>
  <url><loc>https://meowbox.dpdns.org/free-file-sharing</loc><lastmod>2026-10-30</lastmod><priority>0.9</priority></url>
  <url><loc>https://meowbox.dpdns.org/faq</loc><lastmod>2026-10-30</lastmod><priority>0.8</priority></url>
  <url><loc>https://meowbox.dpdns.org/tools</loc><lastmod>2026-10-30</lastmod><priority>0.8</priority></url>
  <url><loc>https://meowbox.dpdns.org/safety</loc><lastmod>2026-10-30</lastmod><priority>0.8</priority></url>
  <url><loc>https://meowbox.dpdns.org/why</loc><lastmod>2026-10-30</lastmod><priority>0.8</priority></url>
  <url><loc>https://meowbox.dpdns.org/legal</loc><lastmod>2026-10-30</lastmod><priority>0.8</priority></url>
  <url><loc>https://meowbox.dpdns.org/contact</loc><lastmod>2026-10-30</lastmod><priority>0.8</priority></url>
  <url><loc>https://meowbox.dpdns.org/login</loc><lastmod>2026-10-30</lastmod><priority>0.6</priority></url>
  <url><loc>https://meowbox.dpdns.org/register</loc><lastmod>2026-10-30</lastmod><priority>0.6</priority></url>
</urlset>
```

**Submission**: Google Search Console (manual), Bing Webmaster Tools (manual), IndexNow (automatic on deploy).

---

## IndexNow

- **Key**: `299acade1dc86348fa74d883ef20b3bd`
- **Key location**: `https://meowbox.dpdns.org/299acade1dc86348fa74d883ef20b3bd.txt`
- **Endpoint**: `https://api.indexnow.org/indexnow`
- **Trigger**: Automatic on every deploy (all sitemap URLs submitted)
- **Response**: `200 OK` from IndexNow

---

## Robots.txt

```
User-agent: *
Allow: /

Sitemap: https://meowbox.dpdns.org/sitemap.xml
```

- No disallows (all public pages crawlable)
- Host directive omitted (canonical via redirect + sitemap)

---

## JSON-LD Structured Data

| Page | Types |
|------|-------|
| **Homepage** | `Organization`, `WebSite`, `WebApplication`, `SoftwareApplication`, `HowTo` |
| **Free File Sharing** | `BreadcrumbList`, `WebPage`, `FAQPage` |
| **FAQ** | `FAQPage` |
| **Tools** | `WebPage` (with API examples) |
| **Safety** | `WebPage` |
| **Why MeowBox** | `WebPage` |
| **Contact** | `WebPage`, `ContactPage` |
| **Legal** | `WebPage` |

### Key Entities

- **Organization**: `MeowBox` (`alternateName`: ["MeowBox Free", "MeowBox File Sharing"], logo, image, email, sameAs: GitHub repo/profile)
- **WebSite**: `MeowBox` (alternateNames: "MeowBox Free", "MeowBox File Sharing", "MeowBox File Hosting", ...)
- **HowTo**: "How to share a file with MeowBox Free in 3 steps" (3 steps, 1 min)
- **FAQPage**: 4 Q&A on `/free-file-sharing`

---

## Meta Tags (Per Page)

| Page | Title (≤ 60 chars) | Description (≤ 160 chars) |
|------|-------------------|---------------------------|
| `/` | MeowBox Free File Sharing — Direct Links, No Ads | MeowBox Free: no-ads file sharing and hosting with direct links. Upload up to 25 MB, no signup, permanent or expiring links, albums and a simple API. |
| `/free-file-sharing` | MeowBox Free File Sharing — Upload & Share Direct Links | MeowBox Free is free file sharing and hosting with direct links. Upload up to 25 MB, no signup, no ads, permanent or expiring links, albums and a simple API. |
| `/faq` | FAQ — MeowBox Free File Sharing | Answers to common questions about MeowBox Free: limits, accounts, API, security, and how to upload. |
| `/tools` | Tools & API — MeowBox Free File Sharing | MeowBox API reference, curl examples, limits, and file-type rules for developers. |
| `/safety` | Safety & Security — MeowBox Free | How MeowBox keeps uploads safe: malware scanning, banned types, rate limits, and privacy. |
| `/why` | Why MeowBox — Free File Sharing & Hosting | Why choose MeowBox: no ads, no signup, direct links, permanent or expiring, albums, API. |
| `/contact` | Contact — MeowBox Free | Get in touch with the MeowBox team for support, abuse reports, or business inquiries. |
| `/legal` | Legal & Privacy — MeowBox Free | Terms of service, privacy policy, DMCA, and acceptable use for MeowBox Free. |
| `/login` | Login — MeowBox Free | Log in to your MeowBox Free account to manage files, albums, and expiries. |
| `/register` | Register — MeowBox Free | Create a free MeowBox Free account for dashboard, albums, and file deletion. |

All pages include:
- `theme-color`, `apple-mobile-web-app-capable`
- `canonical` URL
- Open Graph (`og:title`, `og:description`, `og:type=website`, `og:image=/banner.webp`)
- Twitter Card (`summary_large_image`)
- `msapplication-*` tiles (via `/browserconfig.xml`)
- Favicon set: 96, 192, 512 px

---

## Browserconfig.xml

Location: `https://meowbox.dpdns.org/browserconfig.xml`  
Provides Windows tile images and theme color for pinned sites.

---

## Security.txt

Location: `https://meowbox.dpdns.org/.well-known/security.txt`

```
Contact: mailto:meowboxteam@gmail.com
Contact: https://github.com/BhagattJii/meowbox/security/advisories/new
Expires: 2027-12-31T00:00:00.000Z
Preferred-Languages: en
Canonical: https://meowbox.dpdns.org/security.txt
Policy: https://meowbox.dpdns.org/legal
```

---

## Canonical & Redirect Strategy

| Source | Target | Code | Headers |
|--------|--------|------|---------|
| `*.workers.dev/*` | `https://meowbox.dpdns.org/*` | 301 | `X-Robots-Tag: noindex, nofollow` |
| `www.meowbox.dpdns.org/*` | `https://meowbox.dpdns.org/*` | 301 | `X-Robots-Tag: noindex, nofollow` |
| `/contact.html` | `/contact` | 301 (via HTMLPAGE map) | — |
| `/free-file-sharing.html` | `/free-file-sharing` | 301 | — |
| Other legacy `.html` | Pretty URL | 301 | — |

All redirects include `Cache-Control: public, max-age=3600`.

---

## Internal Linking

- **Footer** on every page: Home, Free File Sharing, FAQ, Tools, Safety, Why MeowBox, Contact, Legal
- **Header linkrow** (homepage): Login, Register, FAQ, Free File Sharing, Tools, Safety, Why MeowBox, Legal, Contact
- **BreadcrumbList** on `/free-file-sharing`
- **Sitemap link** in footer

---

## Content Keywords (Target)

| Primary | Secondary |
|---------|-----------|
| "MeowBox Free" | "free file sharing" |
| "MeowBox Free file sharing" | "no-ads file hosting" |
| "direct link file upload" | "anonymous file upload" |
| "permanent file links" | "expiring file links" |

---

## Monitoring Checklist (Post-Deploy)

- [ ] Sitemap returns 200, valid XML, 10 URLs
- [ ] IndexNow returns 200 for all URLs
- [ ] `robots.txt` returns 200, correct sitemap line
- [ ] `browserconfig.xml` returns 200, `application/xml`
- [ ] `security.txt` returns 200, `text/plain`
- [ ] Homepage JSON-LD validates (Google Rich Results Test)
- [ ] `/free-file-sharing` JSON-LD validates (FAQPage + BreadcrumbList)
- [ ] Redirects: `curl -I https://www.meowbox.dpdns.org/` → 301 + `X-Robots-Tag: noindex, nofollow`
- [ ] Search Console: submit sitemap, request indexing for `/`, `/free-file-sharing`, `/faq`, `/tools`, `/safety`, `/why`
- [ ] Bing Webmaster: submit sitemap, URL removal for `https://www.meowboxx.workers.dev/*`, request indexing

---

## Brand Protection

- **Trademark**: "MeowBox" — monitor for confusingly similar domains
- **Impersonation**: `meowboxx.workers.dev` (old worker) → redirected + noindex
- **Sitelinks**: Target 3–5 sitelinks (FAQ, Tools, Free File Sharing, Safety, Why) via clear structure + Search Console

---

## Competitor Landscape (SEO Context)

| Competitor | Domain Authority | Notes |
|------------|------------------|-------|
| `meowbox.com` | High | Cat subscription box — different intent, but brand collision on "meowbox" |
| `wetransfer.com` | Very High | Paid tiers, 2 GB free |
| `file.io` | Medium | Ephemeral links, no permanent |
| `gofile.io` | Medium | Free, but ads/trackers |

**Strategy**: Own "MeowBox Free file sharing" long-tail; differentiate on *no ads, no signup, permanent links, malware scan*.

---

## Future SEO Tasks

- [ ] Add `WebPage` `dateModified` to all pages
- [ ] Implement `Article` schema for blog/content pages (when added)
- [ ] Add `VideoObject` schema for demo video (when created)
- [ ] Submit to Google News / Discover (not applicable yet)
- [ ] Build backlinks: GitHub profile, README, relevant forums, tech directories
- [ ] Monitor `site:meowbox.dpdns.org` indexation weekly